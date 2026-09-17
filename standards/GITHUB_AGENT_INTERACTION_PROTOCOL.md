# GitHub Agent Interaction Protocol

## 1. Purpose

This protocol defines GitHub-native coordination between Builder, Reviewer, Validator / Local Agent and merge/release control roles.

The objective is that multiple sessions or agents can collaborate without exchanging hidden chat context. GitHub carries the durable contract, routing metadata, event history, code change and exact identities.

Canonical responsibility model:

```text
Issue body      = stable work contract
Issue metadata  = routing and current workflow state
Issue dependency= canonical execution dependency graph
Comments        = append-oriented agent event log
Branch          = isolated implementation concern
PR              = reviewable code change
Stacked PR      = optional unmerged code-baseline dependency
Commit SHA      = exact change / execution identity
Milestone       = version/release aggregation
Validation      = exact-SHA execution evidence
```

Chat is a workspace. It is not the coordination source of truth.

## 2. Three dependency layers

Do not overload one Git/GitHub mechanism to represent every kind of dependency.

### 2.1 Planning DAG

The frozen Task DAG document/checkpoint records why the work was decomposed, task inputs/outputs, acceptance, risks, parallelism and dependency rationale.

It is a planning/history artifact.

### 2.2 Execution DAG — canonical Task DAG

GitHub Task Issues plus native Issue Dependencies are the canonical execution DAG once the plan is materialized.

Use Issue Dependencies for relationships such as:

```text
T02 blocked by T01
T03 blocked by T01
T04 blocked by T02
T04 blocked by T03
```

This is the authoritative machine-consumable task dependency relation during execution.

A planning DAG checkpoint and the execution DAG MUST remain traceable to each other. Material changes to dependency semantics SHOULD leave an explicit change event/rationale rather than silently rewriting history.

### 2.3 Code-baseline dependency — optional Stacked PR

Stacked PR is not the canonical Task DAG.

Use a stacked branch/PR only when one task's code must be based on another task branch that has not yet merged to the integration branch.

Example:

```text
version/vX.Y.Z
  ↑
task/T01-contract
  ↑
task/T02-core
```

PR topology:

```text
T01 PR: task/T01-contract → version/vX.Y.Z
T02 PR: task/T02-core     → task/T01-contract
```

Rules:

- Do not create a stack merely to mirror every Issue dependency.
- Preserve parallel branches when code does not need an unmerged upstream branch.
- A stack describes Git/code baseline dependency, not product/task planning semantics.
- Because a Git branch has one direct base while a Task DAG may fork and join, stacked PRs cannot replace the execution DAG.
- When an upstream stack PR merges, downstream PRs SHOULD be rebased/retargeted onto the correct remaining stack parent or integration branch.
- Any resulting SHA change invalidates SHA-bound review/validation evidence according to their rules; affected review/validation MUST be re-executed.
- When a task's completion depends on another task, the corresponding Issue dependency SHOULD still be recorded even if implementation proceeds early on a stable stacked baseline.

## 3. Hierarchy is not dependency

Use different GitHub mechanisms for different semantics:

```text
Milestone     = version/release grouping
Sub-issue     = belongs-to hierarchy (version/epic/task/validation)
Dependency    = blocked-by / blocking execution relationship
Branch/PR     = implementation and review boundary
Stacked PR    = code-baseline dependency
```

Do not infer execution order merely from sub-issue hierarchy.

## 4. Task Issue contract

A Task Issue is the durable work contract. Its body SHOULD remain relatively stable and contain:

```text
Task ID / title
Milestone / target version
Goal
In scope / out of scope
Frozen PRD / architecture / L3 references
Planning Task DAG reference
Baseline / integration target
Acceptance criteria
Required task-level gates
Known dependencies
Allowed changes
Forbidden changes
Expected outputs
```

Do not use repeated body rewrites as an event log. State changes, review results, fixes and validation results belong in metadata/comments.

## 5. Metadata model

### 5.1 Version

Use GitHub Milestone for version/release grouping when available:

```text
v0.1.0
v2.9.4
```

Do not create one-off version labels by default.

### 5.2 Work type

Portable label fallback:

```text
type:task
type:bug
type:validation
type:blocker
```

If a GitHub Organization provides native Issue Types, projects MAY map these semantics to native types while preserving the same canonical meaning.

### 5.3 Workflow state

Recommended mutable state labels:

