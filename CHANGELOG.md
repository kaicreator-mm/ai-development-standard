# Changelog

## v4.0.0 — 2026-09-24

将 v3.4 的 GitHub-native pull 执行基线升级为统一的 **AI Development Operation Protocol + Multi-Agent Assurance**。v4.0 引入统一 Operation/Assurance/Interchange 组合协议与机器可验证 hardening，但不创建第二套 lifecycle、Validation truth 或 Release Authority；v3.4 的 Task/Execution Pack、Issue Dependency live DAG、exact-SHA Validation、risk-based Review、Candidate Freeze 与 Local-first 执行语义保持兼容。

- 新增 canonical Operation Protocol：每个 material Operation 精确归一为 `PRODUCE / RESEARCH / ASSURE / DECIDE / CONTROL`，Operation 是 lifecycle/correlation abstraction，不替代 Work Item、GitHub durable facts 或 owning authority。
- 明确正交 truth dimensions：workflow routing、Gate/Validation、provider/channel、dispatch、candidate、release 不能压缩成一个 flat state；routing/reducer/controller 只能派生投影，不能制造 owning truth。
- 新增 Assurance Plan 与独立性轴：Review Policy、Review Mode、Coverage、Independence、Aggregation 分离；context/model/executor/evidence independence 分别记录，Assurance 采用 DAG/partial order 而不是固定 Challenge→Validate 流程。
- 新增 model-diverse adversarial review 语义：blind first pass → finding union → optional cross-challenge → conflict disposition → aggregation；majority vote 不能覆盖 unresolved blocker，模型一致不能替代 executable Validation。
- 新增 transport-neutral Agent Interchange/correlation envelope，同时保持 `CORRELATION_ONLY_NON_AUTHORITATIVE`；GitHub 继续作为 durable reference profile，exchange/ACK/timestamp 不改变 authority 或 exact identity。
- 将 Operation routing 集成进现有 execution architecture：统一 dispatch/reducer/controllers 与 Work Item/Task Pack/Execution Pack/Fast Path，同时保留 Task DAG、Issue Dependencies、Candidate Freeze、Release Qualification、Repository Integration 的原有权威边界。
- 强化 Validation/Release contract：Review != Validation；Validation PASS 必须来自 required tuple 的真实执行；Candidate `PREPARED != FROZEN`；`PR PASS != Release PASS`；`Release READY != Repository Integration complete`；freeze/release/integration 均绑定 exact SHA/tree 与 fail-closed preconditions。
- 新增 v4 machine contracts、Golden/Forbidden examples 与 semantic hardening：覆盖 Operation/Assurance identity、finding/blocker dominance、aggregation、Validation report truth、Hidden metadata leakage、Fast Path disqualifiers、Candidate/Release transitions、Interchange、Repository Integration 等反例。
- 完成八类 end-to-end reference flows，并对 v4 自身执行多轮 blind provider-diverse dogfood；历史 R1/R2/R3 `CHANGES_REQUESTED` 保留为 durable evidence，R4 在修复后的 exact subject 上 PASS，随后完成 evidence-only closeout 与 Fresh Independent Review。
- 新增 v3.4→v4 migration/adoption contract：`A0_COMPATIBILITY / A1_MANUAL_PROTOCOL / A2_MACHINE_CONTRACTS / A3_DERIVED_AUTOMATION / A4_FULL_ORCHESTRATION`；adoption level 只改变 implementation surface，不削弱 immutable pin、authority、exact identity、required Validation/Review、blocker dominance、Candidate/Release/Integration 分离或 truthful status semantics。
- `PROJECT_OVERRIDES` 增加 v4 adoption、Assurance/model-diversity、Interchange、reducer/controller、Fast Path 配置边界；项目可以加强规则，不得削弱 Frozen PRD/Architecture 等更高 authority。
- 标准仓库 CI 扩展为完整 v3.3/v3.4/v4 自验证链，包含 Operation、adoption/migration、reference flows、dogfood hardening、canonical surface 与 pre-release semantic regressions。

## v3.4.0 — 2026-09-22

将 v3.3 的执行架构推进为可被独立 Web / Local agent 实际拉取执行的 **GitHub-native pull 执行模型**：吸收 #45（Task/Execution Pack + 双 agent pull 编排）与 #46（version-scoped Validation Handoff Queue）为一个统一 dispatch 架构。不引入并行 scheduler、lifecycle、state authority 或第二套 validation truth（兼容 MINOR）。

