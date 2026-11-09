# R8 — Independent adversarial recheck of the R6 successor witness

**Source:** historical R5 reviewer findings S1–S3; additional R8 model-to-norm challenge. Formal-only experiment; the source candidate PR #1365 HEAD remains `dac263fa4c0ab155406d2f2117459b34322cc988` and is unmerged.

## Discovered false-positive witness (model defect)

R6's `I05` calls `secondStartRecord` satisfiable whenever `originalTerminal ∧ ¬sameDispatch ∧ currentGeneration`, **without establishing that an earlier accepted originalClaim ever existed, that the new successor had fresh authority, or that a successor Claim was accepted**.

Constructive adversarial queries on R6 model bytes `formal/models/authority/admission-boundaries.smt2`, SHA256 `e41df24adab85a1c50358840b7eba3b32662769cfae4047e26acf4bef53cd4cb`:

1. `secondStartRecord ∧ ¬originalClaim` → **SAT** in Z3/cvc5.
2. `secondStartRecord ∧ ¬successorAuthorized` → **SAT** in Z3/cvc5 (the latter predicate not part of R6).
3. An unaccepted successor proposal can similarly be declared a new Start Record.

This is a **P1 in the *formal model's claimed semantic correspondence***, not a P1 demonstrated in normative ADS source or implementation. It invalidates interpreting R6 `I05` as a proof of authorized post-terminal handoff.

## Targeted repair preserving the R6 receipt

R8 does not change historical R6 files. It adds `admission-boundaries-r8.smt2` with a stronger successor constraint:

```smtlib
(assert (=> secondStartRecord
  (and originalClaim originalTerminal (not sameDispatch) currentGeneration
       successorAuthorized successorClaimAccepted)))
```

New queries `I06/I07/I08` each require `UNSAT`; `I05` must remain `SAT` with all its implicit premises satisfiable. The independent R8 mutant explicitly restores the broken R6 predicate and exposes three `SAT` counterexamples. Normal: **18 native queries per solver**, mutually identical; mutant: **3 SAT queries per solver**, mutually identical. Actual execution in the local Linux container used the previous verified binary identities Z3 5.3.3/cvc5 1.4.2 and exact Git model blobs read back from GitHub.

**Scope discipline:** 31 R6 suite cases retained, four new R8 cases added → **35 declared cases / 10 pilot Properties**. Only the four new cases were actually run in this R8 round; previous R5 27 strict and R6 four incrementals are not fresh executions at the new R8 HEAD. R8 strict dual-worktree check, full Python regression, current toolchain-snapshot run and independent fresh semantic reviewer are still `NOT_RUN`.

## Remaining assumptions

An accepted original Claim and separately authorized successor Claim are *abstract Boolean predicates*. The SMT has no real GitHub Claim admission transaction, publication idempotency, compatible-group owner/authority readback, terminal reconciliation, or CAS implementation. Full ADS normative rule denominator remains unknown; do not convert these 18 bounded assertions into a universal theorem or ADS gate.
