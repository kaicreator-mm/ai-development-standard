# v4.8.0 Task DAG — Evidence-Driven Agent Orchestration & Standard Evolution

Status: **FROZEN TASK DAG — 2026-10-01**

Freeze inputs:

- Frozen Product: `PRODUCT_FREEZE.md` blob `8720264f56a23e352b347dd74df966b9416c9129`;
- Frozen PRD blob: `f26439580e00de6ed8b2e27d732a3095eb566219`;
- Frozen Architecture: `L2_FREEZE.md` blob `f495535b6a16c30b3043fbacedb19cc8be01d541`;
- Frozen L2 blob: `f88c85454e80101a0fdf56050e21f11a05279841`;
- Fresh Independent Architecture Re-Review R3: #502 comment `5927313354` = PASS, P0/P1/P2/P3=0, L2 Freeze authorization YES;
- Task DAG Controller: #504;
- planning baseline: `main@e75fe834469c5ea9f9a384f7d84e38c3a48afa46`;
- intended implementation integration target: `version/v4.8.0` after canonical planning integration.

This DAG is subordinate to the Frozen Product and Frozen L2. It cannot weaken owner boundaries, exact-subject/currentness, Review/Validation authority, composite resource admission, Interchange reuse, or the evidence limitations frozen above.

## 1. Planning DAG

```text
ROOTS

T-001 Machine Contract Families ───────────────┐
                                               ├─────► T-002 Execution Architecture Core
                                               │            │
                                               │            ├─────► T-008 Eligibility / Resource Conformance
                                               │            │
                                               │            └─────► T-012 #469 Task-Class Dogfood
                                               │
                                               ├─────► T-004 Task Learning Closeout Wiring
                                               │            │
                                               │            ├─────► T-010 Learning / Evolution Conformance
                                               │            │
                                               │            └─────► T-012 #469 Task-Class Dogfood
                                               │
                                               └─────► T-007 Contract / Compatibility Conformance

T-003 Existing Interchange Profile ────────────┬─────► T-009 Interchange Replay / Restart Conformance
                                               │
                                               └─────► T-011 Heterogeneous Orchestration Dogfood

T-005 ADS Evolution Governance ────────────────┬─────► T-010 Learning / Evolution Conformance
                                               │
                                               └─────► T-013 Cross-Project Evolution Dogfood

SEMANTIC / ADOPTION CONVERGENCE

T-001 ─┐
T-002 ─┤
T-003 ─┼─────► T-006 Registry / Adoption Wiring
T-004 ─┤
T-005 ─┘

CONFORMANCE / DOGFOOD

T-007 ──────────────┐
T-008 ──────────────┼─────► T-011 Heterogeneous Orchestration Dogfood
T-009 ──────────────┘

T-007 ──────────────┐
T-008 ──────────────┼─────► T-012 #469 Task-Class Dogfood
T-004 ──────────────┘

T-004 ──────────────┐
T-005 ──────────────┼─────► T-013 Cross-Project Evolution Dogfood
T-006 ──────────────┤
T-010 ──────────────┘

PRE-CLOSURE JOIN

T-006 ─┐
T-007 ─┤
T-008 ─┤
T-009 ─┤
T-010 ─┼─────► T-014 Integrated Convergence / Closure Inputs
T-011 ─┤
T-012 ─┤
T-013 ─┘
                 │
                 ▼
          Version Closure
```

Exact dependency summary:

```text
T-001: []
T-002: [T-001]
T-003: []
T-004: [T-001, T-002]
T-005: []
T-006: [T-001, T-002, T-003, T-004, T-005]
T-007: [T-001]
T-008: [T-002]
T-009: [T-003]
T-010: [T-004, T-005]
T-011: [T-007, T-008, T-009]
T-012: [T-004, T-007, T-008]
T-013: [T-004, T-005, T-006, T-010]
T-014: [T-006, T-007, T-008, T-009, T-010, T-011, T-012, T-013]
```

Initial roots are **T-001, T-003 and T-005**. These are separate semantic owners/write sets and can progress safely in parallel from the same Frozen planning checkpoint.

## 2. Task definitions

