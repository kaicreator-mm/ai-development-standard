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
