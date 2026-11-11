#!/usr/bin/env python3
"""ADS #1366 R34: bounded source-derived writer-admission interleaving model.

This is a diagnostic model, not a claim that the deployed Host actually ran
both calls concurrently. It models the inspected Tally source shape:
  1. read current task/registry facts (two snapshots, but no shared lock);
  2. reserve with mustBeAbsent on the task-specific protected Claim Key;
  3. publish and persist PUBLISHED_VERIFIED.
Different task keys do not conflict at the per-key CAS layer. The inspected
Host source does not bind Task Pack write sets into this admission request.

The model exhaustively enumerates all 20 order-preserving interleavings of
A:{snapshot,reserve,publish} and B:{snapshot,reserve,publish}. The local
Node24 exact-source experiment remains necessary to confirm runtime behavior.
"""
from __future__ import annotations

import json
import sys
import unittest


def interleavings(a: tuple[str, ...], b: tuple[str, ...]) -> list[tuple[str, ...]]:
    if not a and not b:
        return [()]
    result: list[tuple[str, ...]] = []
    if a:
        result.extend((a[0],) + tail for tail in interleavings(a[1:], b))
    if b:
        result.extend((b[0],) + tail for tail in interleavings(a, b[1:]))
    return result


SCHEDULES = interleavings(("AS", "AR", "AP"), ("BS", "BR", "BP"))


def simulate(
    schedule: tuple[str, ...],
    *,
    same_key: bool = False,
    write_sets_known: bool = False,
    write_sets_overlap: bool = True,
    atomic_write_set_guard: bool = False,
) -> dict[str, bool]:
    registry: dict[str, str] = {}
    blocked = {"A": False, "B": False}
    accepted = {"A": False, "B": False}

    for event in schedule:
        task, operation = event
        key = "shared" if same_key else f"key-{task}"

        if operation == "S":
            # Host source scans all other protected keys. The scan is not
            # atomic with the later per-key CAS reservation.
            other_active = any(existing_key != key for existing_key in registry)
            if other_active:
                blocked[task] = True
            if atomic_write_set_guard and (
                not write_sets_known or write_sets_overlap
            ):
                blocked[task] = True

        elif operation == "R":
            # DomainHarness CAS is linearizable for this physical key only.
            if blocked[task] or key in registry:
                blocked[task] = True
            else:
                registry[key] = "PENDING_GITHUB_PUBLISH"

        elif operation == "P":
            if not blocked[task] and key in registry:
                registry[key] = "PUBLISHED_VERIFIED"
                accepted[task] = True

    return accepted


def simulate_global_lock(order: tuple[str, str]) -> dict[str, bool]:
    """Control: one mutex covers registry snapshot through key reservation."""
    registry: dict[str, str] = {}
    accepted = {"A": False, "B": False}
    for task in order:
        key = f"key-{task}"
        other_active = any(existing_key != key for existing_key in registry)
        if other_active or key in registry:
            continue
        registry[key] = "PENDING_GITHUB_PUBLISH"
        accepted[task] = True
    return accepted


def result() -> dict[str, object]:
    overlapping_unknown = [
        schedule for schedule in SCHEDULES
        if all(simulate(
            schedule,
            same_key=False,
            write_sets_known=False,
            write_sets_overlap=True,
        ).values())
    ]
    same_key_double = [
        schedule for schedule in SCHEDULES
        if all(simulate(
            schedule,
            same_key=True,
            write_sets_known=False,
            write_sets_overlap=True,
        ).values())
    ]
    guarded_double = [
        schedule for schedule in SCHEDULES
        if all(simulate(
            schedule,
            same_key=False,
            write_sets_known=False,
            write_sets_overlap=True,
            atomic_write_set_guard=True,
        ).values())
    ]
    disjoint_double = [
        schedule for schedule in SCHEDULES
        if all(simulate(
            schedule,
            same_key=False,
            write_sets_known=True,
            write_sets_overlap=False,
            atomic_write_set_guard=True,
        ).values())
    ]
    lock_double = []
    for schedule in SCHEDULES:
        order = ("A", "B") if schedule.index("AS") < schedule.index("BS") else ("B", "A")
        if all(simulate_global_lock(order).values()):
            lock_double.append(schedule)

    return {
        "schema": "ads/formal-r34-writer-interleaving-model/v1",
        "scope": "two tasks; three ordered events each; exhaustive 20 interleavings",
        "source_assumptions": {
            "snapshot": "read-only registry snapshot; repeated read detects local drift but is not a global lock",
            "reservation": "mustBeAbsent CAS is scoped to each derived protected Claim Key",
            "different_keys": "per-key CAS does not conflict when task keys differ",
            "write_set_binding": "inspected Host taskAuthority/request has no exact Task Pack write-set field",
            "global_mutex": "no mutex/lease/global CAS key is visible in inspected controller/source",
            "runtime_qualification": "source-derived counterexample only; exact Node24 runtime race remains NOT_RUN",
        },
        "results": {
            "interleavings": len(SCHEDULES),
            "different_keys_overlapping_unknown_write_sets_no_guard": {
                "unsafe_double_accept_schedules": len(overlapping_unknown),
                "witness": list(overlapping_unknown[0]) if overlapping_unknown else None,
            },
            "same_key_per_key_cas": {
                "unsafe_double_accept_schedules": len(same_key_double),
            },
            "global_mutex_snapshot_through_reservation": {
                "unsafe_double_accept_schedules": len(lock_double),
            },
            "atomic_write_set_guard": {
                "unsafe_double_accept_schedules": len(guarded_double),
            },
            "known_disjoint_write_sets": {
                "safe_double_accept_schedules": len(disjoint_double),
            },
        },
    }


class WriterAdmissionInterleavingTests(unittest.TestCase):
    def test_all_order_preserving_interleavings_are_enumerated(self) -> None:
        self.assertEqual(len(SCHEDULES), 20)

    def test_different_keys_can_both_accept_with_overlapping_unknown_write_sets(self) -> None:
        unsafe = [
            schedule for schedule in SCHEDULES
            if all(simulate(schedule).values())
        ]
        self.assertEqual(len(unsafe), 12)
        self.assertEqual(unsafe[0], ("AS", "BS", "AR", "AP", "BR", "BP"))

    def test_same_key_cas_prevents_double_acceptance(self) -> None:
        self.assertFalse(any(
            all(simulate(schedule, same_key=True).values())
            for schedule in SCHEDULES
        ))

    def test_global_mutex_prevents_double_acceptance(self) -> None:
        for schedule in SCHEDULES:
            order = ("A", "B") if schedule.index("AS") < schedule.index("BS") else ("B", "A")
            self.assertFalse(all(simulate_global_lock(order).values()))

    def test_atomic_write_set_guard_blocks_unknown_or_overlapping_sets(self) -> None:
        self.assertFalse(any(
            all(simulate(
                schedule,
                atomic_write_set_guard=True,
                write_sets_known=False,
                write_sets_overlap=True,
            ).values())
            for schedule in SCHEDULES
        ))

    def test_known_disjoint_sets_remain_parallelizable_under_write_set_guard(self) -> None:
        self.assertEqual(sum(
            all(simulate(
                schedule,
                atomic_write_set_guard=True,
                write_sets_known=True,
                write_sets_overlap=False,
            ).values())
            for schedule in SCHEDULES
        ), 12)


if __name__ == "__main__":
    if "--receipt" in sys.argv:
        print(json.dumps(result(), indent=2, sort_keys=True))
    else:
        unittest.main(argv=[sys.argv[0]])
