# v4.9.0 L2 Architecture Evidence — Adaptive Proportional Development Orchestration

Status: **L2 v0.2 REPAIRED SUCCESSOR CANDIDATE — NOT FROZEN; FRESH COMPLETE-DELTA ARCHITECTURE REVIEW REQUIRED**

Frozen Product authority:

- `docs/implementation/4.9.0/PRODUCT_FREEZE.md`;
- Frozen PRD v0.4 blob `a8ec7030a14337a4c2dca853dc474e965679d610`;
- Fresh Product Review #707@5966886681 = PASS;
- Product Freeze Controller #709;
- Product Freeze checkpoint `089555c7911d9fde1ec0bd708c7c77b584d7c305`.

Architecture review lineage:

- L2 v0.1 reviewed by #711@5967289394 on HEAD `540941d06972128865a669e67cec884c6eb41087`, tree `5ecdbd13d7bc01a7e4db5637ed2cf743948ae466`, blob `840b65555b9d98fb5158e2af8571eede78cc811a`;
- #711 verdict = FAIL, `P0=0/P1=4/P2=5/P3=3`;
- #712 is the authoritative finding disposition for F1–F12 and U16–U19.

Reused v4.8 predecessor authority:

```text
V48_FROZEN_PRD_BLOB=f26439580e00de6ed8b2e27d732a3095eb566219
V48_FROZEN_L2_BLOB=f88c85454e80101a0fdf56050e21f11a05279841
```

## 0. Baseline truth and required predecessor owner set

The reviewed planning branch is **not** based on `main@73098dfb576dbcc1252634e14bb3d39b70b94342`; PR #698 was opened from base `9383244abb8172b5ae5135cbd559c72837799375`.

Architecture evidence nevertheless has to account for the sequential predecessor owner set that v4.9 will consume before dependent execution/release:

```text
v4.2 integrated owner set on main@73098df...
  - INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md
  - compatibility-record-v1

v4.3 sequential owner set
  - TASK_DAG_GOVERNANCE_STANDARD.md
  - dag-mutation-record-v1

v4.7 owner/discovery set
  - authority-applicability-entry-v1
  - state-dimension-registry-v1
  - forbidden-inference registry semantics

v4.8 Frozen Product/L2 owner set
  - capability/eligibility/resource selection
  - Dispatch/Claim execution ownership
  - Task Learning Evidence / ADS Evolution path
```

These references are architecture-predecessor authorities, not claims that every predecessor implementation is already present on the v4.9 planning branch. Any v4.9 implementation that depends on a predecessor-owned surface remains non-dispatchable until the required predecessor lineage is integrated and its exact surface is current. There is no generic compatibility-rebind shortcut.

This document is Architecture Evidence only. Task DAG materialization and implementation remain unauthorized until L2 Freeze.

## 1. Architecture decision

v4.9 does **not** create a new assurance-composition owner or a parallel Assurance Resolution family.

The architecture extends the **existing Assurance Plan family** introduced in v4.0 and preserves its ownership of assurance composition and independence-axis semantics. v4.9 adds proof-bound proportional derivation/currentness to that same family, while existing gate owners continue to define the meaning and applicability of Review, Validation, Hidden, Release and other obligations.

The execution shape is:

```text
v4.7 Authority/Applicability registry
        ↓ discover canonical semantic owners
existing Gate Authority precedence chain
        ↓ resolve declarations within each semantic concern
owner-positive reduction predicates + durable/deterministic proofs
        ↓ resolve each concern without model-only downgrade
existing Assurance Plan family (v2 successor)
        ↓ compose concurrently applicable independent obligations
        ↓ preserve Assurance Plan independence + aggregation semantics
existing Execution Architecture reducer/controller
        ├── Task/DAG currentness + v4.3 mutation governance
        ├── JIT legal phase/container selection
        ├── v4.8 hard executor eligibility/resource selection
        ├── Role Execution Profile v1 projection
        └── existing Dispatch → Claim admission
        ↓
role-scoped execution
        ↓
existing gate-owned terminals/evidence
        ↓
ADVERSARIAL_REVIEW finding-union / blocker-dominance
        ↓
merge / candidate / release transitions under existing owners
        ↓
v4.8 Task Learning family successor only where v4.9 fields are needed
```

No second Product/Architecture/Task/DAG/Dispatch/Claim/Review/Validation/Release/Task-Learning lifecycle is introduced. A scheduler daemon remains optional.

## 2. Architecture invariants

