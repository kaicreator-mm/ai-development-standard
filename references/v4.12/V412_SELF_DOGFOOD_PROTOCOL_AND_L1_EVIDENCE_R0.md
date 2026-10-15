# ADS v4.12 — Self-Dogfood / 以 v4.12 项目检验 v4.12 流程（R0）

> **非规范性试验方案 + 首次真实 GitHub L1 观察记录。** 归属 #1096 / Draft PR #1101。并非 v4.12 先行生效、独立审核、Product Freeze、L2 Freeze、可执行 Scaffold 或新的 Gate。严禁用“试验”覆盖项目既有合法 Work Item/Claim/Review/Version Release 权威。**当前 PRD 精确对象：** `docs/product/PRD-v4.12.0-review-candidate.md` **Git blob `0bfbf782c8859e79df52c9b57904ad80bcd718e9`**（R3；正文不在本轮修改）。

## 1. 决策：一条权威轨道 + 一条观察轨道

**YES — 允许以 ADS v4.12 作为 v4.12 自己的第一个试点项目**，覆盖 L1、L2、Scaffold↔Task DAG、Implementation/CI/Review、Release；但过程是“**现有规则合法执行，v4.12 候选在旁边做影子验证**”，不是自举地让尚未批准的 v4.12 规定立即拥有写入/Gate/发布效力。

```text
CANONICAL TRACK: 现行已批准 version pin / GitHub 原生 Issue + Claim + Review + PR/merge +
                 Frozen Product/L2/Task DAG + Validation + RQ/Release Authority
                       ║ actual identities / read-only evidence
SHADOW TRACK:    v4.12 candidate DAG-P/A → Scaffold↔DAG trace → Steward observation →
                 Environment proof → Task outcome learning → falsifiable acceptance
                       ║ observations and proposed corrections ONLY
                legitimate owner explicitly accepts any normative amendment
```

**影子模式不允许：** 跳过 independent Product Review；把 PR/作者自审视为 Freeze；没有 accepted Claim 就写 Scaffold；跳过 public contract required Review；把 import 关系设为 native blocked-by；让双向映射生成器分配写入权限；因模型多数票而更改 Trust/Human DENY；把可编译 stub 当功能 PASS；用未发布 v4.11 候选冒充 Release predecessor；用人工自测伪造 E3/Hidden。

**合规采用分层：**
- `OBSERVE`：只读采集 GitHub 事实和差异；可在当前 L1 **立即进行**。
- `SHADOW_EVALUATE`：在文档/试验 fixture 上演练 v4.12 新谓词并给出 `SUPPORTED | FAIL_CASE | UNKNOWN` 结论，**不是正式 Gate 状态**；当前可进行。
- `APPLY_AUTHORIZED`：只在 Product/L2 冻结、项目合法采用对应版本规则、现有 Work Item/accepted Claim/Review/merge-ready 具备后，真正生成 Scaffold、物化实施 Task/执行。未完成授权前不得从 SHADOW 自行升格。

三层均使用同一 GitHub 事实源，不引入第二图服务、第二 Claim 机器或总调度权威。

## 2. 阶段性验证：先检验当前阶段，后面按合法次序继续

