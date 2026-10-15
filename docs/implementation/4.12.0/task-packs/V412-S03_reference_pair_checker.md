# V412-S03 — Read-only deterministic mapper / pair validator

> **TASK PACK PLANNING DRAFT (NOT FROZEN / NOT EXECUTABLE).** Read-only author preparation on the v4.12 planning branch. The *Task DAG* itself is exact-owner-frozen, but this Pack is not Task/Claim admission. No baseline release or source writer granted.

```ini
TASK_ID=V412-S03
CANONICAL_TYPE=type:task
ONE_CONCERN=REFERENCE_PAIR_CHECKER
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
