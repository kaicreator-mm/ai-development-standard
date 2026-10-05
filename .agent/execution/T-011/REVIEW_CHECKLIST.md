# T-011 Review Checklist

## Exact subject / write set
- [ ] Candidate PR HEAD/TREE/base exact and current (base `version/v4.9.0@a351a6ef...`).
- [ ] Diff limited to the seven Builder write-set paths plus immutable `.agent/execution/T-011/**` (+ the JIT-committed harness path re-bind).
- [ ] Frozen Product/L2/DAG blobs, Task Pack, L3 resolve unchanged at candidate.

## Central wiring acceptance
- [ ] A01-A07 oracles executable and passing; exactly-one-new-default-family accounting real.
- [ ] Manifest adoption complete (v4.9 outputs discoverable; T-002 registration gap closed; inherited verbatim).
- [ ] CI registration appended in style; existing commands unremoved/unreordered.
- [ ] Re-binds provenance-commented; assertion strength preserved (exact-set/identity still fail on violations).
- [ ] Registry metadata authority-free; adoption/migration guidance truthful and resolving.

## Gates
- [ ] Repository verifier PASS; full pinned battery (now incl. v4.9 kernels) PASS.
- [ ] Independent manifest/registry/adoption Validation PASS before Fresh Review; Fresh Review on same unchanged exact HEAD.
