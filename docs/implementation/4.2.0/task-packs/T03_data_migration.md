# T03 — Data & Migration Governance

Depends on: T01
Frozen Product: `fc68e869c18cec07e2a72b8fa5e4520ade1dc5a9`
Frozen L2: `ea4532cacf87c03689351e43363580e2a14acd95`
Review policy: required
Validation scope: concern
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal
Create the single normative owner for persistent-state transition identity, ordering/dependencies, environment applicability and recovery strategy.

## Allowed write-set
- `standards/DATA_MIGRATION_GOVERNANCE_STANDARD.md`
- `references/DATA_MIGRATION_REFERENCE.md`
- `scripts/test_v42_data_migration.py`

## Required semantics
- source and target state/baseline explicit;
- transition is directional;
- fresh install != upgrade;
- successful upgrade != interrupted recovery;
- runtime/database/environment tuple non-substitution;
- migration presence != executed migration;
- high-risk/destructive migration requires risk/recovery treatment;
- recovery strategy required but down migration not universal;
- backup/restore, forward repair, expand/contract and rollback migration can be valid when evidenced;
- production mutation needs explicit applicable authority;
- Fast Path/materiality preserved.

## Forbidden
No rollout/deployment result ownership, no incident lifecycle, no Validation PASS state, no universal migration framework/database.

## Required adversarial tests
Reject fresh->upgrade substitution, A→B->B→A substitution, migration-file->executed inference, credential->production-authority inference and no-down->no-recovery inference.

## Implementation reference
See `L3_REFERENCE_PACKS.md#t03--data--migration-governance`.

## Completion
Exact-HEAD concern Validation + Fresh Independent Review PASS, then merge.