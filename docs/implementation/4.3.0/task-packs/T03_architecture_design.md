# T03 — Architecture Design Standard

Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`
Review: required | Validation: concern | Freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal
Create the durable design-quality owner for material architecture decisions while preserving L2 as the research/evidence workflow.

## Allowed write-set
- `standards/ARCHITECTURE_DESIGN_STANDARD.md`
- `references/ARCHITECTURE_DECISION_REFERENCE.md`
- `scripts/test_v43_architecture_design.py`

## Acceptance
- materiality/applicability rules;
- drivers/invariants/boundaries/ownership/contracts/failure semantics/security/durability/observability/deployment assumptions when material;
- bounded Decision/Alternatives/Rationale/Trade-offs/Failure modes/Evidence/Escape hatch semantics;
- high-impact UNKNOWN cannot silently become implementation freedom;
- no universal architecture paradigm;
- v4.2 remains compatibility/migration semantic owner;
- Fast Path proportionality preserved.

## Forbidden
No L2 prompt replacement, no compatibility/migration standard rewrite, no ADR file-format mandate, no Task decomposition/DAG/profile ownership.

## Reference
`L3_REFERENCE_PACKS.md#t03--architecture-design-standard`.