# Version Integration Workflow

## 1. Purpose

This standard defines how substantial version work is integrated through GitHub when the version contains multiple tasks, multiple agents, frozen product/architecture inputs, or environment-specific validation.

The goal is to keep GitHub as the recoverable execution memory without creating branches for every drafting step.

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

Task/fix PRs target the version branch. The final version PR targets `main`.

### B. Trunk / Fast Path

Use this mode for small, low-risk, already-scoped maintenance where a dedicated version integration branch would not add useful isolation.

```text
main
  └── task/<scope> or fix/<scope>
          ↓
         main
```

Bug fixes, small documentation changes, and narrow maintenance work MAY use this mode if frozen scope and release policy allow it.

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

## 4. Implementation task branches

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
- A task branch starts from the current intended integration baseline.
- A task must state its upstream checkpoint / baseline SHA.
- A task must complete its required task-level validation before merge unless explicitly blocked by a downstream-only environment gate.
- In Version Branch Mode, task PRs merge to the version branch, not directly to `main`.
- Independent task branches MAY run in parallel when the Task DAG permits it.
- Finished short-lived branches SHOULD be deleted after merge unless retention has a documented purpose.

## 5. Validation issues do not automatically create branches

A validation issue is an execution work item, not necessarily a code-change work item.

If validation only executes commands against an exact SHA and produces evidence, no branch or PR is required.

If validation finds a defect that requires a source change, create a separate task/fix branch and PR, then re-run the affected required validation against the new exact SHA.

Evidence from an older SHA MUST NOT be promoted to PASS for the new candidate without real re-execution where the gate requires it.

## 6. Version milestone and issue labels

For repositories that use GitHub Milestones, a release/version SHOULD use a milestone such as `vX.Y.Z` rather than creating one label per version.

Labels express stable properties of a work item. Recommended label taxonomy:

```text
type:task
type:bug
type:validation

handoff:local-agent
executor:codex
executor:claude-code

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

Repositories MAY use equivalent naming, but SHOULD keep the dimensions distinguishable: work type, executor, gate, environment, release impact.

## 7. GitHub fact chain

A substantial version SHOULD be recoverable from GitHub without relying on chat history.

The intended fact chain is:

```text
PRD Freeze
→ L1/L2 evidence as required
→ Task DAG
→ L3 evidence as required
→ Task branches / PRs
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

## 8. Cost and repository hygiene

Branch count itself is not a reason to avoid task isolation. Branches are references to Git objects and do not by themselves require GitHub Actions execution.

However, repositories MUST still follow repository hygiene rules: do not commit build caches, dependency directories, large generated outputs, databases, model weights, installers, or repeated binary artifacts merely because they are produced by task branches.

Cost-sensitive projects SHOULD prefer local/self-hosted validation where appropriate and keep GitHub-hosted CI minimal according to the configured CI profile.

## 9. Selection rule

Use Version Branch Mode when the engineering value of integration isolation, multi-agent handoff, candidate control, or exact-SHA closure is material.

Use Trunk / Fast Path when the change is narrow enough that a version branch would add ceremony without improving correctness, recoverability, or reviewability.
