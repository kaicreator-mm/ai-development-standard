# Version Integration Workflow

## 1. Purpose

This standard defines how substantial version work is integrated through GitHub when the version contains multiple tasks, multiple agents, frozen product/architecture inputs, or environment-specific validation.

The goal is to keep GitHub as the recoverable execution memory without creating branches for every drafting step.

For GitHub-native multi-agent routing, Issue state/events, canonical execution dependencies and risk-based Independent Review, also read `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`.

## 2. Two supported integration modes

### A. Version Branch Mode

Use this mode by default for a substantial version that has one or more of the following:

- frozen PRD / product scope;
- multiple implementation tasks;
- parallel agents;
- multiple validation environments;
- candidate / hidden validation / release closure;
- work expected to span multiple sessions.

Canonical shape:

```text
main
  └── version/vX.Y.Z
        ├── task/vX.Y.Z-t01-<scope>
        ├── task/vX.Y.Z-t02-<scope>
        ├── fix/vX.Y.Z-<issue>-<scope>
        └── ...
              ↓
        version/vX.Y.Z
              ↓
             main
```

Task/fix PRs target the version branch by default. The final version PR targets `main`.

A Task/Fix PR MUST pass its **required** task-level validation, configured required CI when applicable, required Issue Dependencies, and any Independent Review that its Review Policy marks `required`.

Version Branch Mode by itself does **not** make Independent Review mandatory.

### B. Trunk / Fast Path

Use this mode for small, low-risk, already-scoped maintenance where a dedicated version integration branch would not add useful isolation.

```text
main
  └── task/<scope> or fix/<scope>
          ↓
         main
```

Bug fixes, small documentation changes, and narrow maintenance work MAY use this mode if frozen scope and release policy allow it.

Independent Review follows the same risk-based Review Policy; Integration Mode does not override a higher-authority project/task rule.

## 3. Stage artifacts: checkpoint, not branch by default

PRD Freeze, L1 Product Evidence, L2 Architecture Evidence, Task DAG, L3 Implementation Evidence, Candidate Preparation, Validation Evidence and Closeout are engineering facts.

They MUST become stable remote checkpoints when they are used as downstream dependencies, but they SHOULD NOT each receive a dedicated branch merely for formality.

In Version Branch Mode, stage artifacts normally land as commits on `version/vX.Y.Z`:

```text
version/vX.Y.Z
  PRD Freeze checkpoint
  L1 checkpoint (when used)
  L2 checkpoint (when used)
  Task DAG checkpoint
  L3 checkpoint (when used)
  integrated task checkpoints
  candidate / validation / closeout checkpoints
```

A temporary evidence/docs branch MAY be used when the artifact is produced independently or in parallel and needs isolated review.

## 4. Planning DAG and execution DAG

Task DAG has two related representations after freeze:

```text
Planning DAG checkpoint
= decomposition rationale, inputs/outputs, acceptance, risk, parallelism, review policy

Execution DAG
= GitHub Task Issues + native Issue Dependencies
```

GitHub Issue Dependencies are the canonical live Task DAG during execution.

Do not create a dedicated Task-DAG branch merely to represent dependencies.

Sub-issues represent belongs-to hierarchy and MUST NOT be treated as implicit dependency edges.

The planning checkpoint and execution DAG MUST remain traceable. Material dependency changes SHOULD record rationale/event history.

## 5. Implementation task branches

Implementation uses Task / Concern as the default branch boundary.

Recommended names:

```text
task/vX.Y.Z-t01-<scope>
task/vX.Y.Z-t02-<scope>
fix/vX.Y.Z-<issue>-<scope>
test/vX.Y.Z-<scope>
docs/vX.Y.Z-<scope>
```

Rules:

- One concern, one PR.
- A task branch starts from the current intended integration baseline or a justified stack parent.
- A task must state its upstream checkpoint / baseline SHA.
- A task must complete its required task-level validation before merge unless explicitly blocked by a downstream-only environment gate.
- In Version Branch Mode, task PRs merge to the version branch unless they are temporarily based on a justified stack parent.
- Independent task branches MAY run in parallel when the Task DAG permits it.
- Finished short-lived branches SHOULD be deleted after merge unless retention has a documented purpose.

## 6. Stacked PR is optional code-baseline dependency

Stacked PR does not replace Issue Dependency.

Use it only when a Task must build on another unmerged Task branch:

```text
version/vX.Y.Z
  ↑
task/T01-contract
  ↑
task/T02-core
```

Corresponding PR topology:

```text
T01 → version/vX.Y.Z
T02 → task/T01-contract
```

Rules:

- Do not mirror the whole Task DAG as a stack when code can branch independently.
- Issue Dependency remains the canonical execution relationship.
- Stacked PR only captures the current unmerged Git/code baseline relationship.
- When an upstream stack PR merges, downstream PRs SHOULD be rebased/retargeted to the correct remaining parent or version branch.
- Rebase/retarget SHA changes invalidate SHA-bound required review/validation evidence as applicable; re-run affected gates.
- A branch has one direct base while a Task DAG can fork/join, so PR stack topology is not a general DAG representation.

## 7. Risk-based Independent Review

Independent Review is **on-demand**. Every Task/Fix PR SHOULD resolve one Review Policy:

```text
required
recommended
not-required
```

### 7.1 `required`

Use when Review is mandated by Frozen PRD/Architecture, PROJECT_OVERRIDES, Task acceptance, or risk classification.

Typical examples include security/auth/permission changes, public API/schema/migration semantics, cross-service contracts, concurrency/data-integrity logic, high-blast-radius integration and explicit release blockers.

Merge requires Independent Review `PASS` on the current merge-candidate SHA.

### 7.2 `recommended`

Use when a fresh-context review materially improves confidence but should not be a merge gate.

