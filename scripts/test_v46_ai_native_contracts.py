from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


def load(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


class AINativeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.intent = load("intent-assumption-record-v1.schema.json")
        cls.skill = load("skill-metadata-v1.schema.json")
        cls.dispatch = load("dispatch.schema.json")
        cls.execution_pack = load("execution-pack-manifest.schema.json")

    def test_exactly_two_new_default_machine_families(self) -> None:
        self.assertIn("Intent / Assumption Record", self.intent["title"])
        self.assertIn("Skill Metadata", self.skill["title"])
        self.assertFalse((SCHEMAS / "context-snapshot-v1.schema.json").exists())
        self.assertFalse((SCHEMAS / "agent-lifecycle-result-v1.schema.json").exists())

    def test_intent_classification_does_not_self_promote_to_authority(self) -> None:
        classifications = self.intent["properties"]["classification"]["enum"]
        for value in (
            "USER_INTENT",
            "INTERPRETATION",
            "ASSUMPTION",
            "UNKNOWN",
            "DECISION_REQUIRED",
            "DURABLE_REQUIREMENT",
        ):
            self.assertIn(value, classifications)
        durable_rule = self.intent["allOf"][0]["then"]["required"]
        self.assertIn("promotion_authority_ref", durable_rule)
        self.assertIn("promoted_requirement_ref", durable_rule)
        for forbidden in ("product_authority", "architecture_authority", "task_authority", "mutation_allowed"):
            self.assertNotIn(forbidden, self.intent["properties"])

    def test_skill_metadata_records_capability_but_not_authorization(self) -> None:
        props = self.skill["properties"]
        self.assertIn("tool_capability_refs", props)
        self.assertIn("required_authority_refs", props)
        for forbidden in ("trusted", "authorized", "mutation_allowed", "side_effect_allowed", "dispatch_state"):
            self.assertNotIn(forbidden, props)

    def test_dispatch_ai_native_refs_are_optional_and_backward_compatible(self) -> None:
        props = self.dispatch["properties"]
        required = set(self.dispatch["required"])
        self.assertIn("intent_assumption_refs", props)
        self.assertIn("skill_metadata_refs", props)
        self.assertNotIn("intent_assumption_refs", required)
        self.assertNotIn("skill_metadata_refs", required)
        historical_required = {
            "dispatch_id", "repository", "version", "task", "role", "execution_profile",
            "branch", "expected_base_sha", "pinned_standard_revision", "agent_freedom", "dispatch_state",
        }
        self.assertEqual(required, historical_required)

    def test_execution_pack_ai_native_refs_are_optional_and_backward_compatible(self) -> None:
        props = self.execution_pack["properties"]
        required = set(self.execution_pack["required"])
        self.assertIn("intent_assumption_refs", props)
        self.assertIn("skill_metadata_refs", props)
        self.assertNotIn("intent_assumption_refs", required)
        self.assertNotIn("skill_metadata_refs", required)
        historical_required = {
            "pack_id", "task_id", "repository", "version", "base_sha", "task_pack_ref",
            "branch", "agent_freedom", "pinned_standard_revision", "generated_by", "generated_at",
            "core_artifacts", "retention",
        }
        self.assertEqual(required, historical_required)

    def test_new_records_do_not_create_assurance_review_validation_release_state(self) -> None:
        for schema in (self.intent, self.skill):
            props = schema["properties"]
            for forbidden in (
                "assurance_state", "review_state", "validation_state", "release_state",
                "dispatch_state", "agent_freedom", "pass", "ready",
            ):
                self.assertNotIn(forbidden, props)


if __name__ == "__main__":
    unittest.main()
