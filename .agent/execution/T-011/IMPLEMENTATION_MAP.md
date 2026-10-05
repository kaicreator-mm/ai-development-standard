# T-011 Implementation Map

Builder writes only:
1. `standard-manifest.json` — adopt v4.9 outputs (discoverability/registration); exactly-one-new-default-family accounting; inherited verbatim.
2. `.github/workflows/verify-standard.yml` — append the v4.9 focused kernel commands in the established `run:` style (order after existing commands; no removals/reorders).
3. `scripts/test_v48_registry_adoption.py` — RA01/RA02/RA05 provenance-commented re-binds to the post-T003 inventory (exact-set strength preserved).
4. `scripts/test_v49_execution_core.py` — K08 read-only-surface pin re-bind for schemas/dispatch.schema.json (provenance comment; zero assertion-logic change).
5. `scripts/test_v49_role_execution_profile.py` — two pin re-binds (dispatch schema current blob; EXECUTION_ARCHITECTURE current blob) with provenance comments.
6. `references/REGISTRY_ADOPTION_V49_REFERENCE.md` — aliases/successor discovery + progressive adoption.
7. `docs/implementation/4.9.0/MIGRATION_ADOPTION.md` — consumer migration/adoption guidance.

Read-only inputs: the CF inputs listed in MANIFEST (`#745@5992918366`, `#722@5985991276`, `#831@5994177360`, `#841@5995114854` — read via gh); `scripts/test_v47_progressive_disclosure.py` (progressive-adoption style); `references/ASSURANCE_PLAN_V2_COMPATIBILITY.json` + `references/TASK_LEARNING_V2_COMPATIBILITY.json` (same-family evidence); `docs/implementation/4.8.0/MIGRATION_ADOPTION.md` (style).
