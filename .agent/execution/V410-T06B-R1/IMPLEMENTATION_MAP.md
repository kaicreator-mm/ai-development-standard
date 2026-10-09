# V410-T06B R1 implementation map — ordered W1-W14 plan (normative: #861@6013678847)

Implementation follows the six-stage order in EXECUTION_CONTRACT.md. Per-file acceptance tests = TEST_MAP in the write-set plan terminal, folded into TEST_MATRIX.yaml. Key bindings and decisions recorded at this JIT:

## Stage 0 census results (executed read-only at `ab8339f`, recorded in MANIFEST `stage0_census`)

- `schemas/dispatch.schema.json`: no `execution_environment` (additive W1); `execution_profile` enum = the 5 profiles; profile↔role allOf couplings exist (byte-stable A11); `additionalProperties: true`.
- `schemas/local-agent-handoff.schema.json`: already carries `execution_environment` (hazard-1) — W5 dispositions it as the validation-gate environment (A12/A13 guards in W9).
- `TARGET_ENVIRONMENT`: zero occurrences at base (comments-only) — W5 alias disposition (T4).
- Owner-map convergence: T06A reference/merged; seven GAP families + registration route into W13's authorized co-evolution (case-H evidence on `task/v410-t06a-pack-rebind-r2-proposal@7c684309…`).
- Pack core-inventory ownership: `v34_rules.REQUIRED_CORE_ARTIFACTS` stays; W7 reuses; W11 regresses (I1-I6).

## Coupled-surface ledger (from #861@6016615178 — files that MUST move together or be consciously updated)

- `scripts/test_v410_owner_convergence.py`: pins manifest blob `21730a02…`, exact diff shape, and `t48.AUTHORIZED_SECTION_ADDITIONS` content — W13's authorized growth updates it in the same diff.
- `scripts/test_v48_registry_adoption.py`: `AUTHORIZED_SECTION_ADDITIONS`/registry-count guards — evolve ONLY in the W13 co-evolution; all historical invariants/negatives preserved.
- `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md`: seven `STATUS=GAP` rows — closure/update rides the same authorized change (STATUS transitions documented).
- `standard-manifest.json`: moves only inside W13 (verification registration + semantic_authorities growth for the seven families, preserving schema_version=1, 11 legacy entry_ids, aliases, inventories disjoint).

## W7 helper inventory (additive to `scripts/v34_rules.py`)

`normalize_group`, `derive_claim_key` (+serialize/reparse roundtrip), `authorize_non_default`, generation/CAS conformance helper, multi-active projection helper, lineage-ref presence check, TARGET_ENVIRONMENT agreement check, terminal-precedence reducer. `core_artifacts_complete()` reused unchanged.

## W3 JIT decision

Add the three optional named properties (`source_proposal_ref`, `canonical_admission_ref`, `scheduler_origin`) to `schemas/agent-event-v2.schema.json` explicitly (writer conformance F3/T3); no new event type (J1).

## W14 gate

Inspect local-builder/local-validator/web-reviewer bootstrap + validation-handoff queue templates post-Stage-5; touch only where wording re-couples role/environment/profile.

## T06B feedback routing (recorded, non-blocking)

`V410-T06B-WEB-POST-DRIFT-DOGFOOD-DELTA-R2` (admitted #861@6016591816): its terminal's DELTA clauses fold as additive oracle cases; the Builder MAY consume them if published before Stage 4, otherwise a follow-up additive dispatch covers the remainder (NON_BLOCKING by admission).

## T06B boundary

No T04A repair routing, no T02B causality rewrite, no Validation/Release authority, no semantic-owner standard edits beyond the two additive prose surfaces (W4/W5), no historical event migration.
