# R1 semantic challenge (author self-challenge, not independent review)

Scope: PR #1365 at pinned candidate HEAD. Candidate is NOT accepted ADS authority; historical #1353 and published v4.18 are governed separately. All models are bounded abstractions.

| Property | Legal path | Illegal challenge | Important limitation |
|---|---|---|---|
| ADS-P-LC | Historic R0 TLC 27-state result (not rerun in R1) | R0 release and double-Claim mutants | R1 liveness, retries, drift, expiry unproved |
| ADS-P-AUT | Current Builder Claim/write set SAT | No Claim, stale Claim, Validator, unauthorized write set UNSAT; injected mutant SAT | Actual Claim/CAS generation omitted |
| ADS-P-DEP | Two independent lanes can run SAT | Triangle cycle, shared Writer collision, missing readiness UNSAT | Does not prove general DAG acyclicity or unnecessary-edge freedom |
| ADS-P-EVI | Current CI+Review SAT | Stale CI, stale Review, missing Claim or PASS UNSAT | SHA is an abstract identity, not cryptographic verification |
| ADS-P-EVO | Grandfathered and approved prospective SAT | Historical denial persists, prospective unapproved UNSAT | Full v4.18 source mapping not yet independently established |
| ADS-P-CROSS | Release witness SAT | Missing DAG, unauthorized source mutation, stale CI UNSAT | Simplified release prerequisites, not full ADS Release qualification |

Independent semantic assessment: NOT_RUN. SAT means existence within the encoded model, not an ADS-authorized source action. Cross-solver equality checks only model reproducibility.

The strongest detected risk is a MODEL COVERAGE DEFECT: dependency logic excludes just a three-edge triangle and cannot establish arbitrary DAG safety. General DAG properties require a reachability/rank model grounded to actual Task edges; adding more copies of this test is not a repair.

Pending: exact-candidate source checkout byte verification; v4.18 normative denominator and source inventory; Claim generation/expiry/CAS; multi-task fairness and evolution migrations; independently authored semantic challenges.
