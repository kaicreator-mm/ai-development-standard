# v4.8.0 T-017 L3 — Execution Ownership Visibility / Start-Timeout Conformance

Status: **FINAL TASK-SCOPED L3 — JIT EXACT-BASE EXECUTION PACK REQUIRED**

Authority: Frozen Product blob `f26439580e00de6ed8b2e27d732a3095eb566219` + Frozen L2 blob `f88c85454e80101a0fdf56050e21f11a05279841` + Frozen Task DAG R2 commit `d2f18854043c59712c1c9d2518f45843b0ad129c` / blob `21d45c8d1a4ec94621eb8ca6051f21ece8227fdc` + T-017 Task Pack + native dependency readback #686.

This L3 is implementation guidance only. It cannot expand Product/L2/DAG authority, create a new event/lifecycle owner, weaken T-002 claim serialization, replace T-009 Interchange semantics, or manufacture Validation/Review truth.

## Tests

The focused conformance suite `scripts/test_v48_execution_ownership.py` must use explicit durable-fact scenarios and prove at least:

1. **claim-race-single-start** — two logical operators race the same `(work item, role)`; only one accepted `DISPATCH_CLAIMED` becomes the canonical Start Record and the loser cannot execute;
2. **projection-not-authority** — `state:implementing` label/comment/state-card projection without accepted Claim never authorizes execution;
3. **projection-publication-loss** — accepted Claim remains authoritative when current-state projection publication is delayed/failed; duplicate admission stays blocked by durable claim facts;
4. **restart-reconstruction** — active dispatch, actor role, `operator_kind`, `operator_id`, `session_ref` when present, accepted/start time, execution profile, exact/requested/base subject and pack refs reconstruct from durable facts after transient chat/session loss;
5. **idempotent-resume** — same logical operator reclaiming the same dispatch resumes the existing claim and does not create a second active claim/start;
6. **terminal-release-matrix** — `DONE`, `FAILED`, `BLOCKED`, `CANCELLED`, `TIMEOUT`, `STALE`/`SUPERSEDED` cannot leave incompatible active ownership once the durable terminal/release state is unambiguous;
7. **takeover-before-release-rejected** — another operator cannot take over while the prior claim/release outcome remains active or ambiguous;
8. **heartbeat-non-authority** — heartbeat/progress absence is neither Task/Validation FAIL nor implicit release and never mutates a Gate;
9. **timeout-fail-closed** — liveness expiry may initiate timeout/reconciliation but successor claim remains blocked until durable claim/publication/resource/generation/release facts reconcile;
10. **append-only-successor** — TIMEOUT/STALE history remains attributable and a later accepted successor Claim is a distinct durable start;
11. **historical-event-v2-compatible** — historical valid `DISPATCH_CLAIMED` payloads continue to satisfy the current event-v2 schema/compatibility boundary even when richer new-writer provenance is absent;
12. **enriched-new-writer-profile** — a representative new Claim uses existing event-v2 fields plus allowed extension provenance to make start reconstruction auditable without schema or event-family change;
13. **identity-not-labels** — dynamic operator/session identity is durable structured event data, not an unbounded label namespace;
14. **fast-path-proportional** — manual/Fast-Path single-writer execution uses the same accepted-Claim/start semantics without mandatory scheduler service or high-frequency heartbeat.

Regression commands:

```text
python -B scripts/test_v48_execution_ownership.py
python -B scripts/test_v48_execution_architecture.py
python -B scripts/test_v48_interchange_replay_restart.py
python -B scripts/verify_standard.py
```

## Contract

### 1. Start authority

The existing accepted `DISPATCH_CLAIMED` is the Start Record. No label, comment, transport ACK, progress message, heartbeat, state card or transient queue record can substitute for accepted Claim authority.

Authoritative execution/source mutation begins only after Claim admission succeeds under the existing T-002 serialization authority. Rejected/stale/duplicate admission means STOP/recompute.

### 2. New-writer start profile

`GITHUB_AGENT_INTERACTION_PROTOCOL.md` should define a bounded new-writer profile using existing event-v2 semantics. Where applicable/available the accepted Claim should expose:

```text
issue/task/work-item ref
dispatch_id
actor_role
operator_kind
operator_id
session_ref
occurred_at or accepted-time durable ref
execution_profile
sha / requested_head_sha / expected_base_sha as applicable
task_pack_ref / execution_pack_ref as applicable
admission_mode / protected_claim_key / claim_generation or revision when transport supports it
transport_actor when useful
```

The schema remains `ai-dev/event-v2`; no new event version/type is authorized. Optional transport-specific provenance may use the schema's existing additive-extension allowance. Historical claims are not retroactively invalidated for lacking later optional/richer fields.

### 3. Visible current-state projection

After accepted start, GitHub current workflow visibility resolves through `state:claimed → state:implementing` (or role-equivalent running state). This projection improves operator visibility but is not the lock. Dynamic operator/session identity remains in structured event facts.

Any state card/current metadata view may surface active dispatch/operator/since/exact subject only as `NON_AUTHORITATIVE_DERIVED_STATE` reconstructible from durable facts.

