# v4.8.0 Task DAG — Evidence-Driven Agent Orchestration & Standard Evolution

Status: **FROZEN TASK DAG R2 — 2026-10-02**

## 0. Authority and repair history

Freeze inputs:

- Frozen Product: `PRODUCT_FREEZE.md` blob `8720264f56a23e352b347dd74df966b9416c9129`;
- Frozen PRD blob: `f26439580e00de6ed8b2e27d732a3095eb566219`;
- Frozen Architecture: `L2_FREEZE.md` blob `f495535b6a16c30b3043fbacedb19cc8be01d541`;
- Frozen L2 blob: `f88c85454e80101a0fdf56050e21f11a05279841`;
- Fresh Independent Architecture Re-Review R3: #502 comment `5927313354` = PASS, P0/P1/P2/P3=0, L2 Freeze authorization YES;
- Task DAG Controller: #504;
- R2 bounded-repair Controller: #647;
- planning baseline: `main@e75fe834469c5ea9f9a384f7d84e38c3a48afa46`;
- intended implementation integration target: `version/v4.8.0`.

Historical DAG R0 was commit `0a4607e857c3971b9eff6092de46f67ba0a698f5`, blob `16ff752ba9c42ee037bb6939c4beb7d235f87cd6`. Controller audit #504 comment `5927557494` found one bounded planning defect before any Task Pack/L3/JIT/Builder dispatch: R0 T-001 combined all three independent new machine-contract families into one Task/PR. R1 repaired only Task granularity and dependency topology. It did **not** change Frozen Product/L2 semantics.

R1 preserved T-002..T-014 stable identities, narrowed T-001 to Task Learning Evidence, and added:

- T-015 — Logical Agent Capability Profile Contract;
- T-016 — Agent Capability Evidence Contract.

That restored one-concern-per-PR for the three new machine families and increased safe root parallelism without creating shared-owner false parallelism.

R2 is a second bounded **DAG decomposition repair** identified by #647 after execution had already begun. Fresh reread of the exact Frozen Product/L2 confirms that auditable execution ownership/start reconstruction, non-authoritative progress/heartbeat, fail-closed restart/replacement behavior and heterogeneous duplicate-assignment dogfood are already within Frozen semantics. R2 therefore does not amend Product or Architecture.

R2 preserves every R1 Task identity T-001..T-016 and every R1 edge, and adds exactly:

- T-017 — Execution Ownership Visibility / Start-Timeout Conformance;
- `T-002 -> T-017`;
- `T-009 -> T-017`;
- `T-017 -> T-011`.

Graph accounting is `17 Tasks / 41 edges`. T-014 remains transitively blocked through T-011; no redundant T-017→T-014 edge is added. R2 does not reopen or reinterpret any completed Task, and it does not retroactively assert that earlier v4.8 executions used the richer T-017 Start Record/profile. On a repair candidate branch this text is the proposed final R2 authority; it becomes canonical only after a genuinely Fresh Independent DAG review PASS, current-target-safe integration into `version/v4.8.0`, and native Issue Dependency materialization/readback.

## 1. Frozen boundaries

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

A Task discovering a high-impact Architecture UNKNOWN that would change public contract, durability, failure, or authority semantics MUST stop the affected assumption and re-enter Architecture Research Demo/amendment. It may not silently reinterpret Frozen Product/L2/DAG authority.

## 2. Exact dependency graph

```text
T-001: []
T-015: []
T-016: []
T-003: [T-015]
T-005: []
T-002: [T-001, T-015, T-016]
T-004: [T-001, T-002]
T-006: [T-001, T-015, T-016, T-002, T-003, T-004, T-005]
T-007: [T-001, T-015, T-016]
T-008: [T-002]
T-009: [T-003]
T-010: [T-004, T-005]
T-017: [T-002, T-009]
T-011: [T-007, T-008, T-009, T-017]
T-012: [T-004, T-007, T-008]
T-013: [T-004, T-005, T-006, T-010]
T-014: [T-006, T-007, T-008, T-009, T-010, T-011, T-012, T-013]
```

Initial roots remain **T-001, T-015, T-016 and T-005**. T-003 becomes READY after T-015 because any compatible Interchange receiver-capability reference must bind the canonical Logical Agent Profile contract rather than inventing an ad-hoc capability shape.

Safe waves are semantic, not merely numeric:

