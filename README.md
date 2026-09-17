# AI Development Standard

跨项目 AI 软件工程执行规范与工程基线。

当前版本：`v3.1.0`

v3.1 在 v3.0 的 GitHub-native Task DAG、risk-based Independent Review 与多 Agent Issue Interaction 基线上增加 **Actor Role / Logical Operator Attribution**：即使 ChatGPT Web、Local Agent、CI 和人工都通过同一个 GitHub 账号写入，也能审计“哪个角色、哪个具体 Web 页面/Agent/run 做了什么”。

## 核心原则

1. **GitHub 是工程事实源**：repository state、commit SHA、Issue、Issue Dependency、PR、Review、Validation Evidence 与 Release identity 是可审计事实；聊天记录不是事实源。
2. **Planning DAG 与 Execution DAG 分层**：Frozen Task DAG 文档记录规划依据；GitHub Task Issues + Issue Dependencies 是 canonical live execution DAG。
3. **Hierarchy ≠ Dependency**：Milestone 聚合版本，Sub-issue 表达 belongs-to，Issue Dependency 表达 blocked-by；三者不能混用。
4. **Stacked PR ≠ Task DAG**：Stacked PR 只在 Task 必须基于另一个尚未合并的代码分支时使用；它表达 code-baseline dependency，不替代 Issue Dependency。
5. **Role ≠ Operator ≠ GitHub Account**：Role 表示流程职责；Logical Operator 表示具体 Web session/Local Agent/automation/human；GitHub account 只是 transport identity。
6. **Independent Review 按需**：每个 Task/PR 明确 `required / recommended / not-required` Review Policy；Version Branch Mode 本身不再自动创建 mandatory Review Gate。
7. **Review exact-SHA**：Review 被执行时，PASS 只对 reviewed SHA 有效；若 Review 仍是 merge-required evidence 且 HEAD 改变，必须 delta/full re-review。
8. **多会话通过 GitHub 协作**：Issue body 是合同、metadata 是当前状态、comments 是事件历史、PR 是代码变化、SHA 是身份、operator attribution 说明具体执行主体。
9. **Validation 是 mandatory，CI 是 execution mechanism**：任何 required Validation gate 都必须真实执行或如实标记状态；CI 不等同于完整 Validation 或 Release Authority。
10. **CI 默认最小化**：用于低成本、确定性、clean-checkout 独立复核，不默认承载完整平台矩阵、Critical Journeys、Hidden Validation、昂贵 E2E 或 packaging。
11. **Exact-SHA Evidence**：验证和被采用的 Review 结论必须绑定明确 commit SHA；平台验证还必须绑定真实 platform/runtime/toolchain profile。
12. **禁止为变绿而降低标准**：不得删除有效断言、跳过 required gate、擅自改变冻结需求、架构或 release blocker。
13. **规范固定到 immutable revision**：业务项目记录 semantic version + 40-char commit SHA，不隐式跟随 `main/latest`。
14. **Required Gate 有明确权威来源**：Frozen PRD / Contract → Frozen Architecture → PROJECT_OVERRIDES → Task acceptance → Standard defaults。
15. **Blocker 按依赖传播**：一个 Gate/Task 的 blocker 只沿实际 dependency edge 传播；所有独立可执行工作继续推进。
16. **One concern, one PR**：实现 Task/Fix 使用短分支；局部 PASS/Review PASS 不等于 Release PASS。
17. **Stage Artifact 是 checkpoint，不是默认 branch**：PRD Freeze、L1/L2、Task DAG、L3、Candidate、Validation、Closeout 在成为下游依赖时形成远端 checkpoint，但不要求逐阶段机械建分支。
18. **Substantial version 优先 Version Branch Mode**：`task/fix → version/vX.Y.Z → main`；小型、低风险、范围明确的维护可以走 trunk/fast path。
19. **Local Agent Handoff 以 Issue 为合同**：任务特定事实放 Issue，通用执行纪律放 pinned standard/bootstrap prompt；本地 Agent 应能仅凭 repository + issue 恢复执行。
20. **Release Qualification 由完整 required evidence 决定**：Critical Journeys、Hidden Validation、真实 platform/build 与其它 frozen required gates必须在 candidate identity 上形成真实证据。
21. **外部 CI Evidence 必须事务化发布**：immutable evidence 与 mutable discovery pointer 分离；只有完整发布并形成 `completion.json` 的 run 才能更新 `latest.json`，且旧 run 不得覆盖新 pointer。

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
Task Issues + Issue Dependencies + Review Policy
        ↓
