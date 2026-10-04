# T-014 Implementation Map

Builder writes only:

1. `scripts/test_v48_integration_closure.py`
   - deterministic integrated conformance oracles (see TEST_MATRIX.yaml);
   - machine-readable assertions, not structural string matches where behavior exists;
   - reads the live repository state at the candidate itself (registry/manifest/owners), no network.

2. `docs/implementation/4.8.0/closure/INTEGRATED_REGRESSION_EVIDENCE.json`
   - one row per executed command: exact command string, exit code, test/suite counts, executed at exact base SHA;
   - must cover `python -B scripts/verify_standard.py` and every pinned `run:` command from `.github/workflows/verify-standard.yml` at this base;
   - any command that cannot run on this host is recorded `NOT_RUN` with the exact reason — no substitution.

3. `docs/implementation/4.8.0/closure/CLOSURE_INPUTS.md`
   - integrated v4.8 semantics inventory: the three new machine families with their Frozen L2/Product refs; Interchange reuse; owner-uniqueness map v4.1–v4.8;
   - evidence index binding every acceptance oracle to its proof (test id + execution evidence ref);
   - carry-forwards: unresolved adverse findings (incl. T-013 #763 P3-01), routed owner defects, `NOT_RUN|BLOCKED` items with the exact missing capability;
   - explicit statement: these are closure INPUTS; Version Closure verdict authority remains with the later closure gates.

Read-only starting points:
- Frozen authorities at the exact base: `docs/implementation/4.8.0/PRD.md`, `L2_ARCHITECTURE_EVIDENCE.md`, `TASK_DAG.md`, `L3_REFERENCE_PACKS.md`, task packs;
- per-Task evidence already merged on the baseline (dogfood reports, L3 evidence docs, `.agent/execution/T-*/**`);
- prior closure structure reference (historical only): v4.3 closure inputs pattern under `docs/implementation/4.3.0/` if present.