| 阶段 | 当前允许的自验证 | 实际判定/退出条件 | 不能提前做 |
|---|---|---|---|
| **L1 / PRD** | 按需 DAG-P: 一个 #1096 Product intake 关联 #1099 风险 ROI、#1100 三图、#1101 PRD、#1104 prior art；用 `INFORMS` 而不是凭文件引用生成 `blocked_by`；记录 reviewer finding→最小修订→exact blob | PRD 用户价值/权限/非目标与 AC 能支撑独立 Product Review；无材料的新 Issue/Review 不必新增 | 以影子发现宣称 `PRODUCT_FREEZE=PASS`；提前技术 Architecture Demo |
| **L2（Product Freeze 后）** | DAG-A: 只为真正改变架构的不确定项展开依赖；先比对已存在 v4.11 Owner/脚本/API，标 `ALREADY_SATISFIED|BOUNDED_DELTA|DEFER`；测最小 Schema/authority 表达可行性 | Architecture owner 明确每项高影响 UNKNOWN 的处置，合法 L2 Freeze | 把 Demo PASS 当 Product/Task PASS；擅自写 production Bootstrap |
| **Scaffold + DAG Draft（L2 Freeze 后）** | 建右尺工程基线 `S0↔D0...`，一个 canonical accepted Scaffold Work Item/Claim、pre-dispatch Review Policy、PR/merge-ready；用 Git anchors 和 Task bindings 跟踪 material contracts、单 writer、consumers/tests | SF 实际已合并与 DF 冻结配对，含 `source/tree + material-scope/allowlist + DAG checkpoint + mapping inputs`，三方 Product/L2/SF/DF 语义一致 | 无 Claim 写源码、作者 Review public ABI、未 merge SF 冒充已接受 |
| **实施** | postfreeze JIT Task Packs；Builder 首查复用；Reviewer 检查过度抽象/共享写集；变化时 `dag-mutation-record-v1` 重建 Task↔Issue bindings | Task 真正可执行、共享 Integration owner 有证明，PR 局部合法审查及时合并，偏离只复核影响者 | Task↔source import 自增 issue 依赖；自动帮 Task 改公共接口 |
| **版本 Closure** | 记录真实 CI/Host/Hidden/CJ/RQ exact source，重复验证有额外断言与否，Task Learning 根因和成本 | 真实 Release Owner 根据其适用 hard floors 授予/拒绝，已合并实际版本而不是 PR/task 绿灯 | 将影子流程当合规豁免；假 Host E3/版本 PASS |

**场景数量控制：** V1 首先只用 **一个新建项目** + **一个成熟项目** 的 exact-source 冻结 fixture；L1 当前 GitHub 元证据是首个可立即执行观察，不算完成了未来的可执行 Scaffold/Task map。

## 3. 本次已执行的 L1 影子观察 — 实际 GitHub 事实

