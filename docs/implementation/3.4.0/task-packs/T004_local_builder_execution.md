# Task Pack T-004 — Local Builder Execution

- Goal: standardize the LOCAL_BUILDER pull-worker flow: JIT branch, dispatch claim, identity verification, implementation order, local validation, stable-head publication, review request.
- Write set: `standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`, `prompts/**`, `templates/**`, `scripts/**`.
- Forbidden: builder self-asserting Independent Review PASS; silently rewriting Execution Pack `base_sha`; second task authority.
- Canonical flow to standardize:

```text
BUILDER_READY → dispatch claim → identity verification → LOCAL_RUNNING
→ implementation (Tests → Contract → Core → Failure Handling → L3)
→ focused validation → required build/typecheck/lint/test/package checks
→ task-owned real-host/platform checks → local defect repair → rerun affected validation
→ stable exact HEAD pushed → exact-SHA evidence → REVIEW_REQUESTED
```

- Claim-time identity verification: Execution Pack base SHA vs current integration SHA, Task Pack identity, dependency completion identities, pinned standard revision, branch identity, clean worktree.
- Acceptance: LOCAL_BUILDER profile documented end-to-end; worker crash recoverable from GitHub facts alone; pointer-only invocation supported.
- Required gates: verify-standard, test_v34_lifecycle_contracts.
- Validation ownership: concern.
- Review policy: required (version-level consolidation).
- Agent freedom: F1_BOUNDED_IMPLEMENTATION.
- Dependencies: T-003.
