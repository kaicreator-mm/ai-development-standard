# v4.10.0 Task DAG Refinement R1 — Executable Leaves Dogfooding v4.10

Status: **SUCCESSOR REFINED DAG CANDIDATE R1 — CONTROLLER SELF-VALIDATED — FRESH INDEPENDENT PLANNING REVIEW REQUIRED — NOT FROZEN**

Parent planning: `#779`

Execution-preparation amendment: `#844`

Self-dogfood findings: `#845`

Refinement build checkpoint: `#846`

Historical coarse Frozen DAG: `#843` / `docs/implementation/4.10.0/TASK_DAG.md` blob `3b8a0e4fc479b527c54e85783b4514716bec8815`

Frozen Product: `#837` / PRD v0.4 blob `b0b9906035eee253aad4bff0274d3d4c8f90b9db`

Frozen L2: `#842` / L2 v0.2 blob `b03f12700153e128f4a4c02b7e8d7adf960fd7d3`

Current execution-preparation baseline checked before refinement:

```text
MAIN=92e4f764a2630a131d3f156b39f0f09064c9849e
PLANNING_HEAD_BEFORE_REFINEMENT=e7dd7cadda722018877d07d4e6dabc4d02956dff
LIVE_EXECUTION_DAG=NOT_MATERIALIZED
IMPLEMENTATION_AUTHORITY=NO
```

The historical coarse T-001..T-008 remain valid planning/coverage identities. They are **not rewritten**. This successor artifact refines them into executable leaves under the v4.10-consumed Task Decomposition, DAG Governance, Work Item Contract, Execution Pack and Issue-first trigger rules.

---

## 1. Refinement principles

The successor executable DAG MUST satisfy:

```text
minimum coherent concern
+ maximum safe parallelism
+ independently identifiable evidence subject
+ bounded owner/write set
+ stable Task Pack WHAT
+ JIT exact-base HOW
+ native Issue Dependencies after materialization
+ no readiness fabrication
+ no Builder-manufactured Validation verdict
```

Task IDs are namespaced `V410-*` because the repository already contains historical `.agent/execution/T-00x` packs. This avoids ambiguous pack/work identity.

No leaf gets an implementation branch, Execution Pack or Builder dispatch during this refinement stage.

---

## 2. Parent concern → executable leaf mapping

| Historical parent | Successor executable leaves | Refinement rationale |
|---|---|---|
| T-001 | `V410-T01A`, `V410-T01B` | separate canonical Stage-1 lifecycle owner semantics from Product evidence/research/review projections |
| T-002 | `V410-T02A`, `V410-T02B` | separate execution responsibility/control semantics from GitHub/event/machine projection |
| T-003 | `V410-T03A`, `V410-T03B` | separate implementation-quality invariant from Task-decomposition invariant; independently valid owners |
| T-004 | `V410-T04A`, `V410-T04B` | self-dogfood DF-01: workflow/gate-repair and Review finding/currentness are distinct concerns/owners |
| T-005 | `V410-T05A`, `V410-T05B` | self-dogfood DF-02: shared-code safety and execution-learning/feedback are distinct; R10 has no separate leaf |
| T-006 | `V410-T06A`, `V410-T06B` | separate owner discovery/legacy classification from central machine/projection conformance wiring |
| T-007 | `V410-T07A`, `V410-T07B` | separate Product acceptance/closure evidence wiring from core-feature-freeze decision support |
| T-008 | `V410-T08A`, `V410-V01` | self-dogfood DF-03: Builder integration and independent self-dogfood Validation must be separate roles/evidence |

### R9 / R10 non-mechanical task rule

```text
R9 cost/process feedback
  -> covered inside V410-T05B as non-authoritative execution-feedback detail;
     no separate telemetry owner/system Task.

R10 research coherence
  -> covered by V410-T01B + existing Architecture Research owner;
     NO_SEPARATE_LEAF because a separate Research lifecycle would duplicate authority.
```

---

## 3. Successor refined DAG

