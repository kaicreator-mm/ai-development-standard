# Task Pack — T06 Session / Operator Handoff Dogfood

Task: T06
Dependencies: T02, T03, T04, T05
Integration target / merge target: `version/v4.6.0`
Risk: high
Review: required Fresh Independent Review
Validation: exact-subject dogfood Validation, owner T06
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Allowed write-set
- `docs/implementation/4.6.0/dogfood/**`
- `scripts/test_v46_session_handoff_dogfood.py`

## Forbidden scope
No normative owner changes, no production side effect, no hidden chat transcript as required authority, no claim that fixture evidence proves an unexecuted real Agent/runtime dimension.

## Acceptance
A fresh logical session/executor reconstructs from durable facts: request, Frozen/current authority, exact subject identity, completed evidence, findings/blockers, remaining work, next owner/action and forbidden assumptions. Same transport account and logical operator/context are kept distinct. The dogfood packet excludes the originating chat/session as required input.

## Required gates
Focused dogfood test, exact-subject Validation, Fresh Independent Review. Real multi-Agent/runtime execution is required only for dimensions explicitly claimed by the dogfood.

## L3
`docs/implementation/4.6.0/L3_REFERENCE_PACKS.md#t06--session--operator-handoff-dogfood`

## Failure handling
If a required real capability is unavailable, create a dedicated Validation Request binding the exact packet/runtime/claim. Static/fixture proof remains labeled static and cannot be promoted to real-runtime PASS.
