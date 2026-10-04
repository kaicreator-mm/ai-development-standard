# Reference Convention Reference

Non-normative guidance for `REFERENCE_CONVENTION_STANDARD.md`.

## Exact-subject tuple

For an exact-SHA Validation/Review, preserve a tuple such as:

```text
requested_head_sha: <40-hex>
observed_head_sha: <40-hex>
expected_base_sha: <40-hex>
observed_base_sha: <40-hex>
evidence_ref: <durable result pointer>
```

The field names may differ in an owning schema. The invariant is semantic: the requested subject, actually observed/executed subject and expected/current base must remain distinguishable where currentness matters.

## Mutable-locator example

```text
branch = version/v4.7.0
observed_sha = abc...
```

The branch name is a locator. `abc...` is the exact observation at that time. If the branch advances to `def...`, evidence about `abc...` remains evidence about `abc...`; it does not move with the branch.

## Authority example

Good authority references point to a durable owning source such as a Frozen Task Pack or approved project override within its allowed specialization surface.

Bad authority substitutions include:

```text
provider is connected
credential is available
model is strong
tool can write GitHub
```

Those facts may describe capability or provenance, not authorization.

## Evidence/provenance example

A Validation PASS ref for SHA A may be cited by Review for SHA A. It cannot be reused as PASS for SHA B merely because B is a descendant, rebased successor, same branch, or same filename set.

A provenance pointer may say which builder/tool produced an artifact. That does not make the builder/tool the normative owner of artifact qualification.

## Compatibility guidance

Prefer semantic adapters and documentation over mechanical renaming. Existing owner-specific names remain valid when their meaning is clear. If two historical contracts use different names for equivalent concepts, document the compatibility mapping; do not rewrite historical payloads solely for aesthetics.

## Review questions

1. Is this ref mutable or exact?
2. What subject did the evidence actually observe?
3. What owner grants authority for the decision?
4. Is a capability/provenance fact being mistaken for authority?
5. Did subject/currentness drift invalidate evidence applicability?
6. Would normalization change historical wire meaning?
