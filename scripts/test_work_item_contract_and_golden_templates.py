#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    p = ROOT / path
    assert p.exists(), f"missing required asset: {path}"
    return p.read_text(encoding="utf-8")


def require(text: str, *tokens: str) -> None:
    for token in tokens:
        assert token in text, f"missing required token: {token}"


def test_work_item_standard() -> None:
    text = read("standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md")
    require(
        text,
        "Every substantial version MUST maintain a recoverable Version Task DAG.",
        "GitHub Task Issues + native Issue Dependencies",
        "NON_AUTHORITATIVE_DERIVED_STATE",
        "state:claimed",
        "state:validating",
        "state:superseded",
        "review:required",
        "risk:critical",
        "gate:pass",
        "A long chat prompt MUST NOT repair an incomplete Issue.",
    )


def test_golden_standard_and_index() -> None:
    standard = read("standards/GOLDEN_TEMPLATE_STANDARD.md")
    index = read("templates/GOLDEN_INDEX.md")
    require(standard, "Every active normative standard", "Forbidden / Non-conformant", "templates/GOLDEN_INDEX.md")
    for surface in (
        "Version Task DAG",
        "Version umbrella Issue",
        "Implementation Task Issue",
        "Research Issue",
        "Validation request/handoff",
        "Independent Review",
        "Pointer-only trigger",
        "Structured Agent event",
        "Derived Version DAG View",
        "Release/Version closeout",
    ):
        assert surface in index, f"golden index missing surface: {surface}"
    require(index, "Forbidden/rationale", "Verification")


def test_required_templates() -> None:
    paths = [
        "templates/version-issue.md",
        "templates/planning-amendment-issue.md",
        "templates/research-issue.md",
        "templates/research-demo-issue.md",
        "templates/task-issue.md",
        "templates/bug-fix-issue.md",
        "templates/validation-request-issue.md",
        "templates/blocker-issue.md",
        "templates/version-dag-state-card.md",
        "templates/agent-event-comment.md",
        "templates/implementation-pr.md",
        "templates/final-closeout.md",
        "templates/golden/ANTI_PATTERNS.md",
    ]
    for path in paths:
        read(path)


def test_negative_examples_cover_core_failures() -> None:
    text = read("templates/golden/ANTI_PATTERNS.md")
    for token in (
        "live-dag-document-as-authority",
        "gate-result-as-label",
        "agent-identity-as-label",
        "self-asserted-independent-review",
        "long-chat-task-contract",
        "duplicate-workflow-state",
        "invented-state-synonym",
    ):
        assert token in text, f"missing anti-pattern: {token}"


def test_manifest_inventory() -> None:
    manifest = json.loads(read("standard-manifest.json"))
    sections = manifest["sections"]
    # This intentionally fails until the T-012 manifest update is present.
    assert "standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md" in sections["normative_standards"]
    assert "standards/GOLDEN_TEMPLATE_STANDARD.md" in sections["normative_standards"]
    assert "templates/GOLDEN_INDEX.md" in sections["templates"]
    assert "templates/golden/ANTI_PATTERNS.md" in sections["templates"]
    assert "scripts/test_work_item_contract_and_golden_templates.py" in sections["verification"]


def main() -> None:
    tests = [
        test_work_item_standard,
        test_golden_standard_and_index,
        test_required_templates,
        test_negative_examples_cover_core_failures,
        test_manifest_inventory,
    ]
    for test in tests:
        test()
    print(f"work-item/golden-template contract tests: {len(tests)} passed")


if __name__ == "__main__":
    main()
