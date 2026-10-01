# T-011 Task Pack — Heterogeneous Multi-Agent / Resource / Transport Dogfood

Status: **CANDIDATE TASK PACK — NOT BUILDER READY**

Authority: Frozen DAG R1 blob `72dfeee93c092296004c7083b71fdd877d7f1b34`; Issue #517.

```yaml
task_id: T-011
dependencies: [T-007, T-008, T-009]
integration_target: version/v4.8.0
review_policy: required
validation_scope: integration
authoritative_validation: exact-subject
l3_requirement: required
agent_freedom: F1
jit_branch: true
execution_pack: JIT
```

Allowed write set: `docs/implementation/4.8.0/dogfood/orchestration/**` plus bounded scenario harness/tests. Forbidden: silent semantic repair, synthetic evidence labeled real, real-host PASS without execution, standard mutation.

Acceptance: multiple READY work items and materially different Agent profiles; fresh/stale Availability; scarce-resource contention and assignment race; independence conflict; transport duplicate/replay/loss; crash/restart; bounded executor success only when eligible and escalation on semantic ambiguity.

Required Validation: scenario evidence plus exact-subject real-host handoff for external claims. Fresh Review required.