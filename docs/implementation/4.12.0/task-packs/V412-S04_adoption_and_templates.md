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
