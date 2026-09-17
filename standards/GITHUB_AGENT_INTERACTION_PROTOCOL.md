# GitHub Agent Interaction Protocol

## 1. Purpose

This protocol defines GitHub-native coordination between Planner, Builder, optional Independent Reviewer, Validator / Local Agent, merge control and release control.

The objective is that multiple sessions or agents can collaborate without exchanging hidden chat context. GitHub carries the durable contract, routing metadata, event history, code change, exact identities and logical operator attribution.

Canonical responsibility model:

```text
Issue body        = stable work contract
Issue metadata    = routing and current workflow state
Issue dependency  = canonical execution dependency graph
Comments          = append-oriented Agent event log
Actor role        = responsibility performed by an event
Logical operator  = concrete Web session / Local Agent / automation / human that performed it
Transport actor   = GitHub account/API identity that wrote the event
Branch            = isolated implementation concern
PR                = reviewable/mergeable code change
Stacked PR        = optional unmerged code-baseline dependency
Commit SHA        = exact change / execution identity
Milestone         = version/release aggregation
Validation        = exact-SHA execution evidence
Review            = optional or required exact-SHA independent analysis according to Review Policy
```

Chat is a workspace. It is not the coordination source of truth.

A GitHub username is **not** sufficient Agent identity when several Web sessions, local agents or automations use the same account.

## 2. Three dependency layers

Do not overload one Git/GitHub mechanism to represent every kind of dependency.

### 2.1 Planning DAG

The frozen Task DAG document/checkpoint records why the work was decomposed, task inputs/outputs, acceptance, risks, parallelism, Review Policy and dependency rationale.

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
- Any resulting SHA change invalidates SHA-bound required review/validation evidence according to their rules; affected required evidence MUST be re-executed.
- When a task's completion depends on another task, the corresponding Issue dependency SHOULD still be recorded even if implementation proceeds early on a stable stacked baseline.

## 3. Hierarchy is not dependency

Use different GitHub mechanisms for different semantics:

```text
Milestone     = version/release grouping
Sub-issue     = belongs-to hierarchy (version/epic/task/validation)
Dependency    = blocked-by / blocking execution relationship
Branch/PR     = implementation and merge boundary
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
Review Policy
Known dependencies
Allowed changes
Forbidden changes
Expected outputs
```

Do not use repeated body rewrites as an event log. State changes, operator claims, review decisions/results, fixes and validation results belong in metadata/comments.

Current logical ownership SHOULD be recovered from structured events such as `ROLE_CLAIMED`, not by rewriting the stable Issue body.

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

Workflow state is not a Validation/Review Gate status. Gate results still use only:

```text
PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE
```

### 5.4 Review Policy metadata

Independent Review is risk-based; it is not globally mandatory for every Task/Fix PR.

Every implementation Task/PR SHOULD resolve one policy:

```text
review:required
review:recommended
review:not-required
```

Repositories using custom Issue Fields MAY represent the same dimension as `Review Policy = required | recommended | not-required` instead of labels.

At most one Review Policy value applies to a Task/PR.

Semantics:

- `required`: Independent Review is a merge gate. Current merge-candidate SHA requires Review `PASS`.
- `recommended`: Review is useful but optional. It MAY be skipped with an explicit decision/rationale. Review Gate may remain `NOT_RUN` without blocking merge.
- `not-required`: no Independent Review Gate exists for this concern; use `NOT_APPLICABLE`.

Review Policy and Review result are different dimensions. Do not encode `required/recommended/not-required` using Gate states.

### 5.5 Routing / execution dimensions

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

`executor:*` is a routing/capability hint. It does not prove which concrete session or process actually performed an event.

### 5.6 Actor role and logical operator identity

Every new structured Agent event under standard v3.1+ SHOULD identify both the **role** and the **logical operator**.

Role vocabulary:

```text
planner
builder
reviewer
validator
merge-controller
release-controller
```

Operator vocabulary:

```text
operator_kind: chatgpt-web | codex | claude-code | human | github-actions | woodpecker | other
operator_id: <logical executor instance>
session_ref: <opaque page/conversation/process/run alias>
transport_actor: <GitHub/API identity that wrote the event>
```

Semantics:

- `actor_role` says **what responsibility** was performed.
- `operator_kind` says **which execution surface/system** performed it.
- `operator_id` identifies the logical executor context and SHOULD remain stable for that Web session, local worker or automation identity.
- `session_ref` identifies the concrete page/conversation/process/run when useful. It SHOULD be present when multiple concurrent sessions of the same kind exist.
- `transport_actor` identifies the account/API identity that physically wrote to GitHub. It is transport metadata, not logical authorship.

Recommended examples:

```text
chatgpt-web:web-a
chatgpt-web:web-b
codex:ubuntu-build-01
claude-code:windows-01
woodpecker:runner-01
github-actions:verify-standard
human:owner
```

For two ChatGPT Web pages sharing one GitHub account:

```text
Builder page:
  actor_role=builder
  operator_id=chatgpt-web:web-a
  session_ref=domainharness-builder-a
  transport_actor=github:kaicreator-mm

Reviewer page:
  actor_role=reviewer
  operator_id=chatgpt-web:web-b
  session_ref=domainharness-reviewer-b
  transport_actor=github:kaicreator-mm
```

Identity rules:

- `operator_id` need only be unique enough within the repository/version execution window; global identity infrastructure is not required.
- A new ChatGPT page/session SHOULD receive a new `session_ref`; it MAY keep a stable human-friendly `operator_id` if the project intentionally treats it as the same long-lived logical worker.
- Never store tokens, cookies, signed URLs, credentials or secrets in identity fields.
- Dynamic `operator_id/session_ref` SHOULD NOT become GitHub labels; otherwise every session would create label churn. Use structured events instead.
- The same operator MAY perform different roles on different work items.
- The same role MAY be performed by different operators over time.

For required Independent Review, the Reviewer MUST be attributable to a context independent from the Builder context. The same `transport_actor` is allowed, but `operator_id/session_ref` must make the separation auditable.

## 6. Review Policy selection

### 6.1 Authority

Review Policy must follow the normal authority order:

```text
Frozen PRD / Contract
→ Frozen Architecture
→ PROJECT_OVERRIDES
→ Task acceptance / risk classification
→ Standard defaults
```

A lower-authority Task or Agent MUST NOT silently downgrade a higher-authority `required` rule.

### 6.2 Standard default

When no higher authority defines a policy, use **risk-based** selection.

The standard does not make Independent Review mandatory merely because Version Branch Mode is used.

Typical guidance:

#### `required` SHOULD be selected when the concern includes

- security, authentication, authorization, permissions, secrets or trust boundaries;
- public API / external contract semantics;
- database schema or migration semantics;
- cross-service / cross-package contracts with meaningful blast radius;
- concurrency, transactions, locking or data-integrity logic;
- destructive/irreversible behavior or failure-recovery logic;
- release blockers or explicitly high-risk Task classification;
- large/cross-cutting changes where tests/validation alone provide insufficient confidence;
- sensitive areas required by CODEOWNERS/project policy.

#### `recommended` is normally appropriate for

- medium-risk behavior changes;
- non-critical integration/refactor work;
- new functionality with good automated validation but useful independent scrutiny;
- changes where a fresh-context review is cheap relative to risk.

#### `not-required` MAY be selected for

- docs-only/comment-only work;
- deterministic mechanical/generated updates with reliable verification;
- narrowly scoped low-risk changes where independent analysis adds little value;
- project-specific categories explicitly declared safe to merge without Independent Review.

These examples guide classification. Project policy may be stricter.

### 6.3 Decision record

The selected policy SHOULD be visible in the Task Issue and PR.

For `recommended` review that is skipped, record a concise decision/rationale using Issue/PR metadata or an Agent event. Skipping an optional review is not a Validation PASS and must not be represented as one.

