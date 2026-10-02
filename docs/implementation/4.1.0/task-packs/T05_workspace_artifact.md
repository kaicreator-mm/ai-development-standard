# Task Pack — T05 Workspace & Artifact Governance

```yaml
task_id: T05
repository: kaicreator-mm/ai-development-standard
version: 4.1.0
integration_target: version/v4.1.0
merge_target: version/v4.1.0
task_pack_ref: docs/implementation/4.1.0/task-packs/T05_workspace_artifact.md
dependencies: [T01]
allowed_write_set:
  - standards/WORKSPACE_ARTIFACT_STANDARD.md
  - references/WORKSPACE_ARTIFACT_REFERENCE.md
  - scripts/test_v41_workspace_artifact.py
forbidden_scope:
  - T01 shared schemas except consumption/reference
  - standard-manifest.json
  - PROJECT_OVERRIDES and shared workflow/checklist wiring
  - full v4.4 build/package Artifact Manifest design
acceptance:
  - canonical semantic classes and ownership/lifecycle rules are explicit
  - cache/build output cannot imply validation evidence or release artifact
  - runtime state is not disposable cache by default
  - unknown/unowned state cannot be destructively cleaned
  - promotion requires authorized identity/binding rather than file existence
required_gates:
  - class/promotion/cleanup positive and negative checks
validation_scope: concern
validation_owner: T05
review_policy: required
l3_requirement: docs/implementation/4.1.0/L3_REFERENCE_PACKS.md#t05--workspace--artifact-governance
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
execution_pack: JIT
```

## Why

Agents and CI commonly conflate cache, runtime state, generated/build output and durable artifacts. T05 provides one semantic classification/promotion owner without prematurely taking over v4.4 delivery design.

## Acceptance detail

Define class, ownership, mutability, persistence, cleanup, Git/evidence eligibility, reconstruction and promotion semantics for SOURCE, GENERATED_SOURCE, BUILD_OUTPUT, CACHE, RUNTIME_STATE, TEST_ARTIFACT, VALIDATION_EVIDENCE, RELEASE_ARTIFACT and SECRET_MATERIAL.

## Out of scope

No full package/distribution manifest, no Release verdict, no CI evidence ownership rewrite, no central adoption wiring.
