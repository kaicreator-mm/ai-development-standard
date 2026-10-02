# AI Development Standard

当前版本：`v4.7.0`（**未发布 version-branch candidate**）

> `version/v4.7.0` 当前仅表示依赖完整、等待后续 Fresh Independent Review、visible Stage 1 与 Version Closure 的候选线。前任 exact candidate `aae25661feb39f8c77ec59a254790cf04e430b67` 曾在其 exact SHA/tree 上完成 visible Stage 1（#682 Phase 1 PASS）、Candidate Freeze 与 Private Hidden Validation（hidden-validation#41 PASS）；随后针对同一冻结候选的 Fresh Version Closeout（#682 Phase 2）给出 `CHANGES_REQUESTED`，发现 release-identity P1（VERSION/README/CHANGELOG 仍停留在 v4.0.0 旧身份，与 `standards/PROJECT_ADOPTION.md` 的 immutable 采用解析契约冲突），Controller 将该前任候选显式 THAWED/INVALIDATED。前任的 Stage 1/Freeze/Hidden/Closeout 均只是前任 exact SHA/tree 的历史事实，**不转移**到修复后的 successor；当前 successor 不声明 Candidate Freeze、Hidden PASS、Release Qualification、tag、GitHub Release 或正式发布。发布前必须重新完成 **Fresh Independent Review → expected-head merge → exact merged SHA 上的 visible Stage 1 → 新的 Candidate Freeze → required Hidden Validation → Fresh Version Closeout → Release Qualification**。v4.7 的 authority/adoption material 见 [PRD](docs/implementation/4.7.0/PRD.md)、[L2 Architecture Evidence](docs/implementation/4.7.0/L2_ARCHITECTURE_EVIDENCE.md)、[Task DAG](docs/implementation/4.7.0/TASK_DAG.md)、[L3 Reference Packs](docs/implementation/4.7.0/L3_REFERENCE_PACKS.md) 与 [Migration/Adoption](docs/implementation/4.7.0/MIGRATION_ADOPTION.md)。`v4.1`–`v4.6` 为并行版本线，其分支/资料存在不得推导为已发布或已集成到 `main`。

`ai-development-standard` 是 AI-assisted / multi-agent 软件开发的工程事实、验证、交接与发布标准。目标不是制造更多流程，而是让人、ChatGPT Web、Local Agent、CI、Build Host 和 GitHub 在多会话/多环境下仍共享同一套可恢复事实。

## 1. v4.7 candidate 的已集成范围

v4.7 是 v4 系列的 **AI-native Development Convergence** 收敛版本：让没有任何历史 chat 的 capable Agent 仅凭 durable repository/GitHub facts 确定适用的 normative owners、当前 authority/state dimensions、machine contracts/profiles、允许的自主性与所需 evidence，然后正确执行或升级。当前 version branch 已按 Frozen Product/Architecture authority 集成 T01–T10；Task 完成不等于版本级 Release PASS。

