# Task Pack — T03 Git Execution & Worktree Isolation

```yaml
task_id: T03
repository: kaicreator-mm/ai-development-standard
version: 4.1.0
integration_target: version/v4.1.0
merge_target: version/v4.1.0
task_pack_ref: docs/implementation/4.1.0/task-packs/T03_git_execution.md
dependencies: [T01]
allowed_write_set:
  - standards/GIT_EXECUTION_STANDARD.md
  - references/GIT_EXECUTION_REFERENCE.md
  - scripts/test_v41_git_execution.py
forbidden_scope:
  - T01 shared schemas except consumption/reference
  - standard-manifest.json
  - PROJECT_OVERRIDES and shared workflow/checklist wiring
  - redefinition of GitHub Task/dispatch or Validation/Release authority
acceptance:
  - concurrent writable executions require isolated workspace semantics
  - local workspace/branch/commit is non-authoritative until durably published as applicable
  - exact-subject checkout, rewrite, destructive operation, cleanup and recovery rules are explicit
  - cherry-pick cannot bypass Task DAG/sibling/central wiring ownership
  - Git worktree is a reference mechanism, not mandatory technology
required_gates:
  - focused semantic/regression tests
  - destructive/recovery and evidence-rewrite negatives
validation_scope: concern
validation_owner: T03
review_policy: required
l3_requirement: docs/implementation/4.1.0/L3_REFERENCE_PACKS.md#t03--git-execution--worktree-isolation
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
execution_pack: JIT
```

## Why

Issue #188 demonstrates a broad but coherent missing execution concern. T03 owns Git/repository/workspace execution safety while preserving existing GitHub workflow and exact-SHA Gate authority.

## Acceptance detail

Cover repository materialization, branch traceability, worktree/equivalent isolation, role defaults, dirty-tree policy, durable handoff, rewrite/rebase/reset/force-push impact, cherry-pick/stacked baseline boundaries, merge references, cleanup/recovery, destructive operations, submodule/LFS/sparse/partial clone, local hooks and Git capability/signing policy.

## Out of scope

No new workflow state machine, no Task claim semantics, no Release integration verdict, no central shared template/manifest edits.
