# Task Pack — T06 External System Execution

```yaml
task_id: T06
repository: kaicreator-mm/ai-development-standard
version: 4.1.0
integration_target: version/v4.1.0
merge_target: version/v4.1.0
task_pack_ref: docs/implementation/4.1.0/task-packs/T06_external_systems.md
dependencies: [T01]
allowed_write_set:
  - standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md
  - references/EXTERNAL_SYSTEM_EXECUTION_REFERENCE.md
  - scripts/test_v41_external_systems.py
forbidden_scope:
  - T01 shared schemas except consumption/reference
  - standard-manifest.json
  - PROJECT_OVERRIDES and shared workflow/checklist wiring
  - new Validation Gate/result state model
acceptance:
  - fidelity/environment/state-scope/side-effect dimensions are explicit and extensible
  - lower-fidelity PASS cannot satisfy higher-fidelity requirement
  - environment/account/tenant and write authority are evidence-relevant when material
  - infrastructure/credential/service/rate-limit unavailability remains distinct from product defect
  - retry/timeout behavior is bounded
required_gates:
  - fidelity and side-effect negative scenarios
  - infrastructure truth scenarios
validation_scope: concern
validation_owner: T06
review_policy: required
l3_requirement: docs/implementation/4.1.0/L3_REFERENCE_PACKS.md#t06--external-system-execution
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
execution_pack: JIT
```

## Why

External APIs/databases/cloud/LLM/browser/build-host execution can silently escalate fidelity or side-effect authority. T06 defines the execution contract while leaving PASS/FAIL/BLOCKED ownership in Validation.

## Acceptance detail

Define real-vs-double fidelity, provider/project environment identity, ephemeral/shared state, side-effect authority, account/tenant identity, credential references, bounded retries/timeouts and truthful infrastructure failure classification. Provider labels remain extensible.

## Out of scope

No universal provider taxonomy, no production-write authorization by default, no Test/Validation state duplication, no central adoption wiring.
