# Test Data & Scenario Standard

## 1. 目标

本标准定义测试数据、模拟数据、场景、Golden Case、Regression Case、Hidden Validation Data 和规模数据的来源、构造、验证、存储与演化方式。

目标不是生成大量“像真的”数据，而是形成**可追溯、可复现、覆盖风险、能证明行为**的测试资产。

本标准与 `TESTING_STANDARD.md`、`VALIDATION_STANDARD.md` 配合：前者定义测试层级，本文件定义测试输入与场景，后者定义如何根据证据给出 PASS/FAIL/Release 判断。

## 2. 核心原则

1. 模拟数据 MUST 从 contract、schema、领域规则、真实案例或明确 evidence 派生，不得仅凭 LLM 想象。
2. Golden Case MUST 有明确 expected behavior、关键 invariants、rationale 与 provenance。
3. Normal、Boundary、Invalid、Failure、Adversarial、Regression MUST 按风险分开设计，不能只生成 happy path。
4. 大规模 synthetic data SHOULD 使用确定性 generator；随机性必须记录 seed，并记录 generator 版本。
5. LLM 可以设计场景、发现边界、生成语义内容，但默认不得作为 Golden Oracle。
6. LLM 生成数据在成为 test evidence 前 MUST 经 schema/rule/invariant 等确定性验证。
7. 真实缺陷 SHOULD 进入 regression asset，形成 Bug → Reproduction → Regression Case 的闭环。
8. Hidden Validation 的 expected answer 不得暴露给实现 Agent；公开测试与 hidden evidence 必须保持独立。

## 3. 测试数据资产分类

项目应按用途区分：

- **Fixture**：稳定的小型输入，支撑 unit/integration/contract tests。
- **Scenario**：描述用户、系统、风险或失败条件的结构化测试场景。
- **Golden Case**：经过规则/专家/人工审核的高价值基准案例。
- **Boundary Case**：最小/最大、空值、长度、精度、时间、集合大小等边界。
- **Invalid Case**：违反结构 contract 或业务 domain rule 的输入。
- **Failure Injection Case**：timeout、dependency unavailable、partial response、permission denied、corruption 等运行失败。
- **Adversarial Case**：恶意输入、prompt injection、contradictory evidence、untrusted tool output 等对抗性场景。
- **Regression Case**：由已发生 bug / incident 派生并长期保留。
- **Critical Journey Dataset**：支撑端到端核心业务闭环。
- **Hidden Validation Dataset**：实现阶段不可依赖具体答案的独立验证数据。
- **Load / Scale Dataset**：用于容量、性能、稳定性验证的数据。

一个案例可以具有多个标签，但必须有一个主要用途。

## 4. 数据来源与优先级

优先使用最接近真实行为、同时满足安全与授权要求的来源：

1. 合法、已脱敏且允许测试使用的真实数据或生产派生统计特征；
2. 真实业务样本、历史工单、已确认 incident、人工审核案例；
3. 权威公开数据集、标准、规范或领域参考；
4. 项目 contract、schema、PRD、领域规则、Decision Model；
5. 专家/产品/测试人员定义的案例；
6. 基于上述来源由 generator 或 LLM 推导的 synthetic data。

较低优先级来源不能覆盖更高优先级已确认事实。

### 4.1 Provenance

正式 test data pack SHOULD 为来源记录：

- source type；
- source identity / path / URL / dataset version；
- retrieved/frozen date；
- license / usage restriction（外部数据适用时）；
- privacy classification；
- 该来源用于哪些字段、规则或分布。

LLM 生成内容应标记 `source_type=synthetic/llm-derived`，不能伪装成真实样本。

## 5. 隐私与安全

测试数据 MUST NOT 包含真实 secret、token、password、private key。

除项目明确批准且具有合法处理依据外，不得把真实个人敏感数据、客户数据或生产 dump 直接放入 repository。

“脱敏生产数据”与“synthetic data”必须区分：脱敏并不自动意味着无法重新识别；项目需要按自身数据政策审查。

## 6. 场景建模流程

生成数据前先生成 Scenario Matrix，不得直接要求 LLM “生成 1000 条测试 JSON”。

推荐流程：

```text
PRD / Contract / Schema / Rules / Incidents / Real Examples
        ↓
Source Catalog + Data Constraints
        ↓
Scenario Dimensions + Risk Model
        ↓
Scenario Matrix
        ↓
Curated Golden / Boundary / Failure / Adversarial Cases
        ↓
Deterministic Generator / Property-based Generator
        ↓
Schema + Rule + Invariant Validation
        ↓
Coverage Review + Deduplication + Privacy Review
        ↓
Test / Hidden Validation / Regression Assets
```

## 7. Scenario Dimensions

Scenario Matrix 应从风险和行为出发定义维度，例如：

- actor / role / permission；
- input completeness；
- numeric range / size / precision；
- enum / state；
- locale / timezone / encoding；
- evidence quality / contradiction；
- dependency state；
- concurrency / ordering；
- AI-specific ambiguity / prompt injection / unsupported request；
- historical regression class。

不要盲目生成所有笛卡尔积。应优先：

- release blocker；
- contract boundary；
- historically fragile path；
- high-impact failure；
- pairwise/property-based 组合；
- Critical Journey。

## 8. Golden Case

Golden Case 至少包括：

```text
id
intent / scenario
input
expected behavior
required invariants
allowed variation
rationale
provenance
review status
```