### T-001 — Three Machine Contract Families

Lane: `contract`

Own exactly the three new default v4.8 machine families frozen by L2:

1. Task Learning Evidence v1;
2. Logical Agent Capability Profile v1;
3. Agent Capability Evidence v1.

Expected outputs:

- schemas + focused fixtures/examples;
- deterministic positive/negative schema tests;
- backward-compatibility posture showing no fourth Availability/Exchange family;
- machine/prose terminology aligned with Frozen L2.

Acceptance:

- Capability Profile contains logical Agent/operator/model execution claims only;
- runner/host/device/toolchain/resource/concurrency/network facts remain references to existing infrastructure owners;
- Capability Evidence is historical/exact-subject evidence, never current Validation/Review authority;
- Task Learning supports `TASK_LEARNING=NONE_MATERIAL` Fast Path and excludes private chain-of-thought;
- no provider/model scalar correctness score or authority inference.

### T-002 — Execution Architecture Core: Learning, Eligibility and Composite Resource Admission

Lane: `execution-core`

This Task is the **single owner lane** for v4.8 changes to `EXECUTION_ARCHITECTURE_STANDARD.md` and directly related Task/Dispatch execution semantics, avoiding competing PRs against the same semantic owner.

Own:

- Task Learning evidence owner/lifecycle semantics;
- logical Agent capability + environment/runner + Availability + Capability Evidence composition;
- `ELIGIBLE | INELIGIBLE | UNKNOWN` derived projection;
- hard filters before optional ranking;
- optional backward-compatible Task/Execution Pack/Dispatch references;
- scarce/exclusive/capacity-N resource admission;
- one all-or-none linearization point for work claim + every required resource binding;
- crash/publication reconciliation and fail-closed replacement admission.

Acceptance:

- existing READY/Dispatch/Claim remain canonical;
- no scheduler state machine/database becomes authority;
- independent per-key CAS/leases are explicitly insufficient for composite admission;
- capacity-N active accepted bindings never exceed N; exclusive resource is N=1;
- no accepted canonical partial state exists;
- reviewer/validator independence, currentness, authority and security are hard predicates;
- ranking/cost/latency cannot turn INELIGIBLE/UNKNOWN into ELIGIBLE.

### T-003 — Existing Interchange v1 Profile / Adapter Mapping

Lane: `interchange`

Own v4.8's use of the **existing** v4.0 Interchange owner/family.

Expected outputs:

- compatible profile/extension guidance only where a proven v4.8 field/ref gap exists;
- mapping to `GITHUB_AGENT_INTERACTION_PROTOCOL.md` and `ai-dev:event:v2`;
- transport adapter rules for webhook/queue/local/orchestrator/A2A-style carriers without new lifecycle authority;
- idempotency/replay/conflicting-payload/currentness/durable-materialization rules;
- restart reconstruction from durable facts.

Acceptance:

- no `agent-exchange-envelope-v1` replacement family;
- no new Agent Exchange normative owner;
- existing `interchange-envelope-v1` remains canonical generic family;
- transport ACK/progress never means Task/Review/Validation completion;
- critical semantic effects are durable through their canonical owner;
- historical Interchange/Event payloads remain valid.

### T-004 — Task Learning Closeout / Template Wiring

Lane: `learning-wiring`

Depends on T-001/T-002 so exact machine and owner semantics are stable first.

Own only closeout/adoption surfaces, for example applicable Task Pack, Task Issue, final-closeout, review/checklist or Execution Pack references.

Acceptance:

- material-learning path and `NONE_MATERIAL` path are both explicit;
- closeout points to evidence instead of copying large bodies;
- exact-subject behavioral claims cannot silently rebind after code drift;
- learning does not replace ADR, Incident, Product, Architecture, Review or Validation authority;
- no private chain-of-thought is required.

### T-005 — ADS Evolution Governance / Intake

Lane: `governance`

Own classification and promotion governance for:

```text
PROJECT_DEFECT
AGENT_EXECUTION_DEFECT
ENVIRONMENT_OR_TOOL_DEFECT
PROJECT_SPECIFIC_REQUIREMENT
STANDARD_FRICTION_CANDIDATE
ADS_EVOLUTION_CANDIDATE
```

