# Development Workflow

## 1. 目标

该流程用于让 ChatGPT Web、Codex / Claude Code / 其它 Execution Agent、Build Host 与 GitHub 在不同执行环境中协作，同时保证范围、代码状态、验证结果和发布结论可追踪、可复现、可审计。

v3.0 在 v2.3 GitHub-native Agent Interaction 基线上调整 Independent Review：

- Frozen Task DAG → Task Issues + Issue Dependencies 的 execution DAG materialization 保持不变；
- Issue Dependency 继续作为 canonical live Task DAG；
- Stacked PR 继续仅用于真实未合并 code-baseline dependency；
- Builder / Reviewer / Validator queue 保持；
- Independent Review 从“Version Branch Task/Fix 默认 mandatory”改为 **risk-based / on-demand**；
- 每个 Task/PR 明确 `required / recommended / not-required` Review Policy；
- exact-SHA Review 规则只在 Review 被执行/要求时生效；
- Validation 仍然 mandatory；CI 仍然只是 execution mechanism，不是完整 Validation 或 Release Authority。

完整 GitHub 协作协议见 `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`。

## 2. Intake 时先选择 Integration Mode

### 2.1 Version Branch Mode

Substantial version SHOULD 使用：

```text
main
  └── version/vX.Y.Z
        ├── task/vX.Y.Z-t01-<scope>
        ├── task/vX.Y.Z-t02-<scope>
        ├── fix/vX.Y.Z-<issue>-<scope>
        └── ...
              ↓
        version/vX.Y.Z
              ↓
             main
```

适用于：Frozen PRD/Architecture、多 Task、多 Agent、跨会话、多个 validation environment、Candidate/Hidden Validation/Closure 等场景。

### 2.2 Trunk / Fast Path

小型、低风险、范围明确的 maintenance MAY 使用：

```text
main
  └── task/<scope> or fix/<scope>
          ↓
         main
```

Integration Mode SHOULD 在 Stage 0 记录；若开发过程中复杂度显著增加，可以从 fast path 升级到 Version Branch Mode，但不得为了简化流程而反向破坏既有 candidate/integration facts。

**Integration Mode 不决定 Review 是否 required。** Review 由 Review Policy 单独决定。

## 3. 生命周期

### Stage 0 — Intake / Baseline

确认：

```text
scope
repository
target version/task
integration mode
integration branch / target branch
current default branch
current HEAD
existing PRD/Architecture/Task/Validation/CI state
acceptance criteria
known blockers
required evidence
```

如果任务已经明确且影响小，可以直接进入实现。

如果选择 Version Branch Mode，应尽早建立或确认 `version/vX.Y.Z` 远端 integration branch，使后续正式 checkpoint 与 Task PR 有稳定目标。

### Stage 1 — Product / Scope

Stage 1 把 Idea/Intent 与 Stage 0 Intake/Baseline 的结果收敛为被 Product authority 冻结的产品语义。对 material / new normative Product scope，canonical Stage-1 序列 MUST 可按顺序重构：

```text
Idea/Intent
→ Intake/Baseline（Stage 0）
→ semantic L1 Product Evidence
→ Product Research（as needed）
→ Draft PRD / Scope
→ selected Product Review
→ Product Freeze
```

语义与权威边界：

- **semantic L1 Product Evidence** 是语义框架/证据步骤，回答“解决什么问题、为谁解决、成功标准是什么”。L1 不要求独立成文件，不得被坍缩为强制外部研究。
- **Product Research** 仅当现有/静态证据不足以做出 PRD 决策时按比例选择（as needed），范围与所需决策成比例；它对产品 UNKNOWN 给出 disposition 并综合证据。Product Research 生产 evidence，不持有 Product authority，不构成第二产品权威；其结论由 Product authority 采纳或拒绝。
- **selected Product Review** 是对 Draft PRD / Scope 这一确切 Product subject 的独立 evidence/judgment，不是 universal Product Review gate。它不同于 Stage 2.6 面向 implementation Task/PR 的 Review Policy，也不替代后者。选择规则由 applicable Product/project policy 与风险决定，与 Frozen Product / L2 一致：
  - Product scope 为新/实质变更的 normative、semantic、compatibility-sensitive 或 authority-sensitive 内容，或其它 applicable policy 要求时，Product Review MUST 执行；
  - 低风险/已在既有范围内的 Product Freeze，当无任何 owner 要求时，Product Review 可选择或省略；
  - 适用性 UNKNOWN 或相互矛盾时 fail closed，交给 authority/risk disposition，不得静默降级。
  - 低风险/证据充分的工作在无任何更高权威 owner 要求时，不得被强制加入独立 Product Research 或独立 Product Review，可以保持 compact/inline（与 §7 快速路径一致）。
