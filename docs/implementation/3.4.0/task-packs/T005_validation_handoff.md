# Task Pack T-005 — Validation Handoff Profile (absorbs #46)

- Goal: make #46 the canonical Validator execution profile — version-scoped queue projection, exact-SHA dispatch, Validator authority, PASS/FAIL/BLOCKED semantics, HEAD drift, evidence payload, pointer-only invocation.
- Write set: `standards/VALIDATION_STANDARD.md`, `standards/EXECUTION_ARCHITECTURE_STANDARD.md`, `templates/**`, `prompts/**`, `schemas/**`, `scripts/**`.
- Forbidden: independent queue lifecycle; Queue Issue as validation/Task authority; Validator implicitly repairing product source; PASS rewritten onto a successor SHA.
- Queue semantics: version-scoped Issue exposes derived items (`READY / HOLD / RUNNING / PASS / FAIL / BLOCKED / SUPERSEDED`) as a projection of Validator dispatches + gate facts; pointer-only invocation `Continue <project> <version> current READY validation work in Issue #NN`.
- Exact-SHA rule: `requested_head_sha == current PR HEAD` before execution, else `HEAD_DRIFT` → dispatch superseded, no execution as PASS evidence; new candidate → new dispatch identity.
- Evidence minimum: repository, version, task, issue, PR, dispatch_id, expected_base_sha, requested_sha, actual_checked_out_sha, current_pr_head, environment (os/arch/runtimes/toolchain), commands + exit codes, focused test counts, working_tree_clean, source_modifications_after_validation, result.
- Acceptance: queue is projection-only; HEAD drift deterministic; validator MUST-NOTs explicit; evidence contract machine-checkable.
- Required gates: verify-standard, test_v34_lifecycle_contracts.
- Validation ownership: concern.
- Review policy: required (version-level consolidation).
- Agent freedom: F1_BOUNDED_IMPLEMENTATION.
- Dependencies: T-003 (parallel with T-004).
