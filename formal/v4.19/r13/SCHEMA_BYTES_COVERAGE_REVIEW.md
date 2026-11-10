# ADS #1366 — R13 schema bytes negative-case blind spot and repaired native execution

## Execution reassessment

R11's 61/61 Python + 35/35 native strictly qualified historic Exact-SHA remains valid. R13 had 30/30 native results, pinned model/tool input hashes, and 6/6 mutations. But a fresh *guard-to-query* source review found one test-coverage hole with an objective adversarial witness: `publishAdmissible` requires `schemaBytesVerified`, while none of the nine rejection queries forced that predicate false and none of the six mutants removed it.

**Real red reproduction:** from R13 original model Git blob `df743519bf2e7f9ed3aa356b5f0175e7e3fb360c`, remove *only* `schemaBytesVerified` in the guard. Both actual Z3 5.3.3 and cvc5 1.4.2 returned the **identical 11 sat/unsat statuses** (original vs mutant). See `SCHEMA_BYTES_OLD_BLINDSPOT_EXECUTION.json`; mutant SHA `d510c6174a47fdaadd058247979c740934174bbc`. A new Python source guard completeness test also failed against the prior model with nine negatives vs ten conjuncts.

## Minimum repair in existing R13

1. Add **N10**: `acceptedDispatch ∧ ¬schemaBytesVerified` must be UNSAT. This is directly related to the candidate protocol's separate immutable effective-source identity and schema bytes/currentness checks. No new formalization of a production Controller is claimed.
2. Add `drop_schema_bytes_verified` to the original mutation harness, keeping all historical six mutants. The guard deletion now changes **query #11 from UNSAT to SAT**, in both native solvers.
3. Add a Python source-level regression that inventories the current **7 Boolean + 3 equality** guard conjuncts and requires ten distinct admission-negative queries, each asserting acceptance. The test fails on the old R13, passes on this one.
4. Repin `publish-safety.smt2` to Git blob `515454a82171c668739708ef50c46a254dcd9cc8` in `run_proofs.py`, preserving fail-closed pre/post checks of both model blobs and native binary SHA256. Historical R13 receipts remain at their old Git commit; use **new** `REBOUND_V2_` raw receipts for this revised model.

**Executed (not merely planned):** Python 3.13.5 **7/7 PASS**, actual Z3 and cvc5 **16/16 each, 32/32 total paired expected outcomes**, 7/7 adversarial mutants detected by both; model and tool before/after fixed SHA pass. Full raw Git-blob-bound receipts are `REBOUND_V2_SOLVER_EXECUTION.json` / `REBOUND_V2_MUTATION_EXECUTION.json`; machine summary `SCHEMA_BYTES_COVERAGE_REPAIR.json`.

## Semantics and admission boundary

This fixes an **experimental R13 test-sensitivity P2**, not a discovered ADS normative defect. The new N10 is UNSAT because R13's *assumed* necessary-condition guard requires `schemaBytesVerified`. It does **not** prove that any actual producer resolves the valid project-pinned schema bytes, executes a JSON Schema check, serializes a GitHub accepted Claim, or emits exactly the validated payload at the commit boundary. The existing model uses a Boolean for byte verification and abstract equality for schema/payload identity; real source-to-model refinement, time-ordering, effective-version adoption, actual GitHub CAS and independent external semantic review remain **NOT_PROVEN**.

**Decision:** stop adding extra mock controllers or full ADS rule-count percentages. The next high-value step is a **separate fresh reviewer** checking the full candidate source paragraph, the guarded R13 abstractions and counterexamples, and confirming scope/exception correctness. R11 full native 35/Python 61 is not rerun for this R13-only change. No official ADS standard edit, GitHub Actions, Gate, Merge, Freeze, Release, or Local Agent task.
