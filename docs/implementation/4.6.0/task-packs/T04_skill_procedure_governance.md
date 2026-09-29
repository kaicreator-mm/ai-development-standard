# Task Pack — T04 Skill / Reusable Agent Procedure Governance

Task: T04
Dependencies: T01
Integration target / merge target: `version/v4.6.0`
Risk: high
Review: required Fresh Independent Review
Validation: concern, owner T04
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Allowed write-set
- `standards/SKILL_PROCEDURE_GOVERNANCE_STANDARD.md`
- `references/SKILL_PROCEDURE_REFERENCE.md`
- `scripts/test_v46_skill_procedure.py`

## Forbidden scope
No Task/Product authority rewrite, no provider/model mandate, no new Dispatch or side-effect authorization state, no sibling Context/Intent implementation.

## Acceptance
Reusable procedure identity/version/source/owner/applicability and authority-input refs are explicit. Tool and side-effect classes describe procedural needs but do not grant authorization. Imported procedures require project acceptance/provenance. One-off Task facts stay with Task/Execution authority. Compatibility/deprecation/evaluation/failure routing are durable.

## Adversarial minimum
Reject installed→trusted; tool capability→authorized mutation; procedure instruction→override Frozen Product/Task; one-off Task fact→reusable authority; incompatible procedure version→silent acceptance.

## Required gates
Focused semantic/metadata tests, verify-standard CI, exact-head concern Validation, Fresh Independent Review.

## L3
`docs/implementation/4.6.0/L3_REFERENCE_PACKS.md#t04--skill--procedure-governance`

## Failure handling
Untrusted provenance, missing required authority, incompatible version or out-of-scope action fails closed and routes to the applicable owner.
