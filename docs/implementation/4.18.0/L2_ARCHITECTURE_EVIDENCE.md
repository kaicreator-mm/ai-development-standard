# ADS v4.18.0 — L2 Architecture Evidence R0 (source-only, review candidate)

**State:** L2_R0_DRAFT / INDEPENDENT_L2_REVIEW_NOT_RUN / L2_FREEZE_NO / NATIVE_TASK_DAG_NOT_ADMITTED / SOURCE_IMPLEMENTATION_NOT_AUTHORIZED.  
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
| standards/TASK_DECOMPOSITION_STANDARD.md (concern, atomicity, real dependency, central wiring) | a7c3195a89b39ecbc13276f181070b67586feb8c | ONE small optional appendix/section for capability-first decomposition and comparison of alternative valid topologies, without redefining §§4–14 |
| templates/task-dag.md (existing Lane planning authority-as-template) | d136fcbb472c8d5ba126264550d6dc63345ad171 | Compact pre-Freeze requirement/concern trace, candidate topology/serial rationale, advisory dependency motives, SF feedback and Agent capability/role/handoff cells |
| standards/TASK_DAG_GOVERNANCE_STANDARD.md §10A (accepted SF/DF/MI owner) | d1ce81f9b66b6b9d9b7005928609a55a0f3d8b94 | NO normative change; refer to it; test only approved SF/DF/MI semantics |
| standards/EXECUTION_ARCHITECTURE_STANDARD.md §6/§11/§19/§23.4/§27.3 | 1f1601a20db08d263955241607dfd08d8b8f77e1 | NO source change unless independent L2 shows necessary true conflict; Option A preserves JIT/readiness/Claim |
| standards/DEVELOPMENT_WORKFLOW.md §2.4/§2.4A/§4/§9 | 8d14b25dff70991b07d6ea2d963c86bf0e5a6286 | NO duplicate stage/source admission changes |
| standards/MODEL_USAGE_POLICY.md | 79b3590c7fe4b0b085ed346cbac9e24509e7fa66 | NO model-routing change; per-Lane candidate capability is advisory |
| standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md §3/§8/§9 | dd4f3fcadf38263f4f5cf99739d41d1c0a0bd847 | NO new handoff schema; existing remaining-work handoff sufficient pending counterexample |
| standards/PROJECT_STRUCTURE.md §1/§4 | 525380339dd25f6520202f859cfa41db635c1189 | NO Monorepo policy change |
| standards/ARCHITECTURE_DESIGN_STANDARD.md | 19ba240a15016f8381989f20f20d6d5443c4e716 | NO second design authority |
| templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md | 94907154551291342e0b71cca9c823ef89cdbfed | Append small v4.18 planning subsection only, preserve v4.17 G01–G14 and their exact bytes |
| templates/GOLDEN_INDEX.md | b36d4947cfe7db101e9eb4955ea889b55d988ed1 | Existing index link may be updated only if required by existing Golden index oracle, not another parallel catalog |
| tests/test_v417_golden_consistency.py | 3d38d39fc2bb22c3302175506b714ca5c26170cd | Must remain byte-identical; run existing regression, do not redefine G01–G14 |
| standards/RELEASE_STANDARD.md | da3b78b113be238bdce650ccb646f5aa23bc1f9b | No Gate/risk waiver or external-runtime release admission change |

FR owner decisions (proposed for independent L2 adjudication):

| FR | Disposition | Source delivery |
| --- | --- | --- |
| FR-01 | ALREADY_COVERED + prompt gap | Existing Task Decomposition and Lane template; add capability-before-concern / Step-is-not-Issue guidance only |
| FR-02 | ALREADY_COVERED | Reference owner; do not rewrite |
| FR-03 | TRUE_GAP_SMALL | Optional task-decomposition pattern index plus bounded Golden/forbidden |
| FR-04 | TRUE_GAP | Comparison of actual DAG topologies, reason annotations and ordinal path/serial justification |
| FR-05 | TRUE_GAP_SMALL | Pre-Freeze Scaffold-aware feedback in existing Lane template; SF/DF/MI unchanged |
| FR-06 | ALREADY_COVERED | Task Decomp/Project Structure/DAG Governance |
| FR-07 | ALREADY_COVERED + Golden negative | Product Option A; no prospective merge-only native edge |
| FR-08 | TRUE_GAP_SMALL | Candidate WEB/CI/LOCAL capability, independence and human/role constraints on Lane template |
| FR-09 | ALREADY_COVERED + example | Existing GAIP/Exec/Model Usage |
| FR-10 | ALREADY_COVERED subject to counterexample | LAH §3/§8–9 and Exec §23.4; no second tuple/schema by default |
| FR-11, FR-12 | ALREADY_COVERED | Existing Human authority, escalation/assistance patterns |
| FR-13, FR-14 | IMPLEMENTATION_ONLY | One optional advisory Pattern subsection in existing Golden/reference corpus |
| FR-15 | TRUE_GAP_SMALL | Non-gating topology quality checklist; no universal score |
| FR-16 | DEFER/ALREADY_COVERED | Workflow §8; external telemetry owner independently decided |

**L2-D02 (proposed):** constrain normative write set to the Task Decomposition owner and existing Task DAG template. Conformance stays under existing Golden/template/test owner, with a bounded isolated v4.18 additive section. Do not edit G01–G14 definitions, strict public Schemas, global runner, dispatch, Product/Release authorities or v4.17 release records.

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

These are human-readable sections/columns in **existing** Task DAG template, not new YAML fields or a machine scheduler. No duplication into separate state ledgers. Skip unnecessary fields for a small/serial Fast Path with a clear reason.

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

