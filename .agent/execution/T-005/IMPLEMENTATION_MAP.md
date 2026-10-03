# T-005 Implementation Map

## Inputs
- Frozen DAG T-005 definition and reviewed Task Pack.
- Current `standards/RELEASE_STANDARD.md` as the sole Release authority.
- Frozen Product/L2 release-applicability decisions and v4.9 L3 reference.

## Implementation sequence
1. Add prospective Release-owned applicability semantics to `standards/RELEASE_STANDARD.md` without creating a second lifecycle.
2. Define per-gate × subject decision posture, fail-closed UNKNOWN, and fresh version-level evaluation boundary.
3. Preserve existing thaw/invalidation/Hidden/Closeout/RQ authority and historical behavior.
4. Add compact reference examples and deterministic negative/compatibility tests.
5. Run focused test + repository verifier; open one PR to `version/v4.9.0`.

T-010 owns later cross-owner evidence/currentness wiring; T-014/T-015 own dogfood/release-evidence handoff.
