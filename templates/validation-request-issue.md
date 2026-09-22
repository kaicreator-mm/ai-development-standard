# Validation Request — <target>

## Contract

- Target version/task: `<ref>`
- Type: `type:validation`
- State: `<canonical state>`
- Requested exact SHA: `<40-char-sha>`
- Validation scope/profile: `<concern|integration|closure|platform-profile>`
- Validation owner: `<role/work item>`

## Validation Tuple

- artifact/code identity: `<sha/ref>`
- environment: `<runner/build-host/platform>`
- commands/profile: `<durable ref or commands>`
- expected checks: `<checks>`

## Required Evidence

- exact SHA
- environment identity/capability
- executed checks
- result: `PASS | FAIL | BLOCKED | NOT_RUN | NOT_APPLICABLE`
- failure/blocker details when non-PASS

## Staleness Rule

If target HEAD/identity moves, this request/result MUST NOT be asserted onto the new identity.

## Forbidden

Do not encode validation PASS/FAIL as a mutable routing label.
