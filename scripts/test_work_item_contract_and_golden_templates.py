#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_STATES = {
    "state:planned", "state:ready", "state:claimed", "state:implementing",
    "state:review-ready", "state:reviewing", "state:validation-needed",
    "state:validating", "state:changes-requested", "state:merge-ready",
    "state:blocked", "state:done", "state:superseded", "state:cancelled",
}
CANONICAL_REVIEWS = {"review:required", "review:recommended", "review:not-required"}
CANONICAL_TYPES = {
    "type:version", "type:planning", "type:research", "type:research-demo",
    "type:task", "type:bug", "type:fix", "type:validation", "type:blocker",
    "type:release",
}
FORBIDDEN_TRUTH_LABELS = {
    "gate:pass", "gate:fail", "gate:blocked", "gate:not-run", "gate:not-applicable",
    "validation:pass", "validation:passed", "validation:fail", "validation:failed",
    "validation:blocked",
}

REQUIRED_TEMPLATE_SECTIONS = {
    "templates/version-issue.md": {
        "Contract", "Goal", "Frozen Authority", "Canonical DAG", "Materialized Tasks",
        "Required Version Gates", "Closure Criteria", "Forbidden",
    },
    "templates/planning-amendment-issue.md": {
        "Identity", "Reason", "Existing Authority", "Proposed DAG Change",
        "Authority Impact", "Acceptance", "Forbidden",
    },
    "templates/research-issue.md": {
        "Contract", "Research Question", "Authority / Inputs", "Scope",
        "Evidence Requirements", "Required Result", "Acceptance",
    },
    "templates/research-demo-issue.md": {
        "Purpose / Architecture UNKNOWN", "Falsifiable Hypothesis", "Frozen inputs",
        "Fixed baseline / branch", "Evidence strength", "In scope", "Out of scope",
        "Executable scenarios", "Required environment", "Allowed changes",
        "Forbidden changes", "Required validation", "Closeout",
    },
    "templates/task-issue.md": {
        "Contract", "Goal", "In Scope", "Out of Scope", "Frozen Inputs",
        "Dependencies", "Acceptance", "Required Gates", "Execution Constraints",
        "Durable Execution / Prompt Artifacts", "Allowed Changes", "Forbidden Changes",
        "Failure / Blocker Handling", "Completion", "Metadata Invariants",
    },
    "templates/bug-fix-issue.md": {
        "Contract", "Observed Behavior", "Expected Behavior", "Reproduction / Evidence",
        "Scope / Non-scope", "Repair Acceptance", "Allowed / Forbidden Changes", "Completion",
    },
    "templates/validation-request-issue.md": {
        "Contract", "Validation Tuple", "Required Evidence", "Staleness Rule", "Forbidden",
    },
    "templates/blocker-issue.md": {
        "Contract", "Blocking Fact", "Affected Work", "Evidence", "Unblock Condition",
        "Owner / Handoff", "Forbidden",
    },
}


def read(path: str) -> str:
    p = ROOT / path
    assert p.exists(), f"missing required asset: {path}"
    return p.read_text(encoding="utf-8")


def require(text: str, *tokens: str) -> None:
    for token in tokens:
        assert token in text, f"missing required token: {token}"


def markdown_slug(heading: str) -> str:
    heading = re.sub(r"<[^>]+>", "", heading).replace("`", "").strip().lower()
    heading = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE)
    return re.sub(r"\s+", "-", heading).strip("-")


def markdown_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        base = markdown_slug(match.group(1))
        if not base:
            continue
        count = counts.get(base, 0)
        anchors.add(base if count == 0 else f"{base}-{count}")
        counts[base] = count + 1
    return anchors


def validate_ref(ref: str) -> None:
    path, sep, anchor = ref.partition("#")
    text = read(path)
    if sep:
        assert anchor, f"empty anchor in reference: {ref}"
        assert anchor in markdown_anchors(text), f"missing markdown anchor: {ref}"


def section_names(text: str) -> set[str]:
    return {
        match.group(1).strip()
        for match in re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE)
    }


def validate_required_sections(path: str, text: str | None = None) -> None:
    body = read(path) if text is None else text
    missing = REQUIRED_TEMPLATE_SECTIONS[path] - section_names(body)
    assert not missing, f"{path} missing required contract sections: {sorted(missing)}"


