# Task Pack — T07 Adoption & Cross-standard Wiring

Task: T07
Dependencies: T02, T03, T04, T05
Integration target / merge target: `version/v4.6.0`
Risk: high
Review: required Fresh Independent Review
Validation: integration, owner T07
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Allowed write-set
- `standard-manifest.json`
- `templates/golden/STANDARD_COVERAGE.json`
- `templates/project/.dev-standard/PROJECT_OVERRIDES.md`
- `checklists/project-init.md`
- `checklists/pr-review.md`
- `checklists/version-closure.md`
- `docs/implementation/4.6.0/MIGRATION_ADOPTION.md`
- `scripts/test_v46_adoption_wiring.py`

## Forbidden scope
No T01–T05 semantic rewrite, no new lifecycle/Gate/Release state, no v4.7 unified resolver or repository refactor.

## Acceptance
All three v4.6 normative owners, two machine families and references/tests are discoverable. Golden coverage remains exactly aligned with the normative set. PROJECT_OVERRIDES exposes materiality-driven AI-native adoption without weakening Frozen authority. Existing Assurance/Dispatch/Handoff/Validation/Release owners are linked by reference. Fast Path does not require empty records. Historical evidence is not retrofitted.

## Required gates
Focused wiring tests, project-template/adoption regression, verify-standard CI, exact-head integration Validation, Fresh Independent Review.

## L3
`docs/implementation/4.6.0/L3_REFERENCE_PACKS.md#t07--adoption--cross-standard-wiring`

## Failure handling
A required central-wiring path outside this write-set needs an explicit authority amendment before modification. Technical necessity alone is not write authority.
