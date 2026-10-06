# V410-T04B R3 Repair Review Checklist

Fresh successor Validation/Review must bind one unchanged R3 candidate and verify:

- [ ] R3 canonical Execution Pack was current and an accepted repair Builder claim preceded mutation.
- [ ] PR #901 and all R1 candidate gates remain historical-only; no evidence/verdict transfer.
- [ ] Historical bucket-only REVIEW_RESULT payloads remain readable.
- [ ] Newly emitted/current material findings cannot satisfy T04B aggregation without stable identity, severity, root-defect class and evidence/provenance.
- [ ] Writer/admission/conformance behavior is machine-testable, not only prose SHOULD guidance.
- [ ] Two independent reviewers may use different finding IDs for the same logical defect and converge only through a durable deterministic existing-family equivalence/disposition relation.
- [ ] Ambiguous/conflicting duplicate equivalence fails closed; root-defect class alone is not treated as logical-defect identity.
- [ ] Duplicate convergence preserves every reviewer provenance record and does not create majority/model-count authority.
- [ ] Exact-subject stale non-transfer and current conflict fail-closed behavior remain intact.
- [ ] No second Review/finding lifecycle/event/status/registry, no Validation/Release authority, no central manifest wiring.
- [ ] Historical legacy `.agent/execution/V410-T04B/` six-file pack is absent from the R3 candidate.
- [ ] Focused + relevant regression suites pass on exact R3 HEAD/tree.
- [ ] Task/PR PASS is not Release PASS.
