# T-003 Review Checklist

## Exact subject / write set
- [ ] Candidate PR HEAD/TREE/base are exact and current (base `version/v4.9.0@df94641e...`).
- [ ] Diff is limited to the five Builder paths declared in MANIFEST plus immutable `.agent/execution/T-003/**` planning files.
- [ ] Frozen Product/L2/DAG-v0.2 blobs and current Task Pack (`14c65526...`)/L3 blobs resolve unchanged at the candidate.

## Registry integration acceptance
- [ ] One canonical owner/applicability entry per v4.9 concern; inherited entries preserved verbatim; zero duplicates.
- [ ] State-dimension registrations cover proof/currentness + `WAITING_LINEAGE` derived posture; no workflow lifecycle state added.
- [ ] Both registries validate against their inherited v1 schemas (read-only inputs unmutated).
- [ ] Reference docs are descriptive only and grant no authority.

## Forbidden-inference conformance
- [ ] N01–N14 negative oracles executable (not structural strings only) and passing.
- [ ] Inherited F01–F10 state-dimension negatives intact and non-weakened.
- [ ] No second discovery table/resolver; no workflow state; no authority inference from metadata.

## Gates
- [ ] Repository verifier PASS at exact candidate; Builder checks present but not treated as independent Validation.
- [ ] Independent registry/forbidden-inference Validation PASS before Fresh Review; Fresh Review on the same unchanged exact HEAD.
