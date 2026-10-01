# v4.8.0 L2 Architecture Evidence — Evidence-Driven Agent Orchestration & Standard Evolution

Status: **L2 CANDIDATE — NOT FROZEN; FRESH INDEPENDENT ARCHITECTURE REVIEW REQUIRED**

Frozen Product authority:

- `docs/implementation/4.8.0/PRODUCT_FREEZE.md`;
- Frozen PRD blob `f26439580e00de6ed8b2e27d732a3095eb566219`;
- Fresh Independent Product Review R3 #490 terminal `5926142930`;
- Product dogfood basis `#469@5925124956`.

Architecture baseline: current v4.1–v4.7 owners on `main@e75fe834469c5ea9f9a384f7d84e38c3a48afa46` plus the Product Freeze checkpoint on `planning/v4.8-evidence-orchestration`.

## 1. Architecture decision

v4.8 extends the existing execution architecture with **evidence-aware eligibility, resource-aware admission, a transport-neutral exchange binding, and compact Task Learning**, while preserving all current Product/Architecture/Task/Dispatch/Review/Validation/Release authorities.

The architecture is:

```text
Frozen Task / Task Pack authority
        │
        ├── optional execution-requirement metadata
        │
        ▼
canonical READY set
        │
        ├── Agent Capability Claim/Profile
        ├── current Availability / Resource Facts
        ├── exact-subject Capability Evidence
        └── authority/currentness/independence/security constraints
        │
        ▼
Derived Eligibility Resolver
        │
        ├── hard filter: ELIGIBLE / INELIGIBLE / UNKNOWN
        └── optional project ranking among ELIGIBLE choices only
        │
        ▼
existing Dispatch reservation + atomic Claim admission
        │
        ├── optional resource/capacity binding under the same serialization authority
        └── transport-neutral Agent Exchange envelope/adapters
        │
        ▼
existing Builder / Validator / Reviewer execution
        │
        ▼
existing durable Result / Review / Validation / Merge facts
        │
        ├── Task Learning Evidence v1
        └── Standard-friction classification / ordinary ADS Intake
```

GitHub/repository/evidence stores remain durable facts. Eligibility, ranking, queues and resource-selection views remain derived state. No scheduler database, Agent profile registry, message bus, telemetry store, or ranking output becomes project authority.

## 2. Architecture invariants

The following are frozen candidates for v4.8 L2:

1. **Task requirements remain Task authority.** Eligibility metadata may extend Task Pack/Execution Pack/Dispatch references but cannot become a second Task contract.
2. **Capability claim != availability != capability evidence.** None implies authority.
3. **Capability evidence is historical/exact-subject evidence.** It may inform selection but never substitutes for current Review/Validation.
4. **Current availability is time/currentness scoped.** Stale or missing material availability becomes UNKNOWN/ineligible rather than optimistic truth.
5. **Hard eligibility precedes optimization.** Cost, latency, throughput or provider preference never makes an ineligible choice eligible.
6. **READY/Dispatch/Claim remain canonical scheduling/admission owners.** v4.8 adds no second task state machine or claim authority.
7. **Scarce resource reservation uses existing atomic admission semantics.** Resource/capacity keys extend the protected admission set; they do not create an independent scheduler authority.
8. **Reviewer/validator independence is a hard filter, not a ranking preference.**
9. **Agent Exchange is a wrapper/binding only.** Existing semantic owners still define Dispatch, Result, Blocker, Handoff, Review, Validation and Decision meaning.
10. **Transport delivery/acknowledgement is not workflow/gate truth.** Material results become durable through the existing owner before they can affect authoritative current state.
11. **Task Learning is evidence/history, not Product/Architecture/Task/ADR/incident authority.**
12. **No private chain-of-thought is required or retained.** Concise engineering rationale means externally useful decision summary/evidence refs only.
13. **Standard-friction observations cannot self-amend ADS.** Promotion returns through ordinary ADS Intake → L1 → PRD → L2 → Task/Review/Validation.
14. **v4.6 Skill Metadata remains procedure metadata, not Agent capability proof.** Skill presence may contribute to a claim but cannot prove current executor eligibility.
15. **v4.7 registry/discovery remains metadata.** New v4.8 schemas/owners are registered there but registry entries do not grant authority.
16. **v4.8 is additive/non-weakening.** Any required rewrite of historical event/Dispatch/Task authority routes to future-major instead of being hidden in v4.8.