**Golden placement decision (addresses Product R2 P3):** append one v4.18-specific section in the existing STANDARD_CONFORMANCE_EXAMPLES.md, without modifying bytes or semantics of v4.17 G01–G14 section. Focused new v4.18 source-only oracle/test may be in its own test file. Existing tests/test_v417_golden_consistency.py stays unchanged and its regression must pass. If append would alter v4.17 parser/oracle, choose a separate focused v4.18 reference/index location under existing Golden owner and preserve the historical section.

### Layered evidence matrix

| Proof | Status in this L2 | Required at concern/version implementation |
| --- | --- | --- |
| Existing owner texts, exact blob, contract review | AVAILABLE SOURCE | revalidate currentness at implementation |
| Actual source-only Golden test results | NOT_RUN | execute required scoped validators and record exits |
| Native GitHub dependency mutation/readback of new Task DAG | NOT_RUN | only after L2 Freeze and authorized Task DAG creation |
| Real model/agent collaboration and time savings | NOT_RUN | not v4.18 standards-source release prerequisite; external project scope |
| Real platform/physical/human protected acts | NOT_RUN | never inferred from language-only unit fixtures; existing Gate ownership |
| Whole version integration / Hidden / Critical Journeys / Packaging / RQ | NOT_RUN | decide and execute existing appropriate Release Standard gates at version candidate, no blanket waiver |

**L2-D04 (proposed):** use static source-only tests for the planning standard plus existing targeted consistency scripts. Reuse unchanged v4.17 evidence only with exact source/impact qualification; do not claim current full-version PASS on L2 authoring.

## 5. Architecture UNKNOWN disposition and risk ledger

| Unknown or risk | Decision / next owner | Status |
| --- | --- | --- |
| Can merge-only annotations authorize blocked Task Builder? | NO. Product Option A: native DAG unchanged, only lawful split/new Task + accepted Claim permits independent work | RESOLVED |
| Existing source owner duplicated across FRs | Section 2 source/blob owner crosswalk; no expanded normative text for ALREADY_COVERED | RESOLVED_PENDING_REVIEW |
| Are missing LAH/Exec handoff fields a true gap? | Existing §3/§8–9, §23.4 already support remaining work; do not extend unless independent counterexample | REUSE_EXISTING |
| SF↔DF/MI authority and actual pre-Freeze feedback | Task-side DF binding authority remains; pre-Freeze advisory Scaffold critique only | RESOLVED_PENDING_REVIEW |
| Golden v4.17 G01–G14 stability | Only additive v4.18 subheading; unchanged section + old regression at Task validation | CHECK_IN_IMPLEMENTATION |
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
| C — Golden & deterministic oracle | one existing Golden corpus additive section and new test source | frozen L2 contracts, expected A/B semantics | can prepare fixtures; final green after A/B integration | fixture/test Builder, CI validator |
| I — integrated standards source validation | full candidate source consistency, no cross-owner overwrite | accepted A+B+C merges | after siblings, central integration owner | CI/Validator/Review as selected |
| R — version qualification | exact-version Release qualification and main integration | I + full required source gates | final barrier | release/merge controllers |

If exact Golden text requires the same path as another active writer, serialize only that write scope. No arbitrary serial chain A→B→C. Scope/counts remain subject to Task DAG design with native Issue materialization; no Source Scaffold implementation is necessary for this ADS self-change (SF_Binding=NOT_APPLICABLE, since no accepted version-specific source-first SF checkpoint). The SF-related standards scenario uses fictitious accepted SF fixtures, never a claimed real v4.18 SF/MI attestation.

**L2-D05 (proposed):** freeze design as a two-primary-write-lane + evidence-lane + version closure topology, subject to exact native authority and proper Issue/Claim/PR setup after L2 Freeze. Independent preparation and review can overlap; merge/release convergence stays exact.

## 7. Independent L2 R1 review request and Freeze conditions

Review subject is the exact current Git branch HEAD and actual L2 Git blob after commit; all source owner blobs and Product Freeze must be current. Independent reviewer is not the L2 author. Source-only review; no normative source changes, no native Task DAG mutation and no main merge.

**Challenge specifically:**
1. Is the FR-04 TRUE_GAP truly outside Task Decomposition §13 and template Lane prompt, or is the proposed normative Appendix redundant? Could template-only change meet Product?
2. Do all source owner refs and FR dispositions correctly distinguish existing norms, new prose and Golden-only work?
3. Is the optional SF↔DAG feedback entirely *pre-Freeze*, with no second SF writer/DF authority and no hidden MI/rebind loophole?
4. Does Product Option A fully preserve native blocked_by, ready_builder, JIT/Claim and shared-resource §27.3?
5. Does the candidate Golden placement preserve existing v4.17 G01–G14 bytes/oracles and source-only E1 boundary?
6. Are workfronts genuinely disjoint and capable of parallel Task/PR Review, and which native dependencies are strictly necessary?
7. Is any protected human approval, real Host proof, external-effect schema or universal CI/Review being invented?

**Report:** L2_SOURCE_HEAD, L2_BLOB, PRODUCT_FREEZE_REF, P0/P1/P2/P3, each affected exact owner/blob, L2_R1=PASS|CHANGES_REQUESTED|BLOCKED, L2_FREEZE_READY=YES|NO, allowed minimum future source write set and remaining owner actions.

**No explicit L2 Freeze yet.** Only architecture owner may perform that separate transition after suitable independent evidence. No Task source editing authorized by this document.
