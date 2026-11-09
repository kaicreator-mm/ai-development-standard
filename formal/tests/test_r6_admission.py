"""R6 bounded admission test: source index and actual native solver adapter."""
import json
import os
import shutil
import sys
import types
import unittest
from pathlib import Path

FORMAL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FORMAL / "suite"))
from expanded import run_case  # noqa: E402

CASES_PATH = FORMAL / "v4.19" / "r6" / "suite.json"
PROPERTY = "ADS-P-ADMISSION-EXT"


class AdmissionExtendedTests(unittest.TestCase):
    def cases(self):
        spec = json.loads(CASES_PATH.read_text("utf-8"))
        return [c for c in spec["cases"] if c["property_id"] == PROPERTY]

    def test_registration_and_positive_negative_queries(self):
        cases = self.cases()
        self.assertEqual(len(cases), 4)
        self.assertEqual({c["tool"] for c in cases}, {"z3", "cvc5"})
        self.assertEqual({c["purpose"] for c in cases}, {"proof", "mutation"})
        expected = ["unsat"] * 3 + ["sat"] * 2 + ["unsat"] * 3 + ["sat"] * 2 + ["unsat"] * 4 + ["sat"]
        for c in cases:
            self.assertEqual(c["expect"], expected if c["purpose"] == "proof" else ["sat"] * 3)
            self.assertTrue((FORMAL / c["model"]).is_file(), c["id"])

    @unittest.skipUnless(
        (os.environ.get("ADS_FORMAL_Z3") or shutil.which("z3")) and
        (os.environ.get("ADS_FORMAL_CVC5") or shutil.which("cvc5")),
        "R6 native regression needs both verified Z3 and cvc5",
    )
    def test_actual_runner_native_adapter_and_mutants(self):
        opts = types.SimpleNamespace(
            z3=os.environ.get("ADS_FORMAL_Z3") or shutil.which("z3"),
            cvc5=os.environ.get("ADS_FORMAL_CVC5") or shutil.which("cvc5"),
            java="java", tlc_jar="/not-required-for-smt",
        )
        results = [run_case(c, FORMAL, opts) for c in self.cases()]
        self.assertEqual(
            {r["id"]: r["status"] for r in results},
            {c["id"]: ("COUNTEREXAMPLE" if c["purpose"] == "mutation" else "PASS_MODEL")
             for c in self.cases()},
        )
        for model in set(c["model"] for c in self.cases()):
            pair = {r["tool"]: r for r in results if any(
                c["id"] == r["id"] and c["model"] == model for c in self.cases()
            )}
            self.assertEqual(pair["z3"]["actual"], pair["cvc5"]["actual"])


if __name__ == "__main__":
    unittest.main()
