# Task DAG — v3.4.0

## Frozen Inputs

- Version plan: v3.4 GitHub-native Pull Execution, Execution Pack and Exact-SHA Validation Handoff (absorbs #45, #46)
- Architecture decision: `docs/implementation/3.4.0/ARCHITECTURE_DECISION.md` (T-001 output, FROZEN)
- Baseline: `1ce6497402c6e1b54b07cc3bc8f8a46444d1af32` (immutable v3.3.0)
- Integration branch: `version/v3.4.0`
- Standard revision: this repository at the integration branch
- Post-closure corrections: T-011 / Issue #64 and T-012 / Issue #66
- Additive amendments: `T011_TASK_PACK_AMENDMENT.json`, `T012_TASK_PACK_AMENDMENT.json`

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
| T-011 | #64 | T-009 | NO | H | post-closure defect + ISSUE_FIRST_TASK_TRIGGER | pointer-only trigger authority + regression | durable Issue is complete contract; user-visible trigger pointer-only; incomplete Issue repaired first | High | full verify-standard + pointer-only regression + exact-head CI | required | merged as `dddb3bfe...` | DONE |
| T-012 | #66 | T-011 | NO | H | Work Item/DAG/metadata/Golden-template gap | canonical Work Item contract + Golden coverage + templates + verifier | recoverable Version DAG; strict metadata/Issue contract; all normative standards have Golden/Forbidden/rationale coverage | High | full verify-standard + focused Work Item/Golden regression + exact-head CI | required | retargeted to `version/v3.4.0@dddb3bfe...` | DOING |
| T-010 | #57 | T-009, T-011, T-012 | NO | H | RELEASE_STANDARD + post-T012 candidate | closure report | full verifier + Fresh Independent Review + Release Qualification on new exact candidate | High | version closure gates | required | successor candidate after T-012 | REOPENED |

Planning status values: `TODO / DOING / BLOCKED / REVIEW-READY / DONE / DEFERRED / NOT_APPLICABLE / REOPENED`.

The status column is a planning/checkpoint aid, not canonical live execution state. GitHub Task Issues + native Issue Dependencies + events remain the live execution authority.

## Post-closure correction rule

T-001…T-010 were originally planned before T-011/T-012 existed. The original `TASK_PACKS.json` remains the frozen historical planning snapshot. Post-closure tasks are explicit additive corrective amendments rather than silent rewrites:

```text
historical TASK_PACKS.json
+ T011_TASK_PACK_AMENDMENT.json
+ task-packs/T011_pointer_only_trigger.md
+ T012_TASK_PACK_AMENDMENT.json
+ task-packs/T012_work_item_contract.md
= current v3.4.0 planning authority
```

The first T-010 closure on candidate `f90669abda9fab35f4759469f1369ac55ba702fe` is historical evidence only after T-011/T-012 change the version branch. Fresh closure is mandatory on the post-T012 exact candidate.

## Rules

- This checkpoint is the planning/history DAG. GitHub Task Issues + native Issue Dependencies are the canonical live execution DAG once materialized.
- Every substantial version MUST keep the DAG recoverable from this checkpoint plus GitHub durable facts.
- A shared Markdown state table MUST NOT become canonical live execution state; derived state cards must be marked `NON_AUTHORITATIVE_DERIVED_STATE`.
- A task is `DONE` only when its acceptance criteria and required task-level gates are satisfied.
- T-011 Review Policy was `required`; final exact-head CI + Fresh Independent Re-review passed and PR #65 merged to `version/v3.4.0`.
- T-012 Review Policy is `required` because it changes canonical GitHub Work Item semantics used by all Agents/projects.
- T-012 was stacked on T-011 only while the upstream code baseline was unmerged. After T-011 merge it was retargeted to `version/v3.4.0` and explicitly reconciled with integration commit `dddb3bfe...`; its successor exact HEAD requires fresh validation and Independent Review.
- T-010 remains reopened until T-012 merges and fresh exact-head closure gates pass.

## Review Policy Planning

Version-level Review Policy remains `required`. T-012 requires concern-level Independent Review on its final exact PR HEAD before integration. The final post-T012 version candidate then requires a separate Fresh Independent Review during T-010 closure.

## Execution mode

T-011 completed on `task/v3.4.0-t011-pointer-only-trigger` and merged through PR #65 to `version/v3.4.0@dddb3bfe...`.

T-012 executes on `task/v3.4.0-t012-work-item-contract`, now directly targeting `version/v3.4.0`. The branch contains an explicit two-parent reconciliation commit so the already-developed T-012 concern and merged T-011 integration history are both represented without rewriting the full task history. Current live readiness is derived from GitHub Issue/PR/CI/Review facts, not this Markdown status cell.
