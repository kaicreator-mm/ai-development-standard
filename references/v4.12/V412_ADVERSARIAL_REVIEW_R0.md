# v4.12 Contract Candidate — Adversarial Self-Review R0

> **STATIC RED-TEAM / SELF-REVIEW ONLY (NOT Independent/Fresh Review).** Subject: `references/v4.12/V412_CROSS_STAGE_CONTRACTS_R0.md` introduced at commit `e6d7d3a6dd857c5a98888eefe4402a89b2d13c77`. Review input: pinned v4.11 workflow/claim/validation/release/adoption owners plus dogfood #1081/#775/#1072/#926/#1092 and v4.12 #1096/#1099/#1100. No executable GitHub controller implementation, test invocation, real Host evidence or external independent reviewer. Review deliberately seeks counterexamples, unsafe inferences, authority collisions and excess ceremony.

## Result and limitations

```ini
R0_REVIEW_CLASS=AUTHOR_LED_ADVERSARIAL_STATIC
SUBJECT_COMMIT=e6d7d3a6dd857c5a98888eefe4402a89b2d13c77
NOT_A_FRESH_INDEPENDENT_REVIEW=YES
P0_SOURCE_SAFETY_DEFECT=0_CONFIRMED_STATIC_ONLY
P1_DESIGN_GAPS=7
P2_CLARITY_AND_INTEGRATION_GAPS=8
L2_RESERVED_DECISIONS=10
ACTUAL_MACHINE_CONFORMANCE=NOT_RUN
PRODUCT_FREEZE=NO
OVERALL=NEEDS_REVISION_BEFORE_PRODUCT_FREEZE
```

These are **design findings, not verified production defects**. After an in-branch contract repair, each entry requires an explicit `ADDRESSED_IN_CANDIDATE`, `L2_RESERVED`, `DEFER` or `OPEN` disposition; a written fix alone is not a machine-test PASS. Do not turn all findings into separate mandatory Issues, Reviewer dispatches or release blockers.

## P1 — material unanswered contracts in initial draft

| ID | Adversarial scenario / counterexample | Needed change | Existing authority / expected disposition |
|---|---|---|---|
| F01 | Graph keyed only by Task/phase: P studies across two products or two versions share same label, falsely satisfy downstream `CONSUMES` | Bind **repository/project + product/version stream + phase + immutable work-id + revision + exact evidence subject** and phase-owning authority; never merge unrelated graphs | W1 / GitHub Work Item + Product/L2; candidate contract clarification |
| F02 | A Product viability probe must execute before PRD Freeze (e.g. whether real user workflow is technically possible). C01 could forbid all executable technical work until L2, or let P probe self-certify production architecture | Permit **Product-purpose bounded feasibility evidence** in L1 when it answers a Product UNKNOWN; distinguish it from L2 Architecture Research Demo and prohibit promotion of implementation/architecture PASS. Escalate actual architecture decision to post-Freeze L2 | Development Workflow Stage1/Stage2; candidate contract clarification |
| F03 | L2 contract changes, two dependent Tasks drift, reviewer tries blanket revalidation or reuses wrong exact-head PASS. C05 lists fields but not the *decision procedure* | Give minimal deterministic **impact triage**: discover dependent consumers; classify binding changed? required predicate changed? real execution/authority bound changed? retain only verified exact unaffected cases; affected hold/rebind; UNKNOWN fail-closed; no unbounded global rerun | Assurance Plan §§12–13, Validation §6, Release §11, Task DAG Governance; candidate algorithm, schema reserved |
| F04 | A lower-level actor changes `SUPERSEDES` prose in Issue and effectively closes Product evidence, unclaims worker or changes mandatory release gate | Clarify `SUPERSEDES` in P/A only **source-bound version/provenance label** unless decision owner commits an authorized amendment; I uses canonical DAG mutation and dispatch/claim terminal. No new cross-phase status enum | C03/C06, existing Product/Task/Execution/Release; candidate clarification |
| F05 | Product owner wants FAST/omit material human/tenant deny checks, a security owner demands them; both annotations appear current | Explicit **conflict precedence**: same-subject material existing hard obligations remain in force until owning adjudication, Product choice cannot itself revise Release/Trust proof; unresolved contradictory decisions block the affected irreversible action and can leave unrelated work active | #1099, Release §11, Human Decision; candidate clarification |
| F06 | Connected GitHub comment impersonates `PRODUCT_FREEZE=YES` or `ARCHITECTURE_PASS`; workflow imports it as structured graph data | Source-authenticated/canonical emitter provenance and schema validation **before accepting an authority-bearing fact**, and separate parsed untrusted text; source-bound role and immutable event refs | Interaction Protocol §8.1.1/§8.2, event gap #783; candidate reference, existing-owner conformance |
| F07 | Strong simulation outcome is treated as E3 evidence after environment/spec changes; repeated same-test equivalence drops an independent human/negative path | Evidence equivalence must require complete material **predicate set, actor/human independence, real vs simulated fidelity, exact subject/currentness and negative cases**, with accepting gate owner; no cost-based reduction | Validation §3/§5/§6, Release §11, Demo §9/§15; candidate clarification |

