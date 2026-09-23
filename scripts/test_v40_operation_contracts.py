from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from test_protocol_schemas import load_schema, validate_subset
from v40_rules import (
    canonical_semantic_action_key,
    fast_path_eligible,
    validate_assurance_semantics,
    validate_candidate_release_separation,
    validate_finding_disposition,
    validate_hidden_metadata,
    validate_review_aggregation,
    validate_subject_identity,
    validate_validation_result,
)

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "templates" / "golden" / "V4_OPERATION_ASSURANCE_EXAMPLES.json"
SHA_A = "a" * 40
SHA_B = "b" * 40
TREE_A = "c" * 40


def operation_example() -> dict:
    return {
        "protocol_version": "ai-dev-operation/v1",
        "operation_id": "op:T009:implementation",
        "operation_type": "implementation",
        "operation_kind": "PRODUCE",
        "authority_ref": "issue:#81",
        "work_item_ref": "#81",
        "subject": {
            "ref": "PR:#118",
            "identity_binding": "project-defined",
            "owning_required_binding": "exact-sha",
            "identity": {"sha": SHA_A, "project_key": "t009-candidate"},
        },
        "actor_contract": {"role": "builder", "authority_ref": "issue:#81"},
        "inputs": ["task-pack:T009", "standard:4.0.0"],
        "assurance_plan_ref": "assurance:T009",
        "acceptance_criteria": ["v4 machine contracts validate", "focused regressions pass"],
        "failure_routes": ["changes-requested", "blocked"],
        "next_operations": ["assure:T009"],
    }


def binding_example() -> dict:
    return {
        "protocol_version": "ai-dev/operation-binding-v1",
        "operation_id": "op:T009:implementation",
        "operation_kind": "PRODUCE",
        "parent_operation_ref": "version:#72",
        "authority_mode": "CORRELATION_ONLY_NON_AUTHORITATIVE",
    }


def assurance_example() -> dict:
    return {
        "protocol_version": "ai-dev-assurance/v1",
        "assurance_plan_id": "assurance:T009",
        "operation_id": "op:T009:implementation",
        "subject_ref": "PR:#118",
        "subject_identity_ref": f"sha:{SHA_A}",
        "activities": [
            {
                "assurance_id": "review-a",
                "kind": "review",
                "policy": "required",
                "mode": "model-diverse-adversarial",
                "coverage": ["schema-nonweakening", "aggregation", "compatibility"],
                "independence": {
                    "context": "required",
                    "model": "required",
                    "executor": "none",
                    "evidence": "none",
                },
                "depends_on": [],
                "blind_first_pass_ref": "evidence:review-a-blind",
                "collaboration_selected": False,
            },
            {
                "assurance_id": "validation-a",
                "kind": "validation",
                "policy": "required",
                "mode": "executable-validation",
                "coverage": ["focused-v4-regression", "full-repository-verifier"],
                "independence": {
                    "context": "none",
                    "model": "none",
                    "executor": "required",
                    "evidence": "required",
                },
                "depends_on": ["review-a"],
                "collaboration_selected": False,
            },
        ],
        "aggregation": {
            "policy": "finding-union-blocker-dominance",
            "blocker_resolution": "unresolved-valid-blocker-dominates",
            "majority_vote_for_correctness": False,
            "conflict_route": "validation-needed",
        },
        "completion_predicate": "all required activities dispositioned on exact subject identity",
    }


def finding_example(finding_id: str, severity: str, disposition: str) -> dict:
    return {
        "protocol_version": "ai-dev/review-finding-v1",
        "finding_id": finding_id,
        "assurance_id": "review-a",
        "subject_identity_ref": f"sha:{SHA_A}",
        "severity": severity,
        "summary": "durable review finding",
        "blocking": False,
        "status": "DISPOSITIONED",
        "disposition": disposition,
        "evidence_refs": ["issue:#81"],
    }


def aggregation_example() -> dict:
    return {
        "protocol_version": "ai-dev/review-aggregation-v1",
        "aggregate_id": "agg:T009",
        "assurance_plan_id": "assurance:T009",
        "subject_identity_ref": f"sha:{SHA_A}",
        "judgment": "PASS",
        "requested_route": "merge-ready",
        "aggregation_policy": "finding-union-blocker-dominance",
        "finding_refs": ["F-P2-1", "F-P3-1"],
        "unresolved_blocker_refs": [],
        "conflict_refs": [],
    }


