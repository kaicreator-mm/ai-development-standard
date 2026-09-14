# Version Closure Checklist

Version Closure evaluates the integrated candidate/release baseline. PR PASS is not Release PASS.

## Scope / Tasks

- [ ] Frozen PRD/scope is identified.
- [ ] Task DAG is terminal (`DONE / DEFERRED with approval / NOT_APPLICABLE`).
- [ ] Deferred items explain why they do not block this release.
- [ ] Final intended candidate SHA is recorded.

## Validation Matrix

- [ ] Required Fast/Integration gates pass on the exact candidate SHA.
- [ ] Required platform/runtime/toolchain tuples are explicit.
- [ ] Every required tuple has a truthful state and evidence.
- [ ] Cross-build is not used as real platform PASS unless frozen authority explicitly allows it.
- [ ] Critical Journeys pass.
- [ ] Hidden Validation passes for required blocker scenarios.
- [ ] Required external-service boundary checks pass or are explicitly BLOCKED/NOT_RUN.

## Candidate

- [ ] Candidate Prepared artifacts exist.
- [ ] `CANDIDATE_FROZEN_SHA` is recorded only after required visible gates pass.
- [ ] Hidden Validation execution targets the frozen SHA.

## Delivery

- [ ] Real production/release build gate passes where frozen authority requires it.
- [ ] Install/start/upgrade smoke passes where applicable.
- [ ] Migration/rollback/recovery evidence exists where applicable.
- [ ] Artifact identity/checksum is recorded only when relevant/required.

## Documentation

- [ ] README/docs match shipped behavior.
- [ ] Configuration/environment/migration docs are current.
- [ ] Known limitations are explicit.
- [ ] Release/closeout report links exact-SHA validation facts.

## GitHub / Minimal CI

- [ ] Final baseline exists remotely as immutable commit SHA.
- [ ] Project CI profile (`minimal/custom/disabled`) is recorded.
- [ ] If CI is enabled and required by project policy, the configured minimal checks pass on the relevant commit.
- [ ] If CI is disabled, documented exact-SHA clean validation + review policy was followed.
- [ ] No unreviewed implementation remains only in a local working tree.
- [ ] Issues/milestone state matches actual completion.

## Gate Authority

- [ ] Every mandatory release gate can be traced to Frozen PRD/Contract, Frozen Architecture, PROJECT_OVERRIDES, Task acceptance, or Standard default.
- [ ] No mandatory gate was inferred only from a historical workflow, old script, obsolete artifact or Agent guess.

## Decision

Choose exactly one release verdict:

- `READY` — all frozen mandatory gates PASS; no release blocker.
- `CONDITIONAL` — all mandatory gates pass, but an explicitly accepted non-blocking limitation exists.
- `BLOCKED` — mandatory gate is BLOCKED/NOT_RUN or another release blocker exists.
- `FAIL` — a mandatory gate executed and failed, and no newer valid candidate evidence supersedes it.

A Git tag is optional. Release identity MUST always include the immutable commit SHA.
