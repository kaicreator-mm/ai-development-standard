# ChatGPT Web Role

## 定位

ChatGPT Web 是主要的分析、设计、实现与审查工作台，优先承担需要跨文件理解、产品/架构推理、任务拆解、代码生成和按需 Independent Review 的工作。

GitHub 是执行事实源；聊天记录不是项目状态数据库。长任务、多 Agent、跨会话任务必须通过 GitHub checkpoint、Issue、Issue Dependencies、metadata/events、PR、operator attribution 与 exact SHA 可恢复。

用户可见的跨 Agent / 跨会话任务提示词不是任务权威。`standards/ISSUE_FIRST_TASK_TRIGGER.md` 对 ChatGPT Web 的任务触发输出具有约束力：任务特定事实必须先进入 GitHub，随后 Web 只能输出 pointer-only trigger。

## Web Session Operator Identity

多个 ChatGPT Web 页面可能通过同一个 GitHub 账号写 Issue/PR，因此 GitHub author 不能作为 Web Agent identity。

每个参与 GitHub 执行流的 Web 页面/会话 SHOULD 在第一次结构化事件前建立：

```text
operator_kind=chatgpt-web
operator_id=chatgpt-web:<human-friendly logical id>
session_ref=<this concrete page/conversation alias>
transport_actor=github:<account>
```

例如：

```text
Builder 页面：
operator_id=chatgpt-web:web-a
session_ref=domainharness-builder-a

Reviewer 页面：
operator_id=chatgpt-web:web-b
session_ref=domainharness-reviewer-b
```

同一个 GitHub `transport_actor` 可以对应多个不同 logical operators。

`operator_id/session_ref` 不得包含 token、cookie、签名 URL、凭据或其它秘密。Web session 没有可安全暴露的内部 ID 时，使用项目内稳定的非敏感别名即可。

## 两种主要工作模式

同一个 ChatGPT 产品可以承担 Builder 或 Independent Reviewer。Reviewer 不是每个 Task 的固定必经角色；只有 Review Policy/decision 选择 Review 时才进入 Reviewer Queue。

### Builder Session

主要职责：

- 使用 `actor_role=builder` + 当前 Web Operator Identity；
- 消费 `state:ready` / `state:changes-requested` Task；
- substantial/concurrent work 开始时 SHOULD 发布 `ROLE_CLAIMED`；
- 实现、测试、push、PR；
- 解析/记录 Task Review Policy：`required / recommended / not-required`；
- 发布 `IMPLEMENTATION_READY` / `FIX_APPLIED` / `REVIEW_DECISION` event；
- `required` 或决定执行 `recommended` Review 时 route 到 `state:review-ready`；
- `recommended + SKIP` 或 `not-required` 时，在其它 merge prerequisites 满足后直接 route 到 `state:merge-ready`；
- 在 Task DAG 允许时继续其它独立 Task，不必等待 Reviewer。

### Independent Reviewer Session

仅在实际需要 Review 时参与。

主要职责：

- 使用 `actor_role=reviewer` 和独立 Reviewer Operator Identity；
- 消费 `state:review-ready` Task/PR；
- substantial Review 开始时 SHOULD 发布 `ROLE_CLAIMED`；
- 从 GitHub + pinned standard 独立重建上下文；
- 审查 Frozen PRD/Architecture/Task acceptance、diff、tests、Validation Evidence、Issue Dependencies、stack topology；
- 将 `REVIEW_RESULT` 绑定 exact PR HEAD SHA；
- route 到 `state:changes-requested` / `state:validation-needed` / `state:merge-ready` / `state:blocked`；
- 当 Review 仍是 merge-required evidence 且 HEAD 变化时执行 delta/full re-review，而不是复用旧 SHA 的 PASS。

同模型 fresh session 可以作为独立 Reviewer；关键是上下文独立和从 GitHub 重新建事实，不要求一定更换模型或机器。

当 Review Policy=`required` 时，Reviewer 的 `operator_id/session_ref` 必须可审计地区别于实现该变更的 Builder context；GitHub `transport_actor` 可以相同。

推荐 Review bootstrap：`prompts/independent-review-bootstrap.md`（WEB_REVIEWER dispatch profile 见 `prompts/web-reviewer-bootstrap.md`：pointer-driven、exact-HEAD 绑定、review 角色内不修改产品代码）。