```text
Wave A: T-001, T-015, T-016, T-005
Wave B: T-002, T-003, T-007 (when their exact blockers are satisfied)
Wave C: T-004, T-008, T-009
Wave D: T-006, T-010, T-012, T-017
Wave E: T-011, T-013
Wave F: T-014
```

T-017 may become eligible only after T-002 and T-009. T-011 remains the heterogeneous dogfood join after T-007/T-008/T-009 **and T-017**. Actual dispatch is determined by native GitHub Issue Dependencies plus current Task Pack/L3/Execution Pack/resource/currentness gates. A later wave Task may start as soon as its own blockers are satisfied; waves are a safe upper-bound guide, not a batch barrier.

## 3. Task definitions

### T-001 — Task Learning Evidence Contract

Lane: `contract-learning` · Risk: high · Review Policy: required.

Own only `Task Learning Evidence v1`: schema, focused fixtures/examples and deterministic positive/negative contract tests.

Acceptance:

- exact work/subject/evidence refs and currentness semantics are explicit;
- material rationale is externally useful engineering summary, not private chain-of-thought;
- `TASK_LEARNING=NONE_MATERIAL` Fast Path remains valid;
- stale exact-subject learning cannot become successor truth;
- learning never becomes Product/Architecture/Task/ADR/Incident/Review/Validation authority.

Validation: schema + historical compatibility + negative oracles. Intended branch: `task/v4.8.0-t01-task-learning-contract`.

### T-015 — Logical Agent Capability Profile Contract

Lane: `contract-agent-profile` · Risk: high · Review Policy: required.

Own only `Logical Agent Capability Profile v1`: schema, fixtures/examples and focused conformance.

Acceptance:

- logical Agent/operator/model execution claims only;
- runner/host OS, architecture, toolchain/runtime/device inventory, CPU/memory/disk, network reachability, current capacity and provider concurrency remain references to existing infrastructure owners;
- provider/model identity is provenance, not scalar correctness or routing authority;
- Skill Metadata remains procedure metadata, not capability proof;
- tool/credential possession never grants side-effect authority.

Validation: schema + owner-boundary negatives + v4.6 Skill/runner non-duplication checks. Intended branch: `task/v4.8.0-t15-agent-capability-profile`.

### T-016 — Agent Capability Evidence Contract

Lane: `contract-capability-evidence` · Risk: high · Review Policy: required.

Own only `Agent Capability Evidence v1`: schema, fixtures/examples and focused conformance.

Acceptance:

- evidence is historical/exact-subject and may reference logical Agent + runner/environment identities without copying their ownership;
- positive and negative evidence are first-class;
- historical success never becomes current Availability, Validation or Review PASS;
- evidence strength is layered/bounded, not a global scalar Agent score;
- economic/performance conclusions require actually comparable measured methodology.

Validation: schema + stale/currentness + false-authority negative oracles. Intended branch: `task/v4.8.0-t16-agent-capability-evidence`.

### T-002 — Execution Architecture Core

Lane: `execution-core` · Risk: high · Review Policy: required.

Depends on T-001/T-015/T-016. This Task is the **single v4.8 owner lane** for semantic edits to `EXECUTION_ARCHITECTURE_STANDARD.md` and directly related execution semantics, preventing parallel PRs from competing over the same owner.

Own:

- Task Learning owner/lifecycle semantics;
- logical Agent + runner/environment + derived Availability + Capability Evidence composition;
- `ELIGIBLE | INELIGIBLE | UNKNOWN` derived projection;
- hard filters before optional ranking;
- optional backward-compatible Task/Execution Pack/Dispatch requirement/reference semantics;
- scarce/exclusive/capacity-N resource admission;
- one all-or-none linearization point for work claim + every required resource binding;
- crash/publication ambiguity reconciliation and fail-closed replacement admission.

Acceptance:

- READY/Dispatch/Claim remain canonical;
- no second scheduler lifecycle/database becomes authority;
- independent per-key CAS/leases are insufficient for composite admission;
- capacity-N active accepted bindings never exceed N; exclusive resource is N=1;
- no accepted canonical partial state exists;
- authority/currentness/independence/security/resource predicates are hard filters;
- ranking/cost/latency cannot turn INELIGIBLE/UNKNOWN into ELIGIBLE.

Validation: focused semantic, race/capacity/failure and backward-compatibility validation. High-capability L3/reference required. Intended branch: `task/v4.8.0-t02-execution-core`.

### T-003 — Existing Interchange v1 Profile / Adapter Mapping

Lane: `interchange` · Risk: high · Review Policy: required.

