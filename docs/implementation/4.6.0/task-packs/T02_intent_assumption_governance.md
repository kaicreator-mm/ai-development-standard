# Task Pack — T02 Intent & Assumption Governance

Task: T02
Dependencies: T01
Integration target / merge target: `version/v4.6.0`
Risk: high
Review: required Fresh Independent Review
Validation: concern, owner T02
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Allowed write-set
- `standards/INTENT_ASSUMPTION_GOVERNANCE_STANDARD.md`
- `references/INTENT_ASSUMPTION_REFERENCE.md`
- `scripts/test_v46_intent_assumption.py`

## Forbidden scope
No Product/Architecture/Task authority rewrite, no Context/Skill owner implementation, no new workflow/Validation/Release state.

## Acceptance
Distinguish user intent, interpretation, assumption, unknown, decision-required and durable-requirement reference. Material interpretation cannot be restated as user fact. Assumption/unknown cannot self-promote. Promotion points to existing authority facts. Contradictions remain explicit and route to the applicable owner.

## Adversarial minimum
Reject chat→Frozen Product; interpretation→user fact; assumption/unknown→durable requirement; low evidence→silent promotion; contradiction→guessed resolution.

## Required gates
Focused semantic tests, verify-standard CI, exact-head concern Validation, Fresh Independent Review.

## L3
`docs/implementation/4.6.0/L3_REFERENCE_PACKS.md#t02--intent--assumption-governance`

## Failure handling
If correct behavior requires changing Product/Architecture/Task precedence, block and escalate rather than redefining it inside this Task.
