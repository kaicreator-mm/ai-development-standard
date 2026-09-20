from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "scripts" / "verify_standard.py"


class StandardVerifierRegressionTests(unittest.TestCase):
    def run_verifier(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(root / "scripts" / "verify_standard.py")],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )

    def copied_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        destination = Path(temp.name) / "repo"
        shutil.copytree(
            ROOT,
            destination,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )
        return temp, destination

    def test_repository_baseline_passes(self) -> None:
        result = self.run_verifier(ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_asset_and_manifest_entry_cannot_be_deleted_together(self) -> None:
        temp, repo = self.copied_repo()
        self.addCleanup(temp.cleanup)

        victim = "standards/CHATGPT_WEB_ROLE.md"
        (repo / victim).unlink()

        manifest_path = repo / "standard-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for entries in manifest["sections"].values():
            if victim in entries:
                entries.remove(victim)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

        result = self.run_verifier(repo)
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn(victim, output)
        self.assertTrue(
            "bootstrap-required asset is missing" in output
            or "manifest omits bootstrap-required asset" in output,
            output,
        )


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(StandardVerifierRegressionTests)
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
