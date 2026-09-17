# CI Evidence Reference Validation

## 1. Purpose

This document records the real reference validation used to derive and refine `standards/CI_EVIDENCE_STANDARD.md`.

Reference project:

```text
repository: kaicreator-mm/formula
branch: task/ci-evidence-contract-pilot
CI provider: Woodpecker
external evidence backend: Google Drive
workflow: ci-evidence
```

The pilot intentionally tested both successful and failing validation/publication paths. A CI provider UI result alone was not accepted as proof; the external evidence directory and pointer were inspected as consumers would inspect them.

## 2. Validation questions

The pilot tested these claims:

1. A run can be bound to exact SHA + provider run + rerun/attempt without overwrite.
2. Validation result and evidence-publication completion are separate states.
3. `manifest.json`, `validation-summary.json`, `environment.json`, `diagnostic.json`, `SHA256SUMS`, and `completion.json` can form one internally consistent immutable run.
4. `latest.json` can remain a small mutable discovery pointer and update only after completed publication.
5. Failed/incomplete publication must not advance `latest.json`.
6. Build artifacts must be published only when their producer check actually PASSed, with producer/provenance recorded.
7. Published paths must be consumer-facing Evidence-relative paths.
8. A profile should not use one broad command that mixes incompatible platform/visual/release validation tuples when a scoped deterministic profile is available.
9. Consumer hot-path reads should not require full logs or large artifacts.
10. Older pipeline/rerun attempts must not overwrite a newer `latest.json` pointer.

## 3. Pilot history

### Pipeline 5 — first structured Evidence run

```text
pipeline: 5
rerun: 0
exact SHA: f0ca5e2de74d60bd97184da9abc0560bfff23d4f
run key: 5-0-f0ca5e2de74d
```

Observed:

- immutable run identity was created correctly;
- manifest / validation-summary / environment / diagnostic / SHA256SUMS were published;
- `completion.json` existed even though validation profile result was FAIL;
- workflow-level `latest.json` was published after completion;
- validation FAIL was caused by a coarse `npm test` aggregate mixing Linux-compatible logic checks with Windows-packaged, visual/golden, and environment-sensitive tests.

Conclusion:

```text
validation FAIL + publication COMPLETE
```

is a legitimate evidence state. The run also showed that validation profile design must preserve Validation Tuple boundaries rather than compress unrelated failures into one low-information aggregate.

### Pipeline 6 — refined profile and negative publication test

```text
pipeline: 6
rerun: 0
exact SHA: 8d20f8c20b9dcc63eadbf2b1bbbdf0b48b2e8897
run key: 6-0-8d20f8c20b9d
```

The profile was split into deterministic Linux-safe checks. Result:

```text
PASS: 9
FAIL: 0
BLOCKED: 0
NOT_RUN: 0
NOT_APPLICABLE: 0
profile_state: PASS
```

`web-build` PASSed and produced `web-next.tar.zst`; the manifest recorded:

```text
producer_check: web-build
producer_state: PASS
valid: true
```

However, the overall workflow failed during Evidence self-verification. Root cause:

- the verifier globally rejected every consumer path beginning with `artifacts/` as if it were a leaked local staging path;
- but `artifacts/web-next.tar.zst` is a legitimate published namespace inside the immutable Evidence directory.

This run did not create a completed publication marker and did not advance the existing `latest.json` pointer. That negative result validated the publication-transaction rule: incomplete publication must not be advertised as latest completed evidence.

Fix:

- distinguish path type/namespace instead of globally banning `artifacts/...`;
- check logs/reports remain consumer-relative;
- allow real artifact paths under the published `artifacts/` namespace;
- keep existence/provenance/hash validation for actual artifact entries.

The same correction was incorporated into `CI_EVIDENCE_STANDARD.md`.

### Pipeline 7 — corrected end-to-end publication

```text
pipeline: 7
rerun: 0
exact SHA: a52914a43bddaf247ccf6e3a764fdf4f52d4142e
run key: 7-0-a52914a43bdd
Woodpecker result: SUCCESS
```

Observed on Google Drive:

- immutable run directory exists;
- `manifest.json` exists;
- `validation-summary.json` exists;
- `environment.json` exists;
- `SHA256SUMS` exists;
- valid build artifact exists;
- `completion.json` exists;
- workflow-level `latest.json` was updated after completion and points to pipeline 7 / exact SHA `a52914a...`;
- no failure checks are advertised by the latest pointer.

This closed the artifact-namespace defect found by Pipeline 6.

### Pipeline 8 — superseded intermediate commit

