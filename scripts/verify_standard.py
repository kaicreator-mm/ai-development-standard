from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "standard-manifest.json"

# Bootstrap inventory is deliberately code-owned rather than manifest-owned.
# This prevents a single edit from deleting both an active asset and its manifest
# entry while still passing verification. It is the union of the pre-v3.2
# hard-required set plus active core assets introduced or identified during v3.2.
BOOTSTRAP_REQUIRED = {
    "standard-manifest.json",
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
    "standards/PROJECT_STRUCTURE.md",
    "standards/REPOSITORY_STANDARD.md",
    "standards/DOCUMENTATION_STANDARD.md",
    "standards/TESTING_STANDARD.md",
    "templates/project/.dev-standard/VERSION",
    "templates/project/.dev-standard/PROJECT_OVERRIDES.md",
    "templates/project/AGENTS.md",
    "templates/task-issue.md",
    "templates/agent-event-comment.md",
    "templates/local-agent-handoff-issue.md",
    "templates/codex-handoff-issue.md",
    "templates/implementation-pr.md",
    "templates/validation-report.md",
    "templates/final-closeout.md",
    "templates/task-dag.md",
    "checklists/project-init.md",
    "checklists/pr-review.md",
    "checklists/version-closure.md",
    "prompts/L1_PRODUCT_EVIDENCE.md",
    "prompts/L2_ARCHITECTURE_EVIDENCE.md",
    "prompts/L3_IMPLEMENTATION_EVIDENCE.md",
    "prompts/independent-review-bootstrap.md",
    "prompts/local-agent-bootstrap.md",
    "prompts/CODEX_EXECUTION.md",
    "schemas/agent-event-v2.schema.json",
    "schemas/task-contract.schema.json",
    "schemas/validation-report.schema.json",
    "scripts/verify_standard.py",
    "scripts/test_verify_standard.py",
    "scripts/verify_project_standard.py",
    "scripts/test_verify_project_standard.py",
    "scripts/test_protocol_schemas.py",
}

errors: list[str] = []


def require_file(rel: str) -> Path:
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing bootstrap-required file: {rel}")
    return path


def read_required_text(rel: str) -> str:
    path = require_file(rel)
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def load_manifest() -> dict:
    if not MANIFEST_PATH.is_file():
        errors.append("missing required file: standard-manifest.json")
        return {}
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid standard-manifest.json: {exc}")
        return {}
    if manifest.get("schema_version") != 1:
        errors.append("standard-manifest.json schema_version must be 1")
    sections = manifest.get("sections")
    if not isinstance(sections, dict) or not sections:
        errors.append("standard-manifest.json sections must be a non-empty object")
    return manifest


def validate_manifest(manifest: dict) -> list[str]:
    paths: list[str] = []
    seen: set[str] = set()
    sections = manifest.get("sections", {})
    if not isinstance(sections, dict):
        return paths

    for section, values in sections.items():
        if not isinstance(section, str) or not section:
            errors.append("manifest section names must be non-empty strings")
            continue
        if not isinstance(values, list) or not values:
            errors.append(f"manifest section {section!r} must be a non-empty list")
            continue
        for rel in values:
            if not isinstance(rel, str) or not rel:
                errors.append(f"manifest section {section!r} contains invalid path: {rel!r}")
                continue
            candidate = Path(rel)
            if candidate.is_absolute() or ".." in candidate.parts:
                errors.append(f"manifest path must be repository-relative without '..': {rel}")
                continue
            if rel in seen:
                errors.append(f"manifest path declared more than once: {rel}")
                continue
            seen.add(rel)
            paths.append(rel)
            if not (ROOT / rel).is_file():
                errors.append(f"manifest-declared file is missing: {rel}")

    for rel in sorted(BOOTSTRAP_REQUIRED):
        if not (ROOT / rel).is_file():
            errors.append(f"bootstrap-required asset is missing: {rel}")
        if rel not in seen:
            errors.append(f"manifest omits bootstrap-required asset: {rel}")

    machine_contracts = sections.get("machine_contracts", [])
    if isinstance(machine_contracts, list):
        for rel in machine_contracts:
            path = ROOT / rel
            if not path.is_file():
                errors.append(f"machine contract file is missing: {rel}")
                continue
            try:
                schema = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"invalid machine contract JSON {rel}: {exc}")
                continue
            if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                errors.append(f"machine contract does not declare JSON Schema 2020-12: {rel}")
            if schema.get("type") != "object":
                errors.append(f"machine contract root type must be object: {rel}")
            if not schema.get("required"):
                errors.append(f"machine contract must declare required fields: {rel}")

    return paths