ROLE_CLAIMED + Operator Attribution
        ↓
Builder Implementation
        ↓
Required Task Validation
        ↓
PR
   ┌────┴──────────────────────┐
   │                           │
Review selected/required     Review skipped/not-required
   │                           │
Independent Review             │
   │                           │
   └──────────────┬────────────┘
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

流程不是机械阶段瀑布。Bug、小修复、已冻结范围内明确 Task 可以从最接近阶段开始；但事实链、required Validation 和 Release 判断不能伪造。

## Task DAG / GitHub Execution DAG

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
Task Branch / PR  = 实现与 merge/review 边界
Stacked PR        = 可选的未合并代码基线依赖
```

Task DAG 不需要为了表达依赖而建 branch；执行依赖直接 materialize 为 Issue Dependency。

## Actor Role / Logical Operator Attribution

GitHub 显示的 comment/PR author 只是 transport identity。多个 Agent 使用同一个账号时，新事件使用 `ai-dev:event:v2` 明确记录：

```yaml
actor_role: builder
operator_kind: chatgpt-web
operator_id: "chatgpt-web:web-a"
session_ref: "domainharness-builder-a"
transport_actor: "github:kaicreator-mm"
```

字段含义：

```text
actor_role      = 本次动作的流程职责
operator_kind   = chatgpt-web / codex / claude-code / human / github-actions / woodpecker / other
operator_id     = 逻辑执行者，例如具体 Web A / Web B / Build Host Agent
session_ref     = 具体页面、conversation、process、CI run 的非敏感关联别名
transport_actor = 真正向 GitHub 写入的账号/API identity
```

推荐例子：

```text
chatgpt-web:web-a
chatgpt-web:web-b
codex:ubuntu-build-01
claude-code:windows-01
woodpecker:runner-01
github-actions:verify-standard
human:owner
```

不要把动态 `operator_id/session_ref` 做成 GitHub Labels；否则每个会话都会制造 label churn。用结构化 comments/events 保存即可。

需要并发可见性时，开始工作先发布：

```text
ROLE_CLAIMED
```

主动交接/放弃角色时可发布：

```text
ROLE_RELEASED
```

Role claim 是 attribution/routing fact，不是 distributed lock。

历史 `ai-dev:event:v1` 保持有效，不重写历史；v3.1+ 新事件优先 `ai-dev:event:v2`。

## Risk-Based Independent Review

每个 implementation Task/PR SHOULD 明确：

```text
required
recommended
not-required
```

推荐 portable metadata：

```text
review:required
review:recommended
review:not-required
```

### required

Review 是 merge gate。典型场景：security/auth/authorization/permissions/secrets、public API/external contract、schema/migration、cross-service contract、concurrency/transaction/data integrity、destructive/recovery behavior、high-blast-radius integration、release blocker/high-risk concern、CODEOWNERS/project policy 指定区域。

当前 merge-candidate exact SHA 必须 Review `PASS`。

required Review 的 Reviewer 可以和 Builder 使用同一个 GitHub 账号，但必须是可审计的独立 context，例如：

```text
Builder  → operator_id=chatgpt-web:web-a
Reviewer → operator_id=chatgpt-web:web-b
```

### recommended

独立审查有价值但不是 merge gate：

```text
PERFORM → exact-SHA Review
或
SKIP → 记录 rationale，Review Gate 保持 NOT_RUN
```

SKIP 不等于 PASS，也不会自动阻塞 merge。

### not-required

用于项目 policy 允许的真正低风险/机械 concern，例如 docs-only、确定性生成更新等。Review Gate 为 `NOT_APPLICABLE`。

Review Policy 权威顺序：

```text
Frozen PRD / Contract
→ Frozen Architecture
→ PROJECT_OVERRIDES
→ Task acceptance / risk classification
→ Standard defaults
```

## Builder / Reviewer / Validator Interaction

推荐 workflow states：

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

这些是 routing state，不是 Gate 状态。Gate 仍只使用：

```text
PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE
```

典型流水线：

```text
Builder A                                  Reviewer B
operator=chatgpt-web:web-a                 operator=chatgpt-web:web-b
T01 implementation
  ↓
