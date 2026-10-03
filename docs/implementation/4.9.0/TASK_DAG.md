# v4.9.0 Task DAG — Adaptive Proportional Development Orchestration

Status: **TASK DAG FIRST CANDIDATE — NOT FROZEN; FRESH INDEPENDENT DAG REVIEW REQUIRED**

## 0. Frozen inputs

```text
FROZEN_PRD_REVISION=v0.4
FROZEN_PRD_BLOB=a8ec7030a14337a4c2dca853dc474e965679d610
PRODUCT_FREEZE=#709
FROZEN_L2_REVISION=v0.2
FROZEN_L2_BLOB=bd41ea0175b459a6a490fd37ad579e429a58a1c3
ARCHITECTURE_REVIEW=#713@5967608074 PASS
L2_FREEZE=#714
L2_FREEZE_CHECKPOINT=8694a2616e9eb61da9df15fd4a00b0034e368773
TASK_DAG_PLANNER=#715
```

This DAG is the semantic allowed-work/dependency/ownership/evidence envelope for v4.9 implementation. It is **not** a pre-expanded script of every Builder/Reviewer/Validator phase. Runtime/JIT execution phases remain governed by Frozen L2, current Assurance Plan, Task/Execution Pack authority, native Issue Dependencies and current durable facts.

Implementation remains unauthorized until this DAG is independently reviewed, explicitly frozen, Task Packs are materialized, and executable Issues are admitted.

## 1. Frozen boundaries inherited from Product/L2

Every Task Pack/Issue/PR MUST preserve:

```text
ASSURANCE_OWNER=EXISTING_V4_0_ASSURANCE_PLAN_FAMILY
NO_PARALLEL_ASSURANCE_RESOLUTION_FAMILY
GATE_AUTHORITY_PRECEDENCE_BEFORE_CROSS_OWNER_CONJUNCTION
EVERY_V49_REDUCTION_REQUIRES_POSITIVE_OWNER_PERMISSION_AND_PROOF
MODEL_JUDGMENT_ONLY_CANNOT_LOWER_ASSURANCE
UNRESOLVED_ADVERSE_FINDINGS_CARRY_FORWARD
OWNER_DISCOVERY=V47_AUTHORITY_APPLICABILITY_REGISTRY
STATE_REGISTRY=V47_STATE_DIMENSION_REGISTRY
LIVE_DAG_MUTATION=V43_TASK_DAG_GOVERNANCE
SCHEMA_COMPATIBILITY=V42_INTERFACE_COMPATIBILITY_GOVERNANCE
V48_CAPABILITY_ELIGIBILITY_DISPATCH_CLAIM_REUSED
ROLE_EXECUTION_PROFILE_V1=ONLY_NEW_DEFAULT_MACHINE_FAMILY
RELEASE_APPLICABILITY=RELEASE_OWNED_PER_GATE_X_SUBJECT
CONCERN_RELEASE_DECISIONS_DO_NOT_AGGREGATE_TO_VERSION
NO_GENERIC_PREDECESSOR_COMPATIBILITY_REBIND
TASK_LEARNING=V48_SAME_FAMILY_SUCCESSOR_ONLY_IF_NEEDED
WAITING_LINEAGE=DERIVED_NON_DISPATCH_PROJECTION
NO_SECOND_SCHEDULER_OR_CLAIM_LIFECYCLE
NO_PRIVATE_CHAIN_OF_THOUGHT_REQUIRED
MANUAL_GITHUB_NATIVE_PATH_REQUIRED
DOWNSTREAM_DOGFOOD_REQUIRED_BEFORE_RELEASE_GENERALITY
```

A Task that discovers a material Product/Architecture contradiction MUST stop the affected path and route to Product/L2 amendment/currentness governance. It may not silently redesign these boundaries.

## 2. Exact dependency graph

