# T-006 Task Pack — Registry / Discoverability / Adoption Wiring

Status: **CANDIDATE TASK PACK — NOT BUILDER READY**

Authority: Frozen DAG R1 blob `72dfeee93c092296004c7083b71fdd877d7f1b34`; Issue #512.

```yaml
task_id: T-006
dependencies: [T-001, T-015, T-016, T-002, T-003, T-004, T-005]
integration_target: version/v4.8.0
review_policy: required
validation_scope: integration
validation_owner: independent-from-builder
l3_requirement: reference
agent_freedom: F2
jit_branch: true
execution_pack: JIT
```

Allowed write set: `standard-manifest.json`, project-adoption/progressive-disclosure surfaces, migration/adoption references, central verifier wiring. Forbidden: sibling semantic owner rewrites, fourth machine family, new Interchange owner.

Acceptance: exactly three new families discoverable; Interchange represented as reuse; registry grants no semantic authority; historical consumers and Fast Path remain valid.

Required Validation: manifest/registry/project-adoption verifier. Fresh exact-HEAD Review required.