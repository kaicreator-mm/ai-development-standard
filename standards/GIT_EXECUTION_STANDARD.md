# Git Execution & Worktree Isolation Standard

## 1. Purpose and authority

This standard is the normative owner for safe repository materialization and writable Git workspace execution. It governs checkout identity, writable isolation, local branch/worktree traceability, destructive operations, rewrite effects, cleanup and recovery.

It does not own GitHub Task state, Issue Dependency state, dispatch/claim state, Review/Validation results, Candidate Freeze, Release Qualification or repository-integration verdicts.

`schemas/execution-context-v1.schema.json` may project material workspace facts, but that projection is not a workspace state machine and does not create authority.

## 2. Local Git facts are non-authoritative

A local branch, worktree, commit, reflog entry or stash is execution state, not durable project authority by existence alone. Where the project requires a durable handoff, the relevant commit/ref/evidence MUST be published to an authorized durable surface.

Branch existence never means a Task is claimed, READY, reviewed, validated or merge-authorized.

## 3. Exact subject materialization

A Reviewer/Validator or exact-subject executor MUST prove that the materialized checkout matches the requested immutable subject before producing exact-SHA evidence.

At minimum, when applicable, verify:

- repository identity;
- requested SHA/ref and actual checked-out SHA;
- current PR HEAD/base identity when the dispatch is PR-bound;
- required submodule/LFS/sparse/partial materialization completeness;
- working-tree cleanliness or explicitly authorized dirty-state handling.

A branch name is auxiliary metadata and MUST NOT replace exact commit identity.

## 4. Writable workspace isolation

Two logically independent concurrent writers MUST NOT mutate the same writable workspace.

A writable execution MUST use an isolated workspace boundary such as a Git worktree, independent clone, container/VM checkout, or another mechanism that provides equivalent write isolation and exact repository identity.

`git worktree` is a reference mechanism, not mandatory technology.

Read-only consumers MAY share immutable materialization where the mechanism cannot create write races or hidden state coupling.

## 5. Role defaults

Builder-like mutation should occur in a Task-authorized isolated workspace/branch. Reviewer and Validator roles SHOULD prefer clean read-only/detached or otherwise protected exact-subject workspaces when feasible.

A Reviewer/Validator MUST NOT silently repair source in the workspace being reviewed/validated. Repair requires the appropriate Builder authority/dispatch.

## 6. Dirty-tree policy

Before destructive or evidence-bearing execution, the operator MUST classify local modifications as owned, intentionally preserved, generated/disposable under authority, or unknown.

Unknown or unowned changes MUST NOT be discarded to obtain a clean status. If a required exact clean checkout cannot be established without risking work loss, create another clean isolated workspace or report `BLOCKED`.

## 7. Commits, handoff and publication

Unpublished local commits remain non-authoritative project facts. A handoff that depends on them MUST publish an immutable commit/ref to the authorized remote or other durable project authority and record its identity.

A handoff MUST NOT refer only to a branch name when exact identity matters.

## 8. Rewrite, rebase, reset and force-push

Rebase, amend, reset, history rewrite and force-push can change immutable subject identity. Evidence attached to an old exact SHA remains historical and MUST NOT be transferred to a successor SHA by assertion.

If a rewritten successor needs PASS/Review authority, it follows the owning standard's currentness/impact rules. A semantically similar tree does not automatically inherit old exact-SHA evidence.

Force-push or reset MUST NOT be used to bypass an open finding, Validation requirement or Task ownership boundary.

## 9. Destructive operations

Operations such as `git reset --hard`, `git clean`, worktree removal, branch deletion, forced ref movement or equivalent destructive cleanup require established ownership and scope.

When ownership is ambiguous, destructive operations MUST fail closed. Preserve or snapshot potentially valuable unpublished work and use a new clean workspace instead.

## 10. Cherry-pick boundaries

Cherry-pick is a transport mechanism for commits, not Task-DAG authority.

An operator MUST NOT cherry-pick sibling Task work into a branch when doing so bypasses native Task dependencies, write-set ownership, required review/validation or central wiring ownership.

Central/shared wiring explicitly owned by another Task MUST remain with that owner even if a sibling commit is technically cherry-pickable.

## 11. Stacked PR boundaries

Stacked PRs describe real unmerged code-baseline dependency. They are not a substitute for GitHub Issue Dependencies and do not create the live Task DAG.

Use a stacked PR only when a Task genuinely requires another unmerged code baseline. Once the prerequisite is integrated, later independent Tasks SHOULD branch JIT from the live integration target rather than preserve accidental stacks.

## 12. Merge and integration references

A merge commit, merge-result preview or integrated tree is distinct from the reviewed/validated PR HEAD. Existing Validation/Review/Release standards own whether evidence composes across those identities.

Git execution tooling MUST NOT label a merge result PASS merely because its parent PR HEAD passed concern checks.

## 13. Cleanup and recovery

Cleanup MUST preserve unpublished or unknown work. Recovery procedures SHOULD consider:

- reflog/stash/unpublished commits;
- worktree registration and lock state;
- remote-tracking refs;
- interrupted merge/rebase/cherry-pick state;
- submodule changes;
- LFS pointers/content;
- sparse checkout patterns;
- partial-clone/promisor object availability.

A lost local workspace is not proof that the work never existed; durable published commit/evidence identity is the recovery authority when available.

## 14. Materialization variants

Submodules, Git LFS, sparse checkouts and partial clones MAY be used. If they affect required files, tests, generated output or evidence, their materialization state becomes part of execution identity and MUST be sufficient for the requested validation/review profile.

A partial checkout MUST NOT claim whole-repository evidence when relevant omitted content was not materialized.

## 15. Hooks, Git capabilities and signing

Local hooks, signing, Git version/features, credential helpers and platform-specific filesystem behavior are execution capabilities. Projects MAY require specific policies, but an Agent MUST NOT infer authority from whatever happens to be configured on its host.

Commit/tag signing or provenance requirements are mandatory only when project/release authority says so.

## 16. Failure handling

- ambiguous workspace ownership + destructive action requested → `BLOCKED` / use new clean workspace;
- requested exact SHA not materialized → no exact-SHA PASS evidence;
- rewrite changed subject identity → old evidence remains historical;
- required submodule/LFS/object unavailable → execution `BLOCKED` if material;
- conflicting writable operators in same workspace → stop one operator and restore isolation before further mutation.

## 17. Boundary with other owners

- GitHub Task Issues + native Issue Dependencies own live Task DAG authority.
- Execution/dispatch standards own Task claim and role dispatch.
- `VALIDATION_STANDARD.md` owns exact-SHA Validation truth and drift handling.
- Review standards own review subject/currentness.
- Release/repository-integration standards own final integration authority.
- T07 owns central adoption/wiring; this standard does not modify it.
