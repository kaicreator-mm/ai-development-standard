# v3.4.0 Closure Status

Update: 2026-09-22 · Integration branch: `version/v3.4.0` · Status: **REOPENED — T-011 REVIEW REPAIR VALIDATED; RE-REVIEW REQUIRED**

This is the truthful closure record required by `RELEASE_STANDARD.md` / `AGENTS.md`.

The first v3.4.0 closure completed on candidate `f90669abda9fab35f4759469f1369ac55ba702fe`, but Issue #64 identified a normative prompt-authority defect before any GitHub Release was published. v3.4.0 is therefore reopened for bounded corrective Task T-011, followed by T-012 before fresh T-010 closure.

All prior exact-head Validation, Independent Review and Release Qualification remains valid historical evidence for the exact SHA it tested. It MUST NOT be reused as final closure evidence after T-011/T-012 change the version candidate.

## Durable GitHub execution state

- v3.4 umbrella: #47 — REOPENED.
- T-001…T-009: #48…#56 — DONE.
- T-011 pointer-only trigger correction: #64 / PR #65 — REVIEW-READY after bounded repair of the first Independent Review findings.
- T-012 Work Item / Version DAG / Golden Template contract: #66 / PR #67 — stacked implementation exists; cannot integrate before T-011.
- T-010 Version Closure: #57 — REOPENED; blocked on T-011 + T-012 merge, then fresh final closure.
- Historical release PR #58 integrated the first closed candidate to `main`; its review/qualification is historical after T-011/T-012 change `version/v3.4.0`.
- No GitHub Release currently exists for this repository.

## Planning authority

The original `TASK_PACKS.json` remains the historical frozen T-001…T-010 planning snapshot.

Post-closure correction authority is explicit and additive:

- `docs/implementation/3.4.0/T011_TASK_PACK_AMENDMENT.json`
- `docs/implementation/3.4.0/T012_TASK_PACK_AMENDMENT.json` when T-012 is integrated
- `docs/implementation/3.4.0/task-packs/T011_pointer_only_trigger.md`
- T-012 Task Pack on its task branch / eventual integration
- `docs/implementation/3.4.0/TASK_DAG.md`
- Issues #64 and #66

This avoids silently rewriting the original planning snapshot while making post-closure corrections explicit.

## Historical implementation lineage

| Task | Implementation evidence | State |
|---|---|---|
| T-001 authority convergence + Task DAG + Task Packs | `0760f92` | DONE |
| T-002 Task Pack / Execution Pack contracts + standard + templates | `ba3c22e` | DONE |
| T-003 unified dispatch + event-v2/execution-state extensions + v34 rules | `dfad50a` | DONE |
| T-004/T-005 builder+validator profiles, exact-SHA rule, queue, bootstraps | `f34e9e4` | DONE |
| T-006..T-008 closed loop, web control plane, local-first CI, adoption | `0ddba5f` | DONE |
| T-009 conformance + adversarial regression + verifier + CI wiring | `3bdc534` + follow-up | DONE |
| T-011 pointer-only trigger correction | PR #65 current successor candidate | REVIEW-READY |
| T-012 Work Item / Version DAG / Golden Templates | PR #67 stacked candidate | BLOCKED_BY_T011_INTEGRATION |

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

These facts remain audit history. They do not prove the post-T011/T012 candidate.

## T-011 defect and review-repair status

T-011 enforces:

```text
GitHub Issue + referenced repository authority = complete executable task contract
user-visible ChatGPT Web trigger = pointer only
No durable contract -> no trigger
No Issue update -> no new task-specific instruction in chat
```

The first Fresh Independent Review of PR #65 on `48c43e4a...` returned FAIL with P0=0/P1=2:

1. the focused pointer-only test used a partial blacklist and could fail open for forbidden branch/scope/review/evidence/command payloads;
2. the normative standard and Validator queue retained an older `<project> <version>` trigger dialect outside the declared allowlist.

The Builder applied a bounded repair:

- the conformance oracle now fails closed against canonical repository + Issue/PR + optional role/dispatch grammar;
- negative regressions cover branch/base, scope/write-set, arbitrary commands, review/repair, failure, closeout/merge and evidence payloads;
- the old project/version role trigger was removed from the normative standard and Validator queue;
- a regression prevents the old dialect from returning.

Current T-011 successor exact HEAD is authoritative from PR #65. GitHub Actions run #221 / `35722956029` is PASS on that successor exact HEAD, including the repaired focused pointer-only regression and the complete existing verifier chain.

The old Review FAIL remains historical for `48c43e4a...`; a Fresh Independent Re-review is required on the successor exact HEAD before merge.

## Current T-011 gates

1. **Normative authority repair** — PASS on current PR #65 successor candidate.
2. **Focused pointer-only trigger regression** — PASS in run #221.
3. **Full existing verify-standard chain** — PASS in run #221.
4. **Exact-head GitHub Actions verify-standard** — PASS in run #221.
5. **Fresh Independent Re-review of T-011 PR** — NOT_RUN on successor exact HEAD; required P0/P1=0.
6. **Merge T-011 to `version/v3.4.0`** — NOT_RUN until gate 5 passes.

## T-012 and reopened T-010 gates

After T-011 merge:

1. retarget/reconcile PR #67 against current `version/v3.4.0` and re-establish affected exact-head validation/review;
2. merge T-012 only after its required concern gates pass;
3. run full verifier/coherence on the post-T-012 exact version candidate;
4. obtain Fresh version-level Independent Review;
5. perform Release Qualification;
6. reconfirm #45/#46 material acceptance;
7. integrate successor v3.4.0 candidate to `main`;
8. record superseding immutable v3.4.0 baseline.

## Operator / authority boundaries

- Builder may repair review findings and publish exact-head validation evidence, but may not self-assert Independent Review PASS.
- Independent Reviewer must be a distinct logical reviewer context and reconstruct facts from GitHub.
- T-010 release controller cannot inherit historical qualification onto a successor SHA.
- Repository integration remains a distinct bounded step after new Release Qualification READY.

Unresolved states stay explicit; `FAIL`, `BLOCKED`, and `NOT_RUN` are never renamed to manufacture `READY`.