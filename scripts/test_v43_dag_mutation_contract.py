from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "dag-mutation-record-v1.schema.json"


class DagMutationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.props = cls.schema["properties"]
        cls.required = set(cls.schema["required"])

    def test_core_attribution_and_impact_fields_are_required(self) -> None:
        expected = {
            "mutation_id",
            "mutation_class",
            "requested_by",
            "approved_by",
            "reason",
            "affected_task_refs",
            "old_topology_ref",
            "new_topology_ref",
            "old_edges",
            "new_edges",
            "scope_impact",
            "release_impact",
            "task_pack_impact_refs",
            "review_impact",
            "validation_impact_ref",
        }
        self.assertTrue(expected.issubset(self.required))

    def test_mutation_class_is_extensible(self) -> None:
        self.assertEqual(self.props["mutation_class"]["type"], "string")
        self.assertNotIn("enum", self.props["mutation_class"])

    def test_dependency_removal_cannot_omit_reason_or_authority(self) -> None:
        self.assertIn("reason", self.required)
        self.assertIn("requested_by", self.required)
        self.assertIn("approved_by", self.required)

    def test_old_and_new_topology_are_reconstructible(self) -> None:
        for key in ("old_topology_ref", "new_topology_ref", "old_edges", "new_edges"):
            self.assertIn(key, self.required)
        self.assertEqual(self.props["old_edges"]["type"], "array")
        self.assertEqual(self.props["new_edges"]["type"], "array")

    def test_task_pack_review_validation_impact_is_representable(self) -> None:
        self.assertIn("task_pack_impact_refs", self.required)
        self.assertIn("review_impact", self.required)
        self.assertIn("validation_impact_ref", self.required)

    def test_schema_does_not_own_readiness_or_native_mutation(self) -> None:
        forbidden = {
            "task_state",
            "ready",
            "readiness",
            "dispatch_state",
            "validation_state",
            "release_state",
            "apply_mutation",
            "mutation_executed",
        }
        self.assertTrue(forbidden.isdisjoint(self.props))

    def test_schema_is_record_only_and_closed(self) -> None:
        self.assertEqual(self.schema["type"], "object")
        self.assertFalse(self.schema["additionalProperties"])
        self.assertEqual(self.props["schema_version"]["const"], 1)


if __name__ == "__main__":
    unittest.main()
