# <change title>

## Related Work

- Task / Issue: `#<id>`
- Milestone / Version: `<vX.Y.Z>`
- Baseline Commit: `<sha>`
- Standard revision: read `.dev-standard/VERSION`
- Integration target: `<version/vX.Y.Z | main | stack parent branch>`

## Dependency / Branch Topology

- Execution dependencies: `<GitHub Issue Dependencies / none>`
- Branch strategy: `independent | stacked`
- Stack parent PR / branch: `<#pr / branch / NOT_APPLICABLE>`
- Why stacked is required: `<reason / NOT_APPLICABLE>`

Issue Dependency is the canonical Task DAG. Stacked PR is only an optional code-baseline dependency.

## Why

<problem / reason>

## Scope

- In: `<primary concern>`
- Out: `<explicit non-goals if needed>`

## Changes

- <change>

## Contract / Compatibility Impact

`NONE / COMPATIBLE / BREAKING / MIGRATION_REQUIRED`

<details if not NONE>

## Documentation

`UPDATED / NOT_APPLICABLE`

- <authoritative doc path or reason N/A>

## Validation

- Tested SHA: `<sha>`
- Execution environment: `<...>`
- CI profile: `<minimal | custom | disabled>`

| Gate / Tuple | Status | Evidence |
|---|---|---|
| Format | | |
| Lint | | |
| Typecheck | | |
| Unit / Contract | | |
| Integration | | |
| Critical Journeys | | |
| Hidden Validation | | |
| Platform / Production Build | | |
| Minimal CI | | |

Use only `PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`.

For matrix validation, identify exact tuples. A PASS for one SHA/platform/toolchain/profile does not imply another tuple PASS.

## Independent Review

- Required: `YES / NO`
- Review status: `PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`
- Reviewed SHA: `<sha>`
- Reviewer context: `<human / independent session / agent>`
- Review event / evidence: `<Issue/PR comment or review ref>`
- Local validation requested by reviewer: `YES / NO`

In Version Branch Mode, Task/Fix PR review is required by default. Review PASS is valid only for the exact reviewed HEAD SHA. A later commit requires delta or full re-review.

## Failures Found / Root Cause

<none or details>

## Remaining Gates / Blockers

- `<gate → state → reason → downstream impact>`

Do not stop unrelated work solely because one gate is blocked.

## Remaining Issues / Limitations

<none or explicit list>

## Merge Readiness

The PR may enter `state:merge-ready` only when the current merge candidate SHA satisfies the applicable policy:

- required task Validation PASS;
- Independent Review PASS;
- configured required Minimal CI PASS when enabled;
- required upstream Issue dependencies satisfied for merge;
- correct integration target / stack parent;
- no unresolved release-significant blocker/thread.

If a stacked PR is rebased/retargeted and HEAD changes, affected review/validation must be re-established.

## Release Impact

`NO_RELEASE_IMPACT / RELEASE_BLOCKED / RELEASE_READY_REQUIRES_CLOSEOUT`

PR PASS or Minimal CI PASS is not Release PASS.
