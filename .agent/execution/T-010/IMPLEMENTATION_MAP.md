# T-010 Implementation Map

Builder writes only:
1. `references/GATE_EVIDENCE_CURRENTNESS_MATRIX.md` — the high-capability executable owner map: per gate (Assurance/Review/Validation/Hidden/Closeout/RQ/Release/dogfood), the currentness rule (fresh/current candidate, transfer/successor semantics, carried findings, impact decisions), each bound to its owning standard/contract by exact refs (ASSURANCE_PLAN_STANDARD (T-002), review aggregation owner, RELEASE_STANDARD + release applicability owner (T-005), EXECUTION_ARCHITECTURE §28, Frozen L2 evidence matrix rows).
2. `scripts/test_v49_gate_currentness.py` — deterministic transfer/currentness negatives per TEST_MATRIX. Style reference (read-only): `test_v49_execution_core.py` (reducer style), `test_v49_task_learning_v2.py`.
3. `fixtures/gate-currentness/**` — scenario fixtures (stale PASS, successor chains, carried findings, impact decisions).

Read-only inputs: Frozen L2 evidence/currentness matrix rows; the owner standards above; DAG v0.1 `### T-010`; L3 T-010 section.
