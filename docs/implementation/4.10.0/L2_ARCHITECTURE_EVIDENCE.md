# v4.10.0 L2 Architecture Evidence — Successor Whole-Project Convergence

Status: **L2 SUCCESSOR CANDIDATE v0.2 — FRESH INDEPENDENT ARCHITECTURE REVIEW REQUIRED — NOT FROZEN**

Parent planning: `#779`

Successor L2 tracking: `#838`

Historical L2 tracking: `#815` — v0.1 only; stale after Product thaw.

Current Frozen Product authority:

```text
PRODUCT_REFREEZE=#837
PRD_PATH=docs/implementation/4.10.0/PRD.md
PRD_REVISION=v0.4
PRD_BLOB=b0b9906035eee253aad4bff0274d3d4c8f90b9db
FRESH_PRODUCT_REVIEW=#833@5993569646 PASS
```

Planning baseline remains the v4.10 planning baseline `main@92e4f764a2630a131d3f156b39f0f09064c9849e`; implementation admission MUST later re-read then-current canonical owners and legal integration baseline before mutation.

Planning independence: per `#779@5987705061`, v4.10 Product/L2/Task-DAG planning does not wait for execution/release currentness of other versions. This does not permit implementation against stale owners.

This document is Architecture Evidence only. It does not authorize L2 Freeze, Task DAG authority, implementation, Release Qualification or merge until a genuinely Fresh Independent Architecture Review passes on this exact successor subject and Controller records L2 Freeze.

---

## 1. Architecture decision

v4.10 is implemented as **convergence and composition of existing semantic owners**, with the smallest additive hardening needed to make the Frozen Product v0.4 truthful end-to-end.

The architecture MUST NOT introduce a new orchestration platform, Product-review state machine, Human workflow state machine, component registry, learning database, telemetry authority, Release state machine or parallel Task/DAG/Dispatch/Claim family.

The seven Product planes remain architectural views over one owner graph:

```text
AUTHORITY_AND_INTENT
PLANNING_AND_WORK
COLLABORATION_AND_EXECUTION
EVIDENCE_AND_ASSURANCE
REPOSITORY_AND_COMPATIBILITY
LEARNING_AND_EVOLUTION
PROJECTION_AND_CONFORMANCE
```

They are not seven new standards/services/registries.

The governing composition is:

```text
Frozen Product v0.4
        ↓
current canonical owner discovery
        ↓
owner-local semantic hardening
        ├─ Product discovery / lifecycle routing
        ├─ Architecture / research
        ├─ Task decomposition / DAG
        ├─ Dispatch / Claim / human decision
        ├─ implementation quality / compatibility
        ├─ Validation / Review / repair
        ├─ Release / Closure
        └─ optional Task Learning / cost feedback
        ↓
projection + machine-contract updates only where determinism needs them
        ↓
central manifest/template/prompt/verifier convergence
        ↓
requirement-linked Product acceptance + whole-project dogfood
```

The architecture is successful only if Minimum ADS remains usable without a reducer/controller runtime while Advanced ADS can automate the same semantics.

---

## 2. Frozen Product drivers and architecture invariants

### 2.1 Active Product drivers

The active Product requirement set is exactly:

```text
R1  Product discovery lifecycle coherence
R2  Whole-project owner/lifecycle convergence
R3  Human + Multi-Agent collaboration clarity
R4  Human controllability + automation-first quality
R6  Proportional assurance and convergent repair
R7  Agent-oriented granularity
R11 Projection/conformance alignment
R12 Discoverability / compatibility / lineage
```

Subordinate Product dispositions that architecture MUST preserve:

```text
R5  = EXISTING_OWNER_ONLY
R8  = OPTIONAL_PROPORTIONAL_EXISTING_TASK_LEARNING
R9  = L2_DETAIL
R10 = EXISTING_OWNER_ONLY; Product-vs-Architecture research separation is owned by R1
```

### 2.2 Architecture invariants

