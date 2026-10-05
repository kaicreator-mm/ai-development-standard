# v4.10.0 L2 Architecture Evidence — Whole-Project Convergence

Status: **L2 CANDIDATE v0.1 — FRESH INDEPENDENT ARCHITECTURE REVIEW REQUIRED — NOT FROZEN**

Parent planning: `#779`

L2 tracking: `#815`

Frozen Product authority:

```text
PRODUCT_FREEZE=#814
PRD_PATH=docs/implementation/4.10.0/PRD.md
PRD_BLOB=e4c26448acb9a5f88c7f15dc4d023bb9fe0f9e4e
FRESH_PRODUCT_REVIEW=#813@5987814305 PASS
```

Planning baseline: `main@92e4f764a2630a131d3f156b39f0f09064c9849e` / tree `db8cd8185c6206e93512a455a1f9f8b1e121033f`.

Planning independence: per `#779@5987705061`, this L2 and the later Task DAG may be completed without waiting for execution/release/currentness of other versions. Implementation must still rebind to the then-current legal baseline before mutation.

This document is Architecture Evidence only. It does not authorize implementation or an authoritative Task DAG until Fresh Architecture Review + L2 Freeze.

---

## 1. Architecture decision

v4.10 is implemented as **convergence of existing semantic owners**, not as a new orchestration/runtime layer.

The seven Product planes are architectural views over the existing owner graph:

```text
AUTHORITY_AND_INTENT
PLANNING_AND_WORK
COLLABORATION_AND_EXECUTION
EVIDENCE_AND_ASSURANCE
REPOSITORY_AND_COMPATIBILITY
LEARNING_AND_EVOLUTION
PROJECTION_AND_CONFORMANCE
```

They are not seven new standards, services, registries or state machines.

The governing architecture is:

```text
Frozen Product authority
        ↓
current canonical owner discovery
        ↓
owner-local normative hardening
        ├─ workflow / lifecycle
        ├─ task decomposition / DAG
        ├─ execution / dispatch / claim
        ├─ implementation quality / compatibility
        ├─ validation / review / release
        └─ research / learning / adoption
        ↓
additive machine/projection wiring only where needed
        ↓
central manifest / template / prompt / verifier convergence
        ↓
whole-project conformance + self/downstream dogfood
```

No new top-level lifecycle is permitted.

---

## 2. Architecture invariants

1. **One semantic concern → one canonical owner or explicit composition rule.** Projection surfaces never become competing owners.
2. **Durable fact != semantic authority.** GitHub/repository records carry facts/currentness but do not create correctness authority.
3. **Authority != Capability != Authorization.** A capable Agent cannot widen delegated authority.
4. **Evidence != Verdict.** Builder summaries, CI, Validation and Review retain distinct meanings.
5. **Task/PR PASS != Release PASS.** Concern assurance and release assurance remain separate.
6. **Currentness is first-class.** Historical PASS never silently transfers to a changed exact subject.
7. **Human is a first-class actor.** Human judgment/approval/authorization is represented as an explicit control point, not a generic failure fallback.
8. **One Task/DAG/Dispatch/Claim family.** Delegation and handoff enrich existing execution lineage rather than creating nested competing schedulers.
9. **Builder explanation is non-authoritative.** Review navigation may accelerate understanding but cannot self-certify correctness.
10. **Human reviewability is implementation quality.** A green but materially opaque/noisy diff may still be unacceptable for review.
11. **Reuse is semantic, not textual.** Similar code does not automatically justify a shared abstraction.
12. **Shared asset promotion is explicit.** Importability does not imply supported API; Task-local code cannot silently become public/stable authority.
13. **No central component registry by default.** Repository-native module/package/export/architecture/dependency metadata is preferred.
14. **Agent-dispatchable granularity is qualitative.** No universal LOC/file/time/token threshold.
15. **Learning is evidence, not authority.** No execution observation may auto-amend ADS or waive a gate.
16. **Telemetry is advisory.** Cost/latency/estimate-vs-actual data cannot weaken owner-required assurance.
17. **Private chain-of-thought is never a required artifact.** Externalizable rationale and evidence refs are sufficient.
18. **Minimum adoption remains lightweight.** Manual/GitHub-native projects must not require a runtime service/database to conform.
19. **Compatibility and semantic lineage are non-weakening.** Recovered/recomposed trees require their own evidence; version identity is not evidence transfer.
20. **Central wiring is integration, not semantic ownership.** Manifest/templates/verifier work references owner-local decisions rather than redefining them.