- **Product Freeze** 是 Product authority 的显式冻结行为，把一个确切 Product subject 绑定为冻结记录；与本文 “PRD / Scope Freeze” 是同一事件，不是新增 gate。Reviewer 可以推荐 Freeze，但 Product Review PASS、研究结论或 Execution Agent 的意见都只是 evidence/judgment，本身不产生冻结效力，不能替代或自动产生 Product Freeze；只有 Product authority（或其授权的 routing rule）授权该 transition 时，Controller 才能确定性地记录 Freeze。
- **Architecture Research / Research Demo 属于 Stage 2**，不得前移到 Product Freeze 之前充当产品发现（product discovery）的替代品。Product Freeze 后若 Architecture Research 发现产品范围不可行/矛盾，走既有 Product thaw/contradiction 路径。

PRD / Scope Freeze 应明确：

- 本版本解决的问题；
- 用户行为 / 业务规则；
- 功能范围与明确不做；
- release blockers；
- required gates；
- acceptance criteria。

冻结后 Execution Agent 不得自行改变产品语义。

#### Stage 1 Checkpoint

PRD Freeze（Product Freeze）和最终被下游依赖的 L1 Evidence MUST 形成远端 checkpoint。

在 Version Branch Mode，默认直接形成 `version/vX.Y.Z` 上的稳定 commit/checkpoint。不要为了每个 Evidence 文件机械创建独立 branch。

只有当 evidence 由另一个 Agent 独立并行生产、需要隔离 review 或存在显著冲突风险时，才 SHOULD 使用临时 docs/evidence branch。

### Stage 2 — Architecture / Task Definition

Stage 2 的目标是从 Frozen PRD / Scope 得到足够可信的 Architecture Evidence，并在高影响 UNKNOWN 被处理后冻结 L2，再形成 Task DAG。

默认流程：

```text
Frozen PRD / Scope
        ↓
L2 Architecture Evidence
        ↓
Architecture UNKNOWN disposition
   ├── static/source/existing evidence sufficient
   ├── executable Research Demo required
   └── BLOCKED / Architecture Contradiction
        ↓
L2 Architecture Freeze
        ↓
Task DAG
```

Research Demo 是按风险启用的 Architecture Evidence，不是每个版本/Task 的 mandatory gate。详细规则见 `standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md`。

#### Stage 2.1 — Architecture UNKNOWN disposition

L2 研究必须明确关键 Architecture Drivers / Invariants，以及仍然存在的高影响 UNKNOWN。

对每个 material UNKNOWN 至少给出一个 disposition：

```text
STATIC_EVIDENCE_SUFFICIENT
EXECUTABLE_DEMO_REQUIRED
BLOCKED
ARCHITECTURE_CONTRADICTION
```

当以下条件同时成立时，应在 L2 Freeze 前创建 Research Demo / Spike：

```text
material architecture assumption remains UNKNOWN
+ it can change architecture / public contract / durability / failure semantics
+ static/source/existing evidence is insufficient
```

如果已有等价 executable evidence、Frozen Architecture 或成熟 project-local evidence 足以证明该假设，不要为了形式重复创建 Demo。

#### Stage 2.2 — Architecture Research Demo / Spike（按需）

需要 executable evidence 时：

```text
Architecture UNKNOWN
→ falsifiable Hypothesis
→ Research Demo Issue
→ isolated research branch
→ positive + negative/failure executable evidence
→ PASS | FAIL | BLOCKED
→ Architecture Decision / L2 update
```

硬规则：

