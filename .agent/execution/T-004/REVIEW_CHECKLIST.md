# T-004 Review Checklist

## Exact subject / write set
- [ ] Candidate PR HEAD/TREE/base exact and current (base `version/v4.9.0@df94641e...`).
- [ ] Diff limited to the four Builder write-set paths plus immutable 
`.agent/execution/T-004/**` planning files.
- [ ] Frozen Product/L2/DAG blobs, Task Pack, L3, and read-only v4.8 owner refs resolve unchanged at candidate.

## Contract acceptance
- [ ] Role Execution Profile v1 is the only new machine family introduced; schema provider-neutral.
- [ ] P01-P08 negative/positive oracles executable and passing; conflict => BLOCKED (no last-writer-wins); stale/missing refs fail closed.
- [ ] claim_policy_ref/eligibility refs resolve into existing v4.8 owners; no copied inventories; no authority stolen.

## Gates
- [ ] Repository verifier PASS; Builder checks not treated as independent Validation.
- [ ] Independent schema/owner-boundary Validation PASS before Fresh Review; Fresh Review on same unchanged exact HEAD.
