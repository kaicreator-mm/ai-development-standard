# Task Pack — T08 Cross-standard Conformance / Closure Inputs

Task: T08
Dependencies: T06, T07
Integration target / merge target: `version/v4.6.0`
Risk: high
Review: required Fresh Independent Review
Validation: integration/closure-input, owner T08
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Allowed write-set
- `scripts/test_v46_cross_standard_conformance.py`
- `docs/implementation/4.6.0/CLOSURE_INPUTS.md`
- narrowly scoped v4.6 conformance fixtures under `docs/implementation/4.6.0/conformance/**`

## Forbidden scope
No Product/L2/Task authority rewrite, no Version Closure or Release Qualification verdict, no hidden expansion into v4.7 convergence/refactor.

## Acceptance
Integrated tests reject the Product/L2 forbidden inferences, preserve v4.1–v4.5 owner boundaries, historical compatibility and Fast Path proportionality, and bind T06 handoff dogfood evidence to its actual execution fidelity. Closure inputs record exact version SHA, CI/Validation/Review evidence and unresolved findings without turning them into a Release verdict.

## Required gates
Integrated conformance regression, verify-standard CI, exact-head integration Validation, Fresh Independent Review, durable handoff to Version Closure.

## L3
`docs/implementation/4.6.0/L3_REFERENCE_PACKS.md#t08--cross-standard-conformance--closure-inputs`

## Failure handling
Subject drift, unresolved P0/P1, missing required dogfood execution or an owner contradiction remains BLOCKED for Closure. Do not downgrade missing evidence into PASS.