## P2 — useful clarity and execution-economy gaps

| ID | Counterexample | Bounded recommendation |
|---|---|---|
| F08 | P/A graph one node per question accumulates 100 pseudo-issues | Add graph-expansion **materialization rationale**, exit, no duplicate consumer; use inline notes where independent execution/authority is absent |
| F09 | Project Steward alerts keep reopening themselves and increase queue age | Deduplicate observation by exact subject + root cause; use `OPEN/ACKED/RESOLVED/SUPERSEDED` only as **advisory UI**, not canonical workflow state; prefer existing comments/projections |
| F10 | Multiple long HOST jobs and temporary cloud assets compete; `prepare` silently becomes `allocate` | Environment reservation only under existing composite claim, resource hygiene and cleanup receipt; preflight alone gives no authority |
| F11 | Worker stops during L1 human study/remote Demo, leaving participant data and partially executed external effects | Bounded recovery ownership, participant/privacy retention, no restart until outcome reconciled, separate environment cleanup |
| F12 | Cheap optional work always chosen first; expensive version-critical required E3 is starved | Track critical path + fairness/aging within hard-dependency/eligibility constraints; scheduling suggestion cannot waive material E3 |
| F13 | Task Metadata counts imaginary “28 hosts saved”, claims efficiency | Separate counterfactual **estimate** vs actual executed/avoided dispatch and attributable baseline; `UNKNOWN` when unsupported |
| F14 | Reused third-party code/licence shifts, linked evidence remains old but current source is different | Bound supplier revision/licence/rights, downstream affected consumers and safe de-adoption decision; do not over-generalize from same package name |
| F15 | A0 manual project forced to implement graph schema/observer to be compliant | Keep manual INLINE evidence and source pins legal; no new mandatory service/schema and no retroactive historical truth rewrite |

## Adversarial logical probe matrix (reasoned only; not machine-executed)

| Probe | Attack | Draft R0 outcome | Status |
|---|---|---|---|
| X01 | Inline Product with significant immutable safety gate | Existing floor is retained, no 3-DAG requirement | Conceptually covered (C01/C02/C06) |
| X02 | L1 technical feasibility unknown before Freeze | P/A jurisdiction ambiguous | F02 **OPEN** |
| X03 | Cross-project identical node ID and source filename | Node identity insufficient | F01 **OPEN** |
| X04 | Multi-consumer architecture change: safe reuse vs unsafe proof | Impact procedure underspecified | F03 **OPEN** |
| X05 | Malicious model-authored event-shaped text | References existing trust owner, intake projection gap | F06 **OPEN owner conformance** |
| X06 | Two apparently equivalent E3 scenarios with different DENY actor | Original C04 broadly prohibits false reuse; full predicate policy insufficient | F07 **OPEN** |
| X07 | Active claim, lease expired, unpushed local branch | Existing §27.5 correctly forbids takeover | Conceptually covered; execution not tested |
| X08 | P/A `SUPERSEDES` comment claims Freeze or gate mutation | Draft leaves relation generic | F04 **OPEN** |
| X09 | Many advisory issues during merge drain | W2/C07/C08 economy and #926 already apply | Conceptually covered; integration TBD |
| X10 | Prior frozen Product Promise omitted on ROI grounds | C02/C06 and #1099 forbid | Conceptually covered, F05 explicit conflict needed |
| X11 | R1–R8 repeated expensive validation, focused script omitted | C08 and existing Test/CI truth forbid promotion | Conceptually covered; machine proof not run |
| X12 | Version candidate green with Hidden/RQ NOT_RUN | C12 forbids Version PASS | Conceptually covered |

## Revised candidate repair target

Any in-branch R1 repair may address F01–F07 by adding compact cross-contract clarification and negative tests to the same **non-normative** contract file; F08–F15 remain under existing owners or L2 choices unless actual evidence proves a distinct requirement. No duplicate per-finding implementation Task.

## Not yet explicitly decided; requires Product Review vs L2 placement

1. Does **DAG-P or DAG-A** use GitHub native dependencies for independently schedulable *research* nodes, or only an Issue-led Worklist and separately versioned checkpoints? No guessing that implementation DAG governance automatically controls P/A.
2. What is the **identity & revision contract** for P/A work and `CONSUMES` evidence across versions and multi-repo products? Must define expected exactness per truth type, without pretending all historical market evidence has SHA.
3. Which **existing owner signs study sufficiency** when evidence is sourced from external market participants with anonymity/privacy constraints, and when is selected independent product review mandatory?
4. How is phase choice `INLINE/WORKLIST/EXPLICIT_DAG` stored with minimal adoption level; which names/fields are advisory vs enforceable? Avoid universal schema.
5. How are **cross-phase impact edges** materialized/recomputed without another graph database or permanent runner? Manual at A0/A1 should remain lawful.
6. What is the Project Steward **activation/deactivation/ownership** in user-mediated WEB vs continuous LOCAL mode; who reacts when owner is offline, and what can an automation legitimately do?
7. How are **human participant ethics/consent/privacy, hidden validation and E3 evidence** referenced when they cannot be published in GitHub? Evidence may exist privately but inaccessible reviewers cannot assert PASS.
8. What **scheduling fairness** rule prevents cheap prep tasks starving a required Host/Review while preserving currentness/risk priorities? Do not impose unverifiable hard deadlines.
9. What is the minimal **observable cost baseline** for ROI/efficiency without inventing causality/telemetry; optional no-metric fast path?
10. How exactly does **v4.12 adoption and minor-version SemVer** impact pinned projects already mid-Freeze/multi-version lineage, and how to test prospective-only migration?

