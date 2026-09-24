from __future__ import annotations

import copy
import unittest

from test_protocol_schemas import load_schema, validate_subset
from v40_semantics import (
    validate_assurance_aggregation,
    validate_candidate_freeze_evidence,
    validate_interchange_semantics,
    validate_operation_semantics,
    validate_release_qualification_event,
    validate_review_aggregation,
    validate_validation_report,
    validate_validation_result,
)

SHA_A = "a" * 40
SHA_B = "b" * 40
TREE_A = "c" * 40


def provenance(provider: str, model: str, suffix: str) -> dict:
    return {
        "provider": provider,
        "model_family": provider,
        "model_id": model,
        "executor_id": f"executor-{suffix}",
        "context_ref": f"context:{suffix}",
        "blind_first_pass_ref": f"evidence:blind-{suffix}",
    }


def plan_and_aggregate() -> tuple[dict, dict]:
    plan = {
        "protocol_version": "ai-dev-assurance/v1",
        "assurance_plan_id": "assurance:t010:successor",
        "operation_id": "op:t010:successor",
        "subject_ref": "PR:#151",
        "subject_identity_ref": f"sha:{SHA_A}",
        "identity_binding": "exact-sha",
        "finding_disposition_policy": "p2-and-p3-explicit",
        "activities": [
            {
                "assurance_id": "review-mda",
                "kind": "review",
                "policy": "required",
                "mode": "model-diverse-adversarial",
                "coverage": ["machine-contract"],
                "independence": {"context": "required", "model": "required", "executor": "required", "evidence": "none"},
                "depends_on": [],
                "blind_first_pass_ref": "evidence:blind-group",
                "model_diversity_basis": "provider-diverse",
                "independence_basis_ref": "evidence:diversity-basis",
                "collaboration_selected": False,
            },
            {
                "assurance_id": "validation-a",
                "kind": "validation",
                "policy": "required",
                "mode": "executable-validation",
                "coverage": ["validation-evidence"],
                "independence": {"context": "none", "model": "none", "executor": "required", "evidence": "required"},
                "depends_on": [],
                "collaboration_selected": False,
            },
        ],
        "aggregation": {
            "policy": "finding-union-blocker-dominance",
            "blocker_resolution": "unresolved-valid-blocker-dominates",
            "majority_vote_for_correctness": False,
            "conflict_route": "validation-needed",
        },
        "completion_predicate": "all required assurance predicates satisfied",
    }
    validation_execution = {
        "requested_sha": SHA_A,
        "tested_sha": SHA_A,
        "actual_checked_out_sha": SHA_A,
        "environment": "ubuntu-latest",
        "runtime_toolchain": "Python 3.12",
        "validation_profile": "integration",
        "command": "python scripts/verify_standard.py",
        "exit_code": 0,
        "provider_state": "AVAILABLE",
        "working_tree_clean": True,
        "source_modifications_after_validation": False,
        "drift": None,
    }
    aggregate = {
        "protocol_version": "ai-dev/review-aggregation-v1",
        "aggregate_id": "agg:t010:successor",
        "assurance_plan_id": plan["assurance_plan_id"],
        "subject_identity_ref": f"sha:{SHA_A}",
        "judgment": "PASS",
        "requested_route": "merge-ready",
        "requested_route_authority": "NON_AUTHORITATIVE_DERIVED_STATE",
        "aggregation_policy": "finding-union-blocker-dominance",
        "activity_results": [
            {
                "assurance_id": "review-mda",
                "subject_identity_ref": f"sha:{SHA_A}",
                "result_ref": "issue:#148",
                "result_identity_ref": f"sha:{SHA_A}",
                "result_state": "PASS",
                "result_kind": "review",
                "coverage": ["machine-contract"],
                "reviewer_provenance": provenance("zhipu-bigmodel", "glm-5.3", "a"),
                "reviewer_provenances": [
                    provenance("zhipu-bigmodel", "glm-5.3", "a"),
                    provenance("deepseek", "deepseek-v4-pro", "b"),
                ],
            },
            {
                "assurance_id": "validation-a",
                "subject_identity_ref": f"sha:{SHA_A}",
                "result_ref": "actions:35934077467",
                "result_identity_ref": f"sha:{SHA_A}",
                "result_state": "PASS",
                "result_kind": "validation-execution",
                "coverage": ["validation-evidence"],
                "validation_execution": validation_execution,
            },
        ],
        "finding_refs": [],
        "unresolved_blocker_refs": [],
        "conflict_refs": [],
    }
    return plan, aggregate