1. The v4.7 Authority/Applicability registry discovers canonical owners; v4.9 does not create a second owner-discovery table.
2. Within one semantic concern, existing Gate Authority precedence resolves competing declarations first.
3. Across independently applicable concerns/owners, the Assurance Plan composes resolved obligations monotonically; one concern cannot cancel another independent concern.
4. A reduction-direction decision under v4.9 requires positive permission from the owning authority and current durable/deterministic proof of every reduction predicate.
5. `docs-only`, `risk:low`, file count, provider/model confidence, Fast Path, `recommended+skip`, or similar labels/judgment are never sufficient proof by themselves.
6. Model reasoning may propose classification; model output alone never proves a reduction predicate.
7. Unknown/stale/contradictory/ambiguous proof retains the stronger currently legal obligation or yields `BLOCKED`.
8. Assurance Plan is the single per-subject assurance requirement record family; v4.9 does not create a parallel assurance state machine.
9. Existing Assurance Plan aggregation and `ADVERSARIAL_REVIEW` finding-union/blocker-dominance remain canonical.
10. Unresolved adverse findings carry forward across successor subjects until explicitly dispositioned per finding; subject succession only permits re-review, never erases findings.
11. Assurance Plan currentness is identity/proof/finding-set bound and must be rechecked by every authority-bearing consumer.
12. GitHub Task Issues + native Issue Dependencies remain the canonical live execution DAG after materialization.
13. Any new semantic Task or blocked-by edge is governed by v4.3 DAG mutation authority; JIT container reuse alone cannot invent topology.
14. v4.8 capability/eligibility/resource and Dispatch/Claim semantics remain canonical; Role Execution Profile is a projection of role authority, not a second requirement owner.
15. Evidence transfer remains gate-owned; no generic equivalence engine may transfer PASS.
16. Release applicability remains `RELEASE_STANDARD.md`-owned, per Release gate × subject, and version-level applicability is evaluated fresh on the composed candidate.
17. Migration is prospective; in-flight bound candidates retain already-required gates.
18. Schema/contract evolution is evaluated under v4.2 Interface & Compatibility Governance.
19. P4 stays in the v4.8 Task Learning / ADS Evolution family; no parallel learning database/family/intake.
20. Manual/GitHub-native execution remains conformant; no scheduler daemon, runtime DB or proprietary transport is required.
21. Private chain-of-thought, credentials and Hidden oracle payloads are not required by any new record.

## 3. Canonical owner map

| Concern | Canonical owner | v4.9 role | Must not duplicate |
|---|---|---|---|
| Product scope/acceptance | Frozen PRD / Product Freeze | consume only | lower authority |
| Architecture/Task scope | Frozen L2 / Task DAG / Task Pack | consume/enforce | runtime scope invention |
| owner discovery/applicability | v4.7 Authority/Applicability registry | consume registry entries | second discovery table |
| state dimensions / forbidden inferences | v4.7 State-Dimension registry | register v4.9 dimensions/inferences | parallel state vocabulary |
| Gate Authority precedence | `DEVELOPMENT_WORKFLOW.md` §4 + Stage 2.6 | preserve within-concern precedence | replacement precedence chain |
| Work Item Review/risk metadata | `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` §6 | consume; reduction predicates still need proof under v4.9 | metadata becoming proof |
| assurance composition / independence axes | existing v4.0 Assurance Plan owner + same-family successor | add proof-bound derivation/currentness | new super-owner / parallel resolution family |
| finding aggregation/conflict | existing `ADVERSARIAL_REVIEW.md` semantics | carry unresolved findings forward | latest-PASS-wins reducer |
| workflow/reducer/JIT/Dispatch/Claim | `EXECUTION_ARCHITECTURE_STANDARD.md` | consume Assurance Plan; add legal JIT/currentness checks | second scheduler/claim lifecycle |
| live DAG mutation | v4.3 `TASK_DAG_GOVERNANCE_STANDARD.md` | classify ADD/ADD_DEPENDENCY/etc. | text-only dependency authority |
| Task/Execution Pack authority | `EXECUTION_PACK_STANDARD.md` | explicit legal phase refs + exact-base binding | Product/L2/Task redefinition |
| contract/schema compatibility | v4.2 `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` | govern successor schemas/optional refs | “backward-compatible” by assertion |
| Agent capability/eligibility/resource | frozen v4.8 Execution Architecture + capability families | reuse | Role Profile as capability proof |
| provider-neutral role projection | Execution Architecture + **Role Execution Profile v1** | one new machine family; normalize source authority | Task/independence/claim owner duplication |
| model strength routing | `MODEL_USAGE_POLICY.md` | routing input only | model identity as authority |
| provider-specific role/procedure docs | existing role/handoff docs | procedure/routing references only | provider-specific normative Base Contract |
| Validation truth/currentness | `VALIDATION_STANDARD.md` | consume gate-owned bindings/impact rules | generic PASS transfer |
| Review policy/result | Development Workflow + Work Item + existing Review/Adversarial owners | consume exact-subject/current findings | orchestration-created Review truth |
| Release applicability/candidate/release | `RELEASE_STANDARD.md` | per-gate × subject applicability decision owner | concern decision aggregated to version |
| CI evidence/provider | CI standards | consume only | Validation/Release truth |
| event/operator attribution | `GITHUB_AGENT_INTERACTION_PROTOCOL.md` | additive refs only if owner adopts | second event protocol |
| Task Learning/evolution | v4.8 Task Learning family + existing Evolution Intake | same-family successor if new fields needed | parallel learning family/intake |
| downstream generality evidence | Release authority consumes v4.9 dogfood report | release evidence only | execution authority/self-attestation |

