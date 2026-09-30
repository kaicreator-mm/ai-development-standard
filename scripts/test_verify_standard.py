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
V41_CONFORMANCE = ROOT / "scripts" / "test_v41_execution_foundation_conformance.py"


class StandardVerifierRegressionTests(unittest.TestCase):
    def run_verifier(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(root / "scripts" / "verify_standard.py")],
            cwd=root, text=True, capture_output=True, check=False,
        )

    def run_v41_conformance(self, root: Path) -> subprocess.CompletedProcess[str]:
        # sys.executable and absolute file path keep checkout invocation portable.
        return subprocess.run(
            [sys.executable, str(root / "scripts" / V41_CONFORMANCE.name)],
            cwd=root, text=True, capture_output=True, check=False,
        )

    def copied_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        destination = Path(temp.name) / "repo"
        shutil.copytree(
            ROOT, destination,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )
        return temp, destination

    def test_repository_baseline_passes(self) -> None:
        result = self.run_verifier(ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_v41_execution_foundation_conformance_suite_passes(self) -> None:
        self.assertTrue(V41_CONFORMANCE.is_file())
        self.assertTrue((ROOT / "templates" / "golden" / "V41_EXECUTION_FOUNDATION_EXAMPLES.json").is_file())
        result = self.run_v41_conformance(ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("test_dependency_complete_real_owner_suites_execute", result.stdout + result.stderr)

    def test_v41_owner_weakening_is_caught_by_integrated_gate(self) -> None:
        temp, repo = self.copied_repo()
        self.addCleanup(temp.cleanup)
        owner = repo / "standards" / "DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md"
        before = owner.read_text(encoding="utf-8")
        self.assertIn("Local availability is execution evidence only", before)
        owner.write_text(
            before.replace("Local availability is execution evidence only", "Local availability controls repository compatibility", 1),
            encoding="utf-8",
        )
        result = self.run_v41_conformance(repo)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("test_agent_local_runtime_cannot_invent_repository_requirement", result.stdout + result.stderr)

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
