# Pull Request Review Checklist

Use with `templates/implementation-pr.md`. Not every item applies to every PR; mark non-applicable items explicitly when they are release-significant.

## Scope

- [ ] One primary concern; unrelated refactor/format/dependency churn removed.
- [ ] Change matches frozen PRD/Architecture/Task or has an approved scope update.
- [ ] Public contract changes are explicit.

## Structure / Maintainability

- [ ] New code is placed in the correct app/service/package/module.
- [ ] Shared logic has a clear ownership boundary; no new catch-all utility dumping ground.
- [ ] Dependency direction follows project architecture.
- [ ] Generated files have a reproducible source/command.

## Tests

- [ ] Bug fixes include regression evidence where practical.
- [ ] New/changed contracts have appropriate contract tests.
- [ ] Relevant unit/integration/E2E/critical-path tests are updated.
- [ ] Failure paths and boundary conditions are covered according to risk.
- [ ] No meaningful assertion/gate was weakened merely to get green CI.

## Documentation

- [ ] User-visible workflow/config/API/architecture changes update the authoritative docs.
- [ ] README/AGENTS/CLAUDE do not duplicate new facts unnecessarily.
- [ ] `Docs: NOT_APPLICABLE` is justified when no documentation change is needed.

## Validation

- [ ] Required local/Agent gates report PASS/FAIL/NOT_RUN/NOT_APPLICABLE/BLOCKED truthfully.
- [ ] CI is from the PR's actual head commit.
- [ ] Mock/sandbox validation is not misreported as real external boundary validation.
- [ ] Known limitations/blockers are visible.

## Git / Delivery

- [ ] Commit/branch/PR identity is traceable to Task/Issue when applicable.
- [ ] Required review/status checks pass before merge.
- [ ] The PR can merge independently under `One concern, one PR` unless an explicit dependency says otherwise.