manifest = load_manifest()
manifest_paths = validate_manifest(manifest)

version = None
version_tuple = None
version_path = require_file("VERSION")
if version_path.is_file():
    version = version_path.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append(f"VERSION is not SemVer: {version!r}")
    else:
        version_tuple = tuple(int(part) for part in version.split("."))

if version:
    readme = read_required_text("README.md")
    if f"当前版本：`v{version}`" not in readme:
        errors.append("README current version does not match VERSION")

# v3+ risk-based Independent Review contract.
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

if version_tuple and version_tuple[0] >= 3:
    for rel in review_policy_files:
        text = read_required_text(rel)
        if "Review Policy" not in text:
            errors.append(f"{rel} missing Review Policy semantics")
        if "recommended" not in text or "not-required" not in text:
            errors.append(f"{rel} missing risk-based Review Policy choices")

    for rel in (
        "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
        "standards/GITHUB_WORKFLOW.md",
        "templates/project/.dev-standard/PROJECT_OVERRIDES.md",
    ):
        text = read_required_text(rel)
        for token in ("review:required", "review:recommended", "review:not-required"):
            if token not in text:
                errors.append(f"{rel} missing portable Review Policy label: {token}")

    event_protocol = read_required_text("standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md")
    event_template = read_required_text("templates/agent-event-comment.md")
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
        text = read_required_text(rel)
        if "REVIEW_POLICY_DECISION" in text:
            errors.append(f"{rel} uses deprecated REVIEW_POLICY_DECISION; use REVIEW_DECISION")
        for phrase in stale_mandatory_phrases:
            if phrase in text:
                errors.append(f"{rel} contains stale universal Review requirement: {phrase}")

# v3.1+ logical operator attribution contract.
if version_tuple and version_tuple >= (3, 1, 0):
    operator_surfaces = [
        "README.md",
        "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
        "standards/CHATGPT_WEB_ROLE.md",
        "templates/agent-event-comment.md",
        "templates/project/.dev-standard/PROJECT_OVERRIDES.md",
        "prompts/independent-review-bootstrap.md",
        "prompts/local-agent-bootstrap.md",
    ]
    required_tokens = (
        "actor_role",
        "operator_kind",
        "operator_id",
        "session_ref",
        "transport_actor",
    )
    for rel in operator_surfaces:
        text = read_required_text(rel)
        for token in required_tokens:
            if token not in text:
                errors.append(f"{rel} missing operator attribution token: {token}")

    event_protocol = read_required_text("standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md")
    event_template = read_required_text("templates/agent-event-comment.md")
    for rel, text in (
        ("standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md", event_protocol),
        ("templates/agent-event-comment.md", event_template),
    ):
        if "ai-dev:event:v2" not in text or "ai-dev/event-v2" not in text:
            errors.append(f"{rel} missing event v2 schema/marker")
        for event in ("ROLE_CLAIMED", "ROLE_RELEASED"):
            if event not in text:
                errors.append(f"{rel} missing operator lifecycle event: {event}")

    if "transport identity" not in event_protocol and "transport_actor" not in event_protocol:
        errors.append("GitHub Agent Interaction Protocol does not distinguish transport identity")

    if "ai-dev:event:v1" not in event_protocol or "ai-dev:event:v1" not in event_template:
        errors.append("event v1 backward-compatibility is not documented")

if errors:
    print("standard verification: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("standard verification: PASS")
print(f"manifest files: {len(manifest_paths)}")
print(f"bootstrap-required files: {len(BOOTSTRAP_REQUIRED)}")
