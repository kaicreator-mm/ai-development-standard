from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "standard-manifest.json"

# Code-owned bootstrap set prevents deleting an asset together with its manifest entry.
BOOTSTRAP_REQUIRED = {
    "standard-manifest.json",
    "VERSION",
    "README.md",
    "AGENTS.md",
    "standards/CHATGPT_WEB_ROLE.md",
    "standards/DEVELOPMENT_WORKFLOW.md",
    "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
    "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md",
    "standards/ISSUE_FIRST_TASK_TRIGGER.md",
    "standards/VALIDATION_STANDARD.md",
    "standards/RELEASE_STANDARD.md",
    "standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md",
    "standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md",
    "schemas/agent-event-v2.schema.json",
    "schemas/task-contract.schema.json",
    "schemas/validation-report.schema.json",
    "schemas/execution-state.schema.json",
    "schemas/local-agent-handoff.schema.json",
    "scripts/verify_standard.py",
    "scripts/test_verify_standard.py",
    "scripts/test_protocol_schemas.py",
    "scripts/test_execution_architecture.py",
}

errors: list[str] = []


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing required file: {rel}")
        return ""
    return path.read_text(encoding="utf-8")


for rel in sorted(BOOTSTRAP_REQUIRED):
    if not (ROOT / rel).is_file():
        errors.append(f"bootstrap-required asset is missing: {rel}")

try:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as exc:
    errors.append(f"invalid standard-manifest.json: {exc}")
    manifest = {}

if manifest.get("schema_version") != 1:
    errors.append("standard-manifest.json schema_version must be 1")

sections = manifest.get("sections")
if not isinstance(sections, dict) or not sections:
    errors.append("standard-manifest.json sections must be a non-empty object")
    sections = {}

seen: set[str] = set()
manifest_paths: list[str] = []
for section, values in sections.items():
    if not isinstance(values, list) or not values:
        errors.append(f"manifest section {section!r} must be a non-empty list")
        continue
    for rel in values:
        if not isinstance(rel, str) or not rel:
            errors.append(f"manifest section {section!r} contains invalid path: {rel!r}")
            continue
        candidate = Path(rel)
        if candidate.is_absolute() or ".." in candidate.parts:
            errors.append(f"manifest path must be repository-relative: {rel}")
            continue
        if rel in seen:
            errors.append(f"manifest path declared more than once: {rel}")
            continue
        seen.add(rel)
        manifest_paths.append(rel)
        if not (ROOT / rel).is_file():
            errors.append(f"manifest-declared file is missing: {rel}")

for rel in sorted(BOOTSTRAP_REQUIRED):
    if rel not in seen:
        errors.append(f"manifest omits bootstrap-required asset: {rel}")

version = read("VERSION").strip()
if not re.fullmatch(r"\d+\.\d+\.\d+", version):
    errors.append(f"VERSION is not SemVer: {version!r}")
readme = read("README.md")
if version and f"当前版本：`v{version}`" not in readme:
    errors.append("README current version does not match VERSION")

for rel in sections.get("machine_contracts", []):
    try:
        schema = json.loads(read(rel))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid machine contract JSON {rel}: {exc}")
        continue
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append(f"machine contract does not declare JSON Schema 2020-12: {rel}")
    if schema.get("type") != "object" or not schema.get("required"):
        errors.append(f"machine contract must be an object with required fields: {rel}")

execution = read("standards/EXECUTION_ARCHITECTURE_STANDARD.md")
for token in ("Durable facts, derived state, actions", "Separate state dimensions", "Validation ownership and cost placement", "Pointer-only agent invocation", "HEAD drift", "BASE drift", "CI infrastructure exceptions", "Candidate Freeze Controller", "Hidden Validation escaped-defect feedback", "Human Decision Queue", "Progressive adoption"):
    if token not in execution:
        errors.append(f"Execution Architecture missing semantic token: {token}")

validation = read("standards/VALIDATION_STANDARD.md")
for token in ("concern | integration | closure", "INFRA_BLOCKED", "VALIDATION_IMPACT_DECISION", "evidence_reuse_basis"):
    if token not in validation:
        errors.append(f"Validation Standard missing v3.3 semantic token: {token}")

release = read("standards/RELEASE_STANDARD.md")
for token in ("operational state", "THAWED / INVALIDATED", "HIDDEN_PACK_BLIND_SPOT", "Repository Integration"):
    if token not in release:
        errors.append(f"Release Standard missing v3.3 semantic token: {token}")

handoff = read("standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md")
for token in ("Pointer-only principle", "HANDOFF_READY", "schemas/local-agent-handoff.schema.json"):
    if token not in handoff:
        errors.append(f"Local Agent Handoff missing v3.3 semantic token: {token}")

issue_first = read("standards/ISSUE_FIRST_TASK_TRIGGER.md")
for token in ("Issue = durable task contract and current Source of Truth", "Trigger prompt = short ephemeral execution trigger", "one task = one Issue = one trigger prompt"):
    if token not in issue_first:
        errors.append(f"Issue-first trigger regression: missing {token}")
agents = read("AGENTS.md")
if "standards/ISSUE_FIRST_TASK_TRIGGER.md" not in agents:
    errors.append("AGENTS.md does not route Issue-trigger work to ISSUE_FIRST_TASK_TRIGGER.md")

for rel in ("standards/GITHUB_WORKFLOW.md", "standards/VERSION_INTEGRATION_WORKFLOW.md", "standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md", "templates/local-agent-handoff-issue.md", "README.md"):
    text = read(rel)
    if "new writers emit `ai-dev:event:v1`" in text or "publish `ai-dev:event:v1`" in text:
        errors.append(f"{rel} instructs new work to emit event-v1")
    if "ai-dev:event:v2" not in text:
        errors.append(f"{rel} missing canonical event-v2 writer guidance")

demo = read("standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md")
for token in ("falsifiable hypothesis", "The component or boundary under test MUST be real", "What was NOT proven"):
    if token not in demo:
        errors.append(f"Architecture Research Demo regression: missing {token}")

event_schema = json.loads(read("schemas/agent-event-v2.schema.json") or "{}")
event_enum = event_schema.get("properties", {}).get("event", {}).get("enum", [])
for event in ("HANDOFF_READY", "DISPATCH_REQUEST", "CI_INFRA_EXCEPTION", "VALIDATION_IMPACT_DECISION", "CANDIDATE_STATE_CHANGED", "HIDDEN_ESCAPE_DISPOSITION", "RELEASE_QUALIFICATION", "REPOSITORY_INTEGRATION_RESULT"):
    if event not in event_enum:
        errors.append(f"agent-event-v2 schema missing v3.3 event: {event}")

if errors:
    print("standard verification: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("standard verification: PASS")
print(f"manifest files: {len(manifest_paths)}")
print(f"bootstrap-required files: {len(BOOTSTRAP_REQUIRED)}")