```text
T-001: []
T-004: [] + LINEAGE_GATE[V4.8 execution owner surfaces current]
T-005: []
T-006: [] + LINEAGE_GATE[V4.8 Task Learning owner surface current]
T-002: [T-001]
T-003: [T-002]
T-007: [T-002, T-003, T-004, T-005] + LINEAGE_GATE[V4.8 execution owner surfaces current]
T-008: [T-007]
T-009: [T-007]
T-010: [T-002, T-005, T-007]
T-011: [T-003, T-004, T-005, T-006, T-008, T-009, T-010]
T-012: [T-002, T-004, T-005, T-006, T-007, T-008, T-009, T-010]
T-013: [T-008, T-010, T-011]
T-014: [T-002, T-004, T-005, T-010, T-011]
T-015: [T-011, T-012, T-013, T-014] + LINEAGE_GATE[required sequential predecessor lineage current]
```

Semantic roots are T-001, T-004, T-005 and T-006. T-004/T-006 may remain `WAITING_LINEAGE` for execution even though they are root concerns in the planning DAG. A lineage gate is not a fake blocked-by Task edge and MUST NOT be represented as a guaranteed-BLOCKED Builder dispatch.

Safe execution waves are informative only:

```text
Wave A: T-001, T-004, T-005, T-006
Wave B: T-002
Wave C: T-003
Wave D: T-007
Wave E: T-008, T-009, T-010
Wave F: T-011, T-012
Wave G: T-013, T-014
Wave H: T-015
```

A later-wave Task may run as soon as its actual Issue Dependencies, lineage gates, Task Pack, current Assurance Plan and resource/currentness predicates are satisfied. Waves are not batch barriers.

## 3. Owner-lane and shared-write discipline

The DAG deliberately serializes shared normative owners:

- Assurance Plan owner lane: T-001 → T-002;
- Execution Architecture owner lane: T-007 is the single semantic owner lane for `EXECUTION_ARCHITECTURE_STANDARD.md` v4.9 changes;
- Release owner lane: T-005 → T-010 → T-014 when Release surfaces are touched;
- central registry/manifest/adoption wiring: T-011 only;
- integrated conformance suite: T-012 only.

Sibling Tasks MUST NOT opportunistically edit another owner lane merely to make local tests pass. Cross-owner defects route to the owning Task or explicit DAG mutation/amendment.

## 4. Task definitions

### T-001 — Assurance Plan Owner Canonicalization

Lane: `assurance-owner` · Risk: high · Review Policy: `review:required` · L3: **required**.

Goal: move/canonicalize the existing v4.0 Assurance Plan semantic owner into a stable normative standards surface **without changing owner identity or aggregation authority**.

Own:
- stable normative Assurance Plan owner document/reference;
- explicit owner continuity to v4.0 `ASSURANCE_PLAN.md`;
- explicit delegation of finding union/blocker dominance to existing Adversarial Review semantics;
- migration/reference notes needed by the v2 successor.

Must not own: Review/Validation/Release gate truth, owner discovery, Task scope, executor capability, or new assurance lifecycle.

Acceptance:
- historical `assurance-plan-v1` remains valid/readable;
- no parallel proportional-assurance owner is created;
- owner continuity is machine/discovery-addressable later by T-011;
- no semantic change to existing finding aggregation.

Validation owner: concern-level static/normative conformance and historical reference checks.

Intended branch: `task/v4.9.0-t01-assurance-owner`.

### T-002 — Assurance Plan v2 Proof / Composition / Currentness Contract

Lane: `assurance-contract` · Risk: critical/high · Review Policy: `review:required` · L3: **required high-capability contract seed**.

Depends on T-001.

Goal: create the versioned **same-family** Assurance Plan successor and deterministic proof/composition/currentness semantics authorized by Frozen L2.

Own:
- `assurance-plan-v2` (or equivalent successor) schema/contract;
- within-concern Gate Authority precedence representation;
- owner-positive reduction predicate proof states;
- cross-owner monotonic composition after concern resolution;
- assurance floor vs selected-path distinction;
- currentness binding over subject/owner/proof/Task-Pack/Release-decision/unresolved-finding digest;
- successor compatibility evidence under v4.2 governance;
- focused deterministic positive/negative contract tests.

Acceptance includes Product scenarios A/C/M and L2 proof/currentness negatives. `docs-only`, `risk:low`, Fast Path, `recommended+skip`, file count or model judgment cannot independently prove a reduction.

