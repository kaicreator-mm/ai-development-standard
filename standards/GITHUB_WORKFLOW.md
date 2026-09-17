# GitHub Workflow

## 1. GitHub 对象职责

- **Repository files**：长期规范、代码、测试、文档。
- **Issue**：Task、bug、Validation、Handoff、blocker 等 Work Item。
- **Milestone**：版本/发布范围聚合，例如 `vX.Y.Z`。
- **Label**：Work Item 的稳定属性，例如 type、executor、gate、environment、release impact。
- **Branch**：隔离中的实现 concern 或版本集成面。
- **Commit**：不可歧义的执行 baseline / change identity。
- **Push**：发布稳定 checkpoint，使其可恢复、可交接、可审计。
- **Pull Request**：准备评审/合并的一组真实变化。
- **Actions / CI**：可选的最小 clean-checkout 独立复核器，不是完整 Validation 或 Release Authority。
- **Validation Evidence**：exact-SHA 的真实执行证据。
- **Tag / Release**：可选的人类友好发布别名/分发对象；immutable commit SHA 始终是 canonical identity。

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

## 3. 分支建议

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

## 4. Commit

Commit 应保持 concern 相关，避免混入无关格式化或大范围重写。

Handoff、Validation、Candidate 与 Release evidence 必须引用具体 commit SHA。

Commit 与 push 不等价：阶段内部可以有多个本地 commit；达到稳定 checkpoint 时再 push。

## 5. Push / Stage Checkpoint

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

## 6. Issue

Issue 是一次性的 Work Item，不是长期规范文件。

推荐用途：

- implementation task；
- bug；
- validation；
- Local Agent handoff；
- blocker；
- follow-up / deferred work。

Local Agent Handoff SHOULD 使用 `templates/local-agent-handoff-issue.md`。Codex-specific legacy flow MAY 使用 `templates/codex-handoff-issue.md`，但新工作优先 generic Local Agent contract。

重复出现的 bug/feature/support/validation 类型 SHOULD 使用 Issue Form/Template 标准化必要输入。

### 6.1 Milestone 与 Label

版本 SHOULD 优先用 GitHub Milestone 表示，例如：

```text
v0.1.0
v2.9.4
```

不要为每个版本创建一次性 version label，除非项目有明确理由。

推荐稳定标签维度：

```text
type:task
type:bug
type:validation

handoff:local-agent
executor:codex
executor:claude-code

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

项目 MAY 使用等价命名，但 SHOULD 区分 work type、executor、gate、environment 与 release impact。

### 6.2 Validation Issue 与 Branch

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

## 7. Local Agent Handoff

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

## 8. PR

PR 使用 `templates/implementation-pr.md` 或项目等价模板。

原则：

- One concern, one PR；
- 必须说明 baseline、scope、target integration branch、变化、Validation Evidence、known blockers 与 downstream impact；
- 大版本可先 Draft；
- 不要求为了形式填写与当前 concern 无关的长 checklist。

在 Version Branch Mode：

- Task/Fix concern 在项目 merge policy 满足后即可合并到 version branch；
- 不等待同版本其它独立 concern；
- 最终版本 PR 在 integrated version baseline 完成 required closure 后合并 `main`。

在 Trunk/Fast Path：

- 独立 concern 可按项目 policy 直接 PR 到 `main`。

## 9. Ownership

多人协作、共享 package、部署/安全/基础设施等高风险目录 SHOULD 使用 CODEOWNERS 或等价 ownership 规则。

单人私有项目不要求为了形式创建 CODEOWNERS。

## 10. Minimal CI

CI 默认目标是：**用最少资源获得独立 clean-checkout 复核价值**。

### 10.1 默认 profile

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

### 10.2 项目 profile

项目在 `.dev-standard/PROJECT_OVERRIDES.md` 声明：

```text
CI profile = minimal | custom | disabled
```

`custom` 必须明确 checks；`disabled` 必须记录理由与替代的 exact-SHA clean validation / review 路径。

CI 关闭不代表 Validation 可以关闭。

### 10.3 触发策略

优先减少重复执行：

- concern PR 上运行一次 minimal profile；
- version branch/main push 不必机械重复同一昂贵矩阵；
- release candidate 只有项目 policy 要求时才重跑 minimal sanity；
- platform/CJ/Hidden/packaging 由更合适的真实执行环境完成。

Branch 数量本身不会触发 CI；是否触发由 workflow/config 决定。成本控制应优先通过 CI profile、trigger policy 与 self-hosted/local validation 完成，而不是牺牲必要的 Task isolation。

## 11. Repository Storage Hygiene

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

## 12. Stable Branch Protection

`main` 或等价稳定分支 SHOULD 根据项目风险启用 ruleset/branch protection。

若 CI profile 为 `minimal/custom`，可把对应最小 checks 设为 required status checks。

若项目显式 `CI profile = disabled`，不得创建永远无法满足的 required status check；此时 merge policy 应依赖 PR review + required exact-SHA Validation Evidence。

Version Branch 是否启用同等级保护由项目风险决定。多人并行或版本较长时 SHOULD 至少禁止 force push 并保持 PR integration。

## 13. Merge

优先 squash 或项目既定策略。

Concern merge 前需满足项目实际声明的：

```text
concern scope
required task/local validation
review
configured minimal CI（若启用）
correct target integration branch
```

CI 不是 merge 的唯一权威，也不能替代未执行的 required validation。

Task/Fix merge 后，integration branch 的新 commit SHA 成为该集成点远端事实。

最终 Version Closure 必须明确 integrated candidate SHA 与 final `main` baseline SHA，而不是只引用 PR number、branch name 或 tag。
