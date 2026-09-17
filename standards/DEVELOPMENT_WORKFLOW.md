# Development Workflow

## 1. 目标

该流程用于让 ChatGPT Web、Codex / Claude Code / 其它 Execution Agent、Build Host 与 GitHub 在不同执行环境中协作，同时保证范围、代码状态、验证结果和发布结论可追踪、可复现、可审计。

v3.0 在 v2.3 GitHub-native Agent Interaction 基线上调整 Independent Review：

- Frozen Task DAG → Task Issues + Issue Dependencies 的 execution DAG materialization 保持不变；
- Issue Dependency 继续作为 canonical live Task DAG；
- Stacked PR 继续仅用于真实未合并 code-baseline dependency；
- Builder / Reviewer / Validator queue 保持；
- Independent Review 从“Version Branch Task/Fix 默认 mandatory”改为 **risk-based / on-demand**；
- 每个 Task/PR 明确 `required / recommended / not-required` Review Policy；
- exact-SHA Review 规则只在 Review 被执行/要求时生效；
- Validation 仍然 mandatory；CI 仍然只是 execution mechanism，不是完整 Validation 或 Release Authority。

完整 GitHub 协作协议见 `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`。

## 2. Intake 时先选择 Integration Mode

### 2.1 Version Branch Mode

Substantial version SHOULD 使用：

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

适用于：Frozen PRD/Architecture、多 Task、多 Agent、跨会话、多个 validation environment、Candidate/Hidden Validation/Closure 等场景。

### 2.2 Trunk / Fast Path

小型、低风险、范围明确的 maintenance MAY 使用：

```text
main
  └── task/<scope> or fix/<scope>
          ↓
         main
```

Integration Mode SHOULD 在 Stage 0 记录；若开发过程中复杂度显著增加，可以从 fast path 升级到 Version Branch Mode，但不得为了简化流程而反向破坏既有 candidate/integration facts。

**Integration Mode 不决定 Review 是否 required。** Review 由 Review Policy 单独决定。

## 3. 生命周期

### Stage 0 — Intake / Baseline

确认：

```text
scope
repository
target version/task
integration mode
integration branch / target branch
current default branch
current HEAD
existing PRD/Architecture/Task/Validation/CI state
acceptance criteria
known blockers
required evidence
```

如果任务已经明确且影响小，可以直接进入实现。

如果选择 Version Branch Mode，应尽早建立或确认 `version/vX.Y.Z` 远端 integration branch，使后续正式 checkpoint 与 Task PR 有稳定目标。

### Stage 1 — Product / Scope

按需执行 L1 Product Evidence，并冻结 PRD / Scope。

PRD / Scope Freeze 应明确：

- 本版本解决的问题；
- 用户行为 / 业务规则；
- 功能范围与明确不做；
- release blockers；
- required gates；
- acceptance criteria。

冻结后 Execution Agent 不得自行改变产品语义。

#### Stage 1 Checkpoint

PRD Freeze 和最终被下游依赖的 L1 Evidence MUST 形成远端 checkpoint。

在 Version Branch Mode，默认直接形成 `version/vX.Y.Z` 上的稳定 commit/checkpoint。不要为了每个 Evidence 文件机械创建独立 branch。

只有当 evidence 由另一个 Agent 独立并行生产、需要隔离 review 或存在显著冲突风险时，才 SHOULD 使用临时 docs/evidence branch。

### Stage 2 — Architecture / Task Definition

按需执行 L2 Architecture Evidence；随后形成 Task DAG。

Task DAG 至少明确：

- dependency；
- input/output；
- acceptance；
- required validation；
- Review Policy；
- parallelism；
- risk；
- model/executor suitability；
- intended task branch / integration target when useful。

高风险或低成本模型执行的 Task 可按需增加 L3 Implementation Evidence。证据优先级：

```text
Tests → Contract/Interface → Core Implementation → Failure Handling → Examples/Docs
```

#### Stage 2 Checkpoint

L2、Task DAG、L3 在成为 implementation dependency 时 MUST 形成 remote checkpoint。

这些属于 stage artifact，默认 checkpoint，不等于一个独立 branch。

