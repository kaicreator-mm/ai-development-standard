# T-013 Review Checklist

## Exact subject / write set
- [ ] Candidate PR HEAD/TREE/base exact and current (base `version/v4.9.0@d53e943e...`).
- [ ] Diff limited to the three Builder write-set paths plus immutable `.agent/execution/T-013/**`.
- [ ] Frozen blobs resolve unchanged at candidate.

## Flow acceptance
- [ ] M01-M05 oracles executable and passing; every reference resolves; durable-vs-derived accurate; pointer-only triggers conform; descriptive only.

## Gates
- [ ] Repository verifier PASS. Review Policy: recommended — executed by default ( Assurance Plan lower-path skip NOT exercised unless owner-positive permission is proven, which it is not ).
- [ ] Independent reference/example Validation PASS before Fresh Review; Fresh Review on same unchanged exact HEAD.
