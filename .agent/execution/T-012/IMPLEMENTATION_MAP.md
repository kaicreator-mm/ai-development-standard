# T-012 Implementation Map

Builder writes only:
1. `scripts/test_v49_conformance_suite.py` — deterministic stdlib-unittest: one test class per coverage item (precedence vs conjunction; reduction fail-closed; assurance TOCTOU; carry-forward; selector/independence conflicts; JIT in-envelope vs DAG mutation; gate-owned transfer/currentness; Release per-gate applicability/non-aggregation; predecessor lineage wait; Task Learning same-family compat; manual-compatible state reconstruction) + a coverage manifest test asserting all DAG `### T-012` items are covered. Bind to merged owner outputs with exact refs. Style references (read-only): `test_v49_execution_core.py`, `test_v49_gate_currentness.py`.
2. `fixtures/conformance-suite/**` — scenario fixtures.
3. `scripts/test_v49_gate_currentness.py` — F1 t07 re-bind (pin constants + provenance only).
4. `scripts/test_v48_integration_closure.py` — F2 C01/C08 re-binds (pin constants + provenance only).
5. `.github/workflows/verify-standard.yml` — append `python scripts/test_v49_conformance_suite.py` in established style.

Read-only inputs: the DAG v0.1 `### T-012` coverage list; Frozen PRD scenarios A–Q; Frozen L2 positive/negative oracles; the merged owner surfaces (assurance plan standard/schema; role profile schema; release applicability owner; task learning v2; execution core §29; dispatch refs; DAG governance reference; gate currentness matrix).
