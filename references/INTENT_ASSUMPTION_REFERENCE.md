# Intent & Assumption Governance Reference

Implementation guidance subordinate to `standards/INTENT_ASSUMPTION_GOVERNANCE_STANDARD.md`, Frozen v4.6 Product/L2 and the existing T01 `schemas/intent-assumption-record-v1.schema.json`. These cases are illustrative domain facts, not independent Product/Task/Review/Validation decisions.

## Source → interpretation → material clarification

A user says (source `issue:feature-discussion#comment-01`) "support offline use". The Agent might interpret "offline" as "all third-party calls prohibited", but that extra statement must be recorded as `INTERPRETATION`, not `USER_INTENT`. If the distinction affects the Product boundary, mark `materiality=MATERIAL`, include `source_ref`, keep `currentness_ref`, and use conceptual `ROUTE` → wire `CLARIFY` with `disposition.target_ref` pointing at the existing Product decision Issue. If no authorized destination is known, `BLOCK` rather than inventing a PM approval.

Illustrative v1 record for the **interpretation**, not the user's actual sentence:

```json
{
  "schema_version": 1,
  "record_id": "intent-42-interpretation-01",
  "repository": "example/project",
  "subject_ref": "issue:42",
  "classification": "INTERPRETATION",
  "content_ref": "evidence:interpretation-42",
  "source_ref": "issue:42#comment-01",
  "evidence_refs": ["evidence:approved-summary-42"],
  "materiality": "MATERIAL",
  "currentness_ref": "issue:42@observed-sha",
  "disposition": {"action": "CLARIFY", "target_ref": "issue:product-decision-47"},
  "created_by_ref": "agent:analysis-1",
  "created_at": "2026-09-30T08:00:00Z"
}
```

Here `target_ref` identifies **where clarification is requested**. No Product Freeze or user consent has occurred simply because the record validates against JSON Schema.

## Promotion: intent record is an association, not the authority

Before promotion, a material assumption may have `classification=ASSUMPTION` and `disposition.action=PROMOTE_BY_OWNER` with a destination `target_ref`. That is a pending owner request even if the Agent adds speculative references. Only after the actual Product/Architecture/Task owner durably accepts an appropriate requirement may a **new** `DURABLE_REQUIREMENT_REF` record link to it. The new record must have **both** `promotion_authority_ref` and `promoted_requirement_ref`, plus source/currentness evidence appropriate to the claim. Verify that those references actually resolve to the current owner-issued decision; the v1 schema checks shape, not authorization truth.

```json
{
  "schema_version": 1,
  "record_id": "intent-42-requirement-pointer-02",
  "repository": "example/project",
  "subject_ref": "issue:42",
  "classification": "DURABLE_REQUIREMENT_REF",
  "content_ref": "requirement-summary:42",
  "source_ref": "issue:42#comment-01",
  "evidence_refs": ["evidence:product-decision-47"],
  "materiality": "MATERIAL",
  "currentness_ref": "product-frozen-ref:exact-revision",
  "disposition": {"action": "RETAIN"},
  "promotion_authority_ref": "product-owner:approved-decision-47",
  "promoted_requirement_ref": "product:requirements#offline-47",
  "created_by_ref": "agent:scribe-1",
  "created_at": "2026-09-30T09:00:00Z"
}
```

A fixture may validate this shape with synthetic identifiers, but **must not claim** that the fictional owner actually approved anything. Negative cases drop either promotion reference, cite an obsolete target, turn a model's interpretation into `USER_INTENT`, or treat `PROMOTE_BY_OWNER` alone as success.

## Contradiction / supersession without erased history

If two current material sources disagree, preserve `contradiction_refs`, identify the shared semantic owner and route to that owner's decision path. An Agent may not choose by recency, prompt order or number of supporting models. A later `SUPERSEDE` references `supersedes_refs` and a durable replacement via `disposition.target_ref`; the prior contradictory record remains inspectable. Missing owner, source, currentness, replacement or authorized decision is an explicit unresolved `DECISION_REQUIRED`/`BLOCK`, not silent promotion.

## Frozen L2 action-to-wire crosswalk

`ROUTE` = `CLARIFY` plus material owning destination `disposition.target_ref`; `PROMOTE_REF` = `PROMOTE_BY_OWNER` **request**, with separate accepted `DURABLE_REQUIREMENT_REF` only after actual owner-issued target and required two refs; `SUPERSEDE_REF` = `SUPERSEDE` plus prior `supersedes_refs` and replacement target. `RETAIN`, `REJECT` and `BLOCK` are existing schema actions, not new workflow states. When source or destination is unknown, use `BLOCK` instead of writing fictitious `target_ref` values. A user's exact words and an Agent interpretation must keep distinct `source_ref` and `created_by_ref` identities.

## Adoption and evidence strength

Persist material records where the owning project needs durable handoff. Historical Dispatch/Execution Pack records do not need new optional Intent refs retroactively. A valid JSON fixture proves only shape/conformance; it never proves external user consent, actual owner issuance, runtime execution, Validation PASS or Release qualification. This standard creates no Context Snapshot database and never overrides the v4.1–v4.5 security, artifact, migration, deployment or incident owners.