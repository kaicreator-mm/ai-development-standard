# Proportional Orchestration Reference

Normative owner: `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §29 (v4.9 proportional orchestration core). This reference is implementation guidance only. It creates no authority, no lifecycle, no scheduler, and no state store; every semantic rule lives in the owner standard or the consumed contracts it cites.

## 1. What this reference covers

```text
reducer state model                 deterministic projection over durable facts
JIT phase predicate evaluation      fixed input order and verdict mapping (§29.2)
currentness recheck points          Dispatch / Claim / merge / Freeze / RQ (§29.1)
drift and recompute model           pure-function recompute, no stale latch (§29.6)
WAITING_LINEAGE projection rules    derived, non-dispatch, reason-bound (§29.3)
carry-forward reducer behavior      durable unresolved-finding set (§29.5)
no-review-shopping routing          fail-closed re-review preconditions (§29.5)
owner boundaries                    consumed contracts and forbidden over-claims
```

## 2. Reducer state model

The reducer is a pure function `reduce(facts) -> projection`. Durable facts are the only inputs; the projection is the only output; no mutable latch, session memory, or scheduler cache participates.

```text
facts (durable, GitHub/repository/evidence)
  work_item        id, native dependencies[], workflow state
  lineage_refs[]   required predecessor-owned surfaces with exact ref + currentness
  plan_binding     assurance-plan currentness_binding (state + digests, schema
                   assurance-plan-v2.schema.json)
  phases[]         JIT phase candidates with declared source (plan activity | pack declaration)
  candidates[]     (work, role, executor) choices with hard-predicate inputs
  findings[]       unresolved adverse findings + digest; verdict chronology

projection (derived, recomputable, NON_AUTHORITATIVE)
  ready_sets       builder/reviewer/validator/merge ready choices (§6, §27.2)
  jit_verdicts     per phase: READY | WAITING_LINEAGE | BLOCKED (§29.2)
  waiting_lineage  reason-bound derived wait posture (§29.3)
  plan_currentness CURRENT | STALE | UNKNOWN (owner: ASSURANCE_PLAN_STANDARD §12)
  unresolved_set   carried adverse findings (owner: Adversarial Review aggregation)
  claim_decisions  accepted/rejected canonical claims under §11/§11.1/§27.3 serialization
```

Same facts in, same projection out — at any time, on any host, after any crash. The projection can be deleted and rebuilt at zero authority cost (§4.2 of the owner standard).

## 3. JIT phase predicate evaluation order

Evaluate in fixed order; first non-passing gate decides the verdict (§29.2):

```text
1. P1 dependencies       any native dependency not DONE            -> BLOCKED (known-illegal now)
                          any dependency state unknown             -> WAITING_LINEAGE
2. P2 lineage            any required predecessor surface stale    -> WAITING_LINEAGE (reason-bound)
                          any required predecessor surface unknown -> WAITING_LINEAGE
3. envelope              phase not proven in-envelope (E1/E2 absent, or any of the four
                         envelope conditions unprovable)          -> BLOCKED
4. P3 admission          §27 composite admission unavailable      -> BLOCKED
                          §27 composite admission fails            -> BLOCKED
all pass                                                            -> READY
```

Order matters for the negative oracles: a phase with satisfied dependencies but stale lineage is `WAITING_LINEAGE`, never READY and never a guaranteed-BLOCKED dispatch; a phase with current lineage but no in-envelope proof is `BLOCKED`, never "temporarily in-envelope".

In-envelope proofs: `E1` the phase is a required/recommended activity of the current Assurance Plan (consumed by exact ref), or `E2` current Task Pack / Execution Pack authority explicitly declares it. Envelope conditions: no new semantic concern, no ownership change, no dependency-semantics change, no write/acceptance scope widening — each must be provable, not merely unrefuted.

Material topology change is never a phase: new semantic Task => `ADD`; new/removed blocked-by edge => `ADD_DEPENDENCY`/`REMOVE_DEPENDENCY`; split/merge/supersede/lane/owner => the corresponding v4.3 mutation class, with canonical mutation evidence before native mutation.

## 4. Currentness recheck points

Every architecture-owned authority transition re-verifies `currentness_binding.state` immediately before acting (§29.1):

```text
Dispatch reservation/materialization   STALE/UNKNOWN => no dispatch; recompute or BLOCKED
Claim admission (§11 re-read)          STALE/UNKNOWN => admission fails/recomputes;
                                       a new adverse finding after Dispatch prevents Claim
merge / merge-ready (§14)              STALE/UNKNOWN => no merge; recompute or BLOCKED
Candidate Freeze (§15)                 owner transition; STALE/UNKNOWN => no freeze
Release Qualification (§17)            owner transition; STALE/UNKNOWN => no qualification
```

Bound dimensions (owner contract §12, schema `currentness_binding`): subject identity, owner-authority refs + digest, proof-input refs + digest, Task Pack ref + digest, release-decision refs + digest, unresolved-finding refs + digest, final `binding_digest`. Any drift => `STALE`; missing/ambiguous => `UNKNOWN`; neither authorizes anything. An empty set is still bound by its digest — omission is not emptiness.

## 5. Drift and recompute model

```text
drift detected at a recompute point
  -> rebuild the affected projection entries from current durable facts
  -> cached prior values (plan CURRENT, phase READY, precondition pass) have zero weight
  -> recompute converges to the same state the fact plane determines; replay after
     crash/restart reaches the identical state
