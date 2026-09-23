# v4.0 Operation Routing / Reducer Integration

Status: CANDIDATE — T-006 / Issue #78
Version: 4.0.0
Baseline: `version/v4.0.0@2457eaafc00be7ddae4ccee3c2fbe0deb7fe8e3a`
Owning authority: `standards/EXECUTION_ARCHITECTURE_STANDARD.md`
Inputs: `OPERATION_CONTRACT.md`, `ASSURANCE_PLAN.md`, `ADVERSARIAL_REVIEW.md`, `AGENT_INTERCHANGE.md`

## 1. Purpose

This document maps the v4 Operation protocol into the existing durable-facts → reducer → ready-set → controller architecture.

It does **not** create an Operation runtime, a second reducer, or a new source of project truth.

Core invariant:

```text
Durable GitHub/repository/evidence facts remain authoritative.
Operation/interchange facts add correlation and acceptance semantics.
The existing reducer derives current routing state.
Existing controllers perform bounded effects.
```

## 2. Authority and state ownership

The v3.4 orthogonal dimensions remain authoritative and distinct:

```text
workflow routing
Gate / Validation truth
provider/channel state
dispatch state
candidate state
release state
```

v4 adds Operation correlation/composition, not a replacement state axis that can override those dimensions.

`operation_id` identifies/correlates a logical Operation instance. It is not a workflow state, dispatch id, Task id, candidate id, or release verdict.

## 3. Reducer inputs

The reducer MAY consume these durable facts when present:

```text
Work Item / Task Issue identity
canonical Issue Dependency edges
PR / branch / current HEAD / target SHA
Operation identity/kind/subject/parent correlation
Assurance Plan requirements and results
interchange correlation: operation_id / dispatch_id / caused_by / subject identity
Review findings and aggregate judgment
Validation evidence / tuples
provider + CI facts
dispatch lifecycle facts
merge/freeze/repository-integration facts
candidate + release facts
```

Raw chat state, runtime memory, queue caches and transport ACKs remain non-authoritative.

## 4. Derived Operation projection

A reducer MAY derive an Operation projection such as:

```yaml
operation_projection:
  operation_id: <stable logical id>
  operation_kind: <PRODUCE|RESEARCH|ASSURE|DECIDE|CONTROL>
  work_item_ref: <owning durable ref>
  subject_ref: <durable subject>
  subject_identity: <resolved effective identity>
  parent_operation_id: <optional correlation>
  active_dispatches: [<dispatch refs>]
  assurance_requirements: [<refs>]
  stale_refs: [<refs>]
  requested_route: <derived next workflow route when any>
```

This object is `NON_AUTHORITATIVE_DERIVED_STATE`. It can be deleted and reconstructed.

No generic `operation_state` may be used as a substitute for workflow/Gate/provider/dispatch/candidate/release truth.

## 5. Canonical DAG rule — no third execution DAG

Issue #101 is normative for T-006:

```text
Frozen planning DAG -> materialized GitHub Task Issues + Issue Dependencies
                         = canonical live execution DAG
```

Operation relationships express lifecycle composition, causation, correlation, or assurance-local ordering. They MUST NOT independently make a Task READY/BLOCKED contrary to the canonical Work Item DAG.

Rules:

1. Task readiness/blocking comes from the owning Issue Dependency DAG plus existing gate/routing predicates.
2. An Operation dependency that represents a Task dependency must resolve to the owning durable Work Item dependency rather than create a parallel edge authority.
3. Assurance activity dependencies may order activities inside one Operation without becoming Task-DAG edges unless explicitly materialized by the Work Item authority.
4. A reducer may project Operation relationships for observability, but cannot let that projection override the canonical DAG.
5. If Operation metadata and Work Item DAG disagree, fail closed and surface a coherence/authority defect; do not pick the Operation graph as a hidden second authority.

## 6. Review aggregation: judgment and route are orthogonal

Issue #110 P2-1 is normative for T-006.

Conceptual aggregate outputs from `ADVERSARIAL_REVIEW.md` do not become one overloaded machine status.

Map them onto existing dimensions:

```text
review judgment / finding disposition  != requested workflow route
Gate truth                             != workflow routing
```

Examples:

- aggregate `PASS` may satisfy the required Review condition while workflow routing independently becomes `merge-ready` only if all other predicates pass;
- `CHANGES_REQUESTED` means unresolved review findings require a `changes-requested` route; it is not a Validation `FAIL`;
- `VALIDATION_REQUESTED` routes workflow to `validation-needed`; the requested Validation gate remains `NOT_RUN` until actual execution;
- `BLOCKED` must preserve its concrete owning cause (for example authority/evidence/environment dependency) and must not become a universal mixed Review/Gate/provider status.

