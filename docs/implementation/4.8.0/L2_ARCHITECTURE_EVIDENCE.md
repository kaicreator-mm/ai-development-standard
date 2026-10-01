# v4.8.0 L2 Architecture Evidence — Evidence-Driven Agent Orchestration & Standard Evolution

Status: **L2 REPAIRED CANDIDATE — NOT FROZEN; FRESH INDEPENDENT ARCHITECTURE RE-REVIEW REQUIRED**

Frozen Product authority:

- `docs/implementation/4.8.0/PRODUCT_FREEZE.md`;
- Frozen PRD blob `f26439580e00de6ed8b2e27d732a3095eb566219`;
- Fresh Independent Product Review R3 #490 terminal `5926142930`;
- Product dogfood basis `#469@5925124956`.

Architecture review history:

- #494 terminal `5926563715` = `CHANGES_REQUESTED`;
- P0=0 / P1=3 / P2=0 / P3=0;
- Product Freeze validity PASS;
- Research Demo disposition PASS / no pre-Freeze executable demo required;
- the three P1 repairs are incorporated below.

Architecture baseline: current v4.1–v4.7 owners on `main@e75fe834469c5ea9f9a384f7d84e38c3a48afa46` plus the Product Freeze checkpoint on `planning/v4.8-evidence-orchestration`.

## 1. Architecture decision

v4.8 extends the existing execution architecture with **compact Task Learning, logical-Agent capability evidence, constraint-first eligibility/resource admission, reuse of the existing transport-neutral Interchange contract, and evidence-driven ADS evolution feedback**.

It does **not** create another Product/Task/Dispatch/Review/Validation lifecycle, another Agent-message authority, another Runner Capability owner, or a second scheduler state machine.

```text
Frozen Task / Task Pack authority
        │
        ├── optional execution requirements
        ▼
canonical READY set
        │
        ├── Logical Agent Capability Profile
        ├── existing Runner/Host Capability owner facts
        ├── current derived Availability View
        ├── exact-subject Capability Evidence
        └── authority/currentness/independence/security constraints
        │
        ▼
Derived Eligibility Resolver
        │
        ├── hard filter: ELIGIBLE / INELIGIBLE / UNKNOWN
        └── optional ranking among ELIGIBLE choices only
        │
        ▼
COMPOSITE atomic admission
(work claim + every required scarce-resource/capacity binding)
        │
        ▼
existing Dispatch reservation + Claim admission
        │
        ├── existing Interchange Envelope v1 / compatible extension
        └── GitHub ai-dev:event:v2 reference writer profile
        │
        ▼
existing Builder / Reviewer / Validator execution
        │
        ▼
existing durable Result / Review / Validation / Merge facts
        │
        ├── Task Learning Evidence v1
        └── friction classification -> ordinary ADS Intake
```

GitHub/repository/evidence stores remain durable facts. Eligibility, ranking, queue and availability views remain derived. Runtime caches, schedulers, queues and transports are disposable.

## 2. Architecture invariants

1. Task requirements remain Task authority; lower artifacts may narrow but never weaken them.
2. Logical Agent capability, Runner/Host capability, current Availability and Capability Evidence are separate dimensions.
3. Capability never implies authorization, side-effect permission, Review PASS or Validation PASS.
4. `CI_RUNNER_CAPABILITY_STANDARD.md` remains canonical for mutable CI/Build Host platform/toolchain/resource/concurrency capability profiles.
5. v4.6 Skill Metadata remains reusable procedure metadata, not executor capability proof.
6. Capability Evidence is historical/exact-subject evidence and never substitutes for current Validation/Review.
7. Missing/stale material Availability is `UNKNOWN`; UNKNOWN fails closed for hard requirements.
8. Hard eligibility precedes optimization; ranking cannot make an ineligible or unknown choice eligible.
9. READY / Dispatch / Claim and existing admission authority remain canonical.
10. Work admission and all required scarce-resource/capacity reservations share one all-or-none linearization point.
11. Independent per-key successful writes are insufficient for composite admission.
12. Capacity-N active accepted bindings MUST never exceed N; exclusive resource is N=1.
13. Partial canonical states such as `work claimed / resource not held` or `resource held / work not admitted` are forbidden.
14. Accepted work/resource binding facts remain durably reconstructible; transient locks/leases are coordination only.
15. Existing `interchange-envelope-v1` and v4.0 `AGENT_INTERCHANGE.md` remain the transport-neutral correlation owner/family.
16. `ai-dev:event:v2` remains the GitHub writer/admission protocol; v4.8 does not create a competing Agent Exchange owner.
17. Transport ACK/delivery/progress is never workflow/gate truth.
18. Task Learning is evidence/history, not Product/Architecture/Task/ADR/incident authority.
19. No private chain-of-thought, credentials or hidden-evaluator payload is required or retained.
20. Standard-friction observations cannot self-amend ADS; promotion re-enters normal governance.
21. v4.8 remains additive/non-weakening; incompatible rewrites route to future-major.

