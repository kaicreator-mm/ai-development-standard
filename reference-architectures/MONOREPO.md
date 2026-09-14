# Monorepo Reference Architecture

> Reference, not a mandatory template. `standards/PROJECT_STRUCTURE.md` is normative.

## 1. 适用场景

优先考虑 monorepo，当多个模块：

- 属于同一产品/平台；
- 经常需要跨模块原子修改；
- 共享 domain contract、SDK、UI/design system 或工具链；
- 使用统一 CI / release closure；
- 团队规模允许共享仓库权限。

不应仅因为“未来可能复用”就把所有项目塞入一个巨型 monorepo。

## 2. 推荐结构

```text
project/
├── apps/
│   ├── web/
│   ├── admin/
│   └── cli/
├── services/
│   ├── api/
│   └── worker/
├── packages/
│   ├── domain/
│   ├── contracts/
│   ├── sdk/
│   ├── ui/
│   └── storage/
├── tools/
├── tests/
│   ├── integration/
│   ├── e2e/
│   ├── critical-journeys/
│   └── fixtures/
├── docs/
│   ├── product/
│   ├── architecture/
│   ├── implementation/
│   ├── validation/
│   └── release/
├── .github/
│   └── workflows/
├── .dev-standard/
│   ├── VERSION
│   └── PROJECT_OVERRIDES.md
├── AGENTS.md
├── CLAUDE.md
└── README.md
```

只保留实际存在的职责。例如没有独立 service 时不要创建空 `services/`。

## 3. Workspace 原则

- workspace membership 使用明确的一层 glob，例如 `apps/*`、`packages/*`；避免无界 `**` 把 examples/fixtures 意外纳入生产 workspace。
- 根配置尽量轻；模块特有依赖留在模块 manifest。
- 一个 workspace 使用一种 canonical dependency resolution/lockfile 策略。
- 跨模块引用使用 workspace/package/module contract，不使用穿越目录树的脆弱相对路径。

## 4. Package 原则

每个 package 应有一个可描述的职责。例如 `contracts`、`storage-s3`、`ui` 比 `common2`、`helpers-new` 更容易维护。

当 package 变成无关能力集合时，优先按稳定职责拆分，而不是继续增加层级。

## 5. 依赖边界

推荐：

```text
apps/services
    ↓
feature/domain packages
    ↓
contracts/core packages
    ↓
infrastructure adapters（由架构选择具体方向）
```

具体 Clean/Hexagonal/Layered 方向不是本参考强制项，但依赖方向必须显式、一致，并尽量由静态检查约束。

## 6. 测试策略

- package 内测试验证 package contract；
- app/service 内测试验证自身行为；
- 根 integration 验证跨模块组合；
- 根 e2e/critical journeys 验证产品闭环；
- Version Closure 不依赖某一个 workspace package 的局部 test 结论代替完整验证。

## 7. CI 策略

大型 monorepo SHOULD 支持 affected/changed-scope 优化，但优化不能牺牲 release confidence：

- PR：affected lint/type/unit/integration/build；
- main：按风险扩大验证；
- Closure：完整 required regression + Critical Journeys + Hidden Validation + packaging。

缓存必须可失效；CI cache 命中不是跳过 required gate 的理由。

## 8. 发布策略

同一 monorepo 可以：

- 单一产品版本；
- 多 package 独立版本；
- 内部 package 不发布版本，仅随产品 baseline 演进。

选择应写入项目 Architecture/Release policy。不要默认“monorepo 就必须所有包同版本”。

## 9. 何时考虑拆仓

当出现以下长期事实时可以评估拆仓：

- 权限隔离是硬要求；
- release cadence 完全独立且跨模块原子变更极少；
- 仓库规模导致 tooling/CI 无法合理优化；
- 团队 ownership 已形成强服务边界；
- 外部开源/商业分发需要独立治理。

拆仓前应评估 contract versioning、integration test、local development 和跨仓变更成本，不把“目录看起来大”当成唯一原因。
