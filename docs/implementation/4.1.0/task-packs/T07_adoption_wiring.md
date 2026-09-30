# Task Pack — T07 Adoption & Cross-standard Wiring

```yaml
task_id: T07
repository: kaicreator-mm/ai-development-standard
version: 4.1.0
integration_target: version/v4.1.0
merge_target: version/v4.1.0
task_pack_ref: docs/implementation/4.1.0/task-packs/T07_adoption_wiring.md
dependencies: [T02, T03, T04, T05, T06]
allowed_write_set:
  - standard-manifest.json
  - templates/golden/STANDARD_COVERAGE.json
  - templates/project/.dev-standard/PROJECT_OVERRIDES.md
  - standards/DEVELOPMENT_WORKFLOW.md
  - standards/CI_EXECUTION_STANDARD.md
  - standards/CI_EVIDENCE_STANDARD.md
  - standards/TESTING_STANDARD.md
  - standards/VALIDATION_STANDARD.md
  - standards/RELEASE_STANDARD.md
  - standards/PROJECT_ADOPTION.md
  - checklists/project-init.md
  - checklists/pr-review.md
  - checklists/version-closure.md
  - README.md
  - docs/implementation/4.1.0/MIGRATION_ADOPTION.md
  - scripts/test_v41_adoption_wiring.py
forbidden_scope:
  - redefinition of T01-T06 normative semantics
  - new workflow/Gate/Release authority
  - weakening existing v4 truth/authority floor
acceptance:
  - new standards/schemas are discoverable and centrally wired by reference
  - existing owner standards do not duplicate T01-T06 normative content
  - PROJECT_OVERRIDES exposes a lightweight Execution Foundation Profile
  - Fast Path/minimal projects are not forced to instantiate non-applicable machine contracts
  - workflow/checklists surface applicable execution-foundation facts without creating new gates
required_gates:
  - cross-standard verifier tests
  - project template/adoption regression
validation_scope: integration
validation_owner: T07
review_policy: required
l3_requirement: docs/implementation/4.1.0/L3_REFERENCE_PACKS.md#t07--adoption--cross-standard-wiring
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
execution_pack: JIT
```

## Why

T07 is the single convergence owner for shared repository surfaces. Serializing these edits after T02–T06 avoids parallel Tasks racing on the manifest, PROJECT_OVERRIDES or existing normative standards.

## Authority amendment — 2026-09-30 / #285

Fresh Independent Review #281 found that the repository's Golden normative-coverage invariant makes `templates/golden/STANDARD_COVERAGE.json` a necessary central wiring surface whenever T07 expands the canonical normative set, but the Frozen Task Pack omitted that path from `allowed_write_set`.

#285 explicitly adds **only** `templates/golden/STANDARD_COVERAGE.json` to the T07 write-set. This amendment does not change Task dependencies, DAG topology, acceptance semantics, agent freedom, required gates, validation/review ownership, or any T01–T06 normative owner. It does not retrospectively authorize unrelated writes.

## Acceptance detail

Wire new owners through references, update adoption/profile surfaces, manifest inventories and relevant checklists/workflow hooks. Preserve exact existing Gate/Release ownership and A0–A4 progressive adoption semantics. Golden coverage may be updated only as necessary to keep the repository's existing normative-set coverage invariant aligned with the T07 manifest/owner expansion.

## Out of scope

No substantive rewrite of T01–T06 owner standards, no closure verdict, no hidden scope addition, no process-gap #190 implementation.
