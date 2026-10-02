# AI Development Standard

当前版本：`v4.1.0`（仅 `version/v4.1.0` 分支的未发布候选）。先前精确候选 `55ca0d25bc27c887963dfb44bcb049a992ec26d2` 曾完成 Candidate Freeze 与 Hidden Validation PASS；Fresh Closeout 随后发现本 README 状态措辞过期，因此 Controller 已 THAW/INVALIDATE，该 Freeze/Hidden 仅作为历史事实、不得转移为修复后 successor 的当前权威。修复合并后的 successor 必须重新完成 visible Stage1 → Candidate Freeze → Hidden Validation → Fresh Closeout → Release Qualification，当前不宣称 successor Freeze、Hidden PASS、Release Qualification、主分支集成或发布。已发布 `main` 仍为 `v4.0.0`；其它并行 version branch 的状态也不得据此推断。采用项目必须将 `version` 与实际选用的不可变 `revision`（40 位提交 SHA）成对固定，不能把本候选元数据或历史门禁结果视为已发布证明。

`ai-development-standard` 是 AI-assisted / multi-agent 软件开发的工程事实、验证、交接与发布标准。目标不是制造更多流程，而是让人、ChatGPT Web、Local Agent、CI、Build Host 和 GitHub 在多会话/多环境下仍共享同一套可恢复事实。

## v4.1.0 候选内容 — Agent Execution Foundation（尚未发布）

v4.1 T01–T08 的实现已合并至 `version/v4.1.0`，新增五个彼此独立的执行治理规范，并通过**非权威** Execution Context 组合，不替代既有 GitHub、Workflow、Validation、Review、CI 或 Release 权威：

- [Dependency & Toolchain Governance](standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md)：依赖、工具链、兼容性与风险例外；风险接受不等于 Validation PASS。
- [Git Execution & Worktree Isolation](standards/GIT_EXECUTION_STANDARD.md)：独立可写工作区、exact-SHA 与危险操作/恢复边界；本地 Git 状态不取得 GitHub Task 权威。
- [Configuration & Secrets Governance](standards/CONFIGURATION_SECRETS_STANDARD.md)：确定性配置优先级、secret reference/value 分离及最小权限。
- [Workspace & Artifact Governance](standards/WORKSPACE_ARTIFACT_STANDARD.md)：工作区、缓存、构建输出、验证证据和发布制品的分类、归属与提升约束。
- [External System Execution](standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md)：外部依赖的真实保真度、环境、状态和副作用授权；低保真结果不冒充高保真验证。

三类新增默认机器契约位于 [`schemas/execution-context-v1.schema.json`](schemas/execution-context-v1.schema.json)、[`schemas/dependency-toolchain-profile-v1.schema.json`](schemas/dependency-toolchain-profile-v1.schema.json)、[`schemas/dependency-risk-exception-v1.schema.json`](schemas/dependency-risk-exception-v1.schema.json)；旧 v4 payload 保持兼容。跨规范索引/渐进采用见 [`docs/implementation/4.1.0/MIGRATION_ADOPTION.md`](docs/implementation/4.1.0/MIGRATION_ADOPTION.md)，T08 的已合并 conformance/dogfood 内容与**非发布性**证明边界见 [`CONFORMANCE_STATUS.md`](docs/implementation/4.1.0/CONFORMANCE_STATUS.md) 和 [`SELF_DOGFOOD_EVIDENCE.md`](docs/implementation/4.1.0/SELF_DOGFOOD_EVIDENCE.md)。候选准备不代表新 SHA 的版本级真实 Build Host Validation 或 Release PASS；其后续门禁由版本级 Controller 独立执行。

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
