# v4.0 Agent Interchange Correlation Contract

Status: CANDIDATE — T-005 / Issue #77
Version: 4.0.0
Baseline: `version/v4.0.0@a9346e45f0211ecdebb7bde18a890df35866a12d`
Parent authority: `ARCHITECTURE_DECISION.md` + `OPERATION_CONTRACT.md`

## 1. Purpose

This document defines the minimal lifecycle-wide correlation/interchange contract for AI development agents, humans, CI and controllers.

It does not create a second workflow. Every interchange record is subordinate to an existing Operation, Work Item, controller action, or assurance requirement and must resolve back to durable project authority.

Core rule:

```text
Interchange transports/correlates work and evidence.
It does not own lifecycle authority, validation truth, release truth, or canonical blocker state.
```

GitHub remains the v4 reference durable profile. Transport-neutral semantics exist only at the logical envelope layer.

## 2. Why v4 needs correlation beyond v3.4

v3.4 already provides durable GitHub events, logical operator identity, dispatch, exact-SHA review/validation and pointer-only handoff. v4 adds one missing cross-cutting identity: `operation_id`.

The goal is to correlate:

```text
Operation
-> dispatch/request
-> execution result
-> review/finding/challenge
-> validation result
-> decision/controller transition
```

without creating duplicate project state.

## 3. Minimal logical envelope

```yaml
exchange:
  protocol: ai-dev/interchange-v1
  exchange_id: <unique message/event id>
  exchange_type: <family/type>

  operation_id: <parent operation id or bounded controller correlation>
  work_item_ref: <durable Issue/Task/PR ref when applicable>
  dispatch_id: <when dispatched work exists>

  subject:
    ref: <durable subject ref>
    identity_binding: <none | exact | tuple | candidate | inherited>
    identity: <required identity when applicable>

  actor:
    actor_role: <canonical role>
    operator_kind: <execution surface/system>
    operator_id: <logical operator>
    session_ref: <optional session/process/run>
    transport_actor: <optional physical writer>

  causation:
    caused_by: <exchange/event/ref>
    correlation_refs: [<durable refs>]

  payload_ref: <durable payload/event/evidence ref or inline bounded payload>
  occurred_at: <timestamp>
```

This is a logical envelope. It is not a requirement to write one giant object into every GitHub comment.

## 4. Required identity semantics

### 4.1 exchange_id

Identifies one interchange record. Retries must not fabricate a second authoritative outcome for the same idempotent action.

### 4.2 operation_id

Correlates exchange records to one logical Operation instance defined by `OPERATION_CONTRACT.md`.

A bounded controller/assurance action that is intentionally not materialized as a standalone Operation may correlate to the parent Operation plus its controller/assurance identifier. T-009 decides exact schema representation.

### 4.3 dispatch_id

Identifies one dispatch attempt/execution routing instance. Multiple dispatches may belong to the same Operation.

`operation_id != dispatch_id`.

### 4.4 subject identity

If the exchange carries truth about source/artifact/release identity, it must preserve the identity required by the owning standard. Interchange cannot weaken exact-SHA, Validation Tuple, candidate SHA/tree, or frozen release identity.

`identity_binding: inherited` means “resolve and preserve the binding required by the owning durable authority”; it is not permission to replace a required `exact`, `tuple`, or `candidate` binding with a weaker mode. T-009 owns machine enforcement and vocabulary alignment.

### 4.5 operator identity

Preserve v3.4 logical attribution:

```text
actor_role
operator_kind
operator_id
session_ref
transport_actor
```

The GitHub account/API writer is transport provenance, not sufficient logical authorship.

## 5. Exchange families

The logical protocol recognizes these families:

```text
REQUEST
RESULT
FINDING
CHALLENGE
VALIDATION
DECISION
HANDOFF
CONTROL
STATE/ROUTING NOTIFICATION
```

They are families, not necessarily new GitHub event enum values.

### REQUEST

Requests bounded execution/assurance/control work. Must reference durable authority and current identity.

### RESULT

Returns execution output/result for the requested work. It does not automatically imply acceptance.

### FINDING

Records a bounded issue/observation discovered during Review/Assurance. T-004 owns detailed finding severity/conflict semantics.

### CHALLENGE

Questions a prior result/finding/assumption. Used for adversarial/cross-review flows without overwriting the challenged record.

### VALIDATION

Carries validation request/result correlation. `VALIDATION_STANDARD.md` still owns PASS truth.