## Exit posture

R0 has **material design questions**, so it is **NOT Product Freeze ready**, NOT a Fresh Review and NOT a claim that C01–C12 are implemented or conformance-tested. A revised draft should demonstrate owner-based non-duplication and repair F01–F07. After that, one bounded independent Product review can evaluate a frozen *candidate* rather than spawning many per-finding Reviews. P/A graph encoding, reducer and schemas await genuine L2.

**ADVERSARIAL_REVIEW_RESULT = NEEDS_REVISION_BEFORE_PRODUCT_FREEZE; NO_NORMATIVE_ADOPTION.**


## R1 same-author repair/disposition checkpoint

After R0, a revised **non-normative** contract candidate was written at `references/v4.12/V412_CROSS_STAGE_CONTRACTS_CANDIDATE.md`, §17 (R1-F01 through R1-F07). Initial R0 draft path is retired from the branch, preserved at original exact commit. This is **not independent re-review**, nor a validated implementation.

| R0 finding | R1 source disposition | Still needed before actual v4.12 normative adoption |
|---|---|---|
| F01 P1 | **CANDIDATE_TEXT_ADDRESSED** (phase/repo/version identity) | L2 stable machine identity & cross-repo adoption semantics |
| F02 P1 | **CANDIDATE_TEXT_ADDRESSED** (Product-purpose bounded feasibility) | Product owner/Risk-review acceptance and concrete case |
| F03 P1 | **CANDIDATE_TEXT_ADDRESSED** (6-step impact and currentness readback) | Exact owner currentness/equivalence tests, not a second reducer |
| F04 P1 | **CANDIDATE_TEXT_ADDRESSED** (no supersession-derived terminal) | L2 P/A graph projection / explicit authority decision conformance |
| F05 P1 | **CANDIDATE_TEXT_ADDRESSED** (conflict precedence and scoped block) | Owner arbitration negative test and Human DENY dogfood |
| F06 P1 | **CANDIDATE_TEXT_ADDRESSED** (trusted canonical source admission) | Actual pinned-schema producer conformance #783; cannot claim already implemented |
| F07 P1 | **CANDIDATE_TEXT_ADDRESSED** (full-predicate equivalence) | Real gate-owner evidence/negative fidelity test |

**Residual status:** `P1_SEMANTIC_WORDING_OPEN=0` in this self-reviewed candidate; `P1_INDEPENDENT_PRODUCT_REVIEW_REQUIRED_OR_APPLICABLE=NOT_RUN`; `P1_MACHINE_CONFORMANCE=NOT_RUN`. F08–F15 are **L2/owner-disposition candidates**, not fixed through a duplicate subsystem. The ten choices above stay **OPEN** until genuine Product/L2 decisions with precise owners.

### Additional post-repair adversarial escape probes

- **Escape E01 — Mixed evidence ages:** Study collected in 2024, exact source code pinned in 2026. New stable node tuple is not enough; consumer must explicitly judge freshness by claim type. **Product policy unresolved**, do not assert generic time threshold.
- **Escape E02 — Across-project coordinated feature:** Two repositories share a product objective and partially incompatible architecture freezes. "one graph" must remain a *federated logical view* with independent source authorities, not a common mutating DAG. **L2 projection open**.
- **Escape E03 — Resource allocation with no atomic backend:** Current environment may not provide composite admission atomicity; proposing a v4.12 scheduler cannot say YES because a lockfile exists. **BLOCK affected claim / use lawful existing serialized authority**, no fake capacity admission.
- **Escape E04 — Repeated Product Review of unchanged scope:** A new reviewer cannot create new Product Freeze or release evidence merely by saying PASS; treat repeated nonmaterial review as no new authorization. **Existing owner**.
- **Escape E05 — Release metric gaming:** A high throughput of tiny accepted PRs alongside a BLOCKED real E3 critical journey is failure, not success; Steward must rank real critical path and mandatory proof. **W2/owner L2 open**.
- **Escape E06 — No public evidence for human study:** anonymization may make raw participant evidence inaccessible to a public reviewer; *lack of public raw data* alone does not mean none occurred, yet an unauthorized party cannot certify it. Requires authorized secure evidence consumer with redacted trace and privacy policy. **Product privacy/L2 evidence envelope open**.

**Final author-led adversarial verdict on R1 candidate:** `REVIEWED_DRAFT_WITH_EXPLICIT_OPEN_DESIGN_DECISIONS`. Acceptable as an **L1/PRD candidate** for an independent review and real dogfood design, **NOT normative PASS / Product Freeze / implemented cross-stage contract**. No new v4.11 blocking authority.


