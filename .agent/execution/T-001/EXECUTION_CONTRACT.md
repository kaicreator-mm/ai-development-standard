# T-001 Execution Contract

Exact base: `version/v4.9.0@67ad362a47d665c38dbb25f1667b064e6379923d` / tree `9d334c6290e6cf924dd58c909684c5d6451103fe`.
Authority: Frozen Product #709 > Frozen L2 #714 > Frozen DAG #719 > reviewed Task Pack blob `3b88469f36f70c778b87567235bb580d31330cba` > this Execution Pack.

## Source write set
- `standards/ASSURANCE_PLAN_STANDARD.md`
- `references/ASSURANCE_PLAN_REFERENCE.md`
- `scripts/test_v49_assurance_owner.py`

`.agent/execution/T-001/**` is Controller-authored execution authority and MUST NOT be rewritten by the Builder.

## Contract kernel
Canonicalize the existing v4.0 Assurance Plan semantic owner into a stable normative standard surface without changing owner identity, finding union/blocker dominance, Review/Validation/Release authority, or historical `assurance-plan-v1` validity. The new standard surface must explicitly point back to existing owner semantics rather than create a parallel proportional-assurance lifecycle.

Do not implement Assurance Plan v2 proof/composition/currentness (T-002), registry wiring (T-003/T-011), Execution Architecture (T-007), Release semantics (T-005/T-010), or sibling scope.

If implementation requires a schema change, different normative owner, or write outside the listed source set, stop with `TASK_PACK_DEFECT` or `ARCHITECTURE_CONTRADICTION` and route upward; do not widen locally.