### DECISION

Carries an authority-bearing decision such as Review Policy decision or Release Qualification result. The actor/controller must already hold that authority.

### HANDOFF

Marks durable readiness for another executor/profile. User-visible trigger remains pointer-only.

### CONTROL

Carries merge/freeze/integration/controller transition outcomes.

### STATE/ROUTING NOTIFICATION

Records derived/execution routing transitions where the current protocol already requires them. It is not a new flat state machine.

## 6. Causation and correlation

Every exchange should distinguish:

```text
causation = what directly caused this record/action
correlation = what larger Operation/Task/dispatch this belongs to
```

Example:

```text
Operation O-17
  DISPATCH_REQUEST D-4
  -> DISPATCH_CLAIMED D-4
  -> IMPLEMENTATION_READY SHA-X
  -> REVIEW_REQUEST R-2 caused by IMPLEMENTATION_READY
  -> REVIEW_RESULT caused by REVIEW_REQUEST
```

This enables replay/reconstruction without treating chronology alone as authority.

## 7. Stale / duplicate / superseded semantics

### 7.1 STALE

An exchange is stale when its required subject/base/candidate/dispatch identity no longer matches current authority.

Stale evidence remains historical. It must not be silently rebound.

### 7.2 DUPLICATE

A duplicate is the same logical action/result delivered more than once due to retry/transport behavior.

Consumers must deduplicate using durable identity/idempotency basis. Duplicate delivery must not create multiple controller effects.

### 7.3 SUPERSEDED

A newer authorized dispatch/result/candidate replaces the routing relevance of an older one. The old record remains immutable history.

### 7.4 CONFLICT

Two current, credible results/findings disagree. Interchange records the conflict; T-004/owning authority resolves it. Transport ordering or majority count must not silently decide the conflict.

## 8. Idempotency

Controller/event writers must be idempotent at the action boundary appropriate to the event.

At minimum:

- retrying publication of the same accepted event must not create a second semantic transition;
- merge/freeze/integration actions must re-read current identity before effect;
- a stale retry must fail closed rather than apply to a new subject;
- event correction uses a corrective/superseding record, not silent mutation of material history.

T-006/T-009 own the stable controller-effect idempotency basis and executable reducer/schema enforcement. A fresh `exchange_id` must not be sufficient to replay the same semantic controller effect.

## 9. Mapping to current `ai-dev:event:v2`

T-005 concludes that **event-v3 is not justified yet**.

Reason:

1. event-v2 already has actor/operator attribution, dispatch identity, SHA/candidate identity, Review/Validation/Merge/Handoff/Release families;
2. its schema allows additional properties, so correlation fields can be introduced additively during T-009 if machine validation requires them;
3. v4 does not need to redefine existing event semantics;
4. a breaking event version should only be introduced if additive correlation cannot express the required invariants.

Important compatibility constraint: `event` itself is a closed enum. Adding a new event enum value is not automatically backward-compatible merely because additional payload properties are allowed. T-004/T-009 own any challenge-event mapping/versioning decision.

Therefore:

```text
current decision: extend/reuse event-v2 additively for fields only
new event-v3: NOT REQUIRED by T-005
new event enum values: NOT AUTHORIZED by T-005
```

T-009 may add fields such as:

```text
operation_id
exchange_id
caused_by
assurance_id
```

with event-specific requirements where justified, while preserving historical event-v2 compatibility.

## 10. Event-family mapping

| Logical family | Existing v2 examples | v4 treatment |
|---|---|---|
| REQUEST | `DISPATCH_REQUEST`, `VALIDATION_REQUEST` | correlate to operation/dispatch/subject |
| RESULT | `IMPLEMENTATION_READY`, `FIX_APPLIED`, `EXECUTION_PACK_STATE_CHANGED` | result remains candidate/routing evidence |
| FINDING | `REVIEW_RESULT` findings payload, `BLOCKER_REPORTED` | T-004 may add normalized finding semantics |
| CHALLENGE | no dedicated required event today | logical family; machine mapping/versioning deferred to T-009 |
| VALIDATION | `VALIDATION_REQUEST`, `VALIDATION_RESULT`, `VALIDATION_IMPACT_DECISION` | preserve Validation authority |
| DECISION | `REVIEW_DECISION`, `RELEASE_QUALIFICATION`, `HIDDEN_ESCAPE_DISPOSITION` | preserve actor/authority constraints |
| HANDOFF | `HANDOFF_READY`, dispatch events | pointer-only invocation preserved |
| CONTROL | `MERGE_RESULT`, `CANDIDATE_STATE_CHANGED`, `REPOSITORY_INTEGRATION_RESULT` | preserve controller identity checks |
| ROUTING | `ROLE_*`, `DISPATCH_STATE_CHANGED` | derived/execution routing only |

