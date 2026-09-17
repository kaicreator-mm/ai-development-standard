# Codex Handoff — <version/task> <scope>

> Compatibility template. New handoffs SHOULD use `templates/local-agent-handoff-issue.md` plus `prompts/local-agent-bootstrap.md`. Codex is represented with `executor:codex`.

## Standard

Read the business project's `.dev-standard/VERSION` and use exactly that immutable `ai-development-standard` revision.

- Standard version: `<semantic-version>`
- Standard revision: `<40-char-sha>`

## GitHub Context

- Repository: `<owner/repo>`
- Version milestone: `<vX.Y.Z or NOT_APPLICABLE>`
- Integration mode: `<version-branch | trunk-fast-path>`
- Integration / target branch: `<version/vX.Y.Z | main | other>`
- Recommended labels: `type:validation`, `handoff:local-agent`, `executor:codex`, `<gate:...>`, `<env:...>`

## Baseline

- Branch / Ref: `<branch-or-ref>`
- Commit: `<40-char-sha>`
- Scope / Task IDs: `<ids>`

## Frozen Inputs

- PRD / Scope: `<path/ref>`
- Architecture / Contracts: `<path/ref>`
- Task DAG: `<path/ref>`
- L3 / Implementation Evidence: `<path/ref or NOT_APPLICABLE>`

## Web Completed

- <completed item>

## Web Validation

| Gate / Tuple | Status | Tested SHA | Evidence |
|---|---|---|---|
| Format | PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE | | |
| Lint | | | |
| Typecheck | | | |
| Unit / Contract | | | |
| Integration | | | |
| Build Smoke | | | |
| Critical Journey | | | |
| Hidden Validation | | | |
| Platform / Production Build | | | |

## Remaining Work

- <only work that remains>

## Execution Environment

- Executor: `codex`
- Host role: `<Ubuntu Build Host | Windows | macOS | GPU host | other>`
- OS / architecture: `<...>`
- Runtime / toolchain: `<...>`
- Required services/devices: `<...>`
- Required fixtures/data: `<...>`
- Credential assumptions: `<none | description without secret values>`

## Validation Profile

`<fast | integration | critical-journey | hidden | platform | release | custom>`

## Required Gates / Validation Tuples

- [ ] `<exact SHA> × <platform> × <runtime/toolchain> × <profile>`

## Exact Commands / Canonical Entrypoints

```text
<command or project-owned canonical entrypoint>
```

## Allowed Changes

- implementation bug fixes
- dependency/build/platform fixes required by frozen scope
- tests that preserve or strengthen frozen behavior
- documentation synchronization required by the actual change

## Forbidden Changes

- PRD / product scope
- domain semantics / frozen business rules
- public API/data semantics unless explicitly authorized
- security model / architecture boundary
- weakening required tests or gates
- changing mandatory release gate authority

## Branch / PR Rule

Validation-only execution does not require a branch.

If source changes are required:

- create a dedicated task/fix branch;
- target the declared integration branch;
- reference this Issue from the PR;
- rerun affected required gates against the resulting exact SHA.

## Expected Output

1. Final/current HEAD and tested SHA.
2. Final commit / PR if code changed.
3. Validation Report using the pinned standard template.
4. Exact commands + exit codes.
5. Gate matrix / Validation Tuple results.
6. If blocked: reproduction, root cause/evidence, affected scope and release impact.

## Completion Rule

Complete only when all required gates PASS with linked evidence, or the remaining path is explicitly FAIL/BLOCKED with reproduction, evidence, impact and any required upstream decision.

## Bootstrap

Use the pinned `prompts/local-agent-bootstrap.md` with:

```text
Repository: <owner/repo>
Handoff Issue: #<issue-number>
```
