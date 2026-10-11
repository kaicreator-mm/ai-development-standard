# Research Convergence & Exit — 预研收敛与成果交接参考实践

> 状态：REFERENCE CANDIDATE / NON-NORMATIVE。2026-10-11，从 kaicreator-mm/domain-harness v0.8 的实际 Dogfood 提炼，提交 ADS 独立审查。**不是新 Gate、新版本 Freeze 授权或对已有 Frozen 标准的追溯修改。**
>
> 适用：架构探索、Product Evidence 预研、静态/源码研究、可执行 Research Demo、多 Agent 并行探索。尤其适合大版本、Kernel/Runtime/ABI/Trust 等高复杂度课题。
>
> 对齐：standards/DEVELOPMENT_WORKFLOW.md（Stage 1 Product / Stage 2 Architecture）、standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md、#186（静态研究）、#680（门禁成本）、#931（L1→L2→L3 证据脊柱）。若本文与仓库 pinned 规范冲突，以生效的规范与项目 Product authority 为准。

## 1. 观察到的失败模式

DomainHarness v0.8 的研究**产生了真实且可复用的成果**：physically selected Kernel Domain Package 的有界可执行验证、两个独立 Domain App 的复用价值 A/B、Host/Effect/Journal 与 ModelPort 反例、功能保留矩阵及真实 CI 修复。问题不是“研究全部无用”，而是：

1. Product Freeze 的范围判断与技术验证门禁混在一起，某个新技术缺口产生下一轮实验，形成 Research → Findings → Another Demo → Another Review → Product Freeze still BLOCKED 的自循环；
2. 架构实验通过后未及时形成 Product decision / L2 consumption / Task DAG implementation owner，探索活动数量上涨而正式交付不前进；
3. 已有 exact-SHA 实验与同一类反例仍被重复复核、重复派发；scratch 代码清理后无法原样移交，造成证据资产与代码资产不一致；
4. 把“下一阶段必须实现/验证的功能”误当作“本阶段冻结前必须全部完成的代码”；也可能反向把真正违反安全/权限或核心产品可行性的 P1 随意后推；
5. 多角色领取碰撞、过量非阻塞审查、老 CI 状态错误转移到新 HEAD，使调度成本超过新增决策价值。

这些是**阶段和证据路由的实践问题**，不是降低 fail-closed、真实 Validation 或 Independent Review 要求的理由。

主要事实参考：

