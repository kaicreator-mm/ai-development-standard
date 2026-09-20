# AI Development Standard

当前版本：`v3.3.0`

`ai-development-standard` 是 AI-assisted / multi-agent 软件开发的工程事实、验证、交接与发布标准。目标不是制造更多流程，而是让人、ChatGPT Web、Local Agent、CI、Build Host 和 GitHub 在多会话/多环境下仍共享同一套可恢复事实。

## 1. v3.3 的核心变化

v3.3 把标准从“主要靠 Agent 阅读规范后自行推断下一步”推进到“规范 + machine contracts + 可重建 derived state”。

```text
Frozen Planning Facts
        ↓
GitHub Execution DAG
        ↓
Event + Fact Reducer
        ↓
Derived Execution State / Ready Queues
        ↓
Builder / Reviewer / Validator
        ↓
Merge Controller
        ↓
Integrated Candidate
        ↓
Visible Closure
        ↓
CANDIDATE_FROZEN
        ↓
Hidden Validation
        ↓
Release Controller
        ↓
Repository Integration
        ↓
Immutable Baseline
```

自动 runtime 是**可选**的。项目可以人工执行完全相同的状态规则；小型维护仍可使用 Trunk/Fast Path。

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

## 4. v3.3 的状态分离

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

Candidate Freeze 在 v3.3 是 operational immutable state：required visible freeze gates 在一个 exact SHA/tree 上通过后冻结；冻结后不得静默向 candidate ref 写 commit。

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

```text
Level 0  manual standard
Level 1  schemas + verifier
Level 2  reducer + state card
Level 3  ready queues + pointer-only dispatch
Level 4  bounded merge/freeze/release controllers
Level 5  optional automated delivery adapters
```

浏览器自动化、Playwright、特定 CI/dispatcher 都不是标准强制组件。

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
python scripts/test_execution_architecture.py
python scripts/verify_runner_capability_reference.py
```

## 10. Compatibility cleanup

`GITHUB_WORKFLOW.md` 与 `VERSION_INTEGRATION_WORKFLOW.md` 保留稳定路径，但从 v3.3 起只作为导航/兼容入口，不再复制整套规范。这样避免同一规则在三份文档中漂移。

Legacy Codex-specific handoff 仍可兼容；新任务优先使用 generic Local Agent Handoff。

## 11. Source of Truth

- repository `main` + immutable pinned revision = standard content authority;
- `standard-manifest.json` = active asset inventory;
- `schemas/` = machine contracts;
- project Frozen PRD/Architecture/Overrides = project-specific higher authority where applicable.
