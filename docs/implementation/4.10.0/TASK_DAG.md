# Task DAG — ai-development-standard v4.10.0

Status: **FROZEN PLANNING DAG — EXECUTION ISSUES NOT YET MATERIALIZED — IMPLEMENTATION AUTHORITY NO**

Parent planning: `#779`
Planning PR: `#812`
Task DAG checkpoint: `#817`
Frozen Product: `#837` / PRD v0.4 blob `b0b9906035eee253aad4bff0274d3d4c8f90b9db`
Frozen L2: `#842` / L2 v0.2 blob `b03f12700153e128f4a4c02b7e8d7adf960fd7d3`
Fresh Architecture Review: `#839@5994485257` PASS

## 1. Frozen inputs and execution admission boundary

Planning checkpoint base before this DAG was materialized:

```text
PLANNING_BRANCH=planning/v4.10.0
PRE_DAG_HEAD=74ba245ea1c7b7189ad50acf72bcdb4a0d4f2f0b
FROZEN_PRD_BLOB=b0b9906035eee253aad4bff0274d3d4c8f90b9db
FROZEN_L2_BLOB=b03f12700153e128f4a4c02b7e8d7adf960fd7d3
TASK_DAG_AUTHORITY=FROZEN_BY_THIS_DOCUMENT_AND_CHECKPOINT
IMPLEMENTATION_AUTHORITY=NO
```

This is the intended planning/history topology. Execution Issues, native GitHub Issue Dependencies, branches, Task Packs, JIT Execution Packs and implementation dispatches are intentionally **not** materialized by this planning checkpoint.

Before any future implementation admission:

1. re-read current `main` / integration baseline and current canonical owner registry;
2. classify drift against the Frozen Product/L2/Task DAG;
3. create/bind execution Issues and native Issue Dependencies from this DAG;
4. establish each Task's exact Task Pack/Execution Pack, write set, Review Policy and JIT base;
5. do not treat this historical planning baseline as implementation authority if current owners/baseline materially changed.

## 2. Decomposition rationale

The DAG implements L2 C1–C8 as eight compact concern Tasks.

It does **not** use conceptual order as dependency authority. Dependencies below exist only for a real shared-owner/write-set or evidence/integration prerequisite:

- T01 → T04 because both can mutate `DEVELOPMENT_WORKFLOW.md`; Stage 1 lifecycle/Product Review semantics must settle before assurance/repair edits touch the same workflow owner.
- T03 → T05 because shared-code safety can touch Implementation Quality / Task Decomposition; T05 is restricted to residual subordinate-owner gaps after T03 so the same semantic/file surface is not edited independently in parallel.
- T02/T04/T05 → T06 because central owner discovery/projection/conformance must consume settled owner-local semantics. T01 and T03 are already transitively included through T04/T05.
- T06 → T07 because requirement→evidence/closure wiring needs the current converged owner/projection map.
- T07 → T08 because whole-project dogfood/integration must test the final owner + acceptance wiring rather than an intermediate projection.

No stacked PR is planned. Each Task should use an independent JIT branch from the then-current legal integration baseline after its real dependencies are integrated.

## 3. Frozen planning DAG

