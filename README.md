# AI Development Standard

跨项目 AI 软件工程执行规范与工程基线。

当前版本：`v2.3.0`

v2.3 在 v2.2 的 Version Branch / Local Agent Handoff / CI Evidence 基础上增加 **GitHub-native Agent Interaction Protocol**：Frozen Task DAG 继续作为规划与历史 checkpoint，进入执行后由 GitHub Task Issues + Issue Dependencies 承担 canonical live Task DAG；Builder、Independent Reviewer、Validator 通过 Issue metadata/state 与结构化事件协作；Stacked PR 只处理真实未合并 code-baseline dependency，不再与 Task DAG 混用。

## 核心原则

1. **GitHub 是工程事实源**：repository state、commit SHA、Issue、Issue Dependency、PR、Review、Validation Evidence 与 Release identity 是可审计事实；聊天记录不是事实源。
2. **Planning DAG 与 Execution DAG 分层**：Frozen Task DAG 文档记录规划依据；GitHub Task Issues + Issue Dependencies 是 canonical live execution DAG。
3. **Hierarchy ≠ Dependency**：Milestone 聚合版本，Sub-issue 表达 belongs-to，Issue Dependency 表达 blocked-by；三者不能混用。
4. **Stacked PR ≠ Task DAG**：Stacked PR 只在 Task 必须基于另一个尚未合并的代码分支时使用；它表达 code-baseline dependency，不替代 Issue Dependency。
5. **Independent Review 是 Version Branch Task merge gate**：Task/Fix PR 合并 `version/vX.Y.Z` 前默认必须在当前 exact HEAD SHA 上完成 required Validation + Independent Review + configured required CI（若启用）。
6. **Review 也绑定 exact SHA**：PR HEAD 改变后，旧 Review PASS 只对旧 SHA 有效；新 HEAD 必须 delta/full re-review。
7. **多会话通过 GitHub 协作**：Builder、Reviewer、Validator 不交换隐藏聊天上下文；Issue body 是合同、metadata 是当前状态、comments 是事件历史、PR 是代码变化、SHA 是身份。
8. **Validation 是 mandatory，CI 是 execution mechanism**：任何 required gate 都必须真实执行或如实标记状态；CI 不等同于完整验证或 Release Authority。
9. **CI 默认最小化使用**：用于低成本、确定性、clean-checkout 的独立复核，不默认承载完整平台矩阵、Critical Journeys、Hidden Validation、昂贵 E2E 或 packaging。
10. **Exact-SHA Evidence**：验证和 Review 结论必须绑定明确 commit SHA；平台验证还必须绑定真实 platform/runtime/toolchain profile。
11. **禁止为变绿而降低标准**：不得删除有效断言、跳过 required gate、擅自改变冻结需求、架构或 release blocker。
12. **规范必须固定到 immutable revision**：业务项目记录 semantic version + 40-char commit SHA，不隐式跟随 `main/latest`。
13. **Required Gate 有明确权威来源**：Frozen PRD / Contract → Frozen Architecture → PROJECT_OVERRIDES → Task acceptance → Standard defaults。
14. **Blocker 按依赖传播**：一个 Gate/Task 的 blocker 只沿实际 dependency edge 传播；所有独立可执行工作继续推进。
15. **One concern, one PR**：实现 Task/Fix 使用可审查短分支；局部 PASS/Review PASS 不等于 Release PASS。
16. **Stage Artifact 是 checkpoint，不是默认 branch**：PRD Freeze、L1/L2、Task DAG、L3、Candidate、Validation、Closeout 在成为下游依赖时必须形成远端 checkpoint，但不要求逐阶段机械建分支。
17. **Substantial version 优先 Version Branch Mode**：`task/fix → version/vX.Y.Z → main`；小型、低风险、范围明确的维护可以走 trunk/fast path。
18. **Local Agent Handoff 以 Issue 为合同**：任务特定事实放 Issue，通用执行纪律放 pinned standard / bootstrap prompt；本地 Agent 应能仅凭 repository + issue 恢复执行。
19. **Release Qualification 由完整 required evidence 决定**：Critical Journeys、Hidden Validation、真实 platform/build 与其它 frozen required gates 必须在 candidate identity 上形成真实证据。
20. **外部 CI Evidence 必须事务化发布**：immutable evidence 与 mutable discovery pointer 分离；只有完整发布并形成 `completion.json` 的 run 才能更新 `latest.json`，且旧 run 不得覆盖新 pointer。

## 标准生命周期

```text
Idea / Change Request
        ↓
Baseline / Scope
        ↓
L1 Product Evidence（按需）
        ↓
PRD / Scope Freeze checkpoint
        ↓
L2 Architecture Evidence（按需）
        ↓
Frozen Task DAG + L3 Reference（按需）
        ↓
Task Issues + Issue Dependencies
        ↓
Builder Implementation
        ↓
Task Validation
        ↓
PR → Independent Review
        ↓
Local Validation（按需）
        ↓
Merge Ready
        ↓
Version Branch Integrated Baseline
        ↓
Candidate Preparation / Visible Validation
        ↓
Candidate Freeze
        ↓
Hidden Validation
        ↓
Release Qualification
        ↓
Immutable Baseline SHA + optional Tag / Release
```