## 7. Agent roles and queues

### 7.1 Planner

Planner creates/finalizes planning facts, Task Issues, Issue Dependencies and initial Review Policy. Planning events SHOULD identify their logical operator when written through a shared GitHub account.

### 7.2 Builder

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
- resolve Review Policy;
- when review is selected for execution, transition to `state:review-ready`;
- when no review is required/performed and all other merge requirements are satisfied, transition directly to `state:merge-ready`;
- continue other independent Tasks instead of waiting for Reviewer when the execution DAG allows it.

For long-running or concurrent work, Builder SHOULD publish `ROLE_CLAIMED` with its operator attribution before substantial modification.

### 7.3 Independent Reviewer

Reviewer is invoked only for Tasks whose Review Policy/decision selects review.

Reviewer consumes primarily:

```text
state:review-ready
```

Reviewer responsibilities:

- publish its own independent operator attribution / role claim;
- reconstruct context from GitHub and pinned standard, not Builder chat history;
- review the PR against frozen scope, architecture, Task acceptance, tests and evidence;
- bind the review result to exact PR HEAD SHA;
- publish findings and transition to `state:changes-requested`, `state:validation-needed`, `state:merge-ready`, or `state:blocked` as appropriate.

A long-lived Reviewer session MAY process many PRs, but every review must re-read current GitHub facts and must not rely on trust accumulated from earlier tasks.

### 7.4 Validator / Local Agent

Validator consumes primarily:

```text
state:validation-needed
```

or dedicated validation sub-issues with appropriate `gate:*`, `env:*` and `handoff:local-agent` metadata.

Validator executes real environment gates and publishes exact-SHA Validation Evidence. Validation-only work does not require a branch. A source fix requires a separate task/fix branch and revalidation.

Local validation events MUST distinguish the logical local operator from the GitHub account used to post evidence.

### 7.5 Merge control

A Task/Fix PR may become mergeable only after its declared merge policy is satisfied.

Canonical merge formula:

```text
current PR HEAD SHA
+ required task/local Validation PASS
+ Review condition satisfied
+ configured required Minimal CI PASS (when enabled)
+ required upstream Issue dependencies satisfied for merge
+ correct integration target / stack topology
+ no unresolved release-significant blocker/finding
= state:merge-ready
```

Review condition means:

```text
review:required     → Independent Review PASS on current SHA
review:recommended  → PASS on current SHA OR explicit SKIP decision/rationale
review:not-required → Review Gate NOT_APPLICABLE
```

Merge then targets `version/vX.Y.Z`, `main`, or the correct temporary stack parent according to integration mode/topology.

`MERGE_RESULT` SHOULD include the merge-controller's operator attribution.

## 8. Independent Review execution rules

These rules apply whenever Independent Review is performed, and are mandatory when Review Policy is `required`.

### 8.1 Independence

The final review authority SHOULD NOT be the same implementation context that just produced the change.

Acceptable independent review sources include:

- another ChatGPT session;
- another coding/review agent;
- a human reviewer;
- the same model in a fresh context that reconstructs facts from GitHub.

Different model or machine is optional. Independent context and evidence reconstruction are the important properties.

With v2 Agent events, independence SHOULD be auditable from `operator_id/session_ref`. A shared `transport_actor` does not invalidate independence.

### 8.2 Exact-SHA binding

Review PASS is bound to a specific PR HEAD SHA.

If the PR HEAD changes after PASS:

- previous PASS remains historical evidence for the old SHA;
- if review remains required for merge, current Review Gate becomes `NOT_RUN` until re-review;
- a narrow fix MAY receive delta review from `old-reviewed-sha..new-head-sha` when the reviewer confirms the change is sufficiently scoped;
- large or cross-cutting changes require full re-review.

If Review Policy is only `recommended` and the project chooses not to retain review as merge evidence after a later HEAD change, record that decision rather than falsely carrying the old PASS forward.

