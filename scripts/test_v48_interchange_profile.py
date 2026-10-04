from __future__ import annotations

from pathlib import Path
import unittest

from test_protocol_schemas import load_schema, validate_subset


ROOT = Path(__file__).resolve().parents[1]
INTERCHANGE = load_schema("interchange-envelope-v1.schema.json")
PROFILE = load_schema("agent-capability-profile-v1.schema.json")


def valid_handoff() -> dict:
    return {
        "protocol_version": "ai-dev/interchange-v1",
        "exchange_id": "exchange:v48:t003:001",
        "exchange_type": "HANDOFF",
        "operation_id": "v4.8:T-003",
        "work_item_ref": "github:kaicreator-mm/ai-development-standard#508",
        "subject_ref": "github:kaicreator-mm/ai-development-standard/pull/0",
        "subject_identity_ref": "git:kaicreator-mm/ai-development-standard@33dfb8f05bca1ba8fd4ea8d9a2c63eaa8f9aa830",
        "identity_binding": "exact-sha",
        "authority_effect": "CORRELATION_ONLY_NON_AUTHORITATIVE",
        "actor": {
            "actor_role": "builder",
            "operator_kind": "chatgpt-web",
            "operator_id": "v48-t003-builder",
        },
        "causation": {
            "caused_by": "github:kaicreator-mm/ai-development-standard#508",
            "correlation_refs": [
                "schema:agent-capability-profile-v1",
                "task:T-015#522",
            ],
        },
        "payload_ref": "github:kaicreator-mm/ai-development-standard#508:t003-compatibility",
        "occurred_at": "2026-10-01T12:49:00Z",
    }


class V48InterchangeProfileTests(unittest.TestCase):
    def test_existing_interchange_v1_carries_durable_profile_correlation_without_new_fields(self) -> None:
        self.assertEqual(validate_subset(valid_handoff(), INTERCHANGE), [])
        self.assertEqual(INTERCHANGE["properties"]["protocol_version"]["const"], "ai-dev/interchange-v1")
        self.assertEqual(
            INTERCHANGE["properties"]["authority_effect"]["const"],
            "CORRELATION_ONLY_NON_AUTHORITATIVE",
        )
        self.assertEqual(PROFILE["properties"]["schema_version"]["const"], "ai-dev/agent-capability-profile-v1")

    def test_ad_hoc_capability_eligibility_and_authority_fields_are_rejected(self) -> None:
        for field, value in (
            ("receiver_capability_profile", {"role": "builder"}),
            ("receiver_capability_score", 0.99),
            ("eligibility_decision", "ELIGIBLE"),
            ("availability_state", "AVAILABLE"),
            ("review_pass", True),
            ("validation_pass", True),
            ("agent_exchange_authority", "WORKFLOW_TRUTH"),
        ):
            with self.subTest(field=field):
                envelope = valid_handoff()
                envelope[field] = value
                self.assertTrue(validate_subset(envelope, INTERCHANGE))

    def test_interchange_cannot_claim_workflow_authority(self) -> None:
        envelope = valid_handoff()
        envelope["authority_effect"] = "WORKFLOW_AUTHORITY"
        self.assertTrue(validate_subset(envelope, INTERCHANGE))

    def test_parallel_exchange_family_protocol_is_rejected(self) -> None:
        envelope = valid_handoff()
        envelope["protocol_version"] = "ai-dev/agent-exchange-v1"
        self.assertTrue(validate_subset(envelope, INTERCHANGE))

    def test_profile_owner_remains_separate_closed_contract(self) -> None:
        profile = {
            "schema_version": "ai-dev/agent-capability-profile-v1",
            "profile_id": "profile:v48:builder",
            "profile_version": "1",
            "logical_agent_or_runtime_class_ref": "agent-class:builder",
            "eligible_role_claims": ["builder"],
        }
        self.assertEqual(validate_subset(profile, PROFILE), [])
        profile["current_availability"] = "AVAILABLE"
        self.assertTrue(validate_subset(profile, PROFILE))

    def test_no_new_generic_exchange_owner_file_is_required(self) -> None:
        self.assertFalse((ROOT / "standards" / "AGENT_EXCHANGE_BINDING_STANDARD.md").exists())
        self.assertFalse((ROOT / "schemas" / "agent-exchange-envelope-v1.schema.json").exists())

    def test_reference_records_no_change_required_and_event_v2_preservation(self) -> None:
        reference = (ROOT / "references" / "V48_INTERCHANGE_PROFILE_COMPATIBILITY.md").read_text(encoding="utf-8")
        self.assertIn("INTERCHANGE_SCHEMA_CHANGE=NO_CHANGE_REQUIRED", reference)
        self.assertIn("GITHUB_PROTOCOL_CHANGE=NO_CHANGE_REQUIRED", reference)
        self.assertIn("NEW_EXCHANGE_FAMILY=FORBIDDEN", reference)
        self.assertIn("EVENT_V3=NOT_REQUIRED", reference)
        self.assertIn("T015_PROFILE_OWNER=REFERENCED_NOT_COPIED", reference)


if __name__ == "__main__":
    unittest.main()
