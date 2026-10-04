# T-003 Implementation Map

Builder writes only:

1. `standard-manifest.json` — union-extend with canonical v4.9 owner/applicability entries (T-002 assurance proof/currentness, Role Execution Profile v1 reference, Release applicability reference, other new v4.9 semantic concerns); inherited entries preserved verbatim; entry-per-concern uniqueness enforced.
2. `registries/state-dimensions-v1.json` — register v4.9 proof/currentness dimensions and `WAITING_LINEAGE` derived posture + v4.9 forbidden inferences; inherited dimensions (incl. F01–F10 negatives) intact.
3. `references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md` — document the new v4.9 entries (descriptive only).
4. `references/STATE_DIMENSION_REGISTRY_REFERENCE.md` — document the new dimensions (descriptive only).
5. `scripts/test_v49_authority_state_registry.py` — deterministic stdlib-unittest verifier: registry-schema conformance of the two JSON registries, owner uniqueness across all semantic_authorities, currentness binding, and negative oracles N01–N14 (see EXECUTION_CONTRACT). Match the established v4.7/v4.8 registry-test style (read `scripts/test_v47_authority_registry.py` / `test_v47_state_dimension_registry.py` / `test_v48_registry_adoption.py` as style references — read-only).

Read-only starting points:
- inherited registry surfaces at the base (both JSON registries, both schemas, both reference docs);
- `docs/implementation/4.9.0/PRD.md` + L2 forbidden-inference requirements; Frozen DAG v0.2 §3 lineage rules;
- T-002 outputs: `standards/ASSURANCE_PLAN_STANDARD.md`, `schemas/assurance-plan-v2.schema.json`, `references/ASSURANCE_PLAN_V2_*` (the proof/currentness concern being registered);
- #722 preflight terminal (#722@5974905975) — historical input: anticipated registry map, proposed write set, N01–N14 enumeration.
