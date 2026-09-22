# Version <version> — <goal>

## Contract

- Version: `<version>`
- Baseline: `<exact-sha-or-release>`
- Integration branch: `<version-branch>`
- Review Policy: `<required|recommended|not-required>`
- Risk: `<low|medium|high|critical>`

## Goal

<bounded version outcome>

## Frozen Authority

- PRD / Scope: `<ref>`
- Architecture: `<ref>`
- Planning Task DAG: `<ref>`
- Standard pin / overrides: `<refs>`

## Canonical DAG

- Planning DAG checkpoint: `<path/ref>`
- Live DAG: GitHub Task Issues + native Issue Dependencies
- Derived state card: `<ref|NOT_APPLICABLE>`; if present it MUST be marked `NON_AUTHORITATIVE_DERIVED_STATE`

## Materialized Tasks

- `<T-ID> — #<issue>`

## Required Version Gates

- <gate>

## Closure Criteria

- [ ] all required Task dependencies/gates complete
- [ ] final exact candidate validated
- [ ] required Independent Review satisfied
- [ ] Release Qualification satisfied
- [ ] immutable baseline recorded

## Forbidden

- Do not use this body as a live per-Agent event log.
- Do not treat a status table in this Issue as more authoritative than Task Issues/dependencies/evidence.
