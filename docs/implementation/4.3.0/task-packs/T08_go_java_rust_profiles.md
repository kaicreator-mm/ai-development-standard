# T08 — Go + Java + Rust Language Profiles

```yaml
task_id: T08
dependencies: [T06]
integration_target: version/v4.3.0
merge_target: version/v4.3.0
allowed_write_set:
  - profiles/languages/go.md
  - profiles/languages/java.md
  - profiles/languages/rust.md
  - scripts/test_v43_go_java_rust_profiles.py
forbidden_scope:
  - universal ecosystem tool/style mandates
  - Core/Frozen/PROJECT_OVERRIDES authority override
  - non-Go/Java/Rust language profiles
acceptance:
  - Go module/toolchain/build/test/generated/concurrency concerns are mapped
  - Java JDK/build/test/static/generated-source concerns are mapped without Maven/Gradle mandate
  - Rust Cargo/MSRV/features/targets/unsafe concerns are mapped without local-toolchain authority
  - compatibility/preferred/certified/deployment facts remain distinct
required_gates:
  - focused profile tests
  - concern/profile Validation
  - Fresh Independent Review
validation_owner: T08
review_policy: required
l3_requirement: docs/implementation/4.3.0/L3_REFERENCE_PACKS.md#t08--go--java--rust-profiles
agent_freedom: F1_BOUNDED_IMPLEMENTATION
risk: medium
executor_suitability: bounded lower-cost/local builder using official Go/Java/Rust evidence; Strong reviewer for authority mapping
failure_handling:
  - exact compiler/runtime claim not statically established => UNKNOWN or per-ecosystem Validation handoff
  - profile/Core conflict => report and preserve higher authority
```

Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`
Profile evidence: `docs/implementation/4.3.0/PROFILE_SCOPE_EVIDENCE.md`

## Goal
Map neutral implementation requirements to Go, Java and Rust ecosystems without style-guide duplication or Agent-local authority.

## Allowed write-set
- `profiles/languages/go.md`
- `profiles/languages/java.md`
- `profiles/languages/rust.md`
- `scripts/test_v43_go_java_rust_profiles.py`

## Go acceptance
- `go.mod`/toolchain/module authority mapping;
- standard test/build/check examples project-resolved;
- race/context/concurrency and generated-code risks represented;
- no local Go version -> repo compatibility inference.

## Java acceptance
- JDK compatibility vs selected dev/deployment identity distinct;
- Maven/Gradle/project build authority mapped without universal choice;
- test/build/static/generated-source boundaries represented.

## Rust acceptance
- Cargo manifest/lock, MSRV vs preferred toolchain, features/targets and unsafe semantics represented;
- fmt/clippy/test examples stay project-selected mappings;
- no local toolchain presence -> MSRV/compatibility authority.

## Failure handling
Exact ecosystem behavior that is not established by official/source evidence remains `UNKNOWN` and may create a per-ecosystem Validation handoff. A profile cannot resolve a conflict by weakening Core/Frozen/project authority.

## Local gate
If an exact profile claim requires real compiler/tool behavior unavailable to Web/CI, create per-ecosystem exact Validation handoff. Otherwise official ecosystem/source evidence is sufficient for profile mapping.

## Reference
`L3_REFERENCE_PACKS.md#t08--go--java--rust-profiles`.
