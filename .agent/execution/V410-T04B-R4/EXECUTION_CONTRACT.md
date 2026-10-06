# V410-T04B R4 bounded repair contract

Integration base: `30334e8c7b90a327f8597b86c88c785b98df07f7`.
Repair base / historical R3 candidate: `e03beedd9d02336407365efa66efc43d34e96954`.
Task Pack and L3 remain frozen and unchanged.
Execution environment: LOCAL.

Fresh Independent Review R3 on PR #918 returned CHANGES_REQUESTED with P0=0/P1=2/P2=0/P3=0. R3 Validation PASS is historical evidence only for R3 and does not transfer to R4.

## R4 repair scope

P1-1 — writer example / current-event consistency:
- Make the canonical REVIEW_RESULT writer example internally conformant.
- Define executable compatibility between positive legacy P0..P3 buckets and structured records for newly emitted/current events.
- Any positive material bucket not reconstructible from records MUST fail the current new-writer/aggregate conformance path.
- Historical bucket-only payloads remain readable history.

P1-2 — durable post-hoc duplicate reconciliation:
- Reuse the existing review-finding-v1 DUPLICATE/disposition family.
- Support F-A + independent unlinked F-B + later durable F-B DUPLICATE F-A disposition as one logical finding.
- Aggregation must consume the later durable disposition (or an explicit current superseding projection), preserve both original provenance records, remain transport-order invariant, and fail closed on competing/ambiguous/stale/cross-subject disposition.

## Allowed write set
- standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md
- templates/agent-event-comment.md
- scripts/test_v410_t04b_review_currentness.py
- schemas/agent-event-v2.schema.json only if a same-family projection gap is concretely proven
- existing review finding/aggregation validator surface only if focused tests prove a real owner-local gap

## Forbidden
No second Review lifecycle/event/status/registry. No new finding registry. No majority/latest/model/provider-count authority. No T04A/T02B/Validation/Release ownership absorption. No central manifest/discovery changes. No historical verdict transfer.

Keep PR #918 as the same concern PR if practical; new HEAD invalidates R3 exact-subject gates and requires fresh R4 Validation + Fresh Review.
