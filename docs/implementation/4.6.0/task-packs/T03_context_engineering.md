# Task Pack — T03 Context Engineering

Task: T03
Dependencies: none
Integration target / merge target: `version/v4.6.0`
Risk: high
Review: required Fresh Independent Review
Validation: concern, owner T03
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Allowed write-set
- `standards/CONTEXT_ENGINEERING_STANDARD.md`
- `references/CONTEXT_ENGINEERING_REFERENCE.md`
- `scripts/test_v46_context_engineering.py`

## Forbidden scope
No Context Snapshot/database family, no Product/Task/Dispatch state rewrite, no v4.7 repository-wide resolver.

## Acceptance
Define authority precedence, exact-currentness reread, provenance and progressive disclosure. Current higher-authority durable facts beat stale/lower historical context. Required truth may not exist only in an ephemeral session. External resources remain evidence until promoted by the owning authority. Same-level conflicts stay explicit.

## Adversarial minimum
Reject historical chat/memory→override current authority; larger context dump→higher quality; external tool output→Product truth; currentness-sensitive action without live reread; lost-session-only truth→acceptable handoff.

## Required gates
Focused semantic tests, verify-standard CI, exact-head concern Validation, Fresh Independent Review.

## L3
`docs/implementation/4.6.0/L3_REFERENCE_PACKS.md#t03--context-engineering`

## Failure handling
Insufficient or contradictory required context fails closed to unknown/blocked/decision routing. Do not invent missing authority.
