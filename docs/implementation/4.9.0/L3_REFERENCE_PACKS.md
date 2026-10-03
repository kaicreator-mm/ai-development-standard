# v4.9.0 L3 Implementation Reference Packs

Status: **CANDIDATE L3 REFERENCE CHECKPOINT — NOT BUILDER READY**

Authority: Frozen Product #709 / PRD blob `a8ec7030a14337a4c2dca853dc474e965679d610`; Frozen L2 #714 / L2 blob `bd41ea0175b459a6a490fd37ad579e429a58a1c3`; Frozen Task DAG #719 / DAG blob `b9fe0cc7089f64929b4bcf45f7230d950e864db2`; Task Issues #720–#734; Task Packs under `docs/implementation/4.9.0/task-packs/`; native dependency hydration #735 PASS 38/38.

This file is implementation guidance only. Task Packs own scope/write-set/acceptance. JIT Execution Packs own exact-base narrowing. L3 cannot expand Frozen Product/L2/DAG, weaken lineage/currentness, or manufacture Validation/Review/Release truth.

## Shared negative oracles

Reject all of the following across v4.9:

```text
model/provider strength -> normative authority
model judgment or risk label alone -> assurance reduction
one authority owner permission -> cancellation of another owner's requirement
unknown/ambiguous reduction predicate -> lower assurance
historical/stale PASS -> current PASS without owner-defined transfer
new reviewer PASS -> prior adverse finding disappears without explicit successor disposition
Review rerouting -> shopping until PASS
Task dependency completion -> predecessor lineage currentness inherited
lineage/currentness predicate -> fake native Issue dependency edge
WAITING_LINEAGE -> new canonical workflow state
JIT container/phase creation -> semantic DAG scope expansion
runtime topology proposal -> bypass v4.3 DAG governance
registry/discovery metadata -> semantic authority
concern-level Release decision -> version-level Release applicability
compatibility rebind -> retroactive shortening of in-flight release path
Role Profile -> proven Agent Capability
Agent Capability -> role action/terminal authority
Task Learning evidence -> automatic ADS mutation
synthetic dogfood -> real/downstream generality proof
CI PASS -> Review/Validation/Release PASS
private chain-of-thought -> required durable evidence
```

## T-001 — Assurance Plan Owner Canonicalization (#720)

**Tests:** historical v4.0 Assurance Plan owner identity resolves to exactly one canonical owner; `assurance-plan-v1` remains readable; duplicate proportional-assurance owner/family is rejected; existing finding aggregation semantics remain unchanged.

**Contract:** canonicalization/reference migration only. Owner identity and Adversarial Review aggregation authority are preserved; this Task does not own Review/Validation/Release truth, Task scope, capability, or execution lifecycle.

**Implementation:** prefer stable normative owner surface plus explicit historical aliases/references. Keep compatibility additive and deterministic.

**Failure handling:** any need to change aggregation semantics, create a second owner, or reinterpret old records routes to Architecture/Product amendment or owning concern; do not hide it as canonicalization.

**Reference:** Frozen DAG v0.1 `### T-001`; Frozen L2 assurance-owner map; current v4.0 Assurance Plan family.

## T-002 — Assurance Plan v2 Proof / Composition / Currentness Contract (#721)

**Tests:** Gate Authority precedence before cross-owner conjunction; owner-scoped positive reduction permission; proof states for TRUE/FALSE/UNKNOWN; docs-only/risk-low/Fast-Path/recommended-skip/file-count/model judgment cannot independently lower assurance; currentness binds subject/owner/proof/Task Pack/Release decision/unresolved-finding digest; predecessor adverse findings carry forward; stale and ambiguous proofs fail closed.

**Contract:** versioned same-family successor to existing Assurance Plan. It represents assurance floor, selected path, owner permissions and proof/currentness; it does not mint gate PASS or replace owner-specific evidence meaning.

**Implementation:** versioned schema + deterministic fixtures/golden examples + v4.2 compatibility evidence. Prefer explicit refs/digests over copied gate results.

