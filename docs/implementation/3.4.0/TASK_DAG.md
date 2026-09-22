# Task DAG — v3.4.0

## Frozen Inputs

- Version plan: v3.4 GitHub-native Pull Execution, Execution Pack and Exact-SHA Validation Handoff (absorbs #45, #46)
- Architecture decision: `docs/implementation/3.4.0/ARCHITECTURE_DECISION.md` (T-001 output, FROZEN)
- Baseline: `1ce6497402c6e1b54b07cc3bc8f8a46444d1af32` (immutable v3.3.0)
- Integration branch: `version/v3.4.0`
- Standard revision: this repository at the integration branch
- Post-closure correction: T-011 / Issue #64, machine amendment `docs/implementation/3.4.0/T011_TASK_PACK_AMENDMENT.json`

## Planning DAG

| Task | Issue | Depends On | Parallel | Risk | Input / Reference | Output | Acceptance | Model | Required Validation | Review Policy | Code Baseline | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T-001 | #48 | — | NO | H | version plan §1–§4 | ARCHITECTURE_DECISION.md | one converged architecture; #45/#46 mapped | High | verify-standard | required | independent | DONE |
| T-002 | #49 | T-001 | NO | H | decision §2, §5, §6 | schemas + pack templates | Task Pack / Execution Pack machine contracts; freedom field; staleness rules | High | test_protocol_schemas + test_v34_lifecycle_contracts | required | independent | DONE |
| T-003 | #50 | T-002 | NO | H | decision §1, §7 | schemas + reducer rules | unified dispatch events/state; no parallel state machine | High | test_protocol_schemas + test_v34_lifecycle_contracts | required | independent | DONE |
| T-004 | #51 | T-003 | NO | M | decision §9 | LOCAL_AGENT_HANDOFF + bootstrap | JIT builder flow standardized | High | verify-standard + test_v34_lifecycle_contracts | required | independent | DONE |
| T-005 | #52 | T-003 | YES | H | decision §2.4, §8, §9 | VALIDATION + handoff queue template | validator profile + queue projection; exact-SHA rules | High | verify-standard + test_v34_lifecycle_contracts | required | independent | DONE |
| T-006 | #53 | T-004, T-005 | NO | H | decision §1, §9 | interaction protocol + web role | reviewer/merge/DAG closed loop | High | verify-standard + test_v34_lifecycle_contracts | required | independent | DONE |
| T-007 | #54 | T-006 | YES | M | version plan §16 | CI + validation standards | local-first policy integrated | Low | verify-standard | recommended | independent | DONE |
| T-008 | #55 | T-006 | YES | M | version plan §22 | adoption + templates | templates/overrides/retention/Fast Path | Low | verify-standard | recommended | independent | DONE |
| T-009 | #56 | T-002..T-008 | NO | H | version plan §24 | scenarios A–G | positive + adversarial verifier regression | High | all test scripts green | required | independent | DONE |
| T-011 | #64 | T-009 | NO | H | post-closure defect + ISSUE_FIRST_TASK_TRIGGER | pointer-only trigger authority + regression | durable Issue is complete contract; user-visible trigger pointer-only; incomplete Issue repaired first | High | full verify-standard + pointer-only regression + exact-head CI | required | `version/v3.4.0@f90669ab...` | DOING |
| T-010 | #57 | T-009, T-011 | NO | H | RELEASE_STANDARD + post-T011 candidate | closure report | full verifier + Fresh Independent Review + Release Qualification on new exact candidate | High | version closure gates | required | successor candidate after T-011 | REOPENED |

Planning status values: `TODO / DOING / BLOCKED / DONE / DEFERRED / NOT_APPLICABLE / REOPENED`.

## Post-closure correction rule

T-001…T-010 were originally planned before T-011 existed. The original `TASK_PACKS.json` remains the frozen historical planning snapshot. T-011 is an explicit corrective amendment rather than a silent rewrite of that snapshot:

```text
historical planning snapshot
+ T011_TASK_PACK_AMENDMENT.json
+ task-packs/T011_pointer_only_trigger.md
= current v3.4.0 planning authority
```

The first T-010 closure on candidate `f90669abda9fab35f4759469f1369ac55ba702fe` is historical evidence only after T-011 changes the version branch. Fresh closure is mandatory on the successor exact candidate.

## Rules

- This checkpoint is the planning/history DAG. GitHub Task Issues + Issue Dependencies are the canonical live execution DAG once materialized.
- A task is `DONE` only when its acceptance criteria and required task-level gates are satisfied.
- T-011 uses a JIT task branch from the current v3.4 integration baseline because its dependencies are already satisfied.
- T-011 Review Policy is `required` because it changes normative authority placement and cross-agent invocation semantics.
- T-010 remains reopened until T-011 merges and fresh exact-head closure gates pass.

## Review Policy Planning

Version-level Review Policy remains `required`. T-011 additionally requires concern-level Independent Review on its exact PR HEAD before merge to `version/v3.4.0`; the final post-T011 version candidate then requires a separate Fresh Independent Review during T-010 closure.

## Execution mode

T-011 executes on `task/v3.4.0-t011-pointer-only-trigger` from `version/v3.4.0@f90669ab...`, targets `version/v3.4.0`, and does not alter unrelated v3.4 scope. After merge, T-010 reruns closure on the new exact candidate.