# T-011 JIT Execution Contract

## Exact authority
- Issue: #730 / T-011 Registry / Manifest / Adoption Wiring. The SINGLE central shared-file wiring lane.
- Base: `version/v4.9.0@a351a6ef9d2c9733d01df46e9dbd4888e392cc97`, tree `8b67895641d1db9b21aa974d7ba34516a822c923`.
- Frozen Product (`a8ec7030...`), Frozen L2 (`bd41ea01...`), Frozen Task DAG v0.2 (`b9fe0cc7...`), current Task Pack and L3 remain authoritative.
- Immutable DAG v0.1 `### T-011` (blob `4f358ba2...`) is the normative concern; bounded L3.
- Native blockers zero (T-003/T-004/T-005/T-006/T-008/T-009/T-010 all DONE); all five lineage refs current at base.

## Required result (central wiring — consumes completed owner outputs; may NOT rewrite sibling semantic owners)
1. `standard-manifest.json`: register/adopt the completed v4.9 outputs for discoverability (v4.9 schemas, references, focused-test surfaces, the T-002 output registration gap noted at #793/#794, T-010 gate-currentness matrix); exactly-one-new-default-family accounting (Role Execution Profile v1 is the only new default machine family; Assurance Plan v2 and Task Learning v2 recognized as same-family successors, NOT new families); inherited entries preserved verbatim.
2. `.github/workflows/verify-standard.yml`: register the v4.9 focused kernels in the pinned CI battery (test_v49_execution_core, test_v49_authority_state_registry, test_v49_role_execution_profile, test_v49_task_learning_v2, test_v49_gate_currentness, test_v49_execution_contract_refs, test_v49_jit_dag_governance, test_v49_assurance_plan_v2, test_v49_assurance_owner, test_v49_release_applicability — the full current set), appended in the established style. This closes the CF-V49-02 kernel-registration notes. Do not remove or reorder existing commands.
3. Sibling pin re-binds (CF-V49-01/02; provenance-commented, #788 precedent — re-bind ONLY the stale blob/path pins, never weaken assertions):
   - `scripts/test_v48_registry_adoption.py`: RA01/RA02/RA05 re-bind to the post-T003 v4.9 registry inventory (exact-set semantics preserved; a fourth family/unlisted addition/drop/rename must still FAIL);
   - `scripts/test_v49_execution_core.py`: K08 read-only-surface pin re-bind for `schemas/dispatch.schema.json` (T-008 legally mutated it) — pin to the current DAG-owned blob with provenance;
   - `scripts/test_v49_role_execution_profile.py`: the dispatch.schema.json pin (same surface) + the EXECUTION_ARCHITECTURE_STANDARD.md pin (pre-existing; re-bind to the T-007-appended blob ffe4788b-lineage with provenance).
4. `references/REGISTRY_ADOPTION_V49_REFERENCE.md`: compatibility aliases/successor discovery + progressive-adoption references (Assurance v1->v2, Task Learning v1->v2 same-family chains; Role Execution Profile v1 as the only new family).
5. `docs/implementation/4.9.0/MIGRATION_ADOPTION.md`: migration/adoption guidance for consumers (older pinned projects remain valid; re-pin route resolves; what changed for consumers in v4.9).

## Hard boundaries
- May not rewrite sibling semantic owners — the three re-bind files change ONLY stale pin constants (+ provenance comments), zero assertion-logic edits.
- Registry metadata grants no semantic authority; older pinned projects remain valid (verify with the project-standard route).
- No Product/L2/DAG mutation; frozen blobs resolve unchanged at candidate.

## Mutation authority
Only the seven Builder write-set paths in MANIFEST plus the six immutable `.agent/execution/T-011/**` planning files. The JIT pack commit (Controller) already contains the T-011 record relocation + harness path re-bind.
