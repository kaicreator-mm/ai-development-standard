# Project Adoption

## 1. 推荐接入结构

每个业务项目至少增加：

```text
AGENTS.md
.dev-standard/
├── VERSION
└── PROJECT_OVERRIDES.md
```

推荐从 `templates/project/` 初始化，而不是手工重新设计这些文件。

## 2. Immutable Standard Pin

业务项目 MUST 固定到本标准的 immutable commit SHA，不得只引用 `main`、`latest` 或聊天中的“当前版本”。

`.dev-standard/VERSION` canonical 格式：

```text
repository=kaicreator-mm/ai-development-standard
version=<semantic-version>
revision=<40-char-commit-sha>
```

其中 `revision` 是最终、不可变、机器解析的 identity authority。

### 2.1 Immutable Resolution Procedure

Agent / 工程工具解析项目标准时执行：

```text
.dev-standard/VERSION
        ↓
parse repository / version / revision
        ↓
revision is canonical identity
        ↓
resolve exact standard commit
        ↓
verify commit identity == revision
        ↓
read VERSION from exact revision
        ↓
verify VERSION == pinned version
        ↓
read AGENTS / concern-specific standards from same revision
```

规则：

1. 不得 fallback 到 `main/latest`。
2. exact revision 无法解析时不得用其它 revision 替代。
3. 已验证本地 cache 可复用，但必须证明 object identity。
4. 因网络/权限/工具无法解析时为 `BLOCKED`；未执行为 `NOT_RUN`。
5. commit identity 或 VERSION 不一致为 `FAIL`。

## 3. PROJECT_OVERRIDES

`PROJECT_OVERRIDES.md` 只记录项目特有信息：

- repository profile / intentional structure deviation；
- bootstrap / lint / test / build commands；
- validation execution environments；
- CI profile；
- CI provider/backend/runner/workflow execution profile；
- platform/runtime/toolchain requirements；
- project-specific hard boundaries；
- release gates；
- sensitive area / ownership rule。

不得复制整套全局标准，也不得削弱关于事实、Validation、冻结语义和 release claim 的硬约束。

### 3.1 Validation Execution Profile

项目 SHOULD 明确声明真实验证环境，例如：

```text
Linux validation = Ubuntu Build Host
Windows validation = Windows workstation
macOS validation = real macOS host
```

需要矩阵时，required tuple 应明确到：

```text
<platform> × <runtime/toolchain> × <profile>
```

cross-build 不得替代 frozen authority 要求的真实 platform execution。

### 3.2 CI Profile

项目 MUST 明确 CI profile：

```text
minimal
custom
disabled
```

默认推荐 `minimal`。

`minimal` SHOULD 只运行低成本、确定性、clean-checkout checks，例如 project verifier、format/lint/typecheck 子集、快速 unit/contract smoke、basic build smoke。

`custom` 必须列出具体 checks 与使用理由。

`disabled` 必须记录：

- 为什么不使用 CI；
- exact-SHA clean validation 替代路径；
- review/merge policy。

CI profile 不能改变 frozen product/release gate。

### 3.3 CI Execution Profile

当 CI profile 为 `minimal` 或 `custom` 时，项目 SHOULD 按 `CI_EXECUTION_STANDARD.md` 声明真实执行模型，至少包括：

```text
CI provider
CI backend / execution model
CI runner role
workflow config path
workflow config source semantics
execution shell / entrypoint model
runtime/toolchain source
fresh-run / rerun policy
```

如果 clone/checkout 的 provider 默认值会影响可复现性或稳定性，还 SHOULD 明确：

```text
partial clone/filtering
submodule recursion
Git LFS
clone plugin/entrypoint model
```

规则：

1. provider/backend 是执行语义，不是装饰性 metadata；修改 provider-specific workflow 前必须先解析它们。
2. 不得因为字段名叫 `image` 就假设一定代表 container image；含义由 provider + backend 决定。
3. Local/host backend 使用宿主机 runtime 时，应声明 runtime source 并在 CI preflight 中验证真实版本。
4. workflow config source 必须足以解释 provider 是读取当前 PR HEAD、merge ref、base branch、stored snapshot 或其它来源。
5. 新 source SHA 需要能证明该 SHA 的 fresh run；旧 pipeline 的 rerun/restart 不得作为新 HEAD evidence。
6. provider-specific 绝对路径可以作为项目/runner contract 记录，但不得反向成为全局标准硬编码。
7. secrets/registration token/private credential 不得写入 `PROJECT_OVERRIDES.md`。

