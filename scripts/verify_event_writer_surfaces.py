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

# Historical v1 compatibility is deliberately an exact positive allowlist rather
# than a vocabulary/verb classifier. Any edited, extended, or newly introduced
# v1-bearing sentence fails closed unless it is an explicit prohibition below.
# This prevents historical vocabulary from authorizing arbitrary writer wording.
HISTORICAL_V1_REFERENCE_TEXTS = {
    "historical ai-dev:event:v1 comments remain valid history and are read-only compatibility evidence.",
    "historical ai-dev:event:v1 comments remain valid history and are read-only compatibility evidence only.",
}


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


def classify_v1_reference(lines: list[str], index: int) -> str:
    """Classify a v1 reference from the v1-bearing line only.

    Allowed states are intentionally narrow:
    1. an explicit prohibition against emitting/publishing v1; or
    2. an exact canonical historical/read-only compatibility reference.

    Everything else fails closed. There is no generic historical vocabulary
    fallback and no writer-verb blacklist to evade with alternate wording.
    """
    current = normalize_v1_line(lines[index])
    if TOKEN not in current:
        return "none"

    prohibition_markers = (
        "must not emit ai-dev:event:v1",
        "must not publish ai-dev:event:v1",
        "do not emit ai-dev:event:v1",
        "do not publish ai-dev:event:v1",
        "new writers must not emit v1",
        "new writers must not emit ai-dev:event:v1",
        "不得发布 ai-dev:event:v1",
        "不得写入 ai-dev:event:v1",
        "不得 emit ai-dev:event:v1",
    )
    if any(marker in current for marker in prohibition_markers):
        return "explicit-prohibition"

    if current in HISTORICAL_V1_REFERENCE_TEXTS:
        return "historical-compatibility"

    return "stale-or-unclassified"


def scan_writer_surfaces(root: Path = ROOT) -> list[str]:
    violations: list[str] = []
    for rel in writer_surface_paths(root):
        path = root / rel
        if not path.is_file():
            violations.append(f"{rel}: active writer surface is missing")
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if TOKEN not in normalize_v1_line(line):
                continue
            classification = classify_v1_reference(lines, index)
            if classification not in {"explicit-prohibition", "historical-compatibility"}:
                violations.append(
                    f"{rel}:{index + 1}: unclassified/stale new-work event-v1 reference: {line.strip()}"
                )
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
