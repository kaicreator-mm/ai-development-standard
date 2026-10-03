# Implementation Quality Reference

This reference is non-normative guidance for applying `standards/IMPLEMENTATION_QUALITY_STANDARD.md`.

## Minimal project mapping

A useful implementation-quality mapping identifies only durable project facts:

```text
build_entrypoint:
test_entrypoint:
deterministic_checks:
source_roots:
test_roots:
generated_roots:
generation_authority:
public_contract_surfaces:
secret_safe_configuration_refs:
applicable_language_profile:
applicable_archetype_profile:
```

Do not fill absent items with invented conventions merely to complete the worksheet.

## Examples

A TypeScript repository may map deterministic checks to project-selected formatter/lint/typecheck scripts. A Python repository may map them differently. The Core requirement is discoverability and truthful application, not the tool name.

A generated client can be build output while its IDL/schema remains canonical source. Successful code generation proves the generator accepted the source; it does not prove compatibility, release qualification or that manual edits to generated output are authoritative.

A local developer may have a newer compiler or additional linter installed. That is execution capability, not evidence that the project selected that tool/version.

## Review prompts

1. Are build/test/check commands project-authoritative or merely Agent-local guesses?
2. Are deterministic checks applied only where the selected project/ecosystem supports them?
3. Can a maintainer distinguish canonical source from generated output?
4. Is regeneration authority discoverable?
5. Are public errors/contracts explicit where callers depend on them?
6. Are secrets represented by references/redaction rather than ordinary raw values?
7. Is any tool/check result being promoted into Validation or Release truth?
8. Are language/archetype profiles mapping Core requirements rather than becoming competing owners?

## Failure posture

When ecosystem-specific behavior is unclear, use the applicable profile/project authority. When a check/result question belongs to Testing, CI, Validation or Release, route there rather than extending this standard's authority.