1. **One semantic concern → one canonical owner or explicit composition rule.** Projections and evidence indexes never become competing authority.
2. **Durable fact != semantic authority.** GitHub/repository/evidence records carry facts/currentness; they do not create correctness authority.
3. **Authority != Capability != Authorization.** Model/tool strength never widens authority.
4. **Evidence != Verdict != Authority.** Product Review/Validation/CI/Builder summaries cannot themselves freeze Product or qualify Release.
5. **Task/PR PASS != Release PASS.** Release remains separately owned.
6. **Exact-subject currentness is first-class.** Historical PASS remains historical after subject drift.
7. **Product Review is proportional evidence/judgment.** It is required when Frozen Product/risk/policy requires it, not unconditionally for every low-risk adopter Product Freeze.
8. **Product Freeze is a Product-authority act.** A review recommendation never manufactures Product authority.
9. **Human intervention defaults to minimal, but Human controllability/auditability is mandatory.** Authorized humans can inspect, stop/cancel/redirect, decide authority-sensitive questions and reconstruct causation where policy allows/requires.
10. **No mandatory human line-by-line code review.** Quality is protected through applicable architecture/contracts/tests/checks/CI evidence/Validation/Review/security/compatibility/release practices.
11. **Maintainability and diff hygiene remain quality concerns.** Automation-first does not legalize destructive whole-file rewrites, mixed concerns, hidden semantic churn or loss of canonical/generated-source ownership.
12. **One Task/DAG/Dispatch/Claim family.** Delegation/handoff enrich existing lineage; no nested competing scheduler lifecycle.
13. **Task granularity is qualitative.** No universal LOC/file/time/token threshold.
14. **Reuse is semantic, not textual.** Importability is not a public contract and similarity is not a DRY mandate.
15. **Task Learning is optional/proportional evidence.** It never becomes a mandatory Product gate or authority mutation channel.
16. **Cost/process telemetry is advisory L2/implementation input.** It cannot waive gates or rank truth.
17. **Product Research and Architecture Research have different purposes.** Product Research informs Product scope before Freeze; Architecture Research/Demo falsifies architecture assumptions after Product Freeze.
18. **Private chain-of-thought is never a required artifact.** Externalizable rationale/evidence refs are sufficient.
19. **Minimum adoption remains lightweight.** No runtime/database/controller is required for conformance.
20. **Compatibility and semantic lineage are non-weakening.** Recovered/recomposed subjects need current evidence; version identity is not rolled backward to inherit qualification.
21. **Product acceptance §19 is evidence obligation, not a second Release standard.** Existing owners produce the facts; Release owns final candidate qualification.
22. **`ADS_CORE_FEATURE_FREEZE_ELIGIBLE` is Product authority.** Architecture/Closure/CI/Reviewer/model vote may supply evidence only; `YES|NO` is recorded by Product authority and `NO` may coexist with successful v4.10 delivery.
23. **Central wiring is integration, not semantic ownership.** Manifest/templates/verifiers reference owner-local decisions rather than redefining them.

---

## 3. Canonical owner/composition map

The implementation baseline may contain same-family successors. Task admission MUST re-read current canonical owner refs. The semantic placement below is frozen by this L2 once approved; file-level successors may replace paths only through explicit non-weakening owner evolution.

