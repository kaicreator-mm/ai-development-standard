from __future__ import annotations

import copy
import unittest

from test_protocol_schemas import load_schema, validate_subset
from test_v40_operation_contracts import (
    aggregation_example,
    assurance_example,
    finding_example,
)
from v40_semantics import (
    validate_assurance_aggregation,
    validate_assurance_semantics,
    validate_hidden_metadata,
    validate_review_aggregation,
    validate_validation_report,
    validate_validation_result,
)


def two_lane_plan_and_aggregate() -> tuple[dict, dict, list[dict]]:
    plan = assurance_example()
    review_a = plan["activities"][0]
    review_b = copy.deepcopy(review_a)
    review_b["assurance_id"] = "review-b"
    review_b["blind_first_pass_ref"] = "evidence:review-b-blind"
    review_b["independence_basis_ref"] = "evidence:review-b-independence"
    plan["activities"].insert(1, review_b)

    aggregate = aggregation_example()
    result_a = aggregate["activity_results"][0]
    result_b = copy.deepcopy(result_a)
    result_b["assurance_id"] = "review-b"
    result_b["result_ref"] = "issue:#r3-review-b"
    result_b["reviewer_provenance"] = {
        "provider": "deepseek",
        "model_family": "deepseek",
        "model_id": "deepseek-v4-flash",
        "executor_id": "fresh-reviewer-b",
        "context_ref": "context:review-b",
        "blind_first_pass_ref": "evidence:review-b-blind",
    }
    aggregate["activity_results"].insert(1, result_b)

    findings = [
        finding_example("F-P2-1", "P2", "covered"),
        finding_example("F-P3-1", "P3", "recorded"),
    ]
    return plan, aggregate, findings


class V40R3CarryForwardTests(unittest.TestCase):
    def test_fir1_provider_diverse_basis_is_machine_enforced(self) -> None:
        plan, aggregate, findings = two_lane_plan_and_aggregate()
        self.assertEqual(validate_assurance_aggregation(plan, aggregate, findings), [])

        same_provider = copy.deepcopy(aggregate)
        same_provider["activity_results"][1]["reviewer_provenance"]["provider"] = "openai"
        errors = validate_assurance_aggregation(plan, same_provider, findings)
        self.assertTrue(any("distinct providers" in error for error in errors), errors)

        disguised_same_model = copy.deepcopy(aggregate)
        disguised_same_model["activity_results"][1]["reviewer_provenance"].update(
            {
                "provider": "deepseek",
                "model_family": "different-label",
                "model_id": aggregate["activity_results"][0]["reviewer_provenance"]["model_id"],
            }
        )
        errors = validate_assurance_aggregation(plan, disguised_same_model, findings)
        self.assertTrue(any("same-model reuse" in error for error in errors), errors)

    def test_fir1_model_family_architecture_and_configuration_bases(self) -> None:
        plan, aggregate, findings = two_lane_plan_and_aggregate()

        for activity in plan["activities"][:2]:
            activity["model_diversity_basis"] = "model-family-diverse"
        self.assertEqual(validate_assurance_aggregation(plan, aggregate, findings), [])
        same_family = copy.deepcopy(aggregate)
        same_family["activity_results"][1]["reviewer_provenance"]["model_family"] = "gpt-5"
        errors = validate_assurance_aggregation(plan, same_family, findings)
        self.assertTrue(any("distinct model families" in error for error in errors), errors)

        for activity in plan["activities"][:2]:
            activity["model_diversity_basis"] = "architecture-system-diverse"
        architecture = copy.deepcopy(aggregate)
        architecture["activity_results"][0]["reviewer_provenance"]["architecture_system"] = "openai-reasoning"
        architecture["activity_results"][1]["reviewer_provenance"]["architecture_system"] = "deepseek-reasoning"
        self.assertEqual(validate_assurance_aggregation(plan, architecture, findings), [])
        missing_architecture = copy.deepcopy(architecture)
        del missing_architecture["activity_results"][1]["reviewer_provenance"]["architecture_system"]
        errors = validate_assurance_aggregation(plan, missing_architecture, findings)
        self.assertTrue(any("architecture_system" in error for error in errors), errors)

        for activity in plan["activities"][:2]:
            activity["model_diversity_basis"] = "project-approved-different-configuration"
        configurations = copy.deepcopy(aggregate)
        configurations["activity_results"][0]["reviewer_provenance"]["configuration_fingerprint"] = "cfg:reasoning-max"
        configurations["activity_results"][1]["reviewer_provenance"]["configuration_fingerprint"] = "cfg:default"
        self.assertEqual(validate_assurance_aggregation(plan, configurations, findings), [])
        same_configuration = copy.deepcopy(configurations)
        same_configuration["activity_results"][1]["reviewer_provenance"]["configuration_fingerprint"] = "cfg:reasoning-max"
        errors = validate_assurance_aggregation(plan, same_configuration, findings)
        self.assertTrue(any("distinct configuration fingerprints" in error for error in errors), errors)

    def test_fir1_extended_provenance_fields_are_schema_bounded(self) -> None:
        _, aggregate, _ = two_lane_plan_and_aggregate()
        provenance = aggregate["activity_results"][0]["reviewer_provenance"]
        provenance["architecture_system"] = "openai-reasoning"
        provenance["configuration_fingerprint"] = "cfg:max"
        self.assertEqual(validate_subset(aggregate, load_schema("review-aggregation-v1.schema.json")), [])
        malformed = copy.deepcopy(aggregate)
        malformed["activity_results"][0]["reviewer_provenance"]["architecture_system"] = {"secret": "no"}
        self.assertTrue(validate_subset(malformed, load_schema("review-aggregation-v1.schema.json")))

    def test_fir2_hidden_allow_list_values_are_public_scalars(self) -> None:
        valid = {
            "pack_identity": "hidden:v4:r3",
            "pack_revision": "r3",
            "pack_checksum": "sha256:abc",
            "candidate_sha": "a" * 40,
            "coverage_digest": "sha256:def",
            "leak_check": "PASS",
            "evaluator_ref": "issue:#143",
            "evidence_ref": "evidence:hidden-r3",
            "occurred_at": "2026-09-24T00:00:00Z",
        }
        self.assertEqual(validate_hidden_metadata(valid), [])

        for field in ("coverage_digest", "leak_check", "evaluator_ref", "evidence_ref"):
            leaked = copy.deepcopy(valid)
            leaked[field] = {"oracle": "private", "expected_answer": "private"}
            with self.subTest(field=field):
                errors = validate_hidden_metadata(leaked)
                self.assertTrue(any("public scalar string" in error for error in errors), errors)

    def test_fir3_canonical_facade_returns_structured_fail_closed_errors(self) -> None:
        cases = [
            (lambda: validate_assurance_semantics(None), "Assurance Plan"),
            (lambda: validate_assurance_semantics({"activities": [None]}), "activities"),
            (lambda: validate_assurance_aggregation(None, {}, []), "Assurance Plan"),
            (lambda: validate_assurance_aggregation({}, None, []), "review aggregation"),
            (lambda: validate_assurance_aggregation({}, {}, [None]), "findings"),
            (lambda: validate_review_aggregation({}, [None]), "findings"),
            (lambda: validate_validation_report(None), "Validation report"),
            (lambda: validate_validation_result(None), "Validation event"),
        ]
        for call, expected in cases:
            with self.subTest(expected=expected):
                result = call()
                self.assertIsInstance(result, list)
                self.assertTrue(result)
                self.assertTrue(any(expected in error for error in result), result)


if __name__ == "__main__":
    unittest.main()
