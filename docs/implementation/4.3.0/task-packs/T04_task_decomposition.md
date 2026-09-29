# T04 — Task Decomposition Standard

Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`
Review: required | Validation: concern | Freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal
Create the normative owner for concern-sized Task decomposition: minimum coherent concern + maximum safe parallelism.

## Allowed write-set
- `standards/TASK_DECOMPOSITION_STANDARD.md`
- `references/TASK_DECOMPOSITION_REFERENCE.md`
- `scripts/test_v43_task_decomposition.py`

## Acceptance
- Task durable facts include primary concern, inputs, output, write-set/ownership, forbidden scope, acceptance, gates, review/validation, integration target, dependencies;
- file-count-only split and giant mixed-authority Task rejected;
- atomic invariant/shared mutable contract cannot be fake-parallelized;
- real code-baseline/stacked dependency remains allowed;
- lane taxonomy remains advisory;
- sibling/central wiring ownership preserved;
- dependency removal cannot be used to fabricate READY;
- existing Task Pack/Issue/Execution Pack objects are extended/referenced rather than duplicated.

## Forbidden
No DAG mutation policy, no duplicate Task schema/state machine, no central Task Pack template rewrite outside narrowly authorized integration Task.

## Reference
`L3_REFERENCE_PACKS.md#t04--task-decomposition-standard`.