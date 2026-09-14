# Codex Handoff — <version/task> <scope>

## Standard

`kaicreator-mm/ai-development-standard@v1.0.0`

## Baseline

- Repository: `<owner/repo>`
- Branch: `<branch>`
- Commit: `<sha>`
- Scope / Task IDs: `<ids>`

## Web Completed

- <completed item>

## Web Validation

| Gate | Status | Evidence |
|---|---|---|
| Format | PASS/FAIL/NOT_RUN/N/A/BLOCKED | |
| Lint | | |
| Typecheck | | |
| Unit | | |
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

## Forbidden Changes

- PRD / product scope
- domain semantics / frozen business rules
- public API/data semantics unless explicitly authorized
- security model / architecture boundary
- weakening required tests or gates

## Expected Output

1. Final commit / PR.
2. Validation Report using the standard template.
3. CI status.
4. If blocked: failing command, reproduction, root cause/evidence, affected scope and release impact.
