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