## 3. Owner map

| Concern | Canonical owner after v4.8 | v4.8 change | Must not duplicate |
|---|---|---|---|
| Task scope / execution requirements | Task DAG / Task Pack; exact-base narrowing in Execution Pack | optional requirement fields/refs | Product/L2/Validation authority |
| Task Learning evidence semantics | `EXECUTION_ARCHITECTURE_STANDARD.md` | new evidence family + closeout semantics | Task Pack, ADR, Review/Validation result, incident history |
| Execution Pack inputs/retention refs | `EXECUTION_PACK_STANDARD.md` | optional learning/capability refs where useful | Task Learning owner |
| model/risk strength policy | `MODEL_USAGE_POLICY.md` | consume capability evidence but retain risk policy | universal ranking/scoring |
| reusable procedure/Skill | v4.6 `SKILL_PROCEDURE_GOVERNANCE_STANDARD` / Skill Metadata | referenced by capability claims | Agent capability proof |
| Agent capability claim/evidence interpretation | `EXECUTION_ARCHITECTURE_STANDARD.md` | new profile/evidence metadata families | Skill, Dispatch, Validation |
| live provider/runner/resource state | existing provider/runner/environment owner | normalized derived Availability View | capability profile/history |
| READY set / dispatch / claim / atomic admission | `EXECUTION_ARCHITECTURE_STANDARD.md` | eligibility + resource-capacity pre-admission | second scheduler state machine |
| GitHub event writer / logical operator attribution | `GITHUB_AGENT_INTERACTION_PROTOCOL.md` | GitHub adapter consumes/produces exchange binding | transport-neutral semantic owner |
| transport-neutral exchange wrapper | new `AGENT_EXCHANGE_BINDING_STANDARD.md` | one new normative binding owner | Dispatch/Review/Validation lifecycle |
| incident engineering feedback | v4.5 Incident/Recovery/Engineering Feedback | may emit Task Learning/friction refs | ADS evolution decision |
| ADS Intake / standard evolution governance | `DEVELOPMENT_WORKFLOW.md` + normal Product/L1/L2 path | explicit friction classification/promotion route | self-amending telemetry lifecycle |
| authority/applicability discovery | v4.7 canonical manifest/registry | register v4.8 owner/schema refs | semantic owner rules |

## 4. Default machine-contract families

v4.8 L2 proposes exactly **four new default machine-contract families**.

### 4.1 Task Learning Evidence v1

Candidate file: `schemas/task-learning-v1.schema.json`.

Purpose: preserve compact reusable implementation learning bound to the work/exact subject and existing evidence.

Minimum conceptual fields:

```text
schema_version
learning_id
repository_ref
work_item_ref
implementation_subject_ref?
authority_refs[]
summary
rationale_summary?
unexpected_constraint_refs[]
task_pack_or_l3_clarification_refs[]
reusable_invariant_refs[]
known_limitation_refs[]
source_test_validation_review_refs[]
confidence_layers[] = IDENTITY_BOUND | BEHAVIOR_SUPPORTED | INDEPENDENTLY_CHALLENGED
friction_classification?
currentness_ref?
disposition
```

Rules:

- `summary` / `rationale_summary` are concise externally useful engineering summaries, never private chain-of-thought;
- references are preferred over copied evidence bodies;
- exact-code behavioral claims bind to the implementation subject they actually describe;
- `TASK_LEARNING=NONE_MATERIAL` remains the proportional Fast Path and does not require an empty schema object;
- `friction_classification` may classify an observation but cannot create Product/Architecture/standard authority.