## 11. GitHub reference profile

In the GitHub profile, do not duplicate authoritative data already present in the platform object graph.

Reference mapping:

```text
Work Item contract      -> Issue body + referenced Task Pack
operation_id            -> durable field/ref in Work Item/event/pack as introduced
work_item_ref           -> Issue/PR ref
dispatch_id              -> dispatch object/event
subject identity         -> exact SHA/tree/candidate/tuple fields
operator attribution     -> event-v2 actor/operator fields
exchange history         -> append-oriented Issue/PR events/comments
current workflow routing -> canonical metadata + deterministic reducer
validation evidence      -> Validation events/evidence refs
review evidence          -> exact-head Review events/comments
controller effects       -> merge/freeze/release/integration events + repository facts
```

A single serialized Operation envelope is optional. GitHub durable facts remain the reference implementation authority.

## 12. Pointer-only handoff remains normative

Interchange does not justify longer chat prompts.

Before dispatch, all material task-specific facts belong in durable GitHub authority. User-visible invocation remains pointer-only, for example:

```text
执行 owner/repo Issue #N 的当前 READY validation dispatch。
完成 owner/repo PR #N 的当前 READY Independent Review dispatch。
```

The receiving agent reconstructs the Operation/Task context from durable refs.

## 13. No parallel state machine

Interchange must not introduce independent states such as a second `agent_state` whose transitions can disagree with canonical workflow/dispatch/provider/gate/candidate/release dimensions.

Allowed:

- immutable exchange status/provenance needed for delivery/idempotency;
- dispatch states already owned by execution architecture;
- derived correlation projections.

Forbidden:

- using interchange message status as merge/release authority;
- treating delivery ACK as task completion;
- using exchange chronology to override a Gate/Review/Validation result;
- creating a separate lifecycle controller for Agents.

## 14. Transport neutrality boundary

The conceptual envelope may be transported through GitHub, a plugin, queue, webhook, local IPC or another provider.

Transport neutrality does not mean authority neutrality.

A transport implementation must still resolve to the project’s authoritative durable facts and obey:

- identity/staleness rules;
- role/controller authority;
- idempotency;
- pointer-only/durable task contract rules;
- owning Validation/Release semantics.

## 15. Security and provenance

Interchange implementations must distinguish asserted payload fields from deterministically resolved durable facts.

Before accepting a mutating intent/event, validate:

```text
target exists/current
identity resolves exactly when required
actor/role authorized
schema valid
transition legal
higher-authority gates not bypassed
```

Invalid/ambiguous/stale/unauthorized intents fail atomically. No partial mutation.

## 16. Ownership boundaries

- `OPERATION_CONTRACT.md` owns Operation identity/composition.
- this document owns interchange correlation semantics and event-version decision.
- `GITHUB_AGENT_INTERACTION_PROTOCOL.md` remains normative for GitHub event writer/actor/intent interaction.
- `EXECUTION_ARCHITECTURE_STANDARD.md` owns reducer/dispatch/controllers.
- `VALIDATION_STANDARD.md` owns Validation truth.
- `RELEASE_STANDARD.md` owns candidate/release authority.
- T-004 owns detailed finding/challenge/conflict semantics.
- T-009 owns machine schema additions and verifier regressions.

## 17. Anti-patterns

Forbidden:

- a second Agent workflow parallel to the development lifecycle;
- a transport-specific protocol becoming universal authority;
- `event-v3` solely for renaming existing event-v2 concepts;
- reusing `dispatch_id` as `operation_id`;
- silently rebinding evidence after HEAD/candidate drift;
- majority/last-writer-wins conflict resolution;
- ACK/delivery success treated as Gate PASS;
- chat-only task detail that is absent from durable GitHub authority.

## 18. T-005 completion boundary

T-005 freezes correlation/envelope semantics and the `event-v2 additive field extension` decision only. It does not implement schema changes, reducer logic, new event enums or transport software. Those belong to T-004/T-006/T-009 as applicable.