Expected outputs:

- applicable `DEVELOPMENT_WORKFLOW.md`/Intake/template/checklist wiring;
- evidence requirements for promotion;
- NO_CHANGE / MORE_EVIDENCE / normal ADS change routes;
- privacy/publication classification and minimization guidance.

Acceptance:

- no telemetry/threshold/model/scheduler self-amends ADS;
- promotion always re-enters ordinary ADS Intake → L1 → PRD → L2 → Task → Review/Validation;
- v4.5 incident feedback and v4.6 intent/skill ownership remain intact;
- no universal numeric promotion threshold is introduced.

### T-006 — Registry / Discoverability / Adoption Wiring

Lane: `registry-adoption`

Convergence Task after all semantic owner Tasks stabilize.

Own:

- `standard-manifest.json` / v4.7 registry discoverability for new schemas/updated owners;
- project-adoption/progressive-disclosure references;
- migration/adoption notes;
- central wiring that would otherwise create cross-lane write conflicts.

Acceptance:

- registry points to canonical owners but grants no authority;
- Interchange reuse is represented as reuse, not a fourth new family;
- historical consumers remain valid;
- Fast Path adoption remains lightweight.

### T-007 — Contract / Historical Compatibility Conformance

Lane: `contract-conformance`

Own executable machine/prose compatibility tests for T-001.

Acceptance must include negative oracles rejecting:

- Agent capability claim → proven capability;
- Capability Evidence → current Validation/Review PASS;
- provider/model identity → authority/correctness;
- runner/host facts copied into Logical Agent Profile as canonical ownership;
- fourth Availability/Exchange default family;
- stale exact-subject evidence silently rebound to successor source;
- private chain-of-thought required by Task Learning.

Historical v4 fixtures/payloads must remain valid where Frozen L2 requires compatibility.

### T-008 — Eligibility / Composite Resource Admission Conformance

Lane: `scheduling-conformance`

Own deterministic tests/reference scenarios for T-002.

Required cases:

- multiple simultaneously READY Tasks;
- heterogeneous logical Agent profiles;
- stale/fresh Availability facts;
- reviewer/validator independence conflict;
- hard-filter then optional ranking order;
- capacity N with competing assignments;
- N=1 exclusive resource;
- work claim + multiple resource bindings under one composite admission;
- injected partial-write/crash ambiguity;
- fail-closed reconciliation before replacement admission;
- no safe composite primitive → exclusive single writer or BLOCKED/UNAVAILABLE.

A novel distributed multi-key CAS/lease mechanism is out of scope unless separately proven by Research Demo/Validation.

### T-009 — Interchange Replay / Restart Conformance

Lane: `interchange-conformance`

Own deterministic conformance against the existing Interchange family/profile.

Required cases:

- duplicate delivery / same semantic identity + same payload;
- same identity + conflicting payload/digest fails closed;
- lost/replayed delivery;
- stale exact-subject request;
- transport ACK/progress remains non-authoritative;
- authoritative result materialization through existing owner;
- restart reconstructs current authority without transient queue/chat history;
- GitHub `ai-dev:event:v2` remains GitHub admission/writer authority.

### T-010 — Task Learning / Evolution Governance Conformance

Lane: `governance-conformance`

Own executable/fixture conformance for T-004/T-005.

Required cases:

- `TASK_LEARNING=NONE_MATERIAL` Fast Path;
- material learning with identity/evidence layers;
- stale learning remains historical;
- project/Agent/environment/project-specific classifications do not auto-promote;
- STANDARD_FRICTION_CANDIDATE can end in MORE_EVIDENCE/NO_CHANGE;
- ADS_EVOLUTION_CANDIDATE still requires ordinary ADS governance;
- privacy/minimization/project-private vs publishable evidence;
- no hidden Validation/evaluator leakage.

### T-011 — Heterogeneous Multi-Agent / Resource / Transport Dogfood

Lane: `orchestration-dogfood`

Own the Frozen PRD heterogeneous orchestration dogfood.

