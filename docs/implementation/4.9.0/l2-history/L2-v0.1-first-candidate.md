# v4.9.0 L2 Architecture Evidence — Adaptive Proportional Development Orchestration

Status: **L2 FIRST CANDIDATE — NOT FROZEN; FRESH INDEPENDENT ARCHITECTURE REVIEW REQUIRED**

Frozen Product authority:

- `docs/implementation/4.9.0/PRODUCT_FREEZE.md`;
- Frozen PRD v0.4 blob `a8ec7030a14337a4c2dca853dc474e965679d610`;
- Fresh complete-delta Product Review #707 comment `5966886681` = PASS, `P0=P1=P2=P3=0`;
- Product Freeze Controller #709;
- Product Freeze checkpoint `089555c7911d9fde1ec0bd708c7c77b584d7c305`.

Reused v4.8 predecessor authority:

```text
V48_FROZEN_PRD_BLOB=f26439580e00de6ed8b2e27d732a3095eb566219
V48_FROZEN_L2_BLOB=f88c85454e80101a0fdf56050e21f11a05279841
```

Architecture source baseline: current standards on `main@73098dfb576dbcc1252634e14bb3d39b70b94342`, plus the exact frozen v4.8 Product/L2 authorities above and the v4.9 Product Freeze checkpoint.

This document is Architecture Evidence only. It does not authorize Task DAG materialization or implementation until L2 Freeze.

## 1. Architecture decision

v4.9 adds a **deterministic proportional-assurance resolution layer** in front of the existing execution architecture, then extends the existing reducer/dispatch/role/evidence/release semantics to consume that resolution.

It does **not** create a second Product/Architecture/Task/Dispatch/Claim/Review/Validation/Release/Task-Learning lifecycle.

```text
current/pinned authority owners
        +
current durable facts / proof refs
        ↓
Proportional Assurance Resolver
        │
        ├── owner-scoped reduction proof
        ├── monotonic obligation composition
        ├── release applicability decision ref
        ├── evidence-currentness/transfer refs
        └── independence / role requirements
        ↓
Assurance Resolution v1  (durable decision evidence; NOT authority)
        ↓
existing Execution Architecture reducer/controller
        │
        ├── READY / dependency / lineage facts
        ├── JIT phase/container materialization
        ├── v4.8 hard eligibility/resource selection
        ├── Role Execution Profile v1
        └── existing Dispatch → Claim admission
        ↓
Builder / Reviewer / Validator / Controller / specialized role
        ↓
existing gate-owned terminals and findings
        ↓
reducer consumes all adverse/current evidence
        ↓
merge / version closure / release path owned by existing authorities
        ↓
v4.8 Task Learning Evidence + bounded v4.9 friction/recurrence extension
```

GitHub/repository/evidence stores remain durable facts. Assurance resolution, ready sets, queues, wait projections, ranking and runtime caches remain reconstructible derived/decision state. A scheduler daemon remains optional.

## 2. Architecture invariants

1. Gate owners continue to own their requirements; v4.9 composition never becomes a super-authority.
2. An owner-scoped reduction is legal only from positive owner permission whose predicates are proven by current durable facts or an owner-accepted deterministic check.
3. Model output may propose a classification but can never be the sole proof that lowers assurance.
4. Unknown, stale, contradictory or ambiguous reduction predicates fail closed to the owner's unreduced requirement or `BLOCKED` when no stronger legal path is resolvable.
5. `ASSURANCE_FLOOR` is not a scalar score. It is a normalized conjunction of owner-attributed obligation atoms.
6. Cross-owner composition is monotonic: one owner may reduce only atoms it owns; it cannot delete another owner's atoms.
7. Incomparable/conflicting obligations with no owner-defined resolution produce `BLOCKED`, not heuristic choice.
8. `Assurance Resolution v1` records the decision basis; it does not create Product, Task, Review, Validation or Release authority.
9. Existing GitHub Task Issues + Issue Dependencies remain the canonical live execution DAG after Task materialization.
10. The Frozen Task DAG/current Task authority remains the semantic work envelope; runtime orchestration materializes phases only inside it.
11. v4.8 capability/eligibility/resource selection and Dispatch/Claim ownership remain canonical; v4.9 creates no parallel scheduler ownership or claim lock.
12. Role contract and executor capability are separate: Role Execution Profile defines authority/behavior; v4.8 Agent Capability Profile/evidence helps decide executor eligibility.
13. PASS does not erase unresolved adverse findings. Finding union/blocker dominance survives additional reviewers/validators.
14. A new Review after an adverse terminal requires an authorized successor subject or owning-authority disposition; reviewer-shopping is non-conformant.
15. Evidence binding/currentness/transfer remains owned by each Gate Authority. Generic orchestration consumes a positive gate rule; absence of one means historical-only/fresh execution.
16. Release applicability remains owned by `RELEASE_STANDARD.md`; v4.9 only adds prospective owner-defined applicability semantics allowed by Frozen Product.
17. Candidate migration is prospective and cannot remove already-required gates from an in-flight authority-bound candidate.
18. v4.9 P4 extends v4.8 Task Learning / `ADS_EVOLUTION_CANDIDATE`; no parallel learning/evolution family or intake path is created.
19. Manual/GitHub-native execution remains conformant through deterministic documents/events/controllers; no proprietary transport or daemon is mandatory.
20. Private chain-of-thought, secrets and Hidden oracle payloads are never required by the new records.

