# v3.4.0 Closure Status

Update: 2026-09-22 · Integration branch: `version/v3.4.0` · Status: **REOPENED — T-011 POINTER-ONLY TRIGGER CORRECTION IN PROGRESS**

This is the truthful closure record required by `RELEASE_STANDARD.md` / `AGENTS.md`.

The first v3.4.0 closure completed on candidate `f90669abda9fab35f4759469f1369ac55ba702fe`, but Issue #64 identified a normative prompt-authority defect before any GitHub Release was published. v3.4.0 is therefore reopened for bounded corrective Task T-011.

All prior exact-head Validation, Independent Review and Release Qualification remains valid historical evidence for the exact SHA it tested. It MUST NOT be reused as final closure evidence after T-011 changes the version candidate.

## Durable GitHub execution state

- v3.4 umbrella: #47 — REOPENED.
- T-001…T-009: #48…#56 — DONE.
- T-011 pointer-only trigger correction: #64 — DOING.
- T-010 Version Closure: #57 — REOPENED; blocked on T-011 merge, then fresh final closure.
- Historical release PR #58 integrated the first closed candidate to `main`; its review/qualification is historical after T-011 changes `version/v3.4.0`.
- No GitHub Release currently exists for this repository.

## Planning authority

The original `TASK_PACKS.json` remains the historical frozen T-001…T-010 planning snapshot.

Post-closure correction authority is explicit and additive:

- `docs/implementation/3.4.0/T011_TASK_PACK_AMENDMENT.json`
- `docs/implementation/3.4.0/task-packs/T011_pointer_only_trigger.md`
- `docs/implementation/3.4.0/TASK_DAG.md`
- Issue #64

This avoids silently rewriting the original planning snapshot while still making T-011 part of current v3.4.0 authority.

## Historical implementation lineage

| Task | Implementation evidence | State |
|---|---|---|
| T-001 authority convergence + Task DAG + Task Packs | `0760f92` | DONE |
| T-002 Task Pack / Execution Pack contracts + standard + templates | `ba3c22e` | DONE |
| T-003 unified dispatch + event-v2/execution-state extensions + v34 rules | `dfad50a` | DONE |
| T-004/T-005 builder+validator profiles, exact-SHA rule, queue, bootstraps | `f34e9e4` | DONE |
| T-006..T-008 closed loop, web control plane, local-first CI, adoption | `0ddba5f` | DONE |
| T-009 conformance + adversarial regression + verifier + CI wiring | `3bdc534` + follow-up | DONE |
| T-011 pointer-only trigger correction | Issue #64 / current task branch | DOING |

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

These facts remain audit history. They do not prove the post-T011 candidate.

## T-011 defect statement

Current v3.4 wording allowed ChatGPT Web to regress from pointer-only invocation into bespoke task prompts because key clauses were preference-level (`SHOULD`) and because generic bootstrap / Execution Pack prompt material could be misread as user-visible handoff text.

T-011 enforces:

```text
GitHub Issue + referenced repository authority = complete executable task contract
user-visible ChatGPT Web trigger = pointer only
No durable contract -> no trigger
No Issue update -> no new task-specific instruction in chat
```

Task-specific baseline/branch/scope/write-set/acceptance/commands/gates/review/failure/closeout/evidence requirements must be durable before invocation and must not be duplicated in the copied trigger.

## Current T-011 gates

1. **Normative authority repair** — DOING on `task/v3.4.0-t011-pointer-only-trigger`.
2. **Focused pointer-only trigger regression** — NOT_RUN until stable task candidate exists.
3. **Full existing verify-standard chain** — NOT_RUN on final T-011 exact HEAD.
4. **Exact-head GitHub Actions verify-standard** — NOT_RUN on final T-011 exact HEAD.
5. **Required Independent Review of T-011 PR** — NOT_RUN; must use an independent reviewer context and bind to exact PR HEAD.
6. **Merge T-011 to `version/v3.4.0`** — NOT_RUN until gates 2–5 pass.

## Reopened T-010 gates after T-011 merge

1. Full verifier/coherence chain on the new exact `version/v3.4.0` candidate — NOT_RUN.
2. Fresh Independent Review on that exact final candidate — NOT_RUN.
3. Release Qualification on that exact candidate — NOT_RUN.
4. Reconfirm #45/#46 material acceptance remains satisfied — NOT_RUN.
5. Integrate successor v3.4.0 candidate to `main` — NOT_RUN.
6. Record superseding immutable v3.4.0 baseline — NOT_RUN.

## Operator / authority boundaries

- T-011 Builder may implement only the bounded pointer-trigger concern and publish exact-head validation evidence.
- T-011 Independent Reviewer must be a distinct logical reviewer context and reconstruct facts from GitHub.
- T-010 release controller cannot inherit historical qualification onto a successor SHA.
- Repository integration remains a distinct bounded step after new Release Qualification READY.

Unresolved states stay explicit; `FAIL`, `BLOCKED`, and `NOT_RUN` are never renamed to manufacture `READY`.