# Task Pack T-003 — Unified Dispatch Model

- Goal: extend canonical events/reducer/derived state for builder/validator/reviewer claim, run, complete, block and supersede — one dispatch architecture, no parallel state machine.
- Write set: `schemas/**`, `scripts/**`, `standards/EXECUTION_ARCHITECTURE_STANDARD.md`.
- Forbidden: Builder/Validator/Reviewer queue state machines; `event-v3`; collapsing workflow/dispatch/gate/provider dimensions.
- Deliverables:
  - `schemas/dispatch.schema.json` — dispatch_id, repository, version, task, parent issue, PR, role, execution profile, branch, expected base SHA, requested HEAD SHA, Task Pack / Execution Pack identity, validation profile, pinned standard revision, operator freedom, pull dispatch state.
  - `agent-event-v2` extension — `DISPATCH_CLAIMED`, `EXECUTION_PACK_STATE_CHANGED`; pull dispatch vocabulary `READY / CLAIMED / RUNNING / COMPLETED / BLOCKED / SUPERSEDED` mapped onto the v3.3 lifecycle vocabulary; drift/pack/freedom/profile fields.
  - `execution-state.schema.json` extension — derived `execution_pack_state`, `validation_queue` projection fields.
  - `scripts/v34_rules.py` — deterministic classifier functions consumed by T-009 regression.
- Acceptance: new event contracts validate positive and reject bypass forms; v3.3 event vocabulary and invariants preserved (extend, not duplicate).
- Required gates: verify-standard, test_protocol_schemas, test_v34_lifecycle_contracts.
- Validation ownership: concern.
- Review policy: required (version-level consolidation).
- Agent freedom: F1_BOUNDED_IMPLEMENTATION.
- Dependencies: T-002.
