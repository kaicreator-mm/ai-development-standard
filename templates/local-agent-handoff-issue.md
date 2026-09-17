# Local Agent Handoff — <version/task> <scope>

## Standard

Read the business project's `.dev-standard/VERSION` and use exactly that immutable `ai-development-standard` revision.

- Standard version: `<semantic-version>`
- Standard revision: `<40-char-sha>`

## GitHub Context

- Repository: `<owner/repo>`
- Version milestone: `<vX.Y.Z or NOT_APPLICABLE>`
- Integration mode: `<version-branch | trunk-fast-path>`
- Integration / target branch: `<version/vX.Y.Z | main | other>`
- Handoff labels: `<type:validation, handoff:local-agent, ...>`

## Baseline

- Branch / Ref: `<branch-or-ref>`
- Baseline commit: `<40-char-sha>`
- Scope / Task IDs: `<ids>`

## Frozen Inputs

- PRD / Scope: `<path/ref>`
- Architecture / Contracts: `<path/ref>`
- Task DAG: `<path/ref>`
- L3 / Implementation Evidence: `<path/ref or NOT_APPLICABLE>`

## Web Completed

- <completed item>

## Existing Validation Evidence

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

- Executor: `<codex | claude-code | other>`
- Host role: `<Ubuntu Build Host | Windows | macOS | GPU host | other>`
- OS / architecture: `<...>`
- Runtime / toolchain: `<...>`
- Required services/devices: `<...>`
- Credentials / secret assumptions: `<none | description without secret values>`
- Required fixtures/data: `<...>`

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
- <issue-specific additions>

## Forbidden Changes

- PRD / product scope
- domain semantics / frozen business rules
- public API/data semantics unless explicitly authorized
- security model / frozen architecture boundary
- weakening required tests or gates
- changing mandatory release gate authority

## Branch / PR Rule

Validation-only execution does not require a branch.

If a source change is required:

- create a dedicated `task/...` or `fix/<version>-<issue>-<scope>` branch;
- target `<integration / target branch>`;
- reference this Issue from the PR;
- rerun affected required gates against the resulting exact SHA.

## Expected Output / Artifacts

1. Final/current HEAD and tested SHA.
2. Final commit / PR if code changed.
3. Validation Report using the pinned standard template.
4. Exact commands + exit codes.
5. Gate matrix and Validation Tuple results.
6. Changed files and fixed failures.
7. Remaining blockers and downstream release impact.
8. `<project-specific artifact>`.

## Completion Rule

This Issue is complete only when:

- all explicitly required gates are PASS and evidence/PR is linked; **or**
- the remaining path is explicitly FAIL/BLOCKED with reproduction, evidence, impact and any upstream decision required.

Do not close the Issue merely because execution stopped.

## Failure / Blocker Reporting Rule

For FAIL/BLOCKED include where available:

```text
exact command
exit code
key logs
reproduction
expected vs actual
root cause/evidence
affected scope
downstream impact
```

Continue independent work when a blocker affects only part of the DAG.

## Local Agent Bootstrap

Use `prompts/local-agent-bootstrap.md` from the pinned standard revision.

Minimal invocation context:

```text
Repository: <owner/repo>
Handoff Issue: #<issue-number>

Read and execute the pinned Local Agent Bootstrap Prompt. Treat this Issue as the task contract and GitHub as the execution fact source.
```
