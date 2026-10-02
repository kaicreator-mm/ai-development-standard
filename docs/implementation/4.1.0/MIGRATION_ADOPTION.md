# v4.1 Execution Foundation — Migration & Adoption

Status: implementation guidance for Frozen v4.1 Product/L2. This document is non-authoritative where it summarizes normative owners.

## 1. Purpose

v4.1 adds five execution-foundation concerns without replacing existing workflow, Validation, Review, CI or Release authority:

- Dependency & Toolchain Governance
- Git Execution & Worktree Isolation
- Configuration & Secrets Governance
- Workspace & Artifact Governance
- External System Execution

The shared `Execution Context` is a non-authoritative projection of applicable material execution facts.

## 2. Adoption principle

Adopt only the concerns that are material to the project/task, but preserve truth for every concern that actually applies.

```text
material concern -> resolve owning standard -> capture required durable facts/evidence
non-material concern -> no mandatory machine object
truly inapplicable concern -> NOT_APPLICABLE + rationale when a gate/profile asks for it
```

A project does not need to instantiate every v4.1 schema merely because it pins a v4.1-capable standard.

## 3. Execution Foundation Profile

Projects SHOULD use `.dev-standard/PROJECT_OVERRIDES.md` to state which v4.1 execution concerns are material by default and where project authority lives.

Recommended project fields:

```text
execution_foundation.profile = materiality-driven | strict | project-specific
execution_foundation.dependency_toolchain = applicable | NOT_APPLICABLE + reason
execution_foundation.git_execution = applicable | NOT_APPLICABLE + reason
execution_foundation.configuration_secrets = applicable | NOT_APPLICABLE + reason
execution_foundation.workspace_artifact = applicable | NOT_APPLICABLE + reason
execution_foundation.external_systems = applicable | NOT_APPLICABLE + reason
execution_foundation.execution_context = when-material | always | NOT_APPLICABLE + reason
```

These fields configure adoption/discovery only. They cannot weaken Frozen Product/Architecture/Task or required Validation/Release authority.

## 4. Owner map

| Concern | Normative owner |
|---|---|
| dependency manifest/lock/toolchain/risk disposition | `standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md` |
| repository/worktree/exact checkout/destructive Git safety | `standards/GIT_EXECUTION_STANDARD.md` |
| config precedence/secret refs/secret-value handling | `standards/CONFIGURATION_SECRETS_STANDARD.md` |
| workspace/artifact classes/ownership/promotion/cleanup | `standards/WORKSPACE_ARTIFACT_STANDARD.md` |
| external fidelity/environment/side-effect execution | `standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` |
| Validation result/currentness/reuse | existing `standards/VALIDATION_STANDARD.md` |
| Release Qualification | existing `standards/RELEASE_STANDARD.md` |

Other standards and checklists should reference these owners rather than restate their semantics.

## 5. Machine records

Default v4.1 machine-contract families are:

- `schemas/execution-context-v1.schema.json`
- `schemas/dependency-toolchain-profile-v1.schema.json`
- `schemas/dependency-risk-exception-v1.schema.json`

Rules:

- `Execution Context` is non-authoritative and optional when durable machine exchange is useful.
- A Dependency Risk Exception is a risk disposition, never Validation PASS or proof of remediation.
- Secret values do not belong in ordinary durable context/evidence; use secret refs/identity.
- Historical v4 payloads remain valid when optional v4.1 references are absent.

## 6. Progressive adoption

### Minimal / Fast Path

For a small docs/mechanical change with no material toolchain/config/artifact/external-system delta:

- use normal exact Git identity and focused Validation;
- do not generate empty Execution Context or dependency-risk records;
- do not create fake external/environment facts.

### Typical service/library

Usually material:

- dependency/toolchain authority;
- Git exact-subject/worktree semantics;
- config/secret handling if runtime configuration exists;
- workspace/artifact lifecycle if build outputs exist;
- external-system semantics only for real databases/APIs/services used by the task.

### High-risk delivery/integration work

Use explicit execution-context and toolchain/environment refs when evidence reuse or cross-Agent handoff depends on them. Higher risk may strengthen requirements; it does not create new Gate result states.

## 7. Migration from earlier v4

Existing projects keep historical facts exactly as originally produced. Migration is prospective:

1. pin the new standard revision;
2. update `PROJECT_OVERRIDES.md` with truthful execution-foundation applicability;
3. resolve project dependency/toolchain/config/artifact/external authority;
4. update checklists/commands where material;
5. run project/standard verifier and required current Validation;
6. do not retroactively claim old executions had v4.1 context/provenance that was never recorded.

## 8. Forbidden shortcuts

```text
local installed runtime -> repository toolchain requirement
worktree exists -> task state
secret value in private Issue -> acceptable durable secret storage
file exists in build output -> release artifact
mock/sandbox PASS -> unexecuted real external PASS
credential exists -> side-effect authority
risk exception -> Validation PASS
```

## 9. Closure carry-forward

v4.1 T08/Version Closure should verify at least:

- manifest/project template/checklist discoverability;
- Fast Path does not require empty/non-applicable contracts;
- old payloads remain valid;
- carried focused-test depth findings from T01/T02/T05/T06 are dispositioned;
- integrated candidate proves no cross-owner authority duplication.
