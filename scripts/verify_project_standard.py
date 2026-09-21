from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys

EXPECTED_REPOSITORY = "kaicreator-mm/ai-development-standard"
REQUIRED_IDENTITY_KEYS = ("repository", "version", "revision")
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+(?:[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)
SHA40_RE = re.compile(r"^[0-9a-fA-F]{40}$")


def parse_version_identity(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    identity: dict[str, str] = {}

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return identity, [f"cannot read .dev-standard/VERSION: {exc}"]

    lines = text.splitlines()
    if not lines:
        return identity, [".dev-standard/VERSION is empty"]

    allowed = set(REQUIRED_IDENTITY_KEYS)
    for line_number, line in enumerate(lines, start=1):
        if not line or line != line.strip():
            errors.append(
                f"invalid VERSION line {line_number}: expected key=value without blank/outer whitespace"
            )
            continue
        key, separator, value = line.partition("=")
        if not separator or not key or not value or "=" in value:
            errors.append(f"invalid VERSION line {line_number}: expected key=value")
            continue
        if key not in allowed:
            errors.append(f"unknown key in .dev-standard/VERSION: {key}")
            continue
        if key in identity:
            errors.append(f"duplicate key in .dev-standard/VERSION: {key}")
            continue
        identity[key] = value

    for key in REQUIRED_IDENTITY_KEYS:
        if key not in identity:
            errors.append(f"missing key in .dev-standard/VERSION: {key}")

    repository = identity.get("repository")
    if repository is not None and repository != EXPECTED_REPOSITORY:
        errors.append(
            ".dev-standard/VERSION repository must be "
            f"{EXPECTED_REPOSITORY!r}, got {repository!r}"
        )

    version = identity.get("version")
    if version is not None:
        if "<" in version or ">" in version:
            errors.append(".dev-standard/VERSION version contains an unreplaced placeholder")
        elif not SEMVER_RE.fullmatch(version):
            errors.append(f".dev-standard/VERSION version is not SemVer: {version!r}")

    revision = identity.get("revision")
    if revision is not None:
        if "<" in revision or ">" in revision:
            errors.append(".dev-standard/VERSION revision contains an unreplaced placeholder")
        elif not SHA40_RE.fullmatch(revision):
            errors.append(
                ".dev-standard/VERSION revision is not a 40-char hexadecimal commit SHA: "
                f"{revision!r}"
            )

    return identity, errors


def _run_git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def verify_exact_standard_revision(identity: dict[str, str], standard_repo: Path) -> list[str]:
    """Verify immutable standard identity against a local Git object database.

    This function intentionally performs no fallback to main/latest and no implicit
    network fetch. The caller must provide a repository that already contains the
    pinned commit object. That makes resolution deterministic in CI, Build Host,
    cached clones, and offline validation environments.
    """

    errors: list[str] = []
    revision = identity.get("revision")
    expected_version = identity.get("version")
    repository = identity.get("repository")

    if not revision or not expected_version or not repository:
        return ["cannot resolve standard revision because identity is incomplete"]

    if not standard_repo.exists():
        return [f"standard repository path does not exist: {standard_repo}"]

    inside = _run_git(standard_repo, "rev-parse", "--is-inside-work-tree")
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        return [f"standard repository path is not a Git work tree: {standard_repo}"]

    commit_check = _run_git(standard_repo, "cat-file", "-e", f"{revision}^{{commit}}")
    if commit_check.returncode != 0:
        errors.append(
            "pinned standard revision is not resolvable in the provided Git repository: "
            f"{revision}"
        )
        return errors

    resolved = _run_git(standard_repo, "rev-parse", f"{revision}^{{commit}}")
    if resolved.returncode != 0 or resolved.stdout.strip().lower() != revision.lower():
        errors.append(
            "resolved standard commit identity does not equal pinned revision: "
            f"expected={revision!r} actual={resolved.stdout.strip()!r}"
        )
        return errors

    version_result = _run_git(standard_repo, "show", f"{revision}:VERSION")
    if version_result.returncode != 0:
        errors.append(f"pinned standard revision does not contain VERSION: {revision}")
    else:
        actual_version = version_result.stdout.strip()
        if actual_version != expected_version:
            errors.append(
                "pinned standard VERSION mismatch: "
                f"declared={expected_version!r} revision_VERSION={actual_version!r}"
            )

    agents_result = _run_git(standard_repo, "cat-file", "-e", f"{revision}:AGENTS.md")
    if agents_result.returncode != 0:
        errors.append(f"pinned standard revision does not contain AGENTS.md: {revision}")

    return errors


def verify_project(
    root: Path,
    *,
    standard_repo: Path | None = None,
    require_resolution: bool = False,
) -> list[str]:
    errors: list[str] = []
    version_file = root / ".dev-standard" / "VERSION"
    override_file = root / ".dev-standard" / "PROJECT_OVERRIDES.md"
    agents_file = root / "AGENTS.md"

    for path in (version_file, override_file, agents_file):
        if not path.is_file():
            # Normalize separators so diagnostics are identical on POSIX and Windows.
            errors.append(f"missing: {path.relative_to(root).as_posix()}")

    identity: dict[str, str] = {}
    if version_file.is_file():
        identity, identity_errors = parse_version_identity(version_file)
        errors.extend(identity_errors)

    if errors:
        return errors

    if standard_repo is not None:
        errors.extend(verify_exact_standard_revision(identity, standard_repo.resolve()))
    elif require_resolution:
        errors.append(
            "immutable revision resolution required but no standard repository was provided; "
            "use --standard-repo or AI_DEV_STANDARD_REPO"
        )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify a project's ai-development-standard adoption. Structural checks are always "
            "performed; provide --standard-repo to prove the immutable pinned revision/version."
        )
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="project repository root (default: current directory)",
    )
    parser.add_argument(
        "--standard-repo",
        default=os.environ.get("AI_DEV_STANDARD_REPO"),
        help=(
            "local Git checkout/object database containing the pinned standard commit; "
            "may also be supplied through AI_DEV_STANDARD_REPO"
        ),
    )
    parser.add_argument(
        "--require-resolution",
        action="store_true",
        help="fail unless immutable revision resolution is actually performed",
    )
    args = parser.parse_args(argv)

    root = Path(args.project_root).resolve()
    standard_repo = Path(args.standard_repo).resolve() if args.standard_repo else None
    errors = verify_project(
        root,
        standard_repo=standard_repo,
        require_resolution=args.require_resolution,
    )
    if errors:
        print("project standard verification: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("project standard verification: PASS")
    if standard_repo is not None:
        print("immutable revision resolution: PASS")
    else:
        print("immutable revision resolution: NOT_RUN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
