# ADS v4.11.0 — PRD 中文摘要（产品审查版）

> **状态：供产品负责人审查，非冻结、非新产品权威。**
>
> 摘要依据已获独立产品审核的 PRD v0.3 编制。它只帮助快速判断产品方向与取舍；凡摘要与完整 PRD 不一致，均以原 PRD 的精确 Git blob 为准。阅读或修改本摘要、回复一般意见，**不代表批准 Product Freeze**。

| 项目 | 内容 |
| --- | --- |
| 项目 | `kaicreator-mm/ai-development-standard` |
| 目标版本 | `v4.11.0` |
| 完整 PRD | `docs/implementation/4.11.0/PRD.md`，blob `d30f202e8ea662731ff8a4f2ad1ad88cfc5bb179` |
| 已审核的 Product 准备检查点 | `planning/v4.11.0-product-freeze-prep@34df09a2433aec5523ab80c90e885f6d9fc78803` |
| 独立审核 | Product Review R3 `#941@6067535335 PASS`；Git 转录审核 `#942@6068127988 PASS` |
| 待决定 | `#943` Product Authority 是否批准按确切 Git 主体冻结 |
| 本摘要效力 | `REVIEW_ONLY`；不改变 PRD、Review、L2、Task DAG 或 Release 状态 |

## 一、产品目标

**让任何项目只需采用一个 ADS 标准，就能获得成熟、统一、可验证、持续演进的 AI 软件工程方法。**

任何参与项目的 Agent，都必须按照自己的角色、任务、权限及风险遵守适用的工程规范；多个 Agent 协作时还必须遵守统一的交互规范。两套规范必须在同一个 ADS 版本、同一条工程权威与证据链下**无冲突地组合运行**。

目标是提供**工程方法标准**，不是创建另一个编码 Agent、Agent Runtime、IDE、任务管理 SaaS 或通用调度服务。

### 核心产品模型

| 维度 | 要解决的问题 | 必须达到的结果 |
| --- | --- | --- |
| **A. 单 Agent 工程规范完整性** | 单个 Agent 怎样正确完成受权范围内的工程任务？ | 产品、需求、架构、复用、编码、质量、安全、测试、验证、发布和维护中，凡适用的义务都有明确规范 owner、执行输入、验收证据、失败处理与任务终点。要求独立审核或真实 Build Host 的任务允许交接，不能自证通过。 |
| **B. 多 Agent 交互规范完整性** | 多个 Agent 怎样正确分工协作？ | 身份/能力/授权、任务分配、委派与责任移交、通信、并行写集、Claim、调度、审核、冲突、重试恢复、人工决策和集成均有可恢复、可审计的交互规则。**调度属于交互的一部分**。 |
| **C. 统一组合正确性** | 两类规范各自成立，合起来会不会失效？ | 跨 Agent、跨工具、跨环境和跨任务时，权威优先级、必需 Gate、真实证据、独立性与发布状态保持一致；局部 PASS 不得自动升级为全局 PASS。 |

**A、B、C 是三项证明义务，不是三个相互竞争的子标准，更不要求三个新服务。** 优先强化现有 ADS normative owners、schema、模板与一致性测试。

## 二、支持范围

- **项目形态：** Library / Service / CLI；新项目和存量项目。
- **采用等级：** A0–A4；允许手工协议到自动编排逐步升级，但强制性的安全、权限、验证和 Release 真实性底线不变。
- **工程工作：** 产品调研、轻量文档修改、缺陷、功能/契约、公开 API、数据迁移、安全漏洞、外部写操作/部署、发布、故障恢复、退役、上游复用，共 **J01–J12**。
- **角色：** Product Owner、Architect、Planner/Controller、Builder、Validator、Independent Reviewer、Release/Integration Controller，以及适用的人类权威。
- **执行方式：** 单 Agent 或多 Agent；WEB/LOCAL 是粗粒度环境描述，实际资格由能力、权限、独立性、当前性及真实环境证据决定。

