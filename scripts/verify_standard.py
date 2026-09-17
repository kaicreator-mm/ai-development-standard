from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "VERSION",
    "README.md",
    "AGENTS.md",
    "CHANGELOG.md",
    ".github/workflows/verify-standard.yml",
    "standards/DEVELOPMENT_WORKFLOW.md",
    "standards/VERSION_INTEGRATION_WORKFLOW.md",
    "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
    "standards/CHATGPT_WEB_ROLE.md",
    "standards/CODEX_ROLE.md",
    "standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md",
    "standards/CODEX_HANDOFF_PROTOCOL.md",
    "standards/VALIDATION_STANDARD.md",
    "standards/CI_EVIDENCE_STANDARD.md",
    "standards/GITHUB_WORKFLOW.md",
    "standards/RELEASE_STANDARD.md",
    "standards/MODEL_USAGE_POLICY.md",
    "standards/PROJECT_ADOPTION.md",
    "templates/project/.dev-standard/VERSION",
    "templates/project/.dev-standard/PROJECT_OVERRIDES.md",
    "templates/project/AGENTS.md",
    "scripts/verify_project_standard.py",
    "scripts/test_verify_project_standard.py",
    "templates/task-issue.md",
    "templates/agent-event-comment.md",
    "templates/local-agent-handoff-issue.md",
    "templates/codex-handoff-issue.md",
    "templates/implementation-pr.md",
    "templates/validation-report.md",
    "templates/final-closeout.md",
    "templates/task-dag.md",
    "checklists/pr-review.md",
    "prompts/L1_PRODUCT_EVIDENCE.md",
    "prompts/L2_ARCHITECTURE_EVIDENCE.md",
    "prompts/L3_IMPLEMENTATION_EVIDENCE.md",
    "prompts/independent-review-bootstrap.md",
    "prompts/local-agent-bootstrap.md",
    "prompts/CODEX_EXECUTION.md",
]

errors = []
for rel in REQUIRED:
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing required file: {rel}")

version = None
version_path = ROOT / "VERSION"
if version_path.exists():
    version = version_path.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append(f"VERSION is not SemVer: {version!r}")

if version:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if f"当前版本：`v{version}`" not in readme:
        errors.append("README current version does not match VERSION")

# v3+ risk-based Independent Review contract.
# Historical changelog entries intentionally preserve old v2.3 mandatory wording,
# so semantic guards target only active operational documents/templates.
review_policy_files = [
    "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
    "standards/DEVELOPMENT_WORKFLOW.md",
    "standards/GITHUB_WORKFLOW.md",
    "standards/VERSION_INTEGRATION_WORKFLOW.md",
    "templates/task-dag.md",
    "templates/task-issue.md",
    "templates/implementation-pr.md",
    "templates/project/.dev-standard/PROJECT_OVERRIDES.md",
]

if version and int(version.split(".", 1)[0]) >= 3:
    # Every active policy surface must expose all three semantics, but not every
    # document needs to use the portable `review:*` label representation.
    for rel in review_policy_files:
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "Review Policy" not in text:
            errors.append(f"{rel} missing Review Policy semantics")
        if "recommended" not in text or "not-required" not in text:
            errors.append(f"{rel} missing risk-based Review Policy choices")

    for rel in (
        "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
        "standards/GITHUB_WORKFLOW.md",
        "templates/project/.dev-standard/PROJECT_OVERRIDES.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        for token in ("review:required", "review:recommended", "review:not-required"):
            if token not in text:
                errors.append(f"{rel} missing portable Review Policy label: {token}")

    event_protocol = (ROOT / "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md").read_text(
        encoding="utf-8"
    )
    event_template = (ROOT / "templates/agent-event-comment.md").read_text(
        encoding="utf-8"
    )
    if "REVIEW_DECISION" not in event_protocol or "REVIEW_DECISION" not in event_template:
        errors.append("REVIEW_DECISION event is not consistently defined")

    operational_review_files = [
        "AGENTS.md",
        "README.md",
        "standards/DEVELOPMENT_WORKFLOW.md",
        "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
        "standards/GITHUB_WORKFLOW.md",
        "standards/VERSION_INTEGRATION_WORKFLOW.md",
        "standards/CHATGPT_WEB_ROLE.md",
        "standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md",
        "templates/project/AGENTS.md",
        "templates/project/.dev-standard/PROJECT_OVERRIDES.md",
        "templates/task-dag.md",
        "templates/task-issue.md",
        "templates/implementation-pr.md",
        "templates/local-agent-handoff-issue.md",
        "checklists/pr-review.md",
        "prompts/independent-review-bootstrap.md",
        "prompts/local-agent-bootstrap.md",
    ]
    stale_mandatory_phrases = (
        "every Task/Fix PR MUST receive an Independent Review",
        "Independent Review default is mandatory",
        "Version Branch Mode default is Independent Review required",
        "Version Branch Task/Fix PRs require Independent Review",
        "Independent Review 默认 mandatory",
    )
    for rel in operational_review_files:
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "REVIEW_POLICY_DECISION" in text:
            errors.append(f"{rel} uses deprecated REVIEW_POLICY_DECISION; use REVIEW_DECISION")
        for phrase in stale_mandatory_phrases:
            if phrase in text:
                errors.append(f"{rel} contains stale universal Review requirement: {phrase}")

for md in ROOT.rglob("*.md"):
    text = md.read_text(encoding="utf-8")
    if "PASS/FAIL/NOT_RUN/N/A/BLOCKED" in text:
        # Template shorthand is allowed, but canonical docs should use NOT_APPLICABLE.
        pass

if errors:
    print("standard verification: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("standard verification: PASS")
print(f"required files: {len(REQUIRED)}")