### 4.2 Agent Capability Profile v1

Candidate file: `schemas/agent-capability-profile-v1.schema.json`.

Purpose: record **declared/reusable capability claims** for an Agent/runtime/operator class without implying current availability, trust or proof.

Minimum conceptual fields:

```text
schema_version
profile_id
profile_version
agent_or_runtime_class_ref
provenance_ref
eligible_role_claims[]
declared_capability_classes[]
language_archetype_claims[]
tool_class_claims[]
environment_class_claims[]
max_agent_freedom_claim?
resource_class_claims[]
skill_refs[]
security_or_side_effect_class_claims[]
compatibility_refs[]
```

Rules:

- profile content is a claim, not proof;
- provider/model identity may be provenance but is not a correctness score;
- Skill Metadata references describe procedures available to the Agent, not demonstrated executor ability;
- credentials/tool installation do not grant side-effect authority;
- profile version changes do not rewrite historical capability evidence.

### 4.3 Agent Capability Evidence v1

Candidate file: `schemas/agent-capability-evidence-v1.schema.json`.

Purpose: record bounded observed evidence about a capability/task class without turning historical success into current PASS.

Minimum conceptual fields:

```text
schema_version
evidence_id
profile_ref?
logical_operator_or_executor_ref
provider_model_provenance?
task_class_or_capability_class
environment_or_resource_class?
role
exact_subject_ref
task_pack_execution_pack_refs[]
result_refs[]
validation_refs[]
review_refs[]
observed_findings_refs[]
measured_resource_fields?
evidence_strength
observed_at/currentness_scope
negative_or_failure_observation?
```

Rules:

- positive and negative evidence are both valid evidence;
- evidence is exact-subject / environment scoped where material;
- no universal scalar quality score is generated;
- economic/performance conclusions require comparable methodology and cannot be inferred from one task or provider label;
- historical evidence can affect assignment confidence but never current Validation or Review truth.

### 4.4 Agent Exchange Envelope v1

Candidate file: `schemas/agent-exchange-envelope-v1.schema.json`.

Normative owner: new `AGENT_EXCHANGE_BINDING_STANDARD.md`.

Purpose: carry or reference an existing ADS semantic object across GitHub/webhook/queue/local/A2A-style transports while preserving provenance, exact identity, causation and idempotency.

Minimum conceptual fields:

```text
schema_version
exchange_id
semantic_type
semantic_owner_ref
payload_ref | bounded_payload
payload_digest?
repository/work_item/dispatch refs when applicable
sender_logical_operator_ref
sender_role
receiver_role_or_capability_target?
subject_ref?
authority_refs[]
causation_ref?
correlation_ref?
reply_to_ref?
created_at
expires_at/currentness_ref?
idempotency_key
transport_provenance_ref
```

Rules:

- envelope validation never validates the embedded semantic result beyond confirming the declared owner/schema/ref;
- a `REVIEW_RESULT` remains owned by Review; a `VALIDATION_RESULT` remains owned by Validation; a `DISPATCH` remains owned by Dispatch;
- transport ACK/delivery/progress is never Gate PASS, Review PASS or Task completion;
- critical semantic changes must be materialized durably through their canonical owner;
- duplicate delivery with same idempotency identity and same payload is safe/idempotent; same identity with conflicting payload/digest fails closed;
- transient exchange state can be discarded and reconstructed from durable facts where the semantic action is authoritative.

## 5. Availability / Resource Facts — derived normalization, no fifth default schema

v4.8 does **not** introduce a universal durable `ResourceAvailability` authority.

Current availability is sourced from the existing applicable owner: CI runner/provider state, Build Host/device inventory, orchestrator adapter, project-local resource controller, or explicit manual fact. The eligibility layer normalizes those current facts into a derived view equivalent to:

