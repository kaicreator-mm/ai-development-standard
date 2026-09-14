# AI Development Standard

跨项目 AI 软件工程执行规范与工程基线。该仓库定义 ChatGPT Web、Codex、GitHub、Build Host 与 CI 在软件开发生命周期中的统一职责，也定义项目结构、文档、测试、测试数据/Scenario、repository hygiene、模板和 release closure 规则。

当前版本：`v1.3.0`

## 核心原则

1. **GitHub 是代码与执行状态的唯一事实源（Source of Truth）**。聊天记录不能替代 repository state、Issue、PR、commit 或 CI 结果。
2. **ChatGPT Web 优先完成智能密集型工作**：需求澄清、产品/架构研究、PRD、Task DAG、实现、测试设计、代码审查与 Closeout。
3. **Codex 只接手剩余工程闭环**：完整 Build Host 上的真实编译、平台构建、Integration/E2E/Hidden Validation、环境问题复现和最小必要修复。
4. **GitHub CI 是独立裁判**。任何 Agent 的“本地通过”不能替代 required CI gates。
5. **不为 CI 变绿而改变需求**。禁止删除断言、降低测试标准、跳过 required test 或擅自改变冻结的产品/架构语义。
6. **规范必须固定到 immutable revision**。业务项目记录 semantic version + 40-char commit SHA；tag 可选，不隐式跟随 `main/latest`。
7. **过程对象分工明确**：长期规则放仓库文件；单次工作交接放 Issue；真实变更集放 PR；最终事实由 commit + CI + Validation Report 证明。
8. **正式阶段必须留下远端 checkpoint**。PRD、Architecture、Task DAG、L3、可审查 Task、Validation/Closeout 等形成后续依赖时，应 commit + push；阶段内部临时编辑不要求逐步 push。
9. **结构服务于职责，不服务于形式**。复杂多模块产品优先考虑 monorepo，但不创建无职责的空层级。
10. **PR PASS ≠ Release PASS**。版本 Closure 在 integrated baseline 上执行完整 required regression、Critical Journeys、Hidden Validation、真实 packaging/platform 和 Release Qualification。
11. **测试数据也是工程资产**。模拟数据、Golden、Scenario、Regression 与 Hidden Validation Data 必须有来源、规则、覆盖与可重复性证据；LLM 不能凭自评把自己生成的答案提升为 Golden truth。

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
Implementation
        ↓
Web / Local Validation
        ↓
GitHub Baseline / Handoff
        ↓
PR → CI → Review → Merge main
        ↓
Version Closure
        ↓
Critical Journeys / Hidden Validation / Packaging
        ↓
Release Qualification
        ↓
Immutable baseline SHA + optional Tag / Release
```

正式阶段产物在进入下一阶段前按 `Stage Checkpoint Push` 规则形成远端 checkpoint。不是所有任务都必须机械执行 L1/L2/L3；Bug、小修复、已冻结范围内的实现可以从最接近阶段开始，但验证和 GitHub 事实链不能省略。

## 规范入口

### Lifecycle / Git / Release

- Agent 总入口：[`AGENTS.md`](AGENTS.md)
- 完整开发流程：[`standards/DEVELOPMENT_WORKFLOW.md`](standards/DEVELOPMENT_WORKFLOW.md)
- GitHub 工作流：[`standards/GITHUB_WORKFLOW.md`](standards/GITHUB_WORKFLOW.md)
- Validation：[`standards/VALIDATION_STANDARD.md`](standards/VALIDATION_STANDARD.md)
- Release：[`standards/RELEASE_STANDARD.md`](standards/RELEASE_STANDARD.md)
- 项目接入：[`standards/PROJECT_ADOPTION.md`](standards/PROJECT_ADOPTION.md)

### Project Engineering Baseline

- Repository 基线：[`standards/REPOSITORY_STANDARD.md`](standards/REPOSITORY_STANDARD.md)
- 项目/Monorepo 结构：[`standards/PROJECT_STRUCTURE.md`](standards/PROJECT_STRUCTURE.md)
- 文档规范：[`standards/DOCUMENTATION_STANDARD.md`](standards/DOCUMENTATION_STANDARD.md)
- 测试规范：[`standards/TESTING_STANDARD.md`](standards/TESTING_STANDARD.md)
- 测试数据 / Scenario：[`standards/TEST_DATA_AND_SCENARIO_STANDARD.md`](standards/TEST_DATA_AND_SCENARIO_STANDARD.md)

### Agent Roles

- ChatGPT Web：[`standards/CHATGPT_WEB_ROLE.md`](standards/CHATGPT_WEB_ROLE.md)
- Codex：[`standards/CODEX_ROLE.md`](standards/CODEX_ROLE.md)
- Web → Codex：[`standards/CODEX_HANDOFF_PROTOCOL.md`](standards/CODEX_HANDOFF_PROTOCOL.md)
- 模型策略：[`standards/MODEL_USAGE_POLICY.md`](standards/MODEL_USAGE_POLICY.md)

## Templates / References / Checklists / Examples

- `templates/`：Task DAG、PR、Validation、Closeout 和可复制的 `templates/project/` 项目接入基线。
- `reference-architectures/`：非强制的实现/结构参考，例如 monorepo。
- `checklists/`：Project Init、PR Review、Version Closure、Test Data Review 等机械执行清单。
- `references/`：制定标准时采用的公开工程 evidence/provenance。
- `prompts/`：L1/L2/L3、Agent 执行以及 Test Data Generation 基线。
- `scripts/`：标准仓库自身或项目接入自动化，包括 Test Data Pack verifier。
- `examples/`：标准自身的 executable/reference examples；`examples/test-data-pack/quote-assessment/` 展示从规则→Scenario→模拟数据→验证→反馈标准的闭环。

## 外部工程参考

本标准参考优秀公开项目/模板的稳定工程实践，但不绑定其技术栈。工程基线证据见 [`references/GITHUB_ENGINEERING_REFERENCES.md`](references/GITHUB_ENGINEERING_REFERENCES.md)。测试数据标准额外参考 Hypothesis、Faker 与 Schemathesis 的 property-based、reproducible generation、schema-driven generation/replay 思路，详见 [`references/TEST_DATA_ENGINEERING_REFERENCES.md`](references/TEST_DATA_ENGINEERING_REFERENCES.md)。

## 版本策略

本仓库使用 SemVer：

- PATCH：措辞、模板、非语义性修正。
- MINOR：新增兼容的流程、Gate、模板、标准或自动化能力。
- MAJOR：角色职责、Source of Truth、交接模型、必选 Gate 等发生不兼容变化。

业务项目通过 `.dev-standard/VERSION` 固定：

```text
repository=kaicreator-mm/ai-development-standard
version=<semantic-version>
revision=<40-char-commit-sha>
```

`revision` 是实际不可变事实；tag/release 名称可以存在，但不是强制依赖。
