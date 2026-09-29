# T09 — Archetype Profiles

```yaml
task_id: T09
dependencies: [T02, T06]
integration_target: version/v4.3.0
merge_target: version/v4.3.0
allowed_write_set:
  - profiles/archetypes/library.md
  - profiles/archetypes/service.md
  - profiles/archetypes/cli.md
  - scripts/test_v43_archetype_profiles.py
forbidden_scope:
  - web/frontend/worker/SDK/desktop/plugin/monorepo profile expansion
  - Product architecture assumptions
  - v4.7 resolver
acceptance:
  - library maps public/package/consumer concerns without mandatory publication
  - service maps runtime/external/config/deployment/observability applicability without mandatory production deployment
  - CLI maps command/build/package/environment concerns without installer mandate
  - archetypes remain mapping/default layers
  - composition conflicts resolve through higher authority, not discovery order
required_gates:
  - focused archetype composition tests
  - concern/profile Validation
  - Fresh Independent Review
validation_owner: T09
review_policy: required
l3_requirement: docs/implementation/4.3.0/L3_REFERENCE_PACKS.md#t09--archetype-profiles
agent_freedom: F1_BOUNDED_IMPLEMENTATION
risk: medium
executor_suitability: bounded lower-cost/Web builder inside frozen three-archetype set; Strong reviewer for authority composition
failure_handling:
  - profile-composition conflict => preserve higher authority and report conflict
  - need for new archetype family => separate Product/evidence input; do not expand T09
```

Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`
Profile evidence: `docs/implementation/4.3.0/PROFILE_SCOPE_EVIDENCE.md`

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

## Failure handling
Composition ambiguity fails closed to the higher authority/project rule. Evidence for a materially new archetype becomes a later Product input rather than silent scope expansion.

## Forbidden
No web frontend/worker/SDK/desktop/plugin/monorepo expansion in this Task; no Product architecture assumptions; no v4.7 resolver.

## Reference
`L3_REFERENCE_PACKS.md#t09--archetype-profiles`.
