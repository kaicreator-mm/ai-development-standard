# R9 reliability & validation scope — executed toolchain slice

As of 2026-11-10, the formal experiment fixes **two verification-runner defects** without changing any ADS normative rule or the R8 35-case model suite.

**Finding R9-PY-P1-01:** The missing TLC JAR path returned a partial `NOT_RUN` dictionary without `property_id`; the coverage aggregator used `x["property_id"]`. This could turn a deterministic BLOCKED result into a Python exception and an absent receipt. R9 now returns a uniform envelope. Full exact worktree runner regression **NOT_RUN**; do not treat a source diff as executed acceptance.

**Finding R9-PY-P1-02:** The R7 toolchain checker hashed solver bytes but still executed `--version` even on SHA mismatch. R9 checks SHA *before any executable version probe*, and the run orchestrator refuses `run_case()` after failed/unknown tool identity. Both changes are necessary to prevent accidental execution of unverified solvers. For TLC, a mismatched JAR is rejected before Java probing. Java itself remains unpinned and is explicitly a host trust assumption.

## Actual isolated execution (not a claim of full ADS proof)

The exact Git blobs were independently reconstructed from GitHub at code HEAD `a49f691e8537c847183dc991bf275ba330210352` and verified by local `git hash-object`:

- `formal/suite/toolchain.py` → `6705dcb31957dc49efbf6c303b2f08f33d721206`
- `formal/tests/test_toolchain.py` → `edbab0352f174443f8a76b318873b7a1f8618c4e`

Python 3.13.5: **5/5 tests PASS**, including executable/JVM side-effect sentinels that remain absent when hashes mismatch. Log SHA256 `9a23016933a9f6a59442b79613fdba9a85c405f7d26002228f31c03906c106cf`.

Live offline archive binaries: **Z3 5.3.3 PASS**, **cvc5 1.4.2 PASS**, **TLC 2.19 JAR PASS** against recorded inventory hashes. Local run receipt SHA256 `156931cb31cb5ecfc8edcd20fcf183fa0859990e2533d516089f16a0c0804637`. These prove binary identity and helper contract, not mathematical solver correctness or host attestation.

**T08 actual source delta:** From the observed v4.18 baseline to prospective PR #1365, 6/7 mapped sources changed, invalidating **10/10 Properties and 35/35 cases**. An isolated DAG-only change invalidates **5/10 Properties and 15/35 cases** by transitive dependency. These are metadata selections, not rerun solver passes.

## Final acceptance boundary

R9 full Python suite, R8 35-case exact-source native integration, real candidate-code consumer and fresh independent semantic review are **NOT_RUN**. Existing R5 strict 27/27 was executed on its previous HEAD; R6 4/4 and R8 4/4 were incremental model runs on their earlier HEADs. Do not add these numbers to claim a new 35/35 PASS.

Remaining trust assumptions: Java process itself is not pinned, other shared-library/runtime dependencies are not proven, and a hash-check/execution TOCTOU race cannot be excluded by this helper. No new FIR, formal ADS norm, CI gate, Claim, Freeze, merge or release.
