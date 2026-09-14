# Project Structure Standard

## 1. 目标

本标准定义跨项目的目录边界与依赖组织原则。目标是让人和 AI Agent 能快速判断“代码属于哪里、谁可以依赖谁、测试和文档在哪里”，而不是强制所有技术栈使用同一棵目录树。

## 2. 核心原则

- **最小必要结构**：不要为了形式创建空目录或无职责层级。
- **职责优先于技术名词**：目录应表达 deployable、service、shared package、test、docs 等职责。
- **多子模块项目优先 monorepo**：当多个子模块属于同一产品/平台、共享领域模型/工具链/发布闭环并需要原子变更时，优先 Git monorepo。
- **可独立演进才独立仓库**：只有当模块需要独立权限、独立生命周期、明显不同团队边界或不能接受统一仓库耦合时，才优先拆仓。
- **一模块一主要职责**：避免不断膨胀的 `common/`、`utils/`、`shared/` 大杂烩。
- **结构必须支持验证**：实现、测试、fixture、文档和发布事实应能从目录结构快速定位。

## 3. 推荐顶层语义

项目只创建实际需要的目录：

```text
project/
├── apps/                 # 面向用户或外部调用的可部署应用
├── services/             # 可独立运行的后端/worker/domain service
├── packages/             # 可复用库、领域包、SDK、配置包
├── tools/                # 开发/生成/迁移等工程工具
├── tests/                # 跨模块 integration/e2e/critical-journey/fixtures
├── docs/                 # 项目正式文档
├── scripts/              # 简单自动化入口；复杂逻辑应进入 tools/
├── .github/              # GitHub workflow / issue / PR / ownership 配置
├── .dev-standard/        # 本标准 revision 与项目 override
├── AGENTS.md
├── CLAUDE.md             # 使用 Claude 系 coding agent 时可选
└── README.md
```

不要求同时存在 `apps/`、`services/`、`packages/`。例如单一 Python service 可以只保留自己的源码目录和 `tests/`；只有复杂度出现时再升级结构。

## 4. Monorepo 边界

### 4.1 apps

`apps/` 放最终可运行/部署的入口，例如 Web、Admin、Desktop、CLI、API Gateway/BFF。应用可以依赖 `packages/`，不应被其它应用作为库依赖。

### 4.2 services

`services/` 放具有独立运行时边界的服务，例如 API service、worker、scheduler、domain runtime。若模块只是复用代码而没有独立运行时，不应伪装成 service，应放入 `packages/`。

### 4.3 packages

`packages/` 放明确可复用的能力，例如：

- domain model / domain harness
- SDK / client
- UI components
- shared contracts / schemas
- storage adapter
- config preset
- reusable utility with clear ownership

每个 package SHOULD 有稳定名称、明确 public API、自己的最小 README（当用途非显而易见时）和与复杂度匹配的测试。

### 4.4 依赖方向

默认依赖方向：

```text
apps ─────┐
          ├──> packages
services ─┘

tests/integration/e2e ──> apps/services/packages
```

`packages` 不得反向依赖具体 `apps`。共享逻辑如果需要从 app 被复用，应抽到职责明确的 package，而不是跨目录相对引用。

领域层、基础设施层存在进一步依赖约束时，应在 Architecture/Contract 中显式说明，并可由 lint/build rule 自动检查。

## 5. 测试目录

- 模块内部的 unit/component tests MAY 与源码 co-locate，或放模块自己的 `tests/`。
- 跨模块 integration、E2E、Critical Journey、共享 fixture SHOULD 放根 `tests/` 下的明确子目录。
- Hidden Validation 的公开 harness/runner 可以在项目中；真正需要对实现 Agent 保持独立的验证数据按 Hidden Validation 策略管理，不应为了方便直接暴露答案。

推荐：

```text
tests/
├── integration/
├── e2e/
├── critical-journeys/
├── fixtures/
└── helpers/
```

不要建立一个同时混合 unit、E2E、临时脚本和生产数据的无结构 `tests/`。

## 6. 文档目录

`docs/` 遵循 `DOCUMENTATION_STANDARD.md`。源码目录中的局部 README 只解释局部模块；产品、架构、验证和 release 事实不得分散到多个互相矛盾的 README。

## 7. 生成内容与缓存

以下内容默认不得进入 Git：

- dependency cache / `node_modules` / virtualenv
- build cache
- test reports / browser reports
- local database
- logs
- temporary downloads
- IDE/user-local state
- runtime secrets

生成代码只有在以下情况之一成立时 SHOULD commit：

1. 它是发布/消费所需的正式源码工件；
2. 重新生成成本高或生成器在消费端不可用；
3. 需要 code review 生成差异；
4. 项目 contract 明确要求。

被提交的 generated content 必须有可重复的生成命令，并尽量标明“do not edit manually”。

## 8. 依赖与锁文件

- 项目 MUST 提交其包管理器需要的 canonical lockfile，除非该生态明确不推荐。
- 同一 workspace 不应存在多个互相竞争的主锁文件。
- 根 workspace 配置只声明真实 workspace 成员，避免过宽的递归 glob 导致意外把 fixture/example 当生产 package。
- 共享依赖策略应由 workspace/package manager 管理，不通过手工复制 vendor 目录实现。

## 9. 根目录卫生

根目录只保留高发现性的入口文件、workspace/build 配置和少量标准目录。一次性报告、压缩包、截图、测试结果、迁移备份等不得长期堆在根目录。

当根目录新增文件时，应能回答：

1. 为什么必须在 root？
2. 人或 Agent 是否需要从 root 发现它？
3. 它是否有更明确的 `docs/`、`tools/`、`scripts/`、`.github/` 或模块归属？

## 10. 项目差异

业务项目可以通过 `.dev-standard/PROJECT_OVERRIDES.md` 选择不同目录名或布局，但必须保留等价职责边界，并说明偏离本推荐结构的原因。项目 override 不得以“历史如此”为唯一理由持续保留明显混乱的结构。
