# T-011 Orchestration Dogfood — Scenario / Evidence Matrix (ODF-01..ODF-20)

Task: T-011 / Issue #517 · lane `orchestration-dogfood` · target `version/v4.8.0`

## Identity binding

- Exact base SHA: `94955c6f93fd7316406ea96bce8f7c32a62509ef` (tree `bb7f25f1e05ff2423fc79029465bcf7be458a82c`)
- JIT Execution Pack HEAD: `26fdae3dd2b4a686820637665ee6f30811543b1f` (tree `dc2fafc5c1433db23423a49c22c0250a0adc88b6`)
- Task Pack blob: `e1c412c44f67df736d1b1598a590a0eac31a4b22` · L3 blob: `fe7e1c46bcaef45cb7c8ce57615dcf0f1e0feb1a`
- Candidate SHA/tree: bound at execution time by `scripts/test_v48_orchestration_dogfood.py` (it re-reads `git rev-parse HEAD` / `HEAD^{tree}` on the exact checkout) and bound durably in the repair terminal and PR head. A self-referential commit SHA cannot be embedded in a file inside that same commit.
- Corpus fixture: `fixtures/scenario_manifest.json` (corpus version **2**: Phase-5 bounded P1 repair — shadow capability authority removed, canonical-profile eligibility derivation; ODF-01..ODF-18 remain the Task Pack/L3 corpus, ODF-19/ODF-20 are the repair-contract negatives) · Claim fixture: `fixtures/t011_builder_claim_event.json`
- Harness: `python -B scripts/test_v48_orchestration_dogfood.py` (emits the per-run evidence JSON between `T011_ORCHESTRATION_DOGFOOD_EVIDENCE_JSON_BEGIN/END` markers)

## Evidence-class boundary

- `SYNTHETIC_DETERMINISTIC` rows prove only the bounded deterministic semantics exercised by the merged upstream reference oracles over committed corpus fixtures. They are **not** host, device, provider or runtime evidence.
- `REPOSITORY_REAL_EXECUTION` rows executed against real repository artifacts at the exact candidate checkout (real schemas, real durable facts, real git state). They are still **not** external-environment evidence.
- `REAL_HOST_OR_RUNTIME_VALIDATION` was **not executed** by the Builder and is not claimed anywhere in this matrix. Any external host/device/provider/runtime claim requires later independent exact-subject Validation; until then those dimensions remain `NOT_RUN`/`BLOCKED`.
- All measured values in this dogfood are **descriptive only**. They establish **no universal Agent ranking**, **no blanket strong-to-low-cost routing** and **no savings claim**. Ranking inputs in the corpus are the explicit rank tuples only; provider/model provenance is identity provenance, never authorization, correctness or quality authority.

## Scenario rows

### ODF-01 — multi-ready-heterogeneous-eligibility

- L3 tests: #1 · Evidence class: `SYNTHETIC_DETERMINISTIC` + `REPOSITORY_REAL_EXECUTION`
- Inputs: `fixtures/scenario_manifest.json` (3 READY work items, 3 heterogeneous profiles, fresh availability)
- Agent profiles: `strong_semantic_builder`, `bounded_test_builder`, `independent_reviewer_or_validator` (validated against real `agent-capability-profile-v1`); scheduling-side eligibility inputs derive only from the canonical documents (eligible-role claims, actually claimed capabilities, freedom ceiling) — no fixture-only shadow capability field exists (removed in corpus version 2)
- Expected oracle: only hard-eligible candidates reach ranking/admission; profile differences resolve through canonical capability/role/freedom semantics
- Observed: ELIGIBLE ×3 / INELIGIBLE ×2 across 5 profile/work pairs (the reviewer-work × builder-role pair is blocked by role and capability; all inputs canonical); ranking probe observed exactly the 3 eligible items; corpus profile documents validate against the real schema; oracle module is the merged upstream file
- Environment: local build host, exact candidate checkout · Validation: PENDING independent exact-subject Validation · Review: PENDING
- Limitations: proves the merged deterministic eligibility/ranking oracle only; no live dispatch-through-GitHub execution in this row

