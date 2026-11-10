# R10 — Independent source-to-model semantic review (R8 successor Claim)

Independent reviewer pass executed 2026-11-10 on separate exact-SHA Git worktrees,
not reusing any builder-round scratch state. Review base: experiment
`experiment/v4.19-formal-proof-r0` at `cd4d291edc41114ecc26a3853f5f3afbdc0f13ee`;
candidate source: PR #1365 head `dac263fa4c0ab155406d2f2117459b34322cc988`
(unmerged, unchanged). Scope fixed by the R10 acceptance list: the
`ADS-P-ADMISSION-EXT` successor-Claim (post-terminal Start Record) semantics in
`formal/models/authority/admission-boundaries-r8.smt2` against the candidate
normative sources.

## Method

1. Source readback from the exact candidate checkout (blob+anchor verified by the
   strict runner in the same session): terminal/release handling in
   `standards/EXECUTION_ARCHITECTURE_STANDARD.md` (idempotent resume §11; §11.1
   serialized admission; takeover preconditions; attribution between terminal and
   successor Claim) and the matching protocol clauses in
   `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` (terminal ownership release;
   idempotent resume MUST NOT create a second active claim/Start Record).
2. Premise-by-premise mapping of the model's `resume` and `secondStartRecord`
   implications onto those source clauses.
3. Hand derivation of all 18 query outcomes at the review base before execution,
   then execution of the full 35-case strict suite (baseline) to confirm the
   derivation and exclude suite/wiring artifacts.

## Confirmed alignments (review base cd4d291)

- `resume ⇒ originalClaim ∧ sameDispatch ∧ sameOperator ∧ currentGeneration ∧
  ¬originalTerminal ∧ ¬secondStartRecord` matches the source rule that the same
  logical operator re-claiming the same dispatch at the current generation is
  idempotent, keeps exactly one active claim and never creates a second Start
  Record.
- `secondStartRecord ⇒ originalClaim ∧ originalTerminal ∧ ¬sameDispatch ∧
  currentGeneration ∧ successorAuthorized ∧ successorClaimAccepted` matches the
  R8 repair intent and the source takeover preconditions: durable terminal, a
  different dispatch identity, generation currentness, separately authorized new
  dispatch, and an accepted successor Claim (responsibility is attributable
  between the terminal and the successor's accepted Claim).
- Internal consistency: all 18 expected answers at the review base were derived
  by hand and matched by both solvers (16/16 differential pairs PASS).

## Finding R10-SEM-P2-01 (P2, formal experiment model fidelity)

The source takeover clause requires the related **publication** (and resource)
facts to reconcile and states that ambiguous publication/release state **fails
closed** before another operator may take over. The same model file already
consumes `(not publicationAmbiguous)` in the S1 reservation CAS (query R03), but
the S2-R8 successor clause did not. Therefore the `I05` legal-successor witness
was satisfiable with `publicationAmbiguous = true` — a false witness of exactly
the family the R8 round repaired (R6 `I05` successors without premises).

Severity: **P2** — the bounded hypothesis model under-approximated one explicit
source premise; `normative_ads_defect: NOT_ESTABLISHED` (the candidate normative
source is the stricter, correct side; no ADS rule text is defective).

## Repair (experiment write set, commit `671c5fac858de000c867d03284413add204d2b01`)

- `admission-boundaries-r8.smt2`: successor clause now additionally requires
  `(not publicationAmbiguous)`; new query `I09` asserts `secondStartRecord ∧
  publicationAmbiguous` is UNSAT (18 → 19 native queries per solver).
- `formal/v4.19/r10/suite.json`: both `ADS-P-ADMISSION-SUCCESSOR-R8-Z3/CVC5`
  expect lists gain the `I09` unsat answer (18 → 19 entries; case count stays 35).
- `formal/tests/test_r8_successor.py`: model pin re-anchored to SHA256
  `448c01e7e309102e61bbb784975db212b589f23aee9fe3210f5eccf38a4867d0` with the
  19-answer sequence; mutant bytes (`c47171e6a82faac2bc291dcd94af48684027a65d646c29f4e133f248f2d9fab8`)
  and mutant expectations untouched.

## Post-repair verification (final run at 671c5fa)

- Full `formal/tests` unittest: 41/41 OK, 0 skipped, exit 0
  (log SHA256 `81d2207f8b378315a75868eee16c7fe34a6dd96a8d32bb5227915f43df25e6c2`).
- Full strict 35-case suite: `MODEL_AND_SOURCE_PASS`, 16/16 independent solver
  pairs PASS; `I09` answered `unsat` identically by Z3 5.3.3 (`fcd0ca76…`) and
  cvc5 1.4.2 (`6aecddf4…`); both successor mutants remain detected (3×SAT).
- Per-case status diff baseline (cd4d291) vs final (671c5fa): **no case changed
  status**; the only sequence delta is the inserted `unsat` at position 14 of the
  two successor cases. Evidence: `R10_FINAL_STRICT_RUN.json` (committed).

## Post-repair conclusion

The R8 successor-Claim model is semantically **CONSISTENT** with the candidate
source for the modeled premises at the final head, with the publication
fail-closed premise now enforced and adversarially checked (I09). Resource-fact
reconciliation remains unmodeled (bounded abstraction, declared limitation).

## NOT_PROVEN (unchanged boundaries)

Full ADS normative rule denominator; natural-language ⇄ SMT/TLA+ semantic
equivalence theorem; real GitHub Claim CAS / CI / Host / Release execution;
real publication/resource fact verification (inputs remain abstract Booleans);
TLC liveness/fairness, claim expiry, multi-Task CAS, version inheritance;
solver/JVM host provenance beyond pinned bytes; TOCTOU outside the runner.
Historical R5/R6/R8 receipts remain tied to their own earlier exact SHAs and are
not re-executed or reinterpreted here.
