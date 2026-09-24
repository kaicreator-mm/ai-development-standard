from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from test_protocol_schemas import load_schema, validate_subset
from v40_semantics import (
    canonical_semantic_action_key,
    fast_path_eligible,
    validate_assurance_aggregation,
    validate_assurance_semantics,
    validate_candidate_release_separation,
    validate_finding_disposition,
    validate_hidden_metadata,
    validate_operation_semantics,
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
        "assurance_plan_ref": "evidence:assurance:T009",
        "acceptance_criteria": ["v4 machine contracts validate", "focused regressions pass"],
        "failure_routes": ["changes-requested", "blocked"],
        "next_operations": ["op:T009:assure|work-item:#81"],
        "operation_binding_authority": "CORRELATION_ONLY_NON_AUTHORITATIVE",
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
        "identity_binding": "exact-sha",
        "finding_disposition_policy": "p2-and-p3-explicit",
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
                "model_diversity_basis": "provider-diverse",
                "independence_basis_ref": "evidence:review-a-independence",
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


def _provenance(provider: str, family: str, model_id: str, suffix: str) -> dict:
    return {
        "provider": provider,
        "model_family": family,
        "model_id": model_id,
        "executor_id": f"fresh-reviewer-{suffix}",
        "context_ref": f"context:review-{suffix}",
        "blind_first_pass_ref": f"evidence:review-{suffix}-blind",
    }


def aggregation_example() -> dict:
    validation_execution = {
        "requested_sha": SHA_A,
        "tested_sha": SHA_A,
        "actual_checked_out_sha": SHA_A,
        "environment": "ubuntu-latest",
        "runtime_toolchain": "Python 3.12",
        "validation_profile": "concern",
        "command": "python scripts/test_v40_operation_contracts.py",
        "exit_code": 0,
        "provider_state": "AVAILABLE",
        "working_tree_clean": True,
        "source_modifications_after_validation": False,
        "drift": None,
    }
    provenance_a = _provenance("openai", "gpt-5", "gpt-5.6-sol", "a")
    provenance_b = _provenance("deepseek", "deepseek-v4", "deepseek-v4-pro", "b")
    return {
        "protocol_version": "ai-dev/review-aggregation-v1",
        "aggregate_id": "agg:T009",
        "assurance_plan_id": "assurance:T009",
        "subject_identity_ref": f"sha:{SHA_A}",
        "judgment": "PASS",
        "requested_route": "merge-ready",
        "requested_route_authority": "NON_AUTHORITATIVE_DERIVED_STATE",
        "aggregation_policy": "finding-union-blocker-dominance",
        "activity_results": [
            {
                "assurance_id": "review-a",
                "subject_identity_ref": f"sha:{SHA_A}",
                "result_ref": "issue:#119",
                "result_identity_ref": f"sha:{SHA_A}",
                "result_state": "PASS",
                "result_kind": "review",
                "coverage": ["schema-nonweakening", "aggregation", "compatibility"],
                "reviewer_provenance": provenance_a,
                "reviewer_provenances": [provenance_a, provenance_b],
            },
            {
                "assurance_id": "validation-a",
                "subject_identity_ref": f"sha:{SHA_A}",
                "result_ref": "actions:35900647211",
                "result_identity_ref": f"sha:{SHA_A}",
                "result_state": "PASS",
                "result_kind": "validation-execution",
                "coverage": ["focused-v4-regression", "full-repository-verifier"],
                "validation_execution": validation_execution,
            },
        ],
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
        "identity_binding": "exact-sha",
        "authority_effect": "CORRELATION_ONLY_NON_AUTHORITATIVE",
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


def fast_path_context() -> dict:
    value = {
        "scope_bounded": True,
        "validation_ownership_known": True,
        "review_policy_resolved": True,
    }
    for key in (
        "public_contract_change",
        "architecture_change",
        "security_or_trust_boundary_change",
        "migration_or_recovery_complexity",
        "concurrency_or_exactly_once_complexity",
        "cross_repository_or_authority_coupling",
        "unknown_validation_ownership",
        "unresolved_blocking_finding",
        "unresolved_authority_contradiction",
        "model_diverse_or_coherence_assurance_required",
        "nontrivial_execution_pack_required",
        "material_dependency_graph",
    ):
        value[key] = False
    return value


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
        self.assertEqual(validate_operation_semantics(operation_example()), [])

    def test_project_defined_identity_is_non_weakening(self) -> None:
        valid_subject = self.examples["valid"]["project_defined_nonweakening_subject"]
        self.assertEqual(validate_subject_identity(valid_subject), [])
        forbidden = self.examples["forbidden"]["project_defined_weakens_exact_subject"]
        self.assertTrue(validate_subject_identity(forbidden))

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

    def test_assurance_forbids_majority_correctness_and_fake_independence(self) -> None:
        valid = assurance_example()
        self.assertEqual(validate_assurance_semantics(valid), [])
        majority = copy.deepcopy(valid)
        majority["aggregation"] = copy.deepcopy(self.examples["forbidden"]["majority_vote_aggregation"])
        self.assertTrue(validate_subset(majority, load_schema("assurance-plan-v1.schema.json")))
        self.assertTrue(any("majority" in e for e in validate_assurance_semantics(majority)))
        missing_blind = copy.deepcopy(valid)
        del missing_blind["activities"][0]["blind_first_pass_ref"]
        self.assertTrue(validate_assurance_semantics(missing_blind))
        collaboration = copy.deepcopy(valid)
        collaboration["activities"][0]["collaboration_selected"] = True
        self.assertTrue(any("collaborative" in e for e in validate_assurance_semantics(collaboration)))

    def test_required_activity_coverage_and_subject_identity_fail_closed(self) -> None:
        plan = assurance_example()
        findings = [finding_example("F-P2-1", "P2", "covered"), finding_example("F-P3-1", "P3", "recorded")]
        aggregate = aggregation_example()
        self.assertEqual(validate_assurance_aggregation(plan, aggregate, findings), [])
        missing = copy.deepcopy(aggregate)
        missing["activity_results"] = missing["activity_results"][:1]
        self.assertTrue(any("missing required assurance activity" in e for e in validate_assurance_aggregation(plan, missing, findings)))
        stale = copy.deepcopy(aggregate)
        stale["subject_identity_ref"] = f"sha:{SHA_B}"
        self.assertTrue(any("aggregation subject identity differs" in e for e in validate_assurance_aggregation(plan, stale, findings)))

    def test_findings_are_durable_and_blockers_require_evidence_backed_resolution(self) -> None:
        plan = assurance_example()
        findings = [finding_example("F-P2-1", "P2", "covered"), finding_example("F-P3-1", "P3", "recorded")]
        self.assertEqual(validate_review_aggregation(aggregation_example(), findings, plan=plan), [])
        p2_open = self.examples["forbidden"]["p2_without_disposition"]
        self.assertTrue(validate_finding_disposition(p2_open))
        dropped = aggregation_example()
        dropped["finding_refs"] = ["F-P2-1"]
        self.assertTrue(any("dropped" in e for e in validate_review_aggregation(dropped, findings, plan=plan)))

    def test_review_judgment_and_requested_route_are_separate_non_authoritative_fields(self) -> None:
        aggregate = aggregation_example()
        aggregate["judgment"] = "VALIDATION_REQUESTED"
        aggregate["requested_route"] = "validation-needed"
        self.assertEqual(validate_subset(aggregate, load_schema("review-aggregation-v1.schema.json")), [])
        self.assertEqual(aggregate["requested_route_authority"], "NON_AUTHORITATIVE_DERIVED_STATE")
        bad = copy.deepcopy(aggregate)
        bad["judgment"] = "BLOCKED"
        bad["requested_route"] = "merge-ready"
        self.assertTrue(validate_subset(bad, load_schema("review-aggregation-v1.schema.json")))

    def test_semantic_controller_action_key_is_stable_and_transport_independent(self) -> None:
        base = copy.deepcopy(self.examples["valid"]["semantic_action"])
        retry = copy.deepcopy(base)
        retry["exchange_id"] = "ex:2"
        self.assertEqual(canonical_semantic_action_key(base), canonical_semantic_action_key(retry))

    def test_fast_path_is_closed_world_and_escalates_on_material_risk(self) -> None:
        valid = fast_path_context()
        self.assertTrue(fast_path_eligible(valid))
        for flag in ("public_contract_change", "architecture_change", "unresolved_authority_contradiction"):
            context = copy.deepcopy(valid)
            context[flag] = True
            self.assertFalse(fast_path_eligible(context))
        missing = copy.deepcopy(valid)
        del missing["material_dependency_graph"]
        self.assertFalse(fast_path_eligible(missing))
        typo = copy.deepcopy(valid)
        typo["material_dependency_grap"] = False
        self.assertFalse(fast_path_eligible(typo))

    def test_validation_pass_requires_execution_evidence_and_drift_cannot_pass(self) -> None:
        valid = {
            "schema": "ai-dev/event-v2",
            "event": "VALIDATION_RESULT",
            "actor_role": "validator",
            "operator_kind": "github-actions",
            "operator_id": "gha:run",
            "sha": SHA_A,
            "requested_head_sha": SHA_A,
            "actual_checked_out_sha": SHA_A,
            "gate": "verify-standard",
            "environment": "ubuntu-latest",
            "validation_profile": "concern",
            "provider_state": "AVAILABLE",
            "command": "python scripts/test_v40_operation_contracts.py",
            "exit_code": 0,
            "evidence": "actions:run",
            "status": "PASS",
        }
        self.assertEqual(validate_validation_result(valid), [])
        forbidden = copy.deepcopy(valid)
        forbidden["exit_code"] = 1
        self.assertTrue(validate_validation_result(forbidden))
        drifted = copy.deepcopy(valid)
        drifted["drift"] = "HEAD_DRIFT"
        self.assertTrue(validate_validation_result(drifted))

    def test_candidate_freeze_and_release_identity_are_orthogonal_but_bound(self) -> None:
        freeze = {"event": "CANDIDATE_STATE_CHANGED", "candidate_state": "FROZEN", "candidate_sha": SHA_A, "tree_sha": TREE_A, "candidate_ref": "refs/heads/version/v4.0.0", "visible_closure_evidence": "evidence:closure"}
        ready = {"event": "RELEASE_QUALIFICATION", "release_state": "READY", "candidate_sha": SHA_A, "tree_sha": TREE_A}
        self.assertEqual(validate_candidate_release_separation(freeze, ready), [])
        wrong = copy.deepcopy(ready)
        wrong["candidate_sha"] = SHA_B
        self.assertTrue(validate_candidate_release_separation(freeze, wrong))

    def test_hidden_metadata_uses_public_allow_list(self) -> None:
        valid = self.examples["valid"]["hidden_metadata"]
        self.assertEqual(validate_hidden_metadata(valid), [])
        leaked = copy.deepcopy(valid)
        leaked["fixture_content"] = {"secret": "do-not-share"}
        self.assertTrue(validate_hidden_metadata(leaked))


if __name__ == "__main__":
    unittest.main()
