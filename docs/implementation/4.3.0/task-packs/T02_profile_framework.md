# T02 — Profile Framework

Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`
Review: required | Validation: concern | Freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal
Create the lightweight profile information architecture used by language/archetype mappings without implementing the v4.7 repository-wide resolver.

## Allowed write-set
- `profiles/README.md`
- focused profile-framework fixtures/tests, e.g. `scripts/test_v43_profile_framework.py`
- narrowly scoped reference examples owned by this Task

## Acceptance
- stable profile id/version/applicability/reference conventions;
- deterministic composition semantics for language + archetype + PROJECT_OVERRIDES;
- profiles explicitly remain mapping/default layers, not competing normative owners;
- project selection/specialization cannot silently weaken mandatory Frozen/Core authority;
- Agent-local tools/runtime never become profile authority;
- no mandatory profile schema/service unless proven necessary;
- Fast Path/non-applicable profiles remain lightweight.

## Forbidden
No language-specific or archetype-specific profile content, no standards implementation, no unified v4.7 manifest/resolver, no PROJECT_OVERRIDES central wiring.

## Reference
`L3_REFERENCE_PACKS.md#t02--profile-framework`.