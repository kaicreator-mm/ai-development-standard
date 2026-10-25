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

## Optional v4.18 Capability-first / Safe Topology Assessment (planning only)

For a substantial multi-concern version, start from independently acceptable **Product capabilities**, then map each capability to coherent **Concerns**, local Lane steps and actual Task Issues; do not turn every workflow phase, file or checklist step into a separate Issue. Small atomic/Fast Path work (for example, one isolated typo with no shared writer) may record one sentence explaining why no alternative topology is material.

| Product capability / acceptance | Coherent concern / Task | Lane-local steps (not auto-Issues) | Contract / atomic boundary | Unique effective writer / shared integration |
|---|---|---|---|---|
| `<accepted-outcome>` | `T-001` | `<local-workflow>` | `<frozen-ref / invariant>` | `<owned-write-set / central-wiring-task>` |

For a mostly serial candidate, compare one legal alternative or explain concretely why the original chain is necessary. Structural path/independent workfronts are qualitative; record wall-clock, token-cost or speedup as `UNKNOWN` unless measured from admissible evidence.

| Candidate topology | Real prerequisite / advisory dependency reason | Safe parallel workfronts | Shared writer / integration join | Validation / Review / handoff trade-off | Decision |
|---|---|---|---|---|---|
| `<existing-or-alternative>` | `<contract / writer / review-evidence / convergence / resource>` | `<issues or none>` | `<central owner>` | `<scope / UNKNOWN metrics>` | `SELECT / REJECT + reason` |

**These are non-authoritative planning explanations.** Dependency-reason tags do not reclassify GitHub's native `blocked_by`, determine `ready_builder` or `ready_merge`, authorize a source write before a JIT admitted Claim, or bypass required Review/Validation/Release conditions. A real topology change uses the existing formal DAG mutation and native readback, not editing this comparison table.

### Optional pre-Freeze Scaffold feedback

If an actual, accepted source-first SF checkpoint exists, compare its real modules/packages, immutable anchors, contracts and writer paths with proposed concerns **before** binding/freeze. Identify shared manifest/catalog/entrypoint hotspots and consider a qualified contract seam or one central integration owner *within the existing L2 amendment authority*; never infer source-writing permission from SF structure alone. After Freeze, any material SF/DF change follows existing `TASK_DAG_GOVERNANCE_STANDARD.md` §10A and its independent MI/currentness rules. Without an accepted source-first SF, record `SF_PLANNING_FEEDBACK=NOT_APPLICABLE`; the next optional v4.12 SF↔DF binding section remains conditional.

### Candidate Agent, proof and human-assistance fit

| Lane / concern | Candidate skill and risk/freedom | Builder / independent Reviewer | WEB / CI / LOCAL capability actually needed | Remaining-work handoff / true human trigger |
|---|---|---|---|---|
| `<lane>` | `<ability, risk, F0-F3>` | `<role and review policy>` | `<real tools / physical evidence gap>` | `<exact outstanding proof or NOT_APPLICABLE>` |

Choose **capability classes** at planning time, not fixed model branding or an Agent registry. Real operator, current source SHA, legal Claim and environment validation are selected under the existing Dispatch/Execution Pack authority. CI may satisfy actual qualified tests; a Local action is requested only for evidence a supported executor cannot obtain. Human involvement stays bounded to existing protected decisions, actual physical/operator assistance or exceptional authority escalation; routine CI polling and forwarding logs are not new human gates.

## Optional v4.12 Source Scaffold ↔ Task Binding (only when applicable)

Use this section **only** for a project that actually adopts a qualified v4.12+ standard, has an accepted source-first SF checkpoint and needs an explicit DF mapping. It is a *planning snapshot*, not another writable authority or a new required metadata schema. The Task-side anchor binding is the single canonical mapping owner; reference the source facts, do not replicate an editable SF anchor ownership table.

```text
Product ref + blob: <actual frozen Product source>
L2 ref + blob: <actual frozen Architecture source>
Accepted SF commit: <40-char immutable SHA>
SF material source inventory/ref/digest: <actual Git objects incl mode and path>
DF draft source: <candidate file path; NO self-referential final DF hash or MI output here>
Pair Freeze record reference: <separate external attestation to be created AFTER DF Freeze>
Known source-owner pre-approved exclusions: <none or exact paths + authority + reason>
```

| Anchor ID | Kind | Location (accepted SF) | Contract Ref | Canonical Task Issue | Task Pack Ref | Writer / Read-only Consumer |
|---|---|---|---|---|---|---|
| `<stable-id>` | `<structural-kind>` | `<exact-path>` | `<accepted-ref>` | `#<id>` | `<exact-ref>` | `writer` |

Before DF Freeze, verify for **every** `planned_task_id → canonical native GitHub Issue #` binding that the Issue exists and is current, `binding_writer_path_set ⊆ Issue Allowed changes` and `binding_writer_path_set ∩ Issue Forbidden changes = ∅`; missing/UNKNOWN Claim at execution, invalid Task-to-Issue mapping and widened write scope are `MATERIAL/HOLD`. **Do not insert the DF file's final Git blob or its MI digest into that same DF file.** Freeze the completed DF source first, then place its computed exact blob, SF material input identity, separately recomputed MI digest, proof command/input list and current Issue/Claim references into a **separate immutable pair Freeze record** outside the DF/SF/MI input digest; generated indexes and the attestation are never self-hashing inputs. Independently recompute both `anchor → Task` and `Task → anchor` from actual current source objects; reject missing important anchors, duplicate active writers, unexplained added/deleted/renamed files, symlink/gitlink/mode changes and any SF/DF/L2 contradiction. `DAG_ONLY_INPUT` is only a narrowly preauthorized SF-view exemption; it does **not** exclude that input from DF/MI checks. Generated `DERIVED_NONAUTHORITATIVE` indexes never certify themselves. A Task `SPLIT/MERGE/SUPERSEDE` that changes this binding requires the ordinary DAG mutation plus live native Issue Dependency update. If no accepted Scaffold exists, mark this section `NOT_APPLICABLE` with reason, rather than fabricate a source pair or new Task.

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
