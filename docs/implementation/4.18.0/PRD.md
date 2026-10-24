# ADS v4.18.0 — Product Requirements Document R1

> **STATUS:** PRODUCT_DRAFT_R1 / AUTHOR_P1_P2_REPAIR / INDEPENDENT_R2_PENDING / NOT_FROZEN / NOT_NORMATIVE / NO_IMPLEMENTATION_AUTHORITY  
> **VERSION:** v4.18.0 (prospective)  
> **SOURCE BRANCH:** version/v4.18  
> **BASELINE:** ADS v4.17.0 `main@a45644d734fdf94da3e6f9c3f90ffe4ce3c25fda`（v4.17 标准源码经 #1315 合并，**CONDITIONAL source qualification**；RA02 为 NOT_APPLICABLE 而非 PASS；非整套运行时验证完成声明）。审核/冻结时必须重读 exact HEAD、Git blob 与后续漂移  
> **SOURCE:** [ADS #1320](https://github.com/kaicreator-mm/ai-development-standard/issues/1320) 与 2026-10-25 需求讨论  
> **R1 REVIEW:** [#1320 R1 findings](https://github.com/kaicreator-mm/ai-development-standard/issues/1320#issuecomment-6388457224)：P0=0/P1=2/P2=6/P3=3；`CHANGES_REQUESTED`，`PRD_FREEZE_READY=NO`。  
> **NEXT:** 新 exact HEAD/PRD blob 的独立 Product R2 **focused difference review**；即使审核 PASS，也不自动产生 Product Freeze、L2 Freeze、Task/Claim、Main Merge 或 Release 授权。

## 0. 产品定位与核心决策

ADS v4.18 的重点，是在现有开发治理规范上，补足**大型需求如何合理拆分、怎样评估并行方案、如何与架构及项目脚手架联动、如何选择 Agent 并组织协作、什么条件需要人工介入**的工程分析能力。

核心目标：

> 将一个大型需求拆为相对独立且可验证的 Capability / Concern；通过稳定契约和合适的 Scaffold 建立真实源码边界；生成最大化安全并行的 Task DAG；由具备真实能力的多个 Agent、CI、Local Validator 与合法的人类权威协作，尽量减少无意义等待、重复实施、重复 CI 和不必要人工操作。

不得把固定开发步骤（Contract → Core → Adapter → UI → Validation）直接等同于任务分解。步骤流程可以存在于各 Lane 内；不同 Lane 具有不同子需求与局部步骤，最终按真实依赖进行集成。

目标架构包含六种**分析维度，而不是六套新生命周期**：
1. Requirement / Capability：独立用户或系统能力。
2. Architecture / Contract：边界、接口、原子不变量。
3. Project Scaffold：源码模块、Anchor、写集、集中接线点。
4. Task DAG / Workfront：可独立交付 Concern、依赖、并行与汇合。
5. Agent / Human：角色、能力、合法 Claim、协作与人工权威。
6. Evidence / Evaluation：正确性、证据可信度、交付与优化效果。

所有执行事实仍使用现有 GitHub 原生 Task DAG、Task/Execution Pack、Dispatch/Claim、Review/Validation 与 Release 权威；需求树、Scaffold 和 Lane 规划只是结构或规划视图。

## 1. 问题、证据与复用边界

### 1.1 当前问题

- **伪分解：** 大需求被拆成若干串行开发阶段，却没有识别独立子能力。
- **可避免的串行化：** Task DAG 把准备、源码实施、审核、合并和最终发布约束混为单一前置链。
- **Scaffold 未参与优化：** 已有 SF↔DF 绑定，却没有充分利用模块/Contract/写集来选择 Task 拓扑，也没有用 Task 冲突反馈优化源结构。
- **Agent 选择过晚：** DAG 在冻结前未明确必须的能力、环境、独立角色与资源约束。
- **协作重复：** Web、CI、Local、Reviewer、Merge Controller 可能重复同一工作，或在交接时丢失有效来源及 Claim。
- **人工介入不精确：** 把授权/物理协助和普通自动化步骤混在一起。
- **跨阶段分析方法分散：** 现有门禁与生命周期比较完整，但没有系统地规范“如何比较方案与模式”。
- **评估不足：** 仅看 DAG 有无环、Task 数量或 CI PASS，无法解释拓扑是否合理、有没有减少实际成本。

### 1.2 真实案例

[DomainHarness v0.10.2 #1300](https://github.com/kaicreator-mm/domain-harness/issues/1300) 的既有 18 节点计划在 #1320 Intake 时仍以长串行链为主；Host SQLite、订阅投影、文档、外部 Producer Fixture 和只读预检包含可以提前准备的独立工作面。[A6 #1356](https://github.com/kaicreator-mm/domain-harness/issues/1356) 已关闭；[PR #1357](https://github.com/kaicreator-mm/domain-harness/pull/1357) 于 2026-10-24 合并到 DomainHarness `v0.10.2`，属于**该项目按自身 pinned ADS 权威采纳的本地并行草稿修订**。这只能作为回顾性实践证据，不能自动改变 ADS v4.18 规范、别的项目 JIT/Claim 准入或验证要求；尚无可信的实测加速/节约结论。

### 1.3 已有规范：应优先复用

- TASK_DECOMPOSITION_STANDARD：Minimum Coherent Concern、Maximum Safe Parallelism、原子不变量、写集独占、真实依赖、中央接线、Mid-flight SPLIT/HOLD。
- templates/task-dag.md 与已完成的 #181：Lane-Oriented Decomposition、Lane Summary、Parallel、Integration convergence。
- DEVELOPMENT_WORKFLOW §2.4/2.4A：DAG 规划、模型适配、v4.12+ 条件性的 Source-first Scaffold。
- TASK_DAG_GOVERNANCE_STANDARD §10A：已接受的 Source Scaffold (SF) ↔ Task-side DAG Binding (DF)、真实 Anchor、单一有效写入 Task、MI 完整性、双向校验、合法 Mutation。
- EXECUTION_ARCHITECTURE / EXECUTION_PACK：原生 GitHub DAG、JIT 分支、序列化 Claim、Role Ready Sets、F0–F3、精确身份与恢复。
- GITHUB_AGENT_INTERACTION_PROTOCOL / LOCAL_AGENT_HANDOFF_PROTOCOL：逻辑执行体、独立 Reviewer、委托与职责移交、GitHub-only 持久事实与最小 Local Handoff。
- MODEL_USAGE_POLICY §1–4：风险与自由度决定模型强度及非收敛升级；不按模型品牌赋权。
- PROJECT_STRUCTURE §1/§4：多子模块项目优先考虑 Monorepo，但按领域边界决定实际布局，不新增仓库结构权威。
- EXECUTION_ARCHITECTURE §23.4 / LOCAL_AGENT_HANDOFF_PROTOCOL §3、§8–9：已涵盖 proportional continuation、真实剩余工作、受限交接和 GitHub 持久回执。
- EXECUTION_ARCHITECTURE §11.1.1 / §27.3、TASK_DAG_GOVERNANCE §10A：分别涵盖单 Task 受保护 Claim、跨 Task 共享资源准入与单有效 Scaffold Anchor Writer。
- EXECUTION_ARCHITECTURE §19、DEVELOPMENT_WORKFLOW §4（non-converging repair）及 §9：人工决定、异常升级、DENY/WITHHOLD 和真实授权的权威边界。
- ARCHITECTURE_DESIGN_STANDARD 与 RELEASE_STANDARD §11.7A：已存在的架构决策质量和 ADS standards-source qualification 边界。
- 相关实践：[ADS #1173](https://github.com/kaicreator-mm/ai-development-standard/issues/1173)、[#1241](https://github.com/kaicreator-mm/ai-development-standard/issues/1241)、[#1199](https://github.com/kaicreator-mm/ai-development-standard/issues/1199)、[#1200](https://github.com/kaicreator-mm/ai-development-standard/issues/1200)、[#1201](https://github.com/kaicreator-mm/ai-development-standard/issues/1201)。

每项新增功能在 L2 前须判定：ALREADY_COVERED / TRUE_GAP / IMPLEMENTATION_ONLY，并明确既有规范 owner/source/blob；不得仅因换一种说法便复制规则。

## 2. Product 目标、成功标准与优先级

1. 大型需求先形成相对独立 Capability，再映射 Concern、局部步骤、Lane 和真实依赖 DAG；完整保留业务验收与不变量。
2. 对明显串行化的 DAG，能提出更安全合理的替代拓扑或说明为何串行不可避免。
3. 已合法接受的 Scaffold 与 Task DAG 双向映射可供并行规划使用，但不改变 SF↔DF/MI 权威。
4. 任务计划说明合适的 Agent 类别、真实能力/环境、独立审核与交接，不永久绑定厂商模型。
5. 人工决策与人工环境协助可被精确识别、范围最小化，Agent 能依据已持久化证据继续推进。
6. Product、Architecture、Implementation、Validation、Review、Release 等阶段采用适当分析原则和可选 Pattern，而非新增普遍强制 Gate。
7. 所有安全约束优先于并行率；效率提升需有真实证据，缺失数据标记 UNKNOWN。

**P0（核心目标）：** FR-01～FR-12。  
**P1（轻量方法完善）：** FR-13～FR-15。  
**P2（可后置持续演化）：** FR-16。

**产品优先级 ≠ 必须新增规范文本。** P0 表示应满足的 Product outcome，不代表每项 FR 都需要新的文件、字段、PR、Gate 或规范条款。一个 `ALREADY_COVERED` FR 由**原 owner + 其当前 Git blob + 既有/至多一个共享 Golden 正反例**证明满足；不得另写等效条款。`IMPLEMENTATION_ONLY`/纯示例/模式索引不得扩大规范权威。`TRUE_GAP` 才可进入最小规范差异设计，并在 L2 复核。

**R1 评审后的优先增量边界（待 L2 确认）：** FR-04 依赖理由与拓扑替代方案输出；FR-05 在 Freeze 前基于 SF↔DF 的双向边界反馈；FR-08 在现有 Lane Summary 补充 WEB/CI/LOCAL/独立角色与能力要求；FR-07 采用现有 JIT 规则的解释/负例；FR-10 的最小剩余工作 handoff tuple 仅在现有 LAH §3 / EXEC_ARCH §23.4 尚未充分覆盖时才补充。FR-03 的模式索引及 FR-15 的非门禁评价可独立采用轻量示例。优先级不是 12 个独立强制 PR 或冻结前的实施准入。

| FR | R1 新增性初判 | 现有规范/处理建议（L2 须复核当前 Blob） |
| --- | --- | --- |
| FR-01 | ALREADY_COVERED mostly | Task Decomposition §3/§9/§13、task-dag Lane；仅补 Capability-first 提示 |
| FR-02 | ALREADY_COVERED | Task Decomposition §4–6/§10/§13；不重写 |
| FR-03 | PARTIAL / TRUE_GAP_SMALL | 中央接线与原子性已有；提供轻量 Pattern 索引/反例 |
| FR-04 | TRUE_GAP | 可选依赖理由注解、替代拓扑/串行说明；不改 native blocked_by |
| FR-05 | PARTIAL / TRUE_GAP_SMALL | SF↔DF/MI 已有；补冻结前双向规划反馈 |
| FR-06 | ALREADY_COVERED | Task Decomposition、SF↔DF、Project Structure，引用即可 |
| FR-07 | ALREADY_COVERED / CLARIFICATION | 决定采用 JIT/ready_builder 不变的 Option A；禁止 merge-only native 第二语义 |
| FR-08 | PARTIAL / TRUE_GAP_SMALL | Workflow/Model Policy 既有；增加紧凑 Lane capabilities/roles 规划 |
| FR-09 | ALREADY_COVERED | Model Policy、Execution/GAIP/LAH；可选协作示例 |
| FR-10 | PARTIAL / VERIFY_OWNER | LAH §3/§8、Execution §23.4 已有；先核对后必要时最小 tuple |
| FR-11 | ALREADY_COVERED mostly | Execution §19、Workflow §4/§9，设备协助仅示例 |
| FR-12 | ALREADY_COVERED | Workflow §9、人类授权，仅引用/示例 |
| FR-13–14 | IMPLEMENTATION_ONLY | 现有 Golden/Reference 中一处可选索引 |
| FR-15 | PARTIAL | 优化分析是非 Gate 检查表；正确性由已有标准负责 |
| FR-16 | ALREADY_COVERED / DEFER | Workflow §8，跨产品实现不纳入 v4.18 交付前置 |


## 3. 需求与 Task DAG 分解

### FR-01 — 多维需求分解（P0）

区分四种结构：
- **Requirement / Capability Tree：** 大需求、相对独立子需求、Acceptance、Non-goals。
- **Architecture / Scaffold：** 模块、Package、公共 Contracts、原子不变量、源码 Anchor、允许写集。
- **Lane / Workflow：** 按可独立推进的能力或 Concern 形成多个工作流，各有局部 Contract/Implementation/Test 步骤。
- **Task DAG：** 可合法调度 Concern 之间的真实依赖、中央集成及版本汇合。

要求：
- 先寻找具有明确结果的独立 Capability，再按实际 Concern 拆分，不按固定步骤全局串行化。
- Capability、Concern、Step、文件路径之间允许合法多对多关系。一个 Contract 可以支持多个能力，一个 Integration Task 可以消费多个 Lane。
- 内部 Step/测试 Checklist 默认不自动成为 GitHub Issue。独立可合并且权责明确的 Concern 才应考虑 Materialize 为 Task。
- 不能为增加并行度拆开必须整体保证的安全、事务、状态/ABI 不变量。

### FR-02 — Task 拆分原则（P0）

Planner 对主要 Concern 评价：价值/结果独立、Contract 稳定、实现与写集所有权、真实上游依赖、可独立验证、必要集成边界、执行权限与环境、风险/成本。

**硬约束**：完整覆盖 Frozen Product/L2；原子语义正确；不虚构 Task READY；不双写；不删除真实 GitHub blocked_by。允许本来就必须串行的 Task。

### FR-03 — Task Decomposition Patterns（P0）

建立小型**可选**模式库，至少覆盖：
- Fan-out / Fan-in：共享 Contract 后分支并行，中央集成。
- Vertical Slice：独立业务场景的端到端交付切片。
- Parallel Pipelines：多个 Lane 各自拥有适当局部实施流程。
- Contract-first / Platform + Plugins：稳定共享接口后独立 Package/Adapter。
- Evidence Parallel：只读准备、测试设计/Fixture 与合法实施分离。
- Migration / Strangler：并行准备，安全切换点串行集成。
- Atomic Invariant：明确不应并行拆分的 Concern。

模式应记录适用条件、前提、推荐拓扑、写集、集成汇合、反例及评估 Oracle；不是第二套固定流程或权限凭据。

### FR-04 — Task DAG 拓扑评估（P0）

在 DAG Freeze 前，Planner 对大型/明显串行计划 SHOULD：
1. 检查覆盖、正确依赖、原子性和安全可执行性。
2. 以**非权威规划注解**解释依赖理由：集成代码/契约、共享写集、Review/Validation 证据、Merge/Release 汇合、资源/执行体。**选择 Option A：GitHub 原生 blocked_by 仍是唯一真实依赖；理由标签不能重分类 native edge、不能更改 ready_builder/ready_merge、不能授予源码提前开发或绕过 JIT。** 如注解与 native 当前关系冲突，native 关系胜出，受影响源码准入 HOLD；需要拓扑变化时使用已有法定 Task Split/Add/Mutation 与 native readback。
3. 比较候选拓扑的可用并行 Workfront、最长拓扑链、Owner 冲突、Agent/环境匹配、Rebase/CI/Review/交接/集成成本。
4. 提供一项安全替代方案，或给出不可优化的具体证明。
5. 无实测耗时与成本时只能做定性或结构分析，不能声明数值加速。

不设置统一最低并行率、Task 数量、LOC 限制、固定子任务层数或默认必须跑第二规划器。

## 4. Scaffold 与 Task DAG 联合规划

### FR-05 — Scaffold-aware DAG Planning（P0）

已有 v4.12 **条件性** Source Scaffold (SF) ↔ Task-side DAG Binding (DF) 规范为唯一来源；不重建绑定协议。

- 有已接受 SF 时，根据真实 Module、Package、Anchor、Contract、写集识别独立实施 Concern 与中央 Wiring。
- 无合法 SF 时，可以直接用 Frozen L2 模块/Contract 边界规划；SF 专用验收为 NOT_APPLICABLE，不强制生成源码脚手架。
- 在合法规划和 Freeze 前，允许双向评估：Scaffold 提示独立 Lane；DAG 写集冲突提示必要的模块拆分、公共 Contract 或中央集成 Owner。
- 已冻结的 Product/L2/SF/DF/MI/Issue Binding 发生实质变化时，走既有 Amendment、DAG Mutation、GitHub native edge readback、Pair Freeze/MI 重算。
- SF Anchor 本身不是 Task Claim 或写入许可；必须满足当前拥有的 Issue Allowed/Forbidden、合法 Claim 与具体权限。

### FR-06 — 源码所有权及集成边界（P0）

多模块项目的 Monorepo 倾向由现有 `standards/PROJECT_STRUCTURE.md` §1/§4 决定（本 FR 不重新定义布局策略）；在该权威下评估公共 Contracts、Core、Adapter、SDK、apps 与 Tests 的真正业务边界；共享 manifest、workspace/lockfile、Catalog、入口、CI 等按现有单有效写入/资源准入原则确定中央 Owner。

一目录一 Task 不构成合格拆分。现有 Anchor ID/kind/location/contract_ref、Git Object identity、文件 mode/symlink/gitlink、MI 双向可重算性和受控排除机制不变。并行草稿分支不能扩大写集或绕过绑定约束。

## 5. 实施、合并和验证边界

### FR-07 — PREP / IMPLEMENTATION / MERGE / RELEASE 分离（P0）

仅作为规划**概念区分**，不新增四套工作流状态：

- PREP/EVIDENCE：合法只读研究、Fixture 与测试方案设计，不等于 Builder READY。
- IMPLEMENTATION ADMISSIBLE：现有 Issue/native dependency、Role/Claim、Task Pack、exact base、写集及权限真正满足才可写源码。
- MERGE ELIGIBLE：满足 Task 的依赖、真实 CI/Validation、适用独立 Review、target/currentness 以及集成前提。
- RELEASE ELIGIBLE：整版 exact candidate 的 Full/Hidden/Critical Journeys/Packaging/RQ 由现有标准判定。

**Product 决定采用 Option A（v4.18 不改变 §6 JIT / ready_builder）：** 受 native `blocked_by` 的 Task 仍不得仅凭“Merge-only”注解、独立路径或草稿分支获得提前源码实施准入。可独立实施的前置 Concern 只能经现有合法 Task Split/ADD/独立 source-scaffold planning Task（如适用）、真实 native dependency mutation/readback、明确不重叠的 Source Writer、当前合法 Claim 后开始自己的工作；原下游 Task 的真实集成/合并依赖保持。PREP 是只读分析而非写源码。DomainHarness A6 的本地双门禁为回顾性项目特例，**不被 v4.18 普遍采纳**。将“原 Task 原生依赖不变却标记 merge-only 并提前 Builder READY”的机制作为将来独立 Product/L2 研究，不在 v4.18 改变原生边语义、JIT 或 Claim。

## 6. Agent 适配与跨 Agent 协作

### FR-08 — Capability-based Agent Planning（P0）

每个重大 Concern 规划候选执行能力，最终 Dispatch 才核定真实执行体：
1. 合法 Role/Task/Claim/有效规则；
2. 必需工具、代码/平台能力及可核实观测证据；
3. WEB/CI/LOCAL 环境与资源限制；
4. 风险、独立审核要求、F0–F3 自由度；
5. 效率、成本、延迟、交接与返工。

Strong Agent 面向 Product/Architecture、复杂不变量、风险决策与高风险 Reviewer；低成本 Builder 承担 Contract/Tests 已冻结的有界实现；CI/Local 负责自身确能提供的真实运行证据。不能凭模型名称自动赋权，不建立 Agent Registry、模型路由或新调度器。

### FR-09 — Multi-Agent Collaboration Patterns（P0）

可选模式：
- Strong → Lower-cost（设计、验收 Oracle → 有界实现）。
- Planner → Parallel Builders → Integration Owner。
- Web → CI → Local（仅真实剩余环境工作）。
- Builder → Independent Reviewer / Validator。
- Agents → Genuine Human/Delegate Decision → Agents resume。

一个 Task 可涉及不同角色，但并行 Writer 必须同时满足**三个既有约束**：① `EXECUTION_ARCHITECTURE §11.1.1` 每 Task/Role/compatibility_group 的序列化受保护 Claim；② `TASK_DECOMPOSITION §4` 与 `TASK_DAG_GOVERNANCE §10A` 的跨 Task 写集/Scaffold Anchor 单有效 Writer；③ `EXECUTION_ARCHITECTURE §27.3` 对实际共享资源的准入。两 Task 的 Claim Key 不同**不代表**可并发写同一 Catalog/lockfile/Anchor。现有委托/交接、operator_id/session_ref、event-v2、Review 独立性与 GitHub 持久事实仍是唯一权威。

### FR-10 — Minimal Remaining-work Handoff（P0）

复用 `LOCAL_AGENT_HANDOFF_PROTOCOL §3/§8` 与 `EXECUTION_ARCHITECTURE §23.4` 的原有持久交接与 proportional continuation：完成可合法完成的工作后，只移交**最小剩余单元**，而非重做 Task。既有 GitHub 事实应足以解析 current exact subject、accepted Claim/Task Pack、已验证输出、未完成证据/资源、环境能力、接收角色、停止/升级条件、UNKNOWN 或失效证据。只有经 L2 证实这些现有字段无法表达时，才提出最小 tuple/prose 改动，不另建 schema 或事件族。

- WEB 可完成的 GitHub/源码/文档工作优先完成，但不强制每项必须 WEB 先行。
- CI 满足真实 profile 时优先复用，不机械要求 Local 重跑。
- 仅真正的实机、平台、外部效果证明由合格 Local 补做。
- 独立 Reviewer 不得由原 Builder 自证。
- UNKNOWN active Claim / lost ACK / 未确认外部效果须先按现有恢复协议协调，不允许换 Agent 抢占。

## 7. 人工参与与升级

### FR-11 — Human Intervention Classification（P0）

仅在以下真实条件需要人工/合法委托权威：
- **Protected Decision：** Product/架构/权限重大取舍、受保护风险接受、例外、破坏性操作、需人决定的 Release 限制等。
- **Environment Assistance：** 连接物理设备、合法完成访问/同意手续、Agent 无法执行的现场动作。
- **Escalation：** 复用 `DEVELOPMENT_WORKFLOW §4` Non-converging Repair 与 `MODEL_USAGE_POLICY §4`：相同根因反复失败且无新证据、Frozen 事实矛盾、必要权限/效果 UNKNOWN 且无法按已有 owner 规则消解时升级；升级未必自动等于人类审批，先路由正确所属权威。

不让人工抄日志、转发 GitHub 已存指针、轮询 CI、重复低风险代码审核。人工并不是固定阶段门禁。

### FR-12 — Bounded Human Request & Resume（P0）

真正需要人工参与时，给出：当前具体主体/阻塞、选项、风险、推荐（有证据才给）、请求的最小授权/动作、完成后的 Agent 恢复路径。

沿用真实 Human Decision Authority、DENY/WITHHOLD、同一权限主体的有效 supersession、scope/currentness/readback。聊天文本、HUMAN_APPROVED 字符串、同一 GitHub 登录、没有 DENY 均不能铸造真正的人类批准。人工做一个动作不代表 Task 全部合格，Agent 应继续剩余法定验证。

## 8. 跨阶段方法、模式与评估

### FR-13 — Common Engineering Analysis Framework（P1）

为重大 Product、L2、DAG、Implementation、Validation 与 Release 决策提供可选通用方法：

Problem & Goal → Constraints & Invariants → Candidate Patterns → Evaluation / Counterexamples → Decision & Evidence。

可在现有 Artifact/Issue 内简述；普通简单 Task 不强制附加单独分析文件、Review 或 Gate。

### FR-14 — Stage-specific Patterns（P1）

在各原有标准所有者的职责内整理轻量模式与适用/反例：
- Product：Capability Tree、User Journey、Hypothesis/Evidence。
- L2：Bounded Context、Contract-first、Failure Boundary、Trade-off。
- Scaffold：Modular Monorepo、Plugin Boundary、Central Writer。
- Task DAG：Fan-out/Fan-in、Parallel Pipelines、Atomic Concern。
- L3：Tests→Contract→Implementation→Failure Handling、Negative Oracle。
- Implementation：One Concern/PR、Incremental Slice。
- Validation：Risk/Impact-based Regression、真实证据复用。
- Review：Differential、Adversarial、Invariant-based。
- Release：Critical Journeys、Exact Integrated Closure。
- Evolution：Root Cause、Pattern Applicability、Measured Improvement。

模式建议默认只在现有 `templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md`（以及已存在的 Golden Index）中维护**一处可选索引/对照**；相关原标准可以链接，不要求为十个 Stage 分别改写规范或创建新文件。索引提供适用前提/反例，不是新的规范权威，也不要求每个阶段新建文件。

### FR-15 — Planning Quality Evaluation（P1）

两层评价：
- **必须正确：** Product/L2 完整覆盖、Contract/原子性、真实 DAG、唯一写集、SF↔DF 完整性（适用时）、合法 Claim/Actor/人工权威、Review/Validation/Release Gate 不降级。
- **可优化：** Workfront 宽度、结构最长路径、模型与环境适配、重复 PR/CI/Review、Handoff、人为触点、Rebase 和返工、完整交付成本。

绝不为了可观并行比例牺牲不变量，不凭模型声明代替测试结果。

### FR-16 — Evidence-driven Pattern Evolution（P2）

ADS 仅定义自己拥有的规范/Pattern 与合法演化流程；task-meta、Tally、DomainHarness 是否实现采集、选择、候选推荐及运行时效果，分别属于各项目自身 Product/L2 和验收权限，**ADS v4.18 不承诺、不强制这些外部产品的实现行为**。只有来源合格、具有对照与适用范围的实测数据可用于效率判断；任何遥测、推荐评分或 Agent 自报告不得自动改变规范、发布 Gate 或旧项目 pinned 版本。

本项可以晚于 P0/P1 完成，不成为 v4.18 核心路径不必要阻断。

## 9. Product Acceptance Scenarios

**验收证据级别：** v4.18 此处新增/澄清规范的 Product acceptance 以现有 conformance owner 的**E1 SOURCE-ONLY Golden 正反用例**和精确 Git blob/commit 校验为主；可复用 `templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md` 的源级示例及其既有测试 owner。以下含“真实 Node24/SQLite、多人 Agent、Human Approval”的案例在规范测试中应使用**明确标注的虚构场景/Fixture**，验证是否正确拒绝伪资格，不得自称已经进行了真实物理/外部效果/授权验证。DomainHarness #1300/#1356/#1357 仅为回顾性案例。真实多 Agent/Tally/task-meta 集成、外部效果、运行收益测量分别保持 `NOT_RUN` 或项目独立已证事实，不是此次 source-only ADS 标准交付的新增发布前置条件；Release 适用性由原 `RELEASE_STANDARD §11.7A` 和 Gate Owner 判断。

### 正例

- **P01 多维拆分：** 一项多渠道通知大需求拆成 Email、SMS、UI、订阅能力，先冻结公共 Contract，形成具有局部实施流程的并行 Lane，最后完整集成。
- **P02 长链对比：** 输入**虚构**含可独立 Adapter/Docs/Fixture 的 18-node 过度串行 DAG，给出合法替代拓扑，并明确真实依赖、中央 Writer、复验与 Release 汇合；不修改 DomainHarness 的现行 native DAG，也不宣称实测节省。
- **P03 SF 驱动并行：** 已接受 Monorepo SF 中 Contracts/Core/Adapter/SDK Anchor 与实际 Issue/Task 绑定，独立作者没有共享写集竞争；MI 独立验证。
- **P04 DAG 反向评估 SF：** 共享源码导致虚假串行时，在冻结前提出中央接线或源码边界改善方案；冻结后必须合法 Amend。
- **P05 Agent 协作：** Strong 产生 Contract/Oracle，若干合法 Builder 编码，CI 提供真正可用证据，Local 只补充不足的物理验证，Reviewer 独立审核，Merge Owner 集成。
- **P06 最小人工：** 普通 WEB+CI+Review 无人阻塞；真正的设备连接或权限决策只请求限定动作，随后合法恢复。
- **P07 跨阶段模式：** 重大设计选择能说明模式适用前提、替代方案与反例；简单 Task 无额外制度负担。
- **P08 合理串行：** 真实安全/事务原子 Concern 保持单一写入与完整验证，理由充分，不强求并行。

### 负例

- **N01** 删除真实 native blocked_by 来提升并行率 → BLOCK。
- **N02** 两个活动 Claim 竞争 Catalog/lockfile/同一 Scaffold Anchor → 拒绝或按权威串行，双 CI PASS 不代表可合并。
- **N03** SF Anchor 缺失/失效、无 Task Issue 映射、MI 未证明、无 Claim → HOLD。
- **N04** 只有只读 PREP 条件却提前创建实现并声称 Builder READY → 拒绝。
- **N05** Builder 自称独立 Review PASS → 拒绝。
- **N06** Web 静态分析或旧 SHA CI 冒充 Node24/SQLite 实际验证 → 拒绝。
- **N07** GitHub 运输身份或文本 HUMAN_APPROVED 冒充真实授权 → 拒绝。
- **N08** 同一 Claim/effect UNKNOWN 时跨 Web/Local 继续竞争写入 → HOLD/协调。
- **N09** 为并行把原子安全/状态机规则拆成两个无效半成品 → 拒绝。
- **N10** 所有内部 Step 强制独立 Issue/PR/CI/Review/Local/Human → 拒绝过度流程。
- **N11** Frozen L2、Scaffold 或 DF 修改未有合法变更、Native DAG Readback/MI 重算 → HOLD。
- **N12** 无实测数据而声称 2× 加速、节约具体成本 → 不接受效果结论。
- **N13** Agent 仅凭模型名称或自述能力提升权限/F3 → 拒绝。
- **N14** 需要一次人工设备操作却把全部 Task 强迫交给人工 → 不符合最小介入。
- **N15** 用 Capability Tree/Lane 表/依赖原因的 `MERGE_ONLY` 注解宣称 Builder READY，实际 native `blocked_by` 尚未满足 → GitHub native 事实胜出，source HOLD；任何实质变更必须先完成已有 DAG Mutation 和 native 双向 readback。

## 10. 规范变更归属与初步 Task 分流

这只是 Product 的候选归属建议，正式权威应由 L2 检查。

| Surface | 最小必要变更方向 | 禁止重复 |
| --- | --- | --- |
| TASK_DECOMPOSITION_STANDARD | Capability/Concern 分解、并行方案比较、模式适用 | 不复制已有原子/写集/真依赖规则 |
| templates/task-dag.md | 现有 Lane Summary 增加紧凑 Parallelism + Scaffold + Agent 评估 | 不创建第二 DAG |
| TASK_DAG_GOVERNANCE §10A | 在 Planner 示例中复用已有 SF↔DF/MI | 不重写完整性或 Anchor 权威 |
| DEVELOPMENT_WORKFLOW §2.4/2.4A | 必要时轻量引用跨维度规划 | 不新增默认 Scaffold 阶段 |
| EXECUTION_ARCHITECTURE §6/§11.1.1/§23.4/§27.3 与 EXECUTION_PACK | Option A：JIT / ready_builder 不变；仅提供 PREP 与合法 Writer 的负例和引用 | 不新增 merge-only native 依赖或提前源码权限 |
| PROJECT_STRUCTURE §1/§4 | 沿用多模块 Monorepo 的已有政策 | 不新增项目架构默认约束 |
| MODEL_USAGE §1–4 / GAIP / LOCAL_AGENT_HANDOFF §3/§8–9 | 复用能力、独立角色、最小剩余工作和恢复约束 | 不建 Agent 注册或新 Event |
| EXECUTION_ARCHITECTURE §19 / DEVELOPMENT_WORKFLOW §4/§9 | 复用非收敛升级、受保护人类授权和人工协助示例 | 不做新的审批体系 |
| Existing conformance owner | 复合正例 + 小型负例 | 不将静态测试视作真实 Host/Release PASS |

候选工作面：A 需求/Concern/Topology，B Scaffold 联合规划，C Agent/协作，D 人工/升级，E 阶段 Pattern，F 组合 Conformance，R 版本集成。A–E 可以在**真正独立的标准文件写集**上并行，但若竞争相同规范 Owner，必须统一编辑或合法拆分；F/R 保留真实汇合条件。P2 可延后。

## 11. 明确非目标

不引入新 Scheduler/Agent Registry/模型 Router、第二个 DAG、第二 Claims/Dispatch 机制、普遍人审、新的永久 Review/Freeze/Gate、每子步骤 Issue/PR/CI、每 Task 本地全量回归、固定模型提供商、强制所有项目 Source Scaffold、固定并行率/SLA、自动架构变更、非法提前源码写入、未经 Product/L2 冻结改变规范、没有真实证据的部署/外部效果声称。

ADS 规范源码的交付与真实跨系统运行时能力验证是不同 subject；不能以本 R0 声称 Tally/task-meta/DomainHarness 功能已实现。

## 12. Claude 独立 Product R2 差异审核契约

R1 独立审核记录：[#1320@6388457224](https://github.com/kaicreator-mm/ai-development-standard/issues/1320#issuecomment-6388457224)；R0 exact HEAD `37a257d3be60e99e38c494f274a3e1c35860dcdd`，PRD blob `e8d3822bfe0bb5b31b2c991a10a8cbdbdd73b8a6`。R1 结果 P0=0/P1=2/P2=6/P3=3、`CHANGES_REQUESTED`、`PRD_FREEZE_READY=NO`。本文 R1 已修订 P1-1/P1-2 和 P2-1..P2-6，并纳入 P3 的负例、统一索引与外部产品边界。

请独立读取**当前新的 exact branch HEAD 和 PRD Git blob**，只审 R0→R1 实质差异及可能新增的 P0/P1；必要时对照有效 main owner/blob 与 #1320、#1173、#1241、#1199–#1201。重点验证：Option A 是否完全禁止 `MERGE_ONLY` 标签成为 source authority、Product outcome 的 ALREADY_COVERED 如何关闭、Scaffold/Claim/Shared resource 三层权限、A6 历史事实和 source-only Golden 证据级别。

重点反证：
1. Requirement/Capability/Concern/Step/Lane/Task 的层次及多对多映射是否正确，是否在无意中创建第二 DAG。
2. Scaffold-aware Task DAG 是否尊重 SF/DF/MI、Frozen Product/L2、单写入者与 native mutation。
3. PREP/Implementation/Merge 的概念是否与 JIT、真实 Claim / blocked_by 冲突，是否暗中授予提前源码写权限。
4. Agent/Reviewer/Validator、能力证据、委托交接、人类权威是否重复现有标准或擅自扩大权限。
5. Pattern/质量评估是否有真正新增价值，是否会带来过度规范流程。
6. P0/P1/P2 范围是否需要收缩，是否存在能阻塞 v4.18 的不合理依赖。
7. 正负用例是否足以证伪伪并行、伪验证、伪权限与过度拆分。

要求报告：SUBJECT_HEAD、PRD_BLOB、SOURCE_CURRENTNESS、INDEPENDENCE、R1_P1_CLOSURE、R1_P2_CLOSURE、P0/P1/P2/P3 与真实反例/源引文/修正建议、PRODUCT_R2=PASS|CHANGES_REQUESTED|BLOCKED、PRD_FREEZE_READY=YES|NO、NEXT。

**只读审核；不修改源码、不合并、不进行 Product Freeze。**
