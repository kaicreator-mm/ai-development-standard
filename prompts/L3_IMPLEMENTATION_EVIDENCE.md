# L3 Implementation Evidence Research Prompt

你正在执行第三层 Task-level 实现证据研究。产品与架构已基本冻结，Task DAG 已存在。目标是给具体 Task 提供最小、可执行、可验证的 Reference Pack，提高低成本模型/并行 Agent 的实现确定性。

## 从 L1/L2 延续上游证据而非重复发明

消费 Frozen L2 中已选的上游 source/decision refs，仅对本 Task 相关切片进行必要的 **source-currentness** 与许可/测试适用性回读。保持 L1 用户 Job/竞品事实、L2 模式与复用判断、L3 exact implementation/test proof 的三个不同层级：引用上游 issue/PR/revert/benchmark 可说明失败模式，但不等于当前代码行为或本地测试已通过；上游源码/README 的版本变化必须记录为 `UNKNOWN/STALE` 或另有精确 source 依据。

若引用源码实现或 Tests，Reference Pack SHOULD 保留 `upstream identity + immutable version/commit + exact path/test + usage/license scope + observed-vs-inferred + local divergence + validation mapping`；不存在可解析 immutable ref 时不应虚构，明确限制/替代参考路径。已有合格 L2 证据可引用而无需重复广泛研究。**L3 Reference Pack 不是新的 Product 或 Architecture Authority，也不是 license 自动批准。**

## 证据优先级

`Tests → Contract/Interface → Core Implementation → Failure Handling → Examples/Docs`

## 每个 Task 需要回答

1. 哪个成熟项目/官方实现最接近该 Task？
2. 哪些测试最能说明正确行为与边界？
3. 哪个接口/contract 必须保持？
4. 哪段核心实现值得参考，而不是复制整仓库？
5. 失败处理、重试、异常、边界情况怎么做？
6. 版本与 License 是否允许参考/复用？
7. 明确 Do / Don't。

## 输出 Reference Pack

- Task ID / intent
- Selected references + versions + licenses
- Tests to emulate
- Contract/interface notes
- Core implementation excerpts/locations
- Failure handling patterns
- Do / Don't
- Reuse risk
- Acceptance/validation mapping

避免给低成本 Agent 一个巨大仓库让其自行搜索；只提供与 Task 直接相关的最小证据包。
