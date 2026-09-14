# Documentation Standard

## 1. 目标

文档必须帮助人和 Agent 快速回答：项目是什么、当前版本要做什么、为什么这样设计、如何实现/验证、当前 release 是否可信。文档不是代码的平行世界，也不是聊天记录归档。

## 2. 文档职责

### README.md

项目入口，只保留高频信息：定位、主要模块、快速开始、关键命令、文档入口、当前支持状态。README 不应膨胀成完整 PRD 或架构历史。

### AGENTS.md

Agent 的执行入口：读取顺序、硬约束、项目级命令、禁止事项和标准 revision。它应短、明确、可执行，不重复复制整套全局标准。

### CLAUDE.md / 其它 Agent adapter

MAY 存在，用于特定工具的调用习惯；不得成为需求、架构或 validation 的唯一事实源。能引用 AGENTS/标准时应引用而非复制。

### docs/README.md

项目正式文档索引，说明当前有效文档、状态与推荐阅读顺序。

## 3. 推荐 docs 结构

按需要创建，不要求空目录：

```text
docs/
├── product/          # PRD、scope、user journey、产品规则
├── architecture/     # system design、contract、ADR、data flow
├── implementation/   # Task DAG、L3、迁移/实现说明
├── validation/       # validation plan/report、critical journeys
├── release/          # closeout、release notes、known limitations
├── operations/       # deploy/runbook/backup/restore（需要时）
└── README.md
```

项目规模较小时可以扁平化，但职责仍需可识别。

## 4. Single Source of Truth

同一事实 SHOULD 只有一个权威位置。例如 API contract 不应在 PRD、README、CLAUDE.md 和代码注释中维护四份不同版本。

重复出现时：

- 权威文档保存完整事实；
- 其它位置保存简短摘要 + 链接/路径；
- 自动生成内容应来自同一源。

当代码已经是最佳事实源（例如 CLI `--help`、OpenAPI schema），文档应解释使用方式，而不是人工复制所有细节。

## 5. 文档状态

重要阶段文档 SHOULD 标注可审计状态，例如：

- `DRAFT`
- `FROZEN`
- `ACTIVE`
- `SUPERSEDED`
- `DEPRECATED`

冻结 PRD、Architecture Contract、Task DAG、Validation/Closeout 应能关联版本和 Git commit/revision。

不得用“final-final-v2-new.md”这类文件名表达状态。

## 6. PRD / Architecture / Task 的关系

- PRD 定义 WHAT / WHY / acceptance / out-of-scope。
- Architecture 定义系统边界、依赖、contracts、failure model 和关键技术决策。
- Task DAG 将冻结范围转换为 dependency-ordered executable work。
- L3 为风险 Task 提供 Tests → Contract → Implementation → Failure Handling → Reference evidence。

后一级不得悄悄重定义前一级语义。发现冲突时应返回相应阶段修正并形成新的 checkpoint。

## 7. ADR

重大、长期、难逆转且存在真实备选方案的架构决策 SHOULD 使用 ADR 或等价决策记录。轻量实现选择不要滥用 ADR。

ADR 至少包括：Context、Decision、Alternatives、Consequences、Status。

被替代的 ADR 不删除，标为 superseded 并指向新决策。

## 8. 文档与代码同步

影响以下事实的 PR MUST 同步相关文档：

- public API / contract
- 配置或环境变量
- deployment / storage / migration
- user-visible workflow
- required test/release command
- architecture boundary
- known limitation

如果无需更新文档，PR 可以明确写 `Docs: NOT_APPLICABLE`，而不是默认为“忘记更新”。

## 9. 历史文档

Git 历史已经保存普通历史版本，因此不要为每次修改复制一份旧 Markdown 到 `archive/`。

只有以下内容 MAY 保留历史快照：

- 需要长期审计的 release closeout
- 已发布版本的兼容性/迁移文档
- 法规/合同要求的记录
- 后续仍会引用的重大历史决策

其它过期资料应删除或标记 superseded，避免 Agent 检索到错误事实。

## 10. 文档质量要求

正式文档 SHOULD：

- 优先具体名词、路径、命令、contract 和可验证条件；
- 避免“完善、优化、增强”等没有 acceptance 的描述；
- 区分事实、假设、建议与待验证项；
- 对未知内容使用 `UNKNOWN / NOT VERIFIED / BLOCKED`；
- 不复制大量第三方文档，优先引用来源并记录本项目决策。

## 11. 生成文档

API reference、schema reference、CLI reference 等如果可从源码生成，SHOULD 自动生成并在 CI 中检查漂移。生成文件如被提交，必须记录生成命令并禁止手改。