Must attempt to falsify the architecture with:

- multiple READY work items;
- at least two materially different logical Agent capability profiles;
- current/stale environment Availability;
- shared scarce resource contention;
- duplicate/incompatible assignment race;
- reviewer/validator independence conflict;
- transport duplicate/replay/loss;
- crash/restart durable reconstruction;
- lower-cost bounded executor success where appropriate;
- bounded executor escalation on semantic ambiguity.

Synthetic evidence stays labeled synthetic. Any real external host/device/provider claim requires exact-subject real Validation or remains NOT_RUN/BLOCKED.

### T-012 — #469 Task-Class / Bounded-Agent Dogfood

Lane: `469-dogfood`

Consume #469 and successor measured evidence as a **dogfood input**, not pre-authorized standard truth.

Own:

- exact Task-class capability/eligibility evidence capture for bounded-agent runs;
- clarification/escalation count;
- edit/test loop count;
- negative-oracle and contract/write-set drift findings;
- stale pack/base rebinds;
- Validation/Review findings and rework;
- measured resource/time/cost fields only when actually observed;
- comparison limits and evidence-strength classification.

Acceptance:

- `ECONOMIC_SAVINGS=NOT_MEASURED` remains until a comparable methodology actually measures it;
- no blanket strong→low-cost rule;
- provider/model identity remains provenance;
- required Fresh Independent Review remains distinct from Builder/Validation;
- output can support MORE_EVIDENCE, NO_CHANGE or a later evidence-backed candidate, not automatic adoption.

### T-013 — Cross-Project ADS Evolution Dogfood

Lane: `evolution-dogfood`

Own cross-project feedback/evolution falsification using at least two materially distinct Task/project evidence streams when available.

Required cases:

- observation classification;
- false-positive prevention;
- repeated friction aggregation;
- privacy/minimization/publication boundary;
- project-specific requirement rejected as standard change;
- environment/Agent defect rejected as standard change;
- MORE_EVIDENCE / NO_CHANGE path;
- justified ADS_EVOLUTION_CANDIDATE handoff into ordinary ADS Intake.

#469 may be one evidence stream but cannot be the sole basis for broad economic/performance policy.

### T-014 — Integrated Convergence / Version Closure Inputs

Lane: `integration-closure`

This is the only pre-Closure join.

Own integrated v4.8 conformance and durable Version Closure inputs after all semantic/conformance/dogfood lanes complete.

Acceptance:

- exactly three new machine families remain canonical;
- Interchange remains reused, not duplicated;
- owner uniqueness/non-duplication holds across v4.1–v4.8;
- hard eligibility before ranking and composite resource atomicity survive integration;
- historical compatibility/Fast Path remain valid;
- dogfood claims are bounded to their real evidence strength;
- no economic savings or universal routing inference without evidence;
- full repository verifier/regression and required integrated Validation evidence are captured;
- produces closure inputs only, not Release Qualification verdict itself.

## 3. Planning table

