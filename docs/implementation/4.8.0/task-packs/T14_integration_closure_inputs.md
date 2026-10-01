# T-014 Task Pack — Integrated Convergence / Version Closure Inputs

Status: **CANDIDATE TASK PACK — NOT BUILDER READY**

Authority: Frozen DAG R1 blob `72dfeee93c092296004c7083b71fdd877d7f1b34`; Issue #520.

```yaml
task_id: T-014
dependencies: [T-006, T-007, T-008, T-009, T-010, T-011, T-012, T-013]
integration_target: version/v4.8.0
review_policy: required
validation_scope: integrated-closure-inputs
validation_owner: independent-from-builders
l3_requirement: required
agent_freedom: F1
jit_branch: true
execution_pack: JIT
```

Allowed write set: integrated v4.8 conformance tests and `docs/implementation/4.8.0/closure/**`. Forbidden: Release Qualification verdict, tag/main integration, silent semantic repair, unmeasured economic/routing claims.

Acceptance: exactly three new machine families and reused Interchange owner; owner uniqueness; hard eligibility-before-ranking; composite resource atomicity; backward compatibility/Fast Path; bounded dogfood claims; full required repository/integrated validation evidence. Produce closure inputs only.

Required Validation: full integrated regression + closure evidence + independent integration review.