## 3. Owner map

| Concern | Canonical owner after v4.8 | v4.8 role | Must not duplicate |
|---|---|---|---|
| Product / Architecture / Task scope | existing Product/L2/Task owners | consume only | all lower evidence/routing |
| Task execution requirements | Task Pack; exact-base narrowing in Execution Pack | optional requirement refs/fields | Product/L2 authority |
| Task Learning evidence semantics | `EXECUTION_ARCHITECTURE_STANDARD.md` | new evidence family + closeout semantics | Task Pack, ADR, incident, Review/Validation result |
| logical-Agent capability claim/evidence | `EXECUTION_ARCHITECTURE_STANDARD.md` | new Agent Profile + Capability Evidence families | Runner Capability, Skill Metadata, Validation |
| CI / Build Host capability inventory | `CI_RUNNER_CAPABILITY_STANDARD.md` | referenced/composed, not copied | Agent Profile |
| device / provider / project resource capability | applicable existing owner | referenced/composed | generic Agent Profile |
| reusable procedure / Skill | v4.6 Skill owner | referenced by Agent Profile | Agent capability proof |
| current Availability | derived normalization over applicable owners | no durable authority | capability history/profile |
| READY / dispatch / claim / admission | `EXECUTION_ARCHITECTURE_STANDARD.md` | eligibility + composite resource admission | second scheduler lifecycle |
| GitHub event writing / logical operator attribution | `GITHUB_AGENT_INTERACTION_PROTOCOL.md` | reference GitHub profile | Interchange semantics |
| transport-neutral correlation/interchange | existing v4.0 `AGENT_INTERCHANGE.md` + `schemas/interchange-envelope-v1.schema.json` | compatible extension/profile only | new Exchange owner/family |
| ADS evolution governance | normal Development Workflow / Intake / L1 / PRD / L2 | explicit classification/promotion route | self-amending telemetry lifecycle |
| authority discovery | v4.7 manifest/registry | register new refs | owner rules |

## 4. Default machine-contract families

v4.8 introduces exactly **three new default machine-contract families**.

### 4.1 Task Learning Evidence v1

Candidate file: `schemas/task-learning-v1.schema.json`.

Purpose: preserve compact reusable implementation learning bound to work identity, exact subject where material, and existing evidence.

Conceptual fields:

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

- summaries are externally useful engineering rationale, not private chain-of-thought;
- refs/digests are preferred over copied evidence bodies;
- exact-code claims bind to the subject actually evidenced;
- later drift does not inherit stale claims;
- Fast Path may record `TASK_LEARNING=NONE_MATERIAL` without instantiating an empty record.

### 4.2 Logical Agent Capability Profile v1

Candidate file: `schemas/agent-capability-profile-v1.schema.json`.

Purpose: describe **logical Agent/operator/model execution claims** without duplicating infrastructure inventory or implying proof/authority.

Conceptual fields:

```text
schema_version
profile_id
profile_version
logical_agent_or_runtime_class_ref
provider_model_provenance?
eligible_role_claims[]
reasoning_or_semantic_capability_claims[]
language_archetype_claims[]
logical_tool_use_class_claims[]
max_agent_freedom_claim?
skill_refs[]
security_or_side_effect_class_claims[]
environment_or_runner_requirement_refs[]
compatibility_refs[]
```

