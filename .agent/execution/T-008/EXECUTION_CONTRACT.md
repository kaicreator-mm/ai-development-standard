# T-008 JIT Execution Contract

## Exact authority
- Issue: #727 / T-008 Work Item / Execution Pack / Dispatch Reference Wiring.
- Base: `version/v4.9.0@f4fe88542de9d3f5376498e62778e2353391bc57`, tree `82ff224731e854079bdbd40a12eeffe00186b62c`.
- Frozen Product (`a8ec7030...`), Frozen L2 (`bd41ea01...`), Frozen Task DAG v0.2 (`b9fe0cc7...`), current Task Pack and L3 remain authoritative.
- Immutable DAG v0.1 `### T-008` (blob `4f358ba2...`) is the normative concern; bounded L3; backward-compatible refs ONLY.

## Required result
Wire ONLY the refs required to carry Assurance Plan currentness, Role Profile identity, JIT phase and selector-independence/currentness identity through the EXISTING work-item / execution-pack / dispatch contract surfaces:
1. `schemas/dispatch.schema.json`: add OPTIONAL backward-compatible reference fields (e.g. `assurance_currentness_ref`, `role_profile_ref`, `jit_phase_ref` — names may differ if the schema's established style suggests better) that bind a dispatch instance to its currentness/identity artifacts; REQUIRED fields or breaking changes FORBIDDEN (v1 instances must remain valid).
2. `references/EXECUTION_CONTRACT_REFS_V49_COMPATIBILITY.json`: machine-checkable compatibility record (T-002 pattern): baseline = dispatch schema blob at base; per-dimension COMPATIBLE/INCOMPATIBLE with evidence; material-change declaration.
3. `references/EXECUTION_CONTRACT_REFS_V49_REFERENCE.md`: field semantics, claim-time/currentness reference consistency rules, non-goals.
4. `scripts/test_v49_execution_contract_refs.py`: deterministic stdlib-unittest — schema compat (v1 instances still valid; new optional refs populate/consume correctly), claim-binding consistency (refs resolve-or-fail-closed; stale ref cannot pass currentness), no duplicate Task scope/Claim authority/gate truth introduced.

## Hard boundaries
- Must not duplicate Task scope, Claim authority or gate truth; refs are references only.
- No breaking schema change (v1 compatibility mandatory); no normative standard edit; read-only dependency surfaces unmutated.
- No Product/L2/DAG mutation; frozen blobs resolve unchanged at candidate.

## Mutation authority
Only the four Builder write-set paths in MANIFEST plus the six immutable `.agent/execution/T-008/**` planning files.
