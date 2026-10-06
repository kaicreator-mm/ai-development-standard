# V410-T06A — Local Test Command Map (R1)

Preparation unit: `V410-T06A-LOCAL-TEST-COMMAND-MAP-R1`
Parent issue: `#860` (V410-T06A — Owner convergence inventory / discovery / legacy classification)
Task Pack: `docs/implementation/4.10.0/TASK_PACKS_R1.md § V410-T06A`
Repository: `kaicreator-mm/ai-development-standard`
Version: `v4.10.0`
Preparation base SHA: `eea3e69be5ac3e9c1a78f19e9bdf243ad9c58601` (`origin/version/v4.10.0` tip at claim time; T04B R3/R4 integrated via PR #918 at this base)
Branch: `task/v4.10.0-v410-t06a-local-test-command-map-r1`
Mode: `NO_SOURCE_CHANGE` preparation. Every command below was executed for entrypoint-existence and current PASS verification at base; this unit mutates nothing pre-existing and claims no T06A acceptance gate.

## What this map is for

The T06A Task Pack requires gates of "manifest/reference/discovery verification + negative stale-owner tests, concern Validation, Independent Review PASS", with write ownership over `standard-manifest.json`, semantic-authority/discovery surfaces, owner-discovery references, and legacy classification evidence. This map records, for each T06A-owned surface class, the smallest checked-in deterministic command set that verifies it today, each command's observed state at base, and explicit gap dispositions. It is preparation input for T06A execution; it is not T06A execution and not a gate PASS.

## Surface classes → verification commands

### CLASS_1 — Central manifest (`standard-manifest.json`)

Owner of the central manifest/discovery write surface per Task Pack. Contains: `sections` (authority / normative_standards / compatibility_entries / templates / checklists / prompts / machine_contracts / profiles / references / verification / **discovery_standards** / **registries**), `semantic_authorities` metadata (11 entries, each with exactly one `canonical_owner_ref` and optional `compatibility_alias_refs`), and `state_dimensions` metadata.

- `python scripts/verify_standard.py` — manifest ↔ disk inventory verification incl. code-owned bootstrap set (fails if a listed file is missing or an unlisted file shadows; observed PASS at base: 220 manifest files, 41 bootstrap-required files).
- `python scripts/test_verify_standard.py` — negative/self tests for the manifest verifier (observed PASS).
- `python scripts/test_protocol_schemas.py` — schema conformance for all checked-in schemas incl. `authority-applicability-entry-v1` and `state-dimension-registry-v1` (observed PASS).

### CLASS_2 — Semantic-authority / discovery surfaces

- `standards/REFERENCE_CONVENTION_STANDARD.md` (sole `discovery_standards` manifest entry):
  - `python scripts/test_v47_reference_conventions.py` — exact-subject vs expected-base semantics, authority_ref ≠ capability_ref, evidence transfer prohibitions (observed PASS).
- `schemas/authority-applicability-entry-v1.schema.json` + `references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md`:
  - `python scripts/test_v47_authority_registry.py` — registry resolution, competing-owners fail-closed, duplicate/missing owner fail, alias chain/cycle fail, registry grants no mutation/merge/release authority (observed PASS).
  - `python scripts/test_v47_convergence_metadata_contracts.py` — authority entries are discovery metadata only; applicability ≠ forced adoption; no master PASS/READY/BLOCKED vocabulary (observed PASS).
- `references/PROGRESSIVE_DISCLOSURE_ROUTING.md`:
  - `python scripts/test_v47_progressive_disclosure.py` — fresh-pin owner overrides profile/task order; stale chat and larger context never override owner; conflict rejects in both orders; unknown materiality fails closed (observed PASS).
- Library (not a standalone gate): `scripts/resolve_standard_read_set.py` derives the fail-closed read plan and exits non-zero when run raw by design; import-only from an owning controller.

### CLASS_3 — Owner-discovery references / registries

- `references/REFERENCE_CONVENTION_REFERENCE.md` — covered by `test_v47_reference_conventions.py` (asserted together with the standard).
- `registries/state-dimensions-v1.json` + `schemas/state-dimension-registry-v1.schema.json` + `references/STATE_DIMENSION_REGISTRY_REFERENCE.md`:
  - `python scripts/test_v47_state_dimension_registry.py` — every dimension owner-qualified, no global enum, eight required negatives machine-readable, schema rejects lifecycle/grant fields, conflicting owners and dangling rules fail closed (observed PASS).
- Cross-family owner uniqueness / stale-evidence rebinding:
  - `python scripts/test_v48_registry_adoption.py` — one owner per concern without authority; negative probes incl. stale evidence rebinding rejected, removed base inventory entry fails, single-byte change to carried file fails (observed PASS).
  - `python scripts/test_v48_ads_evolution_governance.py` — ADS evolution governance semantics (observed PASS).
  - `python scripts/test_execution_architecture.py` — existing execution-architecture conformance baseline (observed PASS).

### CLASS_4 — Legacy classification evidence / negative stale-owner tests

- **Negative stale-owner coverage** (the Task Pack's "negative stale-owner tests"):
  - `python scripts/test_v47_compatibility_aliases.py` — live inventory: every alias has exactly one real owner; iteration order cannot choose a winner; **silent removal from both inventory and metadata still fails**; **unindexed legacy alias fails even if the file exists**; **unknown alias fails instead of guessing an existing owner**; alias cannot be a normative owner; alias chain cycle and duplicate claim fail (observed PASS).
  - `python scripts/test_v47_authority_registry.py` (negative rows above) and `python scripts/test_v48_registry_adoption.py` (`test_ra_n08_stale_evidence_rebinding_is_rejected`) complete the stale/legacy negative surface.
- **Legacy evidence surfaces reachable at this base**:
  - `standard-manifest.json § compatibility_entries` = `standards/GITHUB_WORKFLOW.md`, `standards/VERSION_INTEGRATION_WORKFLOW.md` (explicitly non-normative compatibility entries).
  - `.agent/execution/T-001-R2 … T-017` legacy execution packs (pre-V410 pack-format lineage) — historical facts, not current authority; covered indirectly by EXECUTION_PACK_STANDARD conformance and by the v4.10 pack-format rows of the v48 suites.
  - `_legacy/` — **does not exist at this base** (present on `main` via v4.9 T015 commit `046710a`, absent from `version/v4.10.0` at `eea3e69`). Recorded as a base-tree fact, not a gap to repair here.

## Observed command matrix at base `eea3e69`

| Command | Entrypoint exists | Result at base | Surface classes |
|---|---|---|---|
| `python scripts/verify_standard.py` | yes | PASS | 1 |
| `python scripts/test_verify_standard.py` | yes | PASS | 1 |
| `python scripts/test_protocol_schemas.py` | yes | PASS | 1,2,3 |
| `python scripts/test_v47_reference_conventions.py` | yes | PASS | 2,3 |
| `python scripts/test_v47_authority_registry.py` | yes | PASS | 2,4 |
| `python scripts/test_v47_compatibility_aliases.py` | yes | PASS | 4 (negative stale-owner) |
| `python scripts/test_v47_convergence_metadata_contracts.py` | yes | PASS | 2 |
| `python scripts/test_v47_state_dimension_registry.py` | yes | PASS | 3 |
| `python scripts/test_v47_progressive_disclosure.py` | yes | PASS | 2 |
| `python scripts/test_v48_registry_adoption.py` | yes | PASS | 3,4 |
| `python scripts/test_v48_ads_evolution_governance.py` | yes | PASS | 3 |
| `python scripts/test_execution_architecture.py` | yes | PASS | 3 (baseline) |

`scripts/resolve_standard_read_set.py` — import-only library; raw execution exits non-zero by design; not a gate command.

## Gap dispositions (explicit, no silent omissions, no opportunistic repair)

1. **No T06A-dedicated successor test exists at base** (`scripts/test_v410_t06a_*.py` absent). Expected: T06A has not executed. Disposition: T06A execution (or its campaign successor) adds its focused suite under its own pack; this map does not create it.
2. **Sibling preparation pack `V410-T06A-LOCAL-OWNER-SNAPSHOT-R1` is not integrated** (its worktree holds only untracked pack files on base `30334e8`; no commit/PR). This map does not depend on it and recomputes all facts from base `eea3e69`.
3. **Base drift vs sibling units**: siblings pinned `30334e8` (T05A-R3); this unit pins `eea3e69` (adds T04B R3/R4 repair, PR #918). Any consumer of sibling-unit preparation evidence must rebind to the T06A execution subject; drift is recorded in `FAILURE_MATRIX.yaml` (`CURRENTNESS_DRIFT`), not repaired here.
4. **`_legacy/` absent on this line** (see CLASS_4). Disposition: base-tree fact; legacy classification at T06A execution time must enumerate `.agent/execution/T-*` packs and compatibility entries as the reachable legacy surface on the exact subject, and re-check whether `_legacy/` appears on the final integration subject.
5. **T06A execution admission remains gated** by the Task Pack dependency set; T04B is now integrated at this base, T05B status must be re-read at T06A claim time. This map claims no dependency completion.

## Consumption procedure (T06A execution / campaign)

1. Rebind to the exact T06A execution subject SHA/tree; re-run every command in the matrix on that subject; record per-command PASS/FAIL/BLOCKED.
2. If any entrypoint is missing on the subject, record BLOCKED — do not substitute.
3. Subject drift supersedes the "Result at base" column entirely; this map's observed results are preparation-time facts bound to `eea3e69` only.
