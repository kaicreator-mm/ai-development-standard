# ADS v4.17.0 — Product Requirements Document R0

**Document state:** `PRD_R0_CANDIDATE / UNREVIEWED / NOT_FROZEN / NO_EXECUTABLE_TASK_AUTHORITY`.
**Owning Product:** [#1279](https://github.com/kaicreator-mm/ai-development-standard/issues/1279); [Product R0 #1299](https://github.com/kaicreator-mm/ai-development-standard/issues/1299), [Independent Product Review #1300](https://github.com/kaicreator-mm/ai-development-standard/issues/1300).
**Supporting L1:** [L1_PRODUCT_EVIDENCE.md](L1_PRODUCT_EVIDENCE.md); source read provisional `version/v4.16@2df2825e47a81ca1b1306e8899d55c49a7a8c776`. **This is not the final qualified v4.16 predecessor**: Final Validator local source-only PASS and Release Qualification not yet concluded.

## 1. Product value and non-negotiable outcomes
v4.17 strengthens **source-qualified Agent engineering reliability, process evaluation, bounded recovery, evidence-based evolution and interoperable public feedback**, without turning ADS into a runtime or duplicating existing standards. At the end, a project can (a) prove first-divergence/correct owner, (b) exercise legal positive ACT and safe refusal ABSTAIN, (c) verify cumulative evolving requirements with independent oracles, (d) resolve stale memories and multi-Agent conflicts, (e) compare optional Harness/Skill changes without leaking evaluators, (f) produce source-qualified behavior/evidence→decision→effect→feedback claims, (g) handle source corrections and changed eligibility, and (h) test GitHub-only task-meta/Tally consumer compatibility.

ADS defines only standard semantics + language-neutral Golden/forbidden conformance. It does **not** implement task-meta private source capture, Tally Agent registry/policies/strategy selection, DomainHarness Kernel or external provider/Host effects.

## 2. In scope: bounded, concern-backed candidate requirements

| FR / concerns | Priority | Product requirement and constraint | Positive/negative acceptance |
| --- | --- | --- | --- |
| FR01 Failure convergence (C01 #1280) | P0 | Classify first true divergence among Product/Architecture/Verifier/Implementation/Environment/Attribution, route to existing root owner, demand falsifiable recovery; nonconvergence escalates rather than blindly retrying | Product contract caused Builder-visible failure routes to Product, valid implementation bug routes to Builder; false fix only bypassing check rejected |
| FR02 Verifier/lucky-pass discipline (C02 #1281) | P0 | Distinguish terminal required checks vs optional process warning; partial/unobserved steps and fabricated output never cause PASS; actual exact-subject verified PASS remains valid within its scope | 6/7 mandatory clauses do not pass; 7/7 evidenced pass survives advisory inefficient-trace warning |
| FR03 ACT/ABSTAIN external safety (C03 #1282) | P0 | Apply existing Claim/write-set/capability/pre-effect/uncertain-ACK controls; do not deny legal low-risk ACT or mint a global human gate | Admitted Tool write allowed; same Task stale Claim/write-set violation refused; benign timeout recovered without duplicate irreversible effect |
| FR04 Evolving-scope cumulative assurance (C04 #1283) | P0 | Preserve lawfully active prior acceptance when scope evolves, protect independent hidden oracle, separate source-only fixtures from actual Host/platform verification | New valid feature that breaks prior required safety test rejected; held-out grader exposed to proposer invalidates evaluation |
| FR05 Currentness vs historical memory (C05 #1284) | P1 | Retrieved/attractive old memory cannot override latest qualified Product/Task/Review/ABI; preserve historical negative provenance and recovery | Old PASS SHA A conflicts with new Task SHA B ⇒ B currentness governs; consistent current retrieved Skill may still help |
| FR06 Multi-Agent shared semantic conflict (C06 #1285) | P1 | Evidence of contract-level shared state and delegated responsibility/Claim causal chain; protect legitimately disjoint parallel Agents; no second state machine/CRDT | Two disjoint files modify same shared ABI ⇒ conflict; two genuinely independent file changes proceed concurrently |
| FR07 Evaluation generalization / cost (C07 #1286) | P1 | Optional matched baseline, cohort, source/environment pin, true independent verifier, held-out contamination exclusion, effects and total experiment/maintenance cost; no training/optimizer | In-sample gain plus held-out regression or oracle leak cannot promote candidate; independently verified beneficial candidate can proceed through existing owner |
| FR08 TraceML behavior qualification (C08 #1287) | P1 | Define source-qualified VersionState, Transition, Pivot and Revisit, legitimate causal edges/opportunity denominator, duplicate and missing-trace uncertainty, no inferred intent from diffs | A→B→A′ proven revisit count; duplicate command, rollback failure, missing intermediate state not auto counted |
| FR09 Evidence-to-decision causal trace (C09 #1295) | P0 | Audit publicly qualified Task/Attempt/ADS+Report revision → advisory Tally choice/Procedure rev → authorized native effect → observed outcome, using existing link semantics and feedback; no private manifest fetch | PRESENTED-but-not-APPLIED is not adoption; APPLIED without independent verifier cannot be claimed effective/Task PASS |
| FR10 Derived eligibility after correction (C10 #1296) | P0 | When original source is lawfully corrected/revoked/stale, downstream derived applicability/Candidate decisions must be requalified, preserving historical facts, existing BUILD occurrence and K effect authority | Authorized revoke prevents new unqualified promotion, but cannot retroactively rewrite Task or change running BUILD; foreign notice rejected |
| FR11 Cross-project Golden qualification (C11 #1297) | P0 | Shared **source-only** ADS test inputs/oracles for mixed-profile producer/consumer, native GitHub digest/revision/readback, partial coverage, corrections, provenance, privacy, feedback; distinguish runtime E2E NOT_RUN | Supported writer/reader works; v4-only reader encountering v5 ⇒ UNSUPPORTED, not empty; missing page ⇒ UNKNOWN |
| FR12 Public metric comparison (C12 #1298) | P1 | Version-qualified public capabilities and safe comparable measurement window/attempt/cost/route semantics; private model route never guessed; reuse v5 strict fields | Legitimately public comparable calls count once; provider route withheld / estimated vs billed incomparable without receipts |

**Important Product admission:** The 12 FRs are *problem/acceptance candidates*, not twelve guaranteed new standards or Task issues. Existing owner and Golden reuse are the default. The reviewer must determine whether existing norms already satisfy a FR and avoid adding source changes for it.

## 3. Mandatory contract invariants
- **Single engineering truth:** GitHub native Task/Dependencies/PR/CI/Review/accepted Claim and actual Host own their real facts; Report/Task Learning and Tally projections cannot mint Task/Review/Validation/Release PASS.
- **Source identity:** Pin effective immutable ADS revision/profile, subject SHA/Task/Attempt, observer/report source, native GitHub ID, integrity/currentness, actor role/session distinct from transport login; never infer missing identity from timestamps or model brand.
- **Epistemic evidence:** OBSERVED, SELF_REPORTED, INFERRED, UNKNOWN kept separate with capture coverage; UNKNOWN is not zero, absent a complete page is not proof of absent Task, and a successful CI job is not general Release PASS.
- **Correction/invalidation:** Preserve original immutable record; allowed corrections/late revisions apply per original owner and compatible wire; derived eligibility re-evaluation never edits historical Effect or secretly hot-swaps live Package.
- **Evolution:** Task Learning/telemetry are inputs only; Product Evidence→PRD→L2→Task DAG→Validation→Review→Release still required for normative changes.
- **Isolation:** No mandatory new gate/judge/scorer, agent optimizer, skill generator, backend, Tally direct task-meta API/DB/manifest/Trace, provider-specific hook, raw chain-of-thought/prompt publication, or private grader disclosure.
- **Compatibility:** Keep v3/v4/v5 historical schema bytes untouched; only future separately approved public wire/projection if actual bounded semantic gap proven. v5 opt-in requires lawful qualified current adoption; old-reader UNSUPPORTED is expected.
- **Proportionality:** Optional simulations/quality/process warnings do not block a legitimate simple Task or weaken required validation. Reuse source-unchanged local tests and justify extra Host/CI by impact.

## 4. Key user journeys and falsifiable cases
**J1 Normal success / legal ACT:** Project uses current frozen Task+ADS pin, permitted Tool capability and Claim; independent evidence proves actual operation and applicable Gate. A diagnostic suggesting inefficiency must not turn true PASS into FAIL. Evidence/feedback distinguishes recommendation, application and independent effect.

**J2 Safe failure / denial / recovery:** expired Claim or wrong write scope refuses effect; benign 503 after unknown ACK is reconciled with source receipts, never blindly repeated. Root fault belongs to external Environment vs Product/Agent as actually evidenced, not automatic blame.

**J3 Long-lived multi-Agent evolving spec:** new feature must preserve old applicable safety contract and current ABI; two separate file writers can conflict on logical Contract despite disjoint file paths. Old Reviewer PASS and stale retrieved memory cannot qualify new SHA.

**J4 Experiment and TraceML:** development-held-out split + reproducible source/state/time basis; a candidate appearing better due to hidden oracle leak or double-counted Pivot fails. Valid opportunity denominator and negative cases preserve uncertainty.

**J5 Task-meta→GitHub→Tally→GitHub:** task-meta emits bounded factual source report; Tally C GitHub reads native summary (no manifest dereference), decides optionally, K/Host executes with legal authority, Tally publishes safe feedback. Duplicate report/correction/partial pages and wrong verifier do not falsely promote Candidate. Real E2E #1210/#1231 separately NOT_RUN, source-only Golden cannot substitute.

## 5. Product/L1 exit conditions (no premature Freeze)
1. Independent source Review of exact L1/PRD blobs and effective provisional base: [#1300](https://github.com/kaicreator-mm/ai-development-standard/issues/1300) P0/P1/P2; no self-review and no separate shared GitHub login identity assumption.
2. For **each** C01–C12, exact source owner+blob and negative/positive evidence; classify ALREADY_NORMATIVE, DOGFOOD_GAP, TRUE_BOUNDED_SPEC_GAP or UNKNOWN_NEEDS_EVIDENCE. High-risk unknown => Product freeze not ready.
3. Explicit Product decisions whether C08/C10 require real normative semantics changes and whether C09/C12 can use current public Report v5 (do not invent v6 by default). C11 must remain a source-only conformance test.
4. On real final v4.16 Release Qualification, choose lawful exact predecessor; revalidate source-compatibility/parent-version selection. Version number alone/branch commit cannot qualify an adoption.
5. After independent Product Review and any repair, publish **explicit** accepted Product Freeze. Then L2 owning architecture/ref + independently reviewed Freeze, 3-phase native Task DAG and implementation concern write sets, not before.

**No downstream implementation release dependency:** task-meta v0.3 [#27](https://github.com/kaicreator-mm/task-meta/issues/27), future TS DomainHarness Tally [#63](https://github.com/kaicreator-mm/tally/issues/63) remain separate owners; their actual live integration is not an ADS source-only Release Gate.

**R0 truth:** Draft and L1 only. The terms `FREEZE_READY`, `REVIEW_PASS`, `TEST_PASS`, `RQ_PASS` are not asserted by this authored PRD.