### 4. Release and replacement

Terminal/release semantics must make incompatible active ownership disappear only when durable facts make the release unambiguous. Historical claims remain append-oriented.

Same operator + same dispatch is idempotent resume. Different operator takeover requires durable terminal/stale/timeout/release/supersession facts and a fresh serialized admission. Ambiguous publication/release/resource state fails closed.

### 5. Progress, heartbeat and timeout

Progress/heartbeat remains optional transport/exchange data and non-authoritative. T-017 must not require periodic heartbeat for manual/Fast-Path execution.

A project/controller may use liveness expiry to initiate investigation or timeout handling, but missing heartbeat alone cannot produce Task/Validation FAIL, Gate mutation, or claim release. `TIMEOUT`/`STALE` replacement still reconciles the durable authority chain before any incompatible successor claim.

## Implementation

Authorized Builder changes are exactly:

1. `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`
   - add the new-writer accepted-Claim Start Record profile;
   - explicitly bind operator/session/start/exact subject reconstruction to durable structured events;
   - state that GitHub current-state labels/cards are derived visibility rather than claim lock;
   - state that historical event-v2 claims remain valid compatibility evidence.

2. `standards/EXECUTION_ARCHITECTURE_STANDARD.md`
   - add the smallest lifecycle clarification needed for active ownership projection, terminal release and timeout/stale replacement reconciliation;
   - preserve existing section 11 serialization/admission owner;
   - make heartbeat/progress non-authority explicit and keep Fast Path/manual proportionality;
   - do not create a second state dimension/lifecycle/database.

3. `scripts/test_v48_execution_ownership.py`
   - deterministic, self-contained conformance over durable facts and current standards/schema;
   - validate new-writer enriched Claim example and historical compatibility against `schemas/agent-event-v2.schema.json` without changing that schema;
   - inspect required normative invariants so documentation and executable oracle cannot silently diverge.

Implementation should reuse existing vocabulary (`DISPATCH_CLAIMED`, `CLAIMED`, `RUNNING`, `TIMEOUT`, `STALE`, `SUPERSEDED`, `state:claimed`, `state:implementing`, `SINGLE_WRITER_ADMISSION`, `LINEARIZABLE_CONDITIONAL_WRITE`). Do not add synonyms or a parallel ownership object.

## Failure Handling

- Need to modify `schemas/agent-event-v2.schema.json`, `schemas/dispatch.schema.json`, Interchange schema/profile, Product/L2/DAG or introduce a new event/state family → `ARCHITECTURE_AMENDMENT_REQUIRED`.
- Need a mandatory runtime database/service to prove ownership → `ARCHITECTURE_AMENDMENT_REQUIRED`.
- Label/comment/state-card used as lock or execution authorization → blocking conformance failure.
- Source mutation/execution before accepted Claim → blocking conformance failure.
- Duplicate accepted active claims for one incompatible `(work item, role)` → blocking T-002/T-017 failure; do not paper over with labels.
- Missing heartbeat treated as Task/Validation FAIL or implicit release → blocking authority violation.
- Timeout/stale successor admitted before durable ambiguity reconciliation → blocking fail-closed violation.
- Historical valid event-v2 claim rejected solely for lacking richer T-017 provenance → compatibility regression.
- Required independent exact-subject Validation unavailable → `BLOCKED` with explicit Validation handoff; never self-certify.
- Any material candidate change after qualifying Validation/Review → stale affected evidence and requalify.

## Evidence expectations

Builder closeout must record exact base, JIT Pack HEAD, candidate HEAD/tree, exact three-path implementation diff, focused/regression command results, and explicitly state Independent Validation/Fresh Review are not claimed.

Independent Validator must run/inspect the focused lifecycle matrix on the exact candidate and verify compatibility/currentness. After qualifying Validation, a genuinely Fresh Independent Reviewer must re-read the exact current PR HEAD and authority. Neither role may inherit the Builder's conclusion as truth.

## Reference

- Frozen Product: `docs/implementation/4.8.0/PRD.md` blob `f26439580e00de6ed8b2e27d732a3095eb566219`
- Frozen L2: `docs/implementation/4.8.0/L2_ARCHITECTURE_EVIDENCE.md` blob `f88c85454e80101a0fdf56050e21f11a05279841`
- Frozen DAG R2: `docs/implementation/4.8.0/TASK_DAG.md` blob `21d45c8d1a4ec94621eb8ca6051f21ece8227fdc`
- Task: #646 / T-017
- Native DAG proof: #686 PASS (`#646 blocked by #510/#515`; `#517` additionally blocked by #646)
- T-002 owner: `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §§6, 11, 11.1
- GitHub writer/operator owner: `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` §§5, 8, 12
- Event schema compatibility input: `schemas/agent-event-v2.schema.json`
- T-009 replay/restart regression: `scripts/test_v48_interchange_replay_restart.py`
- T-017 Task Pack: `docs/implementation/4.8.0/task-packs/T17_execution_ownership_visibility.md`
