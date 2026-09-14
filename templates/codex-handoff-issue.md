# Codex Handoff — <version/task> <scope>

## Standard

Read the business project's `.dev-standard/VERSION` and use exactly that immutable `ai-development-standard` revision.

- Standard version: `<semantic-version>`
- Standard revision: `<40-char-sha>`

## Baseline

- Repository: `<owner/repo>`
- Branch: `<branch>`
- Commit: `<sha>`
- Scope / Task IDs: `<ids>`

## Frozen Inputs

- PRD / Scope: `<path/ref>`
- Architecture / Contracts: `<path/ref>`
- Task DAG: `<path/ref>`

## Web Completed

- <completed item>

## Web Validation

| Gate | Status | Evidence |
|---|---|---|
| Format | PASS/FAIL/NOT_RUN/NOT_APPLICABLE/BLOCKED | |
| Lint | | |
| Typecheck | | |
| Unit | | |
| Contract | | |
| Integration | | |
| Build Smoke | | |

## Remaining Work

- <only work that remains>

## Required Gates

- [ ] <gate>

## Allowed Changes

- implementation bug fixes
- dependency/build/platform fixes required by the frozen scope
- tests that preserve or strengthen the frozen behavior
- documentation synchronization required by the actual change

## Forbidden Changes

- PRD / product scope
- domain semantics / frozen business rules
- public API/data semantics unless explicitly authorized
- security model / architecture boundary
- weakening required tests or gates

## Expected Output

1. Final commit / PR.
2. Validation Report using the pinned standard template.
3. CI status bound to the actual commit.
4. If blocked: failing command, reproduction, root cause/evidence, affected scope and release impact.