Explicitly excluded from this generic profile when already owned elsewhere:

```text
host OS / architecture
installed runtime/toolchain inventory
device inventory
runner CPU/memory/disk
runner/provider concurrency limits
network reachability observations
current resource capacity
```

Those facts remain in `CI_RUNNER_CAPABILITY_STANDARD.md` or the applicable host/device/resource owner and are referenced during eligibility composition.

Profile content is a claim, not proof. Provider/model identity is provenance, not a universal score. Skill presence is procedure availability, not demonstrated executor ability. Tool/credential possession does not grant side-effect authority.

### 4.3 Agent Capability Evidence v1

Candidate file: `schemas/agent-capability-evidence-v1.schema.json`.

Purpose: record bounded observed evidence about a logical Agent/task capability without converting historical success into current PASS.

Conceptual fields:

```text
schema_version
evidence_id
agent_profile_ref?
logical_operator_or_executor_ref
provider_model_provenance?
task_class_or_capability_class
role
exact_subject_ref
environment_ref?
runner_or_resource_capability_ref?
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

Positive and negative evidence are both valid. Environment/runner facts are referenced, not copied as generic Agent profile ownership. No global scalar quality score is created. Economic/performance conclusions require comparable methodology.

## 5. Existing Interchange family — reused, not replaced

v4.8 creates **no new Agent Exchange Envelope family and no new `AGENT_EXCHANGE_BINDING_STANDARD.md`**.

Existing authority already provides:

- `docs/implementation/4.0.0/AGENT_INTERCHANGE.md` — transport-neutral correlation, subject identity, actor/causation, stale/duplicate/superseded/conflict, idempotency, durable-owner boundaries and mapping to GitHub events;
- `schemas/interchange-envelope-v1.schema.json` — active machine contract;
- `GITHUB_AGENT_INTERACTION_PROTOCOL.md` / `ai-dev:event:v2` — GitHub writer/admission semantics.

v4.8 may require an **additive compatible extension/profile** of Interchange v1 only where Frozen Product semantics are not already expressible, for example bounded receiver capability target, expiry/currentness metadata, or payload digest/idempotency hardening. Implementation must first prove the field is absent/needed. A compatible optional field addition or an explicitly versioned successor of the same canonical family is allowed; a parallel envelope family is not.

Hard rules remain:

```text
Interchange correlation != semantic authority
transport ACK != completion
exchange identity != permission
same idempotency identity + same payload -> safe replay
same identity + conflicting payload/digest -> fail closed
stale exchange -> historical only
critical result -> canonical durable owner materialization
```

A `REVIEW_RESULT` remains owned by Review, a `VALIDATION_RESULT` by Validation, Dispatch by Dispatch, and controller decisions by their existing owners.

## 6. Availability / Resource Facts — derived normalization

v4.8 introduces no universal durable Availability schema.

Availability is a `NON_AUTHORITATIVE_DERIVED_STATE` over current facts from the applicable owner:

```text
resource_ref
source_owner_ref
state = AVAILABLE | UNAVAILABLE | UNKNOWN
capability_ref(s)
current_capacity / exclusive_group when owner exposes it
observed_at
expires_at/currentness rule
source_fact_ref
```

Runner/host capability may be current enough for routing but still remains distinct from current run preflight and Validation PASS.

Rules:

- stale/missing material fact -> UNKNOWN;
- UNKNOWN cannot satisfy a hard resource/environment requirement;
- Agent Profile cannot prove host reachability;
- Availability cannot prove logical-Agent quality;
- actual run facts supersede stale inventory for that execution.

## 7. Task execution requirements and eligibility composition

Task Pack remains the owner of execution requirements. Optional additive fields/refs may express:

```text
execution_requirements:
  required_agent_capability_classes[]
  required_environment_or_runner_capability_refs[]
  required_resource_classes[]
  independence_constraints[]
  security_or_side_effect_constraints[]
  max_agent_freedom
  concurrency_or_resource_group_refs[]
  capability_evidence_policy?
  optimization_hints?
```

Eligibility for each READY `(work item, role)` composes:

```text
Frozen/current Task requirements
+ current authority/currentness
+ Logical Agent Capability Profile
+ existing Runner/Host/Device capability facts
+ current Availability View
+ relevant Capability Evidence
+ independence/security/write-set constraints
        ↓