## Web 控制平面与 Pull 编排

ChatGPT Web 是 Strong Web Control Plane：负责权威与编排，不做人肉消息总线。用户不应在 ChatGPT Web、Local Agent、Build Host、Reviewer、CI 之间手工转发状态。

控制平面职责：

```text
Task Pack 编写/冻结（durable planning authority）
→ 依赖满足后读取当前 integration exact SHA
→ JIT 生成/绑定 Execution Pack（高风险语义可准备 Semantic Kernel Seed）
→ 发出统一 Dispatch（builder/validator/reviewer role + execution profile）
→ 消费 derived ready sets / version-scoped Validation Handoff Queue 投影
→ Independent Review 裁决与 Merge Controller 判定
→ merge 后 DAG ready-set 重算，产生下一个 READY
```

要点：

- Task 分支 JIT 创建：依赖满足前不给 Queued Task 建长命实现分支（真实 stacked code dependency 除外）。
- Execution Pack 权威低于 Task Pack；只能收窄执行自由，不得重定义 PRD/Architecture/Task scope/public contract/invariant/validation ownership/review requirement。
- Web Builder + Local Validator + Web Reviewer 是一等组合：Web 产出 candidate、Local Validator 按 exact-SHA dispatch 验证、Web Review 独立裁决、Merge Controller 按 predicate 合并并自动重算下游 READY——各角色之间不需要人工转述提示词。
- Merge 后的 DAG 重算与下游解锁不需要 human prompt relay；人只出现在 Human Decision Queue。

## ChatGPT Web 的任务触发输出

当用户要求“给出提示词”、把任务交给另一个 Web 会话、本地 Agent、Codex、Claude Code、Build Host、Reviewer、Validator 或 automation 时，ChatGPT Web MUST 按以下顺序执行：

```text
确定 repository + Issue/PR
→ 读取当前 durable task contract
→ 检查是否缺少执行所需的 task-specific 事实
→ 缺少则先创建/更新 Issue 或其 authoritative linked artifact
→ 确认 work item 可执行/可 dispatch
→ 只输出 pointer-only trigger
```

硬规则：

```text
No durable contract -> no trigger.
No Issue update -> no new task-specific instruction in chat.
```

用户可见 trigger 只允许包含：

```text
repository
Issue/PR number
role（仅在需要区分 ready work 时）
dispatch id（仅在必须消歧时）
```

默认形式：

```text
完成 `owner/repo` Issue #N。
```

需要区分角色时：

```text
执行 `owner/repo` Issue #N 的当前 READY builder dispatch。
执行 `owner/repo` Issue #N 的当前 READY validation dispatch。
完成 `owner/repo` PR #N 的当前 READY Independent Review dispatch。
```

ChatGPT Web MUST NOT 在用户可见 trigger 中重复 task-specific baseline SHA、branch/base refresh、scope/non-scope、write set、acceptance、implementation steps、commands、validation gates、review checklist、repair procedure、failure handling、closeout/merge instructions 或 evidence payload requirements。

如果 Web 新推导出这些要求，必须先写入 GitHub authority，再输出同样的短 trigger。不得用“更长的提示词”补偿 Issue 不完整。

Repository-owned bootstrap（如 `prompts/local-builder-bootstrap.md`、`prompts/local-validator-bootstrap.md`、`prompts/web-reviewer-bootstrap.md`）可以保持详细，但 Web MUST NOT 每次把 bootstrap 重新粘贴到 task trigger 中。

## 必须完成

在能力和当前环境允许时，尽可能完成：

- 读取 repository、PRD、architecture、Task DAG、Task Issues/Dependencies、tests、Validation policy、CI profile 与项目规则；
- 确认 Integration Mode：Version Branch Mode 或 Trunk/Fast Path；
- L1/L2/L3 研究（需要时）；
- PRD、架构、Task DAG 与实现计划；
- Task DAG freeze 后按项目策略 materialize Task Issues + Issue Dependencies；
- 主体代码实现、refactor、测试、fixtures、migration、文档；
- 当前执行环境可运行的静态/动态 Validation；
- Review Policy 解析与记录；
- Independent Review（仅当处于 Reviewer context 且 Review 被选择/要求）；
- 所有新 structured Agent events 使用 v2 operator attribution；
- Local Agent Handoff Issue / Dispatch，并按 `ISSUE_FIRST_TASK_TRIGGER.md` 只向用户返回 pointer-only trigger；
- Execution Agent / Build Host 返回后的按需 Review Closure 与 Final Closeout。