流程不是机械阶段瀑布。Bug、小修复、已冻结范围内明确 Task 可以从最接近的阶段开始；但事实链、Validation、Review 和 Release 判断不能伪造或跳过 required 部分。

## Task DAG / GitHub Execution DAG

推荐模型：

```text
Frozen Task DAG document
        ↓ materialize
GitHub Task Issues
        ↓
Issue Dependencies      ← canonical live Task DAG
        ↓
Task Branch / PR
        ↓
Stacked PR（只有真实 code-baseline dependency 时）
```

对象职责：

```text
Task DAG document = 规划理由 / 历史 checkpoint
Milestone         = 版本聚合
Sub-issue         = belongs-to hierarchy
Issue Dependency  = execution blocked-by / blocking
Task Branch / PR  = 实现与 Review 边界
Stacked PR        = 可选的未合并代码基线依赖
```

因此 Task DAG 不需要为了表达依赖而建 branch；执行依赖直接 materialize 为 Issue Dependency。

## Builder / Reviewer / Validator Interaction

推荐 mutable workflow states：

```text
state:planned
state:ready
state:implementing
state:review-ready
state:reviewing
state:changes-requested
state:validation-needed
state:merge-ready
state:blocked
state:done
```

这些是 workflow routing state，不是 Gate 状态。Gate 仍只使用：

```text
PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE
```

典型流水线：

```text
Builder A                         Reviewer B
T01 implementation
  ↓
PR #101 + review-ready ─────────→ exact-SHA review
T02 implementation                ↓
  ↓                         PASS / findings / validation request
PR #102 + review-ready ─────────→ review
T03 implementation                ↓
...                              ...
```

Builder 不必等待 Reviewer 才开始其它独立 Task；Reviewer 也不应因为一个独立 PR FAIL 停止其它 Review。

跨 Agent 的关键事件 SHOULD 使用：

```html
<!-- ai-dev:event:v1 -->
```

并记录 `IMPLEMENTATION_READY / REVIEW_RESULT / FIX_APPLIED / VALIDATION_REQUEST / VALIDATION_RESULT / DEPENDENCY_CHANGED / MERGE_RESULT` 等结构化事件。

完整协议：[`standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`](standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md)  
Task Issue 模板：[`templates/task-issue.md`](templates/task-issue.md)  
Agent Event 模板：[`templates/agent-event-comment.md`](templates/agent-event-comment.md)  
Independent Review Prompt：[`prompts/independent-review-bootstrap.md`](prompts/independent-review-bootstrap.md)

## Version Integration

### Version Branch Mode

适用于多 Task、多 Agent、跨会话、跨环境 Validation 或具有 Candidate/Closure 的 substantial version：

```text
main
  └── version/vX.Y.Z
        ├── task/vX.Y.Z-t01-<scope>
        ├── task/vX.Y.Z-t02-<scope>
        ├── fix/vX.Y.Z-<issue>-<scope>
        └── ...
              ↓
        version/vX.Y.Z
              ↓
             main
```

PRD/L1/L2/Task DAG/L3 等规划证据通常直接以 checkpoint commit 落到版本分支，不需要每份文档单独创建 branch。

Task/Fix PR merge 到 version branch 前默认要求：

```text
required task/local Validation PASS
+ Independent Review PASS on current HEAD SHA
+ configured required Minimal CI PASS（若启用）
+ required Issue Dependencies satisfied for merge
+ correct target / stack topology
```

### Trunk / Fast Path

小型低风险维护可以继续：

```text
main
  └── task/<scope> or fix/<scope>
          ↓
         main
```

详细规则见 [`standards/VERSION_INTEGRATION_WORKFLOW.md`](standards/VERSION_INTEGRATION_WORKFLOW.md)。

## Local Agent Handoff

Validation / Build Host / platform work优先使用 GitHub Issue 交接，而不是把一次性过程 Markdown 塞进业务仓库。

推荐 Issue properties：

```text
Milestone: vX.Y.Z
Labels:
  type:validation
  state:validation-needed
  handoff:local-agent
  executor:codex | executor:claude-code
  gate:integration | gate:platform | gate:hidden | ...
  env:ubuntu-build-host | env:windows | env:macos | env:gpu
  release-blocker / blocked:environment (when applicable)
```

Validation-only Issue 不自动创建 branch。只有需要源码修改时才创建 task/fix branch，并针对新 exact SHA 重跑 affected required gates；如果该变更影响已 Review 的 PR HEAD，还必须重新 Review。

通用交接协议：[`standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`](standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md)  
Issue 模板：[`templates/local-agent-handoff-issue.md`](templates/local-agent-handoff-issue.md)  
Bootstrap Prompt：[`prompts/local-agent-bootstrap.md`](prompts/local-agent-bootstrap.md)

## Minimal CI

默认 CI 目标是“最小独立复核”，而不是“把所有验证搬到云端”。