def interchange_example() -> dict:
    return {
        "protocol_version": "ai-dev/interchange-v1",
        "exchange_id": "ex:T009:1",
        "exchange_type": "RESULT",
        "operation_id": "op:T009:implementation",
        "work_item_ref": "#81",
        "dispatch_id": "dispatch:T009:web",
        "assurance_id": "review-a",
        "subject_ref": "PR:#118",
        "subject_identity_ref": f"sha:{SHA_A}",
        "actor": {
            "actor_role": "reviewer",
            "operator_kind": "other",
            "operator_id": "fresh-reviewer",
            "session_ref": "session:1",
            "transport_actor": "github",
        },
        "causation": {
            "caused_by": "dispatch:T009:web",
            "correlation_refs": ["#81", "PR:#118"],
        },
        "payload_ref": "finding:F-P2-1",
        "occurred_at": "2026-09-24T00:00:00Z",
    }


class V40OperationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.examples = json.loads(GOLDEN.read_text(encoding="utf-8"))

    def test_golden_file_protocol(self) -> None:
        self.assertEqual(self.examples["schema"], "ai-dev/v4-golden-examples:1")
        self.assertIn("valid", self.examples)
        self.assertIn("forbidden", self.examples)

    def test_positive_examples_match_machine_schemas(self) -> None:
        cases = [
            ("operation-v1.schema.json", operation_example()),
            ("operation-binding-v1.schema.json", binding_example()),
            ("assurance-plan-v1.schema.json", assurance_example()),
            ("review-finding-v1.schema.json", finding_example("F-P2-1", "P2", "covered")),
            ("review-finding-v1.schema.json", finding_example("F-P3-1", "P3", "recorded")),
            ("review-aggregation-v1.schema.json", aggregation_example()),
            ("interchange-envelope-v1.schema.json", interchange_example()),
        ]
        for schema_name, value in cases:
            with self.subTest(schema=schema_name):
                self.assertEqual(validate_subset(value, load_schema(schema_name)), [])

    def test_project_defined_identity_is_non_weakening(self) -> None:
        valid_subject = self.examples["valid"]["project_defined_nonweakening_subject"]
        self.assertEqual(validate_subject_identity(valid_subject), [])

        forbidden = self.examples["forbidden"]["project_defined_weakens_exact_subject"]
        errors = validate_subject_identity(forbidden)
        self.assertTrue(errors)
        self.assertTrue(any("weakens" in error or "missing sha" in error for error in errors), errors)

    def test_operation_binding_is_correlation_only(self) -> None:
        binding = binding_example()
        self.assertEqual(binding["authority_mode"], "CORRELATION_ONLY_NON_AUTHORITATIVE")
        self.assertEqual(validate_subset(binding, load_schema("operation-binding-v1.schema.json")), [])

    def test_event_v2_remains_additive_and_event_enum_is_not_repurposed(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        self.assertTrue(schema["additionalProperties"])
        enum = schema["properties"]["event"]["enum"]
        for logical_exchange_type in ("REQUEST", "RESULT", "FINDING", "CHALLENGE", "CONTROL"):
            self.assertNotIn(logical_exchange_type, enum)

        event = {
            "schema": "ai-dev/event-v2",
            "event": "HANDOFF_READY",
            "actor_role": "reviewer",
            "operator_kind": "chatgpt-web",
            "operator_id": "web:reviewer",
            "issue": "#81",
            "sha": SHA_A,
            "evidence": "issue:#81",
            "operation_id": "op:T009",
            "exchange_id": "ex:T009:handoff",
            "assurance_id": "review:T009",
            "caused_by": "dispatch:T009",
        }
        self.assertEqual(validate_subset(event, schema), [])

    def test_assurance_forbids_majority_correctness_and_fake_independence(self) -> None:
        valid = assurance_example()
        self.assertEqual(validate_assurance_semantics(valid), [])

        majority = copy.deepcopy(valid)
        majority["aggregation"]["majority_vote_for_correctness"] = True
        self.assertTrue(validate_subset(majority, load_schema("assurance-plan-v1.schema.json")))
        self.assertTrue(any("majority" in e for e in validate_assurance_semantics(majority)))

        missing_blind = copy.deepcopy(valid)
        del missing_blind["activities"][0]["blind_first_pass_ref"]
        self.assertEqual(validate_subset(missing_blind, load_schema("assurance-plan-v1.schema.json")), [])
        self.assertTrue(any("blind first pass" in e for e in validate_assurance_semantics(missing_blind)))

        collaboration = copy.deepcopy(valid)
        collaboration["activities"][0]["collaboration_selected"] = True
        self.assertTrue(any("collaborative" in e for e in validate_assurance_semantics(collaboration)))

    def test_findings_are_durable_and_aggregation_never_votes_away_blockers(self) -> None:
        findings = [
            finding_example("F-P2-1", "P2", "covered by focused regression"),
            finding_example("F-P3-1", "P3", "recorded and dispositioned"),
        ]
        self.assertEqual(
            validate_review_aggregation(aggregation_example(), findings, p3_required=True),
            [],
        )

        p2_open = self.examples["forbidden"]["p2_without_disposition"]
        self.assertTrue(validate_finding_disposition(p2_open))

        dropped = aggregation_example()
        dropped["finding_refs"] = ["F-P2-1"]
        self.assertTrue(
            any("dropped" in e for e in validate_review_aggregation(dropped, findings, p3_required=True))
        )

        blocker = {
            "protocol_version": "ai-dev/review-finding-v1",
            "finding_id": "F-P1-BLOCK",
            "assurance_id": "review-a",
            "subject_identity_ref": f"sha:{SHA_A}",
            "severity": "P1",
            "summary": "unresolved authority blocker",
            "blocking": True,
            "status": "OPEN",
            "evidence_refs": ["issue:#81"],
        }
        aggregate = aggregation_example()
        aggregate["finding_refs"].append("F-P1-BLOCK")
        aggregate["unresolved_blocker_refs"] = ["F-P1-BLOCK"]
        self.assertTrue(
            any("PASS forbidden" in e for e in validate_review_aggregation(aggregate, findings + [blocker]))
        )

    def test_review_judgment_and_requested_route_are_separate_fields(self) -> None:
        aggregate = aggregation_example()
        aggregate["judgment"] = "VALIDATION_REQUESTED"
        aggregate["requested_route"] = "validation-needed"
        self.assertEqual(validate_subset(aggregate, load_schema("review-aggregation-v1.schema.json")), [])
        self.assertNotEqual(aggregate["judgment"], aggregate["requested_route"])

    def test_semantic_controller_action_key_is_stable_and_transport_independent(self) -> None:
        base = copy.deepcopy(self.examples["valid"]["semantic_action"])
        retry = copy.deepcopy(base)
        retry["exchange_id"] = "ex:2"
        reordered = {
            "effect_target": base["effect_target"],
            "expected_precondition": base["expected_precondition"],
            "subject_identity": base["subject_identity"],
            "authority_ref": base["authority_ref"],
            "controller_kind": base["controller_kind"],
        }
        self.assertEqual(canonical_semantic_action_key(base), canonical_semantic_action_key(retry))
        self.assertEqual(canonical_semantic_action_key(base), canonical_semantic_action_key(reordered))

        changed = copy.deepcopy(base)
        changed["expected_precondition"] = {"candidate_state": "THAWED"}
        self.assertNotEqual(canonical_semantic_action_key(base), canonical_semantic_action_key(changed))

    def test_fast_path_is_bounded_and_escalates_on_material_risk(self) -> None:
        valid = self.examples["valid"]["fast_path_context"]
        self.assertTrue(fast_path_eligible(valid))
        for flag in (
            "public_contract_change",
            "architecture_change",
            "security_or_trust_boundary_change",
            "migration_or_recovery_complexity",
            "concurrency_or_exactly_once_complexity",
            "cross_repository_or_authority_coupling",
        ):
            context = copy.deepcopy(valid)
            context[flag] = True
            with self.subTest(flag=flag):
                self.assertFalse(fast_path_eligible(context))
        self.assertFalse(fast_path_eligible(self.examples["forbidden"]["fast_path_public_contract"]))

    def test_validation_pass_requires_execution_evidence_and_drift_cannot_pass(self) -> None:
        valid = self.examples["valid"]["validation_result"]
        self.assertEqual(validate_validation_result(valid), [])

        forbidden = self.examples["forbidden"]["validation_pass_without_execution"]
        self.assertTrue(validate_validation_result(forbidden))

        drifted = copy.deepcopy(valid)
        drifted["drift"] = "HEAD_DRIFT"
        self.assertTrue(any("drifted" in e for e in validate_validation_result(drifted)))

    def test_candidate_freeze_and_release_identity_are_orthogonal_but_bound(self) -> None:
        freeze = {
            "event": "CANDIDATE_STATE_CHANGED",
            "candidate_state": "FROZEN",
            "candidate_sha": SHA_A,
            "tree_sha": TREE_A,
            "candidate_ref": "refs/heads/version/v4.0.0",
            "visible_closure_evidence": "evidence:closure",
        }
        ready = {
            "event": "RELEASE_QUALIFICATION",
            "release_state": "READY",
            "candidate_sha": SHA_A,
            "tree_sha": TREE_A,
        }
        self.assertEqual(validate_candidate_release_separation(freeze, ready), [])
        wrong = copy.deepcopy(ready)
        wrong["candidate_sha"] = SHA_B
        self.assertTrue(validate_candidate_release_separation(freeze, wrong))

    def test_hidden_metadata_uses_canonical_pack_identity_and_rejects_payload_leak(self) -> None:
        valid = self.examples["valid"]["hidden_metadata"]
        self.assertEqual(validate_hidden_metadata(valid), [])
        leaked = self.examples["forbidden"]["hidden_payload_leak"]
        self.assertTrue(any("private payload" in e for e in validate_hidden_metadata(leaked)))


if __name__ == "__main__":
    unittest.main()
