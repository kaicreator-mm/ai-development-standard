# ADS v4.16.0 — R7 Product Scope Delta: Traceable Version / Pivot / Revisit

**State:** \`PRODUCT_DELTA_CANDIDATE / INDEPENDENT_REVIEW_NOT_RUN / FREEZE_NOT_RUN\`. This is a **successor-overlay proposal**, not an edit to frozen R4/R5/R6 or existing T01–T06 source acceptance. **Request:** Issue [#1277](https://github.com/kaicreator-mm/ai-development-standard/issues/1277) (user-selected complete v4.16 Option B); governance parent [#1261](https://github.com/kaicreator-mm/ai-development-standard/issues/1261).

**Exact integration base at creation:** \`version/v4.16@3041a1be3f130e5cc5e676c2e56a99882adfd97c\`. Frozen R4 Product/L2 blob \`fcde65f728a87d6ecd073a37b145fdb5548367b1\`, frozen R5 \`8fe7ccc36ca96a13fd09cbcc1523fbeb70d827fb\`, frozen R6 \`ffe311927337b406a9ea8a54f717367065e43586\`; owner freeze #1261@6338348925/#6338359775; accepted 7-Task DAG blob \`2bbfc230bf7a732957ea9b1d605cf434892b062c\` and owner freeze #1261@6338768231. These artifacts stay immutable. Current R7 content must receive **new independent source Review + explicit Product and L2 delta owner acceptance, then DAG successor Review/Freeze**, rather than receiving authority by proximity to an old Freeze.

## 1. Product decision and benefit

**Goal P-R7-01.** Make the source-qualifiable *behavioral transitions* of engineering Agents and humans comparable enough that independent consumers can distinguish actual candidate selection and evaluation from merely observing shell commands, commits, retries, rollbacks, or self-described reasoning. v4.16 ADS supplies interoperable evidence semantics and an explicitly bounded GitHub-only publication projection. The product **does not** collect raw traces, infer hidden strategy intent, rank Agents automatically, schedule experimental probes, or modify canonical Task/Gate/Claim/Review state.

**Consumer:** task-meta collects/annotates private traces under its own contract and authority; ADS specifies source/identity, evidence qualification, dialect/validation and compatibility; Tally v2 may consume only already-authorized **GitHub** bounded reports and own actual strategy/learning decisions. Consumers can work with partial traces: unobservable intent, missing candidate lineage, unverifiable baseline or incomplete issue pages remain explicit \`UNKNOWN/NOT_COMPARABLE\`, never zero or an inferred success.

**Demonstrable user value.** For two versions of an identified Task with instrumented operations, independently labelled candidates and actual verifier outcomes, a reader can construct a stable state/transition sequence; distinguish genuine Pivot and **nonadjacent** Revisit from rollback/retry/stale or duplicate observations; preserve competing annotations; and decide whether a claimed outcome/cost/efficiency difference is source-comparable. Version labels must not be a direct alias for git commits or Task steps.

**Evidence context, not target threshold:** referenced TraceML research (user Issue #1277, arXiv 2608.26086) and its illustrative Kaggle frequencies are **observational research**, not proof of universal software-engineering improvements or an optimization/qualification threshold. No stipulated Pivot rate, Revisit rate, ROI or causal uplift.

## 2. Product requirements / acceptance

| ID | Required outcome | Executable acceptance and negative oracle |
| --- | --- | --- |
| P-R7-02 | Distinguish observed operation, selected immutable VersionState, candidate, transition and independent VerifierOutcome | One native tool call and one git commit do **not** automatically create one VersionState/Transition; one same-source retry/delivery never creates a Pivot |
| P-R7-03 | VersionState has stable selected material and provenance | Immutable source/tree/ChangeSet identity plus source-qualified Task/Attempt/candidate binding; no mutable refs, no timestamp-only joins. Missing selected material ⇒ not comparable |
| P-R7-04 | Pivot is a supported material strategy/verification/constraint transition, Revisit is supported nonadjacent return | Genuine A→B (Pivot) and A→B→A' with verified A/A' candidate lineage (Revisit) recognized; rollback, restart, same diff, in-place repair and stale cache are explicitly rejected |
| P-R7-05 | Observation vs non-authoritative annotation | \`OBSERVED|SELF_REPORTED|INFERRED|UNKNOWN\` claim-wise, annotator/label vocabulary revision, confidence **only if calibrated and sourced**, contradiction, human review and limitations retained. Model claims of private intent do not become OBSERVED |
| P-R7-06 | Comparisons do not reward missingness | Eligible denominator with complete/partial/unknown coverage, task/risk/cohort, baseline version, independent verifier scope, failure/aborted/censored/retries, budget/clock and parallel branch ordering; unmatched or under-covered ⇒ NOT_COMPARABLE/UNKNOWN, not uplift |
| P-R7-07 | Safe public interoperable projection through existing Report family | Optional **typed bounded** behavior evidence in existing \`ads/github/v5\` \`EXECUTION_SUMMARY\`, not ad hoc unknown keys/name strings; source PUBLISHABLE+native owner readback required; private raw trace / candidate refs not authorized to publish ⇒ withhold field/report |
| P-R7-08 | Historical/current compatibility preserved | v3 Work Item/Event, v4.15 v4 Report, Task Learning v1/v2 stay byte and semantic invariant; v5 original positive reports remain accepted after additive delta; v5-old verifier vs new-field report explicitly UNSUPPORTED/UNKNOWN under effective pin |
| P-R7-09 | Existing authority unchanged | Annotation, profile selection and improvement report do not create new machine Event/Claim/Gate, change Tally/DomainHarness permission, automatically promote Skill/ADS Evolution or bypass T07 Release Qualification |
| P-R7-10 | Source-only conformance produces falsifiable results | At least 12 positive/negative cases B01–B12 including cross-annotator disagreement, missing intermediate Version, branch concurrency and public data privacy; official strict Schema and parser regression, independent R7 source Review plus T08/T09 Reviews |

### Product journey / minimum evidence

1. A collector has *actual* versioned observation receipts + current Task/Attempt refs and selected source/tree/ChangeSet. It may produce a **VersionState** only on a source-qualified selection/commit of material; an Agent describing a plan remains SELF_REPORTED.
2. It forms **Transition** only with witnessed preceding/following selected states and causally comparable branches/attempts; concurrent branches may remain partially ordered or unknown. A source-qualified major candidate/verification/constraint change is Pivot; an evidenced later return after a **real intervening deviation** to prior candidate/equivalent lineage is Revisit. An unverified claimed return stays UNKNOWN.
3. Independent verifier evaluates actual acceptance/quality and comparable denominator/window; no verifier or non-equivalent acceptance ⇒ outcome comparison UNKNOWN, regardless of appealing trajectory.
4. An authorized publisher may reduce private evidence to optional safe v5 report \`behavior_evidence\` with explicit definition/annotation revision and qualified identity/count/denominator/limitations. Tally reads actual GitHub profile/pin/ownership; does **not** fetch task-meta private store. No report shape proves native permission, source fact, or strategy authority.

## 3. Owner boundaries and explicit non-goals

- **Already normative, reused:** \`standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md\` §10 passive observations (source-namespaced ids, attempt, clock and \`OBSERVED|SELF_REPORTED|INFERRED|UNKNOWN\`), \`standards/OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD.md\`, Task Learning v2 exact-source/counterevidence, \`standards/DEVELOPMENT_WORKFLOW.md\` §8 Evolution, T04 \`references/ADS_V416_APPLICABILITY_EVOLUTION.md\`; T01 strict v5 Report schema and T02 physical accounting/cost/watermark.
- **New narrowly owned:** BehaviorState/Transition/Pivot/Revisit *semantic* criteria (T08) and **public v5 typed optional projection** (T09) + T03 actual reader. No mandatory new provider hook, raw trace schema, private backend API, AI classifier, scheduling service, second Gate or immutable older-version rewrite.
- **External implementations remain NOT_RUN:** task-meta actual private instrumentation/annotation, Tally GitHub-only consumer/strategy selection/ROI, provider/Host live evidence #1210/#1231. These have their own Product/L2/Task authority and MUST NOT be claimed by ADS source tests.
- **No automatic product change:** the user authorization selects v4.16 planning scope, not a self-approved L1 Product Freeze or waiver of independent source Review.

## 4. Acceptance mapping, exclusions, rollout

| Concern | Already delivered | R7 added condition |
| --- | --- | --- |
| Existing v4.16 T01 Report v5 | opt-in, strict source/target/collection and publisher pin | T09 optional new member in \`EXECUTION_SUMMARY\` only; do not add report kind or retcon old v4 |
| T04 experiment/Evolution | qualified comparable outcomes and existing Intake route | Reuse; Version/Pivot counts are evidence not causal performance or auto-promotion |
| T02 and §10 timing | physical ID, cost/time/watermark basis | Use source-qualified measurements but do not infer Version sequence from elapsed time |
| T03 reader | after T02, v3/v4/v5 mixed handling | Extend only **after** T09 source update and source-verified T02; actual v5-old/new negotiation regression |
| T07 release | original C01–C16 + Agent tests, RQ | Add B01–B12 positive/negative + changed v5 source/legacy regressions, independent composed version Review |
| Existing frozen Plan | 7 Tasks, 6 native edges | Successor DAG 9 Tasks, 8 native edges proposed (T08→T09, T09→T03); preserve existing 6 (T02→T03 and T03/T04/T05/T06→T07) |

**Acyclic successor:** T08→T09→T03→T07, alongside T01→T02→T03 and T04/T05/T06→T07. Because T02 and T08 have disjoint writes, implementation MAY run in parallel **only after** successor Product/L2/DAG independent acceptance, Native Issues/dependency readback and separate legal source Claims.

**Explicit prior release restrictions:** v4.15→main PR #1211 is still Draft/conditional and v4.16 is a version branch only. v5 output remains \`CANDIDATE_ONLY\` until qualified immutable v4.16 adoption. Old raw v5 test fixtures are test subjects, not normal production publisher authority.

## 5. Independent Product review questions / freeze

1. Is this truly a bounded *standards* product (not a Tally classifier/experiment engine), and do all P-R7 requirements have falsifiable positive/negative results?
2. Does the optional v5 addition permit GitHub-only Tally interoperability without any private Trace dependency, hidden CoT or newly invented publication/Gate authority?
3. Are VersionState/Transition/Revisit intentionally **not equal** to commit history, GitHub Task state or Agent thoughts, with source-integrity and missing-coverage boundaries?
4. Is the version number and v5-new/v5-old reader compatibility/migration plan viable **before v4.16 main adoption**? Is later already-adopted v5 explicitly out of scope?
5. Is the proposed DAG T08→T09→T03 and T02→T03 safe, and are all prior completed Task source Reviews still valid for their exact historical HEAD?

**Decision slots:** \`PRODUCT_SCOPE_READY=YES|NO\`, \`P0/P1/P2\`, \`PUBLIC_WIRE_COMPAT_DECISION=ADDITIVE_PREFERRED|VERSIONED_SUCCESSOR_REQUIRED\`. **No Freeze or DAG mutation without an independent exact-HEAD Review and explicit owner decision.**
