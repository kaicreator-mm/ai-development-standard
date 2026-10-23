# ADS v4.17.0 — L1 Product Evidence R2 (unfrozen)

**Current candidate:** PLANNING_ONLY / L1_R2_AUTHOR_REPAIR / R1_FOCUSED_REVIEW_PASS / R1_HOLISTIC_REVIEW_NEEDS_REVISION / R2_NOT_REVIEWED / PRODUCT_FREEZE=NO. Sections 1–5 preserve historical R0; §6 preserves R1; **§7 is current prospective R2 Product disposition**. Reviewer results: [R1 focused PASS](https://github.com/kaicreator-mm/ai-development-standard/issues/1300#issuecomment-6365436658), [holistic P1-A review](https://github.com/kaicreator-mm/ai-development-standard/issues/1279#issuecomment-6365541383).
**Product umbrella:** [#1279](https://github.com/kaicreator-mm/ai-development-standard/issues/1279) · [Product R0 intake #1299](https://github.com/kaicreator-mm/ai-development-standard/issues/1299) · [Independent Review #1300](https://github.com/kaicreator-mm/ai-development-standard/issues/1300).
**Source baseline, NOT a released predecessor:** `version/v4.16@2df2825e47a81ca1b1306e8899d55c49a7a8c776`, Git tree `bb5e7bbfb24c363aed4103b1872aca43b590c0a0`. [v4.16 T07 exact preflight](https://github.com/kaicreator-mm/ai-development-standard/issues/1271#issuecomment-6363964565) and [Python3.14 local source-only result](https://github.com/kaicreator-mm/ai-development-standard/issues/1271#issuecomment-6364342194). v4.16 Release Qualification/main/tag not witnessed. This L1 branch **must never be merged into or used to alter the pending v4.16 source release candidate**.

## 1. Evidence provenance and problem
The v4.17 Product inputs are 12 [Issue-backed concerns](https://github.com/kaicreator-mm/ai-development-standard/issues/1279): research-driven C01–C08 [#1280](https://github.com/kaicreator-mm/ai-development-standard/issues/1280) through [#1287](https://github.com/kaicreator-mm/ai-development-standard/issues/1287), and cross-system C09–C12 [#1295](https://github.com/kaicreator-mm/ai-development-standard/issues/1295) through [#1298](https://github.com/kaicreator-mm/ai-development-standard/issues/1298). Source-study details and paper-specific claims live in those issues and the linked harness-research records; paper benchmark scores **are not ADS regression thresholds**.

Actual existing ADS source already owns most state/control invariants. Therefore v4.17 is NOT an automatic implementation of twelve new standards. First, independently check each concern as `ALREADY_NORMATIVE`, `DOGFOOD_GAP`, or `TRUE_BOUNDED_SPEC_GAP` against the exact immutable predecessor. Missing or stale evidence remains `UNKNOWN_NEEDS_EVIDENCE`; the R0 hypotheses below cannot themselves establish normative gaps.

## 2. Exact original owner/source evidence matrix
These are Git **blob** identities from the provisional version/v4.16 candidate, not current main nor a future release baseline.

| Normative owner | Blob SHA | Existing applicable rule |
| --- | --- | --- |
| `standards/DEVELOPMENT_WORKFLOW.md` | `8d14b25dff70991b07d6ea2d963c86bf0e5a6286` | Stage 0–7, root defect class and bounded non-convergent repair; §8 Evolution admission; §9 lawful authority |
| `standards/VALIDATION_STANDARD.md` | `1522b85f9e68cc4a1591ea5899b53c224998e5a8` | Gate truth, exact-SHA tuple, drift and required verified evidence |
| `standards/ASSURANCE_PLAN_STANDARD.md` | `ddc39f2843e7af4b41b1cf2e6b34675c23bcb614` | Applicable cumulative obligations, owner composition, adverse finding carry |
| `standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` | `3f7189301f7292200a98ebd027372513a801bc03` | Actual effect authority, unknown terminal outcome and retriable recovery (§21) |
| `standards/EXECUTION_ARCHITECTURE_STANDARD.md` | `1f1601a20db08d263955241607dfd08d8b8f77e1` | §11 single Claim, §23 pre-effect, §28 delegated responsibility/causation, §25 loop |
| `standards/CONTEXT_ENGINEERING_STANDARD.md` | `f41135fc95b75c1b077cbbd37e9645bd4bc7ff29` | §2–3 authoritative currentness, §8–9 stale memory/unknown |
| `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` | `dac829232919d495faf8af2d416f4eaaf48f66bf` | §10 passive task-meta and feedback; §16 immutable v4/v5 reports, manifest-free GitHub-only consumer |
| `standards/SKILL_PROCEDURE_GOVERNANCE_STANDARD.md` | `b4ba0074600dc3a3802663093b663e0f23b57da5` | §6–8 Skill version and owner-valid evaluation/currentness |
| `standards/GOLDEN_TEMPLATE_STANDARD.md` | `d7f73f107c9cbd72a89113419b2c3252670aadda` | Positive+forbidden conformance and single owner index |
| `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` | `ce191ddeade78ff822895b0eb8dd2eff48bbf2a6` | Phase-scoped planning and native Task DAG/Claim authority |
| `schemas/github/v4.16/report.schema.json` | `7478313cc006162432649d734e59c5cd77db5106` | Strict report-only v5 summary/feedback/correction; SHAPE_VALID is not Gate PASS |

### Consequences from source inspection
1. C01: root cause and non-convergence already normatively defined. Demand a novel falsifiable defect before altering it.
2. C02: mandatory independent Gate truth is already exact-subject; process-quality warnings cannot change a legitimate PASS or auto-declare FAIL.
3. C03: pre-effect authority and uncertain remote effect are already defined; test both lawful ACT and safe ABSTAIN plus benign timeout, without blanket veto.
4. C04: current Product/L2/Task + cumulative required Validation already bind; test evolving lawful requirements and hidden oracle integrity.
5. C05: authority over memory and fresh GitHub source already explicitly settled; regression tests likely sufficient.
6. C06: delegated causal refs are already required by Execution Architecture §28.2. Need shared **semantic** conflict scenario, not another CRDT/scheduler.
7. C07: Skill qualification, independent verifier and holdout guards already have owners; optional experiment **comparability** and leakage tests are candidates, not universal optimizer runtime.
8. C08: source-qualified `VersionState/Transition/Pivot/Revisit` *behavior counts/denominators* are not established merely by v5 report metrics; most plausible bounded new semantic owner clarification. Previous unqualified v4.16 R7 was withdrawn, never imported.
9. C09: §28.2 already covers inter-Agent causal responsibility and §16 covers reported adoption phases. Require proof that **publicly auditable** decision linkage is missing before adding wire or record semantics.
10. C10: v4/v5 report correction exists and Skill §6–8 handles stale source, but propagated **derived eligibility** across downstream candidate selection merits targeted counterexample and minimal normative clarification if genuinely absent.
11. C11: Golden standard exists, yet no established **cross-project mixed-profile** source-only corpus with producer/reader outcomes was evidenced by this L1. Reuse test owners, not a new Release Gate.
12. C12: v5 metric identity/window/cost bases already exist; private model-route provenance may be unpublishable. Validate public safe comparability rather than infer a new v6 Schema.

## 3. Concern-to-owner gap intake crosswalk

| C | Priority | **Historical R0 hypothesis (superseded by §§6–7)** | Proposed smallest output |
|---|---|---|---|
| C01 #1280 | P0 | likely ALREADY_NORMATIVE | Source-based root-class vs Builder false blame + legal repair fixture |
| C02 #1281 | P0 | likely ALREADY_NORMATIVE | Process diagnostic vs valid/invalid strict Gate fixture |
| C03 #1282 | P0 | DOGFOOD_GAP candidate | Positive ACT / denied ABSTAIN / benign outage no-regression tests |
| C04 #1283 | P0 | DOGFOOD_GAP candidate | Cumulative scope and hidden-grader protection scenarios |
| C05 #1284 | P1 | likely ALREADY_NORMATIVE | Stale memory entry→propagation→recovery fixtures |
| C06 #1285 | P1 | DOGFOOD_GAP candidate | Logical Contract conflict, disjoint-file/legal parallel pair |
| C07 #1286 | P1 | TRUE_BOUNDED_SPEC_GAP vs DOGFOOD_GAP undecided | Bounded matched variant/holdout/ROI/leakage evidence |
| C08 #1287 | P1 | TRUE_BOUNDED_SPEC_GAP candidate | Transition/Pivot/Revisit opportunity-denominator rules |
| C09 #1295 | P0 | ALREADY_NORMATIVE vs DOGFOOD_GAP undecided | Existing public report/feedback Decision→Effect join proof |
| C10 #1296 | P0 | TRUE_BOUNDED_SPEC_GAP candidate | Revocation/requalification/old BUILD truth table |
| C11 #1297 | P0 | DOGFOOD_GAP candidate | Shared GitHub-only v3/v4/v5 positive+negative Golden |
| C12 #1298 | P1 | ALREADY_NORMATIVE vs PRIVACY/TRUE_BOUNDED_SPEC_GAP undecided | Versioned public metric comparability/capability matrix |

**Historical R0 classifications are hypotheses**, not final admissions, blockers or approvals. §6 and then current §7 supersede these statuses. A later review must give exact text and one conformance positive/negative per Concern; only confirmed `TRUE_BOUNDED_SPEC_GAP` becomes a normative Task candidate.

## 4. Cross-project boundaries and acceptance evidence
- ADS defines only source-authoritative semantics, public contract/version, Golden and qualification.
- [task-meta v0.3 #27](https://github.com/kaicreator-mm/task-meta/issues/27) handles later factual collection, immutable private journal, public Report publication/correction and observed usage; active v0.2 unaffected.
- [Tally future TypeScript+DomainHarness #70–#72](https://github.com/kaicreator-mm/tally/issues/70) handles Engineering B decisions and derived candidate validity; selected S contextual support and **one K** admission/state/effect, C GitHub read/write. No Tally direct task-meta API/manifest/DB/Trace.
- GitHub native Issue/PR/CI/Review and actual Host retain original Engineering/Effect evidence authority; source-only ADS Golden cannot claim end-to-end runtime, task-meta/Tally #1210 remains NOT_RUN unless independently executed.
- v3/v4/v5 historical Schema and report family remain immutable. A prospective public field or version must prove its necessity and safe read compatibility; never invent current v5 keys.

## 5. L1 next checkpoint and source-freeze boundary
1. Independent Product Review [#1300](https://github.com/kaicreator-mm/ai-development-standard/issues/1300) must inspect **exact planning-branch source blobs** and concerns; output P0/P1/P2, `PRODUCT_FREEZE_READY`, and needed repairs (reviewer must be independent from this author).
2. If Review finds P1, repair this R0 candidate prospectively; reviewer performs focused delta, not a fake self-review.
3. Re-read Final Validator/Release Qualification and actual immutable v4.16 qualified predecessor **before** approving Product Freeze and effective v4.17 source compatibility. Pending v4.16 must not be silently treated as released.
4. Product R0 → independent acceptance → Product Freeze → L2 Freeze → Task DAG Freeze → version branch implementation. Source-only PRD is not a Task/Claim/Runner; no main merge.

**Historical R0 status:** SOURCE_READ, PRD_R0_CANDIDATE, VALIDATION_NOT_RUN, REVIEW_NOT_RUN, PRODUCT_FREEZE_NO, V417_IMPLEMENTATION_NOT_RUN. Later independent R0 Review and author R1 repair are in §6.

## 6. Product R1 — independent R0 Review disposition and exact-source gap adjudication (prospective)

**Historical R0 independent Review:** [#1300 comment #6365054251](https://github.com/kaicreator-mm/ai-development-standard/issues/1300#issuecomment-6365054251), inspected H `1056c36be31e6aae83ff3ca5e012fbed67b71681`, L1 blob `7e4a686f33e46599b20b9cb01ac9eb3ff49e8be0` and PRD blob `8505e5fd2c67ace9c14fe15c8abe9835c085f76b`. Verdict `NEEDS_REVISION / P0=0 P1=2 P2=2 / PRODUCT_FREEZE_READY=NO`. This was **author-owned R1 repair**, subsequently independently focused-delta reviewed at exact H `17560a6a9778a78575b230bee0e5242e02762f9c`, L1 blob `6e78ecdc6bb7034b3fea7b5afa33235b84fd4f40`, PRD blob `368361de8d4267f3805ab31f4b012ccad5e28bfc`; [R1 focused PASS](https://github.com/kaicreator-mm/ai-development-standard/issues/1300#issuecomment-6365436658), P0=0/P1=0/P2=2. A separate [holistic review](https://github.com/kaicreator-mm/ai-development-standard/issues/1279#issuecomment-6365541383) found new P1-A: C08 lacked observable strategy identity, so Product still NOT freeze-ready.

### Finalized R1 Product classification by current provisional owner
| Source classification | Concerns | Normative v4.17 authoring disposition |
| --- | --- | --- |
| `ALREADY_NORMATIVE` | C01 #1280, C02 #1281, C05 #1284 | **No normative rewrite.** Retain source-qualified tests/examples and product rationale, route execution failures to original owner. Do not require implementation Tasks for these Concern labels. |
| `DOGFOOD_GAP` | C03 #1282, C04 #1283, C06 #1285, C07 #1286, C09 #1295, C11 #1297, C12 #1298 | Keep bounded existing-owner positive+negative Golden, capability matrix or reference-only public join; do not create new gate, decision protocol, provider metrics or schema by implication. |
| `TRUE_BOUNDED_SPEC_GAP` | C08 #1287 and C10 #1296 | Candidate narrow ADS semantic clarification only: source-qualified trajectory/denominators, and consumer-facing dependency evidence/currentness. Tally owns derived candidate state/actions, not ADS. Future Task admission still needs Product+L2+DAG Freeze. |

**Authoritative source-owner pins unchanged from §2.** C08 is scoped to GitHub Agent Interaction §10 and v5 source interpretation, **not** modifying `schemas/github/v4.16/report.schema.json` bytes. C10 is scoped to GitHub Agent Interaction §16.6–16.7, Context Engineering §2–3 and Skill Procedure §6–8; `EXECUTION_ARCHITECTURE` §29.6 already handles native Dispatch but not Tally business-derived Candidate eligibility. Derived assessment is never a new ADS event/Claim/Gate lifecycle.

### C08 R1 semantic definitions — count only source-qualified observation

All labels below are **optional bounded analysis concepts, not public v5 enums, fields or mandatory tracing**:

| Concept | Qualification / stable identity | Not sufficient |
| --- | --- | --- |
| `VersionState` | Exact repository/source version or artifact SHA/blob+governed strategy/goal reference+scope+independently resolvable evidence owner, with one unique analysis key | Timestamp, Git diff, source branch label alone or untrusted model explanation |
| `Transition` | One distinct source-qualified causal predecessor→successor operation between VersionStates with observed ordering/native lineage and a stable operation/ref key; dedupe same source occurrence | Repeated event delivery, parallel incomparable branches, approximate wall clock or manufactured sequential sort |
| `Pivot` | Qualified Transition plus actual authoritative strategy/goal **change** under same comparison scope; governing owner and before/after strategy intent must be evidenced | Source code change without goal/strategy owner decision; inferred intention from failed tests |
| `Revisit` | Qualified Transition from a departed strategy lineage, with an earlier witnessed A→B departure and new A′ *owner-verified strategy equivalence* (same governed strategy/goal reference or supported compatibility/equivalence evidence, including scope/currentness); exact file SHA need not equal A | Same command twice, failed rollback, merely reverted code text, A and A′ inferred similar from descriptions |

**Denominator and missingness truth:** `D_pivot` = unique independently witnessed comparable **Transition opportunities** with qualified before/after owner-backed strategy identity and in-scope change eligibility; `N_pivot` = those D_pivot with a witnessed strategy/goal change. `D_revisit` = unique witnessed comparable transition opportunities with an **observed** prior departure, adequate known lineage/history and authoritative strategy equivalence predicate resolvable on that opportunity; `N_revisit` = those D_revisit with actual qualified return to an earlier departed strategy. One transition can be eligible for both metrics but each is counted at most once **within each** metric; no source-independent `N/D` generalization. Opportunities whose intermediate version/branch ordering, owner-goal identity, capture coverage or correction are UNKNOWN are **explicit UNKNOWN/excluded from numerator *and* denominator**, with `unknown_opportunities` and observation coverage disclosed separately; no missing-as-no-Pivot. If all eligible opportunities absent then denominator 0 ⇒ `NOT_COMPARABLE/INSUFFICIENT_EVIDENCE`, **not 0%**. A partial trace subset rate cannot be sold as global Agent success, improvement or behavior frequency. Multiple parallel causal paths can be counted independently only if their stable qualified transition identities and eligible opportunity basis are distinct; no artificial global serial order.

**Counterexample pairs:**
- ACT: A(source-strategy=goal-X, exact sha A) → B(goal-Y, sha B) → A′(goal-X, SHA C, owner-qualified equivalence) has 2 distinct observed strategy change Transitions. `D_pivot=2,N_pivot=2`. Only second Transition has witnessed earlier departure and qualifying return: `D_revisit=1,N_revisit=1` under the scoped opportunity rule.
- ABSTAIN: A→B followed by a failed filesystem reset or same command replay without new governed strategy/equivalence evidence => `Revisit` NOT proven; disputed missing B→A′ evidence is UNKNOWN and contributes to neither N nor D. Incomparably parallel A/B histories cannot be temporally sorted into a Pivot.
- TRUE NEGATIVE: fully witnessed change to new code while strategy owner remains goal-X, and all required before/after strategy identities are resolved: `D_pivot=1,N_pivot=0` (do not force ABSTAIN for lawful unchanged strategy).

### C10 R1 source-derived validity and requalification truth table

**Dependency identity:** derived user-visible recommendation/context/eligibility must retain the bounded set of **material public report/native source claims it actually consumed**: canonical GitHub repository/Issue/native comment ID+digest, originating report namespace/id/revision, Task/Attempt/ADS pin/profile, actual source and owner/readback. Do not make every historical report globally mandatory; only inputs that actually support a material decision are relevant. Native GitHub correction owner/currentness resolution in GitHub Interaction §16.6 controls **input facts**, not any new Tally Candidate lifecycle.

| Source evidence read on future material consumption/promotion | ADS consumer qualification of dependent premise | Tally/Host/DomainHarness boundary |
| --- | --- | --- |
| `VERIFIED_CURRENT` with complete bounded pagination, correct owner/target digest, applicable source and surviving source evidence | Eligible for **further owning qualification**, not auto-PASS or automatic application. A correction to unrelated nonmaterial evidence does not invalidate an independent premise. | Tally may assess Candidate via existing business rules; actual Task/Build/effect requires native authority and K admission. |
| `VERIFIED_REVOKED_OR_STALE` by aligned authorized REVOKE/REDACT or material source correction that negates a consumed premise | Dependent conclusion is **no longer qualified for a NEW material selection, promotion, or admission** until independently requalified. Preserve original bytes/lineage and prior observed decisions. A replacement report is a separately verified new source proof. | Tally recalculates only affected Context/Candidate; already-running occurrence remains exact BUILD-pinned, old Host/Task receipts unchanged. New rollback needs existing authorized owner path. |
| `UNVERIFIABLE_OR_PARTIAL` (missing page, 403/429 exhaustion, wrong source SHA, absent owner witness, checksum conflict, mixed-profile incompatibility) | For a *materially dependent* NEW use, `UNKNOWN/INSUFFICIENT_EVIDENCE`: **no positive qualification by absence**; bound retries and refer to owner. | Do not auto-revoke historical Build; Tally must fail closed on new candidate relying on unknown evidence. |
| `FOREIGN_DISPUTED` or malformed/other-namespace correction (no target-owner match) | Does **not** revoke verified source by itself. Preserve DISPUTED/UNVERIFIED notice and independently check whether a new currentness/authority conflict exists. | No speculative cascade invalidation or secret tombstone. If a material currentness conflict remains unresolved, fresh selection must remain UNKNOWN. |

**Boundary timing:** reevaluate at each material **new** context assembly, candidate ranking or adoption decision, before *new* execution/BUILD authorization, and when stale correction is newly observed at the next lawful consumption checkpoint. No synchronous polling requirement, no retroactive false Task FAIL, no automatic running Package mutation/rollback, no new ADS Gate. Nonmaterial corrected metrics cannot invalidate unrelated verified procedure claims; where support is mixed, retained independent premises may still qualify without relying on the revoked input.

**Pairs:** (a) owner-aligned correction revokes sole R1 support for P ⇒ P not eligible for a new Task until separately requalified, old P-running BUILD unchanged; (b) unrelated correction to Q ⇒ P retains valid independent sources; (c) cross-namespace DISPUTE about R1 with verified original intact ⇒ no automatic revocation; (d) partially paginated GitHub history ⇒ UNKNOWN for new relying decision, not clean absence or 0; (e) later owner-verified replacement source can restore future eligibility through ordinary Tally/owner decision, not an ADS automatic approval.

### C09 / C07 / C11 / C12 bounded public-reference and compatibility evidence (R1 P2 closure input)

**Illustrative reference-only joined journey, NOT a wire payload:** `canonical GitHub Task Issue/Attempt/actual accepted Claim` + `ADS pinned public EXECUTION_SUMMARY (report_id/revision/publisher_namespace/native comment URL+ID/digest/source_refs)` → Tally C GitHub completes bounded readback and forms *local/advisory decision* with `experience_ref/procedure_revision` → accepted native Task/Dispatch/BUILD and independently witnessed Host/K Effect where actually authorized → Tally publishes **existing** `EXPERIENCE_USE_FEEDBACK` referencing source-qualified current Task/Attempt, experience/procedure revision, epistemic phase and source refs, with publisher+ADS subject pin, then native GitHub identity/digest readback. Do not publish Tally's local decision schema as a new ADS record, put raw manifest in feedback, or treat source refs as authenticated without resolving their native authority. If K/Host receipt is private/unobservable, the public “effectiveness” join stays `UNKNOWN`, even if feedback phase is self-reported APPLIED. `§28.2` reconstructible delegation is authority-bearing causation; this Tally advice chain is **not** Claim permission.

| Public consumer / metric capability case | Required disposition, and negative proof |
| --- | --- |
| v3 native Issue/Event with compatible pin; v4 report-only supported reader | Admit by effective per-kind pin; v3 is not inferred to contain report fields, v4 profile validates only its own governed kind. |
| v5 report on v5-capable, explicitly adopted producer/consumer | Safe public projection, dedupe by verified namespace/report id/revision+native ID/digest, not timestamps; source ref still requires witness. |
| v4-only reader sees v5 or mixed unadopted stream | `UNSUPPORTED` for comment and `UNKNOWN` for cross-profile absence/denominator; **not zero Attempts**, no silent downgrade or default v5 publication. |
| Native GitHub pagination incomplete, edit/digest mismatch, 429/403, foreign correction | `UNKNOWN/INSUFFICIENT_EVIDENCE` or `DISPUTED/UNVERIFIED` for affected premise, not fabricated no-report evidence or automatic REVOKE. |
| Public metric same unit/window/physical attempt/coverage, witnessed actual observed/billed basis | Source-qualified aggregation and comparison on the compatible cohort; each logical/physical observation counted once under current v5 ledger/correction. |
| Logical retry vs physical attempts, multiple overlapping call windows, estimate later billed | Separate identity, overlap and pricing revisions; no retry or estimate+bill double-count. `ESTIMATED` and `BILLED` remain distinct bases. |
| Provider/model route classified private/unwitnessed, only aggregate public | Publish only clearance-allowed aggregate; route-level comparison `UNKNOWN/NOT_COMPARABLE`, never infer model name from prose, hidden manifest or opaque cost. |
| Matched optional Skill experiment baseline/holdout/cohort with legal measurement | Qualification still requires independent holdout/no leakage, observed full cost/coverage and ordinary Skill/project authority; in-sample apparent uplift alone never qualifies a Build. |

These are bounded source-only **conformance candidates**, not synthetic runtime successes or a mandatory global evaluator. Real downstream task-meta/Tally #1210/#1231 remains `NOT_RUN` until actually witnessed; tests may be Python3.14 but semantics remain language-neutral.

### Product R1 further exit
- Independent fresh **focused R0→R1 blob delta review** of ONLY these two planning files must verify P1-01, P1-02, P2-01, P2-02 and new regressions; no self-PASS.
- v4.16 frozen Release Qualification has a conditional source-only finding; real main merge/tag/adoption and any current predecessor pointer must be re-read before Product Freeze. This planning source cannot be automatically published or merged as v4.16.
- `PRODUCT_FREEZE=NO / L2_FREEZE=NO / TASK_DAG=NOT_ADMITTED / V417_IMPLEMENTATION=NOT_RUN` until owner authority explicitly accepts reviewed Product.


## 7. Product R2 — holistic Claude Review repair: observable C08 + bounded version delivery

**Input:** independent [holistic Product source review, #1279@6365541383](https://github.com/kaicreator-mm/ai-development-standard/issues/1279#issuecomment-6365541383), P0=0/P1=1/P2=4 plus 2 carried. This §7 prospectively supersedes R1 §6 where evidence-class observability or output disposition differs. It does NOT invalidate the narrow original R1 focused PASS. Current Product R2 is **unreviewed author input**; no Freeze, implementation Task or v4.16 baseline promotion.

### 7.1 C08 P1-A resolution — real observed carrier OR explicitly inferred diagnostic, always separated

**Decision:** choose the existing-owner evidence-class approach, **without a new report wire**. Existing `GITHUB_AGENT_INTERACTION_PROTOCOL.md` §10 Level 3 explicitly allows `OBSERVED | SELF_REPORTED | INFERRED | UNKNOWN` per claim and privacy/source-qualified contextual use; it does not require a new raw Trace or public `strategy_id` field. C08 previously proposed `StrategyCandidateRef`: this is a **read-only logical reference** to an actual lawful versioned Product/Task/PRD/approved strategy/procedure/Skill decision when one exists, *not a new ADS field or permission*. It can be absent.

- **Carrier A (OBSERVED source-qualified)**: a bounded *existing* GitHub native Task/Issue + frozen Product/PRD/Task amendment or authorized strategy/procedure/decision reference whose owning authority actually identifies **goal/strategy before and after** with exact subject pin, lawful acceptance/currentness and causally ordered version operation. The observed fact is the native **accepted strategy decision**, not the mere existence of a comment. `A′` equivalence requires owner-accepted strategy reference/lineage or independently source-qualified compatibility/equivalence for the compared goal/scope. If the subject has no such carrier, **OBSERVED eligibility is UNKNOWN**, never filled by classification.
- **Carrier B (INFERRED bounded diagnostic)**: an analysis of actually available GitHub PR source diffs/issue context/Task Learning/step summaries/version lineage with a **declared** classification hypothesis, source evidence refs, `classifier_or_labeler_revision`, rule/version provenance, capture-window/cohort, ordering/evidence class, contradictory counterevidence and uncertainty. Observing a Git commit or report is OBSERVED *as a fact*; interpreting it as a Pivot/Revisit is **INFERRED**, not an authoritative goal decision. A source-owning self-report is `SELF_REPORTED`, also **not** OBSERVED until separately corroborated. Do not invent a strategy identity solely from a code diff or LLM output, do not silently raise INFERRED to OBSERVED, and do not infer Task/Gate PASS, intentional improvement or effect.
- **Carrier C (UNKNOWN/UNQUALIFIED)**: no stable source+classifier/capture opportunity, missing causal lineage, contradictory/missing owner, insufficient permissions/privacy, or incompatible version/profile. Emit `UNKNOWN/NOT_COMPARABLE`; never numeric 0 for unavailable opportunities. Projects without sufficient signals may legitimately have **no C08 quantitative result**, rather than a compulsory capture instrument.

**Denominators must remain distinct from R1 §6 strict calculations:**
- `N_obs_pivot/D_obs_pivot`, `N_obs_revisit/D_obs_revisit`: only independently source-qualified owner-accepted strategy/goal transitions (R1 §6). `D_obs=0` => OBSERVED NOT_COMPARABLE, not 0%.
- `N_inf_pivot/D_inf_pivot`, `N_inf_revisit/D_inf_revisit`: **only classifier-eligible, trace-covered unique transitions in a specified source cohort**, with stable version/operation identity, observable causal ordering and fixed labeler revision. Labeler evidence can classify `PIVOT_CANDIDATE` or `REVISIT_CANDIDATE` with explicitly inferred equivalence; rejected candidate with sufficient measured input stays a measured inferred negative. Unlabelable/missing history/ordering/coverage stays UNKNOWN and is excluded from *both* N_inf and D_inf, with `excluded_unknown_count` and coverage. These metrics describe **frequency of the stated model's labels on eligible evidence**, not actual Pivot/Revisit behavior prevalence or independent verification.
- Never combine OBSERVED and INFERRED numerators/denominators, promote private classifier labels to v5 public report facts, or use any Pivot/revisit rate as a Task/Release/Agent effectiveness Gate. Distinct labeler revisions/cohorts/windows cannot be compared as one rate without separately qualified mapping; no cross-branch artificial ordering.

**Positive and forbidden pairs on real available surfaces:**
1. Public owner-approved Task vA strategy X → authorized changed Task vB strategy Y → later owner-approved equivalent X′ with causal native refs ⇒ **OBSERVED** two qualified Pivots and one eligible Revisit (where R1 opportunity qualification satisfied); exact code SHAs may differ.
2. PR diff + Issue note + witnessed commit ancestry without an approved strategy decision ⇒ optional **INFERRED** label from an identified labeler revision and source cohort only, separately reported; forbidden to call this OBSERVED or assert true causal benefit.
3. Self-declared Agent intent conflicting with Task-approved goal ⇒ preserve `SELF_REPORTED` vs OBSERVED contradiction; never silently select self-report as owner truth.
4. Unrated version/verifier outcome, denied/private publication or not-yet-adopted v5 reader ⇒ legal source-only local classification may remain private; public projected metric withheld or UNSUPPORTED/UNKNOWN. A failed rollback, duplicate command, incomparable parallel paths or missing intermediate leaves actual Revisit unqualified.
5. Current owner intent unchanged across a valid witnessed code edit ⇒ OBSERVED Pivot true negative (0/1 on its own eligible comparison basis). Inferred variant can also emit negative label when full classifier features are present; no obligation to agree with OBSERVED.

**No inference from current carrier availability alone:** This Product decision makes C08 **potentially useful on real GitHub-native material**, not a claim that any active task-meta/Tally build already captures enough transitions to measure it, nor a claim of any witnessed real Pivot sample. Without actual source coverage it remains UNKNOWN. In L2, independently check that the optional read-only Level 3 path is demonstrable using a real GitHub-supported input shape **without inventing new v5 public fields**; Golden positive/negative fixture proves semantic feasibility only.

### 7.2 Output type / closure matrix (supersedes R0 §3 priorities as implementation count)

Risk priority remains original for affected behavior but **does not authorize work that is already normative**:

| FR / concern | Actual ADS v4.17 deliverable type | Existing owner / gate and closure route |
| --- | --- | --- |
| FR01 C01 #1280, FR02 C02 #1281, FR05 C05 #1284 | `CLOSE_WITH_REFERENCE` | Reference current DEVELOPMENT_WORKFLOW, VALIDATION/ASSURANCE, CONTEXT; no new source/Task; preserve useful positive/forbidden cases as linked existing coverage (not 3 new suites) |
| FR03 C03, FR04 C04, FR06 C06, FR07 C07, FR09 C09, FR11 C11, FR12 C12 | `GOLDEN_FIXTURE` | Extend a **bounded shared existing-owner** positive/negative Golden/reference corpus as needed, reuse current tests and schema; no new normative policy, runtime Agent judge or E2E Gate |
| FR08 C08 #1287 | `NORMATIVE_CLARIFICATION` | Prospective GitHub Interaction §10 Level 3 behavior semantics + optionally referenced interpretive positive/forbidden corpus; no original strict v5 Schema mutation |
| FR10 C10 #1296 | `NORMATIVE_CLARIFICATION` | Prospective GitHub Interaction §16.6 / §16.7 cross-source derived *input* applicability only, not Tally Candidate state, no new Claim/Gate/REST bus |

**CLOSE_WITH_REFERENCE handling:** On Product freeze, mark C01/C02/C05 normative rewrite candidate **already covered**, referencing exact owner and Golden; the original intake Issues remain historical and may be closed as `not_planned / superseded by already-owned norm` only after reviewer/owner reconciliation, not silently converted into executable implementation Tasks. DOGFOOD issues may be grouped into one small source-only Golden concern **if write sets and owner test purposes allow**, not seven duplicate PRs.

### 7.3 Release content, bounded Golden plan and measurable Definition of Done

**Prospective source owners** only (final allowed Task write sets and owner approval belong to frozen L2/DAG):
- Normative delta at existing `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` §10 for C08 and §16.6–16.7 for C10 **only if** final independent source-gap review confirms distinct semantics not already owned. Preserve old v3/v4/v5 strict schemas untouched; if needed, a *future* wire version requires a separate full Product+compatibility review, not a hidden v4.17 add-on.
- Reuse `templates/golden/STANDARD_COVERAGE.json`, existing `templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md`, `tests/test_v415_consumer.py` and source-only coverage where suitable, plus a scoped new v4.17 conformance test/reference file only if useful. Add/adjust `standard-manifest.json` **only for genuinely created canonical assets**, and only after Task scope authorization; do not duplicate a standard coverage registry entry.
- Existing `DEVELOPMENT_WORKFLOW`, `VALIDATION_STANDARD`, `CONTEXT_ENGINEERING_STANDARD`, `EXECUTION_ARCHITECTURE_STANDARD`, `RELEASE_STANDARD`, `SKILL_PROCEDURE_GOVERNANCE_STANDARD` retained unchanged unless independently proven actual gap; no default gate.

**Initial Golden **budget**: a bounded *planning target*, not a new universal test quota/Gate:** maximum **14 paired scenarios** across one shared reference corpus: **4 C08** (OBSERVED, INFERRED/self-report conflict, duplicates/parallel/missing, private/ungraded/not-adopted), **4 C10** (verified revoke, partial/unverified, foreign dispute, independent premise/BUILD-pinned continuity) and **6 shared** (C03 ACT/ABSTAIN+ACK, C04 evolving scope, C06 shared ABI, C07 holdout contamination, C09 public join, C11/C12 mixed version/metrics/privacy). Reuse preexisting fixtures when they satisfy a pair. Any gap needing more than 14 pairs requires an explicitly reviewed L2/Task scope amendment; do not inflate into 12 independent mini test frameworks.

**v4.17 source Release DoD:**
1. Product R2 L1/PRD independently reviewed and explicitly Frozen **after** source-owner/candidate release predecessor confirmed; exact SHA/Blob and R1/holistic adverse findings resolved/prospectively carried.
2. L2 design independently reviewed/Frozen, legal DAG from only **confirmed** normative and evidence concerns with disjoint write sets and true native dependencies, and each Task has actual tests/review.
3. Same final v4.17 source SHA/Tree: language-neutral semantics in owner paragraphs, actual executable positive/forbidden conformance, unchanged legacy v3/v4/v5 schema bytes, old-reader UNSUPPORTED and privacy/invalid-source refusal, manifest/coverage consistent.
4. Applicable actual Full Regression, source Critical Journeys, source Packaging/manifest, applicable Hidden determination, independent composed-version Review and **separate Release Qualification** on exact frozen candidate; PASS may not be claimed from a draft, source fixture alone or another SHA.
5. Publish only through existing Version/Release/Main integration authority and immutable ADS revision adoption; no Task/Review/Validation/Release extra Gate, no Tally or task-meta code changes, no real downstream E2E claim (#1210/#1231 remain separate and NOT_RUN unless independently executed).

**Version value decision:** v4.17 as a minor standards version is justified only by accepted C08 and/or C10 **actual normative semantic clarification** and associated source-only coverage; if Product ultimately confirms **only Golden/dogfood without any normative delta**, record a version-scope decision instead of shipping a duplicate feature-version just because twelve Issues exist.

### 7.4 Pre-Freeze currentness and outstanding gates
- Source-only R1 focused Review [#1300@6365436658](https://github.com/kaicreator-mm/ai-development-standard/issues/1300#issuecomment-6365436658) PASS at `17560a6...` remains scoped to its original four findings. Holistic #1279 P1-A and P2 are addressed *as proposed* in this R2; independent R2 reviewer must recheck **all**.
- Current provisional v4.16 `2df2825...` RQ was **CONDITIONAL**; [#1271](https://github.com/kaicreator-mm/ai-development-standard/issues/1271) A03 repair PR #1301 is a separately owned version-only concern and may change qualified predecessor SHA/tree. No implied main merge, release/tag or v4.17 effective adoption from current planning branch.
- `PRODUCT_R2_REVIEW=NOT_RUN; PRODUCT_FREEZE_READY=NO; PRODUCT_FREEZE=NO; L2_FREEZE=NO; TASK_DAG=NOT_ADMITTED`. Future exact R2 commit+blob identifiers are provided by GitHub diff/Review handoff, **not** guessed here.
