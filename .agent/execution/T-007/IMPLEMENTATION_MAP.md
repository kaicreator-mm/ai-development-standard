# T-007 Implementation Map

Builder writes only:

1. `standards/EXECUTION_ARCHITECTURE_STANDARD.md` — new v4.9 proportional-orchestration sections (see EXECUTION_CONTRACT items 1-5). Study the existing standard first (v4.0–v4.8 sections incl. §27 hard eligibility, §11 Claim, §12.1 work items): compose additively, cite the consumed owner contracts (T-002 assurance currentness, T-003 registry dimensions incl. waiting_lineage, T-004 role profile, T-005 release applicability) by exact section/field refs. Every new rule must be machine-checkable in principle (test-matrix oracles bind to it).
2. `references/PROPORTIONAL_ORCHESTRATION_REFERENCE.md` — reference: reducer state model, JIT phase predicate evaluation order, currentness recheck points (Dispatch/Claim/merge), carry-forward reducer behavior, WAITING_LINEAGE projection rules, no-review-shopping routing.
3. `scripts/test_v49_execution_core.py` — deterministic stdlib-unittest semantic kernel: reducer unit tests + JIT predicate truth tables + currentness-drift recompute + race/drift cases (deterministic simulations: concurrent claim vs drift, stale currentness latch forbidden) + carry-forward aggregation + no-review-shopping routing + owner-boundary negatives. Style references (read-only): `scripts/test_v48_execution_architecture.py`, `test_v48_scheduling_conformance.py`, `test_v49_role_execution_profile.py`.
4. `fixtures/execution-core-v49/**` — fixture instances for the kernel tests.

Read-only inputs: the five read_only_dependency_refs in MANIFEST; Frozen PRD acceptance items E/F/G/K/L/M/N; Frozen L2 currentness/JIT/adverse negatives; immutable DAG v0.1 `### T-007`; L3 T-007 section.
