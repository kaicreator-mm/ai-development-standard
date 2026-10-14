# ADS v4.12 — 首版机制决策与项目实践归纳 v0.1

> **STATUS: PRODUCT-DIRECTION DECISIONS / NON-NORMATIVE PRD INPUT.** 记录用户对先前未决内容的明确纠偏，并结合 2026-10-14 GitHub 项目实践形成一版拟采用的可执行语义。此处的“v0.1”是 **v4.12 设计方案版本**，不是已冻结 ADS 标准、真实实施或 Release。待 v4.12 PRD 的 Product Authority 正式冻结后，L2 只负责最小表示/集成与机器验证。既有 v4.11 pin **不被追溯修改**。
>
> References: ADS Product Intake [#1096](https://github.com/kaicreator-mm/ai-development-standard/issues/1096), three graphs [#1100](https://github.com/kaicreator-mm/ai-development-standard/issues/1100), risk-bounded [#1099](https://github.com/kaicreator-mm/ai-development-standard/issues/1099), cross-stage contract [PR #1101](https://github.com/kaicreator-mm/ai-development-standard/pull/1101) C01–C15.

## D01 — Bootstrap 是“从零生成/规划阶段完善项目骨架”，不是对已有冻结实现的非法修改

**决策：** v4.12 允许在 **Product Freeze 与 L2 Freeze 之后、完整 Implementation Task DAG Freeze 之前**，由指定 Scaffold 规划参与者，在明确的 L2 工程范围内**创建新项目**（`NEW_PROJECT_INIT`）或仅对既有项目必要的工程骨架做增量完善（`EXISTING_PROJECT_ADAPT`）。这是 **Scaffold Planning 的合法交付行为**，不视为实现某个 DAG Feature Task，也不产生一个新的人工批准 Gate。

- 用户所指的从零生成目录/基础配置、Contract/Schema、模块结构、占位实现、依赖/锁文件、构建入口、测试入口、受限集成骨架属于 **PLANNING_SCAFFOLD**。细节由实际项目复杂性、L2 合同和后续规划逐步决定。
- v4.12 将在 **现有 DEVELOPMENT_WORKFLOW / Work Item/Task 政策内定义阶段行为的正面权限**：`Product_Freeze_ref + L2_Freeze_ref + appointed_planning_owner + permitted_scaffold_scope + GitHub_repository_write_permission + source_ref + version_pin`。无需额外创设一个 Product/Scaffold Freeze 权威、每次代码生成独立 Issue、单独“Bootstrap 许可审批委员会”，更不应因为从零生成就自动 HIGH_ASSURANCE。
- **真实文件创建仍然是 GitHub 源码写入操作**，必须使用有权限的分支/PR、限定创建/更新路径、保留工作者身份/变更来源和实测输出。若多个 Agent 并行修改有重叠工程文件，仍遵守已有唯一写入 owner/已接受 Claim 与互斥/提交治理；创建新项目也不能豁免基本 GitHub 权限和当前项目 pin。
- Scaffold 阶段**不得未经正式 Task 权威**实现对外承诺的业务功能、应用外部不可逆副作用、执行业务迁移、假造真实 Host、绕过必须的安全/信任边界。少量为证明工程结构“可编译/可加载”的可执行胶水由 Scaffold 规划范围涵盖；有真实功能语义/不可逆风险的工作走正式任务/相应权威。
- 如预冻结计划发现 **Frozen L2 的公共契约不成立**，回到 L2 owner 的合法 Architecture Amendment；**不会**让 Scaffold writer 自行重设计。脚手架不应意外在成熟项目中重置现有源码。
- 对仍采用 v4.11 的项目，旧法仍须通过 Frozen Task DAG / T00 实现脚手架：这是 prospective rule；**不是主张现行 v4.11 源码写入限制不存在**。

**结果：** 之前候选材料的 `PRE_DAG_BOOTSTRAP_AUTHORIZATION=P0_PRODUCT_UNKNOWN` 定位更正为 `PRODUCT_RULE_DECIDED; L2_EXISTING_OWNER_INTEGRATION_NEEDED`。L2 要检查如何在同一 Work Item/Writer/Claim 权威内表达和证明该权限，而**不是重新审查用户是否允许创建全新项目**。

## D02 — GitHub 是 Scaffold↔DAG 事实源；版本化映射与双向生成

**决策：** 采用 **GitHub Git objects + Repo versioned files + existing Issues/PR/native Issue Dependencies**，不引入 SQLite/Postgres/图数据库/另一个同步服务。

最小三类事实/一个派生物：

| 事实/投影 | 推荐位置（项目自行调整） | 谁编辑；阶段 |
|---|---|---|
| `Scaffold` 真实工程与 **material anchor list** | 真实 `src/packages/contracts/tests/config`；轻量 `docs/planning/<version>/scaffold-anchors.json`（可由 package manifest/已有 L2 契约导出） | 规划 Scaffold owner 编辑；完整 DAG 冻结前与 DAG draft 共演进；真实 Git blob/tree 是源码事实 |
| Implementation Task DAG **规划事实** | `docs/planning/<version>/TASK_DAG.md` 或受现有 task-dag 模板约束的 `task-dag.json` | 规划 owner 编辑，在配对 Freeze 记录不可变 checkpoint |
| **双向语义映射关系事实** | 每个 Task 在规划表中的唯一 `scaffold_bindings` 字段（`anchor_id + relation + scope`），以及 material scaffold anchor 的唯一稳定 `anchor_id` | Planning/DAG owner 与 Scaffold owner 相互检查，冻结后必须走 owner 的修改/当前性流程；**不手工维护两个映射表** |
| **派生索引（可选提交）** | `docs/planning/<version>/scaffold-task-map.generated.json` + source pointers | 确定性生成器从 Git 已提交的两个事实输入导出；不允许手工修改，产物只能作一致性/查询投影 |

**GitHub 的角色分离：**
- Git Commit SHA、相关 Scaffold subtree/tree digest、源文件与 anchor 的 `path` → **Scaffold 工程事实**；
- 冻结 `TASK_DAG` checkpoint → **规划权威快照**；
- `Issue #`、Task Pack/L3 和 GitHub native `blocked_by` → **materialized execution DAG 事实**，不是 `scaffold-task-map` 内的装饰性阻塞列表；
- GitHub Issues/PRs/accepted review/validation/event/ref → 唯一阶段与实现协调事实；生成器的状态为 **read-only consistency checking**，不能创建/关闭 Issue、Claim、依赖或 Gate PASS。

**推荐 anchor 粒度（避免全源码索引）：** `CONTRACT | MODULE | CAPABILITY | ADAPTER | PUBLIC_API | SHARED_WIRING | TEST_ENTRY | ENVIRONMENT_SEAM | FUTURE_SEAM`。已存在的模块可直接引用。动态 Domain Package/插件优先按 `capability/package id + manifest/ABI` 定位；文件路径不是稳定身份的唯一依据。无需为每个函数/每个生成文件建立一个 anchor。

**关系：** `IMPLEMENTS | CREATES | MODIFIES | CONSUMES | TESTS | INTEGRATES`；可多对多。Task→Scaffold 是实施定位；Scaffold→Task 是 owner/消费者/验证路径反查；`CONSUMES` 不授予公共契约修改权，源码 import 不自动生成 Task `blocked_by`。

### D02.1 输入数据最低契约（候选示例；L2 可以投影到现有模板）

```json
{
  "scaffold_anchors": [
    {"id":"abi.runtime.v1","kind":"CONTRACT","location":"packages/contracts/src/runtime.ts","lifecycle":"STRUCTURAL_READY","owner":"contract"},
    {"id":"runtime.engine","kind":"MODULE","location":"packages/runtime/src/engine.ts","lifecycle":"UNIMPLEMENTED","owner":"T02"},
    {"id":"app.composition","kind":"SHARED_WIRING","location":"packages/app/src/composition.ts","lifecycle":"STRUCTURAL_READY","owner":"T05"},
    {"id":"host.probe","kind":"FUTURE_SEAM","location":null,"lifecycle":"PLANNED_FUTURE","owner":"T03"}
  ],
  "task_bindings": [
    {"task_id":"T02","links":[{"anchor_id":"runtime.engine","relation":"IMPLEMENTS"},{"anchor_id":"abi.runtime.v1","relation":"CONSUMES"}]},
    {"task_id":"T03","links":[{"anchor_id":"host.probe","relation":"CREATES"},{"anchor_id":"abi.runtime.v1","relation":"CONSUMES"}]},
    {"task_id":"T05","links":[{"anchor_id":"app.composition","relation":"INTEGRATES"},{"anchor_id":"abi.runtime.v1","relation":"CONSUMES"}]}
  ]
}
```

**说明：** 示例只是便于沟通的投影，不增加一个强制 `scaffold-task-map` schema；正式结构以 **L2 复用现有 TASK_DAG.md/Task Pack/manifest** 的最小改动为优先。不能把 `STRUCTURAL_READY` 读成已完成的运行时能力或 `Task PASS`。

### D02.2 确定性生成标准（V1）

1. **读取 Git 基线：** 获取当前仓库、version/integration branch、Product Freeze ref、L2 Freeze ref、Scaffold source commit/subtree tree identity、Task DAG draft revision。不要使用 Chat transcript、未提交本地文件、问题评论中的伪造“PASS”当作当前事实。
2. **解析 anchors：** 从明确声明的适用 `manifest/contract file` 或版本化 anchor list 提取稳定 ID、kind、location、owner、lifecycle；检查不存在的路径只能带 `PLANNED_FUTURE`，当前已编译的路径必须实际可解析。Generated-only 文件可由 Bootstrap owner 接管、不要求 Feature Task。
3. **解析 Task：** 从唯一 Draft/Frozen DAG 事实读取 Task ID、Concern、范围、依赖、测试、`scaffold_bindings`；校验 Task ID 唯一、稳定；真实执行 Task 有可核对 Feature/Contract/Validation/Integration 责任，非每接口自动生成 Task。
4. **联结：** 将 `task_id,anchor_id,relation,scope` 正向合并；同一组边反向派生 Anchor→Task，不复制/二次人工维护。关系只代表实现/消费/测试，不代表可自动添加 GitHub native blocked-by。
5. **规范化输出：** 以稳定 ID/关系排序输出 UTF-8、固定字段、明示 `source_inputs`，记录 checker/generator 版本、当前来源 ref 与 `UNKNOWN`；同样输入产生 byte-identical 的派生索引（忽略时间戳/用户环境/随机顺序）。
6. **局部迭代：** Draft 阶段按需增量生成、反馈 mismatch 给 Scaffold/DAG owner；只有 material anchor/currentness 变更才要求重新审查相关关联项。避免每次生成器调用都产生 PR、独立 Review 或新的 Feature Issue。
7. **配对 Freeze：** 源码侧 SF 必须先有已接受的集成版本 SHA/tree。DAG 的最终 freeze checkpoint DF 再引用**这个 SF**。若该 DAG checkpoint 本身使 repo HEAD 前进，比较**Scaffold scope 的 subtree tree/hash**，不得因文档-only commit 改 HEAD 而误判 Scaffold 失效。存储元组 `(source_version_branch, SF_commit, SF_scaffold_tree, DF_checkpoint, mapping_digest_or_ref, L2_ref)`。无需人为追求两个不同文件有同一 SHA。
8. **实施执行：** Freeze 后从该元组派生 Task Pack，materialize native GitHub Issues/Dependencies；Task 在允许的 write set 内新增私有文件时不要求重新创建完整 Scaffold。公共契约或 Task 拓扑实质变化仍走原 owner amendment/impact/currentness。

### D02.3 验证标准（V1，owner-aware、少测试）

**结构检查（deterministic，可在 WEB/repo 环境执行）：**
- `V01` anchor ID & Task ID 唯一、字段合法、关系枚举有效；无悬空 Task/anchor。
- `V02` 不存在的路径只允许标为 `PLANNED_FUTURE`；存在的 critical anchor 与绑定模块/ABI 应正确匹配。
- `V03` material Task 都有可追溯模块/契约/future seam 或正当的 non-code evidence owner；material Scaffold 公共契约有明确 authority owner/消费者/验证者；不会强制每个文件都有 Task。
- `V04` 不兼容的相同文件/契约写集不得被不同“独立并行” Tasks 静默共享；同一 public contract 可以多个 `CONSUMES`，但受控 `MODIFIES`。
- `V05` mapped Task 真实依赖与规划 DAG 一致；`import/includes` 不被投射成 `blocked_by`。由现有 DAG Governance 主导 canonical Issue Dependencies 变更。
- `V06` `UNIMPLEMENTED`/Mock/Stub/NotImplemented 不产出 Feature Test PASS；仅承认实际执行的工程/契约/负例 smoke 与真实错误/skip 状态。
- `V07` 源码结构/ABI Schema 与已冻结 L2 的 critical semantic contract 一致；映射工具只定位并报错，无法凭代码生成推翻 L2 owner。
- `V08` `SF_scaffold_tree` 和 `DF_checkpoint`、mapping source-input tuple/currentness 匹配；未集成 scaffold 分支、本地/过期 HEAD、失配生成索引不能 Freeze。
- `V09` 每个共享集成入口有合法 integration owner、真正的最终连线任务或已被接受的 baseline 证明；只验证“某模块已存在”不证明用户端真正可达。
- `V10` 同一输入重复生成 byte-identical；变更一个 Task 的 PRIVATE link 仅影响实际相关 map 断言，无整仓重跑/新增 Gate。
- `V11` 动态 Package/plugin/tool-call 能按稳定 contract/package identity 建立 Task 责任，即使无静态 imports。
- `V12` UNKNOWN/冲突/权限缺失不产生虚假 `PASS/READY/NOT_APPLICABLE`；与现有 owner 报告的执行 Gate 仍明确隔离。

**来源驱动实际运行（不混为一体）：** 通用 mapping linter 不执行 Full Regression/Hidden/Release；对应 scaffold 的编译/导入/测试应按 L2 所需真实运行环境执行并留下真实命令与 exit/skip 记录。对多 Agent 集成项目，至少一次 **契约/共享接线可达性的最小 smoke**；这个 smoke 不自动证明 E3/业务行为。

**否定用例**：映射文件直接手工更改后重新生成应检测 drift；两个 Task 同写 public contract；一个接口有 6 个 consumers 不误判 6 个 owners；未声明 Future Seam；路径变更但稳定 ID 不变；DAG 文档-only commit 不误判 scaffold tree；已冻结 Task Issue 通过文字更新但 native Issue Dependency 未改变；NotImplemented 仍然编译成功但不算业务能力；未合并 scaffold commit 被错误引用；外部 Host 不可用时仍报告 NOT_RUN。

## D03 — 其他未决事项：采用首版默认策略（从项目实践反推，后续优化）

| 问题 | v4.12 v0.1 默认判定（Product 方向） | 已有项目实践/来源 | 未来只在发现物质问题时优化 |
|---|---|---|---|
| P/A DAG 是否实体化、Issue dependencies | **按阶段独立选 INLINE / BOUNDED_WORKLIST / EXPLICIT_DAG**。L1/L2 可以以同一 GitHub Issue/文档/轻量子任务组织，不默认强制 native GitHub Dependency。只有确有独立调度的真实阻塞才使用原生 blocked-by；正式 Implementation live DAG 才按现有规则材料化 | [ADS #1081](https://github.com/kaicreator-mm/ai-development-standard/issues/1081)、[app8 #72](https://github.com/kaicreator-mm/app8/issues/72)、[domain-harness #999](https://github.com/kaicreator-mm/domain-harness/issues/999) | 需要跨仓库 L1/A 自动调度且证据完整时再加 |
| 自适应深度与风险 | `FAST/STA​NDARD` 是合法执行/assurance 路径；`EXPLORATORY` 是真实未知；`HIGH_ASSURANCE` 是额外真实硬证据，两者可叠加。每阶段独立选择，UNKNOWN 按现有最严格适用规则；**不造数值阈值和固定 Review 轮数** | ADS #1099 / #680；[app8 #92](https://github.com/kaicreator-mm/app8/issues/92) | 从 W4 实际耗时/失败证据学习，无主观评分转权限 |
| 阶段退出与人类权威 | Product owner 明确 Product Freeze，L2 owner 明确 Architecture Freeze；研究/Demo/LLM PASS 不替代；human H2/H3/H4 真实条件依原 owner 的研究协议/授权而定 | [app8 #92](https://github.com/kaicreator-mm/app8/issues/92)；[domain-harness #999](https://github.com/kaicreator-mm/domain-harness/issues/999) | 只补确实有冲突的 owner precedence |
| 产品/架构/源码漂移 | 复用已有 exact-source/Assurance Plan/Release applicability；**局部影响传播**到当前实际消费者，未知的受影响权威动作 BLOCKED/owner 处置，避免重跑无关 Task。冻结后仅合法 amendment | [xDownload #103](https://github.com/kaicreator-mm/xDownload/issues/103) 和 [domain-harness #1023](https://github.com/kaicreator-mm/domain-harness/issues/1023) | 如有真实需求再添加跨仓库被动索引 |
| Agent Steward | **READ-ONLY** 汇总 accepted Claim/依赖/currentness/Review/critical path/merge-ready；`OBSERVE→VERIFY→ROUTE→AUTHORIZED_ACTION→READBACK`。网页模式可由每次显式查询触发；有现有 Local/Controller 的项目可按需派生周期观察，但不要求新后台服务/轮询 Gate。只有现有 actor 才能变更任务与权限 | [runx #355](https://github.com/kaicreator-mm/runx/issues/355) 合法中央 owner、[shun-assistant #10](https://github.com/kaicreator-mm/shun-assistant/issues/10) JIT/Claim | 只在真实停滞不能靠现有事件解决时增加自动化 |
| 任务划分与中途恢复 | one coherent concern，公共契约优先、真实集成单独 owner；JIT 前复查大 Task；ACTIVE 中拆分先检查已有 Claims/写集、不可双重执行；依真实 Task DAG 变更标准修订 | [domain-harness #1013](https://github.com/kaicreator-mm/domain-harness/issues/1013), [runx #355](https://github.com/kaicreator-mm/runx/issues/355), ADS #775/#1072 | 按发生的重复返工根因改进，不要通用 LOC 上限 |
| 环境与实际验证 | 从 L1 记录真实约束，L2 确定 Build/E3/Host；Task 执行时做 capability+工具链 preflight、真实 exit code/skip/cleanup，复用现有 Runx/CI/Validation owner；真实环境不是所有普通 JS/TS Task 的默认要求 | [runx #318](https://github.com/kaicreator-mm/runx/issues/318), [shun-assistant #10](https://github.com/kaicreator-mm/shun-assistant/issues/10) | 有用时增加设备/Host capability profiles |
| 最小人工与在线人类证据 | 对**判断权**采用多 LLM 质疑/确定性工具/必要真人 owner；对**行为证据**优先现有合法受许可的用户讨论、遥测、研究结果，**不可**假装真人盲标或真实任务完成率；不允许向未授权模型上传敏感数据 | [app8 #92](https://github.com/kaicreator-mm/app8/issues/92) | 仅当实证需求无法回答时做最小真人实验 |
| 研究/代码复用 | 来源和许可可证明→复用现有组件/代码/测试和 L2 决策；同一功能已实现但未从产品入口到达，优先**接线而非再研发**；Demo 不冒充运行时 | [xDownload #101](https://github.com/kaicreator-mm/xDownload/issues/101), [domain-harness #1023](https://github.com/kaicreator-mm/domain-harness/issues/1023) | 只有无法复用的真实 Predicate 才生成新任务 |
| 预算与版本收敛 | 关注 **新证据断言、已完成合法 Merge、解除真实阻塞**；聚合同类根因/减少无新证据的 Review、Host 重跑；保持强制 Release gate × exact subject、Hidden/CJ/版本组成证明 | ADS #1092/#803、[app8 #97](https://github.com/kaicreator-mm/app8/issues/97) | 之后基于 W4 事实校准成本，不虚构节省率 |
| Task Learning 与历史采用 | 使用现有 Task Learning v1/v2 source/currentness；无 material learning 则无需记录；项目标准 Pin、Frozen 历史与 Review/E3 负例保持不变，后续仅 prospectively adopt v4.12 | ADS v4.11 EXECUTION_ARCHITECTURE §30；PROJECT_ADOPTION | 只对真正可重复的经验增加可执行 Skill/Recipe |

## D04 — 采用项目实践做验证，不再预研式无止境扩张

1. **新工程对照**：选一个新项目（可从 app8/T01 或简化的 domain-harness Package ABI 迁移案例**离线模拟**）：同一 L2 约束下，生成项目 Scaffold、同步 Draft DAG、双向映射；检查模块接口、契约、Test Entry 和未实现位真实对应。**不要重写已经完成的 v0.8/app8 成果**。
2. **既有工程对照**：用 runx 五条线和 X01 中央融合、xDownload 已有 S1–S6 但用户入口未接通作为**反例**：生成索引应指出缺失 Shared Wiring/实际入口、并标出正确的 Owner。对存在的源码 `REUSE` 而非生成新项目。
3. **动态能力对照**：domain-harness minimal Microkernel + capability-owned package：Package ID/ABI/manifest 能映射多个 runtime/adapters、验证 Task 而不要求逐个静态函数。
4. **合规反例**：app8 的 AI-generated seed ≠ empirical PASS；runx 真实 Host 未执行 ≠ E3 PASS；GitHub native blocked-by ≠ 源码 import；旧 v4.11 pinned 项目不得用新 v4.12 创建规则去回溯 Task DAG。
5. **效果指标**：仅记录能实际观测的 `mapping_mismatch_count, shared_writer_collisions, orphan_material_stubs, integration_rewire_defects, genuine_host_runs, review/rework_rounds, critical_path_unlock`。基线缺失则 `UNKNOWN`，不得宣称已提升多少百分比。
6. **退出条件**：有真实可解析输入、一版轻量双向索引、可重复 V01–V12 与反例、正确的 Authority 边界；**不强制整套图数据库、抓取平台、原型可视化、二次研究 Demo、新真人群体**。验证通过只证明投影与定义相符，不表示功能/版本 Release 通过。

## D05 — 只剩真正需要后续技术细化的边界

- `L2_INTEGRATION`：确定最轻量具体 `scaffold_anchors` 与 `task_bindings` 在已有模板中的编码和生成器放置方式；实施前在 GitHub 中起一个最小脚本 + fixture 或引用已有工具，避免建立服务。
- `L2_INTEGRATION`：明确配置/工具链/lockfile、Source Tree identity 与 DAG 文档冻结 commit 的稳定配对；避免 self-referential SHA 和 docs-only drift 误判。
- `L2_CONFORMANCE`：在合法 v4.12 标准生效前，验证新的规划阶段 Scaffold 写入权限和超范围实现拒绝机制；**不再列为 Product 决策悬案**。
- `CONDITIONAL`：本地真实 Build Host/复杂 Agent 并发/外部不可逆测试只能用真的环境、权限和证据执行；如果没有，把对应验证真实记录为 `NOT_RUN`，不阻塞创建这份 Product 草案。
- `POST_VERSION_FEEDBACK`：等实际项目有测量数据再细调阈值/调度策略/模板位置；不要在 L1 期间新建大量研究 Gate。

**当前姿态：** `PRODUCT_DIRECTION_DECIDED`（不等于 `PRODUCT_FREEZE`）；`L2_IMPLEMENTATION_PROJECTION_OPEN`（不等于`L1_PRODUCT_UNKNOWN`）；`REAL_MACHINE_CONFORMANCE_NOT_RUN`；`V411_HISTORY_UNCHANGED`。
