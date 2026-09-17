# Changelog

## v2.2.0 — 2026-09-17

新增 provider-neutral CI Evidence Contract，将 CI/自动化验证发布到 Google Drive、S3、MinIO 或其它外部 backend 时的 identity、publication、integrity、discovery 与性能读取路径标准化，同时保持“Validation mandatory、CI 不是 Release Authority”的 v2.x 基线。

- 新增 `standards/CI_EVIDENCE_STANDARD.md`：定义 `manifest.json`、`validation-summary.json`、`environment.json`、`diagnostic.json`、`SHA256SUMS`、`completion.json` 与 workflow-level `latest.json` 的非重叠职责。
- immutable run identity 绑定 provider run + rerun/attempt + exact SHA，避免同一 pipeline rerun 覆盖历史 Evidence。
- `completion.json` 被定义为 Evidence publication commit marker；Validation FAIL 也可以 publication COMPLETE，反之 Validation PASS 也不能把 incomplete publication 视为完整证据。
- `latest.json` 只作为 mutable discovery/cache pointer，必须在 completion 之后更新，并要求 serialization / monotonic compare / CAS 等等价 stale-write protection；它不能成为 Validation 或 Release Authority。
- artifact 必须记录 producer check/state/provenance；producer 未 PASS 时不能把残留 workspace 文件包装成有效 build/package artifact。
- consumer-facing metadata 必须使用 Evidence-relative path；合法的 `artifacts/...` published namespace 与本地 staging root 必须按类型/存在性区分，不能靠简单字符串禁用。
- Validation profile 应保持 Validation Tuple 边界；不要用一个粗粒度命令混合 Windows packaged、Linux logic、visual/golden、Critical Journey、Hidden 或 release packaging 后再输出低信息量 blanket status。
- 增加 hot/evidence/diagnostic/audit/artifact 分层读取模型：日常状态优先读小型 pointer/summary，大日志和大型 binary artifact 仅按需读取。
- `VALIDATION_STANDARD.md`、`TESTING_STANDARD.md`、`RELEASE_STANDARD.md` 与 Agent/README 入口同步接入 CI Evidence Contract；标准仓库 verifier 要求核心合同文件存在。
- 新增 `references/CI_EVIDENCE_REFERENCE_VALIDATION.md`，记录 Formula Woodpecker → Google Drive 真实 pilot：Pipeline 5 验证 `validation FAIL + publication COMPLETE`；Pipeline 6 验证 9/9 checks PASS 但因 Evidence self-verifier namespace 缺陷 publication incomplete 且 latest 不前移；Pipeline 7 修复后完整 PASS 并发布 completion/latest；Pipeline 9 在 final reference SHA `73c5014c2db9a832d8d0c5be335240334f9bae24` 上执行 monotonic/stale/rerun/idempotent/conflict 反例回归并完整 PASS，Drive consumer-side 再确认 immutable run、completion 与 latest pointer。

## v2.1.0 — 2026-09-17

新增版本集成分支与通用 Local Agent Handoff，强化多 Task、多 Agent、跨环境验证时的 GitHub 事实链，同时保留小改动的 trunk 快速路径。

- 新增 `standards/VERSION_INTEGRATION_WORKFLOW.md`：大版本默认可采用 `task/fix → version/vX.Y.Z → main`，小型维护继续允许 `task/fix → main`。
- 明确 PRD Freeze、L1、L2、Task DAG、L3、Candidate、Validation、Closeout 是远端 checkpoint，不要求为了形式分别创建分支；Task/Concern 才是默认独立短分支边界。
- 明确 Validation Issue 本身不自动创建 branch；只有验证发现需要修改源码时才创建 `task/fix` 分支并 PR 到正确 integration branch，随后针对新 exact SHA 重跑 required gates。
- 推荐版本使用 GitHub Milestone，Label 表达稳定属性；新增 `type:*`、`handoff:local-agent`、`executor:*`、`gate:*`、`env:*`、`release-blocker`、`blocked:environment` 分类建议。
- 新增 `standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`，将 Codex-specific handoff 泛化为 Codex、Claude Code、Build Host Agent 或其它可信 execution agent 共用的 Issue contract。
- 新增 `templates/local-agent-handoff-issue.md`，补齐 Execution Environment、Validation Profile、Exact Commands、fixtures/services/credential assumptions、completion rule 与 blocker reporting。
- 新增 `prompts/local-agent-bootstrap.md`，使本地 Agent 只需 `repository + handoff issue` 即可按 pinned standard、baseline SHA、allowed/forbidden changes 和 required gates 初始化并执行。
- 分支数量本身不作为限制 Task isolation 的理由；成本敏感项目继续通过 Minimal CI 与本地/self-hosted validation 控制 GitHub-hosted CI 消耗，并遵守 repository large-file/artifact hygiene。

