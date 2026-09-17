# AGENTS.md

本仓库是 `AI Development Standard` 的权威规范源。

所有参与本仓库或引用本仓库的 AI Agent（包括 ChatGPT Web、Codex、Claude Code 及其它 coding/execution/review agent）必须遵守以下读取顺序：

1. 先读取 `VERSION` 与本文件。
2. 根据当前角色读取：
   - ChatGPT Web / Builder / Reviewer → `standards/CHATGPT_WEB_ROLE.md`
   - Codex / Build Host / Local Execution Agent → `standards/CODEX_ROLE.md`
3. 涉及开发生命周期时读取 `standards/DEVELOPMENT_WORKFLOW.md`。
4. 涉及版本分支、Task 分支、Issue-based Task DAG、Builder/Reviewer/Validator 协作、structured event 或 Stacked PR 时读取：
   - `standards/VERSION_INTEGRATION_WORKFLOW.md`
   - `standards/GITHUB_WORKFLOW.md`
   - `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`
5. 涉及 repository/project 组织时按需读取：
   - `standards/REPOSITORY_STANDARD.md`
   - `standards/PROJECT_STRUCTURE.md`
   - `standards/DOCUMENTATION_STANDARD.md`
   - `standards/TESTING_STANDARD.md`
6. 涉及 Web → 本地/执行 Agent 交接时读取 `standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`。`standards/CODEX_HANDOFF_PROTOCOL.md` 作为 Codex-specific 兼容入口。
7. 涉及测试、构建、Validation、Candidate、Closure 或发布判断时读取 `standards/VALIDATION_STANDARD.md` 与 `standards/RELEASE_STANDARD.md`。
8. 涉及将 CI / automated validation Evidence 发布到 Google Drive、S3、MinIO 或其它外部 Evidence backend 时，还必须读取 `standards/CI_EVIDENCE_STANDARD.md`。
9. 业务项目存在 `.dev-standard/PROJECT_OVERRIDES.md` 时，在不违反本标准硬约束的前提下应用项目级覆盖。

业务项目不应隐式读取本仓库最新 `main`；应以其 `.dev-standard/VERSION` 中记录的 immutable commit SHA 为准。

## 硬约束

- GitHub repository state、commit、Issue、Issue Dependency、PR、Review、Validation Evidence 与 Release identity 是执行事实；聊天记录不是事实源。
- Validation 是 mandatory；CI 只是 execution mechanism。不得用 CI PASS 代替未执行的 Critical Journey、Hidden Validation、真实 platform/build 或其它 required gate。
- CI 默认最小化：只做低成本、确定性、clean-checkout 的独立复核；不要默认把多平台矩阵、昂贵 E2E、Critical Journey、Hidden Validation 或 packaging 放入 CI。
- 启用外部 CI Evidence 发布时，immutable run、exact SHA、Validation Tuple、artifact producer/provenance、`completion.json` publication marker 与 concurrency-safe `latest.json` pointer 必须遵守 `CI_EVIDENCE_STANDARD.md`；`latest.json` 只能做 discovery/cache，不能成为 Release Authority。
- 正式 Stage 或 Task 形成后续步骤依赖的 Evidence、Contract、Task Definition、Validation 或 Release Artifact 时，必须形成 commit 并 push 为远端 checkpoint；阶段内部临时编辑不要求机械 push。
- PRD Freeze、L1/L2、Task DAG、L3、Candidate、Validation、Closeout 默认是 checkpoint 边界，不要求为每个阶段产物机械创建独立分支。
- Frozen Task DAG 是 planning/history checkpoint；采用 Issue-based execution 时，GitHub Task Issues + Issue Dependencies 是 canonical live execution DAG。
- Sub-issue 表达 belongs-to hierarchy，不自动等于 blocked-by；Stacked PR 只表达真实未合并 code-baseline dependency，不得替代 Issue Dependency 或被用来镜像整个 Task DAG。
- Substantial version SHOULD 使用 Version Branch Mode：Task/Fix 短分支合并到 `version/vX.Y.Z`，最终再由版本分支合并 `main`；小型低风险维护 MAY 使用 trunk/fast path。
- Implementation 默认以 Task / Concern 为短分支边界，并遵循 One concern, one PR。Validation-only Issue 不因为存在 Issue 而自动创建 branch；只有需要源码修改时才创建 task/fix branch。
- Version Branch Mode 的 Task/Fix PR merge 到 version branch 前，默认 MUST 完成当前 exact PR HEAD SHA 上的 required task Validation + Independent Review + configured required Minimal CI（若启用），并满足 merge 所需 Issue Dependencies。
- Independent Review 的 final authority SHOULD 与刚完成实现的 context 独立；另一 Session/Agent/人类均可，同模型 fresh context 也可，只要从 GitHub 重新建立事实。
- Review PASS 绑定 exact reviewed SHA；PR HEAD 改变后旧 PASS 只保留历史意义，当前 Review Gate 回到 `NOT_RUN`，必须执行 delta/full re-review。
- Issue body 是相对稳定的 work contract；metadata 表示当前路由状态；comments SHOULD 作为 append-oriented event log。跨 Agent 关键事件优先使用 `templates/agent-event-comment.md` 的 `ai-dev:event:v1` 格式。
- Workflow `state:*` 与 Gate status 不得混淆。Gate 只能使用 `PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE`。
- Required Gate 的来源必须可追溯。优先级：Frozen PRD/Contract → Frozen Architecture → PROJECT_OVERRIDES → Task acceptance → Standard defaults。历史 workflow、旧脚本或 Agent 建议不能自行创建 mandatory release gate。
- Blocker 只阻塞依赖它的下游节点；其它独立可完成工作必须继续推进并最终统一统计。
- 不得为了让测试、Validation、Review 或 CI 通过而降低测试强度、删除有效断言、跳过 required gate 或改变冻结需求。
- Codex / Local Execution Agent 不得在 Handoff 阶段自行重新定义产品需求、领域语义、公共 API、数据语义、安全模型或架构边界。
- ChatGPT Web 在交接执行 Agent 前必须明确 baseline commit、integration branch、已完成内容、剩余工作、required gates、execution environment、allowed/forbidden changes 与 completion rule。
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
