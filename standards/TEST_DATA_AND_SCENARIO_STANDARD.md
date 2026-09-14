# Test Data & Scenario Standard

## 1. 目标与边界

本标准定义测试数据、模拟数据、Scenario、Golden Case、Regression Case、Hidden Validation Data 与规模数据的**来源、构造、生成、验证、存储和演化**。

目标不是生成大量“看起来真实”的记录，而是形成能够证明行为的测试资产：**可追溯、可复现、覆盖风险、能解释为什么正确**。

职责边界：

- `TESTING_STANDARD.md`：测试分层与测试策略；
- 本文件：测试输入、场景、Golden、生成器、数据来源与 coverage；
- `VALIDATION_STANDARD.md`：如何根据执行证据给出 PASS / FAIL / Release 判断。

参考实现见 `examples/test-data-pack/quote-assessment/`。

## 2. 核心原则

1. Test/simulation data MUST 从 contract、schema、领域规则、真实案例或明确 evidence 派生；不得仅凭 LLM 想象业务事实。
2. **Scenario before records**：先设计风险、维度和 Scenario Matrix，再生成记录；不得直接以“生成 N 条 JSON”替代场景设计。
3. Golden Case MUST 有 expected behavior、关键 invariants、allowed variation、rationale、provenance 与 review state。
4. LLM 可以设计场景、发现语义边界、生成语言内容，但默认不得作为 Golden Oracle。
5. LLM 生成数据在成为正式 evidence 前 MUST 经 schema / rule / invariant 等独立验证。
6. Bulk synthetic data SHOULD 使用确定性或可重放 generator；记录 seed、generator version 和影响输出的 runtime/dependency identity。
7. 真实 bug / incident SHOULD 形成 minimal reproduction + regression case。
8. Hidden Validation 的 expected answer 不得暴露给实现 Agent。
9. **数据条数不是 coverage**。Coverage 必须映射到 contract、domain rule、boundary、risk、Critical Journey 或历史 regression。
10. 同一个 LLM 不得成为输入生成者、expected-answer 唯一来源和唯一审批者。

## 3. 数据资产分类

项目应按主要用途区分：

- **Fixture**：稳定的小型输入，支撑 unit / component / integration / contract test。
- **Scenario**：描述用户、系统状态、风险或失败条件的结构化案例。
- **Golden Case**：经规则、专家、人工或已确认真实案例授权的高价值基准。
- **Boundary Case**：最小/最大、空值、长度、精度、集合大小、状态边界等。
- **Schema-invalid Case**：结构、类型、enum、required field 等违反 contract/schema。
- **Domain-invalid Case**：结构合法但违反业务/domain rule。
- **Failure Injection Case**：dependency timeout/unavailable、partial result、permission denied、filesystem/DB failure 等运行故障。
- **Adversarial Case**：恶意输入、prompt injection、contradictory evidence、untrusted tool output 等。
- **Regression Case**：由已发生 bug / incident 派生并长期保留。
- **Critical Journey Dataset**：支撑端到端核心业务闭环。
- **Hidden Validation Dataset**：实现阶段不可依赖其具体答案的独立验证数据。
- **Load / Scale Dataset**：性能、容量、稳定性验证数据。

一个案例 MAY 有多个标签，但必须有一个主要用途。Schema-invalid、Domain-invalid 与 Failure Injection 不应被一个笼统 `failure` 类混为一谈。

## 4. 数据来源与 Provenance

### 4.1 来源优先级

优先使用最接近真实行为、同时满足安全和授权要求的来源：

1. 合法、已审查、允许测试使用的真实数据或生产派生统计特征；
2. 真实业务样本、历史工单、已确认 incident、人工审核案例；
3. 权威公开数据集、标准、规范或领域参考；
4. 项目 PRD、contract、schema、领域规则、Decision Model、accepted ADR；
5. 专家/产品/测试人员定义案例；
6. 基于上述来源由 generator 或 LLM 推导的 synthetic data。

较低优先级来源不得覆盖更高优先级已确认事实。

### 4.2 Source Catalog

正式 Test Data Pack SHOULD 为来源记录：

