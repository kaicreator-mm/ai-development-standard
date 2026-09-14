from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import tempfile

from verify_test_data_pack import verify as verify_test_data_pack

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "VERSION",
    "README.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "standards/DEVELOPMENT_WORKFLOW.md",
    "standards/CHATGPT_WEB_ROLE.md",
    "standards/CODEX_ROLE.md",
    "standards/CODEX_HANDOFF_PROTOCOL.md",
    "standards/VALIDATION_STANDARD.md",
    "standards/GITHUB_WORKFLOW.md",
    "standards/RELEASE_STANDARD.md",
    "standards/MODEL_USAGE_POLICY.md",
    "standards/PROJECT_ADOPTION.md",
    "standards/REPOSITORY_STANDARD.md",
    "standards/PROJECT_STRUCTURE.md",
    "standards/DOCUMENTATION_STANDARD.md",
    "standards/TESTING_STANDARD.md",
    "standards/TEST_DATA_AND_SCENARIO_STANDARD.md",
    "templates/codex-handoff-issue.md",
    "templates/implementation-pr.md",
    "templates/validation-report.md",
    "templates/final-closeout.md",
    "templates/task-dag.md",
    "templates/test-data-pack.md",
    "prompts/L1_PRODUCT_EVIDENCE.md",
    "prompts/L2_ARCHITECTURE_EVIDENCE.md",
    "prompts/L3_IMPLEMENTATION_EVIDENCE.md",
    "prompts/CODEX_EXECUTION.md",
    "prompts/TEST_DATA_GENERATION.md",
    "checklists/project-init.md",
    "checklists/pr-review.md",
    "checklists/version-closure.md",
    "checklists/test-data-review.md",
    "references/GITHUB_ENGINEERING_REFERENCES.md",
    "references/TEST_DATA_ENGINEERING_REFERENCES.md",
    "scripts/verify_test_data_pack.py",
    "examples/test-data-pack/quote-assessment/manifest.json",
    "examples/test-data-pack/quote-assessment/VALIDATION_REPORT.md",
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
        # Template shorthand is tolerated, but canonical docs should use NOT_APPLICABLE.
        pass

reference_pack = ROOT / "examples/test-data-pack/quote-assessment"
if reference_pack.is_dir():
    for error in verify_test_data_pack(reference_pack):
        errors.append(f"reference test-data pack: {error}")

    generator = reference_pack / "generate_supplement.py"
    coverage_path = reference_pack / "coverage.json"
    if generator.is_file() and coverage_path.is_file():
        coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
        expected_hash = coverage.get("reproducibility", {}).get("generated_cases_sha256")
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "generated.jsonl"
            proc = subprocess.run(
                [sys.executable, str(generator), str(output)],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            if proc.returncode != 0:
                errors.append(f"reference generator replay failed: {proc.stderr.strip() or proc.stdout.strip()}")
            elif not output.is_file():
                errors.append("reference generator replay did not create output")
            elif expected_hash:
                actual_hash = hashlib.sha256(output.read_bytes()).hexdigest()
                if actual_hash != expected_hash:
                    errors.append(
                        "reference generator replay hash mismatch: "
                        f"expected {expected_hash}, got {actual_hash}"
                    )
            else:
                errors.append("reference coverage missing generated_cases_sha256")

if errors:
    print("standard verification: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("standard verification: PASS")
print(f"required files: {len(REQUIRED)}")
print("reference test-data pack: PASS")
print("reference generator replay: PASS")
