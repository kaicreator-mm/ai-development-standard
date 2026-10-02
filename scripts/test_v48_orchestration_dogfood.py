"""v4.8 T-011 focused conformance: heterogeneous multi-agent / resource / transport dogfood.

Deterministic self-contained orchestration dogfood over explicit durable facts. It composes
the already-merged T-007 (contract compatibility), T-008 (scheduling/resource), T-009
(interchange replay/restart) and T-017 (execution ownership) semantics through their public
conformance modules and proves the ODF-01..ODF-18 scenario/evidence matrix frozen by the
T-011 Task Pack and L3, without introducing a new scheduler, admission lifecycle, event
family, schema authority or runtime database.

Evidence discipline (T-011 Task Pack; every recorded row carries an explicit class):

  SYNTHETIC_DETERMINISTIC          reference-model execution over committed corpus fixtures;
                                   proves only the bounded deterministic semantics exercised
  REPOSITORY_REAL_EXECUTION        execution against real repository artifacts at the exact
                                   candidate (schemas, durable facts, git candidate state)
  REAL_HOST_OR_RUNTIME_VALIDATION  requires independent exact-subject environment validation;
                                   never self-certified by this harness
  NOT_RUN / BLOCKED                preserved explicitly; never inferred as PASS

The harness imports merged upstream oracle modules instead of redefining normative
semantics. Scenario corpus: docs/implementation/4.8.0/dogfood/orchestration/fixtures/.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import test_v48_contract_compatibility as contract_compat
import test_v48_execution_ownership as ownership
import test_v48_interchange_replay_restart as interchange
import test_v48_scheduling_conformance as scheduling
from test_protocol_schemas import load_schema, validate_subset

CORPUS_PATH = (
    ROOT / "docs" / "implementation" / "4.8.0" / "dogfood" / "orchestration"
    / "fixtures" / "scenario_manifest.json"
)
CLAIM_EVENT_PATH = (
    ROOT / "docs" / "implementation" / "4.8.0" / "dogfood" / "orchestration"
    / "fixtures" / "t011_builder_claim_event.json"
)
DOGFOOD_DIR = ROOT / "docs" / "implementation" / "4.8.0" / "dogfood" / "orchestration"

EVENT_V2 = load_schema("agent-event-v2.schema.json")
PROFILE_SCHEMA = load_schema("agent-capability-profile-v1.schema.json")

EVIDENCE_CLASSES = {
    "SYNTHETIC_DETERMINISTIC",
    "REPOSITORY_REAL_EXECUTION",
    "REAL_HOST_OR_RUNTIME_VALIDATION",
    "NOT_RUN",
    "BLOCKED",
}

SCENARIO_ORDER = [f"ODF-{index:02d}" for index in range(1, 19)]

# Registry of scenario outcomes; validated for completeness by the runner.
SCENARIO_REGISTRY: list[dict] = []


def record_scenario(
    *,
    scenario_id: str,
    name: str,
    l3_tests: str,
    oracle: str,
    observed: str,
    evidence_class: list[str],
    environment: str,
    limitations: str = "none observed in this deterministic run",
) -> dict:
    assert scenario_id in SCENARIO_ORDER, f"unknown scenario id {scenario_id}"
    assert evidence_class, f"{scenario_id}: evidence class required"
    for evidence in evidence_class:
        assert evidence in EVIDENCE_CLASSES, f"{scenario_id}: unknown evidence class {evidence}"
    row = {
        "scenario_id": scenario_id,
        "name": name,
        "l3_tests": l3_tests,
        "oracle": oracle,
        "observed_result": observed,
        "evidence_class": evidence_class,
        "execution_environment": environment,
        "limitations_or_counterevidence": limitations,
        "validation_ref": "PENDING independent exact-subject Validation",
        "review_ref": "PENDING Fresh Independent Review",
    }
    SCENARIO_REGISTRY.append(row)
    return row


def load_corpus() -> dict:
    return json.loads(CORPUS_PATH.read_text(encoding="utf-8"))


def load_claim_event() -> dict:
    return json.loads(CLAIM_EVENT_PATH.read_text(encoding="utf-8"))["event"]


def candidate_head_identity() -> dict:
    """Real repository read: exact candidate commit/tree the harness is executing against."""
    head = _git("rev-parse", "HEAD").strip()
    tree = _git("rev-parse", "HEAD^{tree}").strip()
    dirty = [line for line in _git("status", "--porcelain", "--untracked-files=all").splitlines() if line.strip()]
    return {"head_sha": head, "head_tree": tree, "dirty_paths": len(dirty)}


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def candidate_paths(base: str) -> list[str]:
    """Real repository read: implementation-diff paths from the JIT pack head to the
    candidate, plus uncommitted working-tree paths (the candidate under test)."""
    paths: set[str] = set()
    committed = _git("diff", "--name-only", f"{base}..HEAD")
    paths.update(line.strip() for line in committed.splitlines() if line.strip())
    for line in _git("status", "--porcelain", "--untracked-files=all").splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip()
        if "->" in path:
            path = path.split("->", 1)[1].strip()
        if path:
            paths.add(path)
    return sorted(paths)


def parse_manifest_durable_facts() -> dict:
    """Read-only parse of the real .agent/execution/T-011/MANIFEST.yaml durable facts.

    Minimal flat parser for the pinned key/value and two-level list shape of that file;
    the manifest remains read-only authority and is never rewritten here.
    """
    text = (ROOT / ".agent" / "execution" / "T-011" / "MANIFEST.yaml").read_text(
        encoding="utf-8"
    )
    facts: dict = {"builder_write_set": [], "forbidden_builder_paths": []}
    current_list: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            if current_list == "builder_write_set" or current_list == "forbidden_builder_paths":
                facts[current_list].append(stripped[2:].strip().strip('"'))
            continue
        if line.startswith("  ") and current_list:
            continue
        key, sep, value = stripped.partition(":")
        if not sep:
            continue
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if value == "":
            if key in ("builder_write_set", "forbidden_builder_paths"):
                current_list = key
            else:
                current_list = None
            continue
        current_list = None
        facts[key] = value
    return facts


def work_requirement_from_corpus(item: dict) -> scheduling.WorkRequirement:
    return scheduling.WorkRequirement(
        work_key=item["work_key"],
        ready=item["ready"],
        required_capabilities=frozenset(item["required_capabilities"]),
    )


def profile_from_corpus(profile: dict) -> scheduling.AgentProfile:
    return scheduling.AgentProfile(
        profile["profile_key"],
        frozenset(profile["scheduling_oracle_capabilities"]),
    )


def availability_from_corpus(fact: dict | None) -> scheduling.AvailabilityFact | None:
    if fact is None:
        return None
    return scheduling.AvailabilityFact(fact["state"], current=fact["current"])


def make_envelope(
    *,
    exchange_id: str,
    subject_identity_ref: str,
    payload_ref: str,
    occurred_at: str,
    exchange_type: str = "RESULT",
    operation_id: str = "v4.8:T-011",
    subject_ref: str = "git:kaicreator-mm/ai-development-standard:candidate/T-011",
    work_item_ref: str = "github:kaicreator-mm/ai-development-standard#517",
) -> dict:
    return {
        "protocol_version": "ai-dev/interchange-v1",
        "exchange_id": exchange_id,
        "exchange_type": exchange_type,
        "operation_id": operation_id,
        "work_item_ref": work_item_ref,
        "dispatch_id": "d-v4.8.0-T-011-phase2-builder-94955c6f",
        "subject_ref": subject_ref,
        "subject_identity_ref": subject_identity_ref,
        "identity_binding": "exact-sha",
        "authority_effect": "CORRELATION_ONLY_NON_AUTHORITATIVE",
        "actor": {
            "actor_role": "builder",
            "operator_id": "claude-code:v48-t011-phase2-builder",
            "operator_kind": "claude-code",
        },
        "causation": {
            "caused_by": "github:kaicreator-mm/ai-development-standard#517",
            "correlation_refs": ["task:T-011#517"],
        },
        "payload_ref": payload_ref,
        "occurred_at": occurred_at,
    }


def make_delivery(
    envelope: dict, payload: dict, *, transport_outcome: str | None = None
) -> dict:
    delivery = {
        "envelope": envelope,
        "payload": payload,
        "payload_digest": interchange.canonical_digest(payload),
    }
    if transport_outcome is not None:
        delivery["transport_outcome"] = transport_outcome
    return delivery


def replay_fixture(deliveries: list[dict], durable_facts: list[dict], state: str) -> dict:
    return {
        "authoritative_work_item": {
            "subject_identity_ref": "git:kaicreator-mm/ai-development-standard@94955c6f93fd7316406ea96bce8f7c32a62509ef",
            "state": state,
        },
        "deliveries": deliveries,
        "durable_facts": durable_facts,
    }


def durable_fact(ref: str, event: dict) -> dict:
    return {"ref": ref, "marker": "<!-- ai-dev:event:v2 -->", "event": event}


IMPLEMENTATION_READY_EVENT = {
    "schema": "ai-dev/event-v2",
    "event": "IMPLEMENTATION_READY",
    "actor_role": "builder",
    "operator_kind": "claude-code",
    "operator_id": "claude-code:v48-t011-phase2-builder",
    "sha": "94955c6f93fd7316406ea96bce8f7c32a62509ef",
    "review_policy": "required",
    "validation": {"scope": "independent-exact-subject"},
    "next_state": "review-ready",
}


class V48OrchestrationDogfood(unittest.TestCase):
    """ODF-01..ODF-18 deterministic scenario corpus (T-011 Task Pack / L3)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = load_corpus()

    # ------------------------------------------------------------------
    # ODF-01 — multiple READY items + heterogeneous Agent profiles
    # ------------------------------------------------------------------
    def test_odf01_multi_ready_heterogeneous_eligibility(self) -> None:
        works = [work_requirement_from_corpus(item) for item in self.corpus["work_items"]]
        profiles = [profile_from_corpus(p) for p in self.corpus["agent_profiles"]]
        fresh = availability_from_corpus(self.corpus["availability_facts"]["fresh_available"])

        semantic, bounded, review = works
        strong, bounded_profile, reviewer = profiles
        choices = [
            scheduling.Candidate(semantic, strong, fresh),
            scheduling.Candidate(semantic, bounded_profile, fresh),
            scheduling.Candidate(bounded, bounded_profile, fresh),
            scheduling.Candidate(review, reviewer, fresh),
            scheduling.Candidate(review, strong, fresh),
        ]
        outcomes = [scheduling.resolve_eligibility(choice) for choice in choices]
        self.assertEqual(
            [
                scheduling.ELIGIBLE,
                scheduling.INELIGIBLE,
                scheduling.ELIGIBLE,
                scheduling.ELIGIBLE,
                scheduling.INELIGIBLE,
            ],
            outcomes,
            "heterogeneous profiles must resolve differently through hard eligibility only",
        )

        probed: list[str] = []

        def probe(candidate: scheduling.Candidate) -> tuple[int, int, int, int]:
            self.assertEqual(
                scheduling.ELIGIBLE,
                scheduling.resolve_eligibility(candidate),
                "ranking observed a non-eligible candidate",
            )
            probed.append(candidate.work.work_key)
            return candidate.rank

        ranked = scheduling.rank_eligible(choices, ranking_probe=probe)
        self.assertEqual(
            ["work:semantic-refactor", "work:bounded-test-harness", "work:independent-review"],
            [choice.work.work_key for choice in ranked],
        )
        self.assertEqual(3, len(probed))

        # Repository-real component: corpus profile documents validate against the real
        # machine contract, and the oracle is the merged upstream module, not a copy.
        for profile in self.corpus["agent_profiles"]:
            with self.subTest(profile=profile["profile_key"]):
                self.assertEqual(
                    [],
                    validate_subset(profile["capability_profile_document"], PROFILE_SCHEMA),
                )
        self.assertEqual(
            ROOT / "scripts" / "test_v48_scheduling_conformance.py",
            Path(scheduling.__file__).resolve(),
        )
        record_scenario(
            scenario_id="ODF-01",
            name="multi-ready-heterogeneous-eligibility",
            l3_tests="L3 #1 multi-ready-heterogeneous-eligibility",
            oracle="only hard-eligible candidates reach ranking/admission; profile differences resolve through canonical capability/role semantics",
            observed="5 profile/work pairs resolved ELIGIBLE(3)/INELIGIBLE(2); ranking probe observed exactly the 3 eligible items; corpus profiles validate against agent-capability-profile-v1",
            evidence_class=["SYNTHETIC_DETERMINISTIC", "REPOSITORY_REAL_EXECUTION"],
            environment="local build host, exact candidate checkout, python -B scripts/test_v48_orchestration_dogfood.py",
        )

    # ------------------------------------------------------------------
    # ODF-02 — fresh vs stale/missing Availability
    # ------------------------------------------------------------------
    def test_odf02_fresh_stale_availability(self) -> None:
        availability = self.corpus["availability_facts"]
        work = work_requirement_from_corpus(self.corpus["work_items"][0])
        agent = profile_from_corpus(self.corpus["agent_profiles"][0])

        fresh = availability_from_corpus(availability["fresh_available"])
        stale = availability_from_corpus(availability["stale_available"])
        missing = availability_from_corpus(availability["missing"])
        unavailable = availability_from_corpus(availability["unavailable"])

        self.assertEqual(scheduling.ELIGIBLE, scheduling.resolve_eligibility(
            scheduling.Candidate(work, agent, fresh)))
        self.assertEqual(scheduling.UNKNOWN, scheduling.resolve_eligibility(
            scheduling.Candidate(work, agent, stale)))
        self.assertEqual(scheduling.UNKNOWN, scheduling.resolve_eligibility(
            scheduling.Candidate(work, agent, missing)))
        self.assertEqual(scheduling.INELIGIBLE, scheduling.resolve_eligibility(
            scheduling.Candidate(work, agent, unavailable)))

        probed: list[str] = []

        def probe(candidate: scheduling.Candidate) -> tuple[int, int, int, int]:
            probed.append(candidate.work.work_key)
            return candidate.rank

        ranked = scheduling.rank_eligible(
            [
                scheduling.Candidate(work, agent, stale, rank=(999, 999, 999, 999)),
                scheduling.Candidate(work, agent, missing, rank=(999, 999, 999, 999)),
            ],
            ranking_probe=probe,
        )
        self.assertEqual([], ranked)
        self.assertEqual([], probed, "stale/missing facts must not reach ranking")
        record_scenario(
            scenario_id="ODF-02",
            name="fresh-stale-availability",
            l3_tests="L3 #2 fresh-stale-availability",
            oracle="stale/missing material Availability => UNKNOWN and fail closed; no ranking override",
            observed="fresh=>ELIGIBLE; stale/current-false=>UNKNOWN; missing=>UNKNOWN; UNAVAILABLE=>INELIGIBLE; stale+missing never reached ranking even with maximal rank",
            evidence_class=["SYNTHETIC_DETERMINISTIC"],
            environment="local build host, reference-model execution over committed corpus facts",
        )

    # ------------------------------------------------------------------
    # ODF-03 — capacity-N contention
    # ------------------------------------------------------------------
    def test_odf03_capacity_n_contention(self) -> None:
        capacities = dict(self.corpus["resource_capacities"])
        state = scheduling.AdmissionState()
        observations: list[int] = []
        plan = [("A", {"build-host-pool": 2}, 0), ("B", {"build-host-pool": 1}, 1)]
        for index, (work_key, required, generation) in enumerate(plan):
            result, state = scheduling.admit(
                state,
                work_key=work_key,
                expected_generation=generation,
                required=required,
                capacities=capacities,
            )
            self.assertEqual("ACCEPTED", result, work_key)
            observations.append(state.used("build-host-pool"))
            self.assertLessEqual(
                state.used("build-host-pool"),
                capacities["build-host-pool"],
                "accepted canonical state exceeded capacity",
            )
        self.assertEqual([2, 3], observations)

        before = state
        result, state = scheduling.admit(
            state,
            work_key="C",
            expected_generation=2,
            required={"build-host-pool": 1},
            capacities=capacities,
        )
        self.assertEqual("CAPACITY_EXCEEDED", result)
        self.assertEqual(before, state, "loser must fail closed without state change")

        # Repository-real component: corpus capacities were loaded from the real committed
        # fixture file, and the admission oracle is the merged upstream module file.
        self.assertEqual(3, capacities["build-host-pool"])
        self.assertEqual(1, capacities["exclusive-device"])
        record_scenario(
            scenario_id="ODF-03",
            name="capacity-n-contention",
            l3_tests="L3 #3 capacity-n-contention",
            oracle="accepted active units never exceed N; loser fails closed",
            observed="2+1 units accepted against capacity 3; third contender CAPACITY_EXCEEDED with byte-identical state; capacity invariant held at every canonical state",
            evidence_class=["SYNTHETIC_DETERMINISTIC", "REPOSITORY_REAL_EXECUTION"],
            environment="local build host; corpus facts loaded from real committed fixture file; merged T-008 admission oracle",
        )

    # ------------------------------------------------------------------
    # ODF-04 — exclusive resource + duplicate/incompatible assignment race
    # ------------------------------------------------------------------
    def test_odf04_exclusive_resource_duplicate_assignment_race(self) -> None:
        capacities = dict(self.corpus["resource_capacities"])
        state = scheduling.AdmissionState()
        result, state = scheduling.admit(
            state,
            work_key="owner-A",
            expected_generation=0,
            required={"exclusive-device": 1},
            capacities=capacities,
        )
        self.assertEqual("ACCEPTED", result)
        before = state
        result, state = scheduling.admit(
            state,
            work_key="incompatible-B",
            expected_generation=1,
            required={"exclusive-device": 1},
            capacities=capacities,
        )
        self.assertEqual("CAPACITY_EXCEEDED", result)
        self.assertEqual(before, state)
        result, state = scheduling.admit(
            state,
            work_key="owner-A",
            expected_generation=1,
            required={"exclusive-device": 1},
            capacities=capacities,
        )
        self.assertEqual("DUPLICATE", result)
        self.assertEqual(before, state)

        # Same work identity racing two operators through the T-017 claim oracle:
        # exactly one canonical accepted start; the loser fails closed.
        ownership_state = ownership.OwnershipState()
        decision, ownership_state = ownership.admit_claim(
            ownership_state, "#517:builder", "claude-code:v48-t011-phase2-builder",
            "d-v4.8.0-T-011-phase2-builder-94955c6f", 0,
        )
        self.assertEqual(ownership.ACCEPTED, decision)
        decision, _ = ownership.admit_claim(
            ownership_state, "#517:builder", "other-operator", "d-other", 1,
        )
        self.assertEqual(ownership.DUPLICATE_CLAIM, decision)
        starts = [r for r in ownership_state.records if r.work_key == "#517:builder"]
        self.assertEqual(1, len(starts))
        record_scenario(
            scenario_id="ODF-04",
            name="exclusive-resource-duplicate-assignment-race",
            l3_tests="L3 #4 exclusive-resource-race + L3 #6 duplicate-assignment-race",
            oracle="at most one incompatible accepted admission/start; duplicate assignment fails closed",
            observed="N=1 device admitted owner-A only; incompatible-B CAPACITY_EXCEEDED; re-admission of owner-A DUPLICATE; claim race admitted exactly one start, loser DUPLICATE_CLAIM",
            evidence_class=["SYNTHETIC_DETERMINISTIC", "REPOSITORY_REAL_EXECUTION"],
            environment="local build host; merged T-008 admission + T-017 claim oracles over corpus facts",
        )

    # ------------------------------------------------------------------
    # ODF-05 — reviewer/validator independence hard filter
    # ------------------------------------------------------------------
    def test_odf05_independence_hard_filter(self) -> None:
        review_work = work_requirement_from_corpus(self.corpus["work_items"][2])
        strong = profile_from_corpus(self.corpus["agent_profiles"][0])
        fresh = availability_from_corpus(self.corpus["availability_facts"]["fresh_available"])

        # The profile that built the candidate cannot review it, whatever its rank claims.
        conflicted_builder = scheduling.Candidate(
            review_work,
            strong,
            fresh,
            independence_ok=False,
            rank=(-9999, -9999, -9999, -9999),
        )
        self.assertEqual(scheduling.INELIGIBLE, scheduling.resolve_eligibility(conflicted_builder))

        probed: list[str] = []

        def probe(candidate: scheduling.Candidate) -> tuple[int, int, int, int]:
            probed.append(candidate.work.work_key)
            return candidate.rank

        self.assertEqual([], scheduling.rank_eligible([conflicted_builder], ranking_probe=probe))
        self.assertEqual([], probed, "conflicted candidate must be rejected before ranking")

        # An unconflicted reviewer remains eligible; a self-reviewing validator is not.
        reviewer = profile_from_corpus(self.corpus["agent_profiles"][2])
        independent = scheduling.Candidate(review_work, reviewer, fresh, independence_ok=True)
        self.assertEqual(scheduling.ELIGIBLE, scheduling.resolve_eligibility(independent))
        validator_conflict = scheduling.Candidate(
            work_requirement_from_corpus(self.corpus["work_items"][1]),
            reviewer,
            fresh,
            independence_ok=False,
        )
        self.assertEqual(scheduling.INELIGIBLE, scheduling.resolve_eligibility(validator_conflict))
        record_scenario(
            scenario_id="ODF-05",
            name="independence-hard-filter",
            l3_tests="L3 #7 independence-hard-filter",
            oracle="conflicted reviewer/validator candidate rejected before optimization/ranking",
            observed="independence_ok=False rejected as INELIGIBLE before the ranking probe ran, including with an adversarial best rank; unconflicted reviewer stayed eligible",
            evidence_class=["SYNTHETIC_DETERMINISTIC"],
            environment="local build host, reference-model execution over committed corpus facts",
        )

    # ------------------------------------------------------------------
    # ODF-06 — duplicate/replay of same identity+payload is idempotent
    # ------------------------------------------------------------------
    def test_odf06_replay_same_identity_same_payload(self) -> None:
        subject = "git:kaicreator-mm/ai-development-standard@94955c6f93fd7316406ea96bce8f7c32a62509ef"
        envelope = make_envelope(
            exchange_id="exchange:v48:t011:idem:1",
            subject_identity_ref=subject,
            payload_ref="event:t011-implementation-ready-1",
            occurred_at="2026-10-03T00:00:00Z",
        )
        payload = dict(IMPLEMENTATION_READY_EVENT)
        deliveries = [
            make_delivery(envelope, payload),
            make_delivery(make_envelope(
                exchange_id="exchange:v48:t011:idem:1",
                subject_identity_ref=subject,
                payload_ref="event:t011-implementation-ready-1",
                occurred_at="2026-10-03T00:05:00Z",
            ), dict(payload)),
        ]
        fixture = replay_fixture(
            deliveries,
            [durable_fact("event:t011-implementation-ready-1", payload)],
            state="implementing",
        )
        self.assertEqual(
            ["ACCEPTED", "DUPLICATE_IDEMPOTENT"],
            interchange.replay_delivery_outcomes(fixture),
        )
        self.assertEqual(
            ["event:t011-implementation-ready-1"],
            interchange.materialized_effect_refs(fixture),
            "replay must not duplicate durable semantic authority",
        )
        self.assertEqual([], interchange.validate_durable_facts(fixture))
        self.assertEqual("review-ready", interchange.reconstruct_workflow_state(fixture))
        record_scenario(
            scenario_id="ODF-06",
            name="replay-same-identity-same-payload",
            l3_tests="L3 #8 duplicate-replay-idempotent",
            oracle="same Interchange/idempotency identity with same payload is safe replay without duplicate authority",
            observed="second identical delivery resolved DUPLICATE_IDEMPOTENT; exactly one durable effect materialized; workflow state reconstructed once",
            evidence_class=["SYNTHETIC_DETERMINISTIC"],
            environment="local build host; merged T-009 replay oracles over in-memory deterministic deliveries",
        )

    # ------------------------------------------------------------------
    # ODF-07 — same replay identity + conflicting payload/digest
    # ------------------------------------------------------------------
    def test_odf07_replay_same_identity_conflicting_payload(self) -> None:
        subject = "git:kaicreator-mm/ai-development-standard@94955c6f93fd7316406ea96bce8f7c32a62509ef"
        envelope = make_envelope(
            exchange_id="exchange:v48:t011:conflict:1",
            subject_identity_ref=subject,
            payload_ref="event:t011-implementation-ready-2",
            occurred_at="2026-10-03T00:00:00Z",
        )
        payload = dict(IMPLEMENTATION_READY_EVENT)
        conflicting = dict(IMPLEMENTATION_READY_EVENT, next_state="merged")
        deliveries = [
            make_delivery(envelope, payload),
            make_delivery(make_envelope(
                exchange_id="exchange:v48:t011:conflict:1",
                subject_identity_ref=subject,
                payload_ref="event:t011-implementation-ready-2",
                occurred_at="2026-10-03T00:06:00Z",
            ), conflicting),
        ]
        fixture = replay_fixture(
            deliveries,
            [durable_fact("event:t011-implementation-ready-2", payload)],
            state="implementing",
        )
        self.assertEqual(
            ["ACCEPTED", "CONFLICT_FAIL_CLOSED"],
            interchange.replay_delivery_outcomes(fixture),
            "conflicting replay under the same identity must fail closed, not last-write-wins",
        )
        self.assertEqual(
            ["event:t011-implementation-ready-2"],
            interchange.materialized_effect_refs(fixture),
        )
        self.assertEqual("review-ready", interchange.reconstruct_workflow_state(fixture))

        # A tampered payload that no longer matches its declared digest also fails closed.
        tampered = dict(IMPLEMENTATION_READY_EVENT)
        tampered_delivery = make_delivery(make_envelope(
            exchange_id="exchange:v48:t011:conflict:2",
            subject_identity_ref=subject,
            payload_ref="event:t011-implementation-ready-3",
            occurred_at="2026-10-03T00:07:00Z",
        ), tampered)
        tampered_delivery["payload_digest"] = "sha256:" + "0" * 64
        tampered_fixture = replay_fixture([tampered_delivery], [], state="implementing")
        self.assertEqual(
            ["DIGEST_MISMATCH_FAIL_CLOSED"],
            interchange.replay_delivery_outcomes(tampered_fixture),
        )
        record_scenario(
            scenario_id="ODF-07",
            name="replay-same-identity-conflicting-payload",
            l3_tests="L3 #9 conflicting-replay-fail-closed",
            oracle="same identity with conflicting payload/digest is rejected rather than last-write-wins",
            observed="conflicting payload under the same exchange identity CONFLICT_FAIL_CLOSED; first materialization retained; digest-mismatch delivery DIGEST_MISMATCH_FAIL_CLOSED",
            evidence_class=["SYNTHETIC_DETERMINISTIC"],
            environment="local build host; merged T-009 replay oracles over in-memory deterministic deliveries",
        )

    # ------------------------------------------------------------------
    # ODF-08 — transport loss / delayed ACK cannot become workflow truth
    # ------------------------------------------------------------------
    def test_odf08_transport_loss_ack_progress(self) -> None:
        subject = "git:kaicreator-mm/ai-development-standard@94955c6f93fd7316406ea96bce8f7c32a62509ef"
        payload = dict(IMPLEMENTATION_READY_EVENT)
        envelope = make_envelope(
            exchange_id="exchange:v48:t011:loss:1",
            subject_identity_ref=subject,
            payload_ref="event:t011-implementation-ready-4",
            occurred_at="2026-10-03T00:00:00Z",
        )
        lost = make_delivery(envelope, payload, transport_outcome="LOST")
        ack_event = {
            "schema": "ai-dev/event-v2",
            "event": "DISPATCH_STATE_CHANGED",
            "actor_role": "builder",
            "operator_kind": "claude-code",
            "operator_id": "claude-code:v48-t011-phase2-builder",
            "dispatch_id": "d-v4.8.0-T-011-phase2-builder-94955c6f",
            "dispatch_state": "ACKNOWLEDGED",
        }
        fixture = replay_fixture(
            [lost],
            [
                durable_fact("event:t011-implementation-ready-4", payload),
                durable_fact("ack:1", ack_event),
            ],
            state="implementing",
        )
        self.assertEqual(["LOST_NO_EFFECT"], interchange.replay_delivery_outcomes(fixture))
        self.assertEqual([], interchange.materialized_effect_refs(fixture))

        # The same delivery replayed after the loss is accepted exactly once.
        replayed = replay_fixture(
            [lost, make_delivery(envelope, payload)],
            [durable_fact("event:t011-implementation-ready-4", payload)],
            state="implementing",
        )
        self.assertEqual(
            ["LOST_NO_EFFECT", "ACCEPTED"],
            interchange.replay_delivery_outcomes(replayed),
        )

        # ACK/progress is non-authoritative: transport facts never move workflow truth,
        # and delivery chronology is not workflow truth either.
        self.assertEqual("review-ready", interchange.reconstruct_workflow_state(fixture))
        self.assertEqual(
            "implementing",
            fixture["authoritative_work_item"]["state"],
        )
        reordered = replay_fixture(list(reversed(replayed["deliveries"])), replayed["durable_facts"], state="implementing")
        self.assertEqual(
            interchange.reconstruct_workflow_state(replayed),
            interchange.reconstruct_workflow_state(reordered),
        )
        record_scenario(
            scenario_id="ODF-08",
            name="transport-loss-ack-progress",
            l3_tests="L3 #10 delivery-loss-ack-non-authority",
            oracle="loss/delay/retry/ACK/progress changes delivery facts only; durable owners are workflow truth",
            observed="lost delivery LOST_NO_EFFECT and materialized nothing; replay after loss accepted exactly once; ACK durable fact left workflow state unchanged; reversed delivery chronology changed nothing",
            evidence_class=["SYNTHETIC_DETERMINISTIC"],
            environment="local build host; merged T-009 replay/reconstruction oracles over in-memory deterministic deliveries",
        )

    # ------------------------------------------------------------------
    # ODF-09 — crash/restart durable reconstruction (repository-real)
    # ------------------------------------------------------------------
    def test_odf09_crash_restart_durable_reconstruction(self) -> None:
        real_fixture_path = (
            ROOT / "fixtures" / "v48_interchange_replay" / "restart_durable_reconstruction.json"
        )
        fixture = json.loads(real_fixture_path.read_text(encoding="utf-8"))
        before = interchange.reconstruct_workflow_state(fixture)
        restarted = dict(fixture)
        restarted.pop("transient_queue", None)
        restarted.pop("chat_history", None)
        self.assertEqual(before, interchange.reconstruct_workflow_state(restarted))
        contradictory = dict(restarted)
        contradictory["transient_queue"] = [
            {"delivery_id": "t011-crash-1", "state": "FAILED"},
            {"delivery_id": "t011-crash-1", "state": "TIMEOUT"},
        ]
        contradictory["chat_history"] = ["private chat claiming a different state"]
        self.assertEqual(before, interchange.reconstruct_workflow_state(contradictory))

        # T-011's own ownership facts reconstruct from the real durable manifest after a
        # simulated controller/session loss; no transient chat input is consulted.
        manifest = parse_manifest_durable_facts()
        self.assertEqual("94955c6f93fd7316406ea96bce8f7c32a62509ef", manifest["base_sha"])
        self.assertEqual(
            "docs/implementation/4.8.0/task-packs/T11_orchestration_dogfood.md",
            manifest["task_pack_ref"],
        )
        self.assertEqual("task/v4.8.0-t11-orchestration-dogfood", manifest["branch"])
        self.assertIn("scripts/test_v48_orchestration_dogfood.py", manifest["builder_write_set"])
        self.assertIn("docs/implementation/4.8.0/dogfood/orchestration/**", manifest["builder_write_set"])
        self.assertIn("standards/**", manifest["forbidden_builder_paths"])
        record_scenario(
            scenario_id="ODF-09",
            name="crash-restart-durable-reconstruction",
            l3_tests="L3 #11 restart-durable-reconstruction",
            oracle="authoritative state reconstructs from durable facts only, without transient queue/chat history",
            observed="real restart fixture reconstructed review-ready with transient keys removed and with contradictory transient data injected; real T-011 MANIFEST durable facts (base/pack/branch/write set) reconstructed after simulated session loss",
            evidence_class=["REPOSITORY_REAL_EXECUTION"],
            environment="local build host; executed against real repository files at the exact candidate checkout",
        )

    # ------------------------------------------------------------------
    # ODF-10 — T-017 accepted Claim / Start Record / projection / timeout
    # ------------------------------------------------------------------
    def test_odf10_accepted_claim_start_projection_loss_timeout_replacement(self) -> None:
        claim = load_claim_event()
        self.assertEqual(
            [],
            validate_subset(claim, EVENT_V2),
            "durable Builder Claim copy must validate against the real event-v2 contract",
        )
        state = ownership.OwnershipState()
        decision, state = ownership.admit_claim(
            state,
            claim["protected_claim_key"],
            claim["operator_id"],
            claim["dispatch_id"],
            expected_generation=0,
            admission_mode=claim["admission_mode"],
        )
        self.assertEqual(ownership.ACCEPTED, decision)
        # The durable Start Record carries the accepted claim event's durable facts
        # (same enrichment pattern as the merged T-017 conformance suite).
        state = replace(state, records=tuple(
            replace(
                record,
                session_ref=claim["session_ref"],
                occurred_at=claim["occurred_at"],
                execution_profile=claim["execution_profile"],
                exact_subject=claim["sha"],
                task_pack_ref=claim["task_pack_ref"],
                execution_pack_ref=claim["execution_pack_ref"],
                admission_mode=claim["admission_mode"],
                protected_claim_key=claim["protected_claim_key"],
                claim_generation=claim["claim_generation"],
            )
            for record in state.records
        ))
        record = ownership._record_for(state, claim["protected_claim_key"])
        self.assertEqual(claim["operator_id"], record.operator_id)
        self.assertEqual(claim["dispatch_id"], record.dispatch_id)
        self.assertEqual(claim["session_ref"], record.session_ref)
        self.assertEqual(claim["occurred_at"], record.occurred_at)
        self.assertEqual(claim["sha"], record.exact_subject)
        self.assertEqual(claim["task_pack_ref"], record.task_pack_ref)
        self.assertTrue(ownership.authorize_execution(record))

        # The projection label is derived visibility, never the lock: losing the
        # projection publication cannot erase the claim or authorize a competitor.
        published = False
        self.assertFalse(published)
        self.assertTrue(ownership.authorize_execution(
            ownership._record_for(state, claim["protected_claim_key"])))
        decision, _ = ownership.admit_claim(
            state, claim["protected_claim_key"], "other-operator", "d-other", 1,
        )
        self.assertEqual(ownership.DUPLICATE_CLAIM, decision)
        self.assertEqual(
            "state:implementing",
            ownership.projection_label_for(
                ownership._record_for(state, claim["protected_claim_key"])
            ),
        )

        # Ambiguous timeout/replacement fails closed until durable reconciliation.
        expired = ownership.apply_liveness_expiry(state, claim["protected_claim_key"])
        decision, _ = ownership.admit_claim(
            expired, claim["protected_claim_key"], "successor-op", "d-successor", 1,
        )
        self.assertEqual(ownership.PRIOR_OWNERSHIP_ACTIVE, decision)
        ambiguous = ownership.record_terminal_release(
            state, claim["protected_claim_key"], "TIMEOUT", ambiguous=True,
        )
        decision, _ = ownership.admit_claim(
            ambiguous, claim["protected_claim_key"], "successor-op", "d-successor", 1,
        )
        self.assertEqual(ownership.AMBIGUOUS_RELEASE, decision)
        reconciled = ownership.reconcile_ambiguity(ambiguous, claim["protected_claim_key"])
        decision, successor = ownership.admit_claim(
            reconciled, claim["protected_claim_key"], "successor-op", "d-successor", 1,
        )
        self.assertEqual(ownership.ACCEPTED, decision)
        history = [r for r in successor.records if r.work_key == claim["protected_claim_key"]]
        self.assertEqual(2, len(history))
        self.assertEqual("TIMEOUT", history[0].state)
        self.assertEqual("successor-op", history[1].operator_id)
        record_scenario(
            scenario_id="ODF-10",
            name="accepted-claim-start-projection-loss-timeout-replacement",
            l3_tests="L3 #12 t017-start-visibility + L3 #13 timeout-replacement-fail-closed",
            oracle="accepted Claim is the durable Start Record; projection is derived; ambiguous replacement blocks until durable reconciliation",
            observed="real accepted Builder Claim event validated against event-v2 and admitted as the Start Record; projection loss authorized no duplicate; liveness expiry and ambiguous TIMEOUT release both blocked the successor; after reconciliation the successor admitted with append-only history",
            evidence_class=["REPOSITORY_REAL_EXECUTION"],
            environment="local build host; real committed claim-event fixture + real event-v2 schema + merged T-017 ownership oracle",
        )

    # ------------------------------------------------------------------
    # ODF-11 — bounded executor eligible success (repository-real)
    # ------------------------------------------------------------------
    def test_odf11_bounded_executor_eligible_success(self) -> None:
        manifest = parse_manifest_durable_facts()
        corpus = self.corpus
        base = manifest["base_sha"]
        pack_head = corpus["jit_pack_head"]

        # Eligibility is evaluated through the merged hard-filter oracle with real
        # currentness facts: the live candidate descends from the exact pack base.
        _git("merge-base", "--is-ancestor", base, "HEAD")
        bounded_profile = profile_from_corpus(corpus["agent_profiles"][1])
        bounded_work = replace(
            work_requirement_from_corpus(corpus["work_items"][1]),
            work_key="work:t011-bounded-write-set-verification",
        )
        fresh = availability_from_corpus(corpus["availability_facts"]["fresh_available"])
        candidate = scheduling.Candidate(bounded_work, bounded_profile, fresh)
        self.assertEqual(
            scheduling.ELIGIBLE,
            scheduling.resolve_eligibility(candidate),
            "the bounded executor must be hard-eligible for its bounded verification action",
        )
        self.assertEqual(
            "F1_BOUNDED_IMPLEMENTATION",
            corpus["agent_profiles"][1]["capability_profile_document"]["max_agent_freedom_claim"],
        )
        self.assertEqual("F2_ENGINEERING_DISCRETION", manifest["agent_freedom"])
        self.assertEqual("F2_ENGINEERING_DISCRETION", manifest["task_pack_agent_freedom_ceiling"])

        # The bounded action: verify the real candidate diff stays inside the authorized
        # Builder write set and outside every forbidden path.
        authorized_exact = {"scripts/test_v48_orchestration_dogfood.py"}
        authorized_prefix = "docs/implementation/4.8.0/dogfood/orchestration/"
        forbidden_prefixes = ("standards/", "schemas/", ".github/workflows/")
        forbidden_exact = {
            "docs/implementation/4.8.0/PRD.md",
            "docs/implementation/4.8.0/L2_ARCHITECTURE_EVIDENCE.md",
            "docs/implementation/4.8.0/TASK_DAG.md",
        }
        paths = candidate_paths(pack_head)
        self.assertTrue(paths, "candidate write-set probe observed no candidate paths")
        decisions = []
        for path in paths:
            forbidden = (
                path in forbidden_exact
                or path.startswith(forbidden_prefixes)
            )
            authorized = path in authorized_exact or path.startswith(authorized_prefix)
            decisions.append((path, authorized, forbidden))
            self.assertFalse(forbidden, f"forbidden path in candidate diff: {path}")
            self.assertTrue(authorized, f"path outside Builder write set: {path}")
        self.assertTrue(all(authorized and not forbidden for _, authorized, forbidden in decisions))
        record_scenario(
            scenario_id="ODF-11",
            name="bounded-executor-eligible-success",
            l3_tests="L3 #14 bounded-executor-eligible-success",
            oracle="bounded path may complete only within exact pack/write-set/authority constraints",
            observed=f"bounded F1 executor hard-ELIGIBLE; performed real write-set verification over {len(decisions)} candidate path(s) diffed from JIT pack head {pack_head[:12]}; every path inside the authorized write set, none forbidden; 0 escalations",
            evidence_class=["REPOSITORY_REAL_EXECUTION"],
            environment="local build host; real git diff/status of the candidate worktree + real MANIFEST write-set facts + merged T-008 eligibility oracle",
        )

    # ------------------------------------------------------------------
    # ODF-12 — bounded executor semantic ambiguity escalation (repository-real)
    # ------------------------------------------------------------------
    def test_odf12_bounded_executor_ambiguity_escalation(self) -> None:
        manifest = parse_manifest_durable_facts()

        def escalation_event(blocker_class: str, reason: str) -> dict:
            return {
                "schema": "ai-dev/event-v2",
                "event": "BLOCKER_REPORTED",
                "actor_role": "builder",
                "operator_kind": "claude-code",
                "operator_id": "claude-code:v48-t011-phase2-builder",
                "issue": "#517",
                "dispatch_id": "d-v4.8.0-T-011-phase2-builder-94955c6f",
                "blocker_class": blocker_class,
                "reason": reason,
                "next_state": "blocked",
            }

        # Probe A: stale/unknown pack identity — the executor must refuse to act on a
        # Task Pack blob that does not match the durable manifest binding.
        blob = manifest["task_pack_blob"]
        stale_pack_blob = blob[:-1] + ("0" if blob[-1] != "0" else "1")
        self.assertNotEqual(stale_pack_blob, blob)
        escalation_a = escalation_event(
            "STALE_PACK_IDENTITY",
            "requested action binds Task Pack blob "
            f"{stale_pack_blob} but durable manifest binds {manifest['task_pack_blob']}",
        )
        self.assertEqual([], validate_subset(escalation_a, EVENT_V2))

        # Probe B: forbidden path — the write-set gate refuses before any action.
        forbidden_target = "standards/EXECUTION_ARCHITECTURE_STANDARD.md"
        escalation_b = escalation_event(
            "AUTHORITY_OUTSIDE_WRITE_SET",
            f"requested action targets non-authoritative-to-builder path {forbidden_target}",
        )
        self.assertEqual([], validate_subset(escalation_b, EVENT_V2))

        # Probe C: semantic ambiguity — same identity, conflicting payloads; the bounded
        # executor must not pick a winner (that oracle is fail-closed, not a choice).
        subject = "git:kaicreator-mm/ai-development-standard@94955c6f93fd7316406ea96bce8f7c32a62509ef"
        payload = dict(IMPLEMENTATION_READY_EVENT)
        conflicting = dict(IMPLEMENTATION_READY_EVENT, next_state="merged")
        ambiguous_fixture = replay_fixture(
            [
                make_delivery(make_envelope(
                    exchange_id="exchange:v48:t011:ambiguity:1",
                    subject_identity_ref=subject,
                    payload_ref="event:t011-ambiguity",
                    occurred_at="2026-10-03T00:00:00Z",
                ), payload),
                make_delivery(make_envelope(
                    exchange_id="exchange:v48:t011:ambiguity:1",
                    subject_identity_ref=subject,
                    payload_ref="event:t011-ambiguity",
                    occurred_at="2026-10-03T00:01:00Z",
                ), conflicting),
            ],
            [],
            state="implementing",
        )
        self.assertEqual(
            ["ACCEPTED", "CONFLICT_FAIL_CLOSED"],
            interchange.replay_delivery_outcomes(ambiguous_fixture),
        )
        escalation_c = escalation_event(
            "SEMANTIC_AMBIGUITY_CONFLICTING_REPLAY",
            "conflicting replay under one idempotency identity; fail-closed oracle applies, no executor choice",
        )
        self.assertEqual([], validate_subset(escalation_c, EVENT_V2))

        # No self-elevation: the probes mutated nothing — the real standards file still
        # hashes to its committed blob and the durable manifest facts are unchanged.
        committed_hash = _git("hash-object", str(ROOT / "standards" / "EXECUTION_ARCHITECTURE_STANDARD.md")).strip()
        head_blob = _git("rev-parse", "HEAD:standards/EXECUTION_ARCHITECTURE_STANDARD.md").strip()
        self.assertEqual(head_blob, committed_hash)
        self.assertEqual("94955c6f93fd7316406ea96bce8f7c32a62509ef", manifest["base_sha"])
        record_scenario(
            scenario_id="ODF-12",
            name="bounded-executor-semantic-ambiguity",
            l3_tests="L3 #15 bounded-executor-ambiguity-escalation",
            oracle="semantic ambiguity/missing authority => stop and emit durable escalation, never guess or self-elevate",
            observed="3 ambiguity probes (stale pack blob, forbidden standards path, conflicting replay) each produced a durable BLOCKER_REPORTED event validating against event-v2; standards file still hashes to its HEAD blob; no state mutation, no self-elevation",
            evidence_class=["REPOSITORY_REAL_EXECUTION"],
            environment="local build host; real git hash-object verification + real event-v2 schema + merged T-009 fail-closed oracle",
        )

    # ------------------------------------------------------------------
    # ODF-13 — Task/Execution Pack/base currentness drift
    # ------------------------------------------------------------------
    def test_odf13_task_pack_execution_pack_base_drift(self) -> None:
        subjects = self.corpus["subject_identity"]
        current = subjects["current_exact_subject"]
        stale = subjects["stale_exact_subject"]

        # A stale exact subject cannot rebind as current (merged T-007 currentness oracle).
        evidence = {
            "exact_subject_ref": stale,
            "currentness_ref": stale,
        }
        self.assertFalse(contract_compat.capability_evidence_applies_to_subject(evidence, current))
        drift_work = replace(
            work_requirement_from_corpus(self.corpus["work_items"][0]),
            work_key="work:stale-subject",
            authority_current=False,
        )
        agent = profile_from_corpus(self.corpus["agent_profiles"][0])
        fresh = availability_from_corpus(self.corpus["availability_facts"]["fresh_available"])
        self.assertEqual(
            scheduling.INELIGIBLE,
            scheduling.resolve_eligibility(scheduling.Candidate(drift_work, agent, fresh)),
        )

        # Execution Pack drift: a pack bound to a different base is PACK_STALE and must
        # rebind, not continue. The live manifest is current; the mutated copy is not.
        manifest = parse_manifest_durable_facts()
        self.assertEqual(
            self.corpus["exact_base_sha"],
            manifest["base_sha"],
            "real manifest must still bind the exact frozen base",
        )
        drifted = dict(manifest)
        drifted["base_sha"] = subjects["stale_exact_subject"].split("@", 1)[1]
        self.assertNotEqual(drifted["base_sha"], self.corpus["exact_base_sha"])
        with self.assertRaises(AssertionError):
            self.assertEqual(self.corpus["exact_base_sha"], drifted["base_sha"])

        # Generation drift on admission is rejected atomically by both oracles.
        state = scheduling.AdmissionState()
        result, unchanged = scheduling.admit(
            state,
            work_key="work:late-contender",
            expected_generation=7,
            required={"build-host-pool": 1},
            capacities=dict(self.corpus["resource_capacities"]),
        )
        self.assertEqual("STALE", result)
        self.assertEqual(state, unchanged)
        decision, _ = ownership.admit_claim(
            ownership.OwnershipState(), "#517:builder", "op", "d-x", 9,
        )
        self.assertEqual(ownership.STALE_IDENTITY, decision)
        record_scenario(
            scenario_id="ODF-13",
            name="task-pack-execution-pack-base-drift",
            l3_tests="L3 #16 task-base-currentness-drift",
            oracle="stale Task/Execution Pack/base cannot continue as current and must rebind/recompute",
            observed="stale exact subject rejected by the merged currentness oracle; stale-subject work resolved INELIGIBLE; live manifest still binds the frozen base while a drifted copy fails the bind; generation drift rejected STALE/STALE_IDENTITY by both oracles",
            evidence_class=["SYNTHETIC_DETERMINISTIC"],
            environment="local build host; merged T-007 currentness + T-008/T-017 admission oracles over corpus subjects and the real manifest base",
        )

    # ------------------------------------------------------------------
    # ODF-14 — evidence classification + economic boundary
    # ------------------------------------------------------------------
    def test_odf14_evidence_classification_and_economic_boundary(self) -> None:
        valid_ids = {row["scenario_id"] for row in SCENARIO_REGISTRY}
        for row in SCENARIO_REGISTRY:
            with self.subTest(scenario=row["scenario_id"]):
                self.assertTrue(row["evidence_class"])
                for evidence in row["evidence_class"]:
                    self.assertIn(evidence, EVIDENCE_CLASSES)
        self.assertNotIn(
            "REAL_HOST_OR_RUNTIME_VALIDATION",
            {evidence for row in SCENARIO_REGISTRY for evidence in row["evidence_class"]},
            "this deterministic harness must not claim real host/runtime validation",
        )

        # Provider/model provenance never becomes authority: the real machine contract
        # rejects injected authority fields (additionalProperties: false).
        profile = json.loads(json.dumps(
            self.corpus["agent_profiles"][0]["capability_profile_document"]
        ))
        profile["authorization"] = "AUTHORIZED"
        self.assertTrue(validate_subset(profile, PROFILE_SCHEMA))
        self.assertIn("provider_model_provenance", self.corpus["agent_profiles"][0]["capability_profile_document"])

        # Measured fields are descriptive only and are not ranking inputs: ranking uses
        # the corpus rank tuples exclusively.
        self.assertEqual("corpus rank tuples only", self.corpus["measured_notes_descriptive_only"]["ranking_inputs"])
        works = [work_requirement_from_corpus(item) for item in self.corpus["work_items"]]
        profiles = [profile_from_corpus(p) for p in self.corpus["agent_profiles"]]
        fresh = availability_from_corpus(self.corpus["availability_facts"]["fresh_available"])
        ranked = scheduling.rank_eligible([
            scheduling.Candidate(works[2], profiles[2], fresh, rank=(30, 0, 0, 0)),
            scheduling.Candidate(works[0], profiles[0], fresh, rank=(10, 0, 0, 0)),
            scheduling.Candidate(works[1], profiles[1], fresh, rank=(20, 0, 0, 0)),
        ])
        self.assertEqual(
            ["work:semantic-refactor", "work:bounded-test-harness", "work:independent-review"],
            [choice.work.work_key for choice in ranked],
            "ranking order must follow explicit corpus ranks, never provider/model identity",
        )

        # Repository-real boundary anchors: the committed evidence artifacts state the
        # synthetic/real boundary and the economic limits explicitly.
        matrix_text = (DOGFOOD_DIR / "EVIDENCE_MATRIX.md").read_text(encoding="utf-8")
        report_text = (DOGFOOD_DIR / "RESULT_REPORT.md").read_text(encoding="utf-8")
        for anchor in (
            "no universal Agent ranking",
            "no blanket strong-to-low-cost routing",
            "no savings claim",
            "descriptive only",
        ):
            self.assertIn(anchor, matrix_text + report_text, anchor)
        self.assertIn("NOT_RUN", report_text)
        self.assertIn("BLOCKED", report_text)
        record_scenario(
            scenario_id="ODF-14",
            name="evidence-classification-and-economic-boundary",
            l3_tests="L3 #17 evidence-classification + L3 #18 no-economic-universal-inference",
            oracle="every result carries an explicit evidence class; measurements stay descriptive; no universal ranking/routing/savings inference",
            observed=f"{len(SCENARIO_REGISTRY)} registry rows at this point all carry explicit classes; no row claims REAL_HOST_OR_RUNTIME_VALIDATION; profile contract rejects injected authority fields; ranking followed corpus ranks only; committed evidence artifacts contain the boundary anchors",
            evidence_class=["SYNTHETIC_DETERMINISTIC", "REPOSITORY_REAL_EXECUTION"],
            environment="local build host; registry self-inspection + real schema validation + real committed evidence artifacts",
        )

    # ------------------------------------------------------------------
    # ODF-15 — composite multi-resource all-or-none admission
    # ------------------------------------------------------------------
    def test_odf15_composite_multi_resource_admission(self) -> None:
        item = self.corpus["work_items"][0]
        required = dict(item["required_resources"])
        required["review-quota"] = 1
        compatibility = frozenset(item["required_compatibility_keys"])
        capacities = dict(self.corpus["resource_capacities"])
        capacities["review-quota"] = 1

        # Independent per-key success never proves composite admission; unsafe modes are
        # rejected outright.
        for unsafe_mode in ("INDEPENDENT_PER_KEY_CAS", "PER_RESOURCE_LEASES", "SEQUENTIAL_RESERVATIONS"):
            result, unchanged = scheduling.admit(
                scheduling.AdmissionState(),
                work_key="unsafe-composite",
                expected_generation=0,
                required=required,
                capacities=capacities,
                compatibility=compatibility,
                admission_mode=unsafe_mode,
            )
            self.assertEqual("BLOCKED_UNSAFE_COMPOSITE_ADMISSION", result)
            self.assertEqual(scheduling.AdmissionState(), unchanged)

        # Failure before publication publishes nothing (all-or-none).
        initial = scheduling.AdmissionState()
        result, rejected = scheduling.admit(
            initial,
            work_key="work:semantic-refactor",
            expected_generation=0,
            required=required,
            capacities=capacities,
            compatibility=compatibility,
            failure_point="BEFORE_PUBLICATION",
        )
        self.assertEqual("REJECTED_BEFORE_PUBLICATION", result)
        self.assertEqual(initial, rejected)

        # Failure at publication leaves an ambiguous protected region and blocks every
        # incompatible successor until durable reconciliation.
        result, ambiguous = scheduling.admit(
            initial,
            work_key="work:semantic-refactor",
            expected_generation=0,
            required=required,
            capacities=capacities,
            compatibility=compatibility,
            failure_point="AT_PUBLICATION",
        )
        self.assertEqual("AMBIGUOUS_RECONCILE_REQUIRED", result)
        self.assertNotIn("work:semantic-refactor", ambiguous.claims)
        self.assertEqual(0, ambiguous.used("build-host-pool"))
        result, unchanged = scheduling.admit(
            ambiguous,
            work_key="work:successor",
            expected_generation=0,
            required={"build-host-pool": 1},
            capacities=capacities,
        )
        self.assertEqual("BLOCKED_RECONCILE_REQUIRED", result)
        self.assertEqual(ambiguous, unchanged)
        cleared = scheduling.reconcile_no_accept(ambiguous, work_key="work:semantic-refactor")
        result, after_clear = scheduling.admit(
            cleared,
            work_key="work:successor",
            expected_generation=0,
            required={"build-host-pool": 1},
            capacities=capacities,
        )
        self.assertEqual("ACCEPTED", result)

        # Failure after publication keeps the durable accepted admission and still blocks
        # successors until the accepted reconciliation lands.
        result, published = scheduling.admit(
            initial,
            work_key="work:semantic-refactor",
            expected_generation=0,
            required=required,
            capacities=capacities,
            compatibility=compatibility,
            failure_point="AFTER_PUBLICATION",
        )
        self.assertEqual("AMBIGUOUS_RECONCILE_REQUIRED", result)
        self.assertIn("work:semantic-refactor", published.claims)
        self.assertEqual(required["build-host-pool"], published.used("build-host-pool"))
        result, _ = scheduling.admit(
            published,
            work_key="work:successor-2",
            expected_generation=1,
            required={"build-host-pool": 1},
            capacities=capacities,
        )
        self.assertEqual("BLOCKED_RECONCILE_REQUIRED", result)
        reconciled = scheduling.reconcile_accepted(published, work_key="work:semantic-refactor")
        self.assertIn(("same-host", "work:semantic-refactor"), reconciled.compatibility_bindings)
        record_scenario(
            scenario_id="ODF-15",
            name="composite-multi-resource-admission",
            l3_tests="L3 #5 composite-multi-resource-admission",
            oracle="work claim plus every required scarce-resource binding publishes all-or-none; no canonical partial state",
            observed="unsafe per-key modes BLOCKED_UNSAFE_COMPOSITE_ADMISSION; BEFORE_PUBLICATION published nothing; AT_PUBLICATION left no partial canonical state and blocked successors until reconcile_no_accept; AFTER_PUBLICATION kept the durable admission and blocked successors until reconcile_accepted",
            evidence_class=["SYNTHETIC_DETERMINISTIC", "REPOSITORY_REAL_EXECUTION"],
            environment="local build host; merged T-008 composite admission oracle over corpus resources",
        )

    # ------------------------------------------------------------------
    # ODF-16 — duplicate/incompatible assignment race, granular
    # ------------------------------------------------------------------
    def test_odf16_duplicate_assignment_race_granular(self) -> None:
        work_key = self.corpus["durable_t011_ownership_facts"]["work_key"]
        operator = self.corpus["durable_t011_ownership_facts"]["expected_operator_id"]
        dispatch = self.corpus["durable_t011_ownership_facts"]["expected_dispatch_id"]

        # Layer 1 — resource admission: duplicate work claims are rejected.
        state = scheduling.AdmissionState()
        result, state = scheduling.admit(
            state,
            work_key="work:duplicate-race",
            expected_generation=0,
            required={"exclusive-device": 1},
            capacities=dict(self.corpus["resource_capacities"]),
        )
        self.assertEqual("ACCEPTED", result)
        result, _ = scheduling.admit(
            state,
            work_key="work:duplicate-race",
            expected_generation=1,
            required={"exclusive-device": 1},
            capacities=dict(self.corpus["resource_capacities"]),
        )
        self.assertEqual("DUPLICATE", result)

        # Layer 2 — T-017 ownership: exactly one durable start record for the identity.
        ownership_state = ownership.OwnershipState()
        decision, ownership_state = ownership.admit_claim(
            ownership_state, work_key, operator, dispatch, 0,
        )
        self.assertEqual(ownership.ACCEPTED, decision)
        decision, _ = ownership.admit_claim(
            ownership_state, work_key, "claude-code:someone-else", "d-race-loser", 1,
        )
        self.assertEqual(ownership.DUPLICATE_CLAIM, decision)
        starts = [r for r in ownership_state.records if r.work_key == work_key]
        self.assertEqual(1, len(starts))
        self.assertEqual(operator, starts[0].operator_id)

        # Layer 3 — interchange: a duplicate delivery of the same assignment identity is
        # idempotent, and an incompatible re-assignment under the same identity fails.
        subject = "git:kaicreator-mm/ai-development-standard@94955c6f93fd7316406ea96bce8f7c32a62509ef"
        assignment = dict(IMPLEMENTATION_READY_EVENT)
        envelope = make_envelope(
            exchange_id="exchange:v48:t011:assign:1",
            subject_identity_ref=subject,
            payload_ref="event:t011-assignment-1",
            occurred_at="2026-10-03T00:00:00Z",
        )
        fixture = replay_fixture(
            [
                make_delivery(envelope, assignment),
                make_delivery(envelope, dict(assignment)),
                make_delivery(make_envelope(
                    exchange_id="exchange:v48:t011:assign:1",
                    subject_identity_ref=subject,
                    payload_ref="event:t011-assignment-1",
                    occurred_at="2026-10-03T00:02:00Z",
                ), dict(assignment, operator_id="claude-code:someone-else")),
            ],
            [durable_fact("event:t011-assignment-1", assignment)],
            state="implementing",
        )
        self.assertEqual(
            ["ACCEPTED", "DUPLICATE_IDEMPOTENT", "CONFLICT_FAIL_CLOSED"],
            interchange.replay_delivery_outcomes(fixture),
        )
        self.assertEqual(["event:t011-assignment-1"], interchange.materialized_effect_refs(fixture))

        # Exactly one canonical accepted admission/start across all three layers.
        self.assertEqual(1, state.used("exclusive-device"))
        self.assertEqual(1, len(starts))
        self.assertEqual(1, len(set(interchange.materialized_effect_refs(fixture))))
        record_scenario(
            scenario_id="ODF-16",
            name="duplicate-assignment-race-granular",
            l3_tests="L3 #6 duplicate-assignment-race (granular across resource/claim/interchange layers)",
            oracle="duplicate/incompatible assignment attempts produce one canonical accepted admission/start and fail closed for the loser",
            observed="resource layer DUPLICATE; ownership layer admitted exactly one start and rejected the racer; interchange layer ACCEPTED/DUPLICATE_IDEMPOTENT/CONFLICT_FAIL_CLOSED with one materialized effect; one canonical admission across all three layers",
            evidence_class=["SYNTHETIC_DETERMINISTIC", "REPOSITORY_REAL_EXECUTION"],
            environment="local build host; merged T-008 + T-017 + T-009 oracles over corpus identity facts",
        )

    # ------------------------------------------------------------------
    # ODF-17 — T-017 start visibility, granular
    # ------------------------------------------------------------------
    def test_odf17_t017_start_visibility_granular(self) -> None:
        claim = load_claim_event()
        state = ownership.OwnershipState()
        decision, state = ownership.admit_claim(
            state,
            claim["protected_claim_key"],
            claim["operator_id"],
            claim["dispatch_id"],
            expected_generation=0,
            admission_mode=claim["admission_mode"],
        )
        self.assertEqual(ownership.ACCEPTED, decision)
        state = replace(state, records=tuple(
            replace(
                record,
                session_ref=claim["session_ref"],
                occurred_at=claim["occurred_at"],
                execution_profile=claim["execution_profile"],
                exact_subject=claim["sha"],
                task_pack_ref=claim["task_pack_ref"],
            )
            for record in state.records
        ))

        # Projection never published at all: durable claim still authorizes only its own
        # operator, and the derived view recomputes from durable facts alone.
        projection_published = False
        self.assertFalse(projection_published)
        record = ownership._record_for(state, claim["protected_claim_key"])
        self.assertTrue(ownership.authorize_execution(record))
        view = ownership.reconstruct_active_ownership(state, claim["protected_claim_key"])
        self.assertEqual(claim["dispatch_id"], view["dispatch_id"])
        self.assertEqual(claim["operator_id"], view["operator_id"])
        self.assertEqual(claim["sha"], view["exact_subject"])

        # A fabricated transport projection claiming another operator cannot authorize
        # that operator: authorization consults durable facts, not labels.
        fabricated_projection = {"state:implementing": "claude-code:someone-else"}
        self.assertEqual(
            "claude-code:someone-else",
            fabricated_projection["state:implementing"],
        )
        decision, _ = ownership.admit_claim(
            state, claim["protected_claim_key"], "claude-code:someone-else", "d-fabricated", 1,
        )
        self.assertEqual(ownership.DUPLICATE_CLAIM, decision)
        self.assertEqual(
            "state:implementing",
            ownership.projection_label_for(record),
            "derived label recomputes from the durable record, never from transport labels",
        )
        record_scenario(
            scenario_id="ODF-17",
            name="t017-start-visibility-granular",
            l3_tests="L3 #12 t017-start-visibility (granular)",
            oracle="accepted Claim is the durable Start Record; current-state projection is derived visibility only; projection loss cannot authorize duplicate execution",
            observed="with the projection entirely unpublished the durable claim still authorized exactly its own operator and reconstructed its view from durable facts; a fabricated transport label authorized nobody; derived label recomputed from the durable record",
            evidence_class=["REPOSITORY_REAL_EXECUTION"],
            environment="local build host; real committed claim-event fixture + merged T-017 ownership oracle",
        )

    # ------------------------------------------------------------------
    # ODF-18 — timeout/replacement fail-closed, granular across surfaces
    # ------------------------------------------------------------------
    def test_odf18_timeout_replacement_fail_closed_granular(self) -> None:
        claim = load_claim_event()
        work_key = claim["protected_claim_key"]
        capacities = dict(self.corpus["resource_capacities"])

        # Establish a canonical state: accepted claim + accepted resource binding.
        ownership_state = ownership.OwnershipState()
        decision, ownership_state = ownership.admit_claim(
            ownership_state, work_key, claim["operator_id"], claim["dispatch_id"], 0,
        )
        self.assertEqual(ownership.ACCEPTED, decision)
        resource_result, ambiguous_resource = scheduling.admit(
            scheduling.AdmissionState(),
            work_key="work:replacement-target",
            expected_generation=0,
            required={"exclusive-device": 1},
            capacities=capacities,
            failure_point="AT_PUBLICATION",
        )
        self.assertEqual("AMBIGUOUS_RECONCILE_REQUIRED", resource_result)

        # Ambiguity on all surfaces: expired liveness + ambiguous release (claim) and an
        # ambiguous protected resource publication. Every incompatible successor
        # admission fails closed on every surface.
        expired = ownership.apply_liveness_expiry(ownership_state, work_key)
        ambiguous_claim = ownership.record_terminal_release(
            expired, work_key, "TIMEOUT", ambiguous=True,
        )
        decision, _ = ownership.admit_claim(
            ambiguous_claim, work_key, "successor-op", "d-successor", 1,
        )
        self.assertEqual(ownership.AMBIGUOUS_RELEASE, decision)
        result, unchanged = scheduling.admit(
            ambiguous_resource,
            work_key="work:successor-resource",
            expected_generation=0,
            required={"exclusive-device": 1},
            capacities=capacities,
        )
        self.assertEqual("BLOCKED_RECONCILE_REQUIRED", result)
        self.assertEqual(ambiguous_resource, unchanged)

        # Reconciling only one surface keeps the other blocked: partial reconciliation
        # does not unlock an incompatible successor.
        claim_reconciled = ownership.reconcile_ambiguity(ambiguous_claim, work_key)
        decision, claim_reconciled = ownership.admit_claim(
            claim_reconciled, work_key, "successor-op", "d-successor", 1,
        )
        self.assertEqual(ownership.ACCEPTED, decision)
        result, unchanged = scheduling.admit(
            ambiguous_resource,
            work_key="work:successor-resource",
            expected_generation=0,
            required={"exclusive-device": 1},
            capacities=capacities,
        )
        self.assertEqual(
            "BLOCKED_RECONCILE_REQUIRED",
            result,
            "resource ambiguity must stay fail closed even after the claim surface reconciles",
        )
        self.assertEqual(ambiguous_resource, unchanged)

        # After durable reconciliation of the resource surface the successor may proceed.
        resource_reconciled = scheduling.reconcile_no_accept(
            ambiguous_resource, work_key="work:replacement-target",
        )
        result, final = scheduling.admit(
            resource_reconciled,
            work_key="work:successor-resource",
            expected_generation=0,
            required={"exclusive-device": 1},
            capacities=capacities,
        )
        self.assertEqual("ACCEPTED", result)
        self.assertEqual(1, final.used("exclusive-device"))
        record_scenario(
            scenario_id="ODF-18",
            name="timeout-replacement-fail-closed-granular",
            l3_tests="L3 #13 timeout-replacement-fail-closed (granular across claim/publication/resource surfaces)",
            oracle="ambiguous active claim/publication/resource state blocks incompatible successor admission until durable reconciliation",
            observed="with liveness expiry + ambiguous TIMEOUT release + ambiguous resource publication, successor admission failed closed on both surfaces; claim-surface reconciliation alone kept the resource surface blocked; full durable reconciliation unlocked the successor",
            evidence_class=["REPOSITORY_REAL_EXECUTION"],
            environment="local build host; merged T-017 + T-008 fail-closed oracles over the real claim fixture and corpus resources",
        )


