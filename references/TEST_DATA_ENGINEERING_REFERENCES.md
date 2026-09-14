# Test Data Engineering References

本文件记录 `TEST_DATA_AND_SCENARIO_STANDARD.md` 制定时采用的公开工程参考与提炼原则。它是 provenance/evidence，不是把外部项目的具体实现提升为全局硬规则。

## Hypothesis

Repository: `HypothesisWorks/hypothesis`

Relevant principle:

- Property-based testing 从输入空间/策略生成案例，而不是只写少量手工 example。
- 自动探索人类容易遗漏的 edge cases。
- 发现失败时会尽量缩小到更简单的 failing example，利于形成 minimal reproduction 与 regression case。

Adopted into this standard:

- scenario/risk coverage 比纯数据条数更重要；
- property-based generation 是 deterministic curated cases 的补充；
- 发现失败后应保存最小复现样本进入 regression。

## Faker

Repository: `joke2k/faker`

Relevant principle:

- synthetic data generator 可用于测试、bootstrap 和 stress/load 场景；
- 支持 locale/provider 扩展；
- seed 可以帮助测试重复生成相同序列；
- 仅有 seed 仍不够：generator/dataset 版本升级可能改变结果，因此稳定测试需要 pin generator/dependency revision 或冻结生成结果。

Adopted into this standard:

- generator identity、version、seed 和 locale/runtime assumptions 需要进入 pack metadata；
- 正式冻结 pack 推荐记录 output hash；
- bulk synthetic generation 与 Golden truth 分离。

## Schemathesis

Repository: `schemathesis/schemathesis`

Relevant principle:

- 从 OpenAPI/GraphQL schema 生成 valid、edge 和 invalid inputs；
- 同时检查 schema violations、validation bypass、stateful/integration failures；
- 支持 custom business-rule checks；
- schema coverage、replay past failures 和 baseline 都是测试生成的重要组成部分；
- generated/fuzz input 可混合真实 id、wordlist 或 LLM-generated payload，但仍需要 contract validation。

Adopted into this standard:

- structure/schema invalid、domain invalid、runtime failure 必须区分；
- schema/contract 可以驱动输入生成，但不能替代 domain-rule validation；
- generation 后必须有 coverage/replay/regression 闭环；
- LLM-generated payload 是输入来源之一，不是自动可信的 expected oracle。

## Generalized Rules

综合以上实践，本标准采用：

1. **Evidence-driven**：数据从 contract/rule/evidence 派生。
2. **Scenario before records**：先做风险/维度模型，再生成记录。
3. **Curated + Generated**：Golden/Regression 由高价值 curated cases 承担，bulk coverage 由 deterministic/property-based generator 补充。
4. **Reproducible**：seed + generator version + frozen dependency/hash。
5. **Separated invalidity**：schema-invalid、domain-invalid、failure-injection 分离。
6. **Replayable failures**：任何自动发现的失败都应能形成最小复现和 regression asset。
7. **LLM is not oracle**：LLM 可以辅助构造语义输入，但不能凭自身生成并批准 Golden truth。
