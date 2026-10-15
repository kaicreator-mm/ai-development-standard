# V412-S01 — Phase-scoped planning Scaffold Claim authority

> **TASK PACK PLANNING DRAFT (NOT FROZEN / NOT EXECUTABLE).** Read-only author preparation on the v4.12 planning branch. The *Task DAG* itself is exact-owner-frozen, but this Pack is not Task/Claim admission. No baseline release or source writer granted.

```ini
TASK_ID=V412-S01
CANONICAL_TYPE=type:task
ONE_CONCERN=PHASE_CLAIM_AUTHORITY
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
REVIEW_POLICY=required
RISK=high
L3_REQUIRED=YES
ALLOWED_CHANGES=ONLY_EXACT_PATHS_AND_SCOPES_BELOW_ON_LAWFUL_IMPLEMENTATION_BASELINE
FORBIDDEN_CHANGES=ALL_OTHERS_INCLUDING_FROZEN_PRD_L2_DAG_CLAIM_RELEASE
```

## 1. Goal / source evidence reuse

A project that explicitly and lawfully adopts v4.12 can write its first bounded Scaffold source in Stage 2 after an accepted existing canonical `type:planning` Work Item/Claim and pre-dispatch Review Policy, without introducing any new Task/Gate/Claim owner; older pins remain unaffected.

**Inspect first, build only missing delta.** Read qualified predecessor *exact* relevant normative owner/git blobs and tests and compare to Frozen R3/L2 before implementation. Reuse source-true contracts; no second claim service, graph scheduler, review/gate controller, app generator, or mandatory redundant verification.

## 2. Allowed and forbidden source changes

- **Allowed after legal admission:** `standards/DEVELOPMENT_WORKFLOW.md`: bounded Stage 2→3 sequencing/phase-depth/Scaffold authorization only
- **Allowed after legal admission:** `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`: canonical `type:planning` pre-DF source writer metadata and CAS readback semantics where actually missing
- **Allowed after legal admission:** `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`: only bounded prospective pre-DF admission subsection, preserving `NO_CLAIM_NO_EXECUTION`
- **Allowed after legal admission:** New owner-local `scripts/test_v412_phase_admission.py` only if source-true executable predicates are missing

**Forbidden by default:** all files not specifically assigned above; frozen Product/L2/DAG and research frozen source; shared canonical metadata/manifest/CI unless specifically owned above; other Task writer paths; release/tag/Claim manipulation; external network/secrets/irreversible side effects without separate current authority. Reconcile exact glob and section write sets against the *qualified* version integration tree before Task READY/Claim.

## 3. Tests → Contract → Implementation → Failure Handling → Reference

**Focused executable or source-verifiable acceptance oracles** (a planned oracle is not an executed PASS):

- P01 existing version pins retain historical Stage 2→3 task authority and do not receive early source permission
- P02 current v4.12 adopting project with accepted `type:planning` source scope, Review Policy and CAS Claim can produce source-only Scaffold seams
- N01 missing, stale or competing accepted Claim blocks *first* source file, even on empty repo
- N02 public ABI/schema/security source cannot be declared accepted SF before required independent PR Review and authorized merge
- N03 package-manifest generation cannot authorize `postinstall`, network, credential, deployment or irreversible tool effects
- N04 unknown native CAS API or lost ACK remains `UNKNOWN/HOLD`, never client-side optimistic READY

**Contract.** Reuses one canonical Work Item, current native Issue state/Allowed/Forbidden paths and existing generation-bound CAS Start Record; output is a narrowly adopted stage-specific admission rule, NOT a new state enum, Task alias or human Bootstrap Gate. Product/L2 contract identity pins immutable.

**Implementation strategy.** Small prospective clauses under current three owner documents; cite normative owner rather than duplicate Task protocol. If schema/manifest/shared checker change is actually necessary, submit one bounded S05 proposal, do not edit their files.

**Failure handling.** Any owner conflict, unspecified stage transition, unauthorized tool effect, stale Product/L2 pin or unestablished native Claim → DENY/HOLD; report actual affected owner instead of granting source rights.



**References (immutable planning owner input):** frozen Product R3 blob `0bfbf782c8859e79df52c9b57904ad80bcd718e9`; frozen L2 R5 blob `68608ef6456334d627db1797ba2e023233c84ce7`; frozen DAG blob `adc9e522f3b734a59898091945b9c7545530565a`; checkpoint `7949caf630edbe83d1dff1ffb7cee8906b77c56f`; canonical `standards/DEVELOPMENT_WORKFLOW.md` §Stage2.4/2.5/2.6, `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` §10/§12.1, `GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `TASK_DAG_GOVERNANCE_STANDARD.md`, `VALIDATION_STANDARD.md`, `RELEASE_STANDARD.md`. Those are verified historical version owners, **not** an assertion that the current v4.11 branch released.

## 4. Execution readiness / Review / closure

- Intended concern predecessor(s): none (but absent dependency ≠ READY). Native issue edges require actual API mutation and readback; Markdown is advisory historical.
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
