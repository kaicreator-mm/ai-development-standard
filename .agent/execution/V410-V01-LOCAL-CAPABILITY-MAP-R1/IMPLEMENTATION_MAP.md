# V410-V01-LOCAL-CAPABILITY-MAP-R1 Implementation Map

Exact baseline: `30334e8c7b90a327f8597b86c88c785b98df07f7` (= `origin/version/v4.10.0` tip).
Dependency state: `CANDIDATE_NOT_READY` (T04B/T05B/T06A-T08A pending).

## What this unit added

Validator-side preparation only, inside the allowed write set:

- `.agent/execution/V410-V01-LOCAL-CAPABILITY-MAP-R1/` — contract, manifest, capability
  map, test matrix, failure matrix, this map, review checklist.
- `scripts/test_v410_v01_capability_map.py` — map-integrity verifier (stdlib only, no
  network; git subprocess for HEAD identity only).

No pre-existing file was modified. V01's implementation write set remains NONE.

## Capability anchors read from the exact tree

Validation contract: `docs/implementation/4.10.0/V410_V01_VALIDATION_CONTRACT.md` @ `30334e8`.
Frozen refined DAG authority: `docs/implementation/4.10.0/REFINED_TASK_DAG_FREEZE_R1.md`
(frozen edges incl. `V410-T08A -> V410-V01`).
Task Pack authority: `docs/implementation/4.10.0/TASK_PACKS_R1.md`.
Product authority: `docs/implementation/4.10.0/PRODUCT_FREEZE.md`
(`ADS_CORE_FEATURE_FREEZE_ELIGIBLE` Product-only; R5/R8/R9/R10 subordinate lines 55-58).
Acceptance authority: `docs/implementation/4.10.0/PRD.md` §19 (release blockers @ §19.3).
Execution Pack authority: `standards/EXECUTION_PACK_STANDARD.md`; exercised exemplar pack
`.agent/execution/V410-T05A-R3/` (exact-base manifest + currentness failure class).

## Result shape

15/15 contract subjects mapped: 12 fully AVAILABLE locally, 3 AVAILABLE locally with
host part BLOCKED (subjects 4, 5, 13 — owner GitHub platform), 0 fully BLOCKED.
See `CAPABILITY_MAP.md` for per-subject commands, limitations, and re-read obligations.
