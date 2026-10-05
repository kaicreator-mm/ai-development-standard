# T-006 Implementation Map

Builder writes only:
1. `schemas/task-learning-v2.schema.json` — same-family successor schema (optional execution_friction_class, recurrence refs, optional root-cause relation, prevention refs, recurrence-audit refs; v1 core fields preserved).
2. `references/TASK_LEARNING_V2_COMPATIBILITY.json` — machine-checkable compatibility record following the T-002 compatibility-record pattern (`references/ASSURANCE_PLAN_V2_COMPATIBILITY.json` at the base — read-only style reference): v1 blob identities, per-dimension COMPATIBLE/INCOMPATIBLE with evidence_refs, no unsupported claims.
3. `references/TASK_LEARNING_V2_REFERENCE.md` — reference doc: field semantics, orthogonality to `friction_classification`, routing/authority boundaries.
4. `scripts/test_v49_task_learning_v2.py` — deterministic stdlib-unittest: schema conformance, same-family compatibility (v1 fixture instances remain v1-valid), negative oracles (see TEST_MATRIX). Style references (read-only): `scripts/test_v48_task_learning.py`, `test_v49_assurance_plan_v2.py`.

Read-only starting points: v4.8 Task Learning v1 owner surface (schema + standard at base), Frozen L2 Task Learning section, `docs/implementation/4.9.0/PRD.md`, L3 T-006 section.
