# AI Development Standard

当前版本：`v4.9.0`（**未发布 version-branch candidate**）

> **v4.9.0 谱系组合声明（lineage composition）**：本仓库当前处于 v4.9.0 working line（`version/v4.9.0` 候选线）的谱系组合状态，由两条已记录谱系真实组合而成：
>
> - **v4.9 working line**：`version/v4.9.0@916dcb66850e33cc2a77a7ef75b0968d5c150ccf`（tree `296878a84c2b2f97f1b6ac6f20edb9a7210435bc`），携带 v4.9 planning baseline 与 v4.9 任务内容（T001/T002 执行记录已并入；该线亦携带已在 v4.9 线完成的 T-005 执行记录）。
> - **integrated current main**：`main@92e4f764a2630a131d3f156b39f0f09064c9849e`（tree `db8cd8185c6206e93512a455a1f9f8b1e121033f`），携带 v4.1–v4.8 全部集成内容（含 v4.3-sequential、v4.8 执行/能力/资格/Dispatch-Claim/Task Learning owner surfaces 与 LG47 registry surfaces）及已并入 `main` 的 v4.9 planning lane。
> - **本次组合（composition）**：将 integrated current main 整体并入 v4.9 working line。`.agent/execution/T-002/` 与 `T-005/` 出现两个程序同路径集的 add/add 历史记录碰撞（v4.9 程序与 v4.8 程序），按 #788 先例处理：working line 所属程序（v4.9）的记录保留 canonical 路径，main 侧 v4.8 程序记录按字节原样（blob SHA 不变）迁移至程序级历史路径 `.agent/execution/_legacy/v4.8/T-002/`、`.agent/execution/_legacy/v4.8/T-005/`；组合未发现需要重绑定的路径引用方。
> - **无断言姿态**：本组合自身不声称 Candidate Freeze、Hidden Validation、Release Qualification、发布 tag、GitHub Release、`main` 集成或其它 publication；任何先前程序对各自候选的 Freeze/Hidden/RQ 结论均属 HISTORICAL_ONLY / NON_TRANSFERABLE，不转移到本组合的新 SHA/tree。v4.1–v4.8 的内容、历史与既存门禁证据全部保全（见下方各节）。
> - **后续门（successor gates）**：本组合须依次通过独立 composition Validation、Fresh Review，再按 expected-head 合并回 `version/v4.9.0`；在此之前不得视为已发布标准。采用项目仍必须将 `version` 与实际选用的不可变 `revision`（40 位提交 SHA）成对固定；其它并行 version branch 的状态不得据此推断。
> - **post-recovery recompose（本次组合）**：recovery-integrated `main@4c632256ce403acdbffc321db5cb086ef3dec7f8`（tree `74d6f0a75991252320e6c1724d3d18b6dd0be32f`，`VERSION=4.8.1`，携带 #805 Path D 恢复的 v4.4–v4.7 语义前驱族）已整体并入本 v4.9 working line（`version/v4.9.0@4322a8cc2a1810e3b49b5a92b502e869ac4c70b6`，tree `0d784280faa00227434ce2e885c40a0c9e999a2a`）；其 v4.8.1 顺序集成谱系声明原样保全于下方。本组合自身不声称 Candidate Freeze、Hidden Validation、Release Qualification、发布 tag、GitHub Release 或其它 publication。
>
> **pre-v4.8 lineage recovery 集成记录（原 recovery-integrated `main` 侧声明，`VERSION=4.8.1`，随本次 post-recovery recompose 原样并入保全）**：
>
> **顺序集成谱系声明（sequential integration composition）**：本仓库当前处于 v4.8.1 血缘恢复集成候选状态，在 v4.8.0 顺序集成基线之上按 #805 Path D 恢复了 v4.4–v4.7 语义前驱谱系：
>
> - **本次组合（v4.8.1 lineage recovery successor）**：按 #805@5987352394 的 Path D 条件授权与 #809@5989016307 精确矩阵（经 BUILDER_MATRIX_AMENDMENT_1@6004888809 修正、DELTA_RE_REVIEW PASS@6005027628），将 `version/v4.4.0-sequential`（`7e162ad5…`）、`version/v4.5.0`（`4366c5fb…`）、`version/v4.6.0`（`4ff6e1c4…`）、`version/v4.7.0`（`d8f61312…`）四个合格前驱中当前 `main`（`92e4f764…` / tree `db8cd818…`）缺失的规范属主、machine contracts、references 与 focused verification 面逐 blob 忠实导入，并按 compose-only-missing-delta 组合 5 个共享面（明细见 CHANGELOG v4.8.1 条目）。历史候选的全部门禁结论 HISTORICAL_ONLY / NON_TRANSFERABLE；本组合自身不声称 Candidate Freeze、Hidden PASS、Release Qualification、`main` 集成、发布 tag、GitHub Release 或其它 publication；在其后续独立 Validation、Fresh Review、版本闭合与集成完成前，本候选不得视为已发布标准。`v4.9.0` 身份与 Task 实现归 v4.9 Controller（#745），不受影响。
> - **v4.3–sequential 已集成基线**：按 #705 的顺序谱系，历史已冻结候选 `version/v4.3.0`（`124943821848260b135a008dfaca6bc05a31fbac` / tree `bad3acb42a6e68e31f8e2f9178ecdeb5b2e8d2f1`）中经资格验证的 v4.3 语义增量（源区间 `65c978d7..124943821`，T01–T11）被语义重放到已资格化的 v4.2 `main`（`73098dfb576dbcc1252634e14bb3d39b70b94342`，经 PR #703 集成）之上，形成 `version/v4.3.0-sequential` 顺序候选，并经 PR #708 集成 `main`，形成 merge commit `f62930bd3512a463358b8b642b1bbc5993566940`（tree `6426f3e691bfc93ce3161c14b89031011fbfffb0`）；v4.1/v4.2/v4.3 内容、历史与既存门禁证据全部保全（见下方各节），v4.9.0 planning lane 亦已并入 `main`。
> - **v4.8 candidate 谱系**：前任 exact candidate `33d409d0a7ec92d4f51079dca2c7e32a229eeec9`（tree `302c00bd8534164649ea6d9ee216390027b1cdcf`）曾在其 exact SHA/tree 上完成 visible Stage 1 R2（#772@5977349861 PASS）、Candidate Freeze（#772@5977362955）与 Private Hidden Validation（#773@5977836575 PASS）；随后针对同一冻结候选的 Fresh Version Closeout（#774@5978216909）给出 `CHANGES_REQUESTED`，发现 release-identity P1，Controller 将该前任候选显式 THAWED/INVALIDATED（#774@5978234079）。修复后的 `version/v4.8.0` 候选线推进至 `0ac1a3d43163271469811c2867ff684f680f7443`（tree `779fde0846ef775c31e8372f969534573aac72f5`），Release Qualification #787@5981189207 对该 **exact SHA/tree** 给出 `READY`。
> - **v4.8.0 组合（前次 integration successor，即本次候选的基线）**：将上述 #787 已资格化的 v4.8 语义增量（与 `main` 的 merge-base `94cad2b0487e8a552c66d6bcd1cba36b7779383d`）忠实重放到 `main` `f62930bd` 之上，形成顺序集成候选并经 PR #787 集成 `main`（merge commit `92e4f764a2630a131d3f156b39f0f09064c9849e` / tree `db8cd8185c6206e93512a455a1f9f8b1e121033f`）。#787 对 v4.8 候选的 Release Qualification/Stage/Freeze/Hidden 结论只绑定该候选的 exact SHA/tree，属 HISTORICAL_ONLY / NON_TRANSFERABLE。采用项目仍必须将 `version` 与实际选用的不可变 `revision`（40 位提交 SHA）成对固定；其它并行 version branch 的状态不得据此推断。
> - v4.8 的 authority/adoption material 见 [PRD](docs/implementation/4.8.0/PRD.md)、[L2 Architecture Evidence](docs/implementation/4.8.0/L2_ARCHITECTURE_EVIDENCE.md)、[Task DAG](docs/implementation/4.8.0/TASK_DAG.md)、[L3 Reference Packs](docs/implementation/4.8.0/L3_REFERENCE_PACKS.md) 与 [Migration/Adoption](docs/implementation/4.8.0/MIGRATION_ADOPTION.md)。

