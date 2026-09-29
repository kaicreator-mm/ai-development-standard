# T05 — Task DAG Governance Standard

```yaml
task_id: T05
dependencies: [T01]
integration_target: version/v4.3.0
merge_target: version/v4.3.0
allowed_write_set:
  - standards/TASK_DAG_GOVERNANCE_STANDARD.md
  - references/TASK_DAG_GOVERNANCE_REFERENCE.md
  - scripts/test_v43_task_dag_governance.py
forbidden_scope:
  - new DAG service or Task state vocabulary
  - Product/Architecture override
  - profile semantics
acceptance:
  - planning DAG and live Issue Dependencies are distinct
  - material mutations preserve reason/authority/affected items/old+new topology/impact
  - Task identity cannot absorb materially different work silently
  - dependency removal cannot fabricate readiness
  - PR stack/cherry-pick is not DAG authority
  - T01 schema is consumed without performing native mutation
required_gates:
  - focused DAG-governance tests
  - concern Validation
  - Fresh Independent Review
validation_owner: T05
review_policy: required
l3_requirement: docs/implementation/4.3.0/L3_REFERENCE_PACKS.md#t05--task-dag-governance-standard
agent_freedom: F1_BOUNDED_IMPLEMENTATION
risk: high
executor_suitability: Strong/Web or bounded builder with exact T01 contract; native dependency mutation may require controller/local capability
failure_handling:
  - unavailable native dependency mutation => explicit controller/local handoff; body text is not canonical topology
  - mutation lacking authority/impact => reject and preserve prior live DAG
```

Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`

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
If native dependency mutation is unavailable, create an authorized GitHub/local controller handoff; body text alone is not canonical topology. Invalid/unauthorized mutations fail closed and preserve the prior live DAG.

## Forbidden
No new DAG service, no Task state vocabulary, no Product/Architecture override, no profile semantics.

## Reference
`L3_REFERENCE_PACKS.md#t05--task-dag-governance-standard`.
