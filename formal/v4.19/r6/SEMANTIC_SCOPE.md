# R6 — Close the concrete S1/S2/S3 pilot-model gaps
Date: 2026-11-10. Experiment only; no normative ADS change. Candidate PR #1365 remains at `dac263fa4c0ab155406d2f2117459b34322cc988` (not frozen or merged).

## Root-cause-led scope
R5 independent semantic review produced six observations. Only **S1-S3** call for additional native model predicates; S4 is the conservative model-side write-set discipline already isolated in R4; S5 was repaired in R5; S6 was independently anchor-checked. Do not re-run unchanged 27-case R5 full-pass suite without an impacted reason.

New native SMT property `ADS-P-ADMISSION-EXT` reuses `ADS-M-AUTHORITY`; `admission-boundaries.smt2` models three logically independent bounded obligations, not a new claim admission implementation:
- **S1 reservation serialization:** no two incompatible reservations before durable terminal; stale generation denied; ambiguous publication denies new acceptance; fresh sequential reservation SAT
- **S2 idempotent resume:** a current, same-operator/same-dispatch resume cannot generate a second Start Record, stale resume denied; genuine resume and post-terminal successor each SAT
- **S3 compatibility group grant:** parallel same-work/role claims in *two distinct non-default groups* need durable ref, current grant, correct authority family and matching scope; missing grants UNSAT, fully authorized witness SAT

## Actual new native execution
Z3 5.3.3 and cvc5 1.4.2 executed two models each; both produced **identical ordered output**. Normal model 15 queries: 10 UNSAT unsafe propositions + 5 SAT legal witnesses. Deliberate mutation model: three SAT unsafe witnesses (one each for S1/S2/S3). This is **2 new normal solver case PASS_MODEL + 2 mutation case COUNTEREXAMPLE**, not 18 independently proven ADS rules.

Normal model SHA256: `e41df24adab85a1c50358840b7eba3b32662769cfae4047e26acf4bef53cd4cb`, Git blob `66d89305305541d7e095e053fa8fcb55e9e6a9b4`.
Mutation model SHA256: `056a2360bec5ff0836fbfdb5a766e89c06ea75ccad5d8e3b9ec9da760010e230`, Git blob `3e8fd89ea20ac420499c630697d212defb3490da`.

## Source semantics, bounds and next gate
Anchored to effective canonical v4.18 execution architecture §11.1/§11.1.1, prospective PR #1365 GitHub interaction protocol, and actual `scripts/v34_rules.py` (generation/compatibility validation). The abstract Boolean `grantCurrent`, `grantFamily`, `grantScope` are asserted premises, not implementation proofs. No explicit GitHub reservation CAS linearization point, conflicting transport delivery, cross-worker crash, dispatch visibility projection, timeout or arbitrary compatibility groups are modeled.

R5 full *strict dual-worktree* suite already PASS 27/27 and independent semantic review S1-S6 was completed; R6 adds 4 native cases to a **31-case suite** and does not re-label R5's 27 cases as reexecuted. R6 new strict-source full-suite checkout and independent semantic review of the new property are NOT_RUN until a new exact experiment HEAD receives both validations.

No FIR, scheduler/Claim writer, new ADS norm, CI gate, main merge, Freeze or Release.
