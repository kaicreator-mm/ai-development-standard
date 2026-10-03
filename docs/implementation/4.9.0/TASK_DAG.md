# v4.9.0 Task DAG v0.2 — Adaptive Proportional Development Orchestration

Status: **REPAIRED SUCCESSOR CANDIDATE — NOT FROZEN; FRESH COMPLETE-DELTA DAG REVIEW REQUIRED**

## 0. Authority and revision lineage

Frozen authorities:

```text
FROZEN_PRD_BLOB=a8ec7030a14337a4c2dca853dc474e965679d610
PRODUCT_FREEZE=#709
FROZEN_L2_BLOB=bd41ea0175b459a6a490fd37ad579e429a58a1c3
L2_FREEZE=#714
L2_FREEZE_CHECKPOINT=8694a2616e9eb61da9df15fd4a00b0034e368773
```

Predecessor DAG candidate:

```text
TASK_DAG_REVISION=v0.1
TASK_DAG_BLOB=4f358ba2b32e01ae17ddcdf970151cf28e44bb3f
REVIEW=#716@5968275856
VERDICT=FAIL
P0=0
P1=1
P2=0
P3=0
FINDING=F1 INCOMPLETE_PREDECESSOR_LINEAGE_GATING
DISPOSITION=#717
```

The immutable v0.1 snapshot is `task-dag-history/TASK_DAG-v0.1-first-candidate.md`.

v0.2 changes **only** predecessor-lineage/currentness admission semantics required by #716 F1. Task count, Task identities, concern ownership, write-set intent, acceptance semantics, Review Policies, validation ownership, L3 posture, owner lanes and release/dogfood decomposition remain unchanged from v0.1 unless explicitly restated below.

For unchanged per-Task detail, the normative definition is the exact corresponding section of immutable v0.1 plus the v0.2 dependency/lineage/currentness matrix in this document. If any ambiguity exists, the v0.2 matrix controls dispatch/JIT admission while Frozen Product/L2 control semantics.

Implementation remains unauthorized until v0.2 receives Fresh Review PASS, separate DAG Freeze, and Task Pack/Issue materialization.

## 1. Frozen boundaries

All v0.1 Frozen boundaries remain in force, including:

```text
ASSURANCE_OWNER=EXISTING_V4_0_ASSURANCE_PLAN_FAMILY
NO_PARALLEL_ASSURANCE_RESOLUTION_FAMILY
GATE_AUTHORITY_PRECEDENCE_BEFORE_CROSS_OWNER_CONJUNCTION
EVERY_V49_REDUCTION_REQUIRES_POSITIVE_OWNER_PERMISSION_AND_PROOF
UNRESOLVED_ADVERSE_FINDINGS_CARRY_FORWARD
OWNER_DISCOVERY=V47_AUTHORITY_APPLICABILITY_REGISTRY
STATE_REGISTRY=V47_STATE_DIMENSION_REGISTRY
LIVE_DAG_MUTATION=V43_TASK_DAG_GOVERNANCE
SCHEMA_COMPATIBILITY=V42_INTERFACE_COMPATIBILITY_GOVERNANCE
V48_CAPABILITY_ELIGIBILITY_DISPATCH_CLAIM_REUSED
ROLE_EXECUTION_PROFILE_V1=ONLY_NEW_DEFAULT_MACHINE_FAMILY
RELEASE_APPLICABILITY=RELEASE_OWNED_PER_GATE_X_SUBJECT
TASK_LEARNING=V48_SAME_FAMILY_SUCCESSOR_ONLY_IF_NEEDED
WAITING_LINEAGE=DERIVED_NON_DISPATCH_PROJECTION
NO_GENERIC_PREDECESSOR_COMPATIBILITY_REBIND
NO_SECOND_SCHEDULER_OR_CLAIM_LIFECYCLE
MANUAL_GITHUB_NATIVE_PATH_REQUIRED
DOWNSTREAM_DOGFOOD_REQUIRED_BEFORE_RELEASE_GENERALITY
```

