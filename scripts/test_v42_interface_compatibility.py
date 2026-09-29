from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md"
REFERENCE = ROOT / "references" / "INTERFACE_COMPATIBILITY_REFERENCE.md"
SCHEMA = ROOT / "schemas" / "compatibility-record-v1.schema.json"


class InterfaceCompatibilityGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    def test_contract_baseline_candidate_and_operations_are_explicit(self) -> None:
        text = self.standard.lower()
        for phrase in (
            "canonical contract kind/identity",
            "baseline identity",
            "candidate identity",
            "change operation",
        ):
            self.assertIn(phrase, text)

        required = set(self.schema["required"])
        self.assertTrue({"contract", "baseline", "candidate", "change_operations", "dimensions"}.issubset(required))

    def test_change_operation_and_dimension_outcome_remain_orthogonal(self) -> None:
        props = self.schema["properties"]
        self.assertIn("change_operations", props)
        self.assertIn("dimensions", props)
        outcomes = props["dimensions"]["items"]["properties"]["outcome"]["enum"]
        self.assertNotIn("PASS", outcomes)
        self.assertNotIn("FAIL", outcomes)
        self.assertIn("No operation name implies a universal compatibility result", self.standard)

    def test_dimensions_are_extensible_and_missing_does_not_mean_compatible(self) -> None:
        dimension = self.schema["properties"]["dimensions"]["items"]
        self.assertEqual(dimension["properties"]["name"]["type"], "string")
        self.assertNotIn("enum", dimension["properties"]["name"])
        self.assertNotIn("default", dimension["properties"]["outcome"])
        self.assertIn("Absence of a dimension means **not evaluated**, not compatible", self.standard)
        self.assertIn("dimension missing or `UNKNOWN`", self.standard)

    def test_required_adversarial_inferences_are_rejected(self) -> None:
        required_rows = (
            "| wire-safe | source compatible |",
            "| schema/checker passes | behavior compatible |",
            "| new provider + new consumer pass | old/external consumer compatible |",
            "| dimension missing or `UNKNOWN` | compatible |",
            "| generated client/codegen succeeds | generated artifact is contract authority or proves compatibility |",
        )
        for row in required_rows:
            self.assertIn(row, self.standard)

    def test_consumer_window_and_generated_artifact_boundaries_are_explicit(self) -> None:
        text = self.standard.lower()
        self.assertIn("compatibility window", text)
        self.assertIn("older supported consumers", text)
        self.assertIn("external consumers", text)
        self.assertIn("generated output", text)
        self.assertIn("must not become the canonical contract authority", text)

    def test_deprecation_removal_requires_explicit_authority(self) -> None:
        self.assertIn("Deprecation is a compatibility transition", self.standard)
        self.assertIn("explicit authority for the removal decision", self.standard)
        self.assertIn("Elapsed time alone", self.standard)

    def test_fast_path_is_materiality_driven(self) -> None:
        self.assertIn("need not create empty compatibility records", self.standard)
        self.assertIn("MUST NOT use Fast Path to bypass compatibility evidence", self.standard)

    def test_reference_keeps_tool_output_subordinate(self) -> None:
        self.assertIn("Tool output is evidence, not policy authority", self.reference)
        self.assertIn("New/new success cannot erase old/new risk", self.reference)


if __name__ == "__main__":
    unittest.main()
