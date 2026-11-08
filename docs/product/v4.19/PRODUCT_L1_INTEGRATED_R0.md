# ADS v4.19 — Integrated Product/L1 R0: evolutionary optimization in three domains

**State:** DRAFT / PRODUCT_L1_CANDIDATE / NOT_FROZEN / NO_NORMATIVE_ADOPTION  
**Target:** v4.19.0, based on v4.18.0 and its already-effective exact source.  
**Product scope index:** [#1347](https://github.com/kaicreator-mm/ai-development-standard/issues/1347). **Execution learning:** [#1359](https://github.com/kaicreator-mm/ai-development-standard/issues/1359). **Exploration:** [#1361](https://github.com/kaicreator-mm/ai-development-standard/issues/1361).  
**Owner direction:** v4.19 continues, refines and improves prior ADS versions; not a competing architecture or mutually exclusive set of systems. This document is a reviewable proposed unification, not a rewrite of previously frozen authorities.

## 1. Product outcome and version-evolution invariant

ADS v4.19 SHOULD improve real software delivery by (A) lowering the total cost and delay of executing individual Tasks, (B) improving project-level planning, dependency and Outcome Closure, and (C) learning from exact, real feedback to improve the first two domains.

**Evolution, not replacement:** v4.19 = inherited effective v4.18 contracts + qualified additive deltas + explicit prospective corrections + independently evidenced learning. Existing GitHub-native DAG, Task Pack, Dispatch/Claim/CAS, one Writer, source/write-set authority, Validation/Review, CI, Release and private/visible evidence boundaries remain their existing normative owners. A proposed v4.19 rule is not effective merely because it is written in a Draft PR or an Intake Issue.

For every proposed delta record `ALREADY_COVERED | PRACTICE_REFINEMENT | CONFORMANCE_GAP | NORMATIVE_DELTA | DEFER`; bind an existing standard owner, real source evidence, positive/negative counterexample, compatibility impact, validation and adoption authority. Do not duplicate an already-normative requirement merely under new names.

## 2. Three product domains (classification, NOT three runtimes)

### A. Task Execution Optimization & Management (任务执行优化与管理)

**Question:** how to finish an authorized Task with correct evidence at the lowest justified total cost, avoiding cycles and fake progress?

- Execution Strategy: capability/cost/risk-aware selection, continuous Writer/repair responsibility, minimum justified handoff, proportionate assurance, root-cause-first repair and immediate qualified progression (Delivery-First #1359). No blanket Web-first or Local-first precondition.
- Execution Modes: Web Builder + Local Validation, Local Builder, Single Agent, CI/Runner, Hybrid/Parallel. These are selectable/composable assignment profiles, not rival Task/Claim systems.
- Task execution authority: existing Task Pack, Dispatch/Claim/CAS, dependencies, accepted write set, exact-SHA validation, source-level review where required, CI, integration and native Outcome Closure. The role grants bounded authority; profile/environment/provider are routing/provenance, never substitute permissions.
- Source/behavior reliability: tested-vs-declared discovery; public entry → selected implementation → observable behavior; repair/verification reuse and fail-closed evidence (existing #1341, #1343, #1344, #1354).
- Claim termination (#1360): its own prospective qualified contract, not synonymous with Task CLOSED or Release.

**Web-cost rationale:** where Web execution is genuinely cheaper and technically able to deliver, prefer completing more work in Web, using CI before invoking costlier Local. Web Builder + Local Validation is an **opt-in cost-saving mode** for suitable Tasks. That mode keeps LOCAL_VALIDATION read-only/validation-only on exact SHA. When real Local implementation/repair capability is essential or repeated Web↔Local rework exceeds savings, select existing authorized LOCAL_BUILDER (or another permitted capable executor), with one legal Writer at a time. Do **not** grant LOCAL_VALIDATION source-write authority or bypass frozen Task scope.

Selection minimizes *observed or estimated total* `web + local + CI + handoff + rework + waiting/critical-path + risk-adjusted validation`; where costs are unknown, record UNKNOWN rather than fabricate a speedup. Delivery-First is the general optimization policy, not a separate lifecycle; Web+Local is one concrete mode of that strategy.

### B. Project Optimization & Management (项目优化与管理)

**Question:** how do multiple Tasks and their actual dependencies deliver a useful product/version rather than merely more PRs?

- Stage 1 Product/L1 evidence and bounded exploratory Demo studies with one existing index Issue + Git-versioned inputs, negative cases, receipts and exact source pins when material (#1361 / Draft PR #1362). The optional Stage 1 pattern does **not** bypass mandatory Stage 2 Architecture Research Demo rules.
- Product→L2→Task DAG, true dependencies, concern decomposition, feasible package/shared-generated-file writes, safe concurrent lanes, scarce Host/resource coordination (#1320, #1347).
- Integration, real consumer behavior, current native dependency/Claim state, candidate qualification, Hidden/visible validation where applicable, and Release/Deployment by their original authorities.
- Project progress counts **verified native closed Outcome Tasks / frozen core denominator**, separately showing source, test, review, CI, integration and Closure evidence. Diagnose the earliest actual DAG blocker before producing another Dispatch/PR or reopening already-PASS work.
- Tally, task-meta and external Provider integration (#1352/#1356) use one ADS normative interoperability owner; application implementations remain in their own repositories. This v4.19 Product/L1 classification does not imply implementing an entire new orchestration platform.

### C. Experience & Feedback (经验反馈)

**Question:** which observed Task, Project and Demo results justify a reusable improvement?

- Capture exact repo/Issue/PR, SHA/tree/blob, selected artifact, observed tool/environment/command, evidence/negative case, source freshness, actual outcome, NOT_RUN/UNKNOWN and remaining risk (#1354; existing Task Learning owner).
- Separate observation from inference, source authority from derived projection, model-authored checker PASS from genuine independent semantic/product qualification, and historic PASS from new exact-SHA PASS.
- Root-cause analysis and eligibility/impact assessment; distinguish necessary new-evidence iterations from avoidable handoff ping-pong and repeated checks (#1359, #1341).
- Experience candidate → source-qualified cross-project counterexamples → existing Task Learning/Golden/standard-owner review → selectively approved normative delta or practice/skill improvement. No new experience database, mandatory per-Demo issue or automatic promotion.
- DKE / DIS Demo evidence is domain-specific practice input, not automatic proof of universal efficiency; no arbitrary Node-major requirement for content-only/formal/semantic studies unrelated to Node, while actual source/CI/host compatibility gates remain applicable when required.

## 3. Scope ownership and existing intake

| Product domain | Authoritative proposal/intake | Intended v4.19 treatment |
| --- | --- | --- |
| Task strategy | #1359, #1341, #1241, #1092 | Reuse runbook; distinguish principle, mode, role and execution authority; integrate only genuinely missing deltas |
| Dispatch profile mode | #1353, Task #1357, Draft PR #1358 | Preserve additive schema + five legacy mappings; amend over-broad global Web default before qualifying prospective standard text |
| Task quality | #1343, #1344, Draft PR #1342 | Review source-bound necessary changes; tests and counterexamples; remove redundant MUSTs |
| Claim terminal disposition | #1360 | Crosswalk with existing Claim lifecycle; qualify independently if truly a normative gap; do not presume new event required |
| Project exploration | #1361, Draft PR #1362 | Optional Stage 1 evidence mode, independent Stage 2 authority unchanged |
| Project planning / project status | #1320, #1347, #1348, #1349 | Reuse native DAG and CI floor; correct false dependencies and stale projections |
| Cross-project interoperability | #1352, #1356, #1210 | Contract ownership/crosswalk, bounded implementation; do not make real cross-project E2E PASS without observed result |
| Feedback and retrospective | #1354, #1345, #1346, #1260 | Reuse Task Learning/Golden + exact evidence; measured vs unknown cost/time clearly separated |

Existing frozen Web Builder/Local Validation Product/L2/DAG in #1353 are preserved as historical exact subjects. This R0 proposes an **explicit prospective compatibility disposition**, because their text describes ordinary new Web Builder as a global default whereas #1359 and current Owner intent require selection by total cost and capability. The profile bindings and validator-only semantics are still valid; changing a frozen Product rule requires the normal Product Review + revised exact Freeze/derived L2/DAG process. A new Product R0 does not silently thaw or authorize PR #1358 source changes.

## 4. Version acceptance and boundaries

A qualified v4.19 delivery should demonstrate all of the following, with explicit current exact refs:

1. **Inherited conformance:** effective v4.18 controls retained or a source-bound prospective incompatibility/transition approved. No silent historic rewrites.
2. **Task execution:** one real Web-cost-benefit case, one case where Local Builder continuous repair is cheaper/necessary, and negative cases for illegal validator writes, profile-role mismatch, stale Claim, false PASS and unnecessary handoff. Actual time/cost claims only with observed measurement.
3. **Project management:** a multi-Task project trace verifies true dependencies, safe parallelism, earliest blocker identification and qualified Outcome Closure rather than PR counts.
4. **Exploration:** a small inline/no-Demo scenario and a multi-study exact-source indexed scenario; fail-closed negative/UNKNOWN, clear Stage 1 vs Stage 2 and Product authority.
5. **Experience:** at least one real-source observation→counterexample/qualification→existing owner disposition, including explicit reasons for not adopting overgeneralized claims.
6. **Conformance and release:** changed normative owner syntax and focused conformance, inherited applicable regression/CI, real Host/independent review when the actual frozen scope requires them, exact-SHA requalification, qualified integration + Closure and separate authorized Release decision. No claim that unrun CI/physical Host, independent Reviewer or publication is PASS.

**Non-goals:** second scheduler/DAG/Claim/review protocol; mandatory per-study Issue/semver; automatic overwrite of frozen task authority; blanket Node version gate for semantic Demo contents; invented runtime cost metrics; automatic main/tag/release.

## 5. Delivery plan and gate status

1. **P0 — consolidate Product/L1:** independently review this R0 against source-bound v4.18 and existing #1353 Freeze, #1359, #1361 and #1347. Bind accepted changes to an exact revised Product Freeze, not Issue prose alone.
2. **P1 — qualify bounded deltas:** resolve #1353 mode vs global-default tension; evaluate Draft PR #1358 (profiles), #1362 (Demo Stage 1) and #1342 (source quality) against the accepted Product/L2 and real conformance, repairing only within authorized write sets.
3. **P1 — integrate the surviving changes:** decide minimal L2 and Task DAG, assign single Writer for overlapping `standards/DEVELOPMENT_WORKFLOW.md` across #1342/#1362, preserve v4.18 semantics, run changed-tree tests/CI and exact-SHA review.
4. **P1 — release qualification:** version identity, current source/CI/Review/Hidden applicability and resolved Blockers → actual RQ decision → authorized main/tag/release if qualified. Intakes that require longer experiments are explicitly DEFER/UNKNOWN, not fake-complete blockers or silently adopted requirements.

**As of this R0:** only the #1353 bounded feature has source-bound Product/L2/DAG Freeze. #1359 and #1361 are Intake/Product candidates; Draft PR #1342/#1358/#1362 are unmerged; no integrated v4.19 source qualification, Release Qualification, main adoption or published v4.19 is claimed. Progress is measured by legal stage completion, not these files or PR count.
