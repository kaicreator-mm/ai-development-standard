# CI Evidence Standard

## 1. Purpose

This standard defines a provider-neutral contract for publishing CI / automated validation evidence to an external artifact store such as Google Drive, S3, MinIO, object storage, or another durable evidence backend.

The goal is not to make CI the Release Authority. The goal is to make automated execution evidence:

- exact-SHA bound;
- machine-readable;
- immutable per run;
- cheap to discover and diagnose;
- safe against partial publication and stale-pointer races;
- auditable without downloading large artifacts by default.

This standard inherits the authority and gate semantics from `VALIDATION_STANDARD.md` and `RELEASE_STANDARD.md`.

## 2. Core separation

The contract separates five concerns that MUST NOT be collapsed into one status file:

```text
latest.json
    mutable discovery pointer
        ↓
manifest.json
    immutable run/evidence identity root
        ↓
validation-summary.json
    immutable machine-readable Validation Report
        ↓
SHA256SUMS
    immutable integrity inventory
        ↓
completion.json
    immutable publication commit marker
```

Optional diagnostic/environment/artifact files attach to the immutable run.

Important consequences:

- `latest.json` is a cache/pointer, not authoritative validation evidence.
- `completion.json` says publication completed; it does not mean validation PASS.
- `validation-summary.json` describes one validation profile/tuple; it does not decide release readiness.
- CI provider status is execution metadata, not Release Qualification.

A run may legitimately have:

```text
validation = FAIL
publication = COMPLETE
```

That is a valid and useful evidence record.

## 3. Identity model

Every immutable run MUST have a stable `evidence_id` and exact tested SHA.

Recommended logical identity:

```text
<project>:<workflow>:<provider-run-id>:<attempt>:<40-char-SHA>
```

The run directory SHOULD include enough identity to prevent rerun overwrite, for example:

```text
runs/124-0-0123456789ab/
runs/124-1-0123456789ab/
```

Provider rerun/attempt identity MUST be preserved when the provider can rerun the same pipeline/run number.

Branch/tag names are auxiliary metadata. The exact commit SHA is canonical.

## 4. Recommended storage layout

```text
<root>/
└── <project>/
    └── <workflow>/
        ├── latest.json
        └── runs/
            └── <run-key>/
                ├── manifest.json
                ├── validation-summary.json
                ├── environment.json          # when environment-sensitive
                ├── diagnostic.json           # strongly recommended on FAIL
                ├── SHA256SUMS
                ├── completion.json
                ├── checks/
                ├── reports/
                ├── logs/
                └── artifacts/
```

Do not encode validation outcome such as `-failure` into immutable directory identity. Outcome belongs in evidence content.

A project-level `status-index.json` MAY exist as a discovery cache only when the implementation provides safe concurrent aggregation. It MUST NOT be required by this standard and MUST NOT become Release Authority.

## 5. `manifest.json`

`manifest.json` is the immutable Evidence Identity Root.

It SHOULD include:

```json
{
  "schema": "ai-development-standard/ci-evidence/v1",
  "evidence_id": "project:workflow:124:0:<sha>",
  "project": "project",
  "repository": "owner/repo",
  "commit": "<40-char-sha>",
  "branch": "version/v1.2.3",
  "executor": {
    "provider": "<provider>",
    "pipeline": 124,
    "rerun": 0,
    "workflow": "acceptance",
    "event": "push",
    "raw_status": "success"
  },
  "run_key": "124-0-0123456789ab",
  "validation": "validation-summary.json",
  "environment": "environment.json",
  "inventory": "SHA256SUMS",
  "artifacts": []
}
```

Artifact entries SHOULD include:

```text
name
kind
evidence-relative path
size
sha256
producer check
producer state
validity
```

Artifact validity MUST be consistent with the producer check. A build artifact MUST NOT be treated as valid when its producing build gate was `FAIL`, `BLOCKED`, or `NOT_RUN`.

## 6. `validation-summary.json`

This file is the immutable machine-readable Validation Report for one profile/tuple.

It MUST preserve the standard gate states:

```text
PASS
FAIL
BLOCKED
NOT_RUN
NOT_APPLICABLE
```

Recommended shape:

```json
{
  "schema": "ai-development-standard/validation-summary/v1",
  "evidence_id": "...",
  "subject": {
    "repository": "owner/repo",
    "tested_sha": "<40-char-sha>",
    "branch": "..."
  },
  "validation_tuple": {
    "host_role": "ubuntu-build-host",
    "platform": "linux/x64",
    "runtime": { "node": "v24.x" },
    "profile": "project-linux-minimal"
  },
  "profile_state": "PASS",
  "checks": [],
  "summary": {
    "PASS": 0,
    "FAIL": 0,
    "BLOCKED": 0,
    "NOT_RUN": 0,
    "NOT_APPLICABLE": 0
  }
}
```

