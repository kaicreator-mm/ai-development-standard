from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
REFERENCE = ROOT / "references" / "AI_NATIVE_EXISTING_OWNER_INTEGRATION.md"


def load(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


class ExistingOwnerIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.assurance = load("assurance-plan-v1.schema.json")
        cls.review = load("review-aggregation-v1.schema.json")
        cls.dispatch = load("dispatch.schema.json")
        cls.execution_pack = load("execution-pack-manifest.schema.json")
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_f0_f3_remain_single_execution_freedom_vocabulary(self) -> None:
        expected = [
            "F0_MECHANICAL",
            "F1_BOUNDED_IMPLEMENTATION",
            "F2_ENGINEERING_DISCRETION",
            "F3_ARCHITECTURE_REQUIRED",
        ]
        self.assertEqual(self.dispatch["properties"]["agent_freedom"]["enum"], expected)
        self.assertEqual(self.execution_pack["properties"]["agent_freedom"]["enum"], expected)
        self.assertIn("A stronger model does not self-promote a task to F3", self.reference)

    def test_assurance_plan_already_supports_ai_native_coverage(self) -> None:
        activity = self.assurance["properties"]["activities"]["items"]
        coverage = activity["properties"]["coverage"]
        self.assertEqual(coverage["items"]["type"], "string")
        self.assertNotIn("enum", coverage["items"])
        self.assertIn("model-diverse-adversarial", activity["properties"]["mode"]["enum"])
        self.assertEqual(
            set(activity["properties"]["independence"]["required"]),
            {"context", "model", "executor", "evidence"},
        )

    def test_review_aggregation_already_carries_provenance(self) -> None:
        activity = self.review["properties"]["activity_results"]["items"]
        provenance = activity["properties"]["reviewer_provenance"]
        self.assertTrue({"provider", "model_family", "model_id", "executor_id", "context_ref"}.issubset(set(provenance["required"])))
        self.assertEqual(self.review["properties"]["aggregation_policy"]["const"], "finding-union-blocker-dominance")
        self.assertEqual(self.review["properties"]["requested_route_authority"]["const"], "NON_AUTHORITATIVE_DERIVED_STATE")

    def test_dispatch_remains_executable_handoff_owner(self) -> None:
        required = set(self.dispatch["required"])
        for field in ("role", "execution_profile", "expected_base_sha", "pinned_standard_revision", "agent_freedom", "dispatch_state"):
            self.assertIn(field, required)
        self.assertIn("dispatch.schema.json` remains the executable handoff", self.reference)

    def test_model_metadata_does_not_prove_independence_or_authority(self) -> None:
        self.assertIn("provider/model recorded != independence proven", self.reference)
        self.assertIn("Model strength by itself does not grant F3", self.reference)
        self.assertIn("different provider/model | necessarily independent", self.reference)

    def test_same_transport_account_is_not_logical_context_identity(self) -> None:
        self.assertIn("Same transport identity is not the same concept as logical operator/context identity", self.reference)
        self.assertIn("same GitHub/API account | necessarily same logical context/operator", self.reference)

    def test_no_new_ai_assurance_or_release_state_family(self) -> None:
        self.assertIn("does not create replacement owners", self.reference)
        self.assertIn("No new AI-native PASS/READY state is introduced", self.reference)
        self.assertFalse((SCHEMAS / "ai-assurance-result-v1.schema.json").exists())
        self.assertFalse((SCHEMAS / "ai-agent-lifecycle-v1.schema.json").exists())


if __name__ == "__main__":
    unittest.main()