### 3.1 Owner continuity for Assurance Plan

Implementation may promote the historical v4.0 Assurance Plan owner into a stable normative standards path, but that is **owner continuity/canonicalization**, not a new semantic owner. Compatibility aliases must make the predecessor owner and successor owner identity explicit.

`assurance-plan-v1` remains historical/readable. v4.9 uses a versioned successor in the same canonical Assurance Plan family when new proof/currentness fields cannot fit the closed v1 schema.

## 4. Two-layer assurance resolution

### 4.1 Owner discovery

Owner discovery consumes the v4.7 Authority/Applicability registry. A resolver may cache registry data but cannot become its owner.

If a material semantic concern has no current canonical owner entry or applicability cannot be resolved, the affected reduction is not authorized; choose the stronger legal path or `BLOCKED`.

### 4.2 Layer A — within-concern Gate Authority precedence

For one semantic concern, declarations are resolved using the existing authority chain:

```text
Frozen PRD / Contract
> Frozen Architecture
> PROJECT_OVERRIDES
> Task-specific acceptance / risk classification
> Standard defaults
```

This produces one resolved declaration for that concern. A lower declaration does not become a separately conjunctive “owner atom” after it has been superseded by a higher applicable declaration in the same chain.

A higher authority may override a lower default only within the semantic concern it owns. It cannot cancel a different independently applicable concern.

### 4.3 Reduction-direction proof under v4.9

When the resolved declaration selects a weaker path than the unreduced/currently stronger alternative, the reduction must be backed by:

```text
positive owner rule
+ every required predicate
+ current durable fact or owner-accepted deterministic check for each predicate
```

Examples that require proof when used to reduce assurance include:

```text
docs-only
semantic-neutral
mechanically generated
risk:low
Fast Path eligibility
review:not-required
recommended + skipped
release gate NOT_APPLICABLE
evidence reuse / transfer
same-container independence satisfaction
```

Labels, model judgment and human assertion may point to evidence but are not proof unless the owner explicitly accepts the asserted fact form as a deterministic durable fact.

Pinned pre-v4.9 projects retain their prior authority semantics until prospectively migrated; v4.9 does not rewrite historical executions.

### 4.4 Layer B — cross-concern monotonic composition

After Layer A resolves each semantic concern, concurrently applicable independent obligations compose through the existing Assurance Plan family.

- independent domains compose by conjunction/set union;
- where an owner defines an ordered requirement domain, use the owner-defined meet/stricter rule;
- one concern cannot remove another independent concern;
- incomparable/contradictory obligations without an owner-defined resolution yield `BLOCKED_OWNER_CONFLICT`.

`ASSURANCE_FLOOR` is the composed minimum obligation set, not a scalar score. Execution may select above the floor but never below it.

## 5. Assurance Plan same-family successor

### 5.1 Machine-family decision

v4.9 introduces **no new Assurance Resolution family**.

Because `assurance-plan-v1` is closed (`additionalProperties:false`) and lacks the v4.9 derivation/currentness fields, v4.9 should use a versioned successor such as `assurance-plan-v2.schema.json` in the **same Assurance Plan family**, preserving v1 historical readability and the same semantic owner.

The successor retains the v1 concepts:

```text
subject identity
activities[]
  kind / policy / mode / coverage / independence / dependencies
aggregation = finding-union-blocker-dominance
completion predicate
```

and adds a derivation/currentness block, conceptually:

```text
derivation:
  authority_registry_snapshot_ref
  gate_authority_chain_refs[]
  owner_requirement_derivations[]:
    semantic_concern
    canonical_owner_ref
    resolved_declaring_authority_ref
    unreduced_requirement
    reduction_rule_ref?
    predicates[]:
      predicate_id
      proof_state = PROVEN_TRUE | PROVEN_FALSE | UNKNOWN_OR_AMBIGUOUS | STALE | CONTRADICTORY
      proof_refs[]
      deterministic_rule_ref?
    resolved_requirement
  independent_obligation_refs[]
  assurance_floor_digest
  selected_path_ref
  release_applicability_decision_refs[]
  unresolved_finding_set_ref
  unresolved_finding_set_digest
  wait_or_block_reason?
currentness_binding:
  subject_identity_ref
  authority_currentness_refs[]
  proof_currentness_refs[]
  task_pack_execution_pack_refs[]
  release_decision_refs[]
  unresolved_finding_set_digest
supersedes_assurance_plan_ref?
```

The plan records derivation evidence; it does not create Gate PASS, Task scope, Release applicability, or finding-disposition authority.

### 5.2 Assurance Plan currentness key

A plan is current only when all bound dimensions remain current:

```text
subject identity
canonical owner/applicability registry snapshot or equivalent exact owner refs
every authority_currentness_ref
every material reduction proof ref/digest
Task Pack / Execution Pack identity where applicable
Release-owned applicability decisions used by the plan
unresolved adverse-finding set digest
```

