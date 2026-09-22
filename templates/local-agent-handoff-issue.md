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

If no prior evidence exists, record `NOT_APPLICABLE` explicitly rather than omitting the section from a `HANDOFF_READY` payload.

## Remaining Work

- <only work that remains>

## Validation / Execution

- Validation scope: `<concern|integration|closure>`
- Required gates: `<gate list|NOT_APPLICABLE>`
- Required Validation Tuples: `<exact SHA × environment/platform × runtime/toolchain × profile list|NOT_APPLICABLE>`
- Profile: `<profile>`
- Environment/capabilities: `<requirements|NOT_APPLICABLE>`
- Canonical entrypoints: `<commands/refs|NOT_APPLICABLE>`

## Allowed Changes

- <allowlist|NOT_APPLICABLE>

## Forbidden Changes

- frozen product/architecture/security/public-contract changes unless explicitly authorized
- weakening required gates/tests
- unrelated scope
- <additional constraints|NOT_APPLICABLE>

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

`DRAFT` may be incomplete. `HANDOFF_READY` is valid only after all machine-required completeness fields are present, including Standard version/revision, frozen inputs, existing evidence, required gates/Validation Tuples, execution environment/profile/entrypoints, allowed/forbidden changes, completion/blocker rules and expected outputs. Then publish `ai-dev:event:v2 HANDOFF_READY` with evidence that the machine payload validated and set `HANDOFF_READY`.

An incomplete Issue MUST be repaired before invocation. Missing task-specific detail MUST NOT be supplied only through a longer chat prompt.

After `HANDOFF_READY`, the user-visible worker invocation MUST be pointer-only:

```text
完成 `owner/repo` Issue #N。
```

When role/dispatch disambiguation is required:

```text
执行 `owner/repo` Issue #N 的当前 READY <role> dispatch。
```

The trigger may add only repository, Issue/PR, role and dispatch id when needed. Do not duplicate baseline SHA, branch rules, scope, commands, gates, review procedure, evidence requirements or closeout rules into chat.

Generic worker behavior comes from the pinned repository bootstrap/standard. Do not paste the bootstrap or the Issue contract into the per-task trigger.