from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "standard-manifest.json"

errors: list[str] = []


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

    core_required = {
        "VERSION",
        "README.md",
        "AGENTS.md",
        "CHANGELOG.md",
        "standards/DEVELOPMENT_WORKFLOW.md",
        "standards/VERSION_INTEGRATION_WORKFLOW.md",
        "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
        "standards/PROJECT_STRUCTURE.md",
        "standards/REPOSITORY_STANDARD.md",
        "standards/DOCUMENTATION_STANDARD.md",
        "standards/TESTING_STANDARD.md",
        "standards/VALIDATION_STANDARD.md",
        "standards/RELEASE_STANDARD.md",
        "standards/PROJECT_ADOPTION.md",
        "templates/task-issue.md",
        "templates/agent-event-comment.md",
        "templates/implementation-pr.md",
        "templates/validation-report.md",
        "checklists/project-init.md",
        "checklists/pr-review.md",
        "checklists/version-closure.md",
        "schemas/agent-event-v2.schema.json",
        "schemas/task-contract.schema.json",
        "schemas/validation-report.schema.json",
        "scripts/verify_project_standard.py",
        "scripts/test_verify_project_standard.py",
        "scripts/test_protocol_schemas.py",
        ".github/workflows/verify-standard.yml",
    }
    missing_core = sorted(core_required - seen)
    for rel in missing_core:
        errors.append(f"manifest omits core standard asset: {rel}")

    machine_contracts = sections.get("machine_contracts", [])
    if isinstance(machine_contracts, list):
        for rel in machine_contracts:
            path = ROOT / rel
            if not path.is_file():
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
version_path = ROOT / "VERSION"
if version_path.exists():
    version = version_path.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append(f"VERSION is not SemVer: {version!r}")
    else:
        version_tuple = tuple(int(part) for part in version.split("."))

if version:
    readme_path = ROOT / "README.md"
    if readme_path.is_file():
        readme = readme_path.read_text(encoding="utf-8")
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

if version_tuple and version_tuple[0] >= 3:
    for rel in review_policy_files:
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "Review Policy" not in text:
            errors.append(f"{rel} missing Review Policy semantics")
        if "recommended" not in text or "not-required" not in text:
            errors.append(f"{rel} missing risk-based Review Policy choices")

    for rel in (
        "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
        "standards/GITHUB_WORKFLOW.md",
        "templates/project/.dev-standard/PROJECT_OVERRIDES.md",
    ):
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for token in ("review:required", "review:recommended", "review:not-required"):
            if token not in text:
                errors.append(f"{rel} missing portable Review Policy label: {token}")

    event_protocol_path = ROOT / "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md"
    event_template_path = ROOT / "templates/agent-event-comment.md"
    event_protocol = event_protocol_path.read_text(encoding="utf-8") if event_protocol_path.is_file() else ""
    event_template = event_template_path.read_text(encoding="utf-8") if event_template_path.is_file() else ""
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
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
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
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for token in required_tokens:
            if token not in text:
                errors.append(f"{rel} missing operator attribution token: {token}")

    event_protocol = (ROOT / "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md").read_text(encoding="utf-8")
    event_template = (ROOT / "templates/agent-event-comment.md").read_text(encoding="utf-8")
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