A change to any bound dimension makes the plan stale for authority-bearing use. Stale plans remain historical evidence and must be recomputed or explicitly re-evaluated by the owning authority; latest-wins is forbidden.

Authority-bearing consumers MUST verify plan currentness immediately before acting:

```text
Dispatch materialization
Claim admission
merge/merge-ready transition
Candidate Freeze
Release Qualification
other owner-declared irreversible/authority transitions
```

If Dispatch was created from plan P and a new adverse finding arrives before Claim, Claim admission must fail/recompute rather than execute P as current.

## 6. Role Execution Profile v1 — the only new default machine family

Candidate: `schemas/role-execution-profile-v1.schema.json`.

Owner: Execution Architecture, as a normalized projection of existing source authorities.

Purpose: express the Frozen Product provider-neutral Agent Execution Base Contract without turning provider/model identity or v4.8 capability evidence into authority.

Conceptual fields:

```text
schema_version
role_profile_id
role
profile_version
source_authority_refs[]
required_input_refs[]
allowed_actions[]
forbidden_actions[]
required_evidence_refs[]
terminal_authority_ref
eligibility_predicate_refs[]
independence_requirement_refs[]
selector_conflict_policy_ref?
environment_requirement_refs[]
mutation_class = READ_ONLY | MUTABLE | AUTHORITY_TRANSITION
claim_policy_ref
handoff_requirement_refs[]
```

Hard rules:

1. source authorities prevail; Role Profile never overrides them;
2. conflicting source authorities produce `BLOCKED_SOURCE_AUTHORITY_CONFLICT` until owning authority resolves the conflict;
3. `eligibility_predicate_refs[]` feed the frozen v4.8 hard-eligibility resolver as additional hard predicates;
4. independence requirements are referenced from Assurance Plan/Task/Gate owners; Role Profile does not independently mint them;
5. `claim_policy_ref` derives from existing Execution Architecture §11 / Work Item §12.1 rules; there is no free `REQUIRED|NOT_REQUIRED|INHERIT` switch;
6. provider-specific `CODEX_ROLE`, `CHATGPT_WEB_ROLE`, handoff docs and similar artifacts are procedure/routing inputs only when consistent with higher role authority;
7. `MODEL_USAGE_POLICY` owns model-strength routing, not Role authority;
8. Agent Capability Profile/Evidence proves/claims executor capability only and cannot grant actions/terminal authority.

## 7. Compatibility-governed contract evolution

All schema/contract changes are evaluated under v4.2 Interface & Compatibility Governance. “Optional field” or “versioned successor” is not sufficient by assertion; baseline/candidate identity and material compatibility dimensions must be recorded where required.

### 7.1 Assurance Plan

Use same-family `assurance-plan-v2` (or equivalent versioned successor) because v1 is closed. Historical v1 stays valid/readable. Owner continuity and compatibility aliases are explicit.

### 7.2 Dispatch / Execution Pack

If current schemas lack these refs, add optional refs only under compatibility evidence:

```text
assurance_plan_ref?
role_execution_profile_ref?
phase_ref?
selector_independence_basis_ref?
```

No ref changes Dispatch/Claim authority.

### 7.3 Task Learning

Frozen v4.8 `task-learning-v1` is closed. If v4.9 needs new fields, use a versioned successor in the **same Task Learning family**, preserving v1.

Candidate optional successor fields:

```text
execution_friction_class?
recurrence_refs[]?
root_cause_relation? = SAME | RELATED | UNKNOWN | DIFFERENT
prevention_point_refs[]?
recurrence_audit_ref?
ads_evolution_candidate_ref?
```

`execution_friction_class` describes the kind of execution friction. Existing `friction_classification` describes governance/routing disposition (`PROJECT_DEFECT`, `ADS_EVOLUTION_CANDIDATE`, etc.). They are orthogonal; neither replaces the other.

## 8. JIT orchestration, Task-envelope proof and DAG governance

### 8.1 Legal phase predicate

A JIT role/gate phase is inside the current Task envelope only when at least one is true:

```text
A. it is a required/recommended activity in the current Assurance Plan for this Task/subject;
OR
B. it is explicitly declared by current Task Pack / Execution Pack authority;
```

and all are true:

```text
it does not create a new semantic implementation concern;
it does not change Task ownership;
it does not change existing dependency semantics;
it does not widen the Task write/acceptance scope.
```

If those conditions cannot be proven, the runtime cannot classify it as an in-envelope phase.

### 8.2 Container choice vs live DAG mutation

Reusing one existing Issue for sequential phases, or creating a non-blocking subordinate container that does not alter live Task topology, may be execution-container bookkeeping when current authority permits it.

The following are material v4.3 DAG mutations and require the canonical mutation evidence/approving authority before native mutation:

