# T-009 JIT Execution Contract

## Exact authority
- Issue: #728 / T-009 JIT DAG Mutation Governance Integration.
- Base: `version/v4.9.0@f4fe88542de9d3f5376498e62778e2353391bc57`, tree `82ff224731e854079bdbd40a12eeffe00186b62c`.
- Frozen Product (`a8ec7030...`), Frozen L2 (`bd41ea01...`), Frozen Task DAG v0.2 (`b9fe0cc7...`), current Task Pack and L3 remain authoritative.
- Immutable DAG v0.1 `### T-009` (blob `4f358ba2...`) is the normative concern; bounded L3.

## Required result
Wire v4.9 JIT materialization to the v4.3 Task DAG Governance WITHOUT turning execution-container bookkeeping into silent topology mutation:
1. `references/JIT_DAG_MUTATION_GOVERNANCE_V49_REFERENCE.md` — the deterministic classification: phase/container bookkeeping (NOT semantic mutation) vs semantic DAG mutation; routing for ADD / ADD_DEPENDENCY / REMOVE_DEPENDENCY / split / merge / supersede / defer; mutation-currentness and native Issue Dependency requirements for v4.9 runtime-originated proposals (bound to the v4.3 governance owner by exact refs; textual dependency lists cannot substitute for native graph facts).
2. `scripts/test_v49_jit_dag_governance.py` — deterministic classification tests: every mutation class routes exactly per the reference; bookkeeping never mutates semantic topology; runtime-originated semantic proposals require mutation record + native dependency hydration; Product L + L2 JIT/DAG negatives executable.
3. `fixtures/jit-dag-governance/**` — mutation scenario fixtures.

## Hard boundaries
- Native Task dependency semantics remain canonical (Frozen DAG v0.2); no second governance lifecycle; the v4.3 mutation-record owner stays canonical (cite, do not copy).
- No Product/L2/DAG mutation; frozen blobs resolve unchanged at candidate.

## Mutation authority
Only the three Builder write-set paths in MANIFEST plus the six immutable `.agent/execution/T-009/**` planning files.
