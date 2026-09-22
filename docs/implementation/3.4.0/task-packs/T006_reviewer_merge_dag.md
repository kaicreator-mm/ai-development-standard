# Task Pack T-006 — Reviewer / Merge / DAG Control

- Goal: define the closed loop — review request, changes request, validation request, review pass, merge, downstream unlock — with WEB_REVIEWER pointer-driven from GitHub facts.
- Write set: `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `standards/CHATGPT_WEB_ROLE.md`, `standards/EXECUTION_ARCHITECTURE_STANDARD.md`, `prompts/**`, `scripts/**`.
- Forbidden: reviewer modifying product code in the same review role/session; automatic PASS carry-over on HEAD change; human prompt-relay between roles.
- Reviewer duties: re-read current PR exact HEAD/base, verify evidence SHA identity, read Frozen Authority + Task Pack (Execution Pack as subordinate evidence), inspect complete diff/write set, review Contract / Failure Handling / L3, classify P0–P3. Results: `REVIEW_PASS / CHANGES_REQUESTED / VALIDATION_REQUESTED / BLOCKED`.
- Merge controller: after REVIEW_PASS + satisfied gates, deterministic merge, record identities, recompute DAG ready sets — no human prompt relay; DAG unlock is automatic downstream READY recomputation.
- Acceptance: closed loop specified; Web Builder + Local Validator + Web Reviewer first-class; merge triggers ready-set recomputation.
- Required gates: verify-standard, test_v34_lifecycle_contracts.
- Validation ownership: concern.
- Review policy: required (version-level consolidation).
- Agent freedom: F1_BOUNDED_IMPLEMENTATION.
- Dependencies: T-004, T-005.