```text
new semantic Task -> ADD
new blocked-by edge -> ADD_DEPENDENCY
remove blocked-by edge -> REMOVE_DEPENDENCY
split/merge/supersede/defer/change lane/integration owner -> corresponding v4.3 mutation class
```

Textual dependency lists never substitute for native Issue Dependencies.

### 8.3 WAITING_LINEAGE

`WAITING_LINEAGE` is a derived projection, not a new canonical Issue state. It applies when any required predecessor-owned surface from the sequential v4.3–v4.8 lineage is not yet integrated/current for dependent execution.

Known-not-ready work remains non-dispatchable. No guaranteed-BLOCKED Builder dispatch is created merely to confirm the known lineage absence.

The v4.7 State-Dimension registry must register the derived dimension/posture and the forbidden inference `WAITING_LINEAGE -> workflow BLOCKED/PASS/FAIL` except where an owning workflow explicitly maps it.

## 9. Adverse findings and successor subjects

Finding aggregation remains owned by existing Assurance Plan / `ADVERSARIAL_REVIEW` semantics.

The reducer keeps a durable unresolved finding set separate from latest verdict chronology.

### 9.1 Carry-forward rule

Stale PASS becomes historical according to the owning gate’s subject-currentness rules. **Unresolved adverse findings do not disappear merely because the subject changed.**

When repair creates successor subject S2, every unresolved predecessor finding relevant to the repair lineage is carried into S2’s review contract until explicitly dispositioned.

A successor Review must consume the carried finding set and emit, per finding:

```text
RESOLVED + evidence refs
STILL_PRESENT + evidence refs
NOT_APPLICABLE_TO_SUCCESSOR + evidence refs + owning-rule basis
```

A finding leaves the unresolved set only through that per-finding verification or an explicit owning-authority finding disposition. Chronology, a new SHA, or a later PASS alone cannot remove it.

### 9.2 Authorized repair / re-review

Subject succession permits re-review only when the successor was produced by an authorized mutable repair path (Task/Execution Pack/repair dispatch or explicit owning-authority repair disposition). This authorization enables a new review subject; it does not clear findings.

Same-subject redispatch merely to obtain PASS is rejected.

## 10. Gate-owned evidence binding/currentness matrix

| Evidence/decision family | Canonical owner | Minimum binding/currentness | v4.9 posture |
|---|---|---|---|
| Assurance Plan successor | Assurance Plan owner | subject + owner registry/authority refs + proof refs + Task/Pack refs + release decisions + unresolved-finding digest | recheck at Dispatch/Claim/merge/Freeze/RQ; drift => stale/recompute |
| concern Validation | `VALIDATION_STANDARD.md` + Frozen Task | tested SHA + profile/scope + environment/toolchain + authority refs | existing `VALIDATION_IMPACT_DECISION` only |
| integration Validation | Validation/Integration owner | source/head + target/base + composed result + profile/environment | explicit impact/composition proof only |
| Review | `DEVELOPMENT_WORKFLOW.md` Stage 2.6 / §4 + Work Item §6 + existing Review/Adversarial owners | exact subject/diff + current authority + required independence + carried unresolved findings | material successor => new/full or complete-delta Review; PASS not transferred |
| Hidden | `RELEASE_STANDARD.md` §4–5 + applicable Hidden authority | frozen candidate + private pack/revision + holder policy | fresh-only on candidate/pack/holder drift unless owner positively states otherwise |
| Closeout/RQ | `RELEASE_STANDARD.md` | frozen candidate + predecessor gate bindings + release authority | fresh-only on candidate drift |
| Release applicability decision | `RELEASE_STANDARD.md` | release gate × subject + Release rule/predicate proof + authority currentness | Release-owned only; concern result never auto-aggregates to version |
| CI evidence | CI evidence owner | exact SHA/run/profile/provider where material | according to CI/Validation owner; never generic PASS transfer |
| Task Learning | v4.8 Task Learning owner | work/subject/evidence refs | historical learning evidence only; never Gate PASS |
| Proportional Dogfood Report | Release authority consuming v4.9 dogfood | exact ADS candidate/version + downstream authority baseline + exercised mechanism refs + auditor identity/evidence | ADS candidate thaw/drift => historical-only until Release owner re-evaluates |

Generic rules:

```text
NO_OWNER_TRANSFER_RULE => HISTORICAL_ONLY
UNKNOWN_BINDING => HISTORICAL_ONLY_OR_BLOCKED
OWNER_FRESH_ONLY => FRESH_EXECUTION_REQUIRED
MATERIAL_BINDING_CHANGE => SUCCESSOR_ASSURANCE_REQUIRED
UNRESOLVED_ADVERSE_FINDING => CARRY_FORWARD_UNTIL_DISPOSITION
```

Path disjointness, unchanged HEAD/tree or ancestry are only possible proof inputs under an owner rule; never transfer authority themselves.

## 11. Release applicability architecture

Release applicability is evaluated **per Release-owned gate × subject**, not as one concern-level “release ceremony” switch.

Candidate Release-owned gates include, as applicable:

```text
Candidate Freeze
Hidden Validation
Final Closeout
Release Qualification
repository integration/final-main sanity where Release owner requires it
```

The Release owner may use a vocabulary equivalent to:

```text
REQUIRED_NOW
DEFERRED_TO_VERSION_CLOSURE
NOT_APPLICABLE
UNKNOWN
```

but the applicability decision record is owned by `RELEASE_STANDARD.md`, not Assurance Plan. Assurance Plan only references the Release-owned decision.

Rules:

- `REQUIRED_NOW`: execute the gate on the current subject/candidate when the Release rule requires it;
- `DEFERRED_TO_VERSION_CLOSURE`: illustrative possible result only; it means the concern does not execute that gate now while the version candidate still owes the gate under Release authority;
- `NOT_APPLICABLE`: requires positive Release-owned permission and proven predicates;
- `UNKNOWN`: stronger legal path or `BLOCKED`;
- version-level applicability is evaluated fresh on the composed Frozen candidate;
- **never** derive version-level `NOT_APPLICABLE` by aggregating concern-level `NOT_APPLICABLE`/`DEFERRED` decisions;
- post-Freeze content change keeps current thaw/invalidate/requalification semantics;
- migration is prospective and cannot shorten already-bound gates.

## 12. v4.8/predecessor lineage behavior

L2/Task planning may reference frozen predecessor authorities before every predecessor implementation is integrated. Dependent execution may not guess future files/schemas/runtime behavior.

Affected work remains `WAITING_LINEAGE` until required predecessor surfaces are integrated/current.

The former generic “compatibility rebind proves equivalent target” escape hatch is removed.

If a project needs to substitute a materially different predecessor surface, that is an Architecture Amendment/currentness decision bound to exact predecessor identities and requires the review/authority appropriate to an L2 amendment before dependent execution.

Before v4.9 Release Qualification:

- required sequential predecessor lineage through v4.8 must be integrated as required by Product;
- frozen v4.8 Product/L2 drift/thaw/supersession triggers v4.9 currentness re-evaluation;
- integrated surface differences from this L2 route to L2 amendment, never silent adaptation.

## 13. P4 recurrence / Task Learning architecture

The recurrence audit is evidence-producing logic around the same canonical v4.8 Task Learning / ADS Evolution path.

Input:

```text
current Task Learning / friction evidence
prior candidate related-evidence refs
owner/version/task context
```

Output, in the same family successor where represented:

```text
execution_friction_class?
relation = SAME | RELATED | UNKNOWN | DIFFERENT
earliest_prevention_point_refs[]
reproduction/counterexample refs[]
recommended existing disposition = NONE_MATERIAL | TASK_CLARIFICATION | ADS_EVOLUTION_CANDIDATE | MORE_EVIDENCE
```

`UNKNOWN` never self-promotes standard change. Promotion still enters ordinary ADS Intake → L1 → PRD → L2 → Task governance.

## 14. Downstream dogfood evidence architecture

No new runtime lifecycle is required. A release-consumable **Proportional Dogfood Report** binds:

```text
exact ADS candidate/version
qualifying downstream repository
pinned Product/Architecture/Task/Review/Validation/Release refs
legal baseline workflow
selected proportional workflow
Assurance Plan refs
mechanism matrix: EXERCISED | NOT_EXERCISED + proof refs
container/dispatch/claim/gate/rebind counts
nonzero baseline-vs-selected delta
ambiguous-predicate exercise + fail-closed result
manual/GitHub-native evidence
independent auditor identity/profile
safety-negative evidence refs
UNAUTHORIZED_GATE_OMISSION=0
STALE_PASS_TRANSFER=0
INDEPENDENCE_LOSS=0
CROSS_OWNER_REQUIREMENT_CANCELLATION=0
ADVERSE_TERMINAL_SUPPRESSION=0
claim boundary for unexercised mechanisms
```

The independent auditor cannot be the orchestrator/Builder principal for the tested decisions. The report is Release evidence; it cannot authorize execution. Baseline=selected with zero proportional delta is compatibility evidence only and cannot satisfy downstream generality.

## 15. Compatibility, migration and manual execution

- older pinned projects remain under their pinned authority until prospective owning-governance migration;
- historical records remain historical truth;
- v4.9 successor schemas must follow v4.2 compatibility governance;
- new refs are optional only where their owning authority allows them;
- manual GitHub-native execution may materialize the same Assurance Plan/Role Profile information and use the existing designated admission writer;
- no scheduler daemon, runtime DB or new transport is required;
- `ai-dev:event:v2` remains the event writer protocol unless its owner adopts a compatible successor;
- v4.8 Capability / Dispatch-Claim / Task Learning families remain the foundation;
- Release applicability defaults to current Release authority until prospective v4.9 Release-owned rules are frozen/applicable.

## 16. Architecture UNKNOWNs and dispositions

