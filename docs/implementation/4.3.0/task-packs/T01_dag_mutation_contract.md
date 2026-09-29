# T01 — DAG Mutation Machine Contract

```yaml
task_id: T01
dependencies: []
integration_target: version/v4.3.0
merge_target: version/v4.3.0
allowed_write_set:
  - schemas/dag-mutation-record-v1.schema.json
  - narrowly justified optional refs in existing execution/planning evidence contracts
  - scripts/test_v43_dag_mutation_contract.py
forbidden_scope:
  - Task DAG governance prose
  - GitHub native mutation implementation
  - profile framework or central manifest wiring
acceptance:
  - material mutation identity/class/reason/requesting+approving authority/affected tasks are representable
  - old/new topology and Task Pack/Review/Validation impact are reconstructible
  - REMOVE_DEPENDENCY cannot omit reason/authority
  - no Product/Architecture/Task READY authority or native mutation action is encoded
  - backward-compatible optional integration is preserved
required_gates:
  - focused contract tests
  - concern Validation
  - Fresh Independent Review
validation_owner: T01
review_policy: required
l3_requirement: docs/implementation/4.3.0/L3_REFERENCE_PACKS.md#t01--dag-mutation-machine-contract
agent_freedom: F1_BOUNDED_IMPLEMENTATION
risk: high
executor_suitability: bounded lower-cost/local builder after exact contract freeze; Strong reviewer for semantics
failure_handling:
  - malformed or authority-owning schema semantics => FAIL and repair inside T01
  - conflict with Frozen Product/L2 => ARCHITECTURE_CONTRADICTION; do not redesign locally
```

Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`

## Goal
Implement the single v4.3 machine contract for attributable material live-DAG mutations.

## Allowed write-set
- `schemas/dag-mutation-record-v1.schema.json`
- narrowly justified optional refs in existing execution/planning evidence contracts
- `scripts/test_v43_dag_mutation_contract.py`

## Acceptance
- Draft 2020-12 valid;
- identity/class/reason/requesting+approving authority/affected tasks present for material mutation;
- old/new topology reconstructible;
- Task Pack/Review/Validation impact representable;
- REMOVE_DEPENDENCY cannot omit reason/authority;
- no Product/Architecture/Task READY authority or native mutation action encoded;
- backward-compatible optional integration.

## Failure handling
Schema/verifier failures are T01 defects. Any requirement that would make this schema own live topology or workflow readiness contradicts Frozen scope and must route upward rather than be implemented.

## Forbidden
No Task DAG governance prose, no GitHub mutation implementation, no profile framework, no central manifest wiring.

## Reference
`L3_REFERENCE_PACKS.md#t01--dag-mutation-machine-contract`.
