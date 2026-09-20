# Local Agent Handoff — <version/task> <scope>

Use this Issue as the durable handoff contract. When complete, validate the equivalent machine payload against `schemas/local-agent-handoff.schema.json` and emit `HANDOFF_READY`.

## Standard

- Version: `<semantic-version>`
- Revision: `<40-char-sha>`

## GitHub Context

- Repository: `<owner/repo>`
- Issue: `<#N>`
- Role: `<builder|reviewer|validator>`
- Integration target: `<branch>`
- Parent Task/PR: `<refs|NOT_APPLICABLE>`
- Review Policy: `<required|recommended|not-required|NOT_APPLICABLE>`
- Issue Dependencies: `<refs|none>`

## Baseline

- Ref: `<ref>`
- Exact SHA: `<40-char-sha>`
- Scope/Task IDs: `<items>`

## Frozen Inputs

- PRD/Scope: `<ref|NOT_APPLICABLE>`
- Architecture/Contract: `<ref|NOT_APPLICABLE>`
- Task DAG/L3: `<refs|NOT_APPLICABLE>`

## Existing Evidence

| Gate/Tuple | State | SHA | Evidence |
|---|---|---|---|
| <gate> | PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE | <sha> | <ref> |

## Remaining Work

- <only work that remains>

## Validation / Execution

- Validation scope: `<concern|integration|closure>`
- Profile: `<profile>`
- Environment/capabilities: `<requirements>`
- Canonical entrypoints: `<commands/refs>`

## Allowed Changes

- <allowlist>

## Forbidden Changes

- frozen product/architecture/security/public-contract changes unless explicitly authorized
- weakening required gates/tests
- unrelated scope
- <additional constraints>

## Expected Output

1. exact final/tested SHA;
2. actual environment/toolchain and commands;
3. Gate/Validation results;
4. commit/PR if code changed;
5. evidence/result comment;
6. remaining blocker/downstream impact;
7. next route.

## Completion Rule

`<all required gates PASS + evidence linked, or explicit FAIL/BLOCKED with reproduction/impact>`

## Blocker Rule

`<how to report/route blockers>`

## Handoff State

`DRAFT` until all material fields above are complete. Then publish `ai-dev:event:v2 HANDOFF_READY` and set `HANDOFF_READY`.

After `HANDOFF_READY`, invoke the worker with only:

```text
Repository: <owner/repo>
Handoff Issue: #<N>
Role: <role>
Dispatch: <id if used>

Read the pinned standard and current GitHub state. Execute only this handoff.
```

Do not duplicate the Issue contract into chat.
