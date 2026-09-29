# Task Pack — T01 Shared AI-native Machine Contracts

Task: T01
Dependencies: none
Integration target: `version/v4.6.0`
Risk: high
Review: required Fresh Independent Review
Validation: concern
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Allowed write-set
- `schemas/intent-assumption-record-v1.schema.json`
- `schemas/skill-metadata-v1.schema.json`
- `schemas/dispatch.schema.json`
- `schemas/execution-pack-manifest.schema.json`
- `scripts/test_v46_ai_native_contracts.py`

## Forbidden scope
No normative Intent/Context/Skill policy. No Context Snapshot family. No new Assurance, Review, Validation, Release, Agent-freedom, or Dispatch result/state family.

## Acceptance
Exactly two new default machine-contract families. Existing-schema additions, if needed, are optional references and backward compatible. Intent records do not create Product/Architecture/Task authority. Skill metadata does not create mutation authority. Historical Dispatch and Execution Pack payloads remain valid when new references are absent.

## Required gates
Focused contract tests, verify-standard CI, exact-head concern Validation, and Fresh Independent Review.

## L3
`docs/implementation/4.6.0/L3_REFERENCE_PACKS.md#t01--shared-ai-native-machine-contracts`

## Failure handling
If the frozen contract cannot be represented additively with the repository-supported schema subset, stop as an architecture conflict and route back to L2. Do not create a parallel state family.
