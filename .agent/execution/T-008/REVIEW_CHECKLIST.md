# T-008 Review Checklist

## Exact subject / write set
- [ ] Candidate PR HEAD/TREE/base exact and current (base `version/v4.9.0@f4fe8854...`).
- [ ] Diff limited to the four Builder write-set paths plus immutable `.agent/execution/T-008/**`.
- [ ] Frozen Product/L2/DAG blobs, Task Pack, L3 resolve unchanged at candidate.

## Wiring acceptance
- [ ] W01-W06 oracles executable and passing; backward compatibility proven (v1 instances valid).
- [ ] Refs carry identity only — no duplicate Task scope/Claim authority/gate truth.
- [ ] Compatibility record truthful; material change declared.

## Gates
- [ ] Repository verifier PASS; Builder checks not treated as independent Validation.
- [ ] Independent schema/compat/claim-binding Validation PASS before Fresh Review; Fresh Review on same unchanged exact HEAD.
