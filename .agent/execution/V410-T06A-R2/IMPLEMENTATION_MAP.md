# V410-T06A R2 implementation map — two source surfaces + zero manifest delta, bound to eea3e69

## Surface A — standard-manifest.json: NO CHANGE (governed resolution, not an omission)

R1 prescribed additive `semantic_authorities` rows + registration of the new reference/test. All three manifest mutations are machine-blocked by carried v4.8 frozen-inventory conformance guards that this task's own TEST_MATRIX requires to PASS unmodified (reproduction + outputs: `#860@6013810495`):

- additive row → `test_v48_registry_adoption.semantic_registry_problems` exact-count guard ("carried + exactly three new");
- `sections.references` / `sections.verification` registration → `test_v48_registry_adoption.section_conformance_problems` exact-set guard ("unauthorized additions").

Resolution adopted (R1 terminal Option A): **zero manifest delta**. Frozen L2 #842 §3 explicitly authorizes v4.10 to extend the registry when a material owner is missing, but the mechanical mechanism — evolving the frozen-inventory guard — is T06B/#861 conformance-wiring territory; a builder self-amendment of the guarding contract is the exact NO_GREEN_BY_DELETION anti-pattern. The discovery gap is therefore **recorded, not closed**: the convergence reference carries a per-family registry row with `STATUS=GAP`, `ACTION=STOP_FOR_DISPOSITION`, `ROUTED_TO=T06B(#861)` and the guard evidence. `standard-manifest.json` blob must stay `21730a0251e35e13591d2c84de1c66d6ab2c2408`; the focused test asserts this by blob identity.

## Surface B — references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md (new, non-authoritative, unregistered)

- L2 §5.1-shaped matrix with all columns CONCERN / CANONICAL_OWNER / PROJECTION_SURFACES / MACHINE_CONTRACTS / COMPATIBILITY_ALIASES / LEGACY_SURFACES / STATUS / ACTION / EVIDENCE_REFS; every row carries exact-SHA evidence refs to the base blobs in MANIFEST.yaml `owner_blobs`.
- Covers the v4.10 material concerns from Frozen L2 §3, including the seven families with no current discovery row (task decomposition, task-DAG governance, execution pack, implementation quality, interface compatibility, project adoption, reference convention) — each with its `STATUS=GAP` registry row, owner path, and the routed action.
- Legacy classification table (dispositions rebound at the R1 final rebind, still exact at `eea3e69`): `CURRENT_CARRIED_FORWARD` × 7 (`AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE@59fd5f84…`, `COMPATIBILITY_ALIAS_CONFORMANCE@c7009868…`, `V48_REGISTRY_ADOPTION_REFERENCE@375ac48e…`, `test_v47_authority_registry@731e3fd4…`, `test_v47_compatibility_aliases@80d9f483…`, `test_v48_registry_adoption@55f78fd9…`, `test_v47_reference_conventions@bf6888bd…`); `COMPATIBILITY_ONLY` one-hop aliases × 2 (`GITHUB_WORKFLOW@a96d9c18…`, `VERSION_INTEGRATION_WORKFLOW@60e2bdee…`).
- Explicit declarations: `authority_effect=NONE`, `gate_effect=NONE`, `mutation_authorized=false`; discovery/evidence only, never required at runtime; no resolver, no runtime contract, no precedence layer, no lifecycle, no service.
- **Not registered in the manifest** (blocked; see Surface A). Discoverability trail: repo path + this pack + the focused test that reads it + the PR/issue record. `DISCOVERY_REGISTRATION=BLOCKED_BY_V48_FROZEN_INVENTORY_GUARD` is stated in the reference itself.

## Surface C — scripts/test_v410_owner_convergence.py (new focused regression, unregistered; executes directly)

- Imports `resolve_registry` / `RegistryError` from `test_v47_authority_registry.py` and `semantic_registry_problems` / `section_conformance_problems` from `test_v48_registry_adoption.py` — reuse, never weaker reimplementation; executes the real merged manifest/checkout, never a fixture copy.
- Positive: P1 unique-owner + order-permutation invariance; P2 coverage-gap truthfulness (zero rows added AND seven families documented with GAP rows in the reference); P3 manifest invariants incl. manifest blob-identity `21730a02…` zero-delta proof + carried guard functions on the real manifest; P4 both aliases one-hop non-owner; P6/P7 legacy dispositions present, historical blobs pinned; P8 fresh-observer reconstructibility shape (R1–R12 concern tokens present); P9 diff-shape (candidate touches only the pack + the two source surfaces).
- Negative: N1 competing owner both orders; N2 broken targets (missing owner, alias promotion, alias double-claim, path-escape); N3 explicit stale/historical-owner rejection mutant (`references/V48_REGISTRY_ADOPTION_REFERENCE.md` as owner is rejected; currentness binds `eea3e69`; T04B R3 `e03beedd` marked HISTORICAL_ONLY in the reference, no transfer); N4 gap discipline (`STOP_FOR_DISPOSITION` recorded and the seven concerns genuinely absent from the registry); N5/N6 non-authority declarations + no-resolver/no-supersession negatives; N7 deletion mutants (alias removed from inventory; manifest with an un-enumerated addition still fails the carried guard).

## R1 metadata correction (already applied, same branch)

`.agent/execution/V410-T06A-R1/MANIFEST.yaml`: `dependency_completion` → wire format `<task-id>@<40-hex>`; prose provenance moved to `dependency_notes`; truthful `generated_at`; `material_paths` added. Re-read back: `classify_pack_staleness == PACK_CURRENT` (`#860@6013793088` NEXT satisfied; new blob published).

## T06B boundary

schemas/agent-event-v2, review-finding-v1, review-aggregation-v1, templates, prompts, checklists, golden, verifier/CI wiring, execution-environment WEB|LOCAL refinement = #861. The registry-growth/frozen-inventory-guard evolution question is routed to #861 as the conformance-wiring owner. Any discovered stale projection is recorded as `ACTION=REWIRE_PROJECTION`, routed, not fixed here.
