# ai-development-standard v4.10.0 PRD — Whole-Project Convergence for Human + Multi-Agent Development

Status: **PRODUCT SUCCESSOR CANDIDATE v0.3 — PRODUCT THAWED — FRESH EXTERNAL RE-REVIEW REQUIRED**

PRD revision: `v0.3`

Planning baseline: `main@92e4f764a2630a131d3f156b39f0f09064c9849e` / tree `db8cd8185c6206e93512a455a1f9f8b1e121033f`

Planning parent: `#779`

Historical Product review/freeze lineage:

```text
PRD_v0.1_BLOB=e4c26448acb9a5f88c7f15dc4d023bb9fe0f9e4e
FRESH_PRODUCT_REVIEW=#813@5987814305 PASS
PRODUCT_FREEZE=#814
PRODUCT_THAW_R1=#821 + docs/implementation/4.10.0/PRODUCT_THAW_R1.md
PRD_v0.2_BLOB=bacf667bbc6eeba337a5f75ff63dc090b2173155
FRESH_EXTERNAL_PRODUCT_REVIEW_R2=#822@5988605274 CHANGES_REQUESTED
R2_FINDINGS=P0:0;P1:0;P2:3;P3:0
```

Historical evidence remains attributable only to the exact subject it reviewed. No v0.1/v0.2 verdict transfers automatically to v0.3.

Material evidence inputs: `#808`, `#782`, `#696`, `#775`, `#803`, `#190`, `#186`, `#807`, `#810`, `#811`, Product Amendment `#821`, and external Product review `#822`.

Planning independence: per `#779@5987705061`, v4.10 Product/L2/Task-DAG planning may proceed independently of execution/release currentness of other versions. Other-version facts are evidence inputs only.

No L2 Freeze, Task DAG authority, implementation authority, release authority or repository-integration authority is granted by this candidate.

---

## 1. Product intent

v4.10 is the whole-project convergence release of `ai-development-standard` (ADS).

The Product goal is:

> Make ADS a coherent, machine-projectable, human-controllable and operationally convergent **Human + Multi-Agent Development Collaboration Protocol and Executable Standard System**, so heterogeneous Agents can perform most planning/execution/validation/review work autonomously while humans retain explicit control over intent, authority-sensitive decisions, exceptions and intervention points.

v4.10 is primarily a **convergence and stabilization** release. It MUST prefer strengthening/composing existing owners over inventing parallel subsystems or Product features.

The target outcome is eligibility for a later:

```text
ADS_CORE_FEATURE_FREEZE_ELIGIBLE=YES|NO
```

A `YES` means future ADS evolution defaults to bounded evidence-driven maintenance unless new major-version evidence justifies breaking architecture.

---

## 2. Product category and system boundary

ADS v4.10 is a:

```text
Human + Multi-Agent Development Collaboration Protocol
+
Executable Standard System
```

It standardizes how intent, Product evidence, research, architecture, executable work, semantic authority, durable facts, evidence, independent judgment, currentness, compatibility and human control relate across humans and Agents.

ADS v4.10 MUST NOT become a:

- generic Agent runtime;
- generic scheduler or worker platform;
- project-management SaaS;
- group-chat/supervisor framework;
- checkpoint/tracing database;
- LLM/model gateway;
- Agent discovery service;
- autonomous-development bot product;
- mandatory centralized orchestration service;
- universal component registry.

Optional runtimes may implement ADS. They do not become semantic authority.

Core distinctions:

```text
DURABLE_FACT != SEMANTIC_AUTHORITY
CAPABILITY != AUTHORIZATION
EVIDENCE != VERDICT
BUILDER/AGENT_SUMMARY != INDEPENDENT_EVIDENCE
TASK_OR_PR_PASS != RELEASE_PASS
AUTOMATION != AUTHORITY
```

---

## 3. Primary users and actors

Primary actors are:

1. **Human Product / Architecture / semantic-authority owners** — define intent, Product boundaries, architecture-sensitive choices, risk acceptance and authority-bearing exceptions.
2. **Human or Agent Controllers / Planners** — turn current authority and evidence into legal next work.
3. **Builders** — produce authorized implementation/work product.
4. **Validators** — produce required executable evidence on the required subject/environment.
5. **Reviewers / Auditors, including independent LLM/Agent reviewers** — provide semantic/adversarial judgment where policy requires it.
6. **Downstream adopter teams/projects** — consume ADS at lightweight or advanced adoption levels.
7. **Repository/GitHub/CI/tooling** — durable/projectable execution substrate, not semantic owners.

