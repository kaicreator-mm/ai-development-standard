# Release Standard

## 1. Final Closeout 输入

- 冻结的 PRD / scope；
- Task DAG 最终状态；
- 最终 immutable candidate/baseline commit SHA；
- Validation Report；
- required Validation Tuple matrix；
- Critical Journey 结果；
- Hidden Validation 结果（若项目定义）；
- Platform / Production Build evidence（按 frozen authority）；
- Minimal CI 结果（若项目 profile 启用并要求）；
- 文档同步状态；
- 已知限制与 deferred items。

CI 不再自动作为 Release Qualification 的必要输入。是否为 release-required 由 frozen/project policy 决定。

## 2. Candidate

区分：

```text
Candidate Prepared
Candidate Freeze
```

`Candidate Prepared` 表示 release notes、matrix、closeout、Hidden pack 等准备完成。

只有 required visible gates 在同一个 exact SHA 上满足冻结条件后，才能记录：

```text
CANDIDATE_FROZEN_SHA=<sha>
```

Hidden Validation Execution 默认只对 frozen candidate 执行。

## 3. Release Decision

### PASS / READY

所有 frozen mandatory release blockers 已解决；required gates PASS；文档与实现一致；没有未声明范围缺口。

### CONDITIONAL

required gates 通过，但存在明确、可接受、非阻塞限制。必须记录限制、影响、接受依据与后续 Task。

### BLOCKED

任一 release blocker 未完成，或 mandatory gate 为 `BLOCKED / NOT_RUN`，或范围存在未解释缺口。

### FAIL

存在已实际执行且失败的 mandatory release gate，且尚未通过修复/重新验证形成新的有效 candidate evidence。

## 4. Gate Authority

Release blocker 与 mandatory gate 必须能追溯到：

```text
Frozen PRD / Contract
→ Frozen Architecture
→ PROJECT_OVERRIDES
→ Task acceptance
→ Standard defaults
```

历史 workflow、旧 packaging script、旧 artifact 或 Agent 推测不能自行扩大 release gate。

## 5. Deferred

Deferred 必须是显式产品/版本决策，不得把失败测试简单改名为 deferred。

必须说明：

- deferred 内容；
- 为什么不阻塞当前 release；
- 风险；
- 后续 Task/Issue。

## 6. Release 动作

建议顺序：

```text
Integrated Baseline
→ Candidate Preparation
→ Required Visible Validation on exact SHA
→ Candidate Freeze
→ Hidden Validation
→ Final Closeout
→ Release Qualification
→ record immutable baseline SHA
→ optional tag / release
```

Minimal CI 可以在 PR 或 candidate 阶段提供独立 sanity，但不替代上述真实 release gates。

Tag 不是 release identity 的必要条件。commit SHA 是 canonical immutable identity。

## 7. Release 记录

至少记录：

- 产品版本；
- `CANDIDATE_FROZEN_SHA`（若冻结）；
- final immutable baseline commit SHA；
- Development Standard version + revision；
- required Validation / Critical Journey / Hidden / Platform 结果；
- Minimal CI 结果（若启用）；
- artifact/package identity（只有 frozen authority 要求或项目确实发布 artifact 时）；
- 重要已知限制。

若创建 tag/release，还应记录其名称，但不得只写 tag 而省略 commit SHA。

## 8. Version Closure

版本级收尾使用 `checklists/version-closure.md`。

PR 的局部 Validation 或 Minimal CI PASS 不能替代 integrated candidate 上的 Full Regression、Critical Journeys、Hidden Validation、真实 platform/production build 与 Release Qualification。

Closure 应保留每个 unresolved gate 的真实状态，不得为了输出 READY 而把 `BLOCKED / NOT_RUN / FAIL` 改写成其它状态。