- 新增 `standards/EXECUTION_PACK_STANDARD.md`：Task Pack（durable planning authority：做什么）与 Execution Pack（JIT、绑定 exact integration base 的执行权威：怎么安全做）分离；pack 必需核心 artifacts（MANIFEST / EXECUTION_CONTRACT / TEST_MATRIX / FAILURE_MATRIX / IMPLEMENTATION_MAP / REVIEW_CHECKLIST）不要求空占位文件；矛盾向上路由为 `TASK_PACK_DEFECT / ARCHITECTURE_CONTRADICTION / EXECUTION_PACK_INVALID`。
- Execution Pack staleness 确定性 fail-closed：`PACK_CURRENT / PACK_STALE_NONMATERIAL / PACK_STALE_MATERIAL / PACK_INVALID`；claim 时校验 pack base SHA、Task Pack identity、依赖完成 identity、pinned standard revision、branch；executor 不得静默改写 `base_sha`，NONMATERIAL 仅可经显式授权 impact/rebind 继续。
- Agent freedom 机器可读：`F0_MECHANICAL / F1_BOUNDED_IMPLEMENTATION / F2_ENGINEERING_DISCRETION / F3_ARCHITECTURE_REQUIRED`（task-contract / dispatch / pack manifest / event 均可携带）；executor 不得自我升权，F3 任务要求 `review:required`。
- 新增 `schemas/dispatch.schema.json`：统一 Dispatch（dispatch_id、role、execution profile `LOCAL_BUILDER / LOCAL_VALIDATOR / WEB_REVIEWER / PLATFORM_VALIDATOR / CLOSURE_VALIDATOR`、branch、expected base SHA、requested HEAD SHA、Task Pack / Execution Pack identity、pinned standard revision、operator freedom、pull 状态机 `READY/CLAIMED/RUNNING/COMPLETED/BLOCKED/SUPERSEDED`）；Builder/Validator/Reviewer 不是三套队列状态机，`BuilderReadySet / ValidatorReadySet / ReviewerReadySet` 均为派生投影。
- `ai-dev:event:v2` 扩展（不引入 event-v3）：新增 `DISPATCH_CLAIMED`（worker role + CLAIMED 状态绑定）与 `EXECUTION_PACK_STATE_CHANGED`（scheduler/builder 发布 pack 分类）；dispatch_state 增加 pull 词汇（与 v3.3 lifecycle 词汇 alias 映射）；新增 `agent_freedom / pack_state / drift / execution_profile / requested_head_sha / current_pr_head / actual_checked_out_sha / expected_base_sha / queue_ref / task_pack_ref / execution_pack_ref` 字段；`VALIDATION_RESULT` 携带 `drift=HEAD_DRIFT` 时 schema 级禁止 `status=PASS`。
- JIT 分支规则：Queued Task 依赖完成前不建长命实现分支；默认 依赖合并 → 重算 ready set → 读取当前 integration exact SHA → 建 task 分支 → 生成/绑定 Execution Pack → 发 Builder dispatch；仅真实 stacked code dependency 例外。目标是消除 `ahead N / behind M / refresh / revalidate / rereview` 循环。
- #46 收敛为 Validator 执行档案 + 版本级 Validation Handoff Queue 投影：queue Issue 提供稳定入口、READY/HOLD 发现、exact-SHA identity、provenance 与 restart/recovery，但不是 validation/Task authority、不是独立 workflow 状态机；派生状态 `READY/HOLD/RUNNING/PASS/FAIL/BLOCKED/SUPERSEDED` 由 dispatch/gate facts 投影，多个并存条目确定性投影。
- Exact-SHA 验证规则硬化：执行前 `requested_head_sha == current PR HEAD`，否则 `HEAD_DRIFT` → dispatch superseded，不得作为 PASS evidence、不得静默切换新 HEAD；新候选要求新 dispatch identity；PASS 永远绑定 tested SHA × environment × profile × commands，不得改写到 successor SHA。
- 角色权威边界显式化：Builder 不得自我断言 Independent Review PASS；Validator 不得隐式修改产品源码/修复缺陷/重设计/弱化测试/合并/关闭实现 Issue（真实缺陷→FAIL；环境不可用→BLOCKED；修复必须单独 Builder dispatch）；Reviewer 在同一 review 角色/session 内不得修改产品代码，结果为 `REVIEW_PASS / CHANGES_REQUESTED / VALIDATION_REQUESTED / BLOCKED`，HEAD 变化自动失效 exact-head review。
- Worker 可恢复性：pull worker 崩溃后，替代 worker 仅凭 GitHub facts（dispatch 状态、claimed operator、已发布结果）决定 resume / supersede / nothing-to-do；duplicate claim 不同 operator 拒绝、相同 operator 幂等。
- Merge 闭环：merge 后自动重算 DAG ready sets，无人工提示词转发；baseline refresh ordering——不为已知将过期的 baseline 花费最终权威验证（先验证阻塞者、合并、刷新、再验证被阻塞者）。
- Local-first 执行：默认本地实现→focused tests→lint/typecheck/build→required tests→package→task-owned platform validation→stable HEAD→push→仅 required remote certification；CI 不是常规调试环；区分 required validation profile / normal execution provider / provider-specific attestation（不可替代）。
- Model preparation split：高风险语义允许 Web/Strong 预备紧凑 Semantic Kernel seed（contracts、predicates、fail-closed validators、negative oracle），repository mechanics 归本地 agent；扩展 MODEL_USAGE_POLICY 而非第二套模型路由。
- Local Agent Handoff 协议新增执行档案章节（builder/validator claim-time 身份核验、pack staleness、实现顺序、发布规则）与 worker recovery；handoff schema 增加 `execution_profile / agent_freedom / task_pack_ref / execution_pack_ref / expected_base_sha / requested_head_sha / queue_ref`，DISPATCHED validator handoff 强制 `requested_head_sha + validation_profile`。
- Validation Report schema 扩展 dispatch 身份字段（dispatch_id、expected_base_sha、requested_sha、actual_checked_out_sha、current_pr_head、focused_tests、working_tree_clean、source_modifications_after_validation）。
- 新模板与 bootstrap：`templates/task-pack.md`、`templates/execution-pack/`（核心 artifacts）、`templates/validation-handoff-queue.md`、`prompts/local-builder-bootstrap.md`、`prompts/local-validator-bootstrap.md`、`prompts/web-reviewer-bootstrap.md`；PROJECT_OVERRIDES 增加 `execution_pack.* / pull_worker.* / validation_queue.* / local_first.enabled` 可选字段；Execution Pack 材料必须可从 shipped artifacts 排除（package leakage 为 packaging gate defect）。
- 新增 `scripts/v34_rules.py`（确定性分类器：pack staleness、HEAD drift、validator outcome、freedom、queue projection、claim/recovery/merge/baseline-refresh/package-leak）与 `scripts/test_v34_lifecycle_contracts.py`（44 项正/对抗回归，覆盖场景 A–G、base drift、duplicate claim、review invalidation、package leakage）；`verify_standard.py` 增加 v3.4 semantic tokens 与 bootstrap-required 资产。
- Trunk/Fast Path 保持轻量：小任务可省略 large Execution Pack、Semantic Kernel seed、validation queue、dedicated worker 与非 required review，但保留 authority、exact identity、validation、evidence、merge safety。

