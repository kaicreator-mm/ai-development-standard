from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("verify_project_standard.py")
VALID_REVISION = "0123456789abcdef0123456789abcdef01234567"
VALID_VERSION = (
    "repository=kaicreator-mm/ai-development-standard\n"
    "version=1.2.1\n"
    f"revision={VALID_REVISION}\n"
)


@dataclass(frozen=True)
class Case:
    name: str
    version_text: str = VALID_VERSION
    include_agents: bool = True
    include_overrides: bool = True
    expected_code: int = 0
    expected_status: str = "PASS"
    diagnostic: str = "project standard verification: PASS"


CASES = [
    Case(name="valid official three-field identity"),
    Case(
        name="legacy single-line identity rejected",
        version_text="ai-development-standard@v1.2.0\n",
        expected_code=1,
        expected_status="FAIL",
        diagnostic="invalid VERSION line 1",
    ),
    Case(
        name="missing revision",
        version_text="repository=kaicreator-mm/ai-development-standard\nversion=1.2.1\n",
        expected_code=1,
        expected_status="FAIL",
        diagnostic="missing key in .dev-standard/VERSION: revision",
    ),
    Case(
        name="malformed SHA",
        version_text="repository=kaicreator-mm/ai-development-standard\nversion=1.2.1\nrevision=zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz\n",
        expected_code=1,
        expected_status="FAIL",
        diagnostic="revision is not a 40-char hexadecimal commit SHA",
    ),
    Case(
        name="short SHA",
        version_text="repository=kaicreator-mm/ai-development-standard\nversion=1.2.1\nrevision=0123456789abcdef\n",
        expected_code=1,
        expected_status="FAIL",
        diagnostic="revision is not a 40-char hexadecimal commit SHA",
    ),
    Case(
        name="wrong repository",
        version_text=f"repository=example/wrong\nversion=1.2.1\nrevision={VALID_REVISION}\n",
        expected_code=1,
        expected_status="FAIL",
        diagnostic="repository must be 'kaicreator-mm/ai-development-standard'",
    ),
    Case(
        name="malformed SemVer",
        version_text=f"repository=kaicreator-mm/ai-development-standard\nversion=v1.2\nrevision={VALID_REVISION}\n",
        expected_code=1,
        expected_status="FAIL",
        diagnostic="version is not SemVer",
    ),
    Case(
        name="duplicate key",
        version_text=(
            "repository=kaicreator-mm/ai-development-standard\n"
            "version=1.2.1\n"
            "version=1.2.2\n"
            f"revision={VALID_REVISION}\n"
        ),
        expected_code=1,
        expected_status="FAIL",
        diagnostic="duplicate key in .dev-standard/VERSION: version",
    ),
    Case(
        name="missing AGENTS",
        include_agents=False,
        expected_code=1,
        expected_status="FAIL",
        diagnostic="missing: AGENTS.md",
    ),
    Case(
        name="missing PROJECT_OVERRIDES",
        include_overrides=False,
        expected_code=1,
        expected_status="FAIL",
        diagnostic="missing: .dev-standard/PROJECT_OVERRIDES.md",
    ),
    Case(
        name="template placeholders rejected",
        version_text=(
            "repository=kaicreator-mm/ai-development-standard\n"
            "version=<semantic-version>\n"
            "revision=<40-char-commit-sha>\n"
        ),
        expected_code=1,
        expected_status="FAIL",
        diagnostic="contains an unreplaced placeholder",
    ),
    Case(
        name="unknown identity key rejected",
        version_text=(
            "repository=kaicreator-mm/ai-development-standard\n"
            "version=1.2.1\n"
            f"revision={VALID_REVISION}\n"
            "channel=stable\n"
        ),
        expected_code=1,
        expected_status="FAIL",
        diagnostic="unknown key in .dev-standard/VERSION: channel",
    ),
    Case(
        name="missing repository",
        version_text=f"version=1.2.1\nrevision={VALID_REVISION}\n",
        expected_code=1,
        expected_status="FAIL",
        diagnostic="missing key in .dev-standard/VERSION: repository",
    ),
]


def run_case(case: Case) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory(prefix="project-standard-case-") as temp_dir:
        root = Path(temp_dir)
        standard_dir = root / ".dev-standard"
        standard_dir.mkdir()
        (standard_dir / "VERSION").write_text(case.version_text, encoding="utf-8")
        if case.include_overrides:
            (standard_dir / "PROJECT_OVERRIDES.md").write_text("# Project Overrides\n", encoding="utf-8")
        if case.include_agents:
            (root / "AGENTS.md").write_text("# AGENTS\n", encoding="utf-8")

        return subprocess.run(
            [sys.executable, str(SCRIPT), str(root)],
            text=True,
            capture_output=True,
            check=False,
        )


class ProjectVerifierRegressionTests(unittest.TestCase):
    def test_regression_cases(self) -> None:
        for case in CASES:
            with self.subTest(case=case.name):
                result = run_case(case)
                combined = result.stdout + result.stderr
                self.assertEqual(result.returncode, case.expected_code, combined)
                self.assertIn(f"project standard verification: {case.expected_status}", result.stdout)
                self.assertIn(case.diagnostic, combined)
                print(
                    f"CASE {case.name}: expected={case.expected_code}/{case.expected_status} "
                    f"actual={result.returncode}/{case.expected_status if result.returncode == case.expected_code else 'UNEXPECTED'} "
                    "RESULT=PASS"
                )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ProjectVerifierRegressionTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