```text
resource_ref
source_owner_ref
state = AVAILABLE | UNAVAILABLE | UNKNOWN
capability/resource classes
capacity / exclusive-group facts when known
observed_at
expires_at/currentness condition
source_fact_ref
```

This view is `NON_AUTHORITATIVE_DERIVED_STATE`.

Rules:

- stale/missing material availability => `UNKNOWN`, not AVAILABLE;
- UNKNOWN cannot satisfy a hard environment/resource requirement;
- current provider availability does not prove capability quality;
- a capability profile does not prove the resource is currently reachable;
- projects may retain provider-specific richer facts; normalization must not erase their owner meaning.

## 6. Task execution requirement extension

Task requirements stay with Task Pack authority. v4.8 may add backward-compatible optional fields/refs equivalent to:

```text
execution_requirements:
  required_capability_classes[]
  required_environment_classes[]
  required_resource_classes[]
  independence_constraints[]
  security_or_side_effect_constraints[]
  max_agent_freedom
  concurrency_or_resource_group_refs[]
  capability_evidence_policy?
  optimization_hints?
```

Exact-base narrowing may be repeated/referenced in the Execution Pack/Dispatch only where needed for current execution. Lower artifacts may narrow but never weaken Task requirements.

Missing optional v4.8 fields preserve historical behavior; existing Task Packs remain valid.

## 7. Eligibility Resolver

Eligibility is a deterministic **derived projection**, not a new durable lifecycle state.

For each READY `(work item, role)` candidate:

```text
Frozen/current Task requirements
+ current authority/currentness
+ Agent Capability Profile claims
+ current Availability View
+ relevant Capability Evidence
+ independence/security/write-set/concurrency constraints
        ↓
hard predicates
        ↓
ELIGIBLE | INELIGIBLE | UNKNOWN
```

`UNKNOWN` is fail-closed for any material requirement.

Minimum hard predicates where applicable:

```text
work item remains READY/claimable
Task Pack / Execution Pack current
required role allowed
agent freedom sufficient but not self-elevated
required capability class claimed
required current environment/resource AVAILABLE
required security/side-effect authority present from canonical owner
reviewer/validator independence satisfied
write-set / concurrency compatibility satisfied
exact subject/base current
capability evidence policy satisfied when Task authority requires prior proof
scarce resource capacity can be atomically reserved
```

Capability Evidence is normally advisory unless a higher-authority Task/project policy explicitly requires a demonstrated evidence class. Absence of historical success must not become a universal prohibition for new Agents unless the applicable authority says so.

Eligibility reasons SHOULD be inspectable for debugging/dogfood, but the projection is recomputed from source facts rather than becoming durable authority.

## 8. Optional ranking / assignment policy

Only `ELIGIBLE` candidates enter optional ranking.

Projects/controllers MAY rank by:

```text
Task priority / critical path
queue age
cost class
latency class
resource utilization
resource scarcity
recent retry/escalation history
integration drift risk
relevant capability evidence strength
```

Hard rules:

- ranking cannot change `INELIGIBLE` or `UNKNOWN` to `ELIGIBLE`;
- no default global scalar Agent score is introduced;
- no mandatory economic optimizer is introduced;
- cost/latency fields may be absent/NOT_MEASURED;
- provider/model labels alone cannot determine correctness ranking;
- project ranking policy is configuration/derived policy, not Product/Task authority.

## 9. Resource reservation and parallelism

v4.8 reuses `EXECUTION_ARCHITECTURE_STANDARD.md` section 11.1 atomic admission.

For exclusive or bounded shared resources, dispatch reservation MUST include the applicable resource/capacity key in the serialized admission decision. The existing protected key may be extended by higher-authority compatibility/concurrency grouping, for example:

```text
work_claim_key = (repository, work item, role)
resource_claim_key = (resource_or_capacity_group, slot_or_generation)
```