- source id / type；
- path / URL / dataset identity；
- version、retrieved date 或 frozen revision；
- license / usage restriction（外部来源适用时）；
- privacy classification；
- 来源用于哪些字段、规则、分布或 Golden 判断。

LLM 生成内容必须标记为 synthetic / LLM-derived，不能伪装成真实样本。

### 4.3 隐私与安全

Test data MUST NOT 包含真实 secret、token、password、private key。

除项目明确批准且具有合法处理依据外，不得把真实个人敏感数据、客户数据或 production dump 直接提交 repository。

“脱敏生产数据”与“synthetic data”必须区分；脱敏不自动等于不可重新识别。

## 5. 标准生成流程

```text
PRD / Contract / Schema / Rules / Incidents / Real Examples
        ↓
Source Catalog + Privacy / Usage Constraints
        ↓
Extract Rules / Invariants / Critical Decisions
        ↓
Scenario Dimensions + Risk Rationale
        ↓
Scenario Matrix
        ↓
Curated Golden / Boundary / Invalid / Failure / Adversarial Cases
        ↓
Deterministic / Property-based / Fuzz Generator
        ↓
Schema + Rule + Invariant Validation
        ↓
Coverage + Dedup + Reproducibility + Privacy Review
        ↓
Test / Hidden Validation / Regression Assets
        ↓
Feedback to Rules / Standard
```

如果关键 contract 或 expected behavior 是 `UNKNOWN`，生成过程必须 BLOCKED 或显式留下 unresolved item，不得由 LLM 自行补成业务规则。

## 6. Scenario Dimensions 与 Risk Matrix

### 6.1 Dimension 必须有意义

每个被计入 required coverage 的 dimension MUST 记录：

- values/range；
- why it matters；
- 对应 contract / rule / risk；
- 是否 required coverage。

**没有改变行为、风险或 contract coverage 的 inert dimension 不得用于制造 coverage 数字。** 若只是 exploratory distribution，应标记为 optional/exploratory。

典型维度：

- actor / role / permission；
- input completeness；
- numeric range / size / precision；
- enum / lifecycle state；
- locale / timezone / encoding；
- evidence quality / contradiction；
- dependency state；
- concurrency / ordering；
- AI ambiguity / insufficient evidence / prompt injection；
- historical regression class。

### 6.2 组合策略

不得默认生成所有笛卡尔积。优先：

- release blocker；
- contract boundary；
- historical fragile path；
- high-impact failure；
- pairwise/property-based 组合；
- Critical Journey；
- adversarial combinations。

未覆盖的重要组合或主动排除的组合 SHOULD 记录 rationale。

## 7. Golden Case 与 Expected Oracle

Golden Case 至少包括：

```text
id
intent / scenario
input
expected behavior / decision
required invariants
forbidden behavior
allowed variation
rationale
provenance
review status
```

### 7.1 Golden 选择必须风险驱动

Golden 数量没有跨项目统一最低值。Golden set SHOULD 锁定最高价值语义：关键 happy path、重要拒绝/升级决策、核心 contract 和历史高影响错误，而不是追求固定数量。

### 7.2 AI / LLM Output

优先验证：

- structured output schema；
- decision / classification；
- required facts；
- forbidden claims；
- invariants；
- evidence/citation correctness；
- rule/rubric score。

除非 exact text 本身就是 contract，SHOULD NOT 对自然语言全文做字符串 Golden。

### 7.3 Oracle Authority

Expected result 必须能回溯到以下至少一种 authority：

- deterministic rule / contract；
- approved real case；
- independent reviewer / domain expert；
- accepted evaluator/rubric。

LLM-only expected answer 不能自行升级为 `approved golden`。

## 8. LLM 生成模拟数据协议

LLM SHOULD 负责：

- 读取 frozen contract/rules/source catalog；
- 识别 scenario dimensions；
- 构建 Scenario Matrix；
- 发现语义边界和 adversarial cases；
- 生成需要自然语言、多语言、领域叙述的输入；
- 建议 properties/invariants；
- 在 validation 后分析 coverage gap。

