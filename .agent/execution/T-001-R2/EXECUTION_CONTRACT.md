# T-001 R2 Execution Contract

Exact base: `version/v4.8.0@33dfb8f05bca1ba8fd4ea8d9a2c63eaa8f9aa830`.
Authority: Frozen Product/L2/DAG R1 > T-001 Task Pack > #550 P1 repair requirement > this contract. Freedom: F1 bounded repair.

## Source write set
- `schemas/task-learning-v1.schema.json`
- `scripts/test_v48_task_learning.py`
- `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`

Execution Pack files under `.agent/execution/T-001-R2/**` are read-only after this checkpoint.

## Repair kernel
Close only #550's exact-subject/currentness P1. Code/artifact-specific `implementation_subject_ref` and `currentness_ref` must use the canonical immutable identity `git:<owner>/<repository>@<40-lowercase-hex-commit-sha>`. Mutable branch/tag/ref aliases, repository-only tokens, short/malformed SHAs and ambiguous identities fail closed for current behavioral applicability.

Applicability requires valid immutable subject, valid immutable currentness, valid immutable evaluated current subject, and exact equality across all three. Missing/invalid/drifted refs preserve historical evidence only.

Preserve `TASK_LEARNING=NONE_MATERIAL`, no-private-CoT, no-authority-substitution, bounded confidence layers and T-005 governance ownership. Do not absorb T-015/T-016/T-002 or modify Frozen planning authority.
