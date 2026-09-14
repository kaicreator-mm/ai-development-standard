# Changelog

## v1.3.0 — 2026-09-14

新增 Test Data & Scenario 工程标准，并用仓库自身 reference pack 完成“标准 → 模拟数据 → 验证 → 反馈优化标准”的闭环。

- 新增 `TEST_DATA_AND_SCENARIO_STANDARD.md`：定义来源/provenance、Scenario Matrix、Golden/Regression、Boundary、Schema-invalid、Domain-invalid、Incomplete/Uncertain、Failure Injection、Adversarial、Hidden Validation Data、生成器与 coverage。
- 明确 LLM 适合场景设计、语义边界和自然语言输入，但默认不是 Golden Oracle；同一 LLM 不得同时成为输入生成者、expected-answer 唯一来源和唯一审批者。
- 新增 `prompts/TEST_DATA_GENERATION.md`、`checklists/test-data-review.md`、`templates/test-data-pack.md`。
- 新增 `references/TEST_DATA_ENGINEERING_REFERENCES.md`，记录 Hypothesis、Faker、Schemathesis 的 property-based、seed/version reproducibility、schema-driven generation/replay 等参考依据。
- 新增 `examples/test-data-pack/quote-assessment/`：27 个案例，包含 16 curated、8 deterministic-generated、3 schema-invalid、4 Golden、4 Boundary、2 Domain-invalid、3 Incomplete/Uncertain、2 Adversarial、1 Regression；runtime Failure Injection 对该纯决策 pack 明确为 `NOT_APPLICABLE`。
- 新增 `scripts/verify_test_data_pack.py`，验证 pack integrity、dimension rationale/coverage、provenance、Golden/Regression review、risk mapping 与 frozen hashes。
- 模拟数据实际验证反向强化标准：required dimension 必须有行为/风险意义；schema-invalid/domain-invalid/incomplete/runtime failure 必须区分；Golden 按风险选择；seed 还需 generator/dependency identity；禁止重复 synthetic records 刷 coverage；不适用类别必须 N/A 而非伪造案例。
- `TESTING_STANDARD.md` 与 `VALIDATION_STANDARD.md` 接入 Test Data / Scenario Gate；正式 pack 自身未通过时，下游 Hidden/Critical Journey 结果不得宣称 PASS。
- 标准仓库自验证新增 reference pack 检查与 deterministic generator replay。

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
