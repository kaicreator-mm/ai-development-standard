# ADS #1366 R20 — Actual recorded unittest inventory vs declared source methods

**Purpose:** implement a reusable Python fail-closed audit of an **existing real R17 execution receipt**, grounded in prospective ADS v4.19 candidate `TESTING_STANDARD.md` §6.1 (Git blob `746ec1da78b45f2d2c1fa2177549acbcc6587ca2`, PR #1365 exact HEAD `dac263fa4c0ab155406d2f2117459b34322cc988`, still OPEN/unmerged). No new SMT models, no fake CI/Gate, and no unnecessary native or full suite reruns.

## Review before implementation

R17 already contains a genuine Windows and WSL2 exact-SHA 13/13 Python execution record at `c5eb69c3fcd47ca934b4b87c8004131add6ad5d2`, with immutable source method files and full named-method `unittest -v` logs. The historical receipt checked test **counts** but its machine format did not enumerate the exact required↔executed ID set. Under §6.1, this leaves a narrower question for evidence consumers: did the green result cover the 13 **specific methods** claimed, without missing, duplicate or extra IDs?

Rather than rerun tests or invent another synthetic solver, compare the original bytes and bind a reproducible Python auditor to their known Git blobs. Two files declare 7 + 6 = **13** test methods; both recorded environments individually executed **the same exact 13 IDs**, with no extras, skips, failures or duplicate executions.

## Implemented

- `formal/v4.19/coverage/executed_inventory_audit.py` — read-only stdlib Python AST + `unittest -v` log audit; pins **four original Git blobs** (2 exact test source files, combined log, receipt), original execution HEAD and combined log SHA256; verifies source test IDs, matching log IDs per environment, method-level OK outcomes, summary count, and machine receipt. A missing/edited source/log/receipt, missing test, duplicate method or wrong subject results in `BLOCK` exit 2. The pinned identities are fixed, **not user-overridable admission authority**.
- `formal/tests/test_executed_inventory_audit.py` — nine bounded Python regression cases with synthetic isolated fixtures, including green summary/omitted test, duplicate ID, failing method, source tampering, receipt subject mismatch, false file blob, log drift and wrong environment.
- `formal/v4.19/r20/R20_RECORDED_TEST_INVENTORY_READBACK.json` — the actually observed GitHub frozen source-method IDs and per-host executed ID lists; records what was checked, not a new execution of old tests.

## What actually ran and how results are qualified

- **Real historical GitHub code/log/receipt crosscheck:** 20/20 in-session source/structure/fully qualified method inventory checks PASS; 13/13 observed **in each of WSL2 and Windows**, no missing/extra/duplicate names. This is a **readback** of recorded evidence, not a new test run.
- **New Python audit helper/unit test code:** actual isolated Python 3.13.5 `unittest` **9/9 PASS, zero skips**, with synthetic source/log/receipt test fixtures. Both resulting exact Python file blobs matched local `git hash-object` before GitHub submission. These unit tests do **not** constitute a full exact-worktree execution of the auditor against the unmodified R17 production-grade Git checkout.
- **Not run this round:** new auditor against the full exact GitHub worktree, the R17 Python suite itself, native Z3/cvc5/TLC, and any real publisher/Claim/CAS. Original R17 native 32/32 and Python dual-host 13/13 remain bound to their historical evidence SHA only.

**Usage** from a full experiment checkout: `python formal/v4.19/coverage/executed_inventory_audit.py`. On matching exact bytes returns `PASS_RECORDED_EXACT_BLOB_EXECUTION_INVENTORY`, **not** `MODEL_AND_SOURCE_PASS` or independent host attestation.

**Decision:** close this narrow *recorded test inventory crosscheck* without promoting it into full ADS atomic obligation coverage, no obligatory Local Agent replay for data-only evidence, and continue with another materially changed rule family or authorized real consumer. Full ADS atomic rule denominator `UNKNOWN`. No normative source, existing Claim, Gate, CI, PR #1365, Freeze, Merge or Release mutation.
