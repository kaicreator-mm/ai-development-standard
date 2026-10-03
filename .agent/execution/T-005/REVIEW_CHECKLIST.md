# T-005 Review Checklist

Reviewer/Validator must verify on the exact final candidate:

- [ ] only authorized source write set plus immutable `.agent/execution/T-005/**` pack is present;
- [ ] `RELEASE_STANDARD.md` remains the sole Release authority and no parallel lifecycle appears;
- [ ] applicability is explicit per gate × subject and UNKNOWN fails closed;
- [ ] concern-level applicability does not aggregate into version-level Release Qualification;
- [ ] existing thaw/invalidate/Hidden/Closeout/RQ authority remains intact;
- [ ] migration is prospective-only and cannot shorten in-flight authority-bound gates;
- [ ] T-007/T-010/T-014/T-015 sibling scope is untouched;
- [ ] focused tests and repository verifier pass;
- [ ] independent semantic/historical Validation precedes a genuinely Fresh required Review;
- [ ] merge authorization is expected-head only after currentness recheck.
