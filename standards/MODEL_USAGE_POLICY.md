# Model Usage Policy

## 1. 原则

模型强度由任务风险决定，不由任务标题决定。优先让低成本模型执行边界明确、证据充分、可测试、可回滚的任务；Strong 模型集中处理产品/架构决策、复杂推理、高风险 review 和 release judgement。

## 2. Strong 优先任务

- 新产品或重大产品边界
- PRD 冲突与需求裁决
- 架构取舍与跨服务边界
- 安全模型、权限、数据一致性
- 高影响 schema/API migration
- 多证据冲突的 L1/L2 结论
- Final Closeout 中的重大风险判断

## 3. Lower-cost 适合任务

在提供 Contract、Tests、Reference Pack 后：

- 明确 CRUD / adapter / mapper
- 局部 UI 组件
- 类型与 schema 对齐
- 标准测试补充
- 文档同步
- lint/build/CI 修复
- 明确 failure case 修复

本地 Agent 领域（`LOCAL_BUILDER` / validator profiles）：repository 集成、adapters、fixtures、workspace wiring、compile/type/lint 修复、packaging、平台集成、real-host 执行。

## 3a. Semantic Kernel 准备分工

高风险语义 Concern 允许 Web/Strong 模型先准备紧凑 Semantic Kernel（进入 Execution Pack 的 seed，见 `EXECUTION_PACK_STANDARD.md`）：

```text
domain/public contracts        identity/digest 规则
state-transition predicates    authority boundaries
binding/pinning 规则           fail-closed validators
ordering/concurrency invariants critical ports/interfaces
negative test oracle
```

seed 只包含可验证 contracts/predicates/oracle，不包含私有 chain-of-thought。此后 repository mechanics 才交给 lower-cost 本地执行。这是本政策的延伸，不是第二套模型路由标准。

执行自由度按 Task Pack / Execution Pack 的 `agent_freedom`（F0–F3）机器可读地约束；executor 不得自我提升到更高权威级别。

## 4. 升级条件

出现需求歧义、架构冲突、公共契约变化、安全风险、反复失败或证据不足时，应升级到更强模型/回到 ChatGPT Web，而不是继续盲目迭代。