## v3.3.0 — 2026-09-20

将未发布的 v3.2 machine-verifiable foundations、DomainHarness v0.2 实战暴露的 #24–#33 流程缺口，以及 current-main 的 Issue-first / Architecture Research Demo 增量收敛为一个可执行但不过度官僚化的标准版本。

- 新增 `standards/EXECUTION_ARCHITECTURE_STANDARD.md`，统一定义 durable facts、derived state、ready queues、dispatch lifecycle、staleness、bounded Merge/Candidate Freeze/Release/Repository Integration controllers；runtime automation 可选，GitHub/repository/evidence facts 仍是 durable Source of Truth。
- 明确 workflow state、Gate state、CI/provider state、dispatch state、candidate state、release state 是互相独立的维度，不得用一个状态替代另一个状态。
- Validation ownership 标准化为 `concern | integration | closure`：leaf Task 只承担最小严格 affected gates，Integration owner 承担跨组件 truth，Version Closure 承担 full regression/Critical Journeys/platform/packaging/Hidden/Release Qualification；`PR PASS != Release PASS` 保持不变。
- 精确区分 `HEAD drift / BASE drift / MERGE-RESULT drift / CANDIDATE drift`；旧 evidence 永远归属于实际执行的 `tested_sha`。只有显式 `VALIDATION_IMPACT_DECISION` 能在严格证明 impact=none 时复用 concern evidence，不能把 PASS 改写到未实际执行的 SHA。
- 将 CI execution channel/provider health 与 Validation Gate 解耦；支持 `AVAILABLE / INFRA_BLOCKED / TIMED_OUT / CANCELLED`。当 authority 要求 validation profile 而非 provider-specific attestation 时，可由等价或更强的 trusted clean exact-SHA executor 替代，并记录 `CI_INFRA_EXCEPTION`；provider-specific requirement 不得静默替代。
- Candidate Freeze 升级为 operational immutable state：冻结记录绑定 candidate SHA/tree/ref/visible evidence；冻结后禁止静默移动 candidate ref 或加入 product/docs/evidence commit。需要内容变化时必须 `THAWED/INVALIDATED → successor → affected visible validation → new freeze → required Hidden Validation → new Release Qualification`。
- Hidden Validation 增加 escaped-defect feedback loop：后续发现 release-significant defect 时区分 visible gap、hidden blind spot、pack defect 等；material blind spot 必须以独立 failure-family scenario 加强 private pack，并产生新的 immutable pack identity。
- Local Agent Handoff 增加 machine-verifiable completeness contract 和 `HANDOFF_READY`；完成后优先只发送 `repository + handoff issue` pointer，禁止在 chat 中维护第二份 task contract。
- `ai-dev:event:v2` 成为所有新 structured Agent events 的唯一 writer protocol；历史 v1 保持只读兼容。schema 扩展 dispatch、CI infra、validation impact、candidate、hidden escape、release qualification、repository integration events。
- 新增 `standard-manifest.json` active asset inventory，以及 Task Contract、Validation Report、Execution State、Local Agent Handoff、Agent Event v2 machine schemas；verifier 对缺失资产、schema drift、protocol/version drift 与关键语义回归 fail closed。
- 引入 executable immutable standard resolution：项目 pin 的 40-char revision 必须真实 resolve，且 exact revision 的 `VERSION` 必须与声明 SemVer 一致；禁止 syntactically-valid-but-nonexistent SHA 和 fallback 到 `main/latest`。
- 吸收 `TEST_DATA_AND_SCENARIO_STANDARD.md`：保留 schema/domain-invalid、boundary/adversarial/incomplete cases、risk-driven Golden、deterministic provenance、generator identity/hash 与“LLM 不得同时作为 generator+oracle+sole approver”等规则，并与 current Validation/Hidden authority 对齐。
- 吸收 provider-neutral `CI_EXECUTION_STANDARD.md` 与 `CI_RUNNER_CAPABILITY_STANDARD.md`，明确 provider/backend/runner/workflow source/shell/runtime/checkout semantics；Runner Capability 仅用于 routing，real preflight + exact-SHA evidence 才是 execution truth。
- 保留并正式打包 #34 `ISSUE_FIRST_TASK_TRIGGER.md`：Issue 是 durable current task contract，trigger prompt 仅负责短指针触发；`one task = one Issue = one trigger prompt`。该资产现在进入 manifest + bootstrap regression，不能与 manifest entry 一起被静默删除。
- 保留并正式打包 #36 Architecture Research Demo：只有 material Architecture UNKNOWN 且静态 evidence 不足时才进入 falsifiable executable demo；真实验证目标边界、negative/failure evidence、E1/E2/E3 strength、exact identity 和 mandatory `What was NOT proven` 都保持为回归约束。
- `GITHUB_WORKFLOW.md` 与 `VERSION_INTEGRATION_WORKFLOW.md` 收敛为稳定路径的 compatibility/navigation entries，不再复制整套 orchestration authority，减少规范漂移；Trunk/Fast Path、risk-based Independent Review 和 optional runtime automation 均继续保留。
- 标准仓库 CI 扩展为完整自验证链：`verify_standard.py`、verifier regression、project-standard resolution、project execution profile、protocol schemas、execution architecture regression、runner capability reference。

