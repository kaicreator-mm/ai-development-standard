# L3 Implementation Evidence Research Prompt

你正在执行第三层 Task-level 实现证据研究。产品与架构已基本冻结，Task DAG 已存在。目标是给具体 Task 提供最小、可执行、可验证的 Reference Pack，提高低成本模型/并行 Agent 的实现确定性。

## L3 Detailed Design & Implementation：任务级设计与 DAG-I（增量候选）

L3 不是只有外部 Implementation Reference。它在真实实现任务需要时，围绕一项**可独立验收的成果**提供详细设计/实施契约：已有 Frozen Product/L2/DAG 与当前代码基线、可改写范围、模块与函数/数据结构、输入输出和接口、算法/状态变迁、关键不变量、具体测试与负例 Oracle、失败/超时/恢复、实现参考及验证映射。只对 material concern 展开，简单可证明改动可直接使用现有 Task Pack，无需单独 L3 文档。

L3 的执行依赖图就是已有的 **Implementation Task DAG（DAG-I）**：合法 materialization 后 GitHub native Issue Dependencies 仍是唯一 live Task blocking 权威；Task Pack/Execution Pack、Claim/CAS、write-set、Review Policy、Validation/Release 不另造。任务内部的 Tests→Contract→Implementation→Failure→Docs 是指导性工作序列或局部 checklist，**不是第四套正式 DAG**。可并行的 Contract/Core/Adapter/UI/Integration/Validation 任务，仅在实际工作与写集可以合法独立时拆分。

**L3 退出条件**是已给执行 Agent 足够的 Task-level 合法上下文、可观察的实施/测试契约、适用的工程工具与真实环境验证条件，随后由既有 Task/CI/Review/Integration/Release 证据判断实际完成；L3 研究完成本身不意味着编码 PASS。发现失配时先定位实现根因；只有材料确实否定 L2/L1 时才逐层申请有界修订。详见 [三级设计提案](../docs/intake/2026-11-21-three-phase-adaptive-engineering-r0.md)。

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
