# v4.3 Profile Scope Evidence

Status: **PLANNING EVIDENCE — strengthens #223 P2 traceability; does not broaden Frozen Product scope**

## 1. Purpose

Record why the initial v4.3 language/archetype profile set is bounded to TypeScript, Python, Go, Java, Rust plus library/service/CLI, and where implementation Tasks should obtain ecosystem facts. Profiles remain mappings/defaults subordinate to Core/Frozen/project authority.

## 2. Language scope

The five initial languages represent distinct mainstream build/type/package/runtime models already relevant to ADS projects and provide useful diversity without trying to catalog every ecosystem.

| Language | Official evidence anchor | Profile concerns justified |
|---|---|---|
| TypeScript | TypeScript Handbook / tsconfig reference — https://www.typescriptlang.org/docs/ | compile/typecheck/module-resolution/generated declaration concerns |
| Python | Python Packaging User Guide / `pyproject.toml` specification — https://packaging.python.org/ | interpreter compatibility, packaging/import/environment and variable lock/manager practices |
| Go | Go Modules Reference — https://go.dev/ref/mod | module/toolchain authority, build/test and generated/concurrency-relevant mappings |
| Java | Java SE documentation — https://docs.oracle.com/en/java/ plus project build authority (Maven/Gradle when selected by repository) | JDK compatibility vs selected runtime, build/test/generated-source boundaries |
| Rust | Cargo Book / Rust toolchain documentation — https://doc.rust-lang.org/cargo/ | Cargo manifest/lock, MSRV vs selected toolchain, feature/target/unsafe mappings |

These anchors justify profile mapping subjects; they do **not** make any named formatter, linter, package manager, build tool or exact runtime version a universal ADS requirement.

## 3. Archetype scope

The initial archetypes are intentionally small and correspond to recurring responsibility shapes already represented in the repository adoption vocabulary:

- **library** — public/package/consumer interface concern without assuming independent deployment;
- **service** — runtime/config/external/deployment applicability without requiring every service to be public or production-deployed;
- **CLI** — command interface/build/package/environment concern without mandating an installer format.

Repository evidence includes `templates/project/.dev-standard/PROJECT_OVERRIDES.md`, whose repository-profile vocabulary already distinguishes library, CLI and service-like/single-service projects. v4.3 therefore maps these established project shapes rather than inventing a large new taxonomy.

## 4. Why other profiles are deferred

Web frontend, worker, SDK, desktop, plugin, mobile and monorepo-specific profiles are not rejected as invalid. They are deferred because the Product acceptance can be proven with the initial set, while adding more profiles would increase maintenance and authority-overlap risk before the composition framework is dogfooded.

New profile families require later evidence that they add material mapping semantics not expressible through language + archetype + PROJECT_OVERRIDES composition.

## 5. Implementation evidence rule

T07–T09 MUST:

1. use official/current ecosystem documentation or repository-authoritative facts for concrete mappings;
2. keep compatibility/supported/preferred/certified toolchain dimensions separate under v4.1 Dependency & Toolchain ownership;
3. avoid copying style guides as normative ADS rules;
4. mark uncertain ecosystem facts `UNKNOWN` or request bounded executable proof rather than inferring from the Agent host;
5. escalate any conflict with Frozen/Core authority instead of resolving it by profile discovery order.

`LOCAL_ENV=NOT_REQUIRED` for this planning evidence. Exact compiler/runtime behavior only needs local validation when a later profile claim materially depends on it and static/official evidence is insufficient.
