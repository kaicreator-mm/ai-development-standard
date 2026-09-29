# T04 — API / Service Compatibility Conformance & Dogfood

Depends on: T02
Frozen Product: `fc68e869c18cec07e2a72b8fa5e4520ade1dc5a9`
Frozen L2: `ea4532cacf87c03689351e43363580e2a14acd95`
Review policy: required
Validation scope: concern
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal
Prove the interface compatibility standard rejects common Agent shortcuts and supports a real positive evolution path.

## Allowed write-set
- v4.2 API/service conformance fixtures under repository-conventional conformance/test locations
- `scripts/test_v42_api_compatibility_conformance.py`
- evidence/reference fixtures owned by this Task only

## Required scenarios
1. additive backward-compatible interface evolution positive;
2. wire/schema-safe but source/application-incompatible negative;
3. schema-compatible but behavioral-incompatible negative;
4. new producer + new consumer PASS does not prove old consumer + new producer;
5. baseline/consumer identity drift invalidates prior claim;
6. UNKNOWN/unexecuted dimension cannot become COMPATIBLE.

## Contract boundary
Consumes T01 schemas + T02 standard. Creates no new normative owner.

## Execution choice
Prefer deterministic local fixtures/protocol examples. A real external service is required only if the chosen claim depends on provider behavior; if so, create explicit Validation handoff before execution.

## Failure handling
Weak fixture coverage is a test defect. Provider/network unavailability, if a real provider is required, is BLOCKED rather than fabricated compatibility FAIL/PASS.

## Completion
Exact-HEAD focused Validation + required Fresh Independent Review PASS.