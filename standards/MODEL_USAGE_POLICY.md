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

## 4. 升级条件

出现需求歧义、架构冲突、公共契约变化、安全风险、反复失败或证据不足时，应升级到更强模型/回到 ChatGPT Web，而不是继续盲目迭代。
