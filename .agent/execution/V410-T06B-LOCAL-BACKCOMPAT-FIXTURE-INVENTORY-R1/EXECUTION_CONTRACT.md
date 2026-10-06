# V410-T06B LOCAL Execution Contract — Backcompat Fixture Inventory (R1)

Exact base: `30334e8c7b90a327f8597b86c88c785b98df07f7` (= `origin/version/v4.10.0` tip; HEAD at generation).
Task Pack: `docs/implementation/4.10.0/TASK_PACKS_R1.md#V410-T06B`.
Branch: `task/v4.10.0-v410-t06b-local-backcompat-fixture-inventory-r1`.
Execution environment: `LOCAL`.

Purpose: preparation/inventory unit. Produce a complete, verified inventory of every backward-compatibility, golden, and conformance fixture surface that the V410-T06B central projection & machine-conformance wiring may touch, so the subsequent T06B implementation unit (gated on T06A) knows exactly which pins it must not break. This unit performs NO semantic wiring, NO owner mutation, and NO fixture change.

## Allowed write set

1. `.agent/execution/V410-T06B-LOCAL-BACKCOMPAT-FIXTURE-INVENTORY-R1/` — new execution pack files (six core artifacts plus `BACKCOMPAT_FIXTURE_INVENTORY.md`).
2. `scripts/test_v410_t06b_backcompat_fixture_inventory.py` — one new verification script.

Nothing else. No pre-existing file may be modified.

## Forbidden scope

- No central semantic rewrite and no projection wiring in this unit (that is the gated T06B implementation unit's job, after T06A).
- No second registry, no second golden index, no parallel discovery surface.
- No blanket touch-every-file migration, including of `.agent/execution/_legacy` or historical packs.
- No mutation of any fixture, standard, schema, template, suite, or source file.

## Provenance

Builder claim, recorded in this contract: this unit was dispatched by the user (controller) as LOCAL preparation unit `V410-T06B-LOCAL-BACKCOMPAT-FIXTURE-INVENTORY-R1` of the v4.10.0 campaign (parent Issue #861) against the exact pack `docs/implementation/4.10.0/TASK_PACKS_R1.md#V410-T06B` and exact base `30334e8c7b90a327f8597b86c88c785b98df07f7`, under `agent_freedom: F1_BOUNDED_IMPLEMENTATION`, with the write set and forbidden scope above. Dispatch timestamp: 2026-10-06T09:11:15+06:30. Claim authority derives solely from this user dispatch; no prior R-unit evidence is transferred.

Sequencing disclosure: this contract is durable evidence of the claim; in this LOCAL single-session dispatch the claim text was finalized alongside the additive artifacts and independently re-validated by `scripts/test_v410_t06b_backcompat_fixture_inventory.py` (HEAD binding to the exact base, fixture existence, producer entrypoint existence, kind counts). The T06B implementation unit MUST treat this pack as non-authoritative input and re-verify currentness before any mutation.

## Dependency / currentness state

- Integrated v4.10 predecessors (exact SHAs): T01A@`359e4a9`, T01B@`3d73530`, T02A@`60a4995`, T02B-R2@`9e34e96`, T03A@`788473b`, T03B@`cb6e290`, T04A@`be03b44`, T05A-R3@`a7247fd` (full SHAs in MANIFEST.yaml).
- T06A and its LOCAL snapshot unit are preparation-parallel to this unit; T06B execution admission for semantic wiring remains gated on T06A per TASK_PACKS dependencies.
- V410-T04B and V410-T05B are pending at generation time; this inventory does not depend on them.
- Base binding verified by the verification script output recorded in this pack's TEST_MATRIX evidence path.
