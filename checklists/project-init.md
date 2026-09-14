# Project Initialization Checklist

Use this checklist when creating a new project or adopting the development standard in an existing repository.

## Identity / Standard

- [ ] Repository/product responsibility is clear.
- [ ] `.dev-standard/VERSION` contains repository + semantic version + immutable commit SHA.
- [ ] `.dev-standard/PROJECT_OVERRIDES.md` contains real commands, platforms and boundaries.
- [ ] `AGENTS.md` points to the pinned standard and project overrides.

## Structure

- [ ] Chosen structure is the smallest structure that fits current complexity.
- [ ] Multi-module product/platform considered monorepo before unnecessary repo splitting.
- [ ] Deployables, services and shared packages have distinct responsibilities.
- [ ] No catch-all `common/utils/shared` package without a defined contract.
- [ ] Generated/cache/runtime files are covered by ignore/storage policy.

## Documentation

- [ ] Root README explains purpose, quick start, validation and docs entry.
- [ ] `docs/README.md` indexes current formal docs.
- [ ] Product/architecture/implementation/validation/release docs have clear ownership where applicable.
- [ ] No duplicate source of truth across README/AGENTS/CLAUDE/docs.

## Engineering

- [ ] Canonical dependency manifest/lockfile exists where the ecosystem expects one.
- [ ] Bootstrap command is reproducible.
- [ ] Fast validation command is documented.
- [ ] Test data contains no production secrets or private user data.
- [ ] CI can start from a clean checkout.

## GitHub

- [ ] PR template exists when useful for the collaboration model.
- [ ] Issue form/template exists for recurring issue types when useful.
- [ ] CODEOWNERS/ownership rules exist for sensitive or multi-team areas when useful.
- [ ] Main/default stable branch protection/ruleset matches project risk.

## Release

- [ ] Version/release policy is defined.
- [ ] Critical Journeys are known for a releasable product.
- [ ] Hidden Validation strategy is defined when required.
- [ ] Packaging/platform gates are identified.

Result: `PASS / FAIL / NOT_APPLICABLE / BLOCKED` with evidence for every non-trivial FAIL/BLOCKED.