Depends on T-015. First prove whether Frozen v4.8 semantics expose any concrete field/ref gap in the existing v4.0 Interchange family. `NO_CHANGE_REQUIRED` is a valid outcome. If a real gap exists, own only compatible profile/extension/same-family versioning and adapter mapping.

Acceptance:

- no new Agent Exchange normative owner or replacement `agent-exchange-envelope-v1` family;
- `AGENT_INTERCHANGE.md` + `interchange-envelope-v1` remain canonical generic owner/family;
- `ai-dev:event:v2` remains GitHub writer/admission authority;
- ACK/progress is non-authoritative;
- critical semantic effects materialize through existing durable owners;
- duplicate/replay/conflicting payload/currentness/restart reconstruction preserve historical compatibility.

Validation: protocol/schema/event compatibility; exact gap evidence if mutation is proposed. High-capability protocol L3/reference required. Intended branch: `task/v4.8.0-t03-interchange-profile`.

### T-004 — Task Learning Closeout / Template Wiring

Lane: `learning-wiring` · Risk: high · Review Policy: required.

Depends on T-001/T-002. Own closeout/adoption surfaces only: applicable Task Pack, Task Issue, final-closeout, review/checklist and Execution Pack references.

Acceptance: material/NONE_MATERIAL paths explicit; refs over copied bodies; exact-subject learning does not silently rebind; no private chain-of-thought; no owner substitution. Validation: template/reference + closeout conformance. Intended branch: `task/v4.8.0-t04-learning-closeout`.

### T-005 — ADS Evolution Governance / Intake

Lane: `governance` · Risk: high · Review Policy: required.

Root Task. Own classification/promotion governance for PROJECT_DEFECT, AGENT_EXECUTION_DEFECT, ENVIRONMENT_OR_TOOL_DEFECT, PROJECT_SPECIFIC_REQUIREMENT, STANDARD_FRICTION_CANDIDATE and ADS_EVOLUTION_CANDIDATE.

Acceptance: normal ADS Intake→L1→PRD→L2→Task→Review/Validation remains the only promotion path; no telemetry/model/scheduler self-amendment; no universal numeric promotion threshold; v4.5 incident feedback and v4.6 intent/skill owners remain intact; privacy/publication classification explicit. Validation: workflow/classification negative oracles. High-capability governance L3/reference required. Intended branch: `task/v4.8.0-t05-evolution-governance`.

### T-006 — Registry / Discoverability / Adoption Wiring

Lane: `registry-adoption` · Risk: medium/high · Review Policy: required.

Depends on T-001/T-015/T-016/T-002/T-003/T-004/T-005. This is the central shared-file wiring lane.

Own manifest/v4.7 registry discoverability, project-adoption/progressive-disclosure references and migration/adoption notes.

Acceptance: exactly three new machine families discoverable; Interchange represented as reused; registry grants no semantic authority; historical consumers remain valid; Fast Path lightweight; no sibling semantic owner rewrite. Validation: manifest/registry/project-adoption verifier. Intended branch: `task/v4.8.0-t06-registry-adoption`.

### T-007 — Contract / Historical Compatibility Conformance

Lane: `contract-conformance` · Risk: high · Review Policy: required.

Depends on T-001/T-015/T-016. Own integrated compatibility tests across the three separate contract families; do not redefine their schemas.

Negative oracles include capability claim→proven capability, Capability Evidence→current Validation/Review PASS, provider/model→authority, infrastructure facts becoming Logical Agent owner, fourth Availability/Exchange family, stale exact-subject evidence rebound and private chain-of-thought requirement. Historical v4 fixtures/payloads remain valid where Frozen L2 requires it.

Validation: historical/schema compatibility suite. Intended branch: `task/v4.8.0-t07-contract-conformance`.

### T-008 — Eligibility / Composite Resource Admission Conformance

Lane: `scheduling-conformance` · Risk: high · Review Policy: required.

Depends on T-002. Own deterministic tests/reference scenarios for multiple READY Tasks, heterogeneous Agent profiles, stale/fresh Availability, independence conflict, hard-filter-before-ranking, capacity-N contention, N=1 exclusivity, multi-resource composite admission, injected partial-write/crash ambiguity and fail-closed reconciliation.

A novel distributed multi-key CAS/lease mechanism is out of scope unless separately proven through narrow Research Demo/Validation. Validation: race/capacity/crash deterministic validation. Intended branch: `task/v4.8.0-t08-scheduling-conformance`.

