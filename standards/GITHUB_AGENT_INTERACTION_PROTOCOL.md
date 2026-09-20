# GitHub Agent Interaction Protocol

## 1. Purpose and authority boundary

This protocol defines the GitHub-native contract used by Planner, Builder, Reviewer, Validator, Scheduler, Merge Controller, Release Controller and Repository Integration Controller.

It owns:

- GitHub work-item / metadata / event responsibilities;
- logical operator attribution;
- canonical short-intent admission / normalization / rejection semantics;
- canonical structured-event writer protocol;
- Review Policy interaction semantics;
- recovery from GitHub facts across sessions/agents.

It does **not** redefine orchestration state reduction, validation truth or release authority. Those remain owned by:

- `EXECUTION_ARCHITECTURE_STANDARD.md` — durable facts, derived state, queues, dispatch and controllers;
- `VALIDATION_STANDARD.md` — Validation Tuple, evidence and validation ownership;
- `RELEASE_STANDARD.md` — candidate/release authority;
- `LOCAL_AGENT_HANDOFF_PROTOCOL.md` — handoff completeness and pointer-only local execution.

`EXECUTION_ARCHITECTURE_STANDARD.md` may describe how an executor/reducer consumes accepted intents/events, but it MUST NOT define a second intent contract. If its operational summary conflicts with this protocol's intent admission or event-writer rules, this protocol is authoritative for GitHub interaction semantics.

Core rule:

```text
GitHub carries durable execution facts.
Chat is a workspace, not project state.
```

## 2. Canonical GitHub responsibility model

```text
Issue body        = stable work contract
Issue metadata    = routing/current workflow metadata
Issue dependency  = canonical live execution dependency graph
Comments          = append-oriented event/evidence history
Milestone         = version/release grouping
Branch            = isolated implementation concern
PR                = reviewable/mergeable change
Stacked PR        = optional unmerged code-baseline dependency
Commit SHA        = exact change/execution identity
Validation        = exact-SHA execution evidence
Review            = exact-SHA independent analysis when selected by Review Policy
State card         = non-authoritative derived projection
```

Do not overload one object with another object's semantics.

### Planning DAG vs execution DAG

Frozen Task DAG is a planning/history checkpoint. After materialization:

```text
GitHub Task Issues + native Issue Dependencies = canonical live execution DAG
```

Sub-issue hierarchy is not execution dependency. Stacked PR is not Task DAG; use it only when code truly depends on an unmerged upstream code baseline.

If the connected GitHub capability cannot mutate a canonical object, follow `GITHUB_CAPABILITY_FALLBACK.md`; do not silently replace native dependency semantics with prose.

## 3. Task Issue contract

A Task Issue SHOULD remain relatively stable and contain, as applicable:

```text
Task ID / goal
scope / non-scope
frozen inputs
planning DAG reference
baseline / integration target
acceptance criteria
required gates
Review Policy
dependency summary
allowed / forbidden changes
completion rule
```

Do not use repeated Issue-body rewrites as an event log. Current events, claims, validation, review and merge history belong in metadata/comments.

When an Issue already contains the complete task contract, invocation follows `ISSUE_FIRST_TASK_TRIGGER.md`: send a short repository/Issue pointer instead of copying a second task contract into chat.

## 4. Metadata dimensions

Portable labels may represent stable routing dimensions:

```text
type:task
type:bug
type:validation
type:blocker

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

review:required
review:recommended
review:not-required

handoff:local-agent
executor:codex
executor:claude-code

gate:review
gate:integration
gate:critical-journey
gate:hidden
gate:platform
gate:packaging
```

Projects MAY use native Issue Types/custom fields when available while preserving the same semantics.

Workflow routing state is not Gate state. Gate state remains only:

```text
PASS
FAIL
BLOCKED
NOT_RUN
NOT_APPLICABLE
```

Execution-channel/provider state, dispatch state, candidate state and release state are also separate dimensions as defined by `EXECUTION_ARCHITECTURE_STANDARD.md`.

## 5. Actor role and logical operator identity

A GitHub account/API identity is only transport. It is not sufficient logical-agent identity when multiple Web sessions, Local Agents or automations share the same account.

All newly emitted structured events under the current standard MUST identify the event role and logical operator according to the event-v2 schema.

Canonical `actor_role` vocabulary:

```text
planner
builder
reviewer
validator
scheduler
merge-controller
release-controller
repository-integration-controller
```

Canonical operator fields:

