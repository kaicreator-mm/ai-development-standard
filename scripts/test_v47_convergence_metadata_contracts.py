from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
MANIFEST = ROOT / "standard-manifest.json"


def load(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


class ConvergenceMetadataContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.authority = load("authority-applicability-entry-v1.schema.json")
        cls.state_registry = load("state-dimension-registry-v1.schema.json")
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_authority_entry_is_discovery_metadata_only(self) -> None:
        required = set(self.authority["required"])
        self.assertIn("semantic_concern", required)
        self.assertIn("canonical_owner_ref", required)
        props = self.authority["properties"]
        for forbidden in (
            "normative_body", "mutation_allowed", "merge_allowed", "side_effect_allowed",
            "validation_state", "review_state", "deployment_state", "release_state",
        ):
            self.assertNotIn(forbidden, props)

    def test_applicability_does_not_force_optional_adoption(self) -> None:
        values = set(self.authority["properties"]["applicability_posture"]["enum"])
        self.assertEqual(values, {"ALWAYS", "MATERIALITY_DRIVEN", "OPTIONAL", "PROJECT_DEFINED"})
        self.assertNotIn("adoption_required", self.authority["properties"])

    def test_state_dimensions_bind_owner_and_vocabulary_posture(self) -> None:
        item = self.state_registry["properties"]["dimensions"]["items"]
        required = set(item["required"])
        self.assertEqual(required, {"dimension_id", "canonical_owner_ref", "vocabulary_posture"})
        self.assertEqual(
            set(item["properties"]["vocabulary_posture"]["enum"]),
            {"CLOSED", "OPEN", "OWNER_DEFINED"},
        )

    def test_forbidden_inference_binds_source_to_target(self) -> None:
        item = self.state_registry["properties"]["forbidden_inferences"]["items"]
        required = set(item["required"])
        for field in (
            "rule_id", "source_dimension_ref", "source_fact_ref",
            "target_dimension_ref", "prohibited_conclusion_ref",
        ):
            self.assertIn(field, required)

    def test_state_registry_has_no_live_state_or_authorization_fields(self) -> None:
        text = json.dumps(self.state_registry, sort_keys=True)
        for forbidden in (
            '"current_state"', '"transition"', '"mutation_allowed"', '"merge_allowed"',
            '"side_effect_allowed"', '"validation_result"', '"release_ready"',
        ):
            self.assertNotIn(forbidden, text)

    def test_no_master_pass_ready_blocked_vocabulary(self) -> None:
        text = json.dumps(self.state_registry, sort_keys=True)
        self.assertNotIn('"PASS"', text)
        self.assertNotIn('"READY"', text)
        self.assertNotIn('"BLOCKED"', text)

    def test_historical_manifest_remains_valid_without_v47_metadata(self) -> None:
        self.assertEqual(self.manifest["schema_version"], 1)
        self.assertIn("sections", self.manifest)
        self.assertNotIn("authority_applicability_registry", self.manifest)
        self.assertNotIn("state_dimension_registry", self.manifest)


if __name__ == "__main__":
    unittest.main()