| ID | 观察对象 / 本次实际读取 | 真实结果 | 用来验证哪个 v4.12 假说 |
|---|---|---|---|
| **E01** | [#1101](https://github.com/kaicreator-mm/ai-development-standard/pull/1101) 当前 Draft / PRD Blob | `head_sha=7fc9879bbdc39918330467df7581a6eb3f9c8a88`, base `main@b9461d48d902a2c7c00adff6746afc7a02a0ac3e`, PRD R3 blob `0bfbf782c8859e79df52c9b57904ad80bcd718e9`. Native PR review submissions **0**；R3 独立审核 **未见** | W1 Stage 1 / exact PRD 复核：`FREEZE=NO`，不能把独立 R2 的发现处置或作者 R3 自审传递为新的 Reviewer PASS |
| **E02** | [#1096](https://github.com/kaicreator-mm/ai-development-standard/issues/1096)、[#1099](https://github.com/kaicreator-mm/ai-development-standard/issues/1099)、[#1100](https://github.com/kaicreator-mm/ai-development-standard/issues/1100)、[#1104](https://github.com/kaicreator-mm/ai-development-standard/pull/1104) | Product intake / 风险原则 / 三图在 Issues；#1104 prior-art 仍为 **open draft**，不能以它作为已被 Product 采用的规范。三个具体方向彼此 `INFORMS`；未证明新增的 GitHub native `blocked_by` | W1/5 DAG-P 是可选协作视图，避免为了关系导航制造 Task 阻塞；W5 先复用真实研究而非再检索 |
| **E03** | 当前 v4.11 候选 Git ref 与 git commit | `version/v4.11.0@4924387815fa238382471e690fb169579767d9a1`，较历史 `322e86845f78de8ea8cadb05ec624bfbb3a5de20` 新增 PR #1110 T06 runner 范围保护。PRD 的 `322e` 是历史审查对象，**不能自动冒充最新上游/已发布版本** | W1/currentness：先定位 changed facts，不触发无差别 R3 产品重审 |
| **E04** | 两个 v4.11 候选的同名 10 个 owner 标准/Prompt Git blobs | 对照 `DEVELOPMENT_WORKFLOW`, `GITHUB_AGENT_INTERACTION_PROTOCOL`, `PROJECT_ADOPTION`, `TASK_DAG_GOVERNANCE`, `TASK_DECOMPOSITION`, `EXECUTION_ARCHITECTURE`, `ASSURANCE_PLAN`, `RELEASE`, L1/L2 Prompts：**10/10 blob identical** | C05/W4 只在实际影响边上重评，可明确证明旧规范主体无漂移；不能据此宣称所有 v4.11 代码或 candidate release 仍 current |
| **E05** | GitHub tag/release + Issue [#1021](https://github.com/kaicreator-mm/ai-development-standard/issues/1021) | 未找到 v4.11.0 tag 或 Release；#1021 V01 仍 **open**，当前上游尚不能当 v4.12 已发布 predecessor | W1/Release 授权：R3 Product review 可继续，但未来 v4.12 集成基线必须待真实合格前任固定 |
| **E06** | 现有 [#1096 dogfood 来源](https://github.com/kaicreator-mm/ai-development-standard/issues/1096) 中 domain-harness/runx 的 issue/pr 审核频次 | 两份历史 Title-based 审计已记录 Review Issue 颗粒度、重复轮次、集成与当前性问题；**不是实际 token/Host 时间的准确成本** | W2/W4 选择真实可测 `review_rounds, host_invocations, rework_causes, time_to_merge`；基线缺失填 `UNKNOWN`，禁止宣称已优化百分比 |

**L1 实验状态（本轮真实观察）：**
```ini
OBSERVED_FACTS=6
DAG_P_SHADOW_PROJECTION=YES_DOC_ONLY
INDEPENDENT_R3_PRODUCT_REVIEW=NOT_FOUND
PRODUCT_FREEZE=NO
L2_FREEZE=NO
REAL_SCAFFOLD=NOT_CREATED
IMPLEMENTATION_DAG=NOT_FROZEN
GITHUB_MAPPING_GENERATOR=NOT_IMPLEMENTED
REAL_HOST_E3=NOT_RUN
RELEASE=NOT_QUALIFIED
```

**迄今可确认的增益：** 发现当前应停止重复作者自审、真实上游仅 T06 子集变化/规范 10/10 unchanged、尚缺 R3 独立审核；这些是 **避免无价值操作的方向性反馈**，不是量化节省成本的因果实验证明。具体节约时间和 token 数均 `UNKNOWN`。

## 4. 受控自验证的最小工作约定

每次新任务或版本阶段 checkpoint，在其**已有 Issue/PR/Task Pack 里**做一次小型映射，不建额外数据库，不强制独立 Dogfood Issue：

| 字段 | 范例 | 用途 |
|---|---|---|
| `subject` | `PRD_R3@blob...` | 只评价同一实际当前对象 |
| `phase` | `L1 / L2 / PLANNING / IMPLEMENTATION / CLOSURE` | 阶段图不是新权威 |
| `canonical_authority` | `DEVELOPMENT_WORKFLOW@pinnedSHA` | 当前唯一合法流程 |
| `candidate_rule` | `v4.12 C05 currentness` | 试验的是哪项尚未生效要求 |
| `observed_evidence` | GitHub issue/pr/ref/blob、实际命令/退出码 | 禁止伪造 |
| `expected / observed` | `recheck only affected / 10 blobs unchanged` | 可证伪 |
| `disposition` | `SUPPORTED / FAIL_CASE / UNKNOWN` | **shadow judgement**，不是 Gate status |
| `minimal_change / owner` | `No full rereview; Product Reviewer next` | 学习与合法干预 |

**失败处理：**
- 新规则**妨碍**符合旧版的合法工作（例如强制 A0 安装 runner）→ `FAIL_CASE`，在 Product/L2 权威阶段做有界修订，不强制旧项目改用新规范。
- 新规则**允许**旧版拒绝的源码写入/Review/外部权限绕过 → **立即服从旧标准 DENY**；影子报告不能获准覆盖。
- 新规则的性能/节省收益没有 baseline → `UNKNOWN`，不算 `SUPPORTED`。
- 真正 release blocker 从选定 source owner 判定；因实验失败不额外创建 Gate、孤立 Issue、全量反复验证。
- 确实发现 material Product contradiction，交给 Product owner 有界 thaw/amendment；不是每次新负例都触发完整 PRD 重做。

## 5. 三个阶段性验收与下一行动

**L1-0（现在已可执行的观察）：** 本文件 E01–E06 指向真实 source，Stage1 维持 R3 固定 exact blob，R3 独立 Product Review 尚缺，不因 doc shadow evidence 解除阻断。

**L2-0（合法 Product Freeze 之后）：** source-first 差距表 `ALREADY_SATISFIED | BOUNDED_DELTA | DEFER`；优先仅一个受控 Scaffold writer authority / mapping representation、一个 manifest/read-only generator/checker、两份 source-pinned fixture；Steward/Environment/Task Learning 先对账不新建服务。架构 Demo 只测试真正未被已有源证明的关键 UNKNOWN。

**Implementation-0（L2 和合法 Claim 之后）：** 在 v4.12 自身 **真正的版本实施范围**内优先实际 dogfood `S0 ↔ D0...` → `SF/DF` Pair; P0 只实证 Claim→Review→merged Scaffold，唯一 mapping owners、material fail-closed、Task SPLIT、A0/A1 manual vs generated；执行 Task 按已有 owner gates，失败可局部修改而不是给影子过程授予 release 权威。

**当前单一 next blocker:** 对 **R3 PRD blob `0bfbf782c8859e79df52c9b57904ad80bcd718e9`** 执行一次真实独立 exact-subject Product delta Review，逐项证明 R2 P0-1/P1-1–P1-4 的关闭。通过后按真实 Product Authority Freeze；若有新的实质性 P0/P1，只做一次受控局部修订，禁止“为了 R4 而 R4”。

```ini
DOGFOOD_PROTOCOL_STATUS=R0_NON_NORMATIVE
CANONICAL_PROCESS=PINNED_APPROVED_ADS
CANDIDATE_V412=SHADOW_ONLY_BEFORE_FREEZE
ACTUAL_L1_OBSERVATION=E01-E06_RECORDED
CROSS_STAGE_DOGFOOD=NOT_YET_EXECUTED
INDEPENDENT_R3_REVIEW=NOT_RUN
PRODUCT_FREEZE=NO
NO_NEW_AUTHORITY=YES
NO_NEW_GATE=YES
NO_PREMATURE_PRODUCTION_SCAFFOLD=YES
```


## 6. L1 Self-Dogfood R1 — live owner alignment + 9 bounded shadow predicates (2026-10-15)

**Objective:** During the user's `继续推进` instruction, actually apply v4.12 conditional DAG-P, source-bound proof reuse, cost-bounded stop and evidence-owner nonpromotion **to v4.12 itself**. This is a **read-only source-evaluation experiment**, not an independent review, not test execution on a real Build Host, and not a claim that a v4.12 generator exists. Author-owned currentness check uses actual GitHub results of this iteration; negative mock predicates verify desired rejection *logic only*, not production gate software.

### R1 live source identity (new checkpoint; does not rewrite historical E01–E06)

```ini
PRD_SUBJECT=docs/product/PRD-v4.12.0-review-candidate.md
PRD_R3_BLOB=0bfbf782c8859e79df52c9b57904ad80bcd718e9
PR_1101_HEAD=d275e62eadd443fbcbf9d64aaeff41fdade25d7d
PR_1101_DRAFT=YES
PR_1101_NATIVE_REVIEW_SUBMISSIONS=0
V411_CANDIDATE_CURRENT=4924387815fa238382471e690fb169579767d9a1
V411_VALIDATION_STANDARD_BLOB=1522b85f9e68cc4a1591ea5899b53c224998e5a8
V411_RELEASE_STANDARD_BLOB=c4d72506253ca7f3d95e305dbd84aae0e1fbe2cb
L1_PRIOR_ART_PR_1104=OPEN_DRAFT
L1_PRIOR_ART_DOC_BLOB=3b4de3e63d7e32ac279f948ccd7f3d037b68f806
PRACTICE_ISSUE_1111=CLOSED_INTAKE_COMPLETED_NO_IMPLEMENTATION
PRODUCT_REVIEW_R3=NOT_RUN
PRODUCT_FREEZE=NO
```

### Minimal actual DAG-P projection — no extra GitHub dependency edges

| Work/evidence item | Relationship to PRD #1101 | Claim/phase boundary |
|---|---|---|
| #1096 Product version intake | `PARENT / SCOPE` | Contains Product requirements context; cannot freeze itself |
| #1099 Risk-Bounded Value First | `INFORMS FR-02/07` | Optional ROI rule does not override mandatory Owner |
| #1100 Conditional three graphs | `INFORMS FR-01/03` | L1 coordination view; does not create native `blocked_by` |
| PR #1104 multi-agent prior-art | `INFORMS W1–W5; OPEN_DRAFT` | Source-pinned evidence proposed but not adopted as authority; does not block PRD Review |
| #1111 validation evidence reuse | `INFORMS FR-05/07; INTAKE_COMPLETED` | Reconciled to existing Validation/Release owners; possible bounded L2 delta only, not new P0/mandatory Gate |
| PR #1101 PRD R3 | `PRODUCT_REVIEW_SUBJECT` | Source unchanged; next decisive evidence is real independent Product Review on exact blob |
| v4.11 candidate current `49243878` | `INFORMS AUTHORITY_CURRENTNESS` | Core 10 previously compared owner norm/prompt blobs unchanged vs `322e`; existing candidate not a released predecessor |

**DAG-P depth selected:** `BOUNDED_WORKLIST`, not EXPLICIT_DAG. No new native Issue Dependency was created: these are mostly product evidence/reuse links, not proved execution blockers. The only real workflow blocker is an outstanding independent R3 Product Review before Product Freeze; the inability to release an unreleased v4.11 predecessor is later integration/release currentness, **not reason to discard the current R3 Product Review**.

### R1 actual static shadow evaluations (not formal PASS)

| Test | Source/example | Result | Correct interpretation |
|---|---|---|---|
| T01 | Live PRD R3 Git blob equals expected exact subject | EXPECTED | PRD source identity pinned |
| T02 | Live PR #1101: `0` native Review submissions | EXPECTED DENY | R3 cannot inherit independent PASS or Product Freeze |
| T03 | Independent R2 blob `3e6964...` differs from R3 `0bfbf7...` | EXPECTED DENY | Changed R3 requires exact-subject review |
| T04 | #1111 `closed`, PRD blob unchanged | EXPECTED | Intake resolution does not force new P0, Product amendment or Review round |
| T05 | PR #1104 `open draft` and pinned document blob `3b4de3...` | EXPECTED | Optional L1 prior art cannot self-authorize normative adoption |
| T06 | `VALIDATION_STANDARD.md` §6 contains exact impact decision / affected-or-unknown rerun condition | EXPECTED | Existing owner covers base currentness, avoid implementing second policy |
| T07 | `RELEASE_STANDARD.md` §11 retains per-gate × exact-subject and fail-closed UNKNOWN | EXPECTED | No evidence-reuse shortcut promotes a release verdict |
| T08 | Synthetic negative: review exists for **different** source blob, not R3 | EXPECTED DENY (mock) | Previous-subject PASS cannot be retargeted |
| T09 | Synthetic negative: upstream status `UNKNOWN` | EXPECTED DENY (mock) | No automatic version-integration admission without exact source |

```ini
SHADOW_STATIC_PROBES=9_OF_9_EXPECTED
ACTUAL_SOURCE_PROBES=7
MOCK_LOGICAL_NEGATIVES=2
FORMAL_TEST_OR_CI_PASS=NO
PRODUCT_REVIEW_PASS=NO
NEW_NATIVE_DAG_EDGES=0
NEW_IMPL_TASK_ISSUES=0
NEW_REQUIRED_GATES=0
SAVED_HOST_MINUTES=UNKNOWN
SAVED_MODEL_COST=UNKNOWN
```

**Shadow checker limitation:** the experimental review/freeze boolean in T02/T08/T09 was a *minimal logical negative predicate* against retrieved GitHub facts and intentionally malicious mock cases. It is **not** the actual GitHub Gate Controller, did not exercise its lock/sweep/race paths, and must not be described as executed authoritative Freeze validation.

### Result — three useful signals and one boundary correction

1. **SUPPORTED (source-bound L1 only):** evidence reuse is already specified by `VALIDATION_STANDARD §6` and `RELEASE_STANDARD §11`; #1111's justified prospective delta is at most a missing assertion→obligation execution index. Reusing #1111 and #1104 without reopening PRD demonstrates **L1 stop condition** and reduces duplicate *planned* work (no quantified saved time).
2. **SUPPORTED:** exact source differs per review R2/R3; preserving the same exact R3 PRD despite new evidence append can keep Reviewer target stable. Current candidate changes should invalidate only affected material proofs, not demand complete Product research reset.
3. **SUPPORTED:** a few issue/PR relations are sufficient for this L1; a separate DAG-P graph DB or automatically generated native dependency edges would add ceremony with no proven decision value.
4. **CORRECTION TO AVOID OVERCLAIM:** `EXPECTED` for these lightweight shadow predicates **must not** be reported as actual release/Review/PRD machine `PASS`. The v4.12 real source-evidence contract must label `OBSERVED | STATIC_SHADOW | EXECUTED` distinctly where adoption would otherwise conflate them. This is a future L2 representation concern, not a new Product P0 or approval Gate.

### Next stage and stop rule

**Stop L1 shadow loops now for unchanged R3 source.** Do not commission a third same-author adversarial Product review, rerun the same 9 mock predicates without changed inputs, or create a full-time Steward. **Remaining external dependency**: an independent Reviewer must evaluate exact R3 PRD blob `0bfbf782c8859e79df52c9b57904ad80bcd718e9`, closing R2 P0×1/P1×4 and any new regressions. After authoritative Product Freeze, switch to L2 architecture with minimal existing-owner gap matrix and the two P0 source-pinned project fixtures; then legal Scaffold Planning accepted Claim → Review/merge-ready → paired DAG Freeze. Actual implementation must follow the then-applicable pinned authority; v4.12 shadow rule alone never authorizes source writes.


## 7. L2 self-dogfood R2 — actual Stage-2 source study & bounded Git fixture (2026-10-15)

**Stage authorization changed since historic R0/R1:** Product Freeze is **now** recorded by direct user Product Authority decision (commit `5820542ad1c092e09fae268f7e77a6db3421297b`, PRD blob `0bfbf782c8859e79df52c9b57904ad80bcd718e9`). This moves v4.12 legitimately from Stage1 into **L2 source-first**, not into executable Scaffold source writing or L2 Freeze. Historical `PRODUCT_FREEZE=NO` lines above refer to older observation times and are not current.

**Real tasks this session:**
- Read actual v4.11 Work Item, GitHub Interaction, Task DAG Governance, Validation/Release/Adoption and Stage2 L2 Research owner sources at pinned candidate `4924387815fa238382471e690fb169579767d9a1`, not floating main.
- Refined [L2 R1 source-evidence/ADR](../../docs/architecture/V412_L2_ARCHITECTURE_EVIDENCE_R0.md) (blob `3b9fc0ee5866bb805f24874856787cda24e8f931`): **ADR-01** existing canonical `type:planning|task` + accepted Claim, pre-dispatch Review Policy, original merge-ready; **ADR-02** one structural anchor + one current Task binding, canonical Issue write-set and SPLIT; **ADR-03** separate source material Git-object view, immutable exact allowlist, DF/MI digest and rebuilt non-authoritative index.
- Source-pinned [isolated research Git fixture](../../references/v4.12/fixtures/v412_l2_git_pair_probe.py), blob `9e162804467a9c6e7abdb95df1ad5bbd8bd3cc90`. A matching in-session disposable Git/Python algorithm prototype ran **11/11 synthetic cases** (2 positive, 9 negative) on an actual scratch Git repository. **GitHub committed script exact bytes were not separately executed**; no real Build Host, CI, GitHub Claim, Reviewer/Validator or release execution occurred.
- Verified no Product PRD/Freeze byte drift, no new mandatory owner/Gate, no new executable Task Issues. Draft PR #1101 remains unmerged pending legitimate v4.11 predecessor release/integration.

**Concrete v4.12 standard/process feedback:**
1. `SUPPORTED`: Select `BOUNDED_WORKLIST` DAG-A for three actual source-analysis lanes, without synthetic native Issue dependencies; no need for a graph DB/second live scheduler.
2. `SUPPORTED_AT_E1_ONLY`: Pair-freeze hashing can distinguish unchanged SF source with changed DF/MI; scope and anchors default material, generated outputs excluded from own digest but **must be recomputed**. This supports the L2 design choice, **not** production checker PASS.
3. `SUPPORTED`: Existing Work Item/Claim/Review authority supports proposed source-write ownership; a new Bootstrap human Gate/type would duplicate existing mechanism. **Actual pre-DAG source admission remains prospective and not executed.**
4. `LIMITATION_NOT_A_PRODUCT_DEFECT`: Test evidence strength is independently dimensional: `LOCAL_SYNTHETIC_E1` is not `REAL_GITHUB_CAS`, `REAL_HOST_E3`, `INDEPENDENT_REVIEW` or `VERSION_RELEASE`. The R1+R2 user-facing claims must not collapse them.
5. `UNKNOWN_COST`: User benefit is fewer *planned* redundant components, Issues and full suite retries; actual saved tokens/Host minutes/time-to-merge have no controlled baseline and remain `UNKNOWN`.

**Next risk-bounded step:** the Architecture Owner reviews the *exact* L2 R1 and its high-impact U01/U02/U03 facts. If accepted and no new genuine material UNKNOWN, move to formal L2 Freeze; if an actual unresolved critical source effect/owner condition appears, resolve narrowly before Freeze. Do **not** create a redundant Product R4, a second research service, repeat 11 scenarios unaltered, or start Scaffold production before legitimate Claim and L2 authority.

```ini
DOGFOOD_STAGE=L2_SOURCE_FIRST
PRODUCT_FREEZE=PASS_EXACT_R3
L2_R1_BLOB=3b9fc0ee5866bb805f24874856787cda24e8f931
SYNTHETIC_PROTOTYPE=11_OF_11_EXPECTED
COMMITTED_FIXTURE_EXACT_EXECUTION=NOT_RUN
L2_AUTHORITY_FREEZE=NO
CANONICAL_SOURCE_SCAFFOLD_CLAIM=NONE
IMPLEMENTATION=NOT_STARTED
RELEASE=NOT_QUALIFIED
```


## 8. L2 self-dogfood R3 — adversarial N10 repair without Product thaw

**Practice feedback, exact subject:** [L2 R2 candidate](../../docs/architecture/V412_L2_ARCHITECTURE_EVIDENCE_R0.md) blob `9dd12912550bbd0db30d1f391084ae058eae56db`, [reusable Git research fixture](../../references/v4.12/fixtures/v412_l2_git_pair_probe.py) blob `e360629cac23b481a0539b8c566f83f52e2b9e9b`. Historical R1 `11/11` and prior R2 source identities above remain **historical checkpoints**, not current file digests.

**Genuine negative discovered during Stage2 work:** a frozen **writer-chosen** allowlist may already contain a material code path. Simply pinning the manifest SHA and forbidding its *subsequent* modification is **not sufficient**. `N10` adds an admitted-source owner/classification check before accepting the original SF tuple: only owner-classified exact nonmaterial DAG/derived/Freeze outputs can be excluded from **SF source tree** recheck, and the former two remain covered by independent DAG/map/derived-output proof. Unknown path/category → material or HOLD.

**Result:** added N10 to matching local Git prototype, **12/12 expected**, updated GitHub fixture source, and repaired L2 text. No Product semantic change, no new gate, no full CI run or second all-workstream review. `GITHUB_COMMITTED_FIXTURE_EXACT_RUN=NOT_RUN`; `REAL_BUILD_HOST/ISSUE_CAS/L2_FREEZE=NOT_RUN`. This is a concrete iteration of v4.12 `Risk-Bounded Value First + Task Learning`: one new counterexample → one local contract fix → affected check only.

```ini
DOGFOOD_REAL_FINDING=N10_FROZEN_ALLOWLIST_CAN_PREEXEMPT_SOURCE
FIX=SOURCE_OWNER_ELIGIBILITY_PROOF_BEFORE_SF_ACCEPTANCE
E1_LOCAL_GIT_PROTOTYPE=12_OF_12_EXPECTED
RUNTIME_MACHINE_CONFORMANCE=NOT_RUN
L2_FREEZE=NOT_RECORDED
PRODUCT_R3_FREEZE=UNCHANGED
```
