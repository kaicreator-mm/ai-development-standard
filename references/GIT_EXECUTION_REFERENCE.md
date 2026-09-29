# Git Execution Reference

This document is non-normative guidance for `GIT_EXECUTION_STANDARD.md`.

## 1. JIT Task workspace

A common safe Builder flow is:

```text
1. Read current live integration SHA.
2. Prove native Task dependencies are satisfied.
3. Create the Task branch/workspace from that exact SHA.
4. Record branch + exact base in the Task Issue/Execution Pack.
5. Mutate only the Task-owned write set.
6. Publish immutable commit(s) before durable handoff.
```

A Git worktree is one implementation:

```bash
git fetch origin
git worktree add ../work-T03 -b task/T03 <exact-integration-sha>
```

An independent clone or isolated container checkout can satisfy the same isolation contract.

## 2. Two-writer example

Bad:

```text
Builder A and Builder B both use C:\repo or /srv/repo and modify different-looking files.
```

Even if files differ initially, generators, lock files, Git index state, hooks or cleanup can cross-contaminate the workspace.

Good:

```text
Builder A -> isolated worktree A
Builder B -> isolated worktree B
shared authority -> GitHub Issues / published refs / immutable evidence
```

## 3. Reviewer/Validator exact checkout

A read-only exact-SHA flow can use a fresh clone or detached worktree:

```bash
git fetch origin
git checkout --detach <requested-head-sha>
test "$(git rev-parse HEAD)" = "<requested-head-sha>"
git status --porcelain
```

For PR-bound evidence, also re-read the current PR HEAD/base before and after execution.

## 4. Dirty workspace handling

When `git status` reports unknown local changes, do not immediately run `git reset --hard` or `git clean -fdx`.

Preferred routes:

1. identify the owner and preserve/publish the work;
2. create a clean new worktree/clone for the requested operation;
3. report `BLOCKED` if a required local-only state cannot be safely separated.

## 5. Rewrite and evidence

Example:

```text
validated HEAD = abc123
Builder rebases and force-pushes successor = def456
```

The old evidence remains evidence for `abc123`. Tree similarity does not rewrite it to `def456`. The successor follows Review/Validation currentness or explicit impact/reuse rules.

## 6. Cherry-pick boundary

A sibling Task commit can be technically cherry-picked but still be unauthorized. For example, T02 MUST NOT cherry-pick T03 just to use a helper if that bypasses the frozen DAG/write-set. Shared wiring waits for its owning integration Task.

## 7. Stacked PR example

Stacking is appropriate when Task B truly cannot compile or be reviewed without an unmerged Task A code baseline. It is not appropriate merely because two Tasks were started close together.

Task DAG authority remains GitHub Issue Dependencies. The PR stack only describes code ancestry.

## 8. Cleanup and recovery checklist

Before removing a worktree or branch, check:

```text
working tree clean or changes durably preserved
unpublished commits identified
stash/reflog if relevant
merge/rebase/cherry-pick state absent or intentionally preserved
submodule state understood
LFS pointer/content requirements satisfied
sparse patterns recorded if material
partial-clone required objects available
remote branch/ref/evidence published when handoff depends on it
```

## 9. Capability notes

Older Git versions, filesystem case sensitivity, file locking, long paths, symlink support, local hooks and signing may affect execution. These should be captured when material rather than becoming hidden assumptions.
