# Woodpecker Local Backend Reference Validation

## 1. Purpose

This reference records a real failure/repair sequence used to validate `standards/CI_EXECUTION_STANDARD.md`.

It is intentionally provider-specific and non-normative. The portable requirement is the CI Execution Contract; the concrete paths and commands below apply only to the validated host.

A fuller runner capability snapshot from the same host is recorded in:

- `references/WOODPECKER_UBUNTU_BUILD_01_CAPABILITY_2026-09-18.yaml`

The capability snapshot is routing/infrastructure inventory, not Validation PASS.

## 2. Reference environment

Repository:

```text
kaicreator-mm/domain-harness
```

CI environment:

```text
provider: Woodpecker CI 3.18.1
server: native systemd service
agent: native systemd service
backend: local
max workflows: 1
runner role: Ubuntu Build Host
workspace root: /var/lib/woodpecker/tmp
host Node: v24.21.0
host npm: 11.19.0
```

Relevant real host executables/configuration included:

```text
/usr/bin/bash
/usr/local/bin/node
/usr/local/bin/npm
/usr/local/bin/plugin-git
```

These paths are evidence for this host only.

## 3. Initial failure

A project workflow used container-oriented syntax:

```yaml
steps:
  - name: verify
    image: node:22-bookworm
```

On the selected Woodpecker `local` backend, the value was treated as a local executable/entrypoint rather than a Docker image. The verify step failed before project validation with:

```text
exec: "node:22-bookworm": executable file not found in $PATH
```

The failure demonstrated that provider DSL syntax cannot be interpreted independently from backend semantics.

## 4. Clone-path observations

The provider default clone path also showed optional behavior that the repository did not require:

```text
git fetch --no-tags --depth=1 --filter=tree:0 ...
git submodule update --init --recursive ...
git lfs fetch
git lfs checkout
```

For this repository:

- Git LFS was not required;
- submodules were not required;
- partial clone filtering was not necessary for the Minimal CI profile.

The project workflow therefore made the intended clone behavior explicit rather than relying on defaults.

## 5. Backend-compatible workflow mapping

The validated project mapping used local executables for the local backend:

```yaml
clone:
  - name: git
    image: /usr/local/bin/plugin-git
    settings:
      partial: false
      depth: 1
      recursive: false
      lfs: false

steps:
  - name: verify
    image: /usr/bin/bash
    commands:
      - node --version
      - npm --version
      - node -e 'const major = Number(process.versions.node.split(".")[0]); if (major < 22) { console.error("Node >=22 required"); process.exit(1); }'
      - npm ci
      - npm run lint
      - npm run typecheck
      - npm test
```

The important portable facts are:

- local backend → local executable semantics;
- runtime is host-managed;
- runtime version is checked before project validation;
- optional clone features are enabled only when needed.

The absolute paths are not portable requirements.

## 6. Fresh-run vs rerun finding

During repair, an older Woodpecker pipeline continued to execute an older PR HEAD and its stored workflow subject even after the repository workflow had been fixed.

Observed identities:

```text
old PR HEAD / pipeline subject: 3edded0adea0f775401f0ce6f3f95885befb1a2a
old pipeline: #53
old result: failure

new PR HEAD after CI execution fixes: 42a9bfd158480e4077f530f9a732487628d1c668
new pipeline: #55
```

Restarting the old pipeline did not validate the new HEAD. A fresh pipeline for the new exact SHA was required.

Pipeline #55 used the updated execution contract and proceeded normally on the local backend.

This validates the rule:

```text
rerun(old run / old SHA) != fresh run(current HEAD)
```

## 7. Runner capability probe

A later read-only capability probe, executed on 2026-09-18, confirmed additional routing facts for the same runner role:

```text
OS: Ubuntu 24.04.4 LTS / x86_64
CPU: 2
RAM: 3.4 GiB
Swap: 1.0 GiB
workspace free: about 38 GiB
Woodpecker service user: woodpecker
Node: 24.21.0
npm: 11.19.0
Python: 3.12.3
Go: 1.27.1
GCC/G++: 13.3.0
Clang: 18.1.3
SQLite CLI: 3.45.1
PostgreSQL client: 16.15
Docker/Podman: unavailable
Java: unavailable
Rust: unavailable
.NET: unavailable
```

The `woodpecker` service user successfully completed workspace create/write/delete and Node child-process smoke checks. The host also resolved and completed verified HTTPS requests to GitHub, GitHub API and npm registry endpoints.

This probe establishes routing capability only. Environment-sensitive Validation still requires a run-time preflight and exact-SHA evidence.

## 8. Validated conclusions

This reference supports the following standard requirements:

1. CI provider and backend are material execution facts.
2. Workflow DSL fields must be interpreted using the selected backend semantics.
3. Host/local backends need real host shell/runtime/plugin availability.
4. Runtime/toolchain preflight should happen before expensive validation.
5. Clone optimizations and optional features should match repository needs.
6. A new exact SHA requires evidence from a run that actually tested that SHA.
7. Restart/rerun identity must not be confused with a fresh pipeline for a new HEAD.
8. Provider-specific paths belong in project/infrastructure configuration, not the portable global standard.
9. Runner capability inventory is useful for routing, but does not substitute for run-time Validation Evidence.

## 9. Scope limitation

This reference does not claim that Woodpecker Local Backend is preferred over Docker/Kubernetes/hosted runners.

It proves only that the documented execution mapping worked for the stated real host and that the provider-neutral CI Execution Contract and Runner Capability model are useful to avoid cross-backend/environment assumptions.
