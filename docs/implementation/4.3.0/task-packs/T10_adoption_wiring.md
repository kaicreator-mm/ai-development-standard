# T10 — Adoption & Cross-standard Wiring

Depends on: T03 + T04 + T05 + T07 + T08 + T09
Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`
Review: required | Validation: concern/integration | Freedom: `F1_BOUNDED_IMPLEMENTATION`

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

## Forbidden
No semantic redesign of T01–T09; no new lifecycle state machine; no repository-wide path refactor.

## Reference
`L3_REFERENCE_PACKS.md#t10--adoption--wiring`.