---

## 3. Canonical owner composition map

The exact baseline may gain same-family successors before v4.10 implementation begins; Task admission must re-read current owners. The semantic placement below remains authoritative unless L2 is explicitly thawed.

| Product concern | Canonical owner/composition | v4.10 architecture action | Forbidden duplication |
|---|---|---|---|
| Product scope | Frozen v4.10 PRD / Product Freeze | consume only | L2 redefining Product |
| Architecture decisions | `ARCHITECTURE_DESIGN_STANDARD.md` + Frozen L2 | record composition/boundaries | implementation inventing architecture |
| Research modes | `ARCHITECTURE_RESEARCH_DEMO_STANDARD.md` + workflow/research templates | clarify static research vs executable Demo | second Research lifecycle |
| Task decomposition | `TASK_DECOMPOSITION_STANDARD.md` | add Agent-dispatchable/reviewability/reuse-boundary guidance | numeric split policy |
| live DAG mutation | `TASK_DAG_GOVERNANCE_STANDARD.md` | preserve explicit SPLIT/SUPERSEDE/ADD/dependency mutation | hidden DAG mutation |
| Task/Execution Pack | `EXECUTION_PACK_STANDARD.md` | project review/reuse/currentness metadata where material | parallel Task authority |
| lifecycle / gate routing | `DEVELOPMENT_WORKFLOW.md` | reconcile terminal routes/review-repair semantics | second workflow state machine |
| execution / dispatch / claim | `EXECUTION_ARCHITECTURE_STANDARD.md` | add multi-actor responsibility/delegation projection and learning/cost consumption | second scheduler/claim family |
| Agent event/operator attribution | `GITHUB_AGENT_INTERACTION_PROTOCOL.md` | carry parent/causation/handoff refs where needed | second event protocol |
| local/provider procedures | existing role/handoff standards | consume as procedures | provider-specific semantic authority |
| implementation quality | `IMPLEMENTATION_QUALITY_STANDARD.md` | add human-reviewability/shared-asset maintainability baseline | standalone Review Brief authority |
| public/cross-module compatibility | `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` | govern `PUBLIC_STABLE`/deprecation/change impact | custom component compatibility rules |
| Validation truth | `VALIDATION_STANDARD.md` | preserve exact-subject evidence/currentness | Builder/CI manufacturing Validation PASS |
| Review findings/aggregation | current Review/Adversarial Review owner + `review-finding` / `review-aggregation` contracts | converge severity→verdict, successor/delta review and unresolved-finding handling | latest-PASS-wins |
| CI execution/evidence | CI standards | execution evidence only | CI success becoming Review/Release truth |
| release applicability/qualification | `RELEASE_STANDARD.md` | preserve separate release authority | concern PASS aggregated into release PASS |
| owner discovery | `standard-manifest.json#semantic_authorities` + reference convention/registry surfaces | complete/repair current owner discoverability | second owner registry |
| state vocabulary | current state-dimension registry / execution-state family | extend only if a genuinely new dimension is required | duplicate enums in prose/templates |
| Task Learning / evolution | existing Task Learning semantic owner under `EXECUTION_ARCHITECTURE_STANDARD.md` + `task-learning` family | same-family semantic-learning successor/projection | new learning DB/family/intake |
| project adoption | `PROJECT_ADOPTION.md` | make Minimum vs Advanced path explicit/discoverable | mandatory orchestration runtime |
| immutable compatibility | project pin + compatibility governance | preserve exact revision/currentness truth | `main/latest` as authority |