对 LLM/AI 输出，优先验证：

- decision / classification；
- structured output schema；
- required facts；
- forbidden claims；
- invariants；
- rubric / evaluator score；
- citation/evidence correctness。

除非 contract 明确要求，SHOULD NOT 对自然语言全文做 exact string golden。

LLM 自己生成的 expected result 默认不能自行升级为 `approved golden`；至少需要确定性规则、独立 reviewer、领域专家或已确认真实案例之一进行校验。

## 9. Boundary / Invalid / Failure / Adversarial

### Boundary

从数据类型与业务规则共同推导，例如：`min-1 / min / min+1`、`max-1 / max / max+1`、empty、null、missing、duplicate、very long、Unicode、timezone boundary、decimal precision。

### Invalid

需要区分：

- structure/schema invalid；
- domain/business invalid。

预期应明确是 validation rejection、error object、HTTP status、domain decision 或其它 contract 行为。

### Failure Injection

模拟 dependency timeout/unavailable、partial result、filesystem error、DB conflict、permission denial 等。失败数据与失败机制要分开描述，避免把“错误输入”和“系统故障”混为一谈。

### Adversarial / AI-specific

AI 系统至少考虑：

- prompt injection；
- contradictory evidence；
- insufficient evidence；
- hallucinated citation/tool output；
- ambiguous instruction；
- unsupported action；
- conflicting rules；
- malicious Unicode / encoding tricks（适用时）。

## 10. LLM 在模拟数据生成中的职责

LLM SHOULD 优先承担：

- 从规则和历史问题识别 scenario dimensions；
- 生成 Scenario Matrix；
- 发现语义边界和对抗场景；
- 生成需要自然语言、多语言或领域叙述的输入；
- 建议 property/invariant。

LLM SHOULD NOT 默认承担：

- 无 evidence 的真实分布估计；
- Golden Oracle；
- 大规模 bulk random generation；
- 对自己生成的数据做唯一审核者。

Bulk generation 优先交给可版本化、可 seed、可重复执行的程序 generator。

如果 LLM 直接参与数据生成，SHOULD 记录 model/provider、prompt/instruction revision、generation parameters 和后续 deterministic validation。

## 11. 可重复性

需要随机性的 generator 至少记录：

- generator name/version；
- seed；
- dependency/runtime version（会影响结果时）；
- locale/timezone/clock；
- output hash（正式冻结 pack 推荐）。

相同 generator revision + seed + frozen dependencies SHOULD 能重建同一 dataset；若底层库升级会改变输出，应 pin 版本或将生成结果作为冻结 artifact。

## 12. 推荐目录

```text
tests/
├── fixtures/
├── scenarios/
│   ├── normal/
│   ├── boundary/
│   ├── invalid/
│   ├── failure/
│   └── adversarial/
├── golden/
├── regression/
├── generators/
└── testdata-manifest.*
```

Hidden Validation SHOULD 与实现可见测试隔离，例如独立仓库、受控 artifact 或独立目录/权限边界。

## 13. Test Data Pack 最小元数据

正式 pack SHOULD 包含：

- pack id / version；
- purpose / scope；
- schema/contract references；
- source/provenance catalog；
- scenario taxonomy；
- generator identity / seed；
- case files；
- Golden/Regression review state；
- coverage report；
- validation report；
- privacy/security classification。

JSON/YAML/JSONL 均可，但项目必须选择可稳定解析和 diff 的格式。

## 14. Coverage

不要用“数据条数”代替测试数据质量。

推荐至少审查：

- Scenario Coverage；
- Contract / Schema Coverage；
- Boundary Coverage；
- Failure Coverage；
- Domain Rule Coverage；
- Critical Journey Coverage；
- Regression Coverage；
- AI Adversarial / Semantic Coverage（适用时）。

项目可以使用 property-based testing 或 fuzzing 扩大输入空间；发现失败后应尽量保存最小复现样本并进入 regression。

## 15. Validation Gate

Test data pack 在成为正式验证 evidence 前至少检查：

1. Pack integrity / parsability；
2. schema / type validity（对 intended-valid cases）；
3. intended-invalid cases 确实违反目标约束；
4. expected behavior 与规则/contract 一致；
5. provenance references 可解析；
6. Golden/Regression review 状态合法；
7. scenario/risk coverage 无未解释缺口；
8. duplicate / near-duplicate 不造成虚假覆盖；
9. deterministic generator 可复现或 frozen artifact hash 已记录；
10. secret/PII/privacy review；
11. Hidden data 未泄露给实现侧。

状态使用 `PASS / FAIL / NOT_RUN / NOT_APPLICABLE / BLOCKED`。

## 16. Regression 演化

真实 bug/incident 修复后 SHOULD 执行：

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

若某 regression 不再适用，删除前必须说明 contract/产品语义为何改变，不能因为实现难以通过而直接删除。

## 17. 禁止事项

- 用 LLM 幻觉出的业务事实作为 Golden truth。
- 大量随机记录没有 scenario/risk mapping，却宣称“覆盖充分”。
- 生成数据中包含真实 secret/PII。
- 用同一个 LLM 生成输入、生成答案并独立判自己 PASS。
- 随机失败不能复现且不保存 seed/最小样本。
- 通过复制 production dump 解决测试数据问题。
- Hidden Validation expected answer 暴露给实现 Agent。
- 只检查 schema，而不检查 domain rule 和关键 invariants。
