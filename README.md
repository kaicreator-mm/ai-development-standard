# AI Development Standard

跨项目 AI 软件工程执行规范与工程基线。

当前版本：`v2.0.0`

v2.0 基于 FastDev 真实 Pilot 结果重构：保留 GitHub 事实链、PR、Critical Journey、Hidden Validation、Release Qualification 等核心工程约束，同时把 **Validation** 与 **CI** 解耦。

## 核心原则

1. **GitHub 是工程事实源**：repository state、commit SHA、Issue、PR、Review、Validation Evidence 与 Release identity 是可审计事实；聊天记录不是事实源。
2. **Validation 是 mandatory，CI 是 execution mechanism**：任何 required gate 都必须真实执行或如实标记状态；CI 不再等同于完整验证或 Release Authority。
3. **CI 默认最小化使用**：用于低成本、确定性、clean-checkout 的独立复核，不默认承载完整平台矩阵、Critical Journeys、Hidden Validation、昂贵 E2E 或 packaging。
4. **Exact-SHA Evidence**：验证结论必须绑定明确 commit SHA；平台验证还必须绑定真实 platform/runtime/toolchain profile。
5. **禁止为变绿而降低标准**：不得删除有效断言、跳过 required gate、擅自改变冻结需求、架构或 release blocker。
6. **规范必须固定到 immutable revision**：业务项目记录 semantic version + 40-char commit SHA，不隐式跟随 `main/latest`。
7. **Required Gate 有明确权威来源**：优先级为 Frozen PRD / Contract → Frozen Architecture → PROJECT_OVERRIDES → Task acceptance → Standard defaults。历史 workflow、旧脚本或 Agent 建议不能自动新增 mandatory release gate。
8. **Blocker 按依赖传播**：一个 Gate 的 `BLOCKED` 只阻塞依赖它的下游节点；所有独立可执行工作继续推进。
9. **One concern, one PR**：实现、验证、修复、文档等独立 concern 保持可审查边界；局部 PASS 不等于 Release PASS。
10. **Release Qualification 由完整 required evidence 决定**：Critical Journeys、Hidden Validation、真实 platform/build 与其它冻结 required gates 必须在 candidate identity 上形成真实证据。

## 标准生命周期

```text
Idea / Change Request
        ↓
Baseline / Scope
        ↓
L1 Product Evidence（按需）
        ↓
PRD / Scope Freeze
        ↓
L2 Architecture Evidence（按需）
        ↓
Task DAG + L3 Reference（按需）
        ↓
Implementation Concerns
        ↓
Local / Build Host Validation
        ↓
PR + Minimal CI（默认最小化）+ Review
        ↓
Integrated Baseline
        ↓
Candidate Preparation
        ↓
Required Visible Validation
        ↓
Candidate Freeze
        ↓
Hidden Validation
        ↓
Release Qualification
        ↓
Immutable Baseline SHA + optional Tag / Release
```

流程不是机械阶段瀑布。Bug、小修复、已冻结范围内的明确 Task 可以从最接近的阶段开始；但事实链、Validation 和 Release 判断不能省略。

## Minimal CI

v2.0 的默认 CI 目标是“最小独立复核”，而不是“把所有验证搬到云端”。

默认 Minimal CI SHOULD 包括：

- standard/project verifier；
- format/lint/typecheck 中与项目相关且确定性的部分；
- 快速 unit/contract smoke；
- basic build smoke。

默认 **不**在 Minimal CI 中执行：

- 多平台完整矩阵；
- 真实设备/SDK validation；
- Critical Journeys；
- Hidden Validation；
- 高成本 Docker/E2E；
- release packaging。

项目可通过 `.dev-standard/PROJECT_OVERRIDES.md` 声明 `minimal / custom / disabled` CI profile。若 CI 被显式禁用或不可用，项目必须保留 exact-SHA clean validation、Independent Review 与真实 Release Gate，不得把“没有 CI”解释成“没有验证”。

## Validation Tuple

需要矩阵验证时，最小证据单元是一个 Validation Tuple，例如：

```text
<exact SHA>
× <real platform>
× <runtime/toolchain>
× <validation profile>
```

一个 tuple 的 PASS 不能推导另一个 tuple PASS。平台或矩阵级 PASS 必须由其 required tuples 聚合得出。

## Gate 状态

所有 Gate 只使用：

```text
PASS
FAIL
BLOCKED
NOT_RUN
NOT_APPLICABLE
```

其中：

- `PASS`：已实际执行且满足 acceptance；
- `FAIL`：已实际执行但不满足 acceptance；
- `BLOCKED`：因前置条件、权限、工具、环境或标准缺陷无法完成；
- `NOT_RUN`：尚未执行；
- `NOT_APPLICABLE`：对当前 project/change 确实不适用。

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

### Agent Roles

- ChatGPT Web：[`standards/CHATGPT_WEB_ROLE.md`](standards/CHATGPT_WEB_ROLE.md)
- Codex / Build Host Execution：[`standards/CODEX_ROLE.md`](standards/CODEX_ROLE.md)
- Web → Codex：[`standards/CODEX_HANDOFF_PROTOCOL.md`](standards/CODEX_HANDOFF_PROTOCOL.md)
- 模型策略：[`standards/MODEL_USAGE_POLICY.md`](standards/MODEL_USAGE_POLICY.md)

## Templates / References / Checklists

- `templates/`：Task DAG、PR、Validation、Closeout 和项目接入模板。
- `reference-architectures/`：非强制结构参考。
- `checklists/`：Project Init、PR Review、Version Closure 等机械检查项。
- `references/`：公开工程 evidence/provenance。
- `prompts/`：L1/L2/L3 与 Agent 执行基线。
- `scripts/`：标准仓库自身或项目接入自动化。

## 版本策略

本仓库使用 SemVer：

- PATCH：措辞、模板、非语义性修正。
- MINOR：新增兼容的流程、Gate、模板或自动化能力。
- MAJOR：角色职责、Source of Truth、执行模型、mandatory Gate 或 release semantics 发生不兼容变化。

业务项目通过 `.dev-standard/VERSION` 固定：

```text
repository=kaicreator-mm/ai-development-standard
version=<semantic-version>
revision=<40-char-commit-sha>
```

`revision` 是不可变事实；tag/release 名称是可选的人类友好别名。
