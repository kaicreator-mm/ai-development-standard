# Product Exploration by Versioned Evidence — 探索实践参考（ADS v4.19 候选）

> **定位**：本参考描述如何组织多轮 Demo/实验以减少不确定性。规范所有权仍在 `standards/DEVELOPMENT_WORKFLOW.md` Stage 1、`prompts/L1_PRODUCT_EVIDENCE.md` 和 `standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md` Stage 2。此参考 **不新增 ADS 产品生命周期、审核门禁、Machine Schema、Task DAG 或独立发布权威**，其方法依照实际证据逐步修订。跟踪 [ADS #1361](https://github.com/kaicreator-mm/ai-development-standard/issues/1361)。

## 1. 适用范围：按需求启用

只有当 Product/Scope 的重要 UNKNOWN 无法用现有可信静态证据解决、需要多个可证伪实验、且实验产物会影响产品决定时，SHOULD 使用“一个探索索引 Issue + Git 版本化证据”的组织模式。

- **小而充分的已有研究**：仍在 L1 Evidence/已有 Product Issue 内联处理，记录 `NO_RESEARCH_REQUIRED` 的可靠依据，**不强制创建**索引 Issue/实验分支/PR。
- **多个相互关联的研究/回退**：优先复用已存在的 Product Issue 作主索引；如没有，创建 **一个**探索主 Issue，关联当前 Product 目标、假设、最小下一项证据和有界完成条件。
- **独立具体 Issue** 只在跨仓库/责任方、独立权限或写集、长期阻塞、并行验收、真实设备/外部副作用、高风险或适用 ADS 所有权本身要求时创建；**不要**因一个文件、一次失败或一次研究迭代自动开 Issue。
- **Stage 2 特例必须保留**：`standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md` 对 Architecture Research Demo 已要求 Research Demo Issue + 受隔离 research branch + E1/E2/E3 证据时，按原标准执行。本文“具体 Issue 可选”**仅适用于无更高要求的探索研究**；不得用单个主 Issue 绕过 Stage 2 的必需研究 Issue。
- **Product Research/Architecture Research 不可互换**：在 Product Freeze **前**，Stage 1 Demo 用于探明用户价值、范围/需求可行性、产品形态与验收假设；冻结后 Stage 2 Demo 才用于实际边界、架构不变量和可执行技术验证。Stage 2 若实证否定 Frozen 产品范围，应走既有 Thaw/Contradiction owner，而非修改旧验证结论。

## 2. 组织模型及权威

```text
Stage 0 intake → Stage 1 Product Evidence / Product Research (as needed)
                    │
              existing Product Issue OR one exploration index Issue
                    ├─ Product questions, observed UNKNOWN, priority, evidence index
                    ├─ study-01 r0 → r1 → decision / close
                    ├─ study-02 r0 → negative result → targeted change
                    └─ specific work Issue (only when warranted)
                    ↓
             Product decision recommendation + Owner disposition
                    ↓
             existing Draft PRD → selected Review → Product Freeze
                    ↓
             Stage 2 Architecture Research Demo (its own existing rules)
                    ↓
             L2 Freeze → Task DAG → Delivery-First #1359
```

| Source | 权威职责 | 反例/禁止 |
| --- | --- | --- |
| **Index Issue** | 链接 Product 问题、被检验的假设、每项研究的 exact evidence、总进度、未解决阻塞与可推翻条件、Owner 决策 | Issue 中复制第二份可编辑结果，或者拿 Issue 评论当测试执行收据 |
| **Git study contents** | 输入/真实或合成数据界限、协议、代码、正反例、执行收据、候选图/设计、失败记录、结论、复盘 | 只保留会移动的分支 ref、隐藏固定输入、改写过往 PASS/FAIL |
| **Git commit + blob + PR** | exact 产物身份、增量、审核与历史；必要时使用短期研究分支隔离 | 把「创建 branch/PR」当实验成功或发布 |
| **Specific Issue（按需）** | 独立实质工作、任务责任/权限、跨项目依赖和结果验收 | 每次 study r1/r2 都强制开新的 Issue |
| **Product Authority** | Product Research 的 `ADOPT/REVISE/CONTINUE/REJECT` 建议采纳/驳回，执行现有 Product Review/Freeze | Research PASS 自动 Product Freeze、PRD 认可或 L2 Freeze |

**版本语义**：`study-r0/r1/r2` 是实验候选修订，不是产品 `vX.Y.Z`，也不是 Release。实验每次有 `input Git SHA/blob`、`study revision`、`execution/receipt ref`；覆盖旧实验必须明确指向新继任版本，旧收据不删除。生产知识/源资料由原项目维持唯一可写事实，跨项目只引用带 exact pin 的只读输入，不复制维护一份新数据权威。

**Git 目录示例（可按项目现状采用，非标准硬路径）**：

```text
docs/product-exploration/<exploration-id>/
  INDEX.md                     # optional, derived from canonical index Issue
  studies/
    question-a/
      r0/manifest.yaml          # product question / origin / source exact SHA
      r0/protocol.md            # falsifiable prediction / positive-negative cases
      r0/run-receipt.json       # actual run or explicit NOT_RUN
      r0/findings.md            # evidence / gaps / what was NOT proven
      r1/...                    # only on a real revised study
  decisions/
    outcome.md                  # recommendation and owner decision ref (if any)
```

项目已有合适 `experiments/`、`demos/` 时 MUST **复用现有路径**，不要求迁移到此示例。`manifest.yaml` 是可读建议，不是 ADS 机器 Schema。一个小实验也可以只用一个 Markdown，达到同等证据即可。

## 3. 最小单次研究证据

每项**重要**实验在结论时至少能从 Issue/Git 恢复：

1. **Question/Decision relevance**：它解决哪一个 Product 未知、为何影响产品判断；声明一个可证伪的假设与成功/拒绝条件，并列出开放的反证。
2. **真实输入与来源权利**：数据来源、许可/隐私限制、输入确切 Git/URL/资料定位与 SHA/版本、变更/时效；声明是 `REAL | SYNTHETIC | MIXED`，模拟局部不得冒充真实生产验证。
3. **方法与范围**：运行程序/提示/样本选择、实际 Executor/环境/工具版本、预算和排除项、正/负/UNKNOWN/失败案例；样本有限时不得外推普遍正确。
4. **真实观察**：原始执行日志、exit code、可复核断言、结果与 exact ref；没有真实运行必须标 `NOT_RUN`，计划/脚本文件、单一 LLM 回答、两个 LLM 同意都不是实际验证收据。
5. **结论与限制**：`PASS | FAIL | PARTIAL | BLOCKED | NOT_RUN` 是**该实验的描述性结果**（不创造 ADS 新 Gate），附 What was proven / What was NOT proven、剩余 P0/P1、外部审核/许可证状态和下一项**最小**证据。
6. **历史与处理**：Base/Final commit/blob、研究 rX、修复理由、失效旧证据、新结果，必要的 Owner/Reviewer 独立判断记录。无 source/环境真实性时，不得把自审核或 PR 合并升级成验证 PASS。

**执行环境选择应由实验内容决定，不以工具的大版本制造无关门禁（DKE 实践增量）**：纯 Product 探索的领域文本、Element/CQ/SAP、数据一致性与证据检查，关注真实输入/实际执行/反例/Exact SHA，而不要求 Node 24、固定 Node 版本或特定 Host。可选择当前可用的任一**兼容**执行方式，并记录真实执行器、转换/适配器、已执行的内容以及未覆盖的 Node loader/原生差异；`script exists`、脚本死代码、未经执行的检查不能算 PASS。仅在验证目标自身包含 Node API/Runtime/CI 兼容性，或其他现行 Stage 2/发布门禁明确要求时，才把特定运行时及版本作为**该项技术验证**的变量；这不废止 ADS #1359 对实际工程/CI 的既有要求。变更脚本逻辑需针对变化部分重验，但**不得只因执行者使用另一 Node 版本而自动派发验证**。这一经验来自 [DKE #209](https://github.com/kaicreator-mm/domain-forge/issues/209) 的源码级别审计（曾发现 `expandImpact` 死代码）及后续 V8 有界回归，详见反馈 #1361；不将其升级为新机器 Gate。

**反例是必需的真实性控制**：假设若被推翻，应如实保留失败输入和反证，不允许通过删除失败样本、修改 preregistered 问题、反复调 prompt 到 PASS 而隐瞒试次；重大真实性/隐私/外部副作用风险按现有 ADS 门禁处理。

## 4. 主 Issue 的最小索引信息与停止决策

索引应简短、指向**唯一权威实际文件**：

```text
Product/Scope + target decision
Evidence index (Question | Study Revision | input SHA | result | proof link | remaining UNKNOWN)
Latest observations / earliest useful blocking evidence
Next smallest study & why it changes decision
Owner decision record (if made): ADOPT | REVISE | CONTINUE | REJECT
Related Product/Architecture/Task Issue refs
```

四项 Decision words 只是**建议用语**，不是 Workflow/Event/Task 新状态，也不是自动行为。一个实验 `PASS` 不代表产品 `ADOPT`：仍须判断用户价值、复杂度、替代方案、风险、运维成本与未解决假设；`REJECT` 也应保存失败经验。已足够支持当前决策时停止继续造工具/加测试；证据不足时 `CONTINUE` 并明确下一次实验如何缩减不确定性。

进度不得简单按实验/PR 数相加。建议同时记录 `hypotheses_resolved / hypotheses_in_scope`、关键 UNKNOWN 是否减少、失败假设数量、实际成本与迭代次数（**仅在真实测量时报告数值**），避免通过增加活动数量制造假进展。

## 5. 跨场景复用证据组织方法的边界（实践建议，不新增 Stage 2 权威）

“现有主 Issue + Git exact version evidence + 按需具体 Issue”是一种可在不同阶段**借鉴的证据组织方式**，但本标准提案的正式适用范围仍是 Stage 1 Product Exploration。另一个规范版本的 Conformance Demo 可以借鉴索引、Git 修订和证据依赖关系，**不能**因此规避其既有 Requirements/MUST、Stage 2 Architecture Research Demo 独立 Issue/分支/E1–E3、独立 Review、L2 Freeze、CI 或 Release Gate。研究结果、原生符合性与发布资格由各自 owner 决定。只因新的 Demo 修订、失败测试或改了文件，不自动创建 Issue、产品 SemVer 或 Frozen Task DAG；适用规范要求的具体 Issue 仍必须创建。

### 5.1 证据维度应区分，而非压成单一 PASS

按研究的重要性与实际适用范围，报告可分别注明下列**描述性维度**，并明确“已证明 / 未证明”；这不是新增强制填写的 ADS Schema、状态或额外审批门禁。

| 维度 | 所能证明 | 不得自动推导 |
| --- | --- | --- |
| 原始来源 / provenance | pinned source 与输入范围真实、可回读 | 原始来源足以赋予业务或语义判断的权威 |
| 语义 / 关系 / 反证 | 约束、关系、推导和 UNKNOWN 在特定样本内被检验 | 来源端点可信就代表派生关系被接受或能泛化 |
| 执行 / Consumer / native proof | 真实程序和所记录环境、正反例在确切版本运行 | Mock/结构 PASS 等于真实消费资格，或旧 SHA PASS 继承到新 HEAD |
| 独立判断 / authority | 相应 Reviewer/Owner 真实确认的确切范围与决定 | Source SHA、LLM 自评或 CI SUCCESS 自动变成 Claim、Effect、Freeze、Release |

- 同一 exact HEAD/TREE 的多个 CI context 要保留**逐项状态与 URL**。集成 FAIL、Node24 PASS、通用 verify PASS 只证明后两项通过，不能给整轮 PASS；无步骤日志只能标明失败原因 UNKNOWN，不能凭猜测将其归因为基础设施或代码。
- 不同版本引用历史 PASS 时只复用其原始 source/环境/范围事实；新合约、新原生入口、新 Evidence 义务或新版本要进行实际差异复核。失败、UNKNOWN、早期反例和失效回执不得被新报告覆盖。
- 负面测试必须断言预期的拒绝语义。Runner 自身崩溃、断言未运行或超时不算负例通过。修复最早的真实阻塞后，在同一 Writer/写集内重跑受影响范围；遵循 ADS #1359，不派发 validation-only 往返。

### 5.2 用反事实检查拆分颗粒度，避免证据形式主义

当 Element、知识关系或实验主题被分出单独范围，只承载一条边、一组 UNKNOWN 或单一薄包装时，可以在**同一 pinned 真实输入**上比较保留 Parent 与独立 Split。必须保持原有知识、关系、约束、来源、负例与未知覆盖；“owner map 完整”不是拆分合理性的充分条件。更少的 Element 数不是普遍 KPI，仍须证明独立语义责任。多个证据问题之间可画 Evidence-Question Dependency Map，用于确定最小下一项试验、可并行研究和前置证据；它**不是** Frozen Implementation Task DAG。

### 5.3 DIS v0.2.0 实际实践（限定的反例，不是通用效益证明）

[DomainHarness #1499](https://github.com/kaicreator-mm/domain-harness/issues/1499)复用现有版本主验证 Issue，Product/L1 由 [#1496](https://github.com/kaicreator-mm/domain-harness/issues/1496) 持有、Demo/Matrix/CI 在 [Draft PR #1497](https://github.com/kaicreator-mm/domain-harness/pull/1497) 的 Git 中追踪，未创建新的 Demo 主 Issue。R11 Exact HEAD 4632d5e0b331f0119da0c8d78249b7c1437856a1 / TREE 8f347807680db455cc8627590bc3c60778b9e953 的三个观测分别是 [DIS integration FAILURE](https://ci.kaicreator.com/repos/18/pipeline/2232/1)、[Node24 SUCCESS](https://ci.kaicreator.com/repos/18/pipeline/2232/2)、[generic verify SUCCESS](https://ci.kaicreator.com/repos/18/pipeline/2232/3)。当时 CORE-003 仍为 PARTIAL，R11 无新的成功收据；status-only 不能说明集成失败根因。该案例提示 Source Pin、typed outcome、尚未经独立校验的 Evidence 与真正的 KDP Effect 权威不可互相替代。

案例只证明**组织方式可用于第二种验证场景，尚不证明效率优势**。若节省的时间、审查负担、工具成本没有实测，标记 NOT_MEASURED。未来如需把跨阶段模式变为强制规范，须经独立 scope/owner 审核，不可依靠此候选参考静默改变 Stage 2 门禁。

## 6. 实践反馈与渐进修订（不追溯改写原证据）

**主入口**：[ADS #1361](https://github.com/kaicreator-mm/ai-development-standard/issues/1361)。后续 DKE/Tally/DomainHarness/Runx 等项目可在自身原始 Issue/PR 下保留完整资料，仅在 ADS issue 内记录 `project; exact source; hypothesis; outcome; limitation; process-cost(if measured); what can generalize; counterexample; proposed standard clause`。

- **采纳已有证据，而不是复制实验**：同一 exact blob/tree 的相同 Gate 不因被新 Issue 引用就重新跑；语义变化或目标不同必须说明差异并针对性复核。
- **归纳前先反例验证**：至少考虑一种不适用场景（低风险单问题无需索引、Stage 2 Demo 必须单独 Issue、真实设备测试失败、隐私不允许跨仓库复制）。
- **经验入 ADS 有边界**：实践反馈可以更新参考案例；新增强制规则/机器契约/权威变化需经原有 ADS Product/L2/Review/Release 流程正式处理。不能仅凭单例把样板升级为普遍必须。
- **Delivery-First**：进入实际 Builder/Reviewer/Repairer/Local/CI 执行时遵循 [ADS #1359](https://github.com/kaicreator-mm/ai-development-standard/issues/1359) 的单一 Writer、合并修复/验证和 PASS-to-Next；探索本身无权改写现有合法 Task DAG 或 Release 权威。

## 7. 实例：DKE R2 × Tally v2.1.1 的实际证据

- DKE R2 Draft [DomainForge PR #208](https://github.com/kaicreator-mm/domain-forge/pull/208)，DomainForge 问题 #207；Tally 原始实验 [#299](https://github.com/kaicreator-mm/tally/issues/299) 的知识图谱是唯一输入权威。
- [真实 Tally 图谱纵切 Demo 报告](https://github.com/kaicreator-mm/domain-forge/blob/product/dke-0.0.1-candidate-r1/docs/standards/dke/DKE-0.0.1/demos/tally-v2.1.1/REPORT.md) 提供可追溯数据：Tally exact commit `3e94685ca57a4b7258988826697af1c1c3a6b3c8`、806 非图根记录、6 条 Claim 的候选 Element 范围、S2/S3/S4 的人工引导回退记录、源验证和故障注入。
- **证据边界**：结构检查通过，但知识 Claim 全部待采纳、LLM 自主拆分与 Critic、DKE SAP 独立资格、DIS ECP/AOT 执行**均未证明**。这支持 `CONTINUE`（针对下一实验）而不是通用 `ADOPT`；不得因为例子存在就要求各项目也做相同数量的 Demo 或执行同样的知识图谱检查。
- 后续实践应记录 Issue 管理额外成本、审查差异和实际模型/人类工作量，才能判断这一探索方式是否比固定每实验新 Issue 更高效。

**当前条款姿态**：ADS v4.19 源码候选；不得从本参考或本次 PR 自动推导已冻结 Product/L2、全仓发布、Task DAG、GitHub 合并/main 采用或消费项目统一执行。
