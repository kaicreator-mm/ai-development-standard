# T-015 JIT Execution Contract

## Exact authority
- Issue: #734 / T-015 Integrated v4.9 Dogfood / Release Evidence Handoff. Risk: critical/high. L3: required integration plan.
- Base: `version/v4.9.0@a4f1debe663813712d4f740ec70c14ca6342b0ac`, tree `76e18763c525e357a14e2d21036e597b07151a91` (post-recovery recompose + all v4.9 task merges).
- Immutable DAG v0.1 `### T-015` (blob `4f358ba2...`) is the normative concern. Native blockers zero (T-011/T-012/T-013/T-014 all DONE); LG_SEQ_FULL CURRENT at base (recovery integrated per #805/#905 + recompose PR #909).

## Required result
Integrate the implementation surface and produce version-closure/release handoff EVIDENCE (never the closure/RQ verdict itself):
1. `docs/implementation/4.9.0/integration/INTEGRATION_DOGFOOD_REPORT.md` — the integrated dogfood report: predecessor-lineage exact identity check (all merged task outputs + recovered families at the exact base); representative positive/negative orchestration journeys executed from the T-007 kernel + T-012 conformance surfaces; reconciliation of normative docs/contracts/tests/registry; downstream mechanism exercise per the T-014 contract (the qualifying downstream path exercised where available/required — real external/downstream inability is BLOCKED/NOT_RUN, never guessed PASS); no unsupported generality claim for unexercised mechanisms; downstream generality remains NOT_SATISFIED if the qualifying contract is not met; all safety negatives zero for any run used as generality evidence; no stale predecessor/evidence binding laundered.
2. `docs/implementation/4.9.0/integration/RELEASE_EVIDENCE_HANDOFF.md` — the handoff: what Version Closure can truthfully consume (with NOT_RUN/BLOCKED preserved as NOT_RUN/BLOCKED, never converted to PASS); explicit statement that closure/RQ verdict authority remains with the later gates.
3. `scripts/test_v49_integrated_dogfood.py` — deterministic integrated-dogfood oracles: predecessor-lineage identity; journey execution bindings; reconciliation checks (docs/contracts/tests/registry consistency at the candidate); handoff completeness (no NOT_RUN/BLOCKED converted; no unsupported generality).

## Hard boundaries
- Produces handoff EVIDENCE only — cannot issue Version Closure or Release Qualification verdict; no tag/release; no main integration.
- No Product/L2/DAG mutation; frozen blobs resolve unchanged at candidate; no stale binding laundered.

## Mutation authority
Only the three Builder write-set paths in MANIFEST plus the six immutable `.agent/execution/T-015/**` planning files.