### ODF-02 — fresh-stale-availability

- L3 tests: #2 · Evidence class: `SYNTHETIC_DETERMINISTIC`
- Inputs: corpus availability facts `fresh_available` / `stale_available` / `missing` / `unavailable`
- Expected oracle: stale/missing material Availability → `UNKNOWN`, fail closed; no ranking override
- Observed: fresh → ELIGIBLE; stale (`current=false`) → UNKNOWN; missing → UNKNOWN; UNAVAILABLE → INELIGIBLE; stale+missing never reached the ranking probe even with maximal rank
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: reference-model Availability semantics only; no external availability feed involved

### ODF-03 — capacity-n-contention

- L3 tests: #3 · Evidence class: `SYNTHETIC_DETERMINISTIC` + `REPOSITORY_REAL_EXECUTION`
- Inputs: corpus `resource_capacities` (build-host-pool N=3) loaded from the real committed fixture file
- Expected oracle: accepted active units never exceed N; loser fails closed
- Observed: 2+1 units accepted; third contender `CAPACITY_EXCEEDED` with unchanged state; capacity invariant held at every canonical state
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: single-writer deterministic admission model already authorized by Frozen L2/T-002; no distributed scheduler was built or exercised

### ODF-04 — exclusive-resource-duplicate-assignment-race

- L3 tests: #4 + #6 · Evidence class: `SYNTHETIC_DETERMINISTIC` + `REPOSITORY_REAL_EXECUTION`
- Inputs: corpus `exclusive-device` (N=1), T-017 claim oracle, corpus ownership facts
- Expected oracle: at most one incompatible accepted admission/start; duplicate assignment fails closed
- Observed: N=1 admitted `owner-A` only; `incompatible-B` CAPACITY_EXCEEDED; re-admission of `owner-A` DUPLICATE; claim race admitted exactly one start, loser `DUPLICATE_CLAIM`
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: composed deterministic oracles; no real concurrent process contention was timed

### ODF-05 — independence-hard-filter

- L3 tests: #7 · Evidence class: `SYNTHETIC_DETERMINISTIC`
- Inputs: review work item + builder/reviewer profiles; `independence_ok=False`
- Expected oracle: conflicted reviewer/validator candidate rejected before optimization/ranking
- Observed: conflict → INELIGIBLE before the ranking probe ran, including with adversarial best rank `(-9999,…)`;
 unconflicted reviewer stayed eligible; self-reviewing validator rejected
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: independence modeled as explicit hard fact per Frozen semantics, not inferred

### ODF-06 — replay-same-identity-same-payload

- L3 tests: #8 · Evidence class: `SYNTHETIC_DETERMINISTIC`
- Inputs: in-memory deterministic deliveries built by the harness (existing `ai-dev/interchange-v1` envelope shape, `payload_ref event:t011-implementation-ready-1`)
- Expected oracle: same idempotency identity + same payload = safe replay, no duplicate authority
- Observed: `ACCEPTED` then `DUPLICATE_IDEMPOTENT`; exactly one durable effect materialized; workflow state reconstructed once
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: harness-built deliveries, not replayed production traffic

### ODF-07 — replay-same-identity-conflicting-payload

- L3 tests: #9 · Evidence class: `SYNTHETIC_DETERMINISTIC`
- Inputs: same exchange identity with conflicting payload (`next_state=merged`) and a digest-mismatch delivery
- Expected oracle: fail closed; never last-write-wins
- Observed: `CONFLICT_FAIL_CLOSED` on the conflicting replay (first materialization retained); `DIGEST_MISMATCH_FAIL_CLOSED` on the tampered delivery
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: reference replay oracle over harness-built deliveries

### ODF-08 — transport-loss-ack-progress

