# V410-T06A Local Test Command Map R1 — Implementation Map

Unit: `V410-T06A-LOCAL-TEST-COMMAND-MAP-R1`
Base: `eea3e69be5ac3e9c1a78f19e9bdf243ad9c58601`
Mode: add-only preparation; no pre-existing file mutated.

## Steps performed (in order)

1. **Claim before mutation** — `EXECUTION_CONTRACT.md` written first in the unit, recording exact base, Task Pack, branch, parent issue #860, allowed write set, forbidden scope, and gates.
2. **Surface inventory** — enumerated T06A-owned surface classes from the Task Pack allowed write set against the base tree:
   - `standard-manifest.json` (sections incl. `discovery_standards`/`registries`/`compatibility_entries`; `semantic_authorities` metadata, 11 entries). State-dimension metadata is a separate registry, `registries/state-dimensions-v1.json`, referenced by the manifest but not carried in it.
   - Semantic-authority/discovery: `standards/REFERENCE_CONVENTION_STANDARD.md`, `schemas/authority-applicability-entry-v1.schema.json`, `references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md`, `references/PROGRESSIVE_DISCLOSURE_ROUTING.md`.
   - Owner-discovery references/registries: `references/REFERENCE_CONVENTION_REFERENCE.md`, `references/STATE_DIMENSION_REGISTRY_REFERENCE.md`, `registries/state-dimensions-v1.json`, `schemas/state-dimension-registry-v1.schema.json`.
   - Legacy classification: manifest `compatibility_entries` (`standards/GITHUB_WORKFLOW.md`, `standards/VERSION_INTEGRATION_WORKFLOW.md`), `.agent/execution/T-*` legacy packs; `_legacy/` confirmed absent at base.
3. **Command inventory + live verification** — for each surface class, selected the smallest checked-in deterministic commands and executed every one at base. All 12 gate commands PASS; `resolve_standard_read_set.py` confirmed import-only (raw exit non-zero by design) and excluded from gate commands.
4. **Gap dispositions** — recorded five explicit dispositions in `TEST_COMMAND_MAP.md` (no T06A successor suite at base; sibling owner-snapshot pack unintegrated; base drift vs sibling units recorded as `CURRENTNESS_DRIFT`; `_legacy/` absent on this line; T06A admission still gated).
5. **Verifier** — added `scripts/test_v410_t06a_test_command_map.py` (only new file outside the pack directory); it re-checks pack inventory, map citation integrity, entrypoint existence, surface coverage, and negative stale-owner coverage.

## File ledger

| File | Status |
|---|---|
| `.agent/execution/V410-T06A-LOCAL-TEST-COMMAND-MAP-R1/EXECUTION_CONTRACT.md` | new (first write of unit) |
| `.agent/execution/V410-T06A-LOCAL-TEST-COMMAND-MAP-R1/MANIFEST.yaml` | new |
| `.agent/execution/V410-T06A-LOCAL-TEST-COMMAND-MAP-R1/TEST_MATRIX.yaml` | new |
| `.agent/execution/V410-T06A-LOCAL-TEST-COMMAND-MAP-R1/FAILURE_MATRIX.yaml` | new |
| `.agent/execution/V410-T06A-LOCAL-TEST-COMMAND-MAP-R1/TEST_COMMAND_MAP.md` | new (primary deliverable) |
| `.agent/execution/V410-T06A-LOCAL-TEST-COMMAND-MAP-R1/IMPLEMENTATION_MAP.md` | new (this file) |
| `.agent/execution/V410-T06A-LOCAL-TEST-COMMAND-MAP-R1/REVIEW_CHECKLIST.md` | new |
| `scripts/test_v410_t06a_test_command_map.py` | new (sole new script) |

No pre-existing file modified.

## R1 repair (post-commit)

After the R1 pack commit, an independent re-read of the base tree against the map found one material inaccuracy: `TEST_COMMAND_MAP.md` CLASS_1 and step 2 above attributed `state_dimensions` metadata to `standard-manifest.json`, which carries no such key (its top-level keys are `schema_version`, `description`, `sections`, `semantic_authorities`). The state dimensions are a separate registry at `registries/state-dimensions-v1.json`, referenced by the manifest only through `sections.registries`.

Repair applied (same allowed write set; still add-only against base):

1. CLASS_1 now states the manifest key surface as three machine-checked lists instead of prose, so the class of drift that caused this error fails loudly rather than silently.
2. A new verifier test, `test_class1_manifest_key_surface_matches_manifest`, re-derives those lists from `standard-manifest.json` and fails on mismatch.
3. Gap disposition 1 was reworded: the base tree has no `scripts/test_v410_t06a_*.py`, but this unit's own verifier matches that glob on the candidate, which the earlier wording left ambiguous.

No other claim in the map was found inaccurate: all 12 matrix commands re-ran PASS, all cited surface paths exist, `resolve_standard_read_set.py` exits non-zero when run raw (import-only), and the negative stale-owner probes are present in `test_v47_compatibility_aliases.py`.

## Out of scope (per contract)

No T06A source mutation; no second owner registry; no rewrite of upstream owner Tasks; no deletion of historical evidence; no claim of T06A acceptance gates; no opportunistic repair of recorded gaps.
