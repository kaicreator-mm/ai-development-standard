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

For material shipped public/plugin-facing behavior, implementation evidence MUST distinguish `SOURCE_PRESENT` / `EXPORTED_OR_LOADED` from **actual selected-path invocation and observable contract behavior**. These are explanatory evidence categories, not new workflow/Gate states. An implementation claiming "selected feature supported" when only import/activation occurred must repair the real composition or state the missing integration evidence honestly; applicable Testing/Integration owner alone issues the executable proof. A clean installed public package entrypoint can expose dependency/import breakage hidden by workspace-only tests; include it where the public packaging seam is material. See [DomainHarness #139](https://github.com/kaicreator-mm/domain-harness/issues/139), [#1264](https://github.com/kaicreator-mm/domain-harness/issues/1264), and [#1394](https://github.com/kaicreator-mm/domain-harness/issues/1394).

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

## 11. Material change hygiene

Maintainability and diff hygiene remain enforceable implementation-quality concerns. They are evaluated from durable maintenance and evidence facts — declared scope, change summaries, diff structure, generated-source authority and project check results — not from a universal requirement that a human read every changed line.

When material to maintained intent or evidence, the following mutation patterns are reviewable implementation-quality defects:

- an unnecessary whole-file rewrite or mass comment/doc loss that destroys maintained intent;
- unrelated formatting or generated churn mixed with a semantic change;
- a semantic change hidden outside the declared change scope;
- direct mutation of generated output that ignores its regeneration authority;
- unnecessary public-surface widening or abstraction.

Materiality is judged by maintenance and evidence impact: docs/style churn alone is not automatically a defect. These defect categories bind Agents, tooling and humans equally; they do not introduce a universal human line-by-line review gate and MUST NOT be used to restore one. Automated checks and tests remain the primary quality mechanism, and their passing alone never creates Validation or Release authority.

## 12. Runtime diagnostic logs and actionable failures (v4.19)

For new applications and materially changed startup, execution or error-handling paths, implementations **MUST provide usable diagnostics**, not just a generic failure notice or silent process exit. This is an implementation-quality contract, not a new telemetry provider, logging library or universal CI/Release Gate. Projects that have no meaningful runtime execution (for example documentation-only packages) apply it only to executable paths that exist.

### 12.1 Minimum useful information

For material startup/configuration, initialization, externally visible operation and failure paths, the project MUST make it possible for an authorized operator/developer to identify:

- **what happened** (operation/event, result and stable error classification where practical);
- **where** (service, module/component or execution stage);
- **when** (timestamp for persisted/runtime-emitted log records, with an unambiguous time zone or time basis);
- **which related execution** (request/operation/job correlation ID or equivalent where concurrency, async dispatch or distributed diagnosis makes it material);
- **why or what to do next** (safe cause, violated precondition and actionable recovery/configuration guidance, without inventing a root cause).

Severity SHOULD distinguish debug/information, recoverable warning and actual error/fatal conditions as appropriate; the project may use its ecosystem's existing levels and console/file/system log transport. An error that is handled successfully MUST NOT be represented as a fatal service failure. Log volume, format, retention, rotation and forwarding are proportionate to runtime and project operations; this standard does not prescribe a vendor, collector, JSON schema, tracing stack or universal retention period.

### 12.2 User-facing error versus technical diagnostic

A user/operator-visible error MUST identify the affected action and a meaningful safe reason or next step when known. A developer-visible diagnostic SHOULD add the non-secret exception/cause chain or stack trace and source location when needed to troubleshoot; exposing raw stack traces to untrusted end users is not required and can be unsafe. Both views SHOULD share a stable error/reference ID when correlation is material. Never report success, healthy readiness or completed configuration merely because an exception was caught or logged.

A diagnostic **MUST NOT** consist solely of `Failed`, `Unknown error`, an empty catch, a swallowed exception or an unconditional process exit for a material failure when a more specific safe reason is known. If the cause is genuinely unknown, say so, preserve the error reference and suggest a bounded next troubleshooting step; do not fabricate certainty.

### 12.3 Safety, availability and authority

Logs and exceptions MUST comply with `CONFIGURATION_SECRETS_STANDARD.md` §7 and the applicable privacy rules: do not emit credentials, access tokens, full secret-bearing URLs, raw request bodies or sensitive personal data merely for easier debugging. Redact by default; preserve only the non-secret context necessary to diagnose an incident. Log consumers and sinks cannot create side-effect or Release authority.

When the primary logging sink is unavailable, a service SHOULD make an appropriately safe local/fallback diagnostic visible to an authorized operator where possible rather than failing silently or looping indefinitely. Whether to stop work on a logging failure follows the actual project's security/reliability contract; do not silently downgrade a mandatory audit or authorization log.

### 12.4 Affected-path acceptance

On an applicable changed path, project tests SHOULD cover one successful startup/operation and representative failures: invalid configuration, an external dependency failure, correlation between surfaced error and developer diagnostic where applicable, and redaction of test canaries. Evidence may be local or from the existing selected Testing/Validation profile. Do not impose a new global log snapshot suite or turn a documentation-only change into a runtime test obligation. `TESTING_STANDARD.md` owns the tests; `OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD.md` owns post-activation signal/evidence currentness, not the construction of error messages.