## 2. Named predecessor-lineage currentness predicates

External lineage prerequisites are **not Task dependency edges**. They are reconstructible currentness predicates evaluated at Task admission/JIT/Dispatch time.

```text
LG42_COMPAT = current integrated v4.2 Interface & Compatibility Governance owner
              + required compatibility-record/schema surface identities current

LG43_DAG    = current integrated v4.3 Task DAG Governance owner
              + dag-mutation-record/native dependency semantics current

LG47_REGISTRY = current integrated v4.7 Authority/Applicability registry
                + State-Dimension / forbidden-inference registry surfaces current

LG48_EXEC   = current integrated v4.8 execution/capability/eligibility/resource/
              Dispatch-Claim owner surfaces required by the Task

LG48_LEARNING = current integrated v4.8 Task Learning owner/schema surface

LG_SEQ_FULL = every predecessor-owned surface from v4.2 through v4.8 required by
              the integrated v4.9 candidate is current on the applicable lineage
```

A Task Pack/Issue MUST materialize the exact `LINEAGE_CURRENTNESS_REFS` needed for its Task. A predecessor branch/tag name alone is not currentness evidence.

Hard admission rule:

```text
DEPENDENCIES_READY
AND LINEAGE_CURRENTNESS_REFS_CURRENT
AND TASK_PACK_CURRENT
AND ASSURANCE_PLAN_CURRENT
AND RESOURCE/AUTHORITY/INDEPENDENCE_PREDICATES_PASS
=> ELIGIBLE_FOR_JIT_DISPATCH
```

If any required lineage ref is missing, stale, unknown or superseded:

```text
TASK_EXECUTION_POSTURE=WAITING_LINEAGE
DISPATCH=NO
CLAIM=NO
```

Upstream Task completion never proves later predecessor currentness. Every dependent Task re-checks its own lineage refs immediately before JIT branch/Execution Pack creation and again at dispatch admission where current authority requires it.

## 3. Exact Task dependency + lineage matrix

```text
T-001: deps=[]
       lineage=[]

T-002: deps=[T-001]
       lineage=[LG42_COMPAT]

T-003: deps=[T-002]
       lineage=[LG47_REGISTRY]

T-004: deps=[]
       lineage=[LG42_COMPAT, LG48_EXEC]

T-005: deps=[]
       lineage=[]

T-006: deps=[]
       lineage=[LG42_COMPAT, LG48_LEARNING]

T-007: deps=[T-002, T-003, T-004, T-005]
       lineage=[LG42_COMPAT, LG47_REGISTRY, LG48_EXEC]

T-008: deps=[T-007]
       lineage=[LG42_COMPAT, LG48_EXEC]

T-009: deps=[T-007]
       lineage=[LG43_DAG, LG48_EXEC]

T-010: deps=[T-002, T-005, T-007]
       lineage=[LG42_COMPAT, LG48_EXEC]

T-011: deps=[T-003, T-004, T-005, T-006, T-008, T-009, T-010]
       lineage=[LG42_COMPAT, LG43_DAG, LG47_REGISTRY, LG48_EXEC, LG48_LEARNING]

T-012: deps=[T-002, T-004, T-005, T-006, T-007, T-008, T-009, T-010]
       lineage=[LG42_COMPAT, LG43_DAG, LG47_REGISTRY, LG48_EXEC, LG48_LEARNING]

T-013: deps=[T-008, T-010, T-011]
       lineage=[LG_SEQ_FULL]

T-014: deps=[T-002, T-004, T-005, T-010, T-011]
       lineage=[LG42_COMPAT, LG47_REGISTRY, LG48_EXEC]

T-015: deps=[T-011, T-012, T-013, T-014]
       lineage=[LG_SEQ_FULL]
```

This preserves the v0.1 Task dependency graph exactly. Only external lineage predicates are added/expanded.