**一个真实任务可以同时属于多个工作类别。** 例如安全修复 + 数据迁移 + 部署，必须同时满足安全审核、迁移恢复验证、外部副作用权限以及适用的人工批准。不能选择一个最方便的类别而忽略其余义务。

完整性声明只针对上述已明确的适用范围及经证据证明的等价类；无法证明的组合保持 `UNVERIFIED`，不能用 `NOT_APPLICABLE` 掩盖。

## 三、v4.11 必须交付的六项结果

| # | 必须完成的交付范围 | 验收重点 |
| --- | --- | --- |
| 1 | **适用规则与复合任务解析** | 一个 ADS Pin；确定有效规则、owner 和优先级；多工作类别的义务合并；冲突/未知失败关闭；不能靠低等级项目覆盖取消高风险 Gate。 |
| 2 | **多 Agent 交互及执行资格** | 基于角色、真实能力、权限和独立性的跨 WEB/LOCAL 工作；受保护 Claim、不重复调度、人工否决、合法关键路径恢复。 |
| 3 | **派发、审核、合并安全性** | 发布前契约/schema 检查；同一精确 HEAD 上相互矛盾的已接受 Review 必须裁决；不能因为最新一条 PASS 或 CI 绿灯而绕过阻断。 |
| 4 | **跨 Agent 恢复和信任边界** | 外部写操作可能成功但 ACK 丢失时，不得盲目重试；先去重、状态核实或授权补偿。工具/消息/文档中的不可信指令不能变成权限，敏感信息不能被不当转发。 |
| 5 | **成熟实践真正融入 ADS** | 把下列选定实践转为现有 ADS owner 的规范要求，并提供正反测试；仅做研究报告或竞品对照**不算完成**。 |
| 6 | **A+B+C 可执行完整性验收** | 统一的正向与对抗验证，覆盖最小 A0/A1 与高级 A3/A4；真实环境必要时由合法 Agent 执行；最终走 Candidate Freeze、Hidden、Fresh Closeout、Release Qualification。 |

### 本版必须吸纳的成熟方法

| 参考来源 | ADS 实际吸纳什么 | 不做什么 |
| --- | --- | --- |
| **OpenSpec** | 增量需求/规格变更、已接受规格与真实实现的一致性、过期证据失效 | 不强制安装 OpenSpec；archive 不自动等于 Product Freeze 或测试 PASS |
| **GitHub Spec Kit** | 配置/规则组合的确定性优先级、来源与版本追踪、不可削弱的强制底线 | 不采用竞争性的第二套开发流程，不照搬其优先级 |
| **ADS 自身 Reuse-First** | L1 发现 → L2 H1/H2/H3/BUILD_NEW 复用决策 → L3 测试/契约/失败处理；上游版本/许可证变化需重新评估 | 不强制建集中开源目录，不对低风险任务强制外部调研 |

参考项目的提交版本、许可证与 ADS 既有 owner 对应关系已经在完整 PRD §6 固定。其它 ISO、NIST、SLSA、SPDX、MCP/A2A、BMAD 等作为有条件的研究或兼容性参考，不能直接宣称 ADS 已满足全部外部标准。

## 四、三个必须分别证明的验收目标

| 验收 | 要证明的性质 | 错误情况举例 |
| --- | --- | --- |
| **P1 单 Agent 规范完整性** | 支持范围内，每类任务/角色的适用工程规则和证据能找到唯一权威；未覆盖必须报告 | A0 安全修复被当作文档 Fast Path；没有独立 Reviewer 却自报 Review PASS |
| **P2 多 Agent 交互完整性** | 委派、Claim、通信、调度、审核、冲突与恢复遵守权限和合法状态转换；无法继续时如实 BLOCKED | 两人重复 Claim；WEB 假报 LOCAL 测试；已被人否决的部署又被自动执行 |
| **P3 组合正确性** | 各 Agent 合法行为组合后，仍满足全部强制义务；证据、审核与 Release 不会在交接后升级或失真 | 安全+迁移+部署遗漏 Gate；断连后重复写；同 HEAD 的冲突 Review 被忽略 |

