# Task DAG — <version/scope>

## Frozen Inputs

- PRD: `<path/ref>`
- Architecture / Contracts: `<path/ref>`
- Baseline: `<sha>`
- Standard revision: read `.dev-standard/VERSION`

## Planning DAG

| Task | Issue | Depends On | Parallel | Risk | Input / Reference | Output | Acceptance | Model | Required Validation | Review Policy | Code Baseline | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T-001 | `#<id>` | — | YES/NO | L/M/H | | | | High/Low | | required/recommended/not-required | independent/stacked | TODO |

Planning status values: `TODO / DOING / BLOCKED / DONE / DEFERRED / NOT_APPLICABLE`.

Rules:

- This document/checkpoint is the planning/history DAG. It records decomposition rationale, acceptance, risk, parallelism and intended dependencies.
- Once execution starts, each implementation Task SHOULD map to a GitHub Task Issue when the project uses Issue-based execution.
- GitHub Issue Dependencies are the canonical live execution DAG. `Depends On` in this document MUST remain traceable to the materialized Issue relationships.
- A task may be marked `DONE` only when its acceptance criteria and required task-level gates are satisfied.
- `Parallel=YES` means the task can make useful progress concurrently without unsafe overlapping edits; it does not automatically mean there is no completion dependency.
- `DEFERRED` requires an explicit reason and release impact; it is not a substitute for FAIL.
- High-risk or low-cost-model tasks SHOULD link an L3 Reference Pack using `Tests → Contract → Core Implementation → Failure Handling → Reference`.
- Task boundaries SHOULD map to reviewable concerns and GitHub Issues/PRs when source changes are required.

## Review Policy Planning

Review is risk-based, not universally mandatory.

Use one of:

```text
required
recommended
not-required
```

Guidance:

- `required`: security/auth/permissions, public API/schema/migration semantics, cross-service contracts, concurrency/data-integrity, high-blast-radius integration, release-blocker/high-risk concerns, or project-specific sensitive areas.
- `recommended`: medium-risk behavior/refactor/integration changes where an independent pass materially improves confidence but is not a merge gate.
- `not-required`: genuinely low-risk/mechanical work when project policy allows it.

The planning value is an initial policy. A higher-authority project/task rule may strengthen it later; it must not be silently weakened.

## Execution DAG Materialization

After Task DAG freeze:

```text
Frozen Task DAG checkpoint
        ↓
Task Issues
        ↓
Milestone / type / initial workflow state / Review Policy
        ↓
GitHub Issue Dependencies
        ↓
Builder / optional Reviewer / Validator queues
```

Do not create a Task-DAG branch merely to encode dependencies.

Important semantics:

```text
Planning DAG document = why/how the work was decomposed
Issue Dependency      = canonical execution dependency
Sub-issue             = belongs-to hierarchy
Task Branch / PR      = implementation boundary and optional review boundary
Stacked PR            = optional unmerged code-baseline dependency
```

## Stacked Code Baseline

Set `Code Baseline = stacked` only when the task must build on another task branch that has not yet merged.

A stacked PR does not replace the corresponding Task Issue or Issue Dependency. Do not turn the entire Task DAG into a PR stack merely to mirror task order.

If the stack is rebased/retargeted after an upstream merge, required review/validation evidence affected by the SHA change must be re-established.
