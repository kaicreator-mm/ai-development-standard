# V410-IDENTITY-R1 implementation map — owner boundary and JIT decisions

## Owner boundary (REUSE_FIRST_OWNER_MAP — rebound, not rediscovered)

- **RELEASE_STANDARD / checklists** own the release identity obligation (what the VERSION/README/CHANGELOG triple must say at closure time). This concern executes a bounded slice of that obligation and claims no authority beyond it.
- **VALIDATION_STANDARD** owns exact-subject evidence meaning; `concern` validation scope only.
- **Frozen Product #837 PRD §18/§19** owns requirement meaning; no requirement text is restated here.
- **T06B/T07A/T07B/T08A** hold the positional-registry family pattern this rebind mirrors; their frozen deltas stay asserted.

## Deliverable topology

1. Identity triple delta: `VERSION` (4.10.0), `README.md` (line-3 current-version + blockquote posture sentence; all lineage history verbatim), `CHANGELOG.md` (`## v4.10.0 — Unreleased candidate` integration-facts entry; v4.8.0-and-below entries untouched).
2. Disclosed successor rebind: three positional TASK_CANDIDATES registries (T08A frozen at integrated tip `d864465a`, active flag moved to the V410-IDENTITY entry), the T08A focused suite (BASE_SHA/BASE_TREE + active expectations + frozen-T08A delta guard), the integration runner (BASE_SHA/BASE_TREE, expected_active=V410-IDENTITY, admission refs #779@6063217361 / #779@6063246782).
3. Mechanically forced pin cascade: projection record R2 blob fold (50e26dc6 → 56cf032a), T07A IMPLEMENTATION_MAP row R2 provenance fold, T07A TEST_MATRIX `identity_registry_rebind` provenance block, T07B suite `T07A_INDEX_BLOB_AT_BASE` fold (d3a62083 → 5da87fd6), reference section-2 citation fold. All five pinned surfaces converge in-commit.

## JIT decisions

- Manifest registration: declined — `scripts/verify_standard.py` requires none; `scripts/test_v48_registry_adoption.py` RA exact-set guards forbid unlisted additions. `standard-manifest.json` stays untouched.
- Checklist/CI/golden mutation: declined (dispatch boundary; T07A/T07B/T08A precedent).
- Historical T08A-pack internal records (`.agent/execution/V410-T08A-R1/`): intentionally untouched — they are that generation's own subject records, outside this write set.

## Boundary

No standards edits, no schema/template/verifier changes, no semantic repair of any predecessor surface, no Release/Validation/Review/Freeze authority. The Builder does not merge.