## Targeted adversarial extension: C13 minimum-necessary human evidence

**Status:** author-led static negative review of new C13 contract candidate, not an independent human reviewer or tested empirical protocol.

- **HX01 — label anchoring / blind breach:** candidate labels generated by LLM are shown to a purported "blind" human Gold author; output cannot be represented as independently authored blind human truth. C13 H.3 requires a clear hybrid-vs-human-authored evidence distinction. **CANDIDATE_TEXT_COVERED; empirical dogfood NOT_RUN**.
- **HX02 — counterfeit multi-agent independence:** Builder runs model-A/model-B/model-C against its own files and calls it a genuinely fresh independent reviewer; source- and operator-bound independence is absent. C13 and existing §6 Review boundaries reject the equivalence. **CANDIDATE_TEXT_COVERED; independent review NOT_RUN**.
- **HX03 — coercive approval compression:** "one-click human confirmation" hides side effects, consent, or risk, removing informed choice. C13 must require complete decision-relevant facts, clear allow/deny/refuse, qualified authority and no default ALLOW. Current C13 demands decision card and DENY binding but **explicit UX/consent representation and withdrawal handling remain OPEN L2/PRD**, not proven safe.
- **HX04 — mathematical proof overextension:** deterministic code verifies 48 annotations are well-formed and blinded at the file-format level, incorrectly inferring their semantics true/representative. C13 requires fidelity/predicate boundary and real empirical observation where the Product question needs it. **CANDIDATE_TEXT_COVERED**.
- **HX05 — false cost economy:** LLM x 10 + huge scripts + multiple human rounds might cost more than one qualified person for a short final decision. C13's layer omission/stop rule needs decision-value-based selection and observed cost, no universal "always 3 model rounds." **CANDIDATE_TEXT_COVERED**.
- **HX06 — frozen human-authored oracle requirement:** user wants switch to AI candidates because real Gold is expensive, but existing pinned Product/test protocol explicitly requires independent human authors. Cannot silently bypass it; must either execute requirement or obtain authorized prospective Product/method change and preserve historical inconclusive/fail evidence. **CANDIDATE_TEXT_COVERED; approved methodological amendment not claimed**.
- **HX07 — review confidentiality:** independent human owner permitted to see proprietary source while external model/provider is not; multi-LLM upload might leak protected evidence. Route model work only over approved/redacted data; ineligible model cannot consume protected truth. **P1 PRODUCT POLICY CLARIFICATION NEEDED:** add explicit allowable-information/processor checks before multi-LLM dispatch (W3/Trust/Privacy existing owner).
- **HX08 — no human available:** required real-actor testimony/consent is missing and all AIs agree; Product cannot declare synthetic PASS. Must remain BLOCKED or lawfully revise Product promise/study method and state limitations. **CANDIDATE_TEXT_COVERED**.

**Disposition:** C13 has useful product-level behavior and negative cases, but HX03 and HX07 require explicit consent/identity and model data-transfer constraints in the contract draft. No claim of independent-human replacement, savings or real study completion. `C13_ADOPTION=PRODUCT_CANDIDATE_ONLY; INDEPENDENT_REVIEW=NOT_RUN; REAL_HUMAN_STUDY=NOT_RUN.`


## Targeted adversarial extension: C14 online behavioral evidence

**Scope:** author-led source/ethics/epistemic attack, not independent empirical or legal approval. The candidate is `V412_CROSS_STAGE_CONTRACTS_CANDIDATE.md` §C14.

| ID | Attack / assertion to reject | Countermeasure and current status |
|---|---|---|
| OX01 | 400 forum posts -> 400 unique real humans -> 40% target-market prevalence | Distinguish posts/contributors/population denominator, bot/copied content; `O1` self-report, biased sampling, no unjustified prevalence. **CANDIDATE_COVERED** |
| OX02 | Publicly accessible thread -> license to bulk scrape/store/redistribute/train models | Verify explicit permitted use, current platform policy and applicable privacy/rights, with authorized research access; avoid restricted sites and unauthorized data transfer. **CANDIDATE_COVERED** |
| OX03 | Multiple LLMs agree a subjective complaint proves new UX completion rate | Requires authentic task observation/telemetry or valid study; LLM consensus is interpretation only. **CANDIDATE_COVERED** |
| OX04 | A generated/paid coordinated campaign of "customer complaints" is indexed | Sampling/dedupe/source provenance, account/temporal anomalous signal, contrary platform corroboration. Authorship often uncertain; state UNKNOWN rather than certifying humans. **CANDIDATE_COVERED** |
| OX05 | Visible posts in sensitive health/minor/closed forum treated as fair game | Accessibility != ethical/legal permission; minimize identities, use approved source only, deny unauthorized provider upload. **CANDIDATE_COVERED** |
| OX06 | Imported dataset was valid when acquired, then source deleted a post/revoked its permitted use | Source freshness, rights and retention/delete obligations must be rechecked at use and disposition updated. **PARTIAL: deletion/currentness implementation L2 open** |
| OX07 | Genuine negative feedback from 2022 defines 2026 behavior after product redesign | Time-window and version/region/locale context bound; Product consumer judges outdatedness. **CANDIDATE_COVERED, numeric freshness threshold not mandated** |
| OX08 | Researcher quietly alters planned blind-human Gold methodology by finding similar forum comments | Existing preregistration and required independent human Gold retain authority; public data is separate L1 evidence and cannot self-amend Gold. **CANDIDATE_COVERED** |
| OX09 | Search is aimed only at negative reviews to justify a preselected product | Opposing sampling/selection disclosure and alternative evidence; cannot claim unbiased population. **CANDIDATE_COVERED** |
| OX10 | First-party telemetry was legally collected for purpose A; now re-identifies or sells to third-party LLM | Purpose limitation/permissions and approved processing remain required; derived availability doesn't license new use. **CANDIDATE_COVERED; lawful basis owner remains open** |
| OX11 | Forum signal is useful for `problem exists`, but Product asserts statistical threshold | Distinct decision claims require distinct methods; only the former may be adopted; numeric claim needs valid sampling/instrumentation. **CANDIDATE_COVERED** |
| OX12 | Large optional scraping project prolongs L1 after research already sufficient | Timebox and stop rule; use existing research/approved tools; no new crawler or compulsory DAG. **CANDIDATE_COVERED** |

