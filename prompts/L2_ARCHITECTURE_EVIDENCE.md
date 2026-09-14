# L2 Architecture Evidence Research Prompt

你正在执行第二层架构证据研究。产品范围已基本冻结。目标是验证“什么架构模式最适合这些约束”，而不是从流行技术中挑选工具。

## 输入

- Frozen PRD / scope
- Existing architecture and repository
- Non-functional requirements
- Deployment / team / cost / security constraints

## 研究要求

1. 提取最关键的 architecture drivers 与 invariants。
2. 搜索成熟系统、官方设计、开源实现和失败案例来验证候选模式。
3. 比较数据所有权、边界、同步/异步、失败恢复、幂等、版本、可观测性、升级路径。
4. 优先选择能从现有代码渐进演进的方案，除非重写有充分证据。
5. 对每个重大决策给出 alternatives、trade-offs、failure modes 和 rollback/escape hatch。
6. 明确哪些能力属于公共基础服务，哪些必须留在领域系统。

## 输出

- Architecture Drivers
- Current-state Findings
- Candidate Patterns + Evidence
- Decision Matrix
- Recommended Architecture
- Key ADRs / Invariants
- Migration Plan
- Architecture Risks / Open Questions

研究结果必须能够直接支撑 Task DAG，而不是停留在概念层。
