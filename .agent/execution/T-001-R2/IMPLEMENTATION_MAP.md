# T-001 R2 Implementation Map

Read first: T-001 Task Pack; v4.8 L3 T-001 guidance; Frozen L2 §4.1; #550 P1; current `standards/DEVELOPMENT_WORKFLOW.md` §8; repository-supported schema subset.

Repair only `schemas/task-learning-v1.schema.json`, `scripts/test_v48_task_learning.py`, and `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`.

Use schema `pattern` to enforce one canonical immutable Git exact-subject identity. Keep exact-subject fields optional so identity-bound historical records remain legal; any current-behavior applicability helper/oracle must return false when exact subject/currentness/evaluated subject is missing, mutable, malformed or drifted.

Add negative oracles for branch, symbolic ref/tag, repository-only, short/malformed SHA and equal mutable refs. Preserve Fast Path and all authority/privacy/governance boundaries.
