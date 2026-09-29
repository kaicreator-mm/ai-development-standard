# Task Pack — T02 Dependency & Toolchain Governance

```yaml
task_id: T02
repository: kaicreator-mm/ai-development-standard
version: 4.1.0
integration_target: version/v4.1.0
merge_target: version/v4.1.0
task_pack_ref: docs/implementation/4.1.0/task-packs/T02_dependency_toolchain.md
dependencies: [T01]
allowed_write_set:
  - standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md
  - references/DEPENDENCY_TOOLCHAIN_REFERENCE.md
  - scripts/test_v41_dependency_toolchain.py
forbidden_scope:
  - T01 shared schemas except consumption/reference
  - standard-manifest.json
  - PROJECT_OVERRIDES and shared checklists/workflow wiring
  - Git/config/artifact/external normative owners
acceptance:
  - #187 required semantics are implemented without ecosystem lock-in
  - compatibility and certification are distinct
  - dependency class/path/exposure are preserved in risk disposition
  - risk exception never becomes PASS/remediation
  - dependency/toolchain delta participates in Validation Impact by reference to existing owner
required_gates:
  - focused semantic/regression tests
  - Node/npm and at least one non-Node example
validation_scope: concern
validation_owner: T02
review_policy: required
l3_requirement: docs/implementation/4.1.0/L3_REFERENCE_PACKS.md#t02--dependency--toolchain-governance
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
execution_pack: JIT
```

## Why

Issue #187 contains the detailed Product/research input. T02 turns it into one normative owner after T01 freezes the shared contract vocabulary.

## Acceptance detail

The standard must cover manifest/lock authority, dependency classes, change policy, vulnerability applicability, exceptions, toolchain compatibility/preferred/certification/deployment distinctions, supply-chain/provenance/license/SBOM policy, lifecycle/EOL and Agent behavior. It must reference Validation/CI/Release owners rather than duplicate their Gate semantics.

## Out of scope

No universal package-manager command, no scanner-specific release policy, no central adoption wiring, no edits to sibling normative standards.