### T-009 — Interchange Replay / Restart Conformance

Lane: `interchange-conformance` · Risk: high · Review Policy: required.

Depends on T-003. Own deterministic duplicate/replay/conflict/stale-subject/ACK non-authority/durable materialization/restart tests against existing Interchange reuse and GitHub `ai-dev:event:v2` preservation. Validation: replay/idempotency/restart suite. Intended branch: `task/v4.8.0-t09-interchange-conformance`.

### T-017 — Execution Ownership Visibility / Start-Timeout Conformance

Lane: `execution-ownership-conformance` · Risk: high · Review Policy: required.

Depends on T-002/T-009. Own a bounded conformance concern over the **existing** Dispatch/Claim lifecycle so operator-visible execution ownership and start/terminal/timeout behavior are auditable without creating a second admission authority, event family, scheduler lifecycle or mandatory runtime database.

Owned semantics:

- `NO_CLAIM_NO_EXECUTION`: authoritative execution/source mutation starts only after the applicable Dispatch Claim is accepted; rejected/stale/duplicate Claim means stop/recompute;
- the current accepted `DISPATCH_CLAIMED`/Claim fact is the durable Start Record, not a new authority;
- new-writer/start-profile guidance may expose applicable work/dispatch, role, logical operator/session provenance, accepted/occurrence time, execution profile, exact/base/requested identity, Task/Execution Pack refs and claim/admission generation provenance when supported;
- historical `ai-dev:event:v2` records remain valid and are not retroactively rejected for lacking richer new-writer provenance;
- Issue labels/current-state metadata are visible derived projection (`claimed`/`implementing` or role-equivalent), never the distributed lock;
- terminal FAILED/BLOCKED/CANCELLED/TIMEOUT/STALE/SUPERSEDED/DONE handling leaves no ambiguous incompatible active ownership while preserving append-oriented history;
- same logical operator + same dispatch resume/reclaim is idempotent and does not create a second active claim;
- optional progress/heartbeat stays non-authoritative; missing heartbeat may trigger investigation/timeout policy but cannot itself fabricate Task/Validation failure or authorize unsafe replacement;
- replacement after TIMEOUT/STALE reconciles durable claim/publication/resource facts and fails closed on ambiguity;
- timing/timeout/retry/rebind evidence is descriptive only and must not create unsupported Agent-ranking/economic conclusions.

Required negative oracles include duplicate logical operators racing one work/role with only one canonical accepted start; label/comment without accepted Claim cannot authorize execution; delayed/failed state projection cannot permit duplicate claim; durable operator/session/start/subject reconstruction after chat loss; takeover blocked until durable terminal/stale/timeout/release conditions; heartbeat loss is not Task/Validation FAIL; successor claims after timeout/stale are separately attributable; historical event-v2 compatibility remains intact; Fast Path remains proportional.

Validation: focused Claim/start/projection/release/timeout/restart conformance plus historical compatibility. High-capability Task Pack/risk-scaled L3 required before JIT Builder dispatch. Intended JIT branch after all gates: `task/v4.8.0-t17-execution-ownership`.

If implementation discovers that these requirements need a new lifecycle/event authority, incompatible event-v2 semantics, or a Product/L2 semantic change, stop and route to Architecture amendment/future-major rather than widening T-017.

### T-010 — Task Learning / Evolution Governance Conformance

Lane: `governance-conformance` · Risk: high · Review Policy: required.

Depends on T-004/T-005. Own executable/fixture conformance for NONE_MATERIAL, material learning, stale learning, classification non-promotion, MORE_EVIDENCE/NO_CHANGE, ordinary ADS governance and privacy/hidden-evaluator boundaries. Validation: classification/learning/privacy negative oracles. Intended branch: `task/v4.8.0-t10-governance-conformance`.

### T-011 — Heterogeneous Multi-Agent / Resource / Transport Dogfood

Lane: `orchestration-dogfood` · Risk: high · Review Policy: required.

Depends on T-007/T-008/T-009/T-017. Own the Frozen PRD heterogeneous orchestration dogfood: multiple READY work items, materially different logical Agent profiles, fresh/stale Availability, scarce shared-resource contention, duplicate/incompatible assignment race, reviewer/validator independence conflict, transport duplicate/replay/loss, crash/restart reconstruction, bounded executor success when eligible and escalation on ambiguity.

