# T07 — TypeScript + Python Language Profiles

Depends on: T06
Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`
Review: required | Validation: concern/profile | Freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal
Map the neutral implementation-quality contract to TypeScript and Python ecosystems without converting common tools into universal requirements.

## Allowed write-set
- `profiles/languages/typescript.md`
- `profiles/languages/python.md`
- `scripts/test_v43_ts_python_profiles.py`

## TypeScript acceptance
- manifest/lock/package-manager authority project-resolved;
- Node/runtime compatibility distinct from preferred dev version;
- ESM/CJS/module-resolution risk called out where applicable;
- typecheck/build/runtime/test distinctions explicit;
- generated declarations/output ownership mapped;
- formatter/linter/testing examples remain mappings, not mandates.

## Python acceptance
- `pyproject.toml`/requirements/lock variability recognized;
- interpreter compatibility distinct from preferred dev/runtime;
- packaging/import/environment concerns explicit;
- type/static/test/build tooling project-resolved;
- generated/package output ownership mapped;
- no single environment manager/formatter/type checker mandated.

## Cross-profile negatives
Local installed Node/Python cannot rewrite repository compatibility; profile cannot override Core/Frozen/PROJECT_OVERRIDES authority.

## Local gate
Official/source evidence should suffice. If exact executable profile claims are added that require unavailable Node/Python versions, create a separate exact-subject Validation handoff; do not infer from current Agent host.

## Reference
`L3_REFERENCE_PACKS.md#t07--typescript--python-profiles`.