hard predicates
        ↓
ELIGIBLE | INELIGIBLE | UNKNOWN
```

`ELIGIBLE | INELIGIBLE | UNKNOWN` is derived, not durable authority.

Capability Evidence is advisory by default. A project/Task may explicitly require a demonstrated evidence class; absence of historical success is not a universal ban on new Agents.

## 8. Hard eligibility before optional ranking

Hard predicates include, where applicable:

```text
work item still READY/claimable
Task Pack / Execution Pack current
role allowed
agent freedom sufficient but not self-elevated
logical Agent capability claim satisfies Task need
required runner/host/device capability facts satisfy Task need
required current resource AVAILABLE
security/side-effect authority present from canonical owner
reviewer/validator independence satisfied
write-set/concurrency compatibility satisfied
subject/base current
required capability-evidence policy satisfied
composite scarce-resource admission can succeed atomically
```

Only ELIGIBLE candidates enter optional ranking.

Projects MAY rank by priority, critical path, queue age, cost class, latency class, utilization, scarcity, retry/escalation history, drift risk and relevant evidence strength. Ranking cannot change INELIGIBLE/UNKNOWN to ELIGIBLE. No universal Agent score or economic optimizer is introduced.

## 9. Composite work + scarce-resource admission

v4.8 reuses and tightens `EXECUTION_ARCHITECTURE_STANDARD.md` §11.1 rather than creating a second reservation authority.

For any dispatch needing scarce/exclusive/bounded resources, the protected admission set is:

```text
A = {
  work_claim_key(repository, work_item, role),
  resource_group_1 + required_units,
  resource_group_2 + required_units,
  ...
}
```

**All members of A MUST be admitted through one all-or-none linearization point.**

Conforming modes:

### Mode A — SINGLE_WRITER_ADMISSION

One designated logical admission writer owns one critical section covering:

1. current work claimability;
2. incompatible active dispatch check;
3. every required resource/capacity availability check;
4. capacity counters/tokens;
5. dispatch reservation;
6. accepted work/resource binding publication decision.

No competing writer may independently reserve any member of the same admission set.

### Mode B — LINEARIZABLE_COMPOSITE_CONDITIONAL_WRITE

The adapter/storage layer provides a genuine atomic transaction/CAS over the **entire admission set**, using expected revision/generation (or equivalent). A stale or partially unsatisfied predicate fails the whole mutation. Independent per-key CAS operations are not equivalent.

### Capacity invariant

For each capacity group G with configured capacity N:

```text
sum(active accepted units bound to G) <= N
```

at every canonical state transition.

Exclusive resource = `N=1`.

A task requiring `k` units must fail admission if the post-admission active total would exceed N.

### No partial canonical state

These are forbidden as accepted states:

```text
work claimed + required resource not durably bound
resource durably bound + work/dispatch not admitted
subset of required resources admitted while others failed
```

If an implementation internally acquires multiple transient locks, it must not publish a canonical accepted admission until the full set succeeds atomically.

### Crash / ambiguity recovery

Accepted binding facts record, where applicable:

```text
dispatch/work claim ref
resource group + units/slot
generation/revision
admission mode
accepted-at / durable event ref
release/supersession ref
```

If a crash makes publication outcome ambiguous, the controller fails closed, reconstructs durable work/resource facts, reconciles capacity and **does not issue a replacement incompatible admission** until ambiguity is resolved.

If no composite atomic mechanism is available, shared concurrent admission is non-conformant. Route through one exclusive `SINGLE_WRITER_ADMISSION` path or mark the assignment `BLOCKED/UNAVAILABLE`; do not expose the same capacity concurrently to independent claimers.

This architecture is statically decidable and does not mandate distributed transactions. A later implementation choosing a novel distributed multi-key CAS/lease mechanism must separately prove that mechanism with a narrow Research Demo/Validation before relying on it.

## 10. Dispatch extensions

`schemas/dispatch.schema.json` may receive backward-compatible optional refs such as:

```text
agent_capability_profile_ref?
capability_evidence_refs[]?
runner_or_environment_capability_refs[]?
eligibility_basis_ref?
resource_binding_refs[]?
assignment_policy_ref?
```

These fields explain selection/binding; they do not grant Task scope, Review/Validation authority or side-effect permission. Historical Dispatch payloads remain valid.

## 11. Task Learning lifecycle

```text
implementation / tests / Validation / Review / merge facts
        ↓
