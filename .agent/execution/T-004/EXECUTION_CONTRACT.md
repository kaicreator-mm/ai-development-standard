# T-004 JIT Execution Contract

## Exact authority
- Issue: #723 / T-004 Role Execution Profile v1 Contract.
- Base: `version/v4.9.0@df94641e6082dc7a2988e73eafdffd3bf42668b9`, tree `a8c86675d003d397636304f3441a14385660f9c5` (post lineage-composition PR #792).
- Frozen Product (`a8ec7030...`), Frozen L2 (`bd41ea01...`), Frozen Task DAG v0.2 (`b9fe0cc7...`), current Task Pack and L3 remain authoritative.
- Immutable DAG v0.1 `### T-004` (blob `4f358ba2...`) is the normative concern definition, composed with Frozen DAG v0.2 admission rules.
- `Role Execution Profile v1` is the ONLY new default machine family of v4.9. Native blockers zero; LG42_COMPAT + LG48_EXEC current at base.

## Required result
Implement the Role Execution Profile v1 contract: schema + fixtures + contract/negative-oracle tests + reference doc. Normalizes role requirements and source-authority projections WITHOUT stealing authority:
- normalized source-authority projection fields; source-authority conflict fail-closed rule (BLOCKED, never last-writer-wins);
- eligibility predicate refs INTO the v4.8 hard-eligibility owner (reference, not re-implementation);
- `claim_policy_ref` derives from existing v4.8 Claim rules; independence/model-routing references without stealing their authority;
- provider-neutral fields throughout; references to v4.8 capability/eligibility/Claim owners rather than copied inventories.

## Hard acceptance boundaries (immutable DAG v0.1 `### T-004`)
- Role Profile cannot prove executor capability; Agent Capability cannot grant role actions/terminal authority;
- provider/model identity cannot become normative role authority;
- stale/missing source refs fail closed (BLOCKED/WAITING_LINEAGE posture), never permissive defaults;
- no second lifecycle, no workflow state, no Product/L2/DAG/normative-owner mutation; read-only owner refs unmutated.

## Mutation authority
Only the four Builder write-set paths in MANIFEST plus the six immutable `.agent/execution/T-004/**` planning files. Everything else read-only.