---

## 4. Whole-project authority convergence architecture (R1/R11/R12)

### 4.1 Owner inventory

v4.10 must derive one `OWNER_AUTHORITY_CONVERGENCE_MATRIX` from the repository tree at the implementation baseline.

For every material concern classify:

```text
CONCERN
CANONICAL_OWNER
PROJECTION_SURFACES
MACHINE_CONTRACTS
COMPATIBILITY_ALIASES
LEGACY_SURFACES
STATUS=CURRENT|COMPATIBILITY_ONLY|DEPRECATED|HISTORICAL_ONLY|SUPERSEDED|GAP|CONFLICT
ACTION=KEEP|HARDEN_OWNER|REWIRE_PROJECTION|CLASSIFY_LEGACY|REMOVE_IF_AUTHORIZED|STOP_FOR_DISPOSITION
```

The matrix is planning/implementation evidence, not a new runtime registry. Stable current owner discovery continues through the existing manifest/registry surfaces.

### 4.2 Repair rule

When prose/schema/template/verifier disagree:

1. identify the canonical semantic owner;
2. decide the intended invariant at that owner;
3. repair subordinate projections to match;
4. add deterministic negative coverage where materially useful;
5. do not add another precedence layer solely to hide the contradiction.

### 4.3 Legacy rule

Reachable legacy content must be classified when a fresh Agent could reasonably consume it. Unreachable dead history need not be cosmetically rewritten.

---

## 5. Multi-Agent collaboration architecture (R3)

### 5.1 Preserve the existing dispatch family

Delegation/handoff is represented inside the existing work/dispatch lineage.

Candidate semantic fields, whether stored directly or by refs, are:

```text
parent_work_ref
parent_dispatch_ref
requester_or_delegator
responsibility_owner
executor
responsibility_mode=DELEGATED_SUBWORK|RESPONSIBILITY_HANDOFF
caused_by_event_ref
authority_scope_ref
result_return_ref
```

No child work object may obtain broader effective authority than the intersection of legally delegatable authority, Task/Work authority, role authority and external/project authorization.

### 5.2 Delegation

`DELEGATED_SUBWORK` means the parent/delegator retains responsibility. The child performs a bounded operation and returns evidence/result. It does not become an independent Product/Task owner.

### 5.3 Responsibility handoff

`RESPONSIBILITY_HANDOFF` means active responsibility/control transfers explicitly. The durable handoff identifies the new responsibility owner and the authority scope being transferred.

This is not a second Claim lifecycle; the existing Claim/ownership semantics remain in force.

### 5.4 Typed human participation

Human interaction is projected through existing work/event/handoff mechanisms with explicit semantic type:

```text
INFORMATION_REQUIRED
APPROVAL_REQUIRED
AUTHORITY_DECISION_REQUIRED
AUTHORIZATION_REQUIRED
```

These types describe why the execution cannot legally proceed autonomously; they do not create a new Human workflow state machine.

---

## 6. Human reviewability architecture (R4)

### 6.1 Canonical owner

The implementation-quality invariant belongs to `IMPLEMENTATION_QUALITY_STANDARD.md`.

`TASK_DECOMPOSITION_STANDARD.md` supplies the upstream control: a change that cannot be reviewed coherently may indicate an oversized/mixed concern.

`EXECUTION_PACK_STANDARD.md`, the implementation PR template and Builder terminal may project the same review map. They do not own correctness.

### 6.2 Implementation Review Brief projection

For material changes, project one bounded structure:

```text
INTENT / NON_GOALS
CHANGE_MAP
BEHAVIOR_CHANGE
KEY_INVARIANTS
IMPLEMENTATION_DECISIONS (externalizable rationale only)
REVIEW_HOTSPOTS
DIFF_HYGIENE
EVIDENCE_MAP
KNOWN_LIMITATIONS
REVIEW_ORDER
SHARED_ASSETS_CONSUMED_CREATED_MODIFIED
CONSUMER_IMPACT
```

