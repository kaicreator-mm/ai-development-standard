"""Native-result identity tests: independent of external SMT/TLC binaries."""
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1] / "suite"
spec = importlib.util.spec_from_file_location("ads_r27_execution_inventory", HERE / "execution_inventory.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def case(id_, tool, purpose="proof", property_id="P"):
    return {"id": id_, "tool": tool, "purpose": purpose, "property_id": property_id,
            "model_id": "M", "model": "a.smt2", "expect": ["unsat"]}


def outcome(c):
    return {"id": c["id"], "tool": c["tool"], "purpose": c["purpose"],
            "property_id": c["property_id"], "model_id": c["model_id"],
            "expected": c["expect"], "status": "PASS_MODEL"}


class ExecutionInventoryTests(unittest.TestCase):
    def setUp(self):
        self.selected = [case("smt-z3", "z3"), case("smt-cvc5", "cvc5"),
                         case("tlc-case", "tlc", property_id="L")]
        self.results = [outcome(x) for x in self.selected]

    def test_complete_correct_inventory_passes(self):
        v = audit.audit_execution_results(self.selected, self.results)
        self.assertEqual(v["status"], "PASS")
        self.assertEqual(v["expected_count"], 3)
        self.assertEqual(v["observed_count"], 3)

    def test_tlc_identity_corrupted_after_correct_smt_pairs_fails(self):
        results = [dict(x) for x in self.results]
        results[2]["id"] = "different-tlc"
        v = audit.audit_execution_results(self.selected, results)
        self.assertEqual(v["status"], "FAIL")
        self.assertTrue(any(p.get("field") == "id" for p in v["problems"]))

    def test_tlc_result_missing_after_correct_smt_pairs_fails(self):
        self.assertEqual(audit.audit_execution_results(self.selected, self.results[:2])["status"], "FAIL")

    def test_duplicate_smt_result_must_fail(self):
        results = [dict(x) for x in self.results]
        results[1]["id"] = results[0]["id"]
        self.assertEqual(audit.audit_execution_results(self.selected, results)["status"], "FAIL")

    def test_reordered_results_fail(self):
        self.assertEqual(audit.audit_execution_results(self.selected, self.results[::-1])["status"], "FAIL")

    def test_swapped_purpose_is_not_a_proof(self):
        results = [dict(x) for x in self.results]
        results[0]["purpose"] = "mutation"
        self.assertEqual(audit.audit_execution_results(self.selected, results)["status"], "FAIL")

    def test_wrong_model_or_property_rejected(self):
        for field in ("model_id", "property_id", "tool"):
            with self.subTest(field=field):
                results = [dict(x) for x in self.results]
                results[0][field] = "other"
                self.assertEqual(audit.audit_execution_results(self.selected, results)["status"], "FAIL")

    def test_expected_answer_swapped_rejected(self):
        results = [dict(x) for x in self.results]
        results[0]["expected"] = ["sat"]
        self.assertEqual(audit.audit_execution_results(self.selected, results)["status"], "FAIL")

    def test_empty_or_invalid_selection_fail(self):
        for selected, results in (([], []), (None, []), ("bad", [])):
            with self.subTest(selected=selected):
                self.assertEqual(audit.audit_execution_results(selected, results)["status"], "FAIL")

    def test_malformed_result_rejected(self):
        results = [dict(x) for x in self.results]
        results[2] = None
        self.assertEqual(audit.audit_execution_results(self.selected, results)["status"], "FAIL")

    def test_missing_or_invalid_status_rejected(self):
        for status in (None, "PASS", "unknown"):
            with self.subTest(status=status):
                results = [dict(x) for x in self.results]
                results[0]["status"] = status
                self.assertEqual(audit.audit_execution_results(self.selected, results)["status"], "FAIL")

    def test_old_aggregator_can_false_pass_with_wrong_tlc_metadata(self):
        corrupted = [dict(x) for x in self.results]
        corrupted[2]["model_id"] = "foreign-model"
        # Old differential verifies global result IDs and SMT pairs, not TLC
        # model_id/property/purpose. This is still a valid-ID result set.
        old_good = bool(corrupted) and all(
            r["status"] in ("PASS_MODEL", "COUNTEREXAMPLE") for r in corrupted
        ) and {r["id"] for r in corrupted} == {c["id"] for c in self.selected}
        self.assertTrue(old_good)
        self.assertEqual(audit.audit_execution_results(self.selected, corrupted)["status"], "FAIL")

    def test_permuted_valid_tlc_case_ids_fail(self):
        extra = case("second-tlc", "tlc", property_id="L")
        cases = self.selected + [extra]
        results = [outcome(x) for x in cases]
        results[2]["id"], results[3]["id"] = results[3]["id"], results[2]["id"]
        self.assertEqual({r["id"] for r in results}, {c["id"] for c in cases})
        self.assertEqual(audit.audit_execution_results(cases, results)["status"], "FAIL")

    def test_extra_result_rejected(self):
        self.assertEqual(audit.audit_execution_results(self.selected, self.results + [self.results[0]])["status"], "FAIL")


    def test_tlc_proof_counterexample_status_must_fail_identity_audit(self):
        results = [dict(x) for x in self.results]
        results[2]["status"] = "COUNTEREXAMPLE"
        report = audit.audit_execution_results(self.selected, results)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(p.get("reason") == "SUCCESS_STATUS_PURPOSE_MISMATCH"
                            for p in report["problems"]))

    def test_tlc_mutation_pass_model_status_must_fail_identity_audit(self):
        mutation = case("tlc-mutant", "tlc", purpose="mutation")
        selected = self.selected + [mutation]
        results = [dict(x) for x in self.results] + [outcome(mutation)]
        report = audit.audit_execution_results(selected, results)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(p.get("reason") == "SUCCESS_STATUS_PURPOSE_MISMATCH"
                            for p in report["problems"]))

    def test_tlc_correct_mutation_success_remains_accepted(self):
        mutation = case("tlc-mutant", "tlc", purpose="mutation")
        selected = self.selected + [mutation]
        mutation_result = outcome(mutation)
        mutation_result["status"] = "COUNTEREXAMPLE"
        self.assertEqual(audit.audit_execution_results(
            selected, self.results + [mutation_result])["status"], "PASS")

    def test_invalid_selected_purpose_is_fail_closed(self):
        selected = [dict(x) for x in self.selected]
        selected[2]["purpose"] = "other"
        results = [dict(x) for x in self.results]
        results[2]["purpose"] = "other"
        self.assertEqual(audit.audit_execution_results(selected, results)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