## 3. Canonical owner map

| Concern | Canonical owner after v4.9 | v4.9 change | Must not duplicate |
|---|---|---|---|
| Product scope / acceptance / non-goals | Frozen PRD / Product Freeze | consume only | lower architecture/runtime decisions |
| Architecture/Task scope | Frozen L2 / Task DAG / Task Pack | consume; enforce semantic envelope | runtime JIT scope invention |
| proportional assurance composition | **new `PROPORTIONAL_ASSURANCE_STANDARD.md`** | owns owner discovery/composition algorithm, proof semantics, Assurance Resolution evidence | Review/Validation/Release requirement ownership |
| workflow/reducer/JIT/dispatch/claim | `EXECUTION_ARCHITECTURE_STANDARD.md` | consume assurance resolution; wait/JIT/adverse-terminal rules; role execution profile semantics | second scheduler/task/claim lifecycle |
| executable work-item metadata/state | `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` | optional refs to resolution/profile; no new live state authority | gate PASS/FAIL truth |
| Task/Execution Pack authority | `EXECUTION_PACK_STANDARD.md` | optional assurance/role refs; preserve exact-base/JIT semantics | Product/L2/Task redefinition |
| Agent capability/eligibility/resource scheduling | frozen v4.8 Execution Architecture + capability families | reuse only | Role Profile authority |
| Agent role behavior | `EXECUTION_ARCHITECTURE_STANDARD.md` + **Role Execution Profile v1** | new provider-neutral behavior/authority profile | Agent Capability Profile |
| Validation truth/currentness | `VALIDATION_STANDARD.md` | expose/consume gate-owned binding and transfer rules; existing impact decision remains | generic PASS transfer |
| Review policy/verdict/finding semantics | current Workflow/Work Item/Review evidence owners | add complete currentness/finding consumption requirements; default fresh-only across material subject drift | orchestration-created review authority |
| Release applicability/candidate/release | `RELEASE_STANDARD.md` | prospective applicability states/predicates + no-retroactive-shortening | Orchestrator/L2 invented release policy |
| CI evidence/provider | current CI standards | consume only | Validation/Release truth |
| GitHub event/operator attribution | `GITHUB_AGENT_INTERACTION_PROTOCOL.md` | additive refs/events only if existing v2 cannot carry them | second event protocol |
| Task Learning / evolution | v4.8 `EXECUTION_ARCHITECTURE_STANDARD.md`, Task Learning Evidence v1, existing Evolution Intake | backward-compatible friction/recurrence fields/mappings | new learning DB/family/intake |
| downstream generality evidence | `RELEASE_STANDARD.md` consumes a v4.9 dogfood report/checklist | new release evidence requirement, no new lifecycle | self-attested runtime state |

### Why one new standard owner is justified

`PROPORTIONAL_ASSURANCE_STANDARD.md` owns **composition**, not domain requirements. Putting composition inside Review, Validation or Release would let one gate owner accidentally govern another. Putting it entirely in `EXECUTION_ARCHITECTURE_STANDARD.md` would blur the current explicit boundary that orchestration does not redefine domain authorities. A narrow composition standard preserves both separation and a single deterministic algorithm.

