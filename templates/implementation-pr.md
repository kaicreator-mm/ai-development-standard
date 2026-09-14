# <change title>

## Related Work

- Task / Issue: `#<id>`
- Baseline Commit: `<sha>`
- Standard revision: read `.dev-standard/VERSION`

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

## Failures Found / Root Cause

<none or details>

## Remaining Gates / Blockers

- `<gate → state → reason → downstream impact>`

Do not stop unrelated work solely because one gate is blocked.

## Remaining Issues / Limitations

<none or explicit list>

## Release Impact

`NO_RELEASE_IMPACT / RELEASE_BLOCKED / RELEASE_READY_REQUIRES_CLOSEOUT`

PR PASS or Minimal CI PASS is not Release PASS.
