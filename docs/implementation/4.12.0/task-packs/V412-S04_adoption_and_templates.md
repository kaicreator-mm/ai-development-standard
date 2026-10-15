# V412-S04 — Compact adoption guide and golden reusable templates

> **TASK PACK PLANNING DRAFT (NOT FROZEN / NOT EXECUTABLE).** Read-only author preparation on the v4.12 planning branch. The *Task DAG* itself is exact-owner-frozen, but this Pack is not Task/Claim admission. No baseline release or source writer granted.

```ini
TASK_ID=V412-S04
CANONICAL_TYPE=type:task
ONE_CONCERN=ADOPTION_AND_TEMPLATES
PRODUCT_R3_BLOB=0bfbf782c8859e79df52c9b57904ad80bcd718e9
L2_R5_BLOB=68608ef6456334d627db1797ba2e023233c84ce7
FROZEN_DAG_BLOB=adc9e522f3b734a59898091945b9c7545530565a
DAG_FREEZE_CHECKPOINT=7949caf630edbe83d1dff1ffb7cee8906b77c56f
DAG_FREEZE_RECORD_BLOB=f0a998a73c9319564b239026220ee44934778153
TARGET_VERSION=4.12.0
REAL_V411_RELEASE_PREDECESSOR=NOT_YET_QUALIFIED
REAL_V412_IMPL_BASELINE=NOT_YET_PINNED
PACK_STATUS=AUTHOR_PREPARED_NOT_REVIEWED_OR_FROZEN
NATIVE_TASK_ISSUE=NOT_MATERIALIZED
NATIVE_DEPENDENCIES=NOT_MATERIALIZED
READY=NO
ACCEPTED_CAS_CLAIM=NONE
TASK_PR_SOURCE=NOT_CREATED
TASK_VALIDATION=NOT_RUN
TASK_REVIEW=NOT_RUN
TASK_MERGE=NOT_DONE
FROZEN_DAG_PREDECESSORS=NONE
REVIEW_POLICY=recommended
RISK=medium
L3_REQUIRED=NO
ALLOWED_CHANGES=ONLY_EXACT_PATHS_AND_SCOPES_BELOW_ON_LAWFUL_IMPLEMENTATION_BASELINE
FORBIDDEN_CHANGES=ALL_OTHERS_INCLUDING_FROZEN_PRD_L2_DAG_CLAIM_RELEASE
```

## 1. Goal / source evidence reuse

A new or mature project can adopt the qualified immutable ADS standard using one clear entrypoint without gratuitous Scaffold/DAG generation, unnecessary reviewer loops or a second Task/Release authority.

**Inspect first, build only missing delta.** Read qualified predecessor *exact* relevant normative owner/git blobs and tests and compare to Frozen R3/L2 before implementation. Reuse source-true contracts; no second claim service, graph scheduler, review/gate controller, app generator, or mandatory redundant verification.

## 2. Allowed and forbidden source changes

- **Allowed after legal admission:** `standards/PROJECT_ADOPTION.md`: additive v4.12 adoption, immutable pin, manual A0/A1 vs actual machine A2+ only
- **Allowed after legal admission:** Only uniquely assigned `templates/`/`checklists/` where source-first gap exists; never `templates/task-dag.md`, `templates/GOLDEN_INDEX.md` or shared verifier
- **Allowed after legal admission:** Promote/adapt existing `references/v4.12/V412_PROJECT_ADOPTION_GUIDE_CANDIDATE_R0.md` prose when legally qualified; do not duplicate canonical owners

**Forbidden by default:** all files not specifically assigned above; frozen Product/L2/DAG and research frozen source; shared canonical metadata/manifest/CI unless specifically owned above; other Task writer paths; release/tag/Claim manipulation; external network/secrets/irreversible side effects without separate current authority. Reconcile exact glob and section write sets against the *qualified* version integration tree before Task READY/Claim.

## 3. Tests → Contract → Implementation → Failure Handling → Reference

**Focused executable or source-verifiable acceptance oracles** (a planned oracle is not an executed PASS):

