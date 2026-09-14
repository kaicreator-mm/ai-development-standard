# Development Workflow

## 1. 目标

该流程用于让 ChatGPT Web、Codex / 其它 Execution Agent、Build Host 与 GitHub 在不同执行环境中协作，同时保证范围、代码状态、验证结果和发布结论可追踪、可复现、可审计。

v2.0 的关键变化：

- Validation 是 mandatory；CI 不再等同于完整 Validation。
- CI 默认最小化，仅作为 clean-checkout 独立复核层。
- Blocker 按依赖传播，不再因为单个 gate 被阻塞而停止所有独立工作。
- 阶段减少，状态和依赖更细。

## 2. 生命周期

### Stage 0 — Intake / Baseline

确认：目标、repository、目标版本或 Task、当前默认分支、当前 HEAD、已有 PRD/Architecture/Task/Validation/CI 状态。

输出至少包括：

```text
scope
baseline ref
acceptance criteria
known blockers
required evidence
```

如果任务已经明确且影响小，可以直接进入实现。

### Stage 1 — Product / Scope

按需执行 L1 Product Evidence，并冻结 PRD / Scope。

适用于：新产品、新重大能力、产品边界不清、需要反证或用户 workflow 验证的情况。

PRD / Scope Freeze 应明确：

- 本版本解决的问题；
- 用户行为 / 业务规则；
- 功能范围与明确不做；
- release blockers；
- required gates；
- acceptance criteria。

冻结后 Execution Agent 不得自行改变产品语义。

### Stage 2 — Architecture / Task Definition

按需执行 L2 Architecture Evidence；随后形成 Task DAG。

Task DAG 至少明确：

- dependency；
- input/output；
- acceptance；
- required validation；
- parallelism；
- risk；
- model/executor suitability。

高风险或低成本模型执行的 Task 可按需增加 L3 Implementation Evidence。证据优先级：

```text
Tests → Contract/Interface → Core Implementation → Failure Handling → Examples/Docs
```

### Stage 3 — Implementation Concerns

以 Task / Concern 为主要实现单位。

原则：

- One concern, one PR；
- 大功能优先拆成 Contract → Core → Integration → UI → Validation；
- 当前环境能完成的代码、测试、fixture、migration、文档与局部验证应尽可能完成；
- 不能执行的内容如实进入 gate 状态，不得默认通过；
- 正式 Concern 达到可审查状态后形成远端 checkpoint。

### Stage 4 — Validation / PR / Minimal CI

先执行当前环境或 Build Host 可运行的 Validation，再形成或更新 PR。

#### 4.1 Local / Build Host Validation

根据项目需要执行：

```text
format
lint
typecheck
unit
contract
integration
build smoke
platform validation
Critical Journey
```

Validation 必须绑定明确 commit SHA。真实平台/运行时矩阵使用 Validation Tuple：

```text
<exact SHA> × <real platform> × <runtime/toolchain> × <validation profile>
```

#### 4.2 PR

PR 说明：

```text
baseline
concern scope
changes
validation evidence
known blockers
required downstream gates
```

#### 4.3 Minimal CI

CI 默认只做低成本、确定性、clean-checkout 独立复核。

默认 Minimal CI SHOULD 只包含：

- standard/project verifier；
- format/lint/typecheck 的必要子集；
- 快速 unit/contract smoke；
- basic build smoke。

默认不把以下内容放入 CI：

- 完整多平台矩阵；
- 真实设备/SDK；
- Critical Journeys；
- Hidden Validation；
- 高成本 Docker/E2E；
- packaging。

项目通过 `.dev-standard/PROJECT_OVERRIDES.md` 声明 CI profile：

```text
minimal
custom
disabled
```

`disabled` 必须记录理由，并保留 exact-SHA clean validation + review；没有 CI 不等于没有 Validation。

PR 在 concern scope、required local/build-host validation、Review 与配置的 Minimal CI 满足项目 merge policy 后即可合并 main，不要求等待同版本其它 concern。

### Stage 5 — Integrated Baseline / Candidate Preparation

