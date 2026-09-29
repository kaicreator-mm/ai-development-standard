# T08 — Go + Java + Rust Language Profiles

Depends on: T06
Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`
Review: required | Validation: concern/profile | Freedom: `F1_BOUNDED_IMPLEMENTATION`

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

## Local gate
If an exact profile claim requires real compiler/tool behavior unavailable to Web/CI, create per-ecosystem exact Validation handoff. Otherwise official ecosystem/source evidence is sufficient for profile mapping.

## Reference
`L3_REFERENCE_PACKS.md#t08--go--java--rust-profiles`.