```text
V410-T01A ──┬──> V410-T01B ────────────────────────┐
            └──> V410-T04A ──┐                    │
                              ├──> V410-T04B ──────┤
V410-T02A ──┬──> V410-T02B ──┘                    │
            └──> V410-T05B ────────────────────────┤
                                                   ├──> V410-T06A
V410-T03A ──┐                                      │
            ├──> V410-T05A ────────────────────────┤
V410-T03B ──┘                                      │
                                                   │
                                                   └──> V410-T06A

V410-T06A -> V410-T06B -> V410-T07A -> V410-T07B -> V410-T08A -> V410-V01
```

Canonical edge list:

```text
V410-T01A -> V410-T01B
V410-T01A -> V410-T04A
V410-T02A -> V410-T02B
V410-T02A -> V410-T05B
V410-T03A -> V410-T05A
V410-T03B -> V410-T05A
V410-T04A -> V410-T04B
V410-T02B -> V410-T04B
V410-T01B -> V410-T06A
V410-T04B -> V410-T06A
V410-T05A -> V410-T06A
V410-T05B -> V410-T06A
V410-T06A -> V410-T06B
V410-T06B -> V410-T07A
V410-T07A -> V410-T07B
V410-T07B -> V410-T08A
V410-T08A -> V410-V01
```

No edge exists merely for desired review order. Every edge is justified below by shared owner/write-set or required durable semantic/evidence input.

---

## 4. Executable leaf contracts at DAG level

These are DAG-level stable facts. Full Task Packs are created only after this refined DAG receives Fresh Independent Planning Review PASS and successor Freeze.

### V410-T01A — Stage-1 canonical lifecycle semantics

```text
parent=T-001
primary_concern=Stage-1 lifecycle authority
risk=high
review_policy=required
validation_scope=concern
agent_freedom=F1_BOUNDED_IMPLEMENTATION
planned_write_owner=standards/DEVELOPMENT_WORKFLOW.md
```

Goal:

- make the canonical front-end sequence explicit: Idea/Intent → Intake/Baseline → semantic L1 framing/evidence → Product Research as needed → Draft PRD/Scope → Product Review when selected by risk/policy → Product Freeze by Product authority;
- preserve legal compact/inline/Fast Path behavior;
- distinguish Review evidence/judgment from Product Freeze authority.

Forbidden:

- second Product workflow/state machine;
- universal Product Review ceremony;
- Architecture Research being moved before Product Freeze.

Acceptance includes positive material-scope path plus negative low-risk/no-invented-ceremony path.

### V410-T01B — Product evidence/research/review planning projections

Depends on: `V410-T01A`.

```text
parent=T-001
primary_concern=Stage-1 Product evidence/research planning projections
risk=high
review_policy=required
validation_scope=concern
agent_freedom=F1_BOUNDED_IMPLEMENTATION
planned_write_surfaces=prompts/L1_PRODUCT_EVIDENCE.md; templates/research-issue.md; owner-specific Product planning prompt/template/reference surfaces; focused v4.10 tests
```

Goal:

- stop conflating L1 semantic framing with mandatory research;
- make Product Research proportional and purpose-typed using the existing Research family;
- keep R10 coherence by reusing existing Architecture Research owners rather than creating a second Research lifecycle.

Acceptance includes `L1 != mandatory Product Research`, `Product Research != Architecture Research`, and truthful `NO_RESEARCH_REQUIRED`/inline outcomes.

### V410-T02A — Human + Multi-Agent responsibility/control semantics

```text
parent=T-002
primary_concern=execution responsibility/delegation/handoff/human-control semantics
risk=high
review_policy=required
validation_scope=concern
agent_freedom=F1_BOUNDED_IMPLEMENTATION
planned_write_owner=standards/EXECUTION_ARCHITECTURE_STANDARD.md
```

Goal:

- define/reconcile `DELEGATED_SUBWORK` vs `RESPONSIBILITY_HANDOFF` semantics;
- preserve authority attenuation;
- make responsibility/causation reconstructible;
- express Human controllability through existing Human Decision/execution architecture with minimal routine intervention.

Forbidden: second Claim lifecycle, second Human workflow, capability→authority escalation.

### V410-T02B — GitHub/event/machine projection for collaboration control

Depends on: `V410-T02A`.

