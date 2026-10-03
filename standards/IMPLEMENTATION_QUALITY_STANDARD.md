# Implementation Quality Standard

Status: **Normative — v4.3**

## 1. Purpose

This standard defines a language-neutral implementation-quality baseline. It states what a project must make explicit so an implementation can be built, checked, reviewed and maintained without turning language or ecosystem conventions into universal policy.

It does not own Testing, CI, Validation, Release, Dependency/Toolchain, Config/Secrets, or language/archetype profile semantics. Those owners are referenced where applicable.

## 2. Repository-authoritative entrypoints

A repository MUST make the applicable build, test and deterministic check entrypoints discoverable from durable project facts such as manifests, documented commands, CI configuration, project scripts or project overrides.

An Agent's locally installed tool, IDE action or preferred command MUST NOT become project authority merely because it works on one host.

If multiple entrypoints exist, the project MUST identify which are authoritative for the relevant concern or route ambiguity to project authority.

## 3. Deterministic checks

Projects SHOULD use deterministic formatter, static-analysis, lint, type-check or equivalent checks when the selected ecosystem and project support them materially.

This standard does not mandate one formatter, linter, compiler, type checker, warning policy, coverage threshold, complexity threshold or build system globally.

A missing ecosystem mechanism MUST NOT be replaced by a fabricated universal check. Profiles may map these neutral requirements to ecosystem-specific defaults.

## 4. Source, tests and generated material

Material source, test and generated-file ownership MUST be discoverable when ambiguity could cause unsafe edits.

Generated material MUST identify its regeneration authority or canonical source when the distinction is material. Editing generated output directly does not make that output canonical authority.

The following inference is forbidden:

`generated file changed successfully -> canonical source and regeneration contract are satisfied`.

## 5. Public contracts and errors

When implementation behavior is externally or cross-module observable, public contracts and error behavior MUST be explicit enough for callers and tests to distinguish supported outcomes from technical failures.

Implementation convenience MUST NOT silently narrow an existing compatibility contract or convert technical failure into a successful domain result. Interface compatibility remains owned by the applicable compatibility authority.

## 6. Secret-safe implementation behavior

Implementations MUST preserve Config/Secrets authority. Ordinary source, logs, fixtures, examples or durable evidence MUST NOT require raw secret values when stable references, identities or redacted representations suffice.

`command succeeded with credential present -> side-effect authority granted` is forbidden.

## 7. Composition with existing owners

Implementation quality composes with existing owners rather than duplicating them:

- Dependency/Toolchain owns selected dependency and toolchain truth;
- Config/Secrets owns secret identity and handling boundaries;
- Testing owns test strategy and evidence requirements;
- CI owns automated workflow/check execution posture;
- Validation owns exact-subject validation claims;
- Release owns release qualification;
- language/archetype profiles map this language-neutral baseline to ecosystem/project-shape facts.

A check passing under one owner MUST NOT manufacture PASS under another owner.

## 8. Profile boundary

Language and archetype profiles are subordinate mapping/default layers. They MAY name manifests, standard ecosystem commands, generated-source conventions and common checks, but they MUST NOT weaken Frozen/Core or project authority and MUST NOT manufacture a new universal requirement.

Project overrides may specialize or strengthen applicable mappings; unresolved material conflicts fail closed to the owning project/architecture decision.

## 9. Fast Path and proportionality

Small or non-code changes need not instantiate irrelevant implementation-quality ceremony. Fast Path reduces non-material work; it does not permit bypassing a material build, test, contract, generated-source, secret or public-interface obligation.

## 10. Failure handling

If an ecosystem-specific question is unresolved, route it to the applicable language/archetype profile or project authority rather than inventing a universal rule.

If this standard conflicts with an existing Testing, CI, Validation, Release, Dependency/Toolchain or Config/Secrets owner, fail closed and route to that owner. Do not redefine the owner here.
