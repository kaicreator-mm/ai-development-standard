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

A shared `transport_actor` neither proves nor negates distinct logical operators: separation is established by distinct **declared** `operator_id` / `session_ref` attribution (§7). Executor attribution is **self-declared**: the executing executor supplies `actor_role`, `operator_kind`, `operator_id`, `session_ref` and optional `delegation`, and they are accepted as the attribution source. GitHub login/account identity is transport metadata, never an executor-admission predicate, and no separate credential/Owner verification is required for normal development. Any admission decision that consumes such attribution is still governed by the source-bound admission predicate (§8.1.1); asserted fields inside untrusted transport text are claims to be verified, never self-certifying authority, and a declaration missing required attribution fields fails closed.

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

For required Review, Reviewer MUST be attributable to a declared logical context independent from the Builder context. The same GitHub `transport_actor` is allowed; reviewer independence uses distinct **declared** `operator_id/session_ref` contexts — never GitHub account identity, and no separate credential/Owner verification. The declaration itself makes the separation auditable.

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

### 8.1.1 Source-bound admission: untrusted text vs admitted canonical events

Untrusted transport content and admitted canonical events are two distinct input classes:

```text
untrusted transport content/intent = raw comment / PR body / quoted text, chat relay,
                                    tool ACK, state card — data, never admission
admitted canonical event           = an accepted GitHub event/current object that
                                    passed the full §8.1 admission predicate
```

A schema-valid event shape, marker or role assertion carried inside untrusted transport content — including a quoted/embedded event block, `actor_role=reviewer` or `HUMAN_APPROVED` text — is data. It MUST NOT be admitted by its own shape, MUST NOT acquire the authority it asserts, and MUST NOT by itself produce any canonical Review/human/Claim/gate mutation.

Beyond schema validity, an event asserting logical-operator authority is admitted only with a durably verifiable authorization source: an accepted event/current-object reference, the exact current subject, and `actor_role` / `operator_kind` / `operator_id` / `session_ref` / delegation attribution (§5; the §8.4.1 responsibility projection when work crosses operators) that is **self-declared by that executor and accepted as such** — identity/credential verification is not an admission predicate, and normal development does not suspect the declaration. Authenticated transport alone is insufficient, and a shared `transport_actor` neither proves nor negates genuine operator separation. A quoted or embedded declaration inside untrusted transport content is still not an emitted event — it remains data per the input classes above. Missing or incomplete declared attribution fails closed as `UNAUTHORIZED`/`UNKNOWN` with no canonical mutation.

### 8.2 Current canonical event writer — one Markdown/YAML envelope

All newly emitted structured Agent events MUST use the single latest-only GitHub v3 wrapper, not an older wire marker. **New writers MUST NOT emit v1** (nor any earlier wrapper); the semantic Agent Event v2 payload remains the machine schema within the envelope.

**Latest ADS writer contract:** new machine-readable Issue/PR comments MUST use the common first-line marker `<!-- ads:github -->`, followed by a single fenced YAML mapping with `schema: ads/github/v3`, `kind: event` and `data` containing an existing `ai-dev/event-v2` payload. No separate outer mutation intent is required to publish a canonical event: the authorized writer performs the existing §8.1 source admission and posts this **single event comment** only after admission succeeds.

```yaml
schema: ads/github/v3
kind: event
data:
  schema: ai-dev/event-v2
  event: ROLE_CLAIMED
  actor_role: builder
  operator_kind: codex
  operator_id: "codex:builder-1"
  task: "#120"
```

The payload is verified by `schemas/agent-event-v2.schema.json`; the common envelope is verified by `schemas/github/v4.14/structured-interaction.schema.json`. The self-declared Agent attribution belongs **only to the event payload**, not a redundant wrapper identity. Current data encoding is governed by §16. Format validation alone still grants no Claim, Review, Validation or Gate PASS. **Old `<!-- ai-dev:event:v2 -->` wrapper is not a current writer or reader format**, even though the underlying `ai-dev/event-v2` *payload schema* continues to be reused without a semantic fork.

### 8.3 Latest-only reader posture

Historical `ai-dev:event:v1` comments remain valid history and are read-only compatibility evidence.

This historical evidence statement does **not** require a v1 decoder in current writer/read tooling.

The current parser and emitter accept **only** the §16 `ads/github/v3` document marker. Older comment markers and free-form contract blocks are **historical GitHub records**, not a requirement on new parsers or writers; no compatibility adapter, re-emission, migration or dual-format acceptance is required. Retaining history is distinct from supporting historical wire formats. The underlying `agent-event-v2` field semantics remain the current canonical event payload.

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

### 9.4 Admitted-source authority (v4.11)

The §9.1–§9.3 flows consume only admitted canonical events (§8.1.1); untrusted transport content never becomes a Review fact. Deterministically:

- Raw text asserting review or human authority — for example `actor_role=reviewer`, `HUMAN_APPROVED` or a quoted/embedded event block — acquires no right, satisfies no Review condition, fabricates no human act and never supersedes a real human decision.
- An accepted current Review verdict requires declared reviewer authority: `operator_id`/`session_ref` separation from the Builder context (§5, §7), the exact current subject and a valid accepted event reference. Reviewer independence is established by distinct **declared logical contexts**, never GitHub account identity, and no Owner credential verification is a Review admission predicate. A shared login alone neither proves nor disqualifies reviewer independence; a missing or incomplete declared attribution leaves the Review condition `UNAUTHORIZED`/`UNKNOWN` and unsatisfied.
- Current accepted opposite verdicts on the same exact subject are a conflict, not a judgment: the aggregate records it through the existing conflict surface (`conflict_refs`) with judgment `BLOCKED` pending owning disposition, deterministically and invariant to arrival order, never latest-wins (§9.3).
- A prior-subject `PASS` is never reused for a successor subject: an ambiguous SHA prefix or a missing durable event/proof reference stays `STALE`/`UNKNOWN` (§9.1) and leaves the successor's Review condition unsatisfied, while the superseded `PASS` remains immutable audit history.
- An unauthorized reviewer, an invalid schema, an illegal transition or a live conflicting protected claim is rejected atomically (§8.1) with zero partial canonical mutation, and unattributed delegation/handoff or dual active owners transfer no ownership and amplify no role (§8.4.1, §8.5).

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

### Dispatch pre-publication schema admission (#783)

A producer (Controller/Scheduler/Agent, including manual/Web emitters) that materializes a **new durable canonical dispatch** MUST validate the **fully enriched dispatch object** against the exact `schemas/dispatch.schema.json` at the **effective project-pinned ADS revision** *before* publishing it as READY/QUEUED or accepted canonical dispatch. Schema presence and a parseable event marker alone do **not** prove that this particular emitted object passed. Producer normalization MUST map proposed free-form role/profile text to the **actual schema enum** only when uniquely justified by current facts; it MUST NOT invent aliases, guess a profile or silently accept an invalid `execution_profile`. This is part of existing §8.1 admission and §11 serialized publication, **not a second dispatch lifecycle/gate**.

The producer SHALL check: (1) source identity resolved to one immutable active ADS revision and verified dispatch schema bytes/currentness; (2) the candidate required fields, enum values and role/profile combinations against that schema; (3) existing source/authorization/current claim-key predicates, including serializing the publish; and (4) the exact validation result still matches the object at the write boundary. Missing/ambiguous pinned source, malformed enum, schema rejection or drift between checked and published object => `REJECTED/INVALID_SCHEMA` or `BLOCKED_STALE_SCHEMA` with **zero accepted canonical dispatch/Claim mutation**. Do not infer a dispatch PASS from unexecuted helper tests or a successful GitHub API write of unrelated Markdown.

