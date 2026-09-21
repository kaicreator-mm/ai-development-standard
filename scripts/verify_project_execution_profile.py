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