Validation owner: schema/compatibility + deterministic semantic contract tests.

Intended branch: `task/v4.9.0-t02-assurance-plan-v2`.

### T-003 — Authority / State Registry Integration

Lane: `authority-registry` · Risk: high · Review Policy: `review:required` · L3: bounded.

Depends on T-002.

Goal: integrate v4.9 semantic concerns with the v4.7 Authority/Applicability and State-Dimension/Forbidden-Inference registries without creating a second discovery table.

Own:
- canonical owner/applicability entries for v4.9 assurance proof/currentness, Role Profile, Release applicability references and other new semantic concerns;
- state-dimension registration for proof/currentness and `WAITING_LINEAGE` derived posture;
- forbidden inferences required by Frozen L2.

Must not change domain-owner semantics or create workflow state.

Validation owner: registry schema/verifier and forbidden-inference conformance.

Intended branch: `task/v4.9.0-t03-authority-state-registry`.

### T-004 — Role Execution Profile v1 Contract

Lane: `role-profile-contract` · Risk: high · Review Policy: `review:required` · L3: **required contract seed**.

External lineage gate: frozen/current v4.8 Agent Capability/eligibility owner surfaces must be available before execution mutation is accepted.

Goal: implement the only new default machine family, `Role Execution Profile v1`.

Own:
- schema + fixtures + contract tests;
- normalized source-authority projection fields;
- source-authority conflict fail-closed rule;
- eligibility predicate refs into v4.8 hard eligibility;
- independence/claim/model-routing references without stealing their authority.

Acceptance:
- Role Profile cannot prove executor capability;
- Agent Capability cannot grant role actions/terminal authority;
- provider/model identity cannot become normative role authority;
- `claim_policy_ref` derives from existing Claim rules;
- source conflicts produce BLOCKED, not last-writer wins.

Validation owner: schema, compatibility, owner-boundary and negative-oracle tests.

Intended branch: `task/v4.9.0-t04-role-execution-profile`.

### T-005 — Release Applicability Owner Contract

Lane: `release-applicability` · Risk: critical/high · Review Policy: `review:required` · L3: **required high-capability governance seed**.

Goal: extend `RELEASE_STANDARD.md` with prospective, Release-owned applicability semantics per gate × subject, without creating a parallel release lifecycle.

Own:
- applicability vocabulary/rules equivalent to `REQUIRED_NOW | DEFERRED_TO_VERSION_CLOSURE | NOT_APPLICABLE | UNKNOWN`;
- Release-owned decision identity/reference posture;
- per-gate × subject granularity;
- fresh version-level evaluation on composed candidate;
- non-aggregation from concern decisions to version result;
- prospective migration/no-retroactive-shortening rule.

Acceptance covers Product B/D/J/O and L2 Release negative oracles. Existing thaw/invalidate/Hidden/Closeout/RQ authority remains intact.

Validation owner: Release semantic conformance + historical compatibility.

Intended branch: `task/v4.9.0-t05-release-applicability`.

### T-006 — Task Learning Same-Family Successor

Lane: `task-learning-contract` · Risk: high · Review Policy: `review:required` · L3: bounded.

External lineage gate: frozen/current v4.8 Task Learning v1 owner surface must be available before mutation.

Goal: add v4.9 recurrence/friction fields only through a versioned successor of the existing Task Learning family when needed.

Own:
- successor schema/compatibility evidence;
- optional `execution_friction_class`, recurrence refs, optional root-cause relation, prevention refs and recurrence-audit refs;
- explicit orthogonality to existing `friction_classification`;
- historical v1 validity.

Must not create learning DB, new intake lifecycle or automatic ADS mutation.

Validation owner: same-family compatibility + routing/authority negatives.

Intended branch: `task/v4.9.0-t06-task-learning-v2`.

### T-007 — Execution Architecture Proportional Orchestration Core

Lane: `execution-core` · Risk: critical/high · Review Policy: `review:required` · L3: **required high-capability semantic kernel**.

Depends on T-002/T-003/T-004/T-005 and v4.8 execution lineage currentness.

This is the **single v4.9 semantic owner lane** for edits to `EXECUTION_ARCHITECTURE_STANDARD.md`.

