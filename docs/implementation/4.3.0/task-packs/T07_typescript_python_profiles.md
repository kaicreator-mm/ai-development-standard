# T07 — TypeScript + Python Language Profiles

```yaml
task_id: T07
dependencies: [T06]
integration_target: version/v4.3.0
merge_target: version/v4.3.0
allowed_write_set:
  - profiles/languages/typescript.md
  - profiles/languages/python.md
  - scripts/test_v43_ts_python_profiles.py
forbidden_scope:
  - universal package-manager/formatter/linter/test-tool mandates
  - Core/Frozen/PROJECT_OVERRIDES authority override
  - other language profiles
acceptance:
  - TypeScript manifest/lock/runtime/module/typecheck/build/generated-output concerns are mapped without mandates
  - Python pyproject/requirements/lock/interpreter/packaging/import/static/test/build concerns are mapped without mandates
  - compatibility and preferred/certified toolchain facts remain distinct
  - Agent-local tools cannot rewrite repository authority
required_gates:
  - focused profile tests
  - concern/profile Validation
  - Fresh Independent Review
validation_owner: T07
review_policy: required
l3_requirement: docs/implementation/4.3.0/L3_REFERENCE_PACKS.md#t07--typescript--python-profiles
agent_freedom: F1_BOUNDED_IMPLEMENTATION
risk: medium
executor_suitability: bounded lower-cost/local builder using official TypeScript/Python evidence; Strong reviewer for authority mapping
failure_handling:
  - unsupported ecosystem fact => UNKNOWN or bounded Validation request; do not infer from host
  - profile/Core conflict => Core/Frozen/project authority wins; report conflict
```

Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`
Profile evidence: `docs/implementation/4.3.0/PROFILE_SCOPE_EVIDENCE.md`

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

## Failure handling
Unsupported or version-sensitive ecosystem claims remain `UNKNOWN` or create bounded Validation requests. No profile may resolve an authority conflict by using whatever tool exists on the Agent host.

## Local gate
Official/source evidence should suffice. If exact executable profile claims are added that require unavailable Node/Python versions, create a separate exact-subject Validation handoff; do not infer from current Agent host.

## Reference
`L3_REFERENCE_PACKS.md#t07--typescript--python-profiles`.
