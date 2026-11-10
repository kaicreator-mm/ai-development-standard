"""No native binaries required: prove R13 input pinning fails before subprocess."""
import hashlib
import importlib
import pathlib
import tempfile
import unittest
from unittest import mock
import run_proofs as proof


class ExactGitBindingPreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="ads1366-bind-test-")
        self.addCleanup(self.tmp.cleanup)
        root = pathlib.Path(self.tmp.name)
        for name in proof.PINNED_MODEL_GIT_BLOBS:
            (root / name).write_bytes((proof.ROOT / name).read_bytes())
        self.root_patcher = mock.patch.object(proof, "ROOT", root)
        self.root_patcher.start()
        self.addCleanup(self.root_patcher.stop)

    def test_valid_exact_model_blobs(self):
        self.assertEqual(len(proof.assert_model_hashes("preflight")), 2)

    def test_comment_only_model_change_fails_before_solver(self):
        file = proof.ROOT / "publish-safety.smt2"
        file.write_text(file.read_text() + "\n; harmless comment that leaves SAT answers untouched\n")
        with mock.patch.object(proof, "run_solver", side_effect=AssertionError("must not spawn")) as run:
            with self.assertRaisesRegex(proof.InputBindingError, "model publish-safety.smt2 blob"):
                proof.verify()
            run.assert_not_called()

    def test_missing_model_fails_before_solver(self):
        (proof.ROOT / "weak-admission-gap.smt2").unlink()
        with mock.patch.object(proof, "run_solver", side_effect=AssertionError("must not spawn")) as run:
            with self.assertRaisesRegex(proof.InputBindingError, "missing/unreadable model"):
                proof.verify()
            run.assert_not_called()

    def test_unpinned_tool_fails_before_solver(self):
        bad = proof.ROOT / "not-z3"
        bad.write_text("invalid binary")
        with mock.patch.dict(proof.COMMANDS, {"z3": [str(bad), "-smt2"]}):
            with mock.patch.object(proof, "run_solver", side_effect=AssertionError("must not spawn")) as run:
                with self.assertRaisesRegex(proof.InputBindingError, "tool preflight: z3 SHA256"):
                    proof.verify()
                run.assert_not_called()

    def test_missing_tool_fails_before_solver(self):
        with mock.patch.dict(proof.COMMANDS, {"z3": [str(proof.ROOT / 'missing'), "-smt2"]}):
            with mock.patch.object(proof, "run_solver", side_effect=AssertionError("must not spawn")) as run:
                with self.assertRaisesRegex(proof.InputBindingError, "tool preflight: unreadable z3"):
                    proof.verify()
                run.assert_not_called()

    def test_postflight_tamper_detected(self):
        with mock.patch.object(proof, "assert_tool_hashes", return_value=[{"status":"PASS"}]), \
             mock.patch.object(proof, "run_solver") as run:
            def side_effect(tool, path):
                if tool == "cvc5" and path.name == "publish-safety.smt2":
                    path.write_text(path.read_text() + "\n; changed during validation\n")
                return {"tool": tool,"matched": True,"statuses":proof.EXPECTED[path.name]}
            run.side_effect = side_effect
            with self.assertRaisesRegex(proof.InputBindingError, "postflight: model publish-safety.smt2 blob"):
                proof.verify()


if __name__ == "__main__":
    unittest.main()