v4.1.0 为已完成 Release Qualification 并集成 `main` 的历史事实：Release Qualification #663 已对精确候选 `d0e133ab5d6a4b328818fdee36a41d994aa41e75`（tree `5ae3f7864f07aadb53c3df260e7d1d543a49d8a1`）给出 `READY`，PR #672 随后将该候选集成至 `main`，形成 merge commit `0882a9fd13506991da255136f1e026f8a8f79e6f`。该次 final-main 元数据校正只修复当时的仓库可见状态，未修改已资格化候选、Frozen Product/L2/DAG、实现、schema、标准、测试或 workflow；v4.1 自身不声称存在发布 tag、GitHub Release 或其它 publication。

`ai-development-standard` 是 AI-assisted / multi-agent 软件开发的工程事实、验证、交接与发布标准。目标不是制造更多流程，而是让人、ChatGPT Web、Local Agent、CI、Build Host 和 GitHub 在多会话/多环境下仍共享同一套可恢复事实。

## v4.3.0 — Engineering Design & Implementation Profiles（未发布顺序谱系候选；未声称 Release Qualification/tag/GitHub Release/publication）

v4.3 以 Engineering Design & Implementation Profiles 为主题，在已资格化的 v4.2 `main` 基线之上重放已冻结 v4.3 候选的语义增量（T01–T11），新增工程设计/规划治理边界与语言中立实现 profile 体系，不替代既有 GitHub、Workflow、Validation、Review、CI 或 Release 权威；GitHub Issue Dependencies 继续作为 canonical live execution DAG，v4.3 不创建第二套执行 truth。v4.3 的既存 authority/adoption 材料见 [`docs/implementation/4.3.0/PRD.md`](docs/implementation/4.3.0/PRD.md)、[`L2_ARCHITECTURE_EVIDENCE.md`](docs/implementation/4.3.0/L2_ARCHITECTURE_EVIDENCE.md)、[`TASK_DAG.md`](docs/implementation/4.3.0/TASK_DAG.md)、[`L3_REFERENCE_PACKS.md`](docs/implementation/4.3.0/L3_REFERENCE_PACKS.md)：

