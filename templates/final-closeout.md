# Final Closeout — <version>

- Repository: `<owner/repo>`
- Candidate frozen SHA: `<40-char-sha or NOT_RUN/BLOCKED>`
- Final baseline commit: `<40-char-sha>`
- Relevant PRs: `<ids>`
- Development Standard version: `<semantic-version>`
- Development Standard revision: `<40-char-sha>`
- CI profile: `<minimal | custom | disabled>`

## Scope Completion

- PRD / frozen scope: PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE
- Task DAG terminal state: PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE
- Docs synchronized: PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE

## Validation Summary

| Gate / Tuple | Status | Exact-SHA Evidence |
|---|---|---|
| Fast / Full Regression | | |
| Integration | | |
| Critical Journeys | | |
| Hidden Validation | | |
| Required External Boundary | | |
| Platform / Production Build | | |
| Minimal CI | | |

Use only `PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`.

For platform/runtime matrices, list each required Validation Tuple explicitly. One tuple PASS never implies another tuple PASS.

## Task Learning Evidence Index

Record the closeout disposition for completed work items without copying Task Learning evidence bodies.

| Work Item | Result | Durable Evidence Ref(s) / Digest(s) | Currentness |
|---|---|---|---|
| `<#id>` | `<TASK_LEARNING=NONE_MATERIAL | MATERIAL_REFS>` | `<refs | NOT_APPLICABLE>` | `<CURRENT | HISTORICAL_ONLY | NOT_APPLICABLE>` |

Material refs are interpreted under `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`. Missing, ambiguous, mutable, malformed or stale exact-subject/currentness evidence remains historical only and must not be silently rebound as current behavioral proof. This index is evidence/reference material only; it does not replace Product/Architecture/Task/ADR/Incident/Review/Validation/merge/release authority or establish Release Qualification.

## Gate Authority

For every release-blocking gate, record authority:

```text
Frozen PRD / Contract
Frozen Architecture
PROJECT_OVERRIDES
Task acceptance
Standard default
```

Do not create mandatory gates from historical workflows/scripts alone.

## Deferred Items

<explicit non-blocking items and rationale>

## Remaining Blockers

- `<gate → state → reason → downstream impact>`

A blocker only blocks dependent gates; independent preparation work should already be completed where possible.

## Known Limitations

<explicit limitations>

## Decision

`READY / CONDITIONAL / BLOCKED / FAIL`

Reason: <concise evidence-based decision>

## Release Identity

- Immutable commit SHA: `<sha>`
- Tag: `<optional tag or NOT_APPLICABLE>`
- Release/RC: `<optional id or NOT_APPLICABLE>`
- Artifact/package identity/checksum: `<only if applicable/required>`

PR PASS or Minimal CI PASS is not Release PASS.
