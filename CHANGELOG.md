# Changelog

## v1.2.0 — 2026-09-14

将 AI Development Standard 从流程规范扩展为跨项目工程基线，并参考成熟 GitHub 项目/模板制定可复用标准。

- 新增 `PROJECT_STRUCTURE.md`：定义单项目/monorepo 选择、apps/services/packages 职责、依赖方向、测试/生成内容/lockfile/root hygiene。
- 新增 `REPOSITORY_STANDARD.md`：定义 README/AGENTS/.dev-standard、GitHub metadata、branch protection、secret、dependency、artifact、script/tool 基线。
- 新增 `DOCUMENTATION_STANDARD.md`：定义 README/AGENTS/docs 职责、Single Source of Truth、PRD→Architecture→Task 关系、ADR、状态和历史文档治理。
- 新增 `TESTING_STANDARD.md`：定义 Unit/Contract/Integration/E2E/Critical Journey/Hidden Validation/Packaging 分层，以及 fixture、flaky、coverage、snapshot、external boundary 规则。
- 新增 `reference-architectures/MONOREPO.md`，将 monorepo 作为多子模块同一产品/平台的优先参考，而非强制所有项目采用。
- 新增 `templates/project/` 项目接入模板：README、AGENTS、CLAUDE、docs index、`.dev-standard/VERSION` 与 PROJECT_OVERRIDES。
- 新增 Project Init、PR Review、Version Closure checklists。
- 新增 `references/GITHUB_ENGINEERING_REFERENCES.md`，记录 Turborepo、GitHub Spec Kit、FastAPI Full Stack Template、Cookiecutter Django、Astral uv、VS Code 与 GitHub guidance 的采纳依据。
- 项目固定规范改为 `semantic version + immutable 40-char commit SHA`；tag 变为可选的人类友好别名，不再是强制依赖。
- Release identity 改为 SHA-first；PR PASS 明确不能替代 integrated Version Closure。
- 更新 Task DAG、Implementation PR、Codex Handoff、Final Closeout 模板，与新标准保持一致。

## v1.1.0 — 2026-09-14

新增 Stage Checkpoint Push 规则。

- 明确 Commit 与 Push 的职责不同：阶段内部可有多个本地 commit，不要求每次操作都 push。
- PRD、Architecture Evidence、Task DAG、L3、可审查 Task / Concern、Validation / Closeout 和 Release baseline 等正式阶段产物在成为后续依赖时必须形成远端 checkpoint。
- Implementation 以 Task / Concern 为主要远端同步单位，并继续遵循短分支 + PR + CI / Review 的合并方式。
- 长任务、多 Agent、跨会话工作在正式 Stage / Task checkpoint 主动 push，以支持从 GitHub commit 恢复。
- 将该规则加入 Agent 硬约束与 GitHub Workflow。

## v1.0.0 — 2026-09-14

首个冻结版本。

- 定义 Web-first + Codex Validation 主流程。
- GitHub 作为唯一代码与执行事实源。
- 定义 ChatGPT Web、Codex、Build Host、GitHub CI 四层职责。
- 定义 Codex Handoff Issue 协议。
- 定义 PR、Validation Report、Final Closeout 模板。
- 纳入 L1 / PRD / L2 / Task DAG / L3 / Implementation / Validation / Release 全流程。
- 定义项目级版本固定与 override 规则。