material-learning check
        ├── none -> TASK_LEARNING=NONE_MATERIAL
        └── material -> Task Learning Evidence v1
                         ↓
                   reviewable history/evidence
                         ↓
                   optional friction classification
```

A Task Learning record may reference ADR/incident/Product work but never replaces those owners. Successor code does not silently inherit exact-subject learning claims.

## 12. ADS evolution feedback

Classify execution observations before standard promotion:

```text
PROJECT_DEFECT
AGENT_EXECUTION_DEFECT
ENVIRONMENT_OR_TOOL_DEFECT
PROJECT_SPECIFIC_REQUIREMENT
STANDARD_FRICTION_CANDIDATE
ADS_EVOLUTION_CANDIDATE
```

No new evolution lifecycle schema is required by default. Promotion is an ordinary durable ADS Intake action with evidence refs and proceeds through normal L1 -> PRD -> L2 -> Task -> Review/Validation governance.

Recommended evidence includes affected owner/version, materiality/risk, reproduction/counterexample, independent evidence where feasible, project/task diversity, measured rework/friction, publication/privacy classification and counterevidence/NO_CHANGE/MORE_EVIDENCE disposition.

Telemetry, provider label, one success/failure or heuristic threshold cannot self-amend ADS.

## 13. Privacy / security / evidence minimization

- no credentials/secrets/private chain-of-thought;
- no hidden-validation/evaluator leakage;
- refs/digests over copied sensitive bodies;
- explicit project-private vs publishable evidence classification;
- logical operator identity distinct from transport account/session;
- capability/tool/credential availability never becomes side-effect authority;
- measured performance/resource data only when actually observed.

## 14. Compatibility / progressive adoption

v4.8 remains additive:

- historical Task Packs, Execution Packs, Dispatches, `interchange-envelope-v1`, `ai-dev:event:v2` and Validation/Review payloads remain valid;
- new refs are optional unless v4.8 Task/project authority requires them;
- no new Interchange family is required;
- no universal Availability schema is required;
- Level-0/manual projects may use one designated composite admission writer;
- centralized scheduler/orchestrator is not required;
- Fast Path can use one directly eligible executor + ordinary Dispatch/Claim + `TASK_LEARNING=NONE_MATERIAL`.

## 15. Architecture UNKNOWNs and disposition

| ID | UNKNOWN | Impact | Disposition | Repaired decision |
|---|---|---|---|---|
| U1 | Does generic Agent capability duplicate v4.6 Skill Metadata? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Skill = reusable procedure; logical Agent Profile = execution claim; Capability Evidence = observed execution evidence. |
| U2 | Is durable universal Availability required? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Derived currentness view over existing owners. |
| U3 | Does scarce-resource scheduling require a second reservation authority / can separate keys race? | Critical | `STATIC_EVIDENCE_SUFFICIENT` after #494 repair | No second authority. Require one all-or-none composite linearization point across work + all resources; per-key independent CAS is forbidden. |
| U4 | Can ranking weaken independence/currentness/security? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Ranking sees ELIGIBLE only. |
| U5 | Does transport-neutral exchange require a new owner/family? | Critical | `STATIC_EVIDENCE_SUFFICIENT` after #494 repair | No. Reuse existing v4.0 Interchange owner and `interchange-envelope-v1`; compatible extension/profile only. |
| U6 | Must `ai-dev:event:v2` be replaced? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. It remains GitHub writer/admission profile. |
| U7 | Does Task Learning need a standalone owner? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Execution Architecture owns evidence semantics. |
| U8 | Does ADS evolution need automated promotion lifecycle? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Ordinary ADS Intake/governance. |
| U9 | Is a pre-L2 distributed resource/queue demo required? | High | `STATIC_EVIDENCE_SUFFICIENT` | No, because architecture permits single-writer composite admission and does not depend on unproven distributed multi-key mechanisms. A later novel mechanism requires its own narrow demo. |
| U10 | Does #469 justify default low-cost routing/economic optimization? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Savings remain NOT_MEASURED; blanket routing unsupported. |

### Research Demo decision

**No executable Research Demo is required before L2 Freeze for this repaired architecture.**

#494 explicitly found the P1 repairs statically decidable. This decision depends on not requiring an unproven distributed multi-key admission mechanism. Real heterogeneous Agent/resource contention, transport replay/restart and external-runtime behavior remain later dogfood/Validation obligations.

## 16. Conformance / negative oracles

At minimum reject:

```text
Agent Profile claim -> proven capability
Runner Capability Profile -> Validation PASS
Skill installed -> Agent capability proven
Capability Evidence success -> current Validation/Review PASS
historical capability success -> current Availability
provider/model label -> authorization
credential/tool available -> side-effect authority
stale Availability -> eligible
cost/latency ranking -> ineligible becomes eligible
reviewer independence conflict -> rank around it
capacity N -> N+1 active accepted bindings
per-key CAS success -> composite admission proven
work claimed -> resource reservation inferred
resource reserved -> work claim inferred
ambiguous crash -> immediate replacement admission
transport ACK -> Task/Review/Validation completion
new Exchange family -> bypass existing Interchange owner
exchange retry -> bypass Dispatch/Claim
same idempotency identity + conflicting payload -> accept latest
transient queue state -> durable authority
Task Learning rationale -> Product/Architecture authority
old exact-subject learning -> successor truth
STANDARD_FRICTION_CANDIDATE -> STANDARD_CHANGE
#469 bounded successes -> blanket strong-to-low-cost rule
NOT_MEASURED -> savings claim
Fast Path -> gate/authority waiver
```

Positive later dogfood must cover multiple READY tasks, heterogeneous logical Agent profiles, existing Runner/Host capability refs, stale/fresh Availability, capacity N and exclusive-resource races, independence conflicts, optional ranking after hard filters, Interchange duplicate/replay/loss/recovery, crash reconstruction, bounded low-cost execution with required strong review, escalation on ambiguity, Task Learning material/NONE_MATERIAL paths, and `MORE_EVIDENCE` evolution routing.

## 17. Expected implementation touchpoints

After L2 Freeze, Task DAG should decompose at least:

1. Task Learning schema/profile;
2. Logical Agent Capability Profile schema;
3. Agent Capability Evidence schema;
4. Task/Dispatch optional requirement/reference extensions;
5. Execution Architecture eligibility + composite resource-admission semantics;
6. existing Interchange v1 compatibility extension/profile only if implementation gap is proven;
7. Task Learning closeout + ADS friction/Intake integration;
8. v4.7 manifest/registry/discoverability wiring;
9. deterministic conformance for owner composition, eligibility and composite admission;
10. heterogeneous multi-Agent/resource/interchange dogfood;
11. #469/cross-project evidence dogfood and measured-field discipline;
12. integrated compatibility/closure inputs.

Exact Task IDs/dependencies/write sets/Review Policies are not frozen here; they belong to the Task DAG after L2 Freeze.

## 18. Local environment posture

`LOCAL_ENV=NOT_REQUIRED` for L2 planning/review/freeze.

Real host/device/provider/transport behavior must not be claimed from static evidence. Later tasks create exact-subject Validation handoffs where required.

## 19. L2 Freeze gate

This repaired L2 is **NOT FROZEN**.

Before L2 Freeze:

1. a genuinely fresh high-capability Architecture Reviewer must review the exact repaired L2 candidate;
2. it must explicitly verify closure of #494 P1-1/P1-2/P1-3;
3. P0/P1 must be zero;
4. Product Freeze validity, owner non-duplication, three-family count, composite resource atomicity, existing Interchange reuse, Runner-vs-Agent capability boundary, backward compatibility and Research Demo disposition must PASS;
5. any newly discovered material UNKNOWN must receive an explicit disposition;
6. only then may Controller record L2 Freeze and create the Task DAG.

Task DAG remains **NOT AUTHORIZED** until L2 Freeze.
