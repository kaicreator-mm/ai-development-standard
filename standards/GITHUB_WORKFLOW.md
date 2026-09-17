# GitHub Workflow

## 1. GitHub 对象职责

- **Repository files**：长期规范、代码、测试、文档。
- **Issue**：Task、bug、Validation、Handoff、blocker 等 Work Item；Issue body 是相对稳定的工作合同。
- **Issue Dependency**：canonical execution Task DAG 的 blocking / blocked-by 关系。
- **Sub-issue**：belongs-to 层级，例如 Version/Epic → Task → Validation；不自动表示执行依赖。
- **Milestone**：版本/发布范围聚合，例如 `vX.Y.Z`。
- **Label / Field**：Work Item 的 type、workflow state、executor、gate、environment、release impact 等路由/查询元数据。
- **Issue/PR Comment**：append-oriented Agent 事件、Review/Validation/修复/阻塞历史。
- **Branch**：隔离中的实现 concern 或版本集成面。
- **Stacked PR**：可选的未合并 code-baseline dependency；不是 canonical Task DAG。
- **Commit**：不可歧义的执行 baseline / change identity。
- **Push**：发布稳定 checkpoint，使其可恢复、可交接、可审计。
- **Pull Request**：准备评审/合并的一组真实变化。
- **Actions / CI**：可选的最小 clean-checkout 独立复核器，不是完整 Validation 或 Release Authority。
- **Validation Evidence**：exact-SHA 的真实执行证据。
- **Tag / Release**：可选的人类友好发布别名/分发对象；immutable commit SHA 始终是 canonical identity。

GitHub-native Agent 协作细则见 `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`。

## 2. Integration Mode

项目根据变更规模选择两种模式。

### 2.1 Version Branch Mode

Substantial version SHOULD 使用版本集成分支：

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

适用场景包括：多 Task、多 Agent、跨会话、多个真实执行环境、Candidate/Hidden Validation/Closure，或 Frozen PRD/Architecture 需要统一 integrated baseline 的版本。

Task/Fix PR 默认 target `version/vX.Y.Z`；最终 Version PR target `main`。

Task/Fix PR merge 到 version branch 前，默认必须具备当前 HEAD SHA 上的 required task Validation + Independent Review + configured required Minimal CI（若启用），并满足 merge 所需 Issue Dependencies。

### 2.2 Trunk / Fast Path

小型、低风险、范围明确的维护 MAY 使用：

```text
main
  └── task/<scope> or fix/<scope>
          ↓
         main
```

Bug、小文档修正、已冻结范围内的窄 Task 不要求为了形式创建版本分支。

详细选择规则见 `standards/VERSION_INTEGRATION_WORKFLOW.md`。

## 3. Task DAG / Dependency

### 3.1 Planning DAG

Frozen Task DAG checkpoint 记录：

```text
dependency rationale
input/output
acceptance
required validation
parallelism
risk
model/executor suitability
```

它是规划与历史证据，不是实时调度状态的唯一来源。

### 3.2 Execution DAG

进入执行后，GitHub Task Issues + Issue Dependencies 是 canonical live Task DAG。

例如：

```text
#102 blocked by #101
#103 blocked by #101
#104 blocked by #102
#104 blocked by #103
```

规则：

- Task DAG 文档与 Issue dependency 必须可追踪对应；
- dependency 发生实质变化时 SHOULD 记录 `DEPENDENCY_CHANGED` event/rationale；
- 不为 Task DAG 本身机械创建 branch；
- sub-issue 只表达层级，不替代 dependency；
- blocker propagation 沿实际 dependency edge 传播，不把单一 blocker 扩散到无关 Task。

### 3.3 Stacked PR

Stacked PR 仅在“当前 Task 的代码必须建立在尚未合并的另一个 Task branch 上”时使用。

```text
version/vX.Y.Z
  ↑
task/T01-contract
  ↑
task/T02-core
```

Stacked PR 不是 Task DAG：