**Source-policy substantiation used for negative proof planning, not a permission grant:** Reddit's current help page for Developer Platform / accessing Reddit data distinguishes authorized Reddit for Researchers pathway; Reddit Data API Terms are purpose/rate/rights-restricted; the ICO-hosted international regulatory statement warns public visibility does not make personal data unprotected. Survey quality methodology from AAPOR highlights online coverage and selection bias. Always re-evaluate actual source policy and applicable laws at collection time.

**Open Product/L2:**
- Real-human observational evidence sufficiency and target population criteria **for each Product claim**, especially where the only source is a forum complaint.
- How researchers document third-party platform permissions, revocation, legal deletion, storage and authorized LLM ingestion.
- Whether first-party consented behavioral logs (O3) can offer a real measured success denominator; access rules and cohort representativeness.
- Rights, cross-border jurisdiction and privacy for public-but-sensitive communities.
- Exact integration with #1100 DAG-P and C13 H3 classification: `O1/O2/O3` may be **human-origin historical evidence**, but not automatically a purpose-built `O5` or human decision/independent-review attestation.

**Verdict:** `C14_ADDITION=PRODUCT_CANDIDATE_WITH_NEGATIVE_TESTS`; no operational crawling, actual sample, empirical Gold, legal advice, independent Product review, or L1 Product Freeze. No new implementation Task created.


## Targeted adversarial extension: C15 scaffold baseline and HIGH_ASSURANCE escalation

**Evidence:** author-led static reading of candidate `V412_CROSS_STAGE_CONTRACTS_CANDIDATE.md` §C15, pinned v4.11 DEVELOPMENT_WORKFLOW Stage2.3–2.5, TASK_DECOMPOSITION (one coherent concern, atomicity, central wiring), TASK_DAG_GOVERNANCE (native DAG mutation), ARCHITECTURE_DESIGN and EXECUTION_ARCHITECTURE (Claim and source-write authority), dogfood #775/#1072. Not independent architecture review, not compile/test evidence.

### Attack matrix

| ID | Failure hypothesis | Disposition |
|---|---|---|
| SX01 **P1** | Proposed **pre-DAG codegen** steals execution authority from current v4.11 Task DAG Freeze → materialization → Claim ordering | C15 §S.1 **A default** and conditional **B only after explicit Product/L2 governance amendment**, fail closed on source write. **CANDIDATE_TEXT_ADDRESSED**, no implemented authority change |
| SX02 **P1** | "Interfaces are stable" is interpreted as a complete runnable feature; compile-green NotImplemented yields fake customer acceptance | C15 §S.3 limits checks to contract/build/import smoke, stubs clearly `UNIMPLEMENTED`, distinct functional/real-host gates. **CANDIDATE_TEXT_ADDRESSED** |
| SX03 **P1** | Blanket HIGH_ASSURANCE on any private function or generated file induces endless reviews/Host runs; cost outweighs value | C15 §S.5 impact-based escalation, same-contract normal tests; current mandated security/rights gates remain. **CANDIDATE_TEXT_ADDRESSED** |
| SX04 **P1** | Changed public security ABI silently migrates through a "small" scaffold edit without architecture/product owner | C15 §S.5 explicit Product/L2/compatibility authority and material negative proof; no Builder unilateral change. **CANDIDATE_TEXT_ADDRESSED** |
| SX05 **P1** | Bootstrap consumes a stable contract but upgrades upstream/lockfile or generated license terms behind L2 | C15 §S.3/S.5 and SC10–SC11 demand provenance, rights, actual toolchain, L2 bounded amendment when required. **CANDIDATE_TEXT_ADDRESSED** |
| SX06 **P1** | T00 is authorized but downstream Task DAG assumes shared interface freeze without actual legal acceptance/integration or exact SHA readback | C15 §S.1/S.3/S.4 require accepted exact source, actual integration, consumer JIT re-read; T00 PASS not Release PASS. **CANDIDATE_TEXT_ADDRESSED** |
| SX07 **P2** | Apparent per-interface parallelism splits shared auth state and transactional invariants into invalid partial implementations | C15 §S.4/S.6 preserve atomic invariant; shared wiring owner and real DAG dependencies. **CANDIDATE_TEXT_ADDRESSED** |
| SX08 **P2** | Dynamic domain package/plug-in architecture has no value in stubbing each possible Tool/Capability | C15 §S.2/S.4 and SC12 reject mandatory interface-per-Task abstractions. **CANDIDATE_TEXT_ADDRESSED** |
| SX09 **P2** | Existing mature project has rich clean module structure but scaffold re-generation rewrites everything | REUSE_EXISTING/OMIT chosen before new source; explicit ROI. **CANDIDATE_TEXT_ADDRESSED** |
| SX10 **P2** | Provisional DAG contains placeholder nodes, then user assumes they are frozen implementable Tasks | C15 distinguishes bounding provisional concern inventory vs frozen executable DAG, explicit per-Task identity/admission and lawful mutation. **CANDIDATE_TEXT_ADDRESSED** |
| SX11 **P2** | During T00 scaffold import there is no real error-path test, while end-to-end failure safety depends on error semantics | Contract-specific minimal negative or failure check when inherent; real integration/functional paths stay pending. **CANDIDATE_TEXT_ADDRESSED** |
| SX12 **P2** | Project wants multi-runtime or generated schemas, but scaffold only targets one environment and falsely declares platform matrix PASS | SC03/SC09/SC10 and source/currentness gate scope prohibit cross-platform proof extrapolation. **CANDIDATE_TEXT_ADDRESSED** |

