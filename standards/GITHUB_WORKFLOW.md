# GitHub Workflow

## 1. GitHub 对象职责

- **Repository files**：长期规范、代码、测试、文档。
- **Issue**：Task、bug、Codex Handoff、blocker 等 Work Item。
- **Branch**：一组隔离中的实现。
- **Commit**：不可歧义的执行 baseline / change identity。
- **Push**：把稳定 checkpoint 发布到远端，使其可恢复、可交接、可审计。
- **Pull Request**：准备评审/合并的一组真实变化。
- **Actions / CI**：独立验证。
- **Tag / Release**：已完成版本身份。

## 2. 分支建议

- `feat/<version-or-task>`
- `fix/<issue-or-task>`
- `chore/<scope>`

不强制复杂 GitFlow。小团队优先短分支 + PR + main。

## 3. Commit

Commit 应保持任务相关，避免混入无关格式化或大范围重写。Codex Handoff 必须引用具体 commit。

Commit 与 push 不等价：阶段内部可以有多个本地 commit；只有达到稳定 checkpoint 时才要求把对应 commit push 到远端。

## 4. Push / Stage Checkpoint

不得把“每个操作都 push”作为流程要求。Push 的主要职责是发布正式、稳定、可恢复的 checkpoint。

当正式阶段产物成为后续阶段输入或约束时，阶段结束必须 push。典型包括 PRD Freeze、Architecture Evidence、Task DAG、L3 Implementation Evidence、可审查的 Task / Concern、Validation / Closeout 与 Release baseline。

Implementation 阶段以 `Task / Concern` 为主要远端同步单位。允许先形成多个本地 commit，在该 Task 达到可评审状态后统一 push，并进入 PR / CI / Review。

以下内容通常不要求单独 push：草稿、单文件临时编辑、一次测试运行、尚未形成稳定状态的中间修复。

对长任务、多 Agent、跨会话任务，应在每个正式 Stage 或 Task checkpoint push，确保可以仅依赖 GitHub commit 恢复执行。

## 5. Issue

Codex Handoff 使用 `templates/codex-handoff-issue.md`。普通 Task 可使用项目自己的 Task template。

## 6. PR

PR 使用 `templates/implementation-pr.md`。必须说明变更原因、范围、验证和关联 Issue。大版本可先建 Draft PR，让 Codex在其上完成真实环境修复。

原则上遵循 `One concern, one PR`。每个独立 concern 在局部 Validation / Review / CI 通过后即可按项目策略合并 main，不要求等待同版本其它 concern 一起合并。

## 7. CI

Required checks 应尽可能在 PR merge 前强制。Self-hosted runner 负责特殊 SDK/设备/高成本环境时，应与 cloud runner 的 clean verification 做合理分工。

## 8. Merge

优先 squash 或项目既定策略。Merge 前需满足 required review/CI。Merge 后 Handoff Issue 应自动或手动关闭。