Review MAY be performed. It MAY also be skipped with an explicit decision/rationale. A skipped recommended Review may remain `NOT_RUN` and does not by itself block merge.

If review is performed and produces material findings, those findings must be resolved/dispositioned before merge.

### 7.3 `not-required`

Use for genuinely low-risk/mechanical concerns when project policy permits it. Review Gate is `NOT_APPLICABLE`.

### 7.4 Review execution semantics

Whenever review is performed:

- reviewer reconstructs facts from GitHub + pinned standard;
- final reviewer context SHOULD be independent from implementation context;
- Review Result binds to exact PR HEAD SHA;
- if required Review evidence remains part of merge policy and HEAD changes, old PASS remains historical only and delta/full re-review is required;
- reviewer may request real Local Validation instead of guessing about runtime/platform behavior.

Recommended pipeline when review is selected:

```text
Builder A                    Reviewer B
Task T01 → PR review-ready → review
Task T02 implementation      PASS/findings
Task T02 → merge-ready       (review skipped/not-required)
Task T03 → PR review-ready → review
```

Builder need not wait idle for review when independent work exists. Reviewer should continue other independent review work when one PR fails.

## 8. Validation issues do not automatically create branches

A validation issue is an execution work item, not necessarily a code-change work item.

If validation only executes commands against an exact SHA and produces evidence, no branch or PR is required.

If validation finds a defect that requires a source change, create a separate task/fix branch and PR, then re-run the affected required validation against the new exact SHA.

Evidence from an older SHA MUST NOT be promoted to PASS for the new candidate without real re-execution where the gate requires it.

Validation requested by Reviewer MAY be represented as a dedicated validation sub-issue, but actual blocking semantics use Issue Dependency when another work item/candidate is blocked by it.

## 9. Version milestone and issue metadata

For repositories that use GitHub Milestones, a release/version SHOULD use a milestone such as `vX.Y.Z` rather than creating one label per version.

Recommended portable label taxonomy:

```text
type:task
type:bug
type:validation
type:blocker

state:planned
state:ready
state:implementing
state:review-ready
state:reviewing
state:changes-requested
state:validation-needed
state:merge-ready
state:blocked
state:done

review:required
review:recommended
review:not-required

handoff:local-agent
executor:codex
executor:claude-code

gate:review
gate:fast
gate:integration
gate:critical-journey
gate:hidden
gate:platform
gate:packaging

env:ubuntu-build-host
env:windows
env:macos
env:gpu

release-blocker
blocked:environment
```

A Task SHOULD have at most one `state:*` and one `review:*` value at a time. Workflow state and Review Policy metadata MUST NOT be confused with Gate states (`PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`).

Repositories MAY map type/state/review/executor semantics to native Issue Types or custom fields when available, but the protocol meaning must remain portable.

## 10. GitHub fact chain

A substantial version SHOULD be recoverable from GitHub without relying on chat history.

The intended fact chain is:

```text
PRD Freeze
→ L1/L2 evidence as required
→ frozen Task DAG checkpoint
→ Task Issues + Issue Dependencies + Review Policy
→ L3 evidence as required
→ Task branches / PRs
→ required task validation
→ Independent Review only when selected/required
→ integrated version baseline
→ validation issues + exact-SHA evidence
→ candidate freeze
→ hidden validation
→ closeout
→ final version PR
→ main baseline SHA
→ optional tag/release
```

Each formal checkpoint MUST have an unambiguous commit SHA or Issue/PR reference that resolves to one.

## 11. Merge readiness

For a Task/Fix PR, merge readiness requires:

```text
current PR HEAD SHA
+ required task/local Validation PASS
+ Review condition satisfied
+ configured required Minimal CI PASS (when enabled)
+ required Issue Dependencies satisfied for merge
+ correct target version branch / main / stack parent
+ no unresolved release-significant finding/blocker
```

Review condition:

```text
required     → Review PASS on current HEAD
recommended  → Review PASS on current HEAD OR explicit SKIP decision/rationale
not-required → Review Gate NOT_APPLICABLE
```

Only then should the Task route to `state:merge-ready`.

After merge, publish the resulting integration SHA and move the Task to `state:done` when its completion rule is satisfied.

## 12. Agent interaction history

Issue body is the stable work contract. Metadata is current routing state. Comments are append-oriented event history.

Multi-agent work SHOULD use the `ai-dev:event:v1` format from `templates/agent-event-comment.md` for events such as:

```text
IMPLEMENTATION_READY
REVIEW_DECISION
REVIEW_RESULT
FIX_APPLIED
VALIDATION_REQUEST
VALIDATION_RESULT
DEPENDENCY_CHANGED
MERGE_RESULT
```

This lets a new Builder/Reviewer/Validator session recover from GitHub without previous chat transcripts.

## 13. Cost and repository hygiene

Branch count itself is not a reason to avoid task isolation. Branches are references to Git objects and do not by themselves require GitHub Actions execution.

Independent Review should also be applied according to risk rather than as mechanical cost/latency overhead on every PR.

However, repositories MUST still follow repository hygiene rules: do not commit build caches, dependency directories, large generated outputs, databases, model weights, installers, or repeated binary artifacts merely because they are produced by task branches.

Cost-sensitive projects SHOULD prefer local/self-hosted validation where appropriate and keep GitHub-hosted CI minimal according to the configured CI profile.

## 14. Selection rule

Use Version Branch Mode when the engineering value of integration isolation, multi-agent handoff, candidate control, or exact-SHA closure is material.

Use Trunk / Fast Path when the change is narrow enough that a version branch would add ceremony without improving correctness, recoverability, or reviewability.

Choose Independent Review separately from Integration Mode using the Review Policy and risk/authority model.