Provider/model identity is capability/provenance evidence, not authority.

### 3.1 Human operating posture

Human participation is **first-class but intentionally sparse**.

```text
HUMAN_INTERVENTION_DEFAULT=MINIMIZE
HUMAN_CONTROLLABILITY=REQUIRED
HUMAN_AUDITABILITY=REQUIRED
HUMAN_LINE_BY_LINE_CODE_REVIEW=NOT_REQUIRED_BY_DEFAULT
```

Humans SHOULD intervene when intent, semantic authority, approval, external authorization, policy exception or unresolved high-impact ambiguity requires human ownership. Routine implementation quality should not require humans to manually inspect every generated line.

---

## 4. Canonical planning and development journey

v4.10 MUST make the front-of-funnel Product process explicit rather than collapsing L1 and PRD into one step.

### 4.1 Product discovery / definition

```text
USER_IDEA / INTENT
-> INTAKE / BASELINE
-> L1 PRODUCT EVIDENCE / PROBLEM FRAMING
-> PRODUCT RESEARCH as needed
-> evidence synthesis + Product unknown disposition
-> DRAFT PRD / SCOPE
-> Fresh Independent Product / Adversarial Review
-> PRODUCT FREEZE
```

`PRODUCT_RESEARCH` is evidence used to decide **what should be built / standardized and why**. Depending on the Product, it may include user/domain/current-system/source/competitive/market/dogfood/incident/adoption research.

Product Research is proportional:

- evidence already sufficient -> research may remain inline or minimal;
- material Product unknown -> bounded research work may be created;
- trivial/known maintenance -> do not invent research ceremony.

### 4.2 Architecture / implementation planning

After Product Freeze:

```text
FROZEN PRD / SCOPE
-> L2 ARCHITECTURE EVIDENCE
-> Architecture unknown disposition
   -> static/source/existing evidence sufficient
   -> executable Architecture Research Demo as needed
   -> BLOCKED / contradiction
-> L2 FREEZE
-> Task Decomposition / reuse decision
-> TASK DAG
-> Task Pack / L3 / JIT Execution Pack where applicable
```

Product Research and Architecture Research are different:

```text
PRODUCT_RESEARCH
  decides Product problem/scope/acceptance before PRD Freeze

ARCHITECTURE_RESEARCH / DEMO
  falsifies implementation/architecture assumptions after Product Freeze
```

Architecture evidence may contradict a Frozen PRD only through the existing Product-thaw/contradiction path; it must not silently redefine Product scope.

### 4.3 Execution / assurance / learning

```text
Task admission
-> Dispatch / Claim / eligible executor
-> implementation
-> deterministic checks / tests / CI evidence
-> required Validation
-> required independent Review / multi-LLM adversarial review where policy selects it
-> bounded repair / successor evidence
-> expected-head integration
-> optional/proportional existing-owner Task Learning where materially useful
-> Version Closure / Hidden / Release Qualification where applicable
-> immutable baseline / compatibility evolution
```

This journey may be lightweight or highly automated, but truth/authority/currentness semantics remain consistent.

---

## 5. Core jobs to be done

ADS v4.10 MUST make these jobs coherent end-to-end:

1. Turn a user idea/intent into evidence-backed Product scope through explicit L1 and proportional Product Research before PRD Freeze.
2. Turn Frozen Product intent into Architecture Evidence and bounded executable work without silent semantic drift.
3. Coordinate humans and multiple Agents without losing responsibility, causation, delegation/handoff or authorization boundaries.
4. Keep humans in effective control while minimizing routine human intervention.
5. Establish implementation quality primarily through software-engineering evidence and independent/multi-Agent review rather than mandatory human line inspection.
6. Keep durable fact, authority, evidence, verdict and currentness distinct and reconstructible.
7. Apply proportionate assurance without weakening required gates or exact-subject truth.
8. Bound Task/Dispatch granularity so work is executable, maintainable, independently evidential and safely parallelizable.
9. Keep prose, machine contracts, templates, prompts, checklists, examples, verifiers and CI materially aligned with canonical owners.
10. Preserve compatibility, semantic lineage, release identity and non-weakening evolution.
11. Make current owners, lifecycle entrypoints and adoption paths discoverable without private chat history.
12. Ensure optional reuse/learning/cost optimizations stay within existing owners or L2 detail and do not become new authority families or mandatory ceremony.

