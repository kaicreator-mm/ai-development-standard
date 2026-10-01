# T-004 Task Pack — Task Learning Closeout / Template Wiring

Status: **CANDIDATE TASK PACK — NOT BUILDER READY**

Authority: Frozen DAG R1 blob `72dfeee93c092296004c7083b71fdd877d7f1b34`; Issue #511.

```yaml
task_id: T-004
dependencies: [T-001, T-002]
integration_target: version/v4.8.0
review_policy: required
validation_scope: concern
validation_owner: independent-from-builder
l3_requirement: reference
agent_freedom: F2
jit_branch: true
execution_pack: JIT
```

Allowed write set: applicable Task/Task-Pack/final-closeout/Execution-Pack templates and checklists only. Forbidden: Task Learning schema semantics, Execution Architecture semantics, ADR/Incident/Product/Architecture authority.

Acceptance: material and `NONE_MATERIAL` paths explicit; evidence refs preferred over copied bodies; stale source never silently inherits behavioral claims; no private chain-of-thought or authority substitution.

Required Validation: template/reference conformance and pointer/currentness checks. Fresh exact-HEAD Review required.