- L3 tests: #10 · Evidence class: `SYNTHETIC_DETERMINISTIC`
- Inputs: lost delivery, replay-after-loss, `DISPATCH_STATE_CHANGED` ACK durable fact, reordered delivery chronology
- Expected oracle: delivery facts never become workflow truth; durable owners are authoritative
- Observed: `LOST_NO_EFFECT` (nothing materialized); replay after loss accepted exactly once; ACK fact left workflow state unchanged; reversed chronology changed nothing
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: no real webhook/queue transport exercised (see NOT_RUN dimensions in RESULT_REPORT.md)

### ODF-09 — crash-restart-durable-reconstruction

- L3 tests: #11 · Evidence class: `REPOSITORY_REAL_EXECUTION`
- Inputs: real `fixtures/v48_interchange_replay/restart_durable_reconstruction.json`; real `.agent/execution/T-011/MANIFEST.yaml`
- Expected oracle: authoritative state reconstructs from durable facts only, without transient queue/chat history
- Observed: workflow state reconstructed with transient keys removed and with contradictory transient data injected; real T-011 manifest facts (base/pack refs/branch/write set) reconstructed after simulated session loss
- Environment: local build host, exact candidate checkout · Validation: PENDING · Review: PENDING
- Limitations: simulated controller/process loss inside one process; no actual host crash/reboot was performed (real host restart remains NOT_RUN)

### ODF-10 — accepted-claim-start-projection-loss-timeout-replacement

