# T-001 Task Pack — Task Learning Evidence Contract

Status: **CANDIDATE TASK PACK — NOT BUILDER READY**

Authority: Frozen DAG R1 `634dd746cd16da970bb01822a1b6c59714c52429` / `72dfeee93c092296004c7083b71fdd877d7f1b34`; Frozen L2 `f88c85454e80101a0fdf56050e21f11a05279841`; Issue #507.

```yaml
task_id: T-001
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
- `schemas/task-learning-v1.schema.json`
- focused v4.8 Task Learning tests/fixtures
- T-001 reference material

## Forbidden scope
Logical Agent Capability Profile, Agent Capability Evidence, Execution Architecture integration, Product/L2/DAG authority.

## Acceptance
1. Exact work/subject/evidence/currentness bindings are explicit.
2. `TASK_LEARNING=NONE_MATERIAL` remains a valid no-object Fast Path.
3. Rationale is an externally useful engineering summary, never private chain-of-thought.
4. Stale exact-subject learning remains historical and cannot silently bind successor code.
5. Learning never becomes Product/Architecture/Task/ADR/Incident/Review/Validation authority.

Required Validation: schema positive/negative fixtures, historical compatibility, stale/currentness oracles. Fresh exact-HEAD Review required after Validation.