### 8.3 Review result

Review Gate uses:

```text
PASS
FAIL
BLOCKED
NOT_RUN
NOT_APPLICABLE
```

Rules:

- `required`: merge requires `PASS` on current SHA.
- `recommended`: `NOT_RUN` is allowed when review is explicitly skipped; if review is performed, its material findings must be resolved or dispositioned before merge.
- `not-required`: use `NOT_APPLICABLE`.

Reviewer findings SHOULD identify severity, location/evidence, expected behavior, actual behavior and required change.

When a conclusion requires real execution that the reviewer cannot perform, do not guess. Publish `VALIDATION_REQUEST` and route to the appropriate validation environment.

## 9. Standard event comment format

Agent-to-agent coordination comments SHOULD include a machine-readable marker and YAML payload, followed by optional human-readable Markdown.

### 9.1 Event v2 — current schema

New events under v3.1+ SHOULD use:

```html
<!-- ai-dev:event:v2 -->
```

Base shape:

```yaml
schema: ai-dev/event-v2
event: <EVENT_TYPE>
actor_role: planner | builder | reviewer | validator | merge-controller | release-controller
operator_kind: chatgpt-web | codex | claude-code | human | github-actions | woodpecker | other
operator_id: "<logical operator id>"
session_ref: "<opaque page/conversation/process/run alias>" # strongly recommended for concurrent sessions
transport_actor: "github:<account>"                         # recommended for shared GitHub accounts
task: "#123"                                                # when applicable
pr: "#456"                                                  # when applicable
sha: "<40-char-sha>"                                        # when applicable
status: PASS | FAIL | BLOCKED | NOT_RUN | NOT_APPLICABLE
next_state: <state label without state: prefix, when applicable>
```

Event-specific fields MAY be added, but existing field semantics MUST NOT be silently redefined.

### 9.2 Event v1 compatibility

Historical `<!-- ai-dev:event:v1 -->` / `schema: ai-dev/event-v1` events remain valid evidence. Do not rewrite history only to add attribution.

When a v1 event lacks operator identity, its GitHub author MAY be used only as transport provenance; do not infer which ChatGPT/local context produced it.

### 9.3 Recommended event types

```text
ROLE_CLAIMED
ROLE_RELEASED
TASK_CLAIMED
IMPLEMENTATION_READY
REVIEW_DECISION
REVIEW_RESULT
FIX_APPLIED
VALIDATION_REQUEST
VALIDATION_RESULT
BLOCKER_REPORTED
DEPENDENCY_CHANGED
MERGE_RESULT
```

`TASK_CLAIMED` remains a Builder-specific compatibility event. New cross-role flows SHOULD prefer `ROLE_CLAIMED`.

`ROLE_CLAIMED` means a logical operator has started acting in a workflow role. `ROLE_RELEASED` records intentional handoff/abandonment before the normal result event. Neither event is a Validation/Review PASS.

A role claim is attribution/routing evidence, not a distributed lock. If the project needs exclusive ownership, it must define that separately.

`REVIEW_DECISION` MAY record `required/recommended/not-required`, or `recommended + SKIP/PERFORM`, without pretending that the policy/decision itself is a Gate PASS.

Comments are append-oriented history. If an event is materially wrong, publish a corrective event referencing the superseded comment/event rather than silently rewriting important history.

The canonical concrete examples live in `templates/agent-event-comment.md`.

## 10. Canonical state flow

Review is an optional branch in the Task workflow:

```text
planned
  ↓
ready
  ↓
implementing
  ↓
implementation ready
  ├── review required/selected → review-ready → reviewing
  │      ├── changes-requested → implementing
  │      ├── validation-needed → validation → review-ready
  │      ├── blocked
  │      └── PASS → merge-ready
  │
  └── review not required/skipped
          ↓
       merge-ready
          ↓
        merged
          ↓
         done
```

`merged` is an event, not a required `state:*` label; the Issue may transition directly from `state:merge-ready` to `state:done` after merge bookkeeping.