LLM SHOULD NOT 默认负责：

- 无 evidence 的真实分布估计；
- Golden Oracle；
- 大规模 bulk random generation；
- 自己生成、自己判定、自己批准 Golden。

如果 LLM 直接参与生成，SHOULD 记录 model/provider、prompt/instruction revision、generation parameters 以及后续独立 validation。

通用生成提示词见 `prompts/TEST_DATA_GENERATION.md`。

## 9. Curated Data 与 Generated Data

高价值 Golden、Regression 和特殊 Boundary SHOULD 以 curated asset 保存；bulk / property-based / fuzz 数据 SHOULD 与 curated data 分开存储，或至少在 metadata 中可明确区分。

原因：

- curated case 是审计和语义资产；
- generated case 是覆盖输入空间的工具；
- 两者 review authority、生命周期和更新方式不同。

不得用大量生成记录稀释或替代 Golden/Regression 资产。

## 10. Boundary / Invalid / Failure / Adversarial

### 10.1 Boundary

从类型 + domain rule 同时推导，例如：

`min-1 / min / min+1`、`max-1 / max / max+1`、empty、null、missing、duplicate、very long、Unicode、timezone/daylight boundary、decimal precision、collection size。

只选择与当前 contract/domain 有关的边界，不要求机械覆盖所有通用边界。

### 10.2 Schema-invalid

Intentionally schema-invalid cases SHOULD 与 intended-valid cases 分开存储或明确隔离。

否则 schema validator 无法区分：

- “这是故意非法的测试输入”；
- “Test Data Pack 自己坏了”。

每个 schema-invalid case 必须声明 expected validation error / rejection behavior。

### 10.3 Domain-invalid

结构合法但业务无效，例如 unsupported currency、非法状态转换、negative lead time。Expected result 应指向 domain rule。

### 10.4 Failure Injection

描述运行故障机制，例如 timeout、dependency unavailable、partial response、DB conflict、permission denied。失败机制与业务输入应分开建模。

### 10.5 Adversarial / AI-specific

适用时至少考虑：

- prompt injection；
- contradictory evidence；
- insufficient evidence；
- hallucinated citation / tool output；
- ambiguous instruction；
- unsupported action；
- conflicting rules；
- untrusted Unicode/encoding trick。

## 11. Deterministic / Property-based / Fuzz Generation

### 11.1 Deterministic Reproducibility

需要随机性的 generator 至少记录：

- generator name + version/revision；
- seed；
- 会影响结果的 dependency/runtime version；
- locale/timezone/clock；
- frozen output hash（正式 pack 推荐）。

**Seed alone is insufficient.** Generator/library 数据或算法升级可能改变相同 seed 的输出，因此必须同时固定 generator/dependency identity，或冻结生成 artifact + hash。

### 11.2 Property-based / Fuzz

可以使用 property-based testing / fuzzing 扩大输入空间，但必须有 properties/invariants；不能只生成随机值。

自动发现失败后 SHOULD：

```text
Generated Failure
   ↓
Shrink / Minimal Reproduction
   ↓
Regression Case
   ↓
Required Test
```

## 12. Test Data Pack 推荐结构

```text
test-data-pack/
├── manifest.json|yaml
├── schema/ or contract refs
├── scenario_matrix.*
├── cases/
│   ├── curated.*
│   ├── generated.*
│   └── schema_invalid.*
├── golden/            # 可选：也可在 curated 中标记
├── regression/        # 可选：也可在 curated 中标记
├── generators/
├── coverage.*
└── VALIDATION_REPORT.md
```

具体格式可按项目调整，但必须保持稳定解析、可 diff、可审计。

### 12.1 Manifest 最小信息

正式 pack SHOULD 包含：

- pack id / format version；
- purpose / scope；
- privacy classification；
- schema/contract/rules references；
- provenance catalog；
- scenario taxonomy；
- required dimensions + rationale；
- generator identity / seed；
- case file mapping；
- coverage / validation report references。

## 13. Coverage 与防刷指标

不要用 record count 替代质量。

至少按适用范围审查：

