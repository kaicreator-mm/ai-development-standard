from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from test_protocol_schemas import load_schema, validate_subset
from test_v40_operation_contracts import (
    SHA_A,
    SHA_B,
    TREE_A,
    aggregation_example,
    assurance_example,
    fast_path_context,
    finding_example,
    interchange_example,
    operation_example,
)
from v40_r2_hardening import validate_fast_path_context
from v40_semantics import (
    fast_path_eligible,
    validate_assurance_aggregation,
    validate_candidate_freeze_evidence,
    validate_execution_state_hardening,
    validate_hidden_metadata,
    validate_operation_semantics,
    validate_release_qualification_event,
    validate_review_aggregation,
    validate_review_decision_hardening,
    validate_validation_report,
    validate_validation_result,
)

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "templates" / "golden" / "V4_R2_MACHINE_HARDENING_EXAMPLES.json"


def base_findings() -> list[dict]:
    return [
        finding_example("F-P2-1", "P2", "covered"),
        finding_example("F-P3-1", "P3", "recorded"),
    ]


class V40R2MachineHardeningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(GOLDEN.read_text(encoding="utf-8"))

    def test_gr1_to_gr16_have_explicit_machine_enforcement(self) -> None:
        expected = {f"GR{i}" for i in range(1, 17)}
        self.assertEqual(set(self.data["required_groups"]), expected)
        self.assertEqual(set(self.data["enforcement"]), expected)
        for group, surfaces in self.data["enforcement"].items():
            with self.subTest(group=group):
                self.assertTrue(surfaces)
                self.assertTrue(all(isinstance(item, str) and item for item in surfaces))

    def test_gr1_validation_report_pass_is_execution_and_identity_bound(self) -> None:
        schema = load_schema("validation-report.schema.json")
        wrong = copy.deepcopy(self.data["forbidden"]["validation_report_wrong_checkout"])
        self.assertEqual(validate_subset(wrong, schema), [])
        self.assertTrue(any("must equal tested_sha" in e for e in validate_validation_report(wrong)))

        valid = copy.deepcopy(wrong)
        valid["actual_checked_out_sha"] = SHA_A
        self.assertEqual(validate_validation_report(valid), [])
        self.assertEqual(validate_subset(valid, schema), [])

        for field, value in (
            ("working_tree_clean", False),
            ("source_modifications_after_validation", True),
            ("provider_state", "INFRA_BLOCKED"),
            ("drift", "HEAD_DRIFT"),
        ):
            bad = copy.deepcopy(valid)
            bad[field] = value
            with self.subTest(field=field):
                self.assertTrue(validate_subset(bad, schema) or validate_validation_report(bad))

        missing = copy.deepcopy(valid)
        del missing["actual_checked_out_sha"]
        self.assertTrue(validate_subset(missing, schema))
        self.assertTrue(validate_validation_report(missing))

    def test_gr2_fast_path_is_closed_world_and_typed(self) -> None:
        valid = fast_path_context()
        self.assertTrue(fast_path_eligible(valid))
        missing = copy.deepcopy(valid); del missing["material_dependency_graph"]
        self.assertFalse(fast_path_eligible(missing))
        non_boolean = copy.deepcopy(valid); non_boolean["unresolved_authority_contradiction"] = "UNKNOWN"
        self.assertFalse(fast_path_eligible(non_boolean))
        typo = copy.deepcopy(valid); typo[self.data["forbidden"]["fast_path_unknown_key"]] = False
        self.assertFalse(fast_path_eligible(typo))
        self.assertTrue(validate_fast_path_context(typo))

    def test_gr3_operation_type_kind_mapping_is_machine_enforced(self) -> None:
        schema = load_schema("operation-v1.schema.json")
        bad = operation_example()
        bad["operation_type"] = "release-qualification"
        bad["operation_kind"] = "PRODUCE"
        self.assertTrue(validate_subset(bad, schema))
        self.assertTrue(any("requires operation_kind=DECIDE" in e for e in validate_operation_semantics(bad)))

    def test_gr4_truth_sensitive_operation_identity_cannot_weaken(self) -> None:
        bad = operation_example()
        bad["operation_type"] = "validation"
        bad["operation_kind"] = "ASSURE"
        bad["subject"]["owning_required_binding"] = "exact-sha"
        bad["subject"]["identity_binding"] = "exact-sha"
        self.assertTrue(any("requires owning_required_binding=validation-tuple" in e for e in validate_operation_semantics(bad)))
        plan = assurance_example()
        del plan["identity_binding"]
        self.assertTrue(validate_subset(plan, load_schema("assurance-plan-v1.schema.json")))

    def test_gr5_pass_aggregation_requires_plan_nonempty_results_and_pass_states(self) -> None:
        findings = base_findings()
        aggregate = aggregation_example()
        errors = validate_review_aggregation(aggregate, findings, plan=None)
        self.assertTrue(any("requires owning Assurance Plan" in e for e in errors), errors)

        empty = copy.deepcopy(aggregate); empty["activity_results"] = []
        self.assertTrue(validate_subset(empty, load_schema("review-aggregation-v1.schema.json")))

        failed_result = copy.deepcopy(aggregate); failed_result["activity_results"][0]["result_state"] = "FAIL"
        errors = validate_assurance_aggregation(assurance_example(), failed_result, findings)
        self.assertTrue(any("result_state=PASS" in e for e in errors), errors)

        ghost_ref = copy.deepcopy(aggregate); ghost_ref["activity_results"][0]["result_ref"] = "chat summary only"
        errors = validate_assurance_aggregation(assurance_example(), ghost_ref, findings)
        self.assertTrue(any("durable resolvable reference" in e for e in errors), errors)

    def test_gr6_model_diverse_pass_requires_provenance(self) -> None:
        aggregate = aggregation_example()
        del aggregate["activity_results"][0]["reviewer_provenance"]
        errors = validate_assurance_aggregation(assurance_example(), aggregate, base_findings())
        self.assertTrue(any("reviewer_provenance" in e for e in errors), errors)

        plan = assurance_example()
        del plan["activities"][0]["model_diversity_basis"]
        self.assertTrue(validate_subset(plan, load_schema("assurance-plan-v1.schema.json")))

    def test_gr7_interchange_authority_and_role_are_constrained(self) -> None:
        schema = load_schema("interchange-envelope-v1.schema.json")
        valid = interchange_example()
        self.assertEqual(validate_subset(valid, schema), [])
        bad = copy.deepcopy(valid)
        bad["exchange_type"] = "DECISION"
        bad["actor"]["actor_role"] = "builder"
        bad["subject_identity_ref"] = "ref:main"
        bad["identity_binding"] = "inherited"
        self.assertTrue(validate_subset(bad, schema))
        missing_marker = copy.deepcopy(valid); del missing_marker["authority_effect"]
        self.assertTrue(validate_subset(missing_marker, schema))

    def test_gr8_hidden_metadata_uses_public_allow_list(self) -> None:
        valid = {"pack_identity":"hidden:v4:001","pack_revision":"r1","pack_checksum":"sha256:abc","candidate_sha":SHA_A,"coverage_digest":"sha256:def","leak_check":"PASS"}
        self.assertEqual(validate_hidden_metadata(valid), [])
        for alias in ("fixture", "fixture_content", "oracle", "oracle_payload", "scenario_payload"):
            leaked = copy.deepcopy(valid); leaked[alias] = "secret"
            with self.subTest(alias=alias):
                self.assertTrue(validate_hidden_metadata(leaked))

    def test_gr9_authority_refs_and_marker_are_required_for_decide_assure(self) -> None:
        release = operation_example()
        release.update({"operation_type":"release-qualification","operation_kind":"DECIDE","work_item_ref":"#72","assurance_plan_ref":"evidence:release-assurance"})
        release["subject"] = {"ref":"candidate:v4","identity_binding":"candidate","owning_required_binding":"candidate","identity":{"candidate_sha":SHA_A,"tree_sha":TREE_A}}
        self.assertEqual(validate_operation_semantics(release), [])
        no_plan = copy.deepcopy(release); del no_plan["assurance_plan_ref"]
        self.assertTrue(validate_subset(no_plan, load_schema("operation-v1.schema.json")))
        self_auth = copy.deepcopy(release); self_auth["authority_ref"] = self_auth["operation_id"]
        self.assertTrue(any("self-authority" in e for e in validate_operation_semantics(self_auth)))

    def test_gr10_validation_event_guard_rejects_weak_tuple(self) -> None:
        valid = {"schema":"ai-dev/event-v2","event":"VALIDATION_RESULT","actor_role":"validator","operator_kind":"github-actions","operator_id":"gha:1","sha":SHA_A,"actual_checked_out_sha":SHA_A,"gate":"verify-standard","environment":"ubuntu-latest","validation_profile":"concern","command":"python tests","exit_code":0,"evidence":"actions:1","status":"PASS"}
        self.assertEqual(validate_validation_result(valid), [])
        cases = []
        bad = copy.deepcopy(valid); bad["exit_code"] = 0.0; cases.append(bad)
        bad = copy.deepcopy(valid); bad["sha"] = "not-a-sha"; cases.append(bad)
        bad = copy.deepcopy(valid); bad["actual_checked_out_sha"] = SHA_B; cases.append(bad)
        bad = copy.deepcopy(valid); bad["current_pr_head"] = SHA_B; cases.append(bad)
        bad = copy.deepcopy(valid); bad["provider_state"] = "INFRA_BLOCKED"; cases.append(bad)
        for case in cases:
            self.assertTrue(validate_validation_result(case), case)

    def test_gr11_recommended_review_skip_requires_policy_basis(self) -> None:
        event = {"event":"REVIEW_DECISION","review_policy":"recommended","decision":"skipped","status":"NOT_RUN","next_state":"merge-ready","reason":"small change"}
        self.assertTrue(validate_review_decision_hardening(event))
        event["policy_basis"] = "task-pack:risk-low"
        self.assertEqual(validate_review_decision_hardening(event), [])

    def test_gr12_judgment_route_contradiction_fails_schema_and_semantics(self) -> None:
        bad = aggregation_example(); bad.update(self.data["forbidden"]["review_route_contradiction"])
        self.assertTrue(validate_subset(bad, load_schema("review-aggregation-v1.schema.json")))
        self.assertTrue(validate_review_aggregation(bad, base_findings(), plan=assurance_example()))

    def test_gr13_execution_state_release_candidate_cross_family_invariant(self) -> None:
        state = {"repository":"kaicreator-mm/ai-development-standard","work_item":"#82","workflow_state":"done","candidate_state":"PREPARED","release_state":"READY","ready_queues":[],"derived_from":["event:1"]}
        self.assertTrue(validate_subset(state, load_schema("execution-state.schema.json")))
        self.assertTrue(validate_execution_state_hardening(state))
        state["candidate_state"] = "FROZEN"
        self.assertEqual(validate_subset(state, load_schema("execution-state.schema.json")), [])
        self.assertEqual(validate_execution_state_hardening(state), [])

    def test_gr14_standalone_release_qualification_requires_frozen_candidate_binding(self) -> None:
        event = {"event":"RELEASE_QUALIFICATION","release_state":"READY","candidate_sha":SHA_A,"tree_sha":TREE_A,"evidence":"issue:#85"}
        self.assertTrue(validate_release_qualification_event(event))
        event["candidate_state"] = "FROZEN"; event["candidate_ref"] = "refs/heads/version/v4.0.0"
        self.assertEqual(validate_release_qualification_event(event), [])

    def test_gr15_frozen_closure_evidence_is_durable_and_identity_bound(self) -> None:
        event = {"event":"CANDIDATE_STATE_CHANGED","candidate_state":"FROZEN","candidate_sha":SHA_A,"tree_sha":TREE_A,"visible_closure_evidence":"free text","visible_closure_evidence_identity":"candidate:wrong"}
        self.assertTrue(validate_candidate_freeze_evidence(event))
        event["visible_closure_evidence"] = "evidence:closure-72"
        event["visible_closure_evidence_identity"] = f"candidate:{SHA_A}:{TREE_A}"
        self.assertEqual(validate_candidate_freeze_evidence(event), [])

    def test_gr16_p3_policy_is_derived_from_assurance_plan(self) -> None:
        plan = assurance_example()
        p3 = finding_example("F-P3-OPEN", "P3", "placeholder")
        p3["status"] = "OPEN"; p3.pop("disposition")
        aggregate = aggregation_example(); aggregate["finding_refs"].append("F-P3-OPEN")
        errors = validate_review_aggregation(aggregate, base_findings() + [p3], plan=plan)
        self.assertTrue(any("P3 finding requires durable explicit disposition" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
