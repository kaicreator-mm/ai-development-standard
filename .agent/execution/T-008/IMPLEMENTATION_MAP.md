# T-008 Implementation Map

Builder writes only:
1. `schemas/dispatch.schema.json` — additive optional reference fields only (established schema style; no `$ref`/`definitions` — the repo's supported JSON-Schema subset forbids them).
2. `references/EXECUTION_CONTRACT_REFS_V49_COMPATIBILITY.json` — compatibility record (pattern: `references/TASK_LEARNING_V2_COMPATIBILITY.json` at base).
3. `references/EXECUTION_CONTRACT_REFS_V49_REFERENCE.md` — semantics + consistency rules.
4. `scripts/test_v49_execution_contract_refs.py` — tests per TEST_MATRIX. Style references (read-only): `scripts/test_v49_task_learning_v2.py`, `test_v48_orchestration_dogfood.py` (dispatch fixtures).

Read-only inputs: `schemas/dispatch.schema.json` at base (existing fields/instances), Frozen PRD/L2, DAG v0.1 `### T-008`, L3 T-008 section, §29.1/§29.2 of EXECUTION_ARCHITECTURE_STANDARD.md (what the refs must carry).
