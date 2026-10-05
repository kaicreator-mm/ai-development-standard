# T-012 JIT Execution Contract

## Exact authority
- Issue: #731 / T-012 Deterministic Proportional-Orchestration Conformance Suite. Risk: critical/high. L3: required test-oracle review.
- Base: `version/v4.9.0@d53e943ec7109648485b64a647ed2c7cf553531d`, tree `5ad2dbd8c312a67bb050a3199ab9b29b70c23406` (post T-011 central wiring).
- Frozen Product (`a8ec7030...`), Frozen L2 (`bd41ea01...`), Frozen Task DAG v0.2 (`b9fe0cc7...`), current Task Pack and L3 remain authoritative.
- Immutable DAG v0.1 `### T-012` (blob `4f358ba2...`) is the normative concern. Native blockers zero; all five lineage refs current at base.
- Tests may assert Frozen owner semantics but may NOT redefine them. Final integrated conformance binds ACTUAL MERGED owner outputs and current predecessor lineage.

## Required result
1. `scripts/test_v49_conformance_suite.py` — deterministic suite covering AT MINIMUM the DAG v0.1 `### T-012` coverage list: precedence vs conjunction; reduction proof fail-closed; assurance currentness TOCTOU; adverse finding carry-forward; selector/independence conflicts; JIT in-envelope vs DAG mutation; gate-owned transfer/currentness; Release per-gate applicability/non-aggregation; predecessor lineage wait; Task Learning same-family compatibility; manual-compatible state reconstruction. Bind each scenario to actual merged owner outputs (T-002/T-004/T-005/T-006/T-007/T-008/T-009/T-010 surfaces at this base) with exact refs. The suite is a TEST ORACLE: it asserts owner semantics, never redefines them, and makes no runtime claim beyond executed tests.
2. `fixtures/conformance-suite/**` — scenario fixtures.
3. AUTHORIZED RE-BINDS (Controller per F1/F2 disclosures; provenance-commented, pin-constants only, zero assertion-logic change):
   - `scripts/test_v49_gate_currentness.py` t07 tree-scoped pin: re-bind from `d8fd03db..HEAD ⊆ T-010 write set` (structurally red at any integrated tree) to the actual merged T-010 delta at this base — assert the T-010 content is present via its merged files (same strength: the T-010 outputs must be exactly present);
   - `scripts/test_v48_integration_closure.py`: C01 inventory-size pin re-bind to the post-T-011 manifest inventory; C08 workflow pin re-bind to the current (post-T-011 + T-012-appended) workflow command set — exact-set strength preserved.
4. `.github/workflows/verify-standard.yml`: append the conformance-suite command in the established style (no removals/reorders).

## Hard boundaries
- Suite asserts owner semantics; owner defects discovered route back to owning Tasks (report, do not repair owner files).
- No Product/L2/DAG mutation; frozen blobs resolve unchanged at candidate.

## Mutation authority
Only the five Builder write-set paths in MANIFEST plus the six immutable `.agent/execution/T-012/**` planning files.