---

## 6. Product model — seven conceptual planes

The seven planes are views over one owner graph, not seven new services/standards/state machines.

### 6.1 AUTHORITY_AND_INTENT

Covers Idea/Intent, L1 Product Evidence, Product Research, PRD/Scope, Product Freeze, L2 authority, compatibility/SemVer, semantic lineage and non-weakening rules.

Required outcome: a fresh observer can determine current intent, evidence, authority and who may change it.

### 6.2 PLANNING_AND_WORK

Covers Product Research materialization, Architecture Research, Task Decomposition, Task DAG, Task Pack, Work Item, Execution Pack, implementation seams and shared-boundary decisions.

Required outcome: planning stages are not collapsed; executable work is bounded by real semantic dependencies.

### 6.3 COLLABORATION_AND_EXECUTION

Covers Human + Agent collaboration, Dispatch/Claim, delegation vs responsibility handoff, authority attenuation, eligibility/resources and typed control points.

Required outcome: most routine work can proceed autonomously while a human can inspect/intervene when authority requires it.

### 6.4 EVIDENCE_AND_ASSURANCE

Covers tests/checks, Validation, Review, findings, currentness/evidence composition, proportional assurance and repair convergence.

Required outcome: quality comes from evidence and independent judgment appropriate to risk; no layer manufactures another layer's PASS.

### 6.5 REPOSITORY_AND_COMPATIBILITY

Covers machine-contract/owner discovery, immutable pins, migration/adoption, compatibility, legacy classification and stable/shared surfaces.

### 6.6 LEARNING_AND_EVOLUTION

Covers the **existing Task Learning / evolution owner family** and optional/proportional execution learning. Learning never self-mutates authority and is not a mandatory Product gate.

### 6.7 PROJECTION_AND_CONFORMANCE

Covers templates, prompts, checklists, references, examples, fixtures, machine contracts, verifiers and CI projections. They project/test owners but do not become competing authority.

---

## 7. Human controllability and automation-first quality

### 7.1 Hard Product property: controllability, not mandatory reviewability

The hard requirement is that humans can **control and audit** the system, not that every material Agent-produced diff must be manually understandable line-by-line before it can pass.

A conforming workflow must allow an authorized human, when needed, to:

- inspect current Product/Architecture/Task authority;
- inspect current execution owner/claim and exact subject;
- inspect evidence, independent verdicts, unresolved findings and limitations;
- pause/cancel/stop future automated transitions within policy;
- approve/reject Product/Architecture/exception/authorization-sensitive decisions;
- request a concise explanation/change map/evidence map;
- explicitly override only where an owning authority permits override;
- reconstruct who/what caused an authority-bearing transition.

### 7.2 Quality assurance is evidence-first

Implementation quality should be established by the applicable combination of:

```text
architecture / contracts / invariants
+ tests
+ deterministic static/type/lint/build checks where applicable
+ CI execution evidence
+ Validation
+ independent Review / adversarial Review
+ multiple LLM/Agent reviewers where policy or risk justifies diversity
+ integration / compatibility / security / release practices where applicable
```

No rule says one mechanism alone proves quality. Review Policy remains risk/authority dependent.

### 7.3 Implementation/change summary

A Builder/Agent SHOULD produce a **proportional implementation/change summary** when it materially helps another Agent, reviewer or human control point. It may include intent/non-goals, semantic change map, behavior delta, critical invariants, concise externalizable rationale, high-risk/hotspot areas, evidence map, limitations and shared/public surface impact.

This is navigation/handoff information, not correctness evidence and not self-certification. It SHOULD be generated from existing Task/PR/Builder surfaces where practical and SHOULD NOT require a new standalone report family.

### 7.4 Maintainability/diff hygiene remains real

Removing mandatory `HUMAN_REVIEWABILITY=BLOCKED` does not authorize unreadable engineering.

