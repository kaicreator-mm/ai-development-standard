# ADS v4.12.0 — Product Requirements Document / PRD Review Candidate R2

> **STATUS: PRODUCT REVIEW CANDIDATE R2 · NOT FROZEN · NOT NORMATIVE.** R2 is a **bounded repair of five same-author P1 and four P2 findings** recorded in [`V412_PRD_ADVERSARIAL_R1_SELF_REVIEW.md`](../../references/v4.12/V412_PRD_ADVERSARIAL_R1_SELF_REVIEW.md). External adversarial ChatGPT and Claude reports have **not yet been retrieved/verified in the current GitHub/Files surface**; no claim of their incorporation or PASS is made. 此文件面向 v4.12 的首次明确 Product Review / Product Authority Freeze。它 consolidates 2026-10-14 用户确认的方向和当前 GitHub L1/practice；**不能因本文存在自动宣布 Product Freeze、L2 PASS、Task DAG Freeze、实现完成或 Version Release PASS**。Draft PR [#1101](https://github.com/kaicreator-mm/ai-development-standard/pull/1101) 是当前候选实现入口。Frozen v4.11 历史和采用该版本的项目保持原合法流程。

**Product authority / scope provenance**
- 主规划 [#1096](https://github.com/kaicreator-mm/ai-development-standard/issues/1096)；三图关系 [#1100](https://github.com/kaicreator-mm/ai-development-standard/issues/1100)；风险价值 [#1099](https://github.com/kaicreator-mm/ai-development-standard/issues/1099)。
- [v4.12 范围统一说明](../../references/v4.12/V412_PRODUCT_SCOPE_CONSOLIDATED_R0.md)；[首版机制决策 v0.1](../../references/v4.12/V412_INITIAL_POLICY_DECISIONS_V01.md)；[C01–C15 候选契约](../../references/v4.12/V412_CROSS_STAGE_CONTRACTS_CANDIDATE.md)；[作者主导静态对抗自审](../../references/v4.12/V412_ADVERSARIAL_REVIEW_R0.md)。
- Current normative owner baseline: `standards/DEVELOPMENT_WORKFLOW.md`, `L1_PRODUCT_EVIDENCE.md`, `L2_ARCHITECTURE_EVIDENCE.md`, `TASK_DECOMPOSITION_STANDARD.md`, `TASK_DAG_GOVERNANCE_STANDARD.md`, `GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `EXECUTION_ARCHITECTURE_STANDARD.md`, `PROJECT_ADOPTION.md`, `VALIDATION_STANDARD.md`, `RELEASE_STANDARD.md` at approved version pin. Specific v4.12 normative placement only after Product/L2 approval; this document is not a parallel standard.

## 1. Product problem, users and success

**Problem:** Current ADS has sound Product/L2/Task/Review/Release authority, but large or parallel AI projects frequently overproduce research/Demos, split Tasks badly (oversized or overly tiny), create ad-hoc contracts in parallel branches, leave module-to-entrypoint integration late, repeat Review/real-host validation without novel proof, lose source/evidence currentness, and struggle with task continuity and high human/Build Host cost. A stage-complete-looking project can still have no qualified usable delivery.

**Users:** Product Authority, Architect/L2 owner, planning Agent, Builder, Reviewer, Validator, Controller/Project Steward, human authorized actor and maintainers of existing ADS-based projects. Adoption spans WEB-only, local, Build Host and mixed. No universal compulsory backend/LLM/model/OS/CI vendor.

**Outcome:** Minimize total *lawful* time and cost to deliver a source-accurate, actually functioning, release-eligible increment; uphold existing safety/rights/security/privacy/compatibility/Review/Validation/Release authority. Measure authentic convergence and material defect reduction rather than number of tasks/reviews/studies generated.

**Product success (measurable with available evidence, not fabricated numerical claims):**
- A new substantive multi-module project can go from frozen L2 to a **buildable right-sized Scaffold + frozen Implementation DAG**, with source-true Task/contract ownership and no illegal feature implementation during planning.
- A mature project can **reuse** its existing structure and use compact planning; a small Fast Path produces no empty DAG/scaffold/extra gate.
- Task/Scaffold shared-write collisions, missing integration routes, stale pairs and NotImplemented→PASS misclassification are caught by bounded checks.
- Owner-correct delegated work can be reconstructed from GitHub alone after context loss; no parallel scheduler/gate DB.
- Real blockers, source drift, artificial Issue/Review/Host expansion and optional-work starvation can be surfaced, legally routed and stopped.
- Applicable mandatory assurance is preserved; exact released version truth never inferred from PR/task/model/CI PASS alone.

## 2. Scope and five workstreams

| Workstream | In-scope user-visible ability | Out of scope / authority preserved |
|---|---|---|
| **W1 Adaptive Work Graph** | Conditional P/A research graphs, implementation planning, per-stage depth/risk routing, DAG/Scaffold paired freeze, source/Task trace and safe Task split/replan | No second graph scheduler, mandatory three DAG files, 1-file/1-interface Task or fake GitHub Dependency mutation |
| **W2 Project Steward** | Read-only observability on version progress, real blockers, accepted Claims, critical path, stale proofs, Review conflicts, merge drain and suggested recovery with confirmed readback | No second Controller, autonomous Claim steal, review authority, manufactured blockers |
| **W3 Environment Lifecycle** | Source/role/tenant-bound capability declaration, preflight, real execution/resource eligibility, cleanup and evidence, reuse of existing WEB/LOCAL/CI/E3 facilities | No fake multi-platform obligation, permanent environment service or fabricated E3 |
| **W4 Task Outcome & Learning** | Source-bound Task Result + relevant Metadata; costs/negative outcomes/root causes/reusable patterns; future planning and actual cost adjustment | No new Task Learning truth DB, forced two output files or self-amending normative standard |
| **W5 Research, Reuse & Quality** | Existing L1/L2 evidence and working code reuse, licenced public human reports where suitable, bounded Demo, reusable code/tests/helpers, stronger source/contract/critical journey alignment | No mandatory crawler, endless experiment tooling, blanket human Gold substitution, no unlicensed data or unbounded abstraction framework |

Cross-cutting: **Risk-Bounded Value First**: prefer CORE/material value, remove speculative periphery before Freeze, reuse existing proof when truly equivalent; non-negotiable source-owner trust/human/security/required tests/negative scenarios/release floors prevail.

### 2.1 v4.12 delivery priority — no all-workstream mandate

| Priority | Concrete acceptance-bearing product delta | Completion boundary |
|---|---|---|
| **P0 · required version core** | **FR-01** phase graph/authority applicability; **FR-03** prospective Scaffold Planning and paired Freeze; **FR-04** single-source GitHub bidirectional mapping and minimum deterministic consistency; **FR-05** owner-safe contracts/Task DAG/CI/readback; no-regression with v4.11 pins | Normative owner projection and focused negative conformance on representative new + existing project cases, **not** building five services |
| **P1 · bounded integration** | **FR-02/06/07** risk/human evidence routing, read-only Steward observational workflow, environment preflight/recovery, source-bound Task Learning and bounded phase stop, preferably expressed through **existing** mechanisms | Evidence-backed smallest useful delta, preserve actual owner state/CLAIM/Review/Release; no new always-on service or independent human campaign |
| **P2 · conditional / defer** | Rich GUI, always-running Steward daemon, automated cross-repo risk optimizer, universal full-codebase map, large sampling/cost/LLM benchmark, extra OS/device runner matrix | Do not gate v4.12 release absent an actual higher-owner material requirement; create future proposal only with evidence |

**P0 does not mean every subfeature must be written from scratch.** Reconciliation must first classify existing v4.11 owner implementation `ALREADY_SATISFIED | BOUNDED_DELTA | NOT_APPLICABLE | DEFER` with exact source evidence. Review/Validation/Release floor remains what the existing source owner actually requires.

## 3. FR-01 — Three phase-scoped graphs and stage authority

1. Keep semantic `L1 Product Evidence → PRD → Product Freeze`, `L2 Architecture Evidence/Decision → L2 Freeze`, `Implementation Task DAG → per-Task L3/implementation → Version Closure/Release`. `DAG-P` (L1) and `DAG-A` (L2) are **optional coordination views**; `DAG-I` is the actual substantive version implementation DAG **planned after L2** and completed with its Scaffold.
2. For **each** phase independently select `INLINE | BOUNDED_WORKLIST | EXPLICIT_DAG` based on material unknowns, real dependent ownable work, evidence reuse, risks, coordination and cost. No “all phases heavy” implication.
3. Product research observes a Product question, Architecture Demo an L2 hypothesis and Task test a production concern; these reports never inherit Freeze/Release authority. L1 can use bounded **product-purpose feasibility probes**, without pre-freezing architectural choice or production behavior.
4. Separate `BLOCKED_BY` from `INFORMS / CONSUMES / SUPERSEDES / RELATED_TO`. The actual materialized implementation `blocked_by` graph is **GitHub native Issue Dependencies**, not imports or Markdown. No new state vocabulary or mandatory P/A Issue graph.

**AC-01:** At least one simple Fast Path uses inline P/A and no synthetic nodes; one multi-study L1 has genuine dependent graph/stopping; one real Architecture UNKNOWN has bounded Demo; a nondependent module import is NOT a native Task blocked-by edge.

## 4. FR-02 — Adaptive assurance and minimum-human evidence

1. Risk/consequence and uncertainty are **orthogonal**. `EXPLORATORY` can coexist with `HIGH_ASSURANCE`; neither is a single ordered severity ladder. `FAST` / `STANDARD` choose lawful ceremony/assurance, never weaken owner hard floors.
2. Determine scope/phase profile from real Product consequence, Trust/rights, needed negative proof, current/old evidence, write collision, critical path, environment fidelity and expected **incremental decision value**; record reason/owner/known unknown only where material.
3. For **reserved human judgment**, use bounded multi-LLM adversarial critique (when useful), deterministic tools on machine-verifiable predicates, then only the legitimate minimal human decision/evidence that current policy requires. Never assume model consensus = real human, Fresh Independent Review or approval.
4. For **real human behavior claims**, first examine lawfully usable prior research, permitted community/self-report, authenticated public traces and authorized telemetry; disclose selection/robot/duplication/population/region/time/privacy/provider-access biases. Public complaint ≠ measured prevalence or controlled real UX task completion.
5. AI-authored candidate Gold plus human spot-check is **hybrid evidence**, not independently human-authored blind Gold. Retain real consent/DENY/independent actors when specific method or law requires them; changes to frozen protocols need Product/Study authority, not rhetorical reclassification.

**AC-02:** Machine-complete low-risk scope has zero ceremonial extra human meetings; a real DENY cannot be overridden by three agreeing LLMs; public posts cannot prove population percentage or blind Gold; unauthorised scraping/model upload is rejected; unknown risk cannot select FAST silently.

## 5. FR-03 — Scaffold planning, Task DAG co-evolution and paired Freeze

**User-selected Product behavior:** After legitimate Product and L2 Freeze, the planning owner **may create a right-sized brand-new project Scaffold** (`NEW_PROJECT_INIT`) *before the full Implementation Task DAG Freeze* and progressively enrich **the same project** while drafting the DAG. For mature projects, reuse current checked-in source with only necessary seam additions (`EXISTING_PROJECT_ADAPT`). **Creating planning-stage engineering files is a legitimate planning deliverable**, not “editing an already frozen implementation”, and does **not** require an extra Bootstrap human approval gate.

1. Eligible Scaffold Planning scope: repo/package/module skeleton, contracts/API/schema/type definitions, capability/package manifest, mock/stub marked unimplemented, build/import/export entrypoints, configuration/lockfile, structural composition interfaces, focused contract/negative-smoke fixtures. No speculative framework or full feature implementation to manufacture early green tests.
2. Repo writer must have real GitHub source/write permissions and a scoped responsible planning role, exact Product/L2/version pin, declared allowed/new/write paths, identifiable commits/PR and bounded concurrent writer coordination. Existing Claim/Controller rules apply when protected concurrent claims are actually involved; **do not create a duplicate bootstrap workflow/approver/Gate**.
3. **Separate artifact creation from executable effects.** The permitted `NEW_PROJECT_INIT` operation may create source/config/lock/test/build files within assigned scope, but **file creation is not automatic authorization to execute arbitrary generators, package installation/postinstall scripts, CI hooks, network/registry calls, credential access, remote resource creation or real data mutations**. A selected local deterministic compile/import/contract smoke is lawful only under the existing eligible environment and tool policy; its actual processes, transitive hooks, network and side effects must be appropriately bounded, observed, and attributed. Unknown or protected execution effects require existing owner disposition before execution, **not a new universal human Bootstrap gate**. No planning license to perform irreversible external effects, persist/migrate business data, broaden a security boundary or implement materially promised runtime behavior without proper Feature Task and original Trust/Product/L2 authority.
4. Iteration `Scaffold S0 ↔ DAG D0 → ... → SF↔DF` adds only the module seams/tests/wiring needed to make a planned independently valid concern executable and avoid shared-write collision. Preserve genuine atomic contract/invariant Tasks; no one-interface-one-Task rule.
5. **Paired Freeze requires three-way semantic consistency:** (i) **Frozen Product acceptance + L2 invariants/public ABI, error/trust/data semantics**, (ii) accepted integrated **Scaffold material contracts/source**, and (iii) **Draft Task DAG concerns, write owners, intended consumers, negative/integration tests** must all agree. Agreement between Scaffold and DAG alone is not enough: a material change to Product promises or Frozen L2 public contracts must receive the relevant existing owner's lawful amendment **before** paired acceptance. Private structural elaboration within Frozen L2 can evolve normally. **Freeze identity must be cycle-free**: bind accepted immutable `scaffold_source_commit + versioned material_scaffold_scope/tree_hash + dag_checkpoint + mapping_input_digest_or_ref + Frozen_Product/L2 refs`; exclude the generated mapping output and freeze record **from their own input digest**. Material Scaffold scope covers not just `src/` but relevant contract/build/test/manifest/lock/config/CI inputs. A DAG-doc-only successor commit may change HEAD without invalidating unchanged material Scaffold scope; any material covered drift requires affected recheck. This is one coordinated planning checkpoint, **not** a third authority or an impossible identical-commit-SHA condition.
6. Existing v4.11 pin retains its existing source ordering (e.g. authorized T00 after ordinary DAG); v4.12 must **prospectively express this stage-specific planning permission in existing Development Workflow and GitHub source-writer owners** before implementation under the new revision.

**AC-03:** (a) New-project directory/contracts/tests can be created lawfully under v4.12 planning role with no extra human Gate; (b) `package.json` may be created but a malicious/unknown `postinstall` or real cloud side effect may **not** be run merely because files were created; (c) intentionally mismatched **Frozen L2 public semantics versus mutually matching Scaffold+DAG** blocks paired Freeze; (d) derived-index self-hash and docs-only HEAD drift cannot yield false freeze/invalidations; (e) missing integrated source/stale map/schema or shared mutable writer prevents pair acceptance; (f) a scaffold stub is `NOT_IMPLEMENTED`; (g) existing project keeps stable structure; (h) old pin not retroactively altered.

## 6. FR-04 — GitHub-native bidirectional Scaffold ↔ Task mapping

1. Use **GitHub Git objects and existing planning files/Issue/PR authority** as the only durable primary source. For material anchors, store stable `anchor_id`, type, actual project path or Package/Capability ID, Source/L2 contract ref and ownership/lifecycle; in planned DAG Task record `scaffold_bindings=[{anchor_id, relation, scope}]`. Relations: `IMPLEMENTS | CREATES | MODIFIES | CONSUMES | TESTS | INTEGRATES`.
2. A **single typed many-to-many relation set** produces deterministic forward Task→Scaffold and reverse Scaffold→Task read views; optional `scaffold-task-map.generated.json` is a rebuildable derived artifact, never another manually edited authority or live scheduling truth. The generator **must not ingest/hash its own output or downstream Freeze checkpoint as an input**. Accept only explicit committed versioned source inputs, with scoped manifest/build/test/environment identity and provenance; no unbound current `HEAD` in the generated stable digest.
3. Generator must read **committed, source-current Git inputs**, validate stable IDs/unimplemented/future seams, canonical sort/serialize records with provenance, and generate byte-identical output for same inputs. L2 chooses the lightest implementation (reuse existing manifest/Task Pack rather than force redundant JSON schema).
4. Validation v1 **V01–V12** covers unique IDs, real/pending path identity, material Task/anchor coverage, exclusive writer vs many consumers, no import→blocked-by promotion, Stub-vs-Test PASS, **three-way Frozen Product/L2 semantic compatibility**, cycle-free/scoped exact Scaffold inputs plus DAG checkpoint, **structural wiring ownership vs later functioning user path**, reproducible generation, dynamic Package/Capability IDs, UNKNOWN/fidelity limits.
5. Source changes and new private files after Freeze follow Task write authority/currentness and **only affected** mapping revalidation; actual Task mutation uses existing native GitHub Issue Dependency governance.

**AC-04:** On one new-project and one mature-project case, ADS reference generator produces forward/reverse map from the same committed relation facts, byte-identical for same inputs, and detects duplicate writes, unmatched critical public/semantic contract and absent **structural integration ownership**. The index is non-authoritative and cannot change native Issues/Claim/Review/Gate. Negative cases demonstrate (a) generated index/Freeze self-reference cannot stabilize falsely, (b) DAG-doc-only commit doesn't invalidate unchanged in-scope Scaffold tree, (c) changed lockfile/build/test critical manifest **does** invalidate the material tree, and (d) structural entrypoint smoke ≠ functioning customer behavior. No mandatory per-symbol analyzer or universal requirement to run that generator in an A0/A1 adopting project.

## 7. FR-05 — Task execution, boundaries, code reuse, review and closure

1. One Task = one **coherent concern or invariant**, with real allowed write set, inputs, acceptance, negative tests and integration owner. **Builder conduct:** boundedly inspect current shared contracts, helpers/functions, tests and existing owner modules **before** adding duplicate code; choose `REUSE_EXISTING | ADAPT_IN_SCOPE | EXTRACT_PRIVATE | PROPOSE_SHARED_OWNER_CHANGE | IMPLEMENT_LOCAL | DEFER_REFACTOR`. Extract only when semantics/failure paths really match and maintainability improves; do not create speculative utility classes or catch-all `utils/common`. **Reviewer conduct:** assess actual duplicate behavior, incorrect/harmful abstraction and scope/write-set drift, but do not mint independent refactor blocker/Issue absent material source-owner cause. Existing code-quality owners remain normative.
2. Contract/Core/Adapter/Workflow/UI/Integration/Validation Tasks may form real dependencies; a shared central composition root has an identified single owner. Reuse existing mature source/research before adding code. **Two distinct evidence predicates must not collapse:** `SCAFFOLD_STRUCTURE_WIRED` = named import/registration/composition/test seams structurally connect and honest `NOT_IMPLEMENTED` failures remain; this can support paired planning Freeze **only**. `FEATURE_USER_PATH_REACHABLE` = post-implementation Core/Adapter/Workflow/UI/CLI actually fulfills the Product-facing path on its exact candidate with required negative proofs; **only applicable feature/integration/Release owners can attest this**. The first never implies the second.
3. Builder/reviewer use source-bound PR and deterministic tests; select `required | recommended | not-required` Review under applicable policy per Task; no mandatory three-LLM rounds or independent-human actor on all low-risk PRs.
4. Material Task expansion/split after Freeze follows existing Task DAG Governance, native readback and protected accepted Claim restrictions; do not duplicate an ACTIVE worker. Repeated Review/Host rechecks must have new source subject or genuinely required proof predicate; group same-root-cause repairs.
5. Public API/schema/trust/data-contract changes require owning architecture/compatibility amendment and selective impacted consumer re-evaluation; Product promise change needs Product authority. Ordinary private implementation edits aren't automatically HIGH_ASSURANCE. High consequence security/irreversible/tenant/data integrity requires existing mandatory strengthened proof.
6. **PR/Task PASS ≠ Version Release PASS.** Version selected full regression, material CJ/real E3, Hidden, candidate currentness, qualification and release are owned independently per applicable source/gate×subject, never inferred from scaffold mapping.

**AC-05:** Oversized independent Task safely split; genuinely atomic security concern kept coherent; READY→Claim not duplicated during reroute; **Scaffold structure registration** is verifiable without early feature work, while **post-implementation real user path** is proven separately on the applicable exact candidate; a same-semantic helper is reused rather than gratuitously duplicated, and a materially different policy helper is **not** wrongly unified. Unchanged-scoped PR doesn't trigger unrelated full Host jobs; missing E3 or Hidden remains NOT_RUN/blocked, not PASS.

## 8. FR-06 — Project Steward and Environment Lifecycle

**Steward** reads accepted GitHub/Issue/PR/Claim/source/Review/Validation records and reports `subject, exact provenance, observed symptom, real blocking authority (or advisory), cost/critical path, eligible owning action, recheck evidence`. It may suggest reroute, root-cause work, merge-drain, stop optional work, missing proof recovery and owner decisions. Only existing Controller/Product/L2/Human/Gate authority may perform consequential mutations. Readback is required; mere open advisory Issue is not a merge blocker.

**Environment** identifies WEB, local, Build Host, CI, E3/physical/external/deployment needs only where material; `requirements → prepare → real preflight → authorized allocate/execute → observe → cleanup`. Preflight isn't Claim authority; failed or unknown ACK needs reconciliation before duplicate effects. Dynamic capability, toolchain, secrets/rights and real exit code/skips/source identity are preserved; fake/mocked E1 doesn't assert real E3.

**AC-06:** One **source-backed real** READY stall is reported without synthetic blocker; a legitimate eligible Controller/owner action unblocks and **canonical readback** detects actual result, or records `BLOCKED/UNKNOWN` when no eligible actor/action is available. A fabricated READY is rejected. Actual environment preflight/command exit/cleanup result (including failure/UNKNOWN) is recorded under existing evidence owner; a disconnected Real Host stays NOT_RUN, and protected Claim is not stolen merely because a lease elapsed. No always-on Steward required for WEB-only adoption.

## 9. FR-07 — Task Learning, source-evidence economy and adaptive convergence

Each meaningful Task may produce **Task Result** and **Task Metadata** *logically*, not necessarily two files. Metadata contains real duration or UNKNOWN, failures, root cause, source/host/runner, Review/validation churn, what was excluded and why, and evidence strength `PROVEN | SUPPORTED | HYPOTHESIS`. Uninformative trivial Task may record `TASK_LEARNING=NONE_MATERIAL`. Reusable scripts/fixtures/recipes stay project-local until source evidence supports broader ADS adoption; no self-generated policy amendment/PASS.

Cross-phase Product and L2 studies reuse existing evidence with source/time/subject/fidelity/license limits; Demo only for a high-impact unresolved Architecture UNKNOWN not answerable with current static sources. Per phase/concern use **explicit stop/sufficiency/negative** and total cost of Build + Review + Validation + waiting + rework + environment. Low ROI removes only lawfully optional scope **before Freeze** or via correct prospective owner amendment; never drops mandatory proof retroactively.

**AC-07:** L1 study stops once an authorized bounded Product decision is evidence-supported; no endless demo tooling; Task Learning source/provenance and `PROVEN/SUPPORTED/HYPOTHESIS/UNKNOWN` remain honest and cannot fabricate Release authority. Savings or review-round reductions are reported as **observed** only with actual comparable source-scoped baseline/denominator, otherwise `UNKNOWN` and hypotheses; no mandatory numeric savings threshold or unbounded new benchmark.

## 10. Adoption, compatibility, rollout and delivery slicing

- **Pin-first**: current project ADS version+commit SHA and already Frozen Product/L2/DAG/Release history remain unchanged unless project explicitly upgrades through existing adoption owner. **Distinguish ADS's version implementation obligations from adopter capabilities:** v4.12's own P0 deliverable includes a tested deterministic reference mapping generator/checker and negative fixtures. Projects at **A0/A1** may record the same material GitHub source identities/links and perform honest **manual** consistency checks, with no assertion of `MACHINE_VERIFIED`; **A2+** claims to have verified adopted machine records require actual eligible script/schema execution. All levels retain equal trust/currentness/gate floors; A0/A1 WEB/manual path must stay legal. v4.12 does not require new services/CI/device/graph database/locally installed LLM.
- **Minimum viable v4.12 requirements**: policy wording/projection for conditional graphs, scoped Scaffold Planning permission, exact paired currentness + GitHub mapping/generator/checker with fixtures, existing controller/readback hook and owner alignment. Build only the missing normative delta; reuse existing v4.11 Claim/Assurance/Task Learning/Review/Release semantics with exact evidence.
- **Conditional extensions**: automated Steward monitoring, richer environment scheduling, telemetry-driven risk selection, extra mapping tooling only if real Source Owner/ROI evidence proves necessity. No release-blocking blanket platform matrix or unbounded human study.
- **Implementation organization**: one concern/PR, default early merge to authorized main/integration base after correct Task gates, bounded independent tasks before central wiring. Pairwise Scaffold/DAG Freeze belongs to **development planning**, not Version Candidate Freeze/Release.
- **Product acceptance demos to include at minimum**: new project case (app8/shun-style contract-first), mature source case (runx central wiring), dynamic Package case (domain-harness), previously built-unreachable user capability (xDownload); consume existing Issue/source evidence first. Do not claim running these v4.12 new checks until actually executed.

## 11. Product non-goals and rules of proportionality

**NOT in v4.12:** new general LLM gateway, duplicate DAG/Claim/Review/Release authority, separate compulsory graph or learning DB, single giant autonomous orchestrator, all-stage DAG always, mandatory codegen on mature project, every interface=Task, blanket HIGH_ASSURANCE for contract-neutral edits, mandatory multi-model/human approval for all PRs, global source-symbol graph, mandatory real Host per Task, automatic scraping from prohibited sources, public forum posts as measured UX/Gold, large benchmark/human review program added merely to achieve a ceremony count, cross-project retroactive migration, or fabricated quantified ROI.

Mandatory gates/negative branches from current trusted Product/Architecture/Trust/Human/Assurance/Release owners are never skipped merely because they're expensive or rare.

## 12. Product-to-L2 handoff — decisions *not* blocking PRD freeze

These are **technical design/projection questions**, with chosen product constraints; do not reopen L1 to research indefinitely:
1. Smallest prospective `PLANNING_SCAFFOLD` source writer/role/scope/currentness representation within existing GitHub Work Item/Claim rules, including rejection of out-of-scope feature effects. No new human Gate.
2. L2 choice of an existing manifest/Task Pack projection for anchor/bindings, deterministic generator/checker and JSON optional representation; stable IDs under rename, dynamic plugin/Package.
3. Exact paired SF source/tree and DF DAG checkpoint binding across docs-only commits, currentness/merge/rebase and native Issue dependency readback.
4. Cheapest P/A Worklist/Issue materialization with no second schedule authority.
5. Steward report source, when/how it runs on WEB/LOCAL and lawful Controller correction/readback.
6. Environment resource preflight/allocation/cleanup and protected private/human evidence references using existing owners.
7. Exact code/test changes only where owner reconciliation confirms a material gap; cost metrics obtained from actual tasks, not invented thresholds.

**Source precedence for this review candidate:** exact **reviewed/frozen PRD Product scope** (once actually Frozen) > expressly **adopted** decisions v0.1 scoped by that PRD > current non-normative C01–C15 candidate notes for technical background > historical/superseded author red-team reports for provenance only. **All remain subordinate to the project's pinned existing normative authority until prospective v4.12 approval/adoption**; report prose/old review status does not override actual owner. 

**If a purported L2 detail changes Product promises, protected human rights, source-owner authority or introduces a mandatory gate/major adoption burden, route a targeted Product amendment.** Otherwise proceed to L2 with bounded alternatives and an exact owner.

## 13. PRD Freeze readiness/Review packet (not signed)

```ini
PRD_CANDIDATE=R2
PRODUCT_VERSION=v4.12.0
SOURCE_PIN=v4.11.0_BASELINE_FOR_OWNER_RECONCILIATION
INTAKE=#1096
PHASE=PRODUCT_REVIEW_CANDIDATE
PRODUCT_SCOPE_DECISIONS=FR01-FR07_DOCUMENTED
BOOTSTRAP_PLANNING_PERMISSION=YES_PROSPECTIVE
EXTRA_BOOTSTRAP_HUMAN_GATE=NO
GITHUB_MAPPING=ONE_DURABLE_RELATION_TWO_GENERATED_VIEWS
PAIR_FREEZE=SF_SOURCE_TREE_PLUS_DF_DAG_CHECKPOINT
AUTHORITY_WEAKENING=FORBIDDEN
PRODUCT_REVIEW=EXTERNAL_REPORTS_NOT_VERIFIED_IN_CURRENT_CONTEXT;NEW_R2_INDEPENDENT_REVIEW_NOT_RUN
PRODUCT_FREEZE=NOT_RECORDED
L2=NOT_STARTED
IMPLEMENTATION_DAG=NOT_FROZEN
FUNCTIONAL_CONFORMANCE=NOT_RUN
SELF_R1_FINDINGS=5_P1+4_P2_ADDRESSED_IN_R2_TEXT
INDEPENDENT_CHATGPT_AND_CLAUDE_REPORTS=NOT_RETRIEVED_OR_ADJUDICATED
```

**Ready-for-review checks (no fake PASS):** exact candidate PRD blob; provenance to #1096/#1099/#1100/C01–C15; no historical v4.11 rewrite; no new authority/gate escalation; acceptance AC01–AC07 grounded and falsifiable; legal new-project versus existing-project differential; compatibility/adoption floors preserved; cost/Research boundaries non-circular; negative Owner/Host/Human/Release cases not waived. This Draft may proceed to **one bounded Product Review according to applicable policy**. Explicit Product Freeze is a separate Product Authority decision on that exact reviewed candidate. A Product Review finding must be dispositioned before declaring eligibility; L2 and Implementation Task DAG follow only after proper Product/Architecture ownership.

**Exit if accepted later:** Product Authority records `PRODUCT_FREEZE=PASS` on exact PRD/L1/source ref and identifies the approved normative delta and L2 owner. This document itself makes **no such assertion**.