Synthetic evidence remains labeled synthetic. Real host/device/provider/runtime claims require exact-subject real Validation or remain NOT_RUN/BLOCKED. Evidence matrix/L3 required before dispatch. Intended branch: `task/v4.8.0-t11-orchestration-dogfood`.

### T-012 — #469 Task-Class / Bounded-Agent Dogfood

Lane: `469-dogfood` · Risk: high · Review Policy: required.

Depends on T-004/T-007/T-008. Consume #469 and successor measured evidence as dogfood input, never pre-authorized standard truth.

Own clarification/escalation count, edit/test loops, negative-oracle and contract/write-set drift findings, stale pack/base rebinds, Validation/Review findings/rework and measured resource/time/cost only when actually observed.

Acceptance: `ECONOMIC_SAVINGS=NOT_MEASURED` until comparable measurement; no blanket strong→low-cost rule; provider/model is provenance; Fresh Independent Review remains separate from Builder/Validation; output may be MORE_EVIDENCE/NO_CHANGE/later evidence-backed candidate, not automatic adoption. Risk-scaled L3 + JIT Execution Pack required before bounded/low-cost dispatch. Intended branch: `task/v4.8.0-t12-469-dogfood`.

### T-013 — Cross-Project ADS Evolution Dogfood

Lane: `evolution-dogfood` · Risk: high · Review Policy: required.

Depends on T-004/T-005/T-006/T-010. Own cross-project feedback/evolution falsification with at least two materially distinct Task/project evidence streams when available.

Acceptance covers classification, false-positive prevention, repeated-friction aggregation, privacy/publication boundaries, rejection of project-specific/environment/Agent defects as standard changes, MORE_EVIDENCE/NO_CHANGE and justified ADS_EVOLUTION_CANDIDATE handoff into ordinary ADS Intake. #469 may be one evidence stream but not sole basis for broad economic/performance policy. Evidence matrix/L3 required. Intended branch: `task/v4.8.0-t13-evolution-dogfood`.

### T-014 — Integrated Convergence / Version Closure Inputs

Lane: `integration-closure` · Risk: high · Review Policy: required.

Depends on T-006/T-007/T-008/T-009/T-010/T-011/T-012/T-013. This is the only pre-Closure join. T-017 remains a transitive prerequisite through T-011; no redundant direct T-017 dependency is added.

Acceptance: exactly three new machine families; Interchange reused; owner uniqueness across v4.1–v4.8; hard eligibility-before-ranking and composite atomicity retained; historical compatibility/Fast Path retained; dogfood claims bounded to evidence strength; no unsupported economic/universal routing inference; full repository verifier/regression + required integrated Validation captured. Produces closure inputs only, never Version Closure/Release verdict. High-capability L3/reference + independent integration validator/reviewer required. Intended branch: `task/v4.8.0-t14-integration-closure-inputs`.

## 4. Planning matrix

| Task | Depends On | Parallel | Risk | Executor/model suitability | Required Validation | Review | L3 / Pack posture |
|---|---|---:|---|---|---|---|---|
| T-001 | — | YES | H | high-cap contract designer; bounded builder only from reviewed contract/L3 | schema + compatibility | required | high-cap contract/L3 + Task Pack |
| T-015 | — | YES | H | high-cap capability/owner-boundary designer | schema + owner-boundary | required | high-cap contract/L3 + Task Pack |
| T-016 | — | YES | H | high-cap evidence/currentness designer | schema + stale/false-authority | required | high-cap contract/L3 + Task Pack |
| T-005 | — | YES | H | high-cap governance builder | workflow/classification | required | high-cap governance L3 + Task Pack |
| T-002 | T-001,T-015,T-016 | YES | H | high-cap semantic/concurrency builder | semantics + concurrency/failure | required | high-cap L3 + Task Pack |
| T-003 | T-015 | YES | H | high-cap protocol/owner-boundary builder | protocol/schema/event compatibility | required | high-cap L3 + Task Pack |
| T-007 | T-001,T-015,T-016 | YES | H | bounded test builder + high-cap oracle review | historical/schema compatibility | required | Task Pack; L3 as needed |
| T-004 | T-001,T-002 | YES | H | bounded integration builder after semantic merge | template/closeout | required | Task Pack; focused L3 |
| T-008 | T-002 | YES | H | high-cap concurrency/test builder | race/capacity/crash | required | Task Pack + failure matrix |
| T-009 | T-003 | YES | H | bounded protocol-test builder | replay/restart | required | Task Pack + protocol matrix |
| T-017 | T-002,T-009 | YES | H | high-cap lifecycle/conformance builder | claim/start/projection/release/timeout/restart | required | Task Pack + risk-scaled L3 |
| T-006 | T-001,T-015,T-016,T-002,T-003,T-004,T-005 | YES | M/H | bounded central-wiring builder | manifest/registry/adoption | required | Task Pack |
| T-010 | T-004,T-005 | YES | H | bounded fixture builder + high-cap semantic review | governance/learning/privacy | required | Task Pack |
| T-011 | T-007,T-008,T-009,T-017 | YES | H | heterogeneous Agents + independent validator/reviewer | scenario/real-host as applicable | required | Task Pack + evidence matrix/L3 |
| T-012 | T-004,T-007,T-008 | YES | H | bounded/low-cost where eligible + high-cap independent review | exact Builder/Validation/Review | required | risk-scaled L3 + JIT Execution Pack |
| T-013 | T-004,T-005,T-006,T-010 | YES | H | high-cap evidence/governance owner | cross-project/privacy/currentness | required | Task Pack + evidence matrix/L3 |
| T-014 | T-006,T-007,T-008,T-009,T-010,T-011,T-012,T-013 | NO | H | independent integration validator/reviewer | full integrated regression | required | high-cap L3 + Task Pack |