## 4. Assurance requirement model

### 4.1 Obligation atoms, not a scalar risk score

Each applicable owner contributes one or more normalized obligation atoms:

```text
obligation_id
owner_ref
requirement_domain
minimum_requirement
currentness_ref
positive_reduction_rule_ref?
reduction_predicates[]?
proof_refs[]?
```

Example domains include:

```text
review
validation:<scope/profile>
independence:<dimension>
claim/admission
release-applicability
closure/hidden/rq
security/write-set
currentness/freshness
evidence-transfer
```

For domains with an owner-defined monotonic order, composition takes the stricter value. Across independent domains, composition is set conjunction/union. If two applicable atoms in the same domain are incomparable or contradictory and no owning rule resolves them, the result is `BLOCKED_OWNER_CONFLICT`.

No global numeric risk score participates in authority.

### 4.2 Owner-scoped reduction proof state

A reduction predicate resolves to exactly one proof state:

```text
PROVEN_TRUE
PROVEN_FALSE
UNKNOWN_OR_AMBIGUOUS
STALE
CONTRADICTORY
```

Only `PROVEN_TRUE` may activate the owner's lower requirement.

The proof must reference either:

- current durable facts whose semantics the owner accepts; or
- a deterministic check/rule explicitly accepted by that owner.

A model-generated classification without such proof is `UNKNOWN_OR_AMBIGUOUS` for reduction authority.

For `PROVEN_FALSE`, `UNKNOWN_OR_AMBIGUOUS`, `STALE` or `CONTRADICTORY`, the owner retains its unreduced requirement unless its own rule requires `BLOCKED`.

### 4.3 Composition algorithm

Deterministic order:

```text
1. discover applicable current/pinned owners
2. load each owner's unreduced obligations
3. load only owner-declared reduction permissions
4. evaluate every reduction predicate against accepted proof sources
5. apply owner-scoped reductions only for PROVEN_TRUE
6. normalize obligations by domain
7. compose independent domains by conjunction
8. apply domain-specific stricter/meet rule where defined
9. unresolved owner/applicability/conflict => stronger legal requirement or BLOCKED
10. resolve required roles/gates/independence/release status
11. emit Assurance Resolution v1
```

The resolver may always select an assurance path above the floor; it cannot select below it.

## 5. New machine family 1 — Assurance Resolution v1

Candidate file: `schemas/assurance-resolution-v1.schema.json`.

Owner: `PROPORTIONAL_ASSURANCE_STANDARD.md`.

Purpose: durable, auditable evidence of how current owner requirements and proof refs produced one legal workflow selection. It is a decision record, **not** a source of requirement authority.

Conceptual fields:

```text
schema_version
resolution_id
repository_ref
work_item_ref?
version_ref?
subject_ref
frozen_product_ref
frozen_architecture_ref?
task_or_pack_refs[]
owner_requirements[]:
  owner_ref
  requirement_domain
  unreduced_requirement
  reduction_rule_ref?
  predicates[]:
    predicate_id
    proof_state
    proof_refs[]
    deterministic_rule_ref?
  resolved_requirement
authority_currentness_refs[]
composed_obligations[]
assurance_floor_digest
selected_profile_ref?
required_roles[]
required_gate_refs[]
required_independence_dimensions[]
release_applicability_decision_ref?
evidence_disposition_refs[]
adverse_finding_refs[]
wait_or_block_reason?
actor/controller_ref
created_at
supersedes_resolution_ref?
```

Rules:

- a digest/index is convenience; owners/proofs remain inspectable;
- the record cannot invent a gate or declare PASS;
- missing applicable owner facts invalidate lower-path selection;
- a successor resolution never rewrites its predecessor;
- a stale resolution is historical-only;
- no private chain-of-thought is stored.

## 6. New machine family 2 — Role Execution Profile v1

Candidate file: `schemas/role-execution-profile-v1.schema.json`.

Owner: `EXECUTION_ARCHITECTURE_STANDARD.md`.

Purpose: express the Frozen Product Agent Execution Base Contract for any standardized/used authority-bearing role without duplicating executor capability evidence.

Conceptual fields:

