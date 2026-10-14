# V411-V01 — exact-current source-bound evidence index (BLOCKED)

> **Secondary durable index of already executed local Host evidence**, not newly executed by the WEB author. All raw logs are located at the real Host path recorded in #1021@6156596087 and remain outside GitHub. This file does not assert independent re-execution of those logs.

```ini
CANDIDATE_SHA=322e86845f78de8ea8cadb05ec624bfbb3a5de20
TESTED_SHA=322e86845f78de8ea8cadb05ec624bfbb3a5de20
TESTED_TREE=b793e5b1f65fa5309b7cf9dab8cb5d0168d74abd
EVIDENCE_ONLY_HEAD=SEPARATE_FROM_TESTED_SHA_RESOLVE_PR_HEAD
RUNNER_BLOB=e66eaee20b452f570665bff3e83be493a9eaef6b
REGISTRY_BLOB=e766550551fba48d181a92d9e8d5e8541c9fc046
WORKTREE=HOST_RECORDED_FRESH_CLEAN_t1021-v01freshval
HOST_RECORDED_OS=Windows_10.0.26300_x64_MINGW64
HOST_PYTHON=3.14.7
HOST_GIT=2.55.0.windows.5
HOST_RECEIPT=#1021@6156596087
DISTINCT_REVIEWED_VALIDATION_RECEIPT=#1021@6162591281
FILE_AUTHOR_EXECUTION=NONE
V01=BLOCKED
```

## 1. Whole-current candidate commands and actual outcomes

Distinct local `CLOSURE_VALIDATOR` #1021@6156596087 ran `python -B scripts/verify_standard.py` and all 139 tracked `scripts/test_*.py` **individually** in a clean detached exact-SHA workspace using a timeout wrapper; raw exit statuses collected without masking pipelines.

| Owner evidence | Executed output |
| --- | --- |
| `python -B scripts/verify_standard.py` | EXIT=0, manifest 309, bootstrap-required 41 |
| 139 individual `python -B scripts/test_*.py` | **125 EXIT=0, 14 EXIT=1** (139/139 invoked, not 139 PASS) |
| `scripts/test_v411_t12_abc_conformance.py` included in census | EXIT=0, `records=52 failure_count=0`, 20 test-only PASS, 28 material REQUIRED_NOW BLOCKED, 4 real future NOT_RUN |
| Same 14 scripts at clean parent `dc997f86` | 14 EXIT=1, same failure shapes; current RC-3 merged changes in runner did **not introduce** a new failure among these 14 |
| T09 real human gate in later focused #1021@6162459405 | EXIT=1, `BLOCKED_NO_OPERATOR_AUTHORITY_FILE`, `REAL_HOST_EVIDENCE` lines=0 — proves fail-closed only, not human positive |
| T09 same-object A→B real-human script | **NOT_RUN**, missing human-created file and helper absent on Host |
| Current registered CI run #38460978520 | SUCCESS for 37 configured commands, **zero T12**, not equivalent to full visible regression |

Actual per-command log files in `C:\\xDev\\kAiCreator\\_evidence-private\\ai1021-v411-v01-fresh-closure\\logs\\test_*.log`, `environment.txt`, `regression_results.tsv` (140 lines incl. verify command), `basecheck_results.tsv` (14 comparison exits), `run_regression.sh` — path/metadata **reported by Host**, not fetched or independently read by this evidence compiler. Separate later focused absence receipt in #1021@6162459405 retains its own executor/worktree/log directory.

## 2. The 14 literal red scripts

Each raw `EXIT=1` is retained; replacement scope is an **owner/Validator decision**, not a script result mutation:

```text
scripts/test_v411_central_wiring.py             # 22 tests, 2 fails
scripts/test_v49_integrated_dogfood.py          # 32 tests, 3 fails
scripts/test_v410_owner_convergence.py
scripts/test_v410_t02b_machine_projection.py
scripts/test_v410_t05a_shared_code_safety.py
scripts/test_v410_t07a_acceptance_projection.py
scripts/test_v410_t07b_decision_record.py
scripts/test_v410_t08a_integration_runner.py
scripts/test_v411_merge_admission.py
scripts/test_v411_task_learning.py
scripts/test_v411_t06_claim_admission.py
scripts/test_v411_t08_human_denial_authority.py  # real human case skipped w/o env
scripts/test_v411_t09_effect_boundary.py         # real human case skipped w/o env
scripts/test_v411_t13_role_conduct.py
```

Attribution approved on original #1021@6150684306 and current extension #1021@6160156287: v4.10-era registry/owner pins, per-task frozen authoring-head writesets, T06 whole-document §30 contradiction from legal later source and v4.9 exact shared identity snapshots. Current replacement invariants belong to `verify_standard`, current owner methods / registry tests and T12 exact-runner; if a current semantic false negative is found, route to one Builder repair, not blanket exclusion. Latest distinct Validator #1021@6162591281 accepts this scoped current-fidelity substitution and preserves raw failures.

## 3. Selected machine assurance proof vs material scope boundaries

- **A Claim/review:** T05 same-exact-subject opposite admitted in-process Reviewer events yield BLOCKED both orders; T06 protected Claim atomics/WEB→LOCAL, T13 role traces. Real PR #1097 and #1086 native GitHub Reviews = **zero** at checked time — not legitimate native Review witness, exact exclusion explicitly recorded.
- **B trust/risk:** `test_v411_t01_effective_rules.py` owner EXIT=0 (A0/A4 nonweakening) + `test_v411_t10_untrusted_inputs.py` EXIT=0; GitHub / MCP / A2A message channel negative fixtures exercised **in process**, no remotely deployed adapter claimed.
- **C effect/recovery:** T09 all local persistent SQLite effect/snapshot/ACK-loss/compensation predicates PASS except documented historical write-set assertion. Human operator DENY one real source proof remains missing, same SQLite object A→B with human source NOT_RUN.
- **D upstream:** observed real current OpenSpec and Spec Kit pinned inspected source/LICENSE/NOTICE-root and Spec Kit doc drift; neither practice is direct runtime dependency nor copied protected source in this version; no real H3 permission certified.
- **Four-way J09+J10+J11+J12:** T12 obligation-union omission negatives PASS; *no* same-real-work-subject four-job positive. `MATERIAL_INTERSECTION_UNKNOWN`, supported Product impact unresolved under old Frozen scope. [Draft prospective change PR #1102](https://github.com/kaicreator-mm/ai-development-standard/pull/1102) is proposal, **not** authority.
- **S08 actual human:** focused source test requires `V411_T09_REAL_HOST=1` plus `V411_T09_HUMAN_AUTHORITY_FILE` to a genuinely independent operator-created outside-repo authority record. Latest local record confirms **none saved**, including one unsaved stale/wrong-scope human scratch not accepted. No AI may create a human credential.

## 4. Evidence chain validation boundaries

- `test_v411_t12_abc_conformance.py` includes all 52 selected current reference assertion records and stage-appropriate negative tests; `52/52` is an owner assertion count, **not** 52 real material release Gate PASS results.
- Historical initial V01 `eb8ffb8b` was 139 scripts /126 PASS/13 FAIL, **not** this current successor's 125/14.
- Current independent Kimi Validator #1021@6162591281 independently re-read clean candidate/current ref/receipts/CI, issued **V01=BLOCKED**; did not modify candidate source, re-run 139, or create human evidence.
- GitHub source compilation of this file cannot view ephemeral Host log bytes; independent Fresh Reviewer should request original receipt/log-digest checks where required. New prospective Product scope PR and this evidence-only PR are distinct; neither has changed live version candidate HEAD.
- Later V03 Hidden, V04 Fresh, R01 RQ, R02 integration remain **NOT_RUN** and cannot be imported to V01 from Task/PR CI.

**Document author disposition:** records source/issue facts only, **no fresh PASS assertion**.
