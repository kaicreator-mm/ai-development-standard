# T-016 Task Pack — Agent Capability Evidence Contract

Status: **CANDIDATE TASK PACK — NOT BUILDER READY**

Authority: Frozen DAG R1 `634dd746cd16da970bb01822a1b6c59714c52429` / `72dfeee93c092296004c7083b71fdd877d7f1b34`; Frozen L2 `f88c85454e80101a0fdf56050e21f11a05279841`; Issue #524.

```yaml
task_id: T-016
dependencies: []
integration_target: version/v4.8.0
review_policy: required
validation_scope: concern
validation_owner: independent-from-builder
l3_requirement: required
agent_freedom: F1
jit_branch: true
execution_pack: JIT
```

## Allowed write set
- `schemas/agent-capability-evidence-v1.schema.json`
- focused evidence fixtures/tests
- T-016 reference material

## Forbidden scope
Current Validation/Review authority, current Availability owner, global scalar Agent score, unmeasured economic inference.

## Acceptance
1. Evidence is historical/exact-subject and supports positive and negative observations.
2. It may reference Agent and environment/runner identities without copying their owner facts.
3. Historical success never implies current Availability, Review or Validation PASS.
4. Evidence strength is layered/bounded, not a universal score.
5. Economic/performance conclusions require comparable measured methodology.

Required Validation: schema + false-authority + stale/currentness + economic non-inference oracles. Fresh exact-HEAD Review required.