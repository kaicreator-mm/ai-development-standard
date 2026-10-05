# T-009 Implementation Map

Builder writes only:
1. `references/JIT_DAG_MUTATION_GOVERNANCE_V49_REFERENCE.md` — classification table + routing + currentness/native-dependency requirements, bound to the v4.3 governance owner by exact refs.
2. `scripts/test_v49_jit_dag_governance.py` — deterministic classifier tests per TEST_MATRIX. Style reference (read-only): v4.3 governance tests (locate via `grep -rl "dag.mutation" scripts/` at base).
3. `fixtures/jit-dag-governance/**` — mutation scenario fixtures.

Read-only inputs: v4.3 Task DAG Governance owner standard (find via `grep -l` in standards/), EXECUTION_ARCHITECTURE_STANDARD.md §28 (JIT predicate it wires into), Frozen PRD item L, Frozen L2 JIT/DAG negatives, DAG v0.1 `### T-009`, L3 T-009 section.