A dispatch is publishable only when both the work claim and required resource reservation are admitted consistently.

Allowed implementations remain:

```text
SINGLE_WRITER_ADMISSION
LINEARIZABLE_CONDITIONAL_WRITE
```

A project with no safe reservation primitive MUST serialize use through one designated admission writer or mark the affected concurrent assignment unavailable/blocked. A transient lease may coordinate but cannot become unrecoverable authority; accepted Dispatch/Claim/resource binding refs must remain reconstructible from durable facts.

This solves cross-Task scarce-resource races without creating a second scheduler state machine.

## 10. Dispatch / schema extensions

`schemas/dispatch.schema.json` may receive backward-compatible optional references such as:

```text
capability_profile_ref?
capability_evidence_refs[]?
eligibility_basis_ref?
resource_binding_refs[]?
assignment_policy_ref?
```

These fields explain selection/binding. They do not grant Task scope, Review/Validation authority, or side-effect permission.

Historical Dispatch payloads remain valid when these refs are absent.

## 11. Agent Exchange architecture

### 11.1 Semantic owner vs transport

The exchange envelope distinguishes:

```text
semantic_type / semantic_owner
from
transport adapter / delivery state
```

GitHub `ai-dev:event:v2` remains the canonical GitHub event writer protocol. An adapter may translate between an Exchange Envelope and the existing GitHub event/current-object facts, but it MUST NOT reinterpret semantic owner rules or create a second accepted-intent schema.

Webhook, queue, local IPC, orchestrator and A2A-style transports are adapters only.

### 11.2 Delivery and replay

The binding is compatible with at-least-once delivery:

- same `exchange_id`/idempotency key + same semantic payload/ref => idempotent replay;
- same identity + conflicting payload/digest => fail closed;
- expired/currentness-sensitive work is re-read against durable facts before action;
- transport retry never bypasses Dispatch claim admission;
- transport delivery ACK is not semantic completion.

### 11.3 Durable materialization

If an exchange changes authoritative workflow/gate/side-effect/evidence truth, the receiving controller/worker first validates authority/currentness and then publishes the canonical durable result through the existing owner. The exchange can subsequently carry/reference that durable identity.

After crash/restart, a conforming controller can recover authoritative current state without transient queue history or private chat.

## 12. Task Learning lifecycle

Task Learning is created/updated only from material execution evidence. Recommended closeout flow:

```text
implementation / tests / Validation / Review / merge facts
        ↓
material-learning check
        ├── none -> TASK_LEARNING=NONE_MATERIAL
        └── material -> Task Learning Evidence v1
                         ↓
                   Reviewable evidence/history
                         ↓
               optional friction classification
```

A Task Learning record may point to an ADR/incident/Product issue where one exists; it does not replace those owners.

Later source drift leaves the old learning record historical. A reusable invariant that remains valid on a successor must be re-supported/rebound or cited as historical context rather than silently treated as exact-current truth.

## 13. ADS evolution feedback architecture

Task Learning / incident / Review / Validation findings may classify observations as:

```text
PROJECT_DEFECT
AGENT_EXECUTION_DEFECT
ENVIRONMENT_OR_TOOL_DEFECT
PROJECT_SPECIFIC_REQUIREMENT
STANDARD_FRICTION_CANDIDATE
ADS_EVOLUTION_CANDIDATE
```

No new evolution lifecycle schema is required by default.

Promotion is an ordinary durable GitHub/ADS Intake action carrying evidence refs. A candidate becomes Product/Architecture authority only through the normal ADS process.

Recommended promotion evidence includes:

```text
affected standard owner/version
materiality/risk
reproduction or strong falsifying counterexample
independent evidence where feasible
project/task diversity
measured failures/rework/friction
privacy/publication classification
counterevidence / NO_CHANGE / MORE_EVIDENCE disposition
```

A single successful/failed model run, provider label, telemetry threshold, or project-specific preference cannot self-promote into a standard change.

