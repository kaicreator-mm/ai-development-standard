"""Targeted exact-model test for the R8 successor safety repair."""
import hashlib
import os
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "models" / "authority"
EXPECTED = ["unsat"] * 3 + ["sat"] * 2 + ["unsat"] * 3 + ["sat"] * 2 + ["unsat"] * 3 + ["unsat"] * 4 + ["sat"]
SOURCES = {
    "admission-boundaries-r8.smt2": ("ba38ca65e5f4c3982d0295954a75f5041ae1f4131317f01fdb49ea45f2499daf", EXPECTED),
    "admission-boundaries-r8-mutant.smt2": ("c47171e6a82faac2bc291dcd94af48684027a65d646c29f4e133f248f2d9fab8", ["sat"] * 3),
}
SOLVERS = {"z3": ["z3", "-smt2"], "cvc5": ["cvc5", "--lang=smt2", "--incremental"]}


class R8Targeted(unittest.TestCase):
    def test_checked_in_inputs(self):
        for name, (sha, _) in SOURCES.items():
            p = ROOT / name
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), sha)

    def test_native_answers(self):
        import shutil
        for tool, args in SOLVERS.items():
            actual = os.getenv("ADS_FORMAL_" + tool.upper()) or shutil.which(args[0])
            if actual is None:
                self.skipTest("native solver not installed: " + tool)
            for name, (_, expected) in SOURCES.items():
                with self.subTest(tool=tool, model=name):
                    r = subprocess.run([actual, *args[1:], str(ROOT / name)],
                                       capture_output=True, text=True, timeout=30)
                    self.assertEqual(r.returncode, 0, r.stderr)
                    self.assertEqual(r.stdout.strip().splitlines(), expected)


if __name__ == "__main__":
    unittest.main()
