# T-006 JIT Execution Contract

## Exact authority
- Issue: #725 / T-006 Task Learning Same-Family Successor.
- Base: `version/v4.9.0@df94641e6082dc7a2988e73eafdffd3bf42668b9`, tree `a8c86675d003d397636304f3441a14385660f9c5` (post lineage-composition PR #792).
- Frozen Product (`a8ec7030...`), Frozen L2 (`bd41ea01...`), Frozen Task DAG v0.2 (`b9fe0cc7...`), current Task Pack and L3 remain authoritative.
- Immutable DAG v0.1 `### T-006` (blob `4f358ba2...`) is the normative concern definition, composed with Frozen DAG v0.2 admission rules.
- Native blockers zero; LG42_COMPAT + LG48_LEARNING current at base (v4.8 Task Learning v1 owner surface present).

## Required result
Add v4.9 recurrence/friction fields ONLY through a versioned same-family successor of the existing Task Learning v1 family, and only as far as needed:
- successor schema `task-learning-v2` with same-family compatibility to v1 (v1 instances remain valid historical evidence; no silent re-interpretation);
- optional `execution_friction_class`, recurrence refs, optional root-cause relation, prevention refs and recurrence-audit refs;
- explicit orthogonality to the existing `friction_classification` (no redefinition, no overlap claim);
- truthful machine-checkable compatibility evidence (v1 blob identities, INCOMPATIBLE dimensions fail-closed) following the established compatibility-record pattern;
- routing/authority negatives: learning evidence cannot become authority, cannot create automatic ADS mutation, cannot replace evidence gates.

## Hard boundaries
- No learning DB, no new intake lifecycle, no automatic ADS mutation; no workflow state.
- Read-only owner refs (v1 schema, owner standard) unmutated; frozen blobs resolve unchanged at candidate.
- Missing/unavailable evidence => `NOT_RUN|BLOCKED`, never synthetic PASS.

## Mutation authority
Only the four Builder write-set paths in MANIFEST plus the six immutable `.agent/execution/T-006/**` planning files. Everything else read-only.
