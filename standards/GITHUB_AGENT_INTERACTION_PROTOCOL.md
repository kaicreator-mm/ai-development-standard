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

Canonical Work Item type/state/risk vocabulary, executable Issue readiness, Version Task DAG materialization and mutation safety are owned by `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`.

Golden positive/negative conformance material is owned/indexed by `GOLDEN_TEMPLATE_STANDARD.md` and `templates/GOLDEN_INDEX.md`.

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

User-visible task invocation follows `ISSUE_FIRST_TASK_TRIGGER.md`: GitHub owns the complete task contract; chat carries only a pointer to that durable contract.

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

Every substantial version MUST maintain a recoverable Version Task DAG under `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`.

Frozen Task DAG is a planning/history checkpoint. After materialization:

```text
GitHub Task Issues + native Issue Dependencies = canonical live execution DAG
```

Sub-issue hierarchy is not execution dependency. Stacked PR is not Task DAG; use it only when code truly depends on an unmerged upstream code baseline.

A shared Markdown Task DAG status file MUST NOT be used as canonical live state. A version state card is permitted only as `NON_AUTHORITATIVE_DERIVED_STATE` and must be reconstructible from current GitHub facts.

If the connected GitHub capability cannot mutate a canonical object, follow `GITHUB_CAPABILITY_FALLBACK.md`; do not silently replace native dependency semantics with prose.

## 3. Task Issue contract

Executable Issue structure and readiness are defined by `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` and the type-specific templates indexed by `templates/GOLDEN_INDEX.md`.

A Task Issue MUST contain or reference all material execution facts applicable to the assigned role, including:

```text
Task ID / goal
scope / non-scope
frozen inputs
planning DAG reference
Task Pack / durable execution artifact references
baseline / integration target
acceptance criteria
required gates and validation ownership
Review Policy
risk
dependency summary
execution constraints
allowed / forbidden changes
failure / blocker handling
completion rule
```

The Issue body SHOULD remain relatively stable. Do not use repeated Issue-body rewrites as an event log. Current events, claims, validation, review and merge history belong in canonical metadata/comments/events.

Before a task is invoked in another Web session, Local Agent, Reviewer, Validator or automation, the assigned Issue MUST contain or reference all task-specific execution facts required by the receiver. Missing task detail MUST be materialized in GitHub authority first; a longer chat prompt is not a valid substitute.

Invocation then follows `ISSUE_FIRST_TASK_TRIGGER.md` and MUST be pointer-only. If a new task-specific requirement is discovered, update the Issue/referenced authority before re-invocation.

## 4. Metadata dimensions

Canonical metadata vocabulary and invariants are normative in `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`.

Every materialized Work Item MUST resolve exactly one canonical type. Every active executable Work Item MUST resolve exactly one canonical workflow state. Implementation work MUST resolve exactly one Review Policy before dispatch.

Canonical type vocabulary:

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

Canonical workflow states:

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

Review Policy:

```text
review:required
review:recommended
review:not-required
```

Risk:

```text
risk:low
risk:medium
risk:high
risk:critical
```

Projects MAY use native Issue Types/custom fields when available only when semantics map exactly to the canonical vocabulary. Individual Agents MUST NOT invent aliases/synonyms for canonical workflow dimensions.

Portable routing namespaces MAY include `validation:*`, `executor:*`, `handoff:*`, `gate:*`, and project-local `area:*` / `component:*` / `domain:*` classifications.

Workflow routing state is not Gate state. Gate state remains only:

```text
PASS
FAIL
BLOCKED
NOT_RUN
NOT_APPLICABLE
```

`gate:pass`, `validation:passed`, Agent/session identity labels, and other mutable substitutes for exact evidence are forbidden.

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

Dynamic operator/session identities MUST remain in structured events rather than GitHub labels.

`ROLE_CLAIMED` / `ROLE_RELEASED` provide attribution and routing visibility. They are not Validation PASS and not a distributed lock.

## 6. Independent Review policy

Independent Review is risk-based, not universally mandatory.

Every implementation Task/PR MUST resolve:

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

