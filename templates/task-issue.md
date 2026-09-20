# Task — <ID> <title>

## Contract

- Target version/milestone: `<version>`
- Integration target: `<branch>`
- Baseline SHA: `<40-char-sha>`
- Review Policy: `<required|recommended|not-required>`
- Validation scope: `<concern|integration|closure>`
- Validation owner: `<this task|task/ref|version closure>`

## Goal

<bounded outcome>

## In Scope

- <item>

## Out of Scope

- <item>

## Frozen Inputs

- PRD/Contract: `<ref>`
- Architecture: `<ref>`
- Planning Task DAG: `<ref>`
- L3: `<ref|NOT_APPLICABLE>`

## Dependencies

GitHub Issue Dependencies are canonical once materialized.

- blocked by: `<refs|none>`
- code baseline strategy: `<independent|stacked + parent>`

## Acceptance

- [ ] <criterion>

## Required Gates

Only gates owned by this concern/integration/closure scope belong here.

- [ ] <gate/profile/tuple>

Do not copy the whole release matrix into a leaf Task unless frozen authority assigns it here.

## Allowed Changes

- <paths/concerns>

## Forbidden Changes

- <paths/semantics>

## Completion

Implementation is done only when the declared concern gates, Review condition, dependency/target constraints, and merge result are satisfied. PR PASS is not Release PASS.