```text
schema_version
role_profile_id
role
profile_version
source_authority_refs[]
eligibility_requirements[]
required_input_refs[]
allowed_actions[]
forbidden_actions[]
required_evidence[]
terminal_authority
independence_dimensions[]
selector_conflict_policy?
environment_class?
mutation_class = READ_ONLY | MUTABLE | AUTHORITY_TRANSITION
claim_requirement = REQUIRED | NOT_REQUIRED | INHERIT
handoff_requirements[]
```

Rules:

- Role Profile says what the role may/must do; Agent Capability Profile says what an executor claims/can prove it can do;
- provider/model is never Role authority;
- a project-specific role profile may be stricter but cannot weaken applicable ADS/Frozen authority;
- identical lifecycle depth is not required for every specialized role;
- profiles may be repository documents/YAML/JSON compiled to this shape; no new runtime service is required.

## 7. Existing machine-contract extensions

### 7.1 `schemas/dispatch.schema.json`

Backward-compatible optional refs:

```text
assurance_resolution_ref?
role_execution_profile_ref?
phase_ref?
selector_independence_basis_ref?
```

Dispatch remains the existing executable handoff and lifecycle.

### 7.2 Execution Pack manifest / execution contract

Optional refs:

```text
assurance_resolution_ref?
role_execution_profile_ref?
required_gate_binding_refs[]?
```

These refs narrow execution to the current legal decision; they never redefine Task Pack authority.

### 7.3 v4.8 Task Learning Evidence v1

Backward-compatible optional v4.9 fields/mappings may include:

```text
execution_friction_class?
recurrence_refs[]?
root_cause_relation = SAME | RELATED | UNKNOWN | DIFFERENT
prevention_point_refs[]?
recurrence_audit_ref?
ads_evolution_candidate_ref?
```

No `Execution Learning Record v1`, recurrence database or parallel evolution event family is introduced.

### 7.4 Validation/Review evidence

Existing reports/events may add optional `binding_profile_ref` / `currentness_decision_ref` / `transfer_decision_ref` references only where their owning gate standard adopts them. A generic resolver cannot require or synthesize them unilaterally.

## 8. JIT orchestration and durable wait semantics

The Frozen Task DAG/current Task authority contains semantic concerns/dependencies. It does **not** need to pre-expand every execution phase as an Issue.

Runtime/controller behavior:

```text
semantic work becomes potentially ready
→ compute Assurance Resolution
→ if known lineage/dependency prerequisite absent:
     record/derive WAITING_LINEAGE (no dispatch)
→ if legal role phase required:
     materialize/reuse allowed durable container JIT
→ choose eligible executor via v4.8 hard eligibility
→ existing Dispatch reservation
→ existing Claim admission
→ execute role
→ consume terminal/finding
→ recompute
```

`WAITING_LINEAGE` does not require a new canonical Issue workflow label. It is represented by durable dependency/lineage facts plus, when useful, the current Assurance Resolution `wait_or_block_reason`; derived views may display `WAITING_LINEAGE`.

Known-not-ready work MUST NOT be dispatched merely to obtain a deterministic BLOCKED terminal.

## 9. Phase/container coalescing

One Issue/container may host sequential phases only if the Assurance Resolution and applicable Role Profiles prove every required independence dimension.

Each phase remains distinguishable by:

```text
phase_ref
role_profile_ref
dispatch/claim ref when required
principal/session provenance
exact subject
evidence/terminal
phase transition
```

A container is never proof of independence. When confidentiality, host separation, write isolation, Hidden-holder separation or authority requires another container/session, coalescing is forbidden.

## 10. Adverse terminal and finding dominance

Reducer state includes unresolved adverse findings separately from the latest verdict.

```text
unresolved_finding_set = UNION(current applicable adverse findings)
                         - explicit owning-authority dispositions
                         - findings proven obsolete only by authorized successor-subject rules
```

Hard rules:

- later PASS from another reviewer does not erase an unresolved P0/P1/P2 blocker merely by chronology;
- a same-subject re-dispatch intended only to seek PASS is rejected;
- re-review is eligible only after an authorized successor subject or an owning-authority disposition explicitly permits it;
- historical adverse evidence remains immutable even after disposition;
- orchestrator ranking cannot route around independence/selector conflicts.

