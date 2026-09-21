# CI Execution Standard

## 1. Purpose

This standard defines the execution contract for CI and other automated clean-checkout validation runners.

It answers a different question from `CI_EVIDENCE_STANDARD.md`:

```text
CI Execution Standard = where / how a run executes
CI Evidence Standard  = how run evidence is identified / published / consumed
Validation Standard   = what gates are required and what PASS means
Release Standard      = what evidence is sufficient for release qualification
```

These concerns MUST NOT be collapsed.

A workflow can have correct validation commands but still be invalid for a selected runner/backend when its execution semantics are wrong. A provider status can also be green while required non-CI validation remains `NOT_RUN`.

## 2. Project CI Execution Profile

Every project whose CI profile is `minimal` or `custom` SHOULD declare an auditable CI Execution Profile in `.dev-standard/PROJECT_OVERRIDES.md`.

At minimum the profile SHOULD identify:

```text
CI provider
backend / execution model
runner role
authoritative workflow config path
workflow config source semantics
execution shell or entrypoint model
runtime/toolchain source
clone/checkout model when provider defaults are material
fresh-run / rerun policy
```

The declaration describes semantics, not secrets. Tokens, credentials, private URLs, runner registration secrets and other sensitive values MUST NOT be stored in project overrides.

Provider-specific absolute executable paths MAY be declared by a project when they are part of the real runner contract, but MUST NOT become global standard requirements.

Shared/self-hosted runners SHOULD also have a Runner Capability Profile following `CI_RUNNER_CAPABILITY_STANDARD.md`. That profile supports routing and environment selection; it does not replace run-time preflight or Validation Evidence.

## 3. Backend Semantics Are Part of the Contract

Pipeline DSL fields are interpreted by the selected provider and backend. Projects and Agents MUST NOT assume that syntax has container semantics unless the selected backend actually provides them.

Examples of materially different execution models include:

```text
container backend
host/local backend
hosted VM runner
shell executor
Kubernetes/pod backend
remote build service
```

A field named `image`, `services`, `volumes` or `plugin` may have different meaning or support depending on the backend.

Therefore:

1. provider + backend MUST be known before editing provider-specific workflow syntax;
2. a workflow valid for one backend MUST NOT be assumed valid for another backend;
3. backend changes require re-validation of workflow execution semantics;
4. provider documentation and a real runner execution are authoritative over assumptions based on another CI system.

## 4. Workflow Configuration Identity

The exact source SHA remains the canonical code identity, but automated validation also depends on execution configuration.

When practical, automated evidence SHOULD record:

```text
workflow config path
workflow config source SHA or equivalent immutable identity
provider
backend / execution model
runner role
```

A workflow path alone is insufficient when the provider can execute a stored/snapshotted workflow definition that differs from the current repository file.

The workflow configuration identity is execution provenance. It does not replace the Validation Tuple:

```text
<exact SHA> × <real platform/environment> × <runtime/toolchain> × <validation profile>
```

## 5. Fresh Pipeline vs Rerun

A rerun/restart of an existing provider run is not equivalent to creating a fresh run for the current branch or PR HEAD.

Rules:

1. A new exact source SHA requires a run whose tested subject resolves to that SHA.
2. Rerunning an old-SHA pipeline MUST NOT be used as evidence for a newer SHA.
3. If workflow configuration changed, a rerun is usable only when the provider is proven to resolve the intended new configuration; otherwise create a fresh pipeline/run.
4. Rerun is appropriate for the same SHA and execution subject when recovering from a transient infrastructure failure or when the provider intentionally preserves attempt history.
5. Evidence MUST preserve provider run + attempt/rerun identity when available.

Before diagnosing a repeated failure after a workflow fix, compare at least:

```text
expected PR/branch HEAD SHA
provider run tested SHA
provider run/attempt identity
workflow configuration identity/source
```

Do not repeatedly restart an obsolete run and interpret the unchanged failure as proof that the new workflow is ineffective.

## 6. Clone / Checkout Contract

Minimal CI SHOULD start from a clean checkout of the intended exact SHA.

Clone optimizations and optional repository features can alter failure modes. Projects SHOULD make material settings explicit when provider defaults are unsafe or unnecessary, including as applicable:

```text
clone depth
partial clone/filtering
submodule recursion
Git LFS
sparse checkout
credential persistence
```

Rules:

- enable submodules only when the repository requires them;
- enable Git LFS only when the repository uses it;
- partial clone/filtering SHOULD be disabled when the selected Git/provider/plugin combination cannot reliably materialize the required tree;
- clone plugin/entrypoint semantics MUST match the selected backend;
- checkout logs SHOULD make the tested SHA discoverable.