T-009 owns exact schema/event mapping. T-006 freezes the separation rule.

## 7. Staleness and effective identity

Operation/interchange facts are accepted only after resolving the effective identity required by owning authority.

Typical stale causes include:

```text
PR HEAD drift
base/target drift affecting the concern
candidate replacement/thaw
superseded dispatch
closed/merged Work Item
changed authority/policy
unresolvable inherited/project-defined identity
```

Stale facts remain historical. Reducer output marks/routs them as stale/superseded and recomputes current readiness from durable current facts.

No stale evidence is rebound to a successor identity.

## 8. Stable controller-effect idempotency basis

Issue #99 is normative for T-006.

`exchange_id` is transport/exchange identity and is **not** sufficient as the sole deduplication key for controller effects.

For a controller-effecting action, the logical semantic-action identity MUST be deterministically based on at least:

```text
controller_kind
+ owning work_item_ref / authority ref
+ exact subject identity required by that controller
+ expected current-state / precondition identity
+ intended transition/effect target
```

A dispatch/action id may participate when it is the stable owning action identity. A fresh retry `exchange_id` does not create a fresh semantic transition when the semantic-action identity is unchanged.

Required behavior:

1. replay of the same semantic action is idempotent;
2. a duplicate request after the effect already exists returns/references the existing durable result rather than producing a second effect;
3. a stale retry whose precondition identity no longer matches fails closed;
4. merge/freeze/repository-integration controllers re-read current durable identity immediately before mutation;
5. corrections/supersession are append-oriented durable facts, not silent mutation of historical evidence.

T-009 owns machine schema/verifier enforcement of the stable key and negative cases.

## 9. Ready-set integration

The existing ready-set model remains authoritative.

Operation/Assurance facts only contribute predicates or correlation needed by the existing projections:

```text
BuilderReadySet
ReviewerReadySet
ValidatorReadySet
MergeReadySet
Release/Human Decision projections
```

Examples:

- an ASSURE activity may make a reviewer dispatch READY when Review Policy and identity predicates require it;
- a factual conflict may make a Validation request READY without turning Validation into PASS;
- a completed PRODUCE Operation does not make merge READY if required concern Validation/Review/dependencies remain unsatisfied.

No per-Operation queue becomes a second workflow authority.

## 10. Controller preflight

Every mutating controller performs a fresh deterministic preflight from durable facts.

At minimum:

```text
target/work item still current
subject identity still matches
canonical dependencies satisfied
required Gate/Review predicates satisfied
no unresolved blocking finding/conflict
controller role/authority valid
semantic action not already applied
transition legal from current orthogonal states
```

Controller examples remain separately owned:

- Merge Controller — concern merge only;
- Candidate Freeze Controller — PREPARED -> FROZEN;
- Release Controller — release verdict;
- Repository Integration Controller — final version -> main/baseline effect.

Operation correlation does not merge these authorities.

## 11. Replay and recovery

After cache/runtime loss, the system MUST be able to reconstruct routing by replaying/resolving durable facts.

Recovery order is conceptual, not a second workflow:

```text
read frozen/planning authority
read Work Items + canonical dependencies
resolve current refs/SHAs/candidate/release identity
read accepted events/evidence/results
resolve Operation/interchange correlation
classify stale/superseded facts
derive orthogonal current state
recompute ready sets
resume only legal controller/dispatch actions
```

A local database/cache may accelerate this computation but cannot become recovery authority.

## 12. Concurrency and conflicting facts

When current credible facts conflict:

- chronology alone does not decide;
- transport last-writer-wins is forbidden for authority-bearing results;
- unresolved Review conflict follows T-004 aggregation routing;
- runtime/factual uncertainty routes to Validation/evidence;
- duplicate controller intents resolve through semantic-action idempotency;
- authority conflicts fail closed and route to the owning higher authority.

## 13. Fast Path

Fast Path remains reduced operations, not reduced truth.

A bounded low-risk change need not materialize ceremonial Operation/Assurance objects if the required durable fact chain is already unambiguous. Existing baseline → implementation → required Validation → Review decision → GitHub fact chain → release-impact semantics remain sufficient.

## 14. T-006 completion boundary

T-006 freezes the logical reducer/routing integration only.

It does not implement:

- T-007 Work Item / Task Pack / Execution Pack field changes;
- T-008 Validation/Freeze/Hidden/Release contract changes;
- T-009 JSON schemas, event enum changes, verifier/reducer code or golden regressions;
- a new runtime database, queue service or transport implementation.

The owning normative execution architecture remains `EXECUTION_ARCHITECTURE_STANDARD.md`; this v4 artifact is the implementation/freeze input that downstream Tasks reconcile into machine contracts and final standard text.