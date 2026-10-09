# V410-T04B R4 review checklist

- [ ] accepted R4 Builder claim precedes any R4 source mutation
- [ ] R3 candidate/gates remain historical and do not transfer
- [ ] canonical REVIEW_RESULT writer example is internally bucket↔records consistent
- [ ] current positive material bucket missing from records fails closed
- [ ] historical bucket-only event remains readable but never promoted into current aggregate authority
- [ ] independently emitted F-A and F-B may be reconciled later only by durable same-subject DUPLICATE disposition
- [ ] aggregation consumes the later disposition without rewriting original reviewer facts
- [ ] all original reviewer/finding provenance is preserved
- [ ] event/disposition ordering does not affect result
- [ ] competing/cyclic/stale/cross-subject dispositions fail closed
- [ ] root-class similarity/provider/model/reviewer count never establishes equivalence
- [ ] no new Review/finding lifecycle, state dimension, registry or unrelated authority
- [ ] focused + relevant regression suites pass on one exact R4 HEAD/tree
- [ ] fresh R4 concern Validation and genuinely Fresh Independent Review are both required after source repair
