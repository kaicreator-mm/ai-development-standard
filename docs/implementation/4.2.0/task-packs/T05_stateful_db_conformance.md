# T05 — Stateful Database Migration Conformance & Dogfood

Depends on: T03
Frozen Product: `fc68e869c18cec07e2a72b8fa5e4520ade1dc5a9`
Frozen L2: `ea4532cacf87c03689351e43363580e2a14acd95`
Review policy: required
Validation scope: concern + real-environment evidence when required
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal
Prove persistent-state transition semantics on representative state, including failure/recovery, without substituting fresh bootstrap evidence.

## Allowed write-set
- v4.2 database migration conformance fixtures/scripts owned by this Task
- `scripts/test_v42_migration_conformance.py`
- deterministic seed/state fixtures and evidence helpers

## Required scenarios
1. create a supported source state A with representative data;
2. execute A→B transition and verify target state/data invariants;
3. separately execute fresh bootstrap and prove it is a different subject;
4. exercise at least one failed/interrupted transition and recovery path;
5. demonstrate a valid recovery strategy that does not require a down migration;
6. bind actual database/runtime/environment identity;
7. reject cross-engine/runtime substitution when material.

## Local/external gate
If realistic proof requires an actual SQLite/PostgreSQL or other database runtime not available to Web/GitHub execution, create a dedicated `type:validation` handoff Issue before running it. The handoff MUST bind exact PR HEAD, database/runtime version, fixture identity, allowed state mutation, cleanup and expected evidence.

## Forbidden
No production data, no deployment orchestration, no schema standard redesign, no result fabrication when runtime is unavailable.

## Completion
Required real/focused Validation + Fresh Independent Review PASS on exact HEAD.