Own:
- Assurance Plan currentness consumption/recheck at Dispatch, Claim, merge and other architecture-owned transitions;
- legal JIT phase predicate;
- `WAITING_LINEAGE` derived non-dispatch projection;
- Role Profile hard-predicate wiring into v4.8 eligibility;
- unresolved adverse-finding carry-forward/reducer behavior while preserving Adversarial Review aggregation ownership;
- no-review-shopping routing;
- deterministic recompute on currentness drift.

Acceptance covers Product E/F/G/K/L/M/N and L2 currentness/JIT/adverse negatives. No second scheduler/claim lifecycle or runtime authority store.

Validation owner: semantic reducer/dispatch/claim/JIT/currentness tests including race/drift cases.

Intended branch: `task/v4.9.0-t07-execution-core`.

### T-008 — Work Item / Execution Pack / Dispatch Reference Wiring

Lane: `execution-contract-wiring` · Risk: high · Review Policy: `review:required` · L3: bounded.

Depends on T-007.

Goal: add only the refs required to carry Assurance Plan, Role Profile, phase and selector-independence/currentness identity through existing work/pack/dispatch contracts.

Own:
- backward-compatible refs in Work Item/Execution Pack/Dispatch surfaces where proven necessary;
- v4.2 compatibility records/tests for every material schema change;
- claim-time/currentness reference consistency.

Must not duplicate Task scope, Claim authority or gate truth.

Validation owner: schema/historical compatibility + claim binding tests.

Intended branch: `task/v4.9.0-t08-execution-contract-refs`.

### T-009 — JIT DAG Mutation Governance Integration

Lane: `dag-governance` · Risk: high · Review Policy: `review:required` · L3: bounded.

Depends on T-007.

Goal: wire v4.9 JIT materialization to v4.3 Task DAG Governance without turning execution-container bookkeeping into silent topology mutation.

Own:
- deterministic distinction between phase/container bookkeeping and semantic DAG mutation;
- `ADD`, `ADD_DEPENDENCY`, `REMOVE_DEPENDENCY`, split/merge/supersede/defer routing;
- mutation-currentness and native Issue Dependency requirements for v4.9 runtime-originated proposals.

Acceptance: Product L and L2 JIT/DAG negatives; textual dependency lists cannot substitute for native graph facts.

Validation owner: deterministic mutation classification and mutation-record conformance.

Intended branch: `task/v4.9.0-t09-jit-dag-governance`.

### T-010 — Gate-Owned Evidence Binding / Currentness Integration

Lane: `gate-currentness` · Risk: critical/high · Review Policy: `review:required` · L3: **required high-capability owner map**.

Depends on T-002/T-005/T-007.

Goal: make the Frozen L2 evidence/currentness matrix executable through existing owners without a generic PASS-equivalence engine.

Own only cross-owner wiring/explicit owner rules needed for:
- Assurance Plan currentness;
- Review successor/full/complete-delta semantics and carried findings;
- existing Validation impact decision use;
- Hidden/Closeout/RQ fresh/current candidate rules;
- Release applicability decision binding;
- downstream dogfood candidate binding.

Must not mint PASS or replace owner-specific evidence meaning.

Validation owner: currentness/transfer negative oracles, stale-PASS prevention, successor/adverse finding tests.

Intended branch: `task/v4.9.0-t10-gate-currentness`.

### T-011 — Registry / Manifest / Adoption Wiring

Lane: `central-wiring` · Risk: high · Review Policy: `review:required` · L3: bounded.

Depends on T-003/T-004/T-005/T-006/T-008/T-009/T-010.

This is the single central shared-file wiring lane.

Own:
- manifest/registry discoverability;
- compatibility aliases/successor discovery;
- progressive-adoption/migration references;
- documentation index/reference reconciliation;
- exactly-one-new-default-family accounting.

Acceptance:
- Assurance Plan and Task Learning are recognized as same-family successors, not new families;
- `Role Execution Profile v1` is the only new default machine family;
- registry metadata grants no semantic authority;
- older pinned projects remain valid.

Validation owner: manifest/registry/adoption verifiers.

