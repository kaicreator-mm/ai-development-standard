# Repository Standard

## 1. 目标

定义一个可维护、可自动化、可由人和 Agent 快速接手的 Git repository 最小工程基线。具体技术栈可以不同，但仓库应提供一致的发现路径、事实源和验证入口。

## 2. 根目录最小基线

业务项目 SHOULD 至少具备：

```text
README.md
AGENTS.md
.dev-standard/
├── VERSION
└── PROJECT_OVERRIDES.md
```

根据项目需要增加：

```text
CLAUDE.md
CONTRIBUTING.md
SECURITY.md
LICENSE
CODEOWNERS
.github/
docs/
tests/
scripts/
tools/
```

不要为了满足清单创建内容为空的文件。

## 3. README

README SHOULD 能在几分钟内回答：

- 这个项目解决什么问题；
- 主要模块/运行方式；
- 如何 bootstrap；
- 如何运行最常用验证；
- 文档入口在哪里；
- 当前支持的平台/部署方式。

安装细节、架构历史、大段 API reference 应进入 docs 或生成文档。

## 4. Agent 入口

`AGENTS.md` 是跨 coding-agent 的首要工程入口。特定 Agent 文件（例如 `CLAUDE.md`）应引用 AGENTS 和本标准，不得维护冲突的平行规则。

业务项目 MUST 在 `.dev-standard/VERSION` 固定本标准的 immutable revision；不得只写 `main/latest`。

## 5. GitHub 元数据

`.github/` SHOULD 承载与 GitHub 平台相关的内容：

- Actions workflows
- pull request template
- issue forms/templates
- CODEOWNERS（也可位于仓库允许的其它标准位置）
- dependabot/automation config

对有多人协作、敏感目录或公共仓库的项目，SHOULD 使用 PR template、issue template/form 和 CODEOWNERS 或等价 ownership 机制。

## 6. 主分支保护

生产/发布事实源为 `main` 或项目声明的默认稳定分支时，SHOULD 使用 repository ruleset/branch protection 要求与风险匹配的：

- required status checks
- required review（多人项目）
- 禁止直接 force push
- 必要时禁止删除稳定分支

小型单人私有项目 MAY 不强制 review，但仍应通过 PR/CI 保留真实变更链；项目 override 可记录简化策略。

## 7. 配置与 Secret

- `.env`、token、private key、production credential MUST NOT commit。
- SHOULD 提供 `.env.example`、config example 或 schema，说明必要 key 但不包含真实 secret。
- secret 进入 Git 历史后不能只靠删除文件解决，应执行 credential rotation 和历史治理。

## 8. Dependencies

- 使用生态的 canonical manifest + lockfile。
- CI SHOULD 使用 locked/frozen install 模式（生态支持时）。
- 依赖升级应产生可审查 diff，避免在 feature PR 中无关大规模升级。
- 不得提交普通 dependency cache/vendor 目录，除非项目明确采用 vendoring 并在 override 中说明更新机制。

## 9. Generated / Build Artifact

Release binary、installer、coverage report、Playwright report、test logs、cache 等默认由 CI artifact/release storage 管理，不提交到源码仓库。

若某 generated source 被提交，仓库必须提供可重复生成命令，并在 CI 或 review 中尽量检查 generated drift。

## 10. Scripts 与 Tools

- 少量、简单、稳定的工程入口可放 `scripts/`。
- 具有自身依赖、测试、复杂逻辑或可复用性的工程程序应进入 `tools/`。
- 脚本 SHOULD fail fast、使用非零退出码表达失败，并尽量支持 CI/non-interactive 环境。

不要用多个互相重叠的 `build.sh`、`build2.sh`、`final_build_new.sh` 表达版本历史。

## 11. Contributor / Security 文件

公共项目 SHOULD 提供 `CONTRIBUTING.md`。存在安全敏感面或外部使用者时 SHOULD 提供 `SECURITY.md`，说明漏洞报告渠道与支持版本。

内部项目可以精简，但安全问题报告方式仍应可发现。

## 12. Repository Size / Hygiene

仓库不应用 Git 保存：

- 大型数据库 dump
- 常规日志
- 构建缓存
- 个人下载目录
- 重复压缩包
- 一次性审计输出

确需长期保存的大型 test fixture / model / binary，使用 Git LFS、artifact storage、object storage 或专用数据仓库，并记录获取方式和校验和。

## 13. 可重复工程入口

项目 SHOULD 为常见动作提供少量稳定入口，例如：

```text
bootstrap
format/lint/typecheck
unit
integration
build
critical-journey
hidden-validation
```

具体命令由 `.dev-standard/PROJECT_OVERRIDES.md` 记录。Agent 不应每次重新猜测项目命令。
