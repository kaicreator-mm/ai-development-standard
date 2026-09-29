# T05 — Task DAG Governance Standard

Depends on: T01
Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`
Review: required | Validation: concern | Freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal
Create the normative owner for material mutation of the live execution DAG while GitHub Issue Dependencies remain the canonical live topology mechanism.

## Allowed write-set
- `standards/TASK_DAG_GOVERNANCE_STANDARD.md`
- `references/TASK_DAG_GOVERNANCE_REFERENCE.md`
- `scripts/test_v43_task_dag_governance.py`

## Acceptance
- Planning DAG vs live Issue Dependencies distinction explicit;
- mutation classes ADD/SPLIT/MERGE/SUPERSEDE/ADD_DEPENDENCY/REMOVE_DEPENDENCY/CHANGE_LANE/CHANGE_INTEGRATION_OWNER/DEFER represented;
- material mutation requires reason/authority/affected items/old+new topology/scope+release+Task Pack+Review+Validation impact;
- Task identity cannot silently absorb materially different work;
- dependency removal cannot fabricate readiness;
- PR stack/cherry-pick is not DAG authority;
- consumes T01 mutation schema without making schema perform native mutation.

## Failure handling
If native dependency mutation is unavailable, create an authorized GitHub/local controller handoff; body text alone is not canonical topology.

## Forbidden
No new DAG service, no Task state vocabulary, no Product/Architecture override, no profile semantics.

## Reference
`L3_REFERENCE_PACKS.md#t05--task-dag-governance-standard`.