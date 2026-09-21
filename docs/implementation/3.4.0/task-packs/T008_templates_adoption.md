# Task Pack T-008 — Templates / Adoption / Retention

- Goal: add execution templates, bootstrap pointers, project override capabilities, package exclusion rules, progressive adoption and Fast Path preservation.
- Write set: `templates/**`, `prompts/**`, `standards/PROJECT_ADOPTION.md`, `standards/ISSUE_FIRST_TASK_TRIGGER.md`.
- Forbidden: mandatory large Execution Packs for trivial tasks; Fast Path bloat.
- Deliverables:
  - `templates/task-pack.md`, `templates/execution-pack/` (core artifacts), `templates/validation-handoff-queue.md`.
  - `prompts/local-builder-bootstrap.md`, `prompts/local-validator-bootstrap.md`, `prompts/web-reviewer-bootstrap.md`.
  - Project override capabilities: `execution_pack.enabled/path/retention`, `pull_worker.builder/validator/reviewer`, `validation_queue.enabled/scope`, `local_first.enabled` (exact field names are implementation decisions documented in PROJECT_OVERRIDES template).
- Retention: durable by default — MANIFEST, final Execution Contract, TEST_MATRIX, FAILURE_MATRIX, REVIEW_CHECKLIST, authority-explaining seeds; transient — verbose prompts, debug notes, scratch. Complete packs MAY be retained for provenance; MUST be excludable from shipped package/product artifacts.
- Progressive adoption preserved: execution pack / pull workers / validation queue are opt-in; Trunk/Fast Path unchanged.
- Acceptance: templates exist and are manifest-listed; overrides documented; retention/package exclusion defined; Fast Path lightweight.
- Required gates: verify-standard.
- Validation ownership: concern.
- Review policy: recommended.
- Agent freedom: F1_BOUNDED_IMPLEMENTATION.
- Dependencies: T-006 (parallel with T-007).
