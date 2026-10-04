# T-017 Execution Contract

Exact base: `version/v4.8.0@d2f18854043c59712c1c9d2518f45843b0ad129c` / tree `22d5c97942df51a1b22faedd2c267b3f9d6039e0`.

Authority: Frozen Product/L2/DAG R2 > T-017 Task Pack > task-scoped T-017 L3 > this exact-base contract. T-002 remains the Claim/admission owner; T-009 remains the replay/restart/Interchange conformance predecessor. This pack grants `F2_ENGINEERING_DISCRETION` only inside the exact write set below.

## Builder write set

The exact implementation write set is:

- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md`
- `scripts/test_v48_execution_ownership.py`

The six `.agent/execution/T-017/**` artifacts, T-017 Task Pack and T-017 L3 are planning authority and read-only to the implementation Builder. `schemas/agent-event-v2.schema.json`, Dispatch/Interchange schemas, Product/L2/DAG, templates, workflows and predecessor tests are not writable.

## Contract kernel

1. **NO_CLAIM_NO_EXECUTION** — authoritative role execution and implementation-source mutation begin only after the existing dispatch Claim is accepted. Rejected/stale/duplicate Claim means STOP/recompute.
2. **Accepted Claim is Start Record** — the accepted `DISPATCH_CLAIMED` is the durable start fact; labels/comments/state cards cannot substitute for it.
3. **Auditable new-writer profile** — use existing event-v2 semantics/fields to bind dispatch/work item, role, logical operator, optional session, accepted/start time reference, execution profile, exact/requested/base identity, Task/Execution Pack refs and, when supported, admission mode/protected key/generation provenance. No schema/event-family change is authorized.
4. **Historical compatibility** — valid historical event-v2 claims remain valid history when richer optional T-017 provenance is absent.
5. **Derived visibility** — accepted start visibly resolves through `state:claimed → state:implementing` or role-equivalent running state, but current metadata/state-card projection is not the lock.
6. **Projection failure is fail-closed** — delayed/failed projection publication cannot erase the accepted Claim or permit a duplicate incompatible Claim.
7. **Identity minimization** — dynamic `operator_id`/`session_ref` belongs in structured event facts, not proliferating labels.
8. **Idempotent resume** — same logical operator + same dispatch resumes the existing accepted Claim and never creates another active Claim/Start Record.
9. **Terminal ownership release** — `DONE`, `FAILED`, `BLOCKED`, `CANCELLED`, `TIMEOUT`, `STALE`/`SUPERSEDED` must not leave incompatible active ownership once durable release state is unambiguous; history remains append-oriented.
10. **Replacement admission** — another operator may take over only after durable terminal/stale/timeout/release/supersession and related publication/resource/generation facts reconcile under existing serialized admission.
11. **Heartbeat/progress non-authority** — optional progress/heartbeat never becomes Task/Validation/Gate truth. Missing heartbeat alone cannot fabricate failure or release.
12. **Timeout fail-closed** — liveness expiry may trigger investigation/timeout policy, but an ambiguous prior Claim remains blocking until durable reconciliation; successor start is separately attributable.
13. **Fast Path proportionality** — manual/Fast-Path work may use the same accepted-Claim/visibility semantics without mandatory scheduler service or high-frequency heartbeat.

If any acceptance criterion requires a new event type/version, schema incompatibility, second lifecycle/state owner, mandatory runtime database/service, or Frozen Product/L2 expansion, STOP with `ARCHITECTURE_AMENDMENT_REQUIRED`; do not broaden this Task.

## Evidence and gates

Builder evidence must bind exact base, Pack HEAD, candidate HEAD/tree and prove the implementation diff is exactly the three authorized paths. Required commands:

```text
python -B scripts/test_v48_execution_ownership.py
python -B scripts/test_v48_execution_architecture.py
python -B scripts/test_v48_interchange_replay_restart.py
python -B scripts/verify_standard.py
```

Independent exact-subject concern Validation is required. Only after qualifying Validation may a genuinely Fresh Independent Review assess the exact current PR HEAD. Builder evidence is not independent Validation or Review truth.
