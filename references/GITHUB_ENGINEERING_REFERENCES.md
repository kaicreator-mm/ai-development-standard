# GitHub Engineering References

调研日期：2026-09-14

本文件记录 `AI Development Standard` 制定项目结构、文档、测试和 repository baseline 时参考的公开项目/模板。它们是 evidence/reference，不是本标准的上游依赖，也不意味着逐字复制其结构。

## 1. vercel/turborepo

参考：

- https://github.com/vercel/turborepo
- https://github.com/vercel/turborepo/blob/main/skills/turborepo/references/best-practices/RULE.md
- https://github.com/vercel/turborepo/blob/main/skills/turborepo/references/best-practices/structure.md

吸收：

- `apps/` 表达 deployable，`packages/` 表达共享库；
- 一 package 一主要职责；
- workspace membership 应明确，不使用容易误包含目录的过宽 pattern；
- shared config/package 也应作为明确 package 管理。

未直接照搬：Node/pnpm/Turborepo 专属配置不是跨项目硬标准。

## 2. github/spec-kit

参考：

- https://github.com/github/spec-kit
- https://github.com/github/spec-kit/blob/main/templates/plan-template.md
- https://github.com/github/spec-kit/blob/main/templates/tasks-template.md

吸收：

- specification → plan → tasks → implementation 的可追踪链；
- technical context、constraints、project structure 应在实现前明确；
- Task 应 dependency-aware，并标注可并行性；
- 原则/constitution 类规则应成为后续阶段 gate，而不是聊天约定。

本标准在此基础上保留自己的 L1/L2/L3 Evidence、GitHub facts、Validation 与 Release Closure 模型。

## 3. fastapi/full-stack-fastapi-template

参考：

- https://github.com/fastapi/full-stack-fastapi-template

吸收：

- template repository 应提供可运行开发基线，而不仅是目录空壳；
- backend/frontend 等模块有局部开发文档，root README 作为入口；
- unit/backend test、E2E、Docker/部署和 GitHub Actions 是完整工程基线的不同层；
- local development 与 deployment 文档分责。

未直接照搬：FastAPI/React/PostgreSQL 等具体技术栈。

## 4. cookiecutter/cookiecutter-django

参考：

- https://github.com/cookiecutter/cookiecutter-django
- https://github.com/cookiecutter/cookiecutter-django/blob/main/AGENTS.md

吸收：

- 工程模板自身也需要 tests；
- Agent 入口应明确“这个 repository 是什么/不是什么”、关键命令和测试入口；
- locked dependency / reproducible generation 是模板可靠性的组成部分。

## 5. astral-sh/uv

参考：

- https://github.com/astral-sh/uv
- https://github.com/astral-sh/uv/blob/main/CONTRIBUTING.md

吸收：

- CONTRIBUTING 应给出具体 build/test/format 命令；
- snapshot/golden test 必须有明确 review workflow；
- 文档应区分 getting started、concepts、reference、troubleshooting、internals/policies，而不是所有内容堆进 README。

## 6. microsoft/vscode

参考：

- https://github.com/microsoft/vscode
- https://github.com/microsoft/vscode/blob/main/.github/pull_request_template.md

吸收：

- PR template 应短而强制关注必要事实，不应成为填写负担；
- 大型 repository 也需要清楚的 contribution/testing 入口与 ownership 习惯。

## 7. GitHub repository/community guidance

参考：

- https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file
- https://docs.github.com/en/pull-requests/reference/managing-and-standardizing-pull-requests
- https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates

吸收：

- PR/Issue templates 标准化输入；
- CODEOWNERS 用于路由高上下文/敏感目录 review；
- branch protection/ruleset 用于保护稳定事实源；
- `CONTRIBUTING.md`、`SECURITY.md` 等 community health 文件按项目暴露面使用。

## 8. 采用原则

选择外部实践时遵循：

1. 优先采用跨语言、跨框架仍成立的原则；
2. 工具专属约定降级为 Reference，不写成 MUST；
3. 目录存在必须有真实职责，不为了“看起来标准”创建空结构；
4. Agent-friendly 不等于为 Agent 制造重复文档，仍以 Single Source of Truth 为核心；
5. 本标准最终约束以 `standards/` 为准，本文件只解释 evidence/provenance。
