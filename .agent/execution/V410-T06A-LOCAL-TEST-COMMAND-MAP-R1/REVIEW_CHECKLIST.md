# V410-T06A Local Test Command Map R1 — Review Checklist

Review target: branch `task/v4.10.0-v410-t06a-local-test-command-map-r1` @ `eea3e69be5ac3e9c1a78f19e9bdf243ad9c58601` + this unit's add-only files.

## Provenance

- [ ] `EXECUTION_CONTRACT.md` exists and records base `eea3e69be5ac3e9c1a78f19e9bdf243ad9c58601`, Task Pack `TASK_PACKS_R1.md#V410-T06A`, branch, parent issue `#860`.
- [ ] Contract claim precedes all other unit artifacts (git history / file timestamps consistent with contract-first ordering).
- [ ] `MANIFEST.yaml` binds the same base/branch/parent issue and lists the six core artifacts.

## Scope discipline

- [ ] Only two write locations touched: `.agent/execution/V410-T06A-LOCAL-TEST-COMMAND-MAP-R1/` and `scripts/test_v410_t06a_test_command_map.py`.
- [ ] No pre-existing file mutated (`git diff` against base shows additions only).
- [ ] Map creates no second owner registry and rewrites no upstream owner semantics.

## Content correctness (spot-check against base tree)

- [ ] Every command row in `TEST_COMMAND_MAP.md` exists at base under `scripts/`.
- [ ] Surface citations exist: `standard-manifest.json`, `standards/REFERENCE_CONVENTION_STANDARD.md`, `references/REFERENCE_CONVENTION_REFERENCE.md`, `references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md`, `references/PROGRESSIVE_DISCLOSURE_ROUTING.md`, `references/STATE_DIMENSION_REGISTRY_REFERENCE.md`, `registries/state-dimensions-v1.json`.
- [ ] Negative stale-owner coverage is real: `test_v47_compatibility_aliases.py` contains silent-removal, unindexed-legacy-alias, unknown-alias, and alias-not-owner rows.
- [ ] CLASS_1's three machine-checked key lists (`top_level_keys`, `section_keys`, `semantic_authority_entry_fields`) match `standard-manifest.json` exactly, and the map does not attribute state-dimension metadata to the manifest (it is the separate registry `registries/state-dimensions-v1.json`). The R1 repair note in `IMPLEMENTATION_MAP.md` records the earlier misattribution.
- [ ] Gap dispositions are explicit (five rows); none silently drops a surface.
- [ ] `resolve_standard_read_set.py` is not cited as a standalone gate command.

## Gates

- [ ] `python scripts/test_v410_t06a_test_command_map.py` PASS at base.
- [ ] All 12 matrix commands PASS at base (re-run any row you doubt; drift supersedes the observed column).
- [ ] Map does not claim T06A acceptance, concern Validation, or Independent Review PASS.
