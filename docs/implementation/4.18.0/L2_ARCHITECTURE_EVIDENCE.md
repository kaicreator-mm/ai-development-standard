# ADS v4.18.0 — L2 Architecture Evidence R1 (independent R2 review candidate)

**State:** L2_R1_AUTHOR_REPAIR / INDEPENDENT_L2_R1_CHANGES_REQUESTED_P1_3_P2_3 / INDEPENDENT_L2_R2_NOT_RUN / L2_FREEZE_NO / NATIVE_TASK_DAG_NOT_ADMITTED / SOURCE_IMPLEMENTATION_NOT_AUTHORIZED.  
**Independent L2 R1:** [#1321@6388900470](https://github.com/kaicreator-mm/ai-development-standard/issues/1321#issuecomment-6388900470); P0=0/P1=3/P2=3/P3=2; R1 repairs below are author claims subject to distinct exact-blob R2 review.  
**Source branch:** version/v4.18.  
**Exact frozen Product:** PRD source commit 858d48304500797ff6a759440f13f17c73f8eef2; docs/implementation/4.18.0/PRD.md Git blob 98772b4594caa44b2611853ae482132f7aefa36b.  
**Product authority:** [#1320 Product Freeze #6388802387](https://github.com/kaicreator-mm/ai-development-standard/issues/1320#issuecomment-6388802387), following independent [Product R2 PASS #6388769719](https://github.com/kaicreator-mm/ai-development-standard/issues/1320#issuecomment-6388769719).  
**Predecessor baseline:** main@a45644d734fdf94da3e6f9c3f90ffe4ce3c25fda (v4.17 standards-source conditionally qualified; historical RA02 NOT_APPLICABLE, not PASS).  
**Scope:** Implement the minimal v4.18 TRUE_GAP standards-source design without inventing a second DAG, Task readiness, runtime Agent service or mandatory new Gate.

## 1. Architecture problem, alternatives and decision

### Goal and irreducible invariants

Improve the Product→L2→Scaffold/Task DAG planning outcome: derive distinct capabilities before concerns; detect avoidable serial bottlenecks; compare safe alternative DAG topologies; use existing structural SF↔DF truth to improve planning; include per-Lane Agent/environment/independence/handoff fit. Keep normal Task/Claim/JIT/Review/Validation/Release truth unchanged.

Non-negotiable:
1. Frozen Product/L2, accepted Source Scaffold/DF/MI and GitHub native Issue dependencies retain existing authority.
2. Dependency-reason notes, alternative DAGs and Lane summaries NEVER change ready_builder, native blocked_by or permit an earlier source write.
3. One effective writing concern per owned write-set/Scaffold Anchor, plus actual Claim key and shared-resource constraints, not just one per-task claim key.
4. No automatic human APPROVE, self-review, fake Host PASS, release waiver or retrospective rewrite of v4.17.
5. A standards-source Golden proves only bounded E1 textual/conformance consistency; not real multi-agent execution, physical validation or economic benefit.

### Considered designs

| Candidate | Architectural effect | Ruling |
| --- | --- | --- |
| A. Another scheduler/Task DAG with merge-only dependency type | Introduces shadow edge/readiness semantics and conflicting Claims | REJECT (Product R1 Option A) |
| B. Rewrite Workflow/Execution/Agent/Human standards in many files | Duplicates mature owners, increases cross-file collision, creates false new gates | REJECT |
| C. Minimal owner delta + richer existing DAG planning template + small source-only Golden cases | Reuses real GitHub DAG and SF/DF, focuses on testable gap | SELECT |
| D. No normative change; examples only | Cannot consistently demand planner alternative-topology assessment | REJECT for FR-04 true gap |

**L2-D01 (proposed):** select C. Source changes only where a true gap remains after reviewing current inherited owners. P0 outcomes marked ALREADY_COVERED close by exact owner+Git blob and bounded Golden evidence, not by rewriting standards. The optional Pattern guidance is non-authoritative and cannot be a new Gate.

## 2. Effective-source owner inventory and FR disposition

All source blobs below are existing current main owners inspected for Product R1/R2 or L2 owner discovery. Before any implementation Task dispatch, re-read effective exact candidate owner source and verify no intervening amendment:

| Source / responsibility | Pin / version | Expected delta |
| --- | --- | --- |
| standards/TASK_DECOMPOSITION_STANDARD.md (concern, atomicity, real dependency, central wiring) | a7c3195a89b39ecbc13276f181070b67586feb8c | Only 1–2 narrow SHOULD clauses in existing §13 for bounded alternate topology / reason annotation; avoid a new appendix or rewrites of §§4–14 |
| templates/task-dag.md (existing Lane planning authority-as-template) | d136fcbb472c8d5ba126264550d6dc63345ad171 | Compact pre-Freeze requirement/concern trace, candidate topology/serial rationale, advisory dependency motives, SF feedback and Agent capability/role/handoff cells |
| standards/TASK_DAG_GOVERNANCE_STANDARD.md §10A (accepted SF/DF/MI owner) | d1ce81f9b66b6b9d9b7005928609a55a0f3d8b94 | NO normative change; refer to it; test only approved SF/DF/MI semantics |
| standards/EXECUTION_ARCHITECTURE_STANDARD.md §6/§11/§19/§23.4/§27.3 | 1f1601a20db08d263955241607dfd08d8b8f77e1 | NO source change unless independent L2 shows necessary true conflict; Option A preserves JIT/readiness/Claim |
| standards/DEVELOPMENT_WORKFLOW.md §2.4/§2.4A/§4/§9 | 8d14b25dff70991b07d6ea2d963c86bf0e5a6286 | NO duplicate stage/source admission changes |
| standards/MODEL_USAGE_POLICY.md | 79b3590c7fe4b0b085ed346cbac9e24509e7fa66 | NO model-routing change; per-Lane candidate capability is advisory |
| standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md §3/§8/§9 | dd4f3fcadf38263f4f5cf99739d41d1c0a0bd847 | NO new handoff schema; existing remaining-work handoff sufficient pending counterexample |
| standards/PROJECT_STRUCTURE.md §1/§4 | 525380339dd25f6520202f859cfa41db635c1189 | NO Monorepo policy change |
| standards/ARCHITECTURE_DESIGN_STANDARD.md | 19ba240a15016f8381989f20f20d6d5443c4e716 | NO second design authority |
| references/TASK_DECOMPOSITION_REFERENCE.md (current task decomposition Golden + Forbidden home) | 223b05d8c59e26b10ba888908b2a9dfc3c36e679 | Append optional planning Pattern + G418 source-only paired examples; preserve existing §§1–9 and standard single-owner crosswalk |
| references/TASK_DAG_GOVERNANCE_REFERENCE.md (current DAG/SF guidance) | 62e7cec58f1b5a28e0fae8ea9061a5facfe0c8fa | Reuse unchanged; no new MI/anchor guidance authority |
| templates/golden/STANDARD_COVERAGE.json (canonical normative Golden refs) | 5149d74063433fba6c867bd4bfed015fe0d321c4 | Reuse existing TDS golden_ref/forbidden_ref; no registry change unless exact verifier proves one necessary |
| templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md | 94907154551291342e0b71cca9c823ef89cdbfed | Preserve whole v4.17 G01–G14 definitions and version examples; do NOT duplicate TDS's registered Golden home |
| templates/GOLDEN_INDEX.md | b36d4947cfe7db101e9eb4955ea889b55d988ed1 | Existing index unchanged by default; only central integration owner may alter if verified necessary |
| tests/test_v417_golden_consistency.py | 3d38d39fc2bb22c3302175506b714ca5c26170cd | Must remain byte-identical; run existing G01–G14 regression |
| scripts/test_v411_t13_role_conduct.py | 19f8b55a2757ddc87dc5591bdbe6b15dcbcd0318 | Historical T13 exact-commit TDS/Workflow assertion; already EXIT 1 on main-derived L2 HEAD; retain observed FAIL (do not edit test), NOT_APPLICABLE as new v4.18 exact-owner pin gate subject to RQ owner acceptance |
| scripts/test_v410_t05a_shared_code_safety.py | a0cdc43fa01e55f1ee92209eb7f0fce881032be1 | Historical T05A fixed TDS blob and earlier dual-pin ICGS; already EXIT 1 in source-only reviewer run; retain FAIL, no silent broad 'any SHA' bridge or deletion |
| scripts/test_v43_task_decomposition.py | existing source suite (re-read before Task) | Existing TDS + reference token regression, R1 reviewer reports EXIT 0 /16 OK |
| scripts/test_task_dag_lane_parallelism.py | 1000c2912c76dc5c3df2de6af845c9138d6f5346 | CI template+Workflow token oracle; R1 reviewer reports EXIT 0; must remain green when B edits template |
| scripts/test_work_item_contract_and_golden_templates.py | existing CI oracle (re-read before Task) | Existing template/Golden anchors, reported EXIT 0 /9 |
| scripts/test_v42_adoption_wiring.py | existing wiring oracle (re-read before Task) | STANDARD_COVERAGE golden refs, reported EXIT 0 /8 |
| standard-manifest.json | da85faa21d80f9ec7e61b3f6a6e3cd4bf0061eb4 | Only central I writer registers new test / documentation paths if required |
| .github/workflows/verify-standard.yml | 9fa6099f867b4ce68c0963fbd012f8970753c4d6 | Only central I writer wires the v4.18 targeted test once valid and qualified |
| .github/workflows/verify-github-structured-interaction.yml | 1e1f364846e9bc15ae9161136c924120fe49e34a | No change unless integration evidence shows necessary, central I only |
| scripts/run_v410_integration.py | 0db8cdf4a65da6039624682bd08dbe414471b0eb | Historical runner includes T05A; its observed old-blob FAILURE stays visible; not a current-version all-green claim |
| standards/RELEASE_STANDARD.md | da3b78b113be238bdce650ccb646f5aa23bc1f9b | No Release gate waiver; applicability of historical suites must be challenged at RQ |

FR owner decisions (proposed for independent L2 adjudication):

| FR | Disposition | Source delivery |
| --- | --- | --- |
| FR-01 | ALREADY_COVERED + prompt gap | TDS §3/§9 and TDS Reference §§2/§7/§9 cover concern/lane/dispatch; add capability-before-concern / Step-is-not-Issue prompt only |
| FR-02 | ALREADY_COVERED | Reference owner; do not rewrite |
| FR-03 | PARTIAL / TRUE_GAP_SMALL | TDS Reference §§2/§5/§7 already cover parallel split/central wiring; only additive pattern alternatives + bounded counterexamples in the same Reference |
| FR-04 | TRUE_GAP | Comparison of actual DAG topologies, reason annotations and ordinal path/serial justification |
| FR-05 | TRUE_GAP_SMALL | Pre-Freeze Scaffold-aware feedback in existing Lane template; SF/DF/MI unchanged |
| FR-06 | ALREADY_COVERED | Task Decomp/Project Structure/DAG Governance |
| FR-07 | ALREADY_COVERED + Golden negative | Product Option A; no prospective merge-only native edge |
| FR-08 | PARTIAL / TRUE_GAP_SMALL | TDS Reference §9 already has Agent dispatch facts; only compact WEB/CI/LOCAL and independence/capability cells in existing Lane template |
| FR-09 | ALREADY_COVERED + example | Existing GAIP/Exec/Model Usage |
| FR-10 | ALREADY_COVERED subject to counterexample | LAH §3/§8–9 and Exec §23.4; no second tuple/schema by default |
| FR-11, FR-12 | ALREADY_COVERED | Existing Human authority, escalation/assistance patterns |
| FR-13, FR-14 | IMPLEMENTATION_ONLY | Reuse TDS Reference §§2/§7 as host; one optional advisory subsection there, not duplicate STANDARD_CONFORMANCE_EXAMPLES |
| FR-15 | TRUE_GAP_SMALL | Non-gating topology quality checklist; no universal score |
| FR-16 | DEFER/ALREADY_COVERED | Workflow §8; external telemetry owner independently decided |

**L2-D02 (R1 proposal):** A edits only a **minimal one/two-sentence SHOULD in TDS §13** (alternative safe topology vs bounded serial justification, advisory reasons with native DAG/Claim unchanged); B edits the existing task-dag Lane template; C adds optional Patterns / positive-forbidden G418 examples to the already registered **references/TASK_DECOMPOSITION_REFERENCE.md** plus a separate runnable E1 v4.18 test. I solely owns central `standard-manifest.json`, `.github/workflows/verify-standard.yml`, any necessary Golden coverage/index wiring and integrated source test hook. R solely owns `VERSION`, `CHANGELOG.md`, `README.md` and version Release facts. Do not edit v4.17 G01–G14, their historical source-only test, strict public Schemas, v4.10/v4.11 fixed-subject tests, Execution Architecture, Workflow, Agent/Human authority or v4.17 release records.

**L2-D02a — reviewer P1-1 regression disposition (proposed owner decision, NOT a result waiver):** R1 Reviewer [#1321@6388900470](https://github.com/kaicreator-mm/ai-development-standard/issues/1321#issuecomment-6388900470) physically observed **2/62 FAIL** in `scripts/test_v411_t13_role_conduct.py` because its test asserts current TDS and Workflow bytes equal a historical commit `869b8a3d…`, and **1/39 FAIL** in `scripts/test_v410_t05a_shared_code_safety.py` because the old pinned TDS blob `f355c020…` is not current. Both existed at unmodified v4.18 L2 R0 HEAD and are therefore **preexisting historical exact-subject identity regressions, not v4.18 source defects**. Choose historical evidence-scoped **NOT_APPLICABLE as a *new v4.18 current-owner equality gate***, preserve actual old test FAIL and frozen pin tests/source bytes, and bind the current-version source validation to existing owner semantic/token/Golden/CI tests plus new targeted v4.18 negative cases. `run_v410_integration.py` invokes T05A and will not be reported green: full-suite outcome must retain observed FAIL, with the impact and this explicit scope disposition sent to the Release owner for independent RQ adjudication; if that owner finds a still-applicable mandatory requirement, RQ stays BLOCKED and a lawful focused Task/amendment is required. Do not silently skip tests, auto-waive an actual v4.18 gate, edit their historical pins or assert all-version regression PASS.

## 3. Contract of the new advisory planning analysis

### 3.1 Input sources

- Frozen Product (current exact PRD/accepted acceptance).
- Frozen L2 contract/module/atomic invariant boundaries.
- Any ACCEPTED source-first Scaffold SF exact Git commit/material view + binding anchor inventory (only where a qualified existing adoption exists).
- Existing concern ownership/allowed and forbidden write sets.
- Real native GitHub blocked_by and current materialized Task/PR/Claim state **once Tasks are materialized**.
- Role capability requirements and real WEB/CI/LOCAL environment constraints.

Planning can compare a candidate unmaterialized DAG on paper; do not report candidate “ready” or “merged” based on draft rows.

### 3.2 Required compact output for substantial Task DAGs only

1. **Capability→Concern→Lane mapping:** which Product outcomes are covered and which local steps do not merit separate Issues.
2. **Dependency rationale:** per important edge, *advisory* classes: upstream integrated code/contract, exclusive writer/anchor, validation/review evidence, merge/release convergence, resource/executor. These classes are comments/analysis only; they **do not change** the native edge meaning or claim/readiness admission.
3. **Topology comparison:** baseline candidate vs one safe alternative if materially serial, or bounded explanation why it must remain serial. Compare structural longest path, legal workfronts, central integration, source collision, rebase/CI/Reviewer/Agent handoff risk. Time/cost UNKNOWN unless independently measured.
4. **SF↔DAG pre-Freeze feedback:** acceptance and path/anchor status, derived independent modules/central write hotspots, suggested L2/Scaffold adjustment before actual Freeze. Frozen SF updates use existing Amendment and separate MI/currentness; absence of SF is NOT_APPLICABLE.
5. **Role/evidence plan:** per Lane candidate WEB/CI/LOCAL capability, builder and independent reviewer/validator role, actual physical evidence needs, source/read-only limitations, handoff recipient and human decision/assistance trigger where relevant.
6. **Integration barrier:** one central wiring owner for shared paths; exact merge/release convergence, prior proof reuse only with currentness/impact check.

These are human-readable sections/columns in **existing** Task DAG template, not new YAML fields or a machine scheduler. No duplication into separate state ledgers. The existing Fast Path may omit extra topology comparison for a single atomic docs/typo correction with no real competing concern, shared writer or material cross-module choice; document the one-sentence rationale instead of generating an obligatory second candidate. This is judgment, not a task-count threshold.

### 3.3 Illegal interpretations (mandatory negative oracle)

- Existing native Task B blocked_by A; a Lane note “merge-only / independently mutable” cannot make B Builder READY while A remains unmet. Must HOLD source until lawful native Task split/new independently admitted concern and Claim. Unverified read-only PREP is not source authority.
- A path/anchor may be structurally separate but absent from frozen L2/accepted SF; it cannot be used to invent a new writer permission.
- Two distinct Task Claim keys can still conflict on a shared Catalog/lockfile/Anchor or real resource. Read actual writer owners and shared-resource admission; do not treat per-key serialization as a cross-Task write-set lock.
- A stronger model, same GitHub login, green CI or Reviewer prose does not create appropriate authorization, independent review, real Host verification, or protected human approval.
- A 10-node longer but legal atomic serial plan may be the only correct answer; do not optimize at expense of invariants.

**L2-D03 (proposed):** Alternative topology and reason labels remain non-authoritative planners' aids. Option A is immutable in this v4.18 Product scope; no relaxation of existing Execution Architecture §6 ready sets or JIT.

## 4. Test and evidence plan

**Validation class:** E1 deterministic source-only conformance (language-neutral Golden/forbidden fixtures, existing verifier and small focused tests); no physical Host or native GitHub graph write/effect is claimed.

### Proposed bounded Golden cases

| ID | Test subject | Expected positive | Expected forbidden |
| --- | --- | --- | --- |
| G418-01 | capability-first planner | independent Capability→Concern→Lane and integrated join | one unreasoned Contract→Core→UI global chain as mandatory topology |
| G418-02 | topology comparison | alternative fan-out with real dependencies preserved, unknown duration admitted | deletes native prerequisite or invents numeric speedup |
| G418-03 | Scaffold-aware pre-Freeze | accepted anchor/contract identifies isolated module + central writer, current MI still handled by §10A | duplicate Anchor writer, fake source or post-Freeze unapproved rewrite |
| G418-04 | agent/handoff fit | role-specific WEB/CI/LOCAL and independent review/remaining physical work | 1:1 Task→Local, fake Host PASS, self-review |
| G418-05 | source-admission separation | native blocked_by remains authoritative; separate lawful precursor Task may claim independently | nonauthoritative “merge-only” annotation makes blocked Builder READY |
| G418-06 | atomic serial case | explicit serial rationale with invariant and proportionate tests | fabricated fan-out which splits transaction/security invariant |
| G418-07 | human boundary | bounded legitimate human decision or physical assistance and legal resumption | human approval inferred from arbitrary text / routine CI polling becomes a new human Gate |

Positive/negative labels are *fixture examples*, not new GitHub review/Claim state names. A compact suite may combine cases; counts are not a universal mandated threshold.

**Golden placement decision (resolves L2 R1 P1-2):** registered TDS Golden home is **references/TASK_DECOMPOSITION_REFERENCE.md** by `templates/golden/STANDARD_COVERAGE.json` (`golden_ref`); existing forbidden rationale is TDS `#10-anti-patterns`. Add one v4.18 optional pattern/conformance section to the **same reference** and a new focused E1 oracle such as `tests/test_v418_planning_conformance.py` (exact path chosen before Issue materialization). `references/TASK_DAG_GOVERNANCE_REFERENCE.md` remains untouched. No new second Golden home in STANDARD_CONFORMANCE_EXAMPLES.md; preserve v4.17 G01–G14 and test bytes exactly. If additional coverage-index references are mechanically necessary, ONLY central I owns them and verifies the existing coverage oracle before accepting.

### Layered evidence matrix

| Proof | Status in this L2 | Required at concern/version implementation |
| --- | --- | --- |
| Existing owner texts, exact blob, contract review | AVAILABLE SOURCE | revalidate currentness at implementation |
| Actual source-only Golden test results | NOT_RUN | execute required scoped validators and record exits |
| Native GitHub dependency mutation/readback of new Task DAG | NOT_RUN | only after L2 Freeze and authorized Task DAG creation |
| Real model/agent collaboration and time savings | NOT_RUN | not v4.18 standards-source release prerequisite; external project scope |
| Real platform/physical/human protected acts | NOT_RUN | never inferred from language-only unit fixtures; existing Gate ownership |
| Whole version integration / Hidden / Critical Journeys / Packaging / RQ | NOT_RUN | decide and execute existing appropriate Release Standard gates at version candidate, no blanket waiver |

### Required seven-suite compatibility matrix (real R1 observations, not author reruns)

| Suite | R1 actual result at L2 R0 | Current-version use / owner |
| --- | --- | --- |
| `scripts/test_v411_t13_role_conduct.py` | EXIT 1, 62 tests, 2 FAIL (historical exact owner identity) | Historical T13 pin remains IMMUTABLE; v4.18 current-owner equality applicability: NOT_APPLICABLE proposal; Release owner must independently challenge |
| `scripts/test_v410_t05a_shared_code_safety.py` | EXIT 1, 39 tests, 1 FAIL (historical TDS blob) | Old T05A exact-subject oracle preserved; run_v410_integration impact recorded; not an all-green claim |
| `scripts/test_v43_task_decomposition.py` | EXIT 0, 16 tests | A + C required scoped regression |
| `scripts/test_task_dag_lane_parallelism.py` | EXIT 0 | B **required workflow-wired** regression; retain required lane tokens and Workflow `- parallelism；` + native-DAG owner text, avoid forbidden lane words |
| `scripts/test_work_item_contract_and_golden_templates.py` | EXIT 0, 9 tests | B/C/I targeted Golden/Issue template coverage |
| `scripts/test_v42_adoption_wiring.py` | EXIT 0, 8 tests | C/I exact STANDARD_COVERAGE references and anchors |
| `tests/test_v417_golden_consistency.py` | EXIT 0, 36 tests | C/I/R nonregression on G01–G14; historical fixture bytes unchanged |

**L2-D04 (R1 proposal):** central I must additionally wire the new v4.18 E1 test into a genuine CI workflow and register it in `standard-manifest.json`; merely writing a test file without executing it is not acceptance evidence. Maintain a separate result ledger for (i) new current v4.18 E1 source oracles (must truly PASS), (ii) historical T13/T05A exact-subject failures (observed FAIL, explicit applicability, never fake PASS) and (iii) version-wide source / Release checks (NOT_RUN until executed). Reuse prior unchanged tests only via exact subject/impact qualification. RQ decides final applicability and allowed qualification; this L2 proposal does not bind Release owner.

## 5. Architecture UNKNOWN disposition and risk ledger

| Unknown or risk | Decision / next owner | Status |
| --- | --- | --- |
| Can merge-only annotations authorize blocked Task Builder? | NO. Product Option A: native DAG unchanged, only lawful split/new Task + accepted Claim permits independent work | RESOLVED |
| Existing source owner duplicated across FRs | Section 2 source/blob owner crosswalk; no expanded normative text for ALREADY_COVERED | RESOLVED_PENDING_REVIEW |
| Are missing LAH/Exec handoff fields a true gap? | Existing §3/§8–9, §23.4 already support remaining work; do not extend unless independent counterexample | REUSE_EXISTING |
| SF↔DF/MI authority and actual pre-Freeze feedback | Task-side DF binding authority remains; pre-Freeze advisory Scaffold critique only | RESOLVED_PENDING_REVIEW |
| Historic T13/T05A exact-subject owner pin FAIL | R1 observed FAIL before v4.18 normative edits; old pins immutable; proposed no new current v4.18 owner equality Gate, preserve failures and require qualified Release owner disposition | OWNER_SCOPE_PROPOSED / R2_CHALLENGE_REQUIRED |
| Golden v4.17 G01–G14 stability | Keep original corpus and tests unchanged, append new planning examples only to TDS reference; rerun existing 36-case suite at integrated candidate | CHECK_IN_IMPLEMENTATION |
| Dynamic agent registry/scheduler/Claim effect | Explicitly excluded; no runtime prototype necessary for prose/template delta | NOT_APPLICABLE |
| Source-only tests vs real Host/external effects | E1 only; runtime/physical proofs under other projects and release owners, not fabricated here | RESOLVED |
| CI and platform capability | Runtime tests not yet executed, CI states unknown; targeted tests when Task implementation exists | NOT_RUN |
| Exact L2 review after this candidate | independent reviewer must inspect new L2 Git blob, source owner refs and failure paths | PENDING |

No high-impact architecture UNKNOWN requiring an executable Research Demo for this source-only normative design. If independent L2 review discovers a material unknown, disposition it before declaring L2_FREEZE_READY. This statement is a proposal for that review, not a self-certified PASS.

## 6. Proposed Task DAG workfronts — PREVIEW ONLY

**NOT ADMITTED:** This subsection does not create GitHub Task Issues, native dependencies, Builder Claims or source permission.

After an independently accepted L2 Freeze, favor a small DAG rather than an Issue per FR:

| Workfront / candidate Task | Concern / primary write set | Upstream logic | Parallel window | Actor / evidence |
| --- | --- | --- | --- | --- |
| A — planning rule delta | Task Decomposition owner only | frozen L2 | parallel with B,C if actual native admission allows | bounded standards author / independent reviewer |
| B — task-dag template planning view | templates/task-dag.md only | frozen L2 | parallel with A,C, own source writer | standards template author / review |
| C — TDS reference + standalone E1 oracle | references/TASK_DECOMPOSITION_REFERENCE.md and new tests/test_v418_planning_conformance.py ONLY | **frozen L2 contract alone**; NO native edges on A/B and NO assumed future A/B source bytes | lawful independent Builder after L2 Freeze/Claim; C's own fixture oracle must run independently of unmerged A/B; cross-source integration checked by I | reference/test Builder, CI validator |
| I — central wiring & integrated source validation | standard-manifest.json, .github/workflows/verify-standard.yml; optional coverage/index only if verified | native blocked_by A, B, C | after A/B/C are separately admitted, reviewed, accepted; only I edits shared wiring; E1 whole-source proof after wiring | central Builder + independent reviewer + CI validator |
| R — version metadata, whole-candidate qualification | VERSION, CHANGELOG.md, README.md, release notes/evidence and exact-version qualification | native blocked_by I; all applicable whole-version gates | final barrier, no main merge before RQ | release/merge controllers + qualified validator |

**Proposed real native DAG after L2 Freeze:** A, B and C have **no sibling blocked_by** edges (each requires only Frozen L2, legal Issue/Dispatch/Claim). I `blocked_by {A,B,C}`; R `blocked_by {I}`. Non-authoritative dependency-reason note: A/B/C independent source-owned concerns; I is shared manifest/CI wiring and cross-concern acceptance; R is Release convergence. A serial A→B→C alternative has no demonstrated material dependency and would increase structural critical path, so reject it. A falsely optimistic I parallel merge also fails because I consumes the three accepted outcomes. C may NOT assert actual A/B source behavior until I. All items remain planning previews until real GitHub materialization/readback.

If shared paths actually overlap on execution, serialize only the conflict with lawful DAG mutation; no speculative green CI or premature branches. This ADS version does not adopt source-first SF (SF_Binding=NOT_APPLICABLE; no accepted version-specific SF checkpoint). SF-related conformance uses clearly fictitious accepted SF source fixtures, never a claimed real v4.18 SF/MI attestation.

**L2-D05 (R1 proposal):** accept three truly independent source Task write sets **A/B/C** with no mutual native edges; I central convergence / wiring then R release metadata/qualification. C tests must prove E1 fixture semantics from Frozen L2 on its own branch, and final integrated assertions are I-owned; no `expected A/B semantics` shadow dependency. This is the version's first source-only DAG-analysis dogfood example, not a new live Task graph.

## 7. Independent L2 R2 focused review request and Freeze conditions

Review subject is the exact current Git branch HEAD and actual L2 Git blob after commit; all source owner blobs and Product Freeze must be current. Independent reviewer is not the L2 author. Source-only review; no normative source changes, no native Task DAG mutation and no main merge.

**Focused challenge on R1 P1×3, P2×3 and new P0/P1:**
1. P1-1 historical T13/T05A: seven-suite inventory, exact old-pin FAIL explicitly preserved; whether the **proposed** current-version NOT_APPLICABLE classification is legally sufficient or an actual dual-pin bridge/owner repair is needed; do NOT silently declare full regression PASS.
2. P1-2 Golden owner: references/TASK_DECOMPOSITION_REFERENCE.md + STANDARD_COVERAGE and DAG_GOV reference included, no duplicate conformance home or G01–G14 mutation.
3. P1-3 C independent from Frozen L2 only, no A/B source dependency; native A∥B∥C→I→R and C's standalone oracle does not assert source behavior that requires A/B to have merged.
4. P2-1 central I manifest+CI/optional coverage, R VERSION/CHANGELOG/README, no shared competing writer; P2-2 TDS only §13 tiny SHOULD; P2-3 required template lane CI checker.
5. Verify Product Option A, real Claim/shared resource/JIT, SF↔DF/MI authority and E1-only proof remain unchanged. No new schema/Agent service/human gate or mandatory Host.
6. Assess remaining UNKNOWN, particularly historical source-pin suite applicability and Release owner boundary, before considering L2 Freeze.

**Report:** new exact L2_SOURCE_HEAD, L2_BLOB, PRODUCT_FREEZE_REF, R1_P1_CLOSURE (3/3), R1_P2_CLOSURE (3/3), P0/P1/P2/P3, any new material findings with source/line, L2_R2=PASS|CHANGES_REQUESTED|BLOCKED, L2_FREEZE_READY=YES|NO, scope of historical test owner disposition and any residual Release owner obligations.

**No explicit L2 Freeze yet.** Only architecture owner may perform that separate transition after suitable independent evidence. No Task source editing authorized by this document.