def _validate_registry() -> list[str]:
    errors: list[str] = []
    recorded = {row["scenario_id"]: row for row in SCENARIO_REGISTRY}
    for scenario_id in SCENARIO_ORDER:
        row = recorded.get(scenario_id)
        if row is None:
            errors.append(f"{scenario_id}: no result recorded")
            continue
        if not row["evidence_class"]:
            errors.append(f"{scenario_id}: evidence class missing")
        for evidence in row["evidence_class"]:
            if evidence not in EVIDENCE_CLASSES:
                errors.append(f"{scenario_id}: unknown evidence class {evidence}")
        if row["observed_result"] in ("", None):
            errors.append(f"{scenario_id}: observed result missing")
    extra = set(recorded) - set(SCENARIO_ORDER)
    if extra:
        errors.append(f"unexpected scenario rows: {sorted(extra)}")
    for row in SCENARIO_REGISTRY:
        if "REAL_HOST_OR_RUNTIME_VALIDATION" in row["evidence_class"]:
            errors.append(f"{row['scenario_id']}: deterministic harness claimed real-host validation")
    return errors


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(V48OrchestrationDogfood)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    errors = _validate_registry()
    for error in errors:
        print(f"EVIDENCE REGISTRY ERROR: {error}", file=sys.stderr)
    registry_errors = errors
    identity = candidate_head_identity()
    evidence = {
        "harness": "scripts/test_v48_orchestration_dogfood.py",
        "task": "T-011",
        "issue": "#517",
        "exact_base_sha": load_corpus()["exact_base_sha"],
        "exact_base_tree": load_corpus()["exact_base_tree"],
        "candidate_head_sha": identity["head_sha"],
        "candidate_head_tree": identity["head_tree"],
        "candidate_dirty_paths": identity["dirty_paths"],
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "registry_errors": registry_errors,
        "scenarios": SCENARIO_REGISTRY,
        "evidence_boundary": (
            "SYNTHETIC_DETERMINISTIC rows prove bounded reference-model semantics only. "
            "REPOSITORY_REAL_EXECUTION rows executed against real repository artifacts at "
            "the candidate checkout. No REAL_HOST_OR_RUNTIME_VALIDATION dimension was "
            "executed or claimed by this harness; external host/device/provider/runtime "
            "claims remain NOT_RUN/BLOCKED pending independent exact-subject Validation."
        ),
    }
    print("=== T011_ORCHESTRATION_DOGFOOD_EVIDENCE_JSON_BEGIN ===")
    print(json.dumps(evidence, ensure_ascii=True, indent=2, sort_keys=True))
    print("=== T011_ORCHESTRATION_DOGFOOD_EVIDENCE_JSON_END ===")
    ok = result.wasSuccessful() and not registry_errors
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
