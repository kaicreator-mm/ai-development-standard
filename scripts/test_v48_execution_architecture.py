from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Candidate:
    ready: bool = True
    authority_current: bool | None = True
    profile_matches: bool | None = True
    infrastructure_matches: bool | None = True
    availability: str = "AVAILABLE"
    security_authorized: bool | None = True
    independence_ok: bool | None = True
    write_set_compatible: bool | None = True
    evidence_policy_satisfied: bool | None = True
    composite_admission_available: bool | None = True
    rank: int = 0


def resolve_eligibility(candidate: Candidate) -> str:
    """Deterministic tri-state hard-filter oracle; ranking is intentionally absent."""
    predicates = (
        candidate.ready,
        candidate.authority_current,
        candidate.profile_matches,
        candidate.infrastructure_matches,
        candidate.security_authorized,
        candidate.independence_ok,
        candidate.write_set_compatible,
        candidate.evidence_policy_satisfied,
        candidate.composite_admission_available,
    )
    if any(value is False for value in predicates):
        return "INELIGIBLE"
    if any(value is None for value in predicates):
        return "UNKNOWN"
    if candidate.availability == "UNAVAILABLE":
        return "INELIGIBLE"
    if candidate.availability != "AVAILABLE":
        return "UNKNOWN"
    return "ELIGIBLE"


def rank_eligible(candidates: list[Candidate]) -> list[Candidate]:
    eligible = [candidate for candidate in candidates if resolve_eligibility(candidate) == "ELIGIBLE"]
    return sorted(eligible, key=lambda candidate: candidate.rank)


@dataclass(frozen=True)
class AdmissionState:
    generation: int = 0
    claims: frozenset[str] = frozenset()
    # (resource_group, work_key) -> units; tuple form keeps the state immutable/deterministic.
    bindings: tuple[tuple[str, str, int], ...] = ()
    # (work_key, ((resource_group, units), ...)); ambiguity remains scoped to the affected set.
    ambiguous: tuple[tuple[str, tuple[tuple[str, int], ...]], ...] = ()

    def used(self, resource_group: str) -> int:
        return sum(units for group, _work, units in self.bindings if group == resource_group)

    def ambiguous_resources_for(self, work_key: str) -> tuple[tuple[str, int], ...] | None:
        for ambiguous_work, resources in self.ambiguous:
            if ambiguous_work == work_key:
                return resources
        return None

    def has_ambiguous_overlap(self, required: dict[str, int]) -> bool:
        requested_groups = set(required)
        return any(
            not requested_groups.isdisjoint(group for group, _units in resources)
            for _work_key, resources in self.ambiguous
        )


def admit(
    state: AdmissionState,
    *,
    work_key: str,
    expected_generation: int,
    required: dict[str, int],
    capacities: dict[str, int],
    composite_primitive: str = "SINGLE_WRITER_ADMISSION",
    inject_publication_ambiguity: bool = False,
) -> tuple[str, AdmissionState]:
    """Reference reducer for one all-or-none claim+resource admission decision."""
    if state.ambiguous_resources_for(work_key) is not None or state.has_ambiguous_overlap(required):
        return "BLOCKED_RECONCILE_REQUIRED", state
    if expected_generation != state.generation:
        return "STALE", state
    if work_key in state.claims:
        return "DUPLICATE", state
    if composite_primitive not in {"SINGLE_WRITER_ADMISSION", "LINEARIZABLE_COMPOSITE_CONDITIONAL_WRITE"}:
        return "BLOCKED_UNSAFE_COMPOSITE_ADMISSION", state
    if any(group not in capacities or units <= 0 for group, units in required.items()):
        return "BLOCKED_RESOURCE_FACT_UNKNOWN", state
    if any(state.used(group) + units > capacities[group] for group, units in required.items()):
        return "CAPACITY_EXCEEDED", state

    # Ambiguity publishes no accepted partial claim/binding. Track the affected resource set so
    # distinct work cannot consume overlapping capacity until durable reconciliation resolves A.
    if inject_publication_ambiguity:
        return "AMBIGUOUS_RECONCILE_REQUIRED", replace(
            state,
            ambiguous=state.ambiguous + ((work_key, tuple(sorted(required.items()))),),
        )

    new_bindings = state.bindings + tuple(
        (group, work_key, units) for group, units in sorted(required.items())
    )
    return "ACCEPTED", AdmissionState(
        generation=state.generation + 1,
        claims=state.claims | {work_key},
        bindings=new_bindings,
        ambiguous=state.ambiguous,
    )


