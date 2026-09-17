# Local Agent Handoff — <version/task> <scope>

## Standard

Read the business project's `.dev-standard/VERSION` and use exactly that immutable `ai-development-standard` revision.

- Standard version: `<semantic-version>`
- Standard revision: `<40-char-sha>`

## GitHub Context

- Repository: `<owner/repo>`
- Version milestone: `<vX.Y.Z or NOT_APPLICABLE>`
- Parent Task Issue: `<#issue or NOT_APPLICABLE>`
- Source Review / PR: `<#pr / review event / NOT_APPLICABLE>`
- Integration mode: `<version-branch | trunk-fast-path>`
- Integration / target branch: `<version/vX.Y.Z | main | stack parent | other>`
- Handoff labels/state: `<type:validation, state:validation-needed, handoff:local-agent, ...>`
- Relevant Issue Dependencies: `<#issues / none>`

## Baseline

- Branch / Ref: `<branch-or-ref>`
- Baseline commit: `<40-char-sha>`
- Scope / Task IDs: `<ids>`

## Frozen Inputs

- PRD / Scope: `<path/ref>`
- Architecture / Contracts: `<path/ref>`
- Planning Task DAG: `<path/ref>`
- L3 / Implementation Evidence: `<path/ref or NOT_APPLICABLE>`

GitHub Issue Dependencies are the canonical live execution DAG. A stacked PR, if present, only expresses code-baseline dependency.

## Web / Reviewer Completed

- <completed item>

## Existing Validation / Review Evidence

| Gate / Tuple | Status | SHA | Evidence |
|---|---|---|---|
| Independent Review | PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE | | |
| Format | | | |
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
- target `<integration / target branch>` or the justified stack parent;
- reference this Issue and parent Task from the PR;
- rerun affected required gates against the resulting exact SHA;
- if a previously reviewed PR HEAD changes, route the parent Task back to `state:review-ready` for delta/full re-review.

Do not create a stacked PR unless the source change truly needs an unmerged upstream code baseline.

## Expected Output / Artifacts

1. Final/current HEAD and tested SHA.
2. Final commit / PR if code changed.
3. Validation Report using the pinned standard template.
4. Exact commands + exit codes.
5. Gate matrix and Validation Tuple results.
6. Changed files and fixed failures.
7. Remaining blockers and downstream Issue dependency/release impact.
8. `VALIDATION_RESULT` / `BLOCKER_REPORTED` event when `ai-dev:event:v1` is enabled.
9. `<project-specific artifact>`.

## Completion / Routing Rule

This Handoff Issue is complete only when:

- all explicitly required gates are PASS and evidence/PR is linked; **or**
- the remaining path is explicitly FAIL/BLOCKED with reproduction, evidence, impact and any upstream decision required.

Do not close the Issue merely because execution stopped.

If this handoff was requested by Independent Review and validation PASS:

- publish `VALIDATION_RESULT`;
- route the parent Task back to `state:review-ready`;
- Reviewer closes the Review Gate on the correct exact SHA;
- do not route directly to `state:merge-ready` solely because local validation passed.

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
downstream Issue dependency impact
release impact
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
