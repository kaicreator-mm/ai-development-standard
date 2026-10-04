from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Callable
import unittest

ELIGIBLE = "ELIGIBLE"
INELIGIBLE = "INELIGIBLE"
UNKNOWN = "UNKNOWN"

SAFE_ADMISSION_MODES = {
    "SINGLE_WRITER_ADMISSION",
    "LINEARIZABLE_CONDITIONAL_WRITE",
}


@dataclass(frozen=True)
class WorkRequirement:
    work_key: str
    ready: bool = True
    authority_current: bool | None = True
    required_capabilities: frozenset[str] = frozenset()
    security_authorized: bool | None = True
    write_set_compatible: bool | None = True
    evidence_policy_satisfied: bool | None = True
    composite_admission_available: bool | None = True


@dataclass(frozen=True)
class AgentProfile:
    agent_id: str
    capabilities: frozenset[str]


@dataclass(frozen=True)
class AvailabilityFact:
    state: str
    current: bool | None


@dataclass(frozen=True)
class Candidate:
    work: WorkRequirement
    profile: AgentProfile
    availability: AvailabilityFact | None
    independence_ok: bool | None = True
    rank: tuple[int, int, int, int] = (0, 0, 0, 0)


def resolve_eligibility(candidate: Candidate) -> str:
    """Derive tri-state eligibility from explicit hard facts only."""
    work = candidate.work

    known_hard_predicates = (
        work.ready,
        work.authority_current,
        work.security_authorized,
        work.write_set_compatible,
        work.evidence_policy_satisfied,
        work.composite_admission_available,
        candidate.independence_ok,
    )
    if any(value is False for value in known_hard_predicates):
        return INELIGIBLE
    if any(value is None for value in known_hard_predicates):
        return UNKNOWN

    if not work.required_capabilities.issubset(candidate.profile.capabilities):
        return INELIGIBLE

    availability = candidate.availability
    if availability is None or availability.current is not True:
        return UNKNOWN
    if availability.state == "UNAVAILABLE":
        return INELIGIBLE
    if availability.state != "AVAILABLE":
        return UNKNOWN
    return ELIGIBLE


def rank_eligible(
    candidates: list[Candidate],
    *,
    ranking_probe: Callable[[Candidate], tuple[int, int, int, int]] | None = None,
) -> list[Candidate]:
    """Hard-filter first; ranking is invoked only for ELIGIBLE candidates."""
    eligible = [candidate for candidate in candidates if resolve_eligibility(candidate) == ELIGIBLE]
    key = ranking_probe if ranking_probe is not None else (lambda candidate: candidate.rank)
    return sorted(eligible, key=key)


@dataclass(frozen=True)
class AdmissionState:
    generation: int = 0
    claims: frozenset[str] = frozenset()
    bindings: tuple[tuple[str, str, int], ...] = ()
    compatibility_bindings: tuple[tuple[str, str], ...] = ()
    ambiguous: tuple[tuple[str, tuple[tuple[str, int], ...], tuple[str, ...]], ...] = ()

    def used(self, resource_group: str) -> int:
        return sum(
            units
            for group, _work_key, units in self.bindings
            if group == resource_group
        )

    def ambiguity_for(
        self, work_key: str
    ) -> tuple[tuple[tuple[str, int], ...], tuple[str, ...]] | None:
        for ambiguous_work, resources, compatibility in self.ambiguous:
            if ambiguous_work == work_key:
                return resources, compatibility
        return None

    def ambiguous_overlap(
        self,
        required: dict[str, int],
        compatibility: frozenset[str],
    ) -> bool:
        requested_groups = set(required)
        for _work_key, resources, existing_compatibility in self.ambiguous:
            if not requested_groups.isdisjoint(group for group, _units in resources):
                return True
            if not compatibility.isdisjoint(existing_compatibility):
                return True
        return False


