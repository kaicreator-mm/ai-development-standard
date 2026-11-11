# R33 — v4.18 历史 Host CAS 来源核验（物理 SQLite 独立读回）

OUTPUT_LABEL: `ADS_1366_R33_V418_HOST_CAS_SOURCE_REVIEW_REPAIR`
执行基线：`experiment/v4.19-formal-proof-r0` @ `7b12455d5eb67ec806f467b405cf153da35e5658`（执行前重新 fetch 镜像并确认 tip 与声明一致；R33 工位自 `963d3ff` 快进至该提交后才开始写证据）。

## 1. R32 遗留缺口与本轮目标

R32 只完成了来源/身份静态断言（16/16）与 Task→PR 七路径匹配（7/7），两个 v4.18 原生 `DISPATCH_CLAIMED` 评论（#166 `6507893767`、#169 `6511046226`）当时按 **self-reported host execution** 记账：未直读 Host SQLite 数据库、未独立读回 Woodpecker #98。本轮（R33）在**不创建替代数据库、不模拟接受记录、不修改 v4.19 候选规范/历史 Claim** 的约束下，完成物理层独立核验。

## 2. 原始 Host SQLite CAS 数据库（已定位，非重建）

三个原始运行产物仍在本地（易失 `_tmp` 目录，已按字节一致快照归档，见 `snapshots/SNAPSHOT_SHA256S.txt`）：

| 原始文件 | SHA256 | mtime（本地 +0800） | 角色 |
| --- | --- | --- | --- |
| `_tmp\TALLY_V2_OWNER_AUTHORIZED_BOOTSTRAP_IMPLEMENT_AND_COMPLETE\claim-registry.sqlite` | `abbccd93dc…0eab018` | 2026-10-30 04:44 | #166 Claim 预留注册库 |
| `_tmp\TALLY_V2_T125_CANONICAL_KERNEL_TASK_ADMISSION\kernel-claim-registry.sqlite` | `ea38848b94…d705401cb1` | 2026-10-30 07:35 | #169 Claim 预留注册库（`host-bootstrap-config.json` 的 `reservationRegistry`） |
| `_tmp\TALLY_V2_T125_CANONICAL_KERNEL_TASK_ADMISSION\canonical-dag.sqlite` | `fececd3665…e058a9a18` | 2026-10-30 07:34 | #169 七文件 DAG 写集注册库（Claim 发布**前**状态） |

两个 Claim 注册库的 mtime 与对应 GitHub 评论 `created_at` **精确同分钟**（04:44 ↔ `2026-10-29T20:44:11Z`；07:35 ↔ `2026-10-29T23:35:02Z`）。

## 3. 只读核验结果（完整 dump：`R33_HOST_CAS_DB_DUMP.json`；脚本：`R33_VERIFY_HOST_CAS.py`）

读取方式：SQLite `mode=ro` URI，零写入；每个库读取前后 SHA256 相等（未突变证明）。无 `-wal`/`-shm` 伴生文件。

- **物理键第一性重算**：`tally:v2:claim-admission:` + `sha256("<repo>#<n>:builder:__default__")` 与库中存储键**逐字符相等**（#166 → `2c3d9448…`，#169 → `1c1efb4e…`）。
- **#166 行**：revision **1**，值 JSON `phase=PUBLISHED_VERIFIED`、`generation=1`、`sourceSha=7823e18e…`、`dispatchId=dispatch:166:t06j:bootstrap:20261030:1`、`operatorId=zcode:t166:bootstrap:1`、`writerId=tally-host:win32:t166:bootstrap:1`、`commentId=6507893767`。
- **#169 行**：revision **1**，`phase=PUBLISHED_VERIFIED`、`generation=1`、`sourceSha=3293aace…`、`dispatchId=dispatch:169:t06l:kernel:20261030:1`、`operatorId=zcode:t125:kernel:1`、`writerId=tally-host:win32:t125:kernel:1`、`commentId=6511046226`。
- **DAG 前状态行**：revision **0**，`READY_PENDING_ACCEPTED_CLAIM`，含与 `host-bootstrap-config.json` 相同的七文件 `exactWriteSet` 与 `hostConfigSha256=458bb8d4…`。

## 4. CAS revision 语义来源（写库方实际安装包）

`@kaicreator/domain-harness-host-node@0.10.2-rc.0`（tarball SHA256 `3a0a1139…275c4b8`）`dist/sqlite-adapter.js`：

- 首写 `INSERT … VALUES(?, 0, ?)`，仅 `mustBeAbsent` 可达，重复键 `HOST_KEY_EXISTS`；
- 更新 `UPDATE … SET revision = revision + 1 … WHERE key = ? AND revision = ?`，仅 `mustMatchRevision` 可达，过期期望 `HOST_CAS_CONFLICT`；
- 无条件 put/delete 被 `HOST_PUT_CONDITION_REQUIRED` 拒绝；`begin-immediate` 事务 + WAL + busy_timeout。