- **T01 — Convergence Metadata Contracts**：新增 `schemas/authority-applicability-entry-v1.schema.json` 与 `schemas/state-dimension-registry-v1.schema.json` 两类 machine contracts 及聚焦 schema/向后兼容测试（`scripts/test_v47_convergence_metadata_contracts.py`）；authority/applicability 与 state-dimension 引用事实保持正交。
- **T02 — Authority / Applicability Manifest Registry**：在 canonical `standard-manifest.json` 中增量加入 `semantic_authorities` registry metadata，并新增 owner/applicability 一致性测试（`scripts/test_v47_authority_registry.py`）；registry 只指向 normative owners，不授予 mutation authority，既有 `sections` consumers 保持兼容。
- **T03 — State-Dimension / Forbidden-Inference Registry**：新增 `registries/state-dimensions-v1.json` 与 `scripts/test_v47_state_dimension_registry.py`，提供 qualified state dimensions 与 forbidden cross-dimension inference rules 的 canonical registry data；不拥有 live state values、transitions 或通用 PASS/READY/BLOCKED 语义。
- **T04 — Reference Convention Standard**：新增 `standards/REFERENCE_CONVENTION_STANDARD.md`、`references/REFERENCE_CONVENTION_REFERENCE.md` 与 `scripts/test_v47_reference_conventions.py`，覆盖兼容 subject identity、exact SHA/base、authority refs、evidence refs 与 provenance pointers；不引入 mandatory universal Subject/Authority object，不做历史 schema 重写。
- **T05 — Progressive Disclosure Routing**：新增 `references/PROGRESSIVE_DISCLOSURE_ROUTING.md` 与 `scripts/test_v47_progressive_disclosure.py`，派生组合 AGENTS、pinned ADS、manifest registry、PROJECT_OVERRIDES、profiles 与 exact Task/Execution authority 的读取路由；不建立 Context Snapshot 数据库或新 authority store。
- **T06 — Compatibility / Alias Conformance**：新增 `references/COMPATIBILITY_ALIAS_CONFORMANCE.md` 与 `scripts/test_v47_compatibility_aliases.py`，约束 canonical target 解析、normative owner 唯一性、cycle/broken-target 检测与 evidence-driven path migration posture；不要求物理仓库重构。
- **T07 — Unified Semantic Conformance**：新增 `scripts/test_v47_semantic_conformance.py`（含 `scripts/v47_conformance.py`）与 `references/V47_SEMANTIC_CONFORMANCE_MATRIX.md`，提供 owner 唯一性、mutation authority、state non-inference、exact identity/currentness、profile 解析、machine/prose 一致性与兼容历史的跨标准语义 conformance；不新增 Convergence PASS state family。
- **T08 — Fresh-Agent Self-Dogfood**：`docs/implementation/4.7.0/dogfood/`（`reconstruction.json` 等）与 `scripts/test_v47_fresh_agent_dogfood.py` 提供可复现 dogfood，证明 durable facts 的 reconstruction contract、fidelity separation、stale-subject rejection 与 durable-only bootstrap expectations；committed fixture 刻意标注 `STATIC_OR_RECONSTRUCTION`（`authority_effect=NONE`、`gate_effect=NONE`、`real_fresh_session=NOT_RUN`），REAL fresh-session 场景仍需独立 exact-subject Validation。
- **T09 — Adoption / Migration Wiring**：新增 `docs/implementation/4.7.0/MIGRATION_ADOPTION.md`（`AUTHORITY_EFFECT=NONE`）、`docs/implementation/4.7.0/FUTURE_MAJOR_REGISTER.md` 集成与 `scripts/test_v47_adoption_wiring.py`，只做选定的中心 adoption/migration wiring；不复制 owner 语义，无独立 evidence/authority 不做物理路径迁移。
- **T10 — Cross-standard Closure Inputs**：新增 `docs/implementation/4.7.0/CLOSURE_INPUTS.md`、`scripts/test_v47_cross_standard_closure.py` 与 `references/V47_CLOSURE_CONFORMANCE_REFERENCE.md`，整合 v4.1–v4.7 forbidden-inference regression、historical compatibility、Fast Path proportionality、fresh-Agent reconstruction evidence summary 与 durable Version Closure inputs；仅服务后续 Version Closure，不能自身产生 Freeze、Release Qualification 或 Release verdict。

当前候选只总结实际落库的 standards、schemas、references、registries、tests、dogfood 与 adoption/wiring；没有记录或推导生产 Agent 运行、真实 fresh-session 执行、production deployment 或 release readiness 证据。

v4.7 的冻结产品/架构/任务 authority 位于 `docs/implementation/4.7.0/PRD.md`、`L2_ARCHITECTURE_EVIDENCE.md`、`TASK_DAG.md`、`L3_REFERENCE_PACKS.md`。后续发布判定仍以 `standards/RELEASE_STANDARD.md` 与 `checklists/version-closure.md` 为准。

## 2. v4.0 的核心变化（历史已发布基线）

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

## 3. 最短阅读路径

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

## 4. 不变的核心原则

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

## 5. 状态分离

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

## 6. Candidate Freeze

Candidate Freeze 在 v3.3 起是 operational immutable state：required visible freeze gates 在一个 exact SHA/tree 上通过后冻结；冻结后不得静默向 candidate ref 写 commit。

需要内容修改时：

```text
FROZEN → THAWED/INVALIDATED → successor → affected validation → new freeze
```

Hidden Validation、Release Qualification、Repository Integration 都重新检查 freeze SHA + tree。

## 7. CI 与真实 Validation

CI provider 是执行渠道，不是 Validation/Release Authority。

当项目要求的是 validation profile、而不是某个 provider attestation 时，CI 基础设施故障可以由等价/更强的 trusted clean exact-SHA executor 替代；替代必须留 `CI_INFRA_EXCEPTION`/等价证据。

Provider-specific requirement 则不能静默替代。

## 8. Handoff / 调度

完成的 Local Agent Handoff Issue 应先成为 `HANDOFF_READY`，之后调用只需要：

```text
Repository: owner/repo
Handoff Issue: #N
Role: validator
Dispatch: <id>
```

不要再在 chat 中复制第二份长 Task Contract。

新 structured Agent event 统一写 `ai-dev:event:v2`。历史 v1 只读兼容，不再用于新写入。

## 9. Progressive adoption

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

## 10. Project adoption

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

## 11. Compatibility cleanup

`GITHUB_WORKFLOW.md` 与 `VERSION_INTEGRATION_WORKFLOW.md` 保留稳定路径，但从 v3.3 起只作为导航/兼容入口，不再复制整套规范。这样避免同一规则在三份文档中漂移。

Legacy Codex-specific handoff 仍可兼容；新任务优先使用 generic Local Agent Handoff。

## 12. Source of Truth

- repository `main` + immutable pinned revision = standard content authority；
- `standard-manifest.json` = active asset inventory；
- `schemas/` = machine contracts；
- project Frozen PRD/Architecture/Overrides = project-specific higher authority where applicable。
