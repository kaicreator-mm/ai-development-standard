# T03 — Architecture Design Standard

```yaml
task_id: T03
dependencies: []
integration_target: version/v4.3.0
merge_target: version/v4.3.0
allowed_write_set:
  - standards/ARCHITECTURE_DESIGN_STANDARD.md
  - references/ARCHITECTURE_DECISION_REFERENCE.md
  - scripts/test_v43_architecture_design.py
forbidden_scope:
  - L2 prompt replacement
  - compatibility/migration standard rewrite
  - mandatory ADR file format
  - Task decomposition/DAG/profile ownership
acceptance:
  - materiality/applicability and design drivers/invariants/boundaries are explicit
  - Decision/Alternatives/Rationale/Trade-offs/Failure modes/Evidence/Escape hatch are bounded
  - high-impact UNKNOWN cannot silently become implementation freedom
  - no universal architecture paradigm
  - v4.2 compatibility/migration ownership is preserved
  - Fast Path proportionality is preserved
required_gates:
  - focused semantic tests
  - concern Validation
  - Fresh Independent Review
validation_owner: T03
review_policy: required
l3_requirement: docs/implementation/4.3.0/L3_REFERENCE_PACKS.md#t03--architecture-design-standard
agent_freedom: F1_BOUNDED_IMPLEMENTATION
risk: high
executor_suitability: Strong/Web builder and Fresh Independent Strong reviewer
failure_handling:
  - unresolved high-impact architecture UNKNOWN => BLOCKED/research route, not local invention
  - conflict with L2 or v4.2 owner => route to owning authority
```

Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`

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

## Failure handling
High-impact UNKNOWN or owner conflict fails closed to the appropriate research/authority route. An implementation Agent cannot resolve it by selecting a preferred architecture pattern.

## Forbidden
No L2 prompt replacement, no compatibility/migration standard rewrite, no ADR file-format mandate, no Task decomposition/DAG/profile ownership.

## Reference
`L3_REFERENCE_PACKS.md#t03--architecture-design-standard`.
