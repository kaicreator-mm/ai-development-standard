# T10 — Adoption & Cross-standard Wiring

```yaml
task_id: T10
dependencies: [T03, T04, T05, T07, T08, T09]
integration_target: version/v4.3.0
merge_target: version/v4.3.0
allowed_write_set:
  - standard-manifest.json
  - selected Task Pack / Execution Pack / project adoption references/templates
  - selected .dev-standard/PROJECT_OVERRIDES.md guidance
  - profile discovery/index wiring
  - scripts/test_v43_adoption_wiring.py
forbidden_scope:
  - semantic redesign of T01-T09
  - new lifecycle state machine
  - repository-wide path refactor or v4.7 unified resolver
acceptance:
  - four normative owners and DAG mutation schema are discoverable
  - profile framework + five language + three archetype profiles are deterministically discoverable
  - Task/Execution Packs consume semantics without duplicate Task object
  - PROJECT_OVERRIDES may select/specialize/strengthen without weakening authority
  - historical adopters remain valid and Fast Path proportional
required_gates:
  - focused adoption/integration tests
  - integration Validation
  - Fresh Independent Review
validation_owner: T10
review_policy: required
l3_requirement: docs/implementation/4.3.0/L3_REFERENCE_PACKS.md#t10--adoption--wiring
agent_freedom: F1_BOUNDED_IMPLEMENTATION
risk: high
executor_suitability: Strong/Web integration owner; mechanical wiring may be delegated
failure_handling:
  - owner/profile conflict => fail closed and route to owning Task/authority
  - historical compatibility ambiguity => preserve historical meaning; do not rewrite evidence
  - need for unified repository resolver => defer to v4.7
```

Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`

## Goal
Integrate v4.3 normative owners, DAG mutation contract and profile mappings into repository discoverability/adoption while preserving existing authority and reserving unified resolver convergence for v4.7.

## Allowed write-set
- `standard-manifest.json`
- selected Task Pack / Execution Pack / project adoption references/templates
- selected `.dev-standard/PROJECT_OVERRIDES.md` guidance
- profile discovery/index wiring
- `scripts/test_v43_adoption_wiring.py`

## Acceptance
- four normative owners discoverable;
- DAG mutation schema discoverable/applicable;
- profile framework + five language + three archetype profiles discoverable deterministically;
- Task Pack/Execution Pack consume decomposition/profile semantics without duplicate Task object;
- PROJECT_OVERRIDES can select/specialize/strengthen within authority;
- no v4.7 unified resolver/repository refactor;
- historical adopters remain valid and Fast Path proportional.

## Failure handling
Authority conflicts and historical-compatibility ambiguity fail closed to their owner; central wiring never resolves them by redefining earlier semantics. Repository-wide resolver needs remain v4.7 scope.

## Forbidden
No semantic redesign of T01–T09; no new lifecycle state machine; no repository-wide path refactor.

## Reference
`L3_REFERENCE_PACKS.md#t10--adoption--wiring`.