- Scenario / Risk Coverage；
- Contract / Schema Coverage；
- Boundary Coverage；
- Domain Rule Coverage；
- Failure Coverage；
- Critical Journey Coverage；
- Regression Coverage；
- AI Adversarial / Semantic Coverage。

Coverage claim MUST 能从 risk/rule → case ids 反向追踪。

Duplicate / near-duplicate case 不得被计为独立风险 coverage。Generated cases 增加数量但没有覆盖新 rule/risk 时，不应提升质量结论。

## 14. Validation Gate

Test Data Pack 在成为 required evidence 前至少检查：

1. Pack integrity / parsability；
2. intended-valid input 通过目标 schema/type check；
3. intended-invalid input 确实违反目标 constraint；
4. expected behavior 与 rule/contract/oracle 一致；
5. provenance references 可解析；
6. Golden/Regression review authority 合法；
7. required dimension values 被覆盖或有明确 exception；
8. required risk matrix 无未解释 gap；
9. duplicate/near-duplicate 不造成虚假 coverage；
10. generator 能重放，或 frozen hash 与 artifact 一致；
11. secret/PII/privacy policy 通过；
12. Hidden expected answer 未泄露给实现侧。

状态使用 `PASS / FAIL / NOT_RUN / NOT_APPLICABLE / BLOCKED`。

通用检查清单见 `checklists/test-data-review.md`。

## 15. Hidden Validation

Hidden Validation SHOULD 与实现可见测试保持访问边界，例如独立 repository、受控 artifact、CI secret store 或其它权限隔离。

可以公开：

- pack schema；
- scenario taxonomy；
- required validation contract；

但不应公开会使实现 Agent 针对具体答案过拟合的 hidden input/expected mapping。

Hidden 数据仍必须遵守本标准的 provenance、privacy、reproducibility 与 review 要求。

## 16. Regression 演化

真实 bug / incident 修复后 SHOULD：

```text
Bug / Incident
   ↓
Minimal Reproduction
   ↓
Regression Fixture / Scenario
   ↓
Expected Contract / Invariant
   ↓
Required Test
```

若 regression 不再适用，删除前必须记录 contract/产品语义为何改变，不能因为实现难以通过而直接删除。

## 17. Scale / Distribution Data

当性能/容量目标依赖真实分布时：

- 不得让 LLM 无 evidence 猜测真实频率；
- 优先使用已批准的 aggregate statistics / public dataset / measured distribution；
- synthetic generator 应记录分布假设；
- benchmark 结果必须同时记录 dataset identity。

## 18. Feedback Loop：用数据反向验证标准

生成与验证 Test Data Pack 本身也是一次标准验证。

完成后 MUST 复盘：

- 是否存在 declared dimension 但没有 rule/risk 作用；
- schema-invalid / domain-invalid / failure 是否被错误合并；
- Golden 是否只覆盖 happy path 而遗漏关键风险语义；
- 是否只有 seed、没有 generator/dependency identity；
- coverage 是否可以通过复制相似记录刷高；
- expected answer 是否缺乏独立 authority；
- provenance/privacy metadata 是否不足；
- 是否发现 project contract 本身含糊、冲突或不可测试。

若发现跨项目通用问题，应反馈优化本标准；若是领域问题，应更新项目 contract/rules，而不是在测试数据中暗自创造新语义。

本仓库 reference pack 的实际反馈记录见 `examples/test-data-pack/quote-assessment/VALIDATION_REPORT.md`。

## 19. 禁止事项

- 用 LLM 幻觉出的业务事实作为 Golden truth。
- 没有 scenario/risk mapping 的大量随机记录宣称“覆盖充分”。
- 生成数据中包含真实 secret 或未经批准的 PII/customer data。
- 用同一个 LLM 生成输入、expected answer 并独立批准自己 PASS。
- 随机失败无法复现且不保存 seed/minimal reproduction。
- 直接复制 production dump 作为默认测试数据策略。
- Hidden Validation expected answer 暴露给实现 Agent。
- 只检查 schema，而不检查 domain rule 和关键 invariants。
- 为让实现通过而删除 Golden/Regression Case 或降低 expected invariant。
