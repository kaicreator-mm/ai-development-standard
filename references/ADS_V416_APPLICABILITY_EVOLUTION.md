# ADS v4.16 T04 — Evidence-qualified applicability, experiment economics and Evolution routing

**Status:** T04 source-only candidate for [Issue #1268](https://github.com/kaicreator-mm/ai-development-standard/issues/1268), frozen Product/L2/DAG [#1261](https://github.com/kaicreator-mm/ai-development-standard/issues/1261), integration `version/v4.16@6d147eac6c86eff620d3695a46ccbb3be452debb`. Required independent Review and full actual conformance remain pending; illustrative C11/C13/C14 cases are not real Tally experimental runs, Host costs or Domain Package promotion.

## Existing owner mapping — no new lifecycle

| Concern | Existing owner | Minimal v4.16 interpretation |
| --- | --- | --- |
| Source-qualified Task Learning, currentness/evidence strength and nonmaterial default | `schemas/task-learning-v2.schema.json`; `references/TASK_LEARNING_EVIDENCE_REFERENCE.md` | Keep source refs/digests, exact subject, independent verifier evidence; `TASK_LEARNING=NONE_MATERIAL` needs no empty object |
| Six root-cause classes and canonical destination | `standards/DEVELOPMENT_WORKFLOW.md` §8.1 | `PROJECT_DEFECT → ROUTE_PROJECT`, `AGENT_EXECUTION_DEFECT → ROUTE_EXECUTION`, `ENVIRONMENT_OR_TOOL_DEFECT → ROUTE_ENVIRONMENT`, `PROJECT_SPECIFIC_REQUIREMENT → ROUTE_PROJECT_SPECIFIC`, `STANDARD_FRICTION_CANDIDATE → NO_CHANGE|MORE_EVIDENCE`, `ADS_EVOLUTION_CANDIDATE → OPEN_ADS_INTAKE` |
| Governed actual norm change | same standard §8.2; Product/L2/DAG/Task/Review/Release | A usage signal, rank or Task Learning record cannot self-approve or mutate ADS; follow full ordinary Intake route |
| Public evidence privacy | same standard §8.3 `PROJECT_PRIVATE|RESTRICTED|PUBLISHABLE` | Unless source owner explicitly qualifies PUBLISHABLE, withhold raw prompts, prices, private Trace, invoices or other restricted material |
| Bounded experiment economics | frozen `R4_PRODUCT_L2_REPAIR.md` §3 and `VALIDATION_STANDARD.md` | Count failed, cancelled, aborted and retried trials; qualify success by same verifier/cohort/scope/window. Host/CI/Review/validation/rework/recovery costs included or missing leads UNKNOWN, not fabricated 0 or net ROI |
| Actual candidate creation/Trial runner and cost measurement | Tally / task-meta / Host project-owned implementation | **IMPLEMENTATION_ONLY** external to ADS; no new scheduler, optimization engine or standardized high-frequency telemetry |

## C11: economic comparability and source proof

A comparative observation MAY support a bounded numeric net effect only when source-qualified baseline and variant have the same verifier semantics, cohort definition/revision, acceptance scope and observation window, when **all** trials (including failed, cancelled, aborted, retries and censored) appear in a complete denominator, when nonoverlapping source-backed prices/counts for model/tool/CI/Host/Review/Validation/rework/recovery are complete, and when selection/confounding/cross-currency ambiguity is either controlled by real evidence or stops comparability. Missing costs are `UNKNOWN`, not `0`; `BILLED` and `ESTIMATED` overlapping scopes are not additive. Absence of witnessed matching cohorts refuses a causal or ROI claim. Even a valid comparable observed difference is **association**, not causal improvement without an appropriate design.

`net_effect` in the fixture is intentionally not a financial source standard; it is a bounded arithmetic example over explicit complete economic totals. No real bill or external provider invoice is fabricated by it.

## C13: applicability versus counterexamples

Experience applies to a new Task only if the immutable Task/ADS/profile/environment identity, task class, domain, toolchain, verifier scope and positive preconditions match a supported source, **and** all material exclusion/counterexample refs are checked; missing/stale evidence, conflicting counterexample or evaluator coverage ⇒ `MORE_EVIDENCE`, never auto-apply. A recommendation seen/applied is not proof of measured effectiveness; `CHECKED/EFFECT_OBSERVED` requires matching actual independent evidence. Private source cannot be copied to public GitHub simply because a model judged it useful.

## C14: existing Evolution classification only

For each observed item choose exactly **one** root-cause class as defined in `DEVELOPMENT_WORKFLOW.md` §8.1. Ordinary project defects never become ADS schema changes. Repeated ambiguous friction without reproducible owner evidence ⇒ `MORE_EVIDENCE` / `NO_CHANGE`. A material, verified, source-qualified and independently challenged standards gap MAY be an `ADS_EVOLUTION_CANDIDATE`, which only permits an `OPEN_ADS_INTAKE` and must then follow the normal L1→PRD→L2→Task→Review/Validation→Release chain. It is not an approved modification or Package BUILD activation. No numeric threshold or Agent ranking is authority.

## Deterministic tests and limits

Run `python scripts/test_v416_t04_evolution.py` against the actual matching PR source/fixtures. `tests/fixtures/v416/t04/scenarios.json` records positive/negative C11/C13/C14 examples with local **illustrative** classifications `COMPARABLE_OBSERVATION`, `UNKNOWN`, `APPLICABLE_EVIDENCE`, `MORE_EVIDENCE`, and existing §8 dispositions. These fixture words are **not** a new canonical ADS Event/Gate/workflow enum.

The test does **not** execute a real Task-meta collector, Tally/DomainHarness, real experiment, native GitHub permission or private source export. Real external validation #1210/#1231 remains NOT_RUN. Before source acceptance, run actual required validation and obtain an independent exact HEAD Review; only the existing owner may close T04/merge and decide carried findings.
