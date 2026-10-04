# T-014 JIT Execution Contract

## Exact authority

- Issue: #520 / T-014 Integrated Convergence / Version Closure Inputs.
- Base: `version/v4.8.0@6bfb8aecd4c7e533ae4f392dc4e58de1da71d5b4`, tree `593dd5d12890f68e3830419b07b909ccf587dc2b`.
- Frozen Product (`f26439580e00de6ed8b2e27d732a3095eb566219`), Frozen L2 (`f88c85454e80101a0fdf56050e21f11a05279841`), Frozen DAG R1 (`72dfeee93c092296004c7083b71fdd877d7f1b34`), current Task Pack (`1373438d17ca540c69d14f835d0f7252b7221b82`) and L3 (`8af06fd5bd7237b260fe478c23cb410c0e15898f`) remain authoritative.
- Native blockers are zero at admission (live re-read: all 8 dependencies CLOSED). Any base/authority drift before Builder mutation requires Controller rebind, never a silent rebaseline.

## Required result

Produce durable Version Closure INPUTS on the exact integrated baseline:

1. Run the full required integrated regression on this exact base and bind exact evidence: `python -B scripts/verify_standard.py` plus every pinned `run:` command in `.github/workflows/verify-standard.yml`, each executed individually with exact command, exit code and test counts recorded in `docs/implementation/4.8.0/closure/INTEGRATED_REGRESSION_EVIDENCE.json`.
2. Verify integrated acceptance oracles with a deterministic focused test `scripts/test_v48_integration_closure.py`:
   - exactly three new v4.8 machine families, identified from the Frozen L2/Product — never inferred from test-file counts alone;
   - Interchange owner reused, not duplicated;
   - owner uniqueness across v4.1–v4.8 (no second owner for any inherited semantic concern);
   - hard eligibility-before-ranking and composite resource atomicity retained;
   - historical compatibility / Fast Path retained;
   - dogfood claims bounded to evidence strength; no economic-savings or universal-routing inference without comparable measured evidence.
3. Write `docs/implementation/4.8.0/closure/CLOSURE_INPUTS.md`: the durable, exact-ref-bound closure input set (integrated semantics inventory, evidence index, open carry-forwards incl. T-013 P3-01 note, explicit NOT_RUN/BLOCKED items).

## Hard boundaries

- Produces closure INPUTS only. Never issues Version Closure, Release Qualification, Hidden Validation, tag/release or main-integration verdicts.
- No silent semantic repair of any owner Task: a discovered owner defect is reported in closure inputs and routed back to the owning Task — not fixed in this lane.
- No Product/L2/DAG/normative-owner mutation; frozen blobs must resolve unchanged at the candidate.
- Every claim binds an exact durable ref (SHA/blob/comment/CI run); unavailable evidence is recorded `NOT_RUN|BLOCKED`, never synthetic PASS.
- No secrets, private-project evidence or Hidden payloads.

## Mutation authority

Only the three Builder paths in MANIFEST `builder_write_set` are writable, plus the six immutable `.agent/execution/T-014/**` planning files. Everything else is read-only. Builder tests are not independent Validation; Validation and Fresh Review are separate subsequent gates on the exact candidate HEAD.