def reconcile_no_accept(state: AdmissionState, *, work_key: str) -> AdmissionState:
    """Durable reconciliation proves that no accepted claim/binding exists for work_key."""
    if work_key in state.claims or any(work == work_key for _group, work, _units in state.bindings):
        raise AssertionError("cannot clear ambiguity while durable accepted binding exists")
    return replace(
        state,
        ambiguous=tuple(entry for entry in state.ambiguous if entry[0] != work_key),
    )


def reconcile_accept(
    state: AdmissionState,
    *,
    work_key: str,
    capacities: dict[str, int],
) -> AdmissionState:
    """Reconstruct an already-durable accepted claim/binding from its ambiguous affected set."""
    required = state.ambiguous_resources_for(work_key)
    if required is None:
        raise AssertionError("cannot reconstruct accepted admission without ambiguity record")
    if work_key in state.claims or any(work == work_key for _group, work, _units in state.bindings):
        raise AssertionError("accepted admission already reconstructed")
    if any(group not in capacities or units <= 0 for group, units in required):
        raise AssertionError("durable accepted reconciliation requires known resource facts")
    if any(state.used(group) + units > capacities[group] for group, units in required):
        raise AssertionError("durable accepted reconciliation would violate capacity")

    new_bindings = state.bindings + tuple(
        (group, work_key, units) for group, units in required
    )
    return AdmissionState(
        generation=state.generation + 1,
        claims=state.claims | {work_key},
        bindings=new_bindings,
        ambiguous=tuple(entry for entry in state.ambiguous if entry[0] != work_key),
    )


