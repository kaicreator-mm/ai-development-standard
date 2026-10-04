# T-017 Task Pack — Execution Ownership Visibility / Start-Timeout Conformance

Status: **FINAL TASK PACK — JIT EXECUTION PACK REQUIRED**

Authority: Frozen Product blob `f26439580e00de6ed8b2e27d732a3095eb566219`; Frozen L2 blob `f88c85454e80101a0fdf56050e21f11a05279841`; Frozen Task DAG R2 commit `d2f18854043c59712c1c9d2518f45843b0ad129c` / blob `21d45c8d1a4ec94621eb8ca6051f21ece8227fdc`; native DAG readback #686 PASS; Issue #646.

```yaml
task_id: T-017
lane: execution-ownership-conformance
dependencies: [T-002, T-009]
integration_target: version/v4.8.0
review_policy: required
validation_scope: concern
validation_owner: independent-from-builder
l3_requirement: risk-scaled
agent_freedom_ceiling: F2_ENGINEERING_DISCRETION
jit_branch: true
execution_pack: JIT
```

## Scope

T-017 owns one bounded concern over the **existing** READY / Dispatch / Claim lifecycle: make authoritative execution start, current active ownership, terminal release and timeout/stale replacement behavior reconstructible and operator-visible without creating another admission authority, lifecycle, event family, scheduler or mandatory runtime database.

The existing accepted `DISPATCH_CLAIMED` / current accepted Claim remains the durable Start Record. GitHub labels/current metadata are a visibility/routing projection only; they are never the lock. `PROGRESS` / `HEARTBEAT` remains non-authoritative transport/exchange information.

T-017 MUST preserve:

- T-002 claim serialization and composite admission authority;
- T-009 Interchange replay/restart and durable-materialization boundaries;
- historical `ai-dev:event:v2` compatibility;
- the existing workflow/dispatch vocabularies;
- Fast Path proportionality and manual `SINGLE_WRITER_ADMISSION` compatibility.

## Builder write set

The exact JIT Execution Pack may narrow this Task Pack but MUST NOT broaden it. Authorized implementation paths are:

- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md`
- `scripts/test_v48_execution_ownership.py`

No schema mutation is authorized. In particular, `schemas/agent-event-v2.schema.json`, `schemas/dispatch.schema.json`, Interchange schemas, Product/L2/DAG authority, templates, CI/workflows and T-002/T-009 implementation/tests are read-only inputs for this Task.

If implementation proves that a schema change, new event type, new lifecycle/state owner, incompatible event-v2 requirement, mandatory runtime database or Product/L2 semantic expansion is necessary, STOP with `ARCHITECTURE_AMENDMENT_REQUIRED`; do not widen the Task.

## Contract kernel

### Accepted Claim is the Start Record

A Builder/Reviewer/Validator MUST NOT begin authoritative role execution or mutate implementation source before its dispatch claim is canonically accepted. A rejected, stale or duplicate claim means STOP/recompute.

New-writer guidance for an accepted `DISPATCH_CLAIMED` MUST make the start auditable using existing event-v2 fields where applicable:

```text
work item / dispatch identity
actor_role
operator_kind + operator_id
session_ref when available
occurred_at / accepted-time reference
execution_profile
exact/requested/base identity as applicable
Task Pack / Execution Pack refs when applicable
admission mode / protected claim key / generation provenance when transport supports it
```

Historical event-v2 claims remain valid history when they satisfied the authority in force when written; richer writer guidance MUST NOT retroactively invalidate them.

### Visible current-state projection

Accepted start must visibly resolve through `state:claimed → state:implementing` or the canonical role-equivalent running state. A label/comment/state-card entry without an accepted Claim cannot authorize execution. Dynamic operator/session identity stays in structured durable event data rather than proliferating labels.

A current-state/state-card projection may expose active dispatch/operator/since/exact subject only when those values are derived from durable facts and can be reconstructed after chat/session loss.

### Terminal ownership release

`DONE`, `FAILED`, `BLOCKED`, `CANCELLED`, `TIMEOUT`, `STALE` / `SUPERSEDED` must leave no ambiguous incompatible active ownership. Historical claim/start facts remain append-oriented. Same logical operator + same dispatch resume is idempotent and must not create another active claim.

A different operator may take over only after durable terminal/stale/timeout/release/supersession facts make replacement admission unambiguous under the existing claim-serialization authority.

### Progress / heartbeat / timeout

Progress/heartbeat is optional and non-authoritative. No high-frequency heartbeat requirement is introduced for manual/Fast-Path work.

Missing heartbeat may trigger a liveness investigation or an explicitly configured timeout policy, but heartbeat absence alone MUST NOT fabricate Task/Validation `FAIL`, mutate a Gate, or silently release an ambiguous active claim. Replacement after `TIMEOUT`/`STALE` still requires durable reconciliation of claim/publication/resource/generation/release facts and must fail closed on ambiguity.

## Required conformance / negative oracles

At minimum prove:

1. two logical operators race the same `(work item, role)` and only one canonical accepted Claim/Start Record exists;
2. `state:implementing` label/comment without accepted Claim cannot authorize execution;
3. accepted claim plus delayed/failed projection publication remains the canonical start and cannot permit a duplicate claim;
4. operator/session/start time/dispatch/exact subject reconstruct from durable facts after chat/session loss;
5. same operator + same dispatch reclaim/resume is idempotent;
6. another operator cannot take over before durable terminal/stale/timeout/release conditions permit it;
7. `DONE`/`FAILED`/`BLOCKED`/`CANCELLED`/`TIMEOUT`/`STALE|SUPERSEDED` clear incompatible active ownership without erasing history;
8. lost heartbeat is not Validation FAIL, Task FAIL or an implicit release;
9. timeout/stale history is append-only and successor claim/start is separately attributable;
10. historical event-v2 claim fixtures remain accepted under existing compatibility authority;
11. operator/session identity is recoverable from durable event facts and is not encoded as unbounded labels;
12. Fast Path/manual execution can use the same Claim/visibility semantics without a mandatory orchestration service;
13. no new lifecycle/event family/schema authority/runtime database is introduced.

## Required gates

Builder evidence MUST bind exact candidate SHA/tree and exact base, prove the implementation diff is exactly the three authorized paths, and run at minimum:

```text
python -B scripts/test_v48_execution_ownership.py
python -B scripts/test_v48_execution_architecture.py
python -B scripts/test_v48_interchange_replay_restart.py
python -B scripts/verify_standard.py
```

The focused T-017 suite MUST exercise positive and negative lifecycle/restart/timeout compatibility behavior and validate both an enriched new-writer Claim example and historical event-v2 compatibility without changing the schema.

Required Validation is independent exact-subject concern Validation over claim race/start reconstruction/projection failure/terminal release/heartbeat-timeout/replacement behavior and compatibility. Only after qualifying Validation may a genuinely Fresh Independent Review assess the exact current PR HEAD. Builder, Validator and Reviewer identities remain distinct.

PR/Task PASS does not imply T-011 dogfood, Version Closure or Release Qualification.
