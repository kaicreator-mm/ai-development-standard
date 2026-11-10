# ADS #1366 — Convergence decision after R11

**Decision:** stop adding Demo rounds, extra validation tools and speculative SMT models until the **current exact experiment HEAD** receives one full suite integration result. Source authority is GitHub; [Issue #1366](https://github.com/kaicreator-mm/ai-development-standard/issues/1366) is the program index. The experiment remains non-normative.

## Why the previous flow was inefficient

The sequence after R10 added useful Python reliability checks and synthetic source demonstrations, but repeatedly increased the declared test denominator without a complete integration run. It produced a misleading visual signal of progress: the 35/35 model results and 41/41 Python results are **correct only for R10's former exact commit**, while later 61 declared test methods had not been run together. Do not keep adding tools or one-off rounds until this bottleneck is addressed.

The repo state comparison is mechanical, not speculation:

- Previously strict-validated experiment model HEAD: `671c5fac858de000c867d03284413add204d2b01`.
- Current observed experiment HEAD: `390db1ec8e438d892a6aa3e6661fa0ebdb0a7216`; target candidate: PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988` (open).
- Among R10's **30** Git-model-pinned inputs, **29 are exact-blob identical**, **one changed**: `formal/suite/expanded.py` from `7eabb53f...` to `3a7bbbed...`. The 35-case suite, every native model, and native tool inventory are **unchanged**.
- The R10 35 native outputs can be referenced as historical model evidence; they are **not** current HEAD strict runner PASS. The new runner changed the binary-provenance receipt logic.
- This container has offline Z3/cvc5/TLC pinned bytes **3/3 SHA PASS**, Java available. Two previously added test modules, checked against exact Git blobs, were **reexecuted together 14/14 Python PASS** with log SHA256 `083a53df9aec4a557ad8224b806119c37f0319e89d1662dfe2b0429be4fb6718`. The local copy of `expanded.py` is **not** the exact current Git blob, so this is partial, not full strict integration.

## Execution adjustment and hard stop rule

1. **WEB Builder** performs source-code/model/tool impact analysis, repairs source, and runs whatever actual tools are available. Historic PASS is reused with exact-SHA qualification rather than assumed to be current.
2. **One and only one** latest-SHA full integration acceptance is required before additional expansion: 61 currently declared Python methods (actual zero-skipped discovered/executed result, not count alone) and 35 R10 native cases with `--model-head`, `--source-checkout`, `--strict-source`, and source/tool/model/traceability checks. Check 16 paired SMT groups and TLC adversarial cases. After a repair, recompute impacted closure and rerun the necessary final full qualified subject once.
3. Current container cannot DNS-resolve GitHub for `git clone` and therefore cannot construct two complete authentic worktrees. **LOCAL Agent is not a default developer**; only if this exact Git capability gap persists, give it a **single combined integrate+repair+validate+receipt** task. Never a validation-only handoff. If a Web Git checkout becomes available, all work stays with Web.
4. With integration finally qualified, return to **T01 source→obligation coverage**: 46 normative *documents* and 10 pilot Properties, but total ADS *rule obligations* UNKNOWN. Focus on source-grounded high-impact unmatched obligations; do not use 3/46 file references as proof coverage or generate 46 synthetic property models.
5. Update #1366 with the completed outcome, exact HEAD/TREE, final evidence, P0/P1/P2 and NOT_PROVEN; do not merge or Freeze PR #1365.

Machine-readback evidence: `CONVERGENCE_READBACK.json`. This is an impact/partial-execution receipt, **not** current-head `MODEL_AND_SOURCE_PASS`.
