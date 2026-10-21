"""Local source-contract oracles for frozen #1235 P1-P6/R1-R6/G01-G24.

The isolated model below is NOT an ADS runtime, acceptance authority, native CAS
adapter or physical-effect verifier. Its input facts are test premises, never
observations about S01/S04. Separately exercise the REAL existing shape validator
and the adjacent single-writer adapter; source linkage alone is not behavior proof.
No new protocol/schema/event family or runtime dependency is introduced.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import unittest

import yaml

from verify_github_structured_interaction import ContractError, verify_markdown
from test_v411_t06_claim_admission import ClaimAdmissionAdapter, proposal as adjacent_proposal

ROOT = Path(__file__).resolve().parents[1]
KEY = "kaicreator-mm/ai-development-standard#1237:builder:__default__"
BASE = "9d253c8efd1035b8861122e4cb7e1c062674b0f4"


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

    def test_real_shape_validator_rejects_original_running_claim_before_effect(self):
        effects = []
        with self.assertRaises(ContractError):
            verdict = verify_markdown(self.record("RUNNING"), "event")
            effects.append(verdict)  # unreachable on schema failure
        self.assertEqual([], effects)

    def test_shape_success_does_not_authorize_unknown_frontier(self):
        self.assertEqual("SHAPE_VALID_ONLY", verify_markdown(self.record(), "event"))
        self.assertEqual("HOLD", recovery_decision(Facts(generation=None)))


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
