# Workspace & Artifact Reference

This document is non-normative guidance for `WORKSPACE_ARTIFACT_STANDARD.md`.

## 1. Classification examples

| Example | Likely class | Notes |
|---|---|---|
| `src/app.py` | `SOURCE` | Authoritative source input. |
| generated API client intentionally committed | `GENERATED_SOURCE` | Project accepts generated source as source contract. |
| `dist/app.exe` after build | `BUILD_OUTPUT` | Not a release artifact until authorized promotion. |
| compiler cache / npm cache | `CACHE` | Disposable only when truly reconstructable. |
| local Postgres data directory | `RUNTIME_STATE` | Do not delete as cache by location alone. |
| junit XML / screenshots | `TEST_ARTIFACT` | Becomes Validation evidence only through binding/publication. |
| signed exact-SHA validation report | `VALIDATION_EVIDENCE` | Bound to subject/profile/result. |
| candidate package digest selected for release | `RELEASE_ARTIFACT` | Requires authorized release/candidate binding. |
| API token captured in log | `SECRET_MATERIAL` | Stop publication; it is not ordinary test evidence. |

## 2. Build output is not release artifact

Bad reasoning:

```text
`dist/app.tar.gz` exists
therefore release artifact READY
```

Correct reasoning:

```text
build output exists
→ identify exact source/build provenance
→ satisfy owning validation/release prerequisites
→ authorized promotion binds digest to candidate/release identity
→ then treat the bound item as RELEASE_ARTIFACT
```

## 3. Cache is not evidence

A cache entry may prove that some previous process populated it, but not that the current requested SHA/profile executed successfully. The current validation process may consume cache when allowed, yet PASS still comes from actual required execution/evidence.

## 4. Runtime state example

A Docker/Postgres volume under a build workspace may look disposable. If it contains the only state required to reproduce or continue a test/service flow, classify it as `RUNTIME_STATE` until ownership/reconstruction policy says otherwise.

Deleting it simply because disk space is low can destroy unique state.

## 5. Unknown ownership cleanup

Observed:

```text
/tmp/project-output/data.bin
owner=unknown
reconstructability=unknown
```

Correct action:

```text
preserve/isolate/escalate
```

Incorrect action:

```text
rm -rf because it is under /tmp
```

## 6. Validation evidence promotion

A junit file produced by a focused test is initially `TEST_ARTIFACT`. An authorized Validator may publish a Validation Report that references the junit file, exact tested SHA, runtime/toolchain and profile. That durable binding makes the referenced evidence usable as `VALIDATION_EVIDENCE` for that subject.

Copying the junit file to `evidence/` without the binding is insufficient.

## 7. Secret material example

If a browser trace contains cookies or bearer tokens, classify the sensitive portion as `SECRET_MATERIAL`. Redact/separate it before ordinary evidence publication. The fact that the trace is useful for debugging does not waive secret handling.

## 8. Reconstruction example

Safe rebuild claim:

```text
class=BUILD_OUTPUT
owner=task:T05
inputs=source@sha256:... + toolchain profile ref
reconstruction=declared build command/profile
```

Unsafe claim:

```text
looks generated; probably safe to delete
```

## 9. Fast Path

A small docs-only Task may have only `SOURCE` changes and no material artifact projection. It need not enumerate editor temp files or package caches. If the Task produces a candidate package or secret-bearing trace, those facts become material regardless of Fast Path.