| Concern | Canonical owner/composition | v4.10 architecture action | Forbidden duplication |
|---|---|---|---|
| Product scope / Product acceptance / core-freeze outcome | Frozen PRD v0.4 + Product authority record | consume; produce evidence refs only | L2/Controller/Release redefining Product |
| development lifecycle / Stage routing | `standards/DEVELOPMENT_WORKFLOW.md` | harden Stage 1 to Idea→semantic L1→Product Research as needed→Draft PRD→risk/policy-selected Product Review→Product Freeze; preserve Fast Path | second lifecycle |
| Product Review routing | Frozen Product + `DEVELOPMENT_WORKFLOW.md`; durable review facts through existing GitHub interaction/review surfaces where applicable | add proportional selection/independence/currentness guidance without a new generic Review state machine | unconditional review for every adopter; review=freeze authority |
| Architecture decisions | `standards/ARCHITECTURE_DESIGN_STANDARD.md` + Frozen L2 | record drivers/invariants/owners/UNKNOWNs | implementation inventing architecture |
| Architecture Research/Demo | `standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md` + Stage 2 workflow | preserve post-Product-Freeze architecture evidence role | Product Research being routed through Architecture Demo |
| Product Research materialization | Stage 1 `DEVELOPMENT_WORKFLOW.md` + L1/Product artifacts/templates | define proportional/inline vs bounded research routing | new Research lifecycle/authority |
| Task decomposition | `standards/TASK_DECOMPOSITION_STANDARD.md` | add Agent-dispatchable/context/evidence questions only where not already covered; preserve coherent concern + safe parallelism | numeric split policy; fake parallelism |
| live DAG mutation | `standards/TASK_DAG_GOVERNANCE_STANDARD.md` | preserve explicit mutation/currentness | hidden DAG mutation |
| Task/Execution Pack | `standards/EXECUTION_PACK_STANDARD.md` | project current authority/evidence/acceptance refs where useful | parallel Task authority |
| execution / Dispatch / Claim / human decision | `standards/EXECUTION_ARCHITECTURE_STANDARD.md` | reuse derived ready sets, dispatch/claim serialization and Human Decision Queue; add responsibility/causation projection only if a real gap remains | second scheduler/claim/human workflow |
| GitHub event/operator attribution | `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` + Work Item contract | carry bounded causation/delegation/handoff facts where needed | second event protocol |
| implementation quality / maintainability | `standards/IMPLEMENTATION_QUALITY_STANDARD.md` + Task Decomposition | harden diff-hygiene/change-summary guidance if needed; do not make human readability a mandatory pass gate | standalone Human Reviewability authority |
| public/cross-module compatibility | `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` | preserve supported/public contract and migration/deprecation truth | component-specific compatibility authority |
| Validation truth | `standards/VALIDATION_STANDARD.md` | map acceptance to concern/integration/closure evidence on exact subjects | Builder/CI manufacturing Validation PASS |
| Review findings / independent judgment | existing review policy/finding/aggregation surfaces | clarify severity→verdict, successor/delta currentness and repair convergence only where gaps exist | latest-PASS-wins; model-count authority |
| CI execution/evidence | CI standards | evidence/execution only | CI success becoming Product/Review/Release authority |
| Release qualification | `standards/RELEASE_STANDARD.md` | consume Frozen Product/L2/terminal DAG/required evidence; preserve READY/CONDITIONAL/BLOCKED/FAIL | §19 creating second Release verdict family |
| owner discovery | `standard-manifest.json#semantic_authorities` + reference conventions | complete/repair owner discovery and compatibility aliases | second owner registry |
| state vocabulary | existing state-dimension registry / execution-state family | extend only for a proven new dimension | duplicate prose/template enums |
| shared-code safety (former R5) | Architecture + Task Decomposition + Implementation Quality + Interface Compatibility | preserve non-weakening reuse/public-contract invariants only | Product-level component subsystem/registry |
| Task Learning (former R8) | existing Task Learning semantic owner in `EXECUTION_ARCHITECTURE_STANDARD.md` + `task-learning` machine family | optional/proportional same-family hardening only | mandatory terminal learning gate/new DB |
| cost/process feedback (former R9) | L2/implementation planning evidence; existing execution facts where available | optional descriptive inputs only | scheduling/quality authority |
| research coherence (former R10) | Stage 1 workflow + Architecture Research owner | converge purpose/routing; R1 owns Product-level separation | second Research authority |
| project adoption | `standards/PROJECT_ADOPTION.md` | make Minimum/Advanced routing discoverable | mandatory orchestration runtime |

`standard-manifest.json#semantic_authorities` remains the canonical discovery surface for listed concerns such as development lifecycle, execution state, validation evidence, release qualification, architecture research demo and Task Learning. v4.10 extends that registry only when a material current owner is missing; it does not create a competing registry.

---

## 4. Lifecycle and authority composition (R1/R2)

### 4.1 Product front-end

The canonical semantic flow is:

```text
USER IDEA / INTENT
→ INTAKE / BASELINE
→ L1 PRODUCT EVIDENCE / PROBLEM FRAMING
→ PRODUCT RESEARCH as needed
→ Product unknown disposition / evidence synthesis
→ DRAFT PRD / SCOPE
→ Product Review when selected by Frozen Product / policy / risk
→ PRODUCT FREEZE by Product authority
→ L2 ARCHITECTURE EVIDENCE
→ Architecture UNKNOWN disposition / Demo as needed
→ L2 FREEZE
→ TASK DAG
```

L1 is a semantic framing/evidence step, not necessarily a standalone file. On sufficient-evidence low-risk work, Intake/L1/research disposition may be compact/inline and existing Fast Path may remain legal. Semantic authority/evidence required by applicable policy may not be skipped.

### 4.2 Product Review selection

Architecture does not introduce a universal Product Review gate. Stage 1 must express a selection rule compatible with Frozen Product v0.4:

```text
PRODUCT_REVIEW_REQUIRED
  when Product scope is new/materially changed normative, semantic,
  compatibility-sensitive or authority-sensitive,
  or another applicable Product/project policy requires it

PRODUCT_REVIEW_SELECTABLE_OR_OMITTABLE
  for low-risk/already-scoped Product Freeze where no owner requires it

UNKNOWN / contradictory applicability
  fail closed to authority/risk disposition; do not silently downgrade
```

ADS v4.10 itself is normative/authority-sensitive and therefore required Fresh independent Product Review; downstream projects do not inherit that ceremony mechanically.

### 4.3 Review evidence vs Product authority

```text
Product Review
= evidence / independent judgment on an exact Product subject

Product Freeze
= explicit Product-authority record binding one exact Product subject
```

