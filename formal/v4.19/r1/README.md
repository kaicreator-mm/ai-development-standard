# ADS formal verification R1 (non-normative)

Source: kaicreator-mm/ai-development-standard PR #1365 candidate HEAD dac263fa4c0ab155406d2f2117459b34322cc988. Branch-only experiment; no Freeze, Release, normative gate, or main merge.

Reuses immutable R0 under formal/v4.19/r0 and extends the existing formal/suite/run.py. The R1 pilot contains five native SMT-LIB domains with Z3+cvc5 checks. TLC lifecycle R0 is historical; R1 did not rerun that model.

Run from repo root:

    python formal/suite/run.py --suite formal/v4.19/r1/suite.json --z3 /path/z3 --cvc5 /path/cvc5 --java java --tlc-jar /path/tla2tools.jar --out formal/v4.19/r1/receipt.json

Use --source-checkout /path/to/exact-candidate for Git blob and anchor checks, --strict-source to fail when source alignment is missing, --property or --model to narrow cases, or --changed-source to select affected properties (always invalidates previous source binding).

Test with ADS_FORMAL_Z3 and ADS_FORMAL_CVC5 environment variables:

    python -m unittest discover -s formal/tests -v

Coverage is 5 of 6 declared R1 pilot properties and 0 source-bound verified. The denominator of **all ADS normative rules** has not been established; total ADS coverage is UNKNOWN. R0 TLC semantics, independent review, real Claim/CAS, general DAG cycles, continuous liveness and production Release remain NOT_PROVEN.