```text
parent=T-002
primary_concern=coordination/event projection of settled responsibility/control semantics
risk=high
review_policy=required
validation_scope=concern
agent_freedom=F1_BOUNDED_IMPLEMENTATION
planned_write_surfaces=standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md; existing Dispatch/Event/Execution-state schemas only where deterministic reconstruction requires additive fields; focused compatibility/negative tests
```

Goal: reuse existing refs first and add only same-family optional machine fields proven necessary.

Acceptance includes backward compatibility and negative authority-escalation/ambiguous-causation cases.

### V410-T03A — Automation-first implementation quality

```text
parent=T-003
primary_concern=implementation-quality invariant
risk=high
review_policy=required
validation_scope=concern
agent_freedom=F1_BOUNDED_IMPLEMENTATION
planned_write_owner=standards/IMPLEMENTATION_QUALITY_STANDARD.md; its direct reference/test surfaces
```

Goal:

- preserve evidence-first QA;
- harden maintainability/diff hygiene/generated-source authority/safe mutation expectations;
- explicitly avoid mandatory human line-by-line review as a quality gate.

Acceptance includes whole-file destructive rewrite, mixed semantic/generated churn, hidden scope widening and generated-source authority negative cases.

### V410-T03B — Agent-dispatchable Task decomposition and safe parallelism

```text
parent=T-003
primary_concern=Task decomposition invariant
risk=high
review_policy=required
validation_scope=concern
agent_freedom=F1_BOUNDED_IMPLEMENTATION
planned_write_owner=standards/TASK_DECOMPOSITION_STANDARD.md; its direct reference/test surfaces
```

Goal:

- strengthen qualitative Agent-dispatchable boundaries;
- preserve minimum coherent concern + maximum safe parallelism;
- reject numeric thresholds, fake split and hidden DAG mutation.

Acceptance includes shared-write collision, atomic large concern and central-wiring cases.

### V410-T04A — Gate applicability and repair-routing convergence

Depends on: `V410-T01A`.

```text
parent=T-004
primary_concern=workflow/gate applicability + bounded repair routing
risk=high
review_policy=required
validation_scope=concern
agent_freedom=F1_BOUNDED_IMPLEMENTATION
planned_write_surfaces=standards/DEVELOPMENT_WORKFLOW.md; standards/VALIDATION_STANDARD.md only where gate/currentness owner clarification is required; focused lifecycle tests
```

Goal:

- fail closed on unknown/contradictory applicability;
- prevent cost/docs-only/model-confidence shortcuts from silently reducing required gates;
- route bounded root-class repair and non-converging loop adjudication without universal retry cap.

### V410-T04B — Review finding/aggregation/currentness convergence

Depends on: `V410-T04A`, `V410-T02B`.

```text
parent=T-004
primary_concern=Review finding/aggregation/exact-subject successor semantics
risk=high
review_policy=required
validation_scope=concern
agent_freedom=F1_BOUNDED_IMPLEMENTATION
planned_write_surfaces=standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md and existing review-finding/review-aggregation machine contracts only where current semantics require convergence; focused review-currentness tests
```

Goal:

- make severity→verdict/currentness behavior deterministic enough for repair routing;
- preserve old exact-subject evidence historically;
- allow bounded successor/delta Review only where owner rules permit;
- avoid a second Review lifecycle.

### V410-T05A — Shared-code safety under existing owners

Depends on: `V410-T03A`, `V410-T03B`.

```text
parent=T-005
primary_concern=shared-code promotion/reuse safety
risk=medium
review_policy=required
validation_scope=concern
agent_freedom=F1_BOUNDED_IMPLEMENTATION
planned_write_surfaces=residual existing-owner gaps across Implementation Quality / Task Decomposition / Interface Compatibility only after T03 semantics are integrated; focused tests
```

Goal:

- preserve importability != stable/public contract;
- prevent silent Task-local→project-wide promotion/refactor;
- keep compatibility ownership with existing compatibility authority;
- no mandatory component registry or mechanical DRY policy.

`NO_CHANGE_REQUIRED` is a valid execution result if predecessor semantics and current compatibility owner already satisfy the frozen invariant.