Historical invalid dispatch records are **append-only evidence**. Do not edit them in place or silently recast invalid values as valid. Record a source-bound rejection/correction/superseding dispatch with the current legitimate revision and original reference; readback of actual accepted GitHub facts governs the result. This does not retroactively invalidate otherwise valid old tuples, authorize cross-version adoption, or require ADS to implement a second orchestration process.

**Negative/positive checks** (existing `scripts/test_protocol_schemas.py` schema fixture family): invalid profile enum and profile/role disagreement must reject; accepted canonical enum must pass; a producer given mismatched checked-schema SHA and project-pinned schema identity must **hold**, not publish; preexisting bad source remains historical while a distinct corrected emission is evaluated afresh. The schema checks prove contract syntax, not that every downstream Tally/other producer is instrumented.

Pointer-only invocation applies to every role and is MUST-level for user-visible task triggers. A trigger MAY identify only repository, Issue/PR, role and dispatch id when required to locate the durable contract. It MUST NOT duplicate task-specific SHA/branch/scope/commands/gates/review/closeout instructions.

Canonical examples:

```text
完成 `owner/repo` Issue #N。
执行 `owner/repo` Issue #N 的当前 READY builder dispatch。
执行 `owner/repo` Issue #N 的当前 READY validation dispatch。
完成 `owner/repo` PR #N 的当前 READY Independent Review dispatch。
```

A Reviewer acting independently MUST NOT modify product code in the same review role/session; findings route back through a Builder dispatch.

### Agent completion decision note (prospective; source-only)

After a Task reaches a genuine terminal `COMPLETED` outcome, its acting Agent **MUST append a concise, source-bound summary of the approach and its reason to the canonical GitHub Issue**, or refer to an already-published exact Issue comment. This is a **reporting convention** on the existing append-only Issue surface, not an `ai-dev:event` variant, fresh Task Pack, separate approval, or new Review/CI/merge/Release gate. Keep one compact report rather than duplicating source, logs or the existing accepted outcome event.

```text
TASK_DECISION_SUMMARY=REPORTED
ACTOR=declared role + operator_id (+ session_ref when available)
SUBJECT=Issue and exact PR/implementation SHA or immutable artifact ref
DECISION=bounded approach selected, alternative/trade-off and factual rationale
EXECUTION=unexpected constraint/repair, or NONE
EVIDENCE=source, tests, CI, review refs; actual PASS/FAIL/BLOCKED/NOT_RUN scope
LIMITS=unproven behavior, remaining risks and follow-up ref, or NONE_KNOWN
REUSE=existing functions/libraries/tools/patterns + refs; NONE or UNKNOWN
TASK_LEARNING=NONE_MATERIAL | resolvable task-learning-v1/v2 ref(s)
```

Any factual rationale or claim MUST be recoverable from the cited external source/test/validation/Review; self-reported intent or explanation is not independent verification. Never request or record private chain-of-thought, secrets, unobserved timing/token/cost, fabricated CI results, or unexecuted Host/Hidden PASS. Declared logical Agent attribution remains distinct from GitHub account identity (§5). `BLOCKED`/`FAIL`/superseded attempts SHOULD also report concisely to avoid success-only hindsight; all old canonical events stay historical and append-only.

**Existing Task Learning remains optional/materiality-driven:** a normal Task with no reusable learning writes `TASK_LEARNING=NONE_MATERIAL` inside its completion note, with no empty learning object. Material reusable experience follows the *existing* Task Learning v1/v2 source binding, compatible read rules and `EXECUTION_ARCHITECTURE_STANDARD.md` §30; mere comment frequency or word count never becomes evidence quality or mandatory schema fields.

### Task feedback metadata levels and evidence semantics (ADS definition only; #1175)

The above Issue closeout note is **Level 1** (minimum, every completed Agent Task). It records a concise *decision/result explanation*, not a transcript of deliberation. `DECISION` SHOULD expose material alternatives/trade-offs when there was a genuine choice; `EXECUTION` distinguishes encountered faults and their actual treatment from speculative risks in `LIMITS`. `REUSE` MUST identify relevant existing function/library/API, shared helper, Skill/tool or established design pattern with resolvable refs when material; `NONE` means no such reusable component was used or identified, and `UNKNOWN` means not assessed/observed. Do not claim a new helper as *existing* reuse. `EVIDENCE` explicitly names executed vs skipped/unavailable checks; an Issue closure or self-reported PASS is not a successful test. Actual Task class/risk/dependencies are sourced from the owning durable Issue, not an unsupported model self-grade.

**Level 2 is conditional engineering learning**, not a second mandatory Issue comment: only material reusable findings become existing `task-learning-v1/v2` evidence. Use the existing v2 `execution_friction_class`, recurrence, root-cause relation, prevention-point references and source/currentness contract when applicable; a conclusion such as "same root cause" requires the existing evidence linkage. Otherwise `TASK_LEARNING=NONE_MATERIAL` is the complete fast path. No private chain-of-thought, standalone hindsight summary or subjective assessment may masquerade as v2 `BEHAVIOR_SUPPORTED`.

**Level 3 is a read-only derived analysis contract**, not a new event family, runtime, reporting gate or automatic ranking authority. Downstream consumers may join Level 1 comments, actual GitHub Task/PR/CI/Review/Host evidence and Level 2 records by durable identity and source; they MUST retain per-claim evidence classes `OBSERVED` (externally evidenced event or outcome), `SELF_REPORTED` (Agent statement without independent proof), `INFERRED` (consumer interpretation with source and limitation), and `UNKNOWN` (missing/ambiguous). An observed **comment** proves only that a comment exists; its assertion of correctness remains self-reported absent the cited outcome. Cost/tokens/timing/tool-call success are `UNKNOWN` without trusted measurement, never estimated to fill a report. In-progress, blocked, failed, skipped and superseded attempts remain visible in any purported completion/success denominator.

Role-sensitive fields SHOULD stay subordinate to applicable evidence owners: Builder reports implementation/reuse/change and actual failures; Reviewer reports review strategy, source-bound findings and blind spots; Validator reports what really ran, environmental limitations, skipped checks and falsification; Planner/Architect reports authority-bound options/assumptions and downstream ambiguity. Reviewer and Validator notes do not mint their own Review/Validation PASS or override their owning structured result. A multi-role or provider-routed execution preserves distinct self-declared logical `operator_id`/`session_ref` contexts even when transported through one GitHub user; claimed model names/capabilities are not automatically measured identities.

Synthesis and Agent effectiveness claims MUST declare comparison cohort and observation coverage: role, Task type/scope/risk, environment and applicable gates, independent Review/defect disposition, later revisions/regressions, retries and actual measurable resources. Distinguish implementation defects from environmental/tool failures and review-detection work; separate observed from unobserved trials. Raw completed Issue count, comment length, CI count, self-reported PASS, GitHub actor name, speculative time/cost and small biased samples are **not** valid standalone quality rankings. Derived suggestions may inform existing Task Learning / ADS Evolution Intake only; they cannot change normative ADS standards, automatically reassign Agent authority or approve Release.

See [Agent Task Feedback Metadata Reference](../references/AGENT_TASK_FEEDBACK_METADATA_REFERENCE.md) for concise positive/negative Issue examples, optional role fields and the level/source matrix. This reference does not add machine-schema fields, a new producer API, provider telemetry obligations or Tally execution ownership; any downstream runtime implementation requires separate Product/L2/Task authority.

