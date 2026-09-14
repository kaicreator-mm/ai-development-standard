# Test Data & Scenario Standard

## 1. 目标

本标准定义测试/模拟数据、Scenario、Golden、Regression、Hidden Validation Data 与生成器的来源、构造、验证、存储和演化。

目标不是制造大量“像真的”记录，而是形成**可追溯、可复现、覆盖真实风险、能解释为何正确**的测试资产。

- `TESTING_STANDARD.md` 定义测试分层；
- 本文件定义测试输入/场景/数据资产；
- `VALIDATION_STANDARD.md` 定义如何根据证据判 PASS/FAIL/Release。

Reference implementation：`examples/test-data-pack/quote-assessment/`。

## 2. 硬原则

1. Data MUST 从 contract、schema、领域规则、真实案例或明确 evidence 派生；不得仅凭 LLM 想象业务事实。
2. **Scenario before records**：先建 Source Catalog、规则、风险维度和 Scenario Matrix，再生成记录。
3. Golden MUST 有 expected behavior、invariants、allowed variation、rationale、provenance 与 review authority。
4. LLM 可设计场景、发现边界和生成语义输入，但默认不是 Golden Oracle。
5. LLM 生成数据成为正式 evidence 前 MUST 经独立 schema/rule/invariant validation。
6. Bulk synthetic data SHOULD 使用可重放 generator；记录 seed、generator revision 及影响结果的 dependency/runtime identity。
7. Bug/incident SHOULD 沉淀为 minimal reproduction + Regression Case。
8. Hidden Validation expected mapping 不得暴露给实现 Agent。
9. Record count 不是 coverage；coverage 必须映射 contract、rule、risk、boundary、Critical Journey 或 regression。
10. 同一个 LLM 不得同时成为输入生成者、expected-answer 唯一来源和唯一审批者。

## 3. 数据资产分类

按主要用途区分：

- **Fixture**：稳定的小型测试输入。
- **Scenario**：用户/系统状态、风险或失败条件。
- **Golden Case**：经独立 authority 确认的高价值语义基准。
- **Boundary Case**：min/max/empty/null/precision/time/size/state boundary。
- **Schema-invalid Case**：违反结构/type/required/enum contract。
- **Domain-invalid Case**：结构合法但违反业务规则。
- **Incomplete / Uncertain Case**：结构和状态合法，但事实、身份、证据或条件不足；正确行为通常是 request/defer，而不是 reject。
- **Failure Injection Case**：真实运行故障，如 timeout、dependency unavailable、partial response、DB/filesystem/permission failure。
- **Adversarial Case**：prompt injection、contradictory/untrusted evidence、malicious input 等。
- **Regression Case**：由已发生 bug/incident 派生。
- **Critical Journey Dataset**：支撑端到端核心业务结果。
- **Hidden Validation Dataset**：实现阶段不可依赖具体答案的独立资产。
- **Load / Scale Dataset**：性能、容量、稳定性验证数据。

Schema-invalid、Domain-invalid、Incomplete/Uncertain 和 Failure Injection MUST NOT 被一个笼统 `failure` 类混为一谈。

不是每个 pack 都需要所有类别。无相关边界时应明确 `NOT_APPLICABLE + rationale`，不得为了勾清单伪造场景。

## 4. 来源与 Provenance

### 4.1 来源优先级

优先：

1. 合法、批准用于测试的真实/脱敏数据或生产派生统计；
2. 真实业务样本、工单、incident、人工审核案例；
3. 权威公开数据集/标准；
4. PRD、contract、schema、domain rule、Decision Model、accepted ADR；
5. 专家/产品/测试人员定义案例；
6. 基于上述来源由程序或 LLM 推导的 synthetic data。

低优先级来源不得覆盖高优先级已确认事实。

### 4.2 Source Catalog

正式 pack SHOULD 记录：source id/type、path/URL、version/frozen date、license/usage restriction、privacy classification，以及它支撑哪些字段/规则/分布/Golden。

LLM-derived 内容必须明确标记 synthetic/LLM-derived。

### 4.3 Privacy / Security

MUST NOT 包含真实 secret/token/password/private key。未经批准不得提交真实 PII、客户数据或 production dump。“脱敏”不自动等于不可重识别。

## 5. 标准生成流程

