# Go Language Profile

```yaml
profile_id: language.go
profile_version: 1
profile_kind: language
applicability: Go module/source/build/runtime concern is material
core_owner_refs:
  - standards/IMPLEMENTATION_QUALITY_STANDARD.md
  - standards/DEPENDENCY_TOOLCHAIN_STANDARD.md
source_or_ecosystem_refs: project go.mod/go.sum, applicable go.work, repository CI/build/test rules
project_check_mappings: project-selected go test/build/vet/race/static checks
high_risk_semantics: modules, toolchain identity, build tags, generated code, concurrency/context/race behavior
compatibility_notes: declared go version, preferred development toolchain and certified build/deployment tuple are different facts
```

Status: v4.3 language mapping, subordinate to Frozen/Core and authorized PROJECT_OVERRIDES. No universally selected Go version, linter or deployment shape.

## Module and toolchain authority

Resolve `go.mod` (module, `go` and optional `toolchain` directives), `go.sum` and `go.work` applicability from durable project facts. These are distinct from the version available on the Agent host. A preferred toolchain or installed `go` binary does not prove the repository's declared compatibility or its exact certified build tuple. Dependencies and exception risk remain with Dependency/Toolchain governance.

## Implementation and checks

Map `go test`, `go build`, `go vet` and race checks only where project concern and supported environment make them material. Build tags, OS/architecture targets, cgo requirements, module/public API compatibility and generated-source regeneration require project-specific mapping. Successful static or unit checks do not automatically prove target-specific runtime, concurrent behavior or release qualification. Concurrency and `context` cancellation/deadline behavior may require focused tests; a race detector result is evidence only for its actual tested tuple.

## Failure/authority boundary

Generated output is not canonical source unless explicitly designated. Fast Path avoids empty Go artifacts when non-applicable. Unsupported compiler/runtime claims remain UNKNOWN until bounded target-specific Validation. Combine independently with an archetype mapping; profile conflict must fail closed to the owning project/architecture authority, never profile file order or Agent-local tool preference.