### V410-T05B — Optional Task Learning + non-authoritative execution feedback

Depends on: `V410-T02A`.

```text
parent=T-005
primary_concern=bounded execution learning/feedback evidence semantics
risk=medium
review_policy=required
validation_scope=concern
agent_freedom=F1_BOUNDED_IMPLEMENTATION
planned_write_surfaces=standards/EXECUTION_ARCHITECTURE_STANDARD.md after T02A; existing task-learning schema/reference/test family; no new telemetry service/database
```

Goal:

- preserve Task Learning as optional/proportional evidence;
- preserve `NO_MATERIAL_EXECUTION_LEARNING`;
- keep cost/latency/process observations descriptive/non-authoritative;
- never store private chain-of-thought/secrets/huge logs by requirement;
- never let feedback waive gates or auto-amend ADS.

### V410-T06A — Owner convergence inventory / discovery / legacy classification

Depends on: `V410-T01B`, `V410-T04B`, `V410-T05A`, `V410-T05B`.

```text
parent=T-006
primary_concern=current owner/discovery convergence
risk=high
review_policy=required
validation_scope=concern
agent_freedom=F1_BOUNDED_IMPLEMENTATION
planned_write_surfaces=standard-manifest.json#semantic_authorities; owner-discovery/reference convention/legacy classification surfaces; owner-convergence evidence artifact
```

Goal: produce one current owner map, classify stale/reachable legacy surfaces and remove duplicate/contradictory discovery without creating a second owner registry.

This leaf is the central owner of shared manifest/discovery writes; upstream Tasks must not independently edit those central surfaces.

### V410-T06B — Central projection and machine conformance wiring

Depends on: `V410-T06A`.

```text
parent=T-006
primary_concern=shared projection/machine conformance to settled owners
risk=high
review_policy=required
validation_scope=concern
agent_freedom=F1_BOUNDED_IMPLEMENTATION
planned_write_surfaces=shared schemas/templates/checklists/golden/verifier/CI projection surfaces materially affected by upstream owner changes; v4.10 positive/negative conformance tests
```

Goal: wire settled owner semantics into machine/projection surfaces without redefining them.

Forbidden: central semantic rewrite, second registry, blanket touch-every-file migration.

### V410-T07A — Product acceptance / release-blocker evidence wiring

Depends on: `V410-T06B`.

```text
parent=T-007
primary_concern=Frozen PRD §19 requirement→evidence/closure mapping
risk=high
review_policy=required
validation_scope=concern
agent_freedom=F1_BOUNDED_IMPLEMENTATION
planned_write_surfaces=existing version-closure/release/reference/checklist surfaces; acceptance-evidence index/projection; focused negative tests
```

Goal:

- make R1/R2/R3/R4/R6/R7/R11/R12 evidence obligations reconstructible;
- cover release blockers without creating a second Release verdict;
- preserve exact candidate/currentness truth and no historical evidence transfer.

### V410-T07B — Core-feature-freeze Product-decision support

Depends on: `V410-T07A`.

```text
parent=T-007
primary_concern=durable evidence-input/record path for ADS_CORE_FEATURE_FREEZE_ELIGIBLE
risk=high
review_policy=required
validation_scope=concern
agent_freedom=F1_BOUNDED_IMPLEMENTATION
planned_write_surfaces=existing Product/human decision + closeout/reference/template surfaces only; no new execution/release state dimension
```

Goal:

- support explicit Product-authority `YES|NO` decision;
- `NO` remains legitimate evidence-backed result;
- Version Closure/Release READY/CI/Controller/Reviewer/model vote cannot manufacture `YES`.

This Task implements the record/input path; it does **not** make the final Product decision.

### V410-T08A — Central integration / visible whole-project conformance wiring

Depends on: `V410-T07B`.

```text
parent=T-008
primary_concern=dependency-complete visible integration/conformance assembly
risk=high
review_policy=required
validation_scope=integration
agent_freedom=F1_BOUNDED_IMPLEMENTATION
planned_write_surfaces=integration-only residual wiring/tests/docs/golden fixtures that cannot be owned by one upstream semantic Task
```

