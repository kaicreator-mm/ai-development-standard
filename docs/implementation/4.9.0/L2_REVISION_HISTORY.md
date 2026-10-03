# v4.9.0 L2 Revision History

L2 snapshots are immutable architecture evidence. `L2_ARCHITECTURE_EVIDENCE.md` is the current L2 candidate only.

| Revision | Status | Review / reason | L2 blob | First materialization / reviewed identity |
|---|---|---|---|---|
| v0.1 | superseded / rejected for Freeze | first candidate authored under #710; #711 Fresh Architecture Review FAIL `P0=0/P1=4/P2=5/P3=3` | `840b65555b9d98fb5158e2af8571eede78cc811a` | reviewed HEAD `540941d06972128865a669e67cec884c6eb41087`, tree `5ecdbd13d7bc01a7e4db5637ed2cf743948ae466` |
| v0.2 | current successor / not frozen | #711 F1–F12 disposition under #712; complete-delta successor review required | `bd41ea0175b459a6a490fd37ad579e429a58a1c3` | first materialized HEAD `46074420bd956129cce128eac4722919f0c40117`, tree `a20d3a624c03f658a4cfba835437b419980fe526` |

## Review lineage

### v0.1

- Product authority: Frozen PRD v0.4 / #709;
- L2 builder: #710;
- Fresh Architecture Review: #711@5967289394;
- verdict: FAIL;
- findings: F1–F12, `P0=0/P1=4/P2=5/P3=3`.

### v0.2

- disposition authority: #712;
- preserves Frozen Product semantics;
- removes duplicate assurance owner/family;
- incorporates existing Assurance Plan, Adversarial Review, Gate Authority precedence, v4.2 compatibility, v4.3 DAG governance, v4.7 registry, and v4.8 frozen ownership;
- first materialized as exact blob `bd41ea0175b459a6a490fd37ad579e429a58a1c3` at HEAD/tree `46074420bd956129cce128eac4722919f0c40117` / `a20d3a624c03f658a4cfba835437b419980fe526`;
- later metadata-only history/status commits do not create a new L2 revision when this L2 blob is byte-identical;
- requires fresh independent review bound to the final live HEAD/tree and this same L2 blob, covering the complete v0.1→v0.2 semantic delta.

## Invariants

1. Never rewrite a historical L2 snapshot to make prior Review appear current.
2. Architecture Review terminals bind to exact L2 blob/HEAD/tree.
3. A material successor L2 requires successor Architecture Review.
4. Product Freeze remains valid unless Architecture evidence demonstrates a Product contradiction; #711 found none.
5. Task DAG remains unauthorized until explicit L2 Freeze.
