# Task Pack — T01 Shared AI-native Machine Contracts

Task: T01
Dependencies: none
Integration target: `version/v4.6.0`
Risk: high
Review: required Fresh Independent Review
Validation: concern
Validation owner: T01
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

## Adversarial minimum
At minimum, focused conformance MUST reject:
- intent or assumption classification being treated as Frozen Product, Architecture, or Task authority;
- skill metadata or skill installation being treated as mutation or side-effect authority;
- a Context Snapshot or parallel Agent lifecycle/result family being introduced as a substitute for durable authority refs;
- optional AI-native references becoming mandatory for historical Dispatch or Execution Pack payloads.

## Required gates
Focused contract tests, verify-standard CI, exact-head concern Validation owned by T01, and Fresh Independent Review.

## L3
`docs/implementation/4.6.0/L3_REFERENCE_PACKS.md#t01--shared-ai-native-machine-contracts`

## Failure handling
If the frozen contract cannot be represented additively with the repository-supported schema subset, stop as an architecture conflict and route back to L2. Do not create a parallel state family.