Each check SHOULD record:

```text
id
gate
status
exact command
exit code when executed
start/end timestamp or duration
Evidence-relative log/report path
```

Paths in published metadata MUST be relative to the immutable evidence directory and MUST NOT contain host-absolute paths, `..` traversal, or runner-specific temporary roots. Published top-level namespaces such as `logs/...`, `reports/...`, and `artifacts/...` are valid evidence-relative paths; implementations must distinguish those namespaces from any coincidentally named local staging directory. A leaked local staging prefix must be detected by type/path validation and existence checks rather than by globally banning the legitimate `artifacts/...` namespace.

### 6.1 Aggregate profile state

If a profile-level aggregate is emitted, the default deterministic precedence is:

```text
required FAIL       → FAIL
else required BLOCKED → BLOCKED
else required NOT_RUN → NOT_RUN
else                 → PASS
```

`NOT_APPLICABLE` is legitimate only for checks that truly do not apply.

The aggregate means only the state of this validation profile. It MUST NOT be named or interpreted as `release_ready`.

### 6.2 Profile scope

When a CI profile intentionally excludes platform-specific, visual/golden, Critical Journey, Hidden Validation, packaging, or other release gates, the summary SHOULD state that scope explicitly.

A broad repository command that mixes incompatible validation tuples SHOULD be split into profile-appropriate checks rather than producing a low-information blanket failure.

## 7. `environment.json`

Environment identity SHOULD be emitted whenever the result is platform/runtime/toolchain-sensitive.

It MAY include:

```text
host role
OS/platform/release
architecture
runtime versions
toolchain versions
resource snapshot
```

Do not create dozens of tiny environment text files when one structured JSON document provides the same audit value. Reducing object count is preferred for remote stores with metadata/API overhead.

## 8. `diagnostic.json`

A failed profile SHOULD emit a compact diagnostic index so consumers do not need to read full logs first.

Recommended shape:

```json
{
  "schema": "ai-development-standard/diagnostic/v1",
  "evidence_id": "...",
  "failed_checks": [
    {
      "id": "focused-regression",
      "gate": "TEST",
      "exit_code": 1,
      "log": "logs/focused-regression.log"
    }
  ]
}
```

The diagnostic document is an index, not a replacement for raw evidence.

## 9. `SHA256SUMS`

`SHA256SUMS` is the immutable file integrity inventory for the evidence set before `completion.json` is created.

Rules:

1. It SHOULD cover all immutable run files except itself and `completion.json` according to the implementation's declared inventory rule.
2. The inventory MUST be deterministic.
3. The publisher SHOULD verify local hashes before publication.
4. For a remote store, publication SHOULD include a post-upload integrity check appropriate to that backend.

To avoid circular hashing, `completion.json` MUST NOT be included in an inventory whose hash is itself recorded by `completion.json`.

## 10. `completion.json`

`completion.json` is the immutable Evidence Publication Commit Marker.

It MUST be created only after the main evidence set has been generated and successfully verified/published.

Recommended shape:

```json
{
  "schema": "ai-development-standard/evidence-completion/v1",
  "evidence_id": "...",
  "state": "COMPLETE",
  "completed_at": "...",
  "file_count_excluding_completion": 17,
  "total_bytes_excluding_completion": 123456,
  "manifest_sha256": "...",
  "inventory_sha256": "..."
}
```

No `completion.json` means the evidence set is incomplete for consumers, even if some files are visible remotely.

`completion.json` MAY exist for validation PASS, FAIL, BLOCKED, or NOT_RUN profiles if publication itself completed truthfully.

## 11. `latest.json`

`latest.json` is a mutable discovery pointer for one project/workflow.

Recommended shape:

```json
{
  "schema": "ai-development-standard/ci-latest/v1",
  "evidence_id": "...",
  "project": "project",
  "workflow": "acceptance",
  "pipeline": 124,
  "rerun": 0,
  "commit": "<40-char-sha>",
  "branch": "...",
  "profile_state": "FAIL",
  "failed_checks": ["focused-regression"],
  "completed_at": "...",
  "evidence": "runs/124-0-0123456789ab"
}
```

It MAY duplicate a small amount of status data as a performance cache. That duplicated data is non-authoritative.

### 11.1 Update rules

`latest.json` MUST be updated only after:

```text
immutable evidence generated
→ integrity inventory generated
→ immutable evidence uploaded
→ remote integrity check completed
→ completion.json created and uploaded
→ latest.json updated
```

The implementation MUST prevent an older run or older rerun attempt from overwriting a pointer to a newer completed run.

Acceptable mechanisms include:

- workflow-level serialization plus monotonic provider run/attempt comparison;
- compare-and-swap/versioned-object update;
- transactional index service;
- another mechanism with equivalent stale-write protection.

