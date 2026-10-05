# T-012 Review Checklist

## Exact subject / write set
- [ ] Candidate PR HEAD/TREE/base exact and current (base `version/v4.9.0@d53e943e...`).
- [ ] Diff limited to the five Builder write-set paths plus immutable `.agent/execution/T-012/**`.
- [ ] Frozen Product/L2/DAG blobs, Task Pack, L3 resolve unchanged at candidate.

## Conformance acceptance
- [ ] C01-C12 oracles executable and passing; every DAG v0.1 T-012 coverage item bound to merged owner outputs with exact refs.
- [ ] Suite is a test oracle — asserts owner semantics, redefines none; owner defects routed not repaired.
- [ ] C13: F1/F2 re-binds pin-constants-only with provenance; passing at candidate.

## Gates
- [ ] Repository verifier PASS; integrated battery (incl. appended conformance command) PASS.
- [ ] Independent deterministic A-Q/L2 Validation PASS before Fresh Review; Fresh Review on same unchanged exact HEAD.