Whole-file rewrites, unrelated formatting churn, mass comment/doc loss, hidden semantic changes, mixed independent concerns, weak module boundaries and unnecessary abstraction remain legitimate Implementation Quality / Task Decomposition / Review findings because they increase defect, maintenance or evidence risk.

---

## 8. Human + Multi-Agent collaboration

ADS preserves one existing Task/Dispatch/Claim family.

### 8.1 Delegation vs responsibility handoff

```text
DELEGATED_SUBWORK
  delegator retains responsibility; child performs bounded work and returns evidence/result

RESPONSIBILITY_HANDOFF
  active responsibility/control transfers explicitly under authority
```

Neither creates a second scheduler or Task lifecycle.

### 8.2 Authority attenuation

```text
EFFECTIVE_CHILD_AUTHORITY
<= legally delegatable authority
∩ Task/Work authority
∩ Role authority
∩ project/external authorization
```

A more capable Agent never gains more authority merely from capability.

### 8.3 Typed human control points

Where human participation is legally/materially required, distinguish at least:

```text
INFORMATION_REQUIRED
APPROVAL_REQUIRED
AUTHORITY_DECISION_REQUIRED
AUTHORIZATION_REQUIRED
```

Human participation is not a generic failure fallback, but neither is it a mandatory step for routine autonomous work.

### 8.4 Responsibility / causation lineage

A fresh observer should be able to reconstruct requester/delegator, responsibility owner, executor, subject, result/evidence and transition cause.

---

## 9. Progressive adoption

### 9.1 Minimum ADS

A project MUST be able to obtain core ADS guarantees without deploying a heavy orchestration runtime.

Minimum adoption may include, as applicable:

- immutable ADS pin;
- explicit Idea/Scope/Product/Architecture/Task authority appropriate to the work;
- bounded Issue/PR execution;
- required tests/Validation/Review truth;
- exact-subject/currentness evidence;
- explicit human control/authority points;
- compatibility truth.

It MUST NOT require a reducer/controller service, learning database, component registry or full automation.

### 9.2 Advanced Multi-Agent ADS

Advanced adopters MAY use Task DAG, JIT admission, Task/Execution Packs, Dispatch/Claim, resource-aware routing, parallel Agents, reducer/controller automation, proportional Assurance, optional existing-owner learning/cost feedback and full release orchestration.

Advanced automation must preserve the same Product/authority/currentness semantics.

---

## 10. Whole-project convergence requirements

v4.10 treats the reachable repository as one standard system.

### 10.1 Canonical owner convergence

Every material active concern must have one canonical owner or an explicit composition rule.

Detect/disposition duplicate owners, ambiguous precedence, stale historical references, authority gaps, lower-level weakening, duplicated lifecycle/state ownership and obsolete discoverable aliases.

### 10.2 Lifecycle coherence

At minimum these stages must compose without contradiction:

```text
Idea / Intake
L1 Product Evidence
Product Research
PRD / Product Freeze
L2 / Architecture Research
Task / DAG / Pack
Dispatch / Claim / Execution
Tests / CI / Validation / Review
Integration
Closure / Hidden / RQ where applicable
Evolution / Learning where applicable
```

### 10.3 Prose ↔ executable alignment

Normative prose, schemas, registries, templates, prompts, checklists, references, fixtures, verifiers and CI must materially agree.

A stale passing verifier cannot override current authority; prose cannot claim machine enforcement that materially does not exist.

### 10.4 Legacy/backlog disposition

Reachable legacy surfaces and material backlog receive an explicit current/compatibility/deprecated/historical/superseded/future-major/not-planned disposition where ambiguity could affect a user or Agent.

Dead unreachable history need not be cosmetically rewritten.

---

## 11. Shared-code governance — existing-owner convergence, not a Product feature

External Product review #822 resolved the former R5 candidate as:

```text
R5_SHARED_CODE_DISPOSITION=REDUCE_TO_EXISTING_OWNER_REQUIREMENT
R5_PRODUCT_CLASSIFICATION=EXISTING_OWNER_ONLY
```

v4.10 therefore does **not** create a separate Product requirement, component-governance subsystem or universal registry for shared code.

Existing Architecture / Task Decomposition / Implementation Quality / Interface Compatibility owners should be hardened only as needed to preserve these non-weakening invariants:

- importability does not automatically create a stable/public contract;
- a Task must not silently widen itself into a project-wide refactor;
- public/stable compatibility changes remain owned by compatibility authority;
- no mechanical DRY mandate;
- no mandatory universal component registry.

Producer/consumer/maintainer taxonomy, exact asset classes and reuse-decision mechanics are L2/existing-owner implementation choices, not Product acceptance criteria.

---

## 12. Task granularity and parallelism

A Task can be semantically coherent yet operationally too broad for reliable Agent execution/evidence.

Prefer real seams such as:

```text
contract/shared semantic core
-> parallel independently valid leaves
-> integration/conformance
```

only where each leaf is independently correct/evidential and shared mutable authority is controlled.

Distinguish Task-level and Dispatch-level parallelism. Do not hide DAG mutation behind Dispatch subdivision.

No universal LOC/file/time/token threshold is authorized.

Human line-by-line readability is not the split criterion. Correctness boundary, context boundedness, independent evidence, maintainability, write-set collision and real architecture dependencies are the primary criteria.

---

## 13. Proportional assurance and review/repair convergence

ADS should select the smallest **legal** assurance path at or above every applicable owner requirement.

Cost, model confidence, file count or `docs-only` labels do not independently authorize gate reduction.

Unknown/contradictory reduction predicates fail closed to the stronger legal path or `BLOCKED`.

Review/repair convergence should ensure:

- severity/verdict semantics are operationally clear;
- bounded repair closes the root defect class, not only the cited symptom;
- successor/delta review can be scoped only where authority allows;
- non-converging loops can be adjudicated;
- mechanical/test-harness residuals do not force needless semantic cycles;
- unresolved findings/currentness remain truthful;
- multi-LLM diversity may increase adversarial coverage but cannot create authority by model count alone.

---

## 14. Existing Task Learning and cost/process feedback placement

External Product review #822 resolved the former R8/R9 candidates as:

```text
R8_EXECUTION_LEARNING_DISPOSITION=OPTIONAL_PROPORTIONAL_EXISTING_TASK_LEARNING
R8_PRODUCT_CLASSIFICATION=EXISTING_OWNER_ONLY
R9_COST_PROCESS_FEEDBACK=L2_DETAIL
```

### 14.1 Task Learning posture

Material executions MAY emit concise, evidence-bound learning under the **existing Task Learning family** when doing so has reusable value. Trivial work may emit none.

Hard non-weakening constraints remain:

- no private chain-of-thought/scratchpad retention requirement;
- no secrets/full environment dumps/raw-log archive by default;
- fact vs inference remains explicit;
- learning cannot auto-amend Product/Architecture/ADS authority;
- `NO_MATERIAL_EXECUTION_LEARNING` remains valid;
- no mandatory terminal learning gate is created.

### 14.2 Cost/process feedback posture

Estimate-vs-actual, queue/wait, repair-count or gate-value telemetry is an **optional L2/implementation optimization input**, not v4.10 Product acceptance and never authority for waiving a required gate. Prefer `UNKNOWN` over fabricated precision.

---

## 15. Research owner coherence — existing-owner implementation of R1

External Product review #822 resolved former R10 as:

```text
R10_PRODUCT_CLASSIFICATION=EXISTING_OWNER_ONLY
PRODUCT_VS_ARCH_RESEARCH_SEPARATION=OWNED_BY_R1
```

R1 owns the Product-level lifecycle distinction:

- Product Research occurs before PRD Freeze when Product evidence is insufficient;
- Architecture Research / Demo occurs after Product Freeze when technical/architecture evidence is insufficient.

Existing Research/workflow owners must be converged to this lifecycle without creating a second Research authority. Research may stay inline when small and sufficiently evidenced; executable Demo is required only when static/source/existing evidence cannot resolve a material falsifiable architecture assumption.

For standards/protocol/governance products, L1 should additionally consider current normative-owner overlap, internal dogfood/incidents, compatibility/SemVer impact and duplicate-authority/weakening risk where material.

---

## 16. Compatibility, semantic lineage and release identity

Semantic lineage and release identity are related but not interchangeable.

Historical evidence remains attributable to the exact subject it proved. It never automatically qualifies a reconstructed/recovered/recomposed successor.

