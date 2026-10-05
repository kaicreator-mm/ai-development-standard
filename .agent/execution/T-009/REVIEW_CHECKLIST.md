# T-009 Review Checklist

## Exact subject / write set
- [ ] Candidate PR HEAD/TREE/base exact and current (base `version/v4.9.0@f4fe8854...`).
- [ ] Diff limited to the three Builder write-set paths plus immutable `.agent/execution/T-009/**`.
- [ ] Frozen Product/L2/DAG blobs, Task Pack, L3 resolve unchanged at candidate.

## Classification acceptance
- [ ] G01-G06 oracles executable and passing; bookkeeping never silently mutates topology.
- [ ] v4.3 governance owner cited by exact refs, not copied; native Issue Dependency requirement enforced.

## Gates
- [ ] Repository verifier PASS; Builder checks not treated as independent Validation.
- [ ] Independent mutation-classification Validation PASS before Fresh Review; Fresh Review on same unchanged exact HEAD.