def _accepted_all_or_none(
    state: AdmissionState,
    *,
    work_key: str,
    required: dict[str, int],
    compatibility: frozenset[str],
) -> AdmissionState:
    new_bindings = state.bindings + tuple(
        (group, work_key, units) for group, units in sorted(required.items())
    )
    new_compatibility = state.compatibility_bindings + tuple(
        (key, work_key) for key in sorted(compatibility)
    )
    return AdmissionState(
        generation=state.generation + 1,
        claims=state.claims | {work_key},
        bindings=new_bindings,
        compatibility_bindings=new_compatibility,
        ambiguous=state.ambiguous,
    )


def admit(
    state: AdmissionState,
    *,
    work_key: str,
    expected_generation: int,
    required: dict[str, int],
    capacities: dict[str, int],
    compatibility: frozenset[str] = frozenset(),
    admission_mode: str = "SINGLE_WRITER_ADMISSION",
    failure_point: str | None = None,
) -> tuple[str, AdmissionState]:
    """One logical commit boundary for work claim + every required binding."""
    if state.ambiguity_for(work_key) is not None or state.ambiguous_overlap(required, compatibility):
        return "BLOCKED_RECONCILE_REQUIRED", state
    if expected_generation != state.generation:
        return "STALE", state
    if work_key in state.claims:
        return "DUPLICATE", state
    if admission_mode not in SAFE_ADMISSION_MODES:
        return "BLOCKED_UNSAFE_COMPOSITE_ADMISSION", state
    if any(group not in capacities or units <= 0 for group, units in required.items()):
        return "BLOCKED_RESOURCE_FACT_UNKNOWN", state
    if any(state.used(group) + units > capacities[group] for group, units in required.items()):
        return "CAPACITY_EXCEEDED", state
    if any(key == existing_key for key in compatibility for existing_key, _work in state.compatibility_bindings):
        return "COMPATIBILITY_CONFLICT", state

    protected_resources = tuple(sorted(required.items()))
    protected_compatibility = tuple(sorted(compatibility))

    if failure_point == "BEFORE_PUBLICATION":
        return "REJECTED_BEFORE_PUBLICATION", state
    if failure_point == "AT_PUBLICATION":
        return "AMBIGUOUS_RECONCILE_REQUIRED", replace(
            state,
            ambiguous=state.ambiguous + ((work_key, protected_resources, protected_compatibility),),
        )

    accepted = _accepted_all_or_none(
        state,
        work_key=work_key,
        required=required,
        compatibility=compatibility,
    )
    if failure_point == "AFTER_PUBLICATION":
        return "AMBIGUOUS_RECONCILE_REQUIRED", replace(
            accepted,
            ambiguous=accepted.ambiguous + ((work_key, protected_resources, protected_compatibility),),
        )
    return "ACCEPTED", accepted


def reconcile_no_accept(state: AdmissionState, *, work_key: str) -> AdmissionState:
    if work_key in state.claims or any(work == work_key for _group, work, _units in state.bindings):
        raise AssertionError("durable accepted admission exists; cannot reconcile as no-accept")
    return replace(
        state,
        ambiguous=tuple(entry for entry in state.ambiguous if entry[0] != work_key),
    )


def reconcile_accepted(state: AdmissionState, *, work_key: str) -> AdmissionState:
    ambiguity = state.ambiguity_for(work_key)
    if ambiguity is None:
        raise AssertionError("no ambiguous admission exists")
    resources, compatibility = ambiguity
    if work_key not in state.claims:
        raise AssertionError("accepted reconciliation requires durable work claim")
    if any((group, work_key, units) not in state.bindings for group, units in resources):
        raise AssertionError("accepted reconciliation requires every durable resource binding")
    if any((key, work_key) not in state.compatibility_bindings for key in compatibility):
        raise AssertionError("accepted reconciliation requires every durable compatibility binding")
    return replace(
        state,
        ambiguous=tuple(entry for entry in state.ambiguous if entry[0] != work_key),
    )