An unresolved Issue dependency normally prevents `state:merge-ready`, but MAY NOT prevent implementation from beginning when the upstream branch exposes a stable code baseline and the frozen Task contract permits early/stacked work.

`ROLE_CLAIMED/ROLE_RELEASED` annotate **who** is working; they do not create new workflow states.

## 11. Builder / Reviewer pipeline

A and B may operate continuously when review work exists:

```text
Builder A                               Reviewer B
operator=chatgpt-web:web-a             operator=chatgpt-web:web-b
T01 implementation
  ↓
PR #101 + review-ready ───────────────→ review #101
T02 implementation                      ↓
  ↓                                    PASS / findings
PR #102 (review skipped) → merge-ready
T03 implementation
  ↓
PR #103 + review-ready ───────────────→ review #103
```

Both sessions may post through the same `transport_actor=github:<account>` while remaining distinguishable by `operator_id/session_ref`.

Builder SHOULD NOT wait idle for Reviewer if independent executable work exists.

Reviewer SHOULD continue reviewing independent PRs even if one PR fails, unless the execution DAG makes downstream review meaningless or unsafe.

Normal chat sessions are not background workers. Queue consumption occurs when an agent/session is invoked, scheduled by supported automation, or triggered by an external orchestrator.

## 12. Validation sub-issues

When review or Task policy requires environment-specific execution, a dedicated Validation Issue MAY be created as a sub-issue of the Task Issue.

Example:

```text
Task #31
└── Validation #47 — Windows production build
```

Use dependency when the validation result truly blocks another work item/candidate. Do not use sub-issue hierarchy alone to imply blocking.

The validation issue records exact target SHA, environment/profile, commands, expected result and completion rule according to `LOCAL_AGENT_HANDOFF_PROTOCOL.md` and `VALIDATION_STANDARD.md`.

Validation evidence SHOULD include v2 operator attribution so a fresh session can distinguish Web-requested validation from the concrete Local Agent/run that executed it.

## 13. Execution DAG materialization

After Task DAG freeze:

```text
Frozen Task DAG checkpoint
        ↓
create/update Task Issues
        ↓
apply Milestone / type / Review Policy metadata
        ↓
materialize Issue Dependencies
        ↓
apply initial workflow states
        ↓
Builder / optional Reviewer / Validator queues
        ↓
ROLE_CLAIMED + operator attribution when work begins
        ↓
Task Branch / PR
```

The Task DAG document remains the planning checkpoint. GitHub Issue Dependencies become the live execution dependency graph.

Do not create a Task-DAG branch merely to represent dependencies.

## 14. Merge and dependency rules

Before merging a Task/Fix PR, verify:

- Task Issue and PR are linked;
- PR targets the correct version branch/main branch or correct stack parent;
- required upstream Issue dependencies for merge are resolved;
- current HEAD matches the SHA validated by required gates;
- Review Policy is explicit;
- review condition is satisfied according to `required/recommended/not-required` semantics;
- required task/local validation is PASS;
- configured required CI is PASS when applicable;
- no unresolved release-significant blocker/finding/thread remains.

Where v2 events are used, merge/release evidence SHOULD identify the logical operator responsible for the decision/result.

If a stacked PR is retargeted/rebased after its parent merges, repeat affected **required** review/validation against the new exact SHA before merge.

## 15. Recovery rule

A fresh agent/session SHOULD be able to recover work from:

```text
repository
+ pinned standard revision
+ Task/Validation Issue
+ Issue dependencies/metadata
+ linked PR
+ exact-SHA evidence/comments
+ actor role / logical operator attribution
```

It SHOULD be able to answer from GitHub facts:

```text
who planned/claimed/implemented/reviewed/validated/merged?
which ChatGPT Web page/session or Local Agent/run did it?
which GitHub account transported the event?
which exact SHA did the result apply to?
```

It SHOULD NOT require private reasoning or a previous chat transcript.