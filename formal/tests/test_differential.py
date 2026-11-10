"""Fail-closed differential coverage tests with no external solver dependency."""
import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "suite" / "differential.py"
spec = importlib.util.spec_from_file_location("ads_formal_differential", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def case(tool, purpose="proof", model="m.smt2"):
    return {"id": f"{model}-{purpose}-{tool}", "tool": tool,
            "property_id": "P", "model": model, "purpose": purpose}


def result(c, answer="unsat"):
    return {"id": c["id"], "tool": c["tool"],
            "status": "COUNTEREXAMPLE" if c["purpose"] == "mutation" else "PASS_MODEL",
            "expected": [answer], "actual": {"answers": [answer]},
            "inputs_sha256": {c["model"]: "a" * 64}}


class DifferentialCoverageTests(unittest.TestCase):
    def test_normal_pair_passes(self):
        cases = [case("z3"), case("cvc5")]
        self.assertEqual([x["status"] for x in module.solver_differential(
            cases, [result(c) for c in cases], require_pairs=True)], ["PASS"])

    def test_mandatory_pair_rejects_missing_cvc5_or_z3(self):
        for tool in ("z3", "cvc5"):
            with self.subTest(lone_tool=tool):
                c = case(tool)
                got = module.solver_differential([c], [result(c)], require_pairs=True)
                self.assertEqual(got[0]["status"], "INCONCLUSIVE")
                self.assertEqual(got[0]["reason"], "MISSING_INDEPENDENT_SOLVER_PAIR")

    def test_legacy_single_solver_remains_allowed(self):
        c = case("z3")
        self.assertEqual(module.solver_differential([c], [result(c)]), [])

    def test_mutant_is_an_independent_pair(self):
        cases = [case("z3", "mutation"), case("cvc5", "mutation")]
        self.assertEqual([x["status"] for x in module.solver_differential(
            cases, [result(c, "sat") for c in cases], True)], ["PASS"])

    def test_missing_duplicate_or_wrong_tool_outcomes_fail_closed(self):
        cases = [case("z3"), case("cvc5")]
        a, b = [result(c) for c in cases]
        for responses in ([a], [a, a, b], [a, {**b, "tool": "z3"}],
                          [a, {**b, "actual": {"answers": ["sat"]}}],
                          [a, b, {**b, "id": "orphan"}]):
            with self.subTest(responses=responses):
                reports = module.solver_differential(cases, responses, True)
                self.assertIn("INCONCLUSIVE", [r["status"] for r in reports])

    def test_distinct_models_not_overwritten(self):
        cases = [case(tool, model=model) for model in ("a.smt2", "b.smt2")
                 for tool in ("z3", "cvc5")]
        answers = ["unsat" if c["model"] == "a.smt2" else "sat" for c in cases]
        responses = [result(c, a) for c, a in zip(cases, answers)]
        self.assertEqual([r["status"] for r in module.solver_differential(
            cases, responses, True)], ["PASS", "PASS"])


if __name__ == "__main__":
    unittest.main()
