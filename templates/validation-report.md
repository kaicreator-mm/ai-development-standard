# Validation Report

- Repository: `<owner/repo>`
- Branch / Ref: `<branch-or-ref>`
- Tested SHA: `<40-char-sha>`
- Evidence-only HEAD: `<sha or NOT_APPLICABLE>`
- Standard: `ai-development-standard@v2.0.0` + immutable revision
- Task/Issue: `<id>`
- Execution Host Role: `<ChatGPT env | Ubuntu Build Host | Windows | macOS | self-hosted runner | other>`
- Platform / Architecture: `<...>`
- Runtime / Toolchain: `<...>`
- Validation Profile: `<fast | integration | critical-journey | hidden | platform | release | custom>`
- CI Profile: `<minimal | custom | disabled>`

## Gate Matrix

| Gate / Tuple | Status | Exact Command / Evidence |
|---|---|---|
| Format | PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE | |
| Lint | | |
| Typecheck | | |
| Unit / Contract | | |
| Integration | | |
| Critical Journeys | | |
| Hidden Validation | | |
| Platform / Production Build | | |
| Minimal CI | | |

For matrix validation, identify each tuple explicitly, for example:

```text
<tested SHA> × <real platform> × <runtime/toolchain> × <profile>
```

One tuple PASS never implies another tuple PASS.

## Environment Identity

- OS/version: `<...>`
- Architecture: `<...>`
- Runtime/toolchain versions: `<...>`
- Required service/device identity: `<...>`
- Start/end timestamp: `<...>`

## Changed Files

- `<path>`

## Failures Fixed

- `<symptom → root cause → fix → rerun evidence>`

## Remaining Gates / Blockers

- `<gate → state → reason → downstream impact>`

A blocker only blocks dependent downstream gates. Independent remaining work should continue where possible.

## Known Limitations

- `<none or explicit>`

## Candidate / Release Impact

- Candidate Prepared: `PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE`
- Candidate Freeze: `PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE`
- Hidden Validation Execution: `PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE`
- Release Qualification: `PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE`

Do not infer Release PASS from PR Validation or Minimal CI PASS.