#### Stage 2.5 — Execution DAG Materialization

Task DAG Freeze 后，若项目采用 Issue-based execution，应把规划 DAG materialize 到 GitHub：

```text
Frozen Task DAG checkpoint
        ↓
Task Issues
        ↓
Milestone / type / Review Policy / initial state metadata
        ↓
GitHub Issue Dependencies
        ↓
Builder / optional Reviewer / Validator queues
```

规则：

- Planning DAG document = 规划/历史快照；
- GitHub Issue Dependencies = canonical live execution DAG；
- Sub-issue = belongs-to hierarchy，不自动表达 blocked-by；
- 不为 Task DAG 本身创建 branch；
- dependency 发生实质变化时 SHOULD 记录 rationale / `DEPENDENCY_CHANGED` event；
- `templates/task-issue.md` SHOULD 作为 Task Issue contract 基线。

### Stage 2.6 — Review Policy Selection

每个 implementation Task/PR SHOULD 明确：

```text
required
recommended
not-required
```

权威顺序：

```text
Frozen PRD / Contract
→ Frozen Architecture
→ PROJECT_OVERRIDES
→ Task acceptance / risk classification
→ Standard defaults
```

Standard default 是 **risk-based**，不是 always-review。

典型 `required` 场景：

- security/auth/authorization/permissions/secrets；
- public API / schema / migration semantics；
- cross-service contracts；
- concurrency/transactions/data integrity；
- destructive/recovery behavior；
- high-blast-radius integration；
- release blocker / explicit high-risk concern；
- project ownership policy 明确要求的敏感区域。

典型 `recommended`：中等风险行为/集成/重构变更，独立审查有明显价值但不应成为 merge blocker。

典型 `not-required`：docs-only、机械生成、确定性且低风险的局部变更，且项目 policy 允许。

Task/Agent 不得静默降低更高权威已经声明的 `required`。

### Stage 3 — Implementation Concerns

以 Task / Concern 为主要实现与 branch 单位。

原则：

- One concern, one PR；
- 大功能优先拆成 Contract → Core → Integration → UI → Validation；
- 当前环境能完成的代码、测试、fixture、migration、文档与局部验证应尽可能完成；
- 不能执行的内容如实进入 gate 状态，不得默认通过；
- 正式 Concern 达到可合并/可审查状态后形成远端 checkpoint；
- Task DAG 允许时多个 Task branch MAY 并行；
- Builder MAY 在上一个 PR 等待 Review/Validation 时继续其它独立 Task。

Version Branch Mode 推荐：

```text
task/vX.Y.Z-t01-<scope>
task/vX.Y.Z-t02-<scope>
fix/vX.Y.Z-<issue>-<scope>
```

Task/Fix PR 默认 target `version/vX.Y.Z`。

Task branch 应从明确 integration baseline 开始；不得不记录 baseline 就随意从最新 HEAD 开工。

#### 3.1 Optional Stacked PR

只有当 Task 的代码必须直接建立在另一个尚未合并的 Task branch 上时，才使用 stacked PR：

```text
version/vX.Y.Z
  ↑
task/T01-contract
  ↑
task/T02-core
```

Stacked PR 只表达 code-baseline dependency：

- Issue Dependency 仍是 canonical Task DAG；
- 不得为了镜像 Task DAG 而人工 stack 所有 PR；
- upstream merge 后，下游 PR 应 rebase/retarget 到正确 parent/integration branch；
- SHA 改变后，受影响的 **required** Review/Validation 必须重新执行。

### Stage 4 — Task Validation / PR / Optional Review / Minimal CI

先执行当前环境或 Build Host 可运行的 Validation，再形成或更新 PR。Review 仅在 Review Policy/decision 选择时进入 Review Queue。

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

Validation remains mandatory according to required gate authority. Review is not a substitute for Validation.

#### 4.2 PR / Routing Decision

PR 说明：

```text
Task/Issue
baseline
Issue Dependencies
branch strategy independent/stacked
integration target / stack parent
concern scope
changes
validation evidence
Review Policy / decision
known blockers
required downstream gates
```