```text
state:planned
state:ready
state:implementing
state:review-ready
state:reviewing
state:changes-requested
state:validation-needed
state:merge-ready
state:blocked
state:done
```

A Task Issue SHOULD have at most one `state:*` label at a time.

Workflow state is not a Validation Gate status. Gate results still use only:

```text
PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE
```

### 5.4 Routing / execution dimensions

Recommended labels:

```text
handoff:local-agent
executor:codex
executor:claude-code

gate:review
gate:fast
gate:integration
gate:critical-journey
gate:hidden
gate:platform
gate:packaging

env:ubuntu-build-host
env:windows
env:macos
env:gpu

release-blocker
blocked:environment
```

Projects MAY map stable dimensions to Organization custom Issue Fields where available. The protocol semantics MUST NOT depend on a specific GitHub UI feature; labels remain the portable baseline.

## 6. Agent roles and queues

### 6.1 Builder

Builder consumes primarily:

```text
state:ready
state:changes-requested
```

Builder responsibilities:

- claim/implement the Task;
- create/update the Task branch and PR;
- run available task-level validation;
- publish exact HEAD SHA and evidence;
- transition to `state:review-ready` when reviewable;
- continue other independent Tasks instead of waiting for Reviewer when the execution DAG allows it.

### 6.2 Independent Reviewer

Reviewer consumes primarily:

```text
state:review-ready
```

Reviewer responsibilities:

- reconstruct context from GitHub and pinned standard, not Builder chat history;
- review the PR against frozen scope, architecture, Task acceptance, tests and evidence;
- bind the review result to exact PR HEAD SHA;
- publish findings and transition to `state:changes-requested`, `state:validation-needed`, or `state:merge-ready`.

A long-lived Reviewer session MAY process many PRs, but every review must re-read current GitHub facts and must not rely on trust accumulated from earlier tasks.

### 6.3 Validator / Local Agent

Validator consumes primarily:

```text
state:validation-needed
```

or dedicated validation sub-issues with appropriate `gate:*`, `env:*` and `handoff:local-agent` metadata.

Validator executes real environment gates and publishes exact-SHA Validation Evidence. Validation-only work does not require a branch. A source fix requires a separate task/fix branch and revalidation.

### 6.4 Merge control

A Task/Fix PR may become mergeable only after its declared merge policy is satisfied. In Version Branch Mode the standard default is:

```text
current PR HEAD SHA
+ required task-level Validation PASS
+ Independent Review Gate PASS on that SHA
+ configured required Minimal CI PASS (when enabled)
+ required upstream Issue dependencies satisfied for merge
+ correct integration target
= state:merge-ready
```

Merge then targets `version/vX.Y.Z`.

## 7. Independent Task Review Gate

### 7.1 Default requirement

In Version Branch Mode, every Task/Fix PR MUST receive an Independent Review before merge to the version branch unless an explicit higher-authority project rule defines a narrower exception.

Trunk/Fast Path SHOULD use Independent Review according to project risk/policy; disabling CI does not remove review/validation requirements.

### 7.2 Independence

The final review authority SHOULD NOT be the same implementation context that just produced the change.

Acceptable independent review sources include:

- another ChatGPT session;
- another coding/review agent;
- a human reviewer;
- the same model in a fresh context that reconstructs facts from GitHub.

Different model or machine is optional. Independent context and evidence reconstruction are the important properties.

### 7.3 Exact-SHA binding

Review PASS is bound to a specific PR HEAD SHA.

If the PR HEAD changes after PASS:

- previous PASS remains historical evidence for the old SHA;
- current Review Gate becomes `NOT_RUN` until re-review;
- a narrow fix MAY receive delta review from `old-reviewed-sha..new-head-sha` when the reviewer confirms the change is sufficiently scoped;
- large or cross-cutting changes require full re-review.

### 7.4 Review result

Review Gate uses:

```text
PASS
FAIL
BLOCKED
NOT_RUN
NOT_APPLICABLE
```

`NOT_APPLICABLE` for a Version Branch Task/Fix PR requires explicit authority; it is not a convenience shortcut.

Reviewer findings SHOULD identify severity, location/evidence, expected behavior, actual behavior and required change.

When a conclusion requires real execution that the reviewer cannot perform, do not guess. Publish `VALIDATION_REQUEST` and route to the appropriate validation environment.

## 8. Standard event comment format

