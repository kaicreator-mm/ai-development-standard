from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "docs" / "implementation" / "4.2.0" / "dogfood" / "T04_api_compatibility_cases.json"


def evaluate(case: dict, required_dimensions: list[str]) -> bool:
    if case["tested_baseline"] != case["expected_baseline"]:
        return False
    if case["tested_consumer"] != case["expected_consumer"]:
        return False
    dimensions = case["dimensions"]
    return all(dimensions.get(name) == "COMPATIBLE" for name in required_dimensions)


class APICompatibilityConformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.required_dimensions = payload["required_dimensions"]
        cls.cases = {case["id"]: case for case in payload["cases"]}

    def assert_case(self, case_id: str) -> None:
        case = self.cases[case_id]
        self.assertEqual(evaluate(case, self.required_dimensions), case["expected_compatible"])

    def test_additive_backward_compatible_positive(self) -> None:
        self.assert_case("additive-positive")
        self.assertTrue(evaluate(self.cases["additive-positive"], self.required_dimensions))

    def test_wire_safe_does_not_imply_source_compatible(self) -> None:
        self.assert_case("wire-safe-source-break")
        self.assertEqual(self.cases["wire-safe-source-break"]["dimensions"]["wire"], "COMPATIBLE")
        self.assertEqual(self.cases["wire-safe-source-break"]["dimensions"]["source"], "INCOMPATIBLE")

    def test_schema_safe_does_not_imply_behavior_compatible(self) -> None:
        self.assert_case("schema-safe-behavior-break")
        self.assertEqual(self.cases["schema-safe-behavior-break"]["dimensions"]["schema"], "COMPATIBLE")
        self.assertEqual(self.cases["schema-safe-behavior-break"]["dimensions"]["behavior"], "INCOMPATIBLE")

    def test_new_new_pass_does_not_prove_old_consumer_new_producer(self) -> None:
        self.assert_case("new-new-does-not-prove-old-new")
        case = self.cases["new-new-does-not-prove-old-new"]
        self.assertNotEqual(case["tested_consumer"], case["expected_consumer"])

    def test_baseline_identity_drift_invalidates_prior_claim(self) -> None:
        self.assert_case("baseline-drift")
        case = self.cases["baseline-drift"]
        self.assertNotEqual(case["tested_baseline"], case["expected_baseline"])

    def test_unknown_or_unexecuted_dimension_is_not_compatible(self) -> None:
        self.assert_case("unknown-unexecuted-dimension")
        self.assertEqual(self.cases["unknown-unexecuted-dimension"]["dimensions"]["behavior"], "UNKNOWN")

    def test_fixture_covers_all_required_scenarios(self) -> None:
        self.assertEqual(
            set(self.cases),
            {
                "additive-positive",
                "wire-safe-source-break",
                "schema-safe-behavior-break",
                "new-new-does-not-prove-old-new",
                "baseline-drift",
                "unknown-unexecuted-dimension",
            },
        )


if __name__ == "__main__":
    unittest.main()
