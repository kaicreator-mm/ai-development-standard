# T-015 Review Checklist

## Exact subject / write set
- [ ] Candidate PR HEAD/TREE/base exact and current (base `version/v4.9.0@a4f1debe...`).
- [ ] Diff limited to the three Builder write-set paths plus immutable `.agent/execution/T-015/**`.
- [ ] Frozen blobs resolve unchanged at candidate.

## Integrated dogfood acceptance
- [ ] I01-I06 oracles executable and passing; predecessor identity exact; journeys deterministic; reconciliation real; handoff truthful.
- [ ] No unsupported generality; downstream NOT_SATISFIED posture preserved unless the qualifying contract is met; safety negatives zero; no stale binding laundered.
- [ ] Handoff documents contain no closure/RQ verdict (inputs only).

## Gates
- [ ] Repository verifier PASS; Builder checks not treated as independent Validation.
- [ ] Independent integration/exact-subject-dogfood/closure-handoff Validation PASS before Fresh Review; Fresh Review on same unchanged exact HEAD.
