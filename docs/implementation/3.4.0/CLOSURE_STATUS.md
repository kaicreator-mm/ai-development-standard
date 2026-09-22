# v3.4.0 Closure Status

Update: 2026-09-22 · Integration branch: `version/v3.4.0` · Status: **REOPENED — T-011/T-012 CORRECTIONS IN PROGRESS**

This is the truthful closure record required by `RELEASE_STANDARD.md` / `AGENTS.md`.

The first v3.4.0 closure completed on candidate `f90669abda9fab35f4759469f1369ac55ba702fe`, but Issues #64 and #66 identified normative execution-contract defects before any GitHub Release was published. v3.4.0 is therefore reopened for bounded corrective Tasks T-011 then T-012.

All prior exact-head Validation, Independent Review and Release Qualification remain valid historical evidence for the exact SHA they tested. They MUST NOT be reused as final closure evidence after T-011/T-012 change the version candidate.

## Durable GitHub execution state

- v3.4 umbrella: #47 — REOPENED.
- T-001…T-009: #48…#56 — DONE.
- T-011 pointer-only trigger correction: #64 / PR #65 — REVIEW-READY; exact-head Actions run #199 PASS; required Independent Review pending.
- T-012 Work Item Contract / Version DAG / metadata / Golden Templates: #66 / PR #67 — REVIEW-READY on current stacked exact HEAD after full CI; required Independent Review pending.
- T-010 Version Closure: #57 — REOPENED; blocked on T-011 + T-012 integration, then fresh final closure.
- Historical release PR #58 integrated the first closed candidate to `main`; its review/qualification is historical after the corrective tasks change `version/v3.4.0`.
- No GitHub Release existed when closure was reopened.

## Planning authority

The original `TASK_PACKS.json` remains the historical frozen T-001…T-010 planning snapshot.

Post-closure correction authority is explicit and additive:

- `docs/implementation/3.4.0/T011_TASK_PACK_AMENDMENT.json`
- `docs/implementation/3.4.0/task-packs/T011_pointer_only_trigger.md`
- `docs/implementation/3.4.0/T012_TASK_PACK_AMENDMENT.json`
- `docs/implementation/3.4.0/task-packs/T012_work_item_contract.md`
- `docs/implementation/3.4.0/TASK_DAG.md`
- Issues #64 / #66

This avoids silently rewriting the original planning snapshot while making both corrective tasks part of current v3.4.0 authority.

## Historical implementation lineage

| Task | Implementation evidence | State |
|---|---|---|
| T-001 authority convergence + Task DAG + Task Packs | `0760f92` | DONE |
| T-002 Task Pack / Execution Pack contracts + standard + templates | `ba3c22e` | DONE |
| T-003 unified dispatch + event-v2/execution-state extensions + v34 rules | `dfad50a` | DONE |
| T-004/T-005 builder+validator profiles, exact-SHA rule, queue, bootstraps | `f34e9e4` | DONE |
| T-006..T-008 closed loop, web control plane, local-first CI, adoption | `0ddba5f` | DONE |
| T-009 conformance + adversarial regression + verifier + CI wiring | `3bdc534` + follow-up | DONE |
| T-011 pointer-only trigger correction | #64 / PR #65 | REVIEW-READY |
| T-012 Work Item/DAG/Golden contract | #66 / PR #67 | REVIEW-READY |

## Historical closure evidence

The first closed candidate was:

```text
f90669abda9fab35f4759469f1369ac55ba702fe
```

Historical evidence includes:

- exact-head `verify-standard` run #193 / `35692606829`: PASS;
- Fresh Independent Re-review C on PR #58: PASS, P0=0/P1=0;
- Release Qualification: READY;
- repository integration to `main@418d244f23a6bf724acf5d4c4eff4ea292f1c4db`.

These facts remain audit history. They do not prove the post-T012 candidate.

## T-011 correction

T-011 enforces:

```text
GitHub Issue + referenced repository authority = complete executable task contract
user-visible ChatGPT Web trigger = pointer only
No durable contract -> no trigger
No Issue update -> no new task-specific instruction in chat
```

Current exact T-011 PR #65 HEAD `48c43e4a0dff1fe403136872dabedea30fac09ae` has full Actions run #199 PASS. Required Independent Review remains NOT_RUN.

## T-012 correction

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

The current stacked PR #67 is based on the T-011 exact HEAD because T-012 consumes T-011 pointer-only semantics. Its first implementation candidate `94316138147bc5e6562ee71748324e11c65e1aaf` passed full Actions run #211, including `test_work_item_contract_and_golden_templates.py`. Subsequent planning/closure bookkeeping changes create a successor HEAD and require a fresh exact-head run before Review.

## Current T-011 gates

1. Full exact-head CI — PASS on PR #65 HEAD `48c43e4a...`, run #199.
2. Required Independent Review — NOT_RUN.
3. Merge to `version/v3.4.0` — NOT_RUN until Independent Review PASS.

## Current T-012 gates

1. Normative Work Item / Golden implementation — DONE on task branch.
2. Standard-wide `STANDARD_COVERAGE.json` mapping — DONE; verifier requires exact match with all active normative standards.
3. Focused Work Item / Golden regression — PASS on first candidate run #211; successor exact-head rerun required after bookkeeping changes.
4. Full existing verify-standard chain — PASS on first candidate run #211; successor exact-head rerun required.
5. Required Independent Review — NOT_RUN; must bind to final exact PR #67 HEAD.
6. Retarget/integrate after T-011 merge — NOT_RUN.

## Reopened T-010 gates after T-011 + T-012 merge

1. Full verifier/coherence chain on the new exact `version/v3.4.0` candidate — NOT_RUN.
2. Fresh Independent Review on that exact final candidate — NOT_RUN.
3. Release Qualification on that exact candidate — NOT_RUN.
4. Reconfirm #45/#46 material acceptance remains satisfied — NOT_RUN.
5. Integrate successor v3.4.0 candidate to `main` — NOT_RUN.
6. Record superseding immutable v3.4.0 baseline — NOT_RUN.

## Operator / authority boundaries

- T-011/T-012 Builders may implement only their bounded concerns and publish exact-head validation evidence.
- Required Independent Review must come from a distinct logical reviewer context and reconstruct facts from GitHub.
- T-012 derived DAG views are non-authoritative and cannot replace Task Issues/native Issue Dependencies.
- T-010 release controller cannot inherit historical qualification onto a successor SHA.
- Repository integration remains a distinct bounded step after new Release Qualification READY.

Unresolved states stay explicit; `FAIL`, `BLOCKED`, and `NOT_RUN` are never renamed to manufacture `READY`.
