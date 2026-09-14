# Validation Standard

## 1. 状态枚举

每个 Gate 只能使用：

- `PASS`
- `FAIL`
- `NOT_RUN`
- `NOT_APPLICABLE`
- `BLOCKED`

不要使用“应该没问题”“基本通过”等不可审计描述。

## 2. Gate 分层

### A. Fast Gate

通常包括：format、lint、typecheck、unit、contract smoke、basic build。

目标：快速发现局部回归，适合每个 Task/commit。

### B. Integration Gate

验证 API、DB、queue、filesystem、frontend-backend、external boundary mock/stub 等组合行为。

### C. Critical Journey Gate

基于真实用户路径验证关键业务闭环。不是单个 API 测试的替代品。

### D. Hidden Validation

使用实现 Agent 在开发阶段不依赖其具体答案的独立数据/场景验证正常路径、边界、错误处理和关键不变量。Hidden Validation 失败视项目策略决定是否为 release blocker；默认 P0/P1 关键场景失败为 blocker。

### E. Platform / Production Build

按项目需要验证 Android、Flutter、iOS、Windows、Linux、Docker image、browser bundle、Rust release build 等真实产物。

### F. Clean CI Gate

在 GitHub runner 或可信 self-hosted runner 上从 clean checkout 安装依赖并重复 required gates。

## 3. Required Gate 的确定

Task DAG 或 PRD 应明确 required gates。如果没有显式声明，至少要求：Fast Gate + 与修改范围相关的 Integration/Build Gate。

版本 Closeout 默认还要求：Critical Journey、Hidden Validation（如果项目已定义）、Production Build 与 GitHub CI。

## 4. 失败证据

FAIL/BLOCKED 应尽量记录：

- failing command / job
- exit code
- 关键日志
- reproduction
- expected vs actual
- root cause（若已知）
- affected Task/version
- release blocking level

## 5. 禁止事项

- 删除有效测试以消除失败。
- 将 required gate 改为可选以消除失败。
- 无依据增大 timeout/retry 掩盖确定性 bug。
- 在未执行时写 PASS。
- 把环境不可用写成 PASS；应写 BLOCKED 或 NOT_RUN。
