# Task — <ID> <title>

## Contract

- Target version/milestone: `<version>`
- Canonical type: `type:task`
- Canonical state: `<state:planned|state:ready|...>`
- Integration target: `<branch>`
- Baseline SHA: `<40-char-sha>`
- Review Policy: `<required|recommended|not-required>`
- Risk: `<low|medium|high|critical>`
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
- Task Pack: `<ref>`
- L3: `<ref|NOT_APPLICABLE>`
- Pinned standard / overrides: `<refs>`

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

## Execution Constraints

- <required execution/authority constraint>

## Durable Execution / Prompt Artifacts

- `<ref|NOT_APPLICABLE>`

Any task-specific instruction required by an executor MUST be durable in this Issue or an authoritative artifact referenced here before dispatch. Do not use a long chat prompt to fill missing contract fields.

## Allowed Changes

- <paths/concerns>

## Forbidden Changes

- <paths/semantics>

## Failure / Blocker Handling

- <what becomes FAIL/BLOCKED and where evidence/handoff is recorded>

## Completion

Implementation is done only when the declared concern gates, Review condition, dependency/target constraints, and merge result are satisfied. PR PASS is not Release PASS.

## Metadata Invariants

- exactly one canonical work-item type;
- exactly one active `state:*` workflow state;
- exactly one `review:*` policy for implementation work;
- Gate result and dynamic Agent/session identity are NOT labels.