### Residual genuine Product/L2 decisions (not implementation facts)

- **G1 authority ordering (highest priority):** Should v4.12 authorize path B (source bootstrap **before full** implementation DAG) as a prospective constrained planning path, or leave A as only normative? C15 correctly forbids pretending B already legal. Choose via PRD/L2, not incidental "helpful" builder.
- **G2 scaffold minimality:** What must exist in accepted bootstrap for changed project characteristics? No universal FQN/file tree, language/runtime, smoke matrix or 1-interface/1-Task.
- **G3 interface change and Freeze scope:** Which part of L2 is a truly frozen cross-team contract and which implementation seams remain private; adjust owner/compatibility/consumer matrix accordingly.
- **G4 reference baseline identity:** Which exact merged bootstrap SHA/tree is bound into Task Pack/JIT and how to handle downstream rebind after independent PRs merge?
- **G5 economics & operational proof:** Need dogfood evidence that executing code bootstrap ahead of **full** DAG lowers total wall clock and conflict repairs versus T00 as the first DAG node; no unsupported 30–50% savings claims.
- **G6 real gate scope:** high risk may require real-host security/negative proof even if scaffold compiles; low-risk source-only scaffolding should not inherit whole-version Host/Hidden matrix.

**Adversarial verdict:** `C15_R0_AUTHOR_LED_REVIEW=SEMANTIC_DESIGN_CANDIDATE_READY`; `P1_UNADDRESSED_SEMANTIC=0`; `P1_RUNTIME_MACHINE_PROOF=NOT_RUN`; `INDEPENDENT_ARCHITECTURE_REVIEW=NOT_RUN`; `L2_B_STAGED_BOOTSTRAP_AUTHORITY=OPEN`; `PRODUCT_FREEZE=NO`. No normative change to v4.11 execution/Task DAG, no E3, no completed version release.


## C15 R1 — Co-evolving scaffold + DAG / paired-freeze adversarial update

> **Exact review subject:** C15 revised candidate after user Product direction to generate a real scaffold **before full Implementation DAG Freeze**, enrich it alongside Draft DAG and freeze the **paired identities** before downstream Task execution. Review class = **author-led static adversarial challenge**, not Fresh Independent Review, not tested source, not an approved new work-authority mechanism. The preceding `C15 SX01–SX12` conclusions describe the **historical R0 candidate**, which had default T00 path A. R1 supersedes their path choice; do **not** cite R0 as an authorization for pre-DAG writes.

```ini
SCAFFOLD_PRODUCT_DIRECTION=SCAFFOLD_BEFORE_FULL_DAG_FREEZE
DAG_DRAFT_AND_SCAFFOLD=CO_EVOLVE
FREEZE_TARGET=PAIRED_EXACT_SCAFFOLD_AND_TASK_DAG
USER_PRODUCT_DIRECTION=RECORDED
CURRENT_V411_PRE_DAG_SOURCE_PERMISSION=NO
V412_AUTHORIZATION_DELTA=DESIGN_REQUIRED
MACHINE_TESTS=NOT_RUN
INDEPENDENT_REVIEW=NOT_RUN
PRODUCT_FREEZE=NO
```

### R1 negative-case matrix (planning checks, not executed tests)