- v0.8 产品/冻结控制：[domain-harness #949](https://github.com/kaicreator-mm/domain-harness/issues/949)、[#953](https://github.com/kaicreator-mm/domain-harness/issues/953)；
- 物理 Kernel Package bounded evidence：[PR #994](https://github.com/kaicreator-mm/domain-harness/pull/994)、[#993](https://github.com/kaicreator-mm/domain-harness/issues/993)；
- 双领域复用价值、Claim collision：[domain-harness #972](https://github.com/kaicreator-mm/domain-harness/issues/972)；
- readback / ModelPort / mandatory receipt 负例：[domain-harness #949 Controller 097–099](https://github.com/kaicreator-mm/domain-harness/issues/949#issuecomment-6105721208)；
- 对抗式 MUST/DEFER/STOP 收敛：[domain-harness #949 Controller 100](https://github.com/kaicreator-mm/domain-harness/issues/949#issuecomment-6105898109)；
- PRD 文档与差异：[PR #991](https://github.com/kaicreator-mm/domain-harness/pull/991)；独立工作流反馈 ADS [#680](https://github.com/kaicreator-mm/ai-development-standard/issues/680)、[#926](https://github.com/kaicreator-mm/ai-development-standard/issues/926)。

## 2. 正确的阶段边界：不把研发实现搬进 Product Freeze

| 阶段 | 必须回答的问题 | 可接受的证据/产物 | 不要预支的工作 |
| --- | --- | --- | --- |
| Stage 0 / 可选探索 | 研究的决策问题、消耗者和退出条件是什么？ | baseline、决策问题、既有来源、初始未知、预期投入 | 不按每个想法拆 Issue，不先建立正式实现 DAG |
| Stage 1 / L1 Product | 做什么、为什么、哪些承诺 IN/OUT、用户可观察的验收？ | 用户问题与竞品/替代方案、功能价值、范围取舍、必要时**有界 Product Research** | 不把全面 Runtime/Host 真实实现等同于 PRD Freeze；不靠架构 Demo 代替产品需求决策 |
| Stage 2 / L2 Architecture | 采用何种实现边界？剩余 material Architecture UNKNOWN 需要何种证据？ | 源码/既有项目证据，必要时 E1/E2/E3 的真实 Demo，L2 owner/ABI/风险决策 | 不因每个 Task 都再做 Demo，不把 Demo branch 直接视为正式实现 |
| Task DAG / L3 | 哪个 Task 拥有 Contract、代码、测试和拒绝路径？ | 冻结 L2、实证引用、任务依赖、Review Policy、测试矩阵 | 不重做已解决的 A/B 或在新 Task 中重新证明同一个前提 |
| Implementation / Closure | 真实功能、安全、恢复、CI、Hidden、发布是否 PASS？ | current exact-SHA 真实 Host/集成/回归/独立 Qualification | 不把先前 scratch/E1/E2 PASS 当 production/Release PASS |

**特殊情况：** Product 基本承诺自身是否可行若存在可实证的严重矛盾，Stage 1 的 Product authority 可要求精确、最小的 Product-feasibility evidence，或者明确窄化承诺；这不是允许把 Stage 2 的所有 Architecture Demo 无限前移。产品范围必须由有权角色确定，Agent/Reviewer 不得伪造 Owner 签名。任何 material P0/P1 不能仅靠更换标签消失。

## 3. 研究入场卡：先说明“什么结果会改变决定”

每条独立研究必须可回答以下五问：

1. **Decision:** 消费该证据的 Product/L2/Task/Release 决策是哪一个？谁拥有决策权？
2. **Unknown:** 哪个具体不变量或价值假设仍 UNKNOWN？已知/已有证明有哪些？
3. **Counterfactual:** 如果不研究、沿用成熟代码/现有设计，会失去什么？这个差异是否改变选择？
4. **Minimum proof:** 静态/已有 evidence 是否已足够？如不足，最小真实可执行实验的场景、E1/E2/E3、反例是什么？
5. **Exit and cost:** PASS、FAIL、BLOCKED 分别路由到什么下一步？预计 Issue/Agent/Review/Host 的增量成本，何时停止？

任何“先多做几个 Demo 再说”而没有已命名决策消费者的提案，应默认退回静态/现有证据判断。跨角色与跨会话的材料需要 GitHub 归档；小的控制推断优先写进已有 Issue 注释/投影，不把 Issue 当流水日志。

## 4. 建议的单轮研究闭环

~~~text
Named Product/L2 decision
    ↓
Adversarial intake: existing evidence sufficient?
    ├─ YES → reference exact evidence → decision / stage handoff
    └─ NO  → one bounded hypothesis + real seam + explicit negatives
                 ↓
             PASS | FAIL | BLOCKED
                 ↓
         Independent materiality challenge:
         Did this evidence actually change a decision?
                 ├─ YES → owner accepts/rejects → L2/Task/Release handoff
                 ├─ NO  → STOP, mark evidence historical/reference
                 └─ NEW critical P0/P1 UNKNOWN → authorize ONLY a focused successor
~~~

**研究完成标准 = Evidence complete / decision-ready，不是 Feature complete。** Demo 可在接口尚未产品化、UI/packaging 未完成时收口；但必须写清尚未证明的真实执行/安全/Host/恢复语义。Static Research 可采用 ADOPT/ADAPT/DEFER/REJECT/INSUFFICIENT_EVIDENCE，Executable Research Demo 保留其 PASS/FAIL/BLOCKED；两者不能混淆（#186）。

## 5. 五类出口，以及不得随意后推的风险

| 观察结果 | 正确出口 | 预研是否继续 |
| --- | --- | --- |
| 已有 credible source/executable evidence 回答核心假设 | EVIDENCE_SUFFICIENT → Product decision / L2 | 停止相同主题实验 |
| 技术候选失败，但 Product 用户承诺仍可通过其他架构达成 | REPLAN_ARCHITECTURE → L2 alternatives | 停止失败候选的无限修补 |
| Product 承诺本身选择未定，或成本与核心价值不匹配 | PRODUCT_CHOICE_REQUIRED → Owner IN/OUT 与验收 | 只做真正需要的决策证据，不代替 Owner |
| 机制已知可做但现有 SDK 不具备生产 API/Host 集成 | IMPLEMENTATION_GAP → L2/Task DAG | 预研停止；正式实现与真实测试不可免 |
| 真实的独立性、权限边界、不可逆 Effect、原子恢复或产品核心可行性仍未证明，且会改变架构/冻结范围 | MATERIAL_BLOCKER → 精确 owner + focused proof 或明确 Product rescope | 不得靠“后续再测”假装无风险 |
| 只影响发布候选/真实环境验收 | RELEASE_VALIDATION → future Closure Gate | 预研停止，但 Release 仍须验收 |

对于 P1/P0，**阻断哪一个阶段**需要用可验证理由判断，而不是默认把所有未知都阻断 Product Freeze，也不是一律后推。冻结前需明确安全信任根、用户可见承诺和可行候选；完整的实现回归属于实施/Release，除非本身是证明产品承诺可行性的唯一办法。

## 6. 六条止损触发器（触发后先收敛，不自动生成任务）

- **同问题重复:** 已有两个独立业务样例、足够直接的正/反例和 exact identity，新增第三个样例不能改变方案选择。
- **无新增决策价值:** 连续两次研究/Review 仅重复前次已知缺口或改善叙述；先要求材料性说明，非强制“再审一次”。
- **阶段错置:** 新任务要求在 PRD Freeze 前完整交付 L2/Implementation/Release 级别能力；先审查最小产品承诺和阶段归属。
- **范围失控:** 研究想“顺手修生产接口/再造一套运行时/增加另一个通用服务”；结束当前证据，必要的真实实现进入既有后续 Task。
- **证据短命:** 重要代码、fixture、测试仅存在自动清理 scratch 中；不得声称可直接在未来消费，应把必要最小 reference artifact 固定到受控 Git ref 或在 L2 明确重建成本。
- **Gate/DAG 膨胀:** 问题实际上是一次 Controller 判断/非阻断 P2，却生成独立 Issue、Agent Claim、Review、独立验证链；转为 issue 评论或已有任务的 acceptance 条目。

**可选预算（非强制数值 Gate）**：每一材料决策优先消费现有资料；首个新增 Demo 一次验证一个关键未知；第二个同主题 Demo/独立 Review 需要说明首个证据为何不能决定；如果预研未增加 Product/L2 可采纳事实、却继续增加活动，应触发 STOP/REDUCE/DECIDE 的 Controller review。对新 P0/P1 必须允许重新开启局部研究，不采用僵硬时间或次数上限代替风险判断。

## 7. 每个已完成研究的“资产可复用账本”

记录一次，不在每个阶段复制长报告：

| 字段 | 最低要求 |
| --- | --- |
| QUESTION / CLAIM | 被回答的一条决策问题和结论边界 |
| EVIDENCE_ID | GitHub exact commit/tree/blob、tests/commands、真实 Host、负例、独立 reviewer（若需要） |
| STATUS | STATIC / EXPERIMENTAL_PASS / EXPERIMENTAL_FAIL / IMPLEMENTED / RELEASE_VERIFIED，严禁混用 |
| REUSE_CLASS | CODE / CONTRACT / TEST / FIXTURE / ARCHITECTURE / NEGATIVE / DOCUMENT_ONLY |
| CONSUMER | Product clause / L2 ADR / Task DAG owner / Closure gate |
| LIMITS | 未验证场景、fake boundary、Host/安全隔离限制、风险 |
| ACTION | ADOPT / ADAPT / REIMPLEMENT / DROP / DEFER |
| NEXT_VALIDATION | 后续何时需要真正 Node/Host/CI/Hidden/Release evidence |

**转化效率指标（仅报告真实数，不做虚假百分比）：**研究工作的 Issue/Agent/Review 次数、解决了多少个独立 material UNKNOWN、多少个被 L2/Task DAG 真正消费、重新执行同一 A/B 的次数、研究代码/测试可复用率、最后一次产品决策到正式 DAG 的等待链。数量是成本/有效性信号，不是自动终止标准。

### 代码复用规则

研究 branch 并非 implementation branch，不能不经审查直接 merge。但是也**不能**为了“形式正确”无条件从零重写一套同等实现：

1. L2 写明采用的真实 Kernel/Contract/Tests、源 SHA 与不变量；
2. 对研究源码逐文件采用 REUSE/ADAPT/REIMPLEMENT 判定，记录安全和许可条件；
3. 准许有界拷贝/移植为正式 Task PR 并执行 production Contract/Validation/Review Policy；
4. 测试和失败反例随正式 Task 带入，不接受只转移一句 “PASS”；
5. 若 scratch 已自动清理且只留下 log/digest，不称其为现成代码资产，优先固化可恢复的最小 fixture。

## 8. DomainHarness v0.8 小型反例演练（只能推导边界，不能伪造 Release PASS）

| 已观察事实 | 推荐正确处理 |
| --- | --- |
| #994 物理 Package-owned Kernel 已有 bounded experimental real-code evidence | 在 L2 评估方案和源代码复用；不需要再研究第 N 个 Kernel Demo；保留正式源码审查、安全与真实回归 |
| #972 Approval + Inventory 两种业务事实复用 A/B 有边界正向证据，另发现动态 Effect 缺口 | 产品选择 Kernel Package-first 有条件成立；停止同一 A/B；把 per-request binding 做成正式 L2/Task + negative test |
| PF-02 完成结果读回 scratch 提供可行实现，但裸 query/journal/observe 可绕过权限 | 产品必须承诺经 Host 验证身份、由 Kernel 授权只读结果；正式实现和反例不能省略；无须再建第三个读回实验 |
| ModelPort 数值由 SDK 硬编码、可伪造 | 产品保留“真实计量，否则明确 unmeasured/unsupported”；正式 Host+Kernel observability 在 Task/Release 做，绝不把假 0 当 PASS |
| 新增 DURABLE_MANDATORY 多记录原子收据无当前 Host/K 载体 | **先由 Product Owner 决定是否是本版本初始承诺**；若 OUT，仍必须保留已交付有用持久化/Journal/UNKNOWN/恢复及可选观察；若 IN，真实 K/H 原子与 crash proof 才是 material gate |
| PRD 已多次有界修订，某个旧 HEAD CI 失败而新 HEAD CI 绿 | 一次最终 Owner 范围决策 + exact-new-HEAD 必需 Review/CI；旧 HEAD 的失败继续如实保留，不跨 SHA 偷换，也不因 P2 反复开启整套程序 |

本例仅说明可迁移规则：**Product 决策是否承诺；L2 决定机制；Task 实现；Release 证明运行。** 不能以“少做研究”为名降低未获授权的 caller 身份、Host trust、Effect/Journal 诚实性或释放产物要求。

## 9. 研究退出时的一页交接（可贴到现有 Controller Issue）

~~~text
RESEARCH_EXIT_CARD
OWNER_DECISION=<specific Product/L2 concern and authority>
EXACT_EVIDENCE=<Git refs, cases, real environment, negative cases>
WHAT_PROVEN=<bounded claims>
WHAT_NOT_PROVEN=<material limits>
PRODUCT_SCOPE=IN | OUT | OWNER_DECISION_REQUIRED
ARCH_UNKNOWN=RESOLVED | ADAPT | MATERIAL_BLOCKED
CODE_REUSE=REUSE | ADAPT | REIMPLEMENT | NONE
TEST_REUSE=<exact tracked test/fixture or LOST_SCRATCH>
GATE_NOW=<one actually necessary gate; no invented PASS>
L2_HANDOFF=<owner / contract / invariants>
TASK_DAG_HANDOFF=<implementation concerns + tests once L2 frozen>
CANCELLED_DUPLICATES=<research/Review tasks not to dispatch again>
NEXT_ACTOR=<one owner/Claim key or none>
FREEZE_AUTHORITY=<explicit human/delegated authority, not reviewer>
~~~

### 对抗式最终复问

1. 我们究竟要决定什么？如果现在停止研究，无法作出的决定是哪一个？
2. 最新一次任务改变了方案/范围/安全判断，还是只是增加证据数量？
3. 同一真实机制已有足够确切证据后，下一次 Demo 会不会改变最终选择？
4. 此 P1 是产品范围矛盾、架构重大 UNKNOWN、普通实现缺口，还是仅 Release 验证？
5. 已交付有用功能是否被 “兼容性 OUT” 偷偷删除？
6. 研究产物能否按 Git exact refs 被后续 L2/Task 消费？若不能，缺失资产成本是多少？
7. 当前 GitHub Claim 是否被领取或 Terminal 完成？能否在现有 Issue 中交接，避免重复 Issue 和并发碰撞？
8. 唯一最短合法路径是否已经变成 Product Freeze → L2 → Task DAG？若是，停止生成新的研究任务。

## 10. 采用边界

- 本参考不修改 pinned project baseline、已冻结版本、规范优先级或当前主线的 Claim/Freeze 权限。
- 第一次采用可直接把 §9 的 Exit Card 附加到已有 L1/L2 Controller Issue；无需另建 Issue/Schema/自动化。
- 是否升级成 MUST/SHOULD 的规范性条文，应由 ADS 正式 Product/L2/Review 路径审定，尤其要核对 #186、#680、#931 的 owner 边界及 ADS 当前 Stage 1/Stage 2 规范；不得成为一个新的必过 Gate。
- 如需后续工具化，先用真实 Dogfood 证明它减少了重复研究和到 DAG 的延迟，再考虑调度自动化。
