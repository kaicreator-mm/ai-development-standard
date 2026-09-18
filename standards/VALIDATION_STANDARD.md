# Validation Standard

## 1. 状态枚举与语义

每个 Gate 只能使用：

- `PASS` = gate 已实际执行，且满足该 gate 的 acceptance criteria。
- `FAIL` = gate 已实际执行，但结果不满足 acceptance criteria。
- `BLOCKED` = gate 因前置条件、权限、工具、环境或标准缺陷无法完成。
- `NOT_RUN` = gate 尚未执行。
- `NOT_APPLICABLE` = gate 对当前 project/change 确实不适用。

不要使用“应该没问题”“基本通过”等不可审计描述，也不要把不同层级的状态压成一个值。

mandatory downstream gate 仍是 `NOT_RUN` 时，该 gate 保持 `NOT_RUN`；依赖它的 Release Qualification 通常为 `BLOCKED`，而不是把未执行 gate 改写成 `FAIL`。

## 2. Validation 与执行器分离

Validation 是工程要求；执行器只是实现方式。

允许的执行器包括但不限于：

- ChatGPT 可执行环境；
- Codex / coding agent；
- Ubuntu Build Host；
- Windows workstation；
- macOS host；
- self-hosted runner；
- GitHub Actions；
- 其它可信 clean execution environment。

是否使用 CI 不改变 required gate 的 acceptance criteria。

任何 PASS 都必须来自真实执行证据，不能来自执行器名称、workflow 存在、cross-build 或 Agent 推测。

当执行器是 CI / automated runner 时，provider/backend/runner/workflow/runtime 的执行语义 SHOULD 遵循 `CI_EXECUTION_STANDARD.md`。CI workflow 语法必须按真实 backend 解释，不能把另一个 backend 的 container/local/host 语义直接套用。

## 3. Required Gate Authority

Mandatory Gate 必须有可追溯来源。优先级：

```text
1. Frozen PRD / Product Contract
2. Frozen Architecture / Technical Contract
3. .dev-standard/PROJECT_OVERRIDES.md
4. Task-specific acceptance
5. Standard defaults
```

历史 workflow、旧脚本、旧 artifact、旧 CI matrix 或 Agent 建议不能自动创建 mandatory release gate。

如果需要新增 mandatory gate，应修改其上游冻结权威并留下审计记录。

## 4. Validation Tuple

矩阵验证的最小证据单元是 Validation Tuple：

```text
<exact SHA>
× <real platform/environment>
× <runtime/toolchain>
× <validation profile>
```

示例：

```text
abc123... × Ubuntu 24.04 × Go 1.26 × visible-release
abc123... × Ubuntu 24.04 × Go 1.27 × visible-release
```

规则：

1. 一个 tuple 的 PASS 只证明该 tuple。
2. 一个 toolchain PASS 不得推导另一 toolchain PASS。
3. cross-build 不等价于真实 platform execution。
4. platform/matrix 聚合 PASS 必须由其 required tuples 全部 PASS 得出。
5. 如果 candidate SHA 变化，旧 SHA 的 tuple evidence 不能自动迁移成新 candidate PASS。

CI 的 provider/backend/workflow identity 属于 execution provenance，不替代这个 tuple；但当这些执行配置会改变实际执行语义时，Evidence SHOULD 一并记录。

## 5. Gate 分层

### A. Fast Gate

通常包括：format、lint、typecheck、unit、contract smoke、basic build。

目标：快速发现局部回归，适合每个 Task/Concern。

### B. Integration Gate

验证 API、DB、queue、filesystem、frontend-backend、external boundary mock/stub 等组合行为。

### C. Critical Journey Gate

基于真实用户路径验证关键业务闭环。不是单个 API 测试的替代品。

### D. Hidden Validation

使用实现 Agent 在开发阶段不依赖其具体答案的独立数据/场景，验证正常路径、边界、错误处理、failure injection、rollback 和关键不变量。

Hidden Validation 默认在 Candidate Freeze 后执行。Pack/design 可以提前准备，但 `Hidden Validation Execution` 不得在未冻结 candidate 上伪造 PASS。

### E. Platform / Production Build

按项目需要验证真实 OS、SDK、device、container、browser bundle、release build 或其它生产环境。

### F. Minimal CI Gate

CI 是低成本、clean-checkout 的独立复核层，不是完整 Validation 的替代品。

默认 Minimal CI SHOULD 包含：

- execution environment preflight；
- standard/project verifier；
- format/lint/typecheck 的必要确定性子集；
- 快速 unit/contract smoke；
- basic build smoke。

默认 Minimal CI SHOULD NOT 承载：

- 完整多平台矩阵；
- 真实设备/SDK；
- Critical Journeys；
- Hidden Validation；
- 高成本 E2E；
- release packaging。

项目在 `.dev-standard/PROJECT_OVERRIDES.md` 声明 CI profile：

```text
minimal
custom
disabled
```

- `minimal`：采用默认低成本 profile；
- `custom`：明确列出项目需要的最小独立 checks；
- `disabled`：明确不使用 CI，并记录原因；必须保留 exact-SHA clean validation + review。

启用 CI 时，项目 SHOULD 同时声明 `CI_EXECUTION_STANDARD.md` 所要求的 execution profile。CI profile 的选择不能降低 frozen product/release validation。

## 6. Required Gate 的确定

Task DAG、PRD 或项目 override 应明确 required gates。

如果没有显式声明，至少要求：

- Fast Gate；
- 与修改范围相关的 Integration/Build Gate；
- 项目配置的 Minimal CI（若 CI profile 不是 disabled）。

