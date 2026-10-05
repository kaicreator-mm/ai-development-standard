# Pull Request Review Checklist

Use with `templates/implementation-pr.md`. This checklist is used when Independent Review is selected or required. Not every item applies to every PR; mark release-significant non-applicable items explicitly.

## Review Applicability

- [ ] Task/PR Review Policy is explicit: `required / recommended / not-required`.
- [ ] Policy authority/rationale is traceable to Frozen PRD/Architecture, PROJECT_OVERRIDES, Task acceptance, or documented risk assessment.
- [ ] `required` review is not silently downgraded for convenience, cost, lack of a second human, or CI availability.
- [ ] For `recommended`, a SKIP decision is explicit when review is not performed.
- [ ] `not-required` is used only when review genuinely adds insufficient value relative to the concern risk; Review Gate is `NOT_APPLICABLE`.

## Review Identity

When review is performed:

- [ ] Current PR HEAD SHA is recorded.
- [ ] Review result is bound to that exact SHA.
- [ ] Reviewer reconstructed context from GitHub + pinned standard rather than relying on Builder chat history.
- [ ] Reviewer context is independent from the implementation context when Independent Review is required.
- [ ] If HEAD changed after a prior PASS, delta/full re-review was performed when that review remains part of merge policy; old PASS was not reused for the new SHA.

## Scope

- [ ] One primary concern; unrelated refactor/format/dependency churn removed.
- [ ] Change matches frozen PRD/Architecture/Task or has an approved scope update.
- [ ] Public contract changes are explicit.
- [ ] No new mandatory gate was inferred from a historical workflow/script without authority.
- [ ] Material dependency/toolchain, Git-workspace, configuration/secret, artifact/workspace or external-system effects are routed to the corresponding v4.1 owner instead of inferred from local state.
- [ ] A non-authoritative Execution Context, if present, is not treated as Product/Task/Validation/Release authority.
- [ ] For v4.7 recovered adoption/migration wiring, the concern's canonical owner is resolved through `standard-manifest.json#semantic_authorities`; central wiring/checklist/profile text does not duplicate or take over owner semantics.
- [ ] A v4.7-lineage-incompatible convergence need is routed to `docs/implementation/4.7.0/FUTURE_MAJOR_REGISTER.md` as planning input rather than implemented by path/schema/authority expansion inside an unrelated Task.

## v4.6 AI-native Governance (when material)

- [ ] Intent/Assumption, Context Engineering, and Skill/Reusable Procedure semantics come from their three v4.6 normative owners; this PR does not invent a competing Product/Task/Assurance/Dispatch/Handoff/Validation/Release owner.
- [ ] Material interpretation/assumption/UNKNOWN is not restated as user fact or promoted into durable Product/Architecture/Task truth without the owning authority.
- [ ] Currentness-sensitive claims re-read the live owning fact; stale chat/memory or a larger context dump is not treated as higher authority.
- [ ] Required development truth needed by a successor Agent is durable outside the current chat/session.
- [ ] Skill installation/discovery/tool capability is not treated as trust, Task scope, merge permission or external side-effect authority.
- [ ] AI-native Assurance/Review coverage reuses existing assurance/review owners; model/provider metadata by itself is not proof of independence.
- [ ] Fast Path omits only non-material ceremony. It does not require empty Intent/Skill records, and it does not waive material authority/currentness or required gates.
- [ ] Historical evidence is not retrofitted with v4.6 records or relabeled as current v4.6 evidence.
- [ ] No Context Snapshot/database, repository-wide v4.7 resolver, second autonomy scale, or parallel Review/Validation/Release state was introduced.


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
- [ ] Dependency/toolchain, config, environment and external fidelity facts used by the evidence match the actual validated subject where material.
- [ ] Secret values are absent from ordinary durable logs/evidence; refs/identity are used when secret binding matters.
- [ ] Build output/cache/runtime state is not presented as Validation or Release artifact merely because it exists.
- [ ] When a reviewer cannot establish a runtime/platform fact statically, a VALIDATION_REQUEST is created rather than guessing.

## Task Learning Closeout

- [ ] The PR declares exactly one closeout path: literal `TASK_LEARNING=NONE_MATERIAL` or durable material-learning evidence ref(s)/digest(s).
- [ ] Material learning is reference-first and delegates schema/currentness semantics to `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`; evidence bodies are not copied into the PR merely for ceremony.
- [ ] Missing, ambiguous, mutable, malformed or stale exact-subject/currentness evidence is treated as historical only and is not silently rebound as current behavioral proof.
- [ ] Task Learning is not used as Product/Architecture/Task/ADR/Incident/Review/Validation/merge/release authority and is not presented as exact-HEAD Review/Validation PASS.
- [ ] No private chain-of-thought, hidden evaluator material, credentials, secrets or verbose scratch reasoning is requested or exposed.
- [ ] The `TASK_LEARNING=NONE_MATERIAL` Fast Path remains proportional and does not require an empty Task Learning object.

## Independent Review Result

When review is performed:

- [ ] Review Gate uses only `PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`.
- [ ] Findings identify severity, evidence/location, expected behavior, actual behavior and required change where practical.
- [ ] Release-significant review threads/findings are resolved before merge-ready.
- [ ] Review result is recorded in GitHub review/comment history using the project protocol.

## Minimal CI

- [ ] Project CI profile is `minimal / custom / disabled`.
- [ ] Enabled CI checks are low-cost, deterministic and run from the actual PR head/clean checkout.
- [ ] CI does not replace required Platform/CJ/Hidden/Packaging evidence.
- [ ] If CI is disabled, the documented exact-SHA clean-validation path is followed; Review is required only when the active Review Policy says so.

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
- [ ] Current merge candidate SHA has all **required** Validation, Review and configured CI evidence.
- [ ] For `recommended` Review that was skipped, the skip decision/rationale is recorded.
- [ ] The PR can merge independently under `One concern, one PR` unless an explicit dependency says otherwise.
- [ ] If a stacked PR was rebased/retargeted, affected required review/validation was re-established on the new SHA.
- [ ] PR PASS is not presented as Release PASS.
