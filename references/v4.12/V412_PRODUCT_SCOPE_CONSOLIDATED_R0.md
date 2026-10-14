# ADS v4.12 — Consolidated Product Scope / 统一产品范围说明 R0

> **状态：PRODUCT INTAKE / NON-NORMATIVE / PRD_NOT_FROZEN / L2_NOT_FROZEN / IMPLEMENTATION_DAG_NOT_FROZEN。** 已有首版决策：[`V412_INITIAL_POLICY_DECISIONS_V01.md`](V412_INITIAL_POLICY_DECISIONS_V01.md)，后续 L2 负责最小实现投影。 此文件是 #1096、#1099、#1100 和 PR #1101 中已讨论方向的**阅读入口**，不是另一份 Product authority，不取代原 Issue 的证据、Review/Validation、具体 owner 或 Frozen 文档。事实源以固定版本和被批准的 GitHub 权威为准；文中“确定”表示用户认可的 **v4.12 Product direction**，不表示标准已生效。
>
> Parent intake [#1096](https://github.com/kaicreator-mm/ai-development-standard/issues/1096) · ROI principle [#1099](https://github.com/kaicreator-mm/ai-development-standard/issues/1099) · Three-DAG intake [#1100](https://github.com/kaicreator-mm/ai-development-standard/issues/1100) · Cross-stage contract Draft [PR #1101](https://github.com/kaicreator-mm/ai-development-standard/pull/1101).

## 1. 唯一产品目标

把 ADS 从较固定的阶段流程，发展成 **风险约束、证据充分、复用优先、成本可控的自适应 AI 工程体系**。根据真实问题、架构未知、当前证据、Task 原子性、多 Agent 写集、环境约束、实际价值和总执行成本，选择最小**合法**开发路径；持续完成阶段收敛、真实实现、当前证据、Release 和改进复用。

**四项不可混淆：**
1. `L1/L2/L3` = Product/Architecture/Implementation **证据和权威语义**；`DAG-P/DAG-A/Implementation Task DAG` = **执行组织视图**，不是三个新增审批机关。
2. Scaffold = 真实工程结构/契约/测试基线，不是实现业务功能或 Release PASS；和 **Implementation Task DAG Draft** 协同完善，然后配对冻结。
3. Evidence `INFORMS/CONSUMES` ≠ native `BLOCKED_BY`；一个逻辑 Work Graph 不等于新的图服务/Claim DB。
4. 高风险强制义务不能被 FAST、低 ROI、多个 LLM 赞成、模型评分、Review/Task PASS 或低 Adoption level 降低。

## 2. 五大 Workstream（工作流，不是必须拆出的五个服务或五个 Task）

| W | 内容 | 主要交付效果 |
|---|---|---|
| **W1 Adaptive Work Graph** | 三阶段图、按阶段选择 INLINE/WORKLIST/EXPLICIT、Product/L2/Implementation handoff、脚手架双向映射、Task DAG/JIT/安全拆分、阶段收敛 | 面向实施的可靠计划、合理依赖与并行 |
| **W2 Project Steward** | read-only 状态/漂移/阻塞观察、关键路径、Claim liveness、Review 分歧/重复循环、Merge-drain、Controller 合法动作与回读 | 尽快推进真正阻塞和可合并工作；不生成新权威 |
| **W3 Environment Lifecycle** | WEB/LOCAL/Build/CI/E3/真实设备能力、合法资源预检/分配/隔离/执行/回收、日志退出码与证据 | 减少虚假环境 PASS、重复 Host 运行与清理泄漏 |
| **W4 Task Outcome & Learning** | 逻辑 `Task Result + Task Metadata`、exact subject、成本/Review/等待/失败根因反馈、负知识/合法后续复用 | 更优 Task 划分、调度、验证与长期学习，不自修改规范 |
| **W5 Research/Reuse/Engineering Quality** | L1 竞品/社区用户证据、L2 静态研究/技术 Demo、现有代码/组件/工具复用、许可证、Builder 质量、契约/测试复用 | 减少重复研究和重复造轮子，提升维护与实际交付质量 |

横切原则 [#1099](https://github.com/kaicreator-mm/ai-development-standard/issues/1099)：**Risk-Bounded Value First**。对可选非核心工作采用 `DO_MINIMAL/REUSE/BATCH/TIMEBOX/DEFER/EXCLUDE`，须有真实理由、Owner 与必要触发条件；**不能回溯豁免已冻结 REQUIRED_NOW、权限、安全、数据完整性、外部不可逆行为、明确产品承诺**。

## 3. 新的版本开发链（保留已有 authority）

```text
Idea/Intake
 → L1 Product Evidence + DAG-P (按需)
    已有可信资料/合法公开行为证据优先；必要人工实证/权威裁决
 → Draft PRD → selected Product Review → explicit Product Freeze
 → L2 Architecture Evidence + DAG-A (按需)
    Architecture UNKNOWN、复用决策、边界/不变量、必要真实 Demo
 → explicit L2 Architecture Freeze
 → v4.12 规划阶段明确允许的 NEW_PROJECT_INIT / Scaffold 创建（已有源/权限边界）
 → 项目 Scaffold S0 ↔ Draft Implementation DAG D0
    同步细化至 SF ↔ DF，按需编译/契约/入口/负例 smoke
 → 配对检查并记录 Scaffold SF exact merged SHA/Tree + DAG DF checkpoint
 → Scaffold Baseline accepted + Implementation Task DAG Freeze
 → native GitHub Issue Dependencies + accepted Dispatch/Claim/JIT + L3 per Task
 → 实现/PR/关注点测试与选定独立 Review → 原子/集成/版本验证
 → Candidate Freeze → required Hidden/Closeout/RQ → Repository Integration → Tag
```

**注意:** 对**从零新项目**，v4.12 的 Scaffold 生成是合法的 **Planning 阶段工程产物创建**，不是修改已冻结实现，不增设 Bootstrap 审批 Gate；其范围和真正 Feature 实施权限必须区分。需将阶段许可接入正式 v4.12 Development Workflow 与现有 GitHub/Writer 规则才能生效。现行 v4.11 旧 pin 项目维持其合法 Task DAG/T00 先行流程。详见 [首版决策 §D01](V412_INITIAL_POLICY_DECISIONS_V01.md#d01--bootstrap-是从零生成规划阶段完善项目骨架不是对已有冻结实现的非法修改)。

### 3.1 三个阶段图

| 视图 | 关联语义 | 启用条件 | 何时退出 |
|---|---|---|---|
| `DAG-P` | L1 Product Evidence、Product Research、PRD unknowns | 多个真实依赖/研究者/真实研究对象；简单可 INLINE/BOUNDED_WORKLIST | 研究证据支持 Product owner 做出合法范围决定；Product Freeze 另有明示权威 |
| `DAG-A` | L2 Architecture Evidence、设计/契约/研究 Demo | 多个材料未知项与真实相互依赖；简单只需 Design Note/已有证据 | 高影响 UNKNOWN 足额处置、合法 L2 Architecture Freeze |
| `Implementation Task DAG` | Product+L2 冻结后的实际实施任务规划；L3 按 Task 准备 | 实质性的多 Concern 版本；小型合法 Fast Path 可简化 | **与 Scaffold SF 一起配对冻结**，再 materialize 实施 Issues 并 JIT 实现 |

图的大小和审查强度**按阶段/按 Concern 独立决策**。EXPLORATORY（未知强度）与 HIGH_ASSURANCE（结果风险）互不排斥；不能把高风险当成“三个 DAG 都要重型”的理由。

## 4. Scaffold ↔ Implementation DAG 共演进与双向映射（用户选择的产品方向）

**Scaffold 的“完成”= 工程基线可供 Task 开发**，不是功能、E3/真实 Host、Hidden、Release 完成。**详细程度随实际项目变化**：已成熟项目尽量复用；新多模块项目建立必要 package/module/types/API/tool-call/contracts/config/build/test/import/export；高风险项目确保必要边界、失败契约及测试入口。Stub/NotImplemented 显式声明未实现。

**一个真实合法 Bootstrap writer（或合法互斥受控写集）**逐次完善 S0/S1/SF；Draft DAG 逐次完善 D0/D1/DF。不要在规划时偷做正式业务实现。每次新增 Task 问：需要哪条已存在或计划存在的接口/模块能力边界？由谁实现，写集是什么，谁消费、谁测试？需要新增脚手架基础契约吗？是否真的值得现在新增？

**双向关系是 typed many-to-many，而非一文件/一接口/一 Task：**

| 方向 | 最小可用追溯 |
|---|---|
| Task → Scaffold | 负责创建/实现/修改的契约/模块/未来 seam；只读消费的 API；对应测试；写集及明确禁止事项 |
| Scaffold → Task | Public/Shared seam 的权威编辑 owner；实现者、消费者、集成者与验证者；future/未实现能力与责任 Task |

候选映射关系 `IMPLEMENTS/CREATES/MODIFIES/CONSUMES/TESTS/INTEGRATES`。共享 API 可有六个消费者，但不能因此产生六个互相冲突的写入 owner；源码 `import` 关系不能自动成为 GitHub native `blocked_by` 边。允许存在没有代码锚点的测试/审查 Task，以及不需要独立 feature Task 的生成/Bootstrap-only 文件。

**配对 Freeze 的最小身份元组：**

```text
Frozen Product ref + Frozen L2 ref
+ integrated Scaffold source SHA/tree
+ frozen Implementation Task DAG checkpoint/revision
+ mapping projection/ref and currentness
+ material contract ownership / known future unimplemented seams
+ relevant tested compile/import/build/contract smoke and NOT_RUN limitations
```

一致性检查重点：Material Task 必须可追溯；关键公共契约有 owner+消费者；写集不会假并行；接口/验收一致；未实现 Stub 没被当成功能 PASS；映射与源码/DAG 引用同一有效基线。**不是全符号静态映射，也不另建第三套事实源**。

## 5. Task 的角色与变化治理

**一个 Task = 一个可独立审查/集成的 coherent concern/invariant**，不是强制一接口/一文件一 Task。常见 Contract → Core/Adapter/Workflow/UI → Central Integration → focused concern validation（真正依赖才建 blocked-by）。共享契约尽量先稳定，共享 wiring 有单独合法 owner；特别大的原子安全 concern 可以不拆。

- 正常内部实现/私有 seam 更新 → 相应 Task Pack/currentness + focused tests，按风险选 Review。
- 共享公开 API/Schema/事件、持久化语义、跨模块契约变化 → L2/兼容性 owner 的合法 amendment、受影响 Task/验证定向重评。
- 产品承诺/验收行为变更 → Product thaw/amendment。
- 安全、权限、数据完整性、不可逆外部效应、敏感迁移 → HIGH_ASSURANCE 对应硬证据 + 所需 Authority，**HIGH_ASSURANCE 本身不是变更许可**。
- ACTIVE Task 发现过大/冲突 → 先核对 accepted Claims、写集、已合并代码，走合法 SPLIT/SUPERSEDE/取消/恢复，不偷 Claim、不重做已证实节点。

## 6. 真人成本和 L1 实证（C13/C14）

**判断权：** 当且仅当当前规则允许，采用可选多 LLM 对抗质疑 → 确定性工具验证 → 最小必要真人权威/审核；可以跳过无额外价值的步骤。模型协商、模型数量/多数票不是 Product Freeze、真实独立 Reviewer、法律授权或人类 DENY。

**真实行为证据：** 先查已合法持有的研究/遥测、许可数据集、平台允许的论坛/社区/Issue/产品评价等真实历史资料；确定性治理后再用 AI 提取模式并找反例。论坛帖通常证明“有人这么描述”，不是“目标人群占比”或“新 UX 任务完成率”。机器人、样本偏差、时间、来源、平台 Terms、版权、个人数据许可与模型上传限制必须诚实处理。

证据不足以回答确切 Product UNKNOWN、需要真实行为实验、独立真人盲标 Gold、知情同意/审批时，保留最小 **有效** 真人工作或经合法 Product/Study 方法变更后收缩承诺。禁止用 AI 候选标签+真人随手确认冒充独立真人编写 Gold。

## 7. Project Steward、环境、经验：坚持“观察与合法动作分离”

- **Steward** 读 canonical GitHub/source/证据、识别 READY→CLAIM 停滞、资源与 Claim 冲突、Review 负反馈反复、重要 Merge 老化及版本关键路径；写 **可追溯建议**，由已有 Controller/Product/L2/Human/Gate Owner 执行；再读回确认。其建议/新开辅助 Issue 不能自然变成阻塞。
- **Environment Lifecycle** 记录真实能力/隔离/预检/资源/执行/回收，不能把假环境的编译测试冒充真实环境 E3。Claim 依旧走现有互斥/原子 admission。
- **Task Result + Metadata** 可在原 Task/Issue/checkpoint 中表达；仅有 material learning 时保留 source-bound lessons/causes/cost/negative knowledge，供以后同属类比学习，不自动改 ADS、授予 PASS 或扩大人审。
- **整体收敛** 采用局部失败归因、最小必要负例、条件匹配的已有证据复用、Merge-first on valid proofs 和有界 Review/Host 迭代；PR PASS、Task PASS、version Closure/Release PASS 是不同主体。

## 8. 现有候选契约索引（15 组 ≠ 15 个独立新服务/实施 Task）

| C | 内容 | 主要 W |
|---|---|---|
| C01 | 三阶段图与阶段边界 | W1 |
| C02 | 分阶段自适应执行深度 | W1/W4 |
| C03 | 节点、证据边与任务依赖区分 | W1/W2 |
| C04 | 阶段完成/证据转交、负例真实性 | W1/W5 |
| C05 | 变更后局部 currentness / invalidation | W1/W5 |
| C06 | Product/L2/Task/Claim/Gate 决策权和争议 | W1/W2 |
| C07 | Steward 观察→合法干预→读回 | W2 |
| C08 | 阶段预算、停止规则、重复工作抑制 | W1–W5 |
| C09 | 环境能力、资源、隐私真实性 | W3 |
| C10 | Task Result、Metadata 和学习边界 | W4 |
| C11 | 项目版本采用、恢复和历史兼容 | W1–W3 |
| C12 | Task 与版本 Release 的收敛边界 | W1/W2/W4 |
| C13 | AI 工具优先、最小真人判断权 | W1/W2/W4/W5 |
| C14 | 公开/许可人类历史证据优先 | W1/W4/W5 |
| C15 | Bootstrap/Scaffold ↔ Draft Implementation DAG、配对冻结、双向多对多映射 | W1/W3/W5 |

全文和作者静态对抗审查保留在 PR #1101 的 `V412_CROSS_STAGE_CONTRACTS_CANDIDATE.md` / `V412_ADVERSARIAL_REVIEW_R0.md`。本文件避免重写所有详细验收/反例。

## 9. 产品方向与未决设计 — 必须分清

| 状态 | 内容 |
|---|---|
| **已明确 Product 方向（待正式 PRD Freeze）** | 五大 Workstreams、Risk-Bounded Value First、三阶段图可选、L1/2 证据与权威分离、最低成本/人类证据法、Scaffold+DAG 共演进与配对 Freeze、双向多对多映射、动态按风险治理与 Task Learning |
| **已确定的 Bootstrap Product 规则** | L2 后 **NEW_PROJECT_INIT** 规划阶段可创建 Scaffold，无额外 Gate；限制工程/契约骨架而非业务功能实施；已有项目只增量适配，正式 v4.12 接线后前瞻生效 |
| **已选首版 Product 默认规则** | DAG-P/DAG-A 按需 INLINE/WORKLIST/EXPLICIT；风险与未知正交、Owner 权威优先；多模型/工具替代不需要的真人程序；已有许可真人数据优先；旧项目不强制迁移。以真实项目案例优化，不再要求先推出新一轮独立研究项目 |
| **L2 待实现/投影** | GitHub anchor + DAG scaffold_bindings → 生成只读双向 map、V01–V12；Scaffold subtree/tree 与 DAG checkpoint 配对；规划阶段写入范围的最小治理接线；现有 Steward/Env/Claim/Review 的 owner 复用与验证。不是新的 Product 权限悬案 |
| **需要已有 owner 证实的内容** | v4.11 已完成的 Claim/Assurance/Task Learning/Review/CI 等，先查 exact source + tests + Case，证实 ALREADY_IMPLEMENTED/DELTA/DEFER，不能因为有旧 Issue 就当作新缺口 |

**明确不做：** 第二个规范权威/状态库/Claim 生命周期/发布决策者；所有项目强制三张 DAG、每个接口一个 Task、每个 PR 三模型对抗审核/真人参与；所有源码变更 HIGH_ASSURANCE；脚手架通过代替功能验证；公开帖子自动等于合法真实人 Gold；用无新断言的测试/Research Demo 铺满 Issue。

## 10. 推荐收敛顺序与可验收示例

1. **现在（L1）**：对照已有 owner 做 bounded-gap disposition `ALREADY_SATISFIED | PARTIAL_DELTA | NET_NEW | L2_ONLY | DEFER`；用一个真正新项目和一个既有项目反例检查 ROI 与方法；把本 Summary 精炼成 Product requirements/acceptance，不立刻拆成 15 个 implementation Issues。
2. **PRD**：采纳 [v0.1 首版决策](V412_INITIAL_POLICY_DECISIONS_V01.md)（规划阶段新项目生成合法、GitHub 映射、已有项目首版策略），界定 Hard Floor 和实证权威，进行适用的 Product Review 后由 Product Authority 显式冻结。
3. **L2**：把已确认的规划阶段 Scaffold 创建规则**接入现有 DEVELOPMENT_WORKFLOW 与 GitHub writer/Work Item**；实现最小 map 生成/验证约定（不重复事实源）；其余 Steward/Env/Task Learning 只补真实差距。
4. **Implementation DAG**：按真实可实现的 concern/PR 组织，先建立合法 Bootstrap，协同规划至 paired Freeze；后续 JIT Task Packs/Claims 实施，必要时合法拆分、单一集成 owner。
5. **Closure**：按现有 exact-source mandatory gates，核对 Release Owner × subject applicability，直到一份真正稳定版本候选可被 RQ 和 Release owner 合法接受。

**负例最少包含：** 非法 pre-DAG 源码写入必须拒绝；编译通过 Stub 不得算功能完成；多 Agent 同一共享文件冲突；Task↔Scaffold 映射错位时拒绝 paired Freeze；社区发帖不能证明人口比例；模型多数票不能代替人类批准/人类盲标；旧候选 required gate 不能因 ROI 而取消；局部 Task PASS 不等于 Release PASS；重复 Host 运行若不新增证明应停止但必需安全负例不得跳过。

## 11. Current status

```ini
VERSION=v4.12.0
PHASE=PRODUCT_INTAKE
PRODUCT_DIRECTION=RECORDED_IN_ISSUES_AND_DRAFT_PR
CANDIDATE_CROSS_STAGE_CONTRACTS=C01-C15_PROPOSED_NOT_NORMATIVE
AUTHOR_LED_ADVERSARIAL_REVIEW=DOCUMENTED_NON_INDEPENDENT
INDEPENDENT_PRODUCT_REVIEW=NOT_RUN
PRD_FREEZE=NO
L2_FREEZE=NO
PLANNING_SCAFFOLD_CREATE=PRODUCT_DIRECTION_DECIDED_NOT_YET_NORMATIVE
GITHUB_BIDIRECTIONAL_MAPPING=V01_CONTRACT_DEFINED_IMPLEMENTATION_NOT_RUN
OTHER_MECHANISMS=V01_DEFAULTS_SELECTED_WITH_PROJECT_EVIDENCE
IMPLEMENTATION_TASK_DAG=NOT_CREATED
MACHINE_CONFORMANCE=NOT_RUN
RELEASE_AUTHORITY=NO
V411_FROZEN_CONTRACT_MUTATION=NONE
```

**此 summary 的完成不代表 PRD 或任何 Gate PASS。** 每个新增合规/验证要求都必须先证明独立决策价值与实际 Owner；已有完整实现/证据不得重新造轮子。