Current version identity must not move backward merely to recover older missing semantics.

Where a current owner is a byte-identical or proven non-weakening successor, preserve the current owner. Missing required semantics may be composed only through authorized bounded change. Unknown/conflicting ownership fails closed.

These are Product invariants; exact recovery mechanics are outside this planning chain.

---

## 17. Repository discoverability and projection coherence

A fresh user/Agent should be able to determine without private chat history:

- where to start from an Idea/Intake;
- where L1 Product Evidence and Product Research live;
- when a Draft PRD exists and what freezes it;
- which owner governs a semantic concern;
- what is normative vs reference/example/history;
- where machine contracts live;
- the minimum adoption path;
- optional advanced orchestration;
- legacy/compatibility posture.

Templates/prompts/checklists/examples must project current owners and lifecycle order.

---

## 18. Converged Product requirements

External Product review #822 pressure-tested the v0.2 R1–R12 list. The Product-level set is now intentionally limited to **eight** active requirements. Historical candidate IDs are preserved for traceability.

### R1 — Product discovery lifecycle coherence
`User Idea/Intent -> L1 Product Evidence -> Product Research as needed -> Draft PRD -> Fresh Product Review -> Product Freeze` is explicit, proportional and distinct from Architecture Research.

### R2 — Whole-project owner/lifecycle convergence
Material current/reachable concerns have one canonical owner or explicit composition rule; the full planning/execution/release lifecycle has no contradictory parallel authority.

### R3 — Human + Multi-Agent collaboration clarity
Delegation vs responsibility handoff, authority attenuation, typed human control points and causation/responsibility lineage are explicit while preserving existing Task/Dispatch families.

### R4 — Human controllability + automation-first quality
Human intervention is minimized by default, but authorized humans can inspect, stop, approve/reject authority-sensitive decisions and audit causation/evidence. Quality is primarily protected through applicable software-engineering evidence, Validation and independent/multi-LLM Review rather than mandatory human line review.

### R6 — Proportional assurance and convergent repair
Required assurance remains fail-closed while duplicate ceremony and non-converging repair loops are reduced through existing owners.

### R7 — Agent-oriented granularity
Tasks/Dispatches support bounded context, safe parallelism and independent evidence without numeric universal limits or hidden DAG mutation.

### R11 — Projection/conformance alignment
Schemas/templates/prompts/checklists/references/fixtures/verifiers/CI materially align with canonical owners and lifecycle order.

### R12 — Discoverability / compatibility / lineage
Current owners, entrypoints, adoption paths, legacy classifications, compatibility and semantic-lineage/release-identity truth are discoverable and non-weakening.

### Dispositioned former candidate requirements

```text
R5  = EXISTING_OWNER_ONLY
      Shared-code safety belongs to Architecture/Task/Implementation/Compatibility owners.

R8  = EXISTING_OWNER_ONLY
      Execution learning is optional/proportional in the existing Task Learning family.

R9  = L2_DETAIL
      Cost/process feedback is optional optimization telemetry, not Product acceptance.

R10 = EXISTING_OWNER_ONLY
      Research workflow coherence belongs to existing owners; Product-vs-Architecture research separation is already R1.
```

These dispositions are part of Product scope: they prevent v4.10 from re-expanding into new feature/owner families.

---

## 19. Product acceptance / dogfood scenarios

Representative Product falsification should include:

1. a raw user idea converted to L1 evidence, bounded Product Research, Draft PRD and Product Freeze without skipping/collapsing stages;
2. a trivial/known maintenance case that correctly avoids unnecessary Product Research ceremony;
3. an Architecture unknown discovered after Product Freeze that uses Architecture Research without silently reopening Product scope;
4. a multi-Agent task completed without routine human intervention, with tests/Validation/independent Review carrying quality assurance;
5. an authority-sensitive decision that correctly pauses for an explicit human decision;
6. a human who can inspect current authority/evidence/claim state and stop or redirect an authorized automated flow without reading every line of generated code;
7. a semantic whole-file rewrite caught by deterministic/review evidence despite green unit tests;
8. a Task/Dispatch split that improves context/evidence/parallelism without fake concurrency;
9. minimum-adoption project that does not deploy orchestration infrastructure;
10. advanced project using JIT/Dispatch-Claim/controller automation while preserving the same authority semantics;
11. fresh adopter navigating Idea -> L1 -> Research -> PRD -> L2 -> DAG from repository entrypoints alone.

