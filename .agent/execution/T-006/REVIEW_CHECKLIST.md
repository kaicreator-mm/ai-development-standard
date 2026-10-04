# T-006 Review Checklist

## Exact subject / write set
- [ ] Candidate PR HEAD/TREE/base exact and current (base `version/v4.9.0@df94641e...`).
- [ ] Diff limited to the four Builder write-set paths plus immutable `.agent/execution/T-006/**`.
- [ ] Frozen Product/L2/DAG blobs, Task Pack, L3, and read-only v4.8 Task Learning v1 owner refs resolve unchanged at candidate.

## Same-family successor acceptance
- [ ] task-learning-v2 is a versioned same-family successor; v1 instances remain v1-valid (no silent re-interpretation); compatibility record machine-checkable and truthful.
- [ ] Optional execution_friction_class / recurrence / root-cause / prevention / recurrence-audit fields are references only, resolve-or-fail-closed, orthogonal to friction_classification.
- [ ] No learning DB, no new intake lifecycle, no workflow state, no automatic ADS mutation.

## Gates
- [ ] Repository verifier PASS; Builder checks not treated as independent Validation.
- [ ] Independent same-family-compatibility Validation PASS before Fresh Review; Fresh Review on same unchanged exact HEAD.