Agent-to-agent coordination comments SHOULD include a machine-readable marker and YAML payload, followed by optional human-readable Markdown.

Marker:

```html
<!-- ai-dev:event:v1 -->
```

Base shape:

```yaml
schema: ai-dev/event-v1
event: <EVENT_TYPE>
actor_role: builder | reviewer | validator | merge-controller
task: "#123"
pr: "#456"        # when applicable
sha: "<40-char-sha>"
status: PASS | FAIL | BLOCKED | NOT_RUN | NOT_APPLICABLE
next_state: <state label without state: prefix, when applicable>
```

Recommended event types:

```text
TASK_CLAIMED
IMPLEMENTATION_READY
REVIEW_RESULT
FIX_APPLIED
VALIDATION_REQUEST
VALIDATION_RESULT
BLOCKER_REPORTED
DEPENDENCY_CHANGED
MERGE_RESULT
```

Event-specific fields MAY be added, but existing field semantics MUST NOT be silently redefined.

Comments are append-oriented history. If an event is materially wrong, publish a corrective event referencing the superseded comment/event rather than silently rewriting important history.

## 9. Canonical state flow

Typical Task flow:

```text
planned
  ↓
ready
  ↓
implementing
  ↓
review-ready
  ↓
reviewing
  ├── changes-requested → implementing/review-ready
  ├── validation-needed → validation → review-ready
  ├── blocked
  └── merge-ready
          ↓
        merged
          ↓
         done
```

`merged` is an event, not a required `state:*` label; the Issue may transition directly from `state:merge-ready` to `state:done` after merge bookkeeping.

An unresolved Issue dependency normally prevents `state:merge-ready`, but MAY NOT prevent implementation from beginning when the upstream branch exposes a stable code baseline and the frozen Task contract permits early/stacked work.

## 10. Builder / Reviewer pipeline

A and B may operate continuously:

```text
Builder A                         Reviewer B
T01 implementation
  ↓
PR #101 + review-ready ─────────→ review #101
T02 implementation                ↓
  ↓                              PASS / findings
PR #102 + review-ready ─────────→ review #102
T03 implementation                ↓
...                              ...
```

Builder SHOULD NOT wait idle for Reviewer if independent executable work exists.

Reviewer SHOULD continue reviewing independent PRs even if one PR fails, unless the execution DAG makes downstream review meaningless or unsafe.

Normal chat sessions are not background workers. Queue consumption occurs when an agent/session is invoked, scheduled by supported automation, or triggered by an external orchestrator.

## 11. Validation sub-issues

When review requires environment-specific execution, a dedicated Validation Issue MAY be created as a sub-issue of the Task Issue.

Example:

```text
Task #31
└── Validation #47 — Windows production build
```

Use dependency when the validation result truly blocks another work item/candidate. Do not use sub-issue hierarchy alone to imply blocking.

The validation issue records exact target SHA, environment/profile, commands, expected result and completion rule according to `LOCAL_AGENT_HANDOFF_PROTOCOL.md` and `VALIDATION_STANDARD.md`.

## 12. Execution DAG materialization

After Task DAG freeze:

```text
Frozen Task DAG checkpoint
        ↓
create/update Task Issues
        ↓
apply Milestone / type metadata
        ↓
materialize Issue Dependencies
        ↓
apply initial workflow states
        ↓
execution queues
        ↓
Task Branch / PR
```

The Task DAG document remains the planning checkpoint. GitHub Issue Dependencies become the live execution dependency graph.

Do not create a Task-DAG branch merely to represent dependencies.

## 13. Merge and dependency rules

Before merging a Task/Fix PR in Version Branch Mode, verify:

- Task Issue and PR are linked;
- PR targets the correct version branch or correct stack parent;
- required upstream Issue dependencies for merge are resolved;
- current HEAD matches the SHA reviewed/validated by required gates;
- Independent Review Gate is PASS;
- required task/local validation is PASS;
- configured required CI is PASS when applicable;
- no unresolved release-significant review thread/blocker remains.

If a stacked PR is retargeted/rebased after its parent merges, repeat affected review/validation against the new exact SHA before merge.

## 14. Recovery rule

A fresh agent/session SHOULD be able to recover work from:

```text
repository
+ pinned standard revision
+ Task/Validation Issue
+ Issue dependencies/metadata
+ linked PR
+ exact-SHA evidence/comments
```

It SHOULD NOT require private reasoning or a previous chat transcript.