- 被验证的 component/boundary 必须真实；只允许对无关依赖使用 deterministic fake；
- Demo 必须声明 Evidence Strength `E1 | E2 | E3`；
- 结论必须绑定 baseline/dependency/final exact SHAs；
- closeout 必须明确 `What was proven` 和 `What was NOT proven`；
- Demo 是 evidence，不是 production implementation；不得默认 merge 整个 research branch；
- Demo 完成条件是 **Evidence complete**，不是 Feature complete；
- missing production seam 应创建 follow-up Issue，不得静默扩大 research scope。

推荐使用：

- `templates/research-demo-issue.md`
- `templates/research-demo-report.md`
- `checklists/research-demo-validation.md`

PRD Freeze 后如果某个技术方案 FAIL，默认调整候选 Architecture，而不是自动重开 PRD。只有 evidence 表明 Frozen PRD 的产品要求本身 contradiction/unachievable 时，才发布 Architecture Contradiction 并请求重新打开产品范围。

#### Stage 2.3 — L2 Architecture Freeze

只有当：

- 已识别的高影响 Architecture UNKNOWN 有足够 disposition；
- required executable demos 已形成 PASS/FAIL/BLOCKED evidence；
- 被采用架构不依赖伪造或未说明的 UNKNOWN；
- BLOCKED 项已明确是否阻塞 Freeze；

才能把对应 Architecture Facts 标为 Frozen。

Demo PASS 只证明其明确 Hypothesis；不得外推未测试的 distributed scale、performance、security、multi-platform 或 release readiness。

L2 Freeze 后，普通 implementation Task 直接进入 Task DAG/L3/Implementation。只有开发中新发现的高影响 Architecture UNKNOWN 才重新插入局部 Research Demo；不得形成机械的 `Demo → Implementation` 双实现流程。

#### Stage 2.4 — Task DAG

Task DAG 至少明确：

- dependency；
- input/output；
- acceptance；
- required validation；
- Review Policy；
- parallelism；
- risk；
- model/executor suitability；
- intended task branch / integration target when useful。

高风险或低成本模型执行的 Task 可按需增加 L3 Implementation Evidence。证据优先级：

```text
Tests → Contract/Interface → Core Implementation → Failure Handling → Examples/Docs
```

#### Stage 2 Checkpoint

L2、被 L2 采用的 Research Demo Evidence、Task DAG、L3 在成为 implementation dependency 时 MUST 形成 remote checkpoint。

这些属于 stage artifact，默认 checkpoint，不等于一个独立 branch。Research Demo 可使用隔离的 `research_*` branch 以保护实验 write set，但最终应把 exact evidence identity / validated invariant 引用回 L2，而不是把 research branch 当成 integration branch。

#### Stage 2.5 — Execution DAG Materialization

Task DAG Freeze 后，若项目采用 Issue-based execution，应把规划 DAG materialize 到 GitHub：

```text
Frozen Task DAG checkpoint
        ↓
Task Issues
        ↓
Milestone / type / Review Policy / initial state metadata
        ↓
GitHub Issue Dependencies
        ↓
Builder / optional Reviewer / Validator queues
```

规则：

- Planning DAG document = 规划/历史快照；
- GitHub Issue Dependencies = canonical live execution DAG；
- Sub-issue = belongs-to hierarchy，不自动表达 blocked-by；
- 不为 Task DAG 本身创建 branch；
- dependency 发生实质变化时 SHOULD 记录 rationale / `DEPENDENCY_CHANGED` event；
- `templates/task-issue.md` SHOULD 作为 Task Issue contract 基线。

### Stage 2.6 — Review Policy Selection

每个 implementation Task/PR 在 dispatch 前 MUST 明确且仅解析一个 Review Policy：

```text
required
recommended
not-required
```

该 dispatch prerequisite 的 canonical metadata 语义由 `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` §6 持有；本流程不得降低为 SHOULD 或省略。

权威顺序：

```text
Frozen PRD / Contract
→ Frozen Architecture
→ PROJECT_OVERRIDES
→ Task acceptance / risk classification
→ Standard defaults
```

Standard default 是 **risk-based**，不是 always-review。

典型 `required` 场景：

- security/auth/authorization/permissions/secrets；
- public API / schema / migration semantics；
- cross-service contracts；
- concurrency/transactions/data integrity；
- destructive/recovery behavior；
- high-blast-radius integration；
- release blocker / explicit high-risk concern；
- project ownership policy 明确要求的敏感区域。