Goal:

- integrate owner-local changes;
- run/prepare full visible repository regression/conformance;
- expose semantic defects back to owning leaf through normal repair/DAG governance;
- never hide semantic fixes inside integration.

T08A does not claim Hidden Validation or Release Qualification PASS.

### V410-V01 — Independent v4.10 self-dogfood Validation

Depends on: `V410-T08A`.

```text
parent=T-008
type=type:validation
primary_concern=v4.10 validates its own development/coordination standard against the dependency-complete visible candidate
risk=high
validation_scope=integration/closure-input
implementation_write_set=NONE
builder_role=NOT_APPLICABLE
```

This is deliberately a Validation node, not a Builder Task.

Validate at minimum:

- Idea/L1/Product Research/Product Review/Product Freeze ordering and proportionality;
- Frozen Product/L2/Task DAG authority chain;
- executable leaf Task Pack completeness;
- native Issue Dependency graph exactly matches Frozen refined DAG after materialization;
- no premature branches/Execution Packs before dependencies are satisfied;
- pointer-only task triggers reconstruct complete durable contracts;
- claim/currentness/exact-subject behavior;
- Human controllability with no routine relay burden;
- automation-first quality and independent Review separation;
- Product acceptance evidence mapping and historical evidence non-transfer;
- Task/PR PASS != Release PASS.

Validation failure routes to the owning Task/architecture/Product authority; the Validator does not repair source.

---

## 5. Parallelism waves

### Wave A — independent semantic owners

May run concurrently after future execution materialization/currentness admission:

```text
V410-T01A
V410-T02A
V410-T03A
V410-T03B
```

Their planned normative write owners are distinct.

### Wave B — owner-local successors

After their own prerequisites:

```text
V410-T01B  after T01A
V410-T04A  after T01A
V410-T02B  after T02A
V410-T05B  after T02A
V410-T05A  after T03A + T03B
```

`T01B` and `T04A` may run concurrently because T01B is restricted away from `DEVELOPMENT_WORKFLOW.md`.

`T02B` and `T05B` may run concurrently because T02B owns GitHub/event projection while T05B owns execution-learning feedback surfaces; any discovered overlap requires explicit DAG mutation rather than silent parallel editing.

### Wave C — Review convergence

```text
V410-T04B after T04A + T02B
```

### Wave D onward — deliberate convergence

```text
V410-T06A
-> V410-T06B
-> V410-T07A
-> V410-T07B
-> V410-T08A
-> V410-V01
```

This serial tail is intentional because these nodes own shared central projection, acceptance wiring, final integration and independent evidence respectively.

---

## 6. Frozen Product/L2 coverage map

| Product / L2 concern | Successor leaf coverage |
|---|---|
| R1 Product discovery lifecycle | T01A, T01B |
| R2 owner/lifecycle convergence | T06A, T06B |
| R3 Human + Multi-Agent collaboration | T02A, T02B |
| R4 Human controllability + automation-first quality | T02A, T03A, T03B |
| R6 proportional assurance / convergent repair | T04A, T04B |
| R7 Agent-oriented granularity | T03B |
| R11 projection/conformance alignment | T06A, T06B |
| R12 discoverability/compatibility/lineage | T06A, T07A, T08A/V01 evidence |
| R5 existing-owner shared-code safety | T05A |
| R8 optional/proportional Task Learning | T05B |
| R9 L2 non-authoritative cost/process feedback | T05B |
| R10 research coherence | T01B + existing Architecture Research owner; no separate leaf |
| PRD §19 acceptance / release blockers | T07A, T08A, V01 |
| ADS_CORE_FEATURE_FREEZE_ELIGIBLE support | T07B; final Product decision remains outside implementation Task authority |

---

## 7. v4.10 self-validation of this refinement

Controller self-validation is not independent Review authority.

### 7.1 Task Decomposition Standard

```text
ONE_PRIMARY_CONCERN_PER_EXECUTABLE_LEAF=PASS
BOUNDED_OWNER_WRITE_SET=PASS
INDEPENDENT_EVIDENCE_SUBJECT=PASS
REAL_SAFE_PARALLELISM=PASS
NO_FILE_COUNT_SPLIT=PASS
NO_FAKE_PARALLELISM=PASS
CENTRAL_SHARED_WRITES_ISOLATED=PASS
```

