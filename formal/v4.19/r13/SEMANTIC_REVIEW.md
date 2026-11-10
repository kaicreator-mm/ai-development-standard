# ADS #1366 R13 — Bounded Dispatch publication semantic gap proof

**Source:** candidate PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988` (OPEN), `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` Git blob `935a905d593d7aec027cb54b5b137250ca14a4c1`. Historical R8 `admission-boundaries-r8.smt2` blob `73c7ab4d845129b5f6335e275c9e696bc3a5b3d3`.

## Why this work is warranted
R11 already passed 35/35 native models and 61/61 Python tests at its original exact model/source SHA. Repeating the same test suite or creating new simulated Controller APIs would not resolve the remaining semantic gap. In contrast, the prospective v4.19 source requires the complete enriched dispatch, **effective project-pinned ADS schema**, publication-time equality of the checked and written object, and **zero accepted Dispatch/Claim mutation on schema/pin/drift failure**. The existing R8 `reservedA` guard constrains READY/current generation/publication ambiguity, but has no schema-identity or emitted-payload predicate.

## Actually executed
The exact old `reservedA` definition was compared against R8 Git source. `weak-admission-gap.smt2` has four **SAT** results: the old **reservation abstraction** is satisfiable despite a bad/unresolved schema or unchecked payload, or with a legitimate READY case. This proves only lack of model coverage: reservation is **not** a canonical accepted Dispatch event.

`publish-safety.smt2` is a new bounded, explicitly **asserted** necessary-conditions guard over a *single prospective new durable Dispatch and Claim mutation*. It contains **11 queries**: two nonvacuous legal/blocked `SAT` witnesses and nine forbidden `UNSAT` acceptances (no pin, wrong schema, check/write schema or payload drift, incomplete/failed validation, stale authorization, unserialized publication).

**Z3 5.3.3 and cvc5 1.4.2 each passed 15/15 expectations, 30 matching outputs overall**, with exit code 0 and SHA256 pinned to the historical validated binaries. `run_proofs.py` checks SHA256 **before** launching native tools; a deliberately unpinned fake binary was refused without execution. `run_mutations.py` removed six essential guard conditions and **both solvers caught 6/6** material regressions. Reproduce from this directory:
```bash
ADS_Z3=/path/to/verified/z3 ADS_CVC5=/path/to/verified/cvc5 python3 run_proofs.py
ADS_Z3=/path/to/verified/z3 ADS_CVC5=/path/to/verified/cvc5 python3 run_mutations.py
```
Original complete solver/negative receipts are `SOLVER_PAIR_EXECUTION.json`, `MUTATION_EXECUTION.json`; structured summary `R13_BOUND_EVIDENCE.json`. All four source files and both exact raw receipts were verified against local Git blob SHA at publication.

## Formal qualification, not to overstate
**R13 = BOUNDED_SOURCE_HYPOTHESIS_PASS, NOT production Controller proof.** The nine UNSAT outputs follow from a necessary-condition guard *we posited*, not from verified execution of a real GitHub Scheduler/Agent publisher. Schema/payload identity uses uninterpreted equality, not real SHA-256 or linearizable GitHub CAS. The old `reservedA` is reservation only; its SAT cases cannot establish an ADS normative defect or unsafe accepted mutation. There is no confirmed v4.19 effective project adopter or production readback. Clause-level source/model semantic equivalence and total ADS rule denominator remain **NOT_PROVEN/UNKNOWN**.

**Independent semantic source review: NOT_RUN.** This is Builder source interpretation + two authentic native solvers. New cases are deliberately *not included in R11's frozen 35-case manifest*; no new GitHub Actions, runtime Gate, formal standard change, merge/Freeze/Release or Local Agent task.