**Failure handling:** missing owner permission/proof/currentness, owner conflict or unknown binding => stronger legal path or BLOCKED/HISTORICAL_ONLY according to owner rules; never optimistic downgrade.

**Reference:** Frozen PRD proportional-assurance sections; Frozen L2 proof/currentness matrix; T-001 canonical owner; v4.2 compatibility governance.

## T-003 — Authority / State Registry Integration (#722)

L3 posture: **bounded**.

**Tests:** one canonical owner/applicability entry per concern; proof/currentness and `WAITING_LINEAGE` projection are discoverable; forbidden inference checks reject registry metadata as authority; no duplicate discovery table.

**Contract:** registry/state integration only; semantic owners remain the underlying v4.0/v4.2/v4.3/v4.7/v4.8/v4.9 owners.

**Implementation:** minimal registry entries and verifier fixtures after exact `LG47_REGISTRY` currentness is proven.

**Failure handling:** ambiguous/duplicate owner discovery blocks admission and routes to registry owner; never last-writer-wins.

**Reference:** v4.7 Authority/Applicability + State-Dimension/Forbidden-Inference registries; Frozen DAG `### T-003`.

## T-004 — Role Execution Profile v1 Contract (#723)

**Tests:** source-authority conflict; role actions/terminal authority; eligibility refs; Claim policy refs; provider/model identity cannot grant authority; Role Profile cannot prove capability; Agent Capability cannot grant role semantics; stale/missing source refs fail closed.

**Contract:** `Role Execution Profile v1` is the only new default machine family. It normalizes role requirements and source-authority projections, but capability/availability/claim/independence owners remain external.

**Implementation:** schema + fixtures + negative-oracle tests. Keep provider-neutral fields and references to v4.8 capability/eligibility/Claim owners rather than copying inventories.

**Failure handling:** source-authority disagreement, missing required ref, or stale `LG42_COMPAT`/`LG48_EXEC` => BLOCKED/WAITING_LINEAGE; no last-writer-wins.

**Reference:** Frozen L2 Role Profile section; v4.8 capability/eligibility/Dispatch/Claim owners; v4.2 compatibility governance.

## T-005 — Release Applicability Owner Contract (#724)

**Tests:** per-gate × subject `REQUIRED_NOW|DEFERRED_TO_VERSION_CLOSURE|NOT_APPLICABLE|UNKNOWN`; no concern→version aggregation; fresh version-level evaluation; prospective migration only; old in-flight candidate cannot be retroactively shortened; UNKNOWN fails closed; thaw/Hidden/Closeout/RQ authority remains unchanged.

**Contract:** Release owner decides applicability; this Task extends existing Release semantics and does not create a parallel release lifecycle or grant concern-level release verdicts.

**Implementation:** minimal normative extension + deterministic positive/negative examples and historical compatibility checks.

**Failure handling:** ambiguous owner/granularity/currentness => stronger existing release path or BLOCKED; never infer NOT_APPLICABLE from low risk or local concern PASS.

**Reference:** `RELEASE_STANDARD.md`; Frozen Product scenarios B/D/J/O; Frozen L2 Release owner matrix.

## T-006 — Task Learning Same-Family Successor (#725)

L3 posture: **bounded**.

**Tests:** v1 records remain valid; optional execution-friction/recurrence/root-cause/prevention refs are backward-compatible; recurrence does not auto-promote ADS change; existing `friction_classification` remains distinct.

**Contract:** same-family successor only if needed; no learning database, new intake lifecycle, private-CoT requirement, or self-amending standard.

**Implementation:** additive schema/fixtures after `LG42_COMPAT` + `LG48_LEARNING` currentness; prefer compact refs/summaries.

**Failure handling:** missing comparable recurrence evidence => NONE_MATERIAL/MORE_EVIDENCE rather than promotion.

**Reference:** v4.8 Task Learning owner/schema; Frozen DAG `### T-006`.

## T-007 — Execution Architecture Proportional Orchestration Core (#726)