因此 Claim 行 **revision=1** 恰好等价于一次成功序列：`mustBeAbsent` 插入（rev 0，`PENDING_GITHUB_PUBLISH`）→ GitHub 发布+精确回读后 `mustMatchRevision:0` 更新携带 `PUBLISHED_VERIFIED`（rev 1）。DAG 行 rev 0 为从未更新的首插。

## 5. GitHub 评论身份（API 直读，2026-11-11）

- `6507893767` / `6511046226`：`created_at == updated_at`（未编辑），作者 `kaicreator-mm`；正文 `ads/github/v3` 事件 YAML 的 task/sha/dispatch_id/protected_claim_key/admission_generation=1 与 DB 行**全字段相等**。

## 6. 原始执行证据（非 Owner 转述）

- #166 `bootstrap-receipt.log`：`RECORDED / SERIALIZED_GITHUB_PUBLISH_AND_READBACK_CONFIRMED`，`durableReservation` 与 DB 行一致；驱动（`bootstrap-driver.mjs`）发布后**独立重开**注册库复核 `PUBLISHED_VERIFIED`。
- #169 `canonical-task-writer.log`：原生创建 Issue #169（`state:ready`/`type:task`）并读回，DAG 准入持久化后才走 Claim 流程。
- K 实跑 `run-clean-live-r3.log`：`T06L_REAL_GITHUB_CLAIM_ADMISSION_K_B_C_SQLITE=PASS`、`T02B_BUILD_EXIT=0`，密封 C 负例控制 PASS；`final-status-t06l.json`：`kAdmission=ADMITTED_PENDING_AGENT_EFFECT`，falsifiers **8/8 DENIED**。
- **Woodpecker #98 独立 API 读回**（tally → Woodpecker repo 12 / forge id 1370136575）：pipeline #98（id 17265）`status=success`、push、`version/v2`、commit `2c6631db…`、agent 2266；3 个 workflow、15 个 step **全部 exit_code 0**，与本地 `woodpecker-98.json` 收据一致。R32 的“Woodpecker #98 未经独立读回”缺口就此关闭。

## 7. R32 复用声明

Task #169 → PR #170 七路径精确匹配（7/7、0 越界）**直接复用** R32 结果（`formal/v4.19/r32/R32_CROSS_VERSION_OBLIGATION_PARTITION.json`），本轮未重复静态审查；仅做存在性 sanity：合并提交 `2c9a9b42…`（#170）与 `2c6631db…`（#171）均在 tally git 历史中确认。

## 8. 结论与边界

**PROVEN**（六项核验点）：Protected Claim Key、Generation、CAS revision、PUBLISHED_VERIFIED、GitHub 评论身份、执行前后持久状态——均由物理 DB + 第一性重算 + 未编辑 GitHub 事件 + 原始运行日志相互印证。两个源 SHA 的 `.dev-standard/VERSION` 均钉死 **ADS 4.18.0 @ `2c395c55…`**，全程保持 v4.18.0 权限边界。

**无实现缺陷** → 按约束**未合并任何 Repair、未改任何源码、未创建新 Claim**。

**NOT_PROVEN / 边界（保持诚实）**：

1. 转瞬即逝的 rev 0 `PENDING_GITHUB_PUBLISH` 预留行被原地更新，store 不保留修订历史——中间态由 CAS 语义、驱动收据顺序与文件 mtime 佐证，而非一条独立保存的 rev 0 Claim 行。
2. 运行后防篡改未做密码学证明：DB 是易失 `_tmp` 中的普通文件（无 WAL/SHM、哈希已记录），不能仅凭文件证据排除事后篡改；快照固定了观测字节以便复验。
3. 跨进程同键并发写排斥未在生产运行中演练（单写入者串行产物）；竞态覆盖仍在单测层（fake ports）。
4. K journal 持久化与后继/Grant/资源读回本轮未重跑，`ADMITTED_PENDING_AGENT_EFFECT` 依据原始运行日志 + falsifier 拒绝 + final-status 收据。
5. 原始 DB 受 `_tmp` 自动清理约束；如被清理，复验以 `snapshots/`（捕获时与原件哈希相等）为准。
6. 沿袭 R32：v4.19 Canonical 消费资格、全 ADS 义务分母仍 `NOT_PROVEN`/`UNKNOWN`；历史 Claim 不升格为 v4.19 授权。

## 9. 约束遵守

无 v4.19 候选规范修改；无历史 Claim 修改；无 Merge/Freeze/Release；无替代数据库；无模拟接受记录。机器收据：`R33_HOST_CAS_SOURCE_READBACK.json`。
