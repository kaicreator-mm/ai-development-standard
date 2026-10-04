# T-002 Implementation Map

1. Re-read Frozen L2, T-002 Task Pack, L3 and current `EXECUTION_ARCHITECTURE_STANDARD.md` at exact base.
2. Define composition of logical Agent claims + existing runner/environment owner facts + derived Availability + Capability Evidence without owner duplication.
3. Make hard eligibility filters precede ranking; optimization receives ELIGIBLE candidates only.
4. Specify one safe first implementation path for composite work+resource admission, preferring existing single-writer admission.
5. Specify capacity-N and crash/reconciliation invariants.
6. Add deterministic focused test in `scripts/test_v48_execution_architecture.py` covering positive and negative oracles.
7. Run focused test plus repository verifier/protocol regressions required by the current standard.

No sibling Task semantics or extra files without explicit Controller rebind.