If GitHub write access is unavailable, report `TASK_DECISION_SUMMARY=NOT_PUBLISHED` with the actual transport blocker to the existing handoff/visible execution channel, then repair the comment when possible. Do not forge a comment URI, suppress genuine completion or manufacture a new Gate FAIL/PASS solely from comment delivery. **Only a downstream orchestration consumer** (e.g. Tally) MAY periodically summarize actual Issue+CI+Review+Task Learning evidence; compare Agent outcomes only within similarly risky/difficult roles/environments with counts and missing-data qualifiers, not by raw Issue closes or self-rated success. Such analysis does not grant new Agent authority or modify ADS standards automatically.

### Passive Task execution metadata: collection, storage and use (prospective ADS consumer contract; #1177)

This subsection is the **normative semantics of a passive, provider-neutral execution-observation and learning data plane**. It extends the existing Level 1–3 Task decision/feedback convention, **not** the canonical `ai-dev:event-v2` family, Interchange, Task/Dispatch/Claim authority, validation/review/release verdicts, or any historical v4.8/v4.9 metadata schema. A user-selected **separate implementation project** may supply adapters/receipts/databases, but ADS supplies only rules of interpretation; it neither implements a collector nor presumes that Tally, ZCode, Claude Code, Codex or any provider supports a common hook API.

**WHAT — minimum field semantics and capture classes.** A consumer that accepts a material normalized observation MUST preserve the following or mark material missing identity/fields as `UNKNOWN`/`UNRESOLVED` rather than invent values:

| Logical property | Required meaning |
| --- | --- |
| `observation_id` / `source` | Stable source-namespaced identity with provider run/call/retry/delivery scope; adapter name/version, native event ref, native protocol or OTel convention mapping revision and provenance |
| `observed_at` / `ingested_at` | Source timestamp with precision/timezone/clock basis vs ingest timestamp; observed duration/monotonic scope if available; no causal assumptions from arrival order |
| `work_context` | repo/Task/Issue ref, accepted Dispatch/Claim/Attempt and parent-child relations **if actually resolved**, exact code/PR/ADS immutable pin if available; never a mutable branch as proof |
| `actor` / `operation` | self-declared logical `operator_kind/operator_id/session_ref/role`, separate GitHub transport actor; model/provider/profile and environment if actually seen; session/step/tool/model request/trace/span IDs |
| `outcome` | observed operation completion/error/retry/timeout/cancellation/blocker/unknown with source and scope, **not** Task completion or Gate PASS |
| `measurement` | metric, numeric value/unit/window, original provider vocabulary, source/billing/pricing basis, epistemic class and missing/coverage basis; no invented zeros |
| `evidence` | `OBSERVED | SELF_REPORTED | INFERRED | UNKNOWN` **per claim**, resolvable external ref, source integrity/currentness and `COMPLETE | PARTIAL | UNKNOWN` capture coverage |
| `privacy_class` | `PROJECT_PRIVATE | RESTRICTED | PUBLISHABLE` from source authority; without explicit clearance, data cannot become public merely by being normalized |

Capture classes are (i) engineering identity/Task/attempt/Claim and exact source, (ii) step/tool/Skill/model and retry/escalation events, (iii) actual token/cache/time/tool-count/cost/resource measurements, (iv) CI/Review/Validation/Host/artifact/failure evidence, (v) Level 1 decisions, reuse, constraints and material Task Learning. **Only actually supported/authorized classes are collected**. Missing hooks or limited SDK logs permit a durable-only capture profile; unobserved intermediate steps/cost/time/tokens must remain unknown. A capture profile SHOULD document provider/agent/tool version, supported signals, permissions, sampling, known drops and unavailable fields; `SUPPORTED` does not prove a specific event was emitted.

**HOW — source adapters, correlation and fidelity.** Accepted input surfaces MAY include native hook/SDK/CLI events, MCP/tool wrappers, OpenTelemetry (OTel) traces/logs/metrics, measured Host/process data, authoritative read-only GitHub/CI, and Task Issue comments. Do not claim all providers offer equivalent callbacks. OTel GenAI `gen_ai.operation.name`, provider/model, tool spans and token attributes MAY be mapped where emitted, but adapters MUST pin the **upstream semantic convention version and mapping**, because the GenAI vocabulary evolves. OTel trace/span IDs are correlation hints, **not** canonical ADS Dispatch IDs or accepted GitHub Claims. A native event with no reliable Task binding may be retained privately as `UNRESOLVED` but MUST NOT be assigned by closest timestamp, single shared GitHub login, or model-provider string.

Adapters SHOULD (1) minimize/redact at source; (2) durably journal source event ID, revision, timestamp and coverage; (3) normalize non-authoritatively and join only resolvable Task/Claim/Agent refs; (4) dedupe repeated delivery **without suppressing distinct physical retries**; (5) preserve out-of-order and late observations with append-only corrections and binding lineage; (6) re-read GitHub/CI/Review source before asserting truth. Same source ID + conflicting payload is `CONFLICT` pending reconciliation, never last-writer-wins; collector outage is a **collection gap**, not an Agent Task failure. A missing source/partial API page is never `NOT_APPLICABLE` or an inferred clean result.

**Measurement guards.** Differentiate Task wall time, active Agent time, model/tool latency, queue/CI/Host time and shared resource utilization. Parent/child spans, concurrent agents and waiting time are not additive wall time; do not sum overlapping intervals. Count unique logical model/tool calls separately from physical attempts/retries, avoiding duplicate receipt inflation. Provider-reported input/output token totals may **already include** cache/reasoning subdivisions; never add nested counts twice. Streaming usage without final/billed identity is partial. Preserve actually **billed** amount (currency, source and billing window) separately from estimated cost (price revision, model, unit basis, date and inferred calculation); pricing estimates are not invoices or directly comparable across currencies/providers. Unmeasured resources or unattributed shared Host capacity cannot be silently assigned to one Agent. Source evidence proves only its own observation scope. A self-reported `PASS`, a successful tool call or a closed Issue does not prove exact-source Validation/Review/Release.

**STORE — storage-neutral logical layers.** A consumer SHOULD separate (a) immutable authoritative source refs, (b) append-only raw-*safe* observation journal with source receipts/dedup/correction markers, (c) rebuildable Task/Attempt/session/trace/tool/model/evidence/usage index, and (d) versioned derived learning/evaluation reports. These are **logical** partitions, not four mandatory services. Project-selected SQLite+JSONL/private blobs, Postgres/object storage, or OTel exporters are implementation choices, not ADS dependencies. Joins MUST preserve deterministic source namespace/event/attempt identity, exact code subject and accepted actor/Claim linkage, including `BOUND | PARTIAL | UNRESOLVED | CONFLICT` outcomes. A pointer/cache/projection or retained raw trace MUST NOT supersede canonical GitHub facts. Immutable old observations stay historical; corrections/supersession/reclassification create new cited generations, not silent rewrites. Reports need source input watermark, mapping/query revision, coverage, exclusions and currentness. Storage MUST honor owner-selected retention, per-project/tenant isolation, least-privilege access, safe publication classes, source redaction and lawful deletion/derived invalidation. Ordinary collection MUST NOT require raw prompts, tool-call arguments/results, credentials, PII, Hidden Validation cases or private chain-of-thought.

