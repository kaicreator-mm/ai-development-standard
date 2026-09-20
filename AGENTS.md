# AGENTS.md

本仓库是 `AI Development Standard` 的权威规范源。

所有参与本仓库或引用本仓库的 AI Agent（包括 ChatGPT Web、Codex、Claude Code 及其它 coding/execution/review agent）必须遵守以下读取顺序：

1. 先读取 `VERSION` 与本文件。
2. 根据当前角色读取：
   - ChatGPT Web / Builder / Reviewer → `standards/CHATGPT_WEB_ROLE.md`
   - Codex / Build Host / Local Execution Agent → `standards/CODEX_ROLE.md`
3. 涉及开发生命周期时读取 `standards/DEVELOPMENT_WORKFLOW.md`。
4. 涉及 L2 Architecture Evidence、未决架构假设、Architecture Research Demo / Spike 或 executable architecture evidence 时，读取 `standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md` 与 `prompts/L2_ARCHITECTURE_EVIDENCE.md`。
5. 涉及版本分支、Task 分支、Issue-based Task DAG、Builder/Reviewer/Validator 协作、structured event、Review Policy、Operator Attribution 或 Stacked PR 时读取：
   - `standards/VERSION_INTEGRATION_WORKFLOW.md`
   - `standards/GITHUB_WORKFLOW.md`
   - `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`
6. 涉及通过提示词触发 GitHub Issue 任务、向用户生成可复制任务提示词或把任务派发给 LLM/Agent 时，读取 `standards/ISSUE_FIRST_TASK_TRIGGER.md`。
7. 涉及 repository/project 组织时按需读取：
   - `standards/REPOSITORY_STANDARD.md`
   - `standards/PROJECT_STRUCTURE.md`
   - `standards/DOCUMENTATION_STANDARD.md`
   - `standards/TESTING_STANDARD.md`
8. 涉及 Web → 本地/执行 Agent 交接时读取 `standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`。`standards/CODEX_HANDOFF_PROTOCOL.md` 作为 Codex-specific 兼容入口。
9. 涉及测试、构建、Validation、Candidate、Closure 或发布判断时读取 `standards/VALIDATION_STANDARD.md` 与 `standards/RELEASE_STANDARD.md`。
10. 涉及将 CI / automated validation Evidence 发布到 Google Drive、S3、MinIO 或其它外部 Evidence backend 时，还必须读取 `standards/CI_EVIDENCE_STANDARD.md`。
11. 业务项目存在 `.dev-standard/PROJECT_OVERRIDES.md` 时，在不违反本标准硬约束的前提下应用项目级覆盖。

业务项目不应隐式读取本仓库最新 `main`；应以其 `.dev-standard/VERSION` 中记录的 immutable commit SHA 为准。

## 硬约束

