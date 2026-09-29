# Task Pack — T01 Shared Execution Context & Machine Contracts

> Durable planning authority. Exact-base execution detail belongs to the JIT Execution Pack.

```yaml
task_id: T01
repository: kaicreator-mm/ai-development-standard
version: 4.1.0
integration_target: version/v4.1.0
merge_target: version/v4.1.0
task_pack_ref: docs/implementation/4.1.0/task-packs/T01_shared_machine_contracts.md
dependencies: []
allowed_write_set:
  - schemas/execution-context-v1.schema.json
  - schemas/dependency-toolchain-profile-v1.schema.json
  - schemas/dependency-risk-exception-v1.schema.json
  - schemas/validation-report.schema.json
  - schemas/dispatch.schema.json
  - schemas/execution-pack-manifest.schema.json
  - scripts/test_v41_execution_foundation_contracts.py
forbidden_scope:
  - normative T02-T06 standard prose beyond schema-contract comments
  - standard-manifest.json
  - templates/project/.dev-standard/PROJECT_OVERRIDES.md
  - workflow/checklist/release convergence owned by T07
acceptance:
  - three new schemas implement Frozen L2 semantics
  - existing v4 representative payloads remain valid
  - execution context contains no workflow/Gate/Release authority
  - durable schema has secret references only and no secret-value escape hatch
  - optional v4.1 integrations are additive
required_gates:
  - focused JSON Schema positive/negative tests
  - backward-compatibility fixture validation
validation_scope: concern
validation_owner: T01
review_policy: required
l3_requirement: docs/implementation/4.1.0/L3_REFERENCE_PACKS.md#t01--shared-execution-context--machine-contracts
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
execution_pack: JIT
```

## Why

T01 freezes the shared machine vocabulary before five parallel normative lanes begin. Centralizing schema ownership prevents T02-T06 from inventing incompatible execution-context shapes.

## Acceptance detail

1. `execution-context-v1` is a non-authoritative projection with optional material sections and explicit secret-ref-only semantics.
2. dependency/toolchain profile preserves compatibility, preferred development, certification and deployment identity as distinct facts.
3. dependency risk exception cannot encode PASS/remediation merely because risk is accepted/deferred.
4. optional refs/fields added to current v4 schemas do not invalidate historical representative payloads.
5. focused tests include forbidden authority-state and secret-value cases.

## Out of scope

No full normative Dependency/Git/Config/Artifact/External standard, no central manifest/template wiring, no new lifecycle/Gate state, no v4.4 artifact manifest.
