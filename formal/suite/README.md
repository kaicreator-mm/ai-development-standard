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