典型 `recommended`：中等风险行为/集成/重构变更，独立审查有明显价值但不应成为 merge blocker。

典型 `not-required`：docs-only、机械生成、确定性且低风险的局部变更，且项目 policy 允许。

Task/Agent 不得静默降低更高权威已经声明的 `required`。

### Stage 3 — Implementation Concerns

以 Task / Concern 为主要实现与 branch 单位。

原则：

- One concern, one PR；
- 大功能优先拆成 Contract → Core → Integration → UI → Validation；
- 当前环境能完成的代码、测试、fixture、migration、文档与局部验证应尽可能完成；
- 不能执行的内容如实进入 gate 状态，不得默认通过；
- 正式 Concern 达到可合并/可审查状态后形成远端 checkpoint；
- Task DAG 允许时多个 Task branch MAY 并行；
- Builder MAY 在上一个 PR 等待 Review/Validation 时继续其它独立 Task；
- Frozen L2 已提供充分 Architecture Evidence 时直接实现，不为普通 Task 重复 Research Demo；
- 若实现中新发现会改变架构/公共 contract/durability/failure semantics 的高影响 UNKNOWN，暂停受影响 concern 的架构假设，按 `ARCHITECTURE_RESEARCH_DEMO_STANDARD.md` 建立局部 research evidence，再决定 Architecture Amendment / Task change。

Version Branch Mode 推荐：

```text
task/vX.Y.Z-t01-<scope>
task/vX.Y.Z-t02-<scope>
fix/vX.Y.Z-<issue>-<scope>
```

Task/Fix PR 默认 target `version/vX.Y.Z`。

Task branch 应从明确 integration baseline 开始；不得不记录 baseline 就随意从最新 HEAD 开工。

JIT 分支规则（v3.4，详见 `EXECUTION_PACK_STANDARD.md`）：Queued Task 在依赖完成前不应获得长命实现分支。默认顺序是依赖合并 → 重算 ready set → 读取当前 integration exact SHA → **此时**创建 task branch（并 JIT 生成/绑定 Execution Pack）→ 发出 Builder dispatch。只有真实 stacked code dependency 才允许提前建分支。目的是消除 `ahead N / behind M / refresh / revalidate / rereview` 的反复消耗。

#### 3.1 Optional Stacked PR

只有当 Task 的代码必须直接建立在另一个尚未合并的 Task branch 上时，才使用 stacked PR：

```text
version/vX.Y.Z
  ↑
task/T01-contract
  ↑
task/T02-core
```

Stacked PR 只表达 code-baseline dependency：

- Issue Dependency 仍是 canonical Task DAG；
- 不得为了镜像 Task DAG 而人工 stack 所有 PR；
- upstream merge 后，下游 PR 应 rebase/retarget 到正确 parent/integration branch；
- SHA 改变后，受影响的 **required** Review/Validation 必须重新执行。

### Stage 4 — Task Candidate / Minimal CI / Required Validation / Optional Review

Stage 4 的默认顺序必须避免把昂贵 exact-SHA Validation 放在仍可能改变 candidate identity 的 CI/workflow 修复之前。对于存在真实设备、平台、Build Host、Critical Journey 或其它高成本 Task-owned gate 的 concern，默认顺序是：

```text
implementation complete
→ finalize PR + CI/workflow/config
→ cheap/scoped local checks
→ configured Minimal CI on current exact SHA
→ task candidate identity stabilized
→ expensive Task-owned exact-SHA Validation
→ applicable Independent Review
→ merge without further candidate commits
```

如果当前 concern 没有高成本/外部 Validation，这些可执行步骤 MAY 在不破坏 exact identity 的前提下并行；但 merge prerequisites 不变。

CI/workflow/config change 不是默认的 evidence-only commit。它可能改变 execution semantics，因此在昂贵 Validation 之后出现时必须产生 successor identity，并按 `VALIDATION_STANDARD.md` 的 impact rules 处理；不得把旧 tuple PASS 自动改写到新 SHA。

#### 4.1 Candidate Preparation + Cheap / Scoped Validation

