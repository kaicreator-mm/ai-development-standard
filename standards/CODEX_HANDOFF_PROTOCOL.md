# Codex Handoff Protocol

## 1. 为什么用 Issue

Codex Handoff 是一次性的 Work Item，因此使用 GitHub Issue；长期执行规则留在标准仓库；代码变化使用 PR。不要为每次交接往业务项目 `docs/` 增加过程性 Markdown。

## 2. Issue 命名

推荐：

`[<version-or-task>] Codex Handoff — <validation/fix scope>`

建议 label：`codex-handoff`、`validation`，需要完整 Build Host 时增加 `needs-build-host`，阻塞发布时增加 `release-blocker`。

## 3. 必填字段

- Standard Version
- Repository
- Branch
- Baseline Commit
- Scope / Task IDs
- Web Completed
- Web Validation
- Remaining Work
- Required Gates
- Allowed Changes
- Forbidden Changes
- Expected Output

## 4. Baseline 规则

必须使用完整或足够唯一的 commit SHA。Codex不得以未经确认的更晚 commit 替换 baseline。如果 branch 已前进，应先判断新 commit 是否属于同一任务，并记录实际执行基线。

## 5. 完成条件

Handoff 只有在以下之一发生时结束：

- 所有 required gates PASS，PR/commit 与 Validation Report 已关联。
- 明确 BLOCKED，并提供复现、根因、影响范围和需要 Web 决策的问题。

## 6. Issue 与 PR

PR 应包含 `Closes #<handoff-issue>` 或明确关联。若 PR 尚不能关闭 Issue，可使用 `Refs #<issue>`，直到最终验证完成。