No new review-result family is required by default; reducer semantics consume existing Review/finding evidence.

## 11. Gate-owned evidence binding matrix

Generic orchestration MUST load the applicable gate owner's binding/transfer rule. It cannot infer a universal equivalence rule.

| Evidence family | Default binding owner | Minimum binding dimensions | v4.9 generic transfer posture |
|---|---|---|---|
| concern Validation | `VALIDATION_STANDARD.md` / Frozen Task | tested SHA, profile/scope, environment/toolchain, authority refs | existing explicit impact/currentness rules only |
| integration Validation | Validation/Integration owner | source/head + target/base + composed result + profile/environment | explicit impact/composition proof only |
| Review | Review policy/current authority | exact subject/diff, authority refs, required independence | **fresh-only on material subject change** unless owner explicitly defines successor semantics; complete-delta successor Review is a new Review, not PASS transfer |
| Hidden | Release/Hidden authority | frozen candidate, private pack/revision, holder policy | fresh-only on candidate/pack/holder drift unless owner positively states otherwise |
| Closeout/RQ | `RELEASE_STANDARD.md` | frozen candidate, predecessor gate bindings, release authority | fresh-only on candidate drift |
| CI evidence | CI evidence owner | exact SHA/run/profile/provider when provider-specific | according to CI/Validation owner; never generic PASS transfer |
| Task Learning | v4.8 Execution Architecture | work/subject/evidence refs | historical learning evidence only; never Gate PASS |

Generic rules:

```text
NO_OWNER_TRANSFER_RULE => HISTORICAL_ONLY
UNKNOWN_BINDING => HISTORICAL_ONLY_OR_BLOCKED
OWNER_FRESH_ONLY => FRESH_EXECUTION_REQUIRED
MATERIAL_BINDING_CHANGE => SUCCESSOR_ASSURANCE_REQUIRED
```

Path disjointness, unchanged HEAD or ancestry may be inputs to a gate-specific proof, never authority by themselves.

## 12. Release applicability architecture

`RELEASE_STANDARD.md` remains the owner. v4.9 adds a prospective applicability decision vocabulary to separate concern execution from version-release ceremony:

```text
REQUIRED_NOW
DEFERRED_TO_VERSION_CLOSURE
NOT_APPLICABLE
UNKNOWN
```

Semantics:

### `REQUIRED_NOW`

The current subject/candidate must execute the Release-owned gate now. Mandatory for post-Freeze required content change/thaw paths and whenever current Release authority explicitly requires it.

### `DEFERRED_TO_VERSION_CLOSURE`

The concern/task/PR itself does not run the full release ceremony, but its content remains part of the version candidate and the owning version closure still owes all Release-required gates. This is the normal safe proportional result for many pre-Freeze concerns.

### `NOT_APPLICABLE`

Allowed only under a positive Release-owned rule whose predicates are proven under the Assurance Resolver. It never means that a still-applicable version-level release obligation disappears.

### `UNKNOWN`

Fails closed to the stronger currently legal path or `BLOCKED`.

Migration rules:

- only owning project/Release governance can migrate applicability policy;
- migration is prospective;
- a Frozen/qualified/otherwise authority-bound candidate retains gates already required by its bound authority;
- `FROZEN → required content change` continues to follow current `RELEASE_STANDARD.md` thaw/invalidate semantics.

This vocabulary prevents the ambiguous equation `no task-level release ceremony == no version-level release obligation`.

## 13. v4.8 predecessor and lineage behavior

L2/Task planning may proceed against the exact frozen v4.8 Product/L2 blobs.

Implementation that requires v4.8-owned machine contracts or runtime semantics MUST NOT guess their final integrated file/state. Until the required v4.8 implementation baseline is integrated or an explicit compatibility rebind proves an equivalent target, affected v4.9 executable work remains:

```text
WAITING_LINEAGE
```

This is a non-dispatch state, not a reason to create stale task branches or guaranteed-BLOCKED Builder dispatches.

Before v4.9 Release Qualification:

- required v4.8 predecessor must be in the applicable integrated lineage;
- if frozen v4.8 Product/L2 authority drifts/thaws/supersedes, v4.9 currentness is re-evaluated;
- if integrated implementation surfaces differ materially from the architecture assumed here, route to L2 amendment rather than silent adaptation.

