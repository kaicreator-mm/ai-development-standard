# AI Development Standard

跨项目 AI 软件工程执行规范。该仓库定义 ChatGPT Web、Codex、GitHub、Build Host 与 CI 在软件开发生命周期中的统一职责、交接协议、验证门槛和发布规则。

当前版本：`v1.0.0`

## 核心原则

1. **GitHub 是代码与执行状态的唯一事实源（Source of Truth）**。聊天记录不能替代 repository state、Issue、PR、commit 或 CI 结果。
2. **ChatGPT Web 优先完成智能密集型工作**：需求澄清、产品/架构研究、PRD、Task DAG、实现、测试设计、代码审查与 Closeout。
3. **Codex 只接手剩余工程闭环**：完整 Build Host 上的真实编译、平台构建、Integration/E2E/Hidden Validation、环境问题复现和最小必要修复。
4. **GitHub CI 是独立裁判**。任何 Agent 的“本地通过”不能替代 required CI gates。
5. **不为 CI 变绿而改变需求**。禁止删除断言、降低测试标准、跳过 required test 或擅自改变冻结的产品/架构语义。
6. **规范版本必须固定**。业务项目必须记录采用的本规范版本，升级规范应显式进行，而不是隐式跟随 `main`。
7. **过程对象分工明确**：长期规则放仓库文件；单次工作交接放 Issue；真实变更集放 PR；最终事实由 commit + CI + Validation Report 证明。

## 标准流程

```text
Idea / Change Request
        ↓
L1 Product Evidence（需要时）
        ↓
PRD / Scope Freeze
        ↓
L2 Architecture Evidence（需要时）
        ↓
Task DAG
        ↓
L3 Implementation Evidence（任务需要时）
        ↓
ChatGPT Web Implementation
        ↓
Web Validation
        ↓
GitHub Commit / Branch
        ↓
Codex Handoff Issue
        ↓
Codex + Build Host Validation / Minimal Fix
        ↓
Pull Request
        ↓
GitHub CI
     ↙      ↘
   FAIL     GREEN
    ↓         ↓
 Codex     Final Closeout
    ↓         ↓
 CI again  Merge / Tag / Release
```

不是所有任务都必须机械执行 L1/L2/L3。Bug、小修复、已冻结范围内的实现可以从最接近的阶段开始，但验证和 GitHub 事实链不能省略。

## 入口文档

- Agent 总入口：[`AGENTS.md`](AGENTS.md)
- 完整开发流程：[`standards/DEVELOPMENT_WORKFLOW.md`](standards/DEVELOPMENT_WORKFLOW.md)
- ChatGPT Web 职责：[`standards/CHATGPT_WEB_ROLE.md`](standards/CHATGPT_WEB_ROLE.md)
- Codex 职责：[`standards/CODEX_ROLE.md`](standards/CODEX_ROLE.md)
- Web → Codex 交接：[`standards/CODEX_HANDOFF_PROTOCOL.md`](standards/CODEX_HANDOFF_PROTOCOL.md)
- 验证门槛：[`standards/VALIDATION_STANDARD.md`](standards/VALIDATION_STANDARD.md)
- GitHub 对象与分支规范：[`standards/GITHUB_WORKFLOW.md`](standards/GITHUB_WORKFLOW.md)
- 发布与 Closeout：[`standards/RELEASE_STANDARD.md`](standards/RELEASE_STANDARD.md)
- 模型使用策略：[`standards/MODEL_USAGE_POLICY.md`](standards/MODEL_USAGE_POLICY.md)
- 项目接入方式：[`standards/PROJECT_ADOPTION.md`](standards/PROJECT_ADOPTION.md)

## 模板

`templates/` 中的文件用于生成 Task DAG、Codex Handoff Issue、PR、Validation Report 和 Final Closeout。

## 研究提示词

`prompts/` 提供跨项目 L1/L2/L3 研究基线以及 Codex 执行基线。业务项目可以在不改变核心约束的前提下增加领域专用内容。

## 版本策略

本仓库使用 SemVer：

- PATCH：措辞、模板、非语义性修正。
- MINOR：新增兼容的流程、Gate、模板或自动化能力。
- MAJOR：角色职责、Source of Truth、交接模型、必选 Gate 等发生不兼容变化。

业务项目应固定到 tag，例如 `ai-development-standard@v1.0.0`，不要直接声明“遵循最新 main”。