先完成 implementation，并执行当前环境中的低成本、concern-scoped checks，例如：

```text
format
lint
typecheck
unit
contract
focused integration
basic build smoke
```

这些 checks 仍须按项目 authority 绑定正确 identity，但它们不应被误写成未执行的真实 platform/device/Critical Journey PASS。

在需要昂贵真实环境 Validation 的 Task 上，PR、CI workflow/config、依赖/lockfile/build inputs SHOULD 在进入昂贵 Validation 前完成定稿。

#### 4.2 PR + Minimal CI Before Expensive Validation

PR 说明：

```text
Task/Issue
baseline
Issue Dependencies
branch strategy independent/stacked
integration target / stack parent
concern scope
changes
cheap/scoped validation evidence
Review Policy / decision
known blockers
required downstream gates
```

CI 默认只做低成本、确定性、clean-checkout 独立复核。默认 Minimal CI SHOULD 只包含：

- standard/project verifier；
- format/lint/typecheck 的必要子集；
- 快速 unit/contract smoke；
- basic build smoke。

默认不把完整多平台矩阵、真实设备/SDK、Critical Journeys、Hidden Validation、高成本 Docker/E2E、packaging 放入 Minimal CI。

项目通过 `.dev-standard/PROJECT_OVERRIDES.md` 声明：

```text
minimal
custom
disabled
```

当 CI enabled 且其 profile 是 Task merge prerequisite 时，SHOULD 在高成本 Task-owned Validation 之前让当前 exact candidate SHA 获得该 CI/profile PASS。若 provider/channel `INFRA_BLOCKED`，只能按 `CI_EXECUTION_STANDARD.md` / `VALIDATION_STANDARD.md` 的 authority 使用合法 alternate executor 或保持 BLOCKED；不得把 pending/stuck provider 当 PASS/FAIL。

`disabled` 必须记录理由，并保留 exact-SHA clean validation。CI disabled 不自动意味着 Review required；Review 仍按 Review Policy 决定。

#### 4.3 Expensive / Real-host Task-owned Validation

只有 candidate 的 implementation、CI/workflow/config 和相关 build/dependency inputs 已稳定后，才 SHOULD 启动该 Task 自身 required 的昂贵真实环境 Validation，例如：

```text
real platform/device/SDK
Build Host runtime/integration
crash/restart/recovery tuple
Task-owned Critical Journey
other high-cost environment-specific gate
```

Validation 必须绑定明确 commit SHA。真实平台/运行时矩阵使用 Validation Tuple：

```text
<exact SHA> × <real platform> × <runtime/toolchain> × <validation profile>
```

Validation remains mandatory according to required gate authority. Review is not a substitute for Validation。

Gate ownership 仍按 `concern | integration | closure` 分层：普通 leaf Task 不自动执行完整 release matrix；只有 frozen Task acceptance/Architecture 明确拥有的平台/runtime/CJ gate 才在这里提前执行。跨组件 truth 由 integration owner 负责，full regression / release CJ / platform matrix / packaging / Hidden 由 version closure 负责。

昂贵 Validation 开始后，SHOULD 避免再向同一 task candidate 加 commit。若 HEAD 仍发生变化，旧 evidence 只属于原 tested SHA；必须按 drift/impact rules 重新建立 affected evidence。

#### 4.4 Independent Review（按需）

Builder 完成 implementation、适用 Minimal CI 和 required Task-owned Validation 后：

- `review:required` → 发布 `IMPLEMENTATION_READY`，route 到 `state:review-ready`；
- `review:recommended + PERFORM` → route 到 `state:review-ready`；
- `review:recommended + SKIP` → 记录 `REVIEW_DECISION`，在其它 merge prerequisites 满足后可进入 `state:merge-ready`；
- `review:not-required` → Review Gate `NOT_APPLICABLE`，在其它 merge prerequisites 满足后可进入 `state:merge-ready`。

当 Review 被选择或 required 时：

- final review context SHOULD 与实现 context 独立；
- 可由另一 ChatGPT session、另一 agent、人类 reviewer，或同模型 fresh context 承担；
- Reviewer 重新读取 pinned standard、Task Issue、Issue Dependencies、Frozen inputs、PR diff、Validation Evidence；
- Review Result 绑定 exact PR HEAD SHA；
- required Review 下 HEAD 变化后旧 PASS 不迁移，执行 delta/full re-review；
- runtime/platform 事实无法静态确认时发 `VALIDATION_REQUEST`，不得猜测。

