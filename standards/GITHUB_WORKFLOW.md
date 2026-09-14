# GitHub Workflow

## 1. GitHub 对象职责

- **Repository files**：长期规范、代码、测试、文档。
- **Issue**：Task、bug、Codex Handoff、blocker 等 Work Item。
- **Branch**：一组隔离中的实现。
- **Commit**：不可歧义的执行 baseline / change identity。
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

## 4. Issue

Codex Handoff 使用 `templates/codex-handoff-issue.md`。普通 Task 可使用项目自己的 Task template。

## 5. PR

PR 使用 `templates/implementation-pr.md`。必须说明变更原因、范围、验证和关联 Issue。大版本可先建 Draft PR，让 Codex在其上完成真实环境修复。

## 6. CI

Required checks 应尽可能在 PR merge 前强制。Self-hosted runner 负责特殊 SDK/设备/高成本环境时，应与 cloud runner 的 clean verification 做合理分工。

## 7. Merge

优先 squash 或项目既定策略。Merge 前需满足 required review/CI。Merge 后 Handoff Issue 应自动或手动关闭。
