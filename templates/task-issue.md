# [<Task ID>] <Task title>

## Version / Routing

- Milestone: `<vX.Y.Z>`
- Type: `type:task | type:bug`
- Initial workflow state: `state:planned | state:ready`
- Integration target: `<version/vX.Y.Z | main | stack parent branch>`

## Goal

<what this task must accomplish>

## Scope

### In

- <item>

### Out

- <explicit non-goal>

## Frozen Inputs

- PRD / Scope: `<path/ref>`
- Architecture / Contract: `<path/ref>`
- Planning Task DAG: `<path/ref>`
- L3 / implementation reference: `<path/ref or NOT_APPLICABLE>`
- Standard revision: read `.dev-standard/VERSION`
- Baseline SHA: `<sha>`

## Dependencies

Canonical execution dependencies MUST be represented with GitHub Issue Dependencies.

Human-readable summary:

- Blocked by: `<#issue or none>`
- Blocking: `<#issue or none>`

Do not rely on this text instead of native dependency metadata.

## Code Baseline

- Branch strategy: `independent | stacked`
- Upstream code branch if stacked: `<branch or NOT_APPLICABLE>`
- Reason stacked code baseline is required: `<reason or NOT_APPLICABLE>`

Stacked PR is only for unmerged code-baseline dependency; it does not replace Issue Dependency.

## Acceptance Criteria

- [ ] <criterion>

## Required Task Gates

| Gate | Required | Notes |
|---|---|---|
| Task validation | YES/NO | |
| Independent Review | YES/NO | Version Branch Mode default: YES |
| Minimal CI | YES/NO | per project CI profile |
| Local/platform validation | YES/NO | |

Gate results use only `PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`.

## Allowed Changes

- <allowed scope>

## Forbidden Changes

- Frozen PRD/domain semantics/architecture changes unless explicitly authorized.
- Test/gate weakening merely to obtain green status.
- Unrelated refactor/dependency churn.

## Expected Outputs

- Task branch / PR when source changes are required.
- Exact-SHA validation evidence.
- Independent Review result on the merge candidate SHA.
- Structured agent events in Issue/PR comments when state changes.

## Completion Rule

Task reaches `state:done` only when:

- acceptance criteria are satisfied;
- required dependencies for completion are resolved;
- required task validation is PASS;
- Independent Review is PASS when required;
- configured required CI is PASS when applicable;
- the correct PR has merged to the intended integration target;
- remaining blockers/limitations are explicitly recorded.
