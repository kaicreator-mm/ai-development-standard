# Project Initialization Checklist

Use this checklist when creating a new project or adopting the development standard in an existing repository.

## Identity / Standard

- [ ] Repository/product responsibility is clear.
- [ ] `.dev-standard/VERSION` contains repository + semantic version + immutable commit SHA.
- [ ] `.dev-standard/PROJECT_OVERRIDES.md` contains real commands, validation environments, CI profile, CI execution profile, platforms/toolchains and boundaries.
- [ ] When pinned to v4, `PROJECT_OVERRIDES.md` declares a truthful v4 adoption level (`A0_COMPATIBILITY` through `A4_FULL_ORCHESTRATION`) and compatibility mode.
- [ ] The selected v4 adoption level changes implementation surface only; the project has checked the common non-weakening floor for authority, exact identity, Validation, Review, Candidate/Release and status truthfulness.
- [ ] Existing historical evidence keeps its original subject identity/status during standard migration; no historical evidence is relabeled as newly produced v4 evidence.
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

## Validation

- [ ] Canonical dependency manifest/lockfile exists where the ecosystem expects one.
- [ ] Bootstrap command is reproducible.
- [ ] Fast validation command is documented.
- [ ] Required real execution environments are identified.
- [ ] Required platform/runtime/toolchain tuples are explicit where applicable.
- [ ] Exact-SHA evidence location/format is defined.
- [ ] If v4 reducer/controllers are disabled, every mandatory gate still has a truthful executable manual/fallback path; otherwise the project records `BLOCKED`.
- [ ] Test data contains no production secrets or private user data.

## Minimal CI

- [ ] CI profile is explicitly `minimal / custom / disabled`.
- [ ] `minimal/custom` checks are low-cost, deterministic and clean-checkout reproducible.
- [ ] CI provider, backend/execution model and runner role are declared for enabled CI.
- [ ] Authoritative workflow config path/identity and workflow config source semantics are declared.
- [ ] Provider-specific workflow syntax matches the selected backend semantics; container semantics are not assumed for local/host backends.
- [ ] Required shell/entrypoint and runtime/toolchain source are declared and can be preflight-checked on the real runner.
- [ ] Clone/checkout optional features such as partial clone, submodules and Git LFS match actual repository needs when they are material.
- [ ] A new exact SHA produces/uses a fresh run for that SHA; rerunning an obsolete pipeline is not treated as current-HEAD evidence.
- [ ] Full platform matrices / CJ / Hidden / expensive E2E / packaging are not duplicated into CI without project-specific reason.
- [ ] If CI is disabled, the reason and exact-SHA clean-validation + review path are documented.

## v4 Adoption / Migration

- [ ] `v4.adoption_level` reflects mechanisms that really execute; A2/A3/A4 are not claimed merely because the standard contains schemas/controllers.
- [ ] `v4.assurance.default` and model-diversity defaults do not downgrade stronger Frozen PRD/Architecture/Task requirements.
- [ ] Interchange, if enabled, remains correlation-only/non-authoritative.
- [ ] Fast Path is either disabled, canonical, or stricter; canonical disqualifiers are not removed and low adoption level is not treated as eligibility proof.
- [ ] Candidate PREPARED != FROZEN, PR PASS != Release PASS, and Release READY != Repository Integration complete remain explicit project assumptions.
- [ ] v3.4→v4 historical evidence migration preserves original identity/result and does not rewrite PASS/FAIL/CHANGES_REQUESTED.

## v4.6 AI-native Adoption

Apply these checks only to projects pinned to a v4.6 revision. Adoption is materiality-driven; this section does not require empty machine records for non-material concerns.

- [ ] `PROJECT_OVERRIDES.md` records the v4.6 AI-native profile or explicitly keeps the canonical materiality-driven defaults.
- [ ] The project recognizes exactly three new normative owners: Intent/Assumption Governance, Context Engineering, and Skill/Reusable Procedure Governance.
- [ ] Material intent/interpretation/assumption/UNKNOWN handling cannot silently become Product/Architecture/Task authority; durable machine use points to `schemas/intent-assumption-record-v1.schema.json` only when needed.
- [ ] Required development truth is recoverable from durable GitHub/repository owner surfaces; a project-local Context Snapshot/chat transcript is not the authority substitute.
- [ ] Reusable Skills/procedures have explicit admission/provenance/compatibility handling when material; installation/tool capability is not treated as trust or side-effect authorization.
- [ ] Assurance/Review, F0–F3, Dispatch/Handoff, Validation and Release are referenced through their existing owners rather than duplicated in project-local AI-native policy.
- [ ] Fast Path may omit non-material Intent/Skill records, but it does not omit material authority/currentness facts or higher-authority required gates.
- [ ] Historical evidence is not retrofitted or relabeled as v4.6-produced evidence.
- [ ] No repository-wide v4.7 resolver or second lifecycle/autonomy/Review/Validation/Release vocabulary is introduced by adoption.

## GitHub

- [ ] PR template exists when useful for the collaboration model.
- [ ] Issue form/template exists for recurring issue types when useful.
- [ ] CODEOWNERS/ownership rules exist for sensitive or multi-team areas when useful.
- [ ] Main/default branch protection/ruleset matches project risk and configured CI profile.

## Release

- [ ] Version/release policy is defined.
- [ ] Mandatory release gates have explicit authority sources.
- [ ] Critical Journeys are known for a releasable product.
- [ ] Hidden Validation strategy is defined when required.
- [ ] Platform / production-build gates are identified from frozen authority rather than inferred from old workflows.

Result: `PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE` with evidence for every non-trivial FAIL/BLOCKED.