- **工程设计与规划治理**：新增 [`standards/ARCHITECTURE_DESIGN_STANDARD.md`](standards/ARCHITECTURE_DESIGN_STANDARD.md)、[`standards/TASK_DECOMPOSITION_STANDARD.md`](standards/TASK_DECOMPOSITION_STANDARD.md) 与 [`standards/TASK_DAG_GOVERNANCE_STANDARD.md`](standards/TASK_DAG_GOVERNANCE_STANDARD.md)，建立 Architecture Design、Task Decomposition、Task DAG Governance 的明确治理边界；新增 DAG mutation machine contract [`schemas/dag-mutation-record-v1.schema.json`](schemas/dag-mutation-record-v1.schema.json)。
- **实现质量与 profile framework**：新增语言中立 [`standards/IMPLEMENTATION_QUALITY_STANDARD.md`](standards/IMPLEMENTATION_QUALITY_STANDARD.md) 与 profile framework，定义 deterministic applicability/composition、冲突 fail-closed 与 profile/default layering；明确不在 v4.3 引入 repository-wide resolver。
- **Language implementation profiles**：新增 TypeScript、Python、Go、Java、Rust 语言 profile（[`profiles/languages/`](profiles/README.md)），把语言中立要求映射到生态事实；项目通过 explicit pinned profile refs 与 `PROJECT_OVERRIDES` 选择、specialize 或 strengthen，且不得削弱 Frozen/Core authority。
- **Archetype profiles 与采用规则**：新增 `library / service / cli` archetype profiles（[`profiles/archetypes/`](profiles/README.md)）与 profile catalog / progressive adoption 规则；历史 Task/Validation/Review evidence 保持原 subject/authority，不要求 retroactive profile records。
- **参考实现**：新增 [`references/ARCHITECTURE_DECISION_REFERENCE.md`](references/ARCHITECTURE_DECISION_REFERENCE.md)、[`references/TASK_DECOMPOSITION_REFERENCE.md`](references/TASK_DECOMPOSITION_REFERENCE.md)、[`references/TASK_DAG_GOVERNANCE_REFERENCE.md`](references/TASK_DAG_GOVERNANCE_REFERENCE.md)、[`references/IMPLEMENTATION_QUALITY_REFERENCE.md`](references/IMPLEMENTATION_QUALITY_REFERENCE.md) 与 [`references/IMPLEMENTATION_PROFILE_ADOPTION_REFERENCE.md`](references/IMPLEMENTATION_PROFILE_ADOPTION_REFERENCE.md)。
- **Task Pack / Execution Pack 接入**：governance/profile pointers（`authority_refs`、`implementation_profile_refs`、`project_overrides_ref`）只消费已解析的 authority/profile selection，不复制 Task object，也不自行重新解析更高 authority。
- **T10 采用接线与 T11 Conformance/Dogfood**：normative owners、DAG mutation schema、profile catalog、adoption references 与 v4.3 verification surface 接入 `standard-manifest.json`；conformance dogfood 套件、fixtures 与证据见 [`scripts/test_v43_conformance_dogfood.py`](scripts/test_v43_conformance_dogfood.py) 与 [`docs/implementation/4.3.0/dogfood/`](docs/implementation/4.3.0/dogfood/T11_EVIDENCE.md)。
- **谱系与历史保全**：v4.3 增量组合于已资格化 v4.2 `main` 之上，属顺序谱系而非并行重品牌；v4.2.0/v4.1.0/v4.0.0 全部历史条目与既述事实保持不变；历史并行 `version/v4.3.0` 候选（`124943821`）仅作为语义增量来源被引用，其 #690 Stage1/Freeze/Hidden/Closeout/RQ 结论为 HISTORICAL_ONLY / NON_TRANSFERABLE；并行 version branch 的状态不得据此推断。