Intended branch: `task/v4.9.0-t11-registry-adoption`.

### T-012 — Deterministic Proportional-Orchestration Conformance Suite

Lane: `integrated-conformance` · Risk: critical/high · Review Policy: `review:required` · L3: required test-oracle review.

Depends on T-002/T-004/T-005/T-006/T-007/T-008/T-009/T-010.

Goal: implement deterministic tests for Frozen Product scenarios A–Q plus L2 positive/negative oracles.

Coverage must include at least:
- precedence vs conjunction;
- reduction proof fail-closed behavior;
- assurance currentness TOCTOU;
- adverse finding carry-forward;
- selector/independence conflicts;
- JIT in-envelope vs DAG mutation;
- gate-owned transfer/currentness;
- Release per-gate applicability/non-aggregation;
- predecessor lineage wait;
- Task Learning same-family compatibility;
- manual-compatible state reconstruction.

Validation owner: clean deterministic suite execution; no runtime claim beyond executed tests.

Intended branch: `task/v4.9.0-t12-conformance-suite`.

### T-013 — Manual / GitHub-Native Reference Flow

Lane: `reference-flow` · Risk: medium · Review Policy: `review:recommended` · L3: not required unless a semantic gap is found.

Depends on T-008/T-010/T-011.

Goal: prove the v4.9 workflow can be executed from durable GitHub/repository facts without scheduler daemon, runtime DB or proprietary transport.

Own:
- pointer-only trigger examples;
- manual currentness/recompute/Claim/adverse-finding/JIT examples;
- concise operator/controller reference flow;
- examples that distinguish durable facts from derived state.

Must not create normative semantics absent from Frozen L2/owner standards.

Validation owner: docs/reference-link and deterministic example checks. Review may be skipped only if the current Assurance Plan positively permits that lower path with proven predicates.

Intended branch: `task/v4.9.0-t13-manual-reference-flow`.

### T-014 — Proportional Dogfood / Independent Auditor Contract

Lane: `dogfood-release-evidence` · Risk: high · Review Policy: `review:required` · L3: required evidence-contract review.

Depends on T-002/T-004/T-005/T-010/T-011.

Goal: define the release-consumable downstream dogfood report/checklist and independent safety-auditor contract from Frozen Product §16 / L2.

Own:
- exact ADS candidate binding;
- legal baseline vs selected workflow accounting;
- mechanism exercise matrix;
- nonzero proportional delta requirement;
- ambiguous predicate fail-closed exercise;
- independent auditor eligibility/profile;
- safety-negative evidence/counts;
- manual/GitHub-native run requirement;
- claim boundary for unexercised mechanisms.

The report is Release evidence only and cannot authorize execution.

Validation owner: report/checklist contract tests and independent-auditor negative oracles.

Intended branch: `task/v4.9.0-t14-dogfood-audit-contract`.

### T-015 — Integrated v4.9 Dogfood / Release Evidence Handoff

Lane: `integration-release-evidence` · Risk: critical/high · Review Policy: `review:required` · L3: required integration plan.

Depends on T-011/T-012/T-013/T-014 and required sequential predecessor lineage currentness.

Goal: integrate the implementation surface, execute representative ADS self-dogfood plus at least one qualifying downstream dogfood path when release evidence is required, and produce version-closure/release handoff evidence.

Own:
- integrated compatibility/currentness validation;
- predecessor-lineage exact identity check;
- representative positive/negative orchestration journeys;
- actual downstream mechanism exercise and independent safety audit where available/required;
- reconciliation of normative docs/contracts/tests/registry;
- release evidence handoff only, not Release Qualification verdict itself.

Acceptance:
- no unsupported generality claim for unexercised mechanisms;
- downstream generality remains NOT_SATISFIED if the qualifying contract is not met;
- all safety negatives remain zero for any run used as generality evidence;
- no stale predecessor/evidence binding is laundered;
- version closure can truthfully consume outputs without converting NOT_RUN/BLOCKED into PASS.

Validation owner: integration + exact-subject dogfood + closure handoff. Real external/downstream inability is BLOCKED/NOT_RUN, never guessed PASS.