A project-wide mutable status file with multiple independent workflows SHOULD NOT be used unless concurrent updates are safely aggregated.

## 12. Publication transaction

The recommended publication transaction is:

```text
1. Execute validation checks.
2. Generate validation-summary/environment/diagnostic/manifest.
3. Generate approved artifacts only from successful producer gates.
4. Generate SHA256SUMS.
5. Run local Evidence Contract self-verification.
6. Upload immutable evidence excluding completion.json.
7. Verify remote immutable evidence.
8. Generate completion.json.
9. Self-verify again including completion semantics.
10. Upload completion.json and verify it remotely.
11. Generate latest.json.
12. Self-verify latest against the completed run.
13. Perform concurrency-safe / monotonic latest update.
```

A failed publication transaction MUST NOT advertise the run through `latest.json` as completed.

## 13. Consumer read paths and performance

Consumers SHOULD use a tiered read strategy.

### Hot path — current workflow state

```text
latest.json
```

Use for quick questions such as “what is the latest completed acceptance run?”

### Evidence path — authoritative automated validation result

```text
latest.json or exact-SHA lookup
→ manifest.json
→ validation-summary.json
```

### Diagnostic path — failure analysis

```text
diagnostic.json
→ specific report/log only when needed
```

### Audit path — publication/integrity verification

```text
completion.json
→ SHA256SUMS
→ manifest identity/hash cross-check
```

### Artifact path — large payload access

Large binaries SHOULD be downloaded only when the task requires them.

This separation minimizes remote API round trips and large-file transfer.

## 14. Performance and storage hygiene

Implementations SHOULD prefer:

- one structured environment file over many tiny files;
- compact summary/diagnostic JSON before full logs;
- Evidence-relative indexes so consumers never enumerate directories to guess paths;
- compression for cold/raw logs when the consumer can still access a useful text summary;
- short readable tail/excerpt plus compressed full log when useful;
- no large artifact upload for cheap fast/minimal profiles unless the artifact is explicitly needed;
- rich failure evidence, compact success evidence;
- retention policy appropriate to evidence value and release requirements.

Large build/package artifacts SHOULD normally be produced/published only by profiles that actually own those artifacts. A failed or `NOT_RUN` producer MUST NOT leak a stale workspace artifact into published evidence.

Content-addressed blob storage MAY be introduced later for deduplicating large immutable artifacts, but the logical Evidence Contract SHOULD remain independent of the physical backend.

## 15. Exact-SHA lookup

`latest.json` is only a discovery optimization.

When a user asks whether a specific GitHub SHA, candidate, PR head, version branch, or main baseline is validated, the consumer MUST resolve that exact SHA first and locate matching immutable evidence.

The consumer MUST NOT assume the globally latest run corresponds to the requested SHA.

## 16. Consumer verification minimum

Before treating an external evidence run as usable, a consumer SHOULD verify:

```text
completion.json exists and state = COMPLETE
evidence_id matches across manifest/summary/environment/completion
manifest commit == requested/tested SHA
run identity is internally consistent
validation states are valid
referenced logs/reports/artifacts use safe Evidence-relative paths
artifact producer state and validity agree
integrity inventory/hash chain is consistent when audit-grade evidence is required
```

If these checks fail, the evidence is invalid/incomplete even if the CI provider UI says the workflow completed.

## 17. Security

Published evidence MUST NOT contain secrets, tokens, passwords, production credentials, or private user data not explicitly approved for the evidence store.

Publishers SHOULD run an artifact/evidence secret scan before upload.

Credentials for the evidence backend MUST remain in runner secret/config facilities and MUST NOT be written into manifest/log/evidence files.

## 18. Relationship to Release Qualification

This standard improves CI evidence transport and auditability. It does not change release authority.

Therefore:

- CI profile PASS does not imply Release PASS.
- `completion.json` does not imply validation PASS.
- `latest.json` does not prove a requested candidate SHA.
- artifact presence does not imply artifact validity.
- external evidence storage does not replace required Critical Journey, Hidden Validation, real platform/build, or other frozen release gates.

Release Qualification continues to follow `RELEASE_STANDARD.md` and the project's frozen gate authority.

## 19. Reference implementation evidence

The contract was derived and refined through a real self-hosted Woodpecker → Google Drive pilot in `kaicreator-mm/formula`.

The pilot verified, at minimum:

- exact-SHA run identity;
- provider run + rerun identity;
- immutable per-run directories;
- `manifest.json`;
- `validation-summary.json`;
- `environment.json`;
- failure `diagnostic.json`;
- `SHA256SUMS`;
- `completion.json` on a failed validation run;
- workflow-level `latest.json` after completion;
- remote artifact/evidence publication and integrity checking;
- separation of validation failure from successful evidence publication.

Provider-specific command syntax is intentionally not normative. Projects MAY implement the same contract with other CI and storage systems.
