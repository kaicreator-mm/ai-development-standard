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
    "scripts/verify_project_standard.py",
    "scripts/test_verify_project_standard.py",
    "templates/local-agent-handoff-issue.md",
    "templates/codex-handoff-issue.md",
    "templates/implementation-pr.md",
    "templates/validation-report.md",
    "templates/final-closeout.md",
    "templates/task-dag.md",
    "prompts/L1_PRODUCT_EVIDENCE.md",
    "prompts/L2_ARCHITECTURE_EVIDENCE.md",
    "prompts/L3_IMPLEMENTATION_EVIDENCE.md",
    "prompts/local-agent-bootstrap.md",
    "prompts/CODEX_EXECUTION.md",
]

errors = []
for rel in REQUIRED:
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing required file: {rel}")

version_path = ROOT / "VERSION"
if version_path.exists():
    version = version_path.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append(f"VERSION is not SemVer: {version!r}")

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
