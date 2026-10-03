# T-001 Implementation Map

## Inputs
- Frozen DAG T-001 definition and reviewed Task Pack.
- Existing v4.0 `docs/implementation/4.0.0/ASSURANCE_PLAN.md` owner semantics.
- Current v4.9 L3 reference for T-001.

## Implementation sequence
1. Create stable normative Assurance owner surface in `standards/ASSURANCE_PLAN_STANDARD.md`.
2. Preserve explicit continuity to the v4.0 owner; do not restate or mutate finding aggregation semantics beyond a faithful normative pointer/boundary.
3. Add compact reference/migration guidance in `references/ASSURANCE_PLAN_REFERENCE.md`.
4. Add focused deterministic tests for owner continuity, historical v1 readability and negative authority boundaries.
5. Run focused test + repository verifier; open one PR to `version/v4.9.0`.

No T-002 proof/composition/currentness implementation belongs here.