Intended branch: `task/v4.9.0-t15-integrated-dogfood`.

## 5. Review / validation policy summary

| Task | Risk | Review | Validation ownership | L3 |
|---|---|---|---|---|
| T-001 | high | required | normative/static owner conformance | required |
| T-002 | critical/high | required | schema + deterministic semantics | required |
| T-003 | high | required | registry/forbidden inference | bounded |
| T-004 | high | required | schema + owner boundary | required |
| T-005 | critical/high | required | Release semantic conformance | required |
| T-006 | high | required | same-family compatibility | bounded |
| T-007 | critical/high | required | reducer/JIT/currentness/race | required |
| T-008 | high | required | schema/historical compatibility | bounded |
| T-009 | high | required | DAG mutation classification | bounded |
| T-010 | critical/high | required | evidence currentness/transfer | required |
| T-011 | high | required | registry/manifest/adoption | bounded |
| T-012 | critical/high | required | deterministic conformance suite | required |
| T-013 | medium | recommended | reference/example checks | not-required by default |
| T-014 | high | required | dogfood/auditor contract | required |
| T-015 | critical/high | required | integration/dogfood/closure handoff | required |

`review:recommended` does not mean silently skipped. Any actual skip must be resolved under the current v4.9 Assurance Plan with positive owner permission and proven reduction predicates.

## 6. Task Pack / Issue materialization policy

After DAG Freeze:

1. create Task Packs for the semantic Tasks above;
2. materialize Task Issues + native Issue Dependencies as the canonical live execution DAG;
3. do not create implementation branches before a Task becomes actually READY;
4. lineage-gated Tasks remain represented as planned/waiting durable work and MUST NOT receive Builder dispatch merely to return BLOCKED;
5. create JIT branches/Execution Packs only after dependencies + lineage + current assurance predicates are satisfied;
6. every accepted execution must follow v4.8 Dispatch/Claim ownership when the required predecessor surface is current;
7. execution-time material DAG changes use v4.3 mutation governance rather than editing this frozen planning checkpoint as a live status table.

## 7. Parallelism and collision rules

Safe parallel roots do not imply simultaneous writes to shared central files. T-011 is the central wiring lane and must consume completed owner contracts rather than cherry-picking sibling semantics.

T-012 may prepare independent tests in parallel with T-011 only when its write set does not collide with central registry/manifest surfaces. Final integrated conformance must bind the actual merged owner outputs.

T-013/T-014 may begin after their dependencies independently; neither is a version-closeout barrier until T-015.

## 8. DAG amendment triggers

Use explicit v4.3 DAG mutation/planning amendment when any of the following becomes necessary:

- a new semantic concern not represented by T-001…T-015;
- a new blocked-by relationship;
- split/merge/supersede/defer of a Task identity;
- owner-lane collision requiring responsibility transfer;
- implementation evidence shows Frozen L2 decomposition is materially wrong.

Architecture/Product contradictions route upward rather than being hidden in a DAG mutation.

## 9. Task DAG review/freeze gate

This candidate is **NOT FROZEN**.

Before Task DAG Freeze, a fresh independent high-capability reviewer must verify at least:

- complete traceability to Frozen Product v0.4 and Frozen L2 v0.2;
- all L2 implementation touchpoints are covered exactly once or intentionally composed;
- no parallel owner/family is reintroduced;
- shared-owner lanes prevent sibling PR races;
- dependency graph is acyclic, sufficient and not over-serialized;
- external lineage gates are not misrepresented as fake Task edges or guaranteed-BLOCKED dispatches;
- one-concern-per-PR remains feasible;
- Review Policy/validation/L3 posture is proportional but cannot bypass Frozen authority;
- Release/dogfood/manual paths are represented;
- Task scope is an envelope, not a runtime phase script;
- no implementation authority is implied before Task Pack/Issue materialization.

```text
TASK_DAG_STATUS=CANDIDATE_NOT_FROZEN
TASK_COUNT=15
TASK_DAG_AUTHORITY=YES_FOR_PLANNING_ONLY
IMPLEMENTATION_AUTHORITY=NO
NEXT=FRESH_TASK_DAG_REVIEW
```
