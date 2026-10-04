# T11 Execution Contract — Cross-standard Conformance & Dogfood

Authority is subordinate to Frozen Product/L2/DAG, T11 Task Pack blob `f0851868a19c9e321dcbfb70eb46e8f31cb7efd3`, L3 blob `03ac6c46c6091bad6df5e02d94a07f7c58fb7ef9`, and exact generation base `ea5b39bb27ae36886748420d282350dd1a16476e`.

## Goal
Complete only T11 integrated conformance and planner→bounded-executor dogfood/closure-input evidence. This Task produces evidence inputs, never Version Closure, Candidate Freeze, Hidden Validation or Release Qualification.

## Builder implementation write set
After this pack HEAD, Builder may modify only:
- `scripts/test_v43_conformance_dogfood.py`
- `docs/implementation/4.3.0/dogfood/T11_EVIDENCE.md`
- `docs/implementation/4.3.0/dogfood/fixtures/**`
- `.github/workflows/verify-standard.yml` only if one narrowly-scoped T11 invocation is materially required to integrate the focused suite.

The Builder MUST NOT modify this Execution Pack, Frozen Product/L2/DAG/L3/Task Packs, v4.3 semantic owners/profiles, VERSION/README/CHANGELOG, release/closure authority, or sibling Task evidence.

## Required semantic kernel
- Make all ten Frozen T11 shortcut-negative families executable.
- Integrate profile-resolution and DAG-mutation regressions without creating alternate owners.
- Produce durable planner→bounded-executor dogfood showing a high-capability planner's Product/Architecture-bound Task/Pack can be consumed by a bounded/lower-cost executor interpretation or evaluation without Product/Architecture redesign.
- Dogfood may be simulation/evaluation unless the selected subject materially requires real execution. Synthetic evidence must be labeled as such and cannot become real host/provider proof.
- Bind subject, planner role, bounded executor/evaluator role, expected oracle, actual result, clarification/escalation behavior and redesign-needed YES/NO.
- Preserve exact subject/test/CI/Validation/Review identities and P0–P3 dispositions.

## Currentness / stop rule
Immediately before implementation, re-read live `version/v4.3.0`, #257 native dependencies, Task Pack/L3 blobs and this branch. Proceed only if target remains `ea5b39bb27ae36886748420d282350dd1a16476e`, native blocked_by remains 0, and pack is current. Any material drift => STOP and `CONTROLLER_REBIND_REQUIRED`.

## Completion
Builder runs focused and applicable pinned tests/CI, opens one concern PR to `version/v4.3.0`, posts exact HEAD/tree/write set and real evidence, then stops. Independent Integration Validation and a genuinely new Fresh Review are mandatory successors.