Storage policy:

- Prefer existing PR / Builder terminal / Execution Pack surfaces.
- Avoid a mandatory standalone document family.
- A machine schema is optional only if deterministic tooling needs it; if introduced it must remain a projection of Implementation Quality / Task authority.

### 6.3 Reviewability blocking

`HUMAN_REVIEWABILITY=BLOCKED` is a review/quality reason, not a new lifecycle state.

Objective signals may include unexplained whole-file rewrite, inseparable generated/semantic churn, unexpected mass comment/doc loss, opaque critical invariants, or multiple independent concerns in one diff.

No universal numeric threshold is allowed.

---

## 7. Shared code asset architecture (R5)

No single new Shared Component owner is created. The concern composes existing owners.

### 7.1 Semantic classification

Use a conceptual classification, not necessarily a mandatory machine enum for every helper:

```text
TASK_LOCAL
MODULE_INTERNAL_SHARED
PROJECT_SHARED
PUBLIC_STABLE
DEPRECATED
```

The classification becomes durable only when material to architecture, compatibility, ownership or review.

### 7.2 Owner composition

```text
Architecture Design
  owns whether a shared component boundary is semantically valid

Implementation Quality
  owns maintainable/supported implementation surface and discoverability expectations

Task Decomposition / DAG
  owns promotion Task, shared-core-first decomposition and consumer/integration topology

Interface Compatibility Governance
  owns externally/cross-module stable contract change/deprecation/migration

Validation / Review
  own exact evidence and independent judgment

Task Learning
  may retain reusable observations but never owns the component contract
```

### 7.3 Agent reuse decision

When materially relevant, the executor selects:

```text
USE_EXISTING
EXTEND_EXISTING
KEEP_LOCAL
PROPOSE_SHARED_COMPONENT
```

`PROPOSE_SHARED_COMPONENT` does not widen current Task authority. Promotion beyond scope requires a bounded architecture/task decision.

### 7.4 Consumer impact

A shared-component mutation must expose known material consumers or a bounded discovery basis, compatibility class, critical invariants, focused component tests and affected-consumer/integration evidence according to risk.

Repository-native dependency/export/package tooling should be used for discovery where available. A central component registry is explicitly out of scope unless future evidence proves it necessary.

---

## 8. Agent-oriented Task granularity architecture (R7)

Extend `TASK_DECOMPOSITION_STANDARD.md` with two additional qualitative questions:

1. Is the concern **Agent-dispatchable** with bounded context/write set and independent exact-subject evidence?
2. Is the concern **human-reviewable** without requiring unrelated sibling implementation to understand it?

Prefer:

```text
contract/shared semantic core
        ↓
parallel independently valid leaves/consumers
        ↓
central integration/conformance
```

only where the boundaries are real.

Task-level and Dispatch-level parallelism remain distinct. Dispatch subdivision cannot fabricate new semantic Tasks or bypass DAG mutation authority.

A large Task is not automatically wrong; when one atomic invariant truly spans a large surface it stays coherent and receives stronger structure/tests/review mapping instead of fake splitting.

---

## 9. Proportional assurance and repair convergence architecture (R6)

### 9.1 Assurance floor

v4.10 does not create a new assurance owner. Existing applicable owners compose the minimum legal assurance floor. Cost, model strength, file count or convenience cannot reduce it.

### 9.2 Repair convergence

Existing Review/Workflow owners should gain bounded operational clarification for:

- severity → verdict behavior where currently ambiguous;
- unresolved P0/P1 dominance;
- P2/P3 disposition without unnecessary full repair cycles when policy permits;
- root-defect-class repair rather than symptom-only patching;
- successor/delta re-review scope when exact-subject/currentness rules permit;
- mechanical/test-harness residual classification;
- non-converging repair-loop escalation to owner/controller adjudication;
- diff-hygiene/transport-capability findings.

Do not define a universal repair-round cap. Repeated loops are a signal for disposition/decomposition, not automatic permission to stop.

