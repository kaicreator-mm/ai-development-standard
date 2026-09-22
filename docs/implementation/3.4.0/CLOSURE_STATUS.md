# v3.4.0 Closure Status

Update: 2026-09-22 · Integration branch: `version/v3.4.0` · Status: **REOPENED — T-011 MERGED; T-012 RECONCILIATION / REVIEW IN PROGRESS**

This is the truthful closure record required by `RELEASE_STANDARD.md` / `AGENTS.md`.

The first v3.4.0 closure completed on candidate `f90669abda9fab35f4759469f1369ac55ba702fe`, but Issues #64 and #66 identified normative execution-contract defects before any GitHub Release was published. v3.4.0 remains reopened until T-012 and fresh T-010 closure complete.

Historical Validation / Review / Release Qualification evidence remains valid only for the exact SHA it tested. It MUST NOT be inherited onto successor candidates.

## Durable GitHub execution state

- v3.4 umbrella: #47 — REOPENED.
- T-001…T-009: #48…#56 — DONE.
- T-011 pointer-only trigger correction: #64 / PR #65 — **DONE / MERGED**.
  - final reviewed HEAD: `1d426d805bdf5c818330e2f83dac7a3fabd692e0`;
  - exact-head `verify-standard` run #228 / `35723319909`: PASS;
  - Fresh Independent Re-review: PASS, P0=0 / P1=0 / P2=1 / P3=0;
  - P2 was non-blocking closure-document freshness and is reconciled by the T-012 bookkeeping update;
  - merged integration commit: `dddb3bfe53322df17f712d60f4e9f5582603a921`.
- T-012 Work Item Contract / Version DAG / metadata / Golden Templates: #66 / PR #67 — implementation complete; retargeted to `version/v3.4.0`; topology reconciliation + fresh exact-head validation/review required before merge.
- T-010 Version Closure: #57 — REOPENED; blocked on T-012 integration, then fresh final closure.
- Historical release PR #58 integrated the first closed candidate to `main`; it cannot serve as the successor v3.4.0 integration PR.

## Planning authority

The original `TASK_PACKS.json` remains the historical frozen T-001…T-010 planning snapshot.

Post-closure correction authority is additive:

- `docs/implementation/3.4.0/T011_TASK_PACK_AMENDMENT.json`
- `docs/implementation/3.4.0/task-packs/T011_pointer_only_trigger.md`
- `docs/implementation/3.4.0/T012_TASK_PACK_AMENDMENT.json`
- `docs/implementation/3.4.0/task-packs/T012_work_item_contract.md`
- `docs/implementation/3.4.0/TASK_DAG.md`
- Issues #64 / #66

## Historical implementation lineage

| Task | Evidence | State |
|---|---|---|
| T-001 authority convergence + Task DAG + Task Packs | `0760f92` | DONE |
| T-002 Task Pack / Execution Pack contracts | `ba3c22e` | DONE |
| T-003 unified dispatch / event lifecycle | `dfad50a` | DONE |
| T-004/T-005 builder+validator profiles / exact-SHA / queue | `f34e9e4` | DONE |
| T-006..T-008 closed loop / Web control plane / local-first CI / adoption | `0ddba5f` | DONE |
| T-009 conformance + adversarial verifier regression | `3bdc534` + follow-up | DONE |
| T-011 pointer-only trigger correction | PR #65 → `dddb3bfe...` | DONE |
| T-012 Work Item / DAG / Golden contract | #66 / PR #67 | DOING |

## Historical first closure evidence

First closed candidate:

```text
f90669abda9fab35f4759469f1369ac55ba702fe
```

Historical evidence:

- exact-head `verify-standard` run #193 / `35692606829`: PASS;
- Fresh Independent Re-review C on PR #58: PASS, P0=0/P1=0;
- Release Qualification: READY;
- repository integration to `main@418d244f23a6bf724acf5d4c4eff4ea292f1c4db`.

These facts are audit history only and do not prove the post-T012 candidate.

## T-011 result

T-011 now enforces:

```text
GitHub Issue + referenced repository authority = complete executable task contract
user-visible ChatGPT Web trigger = pointer only
No durable contract -> no trigger
No Issue update -> no new task-specific instruction in chat
```

The first Independent Review on `48c43e4a...` found P1=2. Both findings were repaired: pointer conformance became fail-closed against canonical pointer grammar, and legacy `<project> <version>` trigger forms were removed from normative surfaces. The Fresh Independent Re-review on final HEAD `1d426d805...` passed with P0=0/P1=0 and routed merge-ready. PR #65 then merged to the integration branch as `dddb3bfe...`.

## T-012 scope

T-012 adds:

```text
recoverable substantial-version Task DAG
+ canonical live Task Issues/native Issue Dependencies
+ strict Work Item type/state/review/risk semantics
+ stable executable Issue contract/readiness
+ all-standard Golden/Forbidden/rationale coverage
+ concrete critical templates
+ machine regression
```

Before T-011 merged, T-012 candidate `1ae89bdbb58a2fe4ace9b0fb432f6525fbf960e9` passed Actions run #226 / `35723261901`, including the T-011 pointer repair regression and T-012 Work Item / Golden coverage regression. That PASS proves that historical exact tree only. After retarget to integration commit `dddb3bfe...`, topology is being explicitly reconciled; a successor exact HEAD requires fresh validation and required Independent Review.

## Current T-012 gates

1. Normative Work Item / Golden implementation — DONE.
2. Standard-wide `STANDARD_COVERAGE.json` exact mapping — DONE.
3. T-011 upstream repair synchronization — DONE.
4. Reconcile PR #67 ancestry with merged T-011 integration base — DOING.
5. Fresh full `verify-standard` on reconciled exact HEAD — NOT_RUN until reconciliation commit exists.
6. Required Fresh Independent Review on reconciled exact HEAD — NOT_RUN.
7. Merge T-012 to `version/v3.4.0` — NOT_RUN until gates 4–6 pass.

## Reopened T-010 gates after T-012 merge

1. Full verifier/coherence chain on the new exact `version/v3.4.0` candidate — NOT_RUN.
2. Fresh Independent Review on that exact final version candidate — NOT_RUN.
3. Release Qualification on that exact candidate — NOT_RUN.
4. Reconfirm #45/#46 material acceptance remains satisfied — NOT_RUN.
5. Create a successor `version/v3.4.0 → main` integration PR; historical PR #58 MUST NOT be reused as current candidate authority — NOT_RUN.
6. Integrate successor v3.4.0 candidate to `main` — NOT_RUN.
7. Record superseding immutable v3.4.0 baseline — NOT_RUN.

## Operator / authority boundaries

- T-012 Builder may perform bounded topology reconciliation and publish exact-head validation evidence, but cannot self-assert required Independent Review PASS.
- Derived DAG views remain non-authoritative and cannot replace Task Issues/native Issue Dependencies.
- T-010 release controller cannot inherit historical qualification onto a successor SHA.
- Repository integration remains distinct from Release Qualification.

Unresolved states stay explicit; `FAIL`, `BLOCKED`, and `NOT_RUN` are never renamed to manufacture `READY`.