在 integrated `main` 或 release branch 上形成候选准备状态。

允许在全部 release gate 完成前先准备：

- candidate identity；
- platform matrix；
- Critical Journey matrix；
- Hidden Validation pack；
- closeout checklist；
- release notes draft；
- tag/baseline plan。

正确区分：

```text
Candidate Prepared = preparation complete
Candidate Freeze = required visible gates pass on one exact SHA
```

Candidate Prepared PASS 不代表 Candidate Freeze PASS。

### Stage 6 — Candidate Freeze / Hidden Validation / Closure

只有 required visible gates 在同一个 exact candidate SHA 上满足冻结条件后，才能记录 `CANDIDATE_FROZEN_SHA`。

Candidate Freeze 后执行 Hidden Validation。

版本级 Closure 检查：

- required visible Validation；
- Critical Journeys；
- Hidden Validation；
- 真实 platform / production build；
- external boundaries；
- docs / known limitations；
- project-required Minimal CI（若配置为 required）。

Release Qualification 使用：

- `PASS`：所有 frozen mandatory gates PASS；
- `FAIL`：mandatory gate 已执行并 FAIL；
- `BLOCKED`：mandatory gate 为 BLOCKED/NOT_RUN 或存在 release blocker。

PR PASS 不等于 Release PASS。

### Stage 7 — Release Baseline / Optional Tag / Release

只有达到项目 release policy 后才能宣布版本 READY/发布。

必须记录：

```text
immutable final baseline commit SHA
standard version + revision
release gate summary
known limitations
```

Tag / GitHub Release 是可选的人类友好别名和分发对象，不是 canonical identity。

## 3. Gate Authority

Mandatory Gate 必须能追溯到明确权威来源。优先级：

```text
1. Frozen PRD / Contract
2. Frozen Architecture
3. .dev-standard/PROJECT_OVERRIDES.md
4. Task-specific acceptance
5. Standard defaults
```

以下内容不能自动创建 mandatory release gate：

- 历史 workflow；
- 已弃用脚本；
- 旧版本 artifact；
- Agent 推测；
- “以前项目都这么做”。

若要新增 mandatory release gate，必须通过相应冻结权威的显式变更。

## 4. Blocker Propagation

Blocker 只沿依赖边传播。

示例：

```text
macOS validation BLOCKED
        ↓
Candidate Freeze BLOCKED
        ↓
Hidden Validation Execution NOT_RUN
        ↓
Release Qualification BLOCKED
```

但与 macOS gate 无直接依赖的工作仍继续，例如：

- release notes draft；
- Hidden Validation pack preparation；
- docs synchronization；
-其它平台 validation；
- candidate preparation。

执行 Agent 不应因为单个 blocker 停止整个版本，只在所有可独立工作耗尽或继续会破坏事实/数据时停止。

## 5. Stage Checkpoint Push

开发流程不要求“每个操作都 push”，而要求正式、稳定、可恢复、可交接的结果形成远端 checkpoint。

### 5.1 必须 checkpoint 的情况

至少包括：

- PRD / Scope Freeze；
- L2 Architecture Evidence；
- Task DAG；
- L3 Implementation Evidence；
- 可审查 Task / Concern；
- Validation / Candidate / Closeout；
- Release baseline 与正式 release artifact。

每个 checkpoint 应有 Git commit、remote push 与可解析 commit SHA。

### 5.2 不要求逐步 push

草稿、临时修复、单次测试运行、局部编辑不要求每一步 push。

Implementation 以 Task / Concern 为远端同步单位，不以单文件或每次编辑为单位。

### 5.3 长任务恢复

长任务、多 Agent、跨会话任务应在正式 Stage/Concern checkpoint push，使后续可以仅依赖 GitHub commit 恢复，而不是依赖聊天记录。

## 6. 快速路径

Bug、小修复、文档修正、已冻结范围内明确 Task 可跳过 L1/L2/L3，但不能跳过：

```text
Baseline
→ Implementation
→ Validation
→ GitHub fact chain
→ Release impact decision
```

快速路径不为被跳过阶段制造空提交。
