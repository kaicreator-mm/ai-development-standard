# T-014 Review Checklist

## Exact subject / write set
- [ ] Candidate PR HEAD/TREE/base exact and current (base `version/v4.9.0@d53e943e...`).
- [ ] Diff limited to the three Builder write-set paths plus immutable `.agent/execution/T-014/**`.
- [ ] Frozen blobs resolve unchanged at candidate; no Release surfaces edited.

## Contract acceptance
- [ ] D01-D08 oracles executable and passing; exact-candidate binding, nonzero delta, fail-closed ambiguous predicates, auditor eligibility, evidence-only posture all real.

## Gates
- [ ] Repository verifier PASS; Builder checks not treated as independent Validation.
- [ ] Independent evidence-contract Validation PASS before Fresh Review; Fresh Review on same unchanged exact HEAD.
