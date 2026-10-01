from __future__ import annotations

import unittest

from test_protocol_schemas import assert_supported_schema, load_schema, validate_subset


SCHEMA = load_schema("agent-capability-profile-v1.schema.json")


def valid_profile() -> dict:
    return {
        "schema_version": "ai-dev/agent-capability-profile-v1",
        "profile_id": "logical-agent:web-strong-builder",
        "profile_version": "1",
        "logical_agent_or_runtime_class_ref": "agent-class:chatgpt-web",
        "provider_model_provenance": "provider-model:example/strong-model",
        "eligible_role_claims": ["builder", "planning-builder"],
        "reasoning_or_semantic_capability_claims": ["schema-contract-authoring", "semantic-review-preparation"],
        "language_archetype_claims": ["python", "json-schema"],
        "logical_tool_use_class_claims": ["github-repository-write"],
        "max_agent_freedom_claim": "F1_BOUNDED_IMPLEMENTATION",
        "skill_refs": ["skill:repository-contract-work"],
        "security_or_side_effect_class_claims": ["requires-explicit-mutation-authority"],
        "environment_or_runner_requirement_refs": ["runner-class:python3"],
        "compatibility_refs": ["ads:v4"],
    }


class AgentCapabilityProfileSchemaTests(unittest.TestCase):
    def test_schema_uses_repository_supported_subset(self) -> None:
        assert_supported_schema(SCHEMA)

    def test_logical_claim_profile_positive(self) -> None:
        self.assertEqual(validate_subset(valid_profile(), SCHEMA), [])

    def test_infrastructure_inventory_fields_are_rejected(self) -> None:
        forbidden = (
            "host_os",
            "architecture",
            "runtime_inventory",
            "toolchain_inventory",
            "device_inventory",
            "cpu_count",
            "memory_bytes",
            "disk_bytes",
            "provider_concurrency",
            "network_reachability",
            "current_resource_capacity",
            "availability",
        )
        for field in forbidden:
            with self.subTest(field=field):
                value = valid_profile()
                value[field] = "owned-elsewhere"
                self.assertTrue(validate_subset(value, SCHEMA))

    def test_provider_model_is_provenance_not_score_or_authority(self) -> None:
        for field in ("correctness_score", "routing_score", "authorization", "review_pass", "validation_pass"):
            with self.subTest(field=field):
                value = valid_profile()
                value[field] = 1
                self.assertTrue(validate_subset(value, SCHEMA))

    def test_skill_and_credentials_do_not_become_capability_proof_or_side_effect_authority(self) -> None:
        for field in ("skill_proven_capabilities", "credential_refs", "side_effect_authority"):
            with self.subTest(field=field):
                value = valid_profile()
                value[field] = ["not-allowed"]
                self.assertTrue(validate_subset(value, SCHEMA))

    def test_agent_freedom_claim_is_bounded(self) -> None:
        value = valid_profile()
        value["max_agent_freedom_claim"] = "F4_UNBOUNDED"
        self.assertTrue(validate_subset(value, SCHEMA))

    def test_identity_and_role_claim_are_required(self) -> None:
        for field in ("profile_id", "logical_agent_or_runtime_class_ref", "eligible_role_claims"):
            with self.subTest(field=field):
                value = valid_profile()
                del value[field]
                self.assertTrue(validate_subset(value, SCHEMA))


if __name__ == "__main__":
    unittest.main()