```text
PRD / Contract / Schema / Rules / Incidents / Real Examples
        ↓
Source Catalog + Privacy Constraints
        ↓
Rules / Invariants / Critical Decisions
        ↓
Scenario Dimensions + Risk Rationale
        ↓
Scenario Matrix
        ↓
Curated Golden / Boundary / Invalid / Incomplete / Adversarial Cases
        ↓
Deterministic / Property-based / Fuzz Generation
        ↓
Schema + Rule + Invariant Validation
        ↓
Coverage + Dedup + Reproducibility + Privacy Review
        ↓
Test / Hidden Validation / Regression Assets
        ↓
Feedback to Project Rules / Global Standard
```

若关键 contract/expected behavior 为 `UNKNOWN`，必须 BLOCKED 或显式 unresolved，不能让 LLM自行补成业务规则。

## 6. Scenario Dimensions / Risk Matrix

每个计入 required coverage 的 dimension MUST 记录：

- values/range；
- why it matters；
- 对应 contract/rule/risk；
- 是否 required。

没有改变行为、风险或 contract coverage 的 inert dimension 不得用于制造 coverage；可标为 exploratory。

典型维度：role/permission、completeness、numeric/size/precision、lifecycle state、locale/timezone、evidence quality、dependency state、concurrency/order、AI ambiguity/injection、historical regression。

不要默认生成完整 Cartesian product。优先 release blocker、contract boundary、历史脆弱路径、高影响风险、pairwise/property-based 组合、Critical Journey。主动排除的重要组合 SHOULD 记录 rationale。

## 7. Golden Case / Oracle Authority

Golden 至少包括：

```text
id
intent/scenario
input
expected decision/behavior
required invariants
forbidden behavior
allowed variation
rationale
provenance
review status/authority
```

Golden 选择按风险驱动，不设跨项目统一最低数量。应锁定关键 happy path、拒绝/升级决策、核心 contract 与高影响 regression。

AI/LLM 输出优先验证 structured schema、decision、required facts、forbidden claims、invariants、evidence/citation correctness、rubric score。除非 exact text 本身是 contract，不应对自然语言全文 exact-match。

Expected result MUST 回溯到至少一种 authority：deterministic rule/contract、approved real case、independent reviewer/domain expert、accepted evaluator/rubric。LLM-only expected 不能自行成为 approved Golden。

## 8. LLM 生成协议

LLM SHOULD：读取 frozen sources；识别维度/风险；构建 Scenario Matrix；发现语义/对抗边界；生成自然语言/多语言输入；建议 property/invariant；在验证后分析 coverage gap。

LLM SHOULD NOT：无 evidence 猜真实分布；作为 Golden Oracle；承担大规模 bulk random generation；自己生成、自己判定、自己批准。

直接使用 LLM 生成时 SHOULD 记录 model/provider、prompt/instruction revision、generation parameters 与后续 deterministic validation。

通用提示词：`prompts/TEST_DATA_GENERATION.md`。

## 9. Curated vs Generated

高价值 Golden、Regression、特殊 Boundary SHOULD 保存为 curated asset。Bulk/property/fuzz 数据 SHOULD 与 curated data 分开或可明确区分。

Curated 是审计/语义资产；Generated 是探索输入空间的工具。大量 generated records 不得稀释或替代 Golden/Regression。

## 10. 特殊场景规则

### 10.1 Boundary

从类型 + domain rule 推导，例如 `min-1/min/min+1`、`max-1/max/max+1`、empty/null/missing/duplicate、Unicode、timezone/DST、precision、collection size。只覆盖适用边界。

### 10.2 Schema-invalid

SHOULD 与 intended-valid data 分开存储或明确隔离；每个 case 声明 expected validation rejection。否则 validator 无法区分“故意非法”与“pack 自己坏了”。

### 10.3 Domain-invalid

结构合法但业务无效，expected 必须指向 domain rule。

### 10.4 Incomplete / Uncertain

用于 missing fact、unknown identity/state、insufficient evidence 等**合法但信息不足**的情况。Expected 通常是 request more information、defer、low-confidence 或明确无法判断，不应误标为 runtime failure。

### 10.5 Failure Injection

仅表示运行/依赖故障：timeout、unavailable、partial external result、DB conflict、filesystem error、permission denial 等。失败机制与业务输入要分开建模。

### 10.6 Adversarial / AI-specific

适用时覆盖 prompt injection、contradictory/insufficient/untrusted evidence、hallucinated citation/tool output、ambiguous instruction、unsupported action、conflicting rules、encoding tricks。

## 11. Reproducibility / Property-based / Fuzz

需要随机性的 generator 至少记录：generator name+revision、seed、影响结果的 dependency/runtime、locale/timezone/clock，以及正式冻结时的 output hash。

