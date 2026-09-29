# T01 — Shared Evolution Machine Contracts

Parent version: v4.2.0 Evolution Governance
Frozen Product: `fc68e869c18cec07e2a72b8fa5e4520ade1dc5a9`
Frozen L2: `ea4532cacf87c03689351e43363580e2a14acd95`
Task DAG: `docs/implementation/4.2.0/TASK_DAG.md`
Review policy: required
Validation scope: concern
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal
Implement the minimum machine layer for compatibility and migration truth without introducing lifecycle/Gate state authority.

## Allowed write-set
- `schemas/compatibility-record-v1.schema.json`
- `schemas/migration-transition-v1.schema.json`
- narrowly justified optional references in existing evidence schemas
- `scripts/test_v42_evolution_contracts.py`

## Forbidden
No normative standards, no manifest/PROJECT_OVERRIDES wiring, no Task/Validation/Release state changes, no provider-specific compatibility framework.

## Acceptance
- Draft 2020-12 meta-valid schemas;
- baseline/candidate and source/target identities explicit;
- operation vs compatibility outcome orthogonal;
- compatibility dimensions extensible;
- absent dimensions do not imply compatibility;
- migration recovery represented without mandatory down migration;
- no embedded Gate PASS/FAIL authority;
- historical payloads remain valid when optional refs are absent;
- focused positive and adversarial negatives pass.

## Implementation reference
See `L3_REFERENCE_PACKS.md#t01--shared-evolution-machine-contracts`.

## Completion
Concern Validation + Fresh Independent Review PASS on exact HEAD, then merge to v4.2 integration branch.