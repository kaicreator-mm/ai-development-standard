# Validation Standard

## 1. 状态枚举与语义

每个 Gate 只能使用：

- `PASS` = gate 已实际执行，且满足该 gate 的 acceptance criteria。
- `FAIL` = gate 已实际执行，但结果不满足 acceptance criteria。
- `BLOCKED` = gate 因前置条件、权限、工具、环境或标准缺陷无法完成。
- `NOT_RUN` = gate 尚未执行。
- `NOT_APPLICABLE` = gate 对当前 project/change 确实不适用。

不要使用“应该没问题”“基本通过”等不可审计描述，也不要把不同层级的状态压成一个值。

状态必须绑定到明确层级。例如：

- project verifier command 已执行并返回 exit 1 → **verifier gate = `FAIL`**；
- 若 verifier 的失败根因是 Standard Defect，导致符合标准 contract 的 Adoption 无法被标准 verifier 接受 → **overall Adoption acceptance 可以是 `BLOCKED`**；这不会把已经执行失败的 verifier gate 改写为 `BLOCKED`。
- mandatory downstream gate 仍是 `NOT_RUN` → 对应 gate 保持 `NOT_RUN`；依赖这些 mandatory gates 的 Release Qualification 通常为 `BLOCKED`，而不是自动把未执行 gate 写成 `FAIL`。

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

Required gate 对项目适用但 runner/command 尚未建立时，不得伪造命令或标成 `NOT_APPLICABLE`。应按真实原因使用 `NOT_RUN — <reason>` 或 `BLOCKED — <reason>`，并在项目 override / validation evidence 中记录。

## 4. 失败与阻塞证据

FAIL/BLOCKED 应尽量记录：

- failing / blocked command or job
- exit code（若 command 实际启动）
- 关键日志
- reproduction
- expected vs actual
- root cause（若已知）
- affected Task/version
- release blocking level

对于 `NOT_RUN` 的 mandatory gate，应记录未执行原因和 downstream impact；不得通过把它改写成 `FAIL` 或 `NOT_APPLICABLE` 来简化 Release Qualification。

## 5. 禁止事项

- 删除有效测试以消除失败。
- 将 required gate 改为可选以消除失败。
- 无依据增大 timeout/retry 掩盖确定性 bug。
- 在未执行时写 PASS。
- 把环境不可用写成 PASS；应写 BLOCKED 或 NOT_RUN。
- 把已执行并失败的具体 gate 因 root cause classification 改写成 BLOCKED。
- 把 mandatory downstream `NOT_RUN` 自动改写成 FAIL；应在依赖它的上层 qualification 上表达 BLOCKED。
