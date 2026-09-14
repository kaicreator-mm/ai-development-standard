# GitHub Workflow

## 1. GitHub 对象职责

- **Repository files**：长期规范、代码、测试、文档。
- **Issue**：Task、bug、Handoff、blocker 等 Work Item。
- **Branch**：隔离中的实现 concern。
- **Commit**：不可歧义的执行 baseline / change identity。
- **Push**：发布稳定 checkpoint，使其可恢复、可交接、可审计。
- **Pull Request**：准备评审/合并的一组真实变化。
- **Actions / CI**：可选的最小 clean-checkout 独立复核器，不是完整 Validation 或 Release Authority。
- **Validation Evidence**：exact-SHA 的真实执行证据。
- **Tag / Release**：可选的人类友好发布别名/分发对象；immutable commit SHA 始终是 canonical identity。

## 2. 分支建议

- `feat/<version-or-task>`
- `fix/<issue-or-task>`
- `test/<scope>`
- `chore/<scope>`
- `docs/<scope>`

不强制复杂 GitFlow。小团队优先短分支 + PR + main。

## 3. Commit

Commit 应保持 concern 相关，避免混入无关格式化或大范围重写。

Handoff、Validation、Candidate 与 Release evidence 必须引用具体 commit SHA。

Commit 与 push 不等价：阶段内部可以有多个本地 commit；达到稳定 checkpoint 时再 push。

## 4. Push / Stage Checkpoint

不得把“每个操作都 push”作为流程要求。Push 的主要职责是发布正式、稳定、可恢复的 checkpoint。

典型 checkpoint：PRD Freeze、Architecture Evidence、Task DAG、L3、可审查 Task/Concern、Validation、Candidate、Closeout、Release baseline。

长任务、多 Agent、跨会话任务应在正式 Stage/Concern checkpoint push，使后续可仅依赖 GitHub commit 恢复。

## 5. Issue

Codex/Execution Handoff 可使用 `templates/codex-handoff-issue.md`。普通 Task 可使用项目自己的 Task template。

重复出现的 bug/feature/support 类型 SHOULD 使用 Issue Form/Template 标准化必要输入。

## 6. PR

PR 使用 `templates/implementation-pr.md` 或项目等价模板。

原则：

- One concern, one PR；
- 必须说明 baseline、范围、变化、Validation Evidence、已知 blocker 与 downstream impact；
- 大版本可先 Draft；
- 不要求为了形式填写与当前 concern 无关的长 checklist。

独立 concern 在项目 merge policy 所要求的 Validation / Review / Minimal CI 满足后即可合并 main，不等待同版本其它 concern。

## 7. Ownership

多人协作、共享 package、部署/安全/基础设施等高风险目录 SHOULD 使用 CODEOWNERS 或等价 ownership 规则。

单人私有项目不要求为了形式创建 CODEOWNERS。

## 8. Minimal CI

CI 默认目标是：**用最少资源获得独立 clean-checkout 复核价值**。

### 8.1 默认 profile

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

### 8.2 项目 profile

项目在 `.dev-standard/PROJECT_OVERRIDES.md` 声明：

```text
CI profile = minimal | custom | disabled
```

`custom` 必须明确 checks；`disabled` 必须记录理由与替代的 exact-SHA clean validation / review 路径。

CI 关闭不代表 Validation 可以关闭。

### 8.3 触发策略

优先减少重复执行：

- concern PR 上运行一次 minimal profile；
- main push 不必重复同一昂贵矩阵；
- release candidate 只有项目 policy 要求时才重跑 minimal sanity；
- platform/CJ/Hidden/packaging 由其更合适的真实执行环境完成。

## 9. Stable Branch Protection

`main` 或等价稳定分支 SHOULD 根据项目风险启用 ruleset/branch protection。

若 CI profile 为 `minimal/custom`，可把对应最小 checks 设为 required status checks。

若项目显式 `CI profile = disabled`，不得创建永远无法满足的 required status check；此时 merge policy 应依赖 PR review + required exact-SHA Validation Evidence。

多人项目仍 SHOULD 要求 review、禁止 force push；单人项目可以简化 review，但不能取消事实和 Validation 真实性。

## 10. Merge

优先 squash 或项目既定策略。

Merge 前需满足项目实际声明的：

```text
concern scope
required validation
review
configured minimal CI（若启用）
```

CI 不是 merge 的唯一权威，也不能替代未执行的 required validation。

Merge 后 main 上的 merge/squash commit SHA 成为新的远端事实。Version Closure 必须明确最终 baseline SHA，而不是只引用 PR number 或 tag。