- Issue Dependency 仍是 canonical execution dependency；
- 不要为了镜像 Task DAG 而制造人工 stack；
- 保持可独立 branch 的 Task 并行；
- upstream stack merge 后，下游 PR 应 rebase/retarget 到正确 parent/integration branch；
- SHA 改变后，受影响的 Review/Validation 必须重新建立。

## 4. 分支建议

推荐：

```text
version/vX.Y.Z
task/vX.Y.Z-tNN-<scope>
fix/vX.Y.Z-<issue>-<scope>
test/vX.Y.Z-<scope>
docs/vX.Y.Z-<scope>
```

快速路径也可使用：

```text
feat/<task-or-scope>
fix/<issue-or-scope>
test/<scope>
docs/<scope>
chore/<scope>
```

规则：

- 不强制复杂 GitFlow。
- Task / Concern 是默认短分支边界。
- PRD Freeze、L1、L2、Task DAG、L3、Candidate、Validation、Closeout 默认是 checkpoint，不因阶段存在而机械创建独立 branch。
- 临时 evidence/docs branch 只在独立生产、并行协作或需要隔离 review 时使用。
- 已合并的短分支 SHOULD 删除，除非有明确保留理由。

## 5. Commit

Commit 应保持 concern 相关，避免混入无关格式化或大范围重写。

Handoff、Review、Validation、Candidate 与 Release evidence 必须引用具体 commit SHA。

Commit 与 push 不等价：阶段内部可以有多个本地 commit；达到稳定 checkpoint 时再 push。

## 6. Push / Stage Checkpoint

不得把“每个操作都 push”作为流程要求。Push 的主要职责是发布正式、稳定、可恢复的 checkpoint。

典型 checkpoint：

```text
PRD / Scope Freeze
L1 Product Evidence（若使用）
L2 Architecture Evidence
Task DAG
L3 Implementation Evidence（若使用）
可审查 Task / Concern
integrated version baseline
Validation / Candidate / Closeout
Release baseline
```

长任务、多 Agent、跨会话任务应在正式 Stage/Concern checkpoint push，使后续可仅依赖 GitHub commit 恢复。

## 7. Issue Contract / Metadata / Events

Issue 是一次性的 Work Item，不是长期规范文件。

推荐用途：

- implementation task；
- bug；
- validation；
- Local Agent handoff；
- blocker；
- follow-up / deferred work。

### 7.1 Issue Body = stable contract

Task Issue SHOULD 使用 `templates/task-issue.md` 或项目等价模板，至少记录：

```text
Task ID / goal
scope / non-scope
frozen inputs
baseline / integration target
acceptance
required gates
dependency summary
code baseline strategy
allowed / forbidden changes
completion rule
```

事件历史不要靠反复重写 Issue body 保存。

### 7.2 Milestone / Type / State

版本 SHOULD 优先用 GitHub Milestone 表示，例如：

```text
v0.1.0
v2.9.4
```

推荐 portable labels：

```text
type:task
type:bug
type:validation
type:blocker

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

一个 Task SHOULD 同时最多有一个 `state:*`。

Workflow state label 是路由状态，不是 Validation Gate 状态；Gate 仍只使用：

```text
PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE
```

组织仓库 MAY 用 native Issue Type / custom field 映射 type/state/executor 等语义；portable baseline 仍是 labels + protocol semantics。

### 7.3 Routing labels

```text
handoff:local-agent
executor:codex
executor:claude-code

gate:review
gate:fast
gate:integration
gate:critical-journey
gate:hidden
gate:platform
gate:packaging

env:ubuntu-build-host
env:windows
env:macos
env:gpu

