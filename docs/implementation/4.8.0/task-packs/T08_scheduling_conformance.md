# T-008 Task Pack — Eligibility / Composite Resource Admission Conformance

Status: **CANDIDATE TASK PACK — NOT BUILDER READY**

Authority: Frozen DAG R1 blob `72dfeee93c092296004c7083b71fdd877d7f1b34`; Issue #514.

```yaml
task_id: T-008
dependencies: [T-002]
integration_target: version/v4.8.0
review_policy: required
validation_scope: concern
validation_owner: independent-from-builder
l3_requirement: reference
agent_freedom: F2
jit_branch: true
execution_pack: JIT
```

Allowed write set: deterministic eligibility/resource-admission tests and golden fixtures. Forbidden: scheduler semantic owner changes or trusting a novel distributed CAS/lease without separate Research Demo/Validation.

Acceptance: multiple READY tasks; heterogeneous Agents; fresh/stale Availability; independence conflict; hard-filter-before-ranking; capacity N and N=1; multi-resource composite admission; injected partial-write/crash ambiguity; fail-closed reconciliation.

Required Validation: deterministic race/capacity/crash/failure suite. Fresh exact-HEAD Review required.