```text
pipeline: 8
exact SHA: 06ab213e9573134da51933b324612e44982fce7a
status: ERROR / superseded intermediate checkpoint
```

This commit introduced the first monotonic-pointer helper before the full test/workflow integration commit was formed. It is not a validation candidate and is retained only as branch history. No standard conclusion is derived from it.

### Pipeline 9 — monotonic latest-pointer regression

```text
pipeline: 9
exact SHA: 73c5014c2db9a832d8d0c5be335240334f9bae24
status: PENDING at initial report checkpoint
```

This candidate adds deterministic regression cases for:

- newer pipeline → UPDATE;
- older pipeline → STALE;
- same pipeline newer rerun → UPDATE;
- same pipeline older rerun → STALE;
- identical pointer → IDEMPOTENT;
- same pipeline/rerun with conflicting identity → hard failure;
- invalid negative ordering metadata → hard failure.

The final v2.2.0 closeout must update this section with the actual exact-SHA execution result before release.

## 4. Problems found and repaired

### P0-1 — stale/unproven build artifact provenance

Earlier acceptance packaging could archive `web/.next` on a failed pipeline even when the formal `npm run build` step had not successfully produced that directory. Tests could leave `.next` behind, making a stale artifact look like a formal build output.

Repair:

- clear formal build output before the build gate;
- create artifact only when the dedicated producer check exists and is `PASS`;
- record producer check/state and validity in the manifest.

### P0-2 — workflow discovery pointer

`latest.json` is kept at workflow scope and contains only compact discovery/cache data. It is not validation authority and not release authority.

Repair/validation:

- update only after completed immutable publication;
- include exact SHA, provider run/rerun, profile state and immutable run pointer;
- protect against stale overwrite.

A broad Drive filename search initially returned a false negative for `latest.json`; direct traversal of the known workflow root showed the file existed. Consumer implementations should resolve known project/workflow roots or exact evidence identity rather than treating global filename search as an authoritative existence check.

### P0-3 — publication completion marker

`completion.json` is a publication commit marker, not validation PASS.

Validated states include:

```text
Pipeline 5: validation FAIL, publication COMPLETE
Pipeline 6: validation PASS, publication INCOMPLETE
Pipeline 7: validation PASS, publication COMPLETE
```

This distinction prevents partial remote directories from being mistaken for complete evidence.

### P0-4 — machine-readable validation summary

`validation-summary.json` preserves exact SHA, Validation Tuple, profile scope, per-check commands/status/exit code/timing/log path, and aggregate state counts.

The Pipeline 6 profile produced 9/9 PASS while still explicitly excluding release Critical Journey, Hidden Validation, Windows packaged runtime, release packaging, and out-of-tuple visual/golden baselines. This demonstrates why profile PASS must not be named or interpreted as Release PASS.

### P0-5 — consumer-relative paths

The pilot found two opposite path hazards:

- local staging prefixes can leak into metadata and break remote consumers;
- a simplistic validator can accidentally reject the legitimate published `artifacts/...` namespace.

The final rule validates path safety according to metadata type and published namespace rather than string prefix alone.

## 5. Performance observations

The evidence design intentionally separates hot metadata from cold payloads.

Observed representative sizes during the pilot:

```text
latest.json: about 0.5 KB
validation-summary.json: about 5 KB
web build artifact: about 14 MB on the refined run
```

Therefore a current-status query can normally read one compact pointer; a validation query can read pointer + manifest + summary; diagnostic logs and large artifacts remain cold-path reads.

The pilot does not claim a universal latency multiplier because connector/backend latency varies. What is validated is the transfer/object-access shape: routine state inspection no longer requires downloading a multi-megabyte artifact or enumerating raw logs.

## 6. Scope deliberately not made mandatory

The following are optional optimizations, not required v2.2 contract claims:

- project-wide `status-index.json` — optional only with concurrency-safe aggregation;
- content-addressed blob deduplication — future storage optimization;
- compressed full logs — backend/consumer dependent;
- retention policy values — project/backend policy;
- a specific CI provider or storage provider.

Keeping these optional avoids standardizing unvalidated provider-specific behavior.

## 7. Acceptance for the standard

The CI Evidence Contract is acceptable for v2.2.0 only when all of the following are true:

```text
Formula refined Validation Profile PASS
artifact provenance PASS
Evidence self-verification PASS
remote immutable publication PASS
completion publication PASS
latest pointer update PASS
monotonic/stale pointer regression PASS
ai-development-standard verify-standard PASS
standard diff review recorded
```

The exact final reference SHA and standard baseline SHA must be recorded at closeout.
