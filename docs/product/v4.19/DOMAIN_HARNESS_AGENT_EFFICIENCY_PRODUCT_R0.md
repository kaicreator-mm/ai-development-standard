# ADS v4.19 Product/L1 R0 — Agent execution efficiency and root-cause-led delivery

Status: **DRAFT / NOT_FROZEN / NO_L2_OR_TASK_AUTHORIZATION**  
Version target: **v4.19.0**. Source: [ADS #1341](https://github.com/kaicreator-mm/ai-development-standard/issues/1341), [#1320](https://github.com/kaicreator-mm/ai-development-standard/issues/1320), [#1337](https://github.com/kaicreator-mm/ai-development-standard/issues/1337), [DomainHarness retrospective](../../intake/2026-10-27-domain-harness-agent-time-audit.md).  
Effective release: **ADS v4.18.0**, unchanged. This is a prospective Product candidate, not a standards update or a license to change live project gates.

## 1. Problem and user-visible goal

The observed failure mode is **high internal activity with delayed usable completion**: narrow repair PRs, repeated review/currentness/CI cycles, after-freeze DAG amendments, and Agent idle or coordination time can consume capacity even though each individual step follows the rules. Conversely, a short PR or quick Issue close does not prove that a real Domain App/SDK installed journey works.

The version goal is to **increase the fraction of time and attempts spent on the actual user's necessary delivery path while preserving correct source and security evidence**. Repair decisions should minimize *total* evidence-supported engineering, review, CI, integration and future maintenance cost, not just patch size.

This is a bounded change to *decision quality and evidence interpretation*, not a new scheduler, task-meta product, review gate or automatic optimization policy.

## 2. Baseline owner/crosswalk (do not duplicate existing normative rules)

| Existing owner / rule | Already covered | Proposed v4.19 incremental gap |
| --- | --- | --- |
| DEVELOPMENT_WORKFLOW.md §4 Repair routing and Non-converging repair | root defect class, falsifiable convergence, cross-owner routing, no unbounded retry | Compare plausible **repair levels/alternatives** and identify repeated cross-boundary symptoms before choosing smallest file diff |
| DEVELOPMENT_WORKFLOW.md Stage 2.4/4 and Stage 7 | risk-sensitive DAG, scoped tests, proportional Review, JIT branches | Forecast major **handoff/queue/integration latency** and prove user-valued vertical path, not just file ownership and gates |
| TASK_DECOMPOSITION_STANDARD.md §§3–14 | minimum coherent concern, maximal safe parallelism, alternative topology, atomicity, explicit integration | Compare **coordination overhead vs parallel benefit**; avoid creating many independent tracking Issues for one invariant or the same review delta |
| EXECUTION_ARCHITECTURE_STANDARD.md §6/7/11 | canonical native DAG/ready sets/Claim, concern-integration-closure validation levels | Distinguish ready code lanes from expensive Reviewer/CI/Host **waiting lanes** without introducing a second queue or granting unauthorized early writes |
| GITHUB_AGENT_INTERACTION_PROTOCOL.md + agent-event-v2 | actor / operator / session / attempt source; accepted Claim/terminal semantics | Map optional **actual execution time** to existing identity and support UNKNOWN when traces absent; GitHub lifespan alone insufficient |
| Existing v4.16 Attempt/Retry/Cost/Report work and task-meta | identity and effort/cost evidence infrastructure | Require honest **cross-source metric semantics and overlap/coverage disclaimers**; no duplicate time schema or counting shared transport users as individual agents |
| Existing release/validation and CI evidence owners | exact SHA, CI run IDs, real platform/Hidden/Release qualification | Distinguish CI queued/run vs agent runtime; reuse valid scoped evidence; never translate slow/missing telemetry into gate status |

**Priority:** implement only a verified normative delta. If an outcome is already covered and failed in practice, use example/tooling/dogfood rather than restating the same MUST in another standard.

## 3. Product requirements (candidate)

### R01 — Repair level selected by root cause, not write-set size (P1)

For a materially cross-component, public ABI, state consistency or recurring root-class defect, the repair owner SHOULD record in the **existing Issue/PR**: first divergence or falsifiable causal hypothesis; owning architecture/contract/implementation/environment boundary; user-visible impact; and brief choice among LOCAL_FIX, SHARED_ADAPTER/DEPENDENCY, CONTRACT_AMENDMENT/REFACTOR or DEFER/KNOWN_LIMITATION (only where permitted). The comparison must include affected consumers, regression/security impact, Review/CI/Host cost and expected future maintenance.

Do not mandate architectural review for a one-line, proven local bug. If cause remains UNKNOWN and the path is material, route to existing owner; never let a Builder silently rewrite frozen Product/L2/write sets. Same-root nonconvergence already has a standard escalation route; v4.19 clarifies **what evidence informs** that route instead of inventing another mandatory gate.

### R02 — Time dimensions are distinct, source-bound, and UNKNOWN-safe (P1)

When timing is used to justify dispatch, Task splitting, model routing or process changes, classify the metric correctly:

- **Lead time**: Issue create→close or PR open→merge, with event timestamp provenance; not agent compute.
- **Agent active wall time**: measured on-task active segments per operator/session/run/attempt, optionally observed via task-meta/real tool/runner trace. Do not infer from GitHub comments/Claim gap. Multiple parallel Agents may have summed active agent-hours greater than end-to-end wall time.
- **Queue/wait**: review, CI, dependency, human authorization, external provider or Host resource waiting **only where observable**. Silence is not automatically WAIT.
- **Validation/CI**: provider run queue and execution durations where available; not Agent runtime.
- **Rework**: repeated root-class attempts, currentness invalidation, re-review and re-running tests (must be tied to the same subject/lineage).
- **Delivered value**: installed/real consumer journey acceptance on current exact candidate, independent of task count.

Carry existing task/dispatch/attempt/operator/subject SHA refs, time source, observation window, units and measured/estimated/UNKNOWN classification. Missing start/end, suspended sessions, or untracked local execution remains **UNKNOWN**, never 0, PASS, FAIL or human/Agent fault.

**No requirement** to track every short task manually, buy a tracing backend or expose private transcripts/raw tokens. Structured metrics can be a project-local derived view. No new authority state, obligatory per-Task timing evidence, or universal SLA.

### R03 — Bottleneck-first DAG and Agent selection (P1)

For a *material* proposed DAG, the planner SHOULD evaluate actual high-risk seams, the alternative safe topology, and major **expected wait/critical-path risks**. Distinguish dependencies caused by integrated source, shared write sets, independent Review/Validation, external Host and merge/release convergence. Use measured history when genuinely comparable; otherwise mark duration UNKNOWN and compare topology qualitatively.

A small Task is not automatically efficient; splitting one coherent invariant into separate planning/review/CI/repair Issues can increase handoff and integration lead time. Preserve one Issue/PR for one stable concern, append review attempts and evidence to its PR/Issue, and create a separate Issue only when new independent scope, real authority or reusable defect requires it. Do not hide legitimate independent review by collapsing roles.

Release-determined critical path should be reported alongside ready-to-run independent lanes; idle while waiting for a gate is not a reason to forge READY, relax Claim or create long-lived branches. A controller MAY legally dispatch other independent work with accepted Claim and safe write ownership.

### R04 — Vertical value and right-sized assurance (P1)

For substantial implementation work, capture at least one actual user journey and minimal representative consumer/effect/terminal. Independent component/unit/CI PASS is enabling evidence, not shipped capability.

Place concern-level deltas at leaf, cross-seam proof at integration, required full/Hidden/physical at version closure. Do not rerun expensive full suites on every unchanged short repair without a materially affected validation tuple. Security/authority/correctness-critical intrinsic tests still run as required.

When repetitive R-rounds or Issue proliferation produce no new user-facing acceptance, inspect cause and value before adding another seam or adversarial edge. Legal owner may defer supported noncritical P2/P3 scenarios with limitations; cannot waive confirmed auth bypass, wrong-target non-idempotent effects, cross-tenant data/secret leakage or a frozen required gate for time/cost savings.

### R05 — Agent time used for learning, not gamed as productivity (P2)

Where available, optional per-run evidence SHOULD answer: which concern/attempt, actual agent/provider/model (under existing identity semantics), how long active, which category of wait, which exact source/Review/CI witness, and what delivery outcome? Use **per comparable task type/complexity and evidence level**, not raw global agent leaderboards.

Useful comparison:
- end-to-end version/critical-path elapsed;
- sum of active Agent time across parallel runs, NOT the same as elapsed;
- observed wait-to-work ratio only when numerator and denominator both measured;
- valid re-review/CI reuse;
- corrective attempts by shared root cause;
- integration-ready and installed journeys.

Do not penalize cautious independent Reviewers or incentivize skipping negatives. Token/cost/time optimization is *subordinate* to gate/role/authorization truth.

### R06 — Historical backlog source-quality and useful project status (P2)

Historical open Issue is not automatically current blocker. At version intake or when history materially affects routing, classify candidate as ACTIONABLE_CURRENT / SUPERSEDED / HISTORICAL_EVIDENCE / FUTURE_PROPOSAL or UNKNOWN, link successor and current-version reproduction when necessary. **Advisory classification**; do not mass-close or rewrite existing authority, and do not create duplicate Jira-like tracking schema or new gate.

Display project progress at minimum as *business acceptance + true critical blockers + optional count of completed Tasks*; avoid an isolated changing numerator/denominator as the only status.

## 4. Four differentiated golden/practice scenarios

| Case | Expected safe outcome | Reject |
| --- | --- | --- |
| Known one-function bug with direct regression | LOCAL_FIX + affected tests and applicable existing Review | mandatory new Architecture Review or formal L2 amendment |
| DomainHarness #1013: 40.6h Issue span, 7.3h Claim→Builder-terminal span, overlapping builders | report three different elapsed concepts; **Agent active UNKNOWN** without trace; root-class/PR/CI review breakdown when evidence exists | label 40.6h or 7.3h as “Agent worked continuously”; sum overlapping intervals as serial critical path |
| DomainHarness #1354 A5 repeated R1–R7 on one short PR | reason about manifest/BUILD/Node/public contract and lawful owner; reuse exact evidence, examine alternative DAG | another identical-scope patch/review gate as progress; or automatic waiver after N rounds |
| DomainHarness #1393 provider trust anchor; #1394 CAS consumer shape | separate architectural trust risk from doc/adapter DX; compare actual lower-cost correction with real consumer test | global refactor simply because APIs differ, or scattered hashes as supply-chain guarantee without trust anchor |
| v0.7 158 Issues/day & v0.10.2 A1–A7 | stable concern, grouped reviews, legitimate shared integration owner, critical journey evidence | “more closed Issues = greater release progress”; every Reviewer note becomes a new Task |
| CI host git-lfs failure #782 vs code defect | ENVIRONMENT issue and appropriate provider rerun/alternate evidence; CI wait separate | product-code patch or Agent performance penalty for runner failure |

## 5. Acceptance and falsification before normative promotion

1. ADS owners map each R01–R06 to an existing section and mark **ALREADY_COVERED / DOC_OR_TOOLING_ONLY / NORMATIVE_DELTA**. No blanket new stage, schema or gate.
2. Independent R0 Product Review challenges selected time calculations, source provenance, real Agent time availability, overlap, and claims about correlation vs causality.
3. Demonstrate the six golden scenarios on retained source-bound evidence with a counterexample where minimal local fix wins. All preserved v4.18 role/Claim/frozen/L2/CI/Review/Hidden/Release invariants must still apply.
4. Test counterfactuals: absence of active timing -> UNKNOWN (not zero); PR merged with no installed consumer -> not shipped; waiting review does not authorize edit; non-critical deferred edge cannot suppress current required P0/P1/security gate.
5. If normalized optional telemetry is useful, **prefer consumption/adaptation of existing task-meta/Agent event/Attempt records**. A separate task to add storage, schema or automated timers requires explicit evidence of a real consumer gap and a separate accepted authority decision.
6. Pilot on at least one new version/Task DAG with measured available data; report what was saved only when captured, otherwise report NOT_MEASURED. This is evidence for prospective refinement, not a retroactive release bar.

## 6. Non-goals / hard boundaries

- Do not mandate manual timekeeping or equal time budget per Agent. Do not treat calendar elapsed as token spend or active execution.
- Do not introduce a second scheduler/queue/Claim/event schema, general timer service, universal timeout, retry cap, score threshold or mandatory optimization gate.
- Do not redefine Agent roles, independent Reviewer truth, source permissions, required platform tests, product trust boundary, or standard pin from a timing metric.
- Do not ban small patches, force architecture rewrites, or weaken existing required gates.
- Do not edit released v4.18 in-place or modify already frozen downstream project authorities.
- Do not turn this draft into a normative standard before the usual Product → L2 (if needed) → Task/Review/Validation decision. When only advice/examples are missing, prefer a bounded document/Golden example over normative edits.

## 7. Proposed owner routing for next ADS step

Review [ADS #1341](https://github.com/kaicreator-mm/ai-development-standard/issues/1341) as Product intake owner. Absorb timing evidence into that same version's scope; cross-reference [#1320](https://github.com/kaicreator-mm/ai-development-standard/issues/1320) and [#1337](https://github.com/kaicreator-mm/ai-development-standard/issues/1337). After independent R0 Product delta review, freeze Product only if authorized, then draft the smallest existing-owner standard changes or documentary examples. **The v4.19 feature/proposal branch is for review, not main integration.**
