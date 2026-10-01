# T-003 Task Pack — Existing Interchange v1 Profile / Adapter Mapping

Status: **CANDIDATE TASK PACK — NOT BUILDER READY**

Authority: Frozen DAG R1 blob `72dfeee93c092296004c7083b71fdd877d7f1b34`; Frozen L2 `f88c85454e80101a0fdf56050e21f11a05279841`; Issue #508.

```yaml
task_id: T-003
dependencies: [T-015]
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
- existing `interchange-envelope-v1` schema only if a concrete compatible field/ref gap is proven
- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` adapter mapping where required
- focused protocol compatibility tests/reference material

## Forbidden scope
New Agent Exchange owner/family, replacement envelope family, event-v2 semantic replacement, ACK/progress as workflow truth.

## Acceptance
1. First prove a concrete gap; `NO_CHANGE_REQUIRED` is valid.
2. Reuse existing Interchange v1 owner/family; only compatible extension/profile/same-family versioning is allowed.
3. `ai-dev:event:v2` remains GitHub writer/admission authority.
4. Replay/conflict/currentness/durable materialization/restart preserve historical compatibility.
5. Receiver capability refs bind canonical T-015 rather than an ad-hoc shape.

Required Validation: protocol/schema/event compatibility and exact gap evidence if mutation occurs. Fresh exact-HEAD Review required.