Builder 完成 implementation + 当前可运行 Validation 后：

- `review:required` → 发布 `IMPLEMENTATION_READY`，route 到 `state:review-ready`；
- `review:recommended + PERFORM` → route 到 `state:review-ready`；
- `review:recommended + SKIP` → 记录 `REVIEW_DECISION`，在其它 merge prerequisites 满足后可进入 `state:merge-ready`；
- `review:not-required` → Review Gate `NOT_APPLICABLE`，在其它 merge prerequisites 满足后可进入 `state:merge-ready`。

#### 4.3 Independent Review（按需）

当 Review 被选择或 required 时：

- final review context SHOULD 与实现 context 独立；
- 可由另一 ChatGPT session、另一 agent、人类 reviewer，或同模型 fresh context 承担；
- Reviewer 重新读取 pinned standard、Task Issue、Issue Dependencies、Frozen inputs、PR diff、Validation Evidence；
- Review Result 绑定 exact PR HEAD SHA；
- required Review 下 HEAD 变化后旧 PASS 不迁移，执行 delta/full re-review；
- runtime/platform 事实无法静态确认时发 `VALIDATION_REQUEST`，不得猜测。

Reviewer route：

```text
FAIL → state:changes-requested
needs real execution → state:validation-needed
PASS + merge prerequisites satisfied → state:merge-ready
blocked → state:blocked
```

对于 `recommended` Review，如果选择 SKIP，Review Gate 可保持 `NOT_RUN` 且不阻塞 merge；但已经执行的 Review 若发现 release-significant/material finding，不得因为 Review 非 mandatory 而忽略。

推荐使用：

- `prompts/independent-review-bootstrap.md`
- `checklists/pr-review.md`
- `templates/agent-event-comment.md`

#### 4.4 Minimal CI

CI 默认只做低成本、确定性、clean-checkout 独立复核。

默认 Minimal CI SHOULD 只包含：

- standard/project verifier；
- format/lint/typecheck 的必要子集；
- 快速 unit/contract smoke；
- basic build smoke。

默认不把完整多平台矩阵、真实设备/SDK、Critical Journeys、Hidden Validation、高成本 Docker/E2E、packaging 放入 Minimal CI。

项目通过 `.dev-standard/PROJECT_OVERRIDES.md` 声明：

```text
minimal
custom
disabled
```

`disabled` 必须记录理由，并保留 exact-SHA clean validation。

CI disabled 不自动意味着 Review required；Review 仍按 Review Policy 决定。

#### 4.5 Task Merge Readiness

Task/Fix PR 只有满足以下适用条件才能进入 `state:merge-ready`：

```text
current PR HEAD SHA
+ required task/local Validation PASS
+ Review condition satisfied
+ configured required Minimal CI PASS when enabled
+ required Issue Dependencies satisfied for merge
+ correct integration target / stack parent
+ no unresolved release-significant finding/blocker
```

Review condition：

```text
required     → Independent Review PASS on current SHA
recommended  → PASS on current SHA OR explicit SKIP decision/rationale
not-required → Review Gate NOT_APPLICABLE
```

PR merge 后记录 integration SHA / `MERGE_RESULT`，Task completion rule 满足后进入 `state:done`。

### Stage 4.6 — Local Agent Handoff（按需）

当当前环境无法完成真实 build/platform/integration/CJ/Hidden/packaging 或 Reviewer/Task policy 明确要求真实 execution 时，使用 GitHub Issue 交给 Local Agent / Build Host。

新交接 SHOULD 使用：

- `standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`
- `templates/local-agent-handoff-issue.md`
- `prompts/local-agent-bootstrap.md`

Issue 应通过 Milestone + metadata 表达 version、type、state、executor、gate、environment 和 release impact。

Validation Issue MAY 作为 Task 的 sub-issue 表达层级；如果它真正 blocking 另一个 work item/candidate，应使用 Issue Dependency 表达 blocking 关系。

Validation-only execution不要求 branch。

如果发现必须修改源码：

```text
Validation Issue
→ create task/fix branch
→ minimal correct change
→ PR to declared integration branch
→ new exact SHA
→ rerun affected required gates
→ if Review remains required evidence, re-review affected PR HEAD
```