class V48SchedulingConformance(unittest.TestCase):
    def test_multiple_ready_heterogeneous_profiles_are_deterministic(self) -> None:
        python_work = WorkRequirement(
            work_key="python-task",
            required_capabilities=frozenset({"python"}),
        )
        android_work = WorkRequirement(
            work_key="android-task",
            required_capabilities=frozenset({"android"}),
        )
        python_agent = AgentProfile("python-agent", frozenset({"python"}))
        android_agent = AgentProfile("android-agent", frozenset({"android", "python"}))
        fresh = AvailabilityFact("AVAILABLE", current=True)

        choices = [
            Candidate(python_work, python_agent, fresh),
            Candidate(android_work, python_agent, fresh),
            Candidate(android_work, android_agent, fresh),
        ]
        outcomes = [resolve_eligibility(choice) for choice in choices]
        self.assertEqual([ELIGIBLE, INELIGIBLE, ELIGIBLE], outcomes)
        self.assertEqual(outcomes, [resolve_eligibility(choice) for choice in choices])

    def test_stale_and_missing_availability_fail_closed_unknown(self) -> None:
        work = WorkRequirement("A")
        agent = AgentProfile("agent", frozenset())
        self.assertEqual(UNKNOWN, resolve_eligibility(Candidate(work, agent, None)))
        self.assertEqual(
            UNKNOWN,
            resolve_eligibility(Candidate(work, agent, AvailabilityFact("AVAILABLE", current=False))),
        )
        self.assertEqual(
            UNKNOWN,
            resolve_eligibility(Candidate(work, agent, AvailabilityFact("UNKNOWN", current=True))),
        )
        self.assertEqual(
            INELIGIBLE,
            resolve_eligibility(Candidate(work, agent, AvailabilityFact("UNAVAILABLE", current=True))),
        )

    def test_independence_conflict_is_a_hard_filter(self) -> None:
        candidate = Candidate(
            WorkRequirement("review-sensitive"),
            AgentProfile("builder-who-cannot-review", frozenset()),
            AvailabilityFact("AVAILABLE", current=True),
            independence_ok=False,
            rank=(-9999, -9999, -9999, -9999),
        )
        self.assertEqual(INELIGIBLE, resolve_eligibility(candidate))
        self.assertEqual([], rank_eligible([candidate]))

    def test_all_bound_hard_predicates_fail_closed(self) -> None:
        agent = AgentProfile("agent", frozenset({"python"}))
        fresh = AvailabilityFact("AVAILABLE", current=True)
        cases = (
            (WorkRequirement("authority-unknown", authority_current=None), UNKNOWN),
            (WorkRequirement("write-set-conflict", write_set_compatible=False), INELIGIBLE),
            (WorkRequirement("evidence-unknown", evidence_policy_satisfied=None), UNKNOWN),
            (WorkRequirement("composite-unavailable", composite_admission_available=False), INELIGIBLE),
            (WorkRequirement("capability-mismatch", required_capabilities=frozenset({"android"})), INELIGIBLE),
        )
        for work, expected in cases:
            with self.subTest(work=work.work_key):
                self.assertEqual(expected, resolve_eligibility(Candidate(work, agent, fresh)))

    def test_hard_filter_completes_before_optional_ranking(self) -> None:
        work = WorkRequirement("A")
        agent = AgentProfile("agent", frozenset())
        fresh = AvailabilityFact("AVAILABLE", current=True)
        eligible = Candidate(work, agent, fresh, rank=(50, 50, 50, 50))
        ineligible = Candidate(
            replace(work, work_key="B", security_authorized=False),
            agent,
            fresh,
            rank=(-100, -100, -100, -100),
        )
        unknown = Candidate(
            replace(work, work_key="C"),
            agent,
            AvailabilityFact("AVAILABLE", current=False),
            rank=(-200, -200, -200, -200),
        )
        probed: list[str] = []

        def probe(candidate: Candidate) -> tuple[int, int, int, int]:
            probed.append(candidate.work.work_key)
            if resolve_eligibility(candidate) != ELIGIBLE:
                raise AssertionError("ranking observed a non-eligible candidate")
            return candidate.rank

        ranked = rank_eligible([unknown, ineligible, eligible], ranking_probe=probe)
        self.assertEqual([eligible], ranked)
        self.assertEqual(["A"], probed)

    def test_capacity_n_contention_never_overallocates(self) -> None:
        state = AdmissionState()
        capacities = {"pool": 3}
        result, state = admit(
            state,
            work_key="A",
            expected_generation=0,
            required={"pool": 2},
            capacities=capacities,
        )
        self.assertEqual("ACCEPTED", result)
        result, state = admit(
            state,
            work_key="B",
            expected_generation=1,
            required={"pool": 1},
            capacities=capacities,
        )
        self.assertEqual("ACCEPTED", result)
        self.assertEqual(3, state.used("pool"))

        before = state
        result, state = admit(
            state,
            work_key="C",
            expected_generation=2,
            required={"pool": 1},
            capacities=capacities,
        )
        self.assertEqual("CAPACITY_EXCEEDED", result)
        self.assertEqual(before, state)
        self.assertLessEqual(state.used("pool"), capacities["pool"])

    def test_exclusive_capacity_n1_is_strict(self) -> None:
        state = AdmissionState()
        capacities = {"device": 1}
        result, state = admit(
            state,
            work_key="A",
            expected_generation=0,
            required={"device": 1},
            capacities=capacities,
        )
        self.assertEqual("ACCEPTED", result)
        before = state
        result, state = admit(
            state,
            work_key="B",
            expected_generation=1,
            required={"device": 1},
            capacities=capacities,
        )
        self.assertEqual("CAPACITY_EXCEEDED", result)
        self.assertEqual(before, state)
        self.assertEqual(1, state.used("device"))

    def test_composite_claim_resources_and_compatibility_are_all_or_none(self) -> None:
        initial = AdmissionState()
        capacities = {"gpu": 2, "license": 0}
        result, rejected = admit(
            initial,
            work_key="A",
            expected_generation=0,
            required={"gpu": 1, "license": 1},
            capacities=capacities,
            compatibility=frozenset({"same-host"}),
        )
        self.assertEqual("CAPACITY_EXCEEDED", result)
        self.assertEqual(initial, rejected)
        self.assertNotIn("A", rejected.claims)
        self.assertEqual(0, rejected.used("gpu"))
        self.assertEqual((), rejected.compatibility_bindings)

        result, accepted = admit(
            initial,
            work_key="A",
            expected_generation=0,
            required={"gpu": 1, "license": 1},
            capacities={"gpu": 2, "license": 1},
            compatibility=frozenset({"same-host"}),
        )
        self.assertEqual("ACCEPTED", result)
        self.assertIn("A", accepted.claims)
        self.assertEqual(1, accepted.used("gpu"))
        self.assertEqual(1, accepted.used("license"))
        self.assertIn(("same-host", "A"), accepted.compatibility_bindings)

        before_conflict = accepted
        result, conflict = admit(
            accepted,
            work_key="B",
            expected_generation=1,
            required={"gpu": 1},
            capacities={"gpu": 2, "license": 1},
            compatibility=frozenset({"same-host"}),
        )
        self.assertEqual("COMPATIBILITY_CONFLICT", result)
        self.assertEqual(before_conflict, conflict)

    def test_independent_per_key_cas_is_not_composite_proof(self) -> None:
        initial = AdmissionState()
        for unsafe_mode in ("INDEPENDENT_PER_KEY_CAS", "PER_RESOURCE_LEASES", "SEQUENTIAL_RESERVATIONS"):
            result, state = admit(
                initial,
                work_key=unsafe_mode,
                expected_generation=0,
                required={"pool": 1},
                capacities={"pool": 1},
                admission_mode=unsafe_mode,
            )
            self.assertEqual("BLOCKED_UNSAFE_COMPOSITE_ADMISSION", result)
            self.assertEqual(initial, state)

    def test_failure_injection_is_fail_closed_until_durable_reconciliation(self) -> None:
        initial = AdmissionState()
        capacities = {"pool": 1}

        before_result, before = admit(
            initial,
            work_key="before",
            expected_generation=0,
            required={"pool": 1},
            capacities=capacities,
            failure_point="BEFORE_PUBLICATION",
        )
        self.assertEqual("REJECTED_BEFORE_PUBLICATION", before_result)
        self.assertEqual(initial, before)

        at_result, at = admit(
            initial,
            work_key="A",
            expected_generation=0,
            required={"pool": 1},
            capacities=capacities,
            compatibility=frozenset({"same-host"}),
            failure_point="AT_PUBLICATION",
        )
        self.assertEqual("AMBIGUOUS_RECONCILE_REQUIRED", at_result)
        self.assertNotIn("A", at.claims)
        self.assertEqual(0, at.used("pool"))
        blocked, unchanged = admit(
            at,
            work_key="B",
            expected_generation=0,
            required={"pool": 1},
            capacities=capacities,
        )
        self.assertEqual("BLOCKED_RECONCILE_REQUIRED", blocked)
        self.assertEqual(at, unchanged)
        compatibility_blocked, compatibility_unchanged = admit(
            at,
            work_key="compatibility-overlap",
            expected_generation=0,
            required={"other": 1},
            capacities={"pool": 1, "other": 1},
            compatibility=frozenset({"same-host"}),
        )
        self.assertEqual("BLOCKED_RECONCILE_REQUIRED", compatibility_blocked)
        self.assertEqual(at, compatibility_unchanged)
        cleared = reconcile_no_accept(at, work_key="A")
        accepted, after_clear = admit(
            cleared,
            work_key="B",
            expected_generation=0,
            required={"pool": 1},
            capacities=capacities,
        )
        self.assertEqual("ACCEPTED", accepted)
        self.assertIn("B", after_clear.claims)

        after_result, after = admit(
            initial,
            work_key="C",
            expected_generation=0,
            required={"pool": 1},
            capacities=capacities,
            failure_point="AFTER_PUBLICATION",
        )
        self.assertEqual("AMBIGUOUS_RECONCILE_REQUIRED", after_result)
        self.assertIn("C", after.claims)
        self.assertEqual(1, after.used("pool"))
        blocked, unchanged = admit(
            after,
            work_key="D",
            expected_generation=1,
            required={"pool": 1},
            capacities=capacities,
        )
        self.assertEqual("BLOCKED_RECONCILE_REQUIRED", blocked)
        self.assertEqual(after, unchanged)
        reconciled = reconcile_accepted(after, work_key="C")
        capacity_result, unchanged = admit(
            reconciled,
            work_key="D",
            expected_generation=1,
            required={"pool": 1},
            capacities=capacities,
        )
        self.assertEqual("CAPACITY_EXCEEDED", capacity_result)
        self.assertEqual(reconciled, unchanged)

    def test_oracle_uses_only_existing_owner_and_admission_semantics(self) -> None:
        self.assertEqual(
            {"SINGLE_WRITER_ADMISSION", "LINEARIZABLE_CONDITIONAL_WRITE"},
            SAFE_ADMISSION_MODES,
        )
        state = AdmissionState()
        result, _ = admit(
            state,
            work_key="safe",
            expected_generation=0,
            required={"pool": 1},
            capacities={"pool": 1},
            admission_mode="LINEARIZABLE_CONDITIONAL_WRITE",
        )
        self.assertEqual("ACCEPTED", result)
        blocked, unchanged = admit(
            state,
            work_key="unsupported",
            expected_generation=0,
            required={"pool": 1},
            capacities={"pool": 1},
            admission_mode="NOVEL_DISTRIBUTED_MULTI_KEY_LEASE",
        )
        self.assertEqual("BLOCKED_UNSAFE_COMPOSITE_ADMISSION", blocked)
        self.assertEqual(state, unchanged)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(V48SchedulingConformance)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