```

Concurrent claim versus drift (§29.6): under §11.1 serialization, at most one admission linearizes against still-current predicates; competitors observing drifted/claimed state are atomically rejected as duplicate/stale; an admission racing a drift publishes no canonical claim and no partial state. Legal outcomes are exactly: one accepted claim, or zero accepted claims with recompute/`BLOCKED`. Never both-claim; never silently lost claim.

## 6. WAITING_LINEAGE projection rules

```text
applies when      a required predecessor-owned surface (or §29.2 P2 input) is not
                  integrated/current for dependent execution
shape             derived posture + reason refs; NOT a workflow routing state, NOT a
                  canonical Issue state, NOT a gate verdict
dispatch effect   none — nothing is materialized, nothing is claimable; no
                  guaranteed-BLOCKED dispatch is created to "confirm" the wait
forbidden         F11  state:done          -> LINEAGE_CURRENT   (completion ≠ currentness)
inferences        F17  WAITING_LINEAGE     -> state:blocked
                  F18  WAITING_LINEAGE     -> gate PASS
                  F19  WAITING_LINEAGE     -> gate FAIL
exit              predecessor surface becomes integrated/current -> recompute drops the
                  posture; §29.2 evaluation resumes from current facts
```

Registered in `registries/state-dimensions-v1.json` as `waiting_lineage` (`OWNER_DEFINED`, canonical owner = `EXECUTION_ARCHITECTURE_STANDARD.md`).

## 7. Carry-forward reducer behavior

The reducer maintains the unresolved-finding set as durable state consumed by currentness (its digest is part of the plan binding) and separated from verdict chronology (§29.5):

```text
ingest    an adverse terminal adds its findings to the unresolved set; nothing else removes them
carry     successor subject (authorized repair) -> every lineage-relevant finding is carried
          into the successor review contract
close     per-finding verification only: RESOLVED | STILL_PRESENT |
          NOT_APPLICABLE_TO_SUCCESSOR, each with evidence refs + owning-rule basis; or an
          explicit owning-authority disposition
never     a new reviewer, new model, new route, new SHA, or unrelated PASS closes a finding
```

Aggregation (finding-union, blocker-dominance) remains with the Assurance Plan / Adversarial Review owner. Carry-forward is bookkeeping, not verdict authority.

## 8. No-review-shopping routing

```text
R1 returns a blocking finding
  -> route: authorized repair => successor subject S2 (findings carried) => re-review of S2
  -> route: owning-authority disposition explicitly authorizes re-review
  -> everything else is rejected: same-subject redispatch for PASS, new-reviewer PASS over the
     blocker, discard-and-retry, supersede-and-redisplay around the terminal
```

A new adverse finding arriving between Dispatch and Claim blocks Claim until the plan/currentness is refreshed (§29.1). The orchestrator cannot shop validators either: the same fail-closed preconditions apply to any independent verdict owner.

## 9. Owner boundaries (consumed contracts)

| Concern | Owner (read-only for this lane) | Consumed surface |
| --- | --- | --- |
| plan currentness vocabulary | `standards/ASSURANCE_PLAN_STANDARD.md` | §12 (`CURRENT/STALE/UNKNOWN`) |
| plan binding fields | `schemas/assurance-plan-v2.schema.json` | `currentness_binding.*` |
| finding carry-forward policy | `standards/ASSURANCE_PLAN_STANDARD.md` | §13 |
| finding aggregation | Assurance Plan / Adversarial Review owners | §3 |
| state dimensions + F11-F19 | `registries/state-dimensions-v1.json` | `waiting_lineage`, forbidden inferences |
| role profile family | `schemas/role-execution-profile-v1.schema.json` + reference | projection, hard-predicate feeding |
| release applicability | `standards/RELEASE_STANDARD.md` | §11 (gate × subject, no aggregation) |
| eligibility / claim / admission | `EXECUTION_ARCHITECTURE_STANDARD.md` | §11, §11.1, §27 |

Forbidden over-claims (reject on sight): WAITING_LINEAGE as canonical state; plan `CURRENT` as gate PASS/READY (F13-F16); profile as capability/claim switch; JIT phase self-admission; model judgment as predicate proof; new PASS erasing carried findings; second scheduler/claim lifecycle/runtime authority store.

## 10. Kernel oracles

`scripts/test_v49_execution_core.py` exercises K01-K10 deterministically over `fixtures/execution-core-v49/`: reducer unit tests, JIT truth table, currentness-drift recompute, race/drift fail-closed simulations, carry-forward aggregation, no-review-shopping routing, owner-boundary negatives, and the Product E/F/G/K/L/M/N + L2 negative bindings. Builder evidence is not independent Validation; Validation owns independent rebinding.