旧 SHA 的 PASS 不自动成为新 SHA 的 PASS。

### Stage 5 — Integrated Baseline / Candidate Preparation

在 integrated `version/vX.Y.Z`、`main` 或项目声明 release branch 上形成候选准备状态。

Version Branch Mode 的 integrated baseline SHOULD 来自 version branch；最终 Version PR 合并 main 之前，所有 version-level evidence 必须明确绑定其 candidate identity。

允许在全部 release gate 完成前先准备：candidate identity、platform matrix、Critical Journey matrix、Hidden Validation pack、closeout checklist、release notes draft、tag/baseline plan。

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
- project-required Minimal CI（若配置为 required）；
- Review evidence only when version/task authority makes it required for closure/merge。

Release Qualification 使用：

- `PASS`：所有 frozen mandatory gates PASS；
- `FAIL`：mandatory gate 已执行并 FAIL；
- `BLOCKED`：mandatory gate 为 BLOCKED/NOT_RUN 或存在 release blocker。

Task Review PASS / PR PASS 不等于 Release PASS。

### Stage 7 — Version PR / Release Baseline / Optional Tag / Release

Version Branch Mode 在 Closure 满足后形成最终 Version PR：

```text
version/vX.Y.Z → main
```

Merge 后 `main` 上的新 immutable commit SHA 成为最终 repository baseline。若 merge/squash 改变 commit identity，必须明确区分：

```text
validated candidate SHA
final main baseline SHA
```

若 release policy 要求 final-main sanity/revalidation，则必须真实执行，不得自动把 version-branch candidate evidence 重写为 main PASS。

只有达到项目 release policy 后才能宣布版本 READY/发布。

必须记录：immutable final baseline commit SHA、standard version + revision、release gate summary、known limitations。

Tag / GitHub Release 是可选的人类友好别名和分发对象，不是 canonical identity。

## 4. Gate Authority

Mandatory Gate 必须能追溯到明确权威来源。优先级：

```text
1. Frozen PRD / Contract
2. Frozen Architecture
3. .dev-standard/PROJECT_OVERRIDES.md
4. Task-specific acceptance
5. Standard defaults
```

Review Policy 使用同一 authority chain。Standard default 不再为所有 Version Branch Tasks 创建 mandatory Review Gate。

以下内容不能自动创建 mandatory release/review gate：历史 workflow、已弃用脚本、旧版本 artifact、Agent 推测、“以前项目都这么做”。

若要新增 mandatory release gate 或强制 Review，必须有相应 authority。

## 5. Blocker Propagation

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

与 macOS gate 无直接依赖的 release notes、Hidden pack preparation、其它平台 validation、candidate preparation 等仍继续。

执行 Agent 不应因为单个 blocker 停止整个版本，只在所有可独立工作耗尽或继续会破坏事实/数据时停止。

## 6. Stage Checkpoint Push

开发流程不要求“每个操作都 push”，而要求正式、稳定、可恢复、可交接的结果形成远端 checkpoint。

至少包括：PRD / Scope Freeze、L1（若成为 downstream evidence）、L2 Architecture Evidence、Task DAG、L3、可合并/可审查 Task/Concern、integrated version baseline、Validation/Candidate/Closeout、Release baseline 与正式 release artifact。

草稿、临时修复、单次测试运行、局部编辑不要求每一步 push。

Implementation 以 Task / Concern 为远端同步单位；Stage Artifact 以 checkpoint 为单位。

长任务、多 Agent、跨会话任务应使后续可以仅依赖 GitHub commit、Issue、PR、metadata/events 和 pinned standard 恢复，而不是依赖聊天记录。

## 7. 快速路径

Bug、小修复、文档修正、已冻结范围内明确 Task 可跳过 L1/L2/L3，也可不建立 version branch，但不能跳过：

```text
Baseline
→ Implementation
→ required Validation
→ applicable Review Policy decision
→ GitHub fact chain
→ Release impact decision
```

快速路径不为被跳过阶段制造空提交、空 branch、空 Review 或形式化 Issue。
