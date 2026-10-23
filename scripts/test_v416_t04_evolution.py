#!/usr/bin/env python3
"""T04 deterministic source-contract examples, NOT a real experimental engine."""
from __future__ import annotations
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FX = ROOT / "tests/fixtures/v416/t04/scenarios.json"
DOC = ROOT / "references/ADS_V416_APPLICABILITY_EVOLUTION.md"
ROUTE = {"PROJECT_DEFECT": "ROUTE_PROJECT",
         "AGENT_EXECUTION_DEFECT": "ROUTE_EXECUTION",
         "ENVIRONMENT_OR_TOOL_DEFECT": "ROUTE_ENVIRONMENT",
         "PROJECT_SPECIFIC_REQUIREMENT": "ROUTE_PROJECT_SPECIFIC",
         "STANDARD_FRICTION_CANDIDATE": "MORE_EVIDENCE",
         "ADS_EVOLUTION_CANDIDATE": "OPEN_ADS_INTAKE"}


def bounded_cost_example(o: dict) -> str:
    evidence = ("cohort_matched", "verifier_matched", "window_matched",
                "denominator_complete", "all_outcomes_included",
                "source_costs_complete", "disjoint_accounting",
                "comparable_currency", "selection_bias_controlled")
    return "COMPARABLE_OBSERVATION" if all(o[k] for k in evidence) else "UNKNOWN"


def applicability_example(o: dict) -> str:
    if o["exclusion_present"]:
        return "NOT_APPLICABLE"
    checks = ("task_profile_current", "matched_domain", "matched_toolchain",
              "source_qualified", "independent_verifier", "counterexample_checked")
    return "APPLICABLE_EVIDENCE" if all(o[k] for k in checks) else "MORE_EVIDENCE"


def publication_example(o: dict) -> str:
    return "PUBLISH_MINIMAL" if o["owner_cleared"] and o["publication_class"] == "PUBLISHABLE" else "WITHHOLD"


class T04SourceExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = json.loads(FX.read_text(encoding="utf8"))
        cls.doc = DOC.read_text(encoding="utf8")

    def test_unique_coverage(self):
        self.assertEqual(self.fixtures["schema"], "ads/v416-t04-source-oracle/v1")
        all_cases = [v for group in ("C11", "C13", "C14", "publication") for v in self.fixtures[group]]
        self.assertEqual(len(all_cases), 26)
        self.assertEqual(len({v["id"] for v in all_cases}), len(all_cases))

    def test_comparison_and_counterexamples(self):
        for v in self.fixtures["C11"]:
            with self.subTest(v=v["id"]):
                self.assertEqual(bounded_cost_example(v["input"]), v["expected"])

    def test_applicability_and_exclusions(self):
        for v in self.fixtures["C13"]:
            with self.subTest(v=v["id"]):
                self.assertEqual(applicability_example(v["input"]), v["expected"])

    def test_evolution_owner_and_privacy(self):
        for v in self.fixtures["C14"]:
            with self.subTest(v=v["id"]):
                self.assertEqual(ROUTE[v["classification"]], v["expected"])
        for v in self.fixtures["publication"]:
            with self.subTest(v=v["id"]):
                self.assertEqual(publication_example(v), v["expected"])

    def test_normative_owner_no_auto_promotion(self):
        for token in ("DEVELOPMENT_WORKFLOW.md", "TASK_LEARNING_EVIDENCE_REFERENCE.md",
                      "PUBLISHABLE", "PROJECT_PRIVATE", "RESTRICTED",
                      "NO_CHANGE", "MORE_EVIDENCE", "OPEN_ADS_INTAKE",
                      "Task Learning", "not an approved modification"):
            with self.subTest(token=token):
                self.assertIn(token.lower(), self.doc.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