## 14. P4 recurrence architecture

The recurrence audit is an evidence-producing helper around existing v4.8 Task Learning/Evolution ownership.

Input:

```text
current Task Learning / friction evidence
candidate prior related evidence refs
owner/version/task context
```

Output:

```text
relation = SAME | RELATED | UNKNOWN | DIFFERENT
earliest_prevention_point_refs[]
reproduction/counterexample refs[]
recommended existing disposition = NONE_MATERIAL | TASK_CLARIFICATION | ADS_EVOLUTION_CANDIDATE | MORE_EVIDENCE
```

`UNKNOWN` does not auto-promote a standard change. The audit may be manual/model-assisted, but promotion still enters existing ADS Intake/L1/Product/Architecture governance.

## 15. Downstream dogfood evidence architecture

No new runtime lifecycle is required. A release-consumable **Proportional Dogfood Report** (document/template; schema optional later only if justified) binds:

```text
exact ADS candidate/version
qualifying downstream repository
pinned Product/Architecture/Task/Review/Validation/Release refs
legal baseline workflow
selected proportional workflow
Assurance Resolution refs
mechanism matrix: EXERCISED | NOT_EXERCISED + proof refs
container/dispatch/claim/gate/rebind counts
nonzero baseline-vs-selected delta
ambiguous-predicate exercise and fail-closed result
manual/GitHub-native execution evidence
independent auditor identity/profile
safety-negative evidence refs
UNAUTHORIZED_GATE_OMISSION=0
STALE_PASS_TRANSFER=0
INDEPENDENCE_LOSS=0
CROSS_OWNER_REQUIREMENT_CANCELLATION=0
ADVERSE_TERMINAL_SUPPRESSION=0
claim boundary for unexercised mechanisms
```

The independent auditor must satisfy evidence-source independence and cannot be the orchestrator/Builder principal for the tested decisions.

The report is Release evidence; it does not become execution authority. Baseline=selected with zero proportional delta is compatibility evidence only and cannot satisfy downstream generality.

## 16. Compatibility and progressive adoption

v4.9 is additive/non-weakening:

- older pinned projects continue under their pinned authority until owning governance migrates prospectively;
- historical Dispatch/Claim/Review/Validation/Release evidence remains historical truth;
- new schema refs are optional unless current v4.9/Frozen project authority requires them;
- manual execution may create Assurance Resolution/Role Profile information in durable Markdown/JSON and use one designated existing admission writer;
- no scheduler daemon, runtime DB or new transport is required;
- `ai-dev:event:v2` remains the GitHub event writer protocol unless an additive field/ref is proven necessary;
- v4.8 Agent Capability / Capability Evidence / Task Learning families remain their existing families;
- release applicability defaults to current existing authority until the prospective v4.9 Release-owned rules are implemented and pinned.

## 17. Security / privacy

- store proof refs and externally useful rationale summaries, not private reasoning traces;
- do not copy secrets/credentials/Hidden fixtures into Assurance Resolution or Role Profiles;
- selector/principal/session provenance is retained only as required for accountability/independence;
- capability/tool/credential presence never grants mutation/side-effect authority;
- Hidden-holder separation cannot be collapsed by orchestration;
- model/provider diversity metadata is provenance, not a quality/authority score.

## 18. Architecture UNKNOWNs and disposition

