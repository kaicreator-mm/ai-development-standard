# ADS #1366 R17 — Repair R13-R16-REV-P2-01: exact prospective source-byte binding

**Trigger:** fresh scoped source/model review at R16 HEAD `3dec2ae90f3a8bb6b926be22ecb5e14c9a7572b1`, issue #1366, found an OPEN experiment P2: R13's native runner pinned model blobs and native binaries but **not** source candidate protocol/Schema bytes. This is an evidence trust-boundary defect, not a confirmed ADS normative failure.

## Changed scope (one existing runner + one test + one fixture)

- Target: `formal/v4.19/r13/run_proofs.py`, preserving **unchanged** R13 model SMT blobs and expected SAT/UNSAT answers. Now `assert_source_hashes("preflight")` executes **before model/tool checks and before any native subprocess**, and repeats `postflight`. A missing/unreadable/modified candidate protocol or Schema fixture immediately **BLOCKS**, and postflight detects persistent drift.
- `formal/v4.19/r17/fixtures/GITHUB_AGENT_INTERACTION_PROTOCOL.md` is exactly the **original Git object blob** `935a905d593d7aec027cb54b5b137250ca14a4c1` from PR #1365 exact HEAD `dac263fa4c0ab155406d2f2117459b34322cc988`. The existing R15 Schema fixture is exactly the prospective candidate `5d9233b6b881d9d92f66fc6cd5307a05a0fdbe2f`; it is **reused**, not copied/reformatted or modified.
- New `formal/v4.19/r13/test_source_binding.py` contains 6 declarative Python unittests: original source blobs; comment-only protocol change; schema byte drift; missing protocol; post-run source drift; and frozen provenance vs actual project authorization.
- The runner includes `candidate_source.status=FROZEN_BYTES_ONLY_NOT_LIVE_HEAD_OR_ADOPTION`. A fixed Git blob proves frozen bytes match the reviewed candidate source, **not** that the GitHub PR HEAD is still the same at future runtime, nor that a project lawfully pins that prospective version. Not a formal source/model equivalence theorem.

## Evidence and limits

GitHub exact source blobs/commit/tree are independently readable; source byte identity and runner structure can be confirmed without native binaries. **Python current exact checkout execution and native Z3/cvc5 (new modified runner) must be separately reported** as `NOT_RUN` until actually invoked with the full sources. Historical R13 32/32 paired and 7/7 mutants are frozen to **older** runner/model/tool receipts only and do not retroactively qualify this modified runner; R15 13/13 Windows+WSL remain scoped to its unmodified exact source.

No live GitHub Claim/CAS/READY event or schema validator execution is attempted. R14-GAP-01/02/03 stay OPEN; independent reviewer source-level findings remain preserved. **R13-R16-REV-P2-01 is CODE_REPAIRED_AWAITING_TEST**, not fully closed without an actual exact-source Python run; full ADS rule denominator UNKNOWN. No normative source change, new GitHub Actions/CI Gate, Release/Freeze/Merge.
