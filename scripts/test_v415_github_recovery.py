"""Local source-contract oracles for frozen #1235 P1-P6/R1-R6/G01-G24.

The isolated model below is NOT an ADS runtime, acceptance authority, native CAS
adapter or physical-effect verifier. Its input facts are test premises, never
observations about S01/S04. Separately exercise the REAL existing shape validator
and the adjacent single-writer adapter; source linkage alone is not behavior proof.
No new protocol/schema/event family or runtime dependency is introduced.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, replace
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import jsonschema
import yaml

from verify_github_structured_interaction import ContractError, verify_markdown
from test_v411_t06_claim_admission import ClaimAdmissionAdapter, proposal as adjacent_proposal

ROOT = Path(__file__).resolve().parents[1]
KEY = "kaicreator-mm/ai-development-standard#1237:builder:__default__"
BASE = "9d253c8efd1035b8861122e4cb7e1c062674b0f4"
PRODUCT_BLOB = "b2fdb026952b94b855f54320588261eaa2e57108"


@dataclass(frozen=True)
class Facts:
    # Default is the fully evidenced G19 source-only positive premise.
    refs_complete: bool | None = True
    common_writer: bool | None = True
    old_outcome: str = "REJECTED"
    old_active: bool = False
    revoked: bool | None = True
    consumers_fenced: bool | None = True
    generation: int | None = 7
    external_effects_resolved: bool | None = True
    source_excluded: bool | None = True
    current: bool | None = True
    permissions: bool | None = True
    blocker: bool = False
    deployment: bool = False
    heartbeat_missing: bool = False
    original_chat_available: bool = False
    old_process_observed_stopped: bool = False
    impersonation: bool = False
    guessed_counter: bool = False
    late: str = "NONE"
    phase: str = "RECOVERY"
    merge_acknowledged: bool | None = True
    candidate_validated: bool = False


def recovery_decision(f: Facts) -> str:
    """Pure test model; outputs are derived dispositions, not Gate states."""
    if f.impersonation or f.guessed_counter:
        return "REJECT"
    if f.phase == "MERGE_RESULT" and f.merge_acknowledged is not True:
        return "UNRATIFIED"
    if f.late == "OMITTED_ACCEPTED":
        return "HOLD"
    if (f.refs_complete is not True or f.common_writer is not True
            or f.old_outcome not in {"ACCEPTED", "REJECTED"} or f.old_active
            or f.revoked is not True or f.consumers_fenced is not True
            or f.generation is None or f.generation < 0
            or f.external_effects_resolved is not True or f.deployment
            or f.source_excluded is not True):
        return "HOLD"
    if f.late == "REVOKED_PROPOSAL":
        return "STALE"
    if f.late == "RECONCILED_RESULT":
        return "HISTORICAL_ONLY"
    if f.current is not True or f.permissions is not True or f.blocker:
        return "HOLD"
    if f.phase == "VALIDATION" and not f.candidate_validated:
        return "VALIDATION_NOT_RUN"
    if f.phase == "INTEGRATED":
        return "CONCERN_ONLY" if f.candidate_validated else "HOLD"
    return "CONTINUE_TO_ADMISSION"


class SourceContractTests(unittest.TestCase):
    def test_canonical_owners_and_consumers_link_without_schema_extension(self):
        exe = (ROOT / "standards/EXECUTION_ARCHITECTURE_STANDARD.md").read_text(encoding="utf-8")
        recovery = exe.split("### 23.1 ", 1)[1].split("## 24.", 1)[0]
        for section in ("### 23.2", "### 23.3", "### 23.4"):
            self.assertIn(section, recovery)
        # Wiring checks only; behavioral assertions are separate below.
        for anchor in ("SHAPE_VALID_ONLY", "section 29.1", "section 27.4",
                       "exact current generation", "pre-revocation", "post-revocation",
                       "HOLD successor/downstream", "physical-fence", "next receiving owner/action"):
            self.assertIn(anchor, recovery)
        for path in ("standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md",
                     "templates/agent-event-comment.md", "templates/local-agent-handoff-issue.md",
                     "references/MANUAL_REFERENCE_FLOW_V49.md"):
            text = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("23.", text, path)
        self.assertIn("UNKNOWN forbids", recovery)
        self.assertIn("not a new record family", (ROOT / "standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md").read_text(encoding="utf-8"))


class ExistingPreflightTests(unittest.TestCase):
    def record(self, state="CLAIMED"):
        event = {"schema": "ai-dev/event-v2", "event": "DISPATCH_CLAIMED",
                 "actor_role": "builder", "operator_kind": "codex", "operator_id": "codex:test",
                 "session_ref": "local-model", "transport_actor": "kaicreator-mm", "task": "#1237",
                 "sha": BASE, "standard_revision": BASE, "expected_base_sha": BASE,
                 "dispatch_id": "dispatch:local-test", "dispatch_state": state,
                 "execution_profile": "LOCAL_BUILDER", "task_pack_ref": "https://github.com/kaicreator-mm/ai-development-standard/issues/1237"}
        return "<!-- ads:github -->\n```yaml\n" + yaml.safe_dump(
            {"schema": "ads/github/v3", "kind": "event", "data": event}, sort_keys=False) + "```\n"

    def test_real_shape_validator_rejects_original_running_claim(self):
        with self.assertRaises(ContractError):
            verify_markdown(self.record("RUNNING"), "event")

    def test_shape_success_does_not_authorize_unknown_frontier(self):
        self.assertEqual("SHAPE_VALID_ONLY", verify_markdown(self.record(), "event"))
        self.assertEqual("HOLD", recovery_decision(Facts(generation=None)))

    def dispatch(self):
        return {"dispatch_id": "dispatch:local-test", "repository": "kaicreator-mm/ai-development-standard",
                "version": "v4.15", "task": "#1237", "issue": "#1237", "role": "builder",
                "execution_profile": "LOCAL_BUILDER", "branch": "codex/local-test",
                "expected_base_sha": BASE, "requested_head_sha": BASE, "pinned_standard_revision": BASE,
                "agent_freedom": "F1_BOUNDED_IMPLEMENTATION", "dispatch_state": "READY",
                "task_pack_ref": "https://github.com/kaicreator-mm/ai-development-standard/issues/1237"}

    def validator(self):
        return jsonschema.Draft202012Validator(json.loads(
            (ROOT / "schemas/dispatch.schema.json").read_text(encoding="utf-8")))

    def test_real_dispatch_schema_valid_ready_and_malformed_counterexamples(self):
        self.validator().validate(self.dispatch())
        for field, value in (("role", "scheduler"), ("execution_profile", "LOCAL_VALIDATOR"),
                             ("dispatch_state", "DONE"), ("expected_base_sha", "short-sha")):
            with self.subTest(field=field):
                invalid = {**self.dispatch(), field: value}
                with self.assertRaises(jsonschema.ValidationError):
                    self.validator().validate(invalid)
        missing = self.dispatch()
        del missing["task_pack_ref"]
        with self.assertRaises(jsonschema.ValidationError):
            self.validator().validate(missing)

    def test_shape_pair_unknown_semantics_and_stale_exact_subject_never_admit(self):
        self.assertEqual("SHAPE_VALID_ONLY", verify_markdown(self.record(), "event"))
        self.validator().validate(self.dispatch())
        # Schema accepts any syntactically valid SHA: exact identity is a
        # separate engineering predicate, checked by the existing adapter.
        stale = {**self.dispatch(), "requested_head_sha": "a" * 40}
        self.validator().validate(stale)
        harness = RecoveryApplicationHarness()
        proposal = replace(harness.proposal, head_sha=stale["requested_head_sha"])
        before = harness.snapshot()
        self.assertEqual("INELIGIBLE", harness.apply(Facts(), proposal=proposal))
        self.assertEqual(before, harness.snapshot())
        for facts in (Facts(current=None), Facts(generation=None),
                      Facts(external_effects_resolved=None)):
            with self.subTest(facts=facts):
                before = harness.snapshot()
                self.assertEqual("HOLD", harness.apply(facts, event=self.record(), dispatch=self.dispatch()))
                self.assertEqual(before, harness.snapshot())
        # An actual required binding whose capacity is unknown is another
        # engineering failure, even when both source shapes are valid.
        harness.adapter.resources.capacity.clear()
        before = harness.snapshot()
        self.assertEqual("INELIGIBLE", harness.apply(Facts(), event=self.record(), dispatch=self.dispatch()))
        self.assertEqual(before, harness.snapshot())


class RecoveryApplicationHarness:
    """Isolated same-key fence + existing stateful admission adapter, NOT runtime.

    Every recovery attempt (including a shape failure or old revoked request)
    goes through apply. Only a permitted decision can call the actual adjacent
    adapter. Source effects additionally require its accepted binding. This is a
    bounded executable application model of R4; fixture facts are not observations.
    """

    def __init__(self, active="none"):
        self.adapter = ClaimAdmissionAdapter(capacity={"host": 2})
        self.adapter.generations[KEY] = 7  # exact known fixture frontier
        self.proposal = adjacent_proposal(self.adapter, key=KEY, operator="successor",
                                          resources=(("host", 1),))
        self.source_effects = []
        self.existing = None
        if active != "none":
            old = replace(self.proposal, operator="old" if active == "old" else "successor")
            accepted = self.adapter.admit(old)
            assert accepted.status == "ACCEPTED"
            self.existing = accepted.detail
            self.proposal = adjacent_proposal(self.adapter, key=KEY, operator="successor",
                                              resources=(("host", 1),))

    def snapshot(self):
        # Include full durable contents, not only event counts: claim/dispatch,
        # exact generation, bound capacity, publication history and source effects.
        state = {**vars(self.adapter), "resources": vars(self.adapter.resources)}
        return deepcopy({"adapter": state, "effects": self.source_effects})

    def permits(self, decision):
        return decision == "CONTINUE_TO_ADMISSION"

    def apply(self, facts, *, event=None, dispatch=None, proposal=None, source=False):
        if event is not None:
            try:
                verify_markdown(event, "event")
            except ContractError:
                return "REJECT"
        if dispatch is not None:
            validator = ExistingPreflightTests().validator()
            if not validator.is_valid(dispatch):
                return "REJECT"
        decision = recovery_decision(facts)
        if not self.permits(decision):
            return decision
        if source:
            # This branch models an already-started successor when G23 exposes
            # a false fence. It must recheck the fence before another effect.
            if self.existing is None:
                return "HOLD"
            self.source_effects.append({"binding": self.existing, "effect": "source-write"})
            return "ACCEPTED"
        accepted = self.adapter.admit(proposal or self.proposal)
        if accepted.status == "ACCEPTED":
            self.source_effects.append({"binding": accepted.detail, "effect": "source-write"})
        return accepted.status


# Explicit expected results derive from the immutable frozen Product cases, not
# the implementation's current prose or a self-generated expected-result file.
CASES = [
    ("G01", Facts(original_chat_available=False), "CONTINUE_TO_ADMISSION"),
    ("G02", Facts(generation=None), "HOLD"),
    ("G03", Facts(generation=None, heartbeat_missing=True), "HOLD"),
    ("G04", Facts(old_outcome="ACCEPTED", old_active=True), "HOLD"),
    ("G05", Facts(refs_complete=False), "HOLD"),
    ("G06", Facts(external_effects_resolved=False), "HOLD"),
    ("G07", Facts(deployment=True), "HOLD"),
    ("G08", Facts(old_outcome="UNCERTAIN"), "HOLD"),
    ("G09", Facts(guessed_counter=True), "REJECT"),
    ("G10", Facts(refs_complete=False, generation=100), "HOLD"),
    ("G11", Facts(original_chat_available=False), "CONTINUE_TO_ADMISSION"),
    ("G12", Facts(current=False), "HOLD"),
    ("G13", Facts(phase="VALIDATION", candidate_validated=False), "VALIDATION_NOT_RUN"),
    ("G14", Facts(blocker=True), "HOLD"),
    ("G15", Facts(permissions=False), "HOLD"),
    ("G16", Facts(phase="MERGE_RESULT", merge_acknowledged=None), "UNRATIFIED"),
    ("G17", Facts(phase="INTEGRATED", candidate_validated=True), "CONCERN_ONLY"),
    ("G18", Facts(impersonation=True), "REJECT"),
    ("G19", Facts(old_process_observed_stopped=False), "CONTINUE_TO_ADMISSION"),
    ("G20", Facts(late="REVOKED_PROPOSAL"), "STALE"),
    ("G21", Facts(external_effects_resolved=None), "HOLD"),
    ("G22", Facts(old_outcome="ACCEPTED", old_active=True), "HOLD"),
    ("G23", Facts(late="OMITTED_ACCEPTED"), "HOLD"),
    ("G24", Facts(old_outcome="ACCEPTED", late="RECONCILED_RESULT"), "HISTORICAL_ONLY"),
]


class RecoveryDecisionTests(unittest.TestCase):
    def test_expected_oracle_is_pinned_to_independently_frozen_product(self):
        # Hard-coded expected dispositions above are the selected admission
        # limbs of this independently reviewed immutable Product, not generated
        # from recovery_decision() or the mutable implementation owner prose.
        content = (ROOT / "docs/intake/i1235-github-recovery/PROPOSAL.md").read_text(encoding="utf-8").encode()
        blob = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
        self.assertEqual(PRODUCT_BLOB, blob)
        for case, _, _ in CASES:
            self.assertIn(("| " + case + " | ").encode(), content)

    def test_all_frozen_scenario_admission_limbs_have_explicit_oracles(self):
        self.assertEqual([f"G{i:02}" for i in range(1, 25)], [x[0] for x in CASES])
        for case, facts, expected in CASES:
            with self.subTest(case=case):
                self.assertEqual(expected, recovery_decision(facts))

    def test_each_fence_and_currentness_predicate_is_necessary_including_unknown(self):
        for field in ("refs_complete", "common_writer", "revoked", "consumers_fenced",
                      "external_effects_resolved", "source_excluded", "current", "permissions"):
            for value in (False, None):
                with self.subTest(field=field, value=value):
                    self.assertEqual("HOLD", recovery_decision(replace(Facts(), **{field: value})))

    def test_original_chat_and_heartbeat_never_grant_or_remove_authority(self):
        for available in (True, False):
            for missing in (True, False):
                self.assertEqual("CONTINUE_TO_ADMISSION", recovery_decision(Facts(
                    original_chat_available=available, heartbeat_missing=missing)))
                self.assertEqual("HOLD", recovery_decision(Facts(
                    original_chat_available=available, heartbeat_missing=missing, generation=None)))

    def test_larger_number_cannot_replace_common_authority_or_pending_resolution(self):
        for number in (0, 1, 7, 10**12):
            self.assertEqual("HOLD", recovery_decision(Facts(generation=number, common_writer=False)))
            self.assertEqual("HOLD", recovery_decision(Facts(generation=number, old_outcome="UNCERTAIN")))


class RecoveryApplicationTests(unittest.TestCase):
    def test_all_noncontinuing_scenario_actions_preserve_full_accepted_state(self):
        for case, facts, expected in CASES:
            if expected == "CONTINUE_TO_ADMISSION":
                continue
            with self.subTest(case=case):
                # G22 retains a genuinely accepted active old binding; G23
                # retains the already-started successor and stops further work.
                active = "old" if case in {"G04", "G22"} else "successor" if case == "G23" else "none"
                harness = RecoveryApplicationHarness(active=active)
                before = harness.snapshot()
                proposal = replace(harness.proposal, operator="old") if case == "G20" else harness.proposal
                self.assertEqual(expected, harness.apply(facts, proposal=proposal, source=(case == "G23")))
                self.assertEqual(before, harness.snapshot())

    def test_g19_positive_reaches_real_composite_admission_and_bound_effect_once(self):
        harness = RecoveryApplicationHarness()
        before = harness.snapshot()
        self.assertEqual("ACCEPTED", harness.apply(dict((c, f) for c, f, _ in CASES)["G19"]))
        after = harness.snapshot()
        self.assertNotEqual(before, after)
        self.assertEqual(8, harness.adapter.current_generation(KEY))
        self.assertEqual(1, harness.adapter.resources.active["host"])
        dispatch = harness.adapter.active_claim_on(KEY)
        self.assertEqual("successor", dispatch.claim.operator)
        self.assertEqual((("host", 1),), harness.adapter.bound_resources[dispatch.dispatch_id])
        self.assertEqual(1, len(harness.source_effects))
        self.assertEqual("DISPATCH_CLAIMED", harness.adapter.events[-1]["type"])
        before_retry = harness.snapshot()
        self.assertEqual("STALE", harness.apply(Facts()))
        self.assertEqual(before_retry, harness.snapshot())

    def test_shape_failure_blocks_actual_application_not_a_local_append(self):
        for kwargs in ({"event": ExistingPreflightTests().record("RUNNING")},
                       {"dispatch": {**ExistingPreflightTests().dispatch(), "role": "scheduler"}}):
            with self.subTest(kwargs=kwargs):
                harness = RecoveryApplicationHarness()
                before = harness.snapshot()
                self.assertEqual("REJECT", harness.apply(Facts(), **kwargs))
                self.assertEqual(before, harness.snapshot())
        harness = RecoveryApplicationHarness()
        self.assertEqual("ACCEPTED", harness.apply(Facts(), event=ExistingPreflightTests().record(),
                                                   dispatch=ExistingPreflightTests().dispatch()))

    def test_guard_bypass_mutants_are_detected_by_the_same_state_invariant(self):
        # Demonstrate the exact review counterexample: leave disposition strings
        # correct but bypass their application guard. The invariant MUST detect
        # real accepted state/effect changes, not simply reassert a return string.
        cases = {c: f for c, f, _ in CASES}
        for case in ("G08", "G10", "G20", "G23"):
            with self.subTest(case=case):
                harness = RecoveryApplicationHarness(active="successor" if case == "G23" else "none")
                before = harness.snapshot()
                with patch.object(harness, "permits", return_value=True):
                    proposal = replace(harness.proposal, operator="old") if case == "G20" else harness.proposal
                    harness.apply(cases[case], proposal=proposal, source=(case == "G23"))
                with self.assertRaises(AssertionError):
                    self.assertEqual(before, harness.snapshot())

class ExistingSerializedAdapterTests(unittest.TestCase):
    def test_genuine_adjacent_adapter_rejects_stale_claim_with_zero_mutation(self):
        adapter = ClaimAdmissionAdapter()
        proposal = adjacent_proposal(adapter, key=KEY, operator="worker", session="one", origin="LOCAL")
        result = adapter.admit(proposal)
        self.assertEqual("ACCEPTED", result.status)
        before = adapter.snapshot()
        late = adapter.admit(replace(proposal, operator="late-old-writer", session="old"))
        self.assertEqual("STALE", late.status)
        self.assertEqual(before, adapter.snapshot())

    def test_pending_admission_and_failed_readback_do_not_advance_or_release(self):
        for unavailable in (False, True):
            adapter = ClaimAdmissionAdapter(capacity={"host": 1})
            proposal = adjacent_proposal(adapter, key=KEY, resources=(("host", 1),))
            if unavailable:
                adapter.readback_unavailable = True
            else:
                adapter.ambiguous_keys.add(KEY)
            before = adapter.snapshot()
            self.assertEqual("UNKNOWN", adapter.admit(proposal).status)
            self.assertEqual(before, adapter.snapshot())

    def test_recovery_claim_is_not_validation_and_cannot_wake_dependency(self):
        adapter = ClaimAdmissionAdapter()
        proposal = adjacent_proposal(adapter, key=KEY)
        admitted = adapter.admit(proposal)
        self.assertEqual("ACCEPTED", admitted.status)
        for evidence in (None, {"kind": "claim", "subject": admitted.detail, "status": "PASS"},
                         {"kind": "validation", "subject": "old-head", "status": "PASS"}):
            before = adapter.snapshot()
            self.assertEqual("BLOCKED", adapter.attempt_wake("downstream", evidence).status)
            self.assertEqual(before, adapter.snapshot())


if __name__ == "__main__":
    unittest.main(verbosity=2)