- P01 new project uses v4.12 after explicit adopting-project pin and source/Claim ownership, not before
- P02 mature project reuses checked-in code/contracts/fixtures with bounded source changes and no empty DAG requirement
- P03 A0/A1 WEB/manual evidence has same Gate/trust/currentness floor as A2+, while A2+ machines attach actual executed script proof
- N01 unqualified v4.12 candidate silently used as immutable released pin or older frozen project retro-migrated → reject
- N02 missing/UNKNOWN/NOT_RUN proof mapped to PASS or `NOT_APPLICABLE` without reason → reject
- N03 builder self-review, changing exact allowlist after acceptance or docs-only claim of E3/Release → reject

**Contract.** Adoption never modifies original source-owner Gate enum, Claim CAS or Task DAG dependencies; project-specific immutable `.dev-standard/VERSION` is actual adoption record; FAST/STANDARD/EXPLORATORY/HIGH_ASSURANCE and INLINE/BOUNDED_WORKLIST/EXPLICIT_DAG are proportional planning modes, not new required interfaces.

**Implementation strategy.** Prefer short links to existing v4.11 authoritative standards and Golden examples. Only add v4.12 deltas missing from source; use one-concern patch with targeted doc/golden tests. Offer meaningful Task Learning facts without inventing metrics.

**Failure handling.** Missing version tag/qualified source or project owner adoption → SHADOW-only/non-normative guidance; no change to the project's current pinned permissions.