**Seed alone is insufficient**：库数据/算法升级可能改变同 seed 输出，因此还需 pin generator/dependency 或冻结 artifact+hash。

Property-based/fuzz 必须有 property/invariant，而不是只生成随机值。发现失败后 SHOULD shrink/minimize 并进入 Regression：

```text
Generated Failure → Minimal Reproduction → Regression Case → Required Test
```

## 12. Test Data Pack

推荐：

```text
pack/
├── manifest.json|yaml
├── schema/contract/rule refs
├── scenario_matrix.*
├── cases/
│   ├── curated.*
│   ├── generated.*
│   └── schema_invalid.*
├── generators/
├── coverage.*
└── VALIDATION_REPORT.md
```

Manifest SHOULD 包含 pack id/version、purpose/scope、privacy classification、schema/rules refs、provenance、taxonomy、required dimensions+rationale、generator identity/seed、file mapping、coverage/validation references。

模板：`templates/test-data-pack.md`。

## 13. Coverage / 防刷指标

至少按适用范围审查：Scenario/Risk、Contract/Schema、Boundary、Domain Rule、Incomplete/Uncertain、Failure、Critical Journey、Regression、AI Adversarial/Semantic Coverage。

Coverage MUST 能从 rule/risk → case IDs 反向追踪。Duplicate/near-duplicate 不得算独立风险 coverage；增加相似 synthetic records 不应提高质量结论。

## 14. Validation Gate

正式 pack 成为 required evidence 前至少检查：

1. integrity/parsability；
2. intended-valid 通过 schema/type；
3. intended-invalid 确实违反目标 constraint；
4. expected 与 rule/contract/oracle 一致；
5. provenance 可解析；
6. Golden/Regression authority 合法；
7. required dimension values 覆盖或有 exception；
8. required risk matrix 无未解释 gap；
9. duplicate/near-duplicate 不虚增 coverage；
10. generator 可重放或 frozen hash 一致；
11. secret/PII/privacy policy 通过；
12. Hidden expected mapping 未泄露。

状态：`PASS / FAIL / NOT_RUN / NOT_APPLICABLE / BLOCKED`。

Checklist：`checklists/test-data-review.md`。

## 15. Hidden Validation

Hidden data SHOULD 与实现可见测试保持权限/存储边界。可以公开 pack schema、taxonomy、validation contract，但不公开会让实现 Agent 针对具体答案过拟合的 input/expected mapping。

Hidden data 同样必须满足 provenance、privacy、reproducibility 与 review authority。

## 16. Regression 演化

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

删除 regression 前必须说明 contract/产品语义为何改变，不能因为当前实现过不了就删除。

## 17. Scale / Distribution

当性能/容量测试声称代表真实分布时，不得让 LLM 无 evidence 猜频率。优先 approved aggregate statistics/public dataset/measured distribution；synthetic generator 记录分布假设；benchmark 记录 dataset identity。

## 18. Feedback Loop：数据反向验证标准

生成/验证 pack 后 MUST 复盘：

- declared dimension 是否真正影响 rule/risk；
- schema-invalid/domain-invalid/incomplete/failure 是否分类正确；
- Golden 是否遗漏关键风险语义；
- 是否只有 seed 而没有 generator/dependency identity；
- coverage 是否能被复制相似记录刷高；
- expected 是否缺独立 authority；
- provenance/privacy 是否不足；
- 是否发现项目 contract 本身含糊、冲突或不可测试；
- 某类风险是否实际上 `NOT_APPLICABLE`，而不是必须虚构场景。

跨项目问题反馈本标准；领域问题更新项目 contract/rules，不能在数据中暗自创造新语义。

本仓库实际反馈记录：`examples/test-data-pack/quote-assessment/VALIDATION_REPORT.md`。

## 19. 禁止事项

- LLM 幻觉业务事实作为 Golden truth。
- 大量无 risk mapping 随机记录宣称覆盖充分。
- 真实 secret 或未经批准 PII/customer data。
- 同一 LLM 生成输入+expected 并独立批准自身 PASS。
- 随机失败不可复现且不保存 seed/minimal case。
- 默认复制 production dump。
- Hidden expected answer 暴露给实现 Agent。
- 只查 schema 不查 domain/invariant。
- 为实现通过删除 Golden/Regression 或降低 invariant。
- 为满足 checklist 伪造本项目不适用的场景；应使用 `NOT_APPLICABLE + rationale`。
