# Task Pack T-007 — Local-first CI / Validation Policy

- Goal: integrate local-first execution with validation ownership, alternate executor, provider attestation, CI usage and baseline refresh ordering.
- Write set: `standards/CI_EXECUTION_STANDARD.md`, `standards/VALIDATION_STANDARD.md`, `standards/MODEL_USAGE_POLICY.md`.
- Forbidden: CI outage treated as PASS; weakening provider-specific attestation; making remote CI the normal debug loop.
- Default engineering loop: implement locally → focused tests → lint/typecheck/build → required tests → package check → task-owned platform validation → stable exact HEAD → push → required remote certification only.
- Distinctions to keep explicit: required validation profile vs normal execution provider vs provider-specific attestation requirement; local Ubuntu evidence != Windows/device evidence; task validation != version closure validation.
- Baseline refresh: do not spend final authoritative validation on a candidate whose baseline is already obsolete (PR-A blocks PR-B → validate A, merge, refresh B, new dispatch, validate B).
- Model preparation split: Web/Strong Semantic Kernel for high-risk semantics; Local agents own repository mechanics (extends MODEL_USAGE_POLICY, no second model-routing standard).
- Acceptance: local-first loop default; attestation preserved; refresh ordering stated.
- Required gates: verify-standard.
- Validation ownership: concern.
- Review policy: recommended.
- Agent freedom: F1_BOUNDED_IMPLEMENTATION.
- Dependencies: T-006 (parallel with T-008).