**References (immutable planning owner input):** frozen Product R3 blob `0bfbf782c8859e79df52c9b57904ad80bcd718e9`; frozen L2 R5 blob `68608ef6456334d627db1797ba2e023233c84ce7`; frozen DAG blob `adc9e522f3b734a59898091945b9c7545530565a`; checkpoint `7949caf630edbe83d1dff1ffb7cee8906b77c56f`; canonical `standards/DEVELOPMENT_WORKFLOW.md` §Stage2.4/2.5/2.6, `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` §10/§12.1, `GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `TASK_DAG_GOVERNANCE_STANDARD.md`, `VALIDATION_STANDARD.md`, `RELEASE_STANDARD.md`. Those are verified historical version owners, **not** an assertion that the current v4.11 branch released.

## 3A. #1099 Project Adoption Fast Path — real net value rather than ceremony count

S04 is the **project-facing adoption** owner for the already frozen cross-cutting principle. Reconcile with current `standards/PROJECT_ADOPTION.md` (existing A0–A4 and Fast Path) and reuse `TASK_DECOMPOSITION_STANDARD` (atomic concern) rather than duplicating another ROI standard. The minimum additional project guidance is:

- **Scope first:** distinguish `CORE_MANDATORY | CONDITIONAL_MATERIAL | NONCORE_OPTIONAL | UNKNOWN` as source-grounded *descriptions*, not GitHub labels/Gate enums. Inspect actual user outcome, contract/security/side-effect/consumer reach and aggregated small-risk impact; a “docs-only / small fix / Fast” filename is not self-proof of optionality.
- **Qualitative value/cost decision:** for truly optional scope compare net expected outcome against **implementation + Review + Host/CI + waiting + maintenance + opportunity cost** and alternative reuse/simplification. Say `FAR_EXCEEDS | JUSTIFIED | MARGINAL | NEGATIVE | UNKNOWN` only as supported, non-numeric judgment—no fake savings percentages, centralized telemetry requirement or mandatory decision-card form.
- **Legal stop/defer:** `DO_MINIMAL`, `REUSE_EXISTING`, `BATCH`, `DEFER_WITH_TRIGGER`, `EXCLUDE_WITH_REASON` are allowable *planning advice* when the original owning authority permits; for any material exclusion note who decided, what user promise/test is no longer covered, remaining risk and revisit trigger. An already Frozen Product/mandatory gate cannot be waived by a Task-level ROI note; require proper prospective owner migration.
- **Right-sized people and evidence:** many simple A0/WEB Tasks need no human review beyond the applicable current owner rules; where reserved real-human authority or independently human-authored Gold is genuinely material, minimal real authorized action is non-substitutable. LLM/tool analysis can prepare the short decision evidence and detect negatives; public self-reports are not independent empirical observation or real approval. Do not mandate three LLMs or record forged human consensus.
- **Existing vs new project:** mature projects reuse source/fixtures without generating a new full Scaffold; new projects may use bounded Scaffold only after *qualified adoption and accepted source Claim*. A0/A1 and A2+ share the same currentness/security/Review/Release floor even when evidence collection differs.

**Golden adoption examples (within already owned S04 files, no separate issue):** (A) optional peripheral project feature excluded before Product Freeze with explicit non-user-impact and original Owner; (B) deceptively rare severe auth/human DENY case retained; (C) already Frozen mandatory scenario proposed for deferral and refused pending lawful amendment; (D) duplicate Task/Review proposals merged into one coherent concern with real dependency truth; (E) prior public research reused with sample/region/rights limits and no fake representative human study.

**Acceptance negatives:** a low-cost `A0` path never downgrades a required gate; a self-declared `LOW_ROI` cannot turn `NOT_RUN` into `NOT_APPLICABLE`; Task utility extraction is optional unless actual cross-code semantics/maintenance benefit supports it. If current v4.11 adoption owner already supplies a specific clause, classify it `ALREADY_SATISFIED` and link rather than rewrite.

## 3B. #1123 prospective adopter protocol migration — existing S04 owner

The user's #1123 change intake is accepted **for v4.12 successor planning**, but its Product R4/L2 R6/DAG R4 specific sources are not yet Frozen. This S04 documentation task adds no new writer surface: `standards/PROJECT_ADOPTION.md` and S04-owned examples remain its *only* normative prospective target, after lawful Claim.

**Bounded adoption acceptance:**
- Same account can transport events from several **self-declared** distinct Agents; GitHub `user.login` is not actor role or reviewer-identity eligibility.
- New v4.12 behavior cannot silently replace consumer pins on v4.11/v4.10: `operator_id/session_ref` trust semantics, owner-identity credential behavior and required technical admission are compatibility dimensions, even with unchanged `agent-event-v2` JSON fields. Select the actually supported prospective protocol/adoption migration; don't infer semantic backward compatibility from syntactically valid schema.
- The distinct future [#1119](https://github.com/kaicreator-mm/ai-development-standard/issues/1119) **rolling compatible latest** updater is not implemented in S04. No proactive changes to other repositories or unqualified release pins.
- Retain consumer-side real security credentials, actual GitHub branch rulesets, human participant consent, performed effect / negative case validation where the external product actually requires them. A declared `human` executor does not claim that an off-repo participant consent event occurred.

**Focused counterexamples:** incompatible legacy consumer pin must remain authoritative (NOT auto-adopt); “new protocol but same schema” cannot be declared compatible without behavioral basis; two reviewers via one GitHub transport are not auto-collapsed; absence of actual required user-permission/consent/effect proof remains NOT_RUN. No new Task/Gold/Study required for the ADS standards artifact.

**Current status:** Product scope intake approved, detailed delta candidates not frozen, S04 `review:recommended` remains unchanged; no source PR or implemented migration is claimed.

## 4. Execution readiness / Review / closure

- Intended concern predecessor(s): none (but absent dependency ≠ READY). Native issue edges require actual API mutation and readback; Markdown is advisory historical.
- Risk: **medium**. Stage 2.6 pre-dispatch Review Policy candidate: **recommended**, subject to stronger authority. A Builder cannot self-prove `review:required`.
- Source implementation base: **HOLD** until actual v4.11 Release-qualified predecessor integrated or legally adopted into a v4.12 version branch. Never write normative source under the historic-main planning PR.
- Author/responsible executor shall acquire a current accepted CAS Claim for the *real native Task Issue* before any implementation-source write; a GitHub comment/status alone is insufficient.
- Verification must report exact subject/commit/tree, real command/exit/skip, provenance and strength E1/E2/E3. Only the owning gate/Release actor may promote a result; PR-local PASS ≠ version Release PASS.
- Closeout when authorized source PR is merged on current version integration branch after required Review/validation and canonical readback; otherwise state BLOCKED/NOT_RUN with minimal owning remedy, no duplicate Task Issue/hidden test program.

```ini
TASK_IMPLEMENTATION=NOT_STARTED
TASK_REVIEW=NOT_RUN
TASK_CLAIM=NONE
PACK_FREEZE=NOT_RECORDED
REAL_INTEGRATION_BASE=NOT_VERIFIED
```
