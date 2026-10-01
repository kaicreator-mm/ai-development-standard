# T-012 Task Pack — #469 Task-Class / Bounded-Agent Dogfood

Status: **CANDIDATE TASK PACK — NOT BUILDER READY**

Authority: Frozen DAG R1 blob `72dfeee93c092296004c7083b71fdd877d7f1b34`; Issue #518; seed evidence #469.

```yaml
task_id: T-012
dependencies: [T-004, T-007, T-008]
integration_target: version/v4.8.0
review_policy: required
validation_scope: exact-subject
validation_owner: independent-from-builder
l3_requirement: required
agent_freedom: F1
jit_branch: true
execution_pack: JIT_REQUIRED_BEFORE_BOUNDED_DISPATCH
```

Allowed write set: `docs/implementation/4.8.0/dogfood/469/**` and bounded evidence references. Forbidden: blanket strong→low-cost rule, unmeasured economics, provider/model as authority, Builder self-review.

Acceptance: measure clarifications/escalations, edit/test loops, negative-oracle/scope drift, stale rebinds, Validation/Review findings/rework; resource/time/cost only when observed comparably. Preserve `ECONOMIC_SAVINGS=NOT_MEASURED` until evidence supports otherwise; outcomes may be `MORE_EVIDENCE` or `NO_CHANGE`.

Required Validation: exact-subject Builder + independent Validation + Fresh Review evidence. Risk-scaled L3 and JIT exact-base Execution Pack are mandatory before bounded/low-cost execution.