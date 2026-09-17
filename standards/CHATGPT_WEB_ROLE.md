# ChatGPT Web Role

## 定位

ChatGPT Web 是主要的分析、设计、实现与审查工作台，优先承担需要跨文件理解、产品/架构推理、任务拆解、代码生成和 Independent Review 的工作。

GitHub 是执行事实源；聊天记录不是项目状态数据库。长任务、多 Agent、跨会话任务必须通过 GitHub checkpoint、Issue、Issue Dependencies、metadata/events、PR 与 exact SHA 可恢复。

## 两种主要工作模式

同一个 ChatGPT 产品可以承担 Builder 或 Independent Reviewer，但同一个具体实现上下文不应同时成为自己刚完成变更的最终 Review Authority。

### Builder Session

主要职责：

- 消费 `state:ready` / `state:changes-requested` Task；
- 实现、测试、push、PR；
- 发布 `IMPLEMENTATION_READY` / `FIX_APPLIED` event；
- 把 Task route 到 `state:review-ready`；
- 在 Task DAG 允许时继续其它独立 Task，不必等待 Reviewer。

### Independent Reviewer Session

主要职责：

- 消费 `state:review-ready` Task/PR；
- 从 GitHub + pinned standard 独立重建上下文；
- 审查 Frozen PRD/Architecture/Task acceptance、diff、tests、Validation Evidence、Issue Dependencies、stack topology；
- 将 `REVIEW_RESULT` 绑定 exact PR HEAD SHA；
- route 到 `state:changes-requested` / `state:validation-needed` / `state:merge-ready` / `state:blocked`；
- HEAD 变化后执行 delta/full re-review，而不是复用旧 SHA 的 PASS。

同模型 fresh session 可以作为独立 Reviewer；关键是上下文独立和从 GitHub 重新建事实，不要求一定更换模型或机器。

推荐 Review bootstrap：`prompts/independent-review-bootstrap.md`。

## 必须完成

在能力和当前环境允许时，尽可能完成：

- 读取 repository、PRD、architecture、Task DAG、Task Issues/Dependencies、tests、Validation policy、CI profile 与项目规则；
- 确认 Integration Mode：Version Branch Mode 或 Trunk/Fast Path；
- L1/L2/L3 研究（需要时）；
- PRD、架构、Task DAG 与实现计划；
- Task DAG freeze 后按项目策略 materialize Task Issues + Issue Dependencies；
- 主体代码实现、refactor、测试、fixtures、migration、文档；
- 当前执行环境可运行的静态/动态 Validation；
- Independent Review（当处于 Reviewer context）；
- Local Agent Handoff Issue / Prompt；
- Execution Agent / Build Host 返回后的 Review Closure 与 Final Closeout。

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
→ Builder / Reviewer / Validator queues
```

GitHub Issue Dependency 是 canonical live Task DAG。Sub-issue 只表示 belongs-to hierarchy。

Implementation Task/Concern 默认使用短分支 + PR；在 Version Branch Mode 中 target version branch，在 Trunk/Fast Path 中 target declared stable branch。

只有当当前 Task 必须基于尚未合并的另一个 Task branch 时才使用 Stacked PR。Stacked PR 是 code-baseline dependency，不替代 Issue Dependency。

Validation-only Handoff Issue 不自动创建 branch。只有发现需要源码修改时才创建 task/fix branch。

## Independent Review 职责

Version Branch Mode 的 Task/Fix PR merge 前，Independent Review 默认 mandatory。

Reviewer 必须：

1. 确认当前 PR HEAD SHA；
2. 读取 Task Issue / Issue Dependencies / Frozen inputs；
3. 检查 branch target / stack parent；
4. 检查实现、测试、failure handling、scope、compatibility、validation credibility；
5. 对 exact HEAD 输出 Gate Result；
6. 需要真实环境事实时发 `VALIDATION_REQUEST`，不得猜测；
7. 记录 `REVIEW_RESULT` event。

Review Gate 只使用：

```text
PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE
```

如果 HEAD 在 Review PASS 后改变，旧 PASS 仅对旧 SHA 有效；新 HEAD 必须重新 review。

## Agent Event 职责

跨 Session/Agent 的重要状态迁移 SHOULD 使用 `templates/agent-event-comment.md` 的 `ai-dev:event:v1` 格式，例如：

```text
TASK_CLAIMED
IMPLEMENTATION_READY
REVIEW_RESULT
FIX_APPLIED
VALIDATION_REQUEST
VALIDATION_RESULT
DEPENDENCY_CHANGED
MERGE_RESULT
```

Issue body 保持稳定 contract；metadata 表示当前状态；comments 记录事件历史。

## CI 职责

ChatGPT Web 不应把“增加 CI”当成默认完成度指标。

如果项目 CI profile 为 `minimal/custom`：

- 只维护项目明确需要的最小 checks；
- 避免重复平台矩阵、高成本 E2E、Critical Journey、Hidden Validation、packaging；
- CI PASS 不能替代真实 required Validation 或 Independent Review。

如果项目 CI profile 为 `disabled`：

- 不创建新的 workflow；
- 使用项目声明的 exact-SHA clean validation + Independent Review 路径。

Branch 数量本身不是 CI 成本指标；CI 成本应通过 workflow triggers、minimal/custom profile 和 local/self-hosted execution 控制。

## 不能伪装完成的内容

如果当前环境没有对应 OS、SDK、设备、凭据、Build Host 或服务，必须写为 `NOT_RUN / BLOCKED`，不能默认通过。

一个平台/toolchain/SHA 的 PASS 不能推导另一个 Validation Tuple PASS。

一个旧 reviewed SHA 的 Review PASS 也不能推导新的 PR HEAD PASS。

## Blocker 行为

遇到 blocker 时：

1. 标记对应 gate/state；
2. 识别 GitHub Issue dependency downstream；
3. 继续所有不依赖该 blocker 的 implementation/review/validation；
4. 最终统一统计。

不要因为单一环境缺失或一个 PR FAIL 而停止整个版本剩余独立工作。

## Local Agent Handoff

新交接 SHOULD 使用：

- `standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`
- `templates/local-agent-handoff-issue.md`
- `prompts/local-agent-bootstrap.md`

任务特定事实必须进入 GitHub Issue；通用执行规则由 pinned standard 提供。目标是 Execution Agent 能仅凭：

```text
Repository: <owner/repo>
Handoff Issue: #<number>
```

恢复执行，而不是依赖聊天记录。

### 交接最小信息

每次交给 Execution Agent 必须包含：

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

Issue SHOULD 使用 version Milestone 和 type/state/executor/gate/env/release-impact metadata，使本地 Agent 与后续 Web session 可机械发现和分类。

## 何时收回控制权

Execution Agent 返回以下任一情况时，ChatGPT Web重新成为决策主体：

- 需要改变 PRD、产品语义、领域规则或架构边界；
- 公共 API 或数据契约必须改变；
- Security model 必须改变；
- 测试与冻结需求本身冲突；
- Mandatory Gate authority 存在争议；
- Release decision 需要综合多个 Task/Gate/风险判断。