A reviewer may recommend Freeze but cannot create it merely by `PASS`. A Controller may deterministically record Freeze only when the Product authority/routing rule authorizes that transition.

### 4.4 Architecture contradiction

After Product Freeze, Architecture Research may discover that Product scope is infeasible/contradictory. It routes through the existing Product-thaw/contradiction path. L2/implementation MUST NOT silently weaken Product acceptance.

---

## 5. Whole-project owner convergence architecture (R2/R11/R12)

### 5.1 Owner convergence matrix

Implementation must derive an `OWNER_AUTHORITY_CONVERGENCE_MATRIX` from the then-current repository:

```text
CONCERN
CANONICAL_OWNER
PROJECTION_SURFACES
MACHINE_CONTRACTS
COMPATIBILITY_ALIASES
LEGACY_SURFACES
STATUS=CURRENT|COMPATIBILITY_ONLY|DEPRECATED|HISTORICAL_ONLY|SUPERSEDED|GAP|CONFLICT
ACTION=KEEP|HARDEN_OWNER|REWIRE_PROJECTION|CLASSIFY_LEGACY|REMOVE_IF_AUTHORIZED|STOP_FOR_DISPOSITION
EVIDENCE_REFS
```

This matrix is planning/implementation evidence. It is not a runtime registry and does not supersede `standard-manifest.json#semantic_authorities`.

### 5.2 Repair rule

When prose/schema/template/prompt/verifier/CI projection disagree:

1. identify the canonical semantic owner;
2. recover the intended invariant from current Frozen authority;
3. repair owner-local semantics only if the owner itself is deficient;
4. rewire subordinate projections to match;
5. add deterministic positive/negative conformance coverage where useful;
6. do not add another precedence layer solely to hide contradiction.

A stale passing verifier never outranks current authority. Prose must not claim enforcement that does not exist.

### 5.3 Legacy rule

Reachable legacy surfaces receive an explicit `CURRENT|COMPATIBILITY_ONLY|DEPRECATED|HISTORICAL_ONLY|SUPERSEDED|FUTURE_MAJOR|NOT_PLANNED`-equivalent disposition when ambiguity can mislead a fresh user/Agent. Dead unreachable history need not be cosmetically rewritten.

---

## 6. Human + Multi-Agent collaboration and control architecture (R3/R4)

### 6.1 Preserve existing execution family

Human/Agent execution composes the existing Work Item → Dispatch → Claim → result/evidence architecture. The optional reducer/controller remains a projection; manual GitHub-native operation remains legal.

Delegation/handoff MUST NOT create nested authority or a second Claim lifecycle.

### 6.2 Responsibility semantics

Two semantic modes are sufficient at Product/L2 level:

```text
DELEGATED_SUBWORK
  delegator retains responsibility;
  child performs bounded work and returns result/evidence

RESPONSIBILITY_HANDOFF
  active responsibility/control transfers explicitly
  within bounded delegatable authority
```

A durable implementation must make enough facts reconstructible to identify, where material:

```text
requester/delegator
responsibility owner
executor/operator
parent/causal work or dispatch reference
subject/authority scope
result/evidence return reference
handoff/delegation mode
```

These are semantic facts, not a frozen requirement that every listed name become a new schema field. Existing Dispatch/Event/Issue refs should be reused first. Additive machine fields are justified only when deterministic reconstruction cannot otherwise be achieved.

### 6.3 Authority attenuation

```text
EFFECTIVE_CHILD_AUTHORITY
<= legally delegatable authority
∩ current Work/Task authority
∩ role authority
∩ project/external authorization
```

Capability, credentials or tool access do not expand this intersection.

### 6.4 Human control points

Use the existing `EXECUTION_ARCHITECTURE_STANDARD.md` Human Decision Queue / durable work-event mechanisms for authority-sensitive intervention. Product-level semantic reasons may include information, approval, authority decision or external authorization, but v4.10 does not require a new fixed global enum if existing owner vocabulary can express the distinction.

Required behavior:

- humans are not woken merely to relay prompts, poll CI or compute deterministic ready sets;
- authority-sensitive Product/Architecture/security/public-contract/gate/limitation/destructive decisions route to appropriate human/Product authority unless explicitly delegated;
- an authorized human can inspect current authority/evidence/claim state and, where policy permits, stop/cancel/redirect future automated transitions;
- causation for authority-bearing decisions is durably reconstructible.

Human controllability is a hard Product behavior. Human line-by-line code reading is not.

---

## 7. Automation-first quality and maintainability architecture (R4)

### 7.1 Quality composition

No new quality owner is created. Applicable quality derives from composition of:

```text
Frozen Product / Architecture invariants
+ Task acceptance
+ Implementation Quality
+ Testing / deterministic checks
+ CI execution evidence where selected
+ Validation exact-subject evidence
+ independent Review where selected/required
+ compatibility/security/migration owners where applicable
+ Release qualification at closure
```

One mechanism never manufactures another owner's PASS.

### 7.2 Maintainability/diff hygiene

`IMPLEMENTATION_QUALITY_STANDARD.md` remains language-neutral baseline. v4.10 may harden existing quality/review guidance against materially destructive patterns such as:

- unnecessary whole-file rewrite;
- unrelated formatting/generated churn mixed with semantic change;
- mass comment/doc loss that removes maintained intent;
- hidden semantic changes outside declared scope;
- multiple independent concerns mixed into one Task/PR;
- direct edits to generated outputs that ignore regeneration authority;
- unnecessary abstraction or public-surface widening.

These are defect/maintenance/evidence risks. They are not proof that a human must manually understand every generated line.

### 7.3 Change summary

A proportional Builder/Agent change summary MAY/SHOULD be projected through existing PR/Builder/Execution Pack surfaces when it materially helps an Agent, reviewer or human control point. It is navigation/handoff information, not correctness evidence, and no standalone Review Brief authority is created.

---

## 8. Agent-oriented Task granularity and DAG architecture (R7)

`TASK_DECOMPOSITION_STANDARD.md` remains owner with its existing principle:

> Minimum coherent concern + maximum safe parallelism.

v4.10 adds no numeric threshold. Planning should additionally ensure a material Task is:

1. bounded enough for an eligible Agent to receive the required context/authority/write set;
2. capable of producing an independently identifiable exact evidence subject where its gates require that;
3. not dependent on unrelated sibling implementation merely to be correct;
4. maintainable without hiding a shared mutable authority collision.

Prefer real-boundary structure:

```text
shared contract / owner semantic core when genuinely required
        ↓
parallel independently valid concern leaves
        ↓
explicit central integration / projection / conformance
```

only when each leaf is independently valid. A large atomic invariant may remain one Task with stronger internal structure/tests; fake splitting is forbidden.

Task-level and Dispatch-level parallelism remain distinct. Dispatch subdivision cannot silently mutate Frozen DAG semantics.

---

## 9. Assurance and repair convergence architecture (R6)

### 9.1 Assurance floor

Existing owners compose the smallest legal assurance path. Cost, file count, `docs-only`, model confidence, provider success or schedule pressure cannot independently reduce a required gate.

Applicability `UNKNOWN` or contradictory gate facts fail closed to owner/policy disposition rather than convenience.

### 9.2 Review / repair convergence

Where current owners are ambiguous, v4.10 should clarify using existing Review/Workflow semantics:

- severity → verdict behavior;
- unresolved P0/P1 dominance where policy defines it;
- bounded P2/P3 disposition without unnecessary semantic cycles;
- root-defect-class repair rather than cited-symptom-only repair;
- exact-subject successor/delta review currentness;
- mechanical/test-harness residual classification;
- non-converging repair-loop escalation/adjudication;
- diff hygiene / executor mutation capability findings.

No universal repair-round cap is created. Repetition is evidence that decomposition/authority/root cause requires disposition.

### 9.3 Executor capability

If safe mutation of a shared/line-sensitive surface is required, executor eligibility may treat mutation capability as a hard predicate. An executor that cannot safely mutate the required surface routes/blocks rather than compensating through destructive rewrite.

---

## 10. Subordinate concerns without Product re-expansion (R5/R8/R9/R10)

### 10.1 Shared-code safety — existing-owner-only

No Shared Component Product requirement or registry is created.

Existing owners preserve these non-weakening invariants:

- importability does not imply stable/public contract;
- a Task cannot silently widen into project-wide refactor/promotion;
- public/stable changes remain compatibility-authority concerns;
- textual similarity does not mandate DRY extraction;
- universal component registry is not required.

Exact asset classes, producer/consumer/maintainer taxonomy or reuse-decision metadata are implementation/L2 choices only when evidence shows value.

### 10.2 Task Learning — optional/proportional existing family

Existing Task Learning semantics may capture concise reusable execution knowledge for material work. `NO_MATERIAL_EXECUTION_LEARNING` remains legal. No learning artifact is a required terminal Product gate.

Never require raw/private chain-of-thought, secrets, huge logs or automatic promotion. Promotion into durable project/ADS knowledge is a separate authority decision.

### 10.3 Cost/process feedback — L2 detail

Where trustworthy, planning/execution MAY record descriptive ranges/facts such as expected vs observed elapsed/wait class, repair count, resource contention or gate value. `UNKNOWN` is preferred to fabricated precision.

