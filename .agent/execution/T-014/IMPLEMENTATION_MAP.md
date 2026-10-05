# T-014 Implementation Map

Builder writes only:
1. `references/DOWNSSTREAM_DOGFOOD_AUDIT_CONTRACT_V49.md` — the contract document bound to Frozen Product §16 / L2 rows and the T-010 gate matrix (M10 dogfood row) by exact refs.
2. `scripts/test_v49_dogfood_audit_contract.py` — deterministic negatives per TEST_MATRIX. Style reference (read-only): `test_v49_gate_currentness.py`.
3. `fixtures/dogfood-audit-contract/**` — scenarios.

Read-only inputs: Frozen PRD §16; Frozen L2 dogfood rows; T-010 `references/GATE_EVIDENCE_CURRENTNESS_MATRIX.md` M10; T-005 release applicability owner surfaces; DAG v0.1 `### T-014`; L3 T-014 section.
