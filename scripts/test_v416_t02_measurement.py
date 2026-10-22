#!/usr/bin/env python3
"""T02 actual source-only reducer tests. Not an external billing or Tool runtime qualification."""
from __future__ import annotations
import json
import itertools
import unittest
from pathlib import Path
from v416_measurement_reconciler import metric_total, cost_total, interval_union

ROOT = Path(__file__).resolve().parents[1]
FX = ROOT / "tests/fixtures/v416/t02/scenarios.json"
METHODS = {"metrics": metric_total, "costs": cost_total, "intervals": interval_union}

class T02SourceAccountingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(FX.read_text(encoding="utf-8"))["cases"]

    def test_unique_source_contract_coverage(self):
        self.assertEqual(len(self.cases), 71)
        ids = [x["id"] for x in self.cases]
        self.assertEqual(len(ids), len(set(ids)))
        for prefix in ("C02_", "C03_", "C04_", "C05_", "C12_"):
            self.assertTrue(any(v.startswith(prefix) for v in ids), prefix)

    def test_all_real_python_fixtures(self):
        for example in self.cases:
            with self.subTest(case=example["id"]):
                self.assertEqual(METHODS[example["kind"]](example["rows"]), example["expected"])

    def test_row_order_determinism_for_each_fixture(self):
        # Order must never change source-disposition, even with conflicting replay.
        for example in self.cases:
            if len(example["rows"]) > 4:
                continue
            for perm in itertools.permutations(example["rows"]):
                with self.subTest(case=example["id"]):
                    self.assertEqual(METHODS[example["kind"]](list(perm)), example["expected"])

    def test_fail_closed_empty_populations(self):
        for name, method in METHODS.items():
            with self.subTest(kind=name):
                self.assertEqual(method([])["status"], "UNKNOWN")

    def test_full_source_only_boundedness(self):
        for case in self.cases:
            self.assertNotIn("PASS", str(case["expected"]))
            self.assertNotIn("source_is_authenticated", case)
            self.assertNotIn("provider_invoice_is_real", case)

if __name__ == "__main__":
    unittest.main(verbosity=2)