v3.3 是从 v3.1 的兼容 MINOR 演进；未单独发布 v3.2，其已验证 foundations 直接被 v3.3 收敛并由最终 exact-SHA validation/review 重新建立发布证据。

## v3.1.0 — 2026-09-18

为 GitHub-native Agent Interaction 增加 **Actor Role / Logical Operator Attribution**，解决 ChatGPT Web、Local Agent、CI、人工都通过同一个 GitHub 账号写 Issue/PR 时无法区分真实执行主体的问题。v3.0 的 Review Policy、Validation、Task DAG、Stacked PR 与 Release semantics 保持不变，因此是兼容 MINOR。

- 新 structured Agent events 升级为 `ai-dev:event:v2`；历史 `ai-dev:event:v1` 保持有效，不重写历史。
- Event v2 新增 `actor_role / operator_kind / operator_id / session_ref / transport_actor`，明确区分 workflow responsibility、logical executor、具体页面/进程/run 与 GitHub transport identity。
- `actor_role` 标准角色扩展为 `planner / builder / reviewer / validator / merge-controller / release-controller`。
- `operator_kind` 支持 `chatgpt-web / codex / claude-code / human / github-actions / woodpecker / other`；推荐 `operator_id` 例如 `chatgpt-web:web-a`、`chatgpt-web:web-b`、`codex:ubuntu-build-01`。
- 新增 `ROLE_CLAIMED / ROLE_RELEASED` 事件，用于记录哪个 logical operator 当前承担某个角色；role claim 只是 attribution/routing fact，不是 Gate PASS 或 distributed lock。
- 多个 ChatGPT Web 页面使用相同 GitHub 账号时，使用不同 `operator_id/session_ref`；动态 session/operator identity 不进入 GitHub labels，避免 label churn。
- required Independent Review 现在可以通过 operator attribution 审计 context independence：Builder 与 Reviewer 可共用同一个 GitHub transport account，但必须是可区分的逻辑 context。
- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`、`templates/agent-event-comment.md`、`standards/CHATGPT_WEB_ROLE.md`、Web/Local bootstrap prompts、项目 `PROJECT_OVERRIDES` 与 `AGENTS` 模板同步 Operator Attribution 语义。
- Local Agent / Validation event 必须能区分真正执行命令的本地 operator/run 与发起请求的 Web session，避免共享 GitHub author 造成错误归属。
- `verify_standard.py` 新增 v3.1 semantic guards：检查 Event v2、operator attribution 五字段、`ROLE_CLAIMED/ROLE_RELEASED` 与 v1 backward compatibility。

## v3.0.0 — 2026-09-18

将 v2.3.0 的 universal mandatory Independent Review 改为 **risk-based / on-demand Review Policy**。这是 mandatory Gate semantics 的不兼容变化，因此升级 MAJOR；Validation mandatory、Issue Dependency canonical Task DAG、Stacked PR code-baseline dependency、GitHub-native Agent Interaction 与 Release Authority 保持不变。

Breaking changes:

- Version Branch Mode 不再自动要求每个 Task/Fix PR 都完成 Independent Review；每个 Task/PR 现在显式声明 `required / recommended / not-required` Review Policy。
- `required`：Independent Review 是 merge gate，必须在当前 exact PR HEAD SHA 上满足；HEAD 变化后按影响执行 delta/full re-review。
- `recommended`：Review 是建议性的风险控制，可被显式执行或跳过；跳过使用结构化 policy decision 记录，不伪造 Review PASS，也不阻塞 merge。
- `not-required`：Review 不进入 Reviewer Queue，Review Gate 为 `NOT_APPLICABLE`；Task 满足其它 required merge prerequisites 后可直接进入 merge-ready。
- Review Policy authority 按 `Frozen PRD/Contract → Frozen Architecture → PROJECT_OVERRIDES → Task acceptance/Task DAG → standard risk defaults` 解析，不得因 Version Branch、CI disabled、单人项目或流程习惯自动升级为 mandatory。
- 高风险/关键变更 SHOULD 选择 `required`，包括 security/auth/permission、public API/external contract、schema/migration、shared infrastructure、high-risk concurrency/state、release-critical integration 等；普通实现可 `recommended`；机械性低风险变更可 `not-required`。
- Task DAG、Task Issue、Implementation PR、PROJECT_OVERRIDES、PR Review Checklist 与 GitHub metadata 增加 Review Policy；portable labels 使用 `review:required / review:recommended / review:not-required`。
- Builder 仅在 `required` 或本轮选择执行 `recommended` Review 时将 Task 路由到 `state:review-ready`；`not-required` 或明确跳过的 `recommended` Review 不应制造 Reviewer Queue 工作。
- 新增 `REVIEW_DECISION` 结构化 Agent event，用于记录 recommended Review 的 `skipped` 或 not-required 的 `not-applicable` 决策；Review 被执行时仍使用 exact-SHA `REVIEW_RESULT`。
- `prompts/independent-review-bootstrap.md` 改为 policy-aware：只用于 `required` 或明确调用的 `recommended` Review；遇到 `not-required` 时默认停止而不是制造形式化 Review Gate。
- 一旦 optional Review 实际执行，发现的有效 release-significant finding 仍是工程事实，必须修复、明确接受风险或按 authority 处置，不能因为 Review 原本不是 mandatory 就忽略。
- CI 与 Review 完全解耦：`CI profile=disabled` 仍要求真实 required Validation，但不自动要求 Independent Review；CI enabled 也不能替代 required Review 或 required Validation。
- Root AGENTS、README、Development Workflow、GitHub Workflow、Version Integration Workflow 与 ChatGPT Web Role 全部同步 risk-based Review 语义，避免旧 mandatory 规则残留。

## v2.3.0 — 2026-09-18

新增 GitHub-native Agent Interaction Protocol，将 Task DAG、Issue Dependency、Stacked PR、Independent Review 与 Builder/Reviewer/Validator 多会话协作统一进 v2.x 开发执行模型。

- 新增 `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`：定义 Issue body = stable contract、metadata = routing/current state、comments = append-oriented Agent event log、PR = code change、SHA = exact identity。
- Frozen Task DAG 继续作为 planning/history checkpoint；执行阶段 materialize 为 GitHub Task Issues + native Issue Dependencies，并把 Issue Dependency 定义为 canonical live execution DAG。
- 明确 Milestone / Sub-issue / Issue Dependency 的语义分层：Milestone 聚合版本，Sub-issue 表达 belongs-to hierarchy，Issue Dependency 表达 blocked-by / blocking；不得互相替代。
- 明确 Stacked PR 不是 Task DAG，只在下游 Task 必须建立在尚未合并的上游代码分支上时使用，表达 temporary code-baseline dependency；不得为了镜像 DAG 人工堆叠所有 PR。
- Stacked PR upstream merge 后，下游 PR 需要 rebase/retarget 到正确 parent/integration branch；SHA 改变后，受影响的 Review/Validation 必须重新建立。
- Version Branch Mode 的 Task/Fix PR merge 到 `version/vX.Y.Z` 前默认新增 mandatory Independent Review Gate；Review PASS 绑定 exact PR HEAD SHA，后续 commit 使旧 PASS 只保留历史意义，并要求 delta/full re-review。
- Independent Reviewer 的 final authority 默认与实现 context 分离；允许另一 ChatGPT session、另一 Agent、人类 reviewer，或同模型 fresh context 从 GitHub 独立重建事实。
- 新增 Builder / Reviewer / Validator queue model：Builder 主要消费 `state:ready` / `state:changes-requested`，Reviewer 消费 `state:review-ready`，Validator 消费 `state:validation-needed`；单一 blocker 不停止其它独立 implementation/review/validation。
- 新增 portable workflow metadata：`state:planned / ready / implementing / review-ready / reviewing / changes-requested / validation-needed / merge-ready / blocked / done`，并明确 workflow state 与 Gate status (`PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`) 不得混淆。
- 新增 `templates/task-issue.md`，把 Task Issue 固化为 stable work contract；新增 `templates/agent-event-comment.md` 与 `ai-dev:event:v1`，标准化 `IMPLEMENTATION_READY / REVIEW_RESULT / FIX_APPLIED / VALIDATION_REQUEST / VALIDATION_RESULT / DEPENDENCY_CHANGED / MERGE_RESULT` 等跨 Agent 事件。
- 新增 `prompts/independent-review-bootstrap.md`，让 Reviewer 仅凭 repository + PR/Issue + pinned standard 独立完成 exact-SHA Review。
- `templates/task-dag.md`、`templates/implementation-pr.md`、`checklists/pr-review.md`、`PROJECT_OVERRIDES`、项目 `AGENTS.md` 同步加入 execution DAG、stack topology、review evidence 与 merge-readiness 规则。
- Local Agent Handoff 与 Review workflow 打通：Reviewer 请求真实环境验证时 route 到 validation-needed；Local Agent PASS 后返回 review-ready；若本地修复改变源码/HEAD，则必须重新 Validation + Review。
- GitHub / Version Integration / Development Workflow / ChatGPT Web Role / Root AGENTS / README 同步接入新协议，确保多会话之间通过 GitHub facts 协作而非复制聊天记录。

## v2.2.0 — 2026-09-17

新增 provider-neutral CI Evidence Contract，将 CI/自动化验证发布到 Google Drive、S3、MinIO 或其它外部 backend 时的 identity、publication、integrity、discovery 与性能读取路径标准化，同时保持“Validation mandatory、CI 不是 Release Authority”的 v2.x 基线。

- 新增 `standards/CI_EVIDENCE_STANDARD.md`：定义 `manifest.json`、`validation-summary.json`、`environment.json`、`diagnostic.json`、`SHA256SUMS`、`completion.json` 与 workflow-level `latest.json` 的非重叠职责。
- immutable run identity 绑定 provider run + rerun/attempt + exact SHA，避免同一 pipeline rerun 覆盖历史 Evidence。
- `completion.json` 被定义为 Evidence publication commit marker；Validation FAIL 也可以 publication COMPLETE，反之 Validation PASS 也不能把 incomplete publication 视为完整证据。
- `latest.json` 只作为 mutable discovery/cache pointer，必须在 completion 之后更新，并要求 serialization / monotonic compare / CAS 等等价 stale-write protection；它不能成为 Validation 或 Release Authority。
- artifact 必须记录 producer check/state/provenance；producer 未 PASS 时不能把残留 workspace 文件包装成有效 build/package artifact。
- consumer-facing metadata 必须使用 Evidence-relative path；合法的 `artifacts/...` published namespace 与本地 staging root 必须按类型/存在性区分，不能靠简单字符串禁用。
- Validation profile 应保持 Validation Tuple 边界；不要用一个粗粒度命令混合 Windows packaged、Linux logic、visual/golden、Critical Journey、Hidden 或 release packaging 后再输出低信息量 blanket status。
- 增加 hot/evidence/diagnostic/audit/artifact 分层读取模型：日常状态优先读小型 pointer/summary，大日志和大型 binary artifact 仅按需读取。
- `VALIDATION_STANDARD.md`、`TESTING_STANDARD.md`、`RELEASE_STANDARD.md` 与 Agent/README 入口同步接入 CI Evidence Contract；标准仓库 verifier 要求核心合同文件存在。
- 新增 `references/CI_EVIDENCE_REFERENCE_VALIDATION.md`，记录 Formula Woodpecker → Google Drive 真实 pilot：Pipeline 5 验证 `validation FAIL + publication COMPLETE`；Pipeline 6 验证 9/9 checks PASS 但因 Evidence self-verifier namespace 缺陷 publication incomplete 且 latest 不前移；Pipeline 7 修复后完整 PASS 并发布 completion/latest；Pipeline 9 在 final reference SHA `73c5014c2db9a832d8d0c5be335240334f9bae24` 上执行 monotonic/stale/rerun/idempotent/conflict 反例回归并完整 PASS，Drive consumer-side 再确认 immutable run、completion 与 latest pointer。

## v2.1.0 — 2026-09-17

新增版本集成分支与通用 Local Agent Handoff，强化多 Task、多 Agent、跨环境验证时的 GitHub 事实链，同时保留小改动的 trunk 快速路径。

- 新增 `standards/VERSION_INTEGRATION_WORKFLOW.md`：大版本默认可采用 `task/fix → version/vX.Y.Z → main`，小型维护继续允许 `task/fix → main`。
- 明确 PRD Freeze、L1、L2、Task DAG、L3、Candidate、Validation、Closeout 是远端 checkpoint，不要求为了形式分别创建分支；Task/Concern 才是默认独立短分支边界。
- 明确 Validation Issue 本身不自动创建 branch；只有验证发现需要修改源码时才创建 `task/fix` 分支并 PR 到正确 integration branch，随后针对新 exact SHA 重跑 required gates。
- 推荐版本使用 GitHub Milestone，Label 表达稳定属性；新增 `type:*`、`handoff:local-agent`、`executor:*`、`gate:*`、`env:*`、`release-blocker`、`blocked:environment` 分类建议。
- 新增 `standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`，将 Codex-specific handoff 泛化为 Codex、Claude Code、Build Host Agent 或其它可信 execution agent 共用的 Issue contract。
- 新增 `templates/local-agent-handoff-issue.md`，补齐 Execution Environment、Validation Profile、Exact Commands、fixtures/services/credential assumptions、completion rule 与 blocker reporting。
- 新增 `prompts/local-agent-bootstrap.md`，使本地 Agent 只需 `repository + handoff issue` 即可按 pinned standard、baseline SHA、allowed/forbidden changes 和 required gates 初始化并执行。
- 分支数量本身不作为限制 Task isolation 的理由；成本敏感项目继续通过 Minimal CI 与本地/self-hosted validation 控制 GitHub-hosted CI 消耗，并遵守 repository large-file/artifact hygiene。

## v2.0.0 — 2026-09-15

基于 FastDev 真实 Pilot 重构执行模型：保留 CI，但默认最小化；将 Validation Evidence 提升为版本判断主链，并形式化 Gate Authority、Validation Tuple 与 blocker propagation。

Breaking changes:

- Validation 与 CI 解耦：Validation 是 mandatory；CI 是 execution mechanism，不再自动等同于完整验证或 Release Authority。
- CI profile 改为项目显式声明：`minimal / custom / disabled`；默认推荐 `minimal`，只运行低成本、确定性、clean-checkout 的独立 checks。
- Minimal CI 默认不承载完整多平台矩阵、Critical Journeys、Hidden Validation、高成本 E2E 或 packaging。
- 新增 Validation Tuple：`exact SHA × real platform> × <runtime/toolchain> × <validation profile>`；一个 tuple PASS 不能推导另一 tuple PASS。
- 新增 Required Gate Authority 顺序：Frozen PRD/Contract → Frozen Architecture → PROJECT_OVERRIDES → Task acceptance → Standard defaults；历史 workflow、旧脚本和 Agent 推测不能自动创建 mandatory release gate。
- 新增 DAG blocker propagation：BLOCKED 只阻塞依赖节点；其它独立工作继续执行，最终统一统计。
- 开发生命周期从机械 14 Phase 收敛为更少的 Stage：Baseline → Product/Scope → Architecture/Task → Implementation → Validation/PR/Minimal CI → Candidate → Hidden/Closure → Release。
- Candidate Prepared 与 Candidate Freeze 明确分离；Hidden Validation pack 可提前准备，但 execution 默认只针对 frozen candidate。
- Release Qualification 改为 exact-SHA required evidence 驱动；CI 只有在 frozen/project policy 明确要求时才成为 release-level gate。
- GitHub/PR/Validation 模板同步移除旧的 checkbox-only / CI-first 语义。

FastDev Pilot 直接验证了：Critical Journey 能发现真实产品缺陷、五状态 Gate 语义可审计、exact-SHA evidence 可替代 CI-first 执行模型，同时必须避免单 blocker 停止所有独立工作。

## v1.2.1 — 2026-09-15

修复 v1.2.0 已声明的 immutable project adoption contract 与 project verifier 不兼容问题，并增加最小 self-bootstrap regression。

- `scripts/verify_project_standard.py` 现在只接受 canonical `repository/version/revision` 三字段 identity，并验证 repository、SemVer、40-char hexadecimal revision、duplicate/missing/unknown keys 与未替换 placeholders。
- Legacy `ai-development-standard@vX.Y.Z` 单行 identity 不再作为 canonical PASS。
- 新增 `scripts/test_verify_project_standard.py`，用临时真实 project fixtures 通过 subprocess 覆盖 canonical PASS、legacy FAIL、missing/invalid identity、required-file 缺失等 regression cases。
- `standards/PROJECT_ADOPTION.md` 明确 immutable resolution procedure：exact revision、commit identity、root VERSION consistency、禁止 fallback 到 `main/latest`，并定义 resolution 的 FAIL/BLOCKED/NOT_RUN 语义。
- `standards/VALIDATION_STANDARD.md` 明确 `PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE` 的层级语义，包括 verifier FAIL 与 overall Adoption BLOCKED 可以同时成立，以及 mandatory downstream NOT_RUN 通常使 Release Qualification BLOCKED。
- `PROJECT_OVERRIDES` 模板明确 required-but-unestablished runner 应使用 `NOT_RUN — reason` 或 `BLOCKED — reason`，禁止伪造命令或用 `NOT_APPLICABLE` 隐藏 required gate。
- `verify-standard` CI 现在同时运行 repository verification 与 project-verifier regression suite；`verify_standard.py` 的 REQUIRED 增加与 self-bootstrap concern 直接相关的 executable/template assets。

## v1.2.0 — 2026-09-14

将 AI Development Standard 从流程规范扩展为跨项目工程基线，并参考成熟 GitHub 项目/模板制定可复用标准。

- 新增 `PROJECT_STRUCTURE.md`：定义单项目/monorepo 选择、apps/services/packages 职责、依赖方向、测试/生成内容/lockfile/root hygiene。
- 新增 `REPOSITORY_STANDARD.md`：定义 README/AGENTS/.dev-standard、GitHub metadata、branch protection、secret、dependency、artifact、script/tool 基线。
- 新增 `DOCUMENTATION_STANDARD.md`：定义 README/AGENTS/docs 职责、Single Source of Truth、PRD→Architecture→Task 关系、ADR、状态和历史文档治理。
- 新增 `TESTING_STANDARD.md`：定义 Unit/Contract/Integration/E2E/Critical Journey/Hidden Validation/Packaging 分层，以及 fixture、flaky、coverage、snapshot、external boundary 规则。
- 新增 `reference-architectures/MONOREPO.md`，将 monorepo 作为多子模块同一产品/平台的优先参考，而非强制所有项目采用。
- 新增 `templates/project/` 项目接入模板：README、AGENTS、CLAUDE、docs index、`.dev-standard/VERSION` 与 PROJECT_OVERRIDES。
- 新增 Project Init、PR Review、Version Closure checklists。
- 新增 `references/GITHUB_ENGINEERING_REFERENCES.md`，记录 Turborepo、GitHub Spec Kit、FastAPI Full Stack Template、Cookiecutter Django、Astral uv、VS Code 与 GitHub guidance 的采纳依据。
- 项目固定规范改为 `semantic version + immutable 40-char commit SHA`；tag 变为可选的人类友好别名，不再是强制依赖。
- Release identity 改为 SHA-first；PR PASS 明确不能替代 integrated Version Closure。
- 更新 Task DAG、Implementation PR、Codex Handoff、Final Closeout 模板，与新标准保持一致。

## v1.1.0 — 2026-09-14

新增 Stage Checkpoint Push 规则。

- 明确 Commit 与 Push 的职责不同：阶段内部可有多个本地 commit，不要求每次操作都 push。
- PRD、Architecture Evidence、Task DAG、L3、可审查 Task / Concern、Validation / Closeout 和 Release baseline 等正式阶段产物在成为后续依赖时必须形成远端 checkpoint。
- Implementation 以 Task / Concern 为主要远端同步单位，并继续遵循短分支 + PR + CI / Review 的合并方式。
- 长任务、多 Agent、跨会话工作在正式 Stage / Task checkpoint 主动 push，以支持从 GitHub commit 恢复。
- 将该规则加入 Agent 硬约束与 GitHub Workflow。

## v1.0.0 — 2026-09-14

首个冻结版本。

- 定义 Web-first + Codex Validation 主流程。
- GitHub 作为唯一代码与执行事实源。
- 定义 ChatGPT Web、Codex、Build Host、GitHub CI 四层职责。
- 定义 Codex Handoff Issue 协议。
- 定义 PR、Validation Report、Final Closeout 模板。
- 纳入 L1 / PRD / L2 / Task DAG / L3 / Implementation / Validation / Release 全流程。
- 定义项目级版本固定与 override 规则。