All implementation PRs target `version/v4.8.0` after canonical planning integration. Task branches are JIT from the then-live exact integration SHA only after native blockers and Task Pack/L3/currentness gates satisfy. Do not pre-create long-lived branches from this planning DAG.

## 5. Review and Validation policy

All seventeen Tasks use `Review Policy=required` as a **v4.8-specific risk decision**, not a global ADS rule. Each Task changes public machine/owner/concurrency/governance semantics, validates high-risk compatibility, or produces evidence consumed by integrated closure.

Validation remains distinct from Review. Builder tests never self-certify real-host, concurrency, cross-transport, privacy or cross-project claims. If the execution environment cannot prove a required external claim, create an exact-subject Validation Request and preserve NOT_RUN/BLOCKED rather than simulating PASS.

For any implementation that selects a novel distributed multi-key CAS/lease/queue mechanism beyond one designated composite single-writer path, insert a narrow Research Demo/Validation dependency before that mechanism may be trusted.

## 6. Native Issue DAG and materialization

Stage 2.5 originally materialized R1 as 16 canonical GitHub Task Issues and 38 native edges. GitHub Issue Dependencies remain the canonical **live execution DAG**; this file remains Frozen planning/history authority.

R2 materialization is an additive bounded delta only:

- canonical T-017 is existing planned Issue #646;
- #646 MUST be blocked by T-002/#510 and T-009/#515;
- T-011/#517 MUST retain T-007/#513 + T-008/#514 + T-009/#515 and additionally be blocked by T-017/#646;
- no R1 edge is removed or rewritten;
- T-014/#520 stays transitively blocked through T-011; no redundant #646→#520 edge is added;
- readback MUST equal 17 Tasks / 41 edges with exactly the three new edges above and no missing/extra/cyclic delta;
- #646 remains `PLANNED / NOT_BUILDER_READY` after native graph materialization until its Task Pack + risk-scaled L3 + currentness + JIT exact-base Execution Pack + canonical Builder Dispatch/Claim gates complete;
- no existing completed Task is reopened or treated as if its historical exact-SHA evidence covered T-017.

R1 historical materialization facts remain valid history: #507 is T-001; #508–#520 retain their assigned T-003/T-005/T-002/T-004/T-006…T-014 identities; #522 is T-015; #524 is T-016; duplicate #523 remains excluded.

READY requires native blockers satisfied plus current Frozen R2 DAG, Task Pack/L3/Execution Pack, exact integration baseline, authority/currentness/resource checks and all role/independence gates.

## 7. Integration posture

R1 planning was already canonically integrated and v4.8 implementation is active on `version/v4.8.0`. This R2 repair is therefore a current-target planning repair, not a replay of the historical Draft PR #482 planning sequence.

The R2 candidate MUST receive a genuinely Fresh Independent planning/DAG review on its exact candidate SHA/tree. Only a PASS candidate may be integrated into the then-current `version/v4.8.0` using current-target-safe procedure. After integration, native Issue Dependencies must be materialized/read back before T-017 becomes canonical for execution and before T-011 may be JIT-dispatched under R2.

Implementation continues one concern per PR. Stacked PR is allowed only for a real unmerged code-baseline dependency and never substitutes for Issue Dependencies.
