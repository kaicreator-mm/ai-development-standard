# ADS Model-Based Formal Verification — 实施计划 R1（实验性，非规范）

**Status**: ACTIVE_PILOT_R8 / EXPERIMENT / NO_NORMATIVE_GATE / R5_SOURCE_BOUND_PASS / R6_INCREMENTAL_PLUS_R8_REPAIR / R8_STRICT_NOT_RUN / NOT_FULL_ADS_PROOF  
**Repository**: `kaicreator-mm/ai-development-standard`  
**Work branch**: `experiment/v4.19-formal-proof-r0`  
**Known branch HEAD before this plan**: `af710115af0863a9909b84e05bf2ff9916bd2680`  
**Normative baseline**: ADS v4.18 published and effective per actual project pins; historical v4.19 #1353 frozen scope remains immutable.  
**v4.19 candidate under study**: PR #1365 HEAD `dac263fa4c0ab155406d2f2117459b34322cc988`; candidate, not automatically current/frozen.  
**Tools sources**: Google Drive `App` and `formal-toolkit-linux-x86_64` (https://drive.google.com/drive/folders/1a1H87Q95J0z4sU7R_ZoGnT0xXUpN5Lbi).  
**ADS authority**: This research does not replace Product/L2/DAG Freeze, Task Claim, CI, independent Review, Outcome Closure or Release.

## 0. Outcome and design choice

Build **ADS Domain Model + Python Verification Suite + native formal tools + independently challenged evidence**, without designing an FIR or a replacement ADS engine. Primary success: expose real ADS contradictions, unsafe/reachable states, unjustified serial dependencies, missing cases, and version-compatibility defects; when no defects are found, clearly state the bounded proof scope. Formal model is a *hypothesis about* ADS, not a competing normative source.

Retain existing R0 files under `formal/v4.19/r0/` and the Python runner `formal/suite/run.py`. R0 contains 6 cases (3 Z3/3 TLC), a source-map and mutation counterexamples. Preserve historical receipts. New rounds write independently versioned models, plans, and results; do not rewrite past evidence.

### Direct linking, not FIR

Each model declares **Model ID** and **Property ID**. The Python suite indexes:
`source_path + Git blob SHA + exact rule location + effective version/scope + model_id + property_id + case_id + solver + expected result + assumptions/bound + evidence`.
This is lightweight traceability metadata, not an intermediate logic language; mathematical semantics stay inside native `.smt2`, `.tla`, `.als`, `.dl`, `.lp`, etc. A single property may have several verification cases and solvers; several properties may use one shared model. Bidirectional source → property → case → result and result → property → source navigation is required.

## 1. Model coverage and verification obligations

| Model ID | Scope | Minimum propositions to challenge | Preferred tools |
|---|---|---|---|
| `ADS-M-LIFECYCLE` | Product/L1, L2, DAG Freeze, Dispatch, Claim, validation, Review, Closure, integration, Release; failure and repair | Only legal transitions reachable; illegal release never reachable; valid path exists; recoverable states, under specified fairness, can progress | TLA+/TLC, Z3; Apalache/ProB when needed |
| `ADS-M-AUTHORITY` | Owner/Builder/Validator/Reviewer, Writer, permission, profile, effective scope | No Claim → no authoritative mutation; Validator cannot source-write; profile/environment never grants authority; Writer resource exclusion | Z3 + cvc5 comparison; Alloy for relationships |
| `ADS-M-DEPENDENCY` | Task DAG, scheduling, shared write-set, native dependencies, concurrency | No cycles in accepted DAG; no false serial dependency; parallelism preserves write safety; blocked dependents fail closed | Soufflé, Alloy; Clingo where exceptions/selection matter |
| `ADS-M-EVIDENCE` | Exact-SHA CI, source-currentness, Review independence, claim and evidence provenance | Stale evidence cannot satisfy current subject; NOT_RUN/UNKNOWN cannot masquerade as PASS; traceable evidence required for gates | Z3/cvc5, pySHACL/Jena only where graph representation adds value |
| `ADS-M-EVOLUTION` | v4.18→v4.19 inheritance, prospective policy, frozen historical subjects, source scope | Historical frozen authority unchanged without lawful revision; proposed policy cannot self-activate; qualified changes invalidate only materially impacted proof | Z3, TLA+, relation checks |
| `ADS-M-CROSS` | Interfaces among the five models | Authority/Claim and Lifecycle use same effective rules; DAG readiness agrees with Claim admissions; Release consumes current Evidence; conflicts produce BLOCKED/UNKNOWN | Python crosswalk + cross-solver/multi-model scenarios |

All models must include positive *legal* paths (non-vacuity), deliberately illegal negative paths, boundary cases (unknown/stale/conflict), and explicitly declared finite bounds/assumptions. Distinguish **safety** from **liveness**; temporal progress proofs require stated environmental fairness assumptions and cannot promise actual Agent/CI availability.

## 2. Tool roster and activation policy

| Tier | Tools | Use/selection rule |
|---|---|---|
| Core | Z3 5.3.3; TLA+/TLC 2.19; Python 3 | SMT rules, finite-state transitions; every baseline model run |
| First cross-check | cvc5 1.4.2 | Re-run portable SMT-LIB queries for independent comparison; disagreement/UNKNOWN → inconclusive, not PASS |
| Structural | Alloy 6.2.0; Soufflé 2.5 | Bound relationship consistency, DAG reachability and graph inference |
| Policy exceptions | Clingo 5.8.3 | Nonmonotonic exceptions/priority/choice only with an explicitly specified closed-world treatment; unknown external facts must not become false by default |
| State model escalation | Apalache 0.62.4; ProB 1.16.0 | TLC state explosion, symbolic temporal cases, B invariants/refinement where independently valuable |
| Semantic graphs | pySHACL 0.40.2; SHACL; Apache Jena 6.2.0 | Only if graph/traceability model actually requires RDF/SPARQL/SHACL, not an implicit FIR |
| Higher-assurance/algorithmic | Vampire 5.1.0; Dafny 4.11.0; Lean 4.35.0 | Selected FOL entailment or proof of critical helper algorithms or theorem; do not claim Dafny proves Python source directly |
| Runtimes | Temurin JDK 21.0.13; .NET runtime 8.0.33; Python 3.14 for supplied Clingo wheel | Tool dependencies, not ADS/Node version gates |

Tool source roots:
- `App`: https://drive.google.com/drive/folders/1zZV3LcoOebjKqrbDNH2NOsqPMkM9xgJw
- `formal-toolkit-linux-x86_64`: https://drive.google.com/drive/folders/1a1H87Q95J0z4sU7R_ZoGnT0xXUpN5Lbi

The latter directory contains `MANIFEST.json`, `SHA256SUMS`, `install_offline.py`, artifact and wheelhouse directories. Manifest-declared packages: cvc5 1.4.2, Vampire 5.1.0, Jena 6.2.0, ProB 1.16.0, Dafny 4.11.0, Clingo 5.8.3 (wheel for CPython 3.14), Temurin 21, .NET 8. They are **inspected inventory only** until extracted, hashed and smoke-tested. ProB checksum is recorded-on-download (not independently upstream-verified); respect license/trust boundaries. Run installation only in a suitable isolated Linux x86_64 workspace; never assume connector files are executables; no global installation required. For the Python suite, a tool is **AVAILABLE / NOT_AVAILABLE / NOT_RUN / VERIFIED** independently, never silently skipped as PASS.

Tool duplication is useful only when it independently tests a high-value property, adds new bug-finding coverage, or addresses a proven solver limitation. Do **not** execute every tool on every change.

## 3. Implementation tasks and dependencies (small, parallelizable)

| ID | Task (one consistent Writer per write set) | Dependencies | Deliverable | Acceptance |
|---|---|---|---|---|
| T00 | Inventory/checksum/smoke and environment capability registry | — | `formal/tools/` inventory and run receipts | Tool identities, binary hashes, versions, missing dependencies, trust provenance; UNKNOWN/NOT_RUN explicit |
| T01 | Normative version/scope crosswalk and property inventory | — | Source→Rule→Model→Property index for five areas; exact SHA refs | Active v4.18 vs prospective v4.19 vs historical #1353 separated; source locations inspectable |
| T02 | Extend Python verification runner, no FIR | T00 | Pluggable bounded subprocess adapters and uniform evidence receipts | Timeouts, missing tool, stale source, unexpected output fail closed; no arbitrary shell commands from suite data |
| T03 | Lifecycle + Authority core models | T01,T02 | TLA+ and SMT native models, examples, mutations | Legal-path witness, illegal-path UNSAT/invariant, concurrency negative case |
| T04 | Dependency/DAG + parallelism | T01,T02 | Soufflé/Alloy or SMT models with real ADS cases | Cyclic/false-edge/write collision mutants detected; legal parallel case succeeds |
| T05 | Evidence + Evolution models | T01,T02 | SHA/currentness and version-scope models | Old CI/review cannot become current PASS; history remains protected; positive compatibility |
| T06 | Inter-model consistency | T03,T04,T05 | Integrated scenarios and interface assumptions | No contradictory role/claim/readiness/release semantics without explicit finding; mismatches exposed |
| T07 | Independent semantic challenge + checker mutation | Start after T01 and increment after T03–T06 | Positive/negative golden cases, semantic review notes, mutation receipts | Every modeled property has source, assumptions, witnessed legal path, at least one meaningful negative challenge |
| T08 | Incremental recheck and consolidated coverage/qualification | T06,T07 | Python affected-property selection, report and limits | Changed SHA → dependent proof invalidated; fresh source required for source-bound pass; explicit NOT_PROVEN remainder |

T00, T01 can run in parallel. After their completion, T03/T04/T05 are parallel lanes. T07 begins early and continues with each lane. T06 is the sole integrator for shared semantic interfaces, preventing parallel write conflicts. T08 follows integration. This table is an experimental verification Work DAG, **not** a new canonical ADS Task DAG or authorization grant.

## 4. Python suite behavior and receipt contract

1. Read the pinned source specification (branch/HEAD/blob) and version scope; never treat candidate source as approved without explicit authority.
2. Select affected model/property/cases via stable IDs and dependencies; support `--all`, `--model`, `--property`, `--changed-source`; use existing runner while adding support, not a parallel engine.
3. Recompute input SHA-256 and verify Git blob SHA/currentness; if source checkout missing, report `MODEL_ONLY_PASS` at most (or fail under strict mode).
4. Run tool-specific native models in bounded subprocesses with exact version/args, timeout, deterministic fixture, isolated scratch/output paths and parseable results.
5. Compare expected results/independent solvers, store counterexample witnesses, unsat assumptions, finite bounds, negative-mutant detection and semantic review.
6. Aggregate `PASS_MODEL`, `COUNTEREXAMPLE`, `FAIL`, `INCONCLUSIVE`, `BLOCKED`, `NOT_RUN`; no invented actual CI/Host/Release pass; preserve failed/earlier receipts append-only.
7. Link results back to source rules, model and property IDs. Report *scope coverage* by distinct supported obligations rather than raw test count. Keep denominator and unmodeled rules explicit.

**No successful solver result is sufficient to assert model-to-natural-language semantic equivalence.** Independent reviewer must inspect representative source→model mapping and challenge it with positive/negative cases. `SAT` is not always a defect; `UNSAT` is not always correctness; tool output is interpreted against the explicit query and assumptions.

## 5. Proposed monorepo layout (reuse R0)

```text
formal/
  IMPLEMENTATION_PLAN.md            # this non-normative plan
  models/
    lifecycle/ authority/ dependency/ evidence/ evolution/
    cross/
  suite/
    run.py                           # existing runner, extend only
    tools/                           # bounded adapters
    checks/                          # provenance/expectations/incremental
  cases/
    lifecycle/ authority/ dependency/ evidence/ evolution/ cross/
  tools/
    inventory.json                   # external tool refs, versions, trust/smoke status
  tests/
    test_suite.py                    # existing tests, extend
  v4.19/
    r0/                              # immutable historic experiment
    r1/                              # new versioned proof snapshot and receipts
```

Don't create empty directories or abstract interfaces preemptively. Native models own their logic; Python owns orchestration, not semantics.

## 6. Phased verification and stopping rules

- **M0 — Reproducible tool baseline**: existing Z3/TLC runs reproduced from actual binaries; new-tool smoke capability table complete. Missing optional tools do not block core progress.
- **M1 — Core model**: Lifecycle and Authority formally linked to at least their targeted exact ADS source sections, with legal and illegal witnesses and tested version guards.
- **M2 — Full five-domain pilot**: every area has at least one source-bound property, positive witness, negative challenge and valid receipt; cross-model safety tested.
- **M3 — Semantic reliability**: source→model independent checks, deliberate faulty translations detected, positive/negative fixtures and unproven source coverage enumerated.
- **M4 — Incremental usage**: one real ADS delta triggers only material proof invalidation/rechecks and outputs complete evidence; optional new tools evaluated by marginal defect/counterexample value.

Every round is Git-committed independently with exact source/model/tool versions, actual results, counterexample or witness, limitations, and feedback. New material findings may propose a normative ADS change **only through existing ADS authority**. Avoid repetitive rounds when no incremental evidence is produced; stop/reshape a tool path when it only duplicates prior checks.

## 7. Principal risks and mitigations

- **Correct but irrelevant model**: source and rule IDs plus independent semantic challenge and counterexamples, including missing or misleading translation.
- **Vacuous proof**: require satisfiable positive legal witnesses and explicit negative violation queries.
- **Finite bound mistaken for universal theorem**: label as bounded; escalate to inductive/infinite-state proofs only when justified.
- **Inconsistent multi-tool semantics**: direct shared source references, cross-model obligations, cvc5-vs-Z3 differential tests; disagreement→INCONCLUSIVE.
- **Normative drift**: immutable exact-SHA provenance, explicit historical/current/prospective scope; no unreviewed adoption.
- **Overengineering**: no FIR, no new scheduler, no mandatory tool matrix, no automatic normative gate, no heavy installs just for inventory.
- **Trust/toolchain**: SHA-256 and upstream checksum provenance distinguished, Python 3.14 Clingo wheel compatibility, JDK/.NET prerequisites, isolated smoke and no false claim of execution.

## 8. Initial implementation sequence

Start T00/T01 in parallel; reuse R0 instead of recreating its suite. Then implement T02 minimally (first cvc5 cross-check; Soufflé for DAG when needed) while T03 continues R0 models. Advance T04/T05 independently, merge via T06 and T07; finish with T08 based on demonstrated need. Local environment is only requested when a selected binary genuinely cannot run in the current execution environment; pass a repair+validation task rather than a validation-only ping-pong.

**Planning status**: the work items above are a proposal; no source-model semantic equivalence or expanded proof is claimed by writing this plan.

## 9. 实际实施进度（R5 补充，2026-11-10；不修改原 R1 实施目标）

权威实证文件：`formal/v4.19/r5/EXECUTION_RECEIPT.json`、`RULE_CROSSWALK.json`；R4 的 27 个模型用例保留原轮次收据，不在 R5 重新计数为新执行。该补充是**实验执行记录**，不是 ADS Product/L2/Task DAG Freeze、模型语义独立审核或 Release Gate。

| Task | 最新落实 | 尚未取得的证据 |
|---|---|---|
| T00 | Z3/cvc5/TLC 有已运行的 R2–R4 模型记录；工具来源/哈希登记 | 其它可选工具不以安装数量衡量覆盖 |
| T01 | 7 个固定候选源码 Git blobs、22 个锚点读回；固定 v4.18 观察 SHA；9 Property 正反索引、历史 #1353 Freeze | 完整 ADS 所有生效规则的分母、逐条独立语义审核 |
| T02 | 复用 `formal/suite/run.py`；新增 `--model-head`、模型输入工作树前后绑定、跨模型逐项求解器比较、Traceability blob/锚点审计、失败优先级 | 新组合 Python runner 在两个真实 exact-SHA Git worktree 上的全量回归 |
| T03 | TLC 生命周期安全与变异、Authority/CAS 两求解器有界检查 | 真实 Claim/CAS、显式公平性下可恢复进展的 liveness 证明 |
| T04 | 4 节点 DAG rank + 写集并发安全正反例；虚假串行边 Python 挑战 | 任意 DAG / 实际 Native Task 依赖自动提取 |
| T05 | Evidence/Scope 抽象模型与变异；历史 Freeze 与 prospective 候选分别标识 | 真实 CI/Review Evidence、版本合法迁移的实现映射 |
| T06 | Authority、DAG、Evidence、Writer 共 9 项试点性质关联 | 生产 Claim/CI/Release 的实际执行状态等价性 |
| T07 | 故障变异 10 例历史累计检出、自对抗审查 | 真正独立 Source→Model 语义评价 |
| T08 | 传递式受影响属性选择、双向索引检查、双重 Git 来源绑定和已选范围标签 | 当前 R5 严格模式下的完整 Git checkout / Full unittest / 总规则覆盖率 |

**当前 M 阶段：** M0/M1 部分完成；M2 = `MODEL_ONLY_PASS`（9 个声明的有界试点性质，**0 个严格 source-bound 验证通过**）；M3/M4 部分完成。不能将 9/9 的试点性质覆盖说成 ADS 全规范覆盖率。完整规范规则分母 `UNKNOWN`。R5 未引入新 FIR、规范、CI 门禁或授权变更。

## 10. R6 执行更新（2026-11-10；R5 验证结果按 Exact-SHA 继承而非伪造当前 PASS）

- 在此前 R5 文档编写后，真正独立的 Source→Model 审核、严格双 Git worktree 校验及完整原生套装**已经完成**。R5 执行主体 HEAD 为 `e64702c9a9c18c70767cdacc74f086605b38fb39`，最终重跑 HEAD 为 `974dfcf57ca44099bbffa540b0cc273714f99f54`；`R5_SOURCE_BOUND_RECEIPT.json`、`R5_FINAL_RERUN_RECEIPT.json` 记录 **27/27（17 PASS_MODEL + 10 COUNTEREXAMPLE）**、Python **18/18**、模型双输入绑定 PASS、7/7 候选源检查 PASS、独立语义评价 9 个已有性质的 S1–S6 局限。证明范围仅为这些有界试点性质，不是全 ADS 规范证明。
- R6 把 R5 独立审核的 S1（预留序列化）、S2（同 Operator/Dispatch 幂等 Claim）、S3（兼容组高权威授权）聚合为**一个**新 `ADS-P-ADMISSION-EXT` 性质，不产生 FIR、新状态机或额外控制系统。新增的两个原生 SMT 文件分 15 个正常查询和 3 个故障注入查询；Z3/cvc5 交叉执行产生 **2 PASS_MODEL + 2 COUNTEREXAMPLE**，本轮**新增 4 个实测用例**。已定义 Suite 从 27 扩为 31，用 10 个性质覆盖当前试点模型，但**R6 31/31 严格同 SHA 总套装尚未执行**。
- 当前新增 `formal/tests/test_r6_admission.py`：支持现有 Python runner 对 R6 原生模型自动正反验证。另增 `formal/tests/test_r6_source_consumer.py`：需在 PR #1365 候选 exact checkout 中验证 `scripts/v34_rules.py` 的真实 generation helper 和 group-reference syntax；当前该测试 **NOT_RUN**，不得把 unittest SKIP 当 PASS。
- GitHub 源与模型只做实验性源位置核验；真实 GitHub 预留 CAS、并发 Writer 原子性、完整 Grant Readback/Family/Scope/Currentness、恢复/liveness 尚未被有界模型验证。R6 新增性质的**独立语义复核**及双 SHA 严格验证仍 **NOT_RUN**。
- 继承 R5 的已确认 Source-bound 性质 **9/9（在 R5 固定 HEAD）**；新 R6 性质为 **1/1 MODEL_ONLY**。**不能**以 10/10 声称 R6 全套 Source-bound PASS，也不能把 R5 27 个旧用例计入 R6 新执行数。

### R6 首要剩余工作（T03/T07/T08 增量，而非重建流程）

1. 在两个独立 Git exact worktree 下运行 `formal/v4.19/r6/suite.json` 和 `formal/tests`，对 **新实验 HEAD** 使用 `--model-head`，对候选 SHA 使用 `--source-checkout`、`--strict-source`；设置 `ADS_FORMAL_CANDIDATE_CHECKOUT` 才可执行真实源码消费测试。任何 SKIP/UNKNOWN/FAIL 不能伪装为 PASS。
2. 对新 `ADS-P-ADMISSION-EXT` 做独立 Source→Model 语义审计，尤其要对齐 `admission_generation_conforms` 的 `IDEMPOTENT` *分类*和授权验证的角色/Dispatch/Operator 差别；检查兼容组 ref 的格式通过绝不等于已验证的高权威 Grant。
3. 仅在上述源有效性证明产生新的实际收据后升级 R6 `MODEL_AND_SOURCE_PASS`，并继续把实际 GitHub 预留 CAS、liveness 和全规范义务分母保留为 `NOT_PROVEN`。

## 11. R7 工具身份与证据资格硬化（2026-11-10）

针对 T02/T08 的一个实际证据完整性缺口：R6 前的 Python runner 虽在 JSON Receipt 中**记录**了 Z3、cvc5、TLC 的二进制/包 SHA256，却没有把该证据与 `MODEL_AND_SOURCE_PASS` 的资格绑定。理论上用户可以传入假冒求解器或替换后的 TLC JAR，而返回期望 SAT 文本；只校验模型和源码本身不能检出工具假冒。

- `formal/suite/toolchain.py` 验证**当前选择的** Z3/cvc5 二进制版本及 SHA256、TLC JAR SHA256 和 Java 命令可用性。对照仓库 Git 固定的 `formal/tools/inventory.json`；未选中的工具不作冗余要求。外部 JVM 二进制、动态库和主机信任根尚未按哈希全覆盖，严格如实披露。
- `formal/suite/expanded.py` 已接入执行前后两次工具身份校验，将 `suite/toolchain.py` 和 `tools/inventory.json` 加入模型侧 exact-HEAD Git blob 输入闭包。工具哈希/版本错误或缺失不能获得严格 `MODEL_AND_SOURCE_PASS`；确定性求解器 `FAIL` 优先于 `BLOCKED`，保留 R5 原修复。
- `coverage.source_bound_verified_obligations` 现在要求**最终 Verdict 真正为 `MODEL_AND_SOURCE_PASS`**，解决旧版本即使工具或模型来源不满足资格、也可能给出大于零的 source-bound 计数的问题。
- `formal/tests/test_toolchain.py` 的 3 个独立测试已在当前容器 Python 3.13.5 实际通过；同环境对仓库登记的真实 Z3 5.3.3、cvc5 1.4.2、TLC JAR 2.19 逐一哈希与版本比对，**3/3 PASS**。所有输入文件 Git blob 和本地生成文件对应一致；完整 runner 的新版集成测试已提交到 `formal/tests/test_expanded.py`，但尚未在真实完整 Git 工作树执行，不冒称通过。
- **R7 不新增模型性质和模拟用例**。沿用 R5 固定 SHA 的 **27/27 严格通过**及 R6 另行执行的 **4/4 模型结果**；当前最新实验 HEAD 的 31-case 严格 Source/Model/Toolchain 三重绑定尚未重跑，结论仍是 **NOT_RUN**。完整 ADS 规范义务分母依然 UNKNOWN。

R7 执行回执：`formal/v4.19/r7/EXECUTION_RECEIPT.json`。下一轮优先在完整 Git 环境执行 `formal/tests` 及 R6 的 31-case 总套装，复核 R6 新增 Property 的语义；不要因为已有 R5 记录再重复建立工具框架或形式化中间表示。

## 12. R8 对旧模型的独立自对抗检查与修复（2026-11-10）

R8 非简单加测：对 R6 的 `ADS-P-ADMISSION-EXT` 做反例查找，发现 `I05` 的 **false-positive successor witness**：有新的 `secondStartRecord` 并不蕴含 `originalClaim`，更不蕴含后继独立授权或者真实接受的后继 Claim。由 R6 原始模型构造 `secondStartRecord ∧ ¬originalClaim`、`secondStartRecord ∧ ¬successorAuthorized`，在 Z3 和 cvc5 下均为 `SAT`。这是形式化**模型语义覆盖缺陷**，并非 ADS 正式规范已有安全漏洞的证据。

为保留历史复现性，保留 R6 模型和收据原样，新增 `formal/models/authority/admission-boundaries-r8.smt2` 和独立故障变异模型。新的约束显式要求：
`secondStartRecord ⇒ originalClaim ∧ originalTerminal ∧ ¬sameDispatch ∧ currentGeneration ∧ successorAuthorized ∧ successorClaimAccepted`。在有界范围内新增三条应为 `UNSAT` 的安全检查，保留正向 `I05 SAT` 证明确实存在合法后继，不通过禁止一切 Start Record 的 vacuity 获得绿灯。

**本轮实际工具执行：** 复用已校验的 Z3 5.3.3/cvc5 1.4.2；两套工具对 R8 正常模型的 18 条 SAT/UNSAT 输出逐条一致，对 R8 故障变异的三条禁忌案例均返回 `SAT`。新增 **4 个 R8 原生用例（2 PASS_MODEL + 2 COUNTEREXAMPLE）**；新 `formal/tests/test_r8_successor.py` 在模型原文字节构成的本地隔离测试目录实际 **2/2 PASS**，没有假冒为完整工作树测试。双向 Source→Property→Case 索引检查 **35 用例 / 10 性质 / 7 来源**，无孤儿条目。

**仍需闭环：** 在完整 Git 工作树里，对新 R8 实验 SHA 运行 `formal/v4.19/r8/suite.json` 全部 35 例和 `formal/tests`；执行 `--model-head`、`--source-checkout`、`--strict-source` 及全新 R8 Source→Model 语义独立审核。此前 R5 的 27/27、R6 的 4 个、R8 的 4 个结果分别绑定各自原始 SHA，**不构成 R8 35/35 严格证明通过**。真实 GitHub 预留 CAS、角色/高权威授权读回、跨进程恢复/liveness、ADS 全规范约束总数仍是 `NOT_PROVEN`。
