# DomainHarness lifecycle and Agent-time retrospective (ADS v4.19 input R0)

Status: EVIDENCE / PRODUCT_INTAKE_ONLY. This is **not** an ADS normative amendment, a new gate or proof of any specific Agent's active runtime.
Captured 2026-10-27 UTC from public GitHub repository kaicreator-mm/domain-harness; authoritative underlying issue/PR identities must be rechecked if used for an exact-time conclusion.

## Scope and reproducible counts

GitHub all-state issues endpoint, sorted by creation ascending, 100 per page, pages 1–15. The endpoint mixes Issues and PRs; classify a PR only when pull_request is present. At snapshot there are **1,410 records: 845 Issues + 565 PRs**; **753 Issues closed and 92 open**. Scope is repository-wide since 2026-09-16, not one version.

- Closed Issue creation-to-close elapsed median: **approximately 2.11 hours** (753 closed Issues; median of closed_at minus created_at). **669/753** closed within 24 hours. This is workflow elapsed time, **not** measured Agent active time or user value.
- 2026-10-05: **158 Issues created**, many separated into planning/currentness/fresh-review/validation/CI-diagnosis records around v0.7. This is an issue-fragmentation indicator, **not** a claim that 158 defects or Agent runs were executed.
- **695/845 Issues without labels; 818/845 without assignees; 845/845 without milestones** in this snapshot. Body/comment event logs may still carry lawful authority; missing metadata is a discoverability problem, not automatic lack of Claim/authorization.
- v0.7 titles: **312 Issues** (302 closed, 10 open), by title version regex. Approximate only: some historical records have unmarked/multiple version references. Review-like titles are overlapping heuristic categories, not exact unique review counts.
- At snapshot **80 of 92** open Issues predate the v0.10.3 version lane. They require separate STILL_ACTIONABLE / SUPERSEDED / HISTORICAL / FUTURE classification, not bulk migration to v0.10.3.

### Timestamped examples: lead time vs actual execution