| Task | L2 concern | Lane | Depends On | Parallel posture | Risk | Primary owner/write-set boundary | Output / acceptance | Model | Required Validation | Review Policy | Code baseline | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T-001 | C1 Stage 1 lifecycle / Product Research / Product Review / Freeze | product-lifecycle | — | YES with T-002/T-003 | H | `DEVELOPMENT_WORKFLOW.md` Stage 0/1 + L1/Product planning prompts/templates/references; no generic Review/Release rewrite | Idea→semantic L1→proportional Product Research→Draft PRD→risk/policy-selected Product Review→Product Freeze by Product authority; compact/Fast Path legal; Review=evidence/judgment | High | focused lifecycle/projection tests; negative low-risk/no-ceremony cases; current owner/reference checks | required | independent JIT | TODO |
| T-002 | C2 Human + Multi-Agent responsibility, causation and control | collaboration-control | — | YES with T-001/T-003 | H | `EXECUTION_ARCHITECTURE_STANDARD.md`, `GITHUB_AGENT_INTERACTION_PROTOCOL.md`, existing Work/Dispatch/Event contracts only where needed | delegation vs handoff; authority attenuation; reconstructible causation/responsibility; Human Decision Queue/control semantics; no second Claim/Human workflow; additive/reuse-first machine changes | High | focused execution/event/schema compatibility + negative authority-escalation/control cases | required | independent JIT | TODO |
| T-003 | C3 Automation-first quality / Task granularity / safe mutation | quality-decomposition | — | YES with T-001/T-002 | H | `IMPLEMENTATION_QUALITY_STANDARD.md`, `TASK_DECOMPOSITION_STANDARD.md`, Task/Execution Pack projections; owns shared-code safety only where it is quality/decomposition semantics | automation/evidence-first quality; maintainability/diff hygiene; safe mutation routing; real Task seams/safe parallelism; no mandatory human line-review gate or universal numeric split threshold | High | focused implementation-quality + decomposition + generated-source/write-set negative tests | required | independent JIT | TODO |
| T-004 | C4 Assurance / Review / Repair convergence | assurance-repair | T-001 | YES with T-005 after T-001 | H | current Review/Validation/Workflow owner surfaces; `DEVELOPMENT_WORKFLOW.md` changes occur only after T-001 | fail-closed applicability; severity/verdict/currentness; root-class repair; successor/delta review; non-converging-loop adjudication; no second Review lifecycle or retry cap | High | review/validation/workflow regression + negative illegal-gate-reduction/currentness cases | required | independent JIT after T-001 integrated | TODO |
| T-005 | C5 Subordinate owner hardening: shared-code / Task Learning / cost / research | subordinate-hardening | T-003 | YES with T-004 after T-003 | M | residual existing-owner gaps only; do not re-edit T-003 semantics independently; Task Learning / research / optional telemetry owners; shared-code residuals only if outside T-003 owner scope | evidence-backed hardening or explicit `NO_CHANGE_REQUIRED`; preserve R5 existing-owner-only, R8 optional/proportional, R9 non-authoritative L2 detail, R10 existing-owner research coherence; no new family/registry/telemetry authority | High/Medium | focused owner regressions + negative feature-reexpansion/authority-waiver cases | required | independent JIT after T-003 integrated | TODO |
| T-006 | C6 Owner discovery / projection / machine conformance | projection-conformance | T-002,T-004,T-005 | NO until predecessors integrated | H | central/shared projection surfaces: `standard-manifest.json`, registries/reference routing, shared schemas/templates/checklists/golden/verifier/CI wiring as materially required; owner-local semantics remain upstream | authoritative owner-convergence matrix; stale/legacy classification; minimal same-family projection updates; positive+negative conformance; no second owner registry; shared write collisions centralized here | High | `verify_standard`/schema/manifest/reference/golden/conformance suites + negative stale-projection tests | required | independent JIT after predecessors integrated | TODO |
| T-007 | C7 Product acceptance / closure / core-feature-freeze evidence wiring | acceptance-closure | T-006 | NO | H | Frozen PRD §19 projection into existing Validation/Closure/Release/Product-authority reference surfaces; no Release state ownership | durable R1/R2/R3/R4/R6/R7/R11/R12 evidence map; release-blocker coverage; Minimum/Advanced dogfood refs; explicit Product-authority `ADS_CORE_FEATURE_FREEZE_ELIGIBLE=YES|NO` input/record path; Release remains owner of release verdict | High | focused closure/release/reference tests; acceptance-map completeness + negative automatic-YES/old-evidence-transfer cases | required | independent JIT after T-006 integrated | TODO |
| T-008 | C8 Central integration / whole-project conformance / dogfood | integration-dogfood | T-007 | NO | H | integration/conformance only; central residual wiring/tests/docs; any semantic defect must route back via DAG mutation/successor repair to T-001..T-007 concern owner | integrated v4.10 candidate; full visible regression/conformance; PRD §19 falsification/dogfood evidence preparation; owner/projection consistency; no semantic fixes hidden inside integration; release/Hidden/RQ remain later gates | High | full visible repository regression + whole-project conformance/dogfood + clean-checkout/minimal CI where applicable; no fabricated Hidden/RQ PASS | required | independent JIT after T-007 integrated | TODO |

## 4. Dependency graph

```text
T-001 ───────> T-004 ──┐
                       │
T-002 ─────────────────┼──> T-006 ──> T-007 ──> T-008
                       │
T-003 ───────> T-005 ──┘
```

Interpretation:

- Wave A: `T-001`, `T-002`, `T-003` may execute concurrently after execution materialization/currentness admission.
- Wave B: `T-004` starts after T-001; `T-005` starts after T-003. They may run concurrently and T-002 may still be finishing if legal.
- Wave C: `T-006` waits for T-002/T-004/T-005 and centralizes shared projection/write-set changes.
- Wave D: `T-007` consumes the converged owner/projection map.
- Wave E: `T-008` integrates and falsifies the dependency-complete visible system.