默认 Minimal CI SHOULD 包括：

- standard/project verifier；
- format/lint/typecheck 中与项目相关且确定性的部分；
- 快速 unit/contract smoke；
- basic build smoke。

默认不在 Minimal CI 中执行：

- 多平台完整矩阵；
- 真实设备/SDK validation；
- Critical Journeys；
- Hidden Validation；
- 高成本 Docker/E2E；
- release packaging。

项目可通过 `.dev-standard/PROJECT_OVERRIDES.md` 声明 `minimal / custom / disabled` CI profile。若 CI 被显式禁用或不可用，项目必须保留 exact-SHA clean validation、Independent Review 与真实 Release Gate。

## CI Evidence Contract

当自动化 Evidence 发布到外部 backend 时，推荐布局：

```text
<project>/<workflow>/
├── latest.json
└── runs/<run-key>/
    ├── manifest.json
    ├── validation-summary.json
    ├── environment.json
    ├── diagnostic.json        # FAIL 时推荐
    ├── SHA256SUMS
    ├── completion.json
    ├── logs/
    ├── reports/
    └── artifacts/
```

职责分离：

- `manifest.json`：immutable Evidence Identity Root；
- `validation-summary.json`：一个 Validation Tuple/profile 的机器可读结果；
- `completion.json`：Evidence publication commit marker，不代表 Validation PASS；
- `latest.json`：workflow-level mutable discovery/cache pointer，不代表 Release readiness；
- artifact 必须记录 producer check/state/provenance，失败或未执行 producer 不能产生有效 artifact。

正常读取先看 `latest.json`/summary，小日志与大型 artifact 只按需读取。完整规则见 [`standards/CI_EVIDENCE_STANDARD.md`](standards/CI_EVIDENCE_STANDARD.md)。真实 Formula Woodpecker → Google Drive pilot 的问题发现与修复记录见 [`references/CI_EVIDENCE_REFERENCE_VALIDATION.md`](references/CI_EVIDENCE_REFERENCE_VALIDATION.md)。

## Validation Tuple

```text
<exact SHA>
× <real platform>
× <runtime/toolchain>
× <validation profile>
```

一个 tuple 的 PASS 不能推导另一个 tuple PASS。平台或矩阵级 PASS 必须由其 required tuples 聚合得出。

## 规范入口

### Lifecycle / Git / Release

- Agent 总入口：[`AGENTS.md`](AGENTS.md)
- 完整开发流程：[`standards/DEVELOPMENT_WORKFLOW.md`](standards/DEVELOPMENT_WORKFLOW.md)
- 版本集成：[`standards/VERSION_INTEGRATION_WORKFLOW.md`](standards/VERSION_INTEGRATION_WORKFLOW.md)
- GitHub 工作流：[`standards/GITHUB_WORKFLOW.md`](standards/GITHUB_WORKFLOW.md)
- GitHub Agent 协作：[`standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`](standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md)
- Validation：[`standards/VALIDATION_STANDARD.md`](standards/VALIDATION_STANDARD.md)
- CI Evidence：[`standards/CI_EVIDENCE_STANDARD.md`](standards/CI_EVIDENCE_STANDARD.md)
- Release：[`standards/RELEASE_STANDARD.md`](standards/RELEASE_STANDARD.md)
- 项目接入：[`standards/PROJECT_ADOPTION.md`](standards/PROJECT_ADOPTION.md)

### Project Engineering Baseline

- Repository 基线：[`standards/REPOSITORY_STANDARD.md`](standards/REPOSITORY_STANDARD.md)
- 项目/Monorepo 结构：[`standards/PROJECT_STRUCTURE.md`](standards/PROJECT_STRUCTURE.md)
- 文档规范：[`standards/DOCUMENTATION_STANDARD.md`](standards/DOCUMENTATION_STANDARD.md)
- 测试规范：[`standards/TESTING_STANDARD.md`](standards/TESTING_STANDARD.md)

### Agent Roles / Handoff

- ChatGPT Web / Builder / Reviewer：[`standards/CHATGPT_WEB_ROLE.md`](standards/CHATGPT_WEB_ROLE.md)
- Codex / Build Host Execution：[`standards/CODEX_ROLE.md`](standards/CODEX_ROLE.md)
- Generic Local Agent Handoff：[`standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`](standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md)
- Codex compatibility entry：[`standards/CODEX_HANDOFF_PROTOCOL.md`](standards/CODEX_HANDOFF_PROTOCOL.md)
- 模型策略：[`standards/MODEL_USAGE_POLICY.md`](standards/MODEL_USAGE_POLICY.md)

## Templates / References / Checklists

- `templates/`：Task Issue、Task DAG、Agent Event、PR、Validation、Closeout、Local Agent Handoff 和项目接入模板。
- `reference-architectures/`：非强制结构参考。
- `checklists/`：Project Init、PR Review、Version Closure 等机械检查项。
- `references/`：公开工程 evidence/provenance 与真实 reference validation 记录。
- `prompts/`：L1/L2/L3、Independent Review 与 Agent 执行基线。
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