Reviewer route：

```text
FAIL → state:changes-requested
needs real execution → state:validation-needed
PASS + merge prerequisites satisfied → state:merge-ready
blocked → state:blocked
```

对于 `recommended` Review，如果选择 SKIP，Review Gate 可保持 `NOT_RUN` 且不阻塞 merge；但已经执行的 Review 若发现 release-significant/material finding，不得因为 Review 非 mandatory 而忽略。

推荐使用：

- `prompts/independent-review-bootstrap.md`
- `checklists/pr-review.md`
- `templates/agent-event-comment.md`

#### 4.5 Task Merge Readiness

Task/Fix PR 只有满足以下适用条件才能进入 `state:merge-ready`：

```text
current PR HEAD SHA
+ required concern/task Validation PASS
+ Review condition satisfied
+ configured required Minimal CI/profile PASS when enabled
+ required Issue Dependencies satisfied for merge
+ correct integration target / stack parent
+ no unresolved release-significant finding/blocker
```

Review condition：

```text
required     → Independent Review PASS on current SHA
recommended  → PASS on current SHA OR explicit SKIP decision/rationale
not-required → Review Gate NOT_APPLICABLE
```

Merge controller 在 merge 前 MUST 重新读取 current HEAD/target 并检查 HEAD/BASE/MERGE-RESULT drift。PR merge 后记录 integration SHA / `MERGE_RESULT`，Task completion rule 满足后进入 `state:done`。

#### 4.6 Local Agent Handoff（按需）

当当前环境无法完成真实 build/platform/integration/CJ/Hidden/packaging 或 Reviewer/Task policy 明确要求真实 execution 时，使用 GitHub Issue 交给 Local Agent / Build Host。

新交接 SHOULD 使用：

- `standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`
- `templates/local-agent-handoff-issue.md`
- `prompts/local-agent-bootstrap.md`

Issue 应通过 Milestone + metadata 表达 version、type、state、executor、gate、environment 和 release impact。

Validation Issue MAY 作为 Task 的 sub-issue 表达层级；如果它真正 blocking 另一个 work item/candidate，应使用 Issue Dependency 表达 blocking 关系。

Validation-only execution 不要求 branch。

如果发现必须修改源码或其它 candidate content：

```text
Validation Issue
→ create task/fix branch
→ minimal correct change
→ PR to declared integration branch
→ new exact SHA
→ rerun affected required gates
→ if Review remains required evidence, re-review affected PR HEAD
```

旧 SHA 的 PASS 不自动成为新 SHA 的 PASS。

### Stage 5 — Integrated Baseline / Candidate Preparation

在 integrated `version/vX.Y.Z`、`main` 或项目声明 release branch 上形成候选准备状态。

Version Branch Mode 的 integrated baseline SHOULD 来自 version branch；最终 Version PR 合并 main 之前，所有 version-level evidence 必须明确绑定其 candidate identity。

允许在全部 release gate 完成前先准备：candidate identity、platform matrix、Critical Journey matrix、Hidden Validation pack、closeout checklist、release notes draft、tag/baseline plan。

正确区分：

```text
Candidate Prepared = preparation complete
Candidate Freeze = required visible gates pass on one exact SHA
```

Candidate Prepared PASS 不代表 Candidate Freeze PASS。

### Stage 6 — Candidate Freeze / Hidden Validation / Closure

只有 required visible gates 在同一个 exact candidate SHA 上满足冻结条件后，才能记录 `CANDIDATE_FROZEN_SHA`。

Candidate Freeze 后执行 Hidden Validation。

版本级 Closure 检查：

- required visible Validation；
- Critical Journeys；
- Hidden Validation；
- 真实 platform / production build；
- external boundaries；
- docs / known limitations；
- project-required Minimal CI（若配置为 required）；
- Review evidence only when version/task authority makes it required for closure/merge。

Release Qualification 使用：