| ID | UNKNOWN | Impact | Disposition | Architecture decision |
|---|---|---|---|---|
| U1 | Does proportional assurance need a super-owner? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Existing Assurance Plan remains composition owner. |
| U2 | Can assurance floor be a scalar? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No; resolved concerns + monotonic composition. |
| U3 | Can model output prove reduction? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Durable/deterministic owner-accepted proof only. |
| U4 | Is a parallel Assurance Resolution family needed? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Use same-family Assurance Plan successor. |
| U5 | Does Role Profile duplicate Agent Capability? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No; normalized role projection vs executor capability. |
| U6 | Is a second scheduler/work lifecycle needed? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Existing Task DAG/Execution Architecture/Dispatch-Claim. |
| U7 | Is `WAITING_LINEAGE` a canonical Issue state? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Derived dimension registered via v4.7 registry. |
| U8 | Can generic equivalence override Gate Authority? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Gate-owned transfer only. |
| U9 | Can later PASS erase an adverse finding? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Carry-forward + per-finding disposition. |
| U10 | Does proportional Release applicability remove version closure? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No. Per-gate × subject; version evaluated fresh. |
| U11 | Can migration shorten bound candidate gates? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | No; prospective only. |
| U12 | Does P4 require new learning family/database? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Same-family versioned successor if fields needed. |
| U13 | Must all predecessor implementation already be integrated for planning? | High | `STATIC_EVIDENCE_SUFFICIENT` | No for planning; yes for dependent execution. |
| U14 | Is scheduler daemon/runtime DB required? | High | `STATIC_EVIDENCE_SUFFICIENT` | No. Manual/GitHub-native path. |
| U15 | Is pre-L2 executable Research Demo required? | High | `STATIC_EVIDENCE_SUFFICIENT` | No adopted novel runtime primitive. |
| U16 | Relation to Assurance Plan v1 / Adversarial Review owners? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | Existing owners retained; Assurance Plan same-family successor; aggregation stays existing. |
| U17 | Precedence chain vs conjunction and proof of existing reductions? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | Precedence resolves within concern; conjunction only across independent resolved concerns; v4.9 reductions require proof. |
| U18 | v4.2/v4.3/v4.7 predecessor owners in sequential lineage? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | Explicit owner map + compatibility/DAG/registry integration; waiting until lineage current. |
| U19 | Adverse finding behavior across successor subjects? | Critical | `STATIC_EVIDENCE_SUFFICIENT` | Findings carry forward; successor Review must disposition individually. |

### Research Demo decision

**No executable Research Demo is required before L2 Freeze for this successor candidate.**

All material UNKNOWNs are owner/contract/reducer semantics resolvable from existing durable standards and frozen predecessor authority. No adopted architecture depends on a novel distributed transaction, external service, proprietary queue, or unproven storage primitive.

A later implementation that proposes a novel distributed scheduler/lock/equivalence mechanism beyond these assumptions must create a scoped Research Demo before relying on that mechanism.

## 17. Conformance / negative oracles

At minimum reject:

```text
new v4.9 owner-discovery table -> canonical owner discovery
parallel Assurance Resolution + Assurance Plan disagree -> accept latest
Gate Authority lower default + higher override -> treat both as independent atoms
risk:low/docs-only/model judgment -> reduction PROVEN_TRUE without owner proof
recommended+skip -> legal solely because reviewer chose skip
missing owner/applicability -> assume not applicable
one owner permits skip -> remove independent other-owner gate
Assurance Plan stale on new finding/proof/authority -> Claim/merge continues
new plan -> rewrite old plan
stale PASS -> successor PASS
successor SHA -> predecessor P1 finding dropped without per-finding disposition
R1 FAIL -> R2 PASS erases R1 blocker
same-subject reviewer redispatch -> PASS-shopping
Role Profile -> Task requirements overridden
Role Profile independence refs -> new independence authority
Role Profile claim switch -> bypass existing Claim rule
Agent Capability Profile -> mutation/terminal authority
provider/model name -> Role authority
new blocked-by edge -> no v4.3 DAG mutation evidence
JIT phase not in Assurance Plan/Task Pack -> treated as in-envelope
WAITING_LINEAGE -> canonical Issue state invented
schema optional field -> compatible by assertion without v4.2 governance
no transfer rule -> historical PASS reused
candidate drift -> Hidden/RQ PASS transferred
concern NOT_APPLICABLE aggregate -> version NOT_APPLICABLE
DEFERRED_TO_VERSION_CLOSURE -> version release gate removed
post-Freeze content change -> old candidate remains Frozen
predecessor not integrated -> generic compatibility rebind starts dependent execution
Task Learning v1 closed schema -> silently add fields under v1 identity
execution_friction_class -> replace friction_classification
baseline=selected dogfood -> downstream generality satisfied
orchestrator/Builder self-audit -> independent dogfood audit
transport ACK/cache/state card -> gate/project authority
```

## 18. Positive conformance scenarios

Implementation must eventually prove at least:

1. Authority/Applicability registry resolves the canonical owner for every material reduction concern.
2. Same semantic concern obeys Gate Authority precedence before cross-concern composition.
3. `docs-only`/`risk:low` lower Review path is accepted only with owner-positive deterministic proof under v4.9.
4. Independent obligations compose without cross-owner cancellation.
5. ambiguous reduction proof retains stronger requirement/BLOCKED.
6. Assurance Plan becomes stale when authority/proof/unresolved-finding digest changes; Claim recomputes instead of executing stale plan.
7. new adverse finding after Dispatch prevents Claim until plan/currentness is refreshed.
8. successor Review consumes predecessor unresolved findings and dispositions each one before blocker removal.
9. same-subject reviewer shopping is rejected.
10. Role Profile source conflict blocks; profile hard predicates feed v4.8 eligibility.
11. JIT phase required by Assurance Plan can reuse a container without changing semantic DAG.
12. adding a blocked-by edge produces v4.3 `ADD_DEPENDENCY` evidence and native mutation.
13. Release applicability is decided per gate × subject; concern decisions do not determine version applicability.
14. post-Freeze content change keeps thaw/requalification rules.
15. Task remains `WAITING_LINEAGE` without dispatch until required predecessor surface is integrated/current.
16. Task Learning extension uses same-family successor and preserves v1 historical validity.
17. downstream dogfood produces nonzero legal delta + independent safety audit.
18. all flows remain manually executable through GitHub/durable artifacts without daemon state.

## 19. Expected implementation touchpoints after L2 Freeze

Task DAG should decompose at least:

1. canonicalize existing Assurance Plan semantic owner into stable standards location without changing owner identity;
2. Assurance Plan same-family v2 successor schema + deterministic precedence/proof/composition/currentness rules/tests;
3. v4.7 Authority/Applicability + State-Dimension registry entries/forbidden inferences for v4.9;
4. Execution Architecture integration: plan currentness consumption, legal JIT phase predicate, lineage wait, adverse finding carry-forward;
5. Role Execution Profile v1 schema + source-authority projection + eligibility wiring;
6. Work Item / Execution Pack / Dispatch refs under v4.2 compatibility governance;
7. v4.3 DAG mutation integration for runtime materialization that changes semantic topology;
8. concrete gate-owned evidence binding/currentness integration;
9. Release Standard per-gate × subject applicability decision contract and non-aggregation rule;
10. Task Learning same-family successor for optional v4.9 recurrence/friction fields;
11. Proportional Dogfood Report/checklist + independent auditor contract;
12. deterministic conformance/negative tests covering Product scenarios A–Q and this L2;
13. manual/GitHub-native reference flow and pointer-only task triggers;
14. sequential predecessor-lineage/currentness checks before dependent execution;
15. downstream dogfood + release evidence handoff;
16. closure/docs/manifest compatibility reconciliation.

Exact Task IDs/dependencies/write sets/Review Policies belong to Task DAG after L2 Freeze.

## 20. Local environment posture

`LOCAL_ENV=NOT_REQUIRED` for L2 planning/review/freeze.

No real host/runtime/distributed-service claim is made here. Runtime behavior, integrated predecessor surfaces and downstream dogfood require later exact-subject Validation.

## 21. L2 Freeze gate

This L2 is **NOT FROZEN**.

Before L2 Freeze a genuinely fresh high-capability READ-ONLY Architecture Reviewer must review the exact v0.2 successor candidate and the **complete v0.1→v0.2 semantic delta**, including all #711 F1–F12 repairs.

The review must verify at least:

1. Frozen Product traceability remains intact;
2. existing Assurance Plan / Adversarial Review ownership is preserved;
3. Gate Authority precedence and cross-owner conjunction are deterministic and non-conflicting;
4. every v4.9 reduction path is proof-bound and model-only downgrade is impossible;
5. Assurance Plan currentness closes Dispatch/Claim/merge/Freeze/RQ TOCTOU;
6. adverse findings carry across successors and cannot be reviewer-shopped;
7. v4.2/v4.3/v4.7/v4.8 owner surfaces are consumed without duplication;
8. Role Profile is a projection and feeds v4.8 eligibility without becoming Task/claim/independence authority;
9. Task-envelope/JIT/DAG mutation classification is deterministic;
10. evidence transfer remains gate-owned;
11. Release applicability is per gate × subject with no concern→version aggregation;
12. predecessor lineage has no generic rebind escape;
13. P4 stays in the same Task Learning family;
14. machine-family count is minimal: one new default family (`Role Execution Profile v1`), plus versioned successors/extensions of existing families;
15. U1–U19 dispositions are complete;
16. Research Demo disposition remains justified;
17. P0/P1 = 0 before Freeze.

```text
L2_REVISION=v0.2
L2_STATUS=SUCCESSOR_CANDIDATE_NOT_FROZEN
RESEARCH_DEMO_REQUIRED=NO
TASK_DAG_AUTHORITY=NO
IMPLEMENTATION_AUTHORITY=NO
NEXT=FRESH_COMPLETE_DELTA_ARCHITECTURE_REVIEW
```
