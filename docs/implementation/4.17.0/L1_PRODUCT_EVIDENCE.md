# ADS v4.17.0 — L1 Product Evidence R0

**Candidate:** PLANNING_ONLY / L1_R0_SOURCE_READ / NOT_INDEPENDENTLY_REVIEWED / NOT_FROZEN.
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

| C | Priority | Candidate disposition at R0 | Proposed smallest output |
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

**R0 classifications are hypotheses**, not final admissions, blockers or approvals. A later review must give exact text and one conformance positive/negative per Concern; only confirmed `TRUE_BOUNDED_SPEC_GAP` becomes a normative Task candidate.

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

**Status at authoring:** SOURCE_READ, PRD_R0_CANDIDATE, VALIDATION_NOT_RUN, REVIEW_NOT_RUN, PRODUCT_FREEZE_NO, V417_IMPLEMENTATION_NOT_RUN.