These facts may inform future planning/scheduling policy but never waive required evidence or create correctness/ranking authority.

### 10.4 Research coherence — existing owners implement R1

Product Research is Stage 1 evidence for Product scope/acceptance and may be inline/minimal or a bounded Issue when material. Architecture Research/Demo remains Stage 2 evidence for falsifiable architecture assumptions.

Do not create one universal executable Research pipeline for both. The coherence requirement is shared purpose/terminology/routing, not a second Research authority.

---

## 11. Product acceptance evidence architecture (Frozen PRD §19)

Architecture maps each active Product requirement to existing owners and evidence production. It does not define a second release verdict.

| Product req | Primary architecture evidence producers | Required closure/falsification shape |
|---|---|---|
| R1 | Stage 1 workflow, L1/Product artifacts, Product review/freeze records | material new scope follows semantic stages; sufficient-evidence path demonstrates compact/inline L1 and no unnecessary Research/Product Review ceremony |
| R2 | owner convergence matrix, workflow/manifest/current owner refs | duplicate/stale/contradictory owner or transition detected/dispositioned; no unresolved material contradiction at closure |
| R3 | Execution Architecture + GitHub work/event lineage + focused dogfood | delegation vs handoff, attenuation and causation/responsibility reconstructible without second execution lifecycle |
| R4 | Implementation Quality + tests/checks/Validation/Review + Human Decision Queue | routine autonomous change obtains quality evidence without mandatory human line review; authority-sensitive case routes to correct human/control authority; stop/cancel/redirect/audit demonstrated where policy permits |
| R6 | Review/Workflow/Validation applicability and repair evidence | illegal cost/label/model-confidence gate reduction fails closed; non-converging repair loop receives bounded adjudication |
| R7 | Task Decomposition/DAG evidence | broad work split only on real independently valid seams or retained atomic with bounded evidence; no hidden DAG mutation/fake parallelism |
| R11 | projection/conformance verifier + owner refs | stale passing projection cannot override owner; false prose claim of enforcement detected/dispositioned |
| R12 | discovery/adoption/compatibility/currentness/release identity evidence | fresh adopter finds current owners; recomposed successor does not inherit historical qualification; version identity not rolled backward to recover evidence |

Cross-cutting closure must also prove a lightweight Minimum ADS path and an Advanced ADS path preserving the same authority/currentness truth.

### 11.1 Evidence aggregation boundary

A version-level acceptance/closure index MAY point to the above evidence. Such an index is a projection/reference surface, not a new Gate Authority, Validation state or Release verdict.

Release Qualification remains owned by `RELEASE_STANDARD.md` and consumes the applicable frozen scope, Architecture, terminal DAG, exact candidate and required evidence.

### 11.2 Release blockers

PRD §19.3 release blockers route to their existing owners. L2/Task DAG must ensure work exists to produce/disposition each required evidence family; they do not redefine blocker meaning.

---

## 12. `ADS_CORE_FEATURE_FREEZE_ELIGIBLE` evidence boundary

Architecture MUST support, but MUST NOT decide, the later Product-authority outcome:

```text
ADS_CORE_FEATURE_FREEZE_ELIGIBLE=YES|NO
```

### 12.1 Evidence inputs

The decision consumes at minimum references proving:

- PRD §19 Product acceptance satisfied on applicable release subject;
- R2 owner/lifecycle matrix has no unresolved material duplicate/contradictory authority;
- R11 has no unresolved material prose↔projection/verifier/CI contradiction;
- reachable current-impacting legacy/backlog ambiguity is dispositioned;
- R12 currentness/compatibility/lineage truth is coherent.

### 12.2 Decision authority

The decision is durably recorded by Product authority or an explicitly delegated bounded actor. Existing Product/human decision mechanisms should be reused. No new Release state or execution state is required merely for this `YES|NO`.

`NO` is valid with evidence and does not itself mean v4.10 Release failed. Version Closure, Release READY, CI, Controller state, Review PASS or model consensus cannot automatically imply `YES`.

---

## 13. Research / UNKNOWN disposition

No executable Architecture Research Demo is currently required before successor L2 review. The architecture choices in this L2 are owner-composition and protocol-boundary choices supported by current repository standards.

Material architecture unknowns are bounded as follows:

