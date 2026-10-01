# T-010 Task Pack — Task Learning / Evolution Governance Conformance

Status: **CANDIDATE TASK PACK — NOT BUILDER READY**

Authority: Frozen DAG R1 blob `72dfeee93c092296004c7083b71fdd877d7f1b34`; Issue #516.

```yaml
task_id: T-010
dependencies: [T-004, T-005]
integration_target: version/v4.8.0
review_policy: required
validation_scope: concern
validation_owner: independent-from-builder
l3_requirement: reference
agent_freedom: F2
jit_branch: true
execution_pack: JIT
```

Allowed write set: learning/evolution governance tests, golden fixtures and bounded references. Forbidden: new evolution lifecycle, standard-change auto-promotion, hidden evaluator detail publication.

Acceptance: cover NONE_MATERIAL/material learning, stale learning history, non-promotion of project/Agent/environment/project-specific findings, `MORE_EVIDENCE`/`NO_CHANGE`, ordinary ADS governance, privacy and hidden-evaluator boundaries.

Required Validation: classification/learning/privacy negative oracles. Fresh exact-HEAD Review required.