| Task | Lane | Depends On | Parallel | Risk | Default executor/model suitability | Required Validation | Review Policy | Intended branch | Status |
|---|---|---|---|---|---|---|---|---|---|
| T-001 | contract | — | YES | H | high-capability contract designer; bounded builder allowed only from reviewed L3/contract | schema + compatibility tests | required | `task/v4.8.0-t01-contract-families` | TODO |
| T-002 | execution-core | T-001 | YES | H | high-capability semantic/concurrency builder | focused semantics + concurrency/failure validation | required | `task/v4.8.0-t02-execution-core` | TODO |
| T-003 | interchange | — | YES | H | high-capability protocol/owner-boundary builder | protocol/schema/event compatibility validation | required | `task/v4.8.0-t03-interchange-profile` | TODO |
| T-004 | learning-wiring | T-001,T-002 | YES | H | bounded integration builder after semantic freeze | template/reference + closeout conformance | required | `task/v4.8.0-t04-learning-closeout` | TODO |
| T-005 | governance | — | YES | H | high-capability governance builder | workflow/classification negative-oracle validation | required | `task/v4.8.0-t05-evolution-governance` | TODO |
| T-006 | registry-adoption | T-001,T-002,T-003,T-004,T-005 | YES | M/H | bounded central-wiring builder | manifest/registry/project-adoption verifier | required | `task/v4.8.0-t06-registry-adoption` | TODO |
| T-007 | contract-conformance | T-001 | YES | H | bounded test builder; high-capability oracle review | historical/schema compatibility suite | required | `task/v4.8.0-t07-contract-conformance` | TODO |
| T-008 | scheduling-conformance | T-002 | YES | H | high-capability concurrency/test builder | race/capacity/crash deterministic validation | required | `task/v4.8.0-t08-scheduling-conformance` | TODO |
| T-009 | interchange-conformance | T-003 | YES | H | bounded protocol-test builder | replay/idempotency/restart validation | required | `task/v4.8.0-t09-interchange-conformance` | TODO |
| T-010 | governance-conformance | T-004,T-005 | YES | H | bounded fixture/test builder + strong semantic review | classification/learning/privacy negative oracles | required | `task/v4.8.0-t10-governance-conformance` | TODO |
| T-011 | orchestration-dogfood | T-007,T-008,T-009 | YES | H | heterogeneous Agents; independent validator/reviewer | exact-subject scenario/real-host validation as applicable | required | `task/v4.8.0-t11-orchestration-dogfood` | TODO |
| T-012 | 469-dogfood | T-004,T-007,T-008 | YES | H | bounded/low-cost executor where eligible + high-capability independent reviewer | exact-subject Builder/Validation/Review evidence | required | `task/v4.8.0-t12-469-dogfood` | TODO |
| T-013 | evolution-dogfood | T-004,T-005,T-006,T-010 | YES | H | high-capability evidence/governance owner; project executors bounded by task | cross-project evidence + privacy/currentness validation | required | `task/v4.8.0-t13-evolution-dogfood` | TODO |
| T-014 | integration-closure | T-006,T-007,T-008,T-009,T-010,T-011,T-012,T-013 | NO | H | independent integration validator/reviewer | full integrated regression + closure evidence | required | `task/v4.8.0-t14-integration-closure-inputs` | TODO |

All implementation Task PRs target `version/v4.8.0` after canonical planning integration. Task branches are JIT from the current integration exact SHA only after native blockers satisfy; do not pre-create long-lived branches merely because this planning DAG is Frozen.

## 4. Lane summary / safe parallelism

| Lane | Tasks | Entry prerequisites | Shared-owner/write-set constraint | Converges at |
|---|---|---|---|---|
| contract | T-001,T-007 | Frozen L2; T-007 waits T-001 | T-001 owns the three new schemas; T-007 tests them, not semantic owner rewrites | T-011/T-012/T-014 |
| execution-core | T-002,T-008 | T-001 then T-002 | **T-002 alone owns v4.8 Execution Architecture semantic edits**; T-008 is conformance/tests | T-011/T-012/T-014 |
| interchange | T-003,T-009 | Frozen L2; T-009 waits T-003 | reuse existing Interchange/GitHub owners; no new family | T-011/T-014 |
| learning-wiring | T-004 | T-001,T-002 | templates/checklists/adoption only; no competing Execution Architecture owner edits | T-010/T-012/T-013 |
| governance | T-005,T-010 | Frozen L2; T-010 also waits T-004 | T-005 owns governance semantics; T-010 tests them | T-013/T-014 |
| registry-adoption | T-006 | T-001..T-005 stable | central wiring owner prevents cross-lane manifest conflicts | T-013/T-014 |
| orchestration-dogfood | T-011 | conformance T-007..T-009 | evidence only; no silent semantic repair | T-014 |
| 469-dogfood | T-012 | learning + contract/scheduling conformance | evidence only; no blanket routing/economic inference | T-014 |
| evolution-dogfood | T-013 | learning/governance/registry + conformance | evidence only; promotion through ordinary ADS governance | T-014 |
| integration-closure | T-014 | all required lanes complete | sole pre-Closure central integration/closure-input owner | Version Closure |

