# Rust Language Profile

```yaml
profile_id: language.rust
profile_version: 1
profile_kind: language
applicability: Rust crate/source/build/target concern is material
core_owner_refs:
  - standards/IMPLEMENTATION_QUALITY_STANDARD.md
  - standards/DEPENDENCY_TOOLCHAIN_STANDARD.md
source_or_ecosystem_refs: repository Cargo.toml/Cargo.lock, adopted rust-toolchain file, target/feature/CI configuration
project_check_mappings: project-selected cargo check/test/build/fmt/clippy/security checks
high_risk_semantics: MSRV, features, target triples, unsafe/FFI, generated build-script/output provenance
compatibility_notes: minimum supported Rust version, preferred toolchain and certified target/build tuple are distinct
```

Status: v4.3 language mapping only. This profile does not require a universal Rust toolchain, fmt/clippy policy or release target.

## Cargo and toolchain mapping

Use project-authorized `Cargo.toml`, applicable `Cargo.lock`, optional `rust-toolchain.toml`, feature and workspace configuration. Keep MSRV (minimum supported Rust version) distinct from the developer's selected channel and from exact target-specific certified build/runtime facts. The Agent's installed compiler is execution capability, not authority to narrow compatibility; lockfile policy depends on the project and artifact role.

## Implementation, safety and checks

Map project-selected `cargo check`, `cargo test`, `cargo build`, `cargo fmt`, `cargo clippy` and target/feature matrices only when they are applicable to the task and repository. `unsafe` boundaries, FFI, target-specific features, build scripts and generated files can demand focused contract/failure tests and canonical regeneration evidence. A host-target build or green Clippy run does not establish every supported target, soundness or release qualification. Package publication is not mandatory for every crate or project.

## Failure and composition

Unsupported compiler/MSRV/feature/target claims remain UNKNOWN and require bounded exact-tuple Validation when material. Fast Path permits truthful non-applicability. The language mapping composes independently with archetype mappings and legitimate PROJECT_OVERRIDES without weakening Frozen/Core. Material mapping conflicts route to project/architecture authority, not file order, Agent preference or local tool availability.
