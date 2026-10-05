# T-012 Review Checklist

This checklist is for independent exact-subject Validation and the later genuinely Fresh Independent Review. The Phase-2 Builder must not self-complete either gate.

## Identity / currentness

- [ ] Exact candidate HEAD/tree is recorded.
- [ ] Candidate descends from the bound Pack HEAD and exact JIT base.
- [ ] Live `version/v4.8.0` at Builder claim matched base `257e95531551960cb163a3e20ab2b3d13f415d3c`, or an explicit approved rebind exists.
- [ ] Task Pack blob is `10168f6ea2a1cb3b0ffff9c1a493b0904d82942f`.
- [ ] L3 blob is `82f0ac808f423d861c030413046c2b2e689bfc1d`.
- [ ] Native #518 blockers were zero at Builder claim with #511/#513/#514 DONE.
- [ ] #469 was re-read at Builder claim; no material successor after `5925124956` was silently ignored.

## Exact write set

- [ ] `git diff --name-only <PACK_HEAD>...<CANDIDATE_HEAD>` contains only `docs/implementation/4.8.0/dogfood/469/**`.
- [ ] Frozen Product/L2/DAG are untouched.
- [ ] `standards/**`, `schemas/**`, `scripts/**`, `.agent/**`, other Task Packs/L3s, CI/workflows and release authority are untouched by the Builder candidate.
- [ ] `git diff --check` passes on the exact candidate diff.

## Required outputs

- [ ] `EVIDENCE_MATRIX.md` exists and covers BDF-01..BDF-12.
- [ ] `EXECUTION_OBSERVATIONS.md` exists and records T-012's own Builder facts separately.
- [ ] `RESULT.md` exists and records evidence scope, support, non-support, limitations/counterevidence and one allowed disposition.
- [ ] Any extra file is inside the authorized directory and is strictly evidence-supporting.

## Source integrity

- [ ] Material #469 claims bind exact source refs.
- [ ] Historical source checkpoints are not presented as current without exact successor evidence.
- [ ] S00/C01/C02/A01a/A01b statuses are not upgraded beyond the consumed source state.
- [ ] Source-reported real executions are not relabeled as T-012 executions.
- [ ] Later Validation/Fresh Review findings in #469 are retained where material and not rewritten as Builder-caught findings without support.
- [ ] Provider/model names are provenance only.

## Measurement integrity

- [ ] `0`, `NONE_REPORTED`, `NOT_REPORTED`, `NOT_MEASURED`, `NOT_APPLICABLE` and `BLOCKED` remain distinct.
- [ ] Clarification/escalation values are exact observations, not inferred from silence.
- [ ] Edit/test loops retain task attribution.
- [ ] Negative-oracle, contract/write-set drift and stale/rebind observations distinguish caught vs not reported.
- [ ] Elapsed/resource/token/cost values appear only when actually observed.
- [ ] Any economic comparison declares comparable population, task scope/complexity, gates, measured fields, method and limitations.
- [ ] If comparability is absent, `RESULT.md` states `ECONOMIC_SAVINGS=NOT_MEASURED`.

## Execution-profile / freedom boundary

- [ ] Builder dispatch/claim used F1 or narrower freedom.
- [ ] Bounded/lower-cost execution, if used, was admitted from current eligibility evidence rather than provider/model identity alone.
- [ ] T-012 records its own Builder profile/provider-model provenance without turning it into authority.
- [ ] Material ambiguity above F1 resulted in stop/escalation rather than self-elevation.

## Governance / independence

- [ ] Builder does not claim independent Validation PASS.
- [ ] Builder does not claim Fresh Review PASS.
- [ ] Validator identity/session is independent from Builder.
- [ ] Fresh Reviewer identity/session is genuinely new and independent from Builder/Validator.
- [ ] Green Builder/Validation status is not used to waive Fresh Review.
- [ ] Result contains no blanket strong→low-cost rule or global Agent score.
- [ ] Any `ADS_EVOLUTION_CANDIDATE` is explicitly non-normative and routed through ordinary ADS governance.
- [ ] T-014, Version Closure and Release PASS are not implied by T-012 PASS.

## Repository checks

- [ ] `python -B scripts/verify_standard.py` result is recorded for the exact candidate.
- [ ] Repository verifier PASS is not misrepresented as factual independent validation of #469 evidence.
- [ ] Validator independently challenges exact source bindings and evidence interpretation.

## Terminal requirement

The qualifying Validation terminal must bind exact candidate HEAD/tree, Pack HEAD/tree, source anchor/currentness result, exact changed paths, BDF coverage, command results, findings and a PASS/FAIL/BLOCKED verdict.

Only after qualifying Validation may the Controller dispatch a genuinely Fresh Independent Review on the exact validated candidate.