| UNKNOWN | Disposition | Why it does not block L2 candidate |
|---|---|---|
| exact machine fields for responsibility/delegation/causation | `STATIC_EVIDENCE_SUFFICIENT_FOR_BOUNDARY; TASK_LEVEL_MINIMAL_EXTENSION_IF_NEEDED` | semantic facts are clear; exact projection can reuse existing refs first and is reversible/additive |
| whether Product Review needs a dedicated schema | `NO_SCHEMA_BY_DEFAULT` | Review is evidence/judgment; Issue/comment/current review surfaces are sufficient unless deterministic tooling later proves a machine need |
| exact acceptance evidence index format | `REFERENCE_INDEX_OR_EXISTING_CLOSURE_SURFACE` | evidence-to-owner map is defined; storage shape does not change Product/architecture authority |
| exact core-feature-freeze decision record format | `DURABLE_PRODUCT_AUTHORITY_RECORD; NO_NEW_STATE_DIMENSION_BY_DEFAULT` | decision semantics/authority are fixed; representation can use existing durable decision record conventions |
| exact shared-code taxonomy/reuse metadata | `OPTIONAL_EXISTING_OWNER_DETAIL` | Frozen Product explicitly demoted R5 from Product scope |
| exact cost feedback fields | `OPTIONAL_L2_IMPLEMENTATION_DETAIL` | Frozen Product classifies R9 as L2 detail and non-authoritative |

If implementation discovers that any of these choices changes public contracts, durability, failure semantics, authority or compatibility materially, route through Architecture contradiction/review rather than silently escalating Task freedom.

---

## 14. Machine-contract and projection strategy

### 14.1 Reuse-first rule

Before adding a schema/registry/event field:

1. identify the semantic owner;
2. determine whether existing durable refs already make the fact reconstructible;
3. add a same-family optional field only when deterministic projection/validation materially needs it;
4. preserve backward compatibility unless Frozen authority explicitly authorizes breaking change;
5. add negative verifier coverage for authority/currentness-sensitive fields.

### 14.2 Likely additive projection areas

Potential, not pre-authorized, same-family extensions include:

- existing Dispatch/Event/Work Item refs for parent/causation/responsibility when reconstruction currently fails;
- Stage 1 templates/prompts/checklists for Product Research disposition and Product Review applicability/currentness;
- Task/Execution Pack refs to Frozen Product acceptance/gate obligations where useful;
- Task Learning same-family fields only if existing schema cannot express the selected optional evidence;
- manifest/reference/adoption updates needed to make current owners and entrypoints discoverable;
- closure/conformance references that map PRD §19 requirements to existing evidence.

A machine contract MUST NOT create semantic authority absent from its owner.

### 14.3 Projection convergence

For each owner-local change, update only materially affected projections:

```text
normative prose
schema/registry if deterministic machine behavior needs it
template/prompt/checklist/reference
positive + negative fixtures/tests
verifier/CI projection
adoption/discovery docs
```

Do not touch every surface mechanically when the concern does not project there.

---

## 15. Minimum vs Advanced adoption architecture

### Minimum ADS

A conforming low-risk project can remain repository/GitHub-native with:

- pinned applicable ADS authority;
- semantic Product/Scope/L1 facts proportional to the work;
- Product Research only when evidence is insufficient;
- Product Review only when Product/risk/policy requires it;
- explicit Product authority when Product Freeze is material;
- bounded Task/PR execution;
- required tests/Validation/Review according to applicable owners;
- exact currentness/compatibility truth;
- explicit human authority/control points where needed.

It does not require a reducer/controller service, component registry, learning DB, telemetry system or full multi-Agent orchestration.

### Advanced ADS

Advanced projects may add Task DAG/JIT Execution Packs/Dispatch-Claim/resource-aware routing/parallel Agents/reducer-controller automation/proportional assurance/Task Learning/cost feedback/full release orchestration. These are implementations of the same authority/currentness semantics, not stronger authority.

---

## 16. Candidate implementation concern decomposition

These concerns are **L2 decomposition inputs only**. They are not yet the Frozen Task DAG and their dependency edges must be minimized during Task DAG materialization.

### C1 — Stage 1 lifecycle / Product Research / Product Review / Freeze convergence

Primary owners: `DEVELOPMENT_WORKFLOW.md`, L1/Product prompts/templates, Product planning references.

Deliver: Idea→semantic L1→Product Research as needed→Draft PRD→risk/policy-selected Product Review→Product Freeze authority; legal compact/Fast Path; v4.10 itself remains Fresh-review-required.

### C2 — Human + Multi-Agent responsibility, causation and control

Primary owners: `EXECUTION_ARCHITECTURE_STANDARD.md`, `GITHUB_AGENT_INTERACTION_PROTOCOL.md`, Work Item/Dispatch/Event projections.

Deliver: delegation vs handoff, attenuation, reconstructible causation/responsibility, Human Decision Queue/control semantics with minimal intervention; no second Claim/Human workflow.

### C3 — Automation-first quality / Task granularity / safe mutation

