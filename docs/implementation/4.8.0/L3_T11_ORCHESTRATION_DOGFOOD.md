# v4.8.0 T-011 L3 — Heterogeneous Multi-Agent / Resource / Transport Dogfood

Status: **FINAL TASK-SCOPED L3 — JIT EXACT-BASE EXECUTION PACK REQUIRED**

Authority: Frozen Product blob `f26439580e00de6ed8b2e27d732a3095eb566219` + Frozen L2 blob `f88c85454e80101a0fdf56050e21f11a05279841` + Frozen Task DAG R2 commit `d2f18854043c59712c1c9d2518f45843b0ad129c` / blob `21d45c8d1a4ec94621eb8ca6051f21ece8227fdc` + T-011 Task Pack + native #517 dependency readback.

This L3 is dogfood implementation guidance only. It cannot expand Product/L2/DAG authority, repair upstream normative semantics, create a new scheduler/transport/authority family, or manufacture real-host/provider/runtime Validation.

## Tests

The focused dogfood harness `scripts/test_v48_orchestration_dogfood.py` must assemble one deterministic scenario corpus from already-merged v4.8 semantics and prove at least:

1. **multi-ready-heterogeneous-eligibility** — two or more READY work items and materially different logical Agent profiles resolve only through hard eligibility before optional ranking;
2. **fresh-stale-availability** — fresh required facts may satisfy eligibility; stale/missing material facts become `UNKNOWN` and fail closed;
3. **capacity-n-contention** — concurrent contenders for capacity-N resources never produce more active accepted units than N;
4. **exclusive-resource-race** — N=1 exclusive contention admits at most one incompatible owner;
5. **composite-multi-resource-admission** — work claim plus every required scarce-resource binding publishes all-or-none; no canonical partial state;
6. **duplicate-assignment-race** — duplicate/incompatible assignment attempts produce one canonical accepted admission/start and fail closed for the loser;
7. **independence-hard-filter** — Builder/Reviewer/Validator independence conflict is rejected before ranking and cannot be optimized around;
8. **duplicate-replay-idempotent** — same Interchange/idempotency identity with the same payload is safe replay and does not duplicate semantic authority;
9. **conflicting-replay-fail-closed** — same identity with conflicting payload/digest is rejected rather than last-write-wins;
10. **delivery-loss-ack-non-authority** — loss/delay/retry/ACK/progress changes delivery facts only; authoritative workflow truth comes from durable owners;
11. **restart-durable-reconstruction** — after simulated controller/process/chat loss, READY/claim/resource/start/current durable state reconstructs without transient queue history;
12. **t017-start-visibility** — accepted Claim is the durable Start Record; current-state projection is derived visibility only; projection loss cannot authorize duplicate execution;
13. **timeout-replacement-fail-closed** — ambiguous active claim/publication/resource state blocks incompatible successor admission until durable reconciliation;
14. **bounded-executor-eligible-success** — a bounded executor may complete a bounded dogfood sub-action only when exact Task/Execution Pack, write set, authority and eligibility constraints permit it;
15. **bounded-executor-ambiguity-escalation** — semantic ambiguity, missing authority/currentness or freedom ceiling requires stop/escalation rather than guessing or self-elevation;
16. **task-base-currentness-drift** — stale Task Pack/Execution Pack/base cannot continue as current and must rebind/recompute;
17. **evidence-classification** — each result is explicitly classified as `SYNTHETIC_DETERMINISTIC`, `REPOSITORY_REAL_EXECUTION`, `REAL_HOST_OR_RUNTIME_VALIDATION`, `NOT_RUN` or `BLOCKED`;
18. **no-economic-universal-inference** — dogfood measurements remain descriptive and cannot establish universal Agent ranking, blanket strong→low-cost routing or savings without comparable measured methodology.

Required regression commands on the eventual Builder candidate:

```text
python -B scripts/test_v48_orchestration_dogfood.py
python -B scripts/test_v48_contract_conformance.py
python -B scripts/test_v48_scheduling_conformance.py
python -B scripts/test_v48_interchange_replay_restart.py
python -B scripts/test_v48_execution_ownership.py
python -B scripts/verify_standard.py
```

If an upstream command name has changed on the exact base, the Builder may use the canonical merged successor command only after recording the exact current path; do not silently substitute unrelated coverage.

## Contract

### 1. Scenario corpus is evidence, not new authority

The dogfood corpus may compose existing v4.8 Task contracts, fixtures and durable facts. It must not redefine Logical Agent Profile, Capability Evidence, Availability, eligibility, resource admission, Interchange, Claim/Start Record, Review or Validation semantics.

A failing scenario is evidence against the current design/implementation. It is not permission for T-011 to patch normative standards or schemas. Any required semantic/public-contract repair routes to `ARCHITECTURE_AMENDMENT_REQUIRED` or a separately authorized bounded repair.

### 2. Heterogeneous logical Agents

At least three materially distinct logical profiles should appear in the deterministic corpus, for example:

```text
strong_semantic_builder
bounded_test_builder
independent_reviewer_or_validator
```

Differences must be expressed through canonical capability/role/freedom/evidence/reference semantics, not provider prestige or a scalar quality score. Provider/model names, when present, are provenance only.

### 3. READY + eligibility + ranking

The corpus must contain multiple simultaneously READY work items and enough candidate/resource facts to produce `ELIGIBLE`, `INELIGIBLE` and `UNKNOWN` outcomes. Hard predicates are evaluated before ranking. Optional ranking may reorder only ELIGIBLE choices.

### 4. Resource admission

