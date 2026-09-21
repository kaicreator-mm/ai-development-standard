from __future__ import annotations

import copy
from pathlib import Path
import unittest

from test_protocol_schemas import load_schema, validate_subset

ROOT = Path(__file__).resolve().parents[1]
SHA_A = "1111111111111111111111111111111111111111"
SHA_B = "2222222222222222222222222222222222222222"
SHA_C = "3333333333333333333333333333333333333333"
TREE = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


class V33LifecycleContractRegression(unittest.TestCase):
    def text(self, rel: str) -> str:
        return (ROOT / rel).read_text(encoding="utf-8")

    def event(self, event: str, actor_role: str, **overrides):
        value = {
            "schema": "ai-dev/event-v2",
            "event": event,
            "actor_role": actor_role,
            "operator_kind": "chatgpt-web",
            "operator_id": "chatgpt-web:v33-contract-test",
            "session_ref": "v33-contract-test",
            "transport_actor": "github:kaicreator-mm",
        }
        value.update(overrides)
        return value

    def ready_handoff(self):
        return {
            "repository": "kaicreator-mm/ai-development-standard",
            "issue": "#38",
            "standard_version": "3.3.0",
            "standard_revision": SHA_A,
            "integration_target": "version/v3.3.0",
            "baseline_sha": SHA_B,
            "role": "validator",
            "scope": ["v3.3 release validation"],
            "frozen_inputs": ["Issue #38", "PR #39"],
            "existing_evidence": ["GitHub Actions exact-SHA run"],
            "remaining_work": ["run closure profile"],
            "required_gates": ["verify-standard"],
            "validation_tuples": ["exact SHA x ubuntu-latest x Python 3.12 x closure"],
            "validation_profile": "closure",
            "execution_environment": "trusted clean ubuntu runner",
            "canonical_entrypoints": ["python scripts/verify_standard.py"],
            "allowed_changes": ["none; validation-only"],
            "forbidden_changes": ["frozen product or architecture semantics"],
            "completion_rule": "all required gates PASS or explicit FAIL/BLOCKED evidence",
            "blocker_rule": "publish exact reproduction and downstream impact",
            "expected_output": ["exact tested SHA", "validation evidence"],
            "handoff_state": "HANDOFF_READY",
        }

    def test_handoff_ready_requires_normative_completeness(self) -> None:
        schema = load_schema("local-agent-handoff.schema.json")
        valid = self.ready_handoff()
        self.assertEqual(validate_subset(valid, schema), [])

        required_when_ready = [
            "standard_version",
            "standard_revision",
            "frozen_inputs",
            "existing_evidence",
            "validation_tuples",
            "execution_environment",
            "canonical_entrypoints",
            "required_gates",
        ]
        for field in required_when_ready:
            malformed = copy.deepcopy(valid)
            del malformed[field]
            with self.subTest(field=field):
                errors = validate_subset(malformed, schema)
                self.assertTrue(any(field in error for error in errors), errors)

        draft = {
            "repository": valid["repository"],
            "issue": valid["issue"],
            "handoff_state": "DRAFT",
        }
        self.assertEqual(validate_subset(draft, schema), [])

    def test_dispatched_handoff_requires_dispatch_identity(self) -> None:
        schema = load_schema("local-agent-handoff.schema.json")
        dispatched = self.ready_handoff()
        dispatched["handoff_state"] = "DISPATCHED"

        missing = copy.deepcopy(dispatched)
        self.assertTrue(any("dispatch_id" in e for e in validate_subset(missing, schema)))

        null_identity = copy.deepcopy(dispatched)
        null_identity["dispatch_id"] = None
        self.assertTrue(validate_subset(null_identity, schema), null_identity)

        empty_identity = copy.deepcopy(dispatched)
        empty_identity["dispatch_id"] = ""
        self.assertTrue(validate_subset(empty_identity, schema), empty_identity)

        dispatched["dispatch_id"] = "dispatch-v33-001"
        self.assertEqual(validate_subset(dispatched, schema), [])

    def test_ci_infra_exception_requires_equivalence_and_policy_facts(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        valid = self.event(
            "CI_INFRA_EXCEPTION",
            "validator",
            sha=SHA_A,
            candidate_sha=SHA_A,
            provider="woodpecker",
            execution_channel="self-hosted-ci",
            provider_state="INFRA_BLOCKED",
            validation_profile="minimal-ci",
            alternate_executor="trusted-clean-build-host",
            alternate_evidence="issue:#38 comment:alternate-executor-pass",
            policy_basis="authority requires profile, not provider-specific attestation",
            remaining_impact="normal provider unavailable; validation profile satisfied by equivalent executor",
            reason="provider queue unavailable",
        )
        self.assertEqual(validate_subset(valid, schema), [])

        for field in (
            "candidate_sha",
            "execution_channel",
            "validation_profile",
            "alternate_executor",
            "alternate_evidence",
            "policy_basis",
            "remaining_impact",
        ):
            malformed = dict(valid)
            del malformed[field]
            with self.subTest(field=field):
                errors = validate_subset(malformed, schema)
                self.assertTrue(any(field in error for error in errors), errors)

    def test_frozen_candidate_requires_operational_freeze_identity(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        valid = self.event(
            "CANDIDATE_STATE_CHANGED",
            "release-controller",
            candidate_sha=SHA_A,
            tree_sha=TREE,
            candidate_state="FROZEN",
            candidate_ref="version/v3.3.0",
            visible_closure_evidence="issue:#38 visible-closure-pass",
            standard_revision=SHA_B,
            occurred_at="2026-09-20T14:00:00Z",
            reason="all required visible freeze gates passed",
        )
        self.assertEqual(validate_subset(valid, schema), [])

        for field in ("candidate_ref", "visible_closure_evidence", "standard_revision", "occurred_at"):
            malformed = dict(valid)
            del malformed[field]
            with self.subTest(field=field):
                errors = validate_subset(malformed, schema)
                self.assertTrue(any(field in error for error in errors), errors)

        prepared = self.event(
            "CANDIDATE_STATE_CHANGED",
            "release-controller",
            candidate_sha=SHA_A,
            tree_sha=TREE,
            candidate_state="PREPARED",
            reason="candidate identity prepared before freeze",
        )
        self.assertEqual(validate_subset(prepared, schema), [])

    def impact_event(self, impact: str, reusable: bool, **overrides):
        value = self.event(
            "VALIDATION_IMPACT_DECISION",
            "merge-controller",
            validated_head_sha=SHA_A,
            base_sha_at_validation=SHA_B,
            current_target_sha=SHA_C,
            validation_impact=impact,
            evidence_reusable=reusable,
            evidence_reuse_basis="explicit write-set/build-input analysis",
        )
        value.update(overrides)
        return value

    def test_validation_impact_none_requires_composition_evidence(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        valid = self.impact_event(
            "none",
            True,
            base_delta_evidence="target delta changes unrelated documentation only",
            merge_result_tree=TREE,
        )
        self.assertEqual(validate_subset(valid, schema), [])

        missing_delta = dict(valid)
        del missing_delta["base_delta_evidence"]
        self.assertTrue(any("base_delta_evidence" in e for e in validate_subset(missing_delta, schema)))

        missing_merge_tree = dict(valid)
        del missing_merge_tree["merge_result_tree"]
        self.assertTrue(any("merge_result_tree" in e for e in validate_subset(missing_merge_tree, schema)))

        false_reuse = dict(valid, evidence_reusable=False)
        self.assertTrue(validate_subset(false_reuse, schema), false_reuse)

    def test_affected_or_unknown_impact_cannot_claim_evidence_reuse(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        for impact in ("affected", "unknown"):
            valid = self.impact_event(impact, False)
            with self.subTest(impact=impact, reusable=False):
                self.assertEqual(validate_subset(valid, schema), [])
            invalid = self.impact_event(impact, True)
            with self.subTest(impact=impact, reusable=True):
                self.assertTrue(validate_subset(invalid, schema), invalid)

    def test_handoff_ready_event_links_machine_evidence(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        valid = self.event(
            "HANDOFF_READY",
            "scheduler",
            issue="#31",
            sha=SHA_A,
            evidence="validated schemas/local-agent-handoff.schema.json payload",
        )
        self.assertEqual(validate_subset(valid, schema), [])
        malformed = dict(valid)
        del malformed["evidence"]
        self.assertTrue(any("evidence" in e for e in validate_subset(malformed, schema)))

    def test_issue24_ci_is_finalized_before_expensive_exact_sha_validation(self) -> None:
        workflow = self.text("standards/DEVELOPMENT_WORKFLOW.md")
        ci = workflow.index("#### 4.2 PR + Minimal CI Before Expensive Validation")
        expensive = workflow.index("#### 4.3 Expensive / Real-host Task-owned Validation")
        self.assertLess(ci, expensive)
        for token in (
            "finalize PR + CI/workflow/config",
            "configured Minimal CI on current exact SHA",
            "CI/workflow/config change 不是默认的 evidence-only commit",
            "旧 evidence 只属于原 tested SHA",
        ):
            self.assertIn(token, workflow)

    def test_issue25_validation_ownership_is_tiered(self) -> None:
        architecture = self.text("standards/EXECUTION_ARCHITECTURE_STANDARD.md")
        workflow = self.text("standards/DEVELOPMENT_WORKFLOW.md")
        for token in ("concern", "integration", "closure"):
            self.assertIn(token, architecture)
        self.assertIn("A leaf Task MUST NOT automatically inherit the complete release matrix", architecture)
        self.assertIn("Gate ownership 仍按 `concern | integration | closure` 分层", workflow)
        self.assertIn("full regression / release CJ / platform matrix / packaging / Hidden 由 version closure 负责", workflow)

    def test_issue26_intent_admission_has_one_protocol_authority(self) -> None:
        protocol = self.text("standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md")
        architecture = self.text("standards/EXECUTION_ARCHITECTURE_STANDARD.md")
        for token in (
            "canonical short-intent admission / normalization / rejection semantics",
            "A short intent/result is a transport input, not yet a durable canonical workflow fact",
            "INVALID_SCHEMA",
            "AMBIGUOUS_IDENTITY",
            "STALE_IDENTITY",
            "UNAUTHORIZED",
            "ILLEGAL_TRANSITION",
            "MUST NOT define a second intent contract",
        ):
            self.assertIn(token, protocol)
        for token in (
            "owned exclusively by `GITHUB_AGENT_INTERACTION_PROTOCOL.md`",
            "consumes only intents that have already passed that protocol",
            "MUST NOT define a parallel intent schema",
        ):
            self.assertIn(token, architecture)

    def test_issue30_hidden_blind_spot_requires_successor_pack_lifecycle(self) -> None:
        release = self.text("standards/RELEASE_STANDARD.md")
        for token in (
            "HIDDEN_PACK_BLIND_SPOT",
            "BOTH_VISIBLE_AND_HIDDEN_GAP",
            "new immutable private pack identity/revision/checksum",
            "fix/successor candidate",
            "new freeze",
            "new Release Qualification",
        ):
            self.assertIn(token, release)

    def test_issue32_new_writer_cannot_regress_to_v1(self) -> None:
        protocol = self.text("standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md")
        self.assertIn("All newly emitted structured Agent events MUST use", protocol)
        self.assertIn("New writers MUST NOT emit v1", protocol)
        for rel in (
            "standards/GITHUB_WORKFLOW.md",
            "standards/VERSION_INTEGRATION_WORKFLOW.md",
            "standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md",
            "templates/local-agent-handoff-issue.md",
        ):
            text = self.text(rel)
            self.assertIn("ai-dev:event:v2", text)
            self.assertNotIn("publish `ai-dev:event:v1`", text)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(V33LifecycleContractRegression)
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