def validate_work_item_labels(
    labels: list[str], *, require_type: bool = True, require_state: bool = True,
    require_review: bool = True,
) -> None:
    states = [label for label in labels if label.startswith("state:")]
    reviews = [label for label in labels if label.startswith("review:")]
    types = [label for label in labels if label.startswith("type:")]

    assert not (set(states) - CANONICAL_STATES), f"unknown canonical workflow state(s): {sorted(set(states) - CANONICAL_STATES)}"
    assert not (set(reviews) - CANONICAL_REVIEWS), f"unknown Review Policy value(s): {sorted(set(reviews) - CANONICAL_REVIEWS)}"
    assert not (set(types) - CANONICAL_TYPES), f"unknown canonical work-item type(s): {sorted(set(types) - CANONICAL_TYPES)}"

    if require_state:
        assert len(states) == 1, f"expected exactly one state:* label, got {states}"
    elif states:
        assert len(states) == 1, f"conflicting state:* labels: {states}"
    if require_review:
        assert len(reviews) == 1, f"expected exactly one review:* label, got {reviews}"
    elif reviews:
        assert len(reviews) == 1, f"conflicting review:* labels: {reviews}"
    if require_type:
        assert len(types) == 1, f"expected exactly one type:* label, got {types}"
    elif types:
        assert len(types) == 1, f"conflicting type:* labels: {types}"

    forbidden_truth = sorted(set(labels) & FORBIDDEN_TRUTH_LABELS)
    assert not forbidden_truth, f"Gate/Validation truth MUST NOT be encoded as labels: {forbidden_truth}"
    dynamic_identity = [
        label for label in labels if label.startswith(("agent:", "session:", "operator:", "actor:"))
    ]
    assert not dynamic_identity, f"dynamic Agent/session identity MUST NOT be encoded as labels: {dynamic_identity}"


def validate_live_dag_authority_claim(text: str) -> None:
    normalized = re.sub(r"\s+", " ", text.lower())
    markdown_dag_markers = (
        "task_dag.md", "task-dag.md", "task_dag_status.md", "task-dag-status.md",
        "markdown status table", "shared markdown",
    )
    claims_authority = "canonical" in normalized or "authoritative" in normalized
    claims_live_execution = "live" in normalized or "execution state" in normalized
    if (
        any(marker in normalized for marker in markdown_dag_markers)
        and claims_authority and claims_live_execution
        and "non_authoritative_derived_state" not in normalized
    ):
        raise AssertionError("Markdown Task DAG/status document MUST NOT be canonical live execution authority")


def expect_reject(fn, message: str) -> None:
    try:
        fn()
    except AssertionError:
        return
    raise AssertionError(message)


def test_work_item_standard() -> None:
    text = read("standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md")
    require(
        text,
        "Every substantial version MUST maintain a recoverable Version Task DAG.",
        "GitHub Task Issues + native Issue Dependencies",
        "NON_AUTHORITATIVE_DERIVED_STATE",
        "state:claimed", "state:validating", "state:superseded",
        "review:required", "risk:critical", "gate:pass",
        "A long chat prompt MUST NOT repair an incomplete Issue.",
    )


def test_golden_standard_and_index() -> None:
    standard = read("standards/GOLDEN_TEMPLATE_STANDARD.md")
    index = read("templates/GOLDEN_INDEX.md")
    require(standard, "Every active normative standard", "STANDARD_COVERAGE.json", "Forbidden / Non-conformant", "templates/GOLDEN_INDEX.md")
    for surface in (
        "Version Task DAG", "Version umbrella Issue", "Implementation Task Issue", "Research Issue",
        "Validation request/handoff", "Independent Review", "Pointer-only trigger",
        "Structured Agent event", "Derived Version DAG View", "Release/Version closeout",
    ):
        assert surface in index, f"golden index missing surface: {surface}"
    require(index, "Forbidden/rationale", "Verification")


def test_required_templates_have_contract_sections() -> None:
    for path in REQUIRED_TEMPLATE_SECTIONS:
        validate_required_sections(path)
    task = read("templates/task-issue.md")
    mutated = task.replace("## Acceptance\n", "## Acceptance Removed\n", 1)
    expect_reject(
        lambda: validate_required_sections("templates/task-issue.md", mutated),
        "missing required Task Issue section was not rejected",
    )