Shared-code, Task Learning and cost telemetry may receive L2/existing-owner dogfood, but they are not independent Product Freeze acceptance requirements.

---

## 20. Non-goals

v4.10 MUST NOT:

- collapse Product discovery directly from idea to PRD when material L1/research evidence is required;
- force Product Research when evidence is already sufficient;
- confuse Product Research with Architecture Research Demo;
- create a second Task/DAG/Dispatch/Claim/Review/Validation/Release lifecycle;
- require a centralized runtime/database;
- make humans mandatory line-by-line readers/reviewers of Agent-generated code;
- treat human inability to inspect every line as an automatic quality failure;
- let Agent summaries self-certify correctness;
- use multiple LLM votes as authority without the owning Review/Validation policy;
- create a new Product-level shared-component governance family;
- mandate DRY/common-component extraction by similarity alone;
- let Agents silently promote task-local code into stable/public API;
- require a universal component registry;
- turn execution learning into a mandatory Product gate or new learning family;
- store private chain-of-thought/scratch reasoning;
- require every Task to emit non-empty learning/telemetry;
- make cost/process telemetry a Product delivery authority;
- impose universal LOC/file/time/token thresholds;
- remove required gates because they are expensive;
- make provider/model identity normative authority;
- silently break compatibility or rewrite historical evidence;
- use v4.10 as a generic Agent-platform rewrite.

Breaking redesign belongs to a future major version.

---

## 21. Resolved Product-scope decisions from external R2 review

The v0.2 open questions are closed in v0.3 exactly as recommended by #822:

```text
OQ1_SHARED_CODE
= REDUCE_TO_EXISTING_OWNER_REQUIREMENT

OQ2_EXECUTION_LEARNING
= OPTIONAL_PROPORTIONAL_EXISTING_TASK_LEARNING

OQ3_R1_R12_PRESSURE_TEST
= KEEP_PRODUCT: R1,R2,R3,R4,R6,R7,R11,R12
= EXISTING_OWNER_ONLY: R5,R8,R10
= L2_DETAIL: R9

OQ4_MISSING_PRODUCT_CONCERNS
= NONE
```

No unresolved Product-scope choice remains in this candidate.

---

## 22. Product Freeze criteria v0.3

The successor PRD may be Frozen only after a genuinely Fresh external Product re-review confirms that:

1. Idea -> L1 -> Product Research -> Draft PRD -> Product Review/Freeze is correct, proportional and clearly distinct from Architecture Research;
2. Human Controllability/Auditability is hard Product behavior while routine Human intervention remains minimized;
3. quality assurance correctly relies on applicable tests/checks/CI evidence/Validation/independent or multi-LLM Review/architecture/engineering practices rather than mandatory human line review;
4. #822 R5 disposition is fully resolved as existing-owner-only without a new Product component-governance family;
5. #822 R8 disposition is fully resolved as optional/proportional existing Task Learning without a mandatory terminal gate;
6. #822 R9 is L2 detail and R10 is existing-owner coherence under R1 rather than duplicate Product requirements;
7. the active Product requirement set is exactly R1/R2/R3/R4/R6/R7/R11/R12 unless the Fresh re-review finds a concrete Product defect;
8. no duplicate lifecycle/owner family is introduced;
9. minimum adoption remains lightweight;
10. compatibility/lineage/currentness remain non-weakening;
11. no unresolved P0/P1/P2 Product-scope finding remains.

Only after successor Product Freeze may L2 be rebuilt/rebound. The old L2 blob `390dca32cab3d8647b15149a1ac3c04560c41ddb` is historical/stale because its Product input was thawed.

---

## 23. Planning posture

Current legal sequence:

```text
PRD v0.3 successor candidate
-> Fresh external Product re-review
-> bounded repair if needed
-> successor Product Freeze
-> rebuild/rebind L2 from successor Product authority
-> Fresh Independent Architecture Review
-> L2 Freeze
-> compact Task DAG
```

Other-version execution/release activity is not a prerequisite for this v4.10 planning chain.

Implementation authority remains `NO`.