| ID | Red-team attack | Correct resolution | Candidate status |
|---|---|---|---|
| SXR1-01 **P0 authority candidate** | Developer invokes generator immediately after L2 Freeze, before scoped permission, because Product says "generate before DAG" | **Reject unclaimed source writes** under pinned v4.11. v4.12 must prospectively define bounded Bootstrap admission with real Issue/actor/write scope/currentness and test negative branch. No hidden bypass. | **TEXT_GUARDED / LEGAL IMPLEMENTATION OPEN** |
| SXR1-02 **P1** | Planning Agent and Scaffold Agent both alter public schema; each independently seems current | one incompatible accepted source writer / canonical claim and re-read source, planning consumes newest accepted exact SHA; no silent second mutation authority | TEXT_GUARDED / CONFORMANCE OPEN |
| SXR1-03 **P1** | DAG D1 references adapter v2, scaffold SF still exports v1; paired Freeze marks both ready | cross-check all material contracts/Task paths/ownership against integrated scaffold; do not Freeze until consistent | TEXT_GUARDED / EXACT CHECK OPEN |
| SXR1-04 **P1** | Every change in DAG D0 forces new scaffold PR, which makes DAG stale and causes infinite feedback | bounded co-edit sessions, no new Issue per adjustment, one stable closing candidate; only real material currentness changes trigger new proof | TEXT_GUARDED / COST TEST OPEN |
| SXR1-05 **P1** | Scaffold is on unmerged branch and DAG binds local SHA as production base | require accepted integrated version-branch source identity and current readback before DAG Freeze; local HEAD cannot stand in | TEXT_GUARDED / INTEGRATION TEST OPEN |
| SXR1-06 **P1** | Partial stub returns success codes, basic test passes, DAG marks corresponding feature DONE | stub is explicitly unimplemented and cannot earn functional PASS; task acceptance remains future; honest negative/contract checks | TEXT_GUARDED / MACHINE TEST OPEN |
| SXR1-07 **P1** | Architect discovers material trust boundary after S2 but planner says no time to reopen L2 | return to L2 contradiction/amendment authority; revised exact source + DAG draft only after legitimate decision | TEXT_GUARDED |
| SXR1-08 **P1** | Bootstrap authority accidentally becomes general feature implementation authority, allowing security code before DAG | minimal contract/build/bootstrap only, strict write set and done predicate; implementation features require Task DAG/Claim | TEXT_GUARDED / ADMISSION TEST OPEN |
| SXR1-09 **P2** | Mature repo is overwritten because Product said "generate a project" literally | reuse or minimally enrich existing accepted project, no destructive rewrite without lawful scope | TEXT_GUARDED |
| SXR1-10 **P2** | Complex multi-host scaffold must pass all E3 platform gates before DAG Freeze, despite E3 being downstream version requirement | only intrinsic scaffold acceptance checks now; owner-approved later gates remain unsatisfied until their real execution, never fake PASS | TEXT_GUARDED |
| SXR1-11 **P2** | Source + DAG in separate commits are rejected for not having identical SHA | paired freeze is a **tuple** (accepted exact scaffold source SHA/tree + DAG checkpoint), not an invented identical SHA guarantee | TEXT_GUARDED |
| SXR1-12 **P2** | After paired freeze, Agent renames cross-cutting schema without L2 amendment and creates downstream PR conflicts | classify impact; lawful architecture/Task DAG/compatibility amendment and only affected revalidation, HIGH_ASSURANCE only by consequence | TEXT_GUARDED |
| SXR1-13 **P1** | Bootstrap work never reaches clean closeout; DAG freezes based on transient generator output | version-integrated exact scaffold + bounded bootstrap gates/terminal are mandatory preconditions for DAG Freeze; no Draft->PASS promotion | TEXT_GUARDED / EVIDENCE TEST OPEN |
| SXR1-14 **P2** | Product promise changed while scaffold paths and basic tests still match | Product owner must amend; derive affected architecture/scaffold/DAG impacts; no unchecked freeze | TEXT_GUARDED |

### Residual design decisions and severity

**P0 AUTHORIZATION / BLOCKER TO NORMATIVE ADOPTION:**
1. Define a **legal exception** to the v4.11 sequence for a **bounded pre-full-DAG** Bootstrap **source** work item. Determine if existing GitHub Work Item + single Bootstrap Claim suffices, or whether the workflow and prerequisite predicate genuinely need a minimal prospective amendment. Must not invent parallel claim authority or create a fourth implementation DAG; verify **source writes rejected without that claim**.
2. Define what **implementation is forbidden** in Bootstrap (normal features, security release behavior, migration) vs what limited executable build/contract wiring counts as scaffold; enforce source/write-set owner identity.

**P1 L2 PROJECTIONS:** exact paired source/DAG checkpoint and currentness test; draft design iterates without duplicate accepted Claims; unresolved cross-module contracts and revision collisions; smoke-gate adequacy (without full E3); candidate stabilization and truthful skipped tests.

**P2 OPTIMIZATION:** measure total planning+bootstrap+implementation rework vs old first-DAG-T00 pattern on an actual project; never assert savings without measurements. Preserve no-scaffold Fast Path and reuse for mature repos.

**Reviewer interpretation:** P0 here means **important unresolved authority architecture that blocks declaring the revised workflow normative/ready**; it is **not a confirmed exploitable source defect in v4.11** and creates no new v4.11 Release blocker.

