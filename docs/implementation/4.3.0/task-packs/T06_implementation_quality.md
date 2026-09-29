# T06 — Implementation Quality Standard

Depends on: T02
Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`
Review: required | Validation: concern | Freedom: `F1_BOUNDED_IMPLEMENTATION`

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

## Forbidden
No language-specific profile files, no archetype files, no mandated formatter/linter/build tool, no testing/CI result-state ownership.

## Reference
`L3_REFERENCE_PACKS.md#t06--implementation-quality-standard`.