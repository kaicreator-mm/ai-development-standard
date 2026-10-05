# T-007 Review Checklist

## Exact subject / write set
- [ ] Candidate PR HEAD/TREE/base exact and current (base `version/v4.9.0@1fa88bc1...`).
- [ ] Diff limited to the four Builder write-set paths plus immutable `.agent/execution/T-007/**`.
- [ ] Frozen Product/L2/DAG blobs, Task Pack, L3, and read-only dependency refs resolve unchanged at candidate.

## Semantic kernel acceptance
- [ ] K01-K10 oracles executable (real reducer/predicate/agg semantics, not structural strings) and passing.
- [ ] Assurance currentness consumption at Dispatch/Claim/merge with deterministic drift recompute (no stale latch).
- [ ] JIT predicate truth table complete (READY only when everything passes; WAITING_LINEAGE/BLOCKED otherwise).
- [ ] WAITING_LINEAGE derived non-dispatch; hard filters before ranking; carry-forward with Adversarial Review aggregation ownership preserved; no review shopping.
- [ ] Race/drift cases deterministic and fail-closed.

## Standard composition
- [ ] New sections compose additively; v4.0–v4.8 invariants untouched; consumed contracts cited by exact refs.
- [ ] Product E/F/G/K/L/M/N + L2 currentness/JIT/adverse negatives bound to oracles with exact refs.
- [ ] No second scheduler/claim lifecycle or runtime authority store.

## Gates
- [ ] Repository verifier PASS; Builder checks not treated as independent Validation.
- [ ] Independent reducer/JIT/currentness/race Validation PASS before Fresh Review; Fresh Review on same unchanged exact HEAD.
