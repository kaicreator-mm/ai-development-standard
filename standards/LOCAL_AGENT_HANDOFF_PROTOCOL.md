# Local Agent Handoff Protocol

## 1. Purpose

A Local Agent Handoff transfers a bounded execution or validation work item from ChatGPT Web or another planning/review agent to a coding/execution agent running in a more complete environment.

Supported executors include Codex, Claude Code, other coding agents, a Build Host agent, or an equivalent trusted execution agent.

The GitHub Issue is the handoff contract. Chat history is not required for execution.

When the handoff belongs to a Task workflow, the Local Agent MUST preserve the GitHub Agent Interaction semantics in `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`, including the Task's declared Review Policy.

## 2. Issue naming / metadata

Recommended title:

```text
[<version-or-task>] Local Agent Handoff — <validation/fix scope>
```

For validation-focused work, recommended labels include:

```text
type:validation
state:validation-needed
handoff:local-agent
```

Add executor labels when known:

```text
executor:codex
executor:claude-code
```

Add gate/environment labels as applicable, for example:

```text
gate:integration
gate:platform
gate:hidden
env:ubuntu-build-host
env:windows
env:macos
env:gpu
release-blocker
blocked:environment
```

Use a version Milestone such as `vX.Y.Z` when the repository uses milestones. Do not create a unique version label merely to encode the version.

A Validation Issue MAY be a sub-issue of its parent Task to express hierarchy. If its completion actually blocks another Task/Candidate, use Issue Dependency for the blocking relationship; sub-issue hierarchy alone is not blocking semantics.

## 3. Required issue contract

Every handoff issue MUST identify:

- Standard Version + immutable Standard Revision
- Repository
- Integration Branch / Target Branch
- Baseline Commit
- Parent Task Issue when applicable
- Parent Task Review Policy when applicable
- Scope / Task IDs
- Frozen Inputs: PRD / Architecture / Contract / Task DAG as applicable
- Web/Reviewer Completed
- Existing Validation / Review Evidence
- Remaining Work
- Required Gates / Validation Tuples
- Execution Environment
- Validation Profile
- Exact Commands or canonical project command entrypoints when known
- Required services / fixtures / credentials assumptions
- Allowed Changes
- Forbidden Changes
- Expected Output / Artifacts
- Completion Rule
- Failure / Blocker Reporting Rule

A handoff MUST be executable from the Issue plus repository facts without requiring hidden chat context.

## 4. Baseline discipline

The Issue MUST pin an exact baseline commit SHA.

The execution agent MUST:

1. read repository `AGENTS.md`;
2. read `.dev-standard/VERSION` and `.dev-standard/PROJECT_OVERRIDES.md`;
3. resolve the exact pinned standard revision;
4. read the complete handoff Issue and parent Task/PR when applicable;
5. read relevant Issue Dependencies, workflow state and Review Policy;
6. checkout the specified baseline commit;
7. run `git status` and `git log -1 --oneline` or equivalent checks;
8. record any baseline drift before changing code.

The agent MUST NOT silently replace the pinned baseline with a later branch HEAD.

## 5. Validation execution

For every required gate:

- run the actual command or canonical project entrypoint;
- bind PASS/FAIL/BLOCKED evidence to the exact tested SHA;
- record environment identity and runtime/toolchain where material;
- preserve Validation Tuple boundaries;
- do not infer PASS from another platform, toolchain, CI job, or previous SHA.

If an exact command is not predeclared, the agent MAY resolve it from project-owned entrypoints such as `AGENTS.md`, `PROJECT_OVERRIDES`, package scripts, Make/Task files, or documented build tooling. The resolved command MUST be recorded in the report.

After execution, the agent SHOULD publish a `VALIDATION_RESULT` event using `templates/agent-event-comment.md` when the project follows the GitHub Agent Interaction Protocol.

## 6. Allowed fixes

Unless the Issue narrows the scope further, the Local Agent MAY fix:

- implementation bugs;
- type/lint/format failures;
- dependency/lockfile/build configuration defects;
- platform compatibility defects;
- frozen-scope omissions;
- test implementation defects that do not weaken required behavior;
- documentation synchronization required by the actual change.

The agent MUST NOT independently change:

- frozen PRD / product scope;
- domain semantics or business rules;
- public API/data semantics unless explicitly authorized;
- security model;
- frozen architecture boundary;
- required validation strength;
- mandatory release gate authority.

If solving a failure requires such a change, report it as BLOCKED for that path and continue independent work.

## 7. Branch creation / review routing rule

Validation alone does not require a branch.

If no source change is needed:

```text
Issue → execute against exact SHA → Validation Report → VALIDATION_RESULT → route parent Task according to remaining required gates / Review Policy
```

If a source change is needed, create an isolated task/fix branch, preferably:

```text
fix/<version>-<issue>-<scope>
```

or the repository's equivalent naming convention.

The resulting PR MUST target the correct integration branch (`version/vX.Y.Z` in Version Branch Mode, otherwise the declared stable branch) or a justified stack parent, and reference the handoff Issue / parent Task.

After any code-changing fix:

- affected required Validation gates MUST be re-executed against the resulting exact SHA;
- any prior Review PASS on an older PR HEAD remains historical only for that old SHA;
- if Review Policy is `required`, the changed PR MUST return to `state:review-ready` for delta/full re-review before merge;
- if Review Policy is `recommended`, return to review-ready only when the optional Review is being continued; otherwise record the Review decision and follow remaining merge prerequisites;
- if Review Policy is `not-required`, do not create a Review Gate merely because the SHA changed.

## 8. Blocker behavior

A blocker only blocks dependent nodes.

For FAIL/BLOCKED record, where available:

- exact command;
- exit code;
- key logs;
- reproduction;
- expected vs actual;
- root cause/evidence;
- affected task/version;
- downstream dependency/release impact.

If the project follows structured Agent events, publish `BLOCKER_REPORTED` for material blockers.

Continue all independent work until it is exhausted or continuing would violate frozen facts or safety.

## 9. Completion / routing rule

A handoff is complete when one of the following is true:

1. all required gates are PASS and the final commit/PR + Validation Report are linked; or
2. the remaining path is explicitly FAIL/BLOCKED with reproduction, evidence, impact, and any upstream decision required.

An Issue MUST NOT be closed merely because an agent finished running commands.

When the handoff was requested by an Independent Reviewer:

- validation PASS does not by itself decide the parent Task's Review result;
- if the Review Policy is `required`, or a `recommended` Review is actively in progress, route the parent Task back to `state:review-ready` so the Reviewer can close the Review on the correct SHA;
- if the Reviewer requested validation only as advisory evidence and the Task has no active Review requirement, route according to the actual remaining required gates instead of forcing review-ready.

## 10. Expected final output

The execution agent MUST report at least:

```text
current/final HEAD
tested SHA
execution environment
runtime/toolchain
exact commands + exit codes
gate matrix
changes made
PR/commit identity
fixed failures
remaining blockers
downstream candidate/release impact
```

Gate states are limited to:

```text
PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE
```

Workflow routing state is separate and follows `state:*` metadata from `GITHUB_AGENT_INTERACTION_PROTOCOL.md`.

## 11. Bootstrap prompt

Use the reusable prompt at `prompts/local-agent-bootstrap.md`. The prompt is intentionally generic: task-specific facts belong in the GitHub Issue, not in duplicated chat-only instructions.
