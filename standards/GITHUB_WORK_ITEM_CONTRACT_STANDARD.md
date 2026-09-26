# GitHub Work Item Contract Standard

## 1. Purpose

This standard defines the canonical GitHub Work Item contract for multi-Agent development. It owns Version Task DAG materialization, executable Issue structure, canonical metadata vocabulary, workflow-state transitions, and mutation safety.

It does not replace product/architecture authority, validation truth, review truth, or release authority.

## 2. Core authority model

```text
Frozen Planning DAG document
        ↓ materialize
GitHub Task Issues + native Issue Dependencies
        ↓
canonical live execution DAG
        ↓
Issue metadata + PR/evidence + structured events
        ↓
non-authoritative derived Version DAG View
```

Canonical responsibilities:

```text
TASK_DAG.md       = frozen planning/history checkpoint
Issue body        = stable executable work contract
Issue metadata    = canonical routing/classification/current workflow metadata
Issue dependency  = canonical live execution dependency graph
Comments/events   = append-oriented execution/evidence history
PR                = reviewable/mergeable change surface
State card        = non-authoritative derived projection
Chat trigger      = pointer only
```

A Markdown status table MUST NOT become a second live execution authority.

## 3. Recoverable Version Task DAG

Every substantial version MUST maintain a recoverable Version Task DAG.

A substantial version is one that has multiple executable concerns, cross-concern dependency, version-level validation/review/closure, or multiple Agents/roles.

Rules:

1. planning decomposition MUST be checkpointed in a repository Task DAG artifact;
2. after materialization, Task Issues + native Issue Dependencies are the canonical live execution DAG;
3. Sub-issue hierarchy expresses belongs-to hierarchy and MUST NOT be interpreted as blocked-by unless an actual Issue Dependency exists;
4. Stacked PR expresses an unmerged code-baseline dependency and MUST NOT replace Task DAG dependency;
5. Agents MUST update the owning Issue/PR/events rather than concurrently editing a shared live Task DAG status document;
6. version dashboards/state cards MAY be generated for humans/Agents but MUST be marked `NON_AUTHORITATIVE_DERIVED_STATE` and reconstructible from durable GitHub facts;
7. execution-time dependency changes MUST record rationale and update the native dependency graph when the connected capability supports it;
8. a change that invalidates frozen architecture/planning decomposition requires an explicit planning/architecture amendment.

`TASK_DAG.md` remains a frozen planning/history checkpoint during execution. A Task being claimed, started, reviewed, validated, blocked or completed MUST be reflected through the owning Issue metadata, native dependency facts, PR/evidence and structured events rather than by turning the frozen Task DAG artifact into a live lock/status table.

## 4. Canonical Work Item type

Every materialized work item MUST resolve exactly one canonical type, represented by native GitHub Issue Type when available or by one portable `type:*` label.

Canonical vocabulary:

```text
type:version
type:planning
type:research
type:research-demo
type:task
type:bug
type:fix
type:validation
type:blocker
type:release
```

Agents MUST NOT invent aliases such as `type:feature-task`, `type:wip`, or `kind:implementation` to express the same canonical semantics.

Project-local classification MAY use separate namespaces such as `area:*`, `component:*`, or `domain:*`.

## 5. Canonical workflow state

Every active executable work item MUST resolve exactly one canonical workflow state:

```text
state:planned
state:ready
state:claimed
state:implementing
state:review-ready
state:reviewing
state:validation-needed
state:validating
state:changes-requested
state:merge-ready
state:blocked
state:done
state:superseded
state:cancelled
```

Portable implementations use one `state:*` label. A native/custom field MAY replace the label only if its semantics map exactly to this vocabulary.

Unknown synonyms are non-conformant.

### 5.1 Transition model

The normal implementation path is:

```text
planned
  ↓ dependencies satisfied + contract complete
ready
  ↓ claim
claimed
  ↓ execution begins
implementing
  ↓ candidate stable
review-ready | validation-needed | merge-ready
  ↓
reviewing | validating
  ├─ failure/finding → changes-requested → implementing
  ├─ unavailable external truth → blocked
  └─ required gates satisfied → merge-ready
  ↓ merge/declared completion
 done
```