| ID | UNKNOWN | Impact | Disposition | Architecture decision |
|---|---|---|---|---|
| U1 | Does proportional assurance need a super-owner over Review/Validation/Release? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. One narrow composition standard owns only composition/proof semantics; domain owners keep requirements. |
| U2 | Can `ASSURANCE_FLOOR` be represented as one risk/profile scalar? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Use owner-attributed obligation atoms + domain-specific meet/conjunction; conflict can BLOCK. |
| U3 | Can model classification itself prove a reduction predicate? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Only durable facts or owner-accepted deterministic checks can prove reduction. |
| U4 | Does Assurance Resolution become new authority? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. It is immutable/reconstructible decision evidence referencing authority owners. |
| U5 | Does Role Profile duplicate v4.8 Agent Capability Profile? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Role Profile = required behavior/authority; Agent Capability = executor claim/evidence used for eligibility. |
| U6 | Is a second scheduler/work lifecycle required for JIT phases? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Reuse Task DAG/Issue Dependencies, existing dispatch/claim and JIT container materialization. |
| U7 | Does `WAITING_LINEAGE` require a new canonical Issue state? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Durable dependency/lineage + resolution wait reason; derived display only. |
| U8 | Can generic evidence equivalence override Gate Authority? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Gate-owned binding/transfer matrix; no positive owner rule => historical-only. |
| U9 | Can Review PASS from another reviewer erase an unresolved finding? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Finding-union/blocker dominance is separate from latest terminal chronology. |
| U10 | Does proportional Release applicability mean no version closure? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Distinguish REQUIRED_NOW / DEFERRED_TO_VERSION_CLOSURE / NOT_APPLICABLE / UNKNOWN. |
| U11 | Can migration shorten gates already bound to a Frozen candidate? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Prospective only; current Release thaw semantics preserved. |
| U12 | Does P4 require a new learning/evolution family or database? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Backward-compatible extension/mapping of v4.8 Task Learning and existing Evolution Intake. |
| U13 | Must v4.8 already be integrated before L2/Task planning? | High | `STATIC_EVIDENCE_SUFFICIENT` | No for planning; yes before dependent execution unless explicit compatibility rebind. Use WAITING_LINEAGE. |
| U14 | Is a scheduler daemon/runtime DB required? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Manual/GitHub-native path remains conformant. |
| U15 | Is a pre-L2 executable Research Demo required? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Architecture depends on deterministic contract/reducer semantics already expressible with existing owners; novel runtime mechanisms, if chosen later, require scoped proof then. |

### Research Demo decision

**No executable Research Demo is required before L2 Freeze for this candidate.**

No adopted architecture depends on an unproven external service, distributed transaction, proprietary queue or novel storage primitive. The new behavior is contract/reducer logic whose correctness must be proven by deterministic conformance/negative tests during implementation and by downstream dogfood before Release Qualification.

A later implementation that introduces a novel distributed scheduler/locking/equivalence engine outside these static assumptions must create a narrow Research Demo before that mechanism can satisfy Frozen Architecture.

## 19. Conformance / negative oracles

At minimum reject:

```text
model says low risk -> reduction predicate PROVEN_TRUE
missing owner -> assume not applicable
one owner permits skip -> delete another owner's gate
risk score 2 < 3 -> universal assurance comparison
ambiguous predicate -> choose cheaper path
Assurance Resolution says PASS -> Gate PASS
new Resolution -> rewrite old Resolution
Role Profile capability field -> executor capability proven
Agent Capability Profile -> role mutation authority
provider/model name -> role authority
same Issue/session -> independence proven
selector authored subject -> silently selects friendly reviewer
Reviewer R1 P1 -> R2 PASS erases R1 finding
same-subject redispatch -> PASS-shopping
known lineage block -> dispatch Builder to obtain BLOCKED
JIT phase -> invent new semantic Task concern
path disjoint -> Review/Validation transfer authorized
unchanged HEAD -> all evidence transferable
no transfer rule -> reuse historical PASS
Validation HEAD drift -> impact decision transfers PASS to new HEAD
candidate drift -> Hidden/RQ PASS transferred
pre-Freeze task -> full release ceremony required by default despite release owner deferring to closure
DEFERRED_TO_VERSION_CLOSURE -> release obligation disappears
NOT_APPLICABLE without Release-owner positive rule -> accept
post-Freeze required content change -> retain old candidate freeze
project migration -> remove already-bound Hidden/RQ gate
v4.8 not integrated -> start dependent v4.9 implementation on guessed interfaces
Task Learning friction -> auto-mutate ADS
recurrence similarity -> SAME root cause without evidence
baseline=selected dogfood -> downstream generality satisfied
Builder/orchestrator self-audit -> independent dogfood safety audit
scheduler cache -> durable project authority
transport ACK -> role terminal/gate truth
```

## 20. Positive conformance scenarios

Implementation must eventually prove at least:

