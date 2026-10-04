# T-006 Successor Implementation Map

## COPY_EXACT — pinned v4.7 source

Copy byte-for-byte from `d8f613127d0167453297a5a5e983de048607aa07`:

```text
schemas/authority-applicability-entry-v1.schema.json
schemas/state-dimension-registry-v1.schema.json
scripts/test_v47_convergence_metadata_contracts.py
references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md
scripts/test_v47_authority_registry.py
registries/state-dimensions-v1.json
references/STATE_DIMENSION_REGISTRY_REFERENCE.md
scripts/test_v47_state_dimension_registry.py
standards/REFERENCE_CONVENTION_STANDARD.md
references/REFERENCE_CONVENTION_REFERENCE.md
scripts/test_v47_reference_conventions.py
references/PROGRESSIVE_DISCLOSURE_ROUTING.md
scripts/resolve_standard_read_set.py
scripts/test_v47_progressive_disclosure.py
references/COMPATIBILITY_ALIAS_CONFORMANCE.md
scripts/test_v47_compatibility_aliases.py
```

The v4.8 focused verifier must prove these bytes/blob identities were preserved.

## COMPOSE — current v4.8 base is authoritative starting text

### `standard-manifest.json`

Preserve every current v4.8 inventory entry; add v4.7 T01–T06 discovery assets and `semantic_authorities`; then add the three v4.8 machine families and T006 v4.8 reference/verifier. Do not replace the whole manifest with the v4.7 file.

Distinct concerns may point to the same existing canonical owner. A duplicate semantic concern with competing owners must fail closed. Registry metadata never grants mutation/gate/PASS authority.

### `standards/PROJECT_ADOPTION.md`

Add current v4.8 convergence-discovery guidance. Point to the carried semantic registry, state registry, progressive resolver and V48 adoption reference. Preserve Fast Path and optional/materiality-driven reads.

### `templates/project/.dev-standard/PROJECT_OVERRIDES.md`

Compose the v4.7 convergence-discovery project section into the current v4.8 template, updating migration/reference pointers to v4.8. Do not remove current fields or non-weakening rules.

## ADD — T006 v4.8-owned integration surfaces

### `references/V48_REGISTRY_ADOPTION_REFERENCE.md`

Non-authoritative map. Required explicit outputs:

```text
authority_effect=NONE
gate_effect=NONE
mutation_authorized=false
```

Map three machine families to existing owners/references; reuse Interchange v1; keep Availability derived; identify v4.7 carry-forward provenance.

### `docs/implementation/4.8.0/MIGRATION_ADOPTION.md`

Additive migration only; no historical evidence rebinding, no destructive rewrite, no second Interchange family, no mandatory optional-context loading.

### `scripts/test_v48_registry_adoption.py`

Integrated structural/conformance oracle. Must execute P3 contradiction-aware mutation probes RA-N03/04/05/09/13 as well as RA-N01/02/06/07/08/10/11/12.

## SOURCE READ-ONLY — do not port

Version-bound v4.7 Product/Task/closure evidence, including T07 unified conformance code/evidence and T09/closure/dogfood/release artifacts. Re-test their relevant invariants against v4.8; do not relabel their historical PASS/evidence as current.