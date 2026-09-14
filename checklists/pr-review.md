# Pull Request Review Checklist

Use with `templates/implementation-pr.md`. Not every item applies to every PR; mark release-significant non-applicable items explicitly.

## Scope

- [ ] One primary concern; unrelated refactor/format/dependency churn removed.
- [ ] Change matches frozen PRD/Architecture/Task or has an approved scope update.
- [ ] Public contract changes are explicit.
- [ ] No new mandatory gate was inferred from a historical workflow/script without authority.

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
- [ ] Independent work was not stopped solely because an unrelated gate is blocked.

## Git / Delivery

- [ ] Commit/branch/PR identity is traceable to Task/Issue when applicable.
- [ ] Required review and configured minimal status checks pass before merge.
- [ ] The PR can merge independently under `One concern, one PR` unless an explicit dependency says otherwise.
- [ ] PR PASS is not presented as Release PASS.
