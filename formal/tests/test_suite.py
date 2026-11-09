import importlib.util
import tempfile
import unittest
from pathlib import Path

RUNNER = Path(__file__).resolve().parents[1] / "suite" / "run.py"
spec = importlib.util.spec_from_file_location("ads_formal_suite", RUNNER)
suite = importlib.util.module_from_spec(spec)
spec.loader.exec_module(suite)


class SuiteTests(unittest.TestCase):
    def test_safe_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "good.smt2").write_text("(check-sat)")
            self.assertEqual(suite.safe_file(base, "good.smt2", ".smt2").name, "good.smt2")
            for bad in ("../out.txt", "/etc/passwd", "missing.smt2"):
                with self.assertRaises(ValueError):
                    suite.safe_file(base, bad)

    def test_no_checkout_not_run(self):
        self.assertEqual(suite.source_check(None, {"candidate_head": "a"})["status"], "NOT_RUN")

    def test_wrong_checkout_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(suite.source_check(tmp, {"candidate_head": "0" * 40})["status"],
                             "BLOCKED_WRONG_HEAD")

    def test_missing_tool_does_not_pass(self):
        class Args:
            z3 = "__ads_intentionally_missing_z3__"
            java = "java"
            tlc_jar = "/missing.jar"
        base = Path(__file__).resolve().parents[1] / "v4.19" / "r0"
        x = suite.check({"id": "negative", "tool": "z3", "purpose": "proof",
                         "model": "roles.smt2", "expect": ["unsat"]}, base, Args)
        self.assertEqual(x["status"], "NOT_RUN")

    def test_unknown_not_unsat(self):
        self.assertNotEqual(suite.ANSWER.findall("unknown\n"), ["unsat"])


if __name__ == "__main__":
    unittest.main()