**USE — existing evidence families and safe feedback.** Level 1 Issue decisions stay source-bound `SELF_REPORTED` until corroborated. Material experience MUST use existing Task Learning v1/v2 with evidence/currentness and `NONE_MATERIAL` fast path; cluster similar cases only when root-cause refs/counterexamples justify `SAME | RELATED | UNKNOWN | DIFFERENT`. A later use of a lesson may be analyzed as applied/effective/ineffective/not-applicable/unknown **only with its own source and separate method**; this does not add new v2 schema fields. Existing Agent Capability Profile v1 holds executor **claims**, Agent Capability Evidence v1 holds source-bound positive/negative/mixed observations (including `economic_measurement_status`), Role Execution Profile holds role requirements, and Skill governance owns reusable procedure publication. Derived comparisons MUST state Task type/risk/complexity, role, acceptance and Review requirements, environment, attempts (including blocked/failed), actual method and cost/coverage, observation horizon, sample size and uncertainty. A docs edit and multi-process physical integration are not an unadjusted ranking cohort; GitHub login, narrative verbosity, raw closed Issue count or uninstrumented timing are not Agent quality scores. Reports are subordinate evidence only: no automatic Agent authority, Gate waiver, merge, Release or ADS source mutation. Potential ADS changes follow ordinary Evolution Intake governance.

**Adoption and conformance boundary.** Metadata-only readback (no hooks) is conformant **if** missing per-step counters remain `UNKNOWN`; adapters adding OTel or native hooks must preserve source/map version and privacy. Reject: duplicated webhook/retry double counts; two self-declared operators merged by transport login; cost estimate presented as provider bill; raw secret prompt exported into Issue/public learning; stale SHA treated as current evidence; `UNKNOWN` interpreted as zero/green; a telemetry event treated as accepted Claim or Review/Validation PASS; a repeated lesson automatically modifying ADS. **Collection is observability, not a new Gate** and must not force costly additional CI/Host runs. The external implementation project requires its own Product/L2/Task approval and adoption of a suitable immutable ADS revision; no mandatory wire-schema family is minted here.

The provider capability/OTel crosswalk, private JSONL examples, suggested SQLite/Postgres index relationships, ten-plus negative cases and implementation handoff checklist are in `references/AGENT_EXECUTION_METADATA_COLLECTION_REFERENCE.md`, subordinate to this protocol. Where metadata touches downstream deployed runtime signals or canonical CI evidence, those original standards own the result and this clause owns only the passive execution-side correlation/learning semantics.

### v4.15 task-meta → GitHub safe consumer projection (bounded delta; #1208)