1. DomainHarness [#1013](https://github.com/kaicreator-mm/domain-harness/issues/1013), cross-component Host/Kernel/SDK integration:
   - Issue created 2026-10-11T19:53:27Z; closed 2026-10-13T12:29:57Z: **40h 36m 30s issue elapsed**.
   - One I01 Builder claim comment at [2026-10-11T20:07:43Z](https://github.com/kaicreator-mm/domain-harness/issues/1013#issuecomment-6113198491); parent builder terminal reported 2026-10-12T03:24:19Z: **7h 16m 36s of calendar span**, *not* measured active work. Multiple I01/I02/parent Agent claims and three overlapping implementation PRs were observed in the timeline; do not add these spans as exclusive per-Agent runtime.
   - Integrating [PR #1016](https://github.com/kaicreator-mm/domain-harness/pull/1016) opened 2026-10-12T03:11:22Z and merged 2026-10-13T12:29:06Z: **33h 17m 44s PR elapsed**; includes R1–R5 review, CI, waiting and repair, not 33 hours of uninterrupted Reviewer execution. No disjoint phase durations can be proven merely by subtracting these partly overlapping intervals.
2. DomainHarness [#1354](https://github.com/kaicreator-mm/domain-harness/issues/1354), v0.10.2 A5 architecture/DAG amendment, [PR #1355](https://github.com/kaicreator-mm/domain-harness/pull/1355):
   - PR created 2026-10-24T15:21:08Z; merged 2026-10-24T16:55:56Z: **1h 34m 48s end-to-end PR elapsed**.
   - Auditable issue review milestones: R1 BLOCK 15:32:30Z; R5 BLOCK 16:12:44Z; R6 BLOCK 16:35:19Z; R7 PASS 16:49:49Z. R2–R4 details may be on PR/other threads: avoid presenting count of these four timestamps as the entire review population.
   - A compressed review cycle still indicates repeated topology/manifest/BUILD decision changes; it does **not** by itself establish human/Agent overwork or wasted duration.
3. DomainHarness [#1100](https://github.com/kaicreator-mm/domain-harness/issues/1100) P0 stale admission, [#1101](https://github.com/kaicreator-mm/domain-harness/issues/1101) P1 message dedup, and [#1102](https://github.com/kaicreator-mm/domain-harness/issues/1102) P1 multiple Business acceptance identify *different* defects discovered in v0.8 post-release adversarial review; a shared source-consistency boundary merits bounded root-cause analysis, but no evidence they are the same bug or that every small repair was wrong.
4. v0.10.2 [A1 #1335](https://github.com/kaicreator-mm/domain-harness/issues/1335), [A2 #1341](https://github.com/kaicreator-mm/domain-harness/issues/1341), [A3 #1345](https://github.com/kaicreator-mm/domain-harness/issues/1345), [A4 #1352](https://github.com/kaicreator-mm/domain-harness/issues/1352), [A5 #1354](https://github.com/kaicreator-mm/domain-harness/issues/1354), [A6 #1356](https://github.com/kaicreator-mm/domain-harness/issues/1356), [A7 #1359](https://github.com/kaicreator-mm/domain-harness/issues/1359): multiple prospective amendments around dependency, generated-dist write sets, npm packaging, Node24, and source-draft/merge readiness. This warrants pre-freeze seam smoke and alternative DAG comparison, **not** treating all amendments as avoidable failure.
5. v0.10.3 downstream [#1393](https://github.com/kaicreator-mm/domain-harness/issues/1393) deployed npm Provider trust anchor and [#1394](https://github.com/kaicreator-mm/domain-harness/issues/1394) public Host CAS adapter indicate that genuine consumers can expose missing public integration proof. Different threat classes; don't conflate as a single bug.

## Measurement taxonomy: preserve epistemic status

Distinguish these without creating a second authority store:

| Metric | Meaning | Preferred source | Unsupported inference |
| --- | --- | --- | --- |
| ISSUE_LEAD_TIME | issue created → issue closed, possibly reopened | GitHub issue timestamps | Agent work duration |
| PR_LEAD_TIME | PR opened → accepted merge | GitHub PR timestamps | Reviewer duration |
| CLAIM_TO_TERMINAL_SPAN | current accepted role Claim → corresponding terminal | durable role dispatch/Claim events | continuous active execution |
| AGENT_ACTIVE_ELAPSED | summed monotonic on-task active segments for one run/Attempt, if instrumented | task-meta or provider/runner records | derived from GitHub comment gaps |
| AGENT_ACTIVE_SUM | sum of non-overlapping active segments by run across actors (agent-hours) | distinct run IDs; overlap-safe aggregator | total release wall-clock time |
| CRITICAL_PATH_ELAPSED | earliest to latest accepted dependency-complete milestone along actual DAG | canonical native DAG + timestamped events | sum of all concurrent lane durations |
| QUEUE/WAIT | Claim/review/CI/resource/human waiting, if observable | dispatch, worker and CI records | assume all silent time is waiting |
| REWORK | repeated root-class attempts/HEAD changes attributable to same accepted task | source-bound PR/review/attempt lineage | raw PR count or diff size as waste |
| CI_TIME | run start → completion (including queue only if separately labeled) | CI provider timestamps | Agent compute time |
| DELIVERY_PROGRESS | installed business journey actually executable on a qualified version | current-version real consumer/Release evidence | fraction of Issues closed |

Each derived metric MUST carry scope, source, observed vs estimated vs UNKNOWN, unit, run/attempt/actor identity when applicable, overlapping-work and missing-data qualifiers. **Missing telemetry = UNKNOWN, not zero**. No synthetic clocks, no inference from shared GitHub transport account or closed-Issue timestamps.

Recommended optional time decomposition where instrumentation exists: pre-dispatch wait; claim wait; active implementation; Review queue/active; CI queue/run; real-Host queue/run; dependency/human block; integration/rework. A segment can be UNKNOWN; no precision laundering by subtracting intervals with unknown overlapping activities.

## Cost/throughput diagnosis without metric gaming

- Count user-valued **installed journeys** and acceptance-complete version milestones alongside Issue/PR closure, Review rounds, run attempts, repeated full suites and total latency.
- A time spike or repeated R-round is a **triage signal**, not automatic FAIL/PASS, architecture amendment, or Agent penalty. Compare first divergence, root class, ownership, existing evidence reuse and real security/product significance before intervening.
- Optimize **minimum total cost to correct, reviewed, integrated, shipped behavior**, not minimum diff, issue counts, total tokens or isolated Agent speed. Long critical path can justify independent lane preparation only under lawful DAG/Claim/write-set rules; performance is never execution authority.
- The only directly observed timing in these examples is GitHub event/calendar time; no trace-proven per-Agent active compute time, token/cost totals, or provider-specific attribution was retrieved. Such values are **UNKNOWN** pending task-meta/provider trace.

## Existing ADS owners; no new generic gates

- [ADS #1341](https://github.com/kaicreator-mm/ai-development-standard/issues/1341): root class vs minimal sufficient correction; Development Workflow §4 already owns root-defect routing.
- [ADS #1320](https://github.com/kaicreator-mm/ai-development-standard/issues/1320): parallel DAG alternatives and multi-executor collaboration; Task Decomposition / Execution Architecture already own DAG/claims.
- [ADS #1337](https://github.com/kaicreator-mm/ai-development-standard/issues/1337): value-first vertical evidence and noncritical marginal risk; implementation/validation proportionality already exists.
- ADS existing Attempt/Retry/Cost and agent event identity MUST be reused; if historical timing data is missing, store observation as UNKNOWN, not a newly mandatory schema on every task.

**Intake disposition:** propose v4.19 Product R0 bounded deltas, NOT_FROZEN. The released v4.18 standards and in-flight project pins remain unchanged.