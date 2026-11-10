# R10 — Solver differential coverage regression

## Root defect
`solver_differential` previously ignored native SMT groups if either Z3 or
cvc5 was absent. Its result could therefore be empty even when the caller
expected independent corroboration. This is a **formal checker qualification
defect**, not a demonstrated issue in the ADS normative rules.

The R10 suite now explicitly declares `require_solver_pairs: true` and pins
that declaration through the existing exact Git model-input provenance.
Grouped by `(property_id, model, purpose)`, each group must have exactly one
Z3 and one cvc5 case. A missing partner returns `INCONCLUSIVE`, never PASS.
Duplicate/orphan result IDs, divergent answers, or mismatched solver provenance
are separately rejected. Mutants are compared independently of normal proofs.

Current metadata: **35 cases; 16 SMT pairs / 32 SMT cases; 3 TLC cases; 10
pilot properties; 7 mapped source files; zero missing pairs**.

## Executed isolated evidence
Python 3.13.5, 6/6 `unittest` PASS, return code 0 on the exact Git blob bytes
of `formal/suite/differential.py` and `formal/tests/test_differential.py`.
Git blob readback and test log digest are recorded in
`EXECUTION_RECEIPT.json`. No new SMT/TLC native model was authored.

## Remaining acceptance
Do not infer a 35/35 strict run from model declaration or these six tests.
The complete source-bound R10 runner and independent new-property semantic
review remain NOT_RUN. No ADS normative Gate, merge, Freeze, release or
re-interpretation of the historical R5/R6/R8 receipts.
