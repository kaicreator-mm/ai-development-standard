# Execution Contract — T-004 Task Learning Closeout / Template Wiring

> Subordinate to Frozen Product/L2/DAG, Task #511, the T-004 Task Pack blob `00bf08ea3ad64f75d77d7cc36655ce7711310086`, and this exact-base JIT pack. This contract narrows execution; it does not redefine Task Learning evidence semantics (T-001) or Execution Architecture semantics (T-002).

```yaml
task_pack_ref: blob:00bf08ea3ad64f75d77d7cc36655ce7711310086
base_sha: 54a55086a12d406df07eb80706ba14f861101256
base_tree: 781dec96941ac53ce912e27e6196079c2e895819
branch: task/511-v48-task-learning-closeout
integration_target: version/v4.8.0
agent_freedom: F1_BOUNDED_IMPLEMENTATION
public_contracts_fixed:
  - schemas/task-learning-v1.schema.json
  - references/TASK_LEARNING_EVIDENCE_REFERENCE.md semantics
  - standards/EXECUTION_ARCHITECTURE_STANDARD.md
  - Frozen Product/L2/DAG authority and existing Gate ownership
invariants:
  - TASK_LEARNING=NONE_MATERIAL remains the proportional one-line Fast Path
  - material Task Learning is represented by durable evidence references/digests, not copied evidence bodies
  - stale or ambiguous learning never silently becomes current behavioral proof
  - Task Learning never substitutes for Product/Architecture/Task/ADR/Incident/Review/Validation/merge/release authority
  - no private chain-of-thought, hidden evaluator content, secret, credential, or verbose scratch requirement is introduced
  - Execution Pack wiring records closeout requirements/references only and does not acquire T-002 scheduler/currentness/resource semantics
write_set:
  - templates/task-pack.md
  - templates/task-issue.md
  - templates/implementation-pr.md
  - templates/final-closeout.md
  - checklists/pr-review.md
  - templates/execution-pack/EXECUTION_CONTRACT.md
  - templates/execution-pack/REVIEW_CHECKLIST.md
forbidden:
  - any file outside the seven-path write_set
  - Task Learning schema/reference semantic change
  - Execution Architecture or scheduler/admission/resource/Availability/Interchange semantic change
  - test/script/runtime implementation change
  - authority or Gate ownership change
  - self-review, independent Validation claim, merge, Version Closure, or Release Qualification
completion_rule: >-
  Produce one bounded implementation candidate/PR against version/v4.8.0 whose implementation delta changes
  exactly the seven authorized paths, satisfies the T-004 Task Pack acceptance, records Builder evidence and the
  task's own Task Learning closeout outcome, and hands off exact-HEAD concern Validation. Builder completion is
  not Validation PASS, Review PASS, merge authorization, or Release PASS.
blocker_rule: >-
  STOP and publish CONTROLLER_REBIND_REQUIRED or the applicable TASK_PACK_DEFECT/ARCHITECTURE_CONTRADICTION/
  EXECUTION_PACK_INVALID finding if base/currentness/material authority drifts, an eighth path is required, or
  satisfying acceptance would require changing T-001/T-002 semantics or another authority owner.
```

## Implementation order

`Tests/Oracles → Template Contract → Wiring → Failure Handling → Evidence Handoff`.

Do not add or modify test files in T-004. Use the pre-existing regression commands in `TEST_MATRIX.yaml` plus exact-diff/static acceptance inspection. Any discovered missing semantic/test owner is routed upward rather than absorbed.

## Dispatch identity

The Builder must claim from Issue #511 using the pointer-only trigger posted after Issue #636 records `V48_T004_JIT_ADMISSION=READY`. Before edits, re-read #511, this pack, the T-004 Task Pack/L3, and verify the task branch still descends from planning commit and the integration target has not materially invalidated this pack.
