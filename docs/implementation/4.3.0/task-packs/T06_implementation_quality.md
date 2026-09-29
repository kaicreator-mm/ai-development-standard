# T06 — Implementation Quality Standard

```yaml
task_id: T06
dependencies: [T02]
integration_target: version/v4.3.0
merge_target: version/v4.3.0
allowed_write_set:
  - standards/IMPLEMENTATION_QUALITY_STANDARD.md
  - references/IMPLEMENTATION_QUALITY_REFERENCE.md
  - scripts/test_v43_implementation_quality.py
forbidden_scope:
  - language-specific or archetype profile files
  - universal formatter/linter/build-tool mandates
  - Testing/CI/Validation result-state ownership
acceptance:
  - repository-authoritative build/test/check entrypoints are explicit
  - deterministic checks are required only where project/ecosystem supports them
  - source/test/generated ownership and generated regeneration authority are explicit
  - public error/contract and secret-safe behavior are covered where material
  - v4.1 and existing Testing/CI/Validation owners are referenced rather than duplicated
  - profiles remain subordinate mappings
required_gates:
  - focused language-neutral tests
  - concern Validation
  - Fresh Independent Review
validation_owner: T06
review_policy: required
l3_requirement: docs/implementation/4.3.0/L3_REFERENCE_PACKS.md#t06--implementation-quality-standard
agent_freedom: F1_BOUNDED_IMPLEMENTATION
risk: high
executor_suitability: Strong/Web for normative neutral contract; bounded executor for deterministic tests
failure_handling:
  - ecosystem-specific uncertainty => leave to profile/project authority rather than invent universal rule
  - conflict with existing Testing/CI/Validation owner => fail closed and route to owner
```

Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`

## Goal
Create a compact language-neutral implementation-quality baseline and the normative boundary used by language/archetype profile mappings.

## Allowed write-set
- `standards/IMPLEMENTATION_QUALITY_STANDARD.md`
- `references/IMPLEMENTATION_QUALITY_REFERENCE.md`
- `scripts/test_v43_implementation_quality.py`

## Acceptance
- repository-authoritative build/test/check entrypoints;
- deterministic formatter/static/type checks where project/ecosystem supports them;
- source/test/generated ownership/discoverability;
- generated code regeneration/authority explicit;
- public error/contract discipline where material;
- secret-safe logging/config usage;
- composes with v4.1 Dependency/Toolchain, Config/Secrets, Testing/CI/Validation owners instead of duplicating them;
- no universal arbitrary complexity/coverage thresholds;
- profile mappings subordinate to Core/Frozen/project authority.

## Failure handling
Ecosystem-specific ambiguity stays in the relevant profile/project authority. Conflicts with existing Testing/CI/Validation semantics are owner conflicts, not permission to redefine them in this Task.

## Forbidden
No language-specific profile files, no archetype files, no mandated formatter/linter/build tool, no testing/CI result-state ownership.

## Reference
`L3_REFERENCE_PACKS.md#t06--implementation-quality-standard`.
