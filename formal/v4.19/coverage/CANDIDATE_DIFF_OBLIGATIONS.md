# ADS #1366 — Candidate-delta rule obligations triage (source-first)

**Authority / scope:** PR #1365 candidate HEAD `dac263fa4c0ab155406d2f2117459b34322cc988` (OPEN, not frozen, not normative effective ADS); R11 already strict-qualified 35/35 model + 61/61 Python at exact model HEAD `9a6fb6f5...` as frozen at `a501dead1ab0b44c3cb460f891a1a7ff47cba8d2`. No need to rerun those exact tests after adding data-only coverage evidence.

## What changed in execution strategy

R11's full Exact-SHA acceptance has **already passed**; repeating it or issuing a Local validation-only handoff would waste execution. Stop generating unbounded Demo batches and move to **source-grounded, risk-first rule obligations**. Formalization is warranted only when a falsifiable cross-rule invariant adds evidence beyond existing native validation.

The `standard-manifest.json` enumerates **46 normative documents** for the observed candidate/base inventory. Exactly **7** normative documents have changed Git blobs. This is a deliberately **curated 21-item review shortlist** across those seven source files, representing **16 concern families**: it is *not* an exhaustive list of atomic candidate obligations, still less a count of all ADS rules. Global clause denominator remains **UNKNOWN**.

Every item in `candidate-delta-obligations.json` binds to exact source Git blob, candidate line, and an exact text anchor **confirmed to be newly added by the PR #1365 patch** (not inferred from a filename). Deterministic structural cross-readback passed, including four corrupted-item mutants rejected. Such metadata checks are **not a semantic proof**.

## Evidence tiers (not interchangeable)

| Evidence tier | Curated items | What it actually establishes |
|---|---:|---|
| `SYNTHETIC_PYTHON_DEMO_ONLY` | 4 | The bounded discovery/false-serial demos expose a selected failure pattern, without real host native DAG/consumer coverage |
| `ABSTRACT_PILOT_ONLY` | 3 | Older R11 Authority/Evolution model is relevant background, **not a clause-equivalence proof** |
| `NOT_TESTED` | 14 | Exact source anchor exists, but no direct behavioral demonstration is claimed |

Risk prioritization (for audit scheduling, **not defect counts**): **15 HIGH**, **5 MEDIUM**, **1 LOW**.

## Focused review order

**1. Profile/Dispatch authority + historically frozen admission.** `EXEC-01/02`, `GITHUB-01/02`; cross-read candidate `EXECUTION_PACK_STANDARD`, `GITHUB_AGENT_INTERACTION_PROTOCOL` and the dispatch schema. This is the first reasonable **semantic model-gap review**, not an automatic new SMT model. Determine concrete exact authority/version exceptions first.

**2. Selected public behavior + retained invariants.** `ARCH-01/02/03`, `IMPL-01/02`, `TEST-03`. The new source demands observable end-to-end behavior; do **not** claim that import/export/load or a synthetic proof certifies real Host/consumer routing. Needs a real public consumer source and selected-path evidence.

**3. Actual test inventory and Task DAG decisions.** `TEST-01/02`, `TASK-01/02/03/04`. Existing Python demos prove only synthetic negative/positive distinctions; native GitHub Issue Dependencies, actual CI test collection, accepted Claim and true DAG topology remain separate unproved obligations. No automatic dependency mutation.

**4. Product research and bounded repair ownership.** `DEV-01..05`: versioned Issue+Git research references, honest NOT_RUN and correct Stage 1/2/Gate ownership, and reuse of causal repair lineage. Initially source review / exact historical evidence is more valuable than a new symbolic test.

### Prohibitions and next acceptance

- Do not extrapolate 21 curated items into a completed atomic obligation census; the full denominator is unknown.
- Do not count one `35/35` R11 model result as discharging every new candidate clause.
- Do not create 21 separate Task Issues or synthetic SMT formulae.
- Next active work should review the first authority-profile cross-rule family with actual candidate schema/source anchors and produce a specific accept/revise/unknown disposition; if no model contradiction arises, retain `NOT_PROVEN`.
- No Merge/Freeze/Release/CI Gate/Actions or change to ADS normative standards in this experimental branch.

**Machine evidence:** `candidate-delta-obligations.json`.
