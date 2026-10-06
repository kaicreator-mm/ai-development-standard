# V410-T06A R1 implementation map — three surfaces, bound to eea3e69

## Surface A — standard-manifest.json (additive discovery rows only)

Base blob `21730a0251e35e13591d2c84de1c66d6ab2c2408`, schema_version=1, 11 existing entries (all preserved byte-for-byte in place; additions appended).

Coverage gap recomputed on the exact base tree — these material v4.10 owner families (L2 §3 owner map) are normative assets with NO current discovery row:

| candidate entry_id | owner (path on base tree) | owner blob @eea3e69 |
|---|---|---|
| task-decomposition | standards/TASK_DECOMPOSITION_STANDARD.md | f355c020f07828a62ad617ffa80cb40b708ab4d4 |
| task-dag-governance | standards/TASK_DAG_GOVERNANCE_STANDARD.md | e2ecfdbf0cd79f750aff40276e46a59159465f78 |
| execution-pack | standards/EXECUTION_PACK_STANDARD.md | c7bd2e4ffb87a0ac7fabc54fd78c4eb1fae6ef0d |
| implementation-quality | standards/IMPLEMENTATION_QUALITY_STANDARD.md | 3beba2d0324d95674b7bad2ef621e2aa81c66563 |
| interface-compatibility | standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md | 266aefe32e0990c24fc8c1d6d731c4a3456fc3fc |
| project-adoption | standards/PROJECT_ADOPTION.md | aac0d4bff0ed67e6e23d89903e58732524cab024 |
| reference-convention | standards/REFERENCE_CONVENTION_STANDARD.md | ba6a95b124c1804ea4e13c5c6d058e9ade2cc905 |

Rules per entry: `semantic_concern` string must match the L2 §3 concern naming (builder verifies against #842, no invention); `canonical_owner_ref` = the existing path above; `applicability_posture` reuses an existing T01-schema posture enum value; `compatibility_alias_refs` empty unless a real one-hop alias exists (none known for these families — do not manufacture); prose/comment preserves "missing row != non-applicability". Add a row only where the concern is still not reconstructible from the post-change manifest alone; no cosmetic rows.

## Surface B — references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md (new, non-authoritative)

- L2 §5.1-shaped matrix: CONCERN / CANONICAL_OWNER / PROJECTION_SURFACES / MACHINE_CONTRACTS / COMPATIBILITY_ALIASES / LEGACY_SURFACES / STATUS / ACTION / EVIDENCE_REFS; every row exact-SHA evidence refs to the base blobs in MANIFEST.yaml.
- Legacy classification table (dispositions already rebound at final rebind):
  - CURRENT_CARRIED_FORWARD: AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE@59fd5f84…, COMPATIBILITY_ALIAS_CONFORMANCE@c7009868…, V48_REGISTRY_ADOPTION_REFERENCE@375ac48e…, test_v47_authority_registry@731e3fd4…, test_v47_compatibility_aliases@80d9f483…, test_v48_registry_adoption@55f78fd9…, test_v47_reference_conventions@bf6888bd… — evidence: live manifest registration (@21730a02…) + test_v48_registry_adoption chaining + carried suites green on base.
  - COMPATIBILITY_ONLY (one-hop aliases, never owners): GITHUB_WORKFLOW@a96d9c18…, VERSION_INTEGRATION_WORKFLOW@60e2bdee….
- Explicit declarations: authority_effect=NONE, gate_effect=NONE, mutation_authorized=false; discovery/evidence only, never required at runtime.
- ~~Register in manifest `references` section (needed for verify_standard PASS).~~ **CORRECTED (V410-T06A-PACK-REBIND-R2):** `verify_standard` does not require registration of this surface (it checks declared paths exist and bootstrap-required assets are declared; no undeclared-file scan). Registration in `references` is machine-blocked by the carried v4.8 RA-05 section/additions guard and is resolved by R2 as zero manifest delta — discoverability is by repository path (`V410-T06A-R2/MANIFEST.yaml` `write_set_resolution`; `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md` §3).

## Surface C — scripts/test_v410_owner_convergence.py (new focused regression)

- Reuses `test_v47_authority_registry.resolve_registry` semantics (import, not reimplement).
- Positive: P1 unique-owner order-permutation; P2 added rows ↔ L2 §3 material concerns on exact base tree; P3 manifest invariants (schema_version=1, 11 legacy entry_ids unmodified, sections intact, inventories disjoint); P4 both aliases one-hop non-owner; P6 legacy dispositions present with evidence; P8 fresh-observer reconstructibility shape.
- Negative: N1 competing owner both orders; N2 broken targets; N3 stale-owner rejection mutant (historical T04B R3 candidate must not win); N4 gap/conflict STOP_FOR_DISPOSITION; N7 deletion-from-both-inventories mutant.
- ~~Register in manifest `verification` section.~~ **CORRECTED (V410-T06A-PACK-REBIND-R2):** not required by `verify_standard` and machine-blocked by the same carried v4.8 guard; resolved by R2 as zero manifest delta (see surface B correction above).

## Corrections (round V410-T06A-PACK-REBIND-R2)

- `class: FALSE_MACHINE_CONFORMANCE_CLAIM`. The two lines above (surfaces B and C) instructed registration in `standard-manifest.json` sections while asserting that `verify_standard` PASS required it. The causal claim is **false** (measured at the T06A candidate: `verify_standard` → PASS, `manifest files: 220`, both surfaces unregistered), and the instruction itself is machine-incompatible with the carried v4.8 RA-05 guard, which any such registration would fail. Provenance of the correction: `MANIFEST.yaml` `conformance_corrections` and `TEST_MATRIX.yaml` `corrections`.
- This pack remains **superseded for execution by `V410-T06A-R2`** (and by `V410-T06A-R3` for the successor round): the R1 write set above is retained as published history, not as executable instruction. `authority_effect=NONE`, `gate_effect=NONE`.

## T06B boundary

schemas/agent-event-v2, review-finding-v1, review-aggregation-v1, templates, prompts, checklists, golden, verifier/CI wiring, execution-environment WEB|LOCAL refinement = #861. Any discovered stale projection recorded as ACTION=REWIRE_PROJECTION, routed, not fixed.