Historical `ai-dev:event:v1` comments remain valid history and are read-only compatibility evidence.

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
DISPATCH_CLAIMED
EXECUTION_PACK_STATE_CHANGED
CI_INFRA_EXCEPTION
VALIDATION_IMPACT_DECISION
CANDIDATE_STATE_CHANGED
HIDDEN_ESCAPE_DISPOSITION
RELEASE_QUALIFICATION
REPOSITORY_INTEGRATION_RESULT
```

`TASK_CLAIMED` is retained for compatibility; cross-role flows SHOULD prefer `ROLE_CLAIMED`.

### 8.4.1 Additive responsibility projection fields

`DISPATCH_REQUEST` / `DISPATCH_CLAIMED` events and the dispatch objects they reference MAY carry the additive same-family responsibility projection when work is executed across operators:

```text
parent_dispatch_ref: <dispatch_id of the causal parent/transferor dispatch>
responsibility_mode: DELEGATED_SUBWORK | RESPONSIBILITY_HANDOFF
```

These fields project the responsibility/control semantics settled by `EXECUTION_ARCHITECTURE_STANDARD.md` section 28 onto the existing dispatch/event family; they consume those semantics and never redefine or replace them.

- `DELEGATED_SUBWORK` names the delegating parent dispatch, so requester/delegator, causal parent, executor/operator and bounded scope reconstruct deterministically from durable facts.
- `RESPONSIBILITY_HANDOFF` is valid only when the transferring operator (`created_by` on the dispatch; the parent dispatch owner on the event), the receiving operator (`claimed_by` on the dispatch; `operator_id` on the claim event), the scope and the exact work identity are all durably named. A handoff must then be distinguishable from an ordinary supersession.
- The fields are optional and additive: historical dispatches/events without them remain valid, exactly as for the claim-provenance precedent (`admission_mode` / `protected_claim_key` / `claim_generation`).
- They create no authority, no new event type, no workflow/dispatch state, no second lifecycle and no responsibility registry/ledger. A required responsibility fact that is missing, duplicate or unresolvable fails closed: responsibility/causation reconstruction reports UNKNOWN instead of guessing, and a second active `RESPONSIBILITY_HANDOFF` of the same work identity is rejected like any incompatible second claim.

### 8.4.2 Additive serialized-admission projection fields (v4.10)

Current dispatch/admission/claim writers SHOULD project the serialized-admission facts with the additive optional fields below; they consume `EXECUTION_ARCHITECTURE_STANDARD.md` §11.1.1 semantics and never redefine them. Omit all fields for ordinary dispatches; historical events without them remain valid and require no migration.

```yaml
execution_environment: WEB | LOCAL
scheduler_origin: WEB | LOCAL
source_proposal_ref: "#861@6016320778"
canonical_admission_ref: "#861@6016591816"
protected_claim_key: "kaicreator-mm/ai-development-standard#861:planning_reference_designer:__default__"
admission_generation: 3
compatibility_group: null | "<group>"
compatibility_authority_ref: null | "#<issue>@<comment-id>"
```

Writer rules:

- `execution_environment` is the canonical coarse environment (`WEB | LOCAL`). `TARGET_ENVIRONMENT` appears only in historical durable comments as a proposal-era alias; a writer observing disagreement between the alias and the canonical field fails closed (`STALE`) instead of guessing. `execution_environment` on dispatches is distinct from the validation-gate `environment` on `VALIDATION_*` events and from `operator_kind` (provider provenance).
- `source_proposal_ref` / `canonical_admission_ref` are durable `#<issue>@<comment-id>` references; prose descriptions are not durable and MUST NOT replace them on current admission/claim writers.
- `protected_claim_key` is audit-only provenance equal to the deterministic serialization `repo#task:role:group`; slot 4 is the normalized compatibility group (`__default__` when omitted) and never a revision/session identifier.
- A losing proposal is dispositioned `STALE | SUPERSEDED | REJECTED` on its own dispatch record; it never rewrites or deletes canonical facts, and scheduler wake-ups/checkpoints remain `NON_AUTHORITATIVE_DERIVED_STATE` with terminal precedence.

### 8.5 Accepted Claim as Start Record and ownership visibility

The accepted `DISPATCH_CLAIMED` / current accepted Claim is the durable Start Record for authoritative role execution. A worker MUST NOT begin authoritative role execution or mutate implementation source before its dispatch Claim is accepted (`NO_CLAIM_NO_EXECUTION`). A rejected, stale or duplicate claim means STOP/recompute, not best-effort execution. No label, comment, state card, transport ACK, progress message or heartbeat substitutes for accepted Claim authority.

New writers recording an accepted `DISPATCH_CLAIMED` SHOULD make the start auditable with existing event-v2 fields and, where the transport supports it, additive provenance:

```text
work item / issue + dispatch_id
actor_role
operator_kind + operator_id
session_ref when available
occurred_at / accepted-time durable reference
execution_profile
sha / expected_base_sha / requested_head_sha as applicable
task_pack_ref / execution_pack_ref as applicable
admission_mode / protected_claim_key / claim_generation as additive provenance when supported
parent_dispatch_ref / responsibility_mode as the additive responsibility projection when the dispatch carries delegated subwork or a responsibility handoff (EXECUTION_ARCHITECTURE_STANDARD.md section 28)
transport_actor when useful
```

The schema remains `ai-dev/event-v2`; no new event version or type is authorized. Optional transport-specific provenance uses the schema's existing additive-extension allowance. Historical event-v2 claims remain valid history and are not retroactively invalidated merely because a newer writer records richer optional provenance.

Accepted start MUST visibly resolve through `state:claimed → state:implementing` (or the canonical role-equivalent running state) on the current-state surface. GitHub labels, comments and state cards are reconstructible visibility/routing projections (`NON_AUTHORITATIVE_DERIVED_STATE`), never the claim lock or execution authority. Dynamic operator/session identity remains in structured durable events rather than proliferating per-session labels. A state card MAY expose active dispatch/operator/since/exact subject only as reconstructible derived state.

Terminal ownership release: when a dispatch/claim reaches `DONE`, `FAILED`, `BLOCKED`, `CANCELLED`, `TIMEOUT`, `STALE`/`SUPERSEDED`, no ambiguous incompatible active ownership may remain once the durable terminal/release state is unambiguous; historical claim/start facts stay append-oriented; the same logical operator resuming the same dispatch is idempotent and MUST NOT create a second active claim/Start Record.

Optional progress/heartbeat remains non-authoritative transport/exchange information and MUST NOT become Task/Validation/Gate truth. Lifecycle reconciliation, terminal release and liveness/timeout semantics are owned by `EXECUTION_ARCHITECTURE_STANDARD.md` §11.

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

### 9.1 Review subject and exact-subject currentness

Every Review fact is bound to exactly one subject: the event-level exact `sha` it was published for (the reviewed PR HEAD / candidate commit). For one work item:

```text
current facts = accepted Review facts whose exact subject == the live current
                candidate subject
stale facts   = Review facts bound to any other subject
```

- Only current facts may satisfy the Review condition or feed the current finding aggregate.
- Stale facts remain immutable historical evidence: queryable as history, but never counted, re-bound or transferred as current. A previous subject's `PASS` never satisfies a successor subject, and a previous subject's findings are never silently carried into a successor aggregate.
- Successor/delta review is legal only under the existing owner rules (§7, `prompts/independent-review-bootstrap.md`): a narrow delta may use a delta review, cross-module/architecture/test-semantic change requires full re-review, and either result binds to the new exact subject.
- When the current subject or a fact's subject association is missing or ambiguous, currentness fails closed: the Review condition stays unsatisfied rather than being guessed.

### 9.2 Machine finding records

Newly emitted `REVIEW_RESULT` events that report material findings MUST be machine-reconstructible from the existing `REVIEW_RESULT.findings` surface without human interpretation: every material finding MUST be projected into `findings.records` with stable identity, severity, root-defect class and evidence. Historical payloads without `records` remain readable immutable history; they never satisfy this new-writer contract and are never promoted into a current judgment.

A newly emitted event that reports severity bucket counts MUST be exactly reconstructible from its own `records`: bucket `pN` MUST equal the number of `records` entries with `severity: PN`. A positive bucket without a matching record is an opaque material finding, and a record missing from its reported bucket is an unaccounted finding: either violation fails the current new-writer/aggregate conformance path instead of producing a judgment. Duplicate records count in the emitting event's bucket counts — the event reports them, linked to their canonical identity by `duplicate_of`. Historical bucket-only payloads remain readable history.

```yaml
findings:
  records:
    - finding_id: <stable identity of the logical finding>
      severity: P0 | P1 | P2 | P3
      root_defect_class: <root defect class projection id>
      evidence_refs:
        - <durable evidence reference>
      duplicate_of: <canonical finding_id, only on an explicit duplicate record>
```

