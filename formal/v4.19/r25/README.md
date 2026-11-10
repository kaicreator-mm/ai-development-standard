# R25 — #1366 R24 修复的 Exact-SHA 集成复测闭环（本地执行收据）

主 Issue: [#1366](https://github.com/kaicreator-mm/ai-development-standard/issues/1366) · 候选 PR: [#1365](https://github.com/kaicreator-mm/ai-development-standard/pull/1365)（保持 OPEN，未合并/未 Freeze/未发布，无 GitHub Actions）

## 执行锚点

| 绑定 | SHA |
|---|---|
| 模型工作树（experiment HEAD，含 R24 修复） | `6edd2bad98b455e1bcdd2895f50830412af25cff`（TREE `4380d12244be6a3166f96f2f688fa44315707115`） |
| 候选源工作树（PR #1365 HEAD） | `dac263fa4c0ab155406d2f2117459b34322cc988`（TREE `def156ce156c7301c30cf7df1f4bf956b7817c5f`） |

两个独立 detached Exact-SHA worktree，直接建自 bare mirror（WSL git 创建，规避 R11 INC-1 的 `.git` 指针跨侧不兼容）；执行全程 tracked 文件零修改（执行后复核 DIRTY=0）。修复后 Runner blob 与 R24 收据逐字节核验一致（run.py `8a7dd365…`、expanded.py `bcbff21a…`、测试 `441027a7…`）；`suite_sha256` 与 `tool_inventory_sha256` 均等于 R11 收据值——自 R11 以来唯一变化的严格套件输入正是 R24 修复的两个 Runner 文件本身。

## 结果（验收停止条件全部满足；无新缺陷，无需修复）

- **Python 全量（权威，WSL2）**：`unittest discover` **77/77 实际收集执行、0 skip、0 fail、exit 0**；R24 新增 `test_source_binding_nonvacuity` 7/7 由真实 Git checkout 导入执行——关闭 R24 `real_exact_checkout_imported_tests=NOT_RUN`。
- **严格套件**：`MODEL_AND_SOURCE_PASS`，**35/35** 全选全跑（21 proof PASS_MODEL + 14 mutation COUNTEREXAMPLE），z3×16 + cvc5×16 + TLC×3，exit 0——关闭 R24 `strict_native_solver_after_source_change=NOT_RUN`。
- **求解器差分**：**16/16** 配对 PASS（`require_solver_pairs=true`）；TLC safe 27 states，两个 mutant（7/3 states）均以 COUNTEREXAMPLE 检出。
- **身份核验**：source_alignment 7/7（候选 blob+anchor @ dac263f）；traceability PASS（10 Property / 35 Case / 7 Source）；model before/after PASS @ 6edd2bad；z3/cvc5/tlc jar pre+post 均 VERIFIED（sha256 与 inventory 钉死值逐一相等），java AVAILABLE_UNPINNED；执行后三工具哈希与双工作树状态复核不变。
- **真实 CLI 红绿负探针**：同一负输入（空 `sources` / 真实行空 `anchors`）× 新旧两代 Runner——修复前（9ca0139，sha256 `4a469557…`）真实 z3 跑真实模型后报 vacuous `MODEL_AND_SOURCE_PASS`（exit 0，缺陷在 CLI 层复现）；修复后（6edd2bad，sha256 `90f36453…`）分别 `FAIL SOURCE_BINDINGS_EMPTY_OR_MALFORMED` / `FAIL SOURCE_ANCHORS_EMPTY_OR_MALFORMED`（exit 1）。探针重跑字节级确定。

## Windows 补充与归因（非权威）

Windows Python 3.14.7：7 项新测试 **7/7 PASS**（exit 0）；全量套件 77 项收集、5 失败 + 8 跳过——同一失败集合在 **9ca0139 基线完全复现**（POSIX `#!/bin/sh` 桩不可执行 ×4、`write_text` CRLF vs autocrlf blob 失配 ×1），全部在权威 linux-x86_64 环境通过。定性为**先于 R24 存在的 Windows 环境限制，非本轮回归**；本收据不为其改代码，保持收据与被测 HEAD 精确对应。详见 `R25_WINDOWS_SUPPLEMENT_LOG.txt`。

## 工具复用（零下载）

Z3 5.3.3（`fcd0ca76…`）/ cvc5 1.4.2（`6aecddf4…`）/ TLC 2.19 jar（`936a2620…`）自 `/home/cc/ads-i1366-tools/` 既有缓存恢复，sha256 与 `formal/tools/inventory.json` smokes 逐一相等；执行环境 WSL2 Ubuntu 26.04.1，Python 3.14.4，Java 21.0.13（版本探测，未钉字节）。

## 缺陷分级

ADS 正式规范 P0/P1/P2 = **0/0/0**；实验 open P0/P1/P2 = **0/0/0**。R24-FORMAL-TOOL-P1-01 与 P2-01 双闭环（代码修复 + 全套件 + 严格套件 + 真实 CLI 红绿证据）。本轮**无新修复需求**。

## 限制（继承并重申）

有界试点，不构成 ADS 全规范证明，条款级分母 UNKNOWN；真实 GitHub Claim/CAS/CI/Release、持久读回、liveness/fairness/expiry 未证明；R11/R17/R20 历史收据仍只绑定各自原被测 SHA，未重跑；Java 与共享库未钉字节。

## 本轮证据文件

主收据 `R25_EXACT_CHECKOUT_INTEGRATION.json` · 套件原生收据 `R25_STRICT_RUN.json` · Python 日志 `R25_PYTHON_TESTS_LOG.txt` · 套件日志 `R25_STRICT_RUN_LOG.txt` · 负探针 `R25_NEGATIVE_PROBE_LOG.txt` + `R25_NEGPROBE_*` · 身份复核 `R25_POSTCHECK_IDENTITY.txt` · Windows 补充 `R25_WINDOWS_SUPPLEMENT_LOG.txt`