`blocked` MAY be entered from any active state when a real blocker exists. Recovery MUST re-evaluate dependencies/contract/gates before returning to a runnable state.

`superseded` and `cancelled` are terminal routing states.

An Agent MUST NOT jump from `implementing` to `done` when required Review, Validation, or merge conditions remain unsatisfied.

The `ready → claimed` transition is an admission decision, not a courtesy status update. Claim admission MUST use current durable GitHub facts and the atomic/compare-and-set semantics in section 12.1 before implementation execution begins.

## 6. Review Policy and risk

Every implementation work item MUST resolve exactly one Review Policy before dispatch:

```text
review:required
review:recommended
review:not-required
```

Material implementation/planning work SHOULD also resolve one risk classification:

```text
risk:low
risk:medium
risk:high
risk:critical
```

Risk may derive defaults but MUST NOT override higher-authority frozen requirements.

Conflicting `review:*` or `risk:*` values on the same work item are non-conformant.

## 7. Other metadata namespaces

Canonical routing namespaces MAY include:

```text
validation:<profile-or-scope>
executor:<preferred-provider>
handoff:<kind>
gate:<required-gate-kind>
area:<project-local-area>
component:<project-local-component>
domain:<project-local-domain>
```

Rules:

- `gate:*` expresses a required gate kind, never PASS/FAIL;
- `validation:*` describes routing/scope/profile, never unbound validation truth;
- `executor:*` is routing preference/capability, not current logical Agent identity;
- dynamic Agent/session identity MUST live in structured events (`actor_role`, `operator_kind`, `operator_id`, `session_ref`, optional `transport_actor`);
- labels such as `gate:pass`, `validation:passed`, `agent:web-3`, or `session:abc` are forbidden.

Gate state remains:

```text
PASS | FAIL | BLOCKED | NOT_RUN | NOT_APPLICABLE
```

and is authoritative only through the owning exact evidence semantics.

## 8. Version membership

When GitHub Milestones are available, version/release grouping SHOULD use the Milestone as the canonical membership field rather than proliferating `version:*` labels.

A capability fallback MUST be documented when the connected executor cannot create/mutate the canonical GitHub object.

## 9. Canonical executable Issue contract

An executable Work Item MUST be reconstructible without hidden chat state.

The common contract core MUST cover, as applicable:

```text
Identity / target version
Goal
Authority / Frozen Inputs
Scope / Non-scope
Dependencies
Acceptance
Validation ownership / requirements
Review Policy
Risk
Execution constraints
Allowed / forbidden changes
Failure / blocker behavior
Completion / closeout rule
Referenced durable execution/prompt artifacts
```

Type-specific templates MAY add required sections but MUST NOT remove a common field that is material to execution.

The Issue body SHOULD remain stable. Claims, runtime state changes, validation/review results, and merge history belong in metadata plus append-oriented structured events/comments.

## 10. Issue Contract readiness

No executable work item becomes `state:ready` until the durable contract is complete enough for the assigned role.

```text
CONTRACT_INCOMPLETE → no dispatch
CONTRACT_COMPLETE   → dependency/gate reduction may produce READY
```

A long chat prompt MUST NOT repair an incomplete Issue.

Any task-specific instruction required by an executor MUST exist in the assigned Issue or an authoritative repository/GitHub artifact referenced by that Issue before dispatch.

Specialized durable prompt artifacts MAY exist, but they are subordinate referenced artifacts. The Issue remains the assignment authority and the user-visible trigger remains pointer-only under `ISSUE_FIRST_TASK_TRIGGER.md`.

## 11. Type-specific canonical templates

The maintained template set MUST cover at least:

- version umbrella;
- planning / Task DAG amendment;
- research;
- research demo;
- implementation task;
- bug/fix;
- validation request/handoff;
- blocker;
- release/closure where applicable.

See `templates/GOLDEN_INDEX.md` for the normative mapping.

## 12. Multi-Agent mutation protocol

Before mutating workflow metadata, an Agent MUST:

1. re-read current GitHub facts;
2. verify the expected current state and authority;
3. verify the requested transition is valid;
4. mutate only the owning metadata/object;
5. emit durable structured event/evidence when the protocol requires it;
6. re-read/reduce if the expected state was stale.

