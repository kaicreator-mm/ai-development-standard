# T-009 Task Pack — Interchange Replay / Restart Conformance

Status: **CANDIDATE TASK PACK — NOT BUILDER READY**

Authority: Frozen DAG R1 blob `72dfeee93c092296004c7083b71fdd877d7f1b34`; Issue #515.

```yaml
task_id: T-009
dependencies: [T-003]
integration_target: version/v4.8.0
review_policy: required
validation_scope: concern
validation_owner: independent-from-builder
l3_requirement: reference
agent_freedom: F2
jit_branch: true
execution_pack: JIT
```

Allowed write set: deterministic Interchange replay/idempotency/restart tests and fixtures. Forbidden: new Exchange lifecycle/family, delivery chronology as authority, event-v2 replacement.

Acceptance: same identity+payload idempotent; conflicting payload/digest fails closed; lost/replayed/stale delivery handled; ACK/progress non-authoritative; canonical effects materialize durably; restart reconstructs without queue/chat history.

Required Validation: replay/idempotency/currentness/restart suite. Fresh exact-HEAD Review required.