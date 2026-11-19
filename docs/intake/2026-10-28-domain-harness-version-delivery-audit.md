# DomainHarness cross-version delivery-chain audit — ADS v4.19 evidence R0

**Status:** comparative retrospective; PROSPECTIVE ADS intake only, **not normative**, not a gate, not an authorization to mutate DomainHarness code or frozen v4.18 authority. Snapshot 2026-10-27/28.  
**Subject:** \`kaicreator-mm/domain-harness\` GitHub Issues / PRs across v0.1–v0.10.3.  
**Related:** [ADS v4.19 Product R0](../product/v4.19/DOMAIN_HARNESS_AGENT_EFFICIENCY_PRODUCT_R0.md), [time/issue measurements](2026-10-27-domain-harness-agent-time-audit.md), [ADS #1341](https://github.com/kaicreator-mm/ai-development-standard/issues/1341), [#1320](https://github.com/kaicreator-mm/ai-development-standard/issues/1320), [#1337](https://github.com/kaicreator-mm/ai-development-standard/issues/1337).

## 1. Evaluation frame: one version as a causal delivery chain

For each version, separate six evidence layers:

\`Product/retained behavior → L2/contract & dependency hypotheses → Task DAG/write-set/Agent allocation → code+test+real consumer → Review/CI & finding lineage → repair/integration/Closure & escaped regressions\`.

Record **first divergence**: when was the first fact available that should have changed the plan? Do **not** automatically classify a late defect as proof that original Task decomposition was wrong, or that an independent reviewer was ineffective. A defect can be first observable only when real integration or independent adversarial execution becomes available.

Summarize **avoidable coordination** separately from **necessary correctness work**. Compare design-source fixes, physical test fixes, normal implementation repairs, truly material L2 amendments, and environment failures. An issue can span multiple phases; Issue count is not defect count, labor time, or shipped value.

## 2. Snapshot: version-labelled Issues and version-target PRs

Counts obtained from GitHub REST \`/issues?state=all&per_page=100&page=1..15\` (1,410 entries, split 845 non-PR Issues and 565 PR entries), and \`/pulls?state=all&per_page=100&page=1..6\` (565 PRs); per-version Issue classification is the **first explicit v0.x in issue title**, PR classification by **actual base branch** where version-named. Hence the columns are *not guaranteed to cover exactly the same concerns*. A scope may have multiple Issues/PRs or no explicit version marker; v0.8 "V08" and v0.8.1 titles sometimes classify under v0.8; main and experimental-base PRs excluded. OPEN/CLOSED pertains only to Issue status at snapshot. The following values are evidence-routing signals, not throughput rankings.

| Labelled version | Issues by title | PRs targeting version branch | Working hypothesis from sampled work |
| --- | ---: | ---: | --- |
| v0.1 | 9 | 31 | bootstrap and release/documentation evidence; #39 release closure remains open, do not infer readiness from open status alone |
| v0.2 | 47 | 38 | durable runtime crash/dedup and portable package root caught in review; canonical test discovery coverage gap |
| v0.3 | 86 | 63 | downstream domain-consumer contracts exposed SDK gaps; late compatibility/requalification drift and long-lived backlog |
| v0.4 | 46 | 16 | review/repair process dominates titled work; governance/CI version currentness discovered at closure |
| v0.5 | 0 (title-based) | 2 | **insufficient sampling**: issue title classification does not capture this release's full scope; no strong conclusion about its quality or velocity |
| v0.6 | 47 | 16 | v0.5 carryover, L2 claims of already-integrated code contradicted source, platform/evidence handoff |
| v0.7 | 312 | 93 | extreme task/review/currentness fragmentation, genuine parallelism progress and excess coordination risk |
| v0.8 | 39 explicit "v0.8" titles | 67 | component PRs merged without executable composition; P0/P1 escaped to post-release review |
| v0.8.1 | titles mostly matched v0.8 | 3 | high-severity bounded hotfixes of independently reproduced v0.8 regressions |
| v0.9 | 14 | 39 | explicit product scope narrowing to JS/TS core rather than global OS matrix; focused version validation |
| v0.10 | 53 | 78 | frozen Product→production code mismatch in Hook/Facade/Decision; whole-version review catches coverage gaps |
| v0.10.1 | 13 | 16 | constrained Standard Feature successor, reused retained exact-SHA validation evidence rather than full per-leaf reruns |
| v0.10.2 | 43 | 44 | broad package refactor, repeated A1–A7 planning amendments, generated-dist/manifest/CI/Node24 seam, release doc coverage |
| v0.10.3 | 13 | 5 | draft/downstream intake only at snapshot; production outcome not established; targeted clean external consumers improve feedback |

**CAUTION**: 312 v0.7 Issues include read-only Review/Validation/Currentness matters. 93 version-target PRs do not mean 93 independent features. Neither the 0.8.1 Issue count nor the v0.5 title count can support a "no Issues" or "no defects" conclusion.

## 3. Cross-version causal cases and stage-specific learning

### 3.1 v0.1–v0.2 — tests can be green but semantically incomplete

- [v0.2 #135](https://github.com/kaicreator-mm/domain-harness/issues/135): process interruption left the Workflow Instance unable to progress after restart despite healthy-looking state. Crash-recovery semantics must be tested against actual durable store/restart, not only normal-path unit tests.
- [#136](https://github.com/kaicreator-mm/domain-harness/issues/136): terminal target checked before durable message identity dedup, making retry return reject rather than original ACK. Explicit **ordering invariants** belong to L2 owner and integration test.
- [#139](https://github.com/kaicreator-mm/domain-harness/issues/139): package root pulled Node-specific dependencies while portable \`/v2\` entry was clean; tests of the internal source path did not prove the **advertised public import path**.
- [#162](https://github.com/kaicreator-mm/domain-harness/issues/162): canonical \`npm test\` glob missed nested suites; CI green could coexist with unexecuted critical tests. The needed repair is **test discovery completeness** (expected discovered test count or manifest, canonical command vs actual execution), not another review loop.  
**ADS candidate:** Version/L2 contract should identify high-impact crash/idempotency/portable-public-import invariants and prove at least one real consumer/negative when they are product critical. CI should detect test-discovery omissions proportionately, not globally duplicate all suites.

### 3.2 v0.3 — user-facing domain workflows expose platform abstraction gaps earlier

- [#177](https://github.com/kaicreator-mm/domain-harness/issues/177): draft consumers for 13 domain applications revealed the lack of a first-class registered local Tool binding; business writes had to masquerade as remote HTTP. This is a **common framework API missing consumer requirement**, not merely a single app's bug.
- [#178](https://github.com/kaicreator-mm/domain-harness/issues/178): compiled Domain Data omitted from manifest and dependency check; failure moved from BUILD to runtime.
- [#180](https://github.com/kaicreator-mm/domain-harness/issues/180): \`openInstance\` not idempotent, creating race-prone consumer ceremony.
- [#208](https://github.com/kaicreator-mm/domain-harness/issues/208): v0.2 historical READY candidate diverged by 41 commits as v0.3 research backflow entered that branch. A previously qualified SHA does not qualify a changed version HEAD.
- [#244](https://github.com/kaicreator-mm/domain-harness/issues/244): release closure retains physical validation and independent role handoff; work with a real Host has authority distinct from Web planning.  
**ADS candidate:** Prioritize one *representative downstream consumer path* before freezing highly abstract SDK capability plans. Keep research branches, future versions and qualified released baselines separate. Run scope-constrained exact-SHA qualification only after dependency completeness.

### 3.3 v0.4–v0.6 — review fragmentation and false integration assumptions

- [v0.4 #363](https://github.com/kaicreator-mm/domain-harness/issues/363), [#378](https://github.com/kaicreator-mm/domain-harness/issues/378): independent findings were routed back to **the same existing branch/PR**. Positive: no unrelated rewrite. Possible overhead: independent repair-tracking Issue for every review iteration. Prefer Review comments/attempts within the original concern unless a genuinely new separate owner is needed.
- [#409](https://github.com/kaicreator-mm/domain-harness/issues/409): release candidate's project override and Woodpecker branch filter did not match current v0.4 version branch. This is project/CI configuration currentness, not runtime source error. Validate release branch target/profile before expending full RQ.
- v0.5 issue-title sample is inadequate; [v0.6 #483](https://github.com/kaicreator-mm/domain-harness/issues/483) and [#484](https://github.com/kaicreator-mm/domain-harness/issues/484) explicitly carry v0.5 post-release observations into v0.6; no inference that v0.5 was defect-free.
- [v0.6 #490](https://github.com/kaicreator-mm/domain-harness/issues/490): L2 review found a false claim that the DecisionResolver was wired into production Runtime; source existed but composition did not.  
**ADS candidate:** L2 statements about "implemented", "exported" and "called in selected runtime path" require different evidence; an **export-exists check is not an invocation/behavior check**. CI/environment routing should detect obvious version-profile drift early. Reviews should stay associated with their stable concern when possible.

### 3.4 v0.7 — split by concern, not by each reviewer/controller checkpoint

- [#530](https://github.com/kaicreator-mm/domain-harness/issues/530): frozen topology needlessly made v0.6 source merge a blocker for independent v0.7 refactor; final compatibility evidence may be a separate integration predecessor, not a blocker to all implementation.
- [#537](https://github.com/kaicreator-mm/domain-harness/issues/537): local multi-Agent program controller with 183 comments; real independent waves and JIT can reduce idle time, but event volume/coordination/readback also consumes engineering capacity.
- [#586](https://github.com/kaicreator-mm/domain-harness/issues/586): cross-cutting Microkernel incremental verification as one campaign Issue **explicitly avoids creating an Issue per checkpoint**—a positive pattern worth generalizing.
- [#758](https://github.com/kaicreator-mm/domain-harness/issues/758) and [#764](https://github.com/kaicreator-mm/domain-harness/issues/764): post-merge \`__proto__\` canonical-copy repairs showed concurrent/duplicate work can appear around the same concern. Reconcile accepted Claim + canonical PR/current target before competing repair branches; do not take Issue/PR count as independent progress.
- [#782](https://github.com/kaicreator-mm/domain-harness/issues/782): CI workers lacked git-lfs; failures came at clone before source verification. CI environment defects must be separated from Product code quality.  
**ADS candidate:** Explicitly model task/review/validation/merge *seam ownership* and real dependency reason. Event trace & controller state card may aggregate many checkpoints into one recoverable concern; avoid generating new GitHub Issues just to count progress. Source writes still require accepted Claim and disjoint ownership.

### 3.5 v0.8 → v0.8.1 — integration must verify behavior, not just compile modules

- [#1005](https://github.com/kaicreator-mm/domain-harness/issues/1005) T-F required two real Domain Harness Apps. [#1013](https://github.com/kaicreator-mm/domain-harness/issues/1013) found T-B/T-C/T-D/T-E accepted components still could not compose into a trustworthy Host→K/S→UX production path. Insertion of bounded integration repair after component merges was necessary. **Counterfactual:** a small early protected load→send→query→durable effect path with frozen ABI could have detected missing wiring earlier *if those components were executable then*. Do not force an expensive full App demo for every leaf.
- [#1006](https://github.com/kaicreator-mm/domain-harness/issues/1006) release closure eventually ran formal evidence. Independent post-release audit [#1100](https://github.com/kaicreator-mm/domain-harness/issues/1100) P0: stale admission overwrote FINAL after different writer; [#1101](https://github.com/kaicreator-mm/domain-harness/issues/1101) P1: lost same-message dedup; [#1102](https://github.com/kaicreator-mm/domain-harness/issues/1102) P1: BUILD accepted multi-B while only first Business policy was wired. These are separate real defects on **intercomponent authority and retained behavioral invariants**.
- v0.8.1 bounded hotfix was an appropriate response. Do not count each hotfix as evidence that all small corrections are wrong; root-type recurrence across versions justifies **bounded invariant matrix** for cross-writer CAS/replay and selected package routing.  
**ADS candidate:** For major runtime/architecture replacement, map historical retained capabilities to **executable current public-path witness**, not just a row marked retained in PRD. Integration owner should consume K/S/B/Host/BUILD contracts and prove negative competition and multiple selected bindings **before** final Closure where practical.

### 3.6 v0.9 — a positive scope correction

- [#1026](https://github.com/kaicreator-mm/domain-harness/issues/1026): user clarified JS/TS portable SDK Core vs Node/Windows/Linux/native SQLite adapter proof. A blanket OS matrix for "Core" was not correct Product scope.
- [#1037](https://github.com/kaicreator-mm/domain-harness/issues/1037): current-version one immutable dependency-complete candidate with reused leaf physical evidence and one full/Hidden/Release execution.  
**ADS candidate:** Product scope should classify **abstract Core guarantees vs selectable adapter/Host-specific guarantees**. Testing all environments is not itself more correct; require only the applicable owner profile and honestly disclose unproven portability.

### 3.7 v0.10–v0.10.1 — code presence is not implementation of frozen behavior

- [v0.10 #1264](https://github.com/kaicreator-mm/domain-harness/issues/1264): selected K extension Hooks imported but never called or revalidated by K Primary. A "two modules loaded" test did not prove required authority-controlled dispatch.
- [#1265](https://github.com/kaicreator-mm/domain-harness/issues/1265): selected facade lacked advertised subscribe/stop public path.
- [#1267](https://github.com/kaicreator-mm/domain-harness/issues/1267): Standard Features could be invoked by Host directly, but required S Primary→K admission path was not executed.
- [#1209](https://github.com/kaicreator-mm/domain-harness/issues/1209): real competing-writer test intermittently reported no typed loser outcome; official 3-consecutive requirement failed and the failure required actual outcome/path diagnosis. Avoid inventing a PASS from selective successful retries.
- [v0.10.1 #1291](https://github.com/kaicreator-mm/domain-harness/issues/1291): explicitly reuses exact retained T06 real validation and avoids per-leaf full repetition—positive evidence placement.  
**ADS candidate:** Before claiming a feature delivered, map \`frozen acceptance → compiled selected path → authorized entrypoint → observable result/negative\`; for adaptive composition/feature routing, a loaded-but-never-invoked object is not PASS. Use one integration/public consumer at the seam, not a separate full suite on every leaf.

### 3.8 v0.10.2–v0.10.3 — pre-freeze install/seam prediction and downstream dogfood

- [v0.10.2 A1 #1335](https://github.com/kaicreator-mm/domain-harness/issues/1335), [A2 #1341](https://github.com/kaicreator-mm/domain-harness/issues/1341): clean packed legacy consumers couldn't resolve workspace release-candidate package dependency across current layouts.
- [A3 #1345](https://github.com/kaicreator-mm/domain-harness/issues/1345), [A4 #1352](https://github.com/kaicreator-mm/domain-harness/issues/1352), [A5 #1354](https://github.com/kaicreator-mm/domain-harness/issues/1354), [A6 #1356](https://github.com/kaicreator-mm/domain-harness/issues/1356), [A7 #1359](https://github.com/kaicreator-mm/domain-harness/issues/1359): amendments had genuine basis (generated dist write sets, BUILD shims, actual Node24 gates, safe parallel drafts), but repeated redesign suggests the **plan omitted package/install/CI physical seam feasibility** before detailed file ownership freeze.
- [#1379](https://github.com/kaicreator-mm/domain-harness/issues/1379): documented Package Authoring/extension points marked P1 release scope were absent from candidate despite T08b docs PR source PASS; Source/CI review ≠ full Product acceptance inventory.
- [v0.10.3 #1393](https://github.com/kaicreator-mm/domain-harness/issues/1393): external npm Provider trust-deployment boundary observed under real Tally installed consumer; [#1394](https://github.com/kaicreator-mm/domain-harness/issues/1394): Host DocStore/CAS adapter shape mismatch observed under real ai-rexform install/first send. Keep distinct root classes.
**ADS candidate:** pre-freeze narrowly test **material** physical install/build/manifest and generated write sets for structural refactors; let actual package/CI evidence inform L2/DAG. After freeze, downstream consumer feedback is source evidence with owner/root classification, not retroactive downgrade of prior release or automatic Kernel refactor. An integration acceptance map must include frozen doc/user SDK deliverables where P1.

## 4. Root types to distinguish rather than call all "Agent failures"

| First divergence | Primary root class | E.g. | Preferred ADS owner/path |
| --- | --- | --- | --- |
| Requirement omitted from task acceptance | planning/retention mapping | #1264 #1265 #1379 | Product/Task acceptance mapping; affected integration proof |
| Dependency/owner order wrong | DAG topology/real physical build | #530 #1335–#1359 | Task Decomposition + L2 Amendment where material; not local unauthorized write expansion |
| Public path cannot be executed | cross-component composition | #1013 #1394 | interface/architecture integration owner; clean external consumer |
| Source runtime semantics wrong | implementation/source invariant | #135 #136 #1100 #1101 #1102 | bounded authoritative repair + replay/CAS negatives |
| CI PASS doesn't cover promised tests | test discovery/evidence | #162 | TESTING_STANDARD / CI owner; actual executed suite inventory |
| CI runner cannot run tests | infrastructure/toolchain | #409 #782 | runner owner, legitimate rerun/alternate evidence; avoid product code patches |
| Repeated review finding same concern | workflow/coordination | v0.4 #363/#378, v0.7 #758/#764 | source-bound diff Review and one canonical concern; new Issue only on real independent boundary |
| Release branch diverged after qualification | candidate identity drift | #208 | Release/Version integration exact HEAD and tree qualification |
| Product overextends adapter platform matrix | wrong obligation attribution | #1026 | Product/L2 per core vs optional adapter |
| Emerging downstream common feature gap | product/SDK abstraction | #177/#178/#180, #1393/#1394 | downstream-owned reproducer → DH owner scope, not automatic Kernel change |

**A caution:** Some signals are only counterfactual review suggestions. P0/P1 severity belongs to actual finding/authority. A post-release defect does not prove exactly which earlier Agent could have detected it from evidence then available.

## 5. ADS v4.19 bounded follow-on proposals — crosswalk to existing R01–R06

1. **R01 root-level diagnosis:** extend the *existing* root-class comparison with a "first known falsifier" and "repair owner", source-constrained. No new universal repair gate.
2. **R03 DAG/economics:** during material pre-freeze planning, check generated files, actual packaged consumer graph, CI/runtime version, shared manifest/catalog owner and one executable composition seam (where feasible) **before** fixing exhaustive task write sets. A failed/unknown minimal probe warrants L2 owner disposition, not a fake test PASS. Evaluate a safe parallel alternative including Reviewer/Host wait vs extra handoff cost.
3. **R04 delivery proof:** test discovery should match declared critical suite; one clean real consumer should prove selected code is actually *invoked* and produces the promised authorized behavior—not merely compiled/exported/imported. Reuse per-owner Test/Validation Standards, no new release gate.
4. **R05 measured process learning:** per version, collect optional planning-rework/implementation-rework/reviewer-finding/integration-defect/escaped-defect counters **by root class and actual source** plus Agent active-vs-wait where task-meta evidence exists. Counts are not a leaderboard or independent quality verdict; declared UNKNOWN stays UNKNOWN.
5. **R06 backlog:** current-version reproduced and owner-relevant Issues only in blockers; retain historical release findings and supersession links without carrying outdated gates into successor.
6. **R02 timing:** for repeated R rounds and Release RQ, identify observed PR lifecycle and source-bound waiting intervals; do not call GitHub lead time an Agent computation duration. Parallel Agent-hours may exceed version elapsed. Report uninstrumented segments UNKNOWN.

**Potential substantive missing acceptance to independently review:** specifically check whether existing frozen acceptance and its *real selected path* are connected by an observable test; coverage-by-file, export, mock-only unit, CI-green or staged import must not be mistaken for actual behavior. This may be a stronger delta than creating any new metrics schema.

## 6. Recommended version-retrospective template (advisory; not mandatory new artifact)

Record in the existing Version Closure or lightweight issue comment **when this information improves a future decision**:

\`\`\`text
version / exact release candidate / frozen Product & L2 refs
planned Task DAG nodes / true integration prerequisites / Agent environment owners
current accepted integration and selected user journeys
new requirements discovered after freeze (why first known)
source changes / review P0-P1-P2 / which findings were cross-owner
repair attempts by root class / which evidence narrowed cause
test suite discovered-vs-expected and public clean consumer actual behavior
required CI/physical/Hidden at exact SHA / qualified or UNKNOWN
escaped regressions in successor/post-release window with retained capability owner
end-to-end version and PR elapsed (source timestamps)
Agent active segments, queue waits and cost (measured only; otherwise UNKNOWN)
what to KEEP / SIMPLIFY / MOVE EARLIER / DEFER; responsible ADS/project owner
\`\`\`

**Avoid retrospective bloat:** one short risk-focused summary at version closure or before the next significant version; minor hotfix may only link one source-bound finding. Do not create 1 Issue per counter, per retry or per review iteration. Promote a pattern into ADS only after it demonstrates a cross-project/generalizable normative gap (Development Workflow §8).

## 7. Limitations and necessary independent challenges

- Version counts have mixed classification schemes and truncated scope for v0.5, v0.8.1, unmarked versions, spike branches, and main PRs; they are not normalized velocity data.
- This is a **sampled issue-body/source evidence audit, not 845 individually reproduced source-level regressions**. Current version may have repaired some historical findings without closing the original Issue; recheck current public artifact before applying.
- GitHub comments are durable event timestamps, **not trustworthy active Agent start/end** unless accepted role execution and task-meta actual instrumentation show segments.
- Quantitative time-saving from alternative DAG/Review batching is NOT_MEASURED; avoid claims of X% improvement.
- Existing v4.18 Normative Task Decomposition, Development Workflow, Testing, Validation, CI, Agent event and Task Learning rules may already cover much of this. Independent Product R0 reviewer must classify \`ALREADY_COVERED / DOC_OR_TOOLING / NORMATIVE_DELTA\` before creating additional MUSTs.