No edge exists merely because two concerns are conceptually related. Any future edge change requires normal Task DAG governance and, after Issue materialization, native Issue Dependency mutation evidence.

## 5. Lane summary

| Lane | Tasks | Entry prerequisites | Shared write-set / authority constraint | Converges at |
|---|---|---|---|---|
| product-lifecycle | T-001 | Frozen Product + L2 | T-001 owns Stage 0/1 workflow changes; T-004 must wait before editing same workflow owner | T-006 |
| collaboration-control | T-002 | Frozen Product + L2 | owns execution/interaction responsibility/control semantics; common registry wiring deferred to T-006 | T-006 |
| quality-decomposition | T-003 | Frozen Product + L2 | owns quality/decomposition semantics; residual subordinate hardening waits via T-005 | T-006 |
| assurance-repair | T-004 | T-001 integrated | no overlap with T-002 execution-owner semantics; shared central projections deferred | T-006 |
| subordinate-hardening | T-005 | T-003 integrated | bounded existing-owner gaps only; `NO_CHANGE_REQUIRED` is valid; cannot re-expand Product scope | T-006 |
| projection-conformance | T-006 | T-002,T-004,T-005 integrated | exclusive planned owner of central manifest/registry/shared projection wiring | T-007 |
| acceptance-closure | T-007 | T-006 integrated | maps evidence to existing owners; cannot create Release/Product verdict | T-008 |
| integration-dogfood | T-008 | T-007 integrated | integration only; semantic defects route back to owner Task through explicit DAG repair/mutation | version closure later |

## 6. Acceptance coverage map

| Frozen Product requirement | Primary Task coverage | Final integration coverage |
|---|---|---|
| R1 Product discovery lifecycle | T-001 | T-008 |
| R2 Owner/lifecycle convergence | T-006 | T-008 |
| R3 Human + Multi-Agent collaboration | T-002 | T-008 |
| R4 Human controllability + automation-first quality | T-002, T-003 | T-008 |
| R6 Proportional assurance / convergent repair | T-004 | T-008 |
| R7 Agent-oriented granularity | T-003 | T-008 |
| R11 Projection/conformance alignment | T-006 | T-008 |
| R12 Discoverability/compatibility/lineage | T-006, T-007 | T-008 |

T-007 owns the version-level evidence-reference wiring for all eight requirements; it does not take semantic ownership from the Tasks above.

## 7. Planning policies

### Review Policy

All eight Tasks are initially `required` for Independent Review because v4.10 mutates normative/authority-sensitive ADS semantics or high-blast-radius central integration. A later authority may strengthen requirements but must not silently weaken them. If T-005 resolves to evidence-only `NO_CHANGE_REQUIRED`, its eventual execution Issue may explicitly re-evaluate applicability before dispatch under the then-current Review Policy owner.

### Validation

Validation remains exact-subject and concern/integration/closure scoped under `VALIDATION_STANDARD.md`. Task-level validation must not fabricate release readiness. T-008 visible integration evidence still does not imply Hidden Validation or Release Qualification PASS.

### Branching / code baseline

No implementation branches are pre-created by this planning freeze. Default future admission is:

```text
real dependencies integrated
→ recompute live DAG readiness
→ read current legal integration baseline
→ JIT task branch
→ current Task/Execution Pack
→ accepted claim
→ implementation
```

Use stacked code baselines only if a future DAG mutation establishes a real unmerged code-baseline dependency.

### Issue/native DAG materialization

This document is the frozen planning/history DAG. When implementation is separately authorized, create one execution Issue per Task and materialize the exact dependencies above as native GitHub Issue Dependencies. Body-text dependency lists are not a substitute for the native graph.

## 8. Freeze boundary

This Task DAG freezes planning topology only.

```text
PRODUCT_AUTHORITY=FROZEN_V0_4
L2_AUTHORITY=FROZEN_V0_2
TASK_DAG_AUTHORITY=FROZEN_PLANNING_TOPOLOGY
EXECUTION_ISSUES_MATERIALIZED=NO
NATIVE_ISSUE_DEPENDENCIES_MATERIALIZED=NO
IMPLEMENTATION_AUTHORITY=NO
RELEASE_AUTHORITY=NO
```

Further work in this controller should stop at this planning boundary unless the user separately authorizes execution preparation/materialization or implementation.
