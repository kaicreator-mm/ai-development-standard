# V412-S03 — Read-only deterministic mapper / pair validator

> **CURRENT 2026-10-16 REBIND:** v4.11 standards baseline is now qualified/integrated `main@aac1e1206e4033601616c295e768e51fbc16efb1`; the dedicated `version/v4.12.0` checkpoint is `da5a5bf70a79ec76e0cf9cf7eecc5686dc39e6d5`. User-scoped Product R4 `e924fa29...`, L2 R6 `aede8804...`, Task DAG R4 writer-scope `421378b8...` now have sequential freeze checkpoints (Product `bb3e8baf`, L2 `6f9c13bc`, DAG `0d6c5823`; PR #1130). Earlier statements that the v4.11 predecessor is unqualified, or that R4/R6/DAG-R4 scope is only prospective, describe **earlier authorship history**; they do not govern the current task. This rebind **does not** constitute Pack Freeze, native Issue/Dependency materialization, accepted CAS Claim, implementation execution, or Release PASS. Validate current version HEAD again immediately before any real Task Claim.

> **TASK PACK PLANNING DRAFT (NOT FROZEN / NOT EXECUTABLE).** Read-only author preparation on the v4.12 planning branch. The *Task DAG* itself is exact-owner-frozen, but this Pack is not Task/Claim admission. No baseline release or source writer granted.

```ini
TASK_ID=V412-S03
CANONICAL_TYPE=type:task
ONE_CONCERN=REFERENCE_PAIR_CHECKER
PRODUCT_R3_BLOB=0bfbf782c8859e79df52c9b57904ad80bcd718e9
L2_R5_BLOB=68608ef6456334d627db1797ba2e023233c84ce7
FROZEN_DAG_BLOB=adc9e522f3b734a59898091945b9c7545530565a
PRODUCT_R4_SCOPED_BLOB=e924fa29d8fe3c846eeb7f6ca41131609b19b0ad
L2_R6_SCOPED_BLOB=aede88044697ba45f712ecfa49f615ce48e8af58
DAG_R4_SCOPED_BLOB=421378b8329f51c46697485f57fc9920cfaefed6
PRODUCT_R4_FREEZE_COMMIT=bb3e8bafe459c9fb735b390894a9df24c3d155d0
L2_R6_FREEZE_COMMIT=6f9c13bc607ac098a2a35493cba57dc6e9e1b6b3
DAG_R4_FREEZE_COMMIT=0d6c58230e180cd2fbadbe18d3b12c9d651c0447
V411_QUALIFIED_MAIN_SHA=aac1e1206e4033601616c295e768e51fbc16efb1
V412_INITIAL_SCOPED_INTEGRATION_SHA=da5a5bf70a79ec76e0cf9cf7eecc5686dc39e6d5
DAG_FREEZE_CHECKPOINT=7949caf630edbe83d1dff1ffb7cee8906b77c56f
DAG_FREEZE_RECORD_BLOB=f0a998a73c9319564b239026220ee44934778153
TARGET_VERSION=4.12.0
REAL_V411_RELEASE_PREDECESSOR=QUALIFIED_MAIN_aac1e1206e4033601616c295e768e51fbc16efb1
REAL_V412_IMPL_BASELINE=version/v4.12.0@da5a5bf70a79ec76e0cf9cf7eecc5686dc39e6d5
PACK_STATUS=REBIND_CANDIDATE_REVIEW_PENDING_NOT_FROZEN
NATIVE_TASK_ISSUE=NOT_MATERIALIZED
NATIVE_DEPENDENCIES=NOT_MATERIALIZED
READY=NO
ACCEPTED_CAS_CLAIM=NONE
TASK_PR_SOURCE=NOT_CREATED
TASK_VALIDATION=NOT_RUN
TASK_REVIEW=NOT_RUN
TASK_MERGE=NOT_DONE
FROZEN_DAG_PREDECESSORS=V412-S01;V412-S02
REVIEW_POLICY=required
RISK=high
L3_REQUIRED=YES
ALLOWED_CHANGES=ONLY_EXACT_PATHS_AND_SCOPES_BELOW_ON_LAWFUL_IMPLEMENTATION_BASELINE
FORBIDDEN_CHANGES=ALL_OTHERS_INCLUDING_FROZEN_PRD_L2_DAG_CLAIM_RELEASE
```

## 1. Goal / source evidence reuse

Ship a small side-effect-free reference checker producing deterministic Task→Anchor/Anchor→Task projections and exact scope/currentness proof with one clean-slate plus one pinned mature consumer fixture. ADS ships the checker and tests, NOT these consumer applications.

**Inspect first, build only missing delta.** Read qualified predecessor *exact* relevant normative owner/git blobs and tests and compare to Frozen R3/L2 before implementation. Reuse source-true contracts; no second claim service, graph scheduler, review/gate controller, app generator, or mandatory redundant verification.

## 2. Allowed and forbidden source changes

- **Allowed after legal admission:** New `scripts/v412_scaffold_dag_check.py` (or an existing proven equivalent after source-first analysis)
- **Allowed after legal admission:** New `scripts/test_v412_scaffold_dag_check.py` with focused positive/negative cases
- **Allowed after legal admission:** Uniquely named source-pinned `references/v4.12/fixtures/v412_consumer_new_*` and `v412_consumer_mature_*` **only where source material is genuinely missing**

**Forbidden by default:** all files not specifically assigned above; frozen Product/L2/DAG and research frozen source; shared canonical metadata/manifest/CI unless specifically owned above; other Task writer paths; release/tag/Claim manipulation; external network/secrets/irreversible side effects without separate current authority. Reconcile exact glob and section write sets against the *qualified* version integration tree before Task READY/Claim.

## 3. Tests → Contract → Implementation → Failure Handling → Reference

**Focused executable or source-verifiable acceptance oracles** (a planned oracle is not an executed PASS):

- P01 same exact frozen inputs yield byte-identical canonical forward/reverse generated outputs and provenance
- P02 new and mature Git snapshot each show exactly resolved material scope, single writers, structural integration and current DF/MI
- N01 odd/tab/newline paths, renames, symlinks/gitlinks, added and removed files cannot escape full tracked-object NUL-safe scan
- N02 unknown source, lock, CI, anchor or scope-manifest change after accepted SF invalidates source view; DAG-doc-only exempt change STILL changes DF/MI
- N03 malicious exact-path allowlist pre-exempts ABI/source without Frozen L2/source owner eligibility → reject
- N04 forged generated view, stale derived output, self-referential Freeze record or unchanged bytes with new Task binding → reject/hold
- N05 missing accepted CAS Claim, real native Review or E3 has `NOT_RUN`/`UNKNOWN`, never local E1 PASS

**Contract.** Inputs: exact accepted SF and successor revision Git object IDs; Frozen Product/L2 object pins; versioned accepted SF material scope including safe exact path-role approvals; one canonical DAG/Task-side binding object; optional real Issue IDs. Outputs: canonical read-only forward/reverse map, MV (synthetic digest distinct from actual Git subtree), DF/MI freshness, derived-view recheck, per-predicate evidence `PASS/FAIL/NOT_RUN/UNKNOWN` without minting gate authority.

**Implementation strategy.** Reuse bounded logic from frozen L2 prototype as inspiration; copy only needed logic after source/license/source-shape verification, make production path scanning Git `-z` byte-safe. Never edit the *frozen* `v412_l2_git_pair_probe.py`, prior standards, shared manifest or CI; S05 registers only after own focused checker works.

**Failure handling.** Missing git executable, unsupported bytes or untrusted refs must terminate nonzero/UNKNOWN with deterministic no-write report. Never authenticate or mutate GitHub/claims and never contact cloud services.

**Candidate focused command:** `python -B scripts/test_v412_scaffold_dag_check.py`; capture actual exact-head evidence later, never invent an execution log.

**References (immutable planning owner input):** frozen Product R3 blob `0bfbf782c8859e79df52c9b57904ad80bcd718e9`; frozen L2 R5 blob `68608ef6456334d627db1797ba2e023233c84ce7`; frozen DAG blob `adc9e522f3b734a59898091945b9c7545530565a`; checkpoint `7949caf630edbe83d1dff1ffb7cee8906b77c56f`; canonical `standards/DEVELOPMENT_WORKFLOW.md` §Stage2.4/2.5/2.6, `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` §10/§12.1, `GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `TASK_DAG_GOVERNANCE_STANDARD.md`, `VALIDATION_STANDARD.md`, `RELEASE_STANDARD.md`. Those are verified historical version owners, **not** an assertion that the current v4.11 branch released.

## 4. Execution readiness / Review / closure

- Intended concern predecessor(s): V412-S01, V412-S02. Native issue edges require actual API mutation and readback; Markdown is advisory historical.
- Risk: **high**. Stage 2.6 pre-dispatch Review Policy candidate: **required**, subject to stronger authority. A Builder cannot self-prove `review:required`.
- Source implementation base: v4.11 is qualified and version/v4.12.0 exists. **TASK still HOLD** until this Pack's exact source/index is frozen, canonical native Task/dependencies are read back, and a valid current accepted CAS Claim precedes the first normative source write. Do not implement on historic-main planning PR #1101.
- Author/responsible executor shall acquire a current accepted CAS Claim for the *real native Task Issue* before any implementation-source write; a GitHub comment/status alone is insufficient.
- Verification must report exact subject/commit/tree, real command/exit/skip, provenance and strength E1/E2/E3. Only the owning gate/Release actor may promote a result; PR-local PASS ≠ version Release PASS.
- Closeout when authorized source PR is merged on current version integration branch after required Review/validation and canonical readback; otherwise state BLOCKED/NOT_RUN with minimal owning remedy, no duplicate Task Issue/hidden test program.

```ini
TASK_IMPLEMENTATION=NOT_STARTED
TASK_REVIEW=NOT_RUN
TASK_CLAIM=NONE
PACK_FREEZE=NOT_RECORDED
REAL_INTEGRATION_BASE=VERSION_BRANCH_AT_da5a5bf70a79ec76e0cf9cf7eecc5686dc39e6d5
```
