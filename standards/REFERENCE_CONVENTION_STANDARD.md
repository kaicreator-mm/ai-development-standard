# Reference Convention Standard

Status: **Normative — v4.7**

## 1. Purpose

This standard defines compatible meanings for common development references without replacing owner-specific contracts. Reference naming does not create authority, state or evidence transfer.

## 2. Exact subject identity

When exact identity is material, references MUST distinguish the requested/expected subject from the subject actually tested, validated or reviewed.

Typical meanings:

- `requested_sha` / `review_head` / equivalent: exact candidate identity requested for an activity;
- `tested_sha` / `validated_sha` / equivalent: exact identity actually executed by evidence;
- `expected_base_sha`: exact integration/base identity whose currentness the activity expects;
- `current_head_sha` / live PR HEAD: a mutable observation that MUST be re-read before a currentness-sensitive action.

A branch, tag, channel, alias, `latest`, chat description or other mutable locator MUST NOT substitute for an exact SHA when the owning contract requires exact subject identity.

## 3. Currentness

An exact historical reference remains evidence about its original subject. It does not prove that a mutable branch/PR/base still points to the same identity.

Required negative:

```text
old exact-SHA PASS -> successor exact-SHA PASS
```

Currentness-sensitive actions must re-read the applicable live identity from its owning surface.

## 4. Authority references

An authority reference MUST resolve to durable authority that is allowed to decide the referenced concern: for example a Frozen Product/L2 owner, Task Pack, approved project override, or another explicitly owning standard/work item.

A credential, token, provider, model, tool installation, API capability, runtime availability or transport account is capability/provenance context and MUST NOT become an authority reference merely because it can perform an action.

```text
capability_ref != authority_ref
```

## 5. Evidence and provenance references

Evidence references identify evidence; provenance references identify origin or production lineage. Neither grants mutation/merge/side-effect authority, and neither transfers a PASS/FAIL/READY conclusion to a materially different subject.

```text
evidence_ref present != mutation authorized
provenance_ref present != normative owner
```

The owning Validation/Review/Release/Deployment/etc. contract decides applicability of the referenced evidence.

## 6. Existing owner-specific field names

Existing contracts MAY retain field names such as `head_sha`, `candidate_sha`, `base_sha`, `expected_base_sha`, `artifact_ref`, `authority_ref`, `validation_refs`, or equivalent when their semantics are unambiguous in the owning contract.

v4.7 does not require historical payloads to rename fields into a universal reference object. Cosmetic consistency is not sufficient authority for a wire-format migration.

## 7. No universal replacement object

This standard does not create or require:

- a universal Subject Identity object;
- a universal Authority object;
- a universal Evidence object;
- a repository-wide live currentness database;
- a new workflow/Validation/Review/Release state.

If a future incompatible normalization becomes materially valuable, record it for future-major migration rather than rewriting historical meaning in v4.7.

## 8. Required forbidden inferences

| Reference fact | Forbidden conclusion |
|---|---|
| branch/tag/alias resolves now | exact required subject identity established forever |
| provider/tool/credential ref exists | authority granted |
| evidence ref points to prior PASS | current/successor subject PASS |
| provenance points to owner/tool | provenance source is normative authority |
| two fields have different names | meanings necessarily differ |
| two fields look similar | meanings may be globally collapsed |
| cosmetic normalization is possible | historical schema rewrite authorized |

## 9. Failure handling

Ambiguous material identity, authority or evidence applicability fails closed to the owning contract. Do not normalize by guessing. Broken/stale refs must be refreshed or surfaced as UNKNOWN/BLOCKED under the owning workflow rather than silently substituted.