## v4.2.0 — Evolution Governance（发布准备中；未声称 Release Qualification/tag/GitHub Release/publication）

v4.2 以 Evolution Governance 为主题，在已资格化的 v4.1 基线之上新增两个彼此独立的演进治理规范，并通过可选引用接入既有契约，不替代既有 GitHub、Workflow、Validation、Review、CI 或 Release 权威；v4.2 是 v4 之内的前瞻性增量，历史 payload 与证据保持原有 subject identity，不得因 v4.2 存在而被追溯改标：

- [Interface & Compatibility Governance](standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md)：契约 baseline/candidate 身份、change operations、兼容性维度、consumer/window 证据与 deprecation/removal 义务；schema/checker PASS 不等于行为/源/消费方兼容。
- [Data & Migration Governance](standards/DATA_MIGRATION_GOVERNANCE_STANDARD.md)：directional source→target 持久状态迁移身份、fresh-install 与 upgrade/recovery 的区分、环境适用性与恢复证据；迁移文件存在不等于迁移已执行。

两类新增机器契约位于 [`schemas/compatibility-record-v1.schema.json`](schemas/compatibility-record-v1.schema.json) 与 [`schemas/migration-transition-v1.schema.json`](schemas/migration-transition-v1.schema.json)，旧 v4 payload 保持兼容；参考实现见 [`references/INTERFACE_COMPATIBILITY_REFERENCE.md`](references/INTERFACE_COMPATIBILITY_REFERENCE.md) 与 [`references/DATA_MIGRATION_REFERENCE.md`](references/DATA_MIGRATION_REFERENCE.md)。采用/演进边界见 [`docs/implementation/4.2.0/MIGRATION_ADOPTION.md`](docs/implementation/4.2.0/MIGRATION_ADOPTION.md)，跨规范 conformance 与 closure 输入见 [`CROSS_STANDARD_CONFORMANCE_STATUS.md`](docs/implementation/4.2.0/CROSS_STANDARD_CONFORMANCE_STATUS.md) 与 [`CLOSURE_INPUTS.md`](docs/implementation/4.2.0/CLOSURE_INPUTS.md)。上述内容均不能替代独立版本级 Version Validation、Fresh Review 或发布门禁。

