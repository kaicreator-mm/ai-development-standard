# ADS formal Python runner — optional R1 experiment (no FIR)

This is a small Python **verification process**, not a new normative ADS standard, development gate, proof language, or shared intermediate representation.

The runner reads a per-version test list (which identifies native models and expected results), runs Z3/TLA+/TLC in isolated bounded subprocesses, checks the expected result, hashes model inputs, and writes a JSON receipt. The test list contains no executable Python or shell commands. The reasoning remains in the native .smt2/.tla files.

Run from the repository root:

    python3 formal/suite/run.py --suite formal/v4.19/r0/suite.json --z3 /path/to/z3 --tlc-jar /path/to/tla2tools.jar --out /tmp/ads-formal-receipt.json

For exact input-source alignment, also pass:

    --source-checkout /path/to/checkout-at-candidate-HEAD --strict-source

Without a matching candidate Git checkout, the result is MODEL_ONLY_PASS + source NOT_RUN, even when all model checks pass. Strict source mode exits nonzero for missing, stale, mismatched or unverified source. Any missing tool, timeout, solver UNKNOWN or unexpected output cannot pass.

Mutation cases must produce the specific counterexample; their DETECTED result is an indication that the **checker** catches an intentionally defective model, not a flaw in ADS. Natural-language semantics vs formalized rules must be independently evaluated before wider claims.

To extend: add another version-local test list and native model; add a tool adapter only when needed. Alloy, Lean, pySHACL and Souffle are optional future adapters. Do not install additional frameworks or introduce FIR by default.

## R5 — exact experiment-model provenance (v1 suite only)

For the current v4.19 experiment, use an **experiment Git worktree** containing the formal models and another independent **candidate Git worktree** pinned to PR #1365 candidate HEAD. Execute the existing Python entry point from the experiment worktree.

```bash
python3 formal/suite/run.py \
  --suite formal/v4.19/r4/suite.json \
  --model-head "$(git rev-parse HEAD)" \
  --source-checkout /path/to/candidate-exact-sha-worktree \
  --strict-source \
  --z3 /path/to/z3 --cvc5 /path/to/cvc5 \
  --tlc-jar /path/to/tla2tools.jar \
  --out /tmp/ads-formal-source-bound.json
```

The R5 verifier now checks two independent byte identities:

- `--model-head`: exact experiment HEAD, including the selected native models/configs, suite/index/source-map/Traceability inputs, and the Python runner/helpers; checks them against Git blob SHA **before and after** model execution. Missing model pin limits an ordinary run to MODEL_ONLY_PASS; invalid pin or modified models fail closed; `--strict-source` requires PASS.
- `--source-checkout`: candidate ADS HEAD and all seven declared source Git blobs. All source-map anchors and additional traceability anchors must be present. The source-readback manifest is a constrained sample, **not** every ADS rule.
- `--strict-source` cannot turn a definite solver failure into a weaker BLOCKED finding, and a partial `--property` or `--changed-source` run must retain its selected-scope evidence and may not masquerade as full ADS verification.

The R5 implementation has direct local regression evidence for `provenance.py` and `differential.py`, but the complete newly integrated `formal/suite/run.py` path with dual Git worktrees and all Python tests is **NOT_RUN**. Mandatory independent semantics evaluation is **NOT_RUN**. Do not change this to PASS on source-only inspection. No new FIR, extra scheduler, Claim writer, normative ADS Gate, GitHub Actions job or mandatory Node-major requirement.

**Execution update 2026-11-10 (experiment round 2).** The integrated path above has now been
actually executed, not merely inspected: complete `formal/tests` unittest 18/18 on exact repo
bytes; full r4 suite 27/27 with `--model-head`, `--source-checkout` and `--strict-source`
returned `MODEL_AND_SOURCE_PASS` at experiment HEAD `e64702c` (Z3 5.3.3 + cvc5 1.4.2 + TLC
2.19, binary digests matching `formal/tools/inventory.json`); nine adversarial scenarios
(model tamper, wrong model HEAD, wrong source HEAD, source anchor drift, cross-solver
divergence, incremental invalidation propagation, unmapped changed-source, partial-scope
eligibility, strict-without-checkout) all fail closed; independent Source→Model semantic
review produced with findings S1-S6. Executed defects fixed on the experiment branch:
`e64702c` restores the R3-era rule that `--strict-source` must not mask a definite solver
failure as BLOCKED. Evidence: `formal/v4.19/r5/R5_SOURCE_BOUND_RUN.json`,
`R5_SOURCE_BOUND_RECEIPT.json`, `SEMANTIC_REVIEW.md`, `R5_FINAL_RERUN_RECEIPT.json`. Still
NOT_PROVEN: full ADS rule denominator, natural-language equivalence theorem, real GitHub
Claim/CAS/CI/Host/Release, Freeze or merge.
