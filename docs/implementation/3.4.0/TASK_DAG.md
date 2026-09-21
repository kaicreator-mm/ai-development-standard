# Task DAG — v3.4.0

## Frozen Inputs

- Version plan: v3.4 GitHub-native Pull Execution, Execution Pack and Exact-SHA Validation Handoff (absorbs #45, #46)
- Architecture decision: `docs/implementation/3.4.0/ARCHITECTURE_DECISION.md` (T-001 output, FROZEN)
- Baseline: `1ce6497402c6e1b54b07cc3bc8f8a46444d1af32` (immutable v3.3.0)
- Integration branch: `version/v3.4.0`
- Standard revision: this repository at the integration branch

## Planning DAG

| Task | Issue | Depends On | Parallel | Risk | Input / Reference | Output | Acceptance | Model | Required Validation | Review Policy | Code Baseline | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T-001 | pending | — | NO | H | version plan §1–§4 | ARCHITECTURE_DECISION.md | one converged architecture; #45/#46 mapped | High | verify-standard | required | independent | DONE |
| T-002 | pending | T-001 | NO | H | decision §2, §5, §6 | schemas + pack templates | Task Pack / Execution Pack machine contracts; freedom field; staleness rules | High | test_protocol_schemas + test_v34_lifecycle_contracts | required | independent | DONE |
| T-003 | pending | T-002 | NO | H | decision §1, §7 | schemas + reducer rules | unified dispatch events/state; no parallel state machine | High | test_protocol_schemas + test_v34_lifecycle_contracts | required | independent | DONE |
| T-004 | pending | T-003 | NO | M | decision §9 | LOCAL_AGENT_HANDOFF + bootstrap | JIT builder flow standardized | High | verify-standard + test_v34_lifecycle_contracts | required | independent | DONE |
| T-005 | pending | T-003 | YES | H | decision §2.4, §8, §9 | VALIDATION + handoff queue template | validator profile + queue projection; exact-SHA rules | High | verify-standard + test_v34_lifecycle_contracts | required | independent | DONE |
| T-006 | pending | T-004, T-005 | NO | H | decision §1, §9 | interaction protocol + web role | reviewer/merge/DAG closed loop | High | verify-standard + test_v34_lifecycle_contracts | required | independent | DONE |
| T-007 | pending | T-006 | YES | M | version plan §16 | CI + validation standards | local-first policy integrated | Low | verify-standard | recommended | independent | DONE |
| T-008 | pending | T-006 | YES | M | version plan §22 | adoption + templates | templates/overrides/retention/Fast Path | Low | verify-standard | recommended | independent | DONE |
| T-009 | pending | T-002..T-008 | NO | H | version plan §24 | scenarios A–G | positive + adversarial verifier regression | High | all test scripts green | required | independent | DONE |
| T-010 | pending | T-009 | NO | H | RELEASE_STANDARD | closure report | full verifier + Fresh Independent Review + release qualification | High | version closure gates | required | independent | DOING |

Planning status values: `TODO / DOING / BLOCKED / DONE / DEFERRED / NOT_APPLICABLE`.

Rules:

- This checkpoint is the planning/history DAG. GitHub Task Issues + Issue Dependencies are the canonical live execution DAG once materialized.
- Task Issue materialization for T-002..T-010 is pending until GitHub CLI/API access is restored for this repository; until then this document + `TASK_PACKS.json` are the durable planning authority and commit history on `version/v3.4.0` is the execution record.
- A task is `DONE` only when its acceptance criteria and required task-level gates are satisfied.
- Per-task Independent Review on intermediate merges is consolidated into the version-level Fresh Independent Review on the final exact candidate (see T-010); this consolidation is recorded here rather than silently asserted.

## Review Policy Planning

Version-level Review Policy: `required` (Fresh Independent Review on the final merge candidate before `version/v3.4.0` → `main`). T-007/T-008 are content-only and may consolidate into the same version-level review.

## Execution mode

Tasks execute as sequential commits on `version/v3.4.0` (dependencies are content-sequential: contracts → dispatch → role standards → closed loop → adoption → regression → closure). The JIT branch rule is applied at version granularity: the version branch was created from the immutable v3.3 baseline exactly when implementation became ready, and no long-lived per-task branches precede dependency satisfaction.