**Tests:** Dispatch/Claim currentness TOCTOU; legal JIT phase predicate; lineage wait; hard Role Profile + v4.8 eligibility filters before optional ranking; adverse-finding carry-forward; review-shopping rejection; dependency-ready but lineage-stale cases; recompute on currentness drift; crash/restart reconstruction from durable facts.

**Contract:** single v4.9 semantic owner lane for `EXECUTION_ARCHITECTURE_STANDARD.md`. READY/Dispatch/Claim remain canonical; `WAITING_LINEAGE` is derived; no second scheduler/claim lifecycle/runtime authority store.

**Implementation:** deterministic reducer/state projection over current durable facts; re-check Assurance Plan and exact lineage refs at architecture-owned transitions; JIT only inside Frozen DAG envelope.

**Failure handling:** unknown/stale authority, assurance, lineage, independence or resource fact => no Dispatch/Claim; material topology change routes to T-009/v4.3 governance.

**Reference:** Frozen L2 execution architecture; T-002/T-003/T-004/T-005 contracts; v4.8 execution/claim owners.

## T-008 — Work Item / Execution Pack / Dispatch Reference Wiring (#727)

L3 posture: **bounded**.

**Tests:** old payload compatibility; exact refs round-trip; Claim-time reference consistency; no duplicated Task scope/Claim authority; missing refs fail closed only where owner marks them required.

**Contract:** backward-compatible reference wiring only.

**Implementation:** additive fields + v4.2 compatibility records/tests for every material schema change.

**Failure handling:** incompatible schema change or duplicated authority stops this Task and routes to owning contract/Architecture.

**Reference:** Work Item / Execution Pack / Dispatch schemas; T-007; v4.2 compatibility governance.

## T-009 — JIT DAG Mutation Governance Integration (#728)

L3 posture: **bounded**.

**Tests:** bookkeeping-only JIT vs semantic `ADD|ADD_DEPENDENCY|REMOVE_DEPENDENCY|split|merge|supersede|defer`; native dependency truth; textual lists cannot substitute; stale mutation record; scope-envelope violation.

**Contract:** runtime/JIT proposals are classified and routed through v4.3 Task DAG Governance; no runtime scope invention.

**Implementation:** deterministic classifier + mutation-record references; preserve Frozen planning checkpoint as authority history, not live status table.

**Failure handling:** ambiguous semantic impact => material mutation path or BLOCKED; never silently materialize new topology.

**Reference:** v4.3 Task DAG Governance; Frozen DAG amendment rules.

## T-010 — Gate-Owned Evidence Binding / Currentness Integration (#729)

**Tests:** stale PASS transfer; successor/full/complete-delta Review semantics; carried findings; Validation impact decisions; Hidden/Closeout/RQ exact candidate; Release applicability binding; dogfood candidate binding; owner changes; material subject drift.

**Contract:** cross-owner wiring only. Every gate retains its own evidence meaning and transfer authority; no generic PASS-equivalence engine.

**Implementation:** explicit owner references/currentness predicates and deterministic negative fixtures; reuse existing gate records rather than copying verdicts.

**Failure handling:** no transfer rule => HISTORICAL_ONLY; unknown binding => HISTORICAL_ONLY or BLOCKED; material binding change => successor assurance required.

**Reference:** Frozen L2 evidence/currentness matrix; Review/Validation/Release/Hidden/Closeout/RQ owners.

## T-011 — Registry / Manifest / Adoption Wiring (#730)

L3 posture: **bounded**.

**Tests:** discoverability of Assurance Plan successor, Task Learning successor and Role Execution Profile; exactly one new default family; aliases do not grant authority; older pinned projects remain valid.

**Contract:** central wiring only; semantic owners have already merged before this Task consumes them.

**Implementation:** manifest/registry/index/adoption references in one shared-file lane; avoid sibling semantic edits.

**Failure handling:** owner/family duplication or inconsistent alias blocks integration and routes to owning Task.

**Reference:** Frozen DAG owner-lane rules; v4.7 registries; T-001…T-010 outputs.

