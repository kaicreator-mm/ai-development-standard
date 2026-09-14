# Project Adoption

## 1. 推荐接入结构

每个业务项目增加：

```text
AGENTS.md
.dev-standard/
├── VERSION
└── PROJECT_OVERRIDES.md
```

`.dev-standard/VERSION` 示例：

```text
ai-development-standard@v1.0.0
```

`PROJECT_OVERRIDES.md` 只记录项目特有规则，例如必须使用的测试命令、平台、release gate、禁止修改目录。不得覆盖本标准的硬安全/验证原则。

## 2. 业务项目 AGENTS.md 最小内容

```text
This project follows kaicreator-mm/ai-development-standard@v1.0.0.
Read .dev-standard/PROJECT_OVERRIDES.md before making changes.
For Codex handoff, follow the pinned CODEX_HANDOFF_PROTOCOL and VALIDATION_STANDARD.
```

## 3. 升级标准版本

标准升级必须作为显式 PR/Task：

1. 阅读新版本 changelog。
2. 判断是否与项目 override/CI/流程冲突。
3. 更新 `.dev-standard/VERSION`。
4. 必要时同步模板或 workflow。
5. 运行项目 required validation。
6. 合并后从新版本开始执行。

## 4. 不推荐做法

- 业务项目直接声明“永远使用标准仓库 main”。
- 每个项目复制整套标准后各自修改。
- 把项目特有流程反向塞进全局标准。
- 依赖聊天记忆来判断项目采用哪个标准版本。
