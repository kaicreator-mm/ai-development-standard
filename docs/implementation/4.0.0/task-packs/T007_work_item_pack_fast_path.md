# T-007 Task Pack — Work Item, Packs and Fast Path Integration

Issue: #79
Parent version: #72
Baseline: `acef771c5895d0d4f8b3ee843420ae5ab493b457`
Review Policy: required
Risk: high
Validation scope: concern
Agent freedom: F1_BOUNDED_IMPLEMENTATION

## Goal

Map v4 Operation semantics onto the existing Work Item / Task Pack / Execution Pack / dispatch / Fast Path contracts without creating duplicate authority or changing v3.4 machine wire contracts in this Task.

## Inputs

- merged T-001..T-006 v4 artifacts;
- `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`;
- `standards/EXECUTION_PACK_STANDARD.md`;
- released pointer-only / execution architecture rules;
- T-006 invariant that Operation composition is not a third execution DAG.

## Allowed changes

- `docs/implementation/4.0.0/WORK_ITEM_OPERATION_INTEGRATION.md`;
- this Task Pack;
- T-007 pointer in `docs/implementation/4.0.0/TASK_PACKS.json`.

## Forbidden changes

- canonical workflow-state vocabulary changes;
- new GitHub object type;
- schema/verifier/event implementation;
- T-008 Validation/Release semantics;
- runtime/queue/transport implementation;
- weakening Task Pack vs Execution Pack authority separation.

## Tests / review oracle

A reviewer must verify at least:

1. GitHub Issue remains stable executable Work Item authority;
2. native Issue Dependencies remain canonical live Task DAG;
3. Operation binding is correlation only and cannot become a second workflow state;
4. no giant duplicated Operation payload is required;
5. Task Pack remains WHAT authority and excludes exact-base implementation assumptions;
6. Execution Pack remains JIT HOW authority bound to one exact base;
7. adding Operation correlation does not weaken pack staleness rules;
8. dispatch retains dynamic role/profile/base/head/operator identity;
9. pointer-only invocation remains normative;
10. Fast Path is reduced operations, not reduced truth;
11. Fast Path does not require empty Product/Architecture/Assurance/Execution artifacts;
12. escalation triggers are explicit enough to prevent low-risk mode from swallowing substantial work;
13. escalation preserves historical evidence and materializes only newly required authority;
14. workflow state remains orthogonal to Operation kind/correlation;
15. no T-008/T-009 implementation scope is entered;
16. existing v3.4 Work Items can migrate additively without forced historical rewrites.

## Failure handling

- missing durable task facts -> repair Work Item before dispatch;
- Task Pack / Architecture contradiction -> route upward, do not silently reinterpret;
- stale/invalid Execution Pack -> use owning pack classification/regeneration rules;
- Fast Path scope/risk expansion -> escalate and recompute authority/gates rather than continue under reduced ceremony;
- machine-field need -> carry to T-009 rather than implement here.

## Completion

Repository verifier PASS on final exact HEAD + required Fresh Independent Review PASS on same HEAD + focused merge to `version/v4.0.0`.
