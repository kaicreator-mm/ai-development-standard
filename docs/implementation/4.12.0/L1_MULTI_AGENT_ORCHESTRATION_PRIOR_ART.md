# v4.12 L1 Prior Art — Multi-Agent Orchestration Patterns for ADS

Status: **L1 SOURCE-ONLY RESEARCH / PRODUCT INTAKE CANDIDATE — NOT NORMATIVE, NOT PRODUCT/L2/TASK/RELEASE AUTHORITY**

Parent: [#1096](https://github.com/kaicreator-mm/ai-development-standard/issues/1096) (W1–W5); phase-graph consumer [#1100](https://github.com/kaicreator-mm/ai-development-standard/issues/1100); risk/ROI principle [#1099](https://github.com/kaicreator-mm/ai-development-standard/issues/1099).

Research date: 2026-10-14. ADS reference: `main@b9461d48d902a2c7c00adff6746afc7a02a0ac3e`. These are **static, pinned README/source inspections**; no upstream build, runtime conformance, dependency-vulnerability audit, legal code-reuse approval, or production security assurance was performed.

## 1. Decision boundary and desired outcome

**Integrate transferable ideas into existing ADS owners, not the upstream products or a second orchestration authority.** ADS already defines:
- GitHub Task Issues plus *native Issue Dependencies* as the canonical **live** implementation DAG; frozen `TASK_DAG.md` is a planning checkpoint.
- Existing admission/claim, dispatch, review independence, JIT Execution Packs, validation exact-subject truth, release, and environment isolation.
- Proportional/A0–A4 implementation, allowing manual execution without a permanently running daemon.

This intake therefore asks which **residual** behavior merits a v4.12 Product decision, with evidence that it is not already satisfied. **Do not** create a separate scheduler, DAG store, lifecycle, truth database, task-status enum, framework mandate or universal Gate. `INLINE | BOUNDED_WORKLIST | EXPLICIT_DAG` remains phase-conditional under #1100; L1/L2 completion is never implementation authorization. Optional/low-ROI research stops under #1099 without waiving material safety/authority predicates.

**Stage:** L1 prior-art + owner/gap proposal only. Before any normative change: exact existing-owner/source conformance audit → scoped L1 evidence/PRD → Product review and explicit Freeze → L2 selection (including licence/security/currentness) → bounded implementation Task DAG where necessary.

## 2. Pinned upstream reference evidence

| Project | Pinned source read | Transferable *pattern* | Important boundary / unknown |
| --- | --- | --- | --- |
| [ccteam](https://github.com/firstintent/ccteam) | [README / source @47d0fd6157514695431a76bf9ef2f193574f43cb](https://github.com/firstintent/ccteam/tree/47d0fd6157514695431a76bf9ef2f193574f43cb), `docs/mcp.md`, `docs/hook-dynamic-workflows.md`, `crates/ccteam-flow/src/{journal,scheduler}.rs`, `crates/ccteam-harness/src/adapter.rs` | persistent sessions and per-request correlation, vendor adapters, pre-delegation policy hook, admission limits, replay journal | No ADS Release/Gate authority; flow journal can degrade on write failure; default Claude permission skip / permissive Telegram empty allowlist unsafe for unattended deployment; remote satellite vendor support is not universal |
| [Gas City](https://github.com/gastownhall/gascity) | [README @cef7ec76aae7c3fdd4c7c9880afe9d3bf9567f4f](https://github.com/gastownhall/gascity/blob/cef7ec76aae7c3fdd4c7c9880afe9d3bf9567f4f/README.md) | supervisor reconcile loop, work routing, formulas, declarative packs, runtime-provider separation | Beads-backed tracking is **not** a substitute for ADS GitHub native dependency authority |
| [Beads](https://github.com/gastownhall/beads) | [README @eaed71fbba485418b2e8974fa7d17c0ef037190a](https://github.com/gastownhall/beads/blob/eaed71fbba485418b2e8974fa7d17c0ef037190a/README.md) | dependency-aware ready query, durable issue identity, atomic claim, relationship/recovery vocabulary | Dolt/Beads is a separate SoT; adopt semantics, **not** mandatory Beads storage |
| [Gas Town](https://github.com/gastownhall/gastown) | [README @649b832b7672bc7a2dbef26f5983aba6198b819b](https://github.com/gastownhall/gastown/blob/649b832b7672bc7a2dbef26f5983aba6198b819b/README.md) | ephemeral workers with persistent work identity, supervisor/witness, merge-refinery concepts, workflow templates | Fixed role/team metaphors and its issue store are not ADS authorities |
| [Agent Orchestrator](https://github.com/OrchestratorInc/agent-orchestrator) | [README @11622fc18a553bbd7c499184330a9688413f6147](https://github.com/OrchestratorInc/agent-orchestrator/blob/11622fc18a553bbd7c499184330a9688413f6147/README.md) | live agent/worktree/PR/CI/review projection and feedback loop | UI/Kanban must remain a reconstructible non-authoritative projection |
| [Orch](https://github.com/gabrielkoerich/orch) | [README @b429eb17c378312b2b577834a258714826bfe3c5](https://github.com/gabrielkoerich/orch/blob/b429eb17c378312b2b577834a258714826bfe3c5/README.md) | GitHub-native work routing, per-task/per-attempt artifacts, worktree isolation, recovery | Its internal SQLite jobs and direct PR flows may not match ADS roles/Claim/currentness |
| [Cezar](https://github.com/open-mercato/cezar) | [README @ae60471e94331310b72524540a4d35fb9834e7fc](https://github.com/open-mercato/cezar/blob/ae60471e94331310b72524540a4d35fb9834e7fc/README.md) | parallel worktrees, task queues, child delegation, variants and shared task budgets | Duplicate variants are **read-only/evidence-only by default** unless a single writer / authority is established; not proof of safe concurrent writes |
| [LangGraph](https://github.com/langchain-ai/langgraph) | [README @ccb851effb7b4c6255add86dbeed577061475aff](https://github.com/langchain-ai/langgraph/blob/ccb851effb7b4c6255add86dbeed577061475aff/README.md) | durable state, checkpoints and human-interrupt concepts | Optional backend; no unproven crash-safe/exactly-once assertion |
| [Temporal](https://github.com/temporalio/temporal) | [README @2ac4e9b64260a835a938dd379b18bcecfad13d4e](https://github.com/temporalio/temporal/blob/2ac4e9b64260a835a938dd379b18bcecfad13d4e/README.md) | recoverable workflows, bounded retry/timeout, deterministic external-effect discipline | Heavy service requirement is unjustified for ADS manual/Fast Path; do not introduce Temporal by default |

A pinned README documents **claimed design intent**, not a test pass. For code-level adoption, obtain file-specific reviewed behavior, dependency/licence provenance, explicit L2 disposition and fresh reproducible demonstrations *only if a material UNKNOWN remains*. No third-party code has been copied here.

## 3. Existing ADS owner mapping and proposed disposition

| Proposed consideration | Current canonical owner / source at ADS main baseline | L1 disposition | v4.12 consumer |
| --- | --- | --- | --- |
| Stable Task identity, Issue-ready and dependency edges | `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, `TASK_DAG_GOVERNANCE_STANDARD.md` | **ALREADY_DEFINED**: no new DAG service or state; investigate only time-to-ready/critical-path usability | W1 |
| Phase-scoped DAG-P / DAG-A / DAG-I | #1100, `DEVELOPMENT_WORKFLOW.md` | **EXISTING_PRODUCT_CANDIDATE**: refine conditional views only; never make three mandatory persisted DAGs | W1 |
| Minimum coherent concern; preserve atomic invariants; safe split/supersede | `TASK_DECOMPOSITION_STANDARD.md`, `TASK_DAG_GOVERNANCE_STANDARD.md`, #1096 §8 | **DEFINED / DOGFOOD GAP**: planning/JIT oversized-agent detection and lawful ACTIVE recovery need exact-source conformance/dogfood | W1 |
| Task/worker Session/request/Attempt relationship, cross-vendor handoff and notification correlation | `GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `EXECUTION_ARCHITECTURE_STANDARD.md`, `LOCAL_AGENT_HANDOFF_PROTOCOL.md` | **PARTIAL/VERIFY**: propose *projection only* of existing dispatch generation, execution session, request, attempt and terminal evidence; do not add an authority or new status enum | W2/W4 |
| Ready Set, worker liveness and blocked-owner alerting | `EXECUTION_ARCHITECTURE_STANDARD.md`, #916, #1096 W2 | **DEFINED / VERIFY**: use existing reducer and controller; prefer critical-path and merge-ready unblocking, not throughput by dispatch count | W2 |
| Vendor capability and permission, admission caps, retry/backoff and cost ceilings | `EXECUTION_ARCHITECTURE_STANDARD.md`, `EXECUTION_PACK_STANDARD.md`, `MODEL_USAGE_POLICY.md`, #1096 W3 | **PATTERN_CANDIDATE**: adapter-neutral optional execution policy; no provider/model assumption or auto-PASS | W2/W3 |
| Isolated writers, clean exact-SHA checkout and safe worktree cleanup | `GIT_EXECUTION_STANDARD.md`, `LOCAL_AGENT_HANDOFF_PROTOCOL.md` | **ALREADY_DEFINED**: verify actual enforcement and environment preflight; do not mandate git worktree specifically | W3 |
| Recoverability: durable accepted request, replay, retry, idempotency, ACK-unknown, crash-between-write-and-notify | `EXECUTION_ARCHITECTURE_STANDARD.md`, `GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `EXTERNAL_SYSTEM_EXECUTION_STANDARD.md` | **PARTIAL/VERIFY**: map missing observation/recovery evidence; do not claim exactly-once effect from idempotency-key or journal alone | W2/W3 |
| Task Result + metadata / fail causes / measured rework | v4.11 T05–T11 and #1096 W4; `GITHUB_AGENT_INTERACTION_PROTOCOL.md` | **REUSE_FIRST**: capture only material source-backed learning, never a second learning database or copied private reasoning | W4 |
| Reusable workflows, roles, research/design/implementation patterns | `EXECUTION_PACK_STANDARD.md`, `ARCHITECTURE_RESEARCH_DEMO_STANDARD.md`, #1096 W5 | **PATTERN_CANDIDATE**: versioned opt-in templates/recipes subordinate to Task Pack; no prompt-injection or automated changes to authority | W5 |
| Static-vs-demo-vs-direct-code reuse selection | #1096 W5 and existing L1/L2 authority | **BOUNDED RESEARCH**: H1 pattern harvest / H2 specification reconstruction / H3 legally reviewed code reuse / BUILD_NEW, with licence/currentness/security and falsifiable stop | W5 |

`ALREADY_DEFINED` means a normative rule exists, **not** that every current runtime satisfies it. `PARTIAL/VERIFY` means source/runtime verification remains open, not a new unmet MUST. Owners are filenames or existing issues, **not** new components.

## 4. Candidate integration contract — semantic, not a new schema

**Task / worker / proof separation** (reuse existing record fields wherever possible):

```text
Task:          canonical GitHub Issue + frozen Task Pack, existing Claim/currentness
Dispatch:      accepted eligible work with role + claim generation + target environment
Attempt:       execution observation of one dispatch, potentially failed/interrupted
Session:       vendor runtime handle, may disappear/restart/rebind; not Task authority
Request/Turn:  optional adapter correlation within a Session, not equal to Task completion
Task Result:   output, acceptance predicates, gate-owned terminal/evidence refs
Task Metadata: bounded runtime/actor/cost/failure/recovery/learning evidence projection
Decision:      explicit authority for Product/L2/Review/Validation/Release, never model-inferred
```

Rules proposed **for Product evaluation**, not automatically normative here:
1. Worker `done` or a completed `Turn` does **not** imply Task PASS, Review PASS, Validation PASS, or Release PASS; only owning current evidence can do so.
2. Session replacement/restart does **not** create a new Task, authorize a second writer, transfer an old Claim, or inherit an unrelated Review. Resolve current claim generation/PR/write-set and release/rebind authority first.
3. A retry after unknown ACK or network loss must query durable accepted action/current external state before any non-idempotent mutation; record `UNKNOWN`, not fictitious success or safe retry.
4. Claims, branch/worktree assignments, job queues, and UI status are either GitHub-backed owner facts or reconstructible projections; non-canonical DB/flow state cannot mint a native dependency or satisfy a gate.
5. Checkpoint/replay caches are optimization; journal loss or divergent inputs require truthful invalidation and re-verification of real effects/evidence. `at-least-once` delivery alone is not `exactly-once` execution.
6. Multi-LLM critics may generate independent bounded findings. Deterministic checks validate actual subject; human/product authority is minimized by risk/rights, **not removed where required**. Reviewer independence and actor identity remain enforced.
7. Pre-delegation hooks/policies should default deny on invalid identity/capability/permission/currentness. An Agent under a shared OS user is not a security sandbox. Prefer least privilege and explicit permission mode rather than ccteam's documented skip-permission defaults.
8. Do not mandate standalone orchestrators, containers, Dolt, SQLite, Temporal, LangGraph, Flow scripts or more per-case GitHub Issues for projects that can satisfy the same contract manually.
9. Cost/ROI optimization may defer noncore optional work before freeze under #1099; mandatory current Product/security/currentness/Review/Validation/Release floors remain non-waivable.

## 5. Falsifiable dogfood and stop criteria

**Reuse #1096 D1–D7**, rather than minting seven parallel Test/Issue authorities. In any later authorized conformance program, select representative cases:

| Probe | Observable PASS predicate (not asserted here) | Negative control |
| --- | --- | --- |
| A. Oversize decomposition (#775) | Two genuine independently verifiable seams dispatched only with disjoint write owners and current dependency edges; preserves a necessary atomic counterexample | Giant Task split only by time/LOC or common mutable wiring → reject |
| B. ACTIVE recovery (#1072) | One canonical live Claim/PR selected; new Session/Attempt resumes via lawful authority and preserves exact-source useful work | Competing writers or stale PR CI-green → no merge/claim promotion |
| C. Product-research DAG (#1081) | Research graph stops when decision-value sufficient, no tooling recursion; Product Freeze remains explicit | Demo/research success laundering into L2 or implementation authority → reject |
| D. Merge drain (#926) | READY/MERGE eligible required work processed despite nonblocking advisory issues; valid blocker/current review still honored | Advisory OPEN alone blocking merge or stale PASS enabling merge → reject |
| E. Fast pre-host smoke (#1092) | Cheap focused shape/negative smoke finds a missing-key fault before real-host rerun; required host gate separately truly runs | CI summary alone converted into required exact-host PASS → reject |
| F. Session crash / provider switch | Same Task, current authorized Claim generation; attempt/request/turn linked to durable output; no duplicate effect when ACK unknown | Dead session treated as Task failure/success without evidence → reject |
| G. Permission + remote trust | Unauthenticated IM or tool invocation rejected; permission prompt required for high-impact effect, evidence of denial | Default bypass permissions / empty Telegram allowlist accepted in production → reject |
| H. Replay / journal gap | A divergent script/input invalidates cache; resumed run queries prior external state and reports unknown receipts | Journal append failure interpreted as exactly-once or completed gate → reject |

Evidence must record pinned owner/source, actual executor/host, actual commands and exit, actual decision/gate subject; `UNKNOWN` is allowed and must not be assumed `PASS`. Prefer one bounded real dogfood execution across existing projects; no per-provider giant test matrix without a named material predicate.

**L1 stop rule:** once owner overlap, source-level design rationale, candidate/product counterexamples and residual UNKNOWN disposition are sufficient to choose ADOPT/ADAPT/DEFER/REJECT, stop external mining. A real demo is justified **only** if a material unresolved unknown would change the L2 design; otherwise return to #1096 convergence. No autonomous normative changes, new required PRs or permanent execution services follow from this document.

## 6. Proposed disposition and integration sequence

- **ADOPT at the level of Product candidate semantics**: distinct Task/Dispatch/Attempt/Session/proof boundaries; critical-path/merge-drain projection; truthful retry/ACK-unknown; capability-aware budgets/permissions. Map to *existing* owners and inspect their current conformance before writing any standard amendment.
- **ADAPT if actual source gap is proven**: optional backend adapter, journal/resume receipts, bounded Policy Hook, vendor status/currentness and failure taxonomy. Maintain GitHub as the sole canonical live Issue Dependency graph and durable task/evidence source.
- **REUSE EXISTING**: Claim, Task Pack, worktree isolation, Review/Validation exact-SHA, phase authority, project adoption profiles and Task Learning if verified already present.
- **DEFER**: centralized Gas City/Beads/Temporal service, redundant tracker/DB, universal workflow DSL, mandatory dashboard, automatic merge authority, auto-human-replacement, wholesale upstream code import.
- **REJECT**: bypass-permissions as safe unattended default, public/empty-allowlist IM operator access, turn-completion-as-gate, retry-without-idempotency, unverified schema-to-truth promotion, journal-as-sole-truth, cross-head proof laundering.

**Next authorized step**: #1096 L1 source-gap disposition and Draft PRD selection; #1100 DAG-P/A/I phase-specific adoption; W2/W3/W4/W5 owners consume only proven residual deltas. Fresh Product review and explicit Product Freeze remain separate. This document itself produces `RESEARCH_ARTIFACT=PROPOSED`, `PRODUCT_FROZEN=NO`, `L2_AUTHORITY=NO`, `TASK_DAG_AUTHORITY=NO`, `IMPLEMENTATION_AUTHORITY=NO`, `GATE_PASS=NOT_CLAIMED`.