## v4.1.0 — Agent Execution Foundation（已完成 Release Qualification 并集成 `main`；未声称 tag/GitHub Release/publication）

v4.1 T01–T08 的实现已在资格化候选 `d0e133ab5d6a4b328818fdee36a41d994aa41e75` 上完成，并经 PR #672 集成至 `main`。该版本新增五个彼此独立的执行治理规范，并通过**非权威** Execution Context 组合，不替代既有 GitHub、Workflow、Validation、Review、CI 或 Release 权威：

- [Dependency & Toolchain Governance](standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md)：依赖、工具链、兼容性与风险例外；风险接受不等于 Validation PASS。
- [Git Execution & Worktree Isolation](standards/GIT_EXECUTION_STANDARD.md)：独立可写工作区、exact-SHA 与危险操作/恢复边界；本地 Git 状态不取得 GitHub Task 权威。
- [Configuration & Secrets Governance](standards/CONFIGURATION_SECRETS_STANDARD.md)：确定性配置优先级、secret reference/value 分离及最小权限。
- [Workspace & Artifact Governance](standards/WORKSPACE_ARTIFACT_STANDARD.md)：工作区、缓存、构建输出、验证证据和发布制品的分类、归属与提升约束。
- [External System Execution](standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md)：外部依赖的真实保真度、环境、状态和副作用授权；低保真结果不冒充高保真验证。

三类新增默认机器契约位于 [`schemas/execution-context-v1.schema.json`](schemas/execution-context-v1.schema.json)、[`schemas/dependency-toolchain-profile-v1.schema.json`](schemas/dependency-toolchain-profile-v1.schema.json)、[`schemas/dependency-risk-exception-v1.schema.json`](schemas/dependency-risk-exception-v1.schema.json)；旧 v4 payload 保持兼容。跨规范索引/渐进采用见 [`docs/implementation/4.1.0/MIGRATION_ADOPTION.md`](docs/implementation/4.1.0/MIGRATION_ADOPTION.md)，T08 的 conformance/dogfood 内容与证明边界见 [`CONFORMANCE_STATUS.md`](docs/implementation/4.1.0/CONFORMANCE_STATUS.md) 和 [`SELF_DOGFOOD_EVIDENCE.md`](docs/implementation/4.1.0/SELF_DOGFOOD_EVIDENCE.md)。Release Qualification #663 绑定上述精确候选 SHA/tree，PR #672 只执行 Repository Integration；本次 final-main 元数据校正不重做或转移这些证据，也不构成 tag、GitHub Release 或 publication 声明。

## 1. v4.0 的核心变化（已发布历史）

v4.0 在 v3.4 GitHub-native pull 执行模型之上统一引入 **AI Development Operation Protocol + Multi-Agent Assurance**，但不建立第二套生命周期或新的 truth authority：

```text
Durable authority / Work Item
        ↓
Canonical Operation（PRODUCE / RESEARCH / ASSURE / DECIDE / CONTROL）
        ↓
Assurance Plan（Review / Validation / adversarial challenge / coherence）
        ↓
Derived routing / dispatch / interchange correlation
        ↓
exact-subject evidence + orthogonal Gate / Candidate / Release truth
```

要点：

