# Version Closure Checklist

Version Closure evaluates the integrated `main`/release baseline. PR PASS is not Release PASS.

## Scope / Tasks

- [ ] Frozen PRD/scope is identified.
- [ ] Task DAG is fully terminal (`DONE / DEFERRED with approval / NOT_APPLICABLE`); no hidden TODO remains.
- [ ] Deferred items explain why they do not block this release.
- [ ] Final baseline commit SHA is recorded.

## Regression

- [ ] Fast/full regression required by project policy passes.
- [ ] Integration gates pass.
- [ ] Critical Journeys pass.
- [ ] Hidden Validation passes for required P0/P1 scenarios.
- [ ] Required external-service boundary checks pass or are explicitly BLOCKED/NOT_RUN.

## Delivery

- [ ] Real production/release build or package gate passes.
- [ ] Install/start/upgrade smoke passes where applicable.
- [ ] Migration/rollback/recovery evidence exists where applicable.
- [ ] Artifact identity/checksum is recorded when relevant.

## Documentation

- [ ] README/docs match shipped behavior.
- [ ] Configuration/environment/migration docs are current.
- [ ] Known limitations are explicit.
- [ ] Release/closeout report links validation and CI facts.

## GitHub / CI

- [ ] Final baseline exists remotely as an immutable commit SHA.
- [ ] Required GitHub CI on the relevant final commit is green.
- [ ] No unreviewed implementation remains only in a local working tree.
- [ ] Issues/milestone state matches actual completion.

## Decision

Choose exactly one:

- `READY` — required gates PASS; no release blocker.
- `CONDITIONAL` — required gates pass, but explicitly accepted non-blocking limitation exists.
- `BLOCKED` — blocker exists or required gate is FAIL/NOT_RUN/BLOCKED.

A Git tag is optional. The release identity MUST always include the immutable commit SHA; a tag/release name may be added as a human-friendly alias.