- `finding_id` / `severity` / `evidence_refs` reuse the existing Review finding family (`schemas/review-finding-v1.schema.json` and its validators `scripts/v40_rules.py`, `scripts/v40_semantics.py`: `validate_finding_disposition`, `validate_review_aggregation`); `severity` stays in the existing `P0–P3` family. A record inlines the material finding's identity/severity/evidence block; the Review subject is inherited from the event `sha`, and `status` / `blocking` / disposition continue to belong to the existing finding/disposition flow.
- `finding_id` is stable for one logical defect across re-emission on the same subject and MUST NOT be renumbered by appearance order. Independent reviewers are not assumed to coordinate identities: two records represent the same logical defect only when they share one `finding_id`, or when one record durably declares the existing finding-family duplicate relation `duplicate_of: <canonical finding_id>` (the `schemas/review-finding-v1.schema.json` `status: DUPLICATE` + `duplicate_of` semantics, inlined). Root-defect-class equality is classification evidence, never logical-defect identity; similarity, ordering and count never establish equivalence.
- Duplicate equivalence is deterministic and fails closed. A `duplicate_of` link is valid only when the target `finding_id` exists in the same current aggregate, the target is itself canonical (not `duplicate_of`-linked: no chains or cycles), and the linked records agree on `severity` and `root_defect_class`. A missing target, a chain or cycle, or a materially conflicting linked record MUST NOT be guessed, majority-resolved or silently merged: the current aggregate fails closed instead.
- Emission and reconciliation are separate durable facts. A reviewer MAY emit a genuinely independent unlinked record; a later durable `review-finding-v1` finding fact with `status: DUPLICATE`, `resolution_code: DUPLICATE` and `duplicate_of: <canonical finding_id>` — the existing disposition family, not a new one — reconciles the two into one logical finding for the current aggregate. The disposition binds the same exact review subject (`subject_identity_ref` = the reviewed SHA); a disposition bound to another subject is stale history and is never consumed. Competing dispositions (one finding id linked to different targets), a disposition contradicting an in-emission `duplicate_of` link, an unknown finding id or target, chains or cycles across the union of emission and disposition links, and materially conflicting severity or root-defect class across a reconciled pair all fail closed — never by latest-wins, ordering, majority or count. Reconciliation never rewrites the original reviewer facts: both provenance records stay in the converged finding.
- `root_defect_class` is a projection of the root defect classes owned by `DEVELOPMENT_WORKFLOW.md` §4. It adds, removes and redefines no class, and it owns no repair routing or escalation:

```text
PRODUCT_SEMANTICS_AUTHORITY_CONTRADICTION   product semantics / authority contradiction
ARCHITECTURE_PUBLIC_CONTRACT                architecture / public contract
IMPLEMENTATION_DEFECT                       implementation defect
TEST_FIXTURE_EVIDENCE_DEFECT                test / fixture / evidence defect
ENVIRONMENT_TOOLCHAIN_EXTERNAL_BOUNDARY     environment / toolchain / external boundary
EXECUTION_ATTRIBUTION_DEFECT                execution / attribution defect
GATE_APPLICABILITY_AUTHORITY_AMBIGUITY      gate applicability 或 authority ambiguity
```

- A finding whose identity, severity, root-defect class or evidence is missing or ambiguous is not machine-reconstructible: it MUST NOT be guessed, defaulted, silently dropped or converted into a current `PASS`.
- Findings are evidence and judgment. `Evidence != Verdict != Authority`: a record supports a judgment, `REVIEW_RESULT` is a verdict fact, and merge/release authority remains with the existing Gate Authority chain. Routing a finding's root defect class to repair/escalation stays owned by `DEVELOPMENT_WORKFLOW.md` §4.

### 9.3 Deterministic aggregation

The current finding aggregate is a derived projection over durable Review facts:

- it consumes only current-subject accepted facts (§9.1); stale facts stay historical;
- a current `REVIEW_RESULT` that reports material findings without the structured §9.2 projection is not machine-reconstructible: the aggregate fails closed for that subject instead of deriving a judgment from an opaque payload;
- findings converge by stable identity or by an explicit durable `duplicate_of` equivalence (§9.2) into one logical finding while preserving every originating reviewer's provenance (`operator_id` / `session_ref` / event reference); independent IDs without that relation remain distinct findings;
- reconciliation may also arrive after emission as a durable same-subject `DUPLICATE` disposition from the existing `review-finding-v1` family (§9.2): the aggregate consumes it without rewriting the original reviewer facts, preserving both provenance records and failing closed on competing, ambiguous, stale or cross-subject dispositions;
- the result is deterministic and invariant to event order or transport arrival order;
- materially conflicting current facts fail closed: a conflicting verdict on the same subject, the same identity classified with materially conflicting severity or root-defect class, or an ambiguous or materially conflicting duplicate equivalence MUST NOT be resolved by majority, latest-wins, reviewer/model count, provider or model reputation, cost, turnaround or file count;
- reviewer/model count is coverage evidence only, never verdict authority; and
- aggregation reuses the existing aggregation contract (`schemas/review-aggregation-v1.schema.json`: `judgment` / `finding_refs` / `unresolved_blocker_refs` / `conflict_refs` under `aggregation_policy: finding-union-blocker-dominance`, with `scripts/v40_rules.py` semantics). It introduces no new event family, status dimension, lifecycle, scheduler, registry, Validation authority or Release authority.

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

