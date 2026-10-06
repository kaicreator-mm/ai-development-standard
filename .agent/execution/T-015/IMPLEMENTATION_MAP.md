# T-015 Implementation Map

Builder writes only:
1. `docs/implementation/4.9.0/integration/INTEGRATION_DOGFOOD_REPORT.md` — integrated dogfood report per EXECUTION_CONTRACT item 1 (predecessor identity check; journeys; reconciliation; downstream exercise per T-014 contract; bounded claims).
2. `docs/implementation/4.9.0/integration/RELEASE_EVIDENCE_HANDOFF.md` — closure-consumable handoff per item 2.
3. `scripts/test_v49_integrated_dogfood.py` — deterministic oracles per item 3. Style references (read-only): `test_v49_conformance_suite.py`, `test_v49_manual_reference_flow.py`, `test_v49_dogfood_audit_contract.py`.

Read-only inputs: all merged v4.9 task surfaces (T-002..T-014) at the base; recovered predecessor families; Frozen PRD §16; Frozen L2; T-014 `references/DOWNSSTREAM_DOGFOOD_AUDIT_CONTRACT_V49.md` (the downstream contract to exercise); T-010 gate matrix; DAG v0.1 `### T-015`; L3 T-015 section.
