"""No solvers and no network required for model provenance regression tests."""
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ads_model_provenance", HERE / "suite" / "provenance.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ProvenanceTests(unittest.TestCase):
    def test_clean_dirty_wrong_head_missing_and_untracked(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            def git(*args):
                return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()
            git("init", "-q")
            git("config", "user.name", "ADS Test")
            git("config", "user.email", "ads-test@example.invalid")
            formal = repo / "formal"
            (formal / "suite").mkdir(parents=True)
            model = formal / "suite" / "model.smt2"
            model.write_text("(check-sat)\n")
            git("add", ".")
            git("commit", "-qm", "baseline")
            head = git("rev-parse", "HEAD")
            inputs = ["suite/model.smt2"]
            self.assertEqual(module.model_alignment(formal, inputs, head)["status"], "PASS")
            self.assertEqual(module.model_alignment(formal, inputs, None)["status"], "NOT_RUN")
            self.assertEqual(module.model_alignment(formal, inputs, "0" * 40)["status"], "BLOCKED")
            model.write_text("(check-sat)\n; changed\n")
            self.assertEqual(module.model_alignment(formal, inputs, head)["status"], "FAIL")
            git("checkout", "--", "formal/suite/model.smt2")
            (formal / "suite" / "untracked.smt2").write_text("(check-sat)")
            self.assertEqual(module.model_alignment(formal, ["suite/untracked.smt2"], head)["status"], "FAIL")
            self.assertEqual(module.model_alignment(formal, ["../escape"], head)["status"], "FAIL")
            self.assertEqual(module.model_alignment(formal, [], head)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