Repairs applied during self-validation:

- DF-01 split coarse T-004;
- DF-02 split coarse T-005 and removed mechanical R10 leaf;
- DF-03 separated Builder integration from Validation dogfood.

### 7.2 Task DAG Governance

```text
HISTORICAL_DAG_PRESERVED=#843
PARENT_TASK_IDENTITIES_PRESERVED=PASS
SPLIT_RATIONALE_DURABLE=#844,#845,this artifact
REAL_DEPENDENCY_EDGES_EXPLAINED=PASS
NO_READINESS_FABRICATION=PASS
LIVE_NATIVE_DAG_MUTATION=NOT_YET_APPLICABLE
```

### 7.3 GitHub Work Item Contract readiness

Each implementation leaf can resolve:

```text
type:task
state:planned initially
one review policy
one risk classification
Frozen Product/L2/refined-DAG refs
stable Task Pack
allowed/forbidden scope
acceptance/gates/validation owner
native dependencies after materialization
JIT branch policy
```

`V410-V01` resolves `type:validation` and does not pretend to be implementation work.

Result: `ISSUE_CONTRACT_MATERIALIZATION_READY_AFTER_REFINED_DAG_FREEZE=YES`.

### 7.4 Execution Pack Standard

```text
TASK_PACK_WHAT_STABLE=YES
EXACT_BASE_HOW_DEFERRED_TO_JIT=YES
PREMATURE_IMPLEMENTATION_BRANCHES=NO
PREMATURE_EXECUTION_PACKS=NO
AGENT_FREEDOM_PREPLANNED=YES
```

### 7.5 Issue-first trigger

No trigger is emitted at this stage. Future triggers can remain pointer-only because every task-specific fact will live in Issue + Frozen Task Pack + JIT Execution Pack/Dispatch.

```text
LONG_CHAT_TASK_CONTRACT_REQUIRED=NO
POINTER_ONLY_TRIGGER_FEASIBLE=YES
```

### 7.6 Product/L2 non-weakening

```text
ACTIVE_PRODUCT_REQUIREMENTS_PRESERVED=PASS
R5_R8_R9_R10_SUBORDINATE_PLACEMENT=PASS
HUMAN_CONTROLLABILITY_MINIMAL_INTERVENTION=PASS
AUTOMATION_FIRST_QUALITY=PASS
NO_NEW_RUNTIME_SCHEDULER_REGISTRY_TELEMETRY_FAMILY=PASS
RELEASE_AUTHORITY_NOT_DUPLICATED=PASS
```

### 7.7 Currentness / implementation admission

Main is unchanged at the checked planning baseline as of refinement start, but implementation admission is intentionally still closed.

Before each future executable leaf becomes READY:

```text
re-read current integration baseline
re-read current canonical owners
verify Frozen Product/L2/refined Task DAG currentness
materialize/verify native dependencies
freeze Task Pack revision
wait for real predecessors
create branch JIT
create/bind Execution Pack JIT
accept claim
then implementation may begin
```

---

## 8. Self-validation verdict

```text
V410_REFINED_DAG_SELF_DOGFOOD_R1=PASS_WITH_REPAIRED_FINDINGS
INDEPENDENCE=NO_SELF_REVIEW
P0=0
P1=0
P2_INITIAL=3
P2_REPAIRED=3
P2_OPEN=0
P3=0
REFINED_DAG_FREEZE_RECOMMENDATION=NO_SELF_REVIEW_CANNOT_FREEZE
EXECUTION_ISSUE_MATERIALIZATION=HOLD
IMPLEMENTATION_AUTHORITY=NO
NEXT=FRESH_INDEPENDENT_REFINED_DAG_REVIEW
```

A Fresh Independent Planning/Task-DAG Reviewer must re-read the exact successor artifact/head and independently challenge concern atomicity, real dependencies, write-set collision, Product/L2 coverage, role separation, central-wiring ownership and JIT/currentness discipline before successor refined-DAG Freeze.
