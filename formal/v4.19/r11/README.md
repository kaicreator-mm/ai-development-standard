# R11 — #1366 最终 Exact-SHA 集成收敛（本地执行收据）

主 Issue: [#1366](https://github.com/kaicreator-mm/ai-development-standard/issues/1366) · 候选 PR: [#1365](https://github.com/kaicreator-mm/ai-development-standard/pull/1365)（保持 OPEN，未合并/未 Freeze/未发布，无 GitHub Actions）

## 执行锚点

| 绑定 | SHA |
|---|---|
| 模型工作树（experiment HEAD） | `9a6fb6f5a2b93fa45ed75e4dc39b29c367efacff`（TREE `635cbf53b24a652cb5fcb9c28c9b4289f9f334c6`） |
| 候选源工作树（PR #1365 HEAD） | `dac263fa4c0ab155406d2f2117459b34322cc988` |

两个独立 detached Exact-SHA worktree，直接建自 bare mirror；执行全程 tracked 文件零修改。

## 结果（验收停止条件全部满足）

- **严格套件**：`MODEL_AND_SOURCE_PASS`，**35/35** 用例全选全跑（21 proof PASS_MODEL + 14 mutation COUNTEREXAMPLE），z3×16 + cvc5×16 + TLC×3，exit 0。
- **求解器差分**：**16/16** 配对 PASS（`require_solver_pairs=true`）。
- **TLC**：safe 27 states；两个 mutant 分别 7 / 3 states 均以 COUNTEREXAMPLE 检出。
- **Python 测试**：**61/61 实际收集执行、0 skip、0 fail**（`unittest discover -s tests -v`，env 指向已验证原生工具，R6 consumer 测试真实绑定候选 worktree）。
- **Source/Model/Toolchain pre-post**：全 PASS；z3/cvc5/tlc jar 三个工具 pre+post 均为 VERIFIED（二进制/哈希钉死），java AVAILABLE_UNPINNED。
- **Traceability**：PASS（10 Property / 35 Case / 7 候选源，双向 fail-closed 审计）。

机器读回执行摘要：`R11_FINAL_STRICT_RUN.json`（suite 原生收据）+ `EXECUTION_RECEIPT.json`（本收敛主收据）。日志与哈希见主收据 `*_sha256` 字段。

## 工具复用（零下载、零历史重审）

Z3 5.3.3 / cvc5 1.4.2 / TLC(tla2tools) jar 三个二进制/包均从本机既有缓存恢复，sha256 与 `formal/tools/inventory.json` smokes 逐一相等（详见主收据）。执行环境 WSL2 Ubuntu 26.04（linux-x86_64，与 R0–R10 历史运行同族），Java 21（版本探测，未钉字节，与 inventory 一致）。

## 执行期事件（问题分级）

- **INC-1（P3 基础设施，已解决）**：Windows git 写出的 worktree `.git` 指针是 `C:/...` 形态，WSL git exit 128；改写为 `/mnt/c` gitdir 后两侧 HEAD 均验证通过。无 tracked 文件变更。
- **INC-2（P3 环境，已解决）**：本机 `C:/Application/formal-toolkit-bundler/` 在会话中途被外部进程删除；z3/cvc5 已提前解压并验哈希，TLC jar 自 `formal-tools-assets/cache` 恢复，sha256 与钉死值逐字节一致。
- **INC-3（P4 操作，已解决）**：首轮 Python 测试用了错误求解器路径（/root/... vs /home/cc），全部为 OSError→NOT_RUN 类失败；纠正后 61/61 全绿。
- **无 P0/P1/P2**。formal/ 源码零修改（写集 = 本目录证据文件）。

## 限制（继承并重申）

有界试点性质，不构成 ADS 全规范证明；10 Property / 7 源映射的分母 UNKNOWN；Java 与共享库未钉字节；真实 GitHub Claim/CAS/CI/Release、持久授权、Publication 读回、liveness/fairness/expiry 未证明；R0–R10 历史 PASS 仍只绑定各自 Exact-SHA。本收敛把严格 PASS 扩展到执行锚点两个 SHA 及固化本收据的证据提交。
