# L2 Architecture Evidence Research Prompt

你正在执行第二层架构证据研究。产品范围已基本冻结。目标是验证“什么架构模式最适合这些约束”，而不是从流行技术中挑选工具。

## 输入

- Frozen PRD / scope
- Existing architecture and repository
- Non-functional requirements
- Deployment / team / cost / security constraints
- Existing research / demo evidence and exact SHAs when available

## 消费 L1 上游证据与向 L3 传递决策（按需）

如果 L1 已保存相关 prior-art/竞品证据，优先 **按原 durable ref** 消费，而非从零重复搜索；逐条核对所需上游 revision、claim 类型、时间敏感性和 Product Freeze 后的适用性。失效/不可读取的证据标记 `STALE/UNKNOWN` 并定向补充，不因“L1 已看过”而推断当前架构证据合格。L1 的产品重叠判断不自动产生架构复用许可。

对确实影响架构的上游能力切片，输出有界 handoff：上游身份/精确检视 ref、可证伪的机制事实或故障案例、采纳的模式/重建/直接复用/自研决定及依据、license/security/compatibility 限制与未知、local contract/边界、预期 L3 测试/反例，绑定本次 Frozen Product 和 L2 当前决策。只选择影响实际 Task 的来源；禁止第二套通用 Research 生命周期或强制全量 history mining。

## 研究要求

1. 提取最关键的 architecture drivers、invariants 与 **Architecture UNKNOWNs**。
2. 搜索成熟系统、官方设计、开源实现和失败案例来验证候选模式。
3. 比较数据所有权、边界、同步/异步、失败恢复、幂等、版本、可观测性、升级路径。
4. 对每个重大 UNKNOWN 判断：静态/源码/既有 executable evidence 是否足够。
5. 当一个高影响架构假设仍为 UNKNOWN、会影响架构/公共 contract/durability/failure semantics，且静态证据不足时，按 `standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md` 创建最小 Research Demo / Spike，使用可证伪 Hypothesis 和 exact-SHA executable evidence。
6. 不要为已有充分证据或 Frozen L2 下的普通实现机械创建 Demo。Demo 是风险驱动证据，不是 universal stage/gate。
7. 优先选择能从现有代码渐进演进的方案，除非重写有充分证据。
8. 对每个重大决策给出 alternatives、trade-offs、failure modes 和 rollback/escape hatch。
9. 明确哪些能力属于公共基础服务，哪些必须留在领域系统。
10. 如果 Demo 只否定某个技术方案，调整候选架构；只有证据表明 Frozen PRD 本身 contradiction/unachievable 时，才报告 Architecture Contradiction 并请求重新打开产品范围。
11. 为后续 Task DAG 明确可并行的 ownership/write-set boundaries：哪些 contract/core/adapter/UI/validation/platform/domain concerns 可以形成独立 lane，哪些必须因为共享 mutable contract、central wiring、未冻结 architecture 或真实 code-baseline dependency 保持串行。
12. 不要为了“看起来并行”制造伪 lane；目标是让 Task DAG 暴露 **maximum safe parallelism**，从而允许多个 Agent 在真实独立边界上并行推进并缩短 wall-clock development time。

## Research Demo 规则

需要 Demo 时，至少要求：

- falsifiable Hypothesis；
- Real Under Test 与 Deterministic Fakes；
- positive + negative/failure scenarios；
- observable counters/state/digests；
- Evidence Strength `E1 | E2 | E3`；
- baseline/dependency/final exact SHAs；
- `What was proven` 与 mandatory `What was NOT proven`；
- KEEP / ADAPT / DROP 与 Architecture implications。

优先使用：

- `templates/research-demo-issue.md`
- `templates/research-demo-report.md`
- `checklists/research-demo-validation.md`

## 输出

- Architecture Drivers
- Architecture UNKNOWNs + evidence disposition (`static evidence sufficient | demo required | blocked`)
- Current-state Findings
- Candidate Patterns + Evidence
- Research Demo Evidence references + exact SHAs（如适用）
- Decision Matrix
- Recommended Architecture
- Key ADRs / Invariants
- Migration Plan
- Architecture Risks / Open Questions
- Explicit Architecture Contradictions（如有）
- Task DAG Lane Hints：候选 lane、各 lane 的稳定输入/ownership/write-set 边界、必须串行的真实依赖、建议 convergence/integration point

研究结果必须能够直接支撑 L2 Freeze 和 Task DAG，而不是停留在概念层。未经所需 executable evidence 支持的高影响 UNKNOWN 不得伪装成已冻结 Architecture Fact。进入 Task DAG 生成时，应使用 `templates/task-dag.md` 的 Lane-Oriented Decomposition Prompt 主动寻找安全并行 lane，而不是默认把工作排成单一串行链。