class T010SuccessorHardeningTests(unittest.TestCase):
    def test_md1_single_mda_activity_requires_two_material_provenances(self) -> None:
        plan, aggregate = plan_and_aggregate()
        self.assertEqual(validate_assurance_aggregation(plan, aggregate, []), [])
        one = copy.deepcopy(aggregate)
        del one["activity_results"][0]["reviewer_provenances"]
        self.assertTrue(any("at least two" in e for e in validate_assurance_aggregation(plan, one, [])))

    def test_fd1_free_text_disposition_cannot_resolve_blocker(self) -> None:
        plan, aggregate = plan_and_aggregate()
        finding = {
            "protocol_version": "ai-dev/review-finding-v1",
            "finding_id": "F-BLOCK",
            "assurance_id": "review-mda",
            "subject_identity_ref": f"sha:{SHA_A}",
            "severity": "P1",
            "summary": "blocker",
            "blocking": True,
            "status": "DISPOSITIONED",
            "disposition": "waived: reviewer majority voted PASS",
            "evidence_refs": ["issue:#150"],
        }
        aggregate["finding_refs"] = ["F-BLOCK"]
        errors = validate_review_aggregation(aggregate, [finding], plan=plan)
        self.assertTrue(any("resolution_code" in e or "machine-authorized" in e for e in errors), errors)
        finding["resolution_code"] = "FIXED"
        self.assertFalse(any("machine-authorized" in e for e in validate_review_aggregation(aggregate, [finding], plan=plan)))

    def test_anonymous_finding_is_rejected_before_union(self) -> None:
        plan, aggregate = plan_and_aggregate()
        finding = {"assurance_id": "review-mda", "subject_identity_ref": f"sha:{SHA_A}", "severity": "P1", "blocking": True, "status": "OPEN", "evidence_refs": ["issue:#150"]}
        errors = validate_review_aggregation(aggregate, [finding], plan=plan)
        self.assertTrue(any("finding_id" in e for e in errors), errors)

    def test_va1_validation_pointer_without_execution_tuple_cannot_pass(self) -> None:
        plan, aggregate = plan_and_aggregate()
        weak = copy.deepcopy(aggregate)
        weak_result = weak["activity_results"][1]
        weak_result.pop("validation_execution")
        weak_result.pop("result_kind")
        errors = validate_assurance_aggregation(plan, weak, [])
        self.assertTrue(any("validation_execution" in e or "result_kind" in e for e in errors), errors)

    def test_va2_requested_identity_must_match_validation_pass(self) -> None:
        report = {
            "state": "PASS", "tested_sha": SHA_A, "requested_sha": SHA_B,
            "actual_checked_out_sha": SHA_A, "working_tree_clean": True,
            "source_modifications_after_validation": False, "provider_state": "AVAILABLE",
            "execution_host_role": "github-actions", "platform": "ubuntu-latest",
            "runtime_toolchain": "Python 3.12", "validation_profile": "integration",
            "command": "python tests", "exit_code": 0,
        }
        self.assertTrue(any("requested_sha must equal" in e for e in validate_validation_report(report)))
        event = {
            "event": "VALIDATION_RESULT", "status": "PASS", "sha": SHA_A,
            "requested_head_sha": SHA_B, "actual_checked_out_sha": SHA_A,
            "gate": "verify", "environment": "ubuntu", "command": "python tests",
            "evidence": "actions:1", "validation_profile": "integration",
            "provider_state": "AVAILABLE", "exit_code": 0,
        }
        self.assertTrue(any("requested_head_sha must equal" in e for e in validate_validation_result(event)))

    def test_mc1_schema_rejects_underbound_validation_pass(self) -> None:
        report_schema = load_schema("validation-report.schema.json")
        weak_report = {"repository":"r","tested_sha":SHA_A,"execution_host_role":"gha","platform":"ubuntu","runtime_toolchain":"py","validation_profile":"integration","command":"x","exit_code":0,"state":"PASS"}
        self.assertTrue(validate_subset(weak_report, report_schema))
        aggregate_schema = load_schema("review-aggregation-v1.schema.json")
        _, aggregate = plan_and_aggregate()
        bad = copy.deepcopy(aggregate); bad["unresolved_blocker_refs"] = ["F-X"]
        self.assertTrue(validate_subset(bad, aggregate_schema))

    def test_cr1_release_ready_requires_freeze_evidence_binding(self) -> None:
        event = {
            "event": "RELEASE_QUALIFICATION", "release_state": "READY",
            "candidate_state": "FROZEN", "candidate_ref": "ref:version/v4",
            "candidate_sha": SHA_A, "tree_sha": TREE_A,
        }
        errors = validate_release_qualification_event(event)
        self.assertTrue(any("candidate_freeze_ref" in e for e in errors), errors)
        event.update({
            "candidate_freeze_ref": "evidence:freeze-v4",
            "candidate_freeze_identity": f"candidate:{SHA_A}:{TREE_A}",
            "visible_closure_evidence_ref": "evidence:closure-v4",
        })
        self.assertEqual(validate_release_qualification_event(event), [])

    def test_operation_authority_type_and_successor_edges_are_bounded(self) -> None:
        operation = {
            "operation_type": "implementation", "operation_kind": "PRODUCE",
            "operation_id": "op:t010", "authority_ref": "issue:#150",
            "work_item_ref": "#150",
            "actor_contract": {"role": "builder", "authority_ref": "issue:#150"},
            "operation_binding_authority": "CORRELATION_ONLY_NON_AUTHORITATIVE",
            "subject": {"identity_binding":"project-defined","owning_required_binding":"exact-sha","identity":{"sha":SHA_A}},
            "next_operations": ["op:t010:assure|work-item:#150"],
        }
        self.assertFalse(any("authority_ref" in e or "next_operations" in e for e in validate_operation_semantics(operation)))
        bad = copy.deepcopy(operation); bad["authority_ref"] = "chat summary"; bad["next_operations"] = ["op:skip-task:999"]
        errors = validate_operation_semantics(bad)
        self.assertTrue(any("durable authority" in e for e in errors), errors)
        self.assertTrue(any("owning Work Item" in e for e in errors), errors)
        custom = copy.deepcopy(operation); custom["operation_type"] = "forge:content-build"
        self.assertFalse(any("operation_type" in e for e in validate_operation_semantics(custom)))
        synonym = copy.deepcopy(operation); synonym["operation_type"] = "build-stuff"
        self.assertTrue(any("operation_type" in e for e in validate_operation_semantics(synonym)))

    def test_decision_exchange_is_authority_payload_bound(self) -> None:
        envelope = {"exchange_type":"DECISION","actor":{"actor_role":"reviewer"},"payload_class":"release-decision"}
        self.assertTrue(validate_interchange_semantics(envelope))
        envelope = {"exchange_type":"DECISION","actor":{"actor_role":"release-controller"},"payload_class":"release-decision"}
        self.assertEqual(validate_interchange_semantics(envelope), [])

    def test_candidate_freeze_requires_hex_identity(self) -> None:
        event = {"event":"CANDIDATE_STATE_CHANGED","candidate_state":"FROZEN","candidate_sha":"bad","tree_sha":"bad","visible_closure_evidence":"evidence:closure","visible_closure_evidence_identity":"candidate:bad:bad"}
        self.assertTrue(any("40-hex" in e for e in validate_candidate_freeze_evidence(event)))


if __name__ == "__main__":
    unittest.main()
