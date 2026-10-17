from __future__ import annotations

import argparse
from pathlib import Path
import sys

CI_FIELDS = (
    "CI provider",
    "CI backend / execution model",
    "CI runner role",
    "Workflow config",
    "Workflow config source",
    "Execution shell / entrypoint model",
    "Runtime source",
    "Clone / checkout model",
    "Partial clone policy",
    "Submodule policy",
    "Git LFS policy",
    "Fresh-run / rerun policy",
)


def bullet(text: str, label: str) -> str | None:
    prefix = f"- {label}:"
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    return None


def placeholder(value: str) -> bool:
    return "<" in value and ">" in value


def na(value: str) -> bool:
    return value.upper().replace("_", " ").startswith("NOT APPLICABLE")


def verify(root: Path) -> list[str]:
    path = root / ".dev-standard" / "PROJECT_OVERRIDES.md"
    if not path.is_file():
        return ["missing: .dev-standard/PROJECT_OVERRIDES.md"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    profile = bullet(text, "CI profile")
    if profile is None:
        return ["PROJECT_OVERRIDES missing field: CI profile"]
    if profile not in {"minimal", "custom", "disabled"}:
        errors.append(f"CI profile must be minimal/custom/disabled, got {profile!r}")

    fallback = bullet(text, "Exact-SHA clean-validation fallback")
    if not fallback or placeholder(fallback) or na(fallback):
        errors.append("Exact-SHA clean-validation fallback must be concrete")

    disabled_reason = bullet(text, "Disabled reason (for `disabled`)")
    if profile == "disabled" and (not disabled_reason or placeholder(disabled_reason) or na(disabled_reason)):
        errors.append("disabled CI requires a real Disabled reason")

    if profile in {"minimal", "custom"}:
        for label in CI_FIELDS:
            value = bullet(text, label)
            if not value:
                errors.append(f"enabled CI missing field: {label}")
            elif placeholder(value) or na(value):
                errors.append(f"enabled CI requires concrete field: {label}")

    # v4.13.1+: bind selected required checks before any provider result is known.
    version_path = root / ".dev-standard" / "VERSION"
    version_match = None
    if version_path.is_file():
        import re
        version_match = re.search(r"^version=(\d+)\.(\d+)\.(\d+)", version_path.read_text(encoding="utf-8"), re.M)
    needs_required_checks = bool(
        version_match
        and tuple(map(int, version_match.groups())) >= (4, 13, 1)
    )
    if needs_required_checks and profile in {"minimal", "custom"}:
        import re
        lines = [line for line in text.splitlines()
                 if line.startswith("- Required CI checks:")]
        # Every selected check must be a concrete provider/check identity. There
        # is no globally mandated provider and no truth claim about timestamps.
        if len(lines) != 1:
            errors.append("v4.13.1 requires exactly one Required CI checks declaration")
        else:
            selected = lines[0].partition(":")[2].strip()
            names = [name.strip() for name in selected.split(",")]
            if (
                placeholder(selected) or na(selected)
                or not names or len(set(names)) != len(names)
                or any(not re.fullmatch(
                    r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.: -]+)+", name
                ) for name in names)
            ):
                errors.append(
                    "v4.13.1 enabled CI requires concrete provider/check names "
                    "in Required CI checks"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", nargs="?", default=".")
    args = parser.parse_args()
    errors = verify(Path(args.project_root).resolve())
    if errors:
        print("project execution profile verification: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("project execution profile verification: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
