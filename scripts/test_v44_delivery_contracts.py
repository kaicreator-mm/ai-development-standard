from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict:
    return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))


class DeliveryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.build = load("build-manifest-v1.schema.json")
        cls.promotion = load("artifact-promotion-v1.schema.json")
        cls.plan = load("deployment-plan-v1.schema.json")
        cls.result = load("deployment-result-v1.schema.json")

    def test_four_contracts_are_distinct_closed_objects(self) -> None:
        ids = {
            self.build["$id"],
            self.promotion["$id"],
            self.plan["$id"],
            self.result["$id"],
        }
        self.assertEqual(len(ids), 4)
        for schema in (self.build, self.promotion, self.plan, self.result):
            self.assertEqual(schema["type"], "object")
            self.assertFalse(schema["additionalProperties"])
            self.assertEqual(schema["properties"]["schema_version"]["const"], 1)

    def test_build_output_is_not_promoted_artifact(self) -> None:
        self.assertIn("outputs", self.build["required"])
        self.assertNotIn("artifact", self.build["properties"])
        self.assertIn("artifact", self.promotion["required"])
        artifact = self.promotion["properties"]["artifact"]
        self.assertIn("immutable_identity", artifact["required"])
        self.assertIn("build_ref", self.promotion["required"])

    def test_plan_and_result_are_separate_truth_objects(self) -> None:
        self.assertIn("side_effect_authority_ref", self.plan["required"])
        self.assertNotIn("result_state", self.plan["properties"])
        self.assertIn("plan_ref", self.result["required"])
        self.assertIn("result_state", self.result["required"])

    def test_deployment_results_are_namespaced_domain_facts(self) -> None:
        states = self.result["properties"]["result_state"]["enum"]
        self.assertTrue(states)
        self.assertTrue(all(state.startswith("DEPLOYMENT_") for state in states))
        self.assertNotIn("PASS", states)
        self.assertNotIn("READY", states)
        self.assertNotIn("FAIL", states)

    def test_artifact_identity_is_immutable_identity_not_alias(self) -> None:
        artifact = self.promotion["properties"]["artifact"]
        self.assertIn("immutable_identity", artifact["required"])
        self.assertNotIn("tag", artifact["properties"])
        self.assertNotIn("channel", artifact["properties"])
        self.assertNotIn("filename", artifact["properties"])

    def test_plan_binds_artifact_environment_and_authority(self) -> None:
        required = set(self.plan["required"])
        self.assertTrue({"artifact_ref", "target_environment_ref", "side_effect_authority_ref"}.issubset(required))
        self.assertIn("migration_transition_refs", self.plan["properties"])
        self.assertIn("secret_refs", self.plan["properties"])

    def test_result_is_exact_plan_artifact_environment_scoped(self) -> None:
        required = set(self.result["required"])
        self.assertTrue({"plan_ref", "artifact_ref", "target_environment_ref"}.issubset(required))
        self.assertIn("rollback_result_ref", self.result["properties"])

    def test_no_contract_has_generic_validation_or_release_state(self) -> None:
        forbidden = {"pass", "validation_state", "release_state", "release_ready", "gate_state"}
        for schema in (self.build, self.promotion, self.plan, self.result):
            self.assertTrue(forbidden.isdisjoint(schema["properties"]))

    def test_no_ordinary_secret_value_fields(self) -> None:
        combined = json.dumps([self.build, self.promotion, self.plan, self.result]).lower()
        for forbidden in ("secret_value", "credential_value", "password", "access_token"):
            self.assertNotIn(forbidden, combined)


if __name__ == "__main__":
    unittest.main()
