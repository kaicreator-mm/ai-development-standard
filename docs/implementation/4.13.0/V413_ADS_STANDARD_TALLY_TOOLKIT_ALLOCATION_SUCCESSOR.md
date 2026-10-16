# ADS v4.13 — Standards-only Product Boundary / Tally Toolkit Ownership (Successor Candidate)

> **User Product direction recorded 2026-10-16. SOURCE-ONLY; NON-NORMATIVE; NOT PRD/L2/DAG FROZEN.** Related: [v4.13 #1147](https://github.com/kaicreator-mm/ai-development-standard/issues/1147), [Tally integration #55](https://github.com/kaicreator-mm/tally/issues/55). This is a **successor to prior ADS implementation allocation** in Draft PR [#1148](https://github.com/kaicreator-mm/ai-development-standard/pull/1148) and a scope refinement to Draft PR [#1149](https://github.com/kaicreator-mm/ai-development-standard/pull/1149). It does not discard their reusable research findings, but their implied ADS-hosted CLI/Updater/Steward runtime is superseded.

## Product scope decision — Tally preparation only (user confirmed 2026-10-16)

This is now the **operative planning direction** (not a PRD/L2/Task DAG Freeze), recorded in the **main body** of [v4.13 #1147](https://github.com/kaicreator-mm/ai-development-standard/issues/1147) rather than only in Issue comments.

**Version decision:** Keep the already-unfrozen **ADS v4.13**, do not introduce a special intermediate ADS version just to prepare Tally v2. ADS v4.13 is independently deliverable **before** Tally v2 ships. A subsequent ADS standard update is optional and based on real Tally field evidence, not automatically required.

**All executable work belongs to `kaicreator-mm/tally`.** In particular, no ADS-owned devkit copy/port, host Bootstrap, mise/Worktrunk/native Git Worktree adapter, `ads dev` runtime CLI, Agent Skill/MCP server, multi-Agent scheduler/Portfolio/Steward service, actual multi-repo PR writer, Task learning process or actual Tally Build Host validation. Those are **Tally Product/Architecture/Task DAG/Release scope** under [tally #55](https://github.com/kaicreator-mm/tally/issues/55) and [tally Draft PR #56](https://github.com/kaicreator-mm/tally/pull/56).

### Corrected ADS v4.13 deliverable matrix

| Contract | ADS v4.13 acceptance | Not an ADS v4.13 release condition |
|---|---|---|
| Organization Development Environment Profile | Versioned org defaults + project/host/compatibility precedence, minimal schema/examples, deterministic conflicting-project case | Real installation of mise/Node/Python, Windows/Ubuntu deployment |
| ADS exact-revision consumer contract | Tally-readable immutable effective pin, project overrides, source-currentness, Claim/Role/Review/Validation/Release provenance | Working Tally policy resolver, database or production Agent scheduling |
| GitHub project fact/Attempt distinction | Precise native Issue Dependency/PR/current SHA vs local Agent Attempt/Host/scheduler semantics and counterexamples | Tally Portfolio screen, actual cross-project Ready queue |
| #1119 compatible ADS adoption | Qualified-release compatibility proof and scoped plan → opted-in PR → approved activation/rollback *semantic contract* | Real downstream PR creation or cross-repo updater runtime |
| #1116 proportional assurance | Only genuinely missing capability/delivery-based normative delta + standards-repo actual applicable source/schema checks | Tally CLI/SSH/Docker/Agent actual Full Regression/Hidden Validation |
| Release | Applicable exact-source coherence and final candidate qualification under existing ADS gates | Tally v2's own end-to-end tests, CI/Host actions, feature completion or release qualification |

### Explicit owner/requirement boundary

1. **Tally's ADS-native redesign is prospective.** Existing Tally v1.5.x frozen source and `.dev-standard/VERSION` historical YAML must not be rewritten retroactively or falsely interpreted as the newer canonical pin; Tally implements an explicit local migration when independently admitted.
2. **A normative ADS contract is not a second implementation.** Where v4.12 canonical `standards/*`, `schemas/*` and `scripts/v412_ads_compatible_select.py` already cover a predicate, v4.13 references that exact owner and emits no duplicate global schema, Task DAG engine, validation service or CLI.
3. **Runtime identity**: Tally may store internal Agent Session/Attempt state, but ADS-native GitHub project Task/Issue Dependencies and accepted Claim/PR/Git observations remain externally source-bound facts. Self-declared logical Agent role/identity is separate from GitHub authorization transport; actual policy/Claim/CAS/verification proof remains real.
4. **Rollout**: `qualified_ADS_predecessor -> ADS_v4.13_standards_Release -> Tally_v2_exact_PIN_and_build/release -> optional_new_ADS_feedback`. No mutual release Gate or dependency cycle.
5. **Minimal actual ADS Task split** after L1/L2: source gap audit, org Profile/precedence, interoperability contracts, bounded #1119/#1116 semantics where unimplemented, existing source-only release closure. Merge/drop concerns already satisfied. Draft #1148/#1149 are research history, not executable PRs.
6. **Proof states**: `PRODUCT_FREEZE=NO; L2_FREEZE=NO; DAG_FREEZE=NO; ADS_V413_IMPLEMENTATION=NOT_STARTED; TALLY_V2_REAL_EXECUTION=NOT_RUN`. No claim of Tally runtime conformance from standards-only examples.

## 1. Decision

**ADS = standalone internal Engineering Standard and Organization Configuration Contract.**  
**Tally = ADS-native execution/management platform with the runtime Toolkit bundled in the Tally repo, exposing an independently executable CLI and optional Skill/MCP.**

ADS v4.13 remains conceptually `Organization Development Environment & Toolkit`, but the **Toolkit executable lives in Tally**. For ADS Product naming, the normative v4.13 deliverable is Organization Development Environment Profile + Toolkit/Execution **Contracts**, adoption/compatibility, and only non-duplicative cross-delivery assurance clauses. Any follow-up with Tally runtime is a separate Tally product/release; no Tally runtime implementation work silently becomes an ADS normative release requirement.

## 2. Precise ownership split

| Concern | ADS source owner | Tally source owner | Durable external facts |
|---|---|---|---|
| Standard/phase/Task/Claim/Review/Git/Validation/Release rules | **Normative** pinned version, minimal schemas/reference examples | Reads/adapts in a version-aware, fail-closed manner | Git exact SHA + GitHub Issue/PR/CI/Release |
| Organization Development Environment Profile | Organization/profile schema, precedence, project-overrides and positive/negative cases | Profile resolver, actual setup, host inventory, version install/switch | Actual filesystem/runtime/host process facts |
| Toolchain/Workspace/DevKit | Required behavior, safe lifecycle and source currentness contract | `tally dev` CLI + mise/Worktrunk/native Git/bare mirror adapters and safe cleanup | Git worktrees, branches, remote refs and installed binaries |
| Task/Project Steward, multi-Agent & multi-project | Normative integration/evidence/compatibility, **no controller service** | Existing Tally multi-Agent runtime/DAG, Portfolio, cross-host scheduling, restarts, actual operational state | GitHub-native Task dependencies; actual host/Agent outcomes |
| #1119 qualified compatible ADS upgrades | Immutable release/compatibility/adoption protocol, tiny **read-only reference selector** if needed | **Only cross-project PR updater**: discover opted-in consumers, idempotent scoped PR, activation at checkpoint, rollback | Actual GitHub source update PR/Review/merge and consumer pin |
| #1116 delivery-aware evidence | Concise capability→required current proof standard and no needless CI duplication | Execute actual tests/review/closure evidence per project, not new normative standard | Executed CI/host logs/current candidate |
| W1/W4/W5 conditional planning, learning | Conditional allowed artifacts and stop rule; no new 3-DAG engine or DB | Project planning proposals and actual Task scheduling, bounded evidence-backed learning | GitHub Issues/PR and source-pinned artifacts |

ADS can ship **tiny pure schema/reference scripts** where a standard is otherwise not usable or machine-verifiable; do not confuse those with Tally's host/multi-agent execution engine. ADS itself remains usable by generic agents/other platforms without Tally installation.

## 3. Tally as ADS-native; canonical fact model

- ADS-native project modes: GitHub Issue Dependencies and accepted Claim events remain canonical **project task facts**; Tally Active TaskDAG is a **derived operational scheduling projection**, not a competing fact source; Tally stores distinct host/attempt/agent execution states.
- Tally's old project `.dev-standard/VERSION` YAML v1.2.1 is **not** a valid v4.12+ exact pin file without an explicit prospective migration; historical Tally v1.5 frozen records remain unchanged. Resolve one qualified ADS revision per project/effective accepted Task, not mutable `main/latest`.
- Self-declared logical Agent roles/contexts from ADS v4.12+ are authoritative for role attribution, not GitHub login. Security/actual platform permissions and real irreversible effects remain factual constraints. Do not reinstate owner/account verification gates as hidden `tally` policy.
- Execution truth: Agent outcome is proposal/claim, not real Gate PASS; Tally invokes real impacted tests, source-bound Review and actual GitHub state readback. `CI_PENDING != FAIL`, `SKIP != PASS`, `PR_PASS != RELEASE_PASS`.
- Tally's old distinct Requirements/Planning/Architecture/DAG/Completion contracts should be remodeled as consumers of frozen ADS artifacts, not retained as a second mutable lifecycle/Release authority.
- Proposed CLI works **without Tally daemon or organization DB** for local environment, worktree, inspect and validation commands; Skills/MCP call identical code; multi-project orchestration adds Tally server above that core.

## 4. Required v4.13 planning corrections to earlier drafts

1. Draft [#1148](https://github.com/kaicreator-mm/ai-development-standard/pull/1148) is **historical supplier/pattern research** (mise, Worktrunk, devkit, Agent Skills, CLI surface, acceptance cases), NOT implementation authorization to build `toolkit/ads-dev` in the ADS repository. The actual CLI package/Skill/MCP implementation must instead land in Tally. Keep the portable `Organization Profile` schema and interface rules in ADS.
2. Draft [#1149](https://github.com/kaicreator-mm/ai-development-standard/pull/1149) keeps its **non-toolkit** optimization logic but runtime ownership changes: #1119 opt-in real project updater, W2 status dashboard, W4 execution-level learning and host dispatch run in Tally, not in ADS. ADS owns only standard conformance, release compatibility contract, read-only reference logic and bounded evidence-use rules. No new ADS scheduler.
3. Original #1147 planned `C02` organization Profile and `C03/C04/C05` toolkit/validation/updater executable implementation in ADS. **Re-scope C03/C04/C05 as ADS contracts/example obligations only**, with real Tally work appearing in a separately frozen Tally v2 Task DAG. No separate ADS server, fleet update controller, mandatory Agent UI/OS compatibility matrix.
4. #1116 delta gets **simpler for ADS**: ADS v4.13 standard/spec sources check their own source consistency, normative schema/examples and existing applicability; **Tally** must exercise its own new real CLI/server on actual supported hosts. Do not force executable Tally releases to pass merely because ADS normative release passed.
5. `#1099` Risk-Bounded Value First and `#1123` self-declared logical Agent identity already shipped with ADS v4.12, so reuse as v4.13 baseline; no extra owner identity gate or retrospective re-review of unchanged standard files.
6. `#1119` v4.12 read-only latest-compatible selector is implemented but conservative: its current live checkpoint rejects any open Issue/PR. In prospective v4.13 Tally updater use separation **read-only compatible planning → opt-in scoped PR → actual project checkpoint activation**, never merely weaken source-proof or force an active Task pin migration.

## 5. Minimal proposed ADS deliverables (not a frozen DAG)

**S01** — One canonical v4.13 Product/L2 scope+source-gap audit (existing standards vs devkit/upstream/Tally), accurate version identity, acceptance and consumers.

**S02** — Organization Development Environment Profile v1: schema/precedence and minimal real-project examples. Differentiate compatibility, organization preferred, project frozen override, actual host availability and certified release tuple; no forced global Node, Python or package-manager version.

**S03** — Small Tally integration/Toolkit execution **contract**: explain/bootstrap, task-worktree ensure/resume/cleanup, Validation/GitHub impact, exact source and failure contracts, self-declared Agent context, project/portfolio schema boundaries. No second CLI implementation.

**S04** — #1119 prospective/adoption interface and #1116 capability-based proof update **only where actual missing material rules**. Tally owns real GitHub updater and its own host validation. Reuse v4.12 qualified read-only selector, don't publish floating latest, don't modify projects from ADS release process by default.

**Closure** — one standards-specific self-coherence + self-dogfood under applicable currently authorized Release Standard and actual deterministic reference checkers; no mandatory Tally v2 full release before ADS v4.13 source qualification. Tally real project pilot after its own admission. No new cross-product release-dependency cycle.

All candidate concerns can combine/cancel where code ownership overlaps. One concern/PR, delta-review for tiny fix, one final immutable candidate's required regression when necessary. No separate artificial review/gate/Owner escalation for “moving the toolkit”.

## 6. Cross-repo acceptance criteria (candidate only, NOT_RUN)

| ID | ADS product expectation | Tally future observable proof |
|---|---|---|
| AT01 | One Organization Profile resolves compatible preferred runtime without overriding project requirements | `tally dev env explain` with two different real project configurations |
| AT02 | ADS standard is readable/useable without a Tally binary or API | Standalone Agent consumes exact ADS revision and can independently follow standard |
| AT03 | Toolkit function contracts define exact local/host state and safe cleanup | Tally CLI on Windows/Ubuntu with native Git fallback, no server dependency |
| AT04 | Exact project ADS pin and actual GitHub Task/Claim facts are required for changes | Tally real Task+Agent+PR readback, no duplicate canonical Task DAG |
| AT05 | Multi-project index policy is defined without a second ADS scheduler | Tally 2+ repos + 2 Agent roles/statuses pilot |
| AT06 | ADS compatible published release proposal is source proven; activation cannot drift | Tally scoped opted-in project upgrade PR, retained active Task old SHA |
| AT07 | ADS normative release need only satisfy own applicable standard checks | Tally actual CLI/server candidate gets real runtime checks independently |
| AT08 | No GitHub account-as-actor Owner gate; self-declared logical actors | Two contexts on same transport identity with objectively truthful independent checks |

## 7. Version and evidence truth

```ini
TARGET_ADS_VERSION=4.13.0
STANDARD_OWNER=kaicreator-mm/ai-development-standard
EXECUTABLE_TOOLKIT_OWNER=kaicreator-mm/tally
TALLY_MAJOR_VERSION_CANDIDATE=2.0
ADS_V413_NEW_ARCHITECTURE_PRD_FREEZE=NO
ADS_V413_L2_FREEZE=NO
ADS_V413_TASK_DAG_FREEZE=NO
TALLY_V2_PRODUCT_FREEZE=NO
TALLY_V2_IMPLEMENTATION=NOT_STARTED
CROSS_PROJECT_E2E=NOT_RUN
LEGACY_ADS_PROJECT_PINS_CHANGED=0
HISTORICAL_FROZEN_GATES_RETROACTIVELY_CHANGED=0
```

**This source is a scope-allocation successor proposal, not permission to merge older #1148/#1149 designs unchanged or to write normative v4.13 source before legitimate Product/L2 authorization.**
