# Release Standard

## 1. Final Closeout 输入

- 冻结的 PRD / scope
- Task DAG 最终状态
- 最终 commit/PR
- Validation Report
- GitHub CI required checks
- 文档同步状态
- 已知限制与 deferred items

## 2. Release Decision

### READY

所有 release blocker 已解决；required gates PASS；文档与实现一致；没有未声明的范围缺失。

### CONDITIONAL

required gates 通过，但存在明确、可接受、非阻塞限制。必须记录限制、影响与后续 Task。

### BLOCKED

任一 release blocker 未完成，或 required gate 为 FAIL/NOT_RUN/BLOCKED，或产品范围存在未解释缺口。

## 3. Deferred

Deferred 必须是显式产品/版本决策，不得把失败测试简单改名为 deferred。Deferred 内容需要说明为什么不阻塞当前 release。

## 4. Release 动作

建议顺序：Final Closeout → merge → final main CI → tag → release candidate/release → close milestone/issues。

## 5. Release 记录

至少记录：版本、tag、commit、采用的 Development Standard 版本、CI 结果、重要已知限制。