Semantic roots remain T-001, T-004, T-005 and T-006. A root with unsatisfied lineage is planned work in `WAITING_LINEAGE`; it is not READY-for-dispatch and MUST NOT receive a Builder solely to report the known block.

Informative waves remain:

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

Waves are not barriers. Actual readiness is dependency + lineage + current authority driven.

## 4. Task semantic definitions

The following concern identities and semantics are unchanged from immutable v0.1:

| Task | Concern / owner lane | Review | Validation / L3 | v0.1 normative section |
|---|---|---|---|---|
| T-001 | Assurance Plan Owner Canonicalization | required | normative/static owner conformance / L3 required | `### T-001` |
| T-002 | Assurance Plan v2 Proof / Composition / Currentness Contract | required | schema + deterministic semantics / high-capability L3 | `### T-002` |
| T-003 | Authority / State Registry Integration | required | registry/forbidden-inference / bounded L3 | `### T-003` |
| T-004 | Role Execution Profile v1 Contract | required | schema + owner-boundary / contract L3 | `### T-004` |
| T-005 | Release Applicability Owner Contract | required | Release semantic conformance / high-capability L3 | `### T-005` |
| T-006 | Task Learning Same-Family Successor | required | same-family compatibility / bounded L3 | `### T-006` |
| T-007 | Execution Architecture Proportional Orchestration Core | required | reducer/JIT/currentness/race / semantic-kernel L3 | `### T-007` |
| T-008 | Work Item / Execution Pack / Dispatch Reference Wiring | required | schema/historical compatibility / bounded L3 | `### T-008` |
| T-009 | JIT DAG Mutation Governance Integration | required | mutation classification / bounded L3 | `### T-009` |
| T-010 | Gate-Owned Evidence Binding / Currentness Integration | required | currentness/transfer / high-capability L3 | `### T-010` |
| T-011 | Registry / Manifest / Adoption Wiring | required | registry/manifest/adoption / bounded L3 | `### T-011` |
| T-012 | Deterministic Proportional-Orchestration Conformance Suite | required | deterministic A–Q + L2 oracles / test-oracle L3 | `### T-012` |
| T-013 | Manual / GitHub-Native Reference Flow | recommended | reference/example checks / no L3 by default | `### T-013` |
| T-014 | Proportional Dogfood / Independent Auditor Contract | required | evidence-contract negatives / required L3 | `### T-014` |
| T-015 | Integrated v4.9 Dogfood / Release Evidence Handoff | required | integration/dogfood/closure handoff / required L3 | `### T-015` |

The v0.1 owner/write-set rules remain unchanged:

- T-001→T-002 is the Assurance Plan owner lane;
- T-007 is the only v4.9 semantic lane for `EXECUTION_ARCHITECTURE_STANDARD.md`;
- T-005→T-010→T-014 serializes Release-owner writes when Release surfaces are touched;
- T-011 is the single central registry/manifest/adoption wiring lane;
- T-012 owns integrated conformance; it may prepare disjoint tests in parallel but final tests bind merged owner outputs;
- sibling Tasks may not opportunistically edit another semantic owner lane.

## 5. Lineage materialization contract

Every materialized Task Pack and Task Issue MUST include:

```text
TASK_ID
FROZEN_TASK_DAG_REF
TASK_DEPENDENCY_REFS[]
LINEAGE_CURRENTNESS_REFS[]
LINEAGE_CURRENTNESS_POSTURE=CURRENT|WAITING_LINEAGE|UNKNOWN
LINEAGE_LAST_CHECK_REF
REVIEW_POLICY
VALIDATION_OWNER_REF
L3_REF_OR_POSTURE
IMPLEMENTATION_ADMISSION=NO|READY
```

Rules:

1. `CURRENT` requires exact durable evidence for every named lineage ref.
2. `WAITING_LINEAGE` is derived and non-dispatch; it is not a new canonical Issue workflow state.
3. `UNKNOWN` fails closed exactly like missing currentness for dispatch admission.
4. A dependency becoming DONE does not preserve the dependent Task's lineage currentness.
5. Lineage currentness is re-evaluated before JIT branch/Execution Pack creation.
6. If a lineage ref drifts after branch/pack creation but before Dispatch/Claim, admission re-evaluates and fails closed/rebinds under owner rules.
7. No generic compatibility rebind may substitute a materially different predecessor surface. Such substitution routes to Architecture amendment/currentness governance.
8. Native Task dependency edges remain the canonical live Task topology after materialization; lineage predicates do not become fake blocked-by edges.

## 6. Review / validation / proportional-review posture

The v0.1 Review/Validation/L3 table remains normative. In particular:

- T-001..T-012, T-014 and T-015 remain `review:required`;
- T-013 remains `review:recommended` only, and any actual skip still requires current Assurance Plan owner-positive permission + proven predicates;
- lineage waiting cannot be used to weaken Review or Validation requirements;
- Validation cannot convert missing predecessor lineage into PASS.

## 7. Materialization and JIT policy

After DAG Freeze only:

1. create Task Packs for T-001…T-015 carrying the exact matrix above;
2. materialize Task Issues and native dependency edges for `deps[]` only;
3. record external `LINEAGE_CURRENTNESS_REFS[]` as admission predicates, not Issue dependency edges;
4. materialize waiting Tasks durably if useful, but do not create implementation branches or Builder dispatches while lineage is non-current;
5. create JIT branches/Execution Packs only when dependencies, lineage, Task Pack, Assurance Plan and admission predicates are current;
6. use v4.8 Dispatch/Claim ownership whenever that predecessor surface is current;
7. any execution-time semantic DAG mutation follows v4.3 governance.

## 8. #716 F1 explicit counterexample closure

The following premature-ready paths are now forbidden by exact Task predicates:

```text
T-001 DONE + LG42_COMPAT missing -> T-002 WAITING_LINEAGE, not dispatch-ready
T-002 DONE + LG47_REGISTRY missing -> T-003 WAITING_LINEAGE
T-007 DONE + LG42_COMPAT drift -> T-008 WAITING_LINEAGE
T-007 DONE + LG43_DAG missing -> T-009 WAITING_LINEAGE
T-010 DONE + predecessor drift -> T-011/T-012 re-check their own lineage refs
upstream completion + later predecessor drift -> no inherited stale readiness
T-015 dependencies DONE + any required sequential predecessor missing -> T-015 WAITING_LINEAGE
```

## 9. DAG amendment triggers

The v0.1 amendment rules remain unchanged. New semantic concern, new Task dependency edge, split/merge/supersede/defer, owner-lane transfer, or decomposition contradiction requires explicit v4.3 DAG mutation/planning amendment. Product/Architecture contradictions route upward.

## 10. Successor review/freeze gate

This v0.2 candidate is **NOT FROZEN**.

Before Freeze a fresh independent reviewer must verify:

- v0.1→v0.2 delta is limited to #716 F1 repair and revision bookkeeping;
- Task count/identities/owner lanes/dependency edges/Review Policies are unchanged;
- every direct predecessor consumer has sufficient dispatch-time lineage refs;
- T-011/T-012 do not inherit stale predecessor currentness from completed dependencies;
- lineage predicates do not become fake Task edges or new canonical workflow states;
- Task Pack materialization can reconstruct and re-check the refs;
- Frozen Product/L2 traceability remains intact;
- implementation remains unauthorized before separate Freeze/materialization.

```text
TASK_DAG_REVISION=v0.2
TASK_DAG_STATUS=SUCCESSOR_CANDIDATE_NOT_FROZEN
TASK_COUNT=15
TASK_DAG_AUTHORITY=YES_FOR_PLANNING_ONLY
IMPLEMENTATION_AUTHORITY=NO
NEXT=FRESH_COMPLETE_DELTA_TASK_DAG_REVIEW
```
