# L3 Implementation Evidence Research Prompt

你正在执行第三层 Task-level 实现证据研究。产品与架构已基本冻结，Task DAG 已存在。目标是给具体 Task 提供最小、可执行、可验证的 Reference Pack，提高低成本模型/并行 Agent 的实现确定性。

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
