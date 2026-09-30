# TypeScript Language Profile

```yaml
profile_id: language.typescript
profile_version: 1
profile_kind: language
applicability: TypeScript source/build/runtime concern is material to the project
core_owner_refs:
  - standards/IMPLEMENTATION_QUALITY_STANDARD.md
  - standards/DEPENDENCY_TOOLCHAIN_STANDARD.md
source_or_ecosystem_refs:
  - repository package.json and selected lockfile, if applicable
  - project tsconfig and build/test/CI entrypoints
project_check_mappings: project-selected typecheck/build/test/static checks
high_risk_semantics: runtime compatibility, ESM/CJS interop, module resolution, generated declaration ownership
compatibility_notes: compatibility range, preferred developer version and certified build/deployment tuple are distinct facts
```

Status: **v4.3 subordinate ecosystem mapping**, not a new normative owner. Applicable Frozen/Core constraints and PROJECT_OVERRIDES specialization govern the concrete project; profile discovery and local tool presence grant no authority.

## Manifest, dependency and runtime mapping

Use the repository-selected `package.json` and relevant lockfile (npm, pnpm, Yarn or another project-authorized mechanism) to locate dependency/tooling truth. A lockfile's existence is evidence of the repository choice only when project facts confirm its authority; the Agent MUST NOT pick a universal package manager or silently replace a lock. Runtime compatibility (for example declared Node support) is not the same as preferred developer Node version or an exact certified build/deployment tuple. The Agent's locally installed Node/npm does not narrow repository compatibility.

## Module, type and generated-output mapping

Where material, read project-selected `tsconfig`, package export/module fields and public API contracts before changing ESM/CJS or module resolution. Distinguish `typecheck`, transpile/build, test and actual runtime execution; one successful step does not establish the others. Generated `.d.ts`, emitted JavaScript and generated clients require explicit canonical-source/regeneration authority when material. Directly editing build output is not proof that the source contract was updated.

## Project-owned checks and Fast Path

Map project-selected type checking, build, test, formatting and lint checks to documented scripts/CI; TypeScript, ESLint, Prettier, Vitest or Jest are examples only, not globally required tools. If the repository has no material TypeScript change, the profile axis may be NOT_APPLICABLE without empty records. If the selected compiler/runtime behavior is uncertain or unavailable, keep the claim UNKNOWN and request bounded exact-tuple Validation instead of inferring from an Agent host.

## Conflict and authority boundary

Compose as Frozen/Core + applicable language mapping + applicable archetype mapping + non-weakening PROJECT_OVERRIDES specialization. Resolve a material conflict through the owning project/architecture decision; never by profile file order. This profile does not own Dependency/Toolchain certification, Testing results, CI execution, Validation PASS, Release or Product architecture.