class V48ExecutionArchitecture(unittest.TestCase):
    def standard(self) -> str:
        return (ROOT / "standards/EXECUTION_ARCHITECTURE_STANDARD.md").read_text(encoding="utf-8")

    def test_normative_contract_tokens(self) -> None:
        text = self.standard()
        for token in (
            "READY, Dispatch, and Claim remain canonical",
            "ELIGIBLE\nINELIGIBLE\nUNKNOWN",
            "All hard predicates are evaluated before ranking",
            "Only `ELIGIBLE` choices may enter optional ranking",
            "all required resource bindings MUST linearize all-or-none at one admission point",
            "Independent per-key CAS operations",
            "sum(active accepted units bound to G) <= N",
            "replacement admission for the affected claim/resource set is blocked",
            "no second scheduler/state database, durable Availability owner, or new Exchange family",
        ):
            self.assertIn(token, text)

    def test_hard_filters_precede_ranking_and_tri_state(self) -> None:
        fast_but_ineligible = Candidate(independence_ok=False, rank=0)
        cheap_but_unknown = Candidate(availability="UNKNOWN", rank=1)
        eligible = Candidate(rank=50)
        self.assertEqual("INELIGIBLE", resolve_eligibility(fast_but_ineligible))
        self.assertEqual("UNKNOWN", resolve_eligibility(cheap_but_unknown))
        self.assertEqual("ELIGIBLE", resolve_eligibility(eligible))
        self.assertEqual([eligible], rank_eligible([fast_but_ineligible, cheap_but_unknown, eligible]))

        self.assertEqual("UNKNOWN", resolve_eligibility(Candidate(authority_current=None)))
        self.assertEqual("INELIGIBLE", resolve_eligibility(Candidate(security_authorized=False)))
        self.assertEqual("INELIGIBLE", resolve_eligibility(Candidate(ready=False)))

    def test_capacity_one_and_capacity_n_never_overallocate(self) -> None:
        state = AdmissionState()
        result, state = admit(
            state,
            work_key="A",
            expected_generation=0,
            required={"exclusive": 1, "pool": 2},
            capacities={"exclusive": 1, "pool": 3},
        )
        self.assertEqual("ACCEPTED", result)
        self.assertEqual(1, state.used("exclusive"))
        self.assertEqual(2, state.used("pool"))

        before = state
        result, state = admit(
            state,
            work_key="B",
            expected_generation=1,
            required={"exclusive": 1},
            capacities={"exclusive": 1, "pool": 3},
        )
        self.assertEqual("CAPACITY_EXCEEDED", result)
        self.assertEqual(before, state)

        result, state = admit(
            state,
            work_key="C",
            expected_generation=1,
            required={"pool": 1},
            capacities={"exclusive": 1, "pool": 3},
        )
        self.assertEqual("ACCEPTED", result)
        self.assertEqual(3, state.used("pool"))

        before = state
        result, state = admit(
            state,
            work_key="D",
            expected_generation=2,
            required={"pool": 1},
            capacities={"exclusive": 1, "pool": 3},
        )
        self.assertEqual("CAPACITY_EXCEEDED", result)
        self.assertEqual(before, state)

    def test_multi_resource_admission_is_all_or_none(self) -> None:
        initial = AdmissionState()
        result, after = admit(
            initial,
            work_key="A",
            expected_generation=0,
            required={"gpu": 1, "license": 1},
            capacities={"gpu": 2, "license": 0},
        )
        self.assertEqual("CAPACITY_EXCEEDED", result)
        self.assertEqual(initial, after)
        self.assertNotIn("A", after.claims)
        self.assertEqual(0, after.used("gpu"))

        result, after = admit(
            initial,
            work_key="A",
            expected_generation=0,
            required={"gpu": 1, "license": 1},
            capacities={"gpu": 2, "license": 1},
        )
        self.assertEqual("ACCEPTED", result)
        self.assertIn("A", after.claims)
        self.assertEqual(1, after.used("gpu"))
        self.assertEqual(1, after.used("license"))

        unsafe_result, unsafe_state = admit(
            initial,
            work_key="unsafe",
            expected_generation=0,
            required={"gpu": 1},
            capacities={"gpu": 1},
            composite_primitive="INDEPENDENT_PER_KEY_CAS",
        )
        self.assertEqual("BLOCKED_UNSAFE_COMPOSITE_ADMISSION", unsafe_result)
        self.assertEqual(initial, unsafe_state)

    def test_publication_ambiguity_reconciles_before_replacement(self) -> None:
        initial = AdmissionState()
        result, ambiguous = admit(
            initial,
            work_key="A",
            expected_generation=0,
            required={"pool": 1},
            capacities={"pool": 1},
            inject_publication_ambiguity=True,
        )
        self.assertEqual("AMBIGUOUS_RECONCILE_REQUIRED", result)
        self.assertEqual((("pool", 1),), ambiguous.ambiguous_resources_for("A"))
        self.assertNotIn("A", ambiguous.claims)
        self.assertEqual(0, ambiguous.used("pool"))

        blocked_same, unchanged = admit(
            ambiguous,
            work_key="A",
            expected_generation=0,
            required={"pool": 1},
            capacities={"pool": 1},
        )
        self.assertEqual("BLOCKED_RECONCILE_REQUIRED", blocked_same)
        self.assertEqual(ambiguous, unchanged)

        blocked_overlap, unchanged = admit(
            ambiguous,
            work_key="B",
            expected_generation=0,
            required={"pool": 1},
            capacities={"pool": 1},
        )
        self.assertEqual("BLOCKED_RECONCILE_REQUIRED", blocked_overlap)
        self.assertEqual(ambiguous, unchanged)
        self.assertNotIn("B", unchanged.claims)

        non_overlap, non_overlap_state = admit(
            ambiguous,
            work_key="C",
            expected_generation=0,
            required={"other": 1},
            capacities={"pool": 1, "other": 1},
        )
        self.assertEqual("ACCEPTED", non_overlap)
        self.assertEqual(0, non_overlap_state.used("pool"))
        self.assertEqual(1, non_overlap_state.used("other"))

        unknown_resource, unchanged = admit(
            ambiguous,
            work_key="D",
            expected_generation=0,
            required={"unknown": 1},
            capacities={"pool": 1},
        )
        self.assertEqual("BLOCKED_RESOURCE_FACT_UNKNOWN", unknown_resource)
        self.assertEqual(ambiguous, unchanged)

        reconciled = reconcile_no_accept(ambiguous, work_key="A")
        accepted_b, final = admit(
            reconciled,
            work_key="B",
            expected_generation=0,
            required={"pool": 1},
            capacities={"pool": 1},
        )
        self.assertEqual("ACCEPTED", accepted_b)
        self.assertIn("B", final.claims)
        self.assertEqual(1, final.used("pool"))

        durable_accepted = reconcile_accept(
            ambiguous,
            work_key="A",
            capacities={"pool": 1},
        )
        self.assertIn("A", durable_accepted.claims)
        self.assertEqual(1, durable_accepted.used("pool"))
        blocked_capacity, unchanged = admit(
            durable_accepted,
            work_key="B",
            expected_generation=1,
            required={"pool": 1},
            capacities={"pool": 1},
        )
        self.assertEqual("CAPACITY_EXCEEDED", blocked_capacity)
        self.assertEqual(durable_accepted, unchanged)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(V48ExecutionArchitecture)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
