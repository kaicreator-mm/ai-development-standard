# T09 — Archetype Profiles

Depends on: T02 + T06
Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`
Review: required | Validation: concern/profile | Freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal
Implement the initial evidence-driven archetype mappings for library, service and CLI without turning archetypes into Product Architecture.

## Allowed write-set
- `profiles/archetypes/library.md`
- `profiles/archetypes/service.md`
- `profiles/archetypes/cli.md`
- `scripts/test_v43_archetype_profiles.py`

## Acceptance
- library: public API/package/consumer compatibility applicability mapped without mandatory publication;
- service: runtime/external/config/deployment/observability applicability mapped without mandatory production deployment;
- CLI: command interface/build/package/environment applicability mapped without universal installer format;
- archetype profile remains a mapping/default layer;
- language+archetype composition conflict resolves through higher authority/project rules, not discovery order;
- no profile explosion beyond frozen initial set.

## Forbidden
No web frontend/worker/SDK/desktop/plugin/monorepo expansion in this Task; no Product architecture assumptions; no v4.7 resolver.

## Reference
`L3_REFERENCE_PACKS.md#t09--archetype-profiles`.