## v2.0.0 — 2026-09-15

基于 FastDev 真实 Pilot 重构执行模型：保留 CI，但默认最小化；将 Validation Evidence 提升为版本判断主链，并形式化 Gate Authority、Validation Tuple 与 blocker propagation。

Breaking changes:

- Validation 与 CI 解耦：Validation 是 mandatory；CI 是 execution mechanism，不再自动等同于完整验证或 Release Authority。
- CI profile 改为项目显式声明：`minimal / custom / disabled`；默认推荐 `minimal`，只运行低成本、确定性、clean-checkout 的独立 checks。
- Minimal CI 默认不承载完整多平台矩阵、Critical Journeys、Hidden Validation、高成本 E2E 或 packaging。
- 新增 Validation Tuple：`exact SHA × real platform × runtime/toolchain × validation profile`；一个 tuple PASS 不能推导另一 tuple PASS。
- 新增 Required Gate Authority 顺序：Frozen PRD/Contract → Frozen Architecture → PROJECT_OVERRIDES → Task acceptance → Standard defaults；历史 workflow、旧脚本和 Agent 推测不能自动创建 mandatory release gate。
- 新增 DAG blocker propagation：BLOCKED 只阻塞依赖节点；其它独立工作继续执行，最终统一统计。
- 开发生命周期从机械 14 Phase 收敛为更少的 Stage：Baseline → Product/Scope → Architecture/Task → Implementation → Validation/PR/Minimal CI → Candidate → Hidden/Closure → Release。
- Candidate Prepared 与 Candidate Freeze 明确分离；Hidden Validation pack 可提前准备，但 execution 默认只针对 frozen candidate。
- Release Qualification 改为 exact-SHA required evidence 驱动；CI 只有在 frozen/project policy 明确要求时才成为 release-level gate。
- GitHub/PR/Validation 模板同步移除旧的 checkbox-only / CI-first 语义。

FastDev Pilot 直接验证了：Critical Journey 能发现真实产品缺陷、五状态 Gate 语义可审计、exact-SHA evidence 可替代 CI-first 执行模型，同时必须避免单 blocker 停止所有独立工作。

## v1.2.1 — 2026-09-15

修复 v1.2.0 已声明的 immutable project adoption contract 与 project verifier 不兼容问题，并增加最小 self-bootstrap regression。

- `scripts/verify_project_standard.py` 现在只接受 canonical `repository/version/revision` 三字段 identity，并验证 repository、SemVer、40-char hexadecimal revision、duplicate/missing/unknown keys 与未替换 placeholders。
- Legacy `ai-development-standard@vX.Y.Z` 单行 identity 不再作为 canonical PASS。
- 新增 `scripts/test_verify_project_standard.py`，用临时真实 project fixtures 通过 subprocess 覆盖 canonical PASS、legacy FAIL、missing/invalid identity、required-file 缺失等 regression cases。
- `standards/PROJECT_ADOPTION.md` 明确 immutable resolution procedure：exact revision、commit identity、root VERSION consistency、禁止 fallback 到 `main/latest`，并定义 resolution 的 FAIL/BLOCKED/NOT_RUN 语义。
- `standards/VALIDATION_STANDARD.md` 明确 `PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE` 的层级语义，包括 verifier FAIL 与 overall Adoption BLOCKED 可以同时成立，以及 mandatory downstream NOT_RUN 通常使 Release Qualification BLOCKED。
- `PROJECT_OVERRIDES` 模板明确 required-but-unestablished runner 应使用 `NOT_RUN — reason` 或 `BLOCKED — reason`，禁止伪造命令或用 `NOT_APPLICABLE` 隐藏 required gate。
- `verify-standard` CI 现在同时运行 repository verification 与 project-verifier regression suite；`verify_standard.py` 的 REQUIRED 增加与 self-bootstrap concern 直接相关的 executable/template assets。

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