**最低证据设计：** 18 个基准场景（S01–S18）+ 8 类复合工程场景（X01–X08）；既要有成功路径，也要有能够触发拒绝、阻断、重试和恢复的反例。覆盖数量不代表已通过测试，更不代表证明了所有可能的工程组合。

- **Product Freeze 前：** 产品范围、必需能力、具体反例与未验证项处置必须明确，并经适用的独立 Product Review。
- **L2/实现阶段：** 定义确切 owner、规则投影、机器契约和验证方案；执行必要的正反测试与真实运行环境验证。
- **Release 前：** 对精确候选完成规定的可执行 P1/P2/P3 证据、独立验证、Hidden 和 Release Qualification；不得把 PR/CI PASS 当作 Release PASS。

## 五、明确不做

不新增强制的通用 Agent Runtime、独立 Scheduler SaaS、第二套任务数据库、IDE 或完整 MCP/A2A 服务器；不强制用户同时安装 Spec Kit/OpenSpec/BMAD；不把所有任务变成繁重的研究流程；不要求每一行代码人工审核；不保证所有 Agent 的执行顺序或独立审核观点一致；不声明已经获得外部标准认证或数学意义上的无限场景完整性。

## 六、需要产品负责人重点审查的决策

| 审查事项 | 当前 PRD 提案 |
| --- | --- |
| **产品定位** | 认可“一个 ADS 工程标准、两类规范、三项独立证明义务” |
| **完整性边界** | 同意 Library/Service/CLI、A0–A4、J01–J12 可复合的有限适用范围 |
| **交付范围** | 同意上述六项必须在 v4.11 真正交付，而不是只完成设计和研究 |
| **方法吸纳** | 同意将规格增量同步、规则组合溯源和 Reuse-First 作为本版必需规范能力 |
| **剩余未知项** | 同意未在 S/X 场景中穷举的复合任务继续**属于支持范围**，出现高影响新组合则 `UNVERIFIED/BLOCKED`，必须经 owner 等价证明或补充测试，不能静默豁免 |
| **版本边界** | 同意 v4.11 独立准备；不挪用 v4.10 的 Frozen Product、Hidden、Release 或 main 集成结论 |

**审查反馈建议：** 可对任何一项提出“保留 / 调整 / 删除 + 理由”，特别关注范围是否过大、某种单 Agent 工程义务是否遗漏、交互覆盖是否缺失、组合验证是否足以排除重大风险，以及哪些成熟实践应纳入/推迟。

## 七、审查后流程与当前真实状态

1. 本摘要供审查，**审查摘要不等于批准完整 PRD**。
2. 如有修改意见，先回到 `#938` 修订完整 PRD，并按影响范围补充独立审核。
3. 如认可完整主体及 §六未验证项的处理，才由 Product Authority 对 `#943` 作**明确的冻结授权**，绑定确切 PRD commit/tree/blob。
4. 获得合法 Product Freeze 后，再进入 L2、Task DAG、实现和 P1/P2/P3 可执行证明。

当前真实状态：`#941 Product Review R3 = PASS`；`#942 Git Checkpoint Review = PASS`；`#943 Product Authority = 待决`；`Product Freeze = NO`；`v4.11 L2/Task DAG/正式实现 = 未授权`。

**完整来源：**
- [PRD v0.3 原始审查文本](https://github.com/kaicreator-mm/ai-development-standard/issues/938#issuecomment-6067371136)
- [已核验的 Git PRD](https://github.com/kaicreator-mm/ai-development-standard/blob/34df09a2433aec5523ab80c90e885f6d9fc78803/docs/implementation/4.11.0/PRD.md)
- [场景与证据矩阵](https://github.com/kaicreator-mm/ai-development-standard/blob/34df09a2433aec5523ab80c90e885f6d9fc78803/docs/implementation/4.11.0/PRODUCT_PROOF_MATRIX.md)
- [Product Authority 决策 Issue #943](https://github.com/kaicreator-mm/ai-development-standard/issues/943)
