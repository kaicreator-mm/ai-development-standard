# AGENTS.md

本仓库是 `AI Development Standard` 的权威规范源。

所有参与本仓库或引用本仓库的 AI Agent（包括 ChatGPT Web、Codex 及其它 coding/execution agent）必须遵守以下读取顺序：

1. 先读取 `VERSION` 与本文件。
2. 根据当前角色读取：
   - ChatGPT Web → `standards/CHATGPT_WEB_ROLE.md`
   - Codex / Build Host Execution → `standards/CODEX_ROLE.md`
3. 涉及开发生命周期时读取 `standards/DEVELOPMENT_WORKFLOW.md`。
4. 涉及 repository/project 组织时按需读取：
   - `standards/REPOSITORY_STANDARD.md`
   - `standards/PROJECT_STRUCTURE.md`
   - `standards/DOCUMENTATION_STANDARD.md`
   - `standards/TESTING_STANDARD.md`
5. 涉及 ChatGPT → Codex 交接时读取 `standards/CODEX_HANDOFF_PROTOCOL.md`。
6. 涉及测试、构建、Validation、Candidate、Closure 或发布判断时读取 `standards/VALIDATION_STANDARD.md` 与 `standards/RELEASE_STANDARD.md`。
7. 业务项目存在 `.dev-standard/PROJECT_OVERRIDES.md` 时，在不违反本标准硬约束的前提下应用项目级覆盖。

业务项目不应隐式读取本仓库最新 `main`；应以其 `.dev-standard/VERSION` 中记录的 immutable commit SHA 为准。

## 硬约束

- GitHub repository state、commit、Issue、PR、Review、Validation Evidence 与 Release identity 是执行事实；聊天记录不是事实源。
- Validation 是 mandatory；CI 只是 execution mechanism。不得用 CI PASS 代替未执行的 Critical Journey、Hidden Validation、真实 platform/build 或其它 required gate。
- CI 默认最小化：只做低成本、确定性、clean-checkout 的独立复核；不要默认把多平台矩阵、昂贵 E2E、Critical Journey、Hidden Validation 或 packaging 放入 CI。
- 正式 Stage 或 Task 形成后续步骤依赖的 Evidence、Contract、Task Definition、Validation 或 Release Artifact 时，必须形成 commit 并 push 为远端 checkpoint；阶段内部临时编辑不要求机械 push。
- Required Gate 的来源必须可追溯。优先级：Frozen PRD/Contract → Frozen Architecture → PROJECT_OVERRIDES → Task acceptance → Standard defaults。历史 workflow、旧脚本或 Agent 建议不能自行创建 mandatory release gate。
- Blocker 只阻塞依赖它的下游节点；其它独立可完成工作必须继续推进并最终统一统计。
- 不得为了让测试、Validation 或 CI 通过而降低测试强度、删除有效断言、跳过 required gate 或改变冻结需求。
- Codex / Execution Agent 不得在 Handoff 阶段自行重新定义产品需求、领域语义、公共 API、数据语义、安全模型或架构边界。
- ChatGPT Web 在交接执行 Agent 前必须明确 baseline commit、已完成内容、剩余工作、required gates、allowed/forbidden changes。
- 项目结构必须表达真实职责；不得为了匹配模板创建无职责模块，也不得把多个无关职责长期堆入 catch-all `common/utils/shared`。
- README/AGENTS/CLAUDE/docs 不得维护互相冲突的平行事实源。
- PR 局部 PASS 不得被解释为版本 Release PASS；Version Closure 必须在 integrated candidate/baseline 上完成 required release gates。
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
