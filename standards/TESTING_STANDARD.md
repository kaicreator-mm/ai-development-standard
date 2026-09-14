# Testing Standard

## 1. 目标

测试用于证明行为和边界，不用于制造漂亮数字。测试策略必须与风险、contract、用户关键路径和 release gate 对齐，并能在本地、Agent 执行环境与 CI 之间重复运行。

## 2. 测试层级

### Unit / Component

验证纯逻辑、局部组件和小范围行为。应快速、确定、隔离，适合开发循环和每个 Task 的 Fast Gate。

### Contract

验证 public API、schema、serialization、CLI contract、事件格式、adapter interface 等稳定边界。公共 contract 发生变化时必须有对应测试或明确的兼容性决策。

### Integration

验证多个真实组件组合，例如 API + DB、service + filesystem、frontend + backend、queue/worker、storage adapter。外部第三方可在 PR Gate 使用可信 mock/stub/test double，但不得把 mock 结果当作真实外部服务通过。

### E2E / Critical Journey

验证真实用户或系统关键闭环。Critical Journey 应围绕业务结果，而不是把所有 API 拼接成一条脆弱大测试。

### Hidden Validation

使用实现阶段未依赖其具体答案的独立场景、数据和不变量验证输出质量、边界、错误处理与关键路径。Hidden Validation 不替代常规测试；它是防止实现只迎合公开样例的独立证据层。

### Build / Packaging / Platform

验证真实可交付产物，例如 Docker image、desktop installer、mobile build、browser bundle、release binary 或 migration package。

## 3. 测试布局

- Unit/component tests MAY co-locate 在模块源码旁或模块自己的 `tests/`。
- 跨模块 integration/e2e/critical-journey tests SHOULD 放根 `tests/` 的明确目录。
- fixture/testdata 必须有用途和所有权，不得把生产 dump 直接复制进仓库。
- 大型二进制 fixture SHOULD 使用生成器、外部 artifact 或最小化样本，避免仓库无界增长。

## 4. 测试数据

测试数据 MUST：

- 不包含真实 secret/token/password；
- 避免真实个人敏感数据；
- 在需要随机性时使用可重现 seed 或记录 seed；
- 对时间、时区、locale、排序等不稳定因素显式控制；
- 清楚区分 fixture、golden/snapshot 和 expected result。

## 5. 测试独立性

测试 SHOULD 可独立运行并清理自身状态。不得依赖“必须先运行另一个测试”或开发机历史数据才能通过。

共享 DB/queue/filesystem 时，应通过 isolated namespace、transaction、temporary directory 或等价机制减少互相污染。

## 6. 变更要求

- Bug fix SHOULD 添加能复现该 bug 的 regression test，除非客观不可测试并在 PR 中说明。
- 新 public contract SHOULD 先定义或同步 contract test。
- 数据迁移 SHOULD 测试升级路径；高风险迁移还应验证失败恢复/重试/兼容窗口。
- 错误处理 SHOULD 测真实 failure behavior，不仅验证 happy path。
- UI 变化对关键交互 SHOULD 有 component 或 E2E 证据；纯视觉变化按项目需要使用 screenshot/visual regression。

## 7. Coverage

Coverage 是发现盲区的信号，不是质量目标本身。

禁止：

- 为提高行覆盖率写没有断言价值的测试；
- 为达阈值测试第三方库内部行为；
- 用覆盖率替代关键业务、failure path、contract 和 integration 验证。

项目可以定义 coverage threshold，但必须与风险和历史基线合理对应。

## 8. Flaky Test

Flaky test 是缺陷，不是“偶尔失败可以接受”。

发现 flaky 时：

1. 记录失败证据和可疑非确定因素；
2. 修复 isolation/time/network/concurrency 等根因；
3. 必须临时 quarantine 时，创建明确 Task/Issue、owner 与退出条件；
4. 不得仅通过无限 retry 或扩大 timeout 掩盖确定性问题。

## 9. Snapshot / Golden

Snapshot/golden test 适合复杂结构化输出，但必须可审查。大面积 snapshot 更新不能仅因为“测试需要更新”就接受；PR 必须能解释语义变化。

对 AI/LLM 输出，优先验证结构、约束、不变量、评分规则和关键语义，不对自然语言全文做无意义精确字符串匹配。

## 10. External Boundary

外部 API、云服务、LLM provider、支付、邮件等边界建议分层：

- PR/Fast Gate：contract mock/stub + deterministic fixture；
- Integration Gate：可控 sandbox/test environment；
- Version Closure：对 release blocker 依赖按项目策略执行真实边界验证。

真实外部服务不可用时应写 `BLOCKED/NOT_RUN`，不能用 mock PASS 冒充真实验证 PASS。

## 11. 性能、安全与可靠性

当 PRD/Architecture 声明性能、容量、安全或可靠性目标时，必须有相应可执行验证或清晰的人工 gate。不要在没有目标值和基线时把“性能测试”变成无结论 benchmark。

## 12. CI 分层

与 `VALIDATION_STANDARD.md` 对齐：

- PR/Task 优先跑 Fast Gate + 受影响的 integration/build；
- main/关键 PR 跑更完整的 integration/e2e；
- Version Closure 再执行 Critical Journey、Hidden Validation、真实 packaging/platform 和 required external boundary。

PR PASS 不等于 Release PASS。

## 13. 禁止事项

- 为让 CI 通过删除有效测试/断言。
- 将 required test 标记 skip/xpass 而没有批准的原因。
- 测试实现细节到使正常重构无法进行，而没有 contract 价值。
- 依赖共享开发环境中的残留数据。
- 把没有执行的测试写成 PASS。
