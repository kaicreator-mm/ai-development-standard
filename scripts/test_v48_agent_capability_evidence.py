from __future__ import annotations

import unittest

from test_protocol_schemas import assert_supported_schema, load_schema, validate_subset

SCHEMA = load_schema("agent-capability-evidence-v1.schema.json")


def valid_evidence() -> dict:
    return {
        "schema_version": "ai-dev/agent-capability-evidence-v1",
        "evidence_id": "cap-evidence:T-016:001",
        "agent_profile_ref": "profile:logical-agent-a",
        "logical_operator_or_executor_ref": "operator:builder-a",
        "provider_model_provenance": "provider-model:example/model-a",
        "task_class_or_capability_class": "schema-contract-authoring",
        "role": "builder",
        "exact_subject_ref": "git:repo@1111111111111111111111111111111111111111",
        "environment_ref": "environment:python3",
        "runner_or_resource_capability_ref": "runner-capability:ubuntu-build-01@obs-1",
        "task_pack_execution_pack_refs": ["task-pack:T-016", "execution-pack:T-016@base"],
        "result_refs": ["result:focused-tests-pass"],
        "validation_refs": ["validation:exact-subject-pass"],
        "review_refs": ["review:exact-subject-pass"],
        "observed_findings_refs": ["finding:none-blocking"],
        "evidence_strength": "INDEPENDENTLY_CHALLENGED",
        "observed_at_or_currentness_scope": "historical:exact-subject-only",
        "observation_kind": "POSITIVE",
        "economic_measurement_status": "NOT_MEASURED",
    }


class AgentCapabilityEvidenceSchemaTests(unittest.TestCase):
    def test_schema_uses_repository_supported_subset(self) -> None:
        assert_supported_schema(SCHEMA)

    def test_positive_evidence(self) -> None:
        self.assertEqual(validate_subset(valid_evidence(), SCHEMA), [])

    def test_negative_observation_is_first_class(self) -> None:
        value = valid_evidence()
        value["observation_kind"] = "NEGATIVE"
        value["result_refs"] = ["result:negative-oracle-failed"]
        self.assertEqual(validate_subset(value, SCHEMA), [])

    def test_false_current_authority_fields_are_rejected(self) -> None:
        for field in ("current_availability", "validation_pass", "review_pass", "authorization", "routing_decision"):
            with self.subTest(field=field):
                value = valid_evidence()
                value[field] = "PASS"
                self.assertTrue(validate_subset(value, SCHEMA))

    def test_global_scalar_score_is_rejected(self) -> None:
        value = valid_evidence()
        value["agent_score"] = 0.99
        self.assertTrue(validate_subset(value, SCHEMA))

    def test_owner_facts_are_referenced_not_copied(self) -> None:
        for field in ("host_os", "runtime_inventory", "cpu_count", "memory_bytes", "network_reachability"):
            with self.subTest(field=field):
                value = valid_evidence()
                value[field] = "copied-owner-fact"
                self.assertTrue(validate_subset(value, SCHEMA))

    def test_exact_subject_is_required(self) -> None:
        value = valid_evidence()
        del value["exact_subject_ref"]
        self.assertTrue(validate_subset(value, SCHEMA))

    def test_evidence_strength_is_bounded(self) -> None:
        value = valid_evidence()
        value["evidence_strength"] = "UNIVERSAL_SCORE"
        self.assertTrue(validate_subset(value, SCHEMA))

    def test_economic_status_prevents_unmeasured_inference(self) -> None:
        value = valid_evidence()
        value["economic_measurement_status"] = "SAVINGS_PROVEN"
        self.assertTrue(validate_subset(value, SCHEMA))
        value = valid_evidence()
        value["economic_measurement_status"] = "NOT_MEASURED"
        self.assertEqual(validate_subset(value, SCHEMA), [])


if __name__ == "__main__":
    unittest.main()
