# T-015 Task Pack — Logical Agent Capability Profile Contract

Status: **CANDIDATE TASK PACK — NOT BUILDER READY**

Authority: Frozen DAG R1 `634dd746cd16da970bb01822a1b6c59714c52429` / `72dfeee93c092296004c7083b71fdd877d7f1b34`; Frozen L2 `f88c85454e80101a0fdf56050e21f11a05279841`; Issue #522.

```yaml
task_id: T-015
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
- `schemas/agent-capability-profile-v1.schema.json`
- focused profile fixtures/tests
- T-015 reference material

## Forbidden scope
Runner/host/device inventory ownership, current Availability authority, Capability Evidence schema, global scalar Agent score.

## Acceptance
1. Profile contains logical Agent/operator/model execution claims only.
2. OS/toolchain/device/resource/network/concurrency facts remain references to existing infrastructure owners.
3. Provider/model identity is provenance, not correctness/routing authority.
4. Skill Metadata is procedure metadata, not capability proof.
5. Tool/credential possession never grants side-effect authority.

Required Validation: schema + owner-boundary negatives + v4.6 Skill/runner non-duplication. Fresh exact-HEAD Review required.