from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("verify_project_execution_profile.py")

BASE = """# Project Overrides
- CI profile: minimal
- Exact-SHA clean-validation fallback: local clean checkout
- Disabled reason (for `disabled`): NOT_APPLICABLE
- CI provider: woodpecker
- CI backend / execution model: local
- CI runner role: ubuntu-build-host
- Workflow config: .woodpecker/verify.yaml
- Workflow config source: repository exact SHA
- Execution shell / entrypoint model: bash
- Runtime source: host preflight
- Clone / checkout model: clean checkout
- Partial clone policy: disabled
- Submodule policy: disabled
- Git LFS policy: disabled
- Fresh-run / rerun policy: fresh run for new SHA
"""


def run(text: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        d = root / ".dev-standard"
        d.mkdir()
        (d / "PROJECT_OVERRIDES.md").write_text(text, encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), str(root)], text=True, capture_output=True, check=False)


class Tests(unittest.TestCase):
    def test_v4131_requires_selected_provider_checks(self) -> None:
        valid = BASE + "- Required CI checks: ci/woodpecker/push/ci\n"
        def run_versioned(text: str) -> subprocess.CompletedProcess[str]:
            with tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                d = root / ".dev-standard"
                d.mkdir()
                (d / "PROJECT_OVERRIDES.md").write_text(text, encoding="utf-8")
                (d / "VERSION").write_text(
                    "repository=kaicreator-mm/ai-development-standard\n"
                    "version=4.13.1\n"
                    "revision=0123456789abcdef0123456789abcdef01234567\n",
                    encoding="utf-8",
                )
                return subprocess.run(
                    [sys.executable, str(SCRIPT), str(root)],
                    text=True, capture_output=True, check=False
                )
        self.assertEqual(run_versioned(valid).returncode, 0)
        for value in (BASE, BASE + "- Required CI checks: UNKNOWN\n",
                      BASE + "- Required CI checks: NONE\n"):
            result = run_versioned(value)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Required CI checks", result.stdout)

    def test_v4131_rejects_status_and_conflicting_required_checks(self) -> None:
        def run_v4(override: str) -> subprocess.CompletedProcess[str]:
            with tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                d = root / ".dev-standard"
                d.mkdir()
                (d / "PROJECT_OVERRIDES.md").write_text(override, encoding="utf-8")
                (d / "VERSION").write_text(
                    "repository=kaicreator-mm/ai-development-standard\n"
                    "version=4.13.1\n"
                    "revision=0123456789abcdef0123456789abcdef01234567\n",
                    encoding="utf-8"
                )
                return subprocess.run(
                    [sys.executable, str(SCRIPT), str(root)],
                    capture_output=True, text=True, check=False
                )
        for bad in ("SUCCESS", "PASS", "ci/woodpecker/push/ci\n"
                    "- Required CI checks: github-actions/source"):
            result = run_v4(BASE + "- Required CI checks: " + bad + "\n")
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Required CI checks", result.stdout)
        good = run_v4(
            BASE + "- Required CI checks: ci/woodpecker/push/ci, github-actions/source\n"
        )
        self.assertEqual(good.returncode, 0, good.stdout + good.stderr)

    def test_enabled_profile_passes(self) -> None:
        result = run(BASE)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_enabled_profile_requires_backend(self) -> None:
        result = run(BASE.replace("- CI backend / execution model: local\n", ""))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("CI backend / execution model", result.stdout)

    def test_disabled_profile_needs_reason(self) -> None:
        text = BASE.replace("- CI profile: minimal", "- CI profile: disabled")
        result = run(text)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Disabled reason", result.stdout)

    def test_fallback_cannot_be_na(self) -> None:
        result = run(BASE.replace("local clean checkout", "NOT_APPLICABLE"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("fallback", result.stdout)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
    raise SystemExit(0 if result.wasSuccessful() else 1)