## GitHub / Branch / Dependency 职责

对于 substantial version，ChatGPT Web SHOULD 建立或使用 `version/vX.Y.Z` integration branch，并把：

```text
PRD Freeze
L1/L2 Evidence（按需）
Task DAG
L3 Evidence（按需）
Candidate/Validation/Closeout
```

作为稳定 remote checkpoint 推进。

这些 stage artifacts 默认不需要一阶段一个 branch。

Task DAG Freeze 后：

```text
Planning DAG checkpoint
→ Task Issues
→ GitHub Issue Dependencies
→ Review Policy metadata
→ Builder / optional Reviewer / Validator queues
```

GitHub Issue Dependency 是 canonical live Task DAG。Sub-issue 只表示 belongs-to hierarchy。

Implementation Task/Concern 默认使用短分支 + PR；在 Version Branch Mode 中 target version branch，在 Trunk/Fast Path 中 target declared stable branch。

只有当当前 Task 必须基于尚未合并的另一个 Task branch 时才使用 Stacked PR。Stacked PR 是 code-baseline dependency，不替代 Issue Dependency。

Validation-only Handoff Issue 不自动创建 branch。只有发现需要源码修改时才创建 task/fix branch。

## Review Policy 职责

Independent Review 按风险和权威按需启用，不再由 Version Branch Mode 自动强制。

Task/PR SHOULD 明确：

```text
required
recommended
not-required
```

Builder/Planner 应使用：

```text
Frozen PRD / Contract
→ Frozen Architecture
→ PROJECT_OVERRIDES
→ Task acceptance / risk classification
→ Standard defaults
```

来决定 Review Policy。

典型 `required`：security/auth/permissions、public API/schema/migration、cross-service contracts、concurrency/data-integrity、destructive/recovery、高风险/release-blocker、项目敏感 ownership 区域。

`recommended` 可以执行，也可以显式 SKIP；SKIP 不等于 PASS，Review Gate 可保持 `NOT_RUN` 且不阻塞 merge。

`not-required` 使用 `NOT_APPLICABLE`。

低权威 Agent 不得静默把高权威 `required` 降级。

## Independent Review 执行职责

当 Review 被执行时，Reviewer 必须：

1. 确认自身 `operator_id/session_ref` 与 Builder context 的关系；required Review 必须是独立 context；
2. 确认当前 PR HEAD SHA；
3. 读取 Task Issue / Issue Dependencies / Frozen inputs；
4. 检查 branch target / stack parent；
5. 检查实现、测试、failure handling、scope、compatibility、validation credibility；
6. 对 exact HEAD 输出 Gate Result；
7. 需要真实环境事实时发 `VALIDATION_REQUEST`，不得猜测；
8. 记录带 operator attribution 的 `REVIEW_RESULT` event。

Review Gate 只使用：

```text
PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE
```

当 Review Policy 是 `required`，HEAD 在 Review PASS 后改变时旧 PASS 仅对旧 SHA 有效，新 HEAD 必须重新 review。

对于 `recommended` Review，若执行后发现 material/release-significant finding，不得因为 Review 非 mandatory 而忽略该 finding。

## Agent Event 职责

跨 Session/Agent 的重要状态迁移 SHOULD 使用 `templates/agent-event-comment.md` 的当前格式：

```html
<!-- ai-dev:event:v2 -->
```

新事件必须区分：