def test_metadata_oracle_positive_and_negative() -> None:
    validate_work_item_labels(["type:task", "state:ready", "review:required", "risk:high"])
    mutations = (
        (["type:task", "state:ready", "state:implementing", "review:required"], "duplicate workflow states were not rejected"),
        (["type:task", "state:wip", "review:required"], "unknown workflow state was not rejected"),
        (["type:task", "state:ready", "review:required", "review:recommended"], "conflicting Review Policy values were not rejected"),
        (["type:task", "state:ready", "review:required", "gate:pass"], "Gate PASS label was not rejected"),
        (["type:task", "state:ready", "review:required", "validation:passed"], "Validation PASS label was not rejected"),
        (["type:task", "state:ready", "review:required", "agent:web-7"], "Agent identity label was not rejected"),
        (["type:task", "state:ready", "review:required", "session:abc"], "session identity label was not rejected"),
    )
    for labels, message in mutations:
        expect_reject(lambda labels=labels: validate_work_item_labels(labels), message)


def test_live_markdown_dag_authority_oracle() -> None:
    validate_live_dag_authority_claim(
        "TASK_DAG.md = frozen planning/history checkpoint; GitHub Issue Dependencies = canonical live execution DAG"
    )
    expect_reject(
        lambda: validate_live_dag_authority_claim("TASK_DAG_STATUS.md is the canonical live execution state authority."),
        "live Markdown DAG authority assertion was not rejected",
    )


def test_negative_examples_cover_core_failures() -> None:
    text = read("templates/golden/ANTI_PATTERNS.md")
    for token in (
        "live-dag-document-as-authority", "gate-result-as-label", "agent-identity-as-label",
        "self-asserted-independent-review", "long-chat-task-contract",
        "duplicate-workflow-state", "invented-state-synonym",
    ):
        assert token in text, f"missing anti-pattern: {token}"


def test_all_normative_standards_have_golden_forbidden_rationale_coverage() -> None:
    manifest = json.loads(read("standard-manifest.json"))
    coverage_doc = json.loads(read("templates/golden/STANDARD_COVERAGE.json"))
    normative = manifest["sections"]["normative_standards"]
    records = coverage_doc["coverage"]
    standards = [record["standard"] for record in records]
    assert len(standards) == len(set(standards)), "duplicate standard in STANDARD_COVERAGE.json"
    assert set(standards) == set(normative), (
        "golden coverage must match active normative standards exactly: "
        f"missing={sorted(set(normative) - set(standards))}, extra={sorted(set(standards) - set(normative))}"
    )
    for record in records:
        for key in ("golden_ref", "forbidden_ref", "rationale_ref"):
            ref = record.get(key)
            assert ref, f"{record['standard']} missing {key}"
            validate_ref(ref)

    broken = "templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md#definitely-missing-anchor"
    expect_reject(lambda: validate_ref(broken), "broken Golden/Forbidden/rationale anchor was not rejected")


def test_review_policy_normative_alignment() -> None:
    work_item = read("standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md")
    interaction = read("standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md")
    workflow = read("standards/DEVELOPMENT_WORKFLOW.md")
    require(work_item, "Every implementation work item MUST resolve exactly one Review Policy before dispatch")
    require(interaction, "MUST", "Review Policy")
    require(workflow, "implementation Task/PR 在 dispatch 前 MUST", "GITHUB_WORK_ITEM_CONTRACT_STANDARD.md")
    assert "每个 implementation Task/PR SHOULD 明确" not in workflow, "DEVELOPMENT_WORKFLOW still weakens Review Policy dispatch prerequisite to SHOULD"


def test_manifest_inventory() -> None:
    manifest = json.loads(read("standard-manifest.json"))
    sections = manifest["sections"]
    for path in ("standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md", "standards/GOLDEN_TEMPLATE_STANDARD.md"):
        assert path in sections["normative_standards"]
    for path in (
        "templates/GOLDEN_INDEX.md", "templates/golden/ANTI_PATTERNS.md",
        "templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md", "templates/golden/STANDARD_COVERAGE.json",
        "templates/codex-handoff-issue.md",
    ):
        assert path in sections["templates"], f"manifest missing template: {path}"
    assert "scripts/test_work_item_contract_and_golden_templates.py" in sections["verification"]


def main() -> None:
    tests = [
        test_work_item_standard,
        test_golden_standard_and_index,
        test_required_templates_have_contract_sections,
        test_metadata_oracle_positive_and_negative,
        test_live_markdown_dag_authority_oracle,
        test_negative_examples_cover_core_failures,
        test_all_normative_standards_have_golden_forbidden_rationale_coverage,
        test_review_policy_normative_alignment,
        test_manifest_inventory,
    ]
    for test in tests:
        test()
    print(f"work-item/golden-template contract tests: {len(tests)} passed")


if __name__ == "__main__":
    main()
