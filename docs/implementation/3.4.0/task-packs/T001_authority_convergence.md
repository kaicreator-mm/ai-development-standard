# Task Pack T-001 — Authority Convergence

Task Pack (durable planning authority). Exact-base execution detail belongs to a JIT Execution Pack, not here.

- Goal: freeze the single v3.4 architecture that absorbs #45 (Task/Execution Pack + dual-agent pull orchestration) and #46 (version-scoped Validation Handoff Queue).
- Objects defined: Task Pack, Execution Pack, Dispatch, Validation Handoff Queue, Evidence; authority order; state dimensions; JIT lifecycle; pack staleness; agent freedom F0–F3.
- Write set: `docs/implementation/3.4.0/**`
- Forbidden: any `standards/`, `schemas/`, `templates/` change; any parallel scheduler/lifecycle/state authority.
- Acceptance: one converged architecture decision exists and is frozen; #45/#46 both map onto it; no second queue truth model.
- Required gates: verify-standard.
- Validation ownership: concern (docs-only); version closure owns the final release matrix.
- Review policy: required (consolidated at version-level Fresh Independent Review).
- Agent freedom: F2_ENGINEERING_DISCRETION.
- Dependencies: none.
- Output: `ARCHITECTURE_DECISION.md` (FROZEN), `TASK_DAG.md`, `TASK_PACKS.json`.