- `PASS`：所有 frozen mandatory gates PASS；
- `FAIL`：mandatory gate 已执行并 FAIL；
- `BLOCKED`：mandatory gate 为 BLOCKED/NOT_RUN 或存在 release blocker。

Task Review PASS / PR PASS 不等于 Release PASS。

### Stage 7 — Version PR / Release Baseline / Optional Tag / Release

Version Branch Mode 在 Closure 满足后形成最终 Version PR：

```text
version/vX.Y.Z → main
```

Merge 后 `main` 上的新 immutable commit SHA 成为最终 repository baseline。若 merge/squash 改变 commit identity，必须明确区分：

```text
validated candidate SHA
final main baseline SHA
```

若 release policy 要求 final-main sanity/revalidation，则必须真实执行，不得自动把 version-branch candidate evidence 重写为 main PASS。

只有达到项目 release policy 后才能宣布版本 READY/发布。

必须记录：immutable final baseline commit SHA、standard version + revision、release gate summary、known limitations。

Tag / GitHub Release 是可选的人类友好别名和分发对象，不是 canonical identity。

## 4. Gate Authority

Mandatory Gate 必须能追溯到明确权威来源。优先级：

```text
1. Frozen PRD / Contract
2. Frozen Architecture
3. .dev-standard/PROJECT_OVERRIDES.md
4. Task-specific acceptance
5. Standard defaults
```

Review Policy 使用同一 authority chain。Standard default 不再为所有 Version Branch Tasks 创建 mandatory Review Gate。

以下内容不能自动创建 mandatory release/review gate：历史 workflow、已弃用脚本、旧版本 artifact、Agent 推测、“以前项目都这么做”。

若要新增 mandatory release gate 或强制 Review，必须有相应 authority。

Architecture Research Demo 本身也不是默认 mandatory release gate；它只在 Stage 2 的 material UNKNOWN 需要 executable evidence 时成为 L2 Freeze 的前置证据。

## 5. Blocker Propagation

Blocker 只沿依赖边传播。

示例：

```text
macOS validation BLOCKED
        ↓
Candidate Freeze BLOCKED
        ↓
Hidden Validation Execution NOT_RUN
        ↓
Release Qualification BLOCKED
```

与 macOS gate 无直接依赖的 release notes、Hidden pack preparation、其它平台 validation、candidate preparation 等仍继续。

执行 Agent 不应因为单个 blocker 停止整个版本，只在所有可独立工作耗尽或继续会破坏事实/数据时停止。

## 6. Stage Checkpoint Push

开发流程不要求“每个操作都 push”，而要求正式、稳定、可恢复、可交接的结果形成远端 checkpoint。

至少包括：PRD / Scope Freeze、L1（若成为 downstream evidence）、L2 Architecture Evidence、被 L2 采用的 Research Demo Evidence、Task DAG、L3、可合并/可审查 Task/Concern、integrated version baseline、Validation/Candidate/Closeout、Release baseline 与正式 release artifact。

草稿、临时修复、单次测试运行、局部编辑不要求每一步 push。

Implementation 以 Task / Concern 为远端同步单位；Stage Artifact 以 checkpoint 为单位。

长任务、多 Agent、跨会话任务应使后续可以仅依赖 GitHub commit、Issue、PR、metadata/events 和 pinned standard 恢复，而不是依赖聊天记录。

## 7. 快速路径

Bug、小修复、文档修正、已冻结范围内明确 Task 可跳过 L1/L2/L3，也可不建立 version branch，但不能跳过：

```text
Baseline
→ Implementation
→ required Validation
→ applicable Review Policy decision
→ GitHub fact chain
→ Release impact decision
```

快速路径不为被跳过阶段制造空提交、空 branch、空 Review、空 Research Demo 或形式化 Issue。

## 8. ADS Evolution Feedback / Intake

Implementation, Validation, Review, Incident, Task Learning, dogfood, CI/Build Host and project-operation observations MAY produce evidence for ADS evolution, but observation capture is not standard mutation. Every observation MUST be classified before any promotion decision.

### 8.1 Observation classification and deterministic route

Use exactly one primary class for the current observation:

| Classification | Meaning | Allowed route / disposition |
|---|---|---|
| `PROJECT_DEFECT` | Defect in project code, data, configuration or project-owned contract. | `ROUTE_PROJECT`; fix through the project owner. It does not open an ADS standard change. |
| `AGENT_EXECUTION_DEFECT` | Execution mistake, contract violation, hallucination, write-set drift or other Agent-run defect. | `ROUTE_EXECUTION`; repair/escalate through the existing execution owner. It does not open an ADS standard change. |
| `ENVIRONMENT_OR_TOOL_DEFECT` | Runner, Build Host, CI/provider, network, toolchain or external-tool failure. | `ROUTE_ENVIRONMENT`; route to the applicable environment/tool owner. It does not open an ADS standard change. |
| `PROJECT_SPECIFIC_REQUIREMENT` | Valid requirement that is intentionally local to one project/domain/deployment. | `ROUTE_PROJECT_SPECIFIC`; keep it in project Product/Architecture/Task/override authority. It does not open an ADS standard change. |
| `STANDARD_FRICTION_CANDIDATE` | Evidence that ADS may be causing repeated ambiguity, rework or avoidable friction, but the evidence is not yet sufficient for a normative proposal. | `NO_CHANGE` or `MORE_EVIDENCE`. Any later reclassification to `ADS_EVOLUTION_CANDIDATE` is an explicit new decision, never automatic. |
| `ADS_EVOLUTION_CANDIDATE` | Evidence is sufficient to justify considering a normative ADS change. | `OPEN_ADS_INTAKE`; create an ordinary durable ADS Intake with evidence refs, then use `Intake -> L1 -> PRD -> L2 -> Task -> Review/Validation`. |

Classification is about the observed cause/ownership, not the desired fix. If cause is ambiguous, choose `MORE_EVIDENCE`; do not classify upward to obtain a standard change.

`NO_CHANGE` and `MORE_EVIDENCE` are first-class terminal/current dispositions. `NO_CHANGE` records that the current evidence does not justify a standard change. `MORE_EVIDENCE` records the missing counterexample, reproduction, cross-project diversity, independent challenge, measurement or owner evidence needed before reclassification.

### 8.2 Promotion boundary: ordinary ADS governance only

`ADS_EVOLUTION_CANDIDATE` is not approval and not a mutation authority. The only path that can promote a normative ADS change is the ordinary ADS governance chain:

```text
OPEN_ADS_INTAKE
→ Intake
→ L1 Product Evidence
→ PRD / Scope Freeze
→ L2 Architecture Evidence / Freeze
→ Task DAG / Task
→ Implementation
→ required Validation
→ applicable fresh Review
→ normal integration / release authority
```

Telemetry, model/provider output, scheduler/ranking output, counters, scores, logs, Task Learning records, CI results and dogfood observations MAY be evidence refs only. They MUST NOT edit normative ADS files, mark an evolution candidate approved, or bypass any stage above.

There is no universal numeric promotion threshold. No count, score, success rate, failure rate, cost value, latency value or heuristic can automatically convert `STANDARD_FRICTION_CANDIDATE` into `ADS_EVOLUTION_CANDIDATE` or directly authorize a standard change. Numeric signals are evidence only and remain subject to owner/currentness/counterevidence review.

This feedback path does not replace existing owners: the v4.5 Incident feedback owner remains intact, and the v4.6 Intent/Skill owners remain intact. Incident, Intent and Skill facts may be referenced as evidence, but their canonical semantics and lifecycles stay with those owners.

### 8.3 Privacy / publication classification

Every evolution evidence item MUST carry an explicit publication class before it is copied, quoted or linked outside its source boundary:

```text
PROJECT_PRIVATE
RESTRICTED
PUBLISHABLE
```

Default is fail-closed: absent an explicit `PUBLISHABLE` classification from the applicable source authority, evidence remains `PROJECT_PRIVATE` or `RESTRICTED` and MUST NOT be published as standard evidence. Prefer minimal refs/digests and non-sensitive summaries over copied bodies. Secrets, credentials, private chain-of-thought and hidden-evaluator/Hidden Validation payloads are never publication material.

Changing publication class does not change evidence strength, owner authority or promotion status. A private observation can still lead to `NO_CHANGE`, `MORE_EVIDENCE` or a private ADS Intake; publication is a separate decision.
