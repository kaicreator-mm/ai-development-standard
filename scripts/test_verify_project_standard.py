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
    extra_args: tuple[str, ...] = ()
    expected_code: int = 0
    expected_status: str = "PASS"
    diagnostic: str = "project standard verification: PASS"


CASES = [
    Case(name="valid official three-field identity"),
    Case(
        name="resolution required without repository rejected",
        extra_args=("--require-resolution",),
        expected_code=1,
        expected_status="FAIL",
        diagnostic="immutable revision resolution required",
    ),
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


def write_project(root: Path, case: Case) -> None:
    standard_dir = root / ".dev-standard"
    standard_dir.mkdir()
    (standard_dir / "VERSION").write_text(case.version_text, encoding="utf-8")
    if case.include_overrides:
        (standard_dir / "PROJECT_OVERRIDES.md").write_text(
            "# Project Overrides\n", encoding="utf-8"
        )
    if case.include_agents:
        (root / "AGENTS.md").write_text("# AGENTS\n", encoding="utf-8")


def run_case(case: Case) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory(prefix="project-standard-case-") as temp_dir:
        root = Path(temp_dir)
        write_project(root, case)
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(root), *case.extra_args],
            text=True,
            capture_output=True,
            check=False,
        )


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=True,
    )


def create_standard_repo(root: Path, version: str = "3.1.0") -> str:
    root.mkdir()
    git(root, "init")
    git(root, "config", "user.email", "standard-test@example.invalid")
    git(root, "config", "user.name", "Standard Test")
    (root / "VERSION").write_text(f"{version}\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# AGENTS\n", encoding="utf-8")
    git(root, "add", "VERSION", "AGENTS.md")
    git(root, "commit", "-m", f"standard {version}")
    return git(root, "rev-parse", "HEAD").stdout.strip()


class ProjectVerifierRegressionTests(unittest.TestCase):
    def test_structural_regression_cases(self) -> None:
        for case in CASES:
            with self.subTest(case=case.name):
                result = run_case(case)
                combined = result.stdout + result.stderr
                self.assertEqual(result.returncode, case.expected_code, combined)
                self.assertIn(
                    f"project standard verification: {case.expected_status}", result.stdout
                )
                self.assertIn(case.diagnostic, combined)
                print(
                    f"CASE {case.name}: expected={case.expected_code}/{case.expected_status} "
                    f"actual={result.returncode}/"
                    f"{case.expected_status if result.returncode == case.expected_code else 'UNEXPECTED'} "
                    "RESULT=PASS"
                )

    def test_exact_revision_resolution_passes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="project-resolution-") as temp_dir:
            base = Path(temp_dir)
            standard_repo = base / "standard"
            revision = create_standard_repo(standard_repo, "3.1.0")
            project = base / "project"
            project.mkdir()
            case = Case(
                name="resolved",
                version_text=(
                    "repository=kaicreator-mm/ai-development-standard\n"
                    "version=3.1.0\n"
                    f"revision={revision}\n"
                ),
            )
            write_project(project, case)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(project),
                    "--standard-repo",
                    str(standard_repo),
                    "--require-resolution",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("immutable revision resolution: PASS", result.stdout)

    def test_version_mismatch_fails_resolution(self) -> None:
        with tempfile.TemporaryDirectory(prefix="project-resolution-") as temp_dir:
            base = Path(temp_dir)
            standard_repo = base / "standard"
            revision = create_standard_repo(standard_repo, "3.1.0")
            project = base / "project"
            project.mkdir()
            case = Case(
                name="mismatch",
                version_text=(
                    "repository=kaicreator-mm/ai-development-standard\n"
                    "version=3.2.0\n"
                    f"revision={revision}\n"
                ),
            )
            write_project(project, case)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(project), "--standard-repo", str(standard_repo)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("pinned standard VERSION mismatch", result.stdout)

    def test_nonexistent_but_valid_sha_fails_resolution(self) -> None:
        with tempfile.TemporaryDirectory(prefix="project-resolution-") as temp_dir:
            base = Path(temp_dir)
            standard_repo = base / "standard"
            create_standard_repo(standard_repo, "3.1.0")
            project = base / "project"
            project.mkdir()
            nonexistent = "f" * 40
            case = Case(
                name="nonexistent",
                version_text=(
                    "repository=kaicreator-mm/ai-development-standard\n"
                    "version=3.1.0\n"
                    f"revision={nonexistent}\n"
                ),
            )
            write_project(project, case)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(project), "--standard-repo", str(standard_repo)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("pinned standard revision is not resolvable", result.stdout)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ProjectVerifierRegressionTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
