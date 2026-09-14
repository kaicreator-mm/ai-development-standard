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

`.dev-standard/VERSION` 格式：

```text
repository=kaicreator-mm/ai-development-standard
version=<semantic-version>
revision=<40-char-commit-sha>
```

其中 `revision` 是最终解析依据；`version` 用于人类阅读和 changelog 对照。

## 3. PROJECT_OVERRIDES

`PROJECT_OVERRIDES.md` 只记录项目特有信息，例如：

- repository profile / intentional structure deviation
- bootstrap / lint / test / build / hidden-validation 命令
- platform/runtime requirements
- project-specific hard boundaries
- release gates
- sensitive area / ownership rule

不得复制整套全局标准，也不得削弱本标准关于事实、validation、冻结语义和 release claim 的硬约束。

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
4. 填写真实项目命令和 override；不适用项写 `NOT_APPLICABLE`，不要保留虚假占位命令。
5. 按 `checklists/project-init.md` 检查 repository structure、docs、tests、CI 和 release gates。
6. 作为独立 PR 合并接入变更。

## 6. 升级标准版本

标准升级必须作为显式 PR/Task：

1. 选择目标标准 commit SHA，并确认其 `VERSION`/CHANGELOG。
2. 阅读新版本 changelog 和新增/变化的 standards/templates。
3. 判断与项目 override、结构、CI、release policy 是否冲突。
4. 更新 `.dev-standard/VERSION` 的 `version` 和 `revision`。
5. 必要时同步项目模板/workflow；不要机械覆盖项目已有定制。
6. 运行项目 required validation。
7. 合并后从新 revision 开始执行。

## 7. 不推荐做法

- 声明“永远使用标准仓库 main/latest”。
- 只记录 semantic version 却没有 immutable commit SHA。
- 每个项目复制整套 `standards/` 后各自漂移。
- 把项目领域规则反向塞进全局工程标准。
- 依赖聊天记忆判断项目采用哪个标准 revision。
- 升级标准时不做 diff/review，只覆盖本地文件。
