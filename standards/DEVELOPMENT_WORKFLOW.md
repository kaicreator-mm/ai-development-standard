# Development Workflow

## 1. 目标

该流程用于让 ChatGPT Web 与 Codex 在不同执行环境中协作，同时保证任务范围、代码状态、验证结果和发布结论可追踪、可复现、可审计。

## 2. 生命周期

### Phase 0 — Intake / Baseline

确认：目标、repository、目标版本或 Task、当前默认分支、当前 HEAD、已有 PRD/Architecture/Task/CI 状态。

输出至少包括：`scope`、`baseline ref`、`acceptance criteria`。如果任务已经明确且影响小，可以直接进入实现。

### Phase 1 — L1 Product Evidence（按需）

适用于新产品、新重大能力、产品形态不明确或需要验证用户问题时。目标不是堆竞品，而是确认真实问题、用户 workflow、替代方案、反证和产品边界。

输出：产品证据、反证、关键假设、继续/收缩/停止建议。

### Phase 2 — PRD / Scope Freeze

冻结本版本要解决的问题、用户行为、业务规则、功能范围、明确不做事项、验收条件与 release blocker。

PRD 冻结后，执行 Agent 不得自行改变产品语义。

### Phase 3 — L2 Architecture Evidence（按需）

对关键架构模式、技术边界、依赖、数据流、失败模型和可维护性进行证据验证。输出应能支撑架构决策，而不是技术清单。

### Phase 4 — Task DAG

把冻结范围拆成可执行任务，并明确：依赖、输入、输出、验收标准、适合模型强度、可并行性、风险与 required validation。

### Phase 5 — L3 Implementation Evidence（按需）

为高风险或低成本模型执行的 Task 提供最小 Reference Pack。证据优先级：

`Tests → Contract/Interface → Core Implementation → Failure Handling → Examples/Docs`

### Phase 6 — ChatGPT Web Implementation

ChatGPT Web 尽可能完成：代码、测试、迁移、文档、CI 配置和能在当前环境执行的验证。不能运行的内容必须明确列为 `NOT VERIFIED`，不能默认通过。

### Phase 7 — Web Validation

执行当前环境可运行的 `format / lint / typecheck / unit / integration / build smoke`。记录 PASS/FAIL/NOT_RUN。

交接条件：主体实现达到可交接状态，已知失败已修复或被明确标为 Codex 剩余工作。

### Phase 8 — GitHub Baseline

将 Web 阶段成果落到 GitHub branch/commit。Codex Handoff 必须引用不可歧义的 baseline commit SHA；仅写“最新代码”不合格。

### Phase 9 — Codex Handoff

创建 `codex-handoff` Issue，使用 `templates/codex-handoff-issue.md`。Issue 是本次剩余工作的 Work Item；长期规则不重复粘贴，引用本标准固定版本。

### Phase 10 — Codex + Build Host Validation

Codex 在完整环境中 checkout baseline，执行 Handoff 指定 gates。发现工程问题时做最小必要修复，并在每次修复后重跑受影响 gate。

当问题要求改变冻结需求/架构时，不得擅自修改，应标为 BLOCKED 并返回 Web 决策。

### Phase 11 — Pull Request

真实代码变化通过 PR 表达。PR 关联 Handoff Issue，说明 baseline、发现的问题、根因、修改与验证结果。

### Phase 12 — GitHub CI

在干净 runner 或受控 self-hosted runner 上运行 required gates。CI 是独立裁判，不接受“Codex 本地通过”替代。

### Phase 13 — Final Closeout

ChatGPT Web 根据 Task DAG、实现 diff、Validation Report、CI、文档同步状态做最终判断：

- `READY`：所有 release blocker 与 required gate 通过。
- `CONDITIONAL`：允许发布但存在明确、非阻塞、已记录限制。
- `BLOCKED`：存在 release blocker、required gate FAIL/NOT_RUN 或范围未完成。

### Phase 14 — Merge / Tag / Release

只有达到项目 release policy 后才能 merge/tag/release。发布后关闭对应 Handoff Issue，并保留 Validation/CI 审计链。

## 3. 快速路径

Bug、小修复、文档修正、已冻结范围内的明确 Task 可跳过 L1/L2/L3，但不能跳过：Baseline → Implementation → Validation → GitHub事实链 → Release判断。