Primary owners: `IMPLEMENTATION_QUALITY_STANDARD.md`, `TASK_DECOMPOSITION_STANDARD.md`, Task/DAG/Execution Pack projections.

Deliver: evidence-first quality, maintainability/diff hygiene, Agent-dispatchable qualitative boundaries, real-safe parallelism and safe mutation capability routing; no mandatory human readability gate.

### C4 — Assurance / Review / Repair convergence

Primary owners: current Review/Workflow/Validation composition.

Deliver: fail-closed gate applicability, severity/verdict/currentness clarification, root-class repair, successor/delta review rules and non-converging loop adjudication without a second Review lifecycle.

### C5 — Subordinate owner hardening: shared-code / Task Learning / cost / research

Primary owners: existing Architecture/Task/Implementation/Compatibility, Task Learning, Stage 1/Architecture Research owners.

Deliver only evidence-backed gaps; preserve `R5 existing-owner-only`, `R8 optional/proportional`, `R9 L2 detail`, `R10 existing-owner`. Avoid feature re-expansion.

### C6 — Owner discovery / projection / machine conformance

Primary owners: manifest/reference conventions, schemas/templates/prompts/checklists/verifiers/CI projections.

Deliver owner convergence matrix, stale/legacy classification, minimal same-family machine updates and negative conformance coverage. Central registry duplication forbidden.

### C7 — Product acceptance / closure / core-feature-freeze evidence wiring

Primary owners: Frozen Product §19 + Validation/Release/Closure/Product authority composition.

Deliver requirement→evidence mapping in durable planning/closure surfaces, explicit release-blocker coverage, Minimum/Advanced dogfood references and a durable Product-authority `ADS_CORE_FEATURE_FREEZE_ELIGIBLE=YES|NO` decision input path. Do not create a second Release verdict.

### C8 — Central integration / whole-project conformance / dogfood

Primary purpose: integrate owner-local changes, wire central shared projections, execute whole-project conformance/falsification and route discovered owner defects back to C1–C7.

C8 is not a semantic owner and MUST NOT silently repair owner semantics inside integration wiring.

### 16.1 Dependency posture

The conceptual relation is:

```text
C1..C7 ──> C8
```

Only real code/authority/evidence dependencies may become Task DAG edges. Conceptual relationship, desired review order or shared version membership is insufficient to create a dependency.

Where C1–C7 touch shared manifest/template/verifier surfaces, prefer owner-local changes plus one explicit C8 central-wiring task to reduce write collisions.

---

## 17. Architecture acceptance / falsification

A Fresh Independent Architecture Review must falsify at least:

1. Product v0.4 semantics are preserved without L2 inventing or weakening Product requirements.
2. Product Review is proportional evidence/judgment and Product Freeze remains Product authority; no unconditional downstream review ceremony is introduced.
3. Human controllability maps to existing Human Decision/execution mechanisms with minimal routine intervention; no mandatory Human Reviewability gate survives from historical L2 v0.1.
4. automation-first quality does not weaken maintainability/diff hygiene or exact evidence.
5. R5/R8/R9/R10 remain subordinate and do not reappear as new Product/owner families.
6. every active Product requirement R1/R2/R3/R4/R6/R7/R11/R12 has a plausible owner/evidence production path for PRD §19 acceptance.
7. Release/Validation ownership is preserved and §19 does not define duplicate gate/verdict states.
8. `ADS_CORE_FEATURE_FREEZE_ELIGIBLE` remains Product authority consuming evidence and cannot be manufactured by Closure/Release/CI/Review.
9. Product Research vs Architecture Research separation is operational without a second Research lifecycle.
10. machine-contract additions are reuse-first/additive and no new registry/runtime/database is assumed.
11. C1–C8 are sufficiently coherent for later Task DAG materialization and C8 does not become semantic owner.
12. planning independence from other version execution does not imply stale implementation admission.

Any unresolved high-impact architecture owner conflict, authority duplication or Product contradiction blocks L2 Freeze.

---

## 18. L2 Freeze gate

This successor L2 remains **NOT FROZEN**.

Freeze requires:

- a genuinely Fresh high-capability Independent Architecture Review on the exact successor L2 blob and exact PR planning HEAD/tree;
- `PRODUCT_BOUNDARY_PRESERVED=PASS`;
- no unresolved P0/P1 and no unresolved architecture-boundary P2;
- all high-impact architecture UNKNOWNs either resolved or explicitly safe to defer under the owning standard;
- currentness rechecked immediately before the terminal and before Controller Freeze.

Only after L2 Freeze may #817 materialize the compact authoritative Task DAG. L2 Freeze does not itself authorize implementation; implementation admission still follows Task/DAG/JIT/current-baseline rules.