```text
operator_kind: chatgpt-web | codex | claude-code | human | github-actions | woodpecker | other
operator_id: <logical executor instance>
session_ref: <opaque page/conversation/process/run alias when useful>
transport_actor: <GitHub/API identity that physically wrote the event when useful>
```

Semantics:

- `actor_role` = workflow responsibility performed by the event;
- `operator_kind` = execution surface/system;
- `operator_id` = logical executor identity;
- `session_ref` = concrete page/session/process/run alias;
- `transport_actor` = transport provenance, not logical authorship.

Dynamic operator/session identities SHOULD remain in structured events rather than GitHub labels.

`ROLE_CLAIMED` / `ROLE_RELEASED` provide attribution and routing visibility. They are not Validation PASS and not a distributed lock.

## 6. Independent Review policy

Independent Review is risk-based, not universally mandatory.

Every implementation Task/PR SHOULD resolve:

```text
required
recommended
not-required
```

Authority order remains:

```text
Frozen PRD / Contract
→ Frozen Architecture
→ PROJECT_OVERRIDES
→ Task acceptance / risk classification
→ Standard defaults
```

Semantics:

- `required` — current merge-candidate exact SHA requires Independent Review `PASS`;
- `recommended` — Review may be performed or explicitly skipped; skip is not PASS;
- `not-required` — no Review Gate exists; use `NOT_APPLICABLE`.

A lower-authority Task/Agent MUST NOT silently downgrade higher-authority `required` Review.

Typical high-risk concerns that SHOULD select `required` include security/permission/trust boundaries, public contracts, migration/data-integrity, concurrency/recovery, shared infrastructure and release-critical integration.

## 7. Independent Review execution

When Review is performed:

- reconstruct context from GitHub + pinned standard, not Builder chat history;
- bind the result to exact PR HEAD SHA;
- identify the independent reviewer operator/context;
- publish material findings and required routing;
- request real validation instead of guessing runtime facts.

For required Review, Reviewer MUST be attributable to a context independent from the Builder context. The same GitHub `transport_actor` is allowed, but `operator_id/session_ref` must make the separation auditable.

Acceptable independent contexts include another ChatGPT session, another coding/review agent, a human reviewer, or the same model in a fresh context that reconstructs facts from GitHub.

If PR HEAD changes after a required Review PASS, the old result remains historical. Re-establish affected Review on the new exact SHA before merge.

## 8. Intent admission and canonical event writer protocol

### 8.1 Canonical short-intent contract

A short intent/result is a transport input, not yet a durable canonical workflow fact. It becomes authoritative only after admission succeeds and a conforming canonical event/current-state mutation is published to GitHub.

A short intent SHOULD contain only the judgment-bearing fields the worker actually knows, for example:

```text
event or requested action
issue / PR target
status / decision when applicable
asserted SHA or unambiguous SHA prefix when identity is required
findings / result summary / reason
requested next route or dispatch when applicable
```

The executor MAY enrich an intent only with fields that are deterministically resolvable from current GitHub/repository facts, including:

```text
full exact SHA
repository / Issue / PR relation
current target/base identity
timestamp
actor_role
logical operator attribution
transport identity
schema-required routing metadata
```

A SHA prefix is acceptable only as transport input when it resolves to exactly one relevant current immutable identity. The emitted canonical event MUST contain the full exact SHA required by the event-v2 schema/policy.

Before accepting an intent, the executor MUST validate all applicable conditions:

```text
target/work-item exists and is current
identity resolves unambiguously
asserted identity is not stale for the requested action
operator/role is authorized for the transition
event payload satisfies the current schema
requested transition is legal under current durable facts
no higher-authority gate/contract is bypassed
```

If an intent is invalid, ambiguous, unauthorized, stale or requests an illegal transition, it MUST be rejected atomically. Rejection means:

- no partial canonical event publication;
- no workflow/gate state mutation;
- no silent best-effort interpretation;
- return/record a reason such as `INVALID_SCHEMA`, `AMBIGUOUS_IDENTITY`, `STALE_IDENTITY`, `UNAUTHORIZED`, or `ILLEGAL_TRANSITION`.

An executor ACK/REJECT transport response is not itself a Gate PASS. Implementations MAY persist transport ACK/rejection metadata for idempotence/audit, but canonical workflow facts remain the accepted GitHub event/current object state.

### 8.2 New-work event writer

All newly emitted structured Agent events MUST use:

```html
<!-- ai-dev:event:v2 -->
```

and:

```yaml
schema: ai-dev/event-v2
event: <EVENT_TYPE>
actor_role: <canonical role>
operator_kind: <canonical operator kind>
operator_id: "<logical operator id>"
```

Add event-specific identity/status fields required by `schemas/agent-event-v2.schema.json`.

The schema is the machine contract. Writers MUST NOT invent a parallel event version or silently redefine existing field semantics.

### 8.3 Historical compatibility

Historical `ai-dev:event:v1` remains readable historical evidence and MUST NOT be rewritten merely to upgrade format.

Consumers MAY read v1 for compatibility. **New writers MUST NOT emit v1.**

### 8.4 Event families

Current event-v2 includes, among others:

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
HANDOFF_READY
DISPATCH_REQUEST
DISPATCH_STATE_CHANGED
CI_INFRA_EXCEPTION
VALIDATION_IMPACT_DECISION
CANDIDATE_STATE_CHANGED
HIDDEN_ESCAPE_DISPOSITION
RELEASE_QUALIFICATION
REPOSITORY_INTEGRATION_RESULT
```

`TASK_CLAIMED` is retained for compatibility; cross-role flows SHOULD prefer `ROLE_CLAIMED`.

## 9. Review event invariants

`REVIEW_DECISION` records Review Policy and optional execution decision without fabricating a Review PASS.

Required safe combinations are machine-validated by `agent-event-v2.schema.json`, including:

```text
required      + perform        + NOT_RUN        → review-ready
recommended   + perform        + NOT_RUN        → review-ready
recommended   + skipped        + NOT_RUN        → merge-ready
not-required  + not-applicable + NOT_APPLICABLE → merge-ready
```

A `required` review cannot be skipped or routed directly to merge-ready. A `recommended` direct merge requires an explicit skip decision rather than an ambiguous policy-only event.

`REVIEW_RESULT` must bind to the reviewed SHA and policy. Review `PASS` is not Release PASS.

## 10. Builder / Reviewer / Validator routing

The execution architecture computes ready sets; this protocol defines how the role results are recorded.

Typical routing:

```text
Builder   → state:ready / state:changes-requested
Reviewer  → state:review-ready when Review is selected
Validator → state:validation-needed or dedicated Validation Issue
```

A Builder SHOULD continue independent executable work rather than waiting idle for Review when the execution DAG permits it.

A Reviewer SHOULD continue independent reviews even if another concern fails unless dependency structure makes downstream review meaningless or unsafe.

A Validator publishes exact-SHA environment/profile evidence. Validation-only execution does not require a branch; source fixes require a bounded task/fix branch and affected revalidation.

## 11. Merge interaction

A Task/Fix PR becomes `merge-ready` only when the deterministic prerequisites from `EXECUTION_ARCHITECTURE_STANDARD.md` are satisfied, including:

```text
current PR HEAD
+ required concern Validation
+ Review condition
+ configured required CI/profile condition
+ Issue Dependencies required for merge
+ correct target/stack topology
+ no unresolved release-significant finding
```

Before merge, re-read current HEAD/target and stale evidence. After merge, publish `MERGE_RESULT` with the source/current identity and integration target/result as required by the current schema/policy.

Merge control does not decide Release Qualification.

## 12. Dispatch / handoff interaction

A handoff becomes dispatchable only after its durable Issue contract is complete according to `LOCAL_AGENT_HANDOFF_PROTOCOL.md` and the Local Agent Handoff schema.

After `HANDOFF_READY`, prefer pointer-only invocation:

```text
Repository: owner/repo
Issue: #N
Role: <role>
Dispatch: <id>
```

Dispatch state is derived/routed according to `EXECUTION_ARCHITECTURE_STANDARD.md`. Stale dispatches are cancelled/replaced rather than repaired through chat-only instructions.

## 13. Append-oriented history

Comments/events are append-oriented. If an important event is wrong, publish a corrective/superseding event rather than silently rewriting material history.

A machine-maintained state card MAY summarize current state but is derived, not authority. If it conflicts with durable facts, recompute it.

## 14. Recovery rule

A fresh compatible Agent/session SHOULD be able to recover work from:

```text
repository
+ pinned standard revision
+ assigned Issue / PR
+ Issue Dependencies and metadata
+ exact-SHA Review/Validation evidence
+ structured events / logical operator attribution
```

It SHOULD be able to determine what is ready, what is stale, which exact identity each result applies to, and which operator/context performed it without private reasoning or previous chat transcripts.