## T-012 — Deterministic Proportional-Orchestration Conformance Suite (#731)

**Tests:** Frozen Product scenarios A–Q and all L2 positive/negative oracles, including precedence/conjunction, reduction fail-closed, currentness TOCTOU, adverse findings, selector/independence conflicts, JIT envelope vs mutation, transfer/currentness, Release non-aggregation, lineage waiting, Task Learning compatibility and manual reconstruction.

**Contract:** test-only integrated oracle; it cannot repair sibling semantics or become an owner.

**Implementation:** deterministic fixtures/reference reducers over merged owner outputs; preserve historical fixtures and exact subject identities.

**Failure handling:** semantic failure becomes a finding against the owning Task; do not weaken expected oracle to make suite pass.

**Reference:** Frozen Product A–Q; Frozen L2 oracle matrix; T-002/T-004/T-005/T-006/T-007/T-008/T-009/T-010.

## T-013 — Manual / GitHub-Native Reference Flow (#732)

L3 posture: **not required by default**.

Use existing Task Pack plus merged owner semantics to document pointer-only triggers, currentness/recompute/Claim/adverse-finding/JIT examples and durable-vs-derived facts. This Task may not invent normative semantics. If examples expose a semantic gap, stop and route to the owning Task/DAG amendment. Any Review skip remains current-Assurance-Plan proof-bound.

## T-014 — Proportional Dogfood / Independent Auditor Contract (#733)

**Tests:** exact ADS candidate binding; baseline vs selected path; nonzero proportional mechanism exercise; ambiguous predicate fail-closed; independent auditor eligibility/profile; `UNAUTHORIZED_GATE_OMISSION=0`; `STALE_PASS_TRANSFER=0`; `INDEPENDENCE_LOSS=0`; manual/GitHub-native viability; unexercised mechanism claim boundary.

**Contract:** release-consumable evidence/checklist and auditor contract only; dogfood report cannot authorize execution or Release Qualification.

**Implementation:** structured report/checklist with exact subject, authority basis, comparable counts/reasons where available, decision-value account, safety-negative evidence and explicit `NOT_RUN|BLOCKED` states.

**Failure handling:** no nonzero proportional exercise, auditor independence failure, any safety-negative violation, or missing required real evidence => downstream generality NOT_SATISFIED; synthetic/compatibility-only/no-op runs cannot substitute.

**Reference:** Frozen Product downstream dogfood §16; Frozen L2 dogfood/auditor contract; T-002/T-004/T-005/T-010/T-011.

## T-015 — Integrated Dogfood / Release Evidence Handoff (#734)

**Tests:** full predecessor-lineage exact identity; integrated compatibility/currentness; representative positive/negative orchestration journeys; ADS self-dogfood; qualifying downstream dogfood when required; independent safety audit; registry/docs/contracts/tests reconciliation; full repository verifier/regression.

**Contract:** integrated evidence producer and Version Closure/Release handoff only; does not issue Version Closure or Release Qualification verdict.

**Implementation:** run only on exact integration baseline after all blockers merge and `LG_SEQ_FULL` is current; bind every evidence item to exact candidate/environment/executor and claim strength.

**Failure handling:** mandatory NOT_RUN/BLOCKED, stale lineage/evidence, unsupported generality, safety-negative violation or regression blocks handoff PASS and routes to owning concern/repair. Never guess real-host/downstream PASS.

**Reference:** Frozen Product release/dogfood boundaries; Frozen L2 integration/release evidence; T-011/T-012/T-013/T-014.

## JIT admission rule

No implementation branch or Execution Pack is frozen by this L3 checkpoint. After this Pack/L3 checkpoint receives Fresh Review PASS and canonical planning integration establishes exact `version/v4.9.0`, the Controller must recompute native blockers, `LINEAGE_CURRENTNESS_REFS`, Task Pack/L3 currentness, Assurance Plan, authority/independence/resources and Claim predicates. Only then may a Task become READY and receive a JIT branch/Execution Pack/Dispatch.