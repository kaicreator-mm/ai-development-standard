# Task DAG — <version/scope>

## Frozen Inputs

- PRD: `<path/ref>`
- Architecture / Contracts: `<path/ref>`
- Baseline: `<sha>`
- Standard revision: read `.dev-standard/VERSION`

## Lane-Oriented Decomposition Prompt

Before finalizing Task dependencies, actively look for **safe parallel lanes** that reduce wall-clock development time.

Ask:

1. Which concerns can make useful progress independently after their own prerequisites are satisfied?
2. Can the work be separated by real ownership/write-set boundaries such as contract, core/runtime, adapters/integrations, UI/UX, docs/examples, validation preparation, platform-specific work, or domain/component boundaries?
3. Which shared contract/architecture facts must be frozen first so downstream lanes can execute without guessing?
4. Where should multiple lanes converge into an explicit central wiring/integration Task rather than editing the same files concurrently?
5. Are any apparent lanes actually false parallelism because they share unresolved architecture, overlapping write sets, mutable shared contract ownership, an unmerged code baseline, or the same integration authority?
6. Can unrelated work be moved out of a serial chain without weakening dependency, Review, Validation, or Release truth?

Use lane names that describe the real concern boundary. Examples such as `contract`, `core`, `integration`, `ui`, `validation`, `platform-*`, or domain/component names are guidance, not a mandatory taxonomy.

The goal is **maximum safe parallelism, not maximum task count**. Do not split a single tightly coupled concern into artificial lanes merely to create concurrency.

## Planning DAG

| Task | Issue | Lane | Depends On | Parallel | Risk | Input / Reference | Output | Acceptance | Model | Required Validation | Review Policy | Code Baseline | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T-001 | `#<id>` | `<lane>` | — | YES/NO | L/M/H | | | | High/Low | | required/recommended/not-required | independent/stacked | TODO |

Planning status values: `TODO / DOING / BLOCKED / DONE / DEFERRED / NOT_APPLICABLE`.

Rules:

- This document/checkpoint is the planning/history DAG. It records decomposition rationale, acceptance, risk, parallelism and intended dependencies.
- Once execution starts, each implementation Task SHOULD map to a GitHub Task Issue when the project uses Issue-based execution.
- GitHub Issue Dependencies are the canonical live execution DAG. `Depends On` in this document MUST remain traceable to the materialized Issue relationships.
- A task may be marked `DONE` only when its acceptance criteria and required task-level gates are satisfied.
- `Lane` identifies the planning concurrency/ownership lane; it is not a separate execution authority or state machine.
- Tasks in different lanes SHOULD be allowed to execute concurrently when their real prerequisites are satisfied and their write sets/authority boundaries are compatible.
- `Parallel=YES` means the task can make useful progress concurrently without unsafe overlapping edits; it does not automatically mean there is no completion dependency.
- When parallel lanes must assemble, prefer an explicit convergence/integration Task that owns central wiring and cross-lane composition.
- Do not declare parallel lanes to bypass a real Issue Dependency, shared mutable contract owner, stacked code-baseline dependency, central wiring owner, or unresolved architecture decision.
- Independent docs/tests/adapters/components/platform work and validation preparation SHOULD NOT be serialized behind unrelated implementation work when their inputs are already stable.
- `DEFERRED` requires an explicit reason and release impact; it is not a substitute for FAIL.
- High-risk or low-cost-model tasks SHOULD link an L3 Reference Pack using `Tests → Contract → Core Implementation → Failure Handling → Reference`.
- Task boundaries SHOULD map to reviewable concerns and GitHub Issues/PRs when source changes are required.

## Lane Summary

Before freeze, summarize the intended concurrency plan:

| Lane | Tasks | Entry prerequisites | Shared write-set / authority constraints | Converges at |
|---|---|---|---|---|
| `<lane-a>` | T-001, T-003 | `<facts/dependencies>` | `<none or explicit constraint>` | T-007 |
| `<lane-b>` | T-002, T-004 | `<facts/dependencies>` | `<none or explicit constraint>` | T-007 |

If the DAG is mostly serial, record why the dependencies are real rather than leaving parallelism unexplored.

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
Lane                  = planning hint for safe concurrency/ownership, not authority
```

## Stacked Code Baseline

Set `Code Baseline = stacked` only when the task must build on another task branch that has not yet merged.

A stacked PR does not replace the corresponding Task Issue or Issue Dependency. Do not turn the entire Task DAG into a PR stack merely to mirror task order.

If the stack is rebased/retargeted after an upstream merge, required review/validation evidence affected by the SHA change must be re-established.