PR #101 + review-ready ──────────────────→ exact-SHA review
T02 implementation                          ↓
  ↓                                  PASS / findings / validation request
PR #102 + review:recommended
  ↓ SKIP
merge-ready
```

Reviewer B 只消费实际进入 `state:review-ready` 的 Task。Builder 不必把每个 Task 都送去 B，也不必等待 Reviewer 才开始其它独立 Task。

跨 Agent 关键事件 SHOULD 使用：

```html
<!-- ai-dev:event:v2 -->
```

常用事件：

```text
ROLE_CLAIMED
ROLE_RELEASED
TASK_CLAIMED
IMPLEMENTATION_READY
REVIEW_DECISION
REVIEW_RESULT
FIX_APPLIED
VALIDATION_REQUEST
VALIDATION_RESULT
DEPENDENCY_CHANGED
MERGE_RESULT
```

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

PRD/L1/L2/Task DAG/L3 等规划证据通常以 checkpoint commit 落到版本分支，不需要每份文档单独 branch。

Task/Fix PR merge readiness：

```text
required task/local Validation PASS
+ Review condition satisfied
+ configured required Minimal CI PASS（若启用）
+ required Issue Dependencies satisfied
+ correct target / stack topology
+ no unresolved release-significant blocker/finding
```

Review condition：

```text
required     → Review PASS on current SHA
recommended  → Review PASS OR explicit SKIP rationale
not-required → NOT_APPLICABLE
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

Validation / Build Host / platform work优先使用 GitHub Issue 交接。

Validation-only Issue 不自动创建 branch。只有需要源码修改时才创建 task/fix branch，并针对新 exact SHA 重跑 affected required gates。如果 Review 仍是 required merge evidence，也要针对新 SHA 重新 Review。

Local Agent 必须使用自己的 `operator_id/session_ref` 发布 v2 events，不能因为 GitHub author 和 Web 相同而把本地执行错误归属给 Web。

通用交接协议：[`standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`](standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md)  
Issue 模板：[`templates/local-agent-handoff-issue.md`](templates/local-agent-handoff-issue.md)  
Bootstrap Prompt：[`prompts/local-agent-bootstrap.md`](prompts/local-agent-bootstrap.md)

## Minimal CI

默认 CI 目标是“最小独立复核”，而不是把所有验证搬到云端。

默认 Minimal CI SHOULD 包括：standard/project verifier、相关且确定性的 format/lint/typecheck、快速 unit/contract smoke、basic build smoke。

默认不在 Minimal CI 中执行完整多平台矩阵、真实设备/SDK、Critical Journeys、Hidden Validation、高成本 Docker/E2E、release packaging。

项目可通过 `.dev-standard/PROJECT_OVERRIDES.md` 声明 `minimal / custom / disabled` CI profile。

**CI disabled 不自动要求 Independent Review。** Review 仍按 Review Policy 决定；Validation 仍按 required gate authority 执行。

## CI Evidence Contract

当自动化 Evidence 发布到 Google Drive、S3、MinIO 或其它 backend 时：

```text
<project>/<workflow>/
├── latest.json
└── runs/<run-key>/
    ├── manifest.json
    ├── validation-summary.json
    ├── environment.json
    ├── diagnostic.json
    ├── SHA256SUMS
    ├── completion.json
    ├── logs/
    ├── reports/
    └── artifacts/
```

