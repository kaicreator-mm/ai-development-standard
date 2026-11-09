# R4 verification qualification and root-cause repair
Candidate PR #1365 head dac263fa4c0ab155406d2f2117459b34322cc988 (GitHub readback; not merged/frozen).

**New actual execution:** Z3 5.3.3 / cvc5 1.4.2 both ran `models/cross/writer-exclusion.smt2` and the deliberate mutant; 2 positive native tool cases PASS_MODEL, 2 negative mutation cases COUNTEREXAMPLE. Both Git blobs and SHA-256 digests match independently computed local bytes. 6 SMT assertions per solver in normal model give UNSAT, UNSAT, UNSAT, SAT, SAT, UNSAT. Mutant SAT under both solvers.

**Concrete finding:** two different protected Claim keys can each be valid while their Task write sets overlap. Claim-key admission alone is insufficient to show concurrent source writes safe; known disjointness and active per-Task Writer authority are separate assumptions. This is a *counterexample to the deliberately weakened model*, not proof of an ADS normative defect.

**Real metadata bug repaired:** R3 source-index listed `ADS-P-DEP` and `ADS-P-DEP-4` without `standards/EXECUTION_ARCHITECTURE_STANDARD.md`, though reverse TRACEABILITY did name that source. Committed R4 patch repaired both and integrated a fail-closed bidirectional traceability validator in the **existing** `formal/suite/expanded.py`, no second runner. Independent GitHub structural readback checks: 9 property IDs, 27 case IDs, 7 source paths, 13 native model files and 3 TLC configs; 0 crosslink or dependency-cycle issues. The committed Python code itself has **NOT_RUN** full integration/unit test here, so this is `PASS_STRUCTURAL_READBACK`, not a runtime PASS for the new Python path.

**Cumulative without double-counting:** R2 19 + R3 4 + R4 4 = 27 executed model cases over distinct rounds (17 normal model PASS, 10 intentional mutation detections); 9 declared pilot properties. These are not the denominator of all ADS rules. No past case is relabeled as freshly executed.

**Still unresolved:** exact source checkout and Python strict-source check NOT_RUN; semantic independent source review NOT_RUN; complete Python suite NOT_RUN; actual GitHub CAS, CI, Release and unbounded graph properties NOT_PROVEN. `MODEL_ONLY_PASS` only. No changes to formal ADS authority, historical #1353 freezes, main, tag, release, CI gate, or Task DAG.