- **Operation 是组合协议，不是新 Source of Truth**：workflow、Gate、Validation、provider、dispatch、candidate、release 继续保持正交，单一 flat state 被禁止。
- **Assurance 是 DAG/partial order**：Review Policy、Review Mode、Coverage、Independence、Aggregation 分离；context/model/executor/evidence independence 分别记录。
- **Multi-model 不等于 Validation**：模型一致不能制造 runtime/platform truth；多数票不能覆盖 unresolved blocker。
- **Agent Interchange 只做 correlation**：传输/交换不能获得 owning authority，GitHub durable facts 和 exact identity 仍是 reference profile。
- **Validation / Freeze / Release 分离**：Review != Validation，Candidate PREPARED != FROZEN，PR PASS != Release PASS，Release READY != Repository Integration complete。
- **Machine contracts fail-closed**：v4 schemas、semantic facade、Golden/Forbidden regressions 对 identity、aggregation、Validation truth、Candidate/Release transitions、Fast Path 等提供机器约束。
- **Reference-flow self-dogfood**：v4 自身经过多轮 blind provider-diverse adversarial review；历史 CHANGES_REQUESTED 保留，最终 PASS 绑定 exact subject 与 durable evidence。
- **渐进采用**：项目可从 `A0_COMPATIBILITY` 到 `A4_FULL_ORCHESTRATION` 逐级采用；adoption level 只改变 implementation surface，不削弱 truth strength。

v3.4 的 Task Pack / Execution Pack、统一 Dispatch、exact-SHA validation、Local-first、Issue Dependency live DAG 与 Fast Path 基线全部保留并兼容。

## 2. 最短阅读路径

大多数项目不需要读完所有文件。

### 做产品/版本开发

1. `standards/DEVELOPMENT_WORKFLOW.md`
2. `standards/EXECUTION_ARCHITECTURE_STANDARD.md`
3. `standards/VALIDATION_STANDARD.md`
4. `standards/RELEASE_STANDARD.md`

### 做 GitHub 多 Agent 协作

- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`
- `standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`
- `standards/EXECUTION_PACK_STANDARD.md`（Task Pack / Execution Pack / dispatch / freedom）

### 做 CI / Build Host

- `standards/CI_EXECUTION_STANDARD.md`
- `standards/CI_RUNNER_CAPABILITY_STANDARD.md`
- `standards/CI_EVIDENCE_STANDARD.md`

### 做测试数据 / Hidden Validation

- `standards/TESTING_STANDARD.md`
- `standards/TEST_DATA_AND_SCENARIO_STANDARD.md`

### L2 有高风险 UNKNOWN

- `standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md`

`standard-manifest.json` 是当前 active asset inventory；`schemas/` 是 machine contract。

## 3. 不变的核心原则

### GitHub 是 durable execution fact source

Chat 是工作空间，不是项目状态数据库。长任务必须能够从 repository、Issue、Issue Dependencies、PR、events、commit SHA 和 evidence 恢复。

### Exact identity

Validation/Review 绑定实际执行/审查的 SHA。不能把旧 SHA、另一个平台、另一个 toolchain 的 PASS 自动写到当前候选。

### Gate Authority

Mandatory Gate 按以下顺序追溯：

```text
Frozen PRD / Contract
→ Frozen Architecture
→ PROJECT_OVERRIDES
→ Task acceptance
→ Standard defaults
```

Agent 不自行扩大 release gate。

### Concern strictness, closure completeness

```text
Task/Concern → 最小严格 affected validation
Integration  → cross-component truth
Closure      → full regression / CJ / platform / package / Hidden / Release
```

PR PASS 不等于 Release PASS。

### Review risk-based

```text
required | recommended | not-required
```

Version Branch Mode 本身不自动让每个 PR 都 mandatory Review。

## 4. 状态分离

不要把以下状态混成一个字段：

```text
workflow routing state
Gate state
CI/provider state
dispatch state
candidate state
release state
```

例如 Woodpecker `INFRA_BLOCKED` 不是 candidate `FAIL`；Candidate `FROZEN` 也不是 release `READY`。

详细定义见 `EXECUTION_ARCHITECTURE_STANDARD.md`。

## 5. Candidate Freeze

Candidate Freeze 在 v3.3 起是 operational immutable state：required visible freeze gates 在一个 exact SHA/tree 上通过后冻结；冻结后不得静默向 candidate ref 写 commit。

需要内容修改时：

```text
FROZEN → THAWED/INVALIDATED → successor → affected validation → new freeze
```

Hidden Validation、Release Qualification、Repository Integration 都重新检查 freeze SHA + tree。

## 6. CI 与真实 Validation

CI provider 是执行渠道，不是 Validation/Release Authority。

当项目要求的是 validation profile、而不是某个 provider attestation 时，CI 基础设施故障可以由等价/更强的 trusted clean exact-SHA executor 替代；替代必须留 `CI_INFRA_EXCEPTION`/等价证据。

Provider-specific requirement 则不能静默替代。

## 7. Handoff / 调度

完成的 Local Agent Handoff Issue 应先成为 `HANDOFF_READY`，之后调用只需要：

```text
Repository: owner/repo
Handoff Issue: #N
Role: validator
Dispatch: <id>
```

不要再在 chat 中复制第二份长 Task Contract。

新 structured Agent event 统一写 `ai-dev:event:v2`。历史 v1 只读兼容，不再用于新写入。

## 8. Progressive adoption

v4 的 adoption level 只描述项目实际启用多少协议/自动化能力，不降低任何 mandatory truth/gate：

```text
A0_COMPATIBILITY       v3.4-compatible durable facts + v4 pin
A1_MANUAL_PROTOCOL     手工记录 v4 Operation / Assurance durable facts
A2_MACHINE_CONTRACTS   adopted records 实际经过 schema / semantic verification
A3_DERIVED_AUTOMATION  reducer / routing / controllers 从 durable facts 派生运行
A4_FULL_ORCHESTRATION  项目需要的完整 Operation / Assurance / Interchange automation
```

项目可以长期停留在任何满足自身需求的 level；A0/A1 不要求部署 reducer/controller，也不能被当作跳过 required Validation/Review/Freeze/Release gate 的依据。

详细迁移/override 规则见 `standards/PROJECT_ADOPTION.md` 与 `docs/implementation/4.0.0/MIGRATION_ADOPTION_GUIDE.md`。

## 9. Project adoption

项目至少 pin immutable standard identity，并维护：

```text
.dev-standard/VERSION
.dev-standard/PROJECT_OVERRIDES.md
AGENTS.md
```

校验：

```bash
python scripts/verify_project_standard.py <project> --standard-repo <local-standard-checkout> --require-resolution
python scripts/verify_project_execution_profile.py <project>
```

标准仓库自验证：

```bash
python scripts/verify_standard.py
python scripts/test_verify_standard.py
python scripts/test_verify_project_standard.py
python scripts/test_project_execution_profile.py
python scripts/test_protocol_schemas.py
python scripts/test_v33_lifecycle_contracts.py
python scripts/test_v33_semantic_regressions.py
python scripts/test_v34_lifecycle_contracts.py
python scripts/test_v34_review_repairs.py
python scripts/test_v40_operation_contracts.py
python scripts/test_v40_adoption_migration.py
python scripts/test_v40_reference_flows.py
python scripts/test_execution_architecture.py
python scripts/verify_runner_capability_reference.py
```

## 10. Compatibility cleanup

`GITHUB_WORKFLOW.md` 与 `VERSION_INTEGRATION_WORKFLOW.md` 保留稳定路径，但从 v3.3 起只作为导航/兼容入口，不再复制整套规范。这样避免同一规则在三份文档中漂移。

Legacy Codex-specific handoff 仍可兼容；新任务优先使用 generic Local Agent Handoff。

## 11. Source of Truth

- repository `main` + immutable pinned revision = standard content authority；
- `standard-manifest.json` = active asset inventory；
- `schemas/` = machine contracts；
- project Frozen PRD/Architecture/Overrides = project-specific higher authority where applicable。
