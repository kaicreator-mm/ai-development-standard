# T-007 Task Pack — Contract / Historical Compatibility Conformance

Status: **CANDIDATE TASK PACK — NOT BUILDER READY**

Authority: Frozen DAG R1 blob `72dfeee93c092296004c7083b71fdd877d7f1b34`; Issue #513.

```yaml
task_id: T-007
dependencies: [T-001, T-015, T-016]
integration_target: version/v4.8.0
review_policy: required
validation_scope: concern
validation_owner: independent-from-builder
l3_requirement: reference
agent_freedom: F2
jit_branch: true
execution_pack: JIT
```

Allowed write set: integrated v4.8 compatibility tests/golden fixtures only. Forbidden: contract semantic changes, Execution Architecture semantics, owner reassignment.

Acceptance: reject claim→proof, Capability Evidence→current PASS, provider/model→authority, infrastructure-owner capture, fourth Availability/Exchange family, stale evidence rebinding, and private-CoT requirements; preserve historical v4 payload compatibility required by Frozen L2.

Required Validation: schema/historical compatibility suite + negative-oracle coverage. Fresh exact-HEAD Review required.