Use the Frozen L2/T-002 composite invariant: work claim plus every required scarce-resource/capacity binding shares one all-or-none admission point. Capacity-N must remain within N at every accepted canonical state. Exclusive resource is N=1. Independent per-key success never proves composite admission.

T-011 need not build a production scheduler or distributed transaction system. Deterministic/reference execution may model the conforming single-writer/linearizable behavior already authorized. A novel distributed mechanism requires separate proof and is outside this Task.

### 5. Transport replay/loss

Reuse the existing Interchange v1 owner/family and GitHub `ai-dev:event:v2` writer/admission boundary. Duplicate/replay/loss/conflict scenarios test correlation/idempotency/durable materialization only. Transport ACK/progress/heartbeat remains non-authoritative.

### 6. T-017 execution ownership

A role begins authoritative execution only after accepted Claim. The accepted Claim is the Start Record. `state:claimed`/`state:implementing` or equivalent current-state projection is visible derived state, not the lock. Ambiguous timeout/stale/replacement fails closed until durable reconciliation.

### 7. Bounded executor / escalation

The corpus must demonstrate both sides:

- an eligible bounded executor can perform a bounded, exact-pack, exact-write-set action without unnecessary strong-agent escalation;
- when semantics, authority, currentness, independence, required evidence or agent-freedom constraints are ambiguous/unsatisfied, that executor stops and emits a durable escalation/blocker rather than self-authorizing.

This is dogfood of the Frozen model, not evidence for a blanket low-cost routing rule.

## Implementation

Authorized Builder changes are exactly:

1. `scripts/test_v48_orchestration_dogfood.py`
   - deterministic scenario harness/oracle over current repository semantics;
   - no network/provider dependency required for synthetic/repository-real cases;
   - must emit or make auditable per-scenario evidence classification and outcome.

2. `docs/implementation/4.8.0/dogfood/orchestration/**`
   - bounded scenario fixtures, expected-results/evidence matrix and dogfood result report;
   - may reference existing upstream evidence rather than copying large bodies;
   - must explicitly separate synthetic/repository-real/external-real/NOT_RUN/BLOCKED dimensions.

Normative standards and schemas are read-only. If the harness needs a normative semantic change to pass, stop rather than edit authority.

## Failure Handling

- Need to change Frozen Product/L2/DAG or normative scheduling/Interchange/Claim semantics → `ARCHITECTURE_AMENDMENT_REQUIRED` or separately authorized repair; T-011 stops.
- Need a fourth machine family, new Availability authority, new Exchange family, second scheduler/claim lifecycle or new mandatory runtime database → `ARCHITECTURE_AMENDMENT_REQUIRED`.
- Hard-ineligible/UNKNOWN candidate reaches ranking/admission → blocking dogfood failure.
- Capacity-N exceeded, exclusive N=1 double-admitted, or canonical partial resource/work state observed → blocking dogfood failure.
- Independence conflict optimized around → blocking authority failure.
- Same idempotency identity + conflicting payload accepted → blocking replay failure.
- Transport ACK/progress/heartbeat treated as semantic completion/authority → blocking authority failure.
- Duplicate incompatible accepted Start Records or execution before accepted Claim → blocking T-017 composition failure.
- Crash/restart reconstruction requires private chat/transient queue history → blocking durability failure.
- Ambiguous timeout/stale state permits replacement admission → blocking fail-closed failure.
- Bounded executor guesses across missing authority/semantic ambiguity → blocking escalation failure.
- Synthetic/repository evidence relabeled as external real-host/provider/runtime evidence → blocking evidence-integrity failure.
- Required external claim cannot be executed independently → `NOT_RUN`/`BLOCKED` + exact-subject Validation handoff; never self-certify.
- Any material candidate drift after Validation/Review → stale affected evidence and requalify.

## Evidence matrix

Builder output must include one row per ODF-01..ODF-18 with at least:

```text
scenario_id
exact_candidate_sha/tree
exact_base_sha/tree
input_fixture_or_durable_fact_refs
agent_profile_refs
availability/resource refs
admission/dispatch/claim refs where applicable
transport/interchange refs where applicable
expected_oracle
observed_result
evidence_class
execution_environment
validation_ref_or_NOT_RUN/BLOCKED
review_ref_or_PENDING
limitations/counterevidence
```

No row may imply external-provider/host/device truth from a deterministic reference model.

## Evidence expectations

Builder closeout must record exact base, JIT Pack HEAD/tree, candidate HEAD/tree, exact authorized diff, scenario matrix results, focused/upstream/regression commands and the synthetic-vs-real evidence boundary. It must state independent Validation and Fresh Review are not self-claimed.

Independent Validator must inspect/run the exact candidate scenario corpus and independently verify repository-real claims. External host/device/provider/runtime claims require exact-subject environment-specific Validation or remain `NOT_RUN/BLOCKED`. After qualifying Validation, a genuinely Fresh Independent Reviewer re-reads the exact current PR HEAD and authority.

## Reference

- Frozen Product: `docs/implementation/4.8.0/PRD.md` blob `f26439580e00de6ed8b2e27d732a3095eb566219`
- Frozen L2: `docs/implementation/4.8.0/L2_ARCHITECTURE_EVIDENCE.md` blob `f88c85454e80101a0fdf56050e21f11a05279841`
- Frozen DAG R2: `docs/implementation/4.8.0/TASK_DAG.md` blob `21d45c8d1a4ec94621eb8ca6051f21ece8227fdc`
- Task: #517 / T-011
- Upstream tasks: T-007/#513, T-008/#514, T-009/#515, T-017/#646
- T-011 Task Pack: `docs/implementation/4.8.0/task-packs/T11_orchestration_dogfood.md`