`AUTHOR_LED_ADVERSARIAL_RESULT=PRODUCT_DIRECTION_COHERENT_BUT_AUTHORITY_DESIGN_OPEN`; `FROZEN_V412_PRD=NO`; `L2=NO`; `REAL_HOST=NOT_RUN`. Keep PR in Draft until normal Product Review/Freeze and L2 owner resolution.


## C15 S.8 — Bidirectional scaffold↔DAG mapping adversarial review

> R0 author-led **static** negative review of candidate C15 §S.8, not a Fresh Independent Review, not actual schema/reducer/Build Host conformance.

**Red-team question:** Is a reversible *mapping* from project skeleton to planned Task concerns meaningful if the two graphs do not share cardinality or authority? **Yes if it is typed many-to-many traceability and two derived query directions; no if enforced as code-file↔Task bijection, inferred native blocker, or self-authorized code generation.** C15 §S.8 explicitly uses a single relation basis and two read projections without an independent writable mapping lifecycle.

| ID | Failure trigger | Reviewer expected outcome | Current candidate |
|---|---|---|---|
| BMR01 P1 | One interface is consumed by six tasks; generator claims six owner writers | `CONSUMES` vs `IMPLEMENTS/MODIFIES` distinguished; contract owner isolated; no duplicate writers | Text covered §S.8.1/.2 |
| BMR02 P1 | Source file imports another module, so mapper inserts mandatory GitHub `blocked_by` edge | No structural-to-authoritative DAG promotion; only genuine integrated prerequisites with authorized mutation | Text covered |
| BMR03 P1 | Two independent Task descriptions both change composition root | Shared mutable collision and central integration ownership resolved before Freeze | Text covered |
| BMR04 P1 | One Task has no code artifacts because it is a test/review/evidence task | No forced fake file or 1:1 mapping; cite relevant test/subject owner | Text covered |
| BMR05 P1 | Public stub compiles, reverse mapping labels Task COMPLETE | Map structural presence, runtime proof separately; no validation PASS | Text covered |
| BMR06 P1 | Frozen DAG SHA paired to one scaffold tree, trace index references older unmerged branch | Exact tuple consistency/currentness hold; no authoritative freeze | Text covered |
| BMR07 P1 | Post-freeze Task legitimately introduces files not in scaffold | Task write set controls; optional refresh affected mapping, no artificial whole-DAG thaw | Text covered |
| BMR08 P2 | Generated/readme/lockfile files create unmapped orphan alarms | Limit to *material* shared/contract/structural seams; explicit Bootstrap owner is enough | Text covered |
| BMR09 P2 | 800 symbols produce 800 reverse links and PR/Review churn | Module/contract/test granularity first; lightweight same-reference relation; not a full-program cross-reference scanner | Text covered |
| BMR10 P2 | A dynamic package is loaded by name at runtime and has no static import | Declare capability/package manifest or contract anchor and bounded ownership; no false claim that all runtime dependencies statically resolved | **OPEN L2 conformance** |
| BMR11 P2 | Rename/redirect a contract file but preserve semantics; mapping key path-based and goes stale | Use stable contract identity and current source location; L2 decides file-move currentness adapter | **OPEN L2** |
| BMR12 P1 | Mapping validator decides which Task/Schema to edit when it sees mismatch | **No autonomous owner selection or normative mutation.** Report finding, route to current L2/Task/Bootstrap owner and hold only actually material freeze/currentness | Text covered |

**Residual unresolved (not a blocker to Product candidate prose, but required before normative or claimed functional proof):**

1. **Canonical-link storage and versioning:** no independently written duplicate mapping; Task Pack/contract references vs a derived manifest. Validate source identity and permissions, not path strings alone.
2. **True Task Dependency vs Code Dependency:** negative tests must show the mapper cannot mutate native `blocked_by` or invent a Task Freeze/Claim.
3. **Dynamic runtime packages:** executable domain package, plugin discovery, generated sources, conditional execution and non-code work must be representable without comprehensive static call graph.
4. **Materiality/economics:** low-risk task needs a few refs only; source-index maintenance must not outweigh intended agent-dispatchability benefit.
5. **Current v4.11 boundary:** candidate mutual mapping does **not** authorize pre-DAG scaffold source writes; the existing SXR1-01 legal-bootstrap authority design blocker remains.
6. **Paired Freeze:** ensure (scaffold exact source, frozen DAG revision, mapped critical anchors) are identity-consistent, while implementation outputs after freeze may lawfully evolve.

**Verdict:** `S8_STATIC_REVIEW=PRODUCT_CANDIDATE_CONCEPT_COHERENT`; `MACHINE_MAPPING_CHECK=NOT_RUN`; `INDEPENDENT_REVIEW=NOT_RUN`; `BOOTSTRAP_PRE_DAG_AUTHORITY=L2_OPEN`; `SCAFFOLD_TASK_DAG_PAIRED_FREEZE=NOT_FROZEN`. Do not make a new independent Task DAG, syntax schema service or interface-per-Task mandate.