This is an **incremental publication/consumer crosswalk of the preceding §10 passive-observation owner**, not a new telemetry schema, mandatory provider hook, Task/Attempt lifecycle, Agent Event, evidence grader or GitHub state machine. The separate task-meta implementation owns adapters and private immutable storage. The prospective v4.15 **report-only** `ads/github/v4` Schema/validator (#1205) owns **exact emitted YAML field names and validation**; the frozen v3 Report/Manifest v1 remains unchanged, and old v3 Work Item/Intent/Event contracts stay executable. Do not implement a new free-text/KEY=VALUE machine projection between v3 and v4.

A publisher carrying actual task-meta observations into the *owning GitHub Issue* MUST apply this source/evidence-strength reduction **before** constructing its single bounded schema-validated `EXECUTION_SUMMARY` Report:

| Public consumer need | Existing authoritative source | Safe projection rule / unproven boundary |
| --- | --- | --- |
| Task / Run / Attempt / revision / current source | GitHub Issue/accepted Claim/Dispatch, exact code/ADS revision, task-meta source-correlated Attempt | Preserve stable owning Issue and Attempt; `Run` or child Step linkage that cannot be source-correlated is `UNKNOWN/UNRESOLVED`; no mutable branch or timestamp-only matching |
| Logical actor / session / provider | §5 self-declared logical operator and actual native Agent adapter provenance | Attribute `operator_kind/operator_id/session_ref/role` separately from GitHub transport; model/provider only when actually observed; transport account never grants role eligibility |
| Tool / Model / token / time / cost | §10 source/operation/measurement, adapter coverage and billing/pricing revision | Publish *bounded aggregates with units, window, counted scope, per-claim epistemic class and known/unknown basis*; a missing billing observation cannot be `0` or billed fact; retry/child spans are deduplicated by source identity |
| Verifier / Task result / late evidence | actual CI/Host/Review validated exact subject, not tool ACK or collector | Distinguish independently checked **strict required scope**, partial/skipped/failed and report's self-reported result; a late CI fact creates a new immutable publication revision under the v4 report contract, not mutation of canonical Task/Gate outcome |
| Learning / applicability / feedback | existing Task Learning v2 and exact GitHub Task/Review/CI refs | Only material source-bound experience and applicability limits; `NONE_MATERIAL` is valid. Downstream Tally feedback is a separate manifest-free profile inside the **same** v4 report family, never a private task-meta reply |
| Public privacy/currentness | §10 `privacy_class`, private immutable manifest and GitHub Issue visibility | Only explicit `PUBLISHABLE` sanitized fields; no raw prompt, argument, secret, CoT or detailed trace. Each publication names safe source/digest/coverage; missing or unverifiable private data stays `UNKNOWN` to GitHub-only readers |

**Reduction invariants:** (1) private Attempt/Manifest detail may be richer than GitHub summary but **never** becomes a Tally read prerequisite; (2) only identified leaf physical operations count in aggregate metrics, not both root and child span totals, and retries remain separately attributable; (3) provider-reported usage, estimated price-table spend and billed charges have **distinct bases** and source refs; (4) `COMPLETE|PARTIAL|UNKNOWN` describes observed *instrumentation coverage*, not Task quality; (5) `OBSERVED|SELF_REPORTED|INFERRED|UNKNOWN` applies per claim; (6) partial/failed/skipped attempts remain in denominators instead of being dropped from quality summaries; (7) `SHAPE_VALID_ONLY` and a successful comment POST never prove a required independent verifier PASS.

**Positive/negative consumer examples and capture-source boundary** live in `references/AGENT_EXECUTION_METADATA_COLLECTION_REFERENCE.md`; typed v4 Report profile and schema conformance are implemented under #1205/S02. The task-meta Publisher, Tally GitHub-only runtime and actual E2E are **external implementations**; none of them is proven by this normative text.

### Task Report Publication Contract (immutable manifest v1; historical v4.14 Issue comment v3; #1179/#1185)

**Pin boundary:** the following v3 publication contract remains the unchanged v4.14-pinned producer contract and historical v3-report interpretation. Under a v4.15 effective pin, §16.5 owns all new report publication; v3 non-report kinds remain current. No v4.15 writer emits the four historical v3 report kinds. The §10 Level-1 `TASK_LEARNING=NONE_MATERIAL | ref` note remains unchanged.

A Task's GitHub Issue is the **durable discoverability surface**, not an execution log database. An optional separate collector MAY store reports in OSS/S3/MinIO, a drive or an equivalent private document store, and publish **only a compact safe locator/summary** on the owning Issue. A relational database, always-on scheduler or per-step Issue updates are **NOT REQUIRED**. This is a publication **document/Issue-comment convention**, not another `ai-dev:event`, accepted Dispatch/Claim, Task state or Review/Validation/Release authority. The existing Level 1 completion decision note MUST remain satisfied, either by the same summary comment or by its exact already-published comment link: do not create redundant summaries to comply with both clauses.

**Fixed v1 manifest semantics.** The published document is UTF-8 JSON with `schema_version="ads/task-report-manifest/v1"` and these required top-level keys; a producer MUST NOT silently omit a required key, invent missing facts or reinterpret key names under the same v1 identity:

| Required key | Type and meaning |
| --- | --- |
| `schema_version` | Exact string `ads/task-report-manifest/v1`; this is a **publication document dialect**, not a registered authoritative ADS machine-schema family |
| `report_id`, `report_kind`, `revision` | Stable, source-namespaced `report_id` for one report kind and one originating Task/attempt; `report_kind` in the four-value vocabulary below; integer revision `>=1`, monotonic within that report |
| `work_item_ref`, `attempt_ref`, `attempt_binding` | Canonical repository/Issue ref, stable producer-scoped Attempt ref, and `CANONICAL_DISPATCH | COLLECTOR_ONLY | UNKNOWN`; never claim a collector-only attempt is an accepted GitHub Claim |
| `actor`, `subject_ref` | Declared logical role/operator/session (nullable when unknown, no inferred GitHub-login identity), and exact immutable implementation/artifact subject or explicit `null` when unverified |
| `generated_at`, `privacy_class`, `coverage` | UTC RFC3339 producer time (not proof of event time); `PROJECT_PRIVATE | RESTRICTED | PUBLISHABLE` from owning source authority; `COMPLETE | PARTIAL | UNKNOWN` for covered **capture scope only** |
| `source_refs`, `documents` | Source/evidence locator list (may be empty only with truthful unverified limitation); list of stored document descriptors, each containing `kind`, stable `storage_ref`, `media_type`, non-negative `size_bytes`, and lowercase 64-hex `sha256`; no empty placeholder document |
| `supersedes` | `null` for revision 1; for revision >1, exact immutable previous manifest `storage_ref` + `sha256` and previous revision |

A stored manifest has a **separate SHA-256 calculated over its published bytes**, carried in the Issue comment; it MUST NOT contain a circular self-hash. `report_id` is stable across revisions; a different Attempt or report kind needs a different `report_id`. An `EXECUTION_CORRECTION` is a separately identified `kind: report` v3 comment whose `data.corrects_ref` MUST identify the exact previously published GitHub report comment (or stable equivalent immutable report publication reference). The correction MUST explain its reason in Markdown and point to the former manifest through the previous publication; it does not erase evidence. `corrects_ref` is forbidden for other report kinds by the v4.14 Schema. The underlying `ads/task-report-manifest/v1` **object format** retains its distinct `supersedes` revision lineage; no deprecated `corrects` object or serialized `publication_key` is legal in the v3 comment. New report revisions are immutable, including associated documents. The v1 manifest object parser rejects unknown document-schema versions rather than coercing them. This rule does not authorize supporting legacy GitHub comment envelopes; the current publication wrapper remains v3. Future object-schema changes require separately versioned interface governance.

**Comment classification — latest-only v3.** Only an entire GitHub Issue can carry Labels; they are discovery hints, **not** individual comment classifications. Every new published report is a `<!-- ads:github -->` Markdown/YAML comment with `kind: report` and direct `data` matching `schemas/github/v4.14/structured-interaction.schema.json`. There is no KEY=VALUE header, `<!-- ads:task-report:v1 -->` alternate path, or redundant `PUBLICATION_KEY` property. `report_kind` uses exactly:

- `EXECUTION_SUMMARY`: normally one primary summary per terminal Attempt, satisfying or exactly linking the Level 1 decision note;
- `TASK_LEARNING`: material-only link to actual Task Learning v1/v2;
- `EVIDENCE_UPDATE`: materially new validated source/cost/CI/Review evidence;
- `EXECUTION_CORRECTION`: reference to a prior publication with explicit `corrects_ref`.

**Document publication and recovery.** Producer MUST publish sanitized documents first, validate retrievability/size/digest/access under authorized credentials, then publish the immutable manifest, and **only then** post the Issue locator comment. The report `data.manifest_ref` MUST be a durable object identity or stable access-controlled URL, never a short-lived presigned URL, access token, unapproved private data dump or public path that leaks restricted information. For private storage, keep an opaque durable object reference and authorize/redeliver temporary access links out-of-band. Hash matching proves bytes, not producer identity/permission/semantic truth. A missing/revoked/expired document is `UNAVAILABLE`, not PASS; preserve recoverable publication-failure evidence locally/in the existing handoff channel without fabricating a GitHub URL.

**Idempotency and concurrency.** Derive the publication identity from the actual owning GitHub Issue, `data.report_id` and integer `data.revision` (unambiguous tuple encoding); **do not serialize a redundant publication key field**. Before POST, search and exhaustively paginate owning Issue comments for the same derived identity, including relevant prior attempts; if an identical manifest SHA and key already exists, reuse that **actual comment URL**. Same derived identity with a different manifest SHA is `CONFLICT`: do not overwrite history or accept last-writer-wins; publish a new version/correction only after resolving evidence. GitHub's comment-create API supplies **no universal compare-and-set/exactly-once guarantee**: concurrent publishers SHOULD serialize per Task/report-key or use one bounded publisher queue, and a timeout/ambiguous POST outcome MUST be read back before retrying. If duplicate comments nevertheless occur, retain history and project one resolved primary publication with exact duplicate refs; never count the duplicate as a new Task/Attempt or new tokens/tools. `NOT_PUBLISHED` after a real transport failure is not a completed publication.

**Write frequency and rate safety.** No per-step, per-tool-call or streaming Issue writes. Default to **one terminal `EXECUTION_SUMMARY` publication for each real completed Attempt** (and truthful blocked/failed attempts when reported); extra learning/evidence/correction posts are material-only and MAY be coalesced into the summary. Batch object-store writes independently of GitHub. Publisher MUST implement queue/backpressure and provider rate-limit awareness; use Webhooks/conditional readback where practical, avoid concurrent write bursts, and honor `Retry-After`, `x-ratelimit-remaining/reset` and documented secondary constraints with bounded exponential backoff and jitter. GitHub's published limits can change or be endpoint-specific; **no static posts/minute number is a guaranteed capacity or new ADS Gate**. If the publication backlog grows, defer the GitHub index while preserving durable external receipts; do not block engineering Task completion or misreport status. The GitHub Issue comment remains a safe small report locator with actual data-coverage qualifiers, not a high-frequency metrics sink.

See `references/AGENT_EXECUTION_METADATA_COLLECTION_REFERENCE.md` §7 for the current v1 **object manifest** and v3 **Issue comment** reference with publication recovery. This clause owns only public-facing publication semantics; existing GitHub, artifact, CI Evidence, Task Learning and privacy authorities still own their respective facts.

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

## 16. GitHub Structured Interaction Contract — per-kind effective pin

**Canonical publication form:** Every **new normalized** GitHub Issue body, canonical Agent Event comment, Task Report comment, or native Issue mutation intent uses one Markdown document form:

```text
<!-- ads:github -->
```

followed immediately by one fenced `yaml` mapping and optional human-facing Markdown. The mapping MUST have **exactly three** top-level keys: `schema`, `kind`, `data`. For v4.14 all four kinds use `schema: ads/github/v3`. For v4.15, `work_item | intent | event` continue using that original v3 Schema/offline registry; only current `report` uses `schema: ads/github/v4` and the separate report-only `schemas/github/v4.15/report.schema.json`. There is **one current marker**, one safe YAML loader and explicit schema/kind dispatch, never a duplicate copy of Work Item/Event contracts. YAML aliases, duplicate keys, tags, unsafe multi-document coercions, ignored unknown kinds and multiple canonical markers are invalid.

### 16.1 Typed payload profiles — no double wrapper

| Kind | GitHub surface | Data contract / schema |
| --- | --- | --- |
| `work_item` | Canonical Issue body, stable task contract | `data.profile` selects the canonical Issue type; `data.contract` obeys its required profile. `type:task` validates the existing `schemas/task-contract.schema.json`; other Issue types have bounded profile-required fields, checked by the registered verifier. Human context/long acceptance stays Markdown. |
| `intent` | Agent/tool **request** for a GitHub native Issue mutation | `schemas/github/v4.14/structured-interaction.schema.json` plus operation-specific checks and currentness. The only six actions are `ISSUE_CREATE`, `ISSUE_CONTRACT_UPDATE`, `ISSUE_METADATA_CHANGE`, `ISSUE_DEPENDENCY_CHANGE`, `ISSUE_CLOSE`, `ISSUE_REOPEN`. No separate event/report append operation is permitted. |
| `event` | **One canonical Agent Event comment**, posted by admitted writer | `data` directly satisfies the existing `schemas/agent-event-v2.schema.json`, with the **same** self-declared actor identity and source refs as previously specified. No nested `event` or duplicate operator fields. |
| `report` | **One observational Report comment** | v4.15: §16.5 and `schemas/github/v4.15/report.schema.json`, including manifest-free feedback and correction notice. v4.14: original v3 schema/manifest semantics; historical read-only under a v4.15 pin. No serialized redundant publication key or self digest. |

The latest parser/CLI `scripts/verify_github_structured_interaction.py` uses PyYAML SafeLoader + a standard `jsonschema.Draft202012Validator` with **offline** local `$ref` registry for the existing Task/Event source Schemas; it rejects older format markers and returns `SHAPE_VALID_ONLY` or `INVALID_SCHEMA` for declared normative records. Plain unmarked discussion is not an operation. It supports a safe nested YAML mapping/list profile (duplicate keys/anchors/unsafe tags rejected); richer syntax is not implicitly accepted. `scripts/test_github_structured_interaction.py` covers all kinds and six mutation actions with negative cases. See `references/GITHUB_STRUCTURED_INTERACTION_REFERENCE.md`.


**v4.14 Schema/authority boundary:** The single `schemas/github/v4.14/structured-interaction.schema.json` contains the full structural `oneOf` dispatch, ten Work Item contract profiles, six typed Issue mutation payloads and conditional correction report. The strict source-only validator **does not copy** their field lists in Python. `SHAPE_VALID_ONLY` is not an admitted operation. Equality against live native GitHub state, true source-currentness, self-dependency cycles, no-op changes, authorized Claim and review/CI/release facts are **dynamic rules that JSON Schema cannot prove**, hence remain in the existing GitHub owner/currentness checks. Neither side may silently substitute for the other.

### 16.2 GitHub facts and authority are never in a second writable YAML state

The Issue body's `data.profile` is a **schema selector**, not a second authoritative Issue Type. Live Issue Type/`type:*` label, `state:*` status, Review Policy, native Dependencies and milestone remain **canonical GitHub objects** under `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`. A `work_item` document MUST agree with those objects to become runnable; YAML cannot mark an Issue READY merely by description. Issue IDs and parent/child DAG are **not** copied into a mutable YAML state log.

A normalized `intent` is **untrusted until admitted**. It carries target repo/Issue or null on create, self-declared logical Agent identity, asserted exact prior-currentness ref, intended change and evidence. A schema-valid intent is neither GitHub API permission nor accepted Claim/CAS. The writer MUST read current canonical GitHub facts and enforce the existing Work Item/Dispatch/Claim/review/CI transition and source-provenance rules before modifying the authoritative object. Stale/no-op/conflicting/native-invalid requests are refused with real evidence. No GitHub login-based logical Agent identity test or independent new Owner gate is introduced.

### 16.3 Event/comment and report integrity

An emitted `event` MUST go through §8.1 admission and use the single `kind: event` comment (not an intermediate event-append mutation). The existing Agent Event v2 payload machine semantics and Review/Validation/Release sources remain intact; `event` is not replaced by a generic pass/fail field. Comments containing quoted YAML or suspicious in-band records do not authorize admission.

An emitted v4.14-pinned `report` follows the historical §10 v3 publication/manifest contract. A v4.15-pinned writer follows §16.5: a private manifest is required only for `EXECUTION_SUMMARY`; feedback/correction are manifest-free. GitHub Labels apply to the Issue only. Actual readback, bounded retry, privacy and no high-frequency per-step writes remain mandatory. Current public data identity/digest is distinct from private manifest integrity.

### 16.4 Latest-only applicability and conformance

**Latest-only is scoped by kind and effective immutable ADS pin.** v4.14 readers/writers retain their original qualified v3-only behavior. v4.15 readers/writers keep original v3 Work Item/Intent/Event **current executable** shape/authority, emit only v4 reports, and may read original-schema v3 reports **historical read-only** with missing new facts UNKNOWN. The offline original v3 root and Task/Event registry remain byte-identical. A v3-only reader rejects or cleanly ignores v4 reports. v4 non-report/unknown pairs fail closed, never partially parse as an admitted action. Older v1/v2 wrappers remain unsupported; no bulk rewrite, Claim rebind or automatic migration occurs. `SHAPE_VALID_ONLY` never grants native authority.

No new GitHub runtime, controller, standalone database, secret storage, review stage, Agent identity credential requirement, migration job or Release Gate is introduced. The bounded shape checker validates the portable document fields only. Real GitHub/OSS auth, state admission, atomic conditions, durable comment readback and object ACL enforcement belong to the authorized implementer and are **NOT validated by CI shape tests**.


### 16.5 v4.15 report-only profiles, revisions and public digest

`schemas/github/v4.15/report.schema.json` is a strict Draft 2020-12 root accepting only `schema: ads/github/v4`, `kind: report`, and exactly three discriminated `data.report_kind` profiles. Unknown properties at every typed object level and missing fields fail closed. The reference verifier is read-only and returns `SHAPE_VALID_ONLY`, never Task/Claim/Review/Validation/Release PASS.

Common required fields are `report_id`, integer `revision >=1`, `publisher_namespace`, `report_kind`, `subject`, `actor`, UTC `observed_at`, safe `source_refs`, explicit `limits`, and `supersedes`. `subject` binds repository/actual canonical Issue, Task/Attempt, `attempt_binding`, exact `source_sha`, immutable `ads_revision`, `ads_profile=ads/github/v4:report` and source-backed `currentness`. Actor role/operator/session are declared logical attribution; nullable `transport_actor` is not authentication or ownership proof. A schema-valid source ref remains an assertion until the consumer witnesses the owning source. `observed_at` is producer observation time, not proof of execution time.

| Profile | Required bounded data and limits |
| --- | --- |
| `EXECUTION_SUMMARY` | `capture_coverage`, per-metric `metrics` (`name/value/unit/epistemic/coverage/source_refs/currentness`), explicit `cost`, leaf-only `aggregation`, exact-subject `verifier`, stable private `manifest_ref` + lowercase `manifest_sha256`, `manifest_access`, and `learning`. Capture COMPLETE is collector scope, never strict Task completion. Time/tool/token/cache metrics are observed aggregates, not mandatory fabricated counters. Include failed/retried/partial leaf Attempts and exclusions; never sum parent and children or count duplicate reports as new Attempts. Cost UNKNOWN has null value; BILLED requires actual observed billing source; ESTIMATED has explicit pricing basis and must not be relabelled billed. The private manifest is task-meta-owned; its digest is a separate claim, not verified by the public comparator. |
| `EXPERIENCE_USE_FEEDBACK` | `publisher_source_sha` (actual Tally build), `ads_subject_sha` (exact test/qualified ADS subject), `experience_ref`, `procedure_revision`, `phase`, `epistemic`, `verifier_refs`. Manifest fields are forbidden. PRESENTED, ACCEPTED, APPLIED, SKIPPED, INDEPENDENTLY_CHECKED and OBSERVED_EFFECT are distinct observations; one never implies the next. Only INDEPENDENTLY_CHECKED may carry `verifier_refs` and requires actual observed independent evidence. Other phases may cite bounded native evidence in `source_refs`; none creates Task/Gate PASS. |
| `EXECUTION_CORRECTION` | `target` exact prior owning Issue/comment/report-id/revision/profile/namespace/Task/data-digest, sanitized `reason` and `notice=REVOKE|REDACT|DISPUTE`. No manifest, replacement metrics or replacement facts. An out-of-namespace or unsupported ownership/currentness notice is DISPUTED/UNVERIFIED and cannot automatically invalidate another logical publisher sharing one GitHub login. Native owner/authority verification belongs to the consumer, not Schema. |

Revision 1 has `supersedes:null`. Every later revision names its preceding revision, actual prior comment ref and external public `data_digest`; it is a new immutable GitHub publication. A consumer verifies that predecessor against actual native facts and same owning Issue/namespace/profile/Task/Attempt before acceptance. The new comment's own GitHub-generated ID/URL is **never prefilled in its body**. A private manifest revision additionally follows its own immutable source lineage. Public data never contains raw prompts, reasoning traces, complete tool arguments, credentials or a private manifest body. Authorized redaction may remove a leaked comment; publish a sanitized source-authorized notice/tombstone and preserve source identity without repeating leaked material. No promise to erase GitHub caches/copies.

| v3 report kind | v4.15 publication mapping |
| --- | --- |
| `EXECUTION_SUMMARY` | Initial `EXECUTION_SUMMARY` revision. |
| `EVIDENCE_UPDATE` | New immutable revision of the **same summary report_id and Attempt**, with a new task-meta manifest ref/digest and actual late CI/Host/Review source refs. No new profile/event family. |
| `TASK_LEARNING` | New immutable revision of that existing summary, new manifest ref/digest and actual Task Learning v2 source ref; absent prior summary is INSUFFICIENT_EVIDENCE. The §10 Level-1 NONE_MATERIAL/ref convention stays unchanged. |
| `EXECUTION_CORRECTION` | Notice only. Replacement facts require a separate new revision of the original summary/feedback profile. |

The public comparator is lowercase `SHA256(RFC8785_JCS(validated JSON-normalized data))` over **data only**. Store it in the actual publication/readback receipt or derived index, never inside data (no self hash). Reject duplicate keys/aliases/anchors/unsafe tags/non-JSON types/NaN/Infinity/lone surrogates before digesting. Integers outside the exactly interoperable ±(2^53−1) range must be strings; finite binary64 numbers use ECMAScript shortest representation including negative-zero normalization. Sort property names by UTF-16 code units, preserve array order and original Unicode strings, and emit UTF-8 with no insignificant whitespace. Equivalent YAML styles/map order have equal digests; materially different validated data differs. A matching public digest does not prove private manifest integrity, publisher authentication or engineering correctness. RFC 8785 Appendix B is the independent numeric oracle: https://www.rfc-editor.org/rfc/rfc8785#appendix-B.

Derived identity is `(canonical owning Issue, publisher_namespace, report_id, revision, report_kind)`. Exhaustively search/paginate and read back actual comments after lost POST acknowledgement; same identity+digest is a duplicate, different digest is CONFLICT. No last-writer-wins or atomic exactly-once promise. A witnessed native in-place edit, or changed digest on the same GitHub comment ID, makes the report UNVERIFIED/CONFLICT even if still schema-valid. Where historical original digest/edit evidence is unavailable, integrity is UNKNOWN/INSUFFICIENT_EVIDENCE. No private task-meta receipt/API/object access is required or permitted for a GitHub-only reader. Correction ownership/currentness, effective pin, native Task/PR/Review/CI facts and stronger existing gates must still be actually checked; the local helper cannot witness them.

Executable contract fixtures and positive/negative checks: `tests/fixtures/v415/` and `tests/test_v415_report.py`. `record_disposition` exposes current non-report/historical-report interpretation without admitting operations; `data_digest` validates before hashing; `validate_summary_revision` checks the supplied predecessor and new-source lineage without claiming a remote object/readback. CLI `--effective-pin v4.14|v4.15`, `--writing`, and `--data-digest` are bounded source-validation controls, not production ADS adoption or credential/permission proofs.

### 16.6 GitHub-only consumer and manifest-free feedback

A v4.15 Tally consumer MUST read canonical native GitHub Issue/Dependencies/PR/
Review/CI/Claim and report facts under the exact immutable ADS pin and §16.4
per-kind dispatch. It MUST NOT obtain task-meta private APIs, objects/manifests,
SDK, Trace or private publication receipts. Body-supplied URLs/source refs are
untrusted data, never arbitrary fetch instructions. Resolve permitted references
only through bounded canonical GitHub surfaces. A local derived index is neither
a second writable engineering truth nor a source of Claim/Gate authority.

Each affected collection MUST have complete bounded pagination/cursor readback
before absence, uniqueness, correction absence or dependency completeness is
concluded. Record actual page/query identities, terminal-page observation,
observation interval and limits. Cycles, missing pages, permission failures,
timeouts, rate limits or retry exhaustion yield UNKNOWN/INSUFFICIENT_EVIDENCE for
that scope, never an empty-success result. Honor observed 429/applicable 403
backoff within explicit request/page/retry/time budgets. GitHub surfaces are not
an atomic snapshot; material concurrent drift requires reread or UNKNOWN.

The reader MUST reconcile actual native comment ID/URL, canonical owning Issue,
data-only digest, native edit observations, source/Task/Attempt, exact ADS pin/
profile, predecessor lineage and current source authority. Same identity+digest
deduplicates; identity/digest conflict or a changed digest on one native ID never
uses latest timestamp/input order to choose a winner. Native edits remain
UNVERIFIED/CONFLICT; unavailable historical integrity remains UNKNOWN. A clear
native no-edit observation is bounded, not permanent immutability. Self-declared
`CURRENT`, capture COMPLETE, actor, manifest hash and verifier/source refs are not
witnesses of their truth. Historical reports and late native evidence cannot be
promoted into current summary capture or engineering PASS.

Before applying a correction, the consumer MUST witness the actual target
comment and align canonical repository/Issue and comment URL prefix, Task/
Attempt, original report ID/revision/kind/namespace/digest, notice subject scope,
effective ADS pin/profile, native integrity and current owning publication/
admission authority. Shape validation alone is insufficient. Mismatch or
cross-namespace notice is DISPUTED/UNVERIFIED without automatic cancellation;
missing target/authority is UNVERIFIED. One transport login for different logical
Agents grants no cross-namespace cancellation. An authorized aligned REVOKE/
REDACT invalidates only its target; DISPUTE does not replace facts. Replacement
facts require a separate verified source-profile revision. Privacy tombstones
must be sanitized; GitHub caches/copies are not guaranteed erased.

Tally feedback MUST use the same v4 `EXPERIENCE_USE_FEEDBACK` profile without a
manifest, binding actual running `publisher_source_sha`, exact `ads_subject_sha`,
effective ADS revision/profile, Task/Attempt, experience/procedure revision,
epistemic status, source evidence and explicit limits. PRESENTED, ACCEPTED,
APPLIED, SKIPPED, INDEPENDENTLY_CHECKED and OBSERVED_EFFECT are distinct; none
implies another or Task/Gate PASS. Actual independent evidence is required for
INDEPENDENTLY_CHECKED. Publication follows actual permission/currentness preflight
and native ID/body/digest readback. A lost POST ACK requires complete paginated
identity+digest reconciliation; conflict/incomplete search/concurrent ambiguity
is not permission for blind retry or an exactly-once claim. The new comment's
own ID/URL/digest belongs only in the subsequent receipt, never prefilled data.

Downstream real validation MUST independently witness the same exact Tally TS
build doing GitHub-only reading and manifest-free feedback publication, with
actual native receipts and effective credential/egress coverage. Inventory all
reader/publisher/fallback credentials, actual GitHub App installation/repository
grants or observable PAT grants and their limits, not secrets or requested-only
permissions. Unobservable effective grants remain UNKNOWN. No-private-task-meta
egress requires effective same-build/config coverage including redirects and
failure/fallback paths, a positive GitHub path and denied private path; sampled
absence or a declared allowlist is insufficient. The ADS test-only oracle does
not supply any of these runtime witnesses.

The detailed bounded contract and executable scope are in
[`GITHUB_ONLY_CONSUMER_CONTRACT.md`](../docs/implementation/4.15.0/GITHUB_ONLY_CONSUMER_CONTRACT.md).
`tests/test_v415_consumer.py` exercises offline positive/negative cases with the
existing wire helpers and a test-only oracle. Under the accepted v4.15 scope,
real downstream #1210 evidence is deferred and NOT_RUN, not an ADS source-delivery
prerequisite. Preserve `REAL_TASKMETA_GITHUB_PUBLICATION_NOT_PROVEN` and
`REAL_TALLY_GITHUB_ONLY_READER_FEEDBACK_NOT_PROVEN`; no runtime or RQ PASS follows
from this source contract or its finite tests.

### 16.7 ADS v4.16 opt-in Report v5 (separate minor-version wire)

A qualified, immutable **main** ADS v4.16 adoption SHA and source-qualified explicit v5 publication capability are required before a normal writer emits `schema: ads/github/v5`, `kind: report`. `version/v4.16`, this source candidate or a successful shape test is **CANDIDATE_ONLY**, never automatic producer/consumer migration or a second concurrent default. Existing v3 Work Item/Intent/Event and v4.15 report identity/schema bytes/current readers are unchanged. Historical v3/v4 records are governed by their actual pinned profile. v4 writers continue emitting **only** `ads/github/v4`; a v4-only reader must classify v5 as **UNSUPPORTED** and any cross-profile count/absence/completeness as `UNKNOWN/INSUFFICIENT_EVIDENCE`, never treat it as v4 or no Attempt. A v5-aware reader must dispatch each native comment using its effective immutable ADS pin, marker, report_kind, pagination/currentness and original/schema profile; it may not backfill old v4 values or silently correct a v4 report through a v5 notice. T03 owns the actual source verifier/reader code and full mixed-window tests.

The independent strict JSON Schema is `schemas/github/v4.16/report.schema.json` (Draft 2020-12). It accepts only the three report-only discriminators `EXECUTION_SUMMARY`, `EXPERIENCE_USE_FEEDBACK` and `EXECUTION_CORRECTION`; the GitHub-native `data` has a separate source-owned `publisher_namespace`, logical actor and `publication` projection. **Shape validity is never GitHub permission, source authorization, a serialized Claim, Review/Gate PASS, native comment integrity or proof of external provider effect**. The v5 publishing authority MUST read back actual owning GitHub object, immutable effective ADS/producer pin, Task/Attempt and issue scope, matching publisher namespace, `PUBLISHABLE` source-authority clearance and bounded public projection *before* posting; self-declared `publication.classification=PUBLISHABLE`, `clearance_ref` and `projection_digest` are assertions until independently source-verified. `PROJECT_PRIVATE`, `RESTRICTED`, missing clearance, raw provider/model routing, credentials, prompts, hidden evidence, invoices or unqualified links ⇒ withhold sensitive fields or the whole Report; never write a public placeholder that reveals a private ref.

Every v5 `subject` keeps the **publisher's own** non-null `publisher_source_sha` and immutable `ads_revision` separate from the observed original `source_sha/source_status/source_currentness`. The one source-null publication permitted is an **observational `EXECUTION_SUMMARY`** with `attempt_binding=COLLECTOR_ONLY`, `source_status=UNPINNED|UNKNOWN`, `source_sha=null`, `source_currentness=UNKNOWN`, typed `source_reason`, nonempty source-qualified `collector_observation_refs`, `subject.currentness.state=UNKNOWN`, explicit `verifier.status=NOT_RUN|UNKNOWN`/`subject_sha=null` and no synthetic cost, task Claim or verified PASS. It may be held without publication where authority/clearance is absent. A source-null canonical dispatch, feedback, correction or verified `PASS` is invalid. A later unrelated SHA does **not** repair old dirty bytes.

For a truly witnessed immutable artifact of the **original executed material**, an eligible same-report/Attempt summary revision may carry `source_association` (actual original-material SHA256, immutable source SHA and witnesses) and cite its native `supersedes` chain. This is a *new collector-only observation*; it does not retroactively create `CANONICAL_DISPATCH`, accepted Claim, source-current Gate or a success. Incompatible/colliding revision identities, missing predecessor pages, source association without byte witness or changed native target digest ⇒ `CONFLICT/INSUFFICIENT_EVIDENCE`, never latest-timestamp wins. C06/C08 source-only fixtures are **not** real proof of matched original bytes.

A v5 `EXECUTION_CORRECTION` always has its own pinned publisher/notice source (non-null `notice_publisher_source_sha` must equal current `subject.publisher_source_sha` under the native owner's observed source; a JSON Schema cannot prove cross-field equality). Its `target` binds **the original** canonical repository/Issue + comment URL/ID, `ads_profile=ads/github/v5:report`, original Task/**Attempt**/publisher namespace, report ID/revision/kind, exact public data digest and typed target source status/SHA (nullable only when target is UNPINNED/UNKNOWN). A source-null target is valid as historical description, never as the notice publisher's own source. `REVOKE|REDACT|DISPUTE` never modify the original GitHub comment in place. Before applying a notice, consumer must independently read back exact target and notice IDs/bodies/data-only digests, align native Issue/comment ID, Task/Attempt, report lineage, publisher namespace/authority, original source pin and full pagination/currentness. A wrong Issue, Task, Attempt, namespace, digest, profile, owner or unreachable/edited target ⇒ `UNVERIFIED/DISPUTED`; the v5 Schema is not authority to revoke another logical producer sharing a GitHub transport account. Privacy removal/tombstone is separately owner authorized and cannot guarantee historical caches are erased. Corrections and late source-associated revisions are distinct facts; no correction may be erased by arrival order.

The v5 numeric projection is bounded to public typed `metric_id`, physical/logical attempt and adapter source references, observation ID/revision, window, measurement-kind/unit and cost accounting refs. Actual source receipt identity, qualified alias equality, retry/delta/cumulative deduplication, clock comparability, billed-versus-estimated identity and completeness semantics belong to T02, not to a v5 `value` alone; **no inferred total** from schema-valid numbers. Privacy/source classification applies to every metric/model/provider/cost ref, not just the envelope. T01 source tests cover C01/C06–C10 *Schema shapes* and explicit non-schema authority refusals. Real task-meta publisher, Tally consumer, provider source/Host and GitHub native correction effects remain `NOT_RUN` until separately admitted/witnessed; no v4.16 release is qualified by this subsection alone.