## 14. Privacy / security / evidence minimization

Machine records MUST exclude ordinary secret values and private chain-of-thought.

Cross-project capability/learning evidence records SHOULD prefer:

```text
stable refs/digests
bounded task/capability classes
approved summaries
measured fields only when actually observed
project-private vs publishable classification
```

Hidden Validation details/evaluator secrets are referenced only through allowed evidence surfaces and never copied into learning/capability records.

Authenticated transport identity remains distinct from logical operator/session identity and from independence eligibility.

## 15. Compatibility / progressive adoption

v4.8 is additive:

- existing Task Packs/Execution Packs/Dispatch/events remain valid;
- new schema refs are optional unless a v4.8 Task/profile requires them;
- Level-0/manual execution can use one designated admission writer and manual capability/availability facts;
- centralized scheduler/orchestrator is not required;
- GitHub remains the reference durable fact chain;
- no historical evidence is rewritten;
- Fast Path can use direct eligibility + ordinary Dispatch/Claim + `TASK_LEARNING=NONE_MATERIAL`.

Projects may stop at any progressive-adoption level while preserving the same authority/currentness/serialization semantics.

## 16. Architecture UNKNOWNs and disposition

| ID | UNKNOWN | Impact | Disposition | Decision |
|---|---|---|---|---|
| U1 | Does generic Agent capability duplicate v4.6 Skill Metadata? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Skill describes reusable procedure metadata; Agent Capability Profile describes executor claims; Capability Evidence records observed executor/task-class evidence. |
| U2 | Is a durable universal Availability schema required? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Normalize current owner facts into a derived Availability View with currentness/TTL; no fifth default schema. |
| U3 | Does resource scheduling require a second reservation authority? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Extend existing atomic dispatch/claim admission with resource/capacity protected keys. |
| U4 | Can optional ranking weaken independence/currentness/security? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Ranking receives only hard-filtered ELIGIBLE choices. |
| U5 | Does transport-neutral exchange require a universal lifecycle/result object? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Envelope carries/refers to existing semantic owners; delivery state remains transport-only. |
| U6 | Must GitHub `ai-dev:event:v2` be replaced? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. It remains the GitHub adapter/writer protocol; envelope is additive and historical events remain readable. |
| U7 | Does Task Learning need a new standalone normative owner? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Execution Architecture owns learning evidence semantics; existing ADR/incident/Product owners remain distinct. |
| U8 | Does ADS evolution need an automated promotion state machine? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Classification feeds ordinary GitHub/ADS Intake and governance. |
| U9 | Is a pre-L2 real multi-Agent/queue/transport demo required? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Architecture changes are additive around already-frozen READY/Dispatch/Claim/serialization semantics; real heterogeneous/resource/transport claims are mandatory later dogfood/Validation. |
| U10 | Does #469 justify default lower-cost routing or economic optimization? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Economic savings remain NOT_MEASURED; evidence supports bounded task-class feasibility + continued strong review value only. |

### Research Demo decision

**No executable Research Demo is required before L2 Freeze on the current evidence.**

Reason: all critical owner/authority/concurrency decisions reduce to existing frozen durable-state/atomic-admission semantics plus additive metadata/binding contracts. The Product intentionally does not mandate a specific external queue, A2A runtime, scheduler service, provider, host or economic optimizer whose behavior must be proven before choosing the architecture.

This does **not** waive later executable evidence. Multi-Agent/resource contention/transport replay/restart and real external-runtime claims remain required dogfood/Validation concerns. If Architecture Review finds an assumption that changes public wire/atomicity/durability semantics and cannot be resolved statically, reopen the relevant UNKNOWN as `EXECUTABLE_DEMO_REQUIRED` before L2 Freeze.

## 17. Conformance / negative-oracle architecture

At minimum reject these inference families:

```text
Capability Profile claim -> proven capability                 reject
Skill installed -> executor capability proven                 reject
Capability Evidence PASS -> current Task Validation PASS      reject
historical capability success -> current resource AVAILABLE   reject
provider/model label -> authorization                         reject
credential/tool available -> side-effect authority            reject
stale Availability fact -> hard eligibility satisfied         reject
cost/latency ranking -> ineligible Agent becomes eligible     reject
reviewer independence conflict -> rank around the conflict     reject
same exclusive resource -> two admitted incompatible uses      reject
no serialization primitive -> shared concurrent claiming       reject
transport delivered/ACK -> Task/Review/Validation completion   reject
exchange retry -> bypass Dispatch/Claim admission               reject
same exchange id + conflicting payload -> accept latest         reject
transient queue state -> durable authority                      reject
Task Learning rationale -> Product/Architecture authority       reject
Task Learning old exact subject -> successor behavioral truth   reject
STANDARD_FRICTION_CANDIDATE -> STANDARD_CHANGE                  reject
#469 bounded successes -> blanket strong-to-low-cost rule       reject
NOT_MEASURED economic fields -> savings claim                   reject
Fast Path -> authority/currentness/gate waiver                  reject
```

Positive conformance/dogfood must cover:

- multiple simultaneously READY tasks;
- at least two heterogeneous capability profiles;
- stale and fresh Availability facts;
- scarce/exclusive shared resource with competing assignments;
- incompatible reviewer/validator independence candidate;
- capability evidence that helps selection without becoming authority;
- optional ranking after hard filtering;
- duplicate/replayed/lost exchange delivery;
- crash/restart reconstruction from durable facts;
- lower-cost bounded task success plus required strong review;
- escalation from bounded executor on semantic ambiguity;
- Task Learning `NONE_MATERIAL` and material-learning paths;
- friction classification with both `MORE_EVIDENCE` and candidate-promotion paths.

## 18. Expected implementation touchpoints

L2 expects later Task DAG decomposition to cover, at minimum:

1. shared schemas for Task Learning / Capability Profile / Capability Evidence;
2. Execution Architecture eligibility + resource-admission semantics and optional Task/Dispatch refs;
3. Agent Exchange Binding owner + envelope schema + GitHub adapter mapping;
4. Task Learning closeout/profile integration;
5. ADS evolution/friction classification + Intake/template integration;
6. manifest/v4.7 registry/discoverability/adoption wiring;
7. deterministic eligibility/serialization/exchange conformance;
8. heterogeneous multi-Agent/resource/transport dogfood;
9. #469/cross-project evidence dogfood and measured-field discipline;
10. integrated currentness/backward-compatibility/closure inputs.

Exact Task IDs, dependencies, write sets and Review Policies are **not frozen here**; they belong to the Task DAG after L2 Freeze.

## 19. Local environment posture

`LOCAL_ENV=NOT_REQUIRED` for L2 planning/review/freeze.

Real host/device/provider/transport behavior must not be claimed from static fixtures. Later dogfood must create exact-subject Validation handoffs for any external runtime/resource that Web/CI cannot execute.

## 20. L2 Freeze gate

This L2 is **NOT FROZEN**.

Before L2 Freeze:

1. a genuinely fresh high-capability Architecture Reviewer must review this exact L2 candidate against Frozen Product Authority and current v4.1–v4.7 owners;
2. P0/P1 Architecture findings must be resolved;
3. reviewer must specifically falsify owner duplication, capability-vs-authority leakage, scarce-resource race semantics, exchange-vs-event duplication, backward compatibility and Research Demo disposition;
4. any newly discovered material Architecture UNKNOWN must receive `STATIC_EVIDENCE_SUFFICIENT | EXECUTABLE_DEMO_REQUIRED | BLOCKED | ARCHITECTURE_CONTRADICTION` disposition;
5. only after a current exact-subject PASS may Controller record L2 Freeze and create the Task DAG.

Task DAG remains **NOT AUTHORIZED** until that Freeze.