### 9.3 Tool/transport eligibility

Executor eligibility may include mutation capability when the Task requires safe line-local/shared-file changes. An executor unable to safely mutate the required surface must route/block rather than compensate with destructive whole-file rewriting.

---

## 10. Execution learning and cost-feedback architecture (R8/R9)

### 10.1 Same-family Task Learning

Semantic execution learning extends the existing Task Learning/Evolution owner only.

Conceptual item types:

```text
DISCOVERY
ERROR_ROOT_CAUSE
ENVIRONMENT_FACT
IMPLEMENTATION_DECISION
PROCESS_FINDING
KNOWLEDGE_CANDIDATE
```

Truth posture:

```text
PROVEN
SUPPORTED
HYPOTHESIS
```

Evidence-bound items reference the exact task/subject/environment/code/test/review facts where applicable.

`HYPOTHESIS` is never authority.

### 10.2 Retention/noise

Do not retain raw chain-of-thought, secrets, full machine inventories, huge command logs or duplicate authoritative content. Prefer references to stable evidence.

`NO_MATERIAL_EXECUTION_LEARNING` is valid.

### 10.3 Promotion

Promotion into durable project/ADS knowledge is an explicit owner decision based on recurrence/reproducibility/materiality. Learning records cannot mutate standards automatically.

### 10.4 Cost feedback

Keep planning estimate and observed execution data non-authoritative:

```text
PLAN (optional/materiality-driven)
- active-time range
- elapsed/wait range
- expected gate shape/cost class
- parallelism/write-collision risk
- confidence

ACTUAL (where trustworthy)
- elapsed timestamps
- active time or UNKNOWN
- gate/CI/dependency wait
- repair count
- estimate-vs-actual class
- unique gate findings/decision change where known
```

Where exact active time is unknowable, record `UNKNOWN`.

The preferred projection is existing Task DAG/Task Pack planning metadata plus Task terminal/Task Learning/version aggregation, not a new telemetry service or gate owner.

---

## 11. Research / standard-self L1 architecture (R10)

Keep one `RESEARCH` family.

Static/source/design research:

```text
may remain inline when small
may become a bounded Issue when independently trackable/cross-session/parallel/decision-bearing
terminal disposition may be ADOPT|ADAPT|DEFER|REJECT|INSUFFICIENT_EVIDENCE
```

Executable Architecture Research Demo is used only when static evidence cannot establish a material architecture fact and a falsifiable executable hypothesis is required.

Standards/protocol/governance products add L1 prompts for owner overlap, internal dogfood/incidents, compatibility/SemVer and weakening/duplicate-authority risk. Ordinary applications load those questions only when applicable.

---

## 12. Projection and conformance architecture (R11/R12)

After owner-local semantics are settled, one central integration concern aligns:

- `standard-manifest.json` / owner discovery;
- state/authority registries as applicable;
- schemas and compatibility/read rules;
- L1/L2/L3 prompts;
- Task/Execution Pack and implementation PR templates;
- review/validation/version-closure checklists;
- project adoption/navigation/reference surfaces;
- verifier/CI deterministic checks;
- golden/reference fixtures and negative examples.

The central concern must not rewrite owner semantics. It verifies/projections them.

A fresh adopter path should be testable from repository entrypoints without private historical knowledge.

---

## 13. Machine-contract posture

v4.10 strongly prefers additive/same-family evolution over new machine families.

### 13.1 Likely same-family changes

Subject to implementation-time currentness:

- dispatch/event/execution projection: optional parent/causation/responsibility/handoff refs if deterministic multi-Agent tooling requires them;
- Task Learning: same-family successor/additive fields for semantic execution learning and evidence/currentness;
- review finding/aggregation: only if current contracts cannot represent required convergence/disposition semantics;
- Task/Execution Pack: optional reviewability/shared-asset/cost metadata where machine consumption is useful.

### 13.2 No required new registry

Do not create:

- component registry;
- human-decision database;
- collaboration scheduler family;
- Review Brief authority/schema solely for documentation convenience;
- cost telemetry database;
- second owner/state registry.

