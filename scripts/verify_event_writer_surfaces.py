from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = "ai-dev:event:v1"

ACTIVE_SECTIONS = (
    "normative_standards",
    "compatibility_entries",
    "templates",
    "checklists",
    "prompts",
)
AUTHORITY_WRITER_SURFACES = {"README.md", "AGENTS.md"}

# Issue #32 is a repository invariant, not a natural-language classification
# problem. Literal event-v1 wording is permitted only for these machine-owned
# historical/read-only references. The complete normalized line and its path are
# both authoritative; every registered path must contain exactly one occurrence.
CANONICAL_HISTORICAL_V1_REFERENCE = (
    "historical ai-dev:event:v1 comments remain valid history and are read-only compatibility evidence."
)
ALLOWED_HISTORICAL_V1_REFERENCE_PATHS = frozenset(
    {
        "AGENTS.md",
        "standards/CHATGPT_WEB_ROLE.md",
        "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
        "standards/GITHUB_WORKFLOW.md",
        "standards/VERSION_INTEGRATION_WORKFLOW.md",
        "templates/agent-event-comment.md",
    }
)


def writer_surface_paths(root: Path = ROOT) -> list[str]:
    manifest = json.loads((root / "standard-manifest.json").read_text(encoding="utf-8"))
    sections = manifest["sections"]
    paths = set(AUTHORITY_WRITER_SURFACES)
    for section in ACTIVE_SECTIONS:
        paths.update(sections.get(section, []))
    return sorted(paths)


def normalize_v1_line(line: str) -> str:
    normalized = line.replace("`", "").strip().lower()
    for prefix in ("- ", "* ", "+ ", "> "):
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):].strip()
            break
    return " ".join(normalized.split())


def classify_v1_reference(rel_path: str, line: str) -> str:
    """Classify one literal event-v1 occurrence structurally and fail closed.

    There is deliberately no historical vocabulary fallback, writer-verb list,
    prohibition substring allowance, or surrounding-context interpretation.
    A literal v1 occurrence is allowed only when both its repository path and
    complete normalized line match the machine-owned historical inventory.
    """
    current = normalize_v1_line(line)
    if TOKEN not in current:
        return "none"
    if (
        rel_path in ALLOWED_HISTORICAL_V1_REFERENCE_PATHS
        and current == CANONICAL_HISTORICAL_V1_REFERENCE
    ):
        return "historical-compatibility"
    return "stale-or-unclassified"


def validate_historical_v1_inventory(observed_counts: dict[str, int]) -> list[str]:
    violations: list[str] = []
    for rel in sorted(ALLOWED_HISTORICAL_V1_REFERENCE_PATHS):
        count = observed_counts.get(rel, 0)
        if count != 1:
            violations.append(
                f"{rel}: canonical historical event-v1 reference count must be exactly 1, got {count}"
            )
    return violations


def scan_writer_surfaces(root: Path = ROOT) -> list[str]:
    violations: list[str] = []
    surfaces = writer_surface_paths(root)
    surface_set = set(surfaces)
    observed_counts = {rel: 0 for rel in ALLOWED_HISTORICAL_V1_REFERENCE_PATHS}

    for rel in sorted(ALLOWED_HISTORICAL_V1_REFERENCE_PATHS - surface_set):
        violations.append(f"{rel}: historical event-v1 inventory path is not an active writer surface")

    for rel in surfaces:
        path = root / rel
        if not path.is_file():
            violations.append(f"{rel}: active writer surface is missing")
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if TOKEN not in normalize_v1_line(line):
                continue
            classification = classify_v1_reference(rel, line)
            if classification == "historical-compatibility":
                observed_counts[rel] = observed_counts.get(rel, 0) + 1
                continue
            violations.append(
                f"{rel}:{index + 1}: unregistered/stale event-v1 reference: {line.strip()}"
            )

    violations.extend(validate_historical_v1_inventory(observed_counts))
    return violations


def main() -> int:
    violations = scan_writer_surfaces(ROOT)
    if violations:
        print("event writer surface verification: FAIL")
        for violation in violations:
            print(f"- {violation}")
        return 1
    print("event writer surface verification: PASS")
    print(f"active writer surfaces: {len(writer_surface_paths(ROOT))}")
    print(f"registered historical event-v1 references: {len(ALLOWED_HISTORICAL_V1_REFERENCE_PATHS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