release-blocker
blocked:environment
```

### 7.4 Agent events

Builder/Reviewer/Validator/Merge Controller SHOULD 用 `templates/agent-event-comment.md` 的：

```html
<!-- ai-dev:event:v1 -->
```

+ YAML payload 记录：

```text
TASK_CLAIMED
IMPLEMENTATION_READY
REVIEW_RESULT
FIX_APPLIED
VALIDATION_REQUEST
VALIDATION_RESULT
BLOCKER_REPORTED
DEPENDENCY_CHANGED
MERGE_RESULT
```

Comments 是 append-oriented event log；重要历史错误用 corrective event 修正，不静默重写。

### 7.5 Validation Issue 与 Branch

Validation Issue 不自动创建 branch。

如果只执行验证：

```text
Issue
→ checkout exact SHA
→ execute
→ Validation Report
→ update/close Issue according to completion rule
```

如果验证发现需要源码修改：

```text
Issue
→ task/fix branch
→ code change
→ PR to declared integration branch
→ new exact SHA
→ rerun affected required gates
```

旧 SHA 的 evidence 不得自动迁移到新 SHA。

Local Agent Handoff SHOULD 使用 `templates/local-agent-handoff-issue.md`。Codex-specific legacy flow MAY 使用 `templates/codex-handoff-issue.md`，但新工作优先 generic Local Agent contract。

## 8. Builder / Reviewer / Validator Queues

### Builder

主要消费：

```text
state:ready
state:changes-requested
```

完成可审查实现和当前可运行 Validation 后，发布 `IMPLEMENTATION_READY` 并进入 `state:review-ready`。

Builder 在 Task DAG 允许时 SHOULD 继续其它独立 Task，不必等待 Reviewer。

### Reviewer

主要消费：

```text
state:review-ready
```

读取 pinned standard、Task Issue、Issue Dependencies、Frozen inputs、PR diff、Validation Evidence，并对 exact HEAD SHA 做 Independent Review。

结果路由到：

```text
state:changes-requested
state:validation-needed
state:merge-ready
state:blocked
```

### Validator / Local Agent

主要消费：

```text
state:validation-needed
```

或专门的 Validation Issue。真实执行结果绑定 exact SHA，不因另一个 tuple/旧 SHA PASS 自动继承。

普通 ChatGPT session 不是后台 worker；queue 只在 Agent 被调用、受支持自动化触发或外部 orchestrator 调度时消费。

## 9. Independent Review Gate

Version Branch Mode 的 Task/Fix PR merge 前，Independent Review 默认 mandatory。

规则：

- final review authority SHOULD 与刚完成实现的 context 独立；
- 同模型的 fresh session 可以作为独立 context，只要重新从 GitHub 重建事实；
- Reviewer 不依赖 Builder 私有聊天推理；
- Review PASS 绑定 exact PR HEAD SHA；
- HEAD 改变后，旧 PASS 只保留历史意义；当前 Review Gate 回到 `NOT_RUN`，执行 delta/full re-review；
- runtime/platform 事实无法静态确认时发 `VALIDATION_REQUEST`，不得猜测为 PASS。

推荐启动 Prompt：`prompts/independent-review-bootstrap.md`。

## 10. Local Agent Handoff

新的执行/验证交接 SHOULD 使用 `standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`。

Handoff Issue 必须使 Agent 可以只依赖以下入口开始工作：

```text
repository
issue number
```

Issue 本身提供 task-specific contract；通用执行纪律由 pinned standard 与 `prompts/local-agent-bootstrap.md` 提供。

至少需要：

```text
standard version + revision
repository
integration branch
baseline SHA
scope/task IDs
frozen inputs
web completed
remaining work
required gates / tuples
execution environment
validation profile
exact commands / canonical entrypoints
allowed changes
forbidden changes
expected output
completion rule
failure/blocker reporting rule
```

## 11. PR

PR 使用 `templates/implementation-pr.md` 或项目等价模板。

原则：

- One concern, one PR；
- 必须说明 baseline、scope、Task/Issue、Issue Dependencies、branch strategy、target integration branch、变化、Validation Evidence、Independent Review、known blockers 与 downstream impact；
- 大版本可先 Draft；
- 不要求为了形式填写与当前 concern 无关的长 checklist。

在 Version Branch Mode：

- Task/Fix concern 在 required task Validation + Independent Review + configured required Minimal CI + dependency merge policy 满足后即可合并到 version branch；
- 不等待同版本其它独立 concern；
- 最终版本 PR 在 integrated version baseline 完成 required closure 后合并 `main`。

在 Trunk/Fast Path：

- 独立 concern 可按项目 policy 直接 PR 到 `main`。

## 12. Ownership

多人协作、共享 package、部署/安全/基础设施等高风险目录 SHOULD 使用 CODEOWNERS 或等价 ownership 规则。

单人私有项目不要求为了形式创建 CODEOWNERS，但 Version Branch Task/Fix 的 Independent Review 仍可由另一个 Session/Agent 完成。

## 13. Minimal CI

CI 默认目标是：**用最少资源获得独立 clean-checkout 复核价值**。

### 13.1 默认 profile

`minimal` profile SHOULD 包含：

- standard/project verifier；
- format/lint/typecheck 的必要确定性子集；
- 快速 unit/contract smoke；
- basic build smoke。

SHOULD NOT 默认包含：

- 完整 OS/runtime matrix；
- 真机/真实 SDK；
- Critical Journeys；
- Hidden Validation；
- 高成本 Integration/E2E；
- packaging/release artifact。

### 13.2 项目 profile

项目在 `.dev-standard/PROJECT_OVERRIDES.md` 声明：

```text
CI profile = minimal | custom | disabled
```

`custom` 必须明确 checks；`disabled` 必须记录理由与替代的 exact-SHA clean validation / Independent Review 路径。

CI 关闭不代表 Validation 或 Review 可以关闭。

### 13.3 触发策略

优先减少重复执行：

- concern PR 上运行一次 minimal profile；
- version branch/main push 不必机械重复同一昂贵矩阵；
- release candidate 只有项目 policy 要求时才重跑 minimal sanity；
- platform/CJ/Hidden/packaging 由更合适的真实执行环境完成。

Branch 数量本身不会触发 CI；是否触发由 workflow/config 决定。成本控制应优先通过 CI profile、trigger policy 与 self-hosted/local validation 完成，而不是牺牲必要的 Task isolation。

## 14. Repository Storage Hygiene

分支是 Git refs；但分支提交的不同 Git objects 仍会增加 repository 数据。

不得因为 Task 分支多而重复提交：

- dependency caches / `node_modules`；
- build/dist cache；
- 大型数据库；
- model weights；
- installers；
- 重复压缩包；
- 大型日志/报告；
- 不需要进入 source history 的测试输出。

遵守 `REPOSITORY_STANDARD.md` 的 Git LFS / artifact / object-storage 规则。

## 15. Stable Branch Protection

`main` 或等价稳定分支 SHOULD 根据项目风险启用 ruleset/branch protection。

若 CI profile 为 `minimal/custom`，可把对应最小 checks 设为 required status checks。

若项目显式 `CI profile = disabled`，不得创建永远无法满足的 required status check；此时 merge policy 应依赖 PR Independent Review + required exact-SHA Validation Evidence。

Version Branch 是否启用同等级保护由项目风险决定。多人并行或版本较长时 SHOULD 至少禁止 force push 并保持 PR integration。

## 16. Merge

优先 squash 或项目既定策略。

Version Branch Task/Fix concern merge 前需满足：

```text
correct Task/Issue linkage
correct Issue Dependencies / stack topology
concern scope
required task/local validation
Independent Review on current exact SHA
configured required minimal CI（若启用）
correct target integration branch / stack parent
no unresolved release-significant blocker
```

CI 不是 merge 的唯一权威，也不能替代未执行的 required validation/review。

Task/Fix merge 后，integration branch 的新 commit SHA 成为该集成点远端事实，并 SHOULD 记录 `MERGE_RESULT` event。

最终 Version Closure 必须明确 integrated candidate SHA 与 final `main` baseline SHA，而不是只引用 PR number、branch name 或 tag。
