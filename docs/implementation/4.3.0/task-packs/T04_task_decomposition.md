# T04 — Task Decomposition Standard

```yaml
task_id: T04
dependencies: []
integration_target: version/v4.3.0
merge_target: version/v4.3.0
allowed_write_set:
  - standards/TASK_DECOMPOSITION_STANDARD.md
  - references/TASK_DECOMPOSITION_REFERENCE.md
  - scripts/test_v43_task_decomposition.py
forbidden_scope:
  - DAG mutation policy
  - duplicate Task schema/state machine
  - central Task Pack template rewrite outside later integration ownership
acceptance:
  - Task facts include concern/inputs/output/write-set/forbidden scope/acceptance/gates/review/validation/target/dependencies
  - file-count-only split and giant mixed-authority Task are rejected
  - atomic invariant/shared mutable contract cannot be fake-parallelized
  - real code-baseline stacked dependency remains allowed
  - lane taxonomy is advisory
  - sibling/central wiring ownership is preserved
required_gates:
  - focused decomposition tests
  - concern Validation
  - Fresh Independent Review
validation_owner: T04
review_policy: required
l3_requirement: docs/implementation/4.3.0/L3_REFERENCE_PACKS.md#t04--task-decomposition-standard
agent_freedom: F1_BOUNDED_IMPLEMENTATION
risk: high
executor_suitability: Strong/Web builder because decomposition defines planning authority boundaries
failure_handling:
  - atomicity/ownership ambiguity => keep concern together or route planning decision upward
  - dependency removal that would fabricate READY => reject/fail closed
```

Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`

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

## Failure handling
If ownership/atomicity cannot be established, decomposition remains unresolved rather than forcing parallelism. Removing a dependency to make work appear ready is a planning defect.

## Forbidden
No DAG mutation policy, no duplicate Task schema/state machine, no central Task Pack template rewrite outside narrowly authorized integration Task.

## Reference
`L3_REFERENCE_PACKS.md#t04--task-decomposition-standard`.