- GitHub repository state、commit、Issue、Issue Dependency、PR、Review、Validation Evidence 与 Release identity 是执行事实；聊天记录不是事实源。
- GitHub username/API account 只是 transport identity，不足以区分 ChatGPT Web、Local Agent、CI 或人工的逻辑执行主体。
- v3.1+ 新 structured Agent events SHOULD 使用 `ai-dev:event:v2`，并记录 `actor_role / operator_kind / operator_id / session_ref / transport_actor`。历史 v1 events 保持有效，不重写历史。
- `actor_role` 表示流程职责；`operator_id/session_ref` 表示具体 Web 页面、Local Agent 或 run；`transport_actor` 表示向 GitHub 写入的账号/API identity。三者不得混为一谈。
- 多个 Web/Local contexts 使用同一个 GitHub 账号时，必须通过不同的 `operator_id/session_ref` 保持可审计区分；动态 operator/session identity 不应做成 GitHub label。
- required Independent Review 可以与 Builder 共用同一个 GitHub transport account，但 Reviewer 的 operator/context 必须与 Builder context 可审计地区分。
- Validation 是 mandatory；CI 只是 execution mechanism。不得用 CI PASS 代替未执行的 Critical Journey、Hidden Validation、真实 platform/build 或其它 required gate。
- Independent Review **不是所有 Task/Fix PR 的统一 mandatory gate**。每个 Task/PR 应根据权威来源与风险明确 `required / recommended / not-required` Review Policy。
- `review:required` 时，当前 merge-candidate exact SHA 必须有 Independent Review PASS；`review:recommended` 可执行也可显式 SKIP；`review:not-required` 的 Review Gate 为 `NOT_APPLICABLE`。
- Task/Agent 不得静默降低更高权威来源已经声明的 `required` Review Policy。
- Review 被执行时，Review PASS 绑定 exact reviewed SHA；若 Review 仍是 merge 所需 evidence 且 PR HEAD 改变，旧 PASS 只保留历史意义，必须 delta/full re-review。
- Architecture Research Demo 是风险驱动的 L2 evidence，不是每个 Task 的 mandatory stage/gate。只有 material Architecture UNKNOWN 且静态/源码/既有 evidence 不足时才应创建。
- Research Demo 必须从 falsifiable Hypothesis 开始；被验证边界必须真实，无关依赖才可以 deterministic fake；必须包含 negative/failure evidence、exact identity 与 mandatory `What was NOT proven`，不得用 toy example 外推 production readiness。
- PRD Freeze 后技术方案失败默认调整候选 Architecture；只有 executable evidence 证明 Frozen PRD 自身 contradiction/unachievable 时才请求重新打开产品范围。L2 Freeze 后普通 Task 直接实现，只有新出现的高影响 Architecture UNKNOWN 才重新进入 research/demo。
- CI 默认最小化：只做低成本、确定性、clean-checkout 的独立复核；不要默认把多平台矩阵、昂贵 E2E、Critical Journey、Hidden Validation 或 packaging 放入 CI。
- 启用外部 CI Evidence 发布时，immutable run、exact SHA、Validation Tuple、artifact producer/provenance、`completion.json` publication marker 与 concurrency-safe `latest.json` pointer 必须遵守 `CI_EVIDENCE_STANDARD.md`；`latest.json` 只能做 discovery/cache，不能成为 Release Authority。
- 正式 Stage 或 Task 形成后续步骤依赖的 Evidence、Contract、Task Definition、Validation 或 Release Artifact 时，必须形成 commit 并 push 为远端 checkpoint；阶段内部临时编辑不要求机械 push。
- PRD Freeze、L1/L2、Task DAG、L3、Candidate、Validation、Closeout 默认是 checkpoint 边界，不要求为每个阶段产物机械创建独立分支。
- Frozen Task DAG 是 planning/history checkpoint；采用 Issue-based execution 时，GitHub Task Issues + Issue Dependencies 是 canonical live execution DAG。
- Sub-issue 表达 belongs-to hierarchy，不自动等于 blocked-by；Stacked PR 只表达真实未合并 code-baseline dependency，不得替代 Issue Dependency 或被用来镜像整个 Task DAG。
- Substantial version SHOULD 使用 Version Branch Mode：Task/Fix 短分支合并到 `version/vX.Y.Z`，最终再由版本分支合并 `main`；小型低风险维护 MAY 使用 trunk/fast path。
- Implementation 默认以 Task / Concern 为短分支边界，并遵循 One concern, one PR。Validation-only Issue 不因为存在 Issue 而自动创建 branch；只有需要源码修改时才创建 task/fix branch。
- Issue body 是相对稳定的 work contract；metadata 表示当前路由状态；comments SHOULD 作为 append-oriented event log。跨 Agent 新关键事件优先使用 `templates/agent-event-comment.md` 的 `ai-dev:event:v2` 格式。
- GitHub Issue 已承载 Task contract 时，触发提示词必须遵守 `ISSUE_FIRST_TASK_TRIGGER.md`：提示词默认只负责触发执行，不重复维护 scope、步骤、baseline/branch、acceptance、gates、tests/CI 或 closeout 等 Issue 细节；执行 Agent 必须重新读取 current Issue，并以当前 GitHub 事实而不是旧复制提示词为准。
- 向用户同时提供多个任务触发提示词时，必须一任务一个独立可复制区域；不得把多个任务提示词放进同一个可复制块。优先保持 `one task = one Issue = one trigger prompt`。
- `ROLE_CLAIMED/ROLE_RELEASED` 用于记录哪个 logical operator 正在承担某个角色；它们是 attribution/routing facts，不是 Validation PASS，也不是 distributed lock。
- Workflow `state:*`、Review Policy `review:*` 与 Gate status 不得混淆。Gate 只能使用 `PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`。
- Required Gate 的来源必须可追溯。优先级：Frozen PRD/Contract → Frozen Architecture → PROJECT_OVERRIDES → Task acceptance → Standard defaults。历史 workflow、旧脚本或 Agent 建议不能自行创建 mandatory release gate。
- Blocker 只阻塞依赖它的下游节点；其它独立可完成工作必须继续推进并最终统一统计。
- 不得为了让测试、Validation、Review 或 CI 通过而降低测试强度、删除有效断言、跳过 required gate 或改变冻结需求。
- Codex / Local Execution Agent 不得在 Handoff 阶段自行重新定义产品需求、领域语义、公共 API、数据语义、安全模型或架构边界。
- ChatGPT Web 在交接执行 Agent 前必须明确 baseline commit、integration branch、已完成内容、剩余工作、required gates、execution environment、allowed/forbidden changes、source operator attribution 与 completion rule。
- Local Agent Handoff Issue 必须可由 `repository + issue` 独立执行，不依赖隐藏聊天上下文；任务特定事实属于 Issue，通用执行纪律属于 pinned standard / bootstrap prompt。
- 项目结构必须表达真实职责；不得为了匹配模板创建无职责模块，也不得把多个无关职责长期堆入 catch-all `common/utils/shared`。
- README/AGENTS/CLAUDE/docs 不得维护互相冲突的平行事实源。
- PR 局部 PASS / Review PASS 不得被解释为版本 Release PASS；Version Closure 必须在 integrated candidate/baseline 上完成 required release gates。
- 未完成 required gates 时不得宣称版本 READY。
- 任何无法确定的事实必须标为 `UNKNOWN`、`NOT VERIFIED`、`NOT_RUN` 或 `BLOCKED`，不得猜测为通过。

## Validation Tuple

需要矩阵验证时，一个 PASS 只能证明一个明确 tuple：

```text
<exact SHA> × <real platform> × <runtime/toolchain> × <validation profile>
```

一个 tuple 的 PASS 不得推导另一个 tuple PASS。聚合 Gate 必须由其 required tuples 真实聚合得出。

## 输出状态

Gate 只能使用：

```text
PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE
```

每个 FAIL/BLOCKED 应尽可能提供 failing command、exit code（若已启动）、关键日志、复现、根因、影响与下游 blocking level。
