# V412-S02 — One binding authority and cycle-free SF↔DF planning Freeze

> **CURRENT 2026-10-16 REBIND:** v4.11 standards baseline is now qualified/integrated `main@aac1e1206e4033601616c295e768e51fbc16efb1`; the dedicated `version/v4.12.0` checkpoint is `da5a5bf70a79ec76e0cf9cf7eecc5686dc39e6d5`. User-scoped Product R4 `e924fa29...`, L2 R6 `aede8804...`, Task DAG R4 writer-scope `421378b8...` now have sequential freeze checkpoints (Product `bb3e8baf`, L2 `6f9c13bc`, DAG `0d6c5823`; PR #1130). Earlier statements that the v4.11 predecessor is unqualified, or that R4/R6/DAG-R4 scope is only prospective, describe **earlier authorship history**; they do not govern the current task. This rebind **does not** constitute Pack Freeze, native Issue/Dependency materialization, accepted CAS Claim, implementation execution, or Release PASS. Validate current version HEAD again immediately before any real Task Claim.

> **TASK PACK PLANNING DRAFT (NOT FROZEN / NOT EXECUTABLE).** Read-only author preparation on the v4.12 planning branch. The *Task DAG* itself is exact-owner-frozen, but this Pack is not Task/Claim admission. No baseline release or source writer granted.

```ini
TASK_ID=V412-S02
CANONICAL_TYPE=type:task
ONE_CONCERN=SCAFFOLD_TASK_BINDING_PAIR
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
FROZEN_DAG_PREDECESSORS=NONE
REVIEW_POLICY=required
RISK=high
L3_REQUIRED=YES
ALLOWED_CHANGES=ONLY_EXACT_PATHS_AND_SCOPES_BELOW_ON_LAWFUL_IMPLEMENTATION_BASELINE
FORBIDDEN_CHANGES=ALL_OTHERS_INCLUDING_FROZEN_PRD_L2_DAG_CLAIM_RELEASE
```

## 1. Goal / source evidence reuse

Define one effective Task-side Scaffold anchor binding; preserve frozen planning Task DAG as historical and GitHub native Issue dependencies as live after materialization; fail closed on material SF/DF drift with separately recomputed outputs.

**Inspect first, build only missing delta.** Read qualified predecessor *exact* relevant normative owner/git blobs and tests and compare to Frozen R3/L2 before implementation. Reuse source-true contracts; no second claim service, graph scheduler, review/gate controller, app generator, or mandatory redundant verification.

## 2. Allowed and forbidden source changes

- **Allowed after legal admission:** `standards/TASK_DAG_GOVERNANCE_STANDARD.md`: narrowly add authoritative structural-anchor/Task-binding and scoped pair-currentness rule
- **Allowed after legal admission:** `templates/task-dag.md`: single-source binding and Freeze demonstration only when current template lacks the contract
- **Allowed after legal admission:** New unique `scripts/test_v412_pair_contract.py` (only if bounded contract regression is necessary)

**Forbidden by default:** all files not specifically assigned above; frozen Product/L2/DAG and research frozen source; shared canonical metadata/manifest/CI unless specifically owned above; other Task writer paths; release/tag/Claim manipulation; external network/secrets/irreversible side effects without separate current authority. Reconcile exact glob and section write sets against the *qualified* version integration tree before Task READY/Claim.

## 3. Tests → Contract → Implementation → Failure Handling → Reference

**Focused executable or source-verifiable acceptance oracles** (a planned oracle is not an executed PASS):

- P01 one source anchor with structural `{anchor_id,kind,location,contract_ref}` and one current writer in Task-side binding yields consistent forward and reverse views
- P02 DF-only approved exact-path change reuses unchanged SF material source view but forces current DF/MI mapping recheck
- N01 duplicate active writer, dangling important anchor, SPLIT without `dag-mutation-record-v1` binding refresh → HOLD
- N02 L2 public/trust ABI mismatch rejected even when SF and DF agree
- N03 unknown added/deleted/renamed source, lock, CI, manifest, symlink/gitlink or anchor change is material by default
- N04 preaccepted writer-chosen source exemption and forged generated index are independently rejected; no self-hash
- N05 scaffold structure/stub never becomes feature user-path/release PASS

**Contract.** Immutable pair has accepted SF commit+versioned exact material-view object inventory and source-owner-approved exemption paths, DF exact blob and distinct MI digest, Frozen Product/L2 pins, generated output independently recomputed. Exemption for DAG_ONLY_INPUT never waives DF/MI, DERIVED_NONAUTHORITATIVE never waives regeneration, Freeze record never waives owner action.

**Implementation strategy.** Append minimal normative clauses to existing Task DAG Governance and example projection to task-dag template. Do not mint a second writable anchor `owner`/status or new graph backend; frozen research script `references/v4.12/fixtures/v412_l2_git_pair_probe.py` is READ ONLY.

**Failure handling.** Missing current actual Git object, unclassifiable exemption, inconsistent structural/semantic source, outdated native SPLIT ownership → `MATERIAL/HOLD`; source owner supersedes/rebaselines through existing governance, not self-acceptance.



**References (immutable planning owner input):** frozen Product R3 blob `0bfbf782c8859e79df52c9b57904ad80bcd718e9`; frozen L2 R5 blob `68608ef6456334d627db1797ba2e023233c84ce7`; frozen DAG blob `adc9e522f3b734a59898091945b9c7545530565a`; checkpoint `7949caf630edbe83d1dff1ffb7cee8906b77c56f`; canonical `standards/DEVELOPMENT_WORKFLOW.md` §Stage2.4/2.5/2.6, `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` §10/§12.1, `GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `TASK_DAG_GOVERNANCE_STANDARD.md`, `VALIDATION_STANDARD.md`, `RELEASE_STANDARD.md`. Those are verified historical version owners, **not** an assertion that the current v4.11 branch released.

## 4. Execution readiness / Review / closure

- Intended concern predecessor(s): none (but absent dependency ≠ READY). Native issue edges require actual API mutation and readback; Markdown is advisory historical.
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
