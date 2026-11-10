"""End-to-end receipt verdict must reject a wrong TLC model identity.

No external solver is invoked; only the native result seam is deliberately
mocked. The real r10 suite/trace source files are loaded from the checkout.
"""
import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "v4.19" / "r10" / "suite.json"
sys.path.insert(0, str(ROOT / "suite"))
spec = importlib.util.spec_from_file_location("ads_formal_r27_runner", ROOT / "suite" / "expanded.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class InventoryAdmissionTests(unittest.TestCase):
    def test_wrong_tlc_model_id_blocks_even_when_smt_pairs_agree(self):
        declared = json.loads(SUITE.read_text("utf8"))
        self.assertTrue(declared["require_solver_pairs"])
        self.assertEqual(len(declared["cases"]), 35)
        seen = []

        def native_result(case, root, options):
            seen.append(case["id"])
            status = "COUNTEREXAMPLE" if case["purpose"] == "mutation" else "PASS_MODEL"
            return {"id": case["id"], "model_id": "FORGED-TLC-MODEL" if case["tool"] == "tlc" else case["model_id"],
                    "property_id": case["property_id"], "tool": case["tool"], "purpose": case["purpose"],
                    "status": status, "expected": case["expect"],
                    "actual": {"answers": case["expect"]} if case["tool"] != "tlc" else {"distinct_states": 27},
                    "inputs_sha256": {case["model"]: "a" * 64}}

        with tempfile.TemporaryDirectory() as tmp:
            options = types.SimpleNamespace(model=None, property=None, changed_source=None,
                                            model_head=None, source_checkout=tmp, strict_source=True,
                                            out=str(Path(tmp) / "receipt.json"))
            with (mock.patch.object(runner, "run_case", side_effect=native_result),
                  mock.patch.object(runner, "model_alignment", return_value={"status": "PASS"}),
                  mock.patch.object(runner, "toolchain_alignment", return_value={"status": "PASS", "checks": []}),
                  mock.patch.object(runner, "source_alignment", return_value={"status": "PASS", "checks": []})):
                code = runner.main_v1(options, SUITE, declared)
            report = json.loads(Path(options.out).read_text("utf8"))
        self.assertEqual(len(seen), 35)
        self.assertEqual(code, 2)
        self.assertEqual(report["model_verdict"], "BLOCKED")
        self.assertEqual(report["execution_inventory_audit"]["status"], "FAIL")
        self.assertEqual(report["coverage"]["source_bound_verified_obligations"], 0)
        self.assertTrue(any(p.get("field") == "model_id" for p in report["execution_inventory_audit"]["problems"]))


if __name__ == "__main__":
    unittest.main()
