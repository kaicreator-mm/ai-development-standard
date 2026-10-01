# T-002 Task Pack — Execution Architecture Core

Status: **CANDIDATE TASK PACK — NOT BUILDER READY**

Authority: Frozen DAG R1 blob `72dfeee93c092296004c7083b71fdd877d7f1b34`; Frozen L2 `f88c85454e80101a0fdf56050e21f11a05279841`; Issue #510.

```yaml
task_id: T-002
dependencies: [T-001, T-015, T-016]
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
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md`
- directly related backward-compatible Task/Execution Pack/Dispatch semantics
- focused v4.8 execution-architecture tests

## Forbidden scope
Second scheduler lifecycle/database, durable Availability owner, new Exchange family, treating independent per-key reservations as composite atomicity.

## Acceptance
1. Compose logical Agent + runner/environment owner facts + derived Availability + Capability Evidence.
2. Eligibility is derived `ELIGIBLE|INELIGIBLE|UNKNOWN`; hard authority/currentness/independence/security/resource filters precede ranking.
3. READY/Dispatch/Claim remain canonical.
4. Work claim plus every required resource/capacity binding has one all-or-none linearization point.
5. Capacity N cannot over-allocate; crash/publication ambiguity fails closed and reconciles before replacement admission.

Required Validation: semantic regression + deterministic contention/capacity/crash cases + backward compatibility. Fresh exact-HEAD Review required.