# Task DAG — <version/scope>

## Frozen Inputs

- PRD: `<path/ref>`
- Architecture / Contracts: `<path/ref>`
- Baseline: `<sha>`
- Standard revision: read `.dev-standard/VERSION`

| Task | Depends On | Parallel | Risk | Input / Reference | Output | Acceptance | Model | Required Validation | Status |
|---|---|---|---|---|---|---|---|---|---|
| T-001 | — | YES/NO | L/M/H | | | | High/Low | | TODO |

Status values: `TODO / DOING / BLOCKED / DONE / DEFERRED / NOT_APPLICABLE`.

Rules:

- A task may be marked `DONE` only when its acceptance criteria and required task-level validation are satisfied.
- `Parallel=YES` means the task can run concurrently without depending on another unfinished task and without unsafe overlapping edits.
- `DEFERRED` requires an explicit reason and release impact; it is not a substitute for FAIL.
- High-risk or low-cost-model tasks SHOULD link an L3 Reference Pack using `Tests → Contract → Core Implementation → Failure Handling → Reference`.
- Task boundaries SHOULD map to reviewable concerns and, where useful, GitHub Issues/PRs.