### 13.3 Compatibility

Any machine-contract successor is governed by Interface Compatibility authority. Historical payloads retain original meaning; optional additions must not retroactively make old records invalid without explicit migration authority.

---

## 14. Product requirement → architecture proof map

| PRD requirement | Architecture proof | Primary implementation concern |
|---|---|---|
| R1 owner convergence | Owner matrix + canonical registry projection | C1 |
| R2 lifecycle coherence | workflow/state/dispatch transition audit + negative conformance | C2/C5 |
| R3 Human+Multi-Agent | responsibility/delegation/handoff/attenuation + typed human participation | C2 |
| R4 reviewability | Implementation Quality invariant + Review Brief projections + diff hygiene | C3 |
| R5 shared-code lifecycle | owner-composed classification/reuse/promotion/consumer impact | C3/C4 |
| R6 proportional assurance/repair | existing assurance floor + review/repair convergence | C5 |
| R7 Agent granularity | Task Decomposition + DAG mutation + integration pattern | C4 |
| R8 execution learning | same-family Task Learning successor/projection | C6 |
| R9 cost/process feedback | optional estimate/actual projection + aggregation | C6 |
| R10 research coherence | one Research family + static/Demo applicability | C7 |
| R11 projection alignment | central manifest/template/schema/verifier integration | C7/C8 |
| R12 discoverability/compatibility/lineage | adoption/navigation/legacy classification + compatibility checks | C1/C8 |

---

## 15. Candidate implementation concern decomposition

This is **L2 decomposition input**, not yet the authoritative Task DAG.

### C1 — Authority / owner / legacy convergence

Build whole-project owner and reachable-legacy matrices; repair canonical owner discovery/classification and remove ambiguity without adding another owner registry.

### C2 — Lifecycle + Human/Multi-Agent collaboration convergence

Harden existing workflow/execution/interaction owners for delegation vs responsibility handoff, authority attenuation, typed human participation, causation/responsibility lineage and transition coherence.

### C3 — Human Reviewability + Shared Asset implementation quality

Harden Implementation Quality / compatibility / Builder projections for Review Brief, diff hygiene, supported shared surfaces, producer-consumer-maintainer responsibilities and consumer impact.

### C4 — Task Decomposition / DAG / reuse-promotion granularity

Add Agent-dispatchable + human-reviewable decomposition guidance, contract/shared-core → leaves → integration pattern, explicit promotion boundary and existing DAG mutation composition.

### C5 — Assurance / Review / Repair convergence

Clarify existing review/aggregation/Validation/workflow owner composition, repair convergence, successor/delta re-review, adverse finding carry-forward and executor mutation-capability routing.

### C6 — Execution Learning + Cost Feedback

Extend the existing Task Learning/Evolution path with bounded semantic learning, truth levels/currentness/promotion/noise rules and optional estimate-vs-actual/gate-value projections.

### C7 — Research + L1 + Adoption/Projection hardening

Clarify static research vs executable Demo, standards-self L1 applicability, minimum-vs-advanced adoption and update prompts/templates/checklists/references consistently.

### C8 — Central integration / conformance / dogfood

Wire manifest/registries/schemas/verifier/golden references; run whole-project cross-owner conformance and representative minimum/advanced/multi-Agent/reviewability/shared-component/research dogfood. Owner defects route back to C1–C7 rather than being silently fixed in central wiring.

Directional DAG shape:

```text
C1 ─┐
C2 ─┤
C3 ─┤
C4 ─┼──> C7 where owner projections require settled semantics
C5 ─┤
C6 ─┘

C1..C7 ──> C8 central integration/conformance/dogfood
```

Exact dependencies must be minimized during Task DAG materialization. Conceptual relationship alone is not a dependency.

---

## 16. Write-set / ownership strategy

Task DAG materialization should isolate owner-local semantic files from central wiring.

Expected pattern:

```text
owner-local Tasks:
  standards/<canonical-owner>.md
  owner-specific schemas/references/tests

projection Task(s):
  prompts/templates/checklists/adoption/reference surfaces

central integration:
  standard-manifest.json
  shared registries
  global verifier/golden/conformance suites
```

If one shared file must be touched by many concerns, defer that shared mutation to C8 unless the file is itself the canonical owner for one concern.

One concern / one PR remains preferred.

---

## 17. Validation and review architecture

Each implementation concern should have the smallest strict concern evidence appropriate to its owner.

Examples:

- normative prose + schema: focused semantic/schema negative tests;
- workflow/state: lifecycle transition/forbidden-inference cases;
- Task decomposition: positive/negative DAG/decomposition examples;
- reviewability/shared assets: dogfood fixtures proving both justified reuse and justified keep-local, plus noisy-diff rejection;
- learning: truth/currentness/privacy/noise/promotion negative tests;
- projection: manifest/read-set/template/verifier consistency checks.

C8 owns integrated cross-standard regression and representative end-to-end dogfood. Leaf tasks should not all inherit the full closure suite merely because it exists.

Independent Review remains separate from executable Validation where policy requires it.

---

## 18. Dogfood architecture

At minimum C8 should exercise:

1. minimum/manual ADS bounded maintenance;
2. advanced multi-Agent execution with delegated subwork;
3. explicit human authority decision;
4. reviewable Agent implementation with Review Brief;
5. deliberately noisy/opaque diff rejected or decomposed despite green tests;
6. `USE_EXISTING` shared component path;
7. `EXTEND_EXISTING` with consumer-impact evidence;
8. `KEEP_LOCAL` where abstraction would be wrong;
9. `PROPOSE_SHARED_COMPONENT` routed without scope widening;
10. `NO_MATERIAL_EXECUTION_LEARNING` trivial path;
11. evidence-bound recurring execution learning;
12. static research without Demo;
13. executable Demo escalation when evidence requires it;
14. legitimate Task split and a fake-parallelism negative case;
15. bounded repair/re-review convergence;
16. fresh adopter owner/discoverability navigation.

Dogfood success is evidence for v4.10 implementation/release later; it is not required to freeze this L2 or Task DAG.

---

## 19. Architecture non-goals

v4.10 architecture MUST NOT introduce:

- a generic Agent runtime;
- a second Task/DAG/Dispatch/Claim family;
- a second Review/Validation/Release family;
- a mandatory central scheduler/database;
- a universal shared-component registry;
- automatic DRY/promotion rules;
- universal LOC/file/time/token thresholds;
- raw chain-of-thought capture;
- an automatic learning→standard mutation path;
- cost-based gate waiver;
- provider/model identity as semantic authority;
- historical PASS transfer to a different exact subject;
- other-version execution as a prerequisite for v4.10 Product/L2/Task-DAG planning.

---

## 20. L2 Freeze criteria

L2 may be Frozen when a genuinely Fresh Independent Architecture Review confirms on the exact candidate that:

1. every Product requirement R1–R12 has a legal owner/composition path;
2. no proposed architecture creates a parallel lifecycle/owner family;
3. multi-Agent collaboration uses existing Task/Dispatch/Claim semantics with bounded responsibility/authority lineage;
4. Review Brief remains a non-authoritative projection;
5. shared-code lifecycle composes existing Architecture/Quality/Task/Compatibility owners without central registry or mechanical DRY;
6. Task granularity remains qualitative and uses existing DAG mutation authority;
7. execution learning/cost feedback stay in existing Learning/Evolution paths and cannot waive gates;
8. machine-contract changes are additive/same-family where possible and compatibility-governed;
9. candidate concern decomposition C1–C8 is sufficient to produce a compact Task DAG without reopening Product scope;
10. no unresolved P0/P1 Architecture finding remains.

After L2 Freeze, materialize the authoritative Task DAG from C1–C8 with only real dependencies. Do not begin implementation until Task Packs/L3/JIT admission required by the then-current standard are satisfied.