- `manifest.json`：immutable Evidence Identity Root；
- `validation-summary.json`：Validation Tuple/profile 的机器可读结果；
- `completion.json`：Evidence publication commit marker，不代表 Validation PASS；
- `latest.json`：mutable discovery/cache pointer，不代表 Release readiness；
- artifact 必须记录 producer check/state/provenance。

完整规则见 [`standards/CI_EVIDENCE_STANDARD.md`](standards/CI_EVIDENCE_STANDARD.md)。

## Validation Tuple

```text
<exact SHA>
× <real platform>
× <runtime/toolchain>
× <validation profile>
```

一个 tuple 的 PASS 不能推导另一个 tuple PASS。

## 规范入口

### Lifecycle / Git / Release

- [`AGENTS.md`](AGENTS.md)
- [`standards/DEVELOPMENT_WORKFLOW.md`](standards/DEVELOPMENT_WORKFLOW.md)
- [`standards/VERSION_INTEGRATION_WORKFLOW.md`](standards/VERSION_INTEGRATION_WORKFLOW.md)
- [`standards/GITHUB_WORKFLOW.md`](standards/GITHUB_WORKFLOW.md)
- [`standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`](standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md)
- [`standards/VALIDATION_STANDARD.md`](standards/VALIDATION_STANDARD.md)
- [`standards/CI_EVIDENCE_STANDARD.md`](standards/CI_EVIDENCE_STANDARD.md)
- [`standards/RELEASE_STANDARD.md`](standards/RELEASE_STANDARD.md)
- [`standards/PROJECT_ADOPTION.md`](standards/PROJECT_ADOPTION.md)

### Project Engineering Baseline

- [`standards/REPOSITORY_STANDARD.md`](standards/REPOSITORY_STANDARD.md)
- [`standards/PROJECT_STRUCTURE.md`](standards/PROJECT_STRUCTURE.md)
- [`standards/DOCUMENTATION_STANDARD.md`](standards/DOCUMENTATION_STANDARD.md)
- [`standards/TESTING_STANDARD.md`](standards/TESTING_STANDARD.md)

### Agent Roles / Handoff

- [`standards/CHATGPT_WEB_ROLE.md`](standards/CHATGPT_WEB_ROLE.md)
- [`standards/CODEX_ROLE.md`](standards/CODEX_ROLE.md)
- [`standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`](standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md)
- [`standards/CODEX_HANDOFF_PROTOCOL.md`](standards/CODEX_HANDOFF_PROTOCOL.md)
- [`standards/MODEL_USAGE_POLICY.md`](standards/MODEL_USAGE_POLICY.md)

## Templates / References / Checklists

- `templates/`：Task Issue、Task DAG、Agent Event、PR、Validation、Closeout、Local Agent Handoff、项目接入模板。
- `checklists/`：Project Init、PR Review、Version Closure。
- `references/`：工程 evidence/provenance 与 reference validation。
- `prompts/`：L1/L2/L3、Independent Review、Local Agent 执行基线。
- `scripts/`：标准仓库自身或项目接入自动化。

## 版本策略

本仓库使用 SemVer：

- PATCH：措辞、模板、非语义性修正。
- MINOR：新增兼容的流程、Gate、模板或自动化能力。
- MAJOR：角色职责、Source of Truth、执行模型、mandatory Gate 或 release semantics 发生不兼容变化。

v3.1.0 是 MINOR：它为 GitHub Agent Interaction 增加兼容的 Actor Role / Logical Operator attribution 和 event v2；v3.0 的 Review/Validation/Release semantics 不变。

业务项目通过 `.dev-standard/VERSION` 固定：

```text
repository=kaicreator-mm/ai-development-standard
version=<semantic-version>
revision=<40-char-commit-sha>
```

`revision` 是不可变事实；tag/release 名称是可选的人类友好别名。
