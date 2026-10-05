# T-007 JIT Execution Contract

## Exact authority
- Issue: #726 / T-007 Execution Architecture Proportional Orchestration Core.
- Base: `version/v4.9.0@1fa88bc1a54970af79ce506a056c2ae5e3203be8`, tree `0a261a6227676a046e532f20f497c576f25a5916`.
- Frozen Product (`a8ec7030...`), Frozen L2 (`bd41ea01...`), Frozen Task DAG v0.2 (`b9fe0cc7...`), current Task Pack and L3 remain authoritative.
- Immutable DAG v0.1 `### T-007` (blob `4f358ba2...`) is the normative concern definition, composed with Frozen DAG v0.2 admission rules.
- This is the SINGLE v4.9 semantic owner lane for `standards/EXECUTION_ARCHITECTURE_STANDARD.md`. Risk: critical/high. L3: high-capability semantic kernel required.
- Native blockers zero (T-002/T-003/T-004/T-005 all DONE); LG42_COMPAT + LG47_REGISTRY + LG48_EXEC current at base.

## Required result
Extend the execution architecture standard with the v4.9 proportional orchestration core — exactly the DAG v0.1 `### T-007` owned semantics, nothing more:
1. Assurance Plan currentness consumption/recheck at Dispatch, Claim, merge and other architecture-owned transitions (consumes the T-002 Assurance Plan v2 currentness contract);
2. legal JIT phase predicate (dependencies + lineage predicates + pack/admission checks; READY only when all pass; deterministic recompute on currentness drift — drift => recompute, never stale-latch);
3. `WAITING_LINEAGE` derived non-dispatch projection (consumes the T-003 registry semantics: derived, authority-free, never a workflow state);
4. Role Profile hard-predicate wiring into v4.8 eligibility (hard filters BEFORE ranking; consumes the T-004 Role Execution Profile contract);
5. unresolved adverse-finding carry-forward/reducer behavior while preserving Adversarial Review aggregation ownership (no review shopping; aggregation stays with the review owner);
6. acceptance covers Frozen Product acceptance items E/F/G/K/L/M/N and the L2 currentness/JIT/adverse negatives — read them from the frozen docs and bind each to machine-checkable oracles.

## Hard boundaries
- No second scheduler/claim lifecycle or runtime authority store; no workflow state; no parallel owner/family creation.
- WAITING_LINEAGE stays derived/non-dispatch (registry F11-F19 semantics); source-authority disagreement or stale refs => BLOCKED, never last-writer-wins.
- The standard edit is EXTENSIVE-but-additive in the v4.9 voice: new sections compose with v4.0–v4.8 content; historical sections untouched; no weakening of v4.8 §27 hard-eligibility or any inherited invariant.
- Every semantic claim binds an exact ref (owner standard sections, schema fields, registry dimensions); unavailable evidence => NOT_RUN|BLOCKED.
- No Product/L2/DAG mutation; frozen blobs resolve unchanged at candidate.

## Mutation authority
Only the four Builder write-set paths in MANIFEST plus the six immutable `.agent/execution/T-007/**` planning files. The read-only dependency refs are inputs only. Builder tests are not independent Validation.
