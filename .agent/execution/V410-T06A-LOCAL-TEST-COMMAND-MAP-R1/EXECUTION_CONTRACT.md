# V410-T06A — Local Test Command Map R1 Execution Contract

Exact base: `eea3e69be5ac3e9c1a78f19e9bdf243ad9c58601` (`origin/version/v4.10.0` tip at claim time; HEAD of this worktree verified equal at contract time).
Task Pack: `docs/implementation/4.10.0/TASK_PACKS_R1.md § V410-T06A` (owner convergence inventory / discovery / legacy classification).
Parent issue: `#860`.
Branch: `task/v4.10.0-v410-t06a-local-test-command-map-r1`.
Worktree: `D:\xDev\ai-development-standard\v410-t06a-local-test-command-map-r1`.
Execution environment: `LOCAL` (preparation unit; Fresh Review on WEB per Task Pack review policy).
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`.

Purpose: current-state test command map for the V410-T06A owner-convergence concern. The Task Pack requires gates of "manifest/reference/discovery verification + negative stale-owner tests, concern Validation, Independent Review PASS". This unit maps every T06A-owned surface class (manifest, semantic-authority/discovery, owner-discovery references, legacy classification evidence) to the smallest checked-in deterministic command(s) that verify it, records whether each command entrypoint exists and passes at base, and classifies gaps explicitly (no silent omissions, no invented waivers). This unit produces inventory and verification only; it executes no T06A source mutation and creates no authority.

## Admission timing

Preparation only. T06A execution admission stays gated by its Task Pack dependencies; this pack is preparation input. Notably T04B is now integrated at this base (merge `eea3e69`, PR #918) while T05B was not a DAG dependency outstanding at claim time of sibling units; the map records current integration facts at base and does not claim dependency completion for T06A execution.

## Allowed write set

New files only under:

1. `.agent/execution/V410-T06A-LOCAL-TEST-COMMAND-MAP-R1/` (execution pack core: `MANIFEST.yaml`, `EXECUTION_CONTRACT.md`, `TEST_MATRIX.yaml`, `FAILURE_MATRIX.yaml`, `IMPLEMENTATION_MAP.md`, `REVIEW_CHECKLIST.md`, plus primary deliverable `TEST_COMMAND_MAP.md`).
2. `scripts/test_v410_t06a_test_command_map.py` — deterministic verifier for this unit.

## Forbidden scope

No mutation of any pre-existing file (including `standard-manifest.json`, `standards/`, `schemas/`, `scripts/` other than the one new verifier, `docs/implementation/4.10.0/*`, `_legacy/*`). No second owner registry. No semantic rewrite of upstream owner Tasks. No deletion/rewrite of historical evidence. No claim that this preparation unit satisfies T06A acceptance gates. No opportunistic repair: a material residual gap is recorded in the map with an explicit disposition, not fixed here.

## Provenance

Builder claim: this unit was dispatched by the user (controller) as LOCAL preparation unit `V410-T06A-LOCAL-TEST-COMMAND-MAP-R1` against the exact Task Pack `docs/implementation/4.10.0/TASK_PACKS_R1.md#V410-T06A` and exact base `eea3e69be5ac3e9c1a78f19e9bdf243ad9c58601`, on branch `task/v4.10.0-v410-t06a-local-test-command-map-r1`, parent issue `#860`, worktree `D:\xDev\ai-development-standard\v410-t06a-local-test-command-map-r1`. This contract is written BEFORE any other file mutation in this unit and is the durable record of that claim.

## Gates

This unit's gate is `python scripts/test_v410_t06a_test_command_map.py` (must PASS at base). The verifier checks: pack core inventory present and self-consistent; every command entrypoint cited in `TEST_COMMAND_MAP.md` exists at base; every cited owner/surface path exists at base; map covers the four T06A surface classes; no cited command is silently non-deterministic (each maps to a checked-in script or documented standard command); negative/stale-owner test coverage is present in the map where the Task Pack requires it. T06A's own acceptance gates (concern Validation, Independent Review PASS) are NOT claimed by this unit.