The DAG intentionally does **not** split `EXECUTION_ARCHITECTURE_STANDARD.md` semantics across parallel Tasks. Apparent extra concurrency there would be false parallelism because Task Learning, capability composition, eligibility and resource admission share one canonical owner and interact at Dispatch/Claim admission.

## 5. Review / Validation policy

All fourteen Tasks have `Review Policy=required` because each either changes public machine/owner/concurrency/governance semantics, validates high-risk compatibility, or produces evidence used by integrated Version Closure. This is a v4.8 task-level risk decision, not a global ADS rule that every Task in every project requires review.

Validation remains distinct from Review. A Builder's green tests do not self-certify real-host, concurrency, cross-transport, privacy, or cross-project claims. Where the current environment cannot execute a required external claim, create an exact-subject Validation Request and preserve `NOT_RUN/BLOCKED` rather than simulating PASS.

## 6. L3 / Task Pack planning

Before Builder dispatch:

- every Task receives a Task Pack with dependencies, allowed/forbidden write set, acceptance, Review Policy, required Validation, agent freedom, baseline/currentness handling and branch target;
- high-risk semantic Tasks T-001/T-002/T-003/T-005 and integration T-014 SHOULD receive high-capability-authored L3/reference guidance;
- T-012 MUST receive a risk-scaled exact Task-class/L3 + JIT Execution Pack suitable for bounded/low-cost execution and must preserve independent Validation/Review;
- T-011/T-013 require explicit evidence matrices and real-vs-synthetic boundaries;
- L3/reference material cannot expand Frozen Product/L2 scope.

## 7. Native Issue dependency graph

After this Frozen Task DAG checkpoint, Stage 2.5 materializes each T-001..T-014 as a GitHub Task Issue. GitHub Issue Dependencies are then the canonical live execution DAG; this file remains planning/history authority.

The native dependency graph must equal the exact dependency summary in §1. Body-text dependency lists are descriptive only and do not replace native GitHub dependency metadata.

Task Issue materialization does not itself mean Builder-ready. READY requires native blockers satisfied plus current Task Pack/L3/Execution Pack and required authority/currentness/resource checks.

## 8. Integration posture

Current planning artifacts remain in Draft PR #482 until the planning checkpoint is canonically integrated. After Product/L2/Task DAG and required downstream Task Packs/L3 are stable and planning integration is accepted, establish `version/v4.8.0` from the canonical integration baseline.

Implementation follows one concern per PR targeting `version/v4.8.0`. Stacked PR is allowed only for a real unmerged code-baseline dependency and never substitutes for Issue Dependencies.

## 9. Frozen boundaries carried into every Task

Every Task Pack/Issue/PR MUST preserve:

```text
NEW_DEFAULT_MACHINE_FAMILIES=3
INTERCHANGE=REUSE_EXISTING_V1
CAPABILITY_DOES_NOT_IMPLY_AUTHORITY
CAPABILITY_EVIDENCE_DOES_NOT_IMPLY_CURRENT_VALIDATION_OR_REVIEW
RUNNER_HOST_RESOURCE_FACTS_RETAIN_EXISTING_OWNERS
AVAILABILITY=DERIVED_CURRENT_STATE
HARD_ELIGIBILITY_PRECEDES_OPTIONAL_RANKING
RESOURCE_ADMISSION=ONE_ALL_OR_NONE_COMPOSITE_LINEARIZATION_POINT
INDEPENDENT_PER_KEY_CAS=INSUFFICIENT
TRANSIENT_TRANSPORT_IS_NOT_DURABLE_AUTHORITY
NO_SELF_AMENDING_ADS
ECONOMIC_SAVINGS=NOT_MEASURED_UNLESS_COMPARABLY_MEASURED
BLANKET_STRONG_TO_LOW_COST_RULE=NOT_SUPPORTED
NO_PRIVATE_CHAIN_OF_THOUGHT_REQUIRED
FAST_PATH_REMAINS_PROPORTIONAL
```

A Task that discovers a high-impact Architecture UNKNOWN that would change public contract/durability/failure/authority semantics must stop the affected assumption and re-enter the standard's Architecture Research Demo / amendment path; it may not silently reinterpret this Frozen DAG or L2.
