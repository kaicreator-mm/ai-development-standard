from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

required = {
    "standards/CI_RUNNER_CAPABILITY_STANDARD.md": (
        "Capability Profile Semantics",
        "Runtime Preflight Still Required",
        "Profile Storage",
        "templates/ci-runner-capability.yaml",
    ),
    "templates/ci-runner-capability.yaml": (
        "schema: ai-development-standard/ci-runner-capability/v1",
        "observed_at:",
        "workspace_write_delete:",
        "child_process_spawn:",
        "capabilities:",
        "limitations:",
    ),
    "references/WOODPECKER_UBUNTU_BUILD_01_CAPABILITY_2026-09-18.yaml": (
        "schema: ai-development-standard/ci-runner-capability/v1",
        "id: ubuntu-build-01",
        "provider: woodpecker",
        "provider_version: 3.18.1",
        "backend: local",
        "release: 24.04.4 LTS",
        "cpu_count: 2",
        "memory_total: 3.4GiB",
        "max_workflows: 1",
        "node: v24.21.0",
        "python3: 3.12.3",
        "go: 1.27.1",
        "docker: unavailable",
        "java: unavailable",
        "rust: unavailable",
        "dotnet: unavailable",
        "native-node-build",
        "workspace-write-delete",
        "child-process-spawn",
        "secrets_redacted: true",
        "contains_credentials: false",
    ),
}

errors: list[str] = []
for rel, tokens in required.items():
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"missing runner capability file: {rel}")
        continue
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            errors.append(f"{rel} missing capability token: {token}")

reference = ROOT / "references/WOODPECKER_UBUNTU_BUILD_01_CAPABILITY_2026-09-18.yaml"
if reference.is_file():
    text = reference.read_text(encoding="utf-8")
    forbidden = (
        "WOODPECKER_AGENT_SECRET=",
        "WOODPECKER_GITHUB_SECRET=",
        "PRIVATE_KEY=",
        "ACCESS_TOKEN=",
        "PASSWORD=",
    )
    for token in forbidden:
        if token in text:
            errors.append(f"runner capability reference leaks forbidden secret-like field: {token}")

    if "Capability inventory is suitable for routing only" not in text:
        errors.append("runner capability reference does not separate routing inventory from Validation Evidence")

if errors:
    print("runner capability reference verification: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("runner capability reference verification: PASS")
print(f"checked files: {len(required)}")
