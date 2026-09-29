# T02 — Profile Framework

```yaml
task_id: T02
dependencies: []
integration_target: version/v4.3.0
merge_target: version/v4.3.0
allowed_write_set:
  - profiles/README.md
  - scripts/test_v43_profile_framework.py
  - narrowly scoped profile-framework fixtures/reference examples
forbidden_scope:
  - language-specific or archetype-specific profile content
  - normative standards implementation
  - repository-wide v4.7 resolver
  - central PROJECT_OVERRIDES wiring
acceptance:
  - stable profile id/version/applicability/reference conventions
  - deterministic language + archetype + PROJECT_OVERRIDES composition
  - profiles remain mapping/default layers, not normative owners
  - project specialization cannot silently weaken Frozen/Core authority
  - Agent-local tooling cannot become profile authority
  - Fast Path/non-applicable profiles remain lightweight
required_gates:
  - focused profile-framework tests
  - concern Validation
  - Fresh Independent Review
validation_owner: T02
review_policy: required
l3_requirement: docs/implementation/4.3.0/L3_REFERENCE_PACKS.md#t02--profile-framework
agent_freedom: F1_BOUNDED_IMPLEMENTATION
risk: high
executor_suitability: Strong/Web for composition semantics; bounded executor for fixtures/tests
failure_handling:
  - composition ambiguity or authority conflict => fail closed and route to owning Frozen/Core authority
  - need for repository-wide resolver => defer to v4.7; do not expand T02
```

Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`

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

## Failure handling
Ambiguous composition or conflicting authority is not resolved by discovery order. Report the conflict and route to the owning authority. Any requirement for a repository-wide resolver is future v4.7 scope.

## Forbidden
No language-specific or archetype-specific profile content, no standards implementation, no unified v4.7 manifest/resolver, no PROJECT_OVERRIDES central wiring.

## Reference
`L3_REFERENCE_PACKS.md#t02--profile-framework`.
