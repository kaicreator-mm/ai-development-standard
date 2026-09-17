# Pull Request Review Checklist

Use with `templates/implementation-pr.md`. Not every item applies to every PR; mark release-significant non-applicable items explicitly.

## Review Identity

- [ ] Current PR HEAD SHA is recorded.
- [ ] Review result is bound to that exact SHA.
- [ ] Reviewer reconstructed context from GitHub + pinned standard rather than relying on Builder chat history.
- [ ] Reviewer context is independent from the implementation context when Independent Review is required.
- [ ] If HEAD changed after a prior PASS, delta/full re-review was performed and old PASS was not reused for the new SHA.

## Scope

- [ ] One primary concern; unrelated refactor/format/dependency churn removed.
- [ ] Change matches frozen PRD/Architecture/Task or has an approved scope update.
- [ ] Public contract changes are explicit.
- [ ] No new mandatory gate was inferred from a historical workflow/script without authority.

## Task / Dependency Semantics

- [ ] PR is linked to the correct Task/Issue.
- [ ] Planning Task DAG reference is traceable.
- [ ] GitHub Issue Dependencies express the canonical execution dependencies.
- [ ] Sub-issue hierarchy is not being misused as execution dependency.
- [ ] If PR is stacked, the stack is justified by a real unmerged code-baseline dependency.
- [ ] Stacked PR topology is not being used as the canonical Task DAG.
- [ ] PR base/target is the correct version branch, main branch, or stack parent.
- [ ] Required upstream dependencies for merge are satisfied, or the PR remains non-merge-ready.

## Structure / Maintainability

- [ ] New code is placed in the correct app/service/package/module.
- [ ] Shared logic has a clear ownership boundary; no new catch-all utility dumping ground.
- [ ] Dependency direction follows project architecture.
- [ ] Generated files have a reproducible source/command.

## Tests / Validation

- [ ] Bug fixes include regression evidence where practical.
- [ ] New/changed contracts have appropriate contract tests.
- [ ] Relevant unit/integration/E2E/critical-path tests are updated.
- [ ] Failure paths and boundary conditions are covered according to risk.
- [ ] No meaningful assertion/gate was weakened merely to get green Validation/CI.
- [ ] Tested commit SHA is explicit.
- [ ] Required Validation Tuples are explicit where platform/toolchain matrix applies.
- [ ] One tuple PASS is not reused as another tuple PASS.
- [ ] Mock/sandbox/cross-build evidence is not misreported as real platform/external validation.
- [ ] When a reviewer cannot establish a runtime/platform fact statically, a VALIDATION_REQUEST is created rather than guessing.

## Independent Review Gate

- [ ] Version Branch Task/Fix PR has Independent Review unless an explicit higher-authority exception applies.
- [ ] Review Gate uses only `PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`.
- [ ] Findings identify severity, evidence/location, expected behavior, actual behavior and required change where practical.
- [ ] Release-significant review threads/findings are resolved before merge-ready.
- [ ] Review result is recorded in GitHub review/comment history using the project protocol.

## Minimal CI

- [ ] Project CI profile is `minimal / custom / disabled`.
- [ ] Enabled CI checks are low-cost, deterministic and run from the actual PR head/clean checkout.
- [ ] CI does not replace required Platform/CJ/Hidden/Packaging evidence.
- [ ] If CI is disabled, the documented exact-SHA clean-validation + review path is followed.

## Documentation

- [ ] User-visible workflow/config/API/architecture changes update authoritative docs.
- [ ] README/AGENTS/CLAUDE do not duplicate new facts unnecessarily.
- [ ] `Docs: NOT_APPLICABLE` is justified when no documentation change is needed.

## Blockers

- [ ] FAIL/BLOCKED/NOT_RUN states are truthful.
- [ ] Each blocker records downstream impact.
- [ ] Blocker propagation follows Issue/dependency edges rather than stopping unrelated work.
- [ ] Independent work was not stopped solely because an unrelated gate is blocked.

## Git / Delivery

- [ ] Commit/branch/PR identity is traceable to Task/Issue when applicable.
- [ ] Task workflow state is not confused with Gate status.
- [ ] Current merge candidate SHA has required Validation + Independent Review + configured required CI.
- [ ] The PR can merge independently under `One concern, one PR` unless an explicit dependency says otherwise.
- [ ] If a stacked PR was rebased/retargeted, affected review/validation was re-established on the new SHA.
- [ ] PR PASS is not presented as Release PASS.