当 CI profile 为 `disabled` 时，CI execution fields MAY 使用 `NOT_APPLICABLE — <reason>`，但 exact-SHA clean-validation fallback 仍必须真实可执行。

### 3.4 Required Gate Authority

项目 mandatory gate 必须遵循：

```text
Frozen PRD / Contract
→ Frozen Architecture
→ PROJECT_OVERRIDES
→ Task acceptance
→ Standard defaults
```

PROJECT_OVERRIDES 可以增加项目真实需要的 gate，但不得因为历史 workflow/旧脚本存在而推导新 mandatory gate。

### 3.5 Required-but-unestablished command / runner

命令字段必须描述真实可执行能力，不得为满足 checklist 编造 shell command。

- 尚未执行且 runner 待建立：`NOT_RUN — <reason>`；
- 因前置条件/权限/工具/环境当前无法建立/执行：`BLOCKED — <reason>`；
- 只有确实不适用时：`NOT_APPLICABLE — <reason>`。

不得用 `NOT_APPLICABLE` 隐藏 required gate，也不得用 placeholder command 冒充 executable validation。

### 3.6 Execution Pack / Pull Worker / Validation Queue（v3.4，可选）

v3.4 能力是渐进可选的；不启用不削弱任何 required gate。项目 MAY 在 `PROJECT_OVERRIDES.md` 声明：

```text
execution_pack.enabled / path / retention / package_exclusion
pull_worker.builder / validator / reviewer
validation_queue.enabled / scope
local_first.enabled
```

语义：

- Execution Pack 权威低于 Task Pack，只能收窄执行自由（`EXECUTION_PACK_STANDARD.md`）；
- Builder/Validator/Reviewer 是同一个 canonical dispatch 架构的 role/profile，不是三套队列状态机；
- version-scoped Validation Handoff Queue 是 Validator dispatch 的投影（`templates/validation-handoff-queue.md`），不是第二工作流权威；
- Execution Pack 材料（`.agent/execution/`）必须可从 shipped package/product artifacts 中排除，package leakage 属于 packaging gate defect；
- Fast Path 小任务可省略 large Execution Pack / seed / validation queue / dedicated worker，但保留 authority、exact identity、validation、evidence、merge safety。

## 4. 业务项目 AGENTS.md

最小逻辑：

```text
Read .dev-standard/VERSION and .dev-standard/PROJECT_OVERRIDES.md first.
Resolve the exact pinned standard revision.
Then read pinned AGENTS.md and concern-specific standards.
```

推荐使用 `templates/project/AGENTS.md`。

## 5. 首次接入

1. 确认 repository baseline 和 project type。
2. 复制 `templates/project/` 中适用文件。
3. 写入当前采用标准的 version + 40-char revision。
4. 填写真实 commands、validation environments、CI profile、CI execution profile、platform/toolchain matrix、release gates。
5. 完成 immutable resolution 与 version/revision consistency 验证。
6. 执行 `scripts/verify_project_standard.py <project-root>` 或 pinned revision 中等价 verifier。
7. 按 `checklists/project-init.md` 检查 repository structure、docs、tests、Validation、Minimal CI execution/evidence policy 和 release gates。
8. 作为独立 PR 合并接入变更。

## 6. 升级标准版本

标准升级必须作为显式 PR/Task：

1. 选择目标标准 commit SHA 并确认 VERSION/CHANGELOG。
2. 阅读 breaking changes 与新增/变化 standards/templates。
3. 判断与项目 override、Validation、CI profile、CI execution profile、release policy 是否冲突。
4. 更新 `.dev-standard/VERSION`。
5. 必要时同步项目模板；不要机械覆盖已有定制。
6. 重新完成 immutable resolution。
7. 运行 project verifier 与项目 required validation。
8. 合并后从新 revision 开始执行。

## 7. 不推荐做法

- 声明永远使用 standard `main/latest`。
- 只记录 semantic version 没有 immutable SHA。
- exact revision 失败后偷偷读取 main/latest。
- 每项目复制整套 standards 后各自漂移。
- 把领域规则反向塞入全局工程标准。
- 依赖聊天记忆判断采用 revision。
- 把 CI 当成完整 Validation 或 Release Qualification。
- 未声明 backend 就按另一个 CI/backend 的语义修改 workflow。
- 用旧-SHA pipeline rerun 冒充当前 PR HEAD 的 Validation Evidence。
- 为追求“绿”把 required gate 从 override 中删除。
