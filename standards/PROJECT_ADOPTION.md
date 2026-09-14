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

业务项目 MUST 固定到本标准的 immutable commit SHA，不得只引用 `main`、`latest` 或聊天中的“当前版本”。Tag 可以作为人类友好别名，但不是必需事实源。

`.dev-standard/VERSION` canonical 格式：

```text
repository=kaicreator-mm/ai-development-standard
version=<semantic-version>
revision=<40-char-commit-sha>
```

其中：

- `repository` 标识规范仓库；当前 canonical 值为 `kaicreator-mm/ai-development-standard`；
- `version` 是人类可读 SemVer，用于 changelog/升级对照；
- `revision` 是最终、不可变、机器解析的 identity authority。

Legacy 单行形式（例如 `ai-development-standard@v1.2.0`）不是 canonical project identity，不能作为 immutable adoption PASS。

### 2.1 Immutable Resolution Procedure

Agent / 工程工具解析项目标准时应执行以下链路：

```text
.dev-standard/VERSION
        ↓
parse repository / version / revision
        ↓
revision is canonical identity
        ↓
resolve the standard commit using exact revision
        ↓
verify resolved commit identity == revision
        ↓
read root VERSION from that exact revision
        ↓
verify root VERSION == pinned version
        ↓
read AGENTS.md / concern-specific standards from the same revision
```

规则：

1. 不得自动 fallback 到 `main`、`latest`、moving tag 或聊天记忆。
2. exact revision 无法解析时，不得使用其它 revision 代替。
3. 已验证的本地 Git object/cache 可以离线复用，但必须能证明 object identity 等于 pinned `revision`。
4. resolution 因网络、权限、工具或 prerequisite 无法完成时，Adoption resolution 为 `BLOCKED`；尚未执行 resolution 时为 `NOT_RUN`。
5. exact revision 成功解析但 commit identity 与 `revision` 不一致，或该 revision 根 `VERSION` 与 pinned `version` 不一致时，为 `FAIL`。
6. 只有 immutable resolution 与 version/revision consistency 已验证后，才可把该标准 revision 作为当前 project 的已解析规范源。

实现不绑定 GitHub，但在 GitHub-hosted repository 上可以使用例如：

```text
GET /repos/<repository>/contents/<path>?ref=<revision>
https://raw.githubusercontent.com/<repository>/<revision>/<path>
```

或通过 Git：

```bash
git fetch <remote> <revision>
git cat-file -e <revision>^{commit}
git show <revision>:VERSION
git show <revision>:AGENTS.md
```

任何平台实现都必须保持相同语义：**exact immutable revision first, no implicit fallback**。

## 3. PROJECT_OVERRIDES

`PROJECT_OVERRIDES.md` 只记录项目特有信息，例如：

- repository profile / intentional structure deviation
- bootstrap / lint / test / build / hidden-validation 命令
- platform/runtime requirements
- project-specific hard boundaries
- release gates
- sensitive area / ownership rule

不得复制整套全局标准，也不得削弱本标准关于事实、validation、冻结语义和 release claim 的硬约束。

### 3.1 Required-but-unestablished command / runner

命令字段必须描述真实可执行能力，不得为了满足 checklist 编造 shell command。

如果某个 gate 对项目确实适用，但 runner/command 尚未建立：

- 尚未执行且 runner 只是仍待建立：记录 `NOT_RUN — <reason>`；
- 因前置条件、权限、工具、环境或标准缺陷当前无法建立/执行：记录 `BLOCKED — <reason>`；
- 只有该 gate 对项目/变更确实不适用时才能使用 `NOT_APPLICABLE — <reason>`。

不得用 `NOT_APPLICABLE` 隐藏尚未实现的 required gate，也不得用假的 placeholder command 冒充 executable validation。

## 4. 业务项目 AGENTS.md

最小逻辑：

```text
Read .dev-standard/VERSION and .dev-standard/PROJECT_OVERRIDES.md first.
This project follows the immutable kaicreator-mm/ai-development-standard revision recorded there.
Then read the pinned standard AGENTS.md and the concern-specific standards.
```

推荐直接使用 `templates/project/AGENTS.md`。

## 5. 首次接入

1. 确认当前 repository baseline 和 project type。
2. 复制 `templates/project/` 中适用文件。
3. 把当前已采用标准的 40-char commit SHA 写入 `.dev-standard/VERSION`。
4. 填写真实项目命令和 override；按 §3.1 使用真实的 executable command / `NOT_RUN` / `BLOCKED` / `NOT_APPLICABLE`，不要保留虚假占位命令。
5. 按 §2.1 完成 immutable resolution 与 version/revision consistency 验证。
6. 执行 `scripts/verify_project_standard.py <project-root>` 或项目采用 revision 中等价的 project verifier。
7. 按 `checklists/project-init.md` 检查 repository structure、docs、tests、CI 和 release gates。
8. 作为独立 PR 合并接入变更。

## 6. 升级标准版本

标准升级必须作为显式 PR/Task：

1. 选择目标标准 commit SHA，并确认其 `VERSION`/CHANGELOG。
2. 阅读新版本 changelog 和新增/变化的 standards/templates。
3. 判断与项目 override、结构、CI、release policy 是否冲突。
4. 更新 `.dev-standard/VERSION` 的 `version` 和 `revision`。
5. 必要时同步项目模板/workflow；不要机械覆盖项目已有定制。
6. 按 §2.1 重新验证 immutable resolution 与 version/revision consistency。
7. 运行 project verifier 与项目 required validation。
8. 合并后从新 revision 开始执行。

## 7. 不推荐做法

- 声明“永远使用标准仓库 main/latest”。
- 只记录 semantic version 却没有 immutable commit SHA。
- exact revision 解析失败后偷偷读取 main/latest。
- 每个项目复制整套 `standards/` 后各自漂移。
- 把项目领域规则反向塞进全局工程标准。
- 依赖聊天记忆判断项目采用哪个标准 revision。
- 升级标准时不做 diff/review，只覆盖本地文件。