### Execution profiles and pointer-only role invocation

Roles execute under one canonical dispatch architecture (`schemas/dispatch.schema.json`) with an execution profile — `LOCAL_BUILDER`, `LOCAL_VALIDATOR`, `WEB_REVIEWER`, `PLATFORM_VALIDATOR`, `CLOSURE_VALIDATOR`. Profiles configure execution authority; they never introduce separate role lifecycles or queue state machines. `BuilderReadySet / ValidatorReadySet / ReviewerReadySet` and any version-scoped Validation Handoff Queue are derived projections.

Pointer-only invocation applies to every role and is MUST-level for user-visible task triggers. A trigger MAY identify only repository, Issue/PR, role and dispatch id when required to locate the durable contract. It MUST NOT duplicate task-specific SHA/branch/scope/commands/gates/review/closeout instructions.

Canonical examples:

```text
完成 `owner/repo` Issue #N。
执行 `owner/repo` Issue #N 的当前 READY builder dispatch。
执行 `owner/repo` Issue #N 的当前 READY validation dispatch。
完成 `owner/repo` PR #N 的当前 READY Independent Review dispatch。
```

A Reviewer acting independently MUST NOT modify product code in the same review role/session; findings route back through a Builder dispatch.

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

Before merge, re-read current HEAD/target and stale evidence. After merge, publish `MERGE_RESULT` with the source/current identity and integration target/result as required by the current schema/policy, then recompute downstream ready sets — the DAG unlock of downstream READY work is automatic and requires no human prompt relay between roles.

Merge control does not decide Release Qualification.

## 12. Dispatch / handoff interaction

A handoff becomes dispatchable only after its durable Issue contract is complete according to `LOCAL_AGENT_HANDOFF_PROTOCOL.md`, `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, and the Local Agent Handoff schema.

A dispatch references Task Pack identity and, when generated, Execution Pack identity (`EXECUTION_PACK_STANDARD.md`); workers verify pack staleness and exact identity at claim time and publish `DISPATCH_CLAIMED`. The accepted Claim is the Start Record per §8.5; current-state labels/cards remain derived visibility and are never the lock. A version-scoped Validation Handoff Queue, when enabled, is a projection of Validator dispatches — pointer-only invocation into the queue never makes the queue Issue a second validation or Task authority.

After `HANDOFF_READY`, user-visible invocation MUST remain pointer-only. If a new task-specific requirement appears, update the Issue/Dispatch/authoritative artifact first and then invoke with the same pointer form. Stale dispatches are cancelled/replaced rather than repaired through chat-only instructions.

## 13. Append-oriented history

Comments/events are append-oriented. If an important event is wrong, publish a corrective/superseding event rather than silently rewriting material history.

A machine-maintained state card MAY summarize current state but is derived, not authority. It MUST use the `NON_AUTHORITATIVE_DERIVED_STATE` semantics from `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`. If it conflicts with durable facts, recompute it.

## 14. Recovery rule

A fresh compatible Agent/session SHOULD be able to recover work from:

```text
repository
+ pinned standard revision
+ assigned Issue / PR
+ Issue Dependencies and canonical metadata
+ exact-SHA Review/Validation evidence
+ structured events / logical operator attribution
```

It SHOULD be able to determine what is ready, what is stale, which exact identity each result applies to, and which operator/context performed it without private reasoning or previous chat transcripts.

## 15. Golden / Forbidden guidance

Positive and negative examples for GitHub interaction are indexed in `templates/GOLDEN_INDEX.md`.

At minimum, implementations MUST be able to distinguish:

- complete executable Issue vs chat-repaired incomplete Issue;
- one canonical workflow state vs duplicate/invented states;
- required `gate:*` kind vs false `gate:pass` truth;
- structured Agent identity vs `agent:*` session labels;
- canonical live Issue Dependency DAG vs a shared live-status Markdown document;
- pointer-only trigger vs a long second task contract.

The rationale and maintained non-conformant examples are in `templates/golden/ANTI_PATTERNS.md`.