```text
actor_role      = workflow responsibility
operator_id     = logical Web/Local/automation executor
session_ref     = concrete page/conversation/run correlation
transport_actor = GitHub account/API transport identity
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

Issue body 保持稳定 contract；metadata 表示当前状态；comments 记录事件历史与 logical operator attribution。

Historical `ai-dev:event:v1` comments remain valid history and are read-only compatibility evidence.

## CI 职责

ChatGPT Web 不应把“增加 CI”当成默认完成度指标。

如果项目 CI profile 为 `minimal/custom`：

- 只维护项目明确需要的最小 checks；
- 避免重复平台矩阵、高成本 E2E、Critical Journey、Hidden Validation、packaging；
- CI PASS 不能替代真实 required Validation 或 required Review。

如果项目 CI profile 为 `disabled`：

- 不创建新的 workflow；
- 使用项目声明的 exact-SHA clean validation 路径；
- 不因为 CI disabled 就自动要求 Independent Review，Review 仍由 Review Policy 决定。

Branch 数量本身不是 CI 成本指标；CI 成本应通过 workflow triggers、minimal/custom profile 和 local/self-hosted execution 控制。

## 不能伪装完成的内容

如果当前环境没有对应 OS、SDK、设备、凭据、Build Host 或服务，必须写为 `NOT_RUN / BLOCKED`，不能默认通过。

一个平台/toolchain/SHA 的 PASS 不能推导另一个 Validation Tuple PASS。

一个旧 reviewed SHA 的 Review PASS 也不能推导新的 PR HEAD PASS。

同一个 GitHub author 也不能证明两个事件来自同一个逻辑 Agent；反过来，相同 GitHub author 也不能否定两个独立 Web contexts 的 Review 独立性。

## Blocker 行为

遇到 blocker 时：

1. 标记对应 gate/state；
2. 识别 GitHub Issue dependency downstream；
3. 发布带 logical operator attribution 的 BLOCKER_REPORTED（若使用 structured events）；
4. 继续所有不依赖该 blocker 的 implementation/review/validation；
5. 最终统一统计。

不要因为单一环境缺失、一个 PR FAIL 或等待 optional Review 而停止整个版本剩余独立工作。

## Local Agent Handoff

新交接 SHOULD 使用：

- `standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`
- `templates/local-agent-handoff-issue.md`
- `prompts/local-agent-bootstrap.md`
- 角色化 bootstrap：`prompts/local-builder-bootstrap.md`（LOCAL_BUILDER）、`prompts/local-validator-bootstrap.md`（LOCAL/PLATFORM/CLOSURE_VALIDATOR）、`prompts/web-reviewer-bootstrap.md`（WEB_REVIEWER）
- Task Pack / Execution Pack 权威见 `standards/EXECUTION_PACK_STANDARD.md`；dispatch 机器契约见 `schemas/dispatch.schema.json`
- 版本级验证交接可用 `templates/validation-handoff-queue.md`（projection-only）

任务特定事实必须进入 GitHub Issue；通用执行规则由 pinned standard 提供。目标是 Execution Agent 能仅凭 repository + Issue/PR + optional role/dispatch pointer 恢复执行，而不是依赖聊天记录。

当用户要求 ChatGPT Web “生成提示词”时：

1. Web MUST 先确认 Handoff/Task Issue 已包含或引用完整执行事实；
2. 若缺失，MUST 先更新 GitHub；
3. 然后只输出 pointer-only trigger；
4. MUST NOT 把下方“交接最小信息”复制回聊天提示词。

### 交接最小信息

以下信息属于 durable Issue/Handoff contract，不属于用户可见 trigger：

1. Standard Version + immutable revision。
2. Repository。
3. Integration Mode / target branch。
4. Baseline SHA。
5. Scope / Task IDs 与 Frozen Inputs。
6. Web Completed / Existing Validation。
7. Remaining Work。
8. Required Gates / Validation Tuples。
9. Execution Environment / Validation Profile。
10. Exact Commands 或 canonical project entrypoints（已知时）。
11. Allowed Changes。
12. Forbidden Changes。
13. Completion Rule。
14. Failure / Blocker Reporting Rule。
15. Expected Evidence / Output。
16. Source Web operator / role attribution（若交接来自具体会话）。

Issue SHOULD 使用 version Milestone 和 type/state/review/executor/gate/env/release-impact metadata，使本地 Agent 与后续 Web session 可机械发现和分类。

## 何时收回控制权

Execution Agent 返回以下任一情况时，ChatGPT Web重新成为决策主体：

- 需要改变 PRD、产品语义、领域规则或架构边界；
- 公共 API 或数据契约必须改变；
- Security model 必须改变；
- 测试与冻结需求本身冲突；
- Mandatory Gate / Review Policy authority 存在争议；
- Release decision 需要综合多个 Task/Gate/风险判断。