1. known single owner + proven reduction predicate selects the owner-permitted lower obligation;
2. same owner + ambiguous predicate retains stronger requirement/BLOCKED;
3. two owners compose without cross-owner cancellation;
4. incomparable owner requirements BLOCK rather than heuristic-pick;
5. low-risk concern gets focused concern gates while release work is `DEFERRED_TO_VERSION_CLOSURE` where Release owner permits;
6. post-Freeze content change remains `REQUIRED_NOW` and follows thaw/requalification;
7. Task remains `WAITING_LINEAGE` without dispatch when v4.8 implementation lineage is missing;
8. JIT phase uses existing Task/Dispatch/Claim and cannot widen semantic scope;
9. capable executor rejected for independence/selector conflict;
10. one durable container carries Builder→Review only when independent phase constraints actually pass;
11. unresolved adverse finding survives unrelated later PASS;
12. successor subject after authorized repair permits fresh re-review;
13. concern Validation base drift reuses evidence only through current Validation owner impact semantics;
14. Review material subject change requires a new review, not PASS transfer;
15. P4 recurrence produces v4.8-compatible learning/evolution evidence only;
16. downstream dogfood records at least one nonzero legal delta and independent safety audit;
17. all flows can be executed manually/GitHub-native with no scheduler daemon.

## 21. Expected implementation touchpoints

After L2 Freeze, Task DAG should decompose at least:

1. `PROPORTIONAL_ASSURANCE_STANDARD.md` + Assurance Resolution v1 schema + deterministic composition rules/tests;
2. Execution Architecture integration: resolution consumption, JIT/wait semantics, adverse-finding reducer rules;
3. Role Execution Profile v1 schema + Base Contract semantics;
4. Work Item / Execution Pack / Dispatch backward-compatible refs;
5. gate-owned evidence binding/currentness matrix integration, including Review fresh-only and existing Validation impact semantics;
6. Release Standard prospective applicability vocabulary/predicates and migration protection;
7. v4.8 Task Learning friction/recurrence backward-compatible extensions;
8. v4.8 capability/eligibility/Dispatch-Claim integration and predecessor-lineage wait/rebind behavior;
9. Proportional Dogfood Report/checklist + independent auditor profile/terminal;
10. deterministic conformance/negative oracle suite covering Product scenarios A–Q and L2 §19–20;
11. manual/GitHub-native reference flow / examples and pointer-only task triggers;
12. registry/discoverability/docs reconciliation;
13. integrated downstream dogfood + release evidence handoff;
14. closure/currentness compatibility work.

Exact Task IDs, dependencies, write sets, Review Policies and task branching belong to the Task DAG after L2 Freeze.

## 22. Local environment posture

`LOCAL_ENV=NOT_REQUIRED` for L2 planning/review/freeze.

No real runtime/host/distributed-service claim is made by this Architecture Evidence. Real implementation behavior, v4.8 integrated surfaces and downstream project dogfood require later exact-subject validation.

## 23. L2 Freeze gate

This L2 is **NOT FROZEN**.

Before L2 Freeze:

1. a genuinely fresh high-capability READ-ONLY Architecture Reviewer must review the exact L2 candidate;
2. reviewer must verify Frozen Product traceability for all four pillars and #702 F1–F12 safety repairs;
3. `PROPORTIONAL_ASSURANCE_STANDARD.md` must be confirmed as a narrow composition owner, not a super-gate owner;
4. two-new-family count and all existing-family extensions must be non-duplicative;
5. obligation-atom composition, fail-closed proof semantics and adverse-finding dominance must PASS;
6. Role Profile vs Agent Capability boundary must PASS;
7. evidence binding matrix must preserve Gate Authority and not generically transfer PASS;
8. Release applicability vocabulary must preserve current candidate/thaw/closure authority and prospective-only migration;
9. v4.8 predecessor binding/WAITING_LINEAGE strategy must PASS;
10. P4 reuse/no-parallel-learning-lifecycle must PASS;
11. Research Demo disposition must PASS or any newly identified material UNKNOWN must be explicitly dispositioned;
12. P0/P1 must be zero before Freeze.

```text
L2_STATUS=CANDIDATE_NOT_FROZEN
RESEARCH_DEMO_REQUIRED=NO
TASK_DAG_AUTHORITY=NO
IMPLEMENTATION_AUTHORITY=NO
NEXT=FRESH_INDEPENDENT_ARCHITECTURE_REVIEW
```