A stale or duplicate claim MUST NOT overwrite a newer claim/state.

`ROLE_CLAIMED` is attribution/routing evidence, not a distributed lock. Controllers/reducers MUST still use current durable state.

### 12.1 Atomic Task claim / compare-and-set admission

Claim admission is a compare-and-set operation over current durable GitHub facts. For a non-concurrent `(work item, role)` claim to be accepted, the claim writer MUST re-read and verify immediately before acceptance that all applicable predicates still hold:

```text
workflow_state is claimable for this role
AND contract/dependencies/gates still permit execution
AND no incompatible active dispatch/claim exists
AND bound Task Pack / Execution Pack is current when applicable
AND expected base / requested immutable identity is current when applicable
```

For ordinary Builder work, the normal claimable states are `state:ready` and an explicitly routed repair `state:changes-requested`. A project MAY define another role-specific claimable state only when that state is already part of the canonical workflow model and the dispatch contract authorizes it.

A successful claim MUST durably identify the dispatch, work item, role and logical operator, and MUST move the owning work item through the valid `ready → claimed → implementing` path (or the canonical role-equivalent running path). The claim event/history and Issue workflow metadata together are the durable execution facts; a derived DAG view is not the lock.

At most one incompatible active claim/dispatch per `(work item, role)` is permitted unless durable higher-authority project/task policy explicitly authorizes parallel execution and defines how those dispatches are compatible.

If two schedulers/workers race from the same observed READY facts, only the first claim that is accepted against the still-current predicates may become canonical. A later competing logical operator MUST re-read current facts and reject atomically as duplicate/stale when the expected previous state or active-dispatch predicate no longer holds. Rejection means:

```text
no accepted claim event for the competing operator
no transition to claimed/RUNNING
no implementation execution or source mutation
no partial workflow-state mutation
recompute current state / ready set
```

A worker MUST NOT create or mutate implementation work before its claim is accepted. Scheduler-side JIT preparation that is part of one canonical dispatch (for example creating the predetermined task branch or Execution Pack) remains allowed, but it MUST NOT be interpreted as a worker claim and MUST be idempotent/reconstructible.

The same logical operator re-claiming the same dispatch is idempotent: it may recover/resume from the existing durable claim but MUST NOT create a second active claim or dispatch identity.

`ROLE_CLAIMED` remains attribution only. Neither a role label, a Task DAG Markdown status, a state card, nor an in-memory scheduler mutex may substitute for the durable workflow + dispatch claim predicate.

## 13. Golden conformance example

A conformant implementation Task looks like:

```text
Milestone: v0.4
Type: type:task
State: state:ready
Review: review:required
Risk: risk:high
Dependencies: native Issue Dependencies
Body: complete Task Issue contract
Trigger: 完成 `owner/repo` Issue #123。
```

The Agent reads the Issue, claims the role using the section 12.1 admission predicate, changes state through a valid transition, writes implementation/PR/evidence, and never needs hidden chat instructions.

## 14. Forbidden examples and rationale

Forbidden:

```text
state:ready + state:implementing
```

Reason: two workflow states make routing non-deterministic.

Forbidden:

```text
gate:pass
validation:passed
```

Reason: a mutable label is not exact-SHA validation truth and can become stale after HEAD drift.

Forbidden:

```text
agent:chatgpt-web-7
session:abcd
```

Reason: logical operator/session identity is dynamic structured-event data, not stable routing metadata.

Forbidden:

```text
TASK_DAG_STATUS.md is edited by every Agent and treated as current execution truth
```

Reason: concurrent document edits create a second state authority and are not an atomic representation of Issue/PR/evidence facts.

Forbidden:

```text
Agent A and Agent B both read state:ready; both begin implementation; claims are reconciled later.
```

Reason: claim admission is compare-and-set against current durable facts. The competing claim MUST be rejected before it can enter RUNNING or mutate implementation work.

Forbidden:

```text
Issue says “implement feature X”; chat prompt contains the actual branch, acceptance, tests, gates and closeout rules.
```

Reason: execution depends on hidden ephemeral instructions; the Issue contract is incomplete.

Additional maintained anti-patterns are indexed from `templates/GOLDEN_INDEX.md`.
