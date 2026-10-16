# ADS v4.13 — Non-Toolkit Residual Scope Optimization (L1/L2 Candidate)

> **SOURCE-ONLY / NON-NORMATIVE / NOT PRODUCT-FROZEN / NO EXECUTION OR RELEASE AUTHORITY.**  
> Planning parent: [#1147](https://github.com/kaicreator-mm/ai-development-standard/issues/1147). The separate [#1148](https://github.com/kaicreator-mm/ai-development-standard/pull/1148) covers **Organization Development Environment & Toolkit**; this document concerns **other** remaining v4.13 domains. Existing ADS source and users' declared role/agent identities remain authoritative. Do not retroactively mutate v4.12.0/v4.12.1 frozen claims or historical results.

## 1. Product direction / optimization rule

**Less new orchestration, fewer gates and less idle time; keep actual current-subject engineering truth.** Source-grounded v4.12 adoption already provides much of the material needed for v4.13:

- `standards/PROJECT_ADOPTION.md` §2.1A defines qualified released/latest-compatible **read-only** recommendations, explicit project opt-in and exact effective SHA.
- `scripts/v412_ads_compatible_select.py` is a **real** read-only implementation, not a placeholder. Its `select()` checks source/Release/compatibility evidence and project checkpoint. Do not rewrite it as a second simultaneous authority without a migration plan.
- `standards/VALIDATION_STANDARD.md` §§4–6 already separates concern/integration/closure, preserves actual runtime/profile/currentness and `VALIDATION_IMPACT_DECISION`; repeating this rule as an all-new v4.13 gate would be redundant.
- `standards/RELEASE_STANDARD.md` §11.7 and v4.12 #1143 already supply source-delivery-specific release applicability. v4.13 ADS now also ships an **actual executable toolkit**, so tests appropriate to the shipped CLI must be executed; `STANDARDS_SPECIFICATION` cannot hide untested executable behavior.
- #1099 and #1123 v4.12 scoped deltas were actually closed: risk-bounded value and self-declared actor/transport distinction are already normative. Reuse rather than reinvent.
- #1096 initially listed broad W1–W5 Product themes; *the frozen* v4.12 shipped S01–S05, not all future themes. Do not create five new independent services by default.

## 2. Priority A: #1119 — Proactive ADS updater as thin GitHub PR executor

### 2.1 Existing concrete bottleneck: blanket active-project gate

On current `main`, `scripts/v412_ads_compatible_select.py` `live_project_state()` calls both `/issues?state=open&per_page=100` and `/pulls?state=open&per_page=100`, and rejects when **any** is open (`ACTIVE_OR_UNCLASSIFIED_WORK_ITEM`). This is a **deliberately conservative fail-closed rule** in the v4.12 read-only selector, not proof that all open Issues or PRs actually share a live, conflicting Task/Claim/frozen candidate. On a constantly active organization repository it can indefinitely withhold compatible upgrade recommendations; *loosening it in place without replacing the missing source proof would be unsafe.*

**v4.13 proposal: separate prospective planning from effective pin activation.**

```text
Qualified ADS released source + proven consumer compatibility
          -> PROSPECTIVE_READ_ONLY_CANDIDATE
          -> OPTED_IN_SCOPED_CONSUMER_UPDATE_PR
          -> PR CHECKS + CURRENTNESS + PROJECT CHECKPOINT
          -> EFFECTIVE_NEW_SHA_FOR_NEW_ELIGIBLE_TASKS
          -> (if necessary) ROLLBACK_PR / NEW CHECKPOINT
```

- **Prospective discovery** may run while unrelated Issues/PRs are open, but its output has `effective_pin_changed=false`, no PASS claims about a project's Task activity, and is not an activation permission. Distinguish `OPEN_ISSUE` from `ACTIVE_CLAIM`, `FROZEN_CANDIDATE`, `CURRENT_PIN_AT_CHECKPOINT`, `CHANGED_SOURCE_SUBJECT`, `UNKNOWN` based on *actual* evidence.
- **Preparation** is bounded by per-project explicit opt-in, compatibility proof from the qualified read-only selector or a source-equivalent prospective resolver, and GitHub source readback. May create a proposed update PR **without merging or changing the effective pin**. If active work status is unknown, output `PREPARED_BUT_ACTIVATION_BLOCKED`, never a safe-to-merge assertion.
- **Activation** requires a project-compatible checkpoint and an exact current target branch `HEAD` readback/CAS; a project still running unrelated Tasks is not globally frozen simply because Issues are open. Existing Tasks/accepted Claims retain their **previous immutable ADS revision/checkout and source-specific evidence**; no cross-attempt floating-pin fallback, no retroactive Task rebinding. Any uncertainty about task source isolation, accepted Claim impact, frozen release or config scope blocks actual activation.
- **Rollback** is a new bounded project update PR from saved `old_sha,new_sha,target_branch_head` and observed effects; preserve historical PASS at original SHA without pretending it certifies rollback. `--force` overwrite, branch protection bypass, auto-merge without applicable project CI/Review and direct write to frozen Task files are forbidden.

### 2.2 Avoid a new fleet platform

Default = existing GitHub API/CLI actions invoked manually or from an opted-in existing CI workflow on **qualified Release**; periodic polling daemon, database, registry, PR bot account/Owner identity validator, organization-wide compulsory adoption and cross-project scheduler are non-goals. Use GitHub PR/Issue history as durable outcome:

- One idempotency identity e.g. `(consumer_repo, target_base_head, old_ads_sha, new_ads_sha, adoption_policy_revision)`, plus search/readback of actual existing PRs; prevent duplicate or stale branches. Distinguish `PR_EXISTS`, `CREATED`, `MERGED`, `DECLINED`, `BLOCKED`, `NOT_RUN`.
- Explicit opt-in from authoritative project adoption settings; read-only organizational inventory may suggest candidates but **cannot** silently consent for individual projects. Default write set: only effective `.dev-standard/VERSION` and explicitly generated ADS-owned docs if required. `PROJECT_OVERRIDES.md`, project lockfiles, frozen PRD/L2/DAG, currently accepted Claims and unrelated code untouched.
- GitHub pagination, permission failures, ETag/revision currentness, PR dedup, target base branch (not always `main`), rate limit/backoff and branch protection are observed facts. One project rejected/blocked does not prevent others from receiving *accurate* independent results.
- **Generalize Release evidence seam only where needed**: v4.12 S05 hardcodes several version-specific source/Issue/event proof details (the function `qualified_integrated_release` reasons over S06-specific event names and `candidate_sha`, `candidate_tree`, `release_verdict`). A future-v4.13 source-qualified release may need different reference events. Define a small read-only *version-generic verified release proof projection* with precise raw source refs instead of copy-pasting a second giant GitHub proof parser; prove both the v4.12 baseline and a future candidate. `PUBLISHED_TAG` or `CI_SUCCESS` alone never suffices.

**Renovate option**: [Renovate regex custom managers](https://docs.renovatebot.com/modules/manager/regex/) can prepare PRs for version-like text; [Renovate organization autodiscovery](https://docs.renovatebot.com/getting-started/installing-onboarding/) supports installed repositories. But its ordinary dependency/version matching and automerge do **not** prove ADS's material `actor/authority/Claim/Review/Release` compatibility. Prefer a tiny native GitHub updater for the one special ADS pin; consider Renovate solely as an optional **PR generation transport** after ADS has independently produced a verified immutable upgrade decision. Do not install a separate organization-wide Renovate daemon solely for ADS unless actual operating cost/benefit is shown.

## 3. Priority B: #1116 — Delivery capabilities, not six new verification engines

Retain the **delivery artifact types** as informative categories, but derive gate applicability from two orthogonal dimensions:

1. **What is really shipped?** `NORMATIVE_SPEC`, `EXECUTABLE_LIBRARY_OR_CLI`, `SERVICE_OR_APP`, `HARDWARE_OR_EXTERNAL_EFFECT` may coexist. Do not let a mixed ADS standards+Toolkit product call everything documentation.
2. **What real capabilities and guarantees are promised?** Contract/schema, import/call API, command-line, platform-specific build/install, host/remote runtime, irreversible/external/physical side effects, auth/permissions, compatibility/upgrade, actual packaging. Frozen Product/L2/Project requirements control which are `REQUIRED`.

Generate a **small coverage-to-evidence view**, not a new full per-type state machine:

| Shipped capability | Minimal representative evidence | Must not be inferred |
|---|---|---|
| Normative docs/contracts/schema | Internal source/manifest coherence, deterministic impact-aware positive/negative examples | Real deployed user/effect/authority PASS |
| Executable CLI/SDK | Actual entrypoint/API check, necessary runtime/toolchain tuple and affected negative tests | A docs-only static check certifies CLI |
| Local filesystem/Git/env mutation | Actual temp-workspace write/rollback/safety/collision and path containment tests | Synthetic fixture proves real host behavior |
| Service/remote/physical effects when actually promised | The applicable real host/endpoint/negative boundaries | A local mock is external E3 PASS |
| Packaged binary/distribution when actually promised | Applicable package/install/launch check | Standard docs repository automatically ships a package |

One `required obligation -> exact subject/environment -> executed assertion/exit/skip -> gate` projection can satisfy multiple existing evidence consumers **only for identical actual predicates and valid exact-currentness**. `NOT_RUN/NOT_APPLICABLE` remain different; a skipped test is not PASS.

**Version cadence**: `SELF_COHERENCE` and `SELF_DOGFOOD` plus existing applicable Release Qualification precede ADS release; `FIELD_VALIDATION` is postrelease feedback unless frozen Product specifically requires it earlier. Do not add three new Gate states or delay standards+CLI release for mandatory synchronized domain-harness/runx/xDownload pilots. A tool that was changed after proof gets affected recheck; a tiny repair gets bounded delta review; one final candidate-level required regression suffices when no new required failure class exists. Prefer one local-versus-CI execution budget and reuse actual exits, preserving final Release truth.

**Candidate implementation**: a concise delta under existing `VALIDATION_STANDARD.md` and `RELEASE_STANDARD.md`, plus a handful of positive/negative cases. Only introduce a machine schema/template if an actual consumer cannot operate with existing evidence formats. **No six implementations or mandatory six-type matrix.**

## 4. Priority C: W1 — one graph source, conditional views, bounded JIT

The shipped ADS `DEVELOPMENT_WORKFLOW.md` and `TASK_DAG_GOVERNANCE_STANDARD.md` already own phase sequencing and implementation Issue dependencies. #1100's `DAG-P/DAG-A/DAG-I` design should be **projection behavior** not an obligatory file/db per phase:

| Work pattern | Recommended mode | Stop/materialization condition |
|---|---|---|
| Straightforward correction / single bounded Task | `INLINE` or existing Fast Path | No empty P/A DAG just for traceability |
| Several Product questions or L2 alternatives | `BOUNDED_WORKLIST` with refs and outcomes | Stop at sufficient Product/L2 decision; do not recursively build research DAG |
| Real multi-owner dependencies with concurrent changes | `EXPLICIT_DAG` when justified, existing GitHub Issue Dependencies for materialized implementation tasks | Preserve one canonical source and exact task identity; planning projections never count as native blocked_by |

**Project Steward W2** should be a read-only `ads status/explain` reducer over Issue/PR/CI/current source, listing actual `READY`, `STALLED`, `BLOCKED`, `UNKNOWN`, outdated review and material critical-path issues. It **cannot** create a second task state, issue-dependency store or assign Claim without existing authorized controller action. An optional existing GitHub Actions [reusable workflow](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows) can produce a snapshot if needed; never force a continuously running steward service. GitHub [Issue Dependencies API](https://docs.github.com/en/rest/issues/issue-dependencies) supports read-only native blocker observation; do not derive blocker status just from text or age. Project alerting/follow-up only when someone opts in; no progress % without real denominator/evidence.

**W3 environment lifecycle** belongs to #1148 toolkit design, not a separate W3 engine here. Reuse its `env explain/doctor` outputs. Don't double-build a platform matrix in Steward.

## 5. Priority D: W4/W5 — selective material learning, not telemetry infrastructure

Keep existing Task Result/Task Learning source owners; prefer one compact durable Issue/PR outcome record when there is **materially reusable knowledge**:

```text
subject + exact SHA + changed decision
what failed / why + reproducible evidence
verified remedy / regression test + applicable scope
status=PROVEN|SUPPORTED|HYPOTHESIS + counterexample
reuse instruction or stop/defer trigger
```

- **No record** for routine trivial PASS without novel insight; no user-invisible new DB, training daemon, permanent Agent transcript archive, generic prompt spam or mandatory human author/reviewer.
- L1/L2 prior-art and pattern harvest are **conditional**. Distinguish reference-license/provenance and actual executable test. Research ends when enough current reliable evidence exists to choose; new tools/LLM reviews only for new material uncertainty.
- Operational measures (duplicate validation invocation, PR merge latency, number of genuine blocked critical-path tasks, actual host reruns, field defect) are **computed from observed GitHub/CI/Host facts**. UNKNOWN is unknown; no fabricated ROI or required always-on tracking.
- New candidate ADS standard revisions require specific recurring failure class/impact/reproducer. Single-project local optimization should normally be a project override first, not immediate compulsory global normative rule.

## 6. Reconciliation and scope pruning (critical-path order)

| Original proposed v4.13 or v4.12 legacy theme | Proposed v4.13 status | Existing source | Scope discipline |
|---|---|---|---|
| v4.12 latest-compatible selector | **REUSE_AS_IS_OR_MINIMAL_BOUNDARY_ADAPTER** | S04/S05, `scripts/v412_ads_compatible_select.py` | Do not refactor whole verifier as new authority |
| #1119 actual cross-project update/rollback | **IMPLEMENT_MINIMAL** | #1119, `PROJECT_ADOPTION.md` | One core updater concern + focused safe activation tests |
| #1116 standards-repo self-verification | **ALREADY_IMPLEMENTED_FOR_ADS_V412** | Release §11.7, #1143 | No invented extra Owner/E3 gate |
| #1116 general multi-delivery applicability | **ADOPT_BOUNDED_DELTA** | Validation/Release Standards | Compact capability-to-proof policy; no six separate validators |
| #1100 conditional L1/L2 DAG | **REUSE/ONLY IF MATERIAL_GAP** | Workflow/Task DAG norms | No new universal three-DAG artifacts |
| W2 Project Steward | **READ_ONLY_OPTIONAL** | Existing GitHub native Issue/PR/CI state | No new scheduler/daemon |
| W3 Environment Lifecycle | **IN #1148 TOOLKIT** | devkit + existing tooling standards | No overlapping Task/PR or Platform service |
| W4 Task Learning | **REUSE_EXISTING** | existing Task Learning norms / Issue comments | Material-only concise records |
| W5 research reuse/ROI | **REUSE_EXISTING/OPTIONAL** | #1099, existing L1/L2 evidence | No mandatory competitor study |
| Self-declared logical actors / no GitHub-username gate | **ALREADY_DONE v4.12** | #1123 resolved | No identity reenrollment |
| Cross-project field feedback | **POSTRELEASE CONTINUOUS** | #1116 lifecycle | Not a release blocker by default |

## 7. Small falsifiable acceptance set — candidate only, NOT_RUN

| ID | Required result | Negative proof / forbidden shortcut |
|---|---|---|
| U01 | A qualified compatible release can be discovered and an update **PR prepared** while unrelated issues remain open | Do not auto-activate a new pin while accepted Task snapshot/freeze impact is unknown |
| U02 | Existing Task remains on previously immutable ADS revision after a future-compatible PR opens | No silent runtime switch or historical evidence re-label |
| U03 | Update PR deduplicates per project and exact old/new SHA and declines stale base/permissions | No duplicate PR storm, `main/latest` or direct protected branch writes |
| U04 | New version Proof references actual release/current test outcomes with generic source-bound parsing | Never accept same semver, tag, plain green CI or self-declared compatibility as qualified |
| U05 | A standards-only project has applicable source checks while a standards+CLI package has real CLI tests | No false `NOT_APPLICABLE` on an actual shipped executable |
| U06 | Same executed log covers multiple owner obligations when actual assertions/current tuple coincide | No automatic repeat of full suite per Gate label, skip != PASS |
| U07 | A small simple issue uses Fast Path with no empty L1/L2 DAG | High-impact dependency case cannot avoid required GitHub blocked_by edge |
| U08 | Read-only Steward reports live blockers/currentness and separates provider PENDING from FAIL | No stale textual Issue blocker presented as native dependency |
| U09 | Task metadata produced only for a reproducible material lesson with exact source | No mandatory per-Task telemetry/knowledge database or fake model cost |
| U10 | ADS qualifies after coherence + actual self-dogfood + applicable Release checks, real projects provide subsequent feedback | No required synchronized external adopter releases unless frozen Product explicitly calls for it |
| U11 | New Product scope uses risk-bounded stop decisions with concrete user-value tradeoff | No recursive Review R1–R8 / full CI loop without a new material failure class |

## 8. Suggested Task DAG impact — reuse parent #1147 concerns

No new native Issue/Task/Gate is created by this design; **DO NOT predeclare these as executable until Product/L2 Freeze**.

- Reuse #1147 **C05/#1119**: one source-bounded multi-repo updater/rollback concern; retain v4.12 read-only selector, add prospective-vs-activation separation, version-generic release proof seam only if needed.
- Reuse **C06/#1116**: one small capability-based type-aware validation/release normative delta. Coalesce into C04 or mark already satisfied if implementation review proves it.
- **W1/W2/W4/W5**: no automatic independent implementation concerns; adopt a small reusable status/projection or standard wording **only if** a real material source gap cannot be met with current GitHub queries and shipped standards.
- **C02–C04** organization Toolkit remain **#1148's** separate design; do not expand that PR.
- Final actual shipped ADS Toolkit needs real targeted executable tests in addition to standards source self-check; one final candidate regression, independent review as applicable, Release Qualification, postrelease consumer evidence follow-on.

## 9. L2 decisions and proof still needed

1. **Selector seam:** decide whether read-only `v412_ads_compatible_select.py` can expose a genuinely source-equivalent qualified-release/compatibility recommendation for *prospective PR preparation* without falsely passing its strict activation-readiness checkpoint; otherwise create a small separate preview plan that still fails closed on missing immutable Release/compatibility evidence.
2. **Task activity:** use project/source native Issue Dependency/Claim/frozen Candidate evidence (not generic open Issue count) for actual activation. Unknown material status holds activation; no forged safe status.
3. **Renovate vs native GitHub writer:** quick cost/safety check. Choose native small writer unless organization already operates Renovate and exact-SHA policy can be inserted without adding a second verification authority.
4. **Capability applicability:** clarify standards+Toolkit product split, real Windows/Linux commands/host checks, and existing validation evidence projection. Do not regress risk-required independent Review or release currentness.
5. **Field feedback:** pick one or two actual consumer examples for after release, with no mandatory completion before qualified ADS source release.

### Reference links

- ADS: [#1147](https://github.com/kaicreator-mm/ai-development-standard/issues/1147), [#1119](https://github.com/kaicreator-mm/ai-development-standard/issues/1119), [#1116](https://github.com/kaicreator-mm/ai-development-standard/issues/1116), [#1100](https://github.com/kaicreator-mm/ai-development-standard/issues/1100); source `scripts/v412_ads_compatible_select.py`, `standards/PROJECT_ADOPTION.md`, `standards/VALIDATION_STANDARD.md`, `standards/RELEASE_STANDARD.md`.
- External capability background: [Renovate regex manager](https://docs.renovatebot.com/modules/manager/regex/); [Renovate onboarding](https://docs.renovatebot.com/getting-started/installing-onboarding/); [GitHub REST issue dependencies](https://docs.github.com/en/rest/issues/issue-dependencies); [GitHub reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).

**Verdict:** `ADOPT_BOUNDED_CORE_DELTA` for #1119 and genuinely missing #1116 rules. `REUSE/OPTIONAL/DEFER` for other already-covered themes. No second platform, second source of truth, repeated full-root tests, identity/Owner gate, or automatic downgrade of material engineering proof.