版本 Closure 根据 frozen authority 还可能要求：

- Critical Journey；
- Hidden Validation；
- Platform / Production Build；
- external boundary；
- project-specific release gates。

CI 不自动成为 Release Qualification blocker；只有 frozen/project policy 明确把某个 CI gate 列为 release-required 时，它才是版本级 mandatory gate。

## 7. Exact-SHA Evidence

Validation Report 应尽量记录：

```text
repository
tested SHA
branch/ref（辅助信息）
execution host role
OS/platform
architecture
runtime/toolchain
validation profile
exact command
start/end timestamp
exit code
key logs
state
```

如果 report commit 晚于被测试 commit，必须区分：

```text
tested checkpoint = <sha>
evidence-only head = <sha>
```

不得把 working-tree PASS 宣称为未实际执行的 commit SHA PASS。

对 CI run，还 SHOULD 核对 provider run tested SHA 与当前请求 SHA 是否一致。旧 pipeline 的 rerun/restart 只证明其原有 run subject；不得用旧 SHA 的 rerun 作为新 PR HEAD 的 PASS。

当 CI/自动化 Validation Evidence 发布到外部 artifact store 时，SHOULD 遵循 `CI_EVIDENCE_STANDARD.md`：immutable run 必须绑定 exact SHA，`validation-summary.json` 必须保留 Validation Tuple 和五状态 Gate 语义；`latest.json` 只能作为 discovery pointer，不能替代 exact-SHA evidence lookup。

## 8. Blocker Propagation

`BLOCKED` 只沿依赖边传播。

一个 gate BLOCKED 时：

1. 标记该 gate 与直接依赖的 downstream state；
2. 记录原因和 release impact；
3. 继续执行所有不依赖该 gate 的工作；
4. 不重复无意义 retry；
5. 最后统一统计。

示例：

```text
macOS tuple BLOCKED
→ Candidate Freeze BLOCKED
→ Hidden Validation Execution NOT_RUN
→ Release Qualification BLOCKED
```

但 Candidate Preparation、Hidden Pack Preparation、其它平台 validation、release notes 等仍应继续。

## 9. 失败与阻塞证据

FAIL/BLOCKED 应尽量记录：

- failing / blocked command or job；
- exit code（若 command 实际启动）；
- 关键日志；
- reproduction；
- expected vs actual；
- root cause（若已知）；
- affected Task/version；
- downstream blocking level。

对于 `NOT_RUN` 的 mandatory gate，应记录未执行原因和 downstream impact。

CI execution/configuration failure（例如 backend 下配置了不存在的本地 executable）不得写成项目测试 PASS。若 runner/environment 本身因外部前置条件当前无法建立，则按真实状态使用 `BLOCKED`/`NOT_RUN`，不要为了“CI 红”而改变 required gate 语义。

外部 Evidence Contract 中的 `completion.json` 只表示 publication COMPLETE。即使 Validation 为 `FAIL/BLOCKED/NOT_RUN`，只要 evidence truthfully 完整发布，仍可以存在 `completion.json`；不得把 publication complete 误写为 Validation PASS。

## 10. CI Execution Contract

当项目启用 CI，使用 [`CI_EXECUTION_STANDARD.md`](CI_EXECUTION_STANDARD.md) 声明/验证：

```text
provider
backend / execution model
runner role
workflow config identity/source
shell / entrypoint model
runtime/toolchain source
clone/checkout semantics when material
fresh-run / rerun semantics
```

推荐执行顺序：

```text
clean checkout
→ environment preflight
→ bootstrap
→ project/standard verifier
→ cheap deterministic checks
→ evidence publication when configured
```

provider status 和 pipeline restart 行为不能替代 exact-SHA identity 检查。

## 11. CI Evidence Contract

当项目需要让 CI Evidence 可被 ChatGPT、Agent、Release tooling 或其它消费者稳定读取时，使用 [`CI_EVIDENCE_STANDARD.md`](CI_EVIDENCE_STANDARD.md)。

最小职责分离：

```text
latest.json             = mutable discovery pointer
manifest.json           = immutable evidence identity root
validation-summary.json = immutable machine-readable Validation Report
SHA256SUMS              = immutable integrity inventory
completion.json         = immutable evidence publication commit marker
```

推荐 consumer 顺序：

```text
resolve requested exact SHA
→ locate matching immutable run
→ verify completion / identity
→ read validation-summary
→ on failure read diagnostic + specific logs
→ download large artifacts only when required
```

CI provider UI/status 可以帮助发现 execution run，但不能替代上述 exact-SHA Evidence Contract。

## 12. 禁止事项

- 删除有效测试以消除失败。
- 将 required gate 改为可选以消除失败。
- 无依据增大 timeout/retry 掩盖确定性 bug。
- 在未执行时写 PASS。
- 把环境不可用写成 PASS。
- 把已执行失败的具体 gate 因 root cause classification 改写成 BLOCKED。
- 把 mandatory downstream `NOT_RUN` 自动改写成 FAIL。
- 把 CI PASS 当成未执行的 Platform/CJ/Hidden/Packaging PASS。
- 把 cross-build 当成真实 platform PASS。
- 把旧-SHA pipeline rerun 当成当前 HEAD PASS。
- 未声明 CI backend 就按另一个 backend 的语义解释 provider-specific workflow 字段。
- 把 `latest.json` 当成请求 SHA 的权威 Validation Evidence。
- 把 `completion.json` 当成 Validation PASS。
- 发布 producer 未 PASS 的 stale build/package artifact 并把它标记为有效。
