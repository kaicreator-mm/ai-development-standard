from __future__ import annotations

import argparse
from pathlib import Path
import re
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
            errors.append(f"invalid VERSION line {line_number}: expected key=value without blank/outer whitespace")
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


def verify_project(root: Path) -> list[str]:
    errors: list[str] = []
    version_file = root / ".dev-standard" / "VERSION"
    override_file = root / ".dev-standard" / "PROJECT_OVERRIDES.md"
    agents_file = root / "AGENTS.md"

    for path in (version_file, override_file, agents_file):
        if not path.is_file():
            errors.append(f"missing: {path.relative_to(root)}")

    if version_file.is_file():
        _, identity_errors = parse_version_identity(version_file)
        errors.extend(identity_errors)

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify a project's minimal immutable ai-development-standard adoption."
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="project repository root (default: current directory)",
    )
    args = parser.parse_args(argv)

    root = Path(args.project_root).resolve()
    errors = verify_project(root)
    if errors:
        print("project standard verification: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("project standard verification: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
