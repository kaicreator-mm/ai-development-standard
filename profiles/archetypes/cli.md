# CLI Archetype Profile

```yaml
profile_id: archetype.cli
profile_version: 1
profile_kind: archetype
applicability: command-line interface execution or packaging concern is material
core_owner_refs:
  - standards/IMPLEMENTATION_QUALITY_STANDARD.md
  - standards/CONFIGURATION_SECRETS_STANDARD.md
source_or_ecosystem_refs: project command grammar, entrypoints, argument/error behavior, environment and package rules
project_check_mappings: project-selected command contract, exit-status, invocation, packaging and cross-platform checks
high_risk_semantics: argument/output contract, exit codes, environment/credential handling, non-container package/install identity
compatibility_notes: source execution, built binary/package, installer and target-platform behavior are distinct evidence tuples
```

Status: v4.3 subordinate archetype mapping. CLI does not imply one installer format, shell, package manager, OS or Distribution mechanism.

## Applicability and contracts

Map project-authoritative command names/arguments, stdin/stdout/stderr behavior, exit-code/error contracts, working-directory/environment assumptions and filesystem side effects to existing Testing/Implementation/Config authorities. A command working in an Agent's shell does not prove target-platform packaging/install behavior or grant write authority. Where public commands are supported, compatibility and deprecation claims need the material consumer/baseline tuple.

## Build, package and installation

Separate source invocation, compilation/build output, package/installer identity, optional publication and actual install/upgrade execution. Some CLI projects ship source or an internal script, so universal installer requirements are prohibited. Exact target OS/architecture, runtime/toolchain and distribution method are project-selected; cross-platform claims not executed remain UNKNOWN and require bounded validation rather than host substitution.

## Composition and failure handling

Combine independently with an applicable language profile. PROJECT_OVERRIDES can specialize mapping/defaults but cannot weaken Frozen/Core, invent required installation, change command ownership or promote a green local CLI test into Validation/Release PASS. Material conflicts fail closed to Product/Architecture/project authority, not profile file order. Fast Path avoids irrelevant package/install evidence where truly non-applicable.
