# AGENTS.md

本仓库是 `AI Development Standard` 的权威规范源。

所有参与本仓库或引用本仓库的 AI Agent（包括 ChatGPT Web、Codex 及其它 coding agent）必须遵守以下顺序：

1. 先读取 `VERSION` 与本文件。
2. 根据当前角色读取：
   - ChatGPT Web → `standards/CHATGPT_WEB_ROLE.md`
   - Codex → `standards/CODEX_ROLE.md`
3. 涉及开发生命周期时读取 `standards/DEVELOPMENT_WORKFLOW.md`。
4. 涉及 ChatGPT → Codex 交接时读取 `standards/CODEX_HANDOFF_PROTOCOL.md`。
5. 涉及测试、构建或发布判断时读取 `standards/VALIDATION_STANDARD.md` 与 `standards/RELEASE_STANDARD.md`。
6. 业务项目存在 `.dev-standard/PROJECT_OVERRIDES.md` 时，在不违反本标准硬约束的前提下应用项目级覆盖。

## 硬约束

- GitHub repository state、commit、Issue、PR、CI 是执行事实；聊天记录不是事实源。
- 不得为了让测试或 CI 通过而降低测试强度、删除有效断言、跳过 required gate 或改变冻结需求。
- Codex 不得在 Handoff 阶段自行重新定义产品需求、领域语义、公共 API、数据语义、安全模型或架构边界。
- ChatGPT Web 在交接 Codex 前必须明确 baseline commit、已完成内容、剩余工作、required gates 和禁止修改项。
- 未完成 required gates 时不得宣称版本 READY。
- 任何无法确定的事实必须标为 `UNKNOWN`、`NOT VERIFIED` 或 `BLOCKED`，不得猜测为通过。

## 输出风格

执行报告优先使用可审计状态：`PASS / FAIL / NOT_RUN / NOT_APPLICABLE / BLOCKED`。每个 FAIL/BLOCKED 应尽可能提供 failing command、复现方式、根因或当前证据。