A clone failure is infrastructure/execution evidence, not project-test PASS or FAIL.

## 7. Execution Environment Preflight

Before expensive project validation, CI SHOULD perform a small deterministic preflight appropriate to the execution model.

The preflight SHOULD establish enough facts to diagnose runner mismatch, for example:

```text
exact checked-out SHA
provider/backend/runner role when available
working directory
shell/entrypoint availability
required runtime/toolchain versions
required executable availability
```

Typical runtime checks MAY include commands such as:

```text
git rev-parse HEAD
node --version
npm --version
python --version
java -version
```

Use only commands relevant to the project.

A deterministic workflow defect such as selecting a non-existent local executable is a real CI execution failure. Do not classify it as project validation PASS. If the required execution environment itself cannot currently be provisioned because of an external prerequisite, record the affected required gate according to `VALIDATION_STANDARD.md` (`BLOCKED` or `NOT_RUN` as applicable).

## 8. Local / Host Backend Rules

For local/host/shell backends, the runtime usually comes from the runner host rather than an isolated container image.

Projects using such a backend SHOULD explicitly declare:

```text
runner host role
shell/entrypoint model
runtime/toolchain source
required runtime/toolchain versions
provider-specific local plugin/clone mechanism when applicable
```

The project SHOULD verify the host-provided runtime version before dependency installation and tests.

Do not encode one machine's absolute executable paths into the global standard. If absolute paths are required by the provider/backend, keep them in the project workflow/override or infrastructure configuration and validate them on the real runner.

## 9. Container Backend Rules

For container-based backends, project workflows SHOULD pin or constrain images/toolchains enough to make the Minimal CI result reproducible.

Container execution does not automatically prove real-host/platform gates. A Linux container on a Linux runner is not evidence for Windows/macOS/device/platform tuples unless frozen authority explicitly defines that tuple as sufficient.

## 10. Minimal CI Execution Order

A useful default ordering is:

```text
clean checkout
→ execution environment preflight
→ dependency bootstrap
→ standard/project verifier
→ format/lint/typecheck subset
→ fast unit/contract smoke
→ basic build smoke
→ evidence publication when configured
```

Projects MAY customize the order where dependencies require it, but SHOULD keep cheap configuration/runtime failures ahead of expensive validation.

## 10a. Local-first execution

When an authorized equivalent local execution environment exists, the default engineering loop is local-first:

```text
implement locally
→ focused tests
→ lint/typecheck/build
→ required tests
→ package check
→ task-owned platform validation
→ stable exact HEAD
→ push
→ required remote certification only
```

Remote CI SHOULD NOT be used as the normal compile/debug loop. However:

```text
provider-specific attestation remains mandatory when explicitly required
CI outage != PASS
local Ubuntu evidence != Windows/device evidence
task validation != version closure validation
```

Distinguish three facts that MUST NOT be collapsed:

```text
required validation profile          (what must be proven)
normal execution provider            (where it normally runs; CI or local host)
provider-specific attestation        (provider-bound proof that cannot be substituted)
```

Alternate-executor substitution and `CI_INFRA_EXCEPTION` remain governed by `VALIDATION_STANDARD.md`. Baseline refresh ordering (validate blocking candidates before spendable-obsolete ones) is governed by `EXECUTION_ARCHITECTURE_STANDARD.md` §6.

## 11. Relationship to Evidence and Gate States

Provider job status is execution metadata. Gate state remains governed by `VALIDATION_STANDARD.md`.

Examples:

```text
workflow cannot start because configured local executable does not exist
→ CI execution FAIL; required Minimal CI is not PASS

old SHA rerun succeeds after current HEAD changed
→ historical PASS for old SHA only

project tests PASS but evidence publication fails
→ validation may PASS; evidence publication incomplete

CI PASS but required Windows real-host tuple NOT_RUN
→ CI PASS does not make release PASS
```

When external evidence publication is enabled, use `CI_EVIDENCE_STANDARD.md` and include execution provenance where useful.

## 12. Provider-Specific References

Provider-specific examples are non-normative references. They demonstrate one valid mapping of this standard and MUST NOT be copied blindly into another backend.

A validated Woodpecker Local Backend case is documented in:

- `references/WOODPECKER_LOCAL_BACKEND_REFERENCE.md`

A capability snapshot for the same Ubuntu runner role is documented in:

- `references/WOODPECKER_UBUNTU_BUILD_01_CAPABILITY_2026-09-18.yaml`

Runner capability semantics are defined in:

- `standards/CI_RUNNER_CAPABILITY_STANDARD.md`

The normative rule is the execution/capability contract above, not any particular Woodpecker path or command.