- L3 tests: #12 + #13 · Evidence class: `REPOSITORY_REAL_EXECUTION`
- Inputs: real `fixtures/t011_builder_claim_event.json` (verbatim copy of the accepted Builder Claim on #517) validated against the real `agent-event-v2` schema; merged T-017 ownership oracle
- Expected oracle: accepted Claim is the durable Start Record; projection is derived; ambiguous replacement blocks until durable reconciliation
- Observed: claim event validated + admitted as Start Record; projection loss authorized no duplicate; liveness expiry and ambiguous TIMEOUT release blocked the successor; reconciliation admitted the successor with append-only history
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: the durable original of the claim lives in the Issue comment; this row exercised a verbatim committed copy

### ODF-11 — bounded-executor-eligible-success

- L3 tests: #14 · Evidence class: `REPOSITORY_REAL_EXECUTION`
- Inputs: real `.agent/execution/T-011/MANIFEST.yaml` write set; real `git diff/status` of the candidate worktree vs JIT pack head `26fdae3dd2b4a686820637665ee6f30811543b1f`; corpus `bounded_test_builder` (F1) profile; corpus work-item freedom ceiling bound to the real manifest pack ceiling
- Expected oracle: bounded path may complete only within exact pack/write-set/authority constraints
- Observed: F1 executor hard-ELIGIBLE with eligibility derived from its canonical profile (role + claimed capability + freedom ceiling `freedom_le:F2` equal to the real manifest `task_pack_agent_freedom_ceiling`); an otherwise-identical F3-over-claim variant of the same document failed hard eligibility; real write-set verification over the candidate paths; every path inside `scripts/test_v48_orchestration_dogfood.py` + `docs/implementation/4.8.0/dogfood/orchestration/**`, none forbidden; 0 escalations
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: bounded action = write-set conformance verification; no provider-backed generation step was executed (provider claim remains NOT_RUN)

### ODF-12 — bounded-executor-semantic-ambiguity

- L3 tests: #15 · Evidence class: `REPOSITORY_REAL_EXECUTION`
- Inputs: stale pack blob probe, forbidden standards path probe, conflicting-replay probe; real `agent-event-v2` schema; `git hash-object` verification of `standards/EXECUTION_ARCHITECTURE_STANDARD.md`
- Expected oracle: ambiguity/missing authority → stop + durable escalation, never guess or self-elevate
- Observed: three `BLOCKER_REPORTED` escalation payloads validated against event-v2; standards file still hashes to its HEAD blob; no state mutation, no self-elevation
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: escalations were validated as durable event payloads; they were not delivered to a live GitHub Issue (transport delivery remains NOT_RUN)

### ODF-13 — task-pack-execution-pack-base-drift

- L3 tests: #16 · Evidence class: `SYNTHETIC_DETERMINISTIC`
- Inputs: corpus subject identities (current/stale/successor), real manifest base binding, generation drift probes
- Expected oracle: stale Task/Execution Pack/base cannot continue as current; must rebind/recompute
- Observed: stale exact subject rejected by the merged T-007 currentness oracle; stale-subject work INELIGIBLE; drifted manifest copy failed the exact-base bind; generation drift rejected `STALE`/`STALE_IDENTITY`
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: drift simulated by mutation, not by an actual repository rebinding event

### ODF-14 — evidence-classification-and-economic-boundary

- L3 tests: #17 + #18 · Evidence class: `SYNTHETIC_DETERMINISTIC` + `REPOSITORY_REAL_EXECUTION`
- Inputs: harness scenario registry; real profile schema; real committed `EVIDENCE_MATRIX.md` / `RESULT_REPORT.md`
- Expected oracle: every result carries an explicit evidence class; measurements stay descriptive; no universal ranking/routing/savings inference
- Observed: all registry rows carry explicit classes; no row claims `REAL_HOST_OR_RUNTIME_VALIDATION`; profile contract rejects injected authority fields; ranking followed corpus rank tuples only; boundary anchors present in the committed artifacts
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: this is a self-inspection of evidence discipline, not an external audit

### ODF-15 — composite-multi-resource-admission

- L3 tests: #5 · Evidence class: `SYNTHETIC_DETERMINISTIC` + `REPOSITORY_REAL_EXECUTION`
- Inputs: composite requirement (build-host-pool + review-quota + compatibility key `same-host`), failure-point injection
- Expected oracle: work claim + every required scarce-resource binding publishes all-or-none; no canonical partial state
- Observed: unsafe per-key modes `BLOCKED_UNSAFE_COMPOSITE_ADMISSION`; BEFORE_PUBLICATION published nothing; AT_PUBLICATION left no partial canonical state and blocked successors until `reconcile_no_accept`; AFTER_PUBLICATION kept the durable admission and blocked successors until `reconcile_accepted`
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: deterministic single-writer composite admission, not a distributed transaction coordinator

### ODF-16 — duplicate-assignment-race-granular

- L3 tests: #6 (granular across resource/claim/interchange layers) · Evidence class: `SYNTHETIC_DETERMINISTIC` + `REPOSITORY_REAL_EXECUTION`
- Inputs: corpus ownership identity facts + `exclusive-device` + `exchange:v48:t011:assign:1` deliveries
- Expected oracle: one canonical accepted admission/start; loser fails closed in every layer
- Observed: resource DUPLICATE; ownership exactly one start, racer rejected; interchange `ACCEPTED`/`DUPLICATE_IDEMPOTENT`/`CONFLICT_FAIL_CLOSED` with one materialized effect
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: three-layer composition of merged oracles; no real GitHub assignment mutation

### ODF-17 — t017-start-visibility-granular

- L3 tests: #12 (granular) · Evidence class: `REPOSITORY_REAL_EXECUTION`
- Inputs: real claim fixture; unpublished/fabricated projections
- Expected oracle: Start Record is the accepted Claim; projection is derived visibility; projection loss cannot authorize duplicate execution
- Observed: with the projection unpublished the durable claim still authorized exactly its own operator and reconstructed its view from durable facts; a fabricated transport label authorized nobody; derived label recomputed from the durable record
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: projection surfaces simulated in-memory (no real Project/board state consulted)

### ODF-18 — timeout-replacement-fail-closed-granular

- L3 tests: #13 (granular across claim/publication/resource surfaces) · Evidence class: `REPOSITORY_REAL_EXECUTION`
- Inputs: real claim fixture + liveness expiry + ambiguous TIMEOUT release + ambiguous resource publication
- Expected oracle: ambiguous active claim/publication/resource state blocks incompatible successor admission until durable reconciliation
- Observed: successor admission failed closed on both surfaces; claim-surface reconciliation alone kept the resource surface blocked; full durable reconciliation unlocked the successor
- Environment: local build host · Validation: PENDING · Review: PENDING
- Limitations: timeouts modeled via explicit liveness/ambiguity facts; no wall-clock timeout service was exercised

### ODF-19 — wrong-role-cannot-reach-ranking-or-admission

- L3 tests: Phase-5 P1 repair contract `#517@5966292564` (wrong-role negative) · Evidence class: `SYNTHETIC_DETERMINISTIC` + `REPOSITORY_REAL_EXECUTION`
- Inputs: in-memory schema-valid variant of the real `independent_reviewer_or_validator` capability profile document (identical canonical capability claims, `eligible_role_claims` narrowed to `builder`); corpus reviewer work item (`required_role_claim: reviewer`); merged T-008 hard-filter oracle
- Expected oracle: a candidate whose canonical profile does not claim the work's required role is hard-INELIGIBLE before ranking/admission, whatever its rank or capabilities
- Observed: builder-role-only impostor stayed INELIGIBLE for the reviewer work with adversarial best rank `(-9999,…)` although it canonically claimed `fresh-independent-review`; in a composed pool with a role-conforming control, only the control was ranked and admitted (`review-quota` consumed exactly once, impostor contributed nothing); the role-conforming control with identical capability claims resolved ELIGIBLE
- Environment: local build host · Validation: PENDING (successor exact-subject) · Review: PENDING (successor fresh review)
- Limitations: reference-model composition over a mutated copy of the real corpus document; no live dispatch was performed

### ODF-20 — unclaimed-capability-cannot-reach-ranking-or-admission

- L3 tests: Phase-5 P1 repair contract `#517@5966292564` (unclaimed-capability negative) · Evidence class: `SYNTHETIC_DETERMINISTIC` + `REPOSITORY_REAL_EXECUTION`
- Inputs: real committed corpus documents; the strong semantic builder's canonical profile (which does **not** claim `deterministic-harness-authoring`); corpus bounded-harness work item; merged T-008 hard-filter oracle
- Expected oracle: a capability not claimed in the canonical capability profile document cannot participate in hard eligibility; no non-canonical capability source exists
- Observed: the corpus carries no `scheduling_oracle_capabilities` shadow field (removed in corpus version 2); the strong semantic builder's canonical claims exclude `deterministic-harness-authoring`, so it stayed INELIGIBLE for the bounded-harness work (role and freedom both allow) with adversarial best rank; ranking probe never fired; the canonically-claiming bounded builder control resolved ELIGIBLE for the same work
- Environment: local build host · Validation: PENDING (successor exact-subject) · Review: PENDING (successor fresh review)
- Limitations: falsifies the exact shadow drift identified by the Phase-4 Fresh Review P1 over the committed corpus; proves no residual shadow authority participates in eligibility

## External dimensions — explicit posture

| Dimension | Class | Reason |
|---|---|---|
| Real host/runtime restart (OS-level crash/reboot) | `NOT_RUN` | requires independent exact-subject host Validation |
| Real GitHub transport delivery of escalation events | `NOT_RUN` | requires exact-subject transport Validation |
| Real provider-backed bounded-executor generation step | `NOT_RUN` | requires exact-subject provider Validation; no provider claim made |
| Real webhook/queue transport with loss/replay | `NOT_RUN` | reference-model replay oracle only |
| Economic/model-ranking claims | none made | measurements are descriptive only; **no universal Agent ranking**, **no blanket strong-to-low-cost routing**, **no savings claim** |

Validation status for every row: independent exact-subject scenario/integration Validation **PENDING** (`NOT_RUN` by this Builder; never self-certified). Fresh Independent Review: **PENDING**, permitted only after qualifying Validation.
