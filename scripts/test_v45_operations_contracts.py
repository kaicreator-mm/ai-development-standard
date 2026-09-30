from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict:
    return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))


class OperationsContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.observation = load("runtime-observation-context-v1.schema.json")
        cls.incident = load("incident-event-v1.schema.json")
        cls.maintenance = load("maintenance-policy-v1.schema.json")

    def test_runtime_observation_binds_subject_and_window(self) -> None:
        required = set(self.observation["required"])
        self.assertTrue({
            "artifact_ref",
            "deployment_ref",
            "environment_ref",
            "observation_window",
            "signal_refs",
        }.issubset(required))
        self.assertEqual(
            set(self.observation["properties"]["observation_window"]["required"]),
            {"start_ref", "end_ref"},
        )

    def test_runtime_observation_has_no_universal_health_or_gate_state(self) -> None:
        props = self.observation["properties"]
        for forbidden in ("healthy", "pass", "ready", "validation_state", "release_state", "gate_state"):
            self.assertNotIn(forbidden, props)

    def test_signal_classes_are_extensible(self) -> None:
        classes = self.observation["properties"]["signal_classes"]
        self.assertEqual(classes["items"]["type"], "string")
        self.assertNotIn("enum", classes["items"])

    def test_incident_is_append_fact_not_mutable_current_state(self) -> None:
        required = set(self.incident["required"])
        self.assertTrue({"incident_id", "event_id", "event_kind", "occurred_at", "actor_or_authority_ref"}.issubset(required))
        props = self.incident["properties"]
        self.assertNotIn("current_state", props)
        self.assertNotIn("status", props)
        self.assertNotIn("closed", props)
        self.assertNotIn("enum", props["event_kind"])

    def test_incident_can_reference_recovery_and_follow_up_without_owning_them(self) -> None:
        props = self.incident["properties"]
        self.assertIn("deployment_recovery_refs", props)
        self.assertIn("migration_recovery_refs", props)
        self.assertIn("engineering_follow_up_refs", props)

    def test_maintenance_support_is_explicit_authority_not_branch_presence(self) -> None:
        line = self.maintenance["properties"]["support_lines"]["items"]
        required = set(line["required"])
        self.assertTrue({"line_id", "baseline_ref", "support_state", "allowed_change_classes", "authority_ref"}.issubset(required))
        self.assertNotIn("enum", line["properties"]["support_state"])
        self.assertNotIn("branch", line["properties"])
        self.assertNotIn("tag", line["properties"])
        self.assertNotIn("package", line["properties"])

    def test_backport_result_binds_source_target_result_and_evidence(self) -> None:
        props = self.maintenance["properties"]
        self.assertIn("backport_results", props)
        result = props["backport_results"]["items"]
        required = set(result["required"])
        self.assertTrue({
            "source_ref",
            "target_support_line_ref",
            "target_baseline_ref",
            "result_sha_ref",
            "validation_refs",
        }.issubset(required))
        self.assertEqual(result["properties"]["validation_refs"]["minItems"], 1)
        self.assertIn("review_refs", result["properties"])
        self.assertIn("release_refs", result["properties"])

    def test_source_only_pass_cannot_satisfy_result_sha_evidence(self) -> None:
        props = self.maintenance["properties"]
        result = props["backport_results"]["items"]
        required = set(result["required"])
        self.assertIn("result_sha_ref", required)
        self.assertIn("validation_refs", required)
        self.assertNotIn("validation_ref", result["properties"]["source_ref"])
        for ambiguous_top_level in (
            "backport_source_refs",
            "result_sha_refs",
            "validation_refs",
            "review_refs",
            "release_refs",
        ):
            self.assertNotIn(ambiguous_top_level, props)

    def test_no_contract_stores_ordinary_sensitive_values(self) -> None:
        combined = json.dumps([self.observation, self.incident, self.maintenance]).lower()
        for forbidden in ("secret_value", "credential_value", "password", "access_token", "raw_payload"):
            self.assertNotIn(forbidden, combined)

    def test_contracts_do_not_create_validation_or_release_pass(self) -> None:
        for schema in (self.observation, self.incident, self.maintenance):
            props = schema["properties"]
            self.assertNotIn("validation_state", props)
            self.assertNotIn("release_state", props)
            self.assertNotIn("pass", props)


if __name__ == "__main__":
    unittest.main()
