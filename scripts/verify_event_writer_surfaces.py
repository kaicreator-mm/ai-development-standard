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


def writer_surface_paths(root: Path = ROOT) -> list[str]:
    manifest = json.loads((root / "standard-manifest.json").read_text(encoding="utf-8"))
    sections = manifest["sections"]
    paths = set(AUTHORITY_WRITER_SURFACES)
    for section in ACTIVE_SECTIONS:
        paths.update(sections.get(section, []))
    return sorted(paths)


def classify_v1_reference(lines: list[str], index: int) -> str:
    current = lines[index].replace("`", "").lower()
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

    stale_writer_markers = (
        "publish ai-dev:event:v1",
        "emit ai-dev:event:v1",
        "write ai-dev:event:v1",
        "use ai-dev:event:v1",
        "send ai-dev:event:v1",
        "create ai-dev:event:v1",
        "发布 ai-dev:event:v1",
        "写入 ai-dev:event:v1",
        "使用 ai-dev:event:v1",
    )
    if any(marker in current for marker in stale_writer_markers):
        return "stale-or-unclassified"

    start = max(0, index - 2)
    end = min(len(lines), index + 3)
    context = " ".join(lines[start:end]).replace("`", "").lower()
    historical_markers = (
        "historical",
        "compatib",
        "backward",
        "legacy",
        "readable",
        "read-only",
        "历史",
        "兼容",
        "旧版",
        "保留",
    )
    if any(marker in context for marker in historical_markers):
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
            if TOKEN not in line.replace("`", "").lower():
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
