# ADS Model-Based Formal Verification — 实施计划 R0–R18（实验性，非规范）

**Status**: ACTIVE_PILOT_R21 / EXPERIMENT / NO_NORMATIVE_GATE / R17_PINNED_13_PYTHON_BOTH_HOSTS_32_NATIVE_PASS_AT_5a81503 / R11_STRICT_61_PYTHON_35_NATIVE_HISTORICAL / 46_NORMATIVE_DOC_BLOBS_INDEXED / 25_SELECTED_ATOMS_NOT_FULL_DENOMINATOR / FULL_ADS_SEMANTIC_PROOF_NOT_PROVEN  
**Canonical main Issue (all progress and future handoffs)**: [#1366](https://github.com/kaicreator-mm/ai-development-standard/issues/1366) — all prior R0–R10 evidence, T00–T08, status, open obligations and Delivery-First/Web-First execution ownership.  
**Historical full strict integration**: experiment model SHA `671c5fac858de000c867d03284413add204d2b01` (35/35 model; 41/41 Python; 16/16 paired; Source/Model/Toolchain PASS), frozen in `formal/v4.19/r10/FINAL_INTEGRATION_RECEIPT.json` at `62b00b070744887e39b37b514ffb2390f4cb2666`.  
**R11 actual strict integration**: model HEAD `9a6fb6f5a2b93fa45ed75e4dc39b29c367efacff` and candidate source HEAD `dac263fa4c0ab155406d2f2117459b34322cc988`; 61/61 actual Python tests, 35/35 native cases, 16/16 independent SMT pairs, tool/source/model/trace pre/post PASS, committed as `formal/v4.19/r11/EXECUTION_RECEIPT.json` at `a501dead1ab0b44c3cb460f891a1a7ff47cba8d2`. Later `formal/v4.19/coverage/` source-audit commits have not changed those pinned executable subjects; their metadata-only checks are not fresh native model runs.  

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

## 13. R9 验证器可用性、工具安全及真实差量重检（2026-11-10）

针对验收工具本身而非新增 SMT 公式的根缺陷，R9 修改 `formal/suite/expanded.py`：

- **R9-PY-P1-01（缺失 TLC 的收据崩溃风险）**：旧 `run_case()` 的 TLC JAR 缺失分支只返回 `id/status/tool/inputs_sha256/reason`，而 `main_v1()` 汇总会读取 `property_id`。因此缺失可选 TLC 时可能在 Python 汇总阶段抛出 KeyError、无法写出预期 `BLOCKED/NOT_RUN` 收据。修复为完整统一结果结构，新增缺失 TLC 三用例的测试。
- **R9-PY-P1-02（身份不可信二进制被执行）**：R7 引入了双次工具 SHA 校验，但原 runner 只在结果裁决时拒绝不符工具，仍可能先执行假冒的 Z3/cvc5。R9 把工具身份检测和模型来源检测一同作为**执行前预检**；未登记或错误哈希的工具一律不执行并 fail-closed。由已通过身份检测的工具产生的明确 `FAIL` 继续优先于缺少源码 checkout 的 `BLOCKED`。测试通过 mock 信任边界隔离这两种不同情况。
- T08 真正利用 v4.18→v4.19 候选的 `formal/v4.19/r5/RULE_CROSSWALK.json` 与 R8 的 10-Property DAG 做增量失效演练，而非只构造 synthetic 输入。已固定的 7 个源中有 **6 个发生候选差异/新建**，传递失效为 **10/10 Property、35/35 Case**；单独变更集成 DAG 文档时为 **5/10 Property、15/35 Case**。未映射文件若输入 `--changed-source` 则返回空选集，正式 source-bound 裁决必须 BLOCKED/STALE，绝不能等同于 PASS。新增回归核对这些数据。
- **实际执行边界**：本轮已经通过 GitHub 原文/结构核对、固定差量集合的动态依赖分析并提交代码与测试；**完整 Git 源码与工具环境下的 Python unittest 和 35-case R9 严格验证均 NOT_RUN**。R5 曾在它自己的 Exact HEAD 27/27 PASS，R6/R8 有新增原生模型的增量执行收据，不能据此给 R9 当前 HEAD 标注 PASS。工具提供的 `toolchain.py` 字节检测无法证明整个宿主或动态加载库可信，仍按原范围披露。
- R9 继续不新增 FIR、调度器或新正式 ADS 规范。建议下一步只做**一次完整的当前 HEAD + 候选 HEAD 双工作树修复/验证/独立语义审核**，避免无必要的人工轮次往返。

R9 原生增量用例新增 **0 个**，试点仍是 10 个性质与 35 个模型用例，完整 ADS 规则分母依然 UNKNOWN。

## 14. R9 已执行的精确 Git-blob 工具侧回归（2026-11-10）

本轮在校验器本身的最后一道 `--version` 路径发现并消除了遗漏：**R7 原校验器虽然拒绝哈希不匹配的工具，但仍先执行其 `--version`**；R9 将哈希检查前移到任何原生工具版本探测之前，并增加副作用哨兵负面测试。修复后将 GitHub 的 `formal/suite/toolchain.py` 与 `formal/tests/test_toolchain.py` 逐字节重建到隔离的 Python 工作目录，`git hash-object` 与 GitHub blob 1:1 一致，执行**5/5 unittest PASS**。使用用户提供离线分发归档抽取的 Z3 5.3.3、cvc5 1.4.2 和 TLC 2.19 JAR 真实核对**3/3 PASS**，版本和 SHA256 与 `formal/tools/inventory.json` 一致。

详细实际执行收据在 `formal/v4.19/r9/EXECUTED_RECEIPT.json`，根因与适用边界在 `formal/v4.19/r9/FINDINGS_AND_LIMITS.md`。注意 `test_expanded.py` 新增的完整 runner 测试（缺失 TLC 结果结构、错误工具执行前阻断、R8 真实差量选择）、R8 35-case 严格双 worktree 源绑定及独立语义评价仍未执行；**新轮次不得自称 R9 全套 Source-bound PASS**。当前仍为 10 个试点性质 / 35 个声明模型用例，ADS 全规范义务总数未知。

## 15. R10 双求解器缺失的 Fail-Closed 证明资格（2026-11-10）

**修复缺陷 R10-PY-P1-01：** 旧 `solver_differential(selected, results)` 遇到一个模型只登记了 Z3 或只登记了 cvc5 时直接 `continue`。如果配对用例从 `suite.json` 及索引/Traceability 一同消失，验证器可得到空/不完整差分结果，却没有明确指出缺少独立交叉复核。这与当前正式声明的 Z3/cvc5 交叉比较资格不符。

**最小修复：** `formal/suite/differential.py` 增加 `require_pairs=False`（历史单求解器兼容）；要求配对时，每个 `(property_id, model, purpose)` 的 Z3+cvc5 两侧必须各有唯一用例和一致结果。缺侧、重复 ID、孤立结果、工具来源错位或实际结果不一致都给 `INCONCLUSIVE`。当前 `formal/v4.19/r10/suite.json` 从 R8 35-case suite 复制，只增加 `require_solver_pairs: true`；主运行器根据 Git 固定的 Suite 字段调用比较器。R8 历史文件和所有已有 Case/Property 的内容保持不变。

**实际单元回归（精确文件级）：** Python 3.13.5 的 `formal/tests/test_differential.py` 在隔离工作目录运行 6/6 PASS、exit 0；`formal/suite/differential.py` 和 `formal/tests/test_differential.py` 的本地 `git hash-object` 分别为 `0266543c4edb991472ce781615b2bb8e77a5307b` 和 `34ceb558d67a5a42a9c540dde95471f4059de3dc`，与 GitHub 提交 blob 完全一致。GitHub metadata 校验发现当前 35-case 套装包含 16 对 SMT（32 Case）、3 个 TLC Case、10 个试点性质，反向 Source→Property→Case 链接没有缺失。新增 `test_expanded.py` 集成检查已提交但完整 Git 工作树下尚未执行。

**验收仍受限：** 这不构成 R10 35/35 Source-bound PASS；R5 27/27 历史严格验证仍按旧 HEAD 引用，R6/R8 分别有 4 个增量模型结果。当前缺少双 Exact-SHA Git worktree 的完整 `formal/tests` 回归、35-case 最新 runner 严格重跑、R8 新模型的独立语义复核，真实 GitHub CAS/Claim/Host/CI/Release 也仍未建模验证。ADS 规则义务分母保持 UNKNOWN，不引入正式 Gate、FIR 或 Node 版本限制。

R10 机器化收据：`formal/v4.19/r10/EXECUTION_RECEIPT.json`。

## 16. 统一主 Issue 回溯入口（2026-11-10）

历史验证 R0–R10 不再以聊天记录或任意单轮 JSON 作为项目进度入口。**[#1366](https://github.com/kaicreator-mm/ai-development-standard/issues/1366) 是本实验唯一主进度与工作索引**，保存 T00–T08 任务、轮次原始证据、历史 Exact-SHA、R10 的 35/35 与最新 HEAD 的 NOT_RUN 区别、剩余证明义务以及 Delivery-First → Web-First 派发规则。原始收据和模型**仍保留在 Git 版本化目录**，不复制粘贴覆盖、不回写修改历史 PASS。

后续执行前先读 Issue #1366 和本文件，再刷新候选 PR #1365 与实验分支 HEAD；有重要实际结果则提交 Git 固化，并在 Issue #1366 追加对应 Exact-SHA 与 PASS/BLOCK/NOT_RUN。只有真正独立、持续性强的任务才创建按需子 Issue；默认 Web Builder 连续完成实现、修复、测试和收据，本地 Agent 仅限 Web 缺失能力的最小一体化修复与复测。

## 17. Issue #1366 / T01 有效规范文件映射与真实 Discovery Demo（2026-11-10）

**由主 Issue [#1366](https://github.com/kaicreator-mm/ai-development-standard/issues/1366) 统一跟踪，不建立每轮子 Issue。** 从观察 v4.18 baseline `ac7e7e51de3a7ac27343f16a96568c0b0f2c5349` 到未合并候选 PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988`，使用两份完整 Git Tree 与完全一致的 `standard-manifest.json` Git blob，逐字节枚举 Manifest `normative_standards` 的 **46 份**正式规范文件（另有 2 个兼容入口不计作重复规范 authority）。`formal/v4.19/coverage/normative-file-matrix.json` 固定每份文档的两端 Git blob/候选大小/映射 Property IDs；`INVENTORY_READBACK.json` 记录 4 个负面矩阵变异的拒绝与结构审计。结果：**3/46 规范文档由现有试点性质引用，43/46 尚无映射；候选相对于该观察基线 7/46 文档发生 blob 变更，包含 5 份尚未映射的变更文件**。R5 选定的七条 crosswalk source 只是试点子集，不是整个 Manifest 的变更分母。**规范条款/证明义务的计数仍 UNKNOWN**，不得将 3/46 与 10/10 pilot Property 误认为规则级证明覆盖率。

五份发生变更但尚未映射的候选正式文件：`ARCHITECTURE_DESIGN_STANDARD.md`、`DEVELOPMENT_WORKFLOW.md`、`IMPLEMENTATION_QUALITY_STANDARD.md`、`TASK_DECOMPOSITION_STANDARD.md`、`TESTING_STANDARD.md`。其中优先对 PR #1365 增补的 `TESTING_STANDARD.md` §6.1（执行测试发现清单应匹配声明范围）进行实际 Python 正反 Demo，避免新增无必要的 SMT 公式。

**真实最小 Demo：** `formal/v4.19/coverage/discovery_probe.py` 生成一个根测试和一个嵌套测试，以独立 Python 子进程执行 `unittest discover`，由被执行测试写 `.ran` 哨兵，按真实运行 ID 对照声明套装。`-p test_root.py` 虽然进程 PASS，却只执行 **1/2**，嵌套要求保持 **NOT_RUN**；`-p test_*.py` 实际执行 **2/2**，声明套装才可 PASS。第一次进程内复用 `unittest.TestLoader` 曾因 `sys.modules` 跨临时目录缓存失败，已改为独立子进程修复。**隔离的仓库形态 Python 3.13.5 unittest 4/4 PASS**（原始日志 SHA256 `ae1481edad2e8e05e8791c8c269fbde2038495d50654604fd235bf0f0c381c5e`），GitHub 提交的两份 Python blob 与实际运行过的本地 Git blob 一致：`37b5b3852ce01c518c0ce1afe1ee7a01f739373f` / `bffd765812ba3e261c94e08b88166c160e61fe83`。完整收据在 `formal/v4.19/coverage/DISCOVERY_DEMO_EXECUTION.json`。这仅证明 synthetic test collection 情形，不证明真实 CI/provider、全部 ADS 规则或 LTL/SMT 语义等价。

**新 HEAD 的完整验收边界：** GitHub 静态盘点当前 `formal/tests/test_*.py` **47 个测试方法**，不是可冒称的 47/47 实际 PASS；R10 历史 41/41 绑定旧 SHA、当前独立运行了新增 4/4。最新 HEAD 严格 `formal/tests` + R10 的 35 原生模型全套仍 **NOT_RUN**；无新 Gate、冻结、合并或发布。

## 18. 主 Issue #1366 — 收据 postflight 资格与 Task DAG 虚假串行最小反例（2026-11-10）

**根因与真实负面：** 在 `expanded.py` 的收据摘要中，工具 `tool_versions` 曾只从执行前的 `toolchain_before` 派生。隔离 Python 负例用 `preflight=PASS, postflight=FAIL` 证明 `tool_versions.z3.status` 仍可能是 `VERIFIED`（负面断言如期失败）；**原本的整体 strict verdict 仍已根据 after-check 阻断**，故问题为 P2 证据元数据一致性，而不是已确认 ADS 规范缺陷。现在生产 runner 使用 `tool_version_report(toolchain_before, toolchain_after)`：仅两端 PASS、二进制/JAR 摘要一致才显示 `VERIFIED`，否则 `REJECTED`；收据写入不再次启动原生工具。保留一个参数形式只作历史单测兼容。固定 `formal/v4.19/coverage/POSTFLIGHT_RECEIPT.json` 及修复说明。

**真实最小 Task DAG Demo：** 从未映射的候选 `standards/TASK_DECOMPOSITION_STANDARD.md` §13.1 提取一个可证伪区分：仅为了后续 Review/Release 汇合而形成的边与真正需要上游集成代码或共享写集的边不同；脚本 `dag_edge_probe.py` 给出 `POSSIBLE_FALSE_SERIAL_EDGE` **建议**，但原生依赖存在时仍 `HOLD_NATIVE_DEPENDENCY`，不变更真实 GitHub Issue Dependency、不发 Task Claim、不授权并行执行。实际代码/共享写集依赖维持 `MATERIAL_SERIAL_EDGE`；缺乏冻结依据或类型错误保持 `UNKNOWN / NOT_AUTHORIZED`。`formal/v4.19/coverage/DAG_EDGE_EXECUTION.json` 绑定模型与源规范的候选 SHA。此脚本仅用于 synthetic bounded evidence 试点，不替代真正 Task DAG authority 或工作流引擎。

**已实际执行：** Python 3.13.5 下新增两组源代码回归各 **7/7 PASS**，在同一隔离仓库形态组合再次运行 **14/14 PASS**，组合日志 SHA256 `083a53df9aec4a557ad8224b806119c37f0319e89d1662dfe2b0429be4fb6718`。两组 Python test 文件和 DAG Demo 源文件在本地测试后取得 Git blob，GitHub readback 与本地 exact blobs 一致。另实际执行了前一版本收据错误的**预期失败**负面重放：非 PASS，不得计入通过项。

**覆盖口径：** 当前 Git `formal/tests/test_*.py` 有 **11 个源文件、61 个静态声明测试方法**（原来 47 + 当前两组各 7）；这不等于最新 HEAD 全部 61/61 已执行。历史 R10 的 35/35 native strict + 41/41 Python PASS 只绑定 `671c5fac...` 的模型/对应候选 Git SHA；最新 HEAD 的完整 strict suite 和全 61 Python `NOT_RUN`。脚本 Source→Model 自然语言等价、全部 ADS 规范义务分母和实际 GitHub CAS/CI/Host/Release 均未证明。**后续首要工作应集中一次精确 SHA 全量集成，不继续无界增加工具/测试轮次。**

## 19. #1366 真实 Dispatch 消费者的项目版本准入（2026-11-10）

主 Issue #1366 的 R12 源码审查确认：候选 v4.19 的 `schemas/dispatch.schema.json` **7/7 Profile→Role** 条件正确，辅助函数与模拟 Claim Admission 测试不能直接证明生产者按当前项目钉死 ADS revision 完成原子 Dispatch。原始收据 `formal/v4.19/coverage/CANONICAL_DISPATCH_CONSUMER_READBACK.json`。

为防止用错误版本系统重复证明，本轮进一步真实读取 `kaicreator-mm/tally` 的 **main**（`e988321439f65b55936a691c02250b6d62a29409`）和 **version/v2**（`7ebb1cdd0a79fc82cc938e35f852a80dd8e15332`）Git HEAD/TREE 和 `.dev-standard/VERSION` / `.dev-standard/PROJECT_OVERRIDES.md`：两个 `VERSION` 都精确声明 **ADS 4.18.0** `revision=2c395c55569fe2edf3f4135f12d3d069e526d0b7`，且 Overrides 将 A1_MANUAL_PROTOCOL v4.18 接入限制为 v2 版本线，保留历史 `main`/旧 Claim 的原准入。**Tally 本次观察分支不能作为 v4.19 Profile/Claim/生产发布的真实消费者**，不能把其同名 `Service.Dispatch` 当作 ADS Canonical Dispatch 的实现。两个分支 Git blob 一致，5 个负面准入变体拒绝、1 个正面控制通过，只是来源/资格判别，不是运行时验证。证据 `PROJECT_PIN_CONSUMER_ELIGIBILITY.json` 与 `PROJECT_PIN_CONSUMER_DECISION.md`。

**调整：** 先取得一个实际有效的 v4.19 项目版本 pin、冻结 Task/Claim 与生产者发布路径，再做最小真实消费链检查（enriched→pinned-schema→role/profile→Claim/currentness→atomic publication→readback）。未满足版本准入时 `NOT_PROVEN`，不再添加模拟状态机/重复 R11 全量测试，不派本地 Agent；无 ADS 规范修改、Merge、Freeze 或 Release。

## 20. #1366 46 文件规范措辞候选扫描与源义务分母（2026-11-10）

**交付：** 由主 Issue #1366 继续管理，针对候选 PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988` 按其 `standard-manifest.json.sections.normative_standards` **逐一实际读取 46/46 份规范文件**，每份完整 Git blob 和已有 `normative-file-matrix.json` 精确匹配。因连接器单次调用数限制，分成 5 个 Git blob 暂存批次（10/10/10/10/6），最终**一个 Git 提交**将五批与 `NORMATIVE_MODAL_SCAN.json`、`NORMATIVE_MODAL_SCAN.md` 固化。完整来源检查与 5 个结构负面变异均 PASS。

**实际扫描数据：** 46 份规范文本中，**1,509 条 Markdown 物理行**包含选定英语或中文模态标记（MUST/SHALL/REQUIRED、NEVER/PROHIBITED、SHOULD、必须/不得/禁止等），其中 **7 份变更文件的 420 行**满足扫描条件。扫描排除部分代码块和标题，保留了候选源码行号、Git blob 与有限示例。**1,509 不是原子规范义务数，420 不是新义务数，均不构成证明覆盖率分母。** 一个源行可能有多个规则，也可能仅是举例；没有明确模态词的规则会漏检。条款/义务总分母仍 `UNKNOWN`。这是为下一阶段人工语义拆分建立导航索引，而不是批量生成 SMT 用例。

**优先级调整：** 下游 Tally 两条被检查分支确实采用 ADS 4.18，故不能充当 v4.19 候选 Dispatch 真实消费的证据；但这只阻塞真实 Producer/Claim 端到端证据，**不阻塞规范本身的源语义建模**。下一步应从现有 21 项已人工筛选的高风险候选差异入手，少量逐条拆分权限/前置/例外/未知/反例/版本适用并对照既有 `ADS-P-*`；有可证伪且现有模型未覆盖的真实跨规则矛盾才新增最小 SMT/TLC。R11 全部 native/Python 验收可按原 Exact-SHA 复用，无须重复 Local Agent 验证；不得把词法索引当成模型证明或正式 Release Gate。

## 21. #1366 原子义务拆分与模型来源关联资格（2026-11-10）

在真实采纳 ADS v4.19 的 Dispatch 生产者尚未确认时，不能把 Tally v4.18 用作生产级反例；但仍可进行候选规范源码逻辑审查。使用 PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988` 精确 Git blob，把现有 21 项优先变更观察拆成 **25 项待独立审查的原子化解释草案**（6 个专题）。自对抗修正识别并拆开 LOCAL_VALIDATION 三项条件（validator-only / exact-SHA / real local gap）、Dispatch 预发布的 full payload vs active pinned schema、Architecture 未运行 UNKNOWN vs 后续被授权的有界集成检查。原始 `ATOMIC_RULE_SAMPLE.json` 逐项附源码路径/行/锚点、作用范围、前置、单项义务、预期负面反例、类比的 `ADS-P-*`、证据等级和未证明边界。

**最关键的自我修正**：25 项中仅 **14 项**的既有 Property 源索引直接引用同一规范文件，其余 **11 项**只是主题类比，不构成来源关联。即使在 14 项中，**条款语义等价证明仍为 0**；全部 ADS 原子规则分母 `UNKNOWN`，不得写出 `14/25` 的证明率。6 个原子文档结构负面变异、另 7 个复合拆分相关结构负面变异和 3 个 Property 来源误连负面检查均拒绝（不同阶段的局部结构检查，非独立语义证明）。本轮 **仅覆盖源证据文档**，不更改 runner/模型、不重跑已绑定 SHA 的 R11 严格 35/35 与 61/61、不派本地 Agent。

**下一步**：先独立复核 `DP-01S/DP-02/DP-05/DP-06` 的版本绑定/发布瞬间一致性/零接受写入，再决定是否存在可用最小 SMT 反例；无实际源依据不继续堆模拟模型。文件索引：`formal/v4.19/coverage/ATOMIC_RULE_SAMPLE.json`、`ATOMIC_RULE_SAMPLE_REVIEW.md`。

## 22. #1366 R13 — Dispatch 发布前完整对象/有效 Schema/写入同一性最小双求解器验证（2026-11-10）

候选 `GITHUB_AGENT_INTERACTION_PROTOCOL.md` 精确 blob `935a905d593d7aec027cb54b5b137250ca14a4c1` 的 `DP-01F/DP-01S/DP-02/DP-05/DP-06` 义务指出 R8 旧 `reservedA` 模型仅检查 READY/generation/publication ambiguity，并未表达 Schema pin 与 checked-vs-published object。以原 `reservedA` 语义相同的窄抽象跑出 **4 SAT** 非受约束见证，不能把 reservation SAT 解释为真实 Dispatch 已接受。

新增 `formal/v4.19/r13/` 自包含实验模型与真实执行脚本：发布前必要条件模型 **11 项**（2 SAT 正例、9 UNSAT 禁止接受状态）；Z3 5.3.3 与 cvc5 1.4.2 各自 15/15、共 **30/30 求解结果符合预期**。**6/6** 删除关键 guard 的变异均被两个求解器检测；未钉死的工具测试文件在子进程启动前被拒绝。验证脚本及原始 JSON 收据与实际运行文件的 Git blob 一致，二进制 SHA256 与 R11 工具匹配。

这是 `BOUNDED_SOURCE_HYPOTHESIS_PASS`，**不是**真实 GitHub Controller/Claim CAS 证明、自然语言⇄SMT 的已证明等价或全 ADS 合规证书。新模型不修改原 R11 35-case/61-Python 受测基线，R11 历史 PASS 继续按其 Exact-SHA 复用。后续先做独立语义复核并寻找确实采用 v4.19 的版本钉死真实发布者；没有时真实消费维持 `NOT_PROVEN`。无本地 Agent、正式规范修改、Gate、Merge、Freeze、Release。

## 23. #1366 R13 原生输入绑定 fail-closed 修复（2026-11-10）

执行复盘发现 `R13-RECEIPT-P2-01`：R13 runner 原来记录模型 Git blob，却没有与固定的受审 Blob 作硬性比较；同一 SAT/UNSAT 的非授权模型微调可能被错误判作 PASS。**已在原实验写集直接修复** `run_proofs.py`（模型 2/2 Git blob＋Z3/cvc5 2/2 binary SHA256 前后检验），并使 `run_mutations.py` 同样钉死其源输入/工具，临时变异模型单独允许变化。实际 Python fail-closed **6/6 PASS**；双原生求解器 **30/30 PASS**，6/6 删除约束变异被检出；模型与工具 pre/post **2/2 PASS**。原 R13 收据及其旧 Exact-SHA 历史证据保留，新收据为 `REBOUND_SOLVER_EXECUTION.json`、`REBOUND_MUTATION_EXECUTION.json`、`RECEIPT_BINDING_REPAIR.json`。

经同一 Builder 自对抗源码审查，R13 的 `DP-01F/01S/02/05/06` 仍只是单个拟议新 Dispatch 发布的必要条件**假设**：未验证实际 pin 读取、Schema bytes、时间顺序、GitHub CAS/write-readback，旧 R8 `reservedA` 的 SAT 亦仅针对 reservation。**独立语义审核 NOT_RUN**，源规范↔模型严格等价和正式 ADS 全规则证明仍 `NOT_PROVEN`。R11 历史 61 Python/35 原生 strict 不重跑，未修改其固定模型或 ADS 标准；后续优先独立语义复核，而非继续堆积 Demo。

## 24. #1366 R13 Schema bytes 必要条件的真实测试覆盖修复（2026-11-10）

推进前先对前一 R13 的 native 查询与变异覆盖作源对抗审核：`publishAdmissible` 有 **10 个原子 guard conjuncts**（7 Boolean + 3 equality），但 R13 只有 9 个禁止接受查询，遗漏了 `schemaBytesVerified` 的假条件。实际将 guard 中 `schemaBytesVerified` 删除而不改变其他内容，Z3/cvc5 的 11 项旧查询全部同结果，证明现有套装有真实盲区，属于 **R13-TEST-P2-02 实验验证覆盖**，非 ADS 规范缺陷。旧原始/变异收据不改写。

**本轮已执行修复**：在原 `formal/v4.19/r13/publish-safety.smt2` 增加 N10 `acceptedDispatch ∧ ¬schemaBytesVerified → UNSAT`，变异脚本加一项删除此 guard；Python 添加对全部 10 项 guard 每项至少有显式禁止接受反例的结构约束（旧模型实际红 9≠10、新模型绿）。经真实 Z3 5.3.3 与 cvc5 1.4.2 **各 16/16、共 32/32 查询符合预期**，**7/7 变异均被两求解器检出**，Python **7/7 PASS**，模型/原生工具双时点 Exact-SHA 与历史固定 SHA256 继续 PASS。原始 negative-red 和新 native 结果分别固定于 `SCHEMA_BYTES_OLD_BLINDSPOT_EXECUTION.json`、`REBOUND_V2_SOLVER_EXECUTION.json`、`REBOUND_V2_MUTATION_EXECUTION.json`，总收据 `SCHEMA_BYTES_COVERAGE_REPAIR.json`。

R13 仍只是在**假设发布必要条件**前提下的一次有界安全性测试：尚无真实 v4.19 项目版本采用、Dispatch/Claim 生产者、完整 Schema bytes 核验／GitHub CAS、时序或独立语义评审收据，严格标注 `NOT_PROVEN`。R11 历史严格执行不重复，本轮只修改实验模型/测试/收据和本实施计划；下一步优先真正独立审核该来源绑定模型再决定是否需要新不变量，不扩大模拟 Demo。


## 25. Issue #1366 R14 — R13 规范到模型的 Fresh Source-First 语义边界审核（2026-11-10）

本轮重新读取候选 PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988` 的 `GITHUB_AGENT_INTERACTION_PROTOCOL.md` 源 Git blob `935a905d593d7aec027cb54b5b137250ca14a4c1`，实验受审 R13 `publish-safety.smt2` blob `515454a82171c668739708ef50c46a254dcd9cc8`，以及固定 Runner 和 10 项负例结构测试；GitHub 实际读回的静态约束 **16/16 PASS**，完整机器收据保存在 `formal/v4.19/r14/SOURCE_MODEL_READBACK.json`，逐项语义差距在 `R14_SOURCE_FIRST_SCOPE_REVIEW.md`。

发现并限定三项未覆盖边界：**(1)** 源 §10 要求发布 READY/QUEUED *或* accepted 前的校验，而 R13 模型只看 acceptedDispatch/ClaimMutation；**(2)** `prePublicationCheckCompleted` 是布尔假设而非事件先后关系；**(3)** schema bytes/对象相等/Claim CAS/历史 append-only readback 未由真实生产者证据导出。**不是**已证实的 ADS 规范问题；模型在其有界假设内保持原 R13 历史 32/32 Z3/cvc5 + 7/7 变异资格，本轮 **没有执行新原生 SMT/Python**，未扩大 R13 的 Source-to-Model 等价范围。外部真正独立语义审核仍 `NOT_RUN`，合法 v4.19 发布者仍 `NOT_PROVEN`，条款级总数 `UNKNOWN`。

后续关键路径：先从具有有效项目 v4.19 pin 的真正 Producer / 当前 Task / Accepted Claim 取得校验前后与 READY/QUEUED/accepted 发布读回证据；没有时以独立源码审核和现有边界限制收敛，不继续无界叠加模拟 Controller 或对未修改的 R11 严格套件重复派发 Local Agent。无正式规范修改、CI Gate、Merge、Freeze、Release。


## 26. #1366 R15 — 真实 Dispatch Schema 的结构验证与授权边界（2026-11-10）

R14 已确认三个源语义缺口；本轮不再无界增加模拟 Controller/SMT 模型，而是按 Reuse-First 使用候选 PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988` 的真实 `schemas/dispatch.schema.json` Git blob `5d9233b6b881d9d92f66fc6cd5307a05a0fdbe2f`，复用仓库已有 `scripts/test_protocol_schemas.py` 的 dependency-free Schema subset 检查能力。新增 `formal/v4.19/r15/schema_boundary.py`、`test_schema_boundary.py`，并将候选 Schema **原有 blob** 作为 `r15/fixtures/dispatch.schema.json` 引入，使 Git checkout 可以用同一固定字节复跑。

**真实源码观察**：`LOCAL_VALIDATION` 的 validator 角色条件 Schema 有效，但 `requested_head_sha` 和 `validation_profile` 虽然 required，值仍可以为 null；任意形状合法的 40-hex `pinned_standard_revision` 也不能证明项目有效 revision；`dispatch_state=READY` 的 Schema PASS 不能证明实际发布前检验和 CAS。已基于 GitHub 真实候选 Schema 运行 **14/14 JavaScript subset 结构正反例匹配**，并在隔离容器中以**合成 Schema 子集 + 本地 checker 替身**执行 Python 逻辑回归 **12/12 PASS**；两者均明确标记范围。**真正候选原始 Schema + 仓库原生 Python checker 的组合测试未在本环境执行 = NOT_RUN**，不能把 12/12/14/14 写成 R15 的完整原生 Source-bound Python PASS。运行命令在 `r15/R15_SCHEMA_BOUNDARY_REVIEW.md`；R11/R13 的历史原生证据仅按原 SHA 继承。

新代码只产生 `SHAPE_VALID_ONLY/INVALID_SCHEMA/BLOCK`，永远 `canonical_admission=NOT_PROVEN` 和 `publication_authorized=false`，不建立新的 Dispatch authority。最新优先项为精确仓库组合 Python 验证或已有合法 v4.19 生产者的真实 pre-publication/Claim-CAS readback（未确认时不作实际授信）。独立源码到模型等价审核仍 NOT_RUN，全 ADS 原子义务分母 UNKNOWN；不修改正式规范、不增 Gate、不合并/Freeze/Release。


## 27. #1366 R15-P2-01 — 精确 Schema 身份验证入口加固（2026-11-10）

在 R15 新代码提交后复盘发现 `assess(..., expected_blob=...)` 允许调用者覆盖应固定的 source Git blob，产生虚假的 `EXACT_BLOB_PASS` 元数据（虽仍不授予发布权限）。已移除外部覆盖参数，固定使用 `PINNED_SCHEMA_BLOB`，并新增 `test_cannot_inject_expected_blob` 负例。代码和测试文件已按相同实验写集提交；当前 Python 声明 **13 项**，修改后真实仓库源组合 Python 执行仍 `NOT_RUN`，不得把提交前基于合成夹具的 12/12 直接提升为最新代码 13/13。

同时对实验分支与 PR #1365 的 `scripts/test_protocol_schemas.py` 真实 Git blob 作版本差异检查：文件 SHA 不同（`248d652...` vs `96edf241...`），但 `assert_supported_schema` + `validate_subset` 源码函数体 **5,706 字符逐字一致**。继续复用现有校验器，不创造新 Schema Engine。R15 的真实候选 Schema 结构正反案例仍只具备已记录的 JS 14/14 证据，完整 Python 最新 HEAD = NOT_RUN；没有修改 ADS 正式规范、CI Gate、PR #1365 或 R11/R13 历史收据。


## 28. #1366 R15-P2-02 — exact-source Python 集成的真实 red→green 闭环（2026-11-11）

本地 Agent 在 detached Exact-SHA 工作树（`3257080` / TREE `5d93648`，运行前四个关键文件 blob 经 `git hash-object` 与提交 blob 逐一相符，fixture blob 与候选 `dac263f` 的 `schemas/dispatch.schema.json` 同 blob）首次真实执行 R15 记录的标准命令 `python -m unittest discover -s formal/v4.19/r15 -p 'test_schema_boundary.py' -v`，结果 **exit 1、0 项执行**：真身 `scripts/test_protocol_schemas.py` 第 619 行的模块级兄弟导入 `from v34_rules import ...` 在仅 REPO_ROOT 进 sys.path 时不可解析。此前隔离 12/12 用的是本地 checker 替身，从未覆盖这条真实接线——**R15-P2-02 实验证据基础设施缺陷**（非 ADS 规范缺陷，P0/P1/P2 仍 0/0/0）。

同写集最小修复：`schema_boundary.py` 将 `REPO_ROOT/scripts` 与 `REPO_ROOT` 一并加入 sys.path（新 blob `15a8634e27946fca3c49db4f336687f4cf10bba3`），共享 checker 不改动。修复后双环境复跑 **13/13、零跳过、exit 0**：WSL2 Ubuntu 26.04.1（Python 3.14.4）与 Windows 10.0.26300（Python 3.14.7）。CLI `main()` 冒烟双环境各 3 案例：正例与可空 validator 形态 exit 0（`EXACT_BLOB_PASS` + `SHAPE_VALID_ONLY`，`publication_authorized=false` 恒成立），篡改 schema（fixture 字节+换行，置于工作树外）exit 2 `BLOCK`，observed blob `45a510f5...` ≠ 钉死值。

**资格口径**：exact-source Python 集成 PASS 绑定**修复后 HEAD** × 两个实测环境；`3257080` 原样提交在该项上是 FAIL（exit 1），不得回溯标记为 PASS。机器收据 `formal/v4.19/r15/EXACT_SOURCE_PYTHON_RECEIPT.json`，逐字日志 `EXACT_SOURCE_PYTHON_LOG.txt`（SHA256 `d1f1614d...`）。边界不变：真实 v4.19 publisher/Claim/CAS/readback `NOT_PROVEN`，源↔模型语义等价 `NOT_PROVEN`，外部独立审核 `NOT_RUN`，全 ADS 原子义务分母 `UNKNOWN`。无正式规范修改、无新 Gate、不合并/Freeze/Release。


## 29. #1366 R16 — 下游精确版本资格调查与独立审核准入准备（2026-11-11）

R15 exact-source Python 已由本地 Agent 在修复后实验 HEAD `4de398a02f4c96d20ad763ea11d81a9a40ff0266` 完成 WSL2 + Windows 双环境 **13/13 zero-skip PASS**（CLI 正负 3×2 实跑）；此前 HEAD `3257080` 的确切源组合曾因 `v34_rules` 导入失败，**不得后向提升 PASS**。本轮不重复 R15/R11/R13 未改动模型与用例，转向 R14 仍缺的真实发布者资格来源。

GitHub 原生读回实际检查了 **12 个仓库的 14 个指定分支元组**、每个 `.dev-standard/VERSION`：**8** 个具备明确旧版本 ADS pin（4.0/4.9/4.14/4.18），**1** 个仅有 `4.0.0` 且不含 ADS revision，**5** 个在所查 `main` 分支未找到该文件。**0/14** 能确认有效采用候选 PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988`。细节精确 HEAD/blob 与失败分类见 `formal/v4.19/r16/R16_CONSUMER_ELIGIBILITY_READBACK.json`；8 个合成资格负控都未被误判为真实 PASS。尤其 `domain-harness/dis/0.2.0-element-intelligence-r1` 和 `tally/version/v2` 的直接文件读取均明确钉在 ADS 4.18，不能作为 v4.19 Dispatch/Claim 生产 E2E。**本调查不是全组织/全分支穷举，未找到文件 ≠ 未采用 ADS**，更不代表全球没有 v4.19 使用者。

因此真实 v4.19 `enrich→effective pinned schema→authorized Task/Claim→serialized READY/QUEUED/accepted publication→durable readback` 仍 `NOT_PROVEN`，不为了完成指标强行借用旧项目或伪造 Claim。已将下一轮**真正独立源码/模型审核**的准确输入与 P0/P1/P2/缺口/实际执行收据要求固化于 `formal/v4.19/r16/INDEPENDENT_REVIEW_SCOPE.md`，当前仍 `NOT_RUN`；这只是待独立执行的审查合同而非独立审核通过。完整 ADS 原子规则分母 UNKNOWN。无规范/原模型/CI Gate/Merge/Freeze/Release 改动。


## 30. #1366 R17 — 独立审核实验 P2 源规范输入身份证据补链（2026-11-11）

在全新审核 HEAD `3dec2ae90f3a8bb6b926be22ecb5e14c9a7572b1` 的 `R13_R16_INDEPENDENT_REVIEW_RECEIPT.json` 中确认 `R13-R16-REV-P2-01`：R13 的原生 runner 对模型与工具 SHA256 做前后钉死，但未对候选协议/Schema 字节做相同绑定。**本轮在原实验 `formal/v4.19/r13/run_proofs.py` 中直接修复**，增加候选 Protocol `935a905d593d7aec027cb54b5b137250ca14a4c1` 和已有候选 Schema `5d9233b6b881d9d92f66fc6cd5307a05a0fdbe2f` 的前/后 Git blob 比对，任一漂移或缺失立即 `InputBindingError/BLOCK`；Protocol fixture 使用候选 PR #1365 原始 Git object，不人为重写。增加 `r13/test_source_binding.py` 6 项声明式负例/身份测试，原 SMT/原 R11/R13 历史执行收据不变。

**资格**：本轮对新程序 GitHub blob/结构进行读回验证；如未获得完整 exact-source Python 执行，不将新 runner 标为 Python PASS，更不将 R13 历史 32/32 paired 强行转移到修改后的 runner。冻结协议版本源 SHA 只能说明候选源码字节被钉死；不能推导 PR HEAD 在未来运行时没有变化，亦不能推导真正 Project/Task 有效版本采用、规范 ⇄ SMT 等价、真实 GitHub Claim/CAS 发布。最新状态见 `formal/v4.19/r17/R17_SOURCE_PROVENANCE_REPAIR.md` / `R17_SOURCE_PROVENANCE_RECEIPT.json`；独立审核实验 P2 标记为 `CODE_REPAIRED_AWAITING_TEST`，ADS 正式规范 P0/P1/P2=0/0/0；不增加 Controller toy-model、官方 Gate、GitHub Actions 或自动 Merge/Freeze/Release。


## 31. #1366 R17 收敛执行 — exact-source Python 与固定 SHA256 原生双求解器闭环（2026-11-11）

R17 P2 修复代码在其**被测 Exact-SHA `c5eb69c3fcd47ca934b4b87c8004131add6ad5d2`（TREE `762083f7a01355c01e4fc285772e6e926edea032`）**完成 §30 遗留的 `EXACT_SOURCE_TEST`：双 Exact-SHA worktree 全程 tracked 文件零修改，R11/R13 历史收据未重跑、未改写，候选 PR #1365 仍 OPEN/未合并。

- [x] **新旧输入绑定 Python 测试 13/13 双环境零跳过 PASS**：`unittest discover -s formal/v4.19/r13 -p 'test_*binding*.py' -v` 精确命中 2 个文件 13 项（`test_binding_preflight.py` 旧 7 + `test_source_binding.py` 新 6，无 "0 tests" 陷阱）；WSL2 Ubuntu 26.04.1 × Python 3.14.4 与 Windows 10.0.26300 × Python 3.14.7 均 `OK, exit 0`。**无 red 缺陷，无修复需求**。
- [x] **固定 SHA256 原生双求解器单次正跑 32/32**：修改后 `run_proofs.py`（blob `f2780a16…`）以 Z3 5.3.3（`fcd0ca76…`）+ cvc5 1.4.2（`6aecddf4…`）实跑，每求解器 16 项状态（reservation gap 4 SAT + publish-safety 2 SAT/10 UNSAT）与预期逐项一致、双求解器逐对相同；source/model/tool 前后 **12 项绑定检查全 PASS**。
- [x] **真实未钉死二进制负探针 BLOCK**：换用 SHA256 不符的真实 cvc5（`cc6781dd…`）执行同一 runner → `exit 2`、`pair_status=BLOCK`、求解器查询 **0 次启动**，fail-closed 源字节+工具绑定路径真实生效。
- [x] **证据固化**：`formal/v4.19/r17/{R17_PYTHON_BINDING_TESTS_RECEIPT.json, R17_PYTHON_BINDING_TESTS_LOG.txt, R17_NATIVE_DUAL_SOLVER_EXECUTION.json}`（含正跑完整 runner 输出与负探针输出嵌入）。

**资格**：`R17_EXACT_SOURCE_TEST_CLOSED / PYTHON_13_OF_13_DUAL_ENV_ZERO_SKIP / NATIVE_32_OF_32_PAIRED / FAIL_CLOSED_BLOCK_VERIFIED / R13_R16_REV_P2_01_CODE_REPAIR_EXECUTION_QUALIFIED`。独立审核实验 P2（`R13-R16-REV-P2-01`）的代码修复+实测链路闭环；ADS 正式规范 P0/P1/P2 仍 **0/0/0**。源⇄SMT 语义等价、有效 v4.19 项目 pin 的真实生产 Dispatch/Claim/CAS/读回仍 `NOT_PROVEN`，全 ADS 原子义务分母仍 UNKNOWN。不改正式规范、不加 Gate/Actions、不 Merge/Freeze/Release。


## 32. #1366 R18 — 将一个真实候选改动从“单行/单义务”细化为可审查的跨 Owner 原子片段（2026-11-11）

推进前核对最新 HEAD `5a81503d6f2a16b0f31ce053353bbdcadfcf9582`：R17 新旧输入绑定 Python 在 WSL2/Windows 各 **13/13 PASS**、修改后的 Runner 双原生 **32/32 PASS**、错误 cvc5 fail-closed BLOCK，实验 P2 已闭环。R11、R13 历史模型均无需重跑。下一主线转向 §6-B 的规范义务真实盘点，不再以增加重复求解用例作为进度指标。

**真实源码比较**：候选 PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988` 与观察基线 `ac7e7e51de3a7ac27343f16a96568c0b0f2c5349` 的 `IMPLEMENTATION_QUALITY_STANDARD.md` Git blob 分别 `c37c4a223e21764ebe211f0e7bdd886a2060c5e2` / `3beba2d0324d95674b7bad2ef621e2aa81c66563`；精确行比较保留开头 **42** 行、结尾 **50** 行不变，只插入**第 43 行一条复合规范段落＋第 44 行空行**。既有 `ATOMIC_RULE_SAMPLE.json` 仅以 `IM-01` 表示这条长规范段落。本轮新增 `formal/v4.19/r18/R18_DELTA_ATOMICITY_LEDGER.json` 中 **7 个待独立审核的候选叶子约束**（源码存在/加载不等于实际 selected path、可观察 contract behavior、禁止凭空产生新 Gate、未集成时 repair 或保留缺证、Testing/Integration 独占可执行证明、packaging seam material 时 clean installed entrypoint），明确条件、Owner、负面场景、精确源码锚点。联合读回 `ARCHITECTURE_DESIGN_STANDARD.md:51` 与 `TESTING_STANDARD.md:72`，确认设计/测试/实现 Quality 的语义 owner 分离。

**实际执行**：直接 GitHub exact-blob 与逐行源码对照、历史 `IM-01` 对照及文档交叉约束审计 **14/14 PASS**。这是 **source audit**，本轮没有重新执行 Python/SMT 或真实项目运行。7 个叶子仅为同一源段的待审细分，**不是**已批准的 7 条原子规则，更不等于将原 25 项台账升级为 31 项已证明性质。完整 ADS 全规范义务分母仍 **UNKNOWN**，外部独立语义审核与真实 v4.19 Dispatch/Claim/CAS 仍 **NOT_PROVEN**。源差量审查文档 `formal/v4.19/r18/R18_SOURCE_DELTA_REVIEW.md`；下阶段优先独立审核这 7 项的原子性/适用条件，再决定是否需要源消费者的最小可执行验证，不新增通用 FIR/Gate/Release 流程。


## 33. #1366 R19 — R18 复合规则盲审式语义纠偏，消除候选义务虚增（2026-11-11）

重新读取实验 HEAD `4044557fcf28a9a1b2beda8fcd0d7850f943c633`、R18 原始七项 `79f8b7411b3532bf8098345497a5353e3246e917` 与候选 PR #1365 精确规范源码 `c37c4a223e21764ebe211f0e7bdd886a2060c5e2`，并对照 Architecture `51fad2c5b35779bcd402eb62cab9a6e563e6dd93` / Testing `746ec1da78b45f2d2c1fa2177549acbcc6587ca2`。发现 `R19-REVIEW-QUALITY-P2-01`（**实验台账原子性 P2，不是 ADS 正式规范缺陷**）：R18 将 `SOURCE_PRESENT` 与 `EXPORTED_OR_LOADED` 两个不充分证据示例作为两条候选规则，且把 “not new workflow/Gate states” 解释性限制提升为单独可计数约束；而 `IM43-03` 的“实际选中调用”与“可观察契约结果”可以独立失败，应分别审查。

直接将 R18 **7 项草案**调和为 `formal/v4.19/r19/R19_RECONCILED_ATOMS.json` 中 **5 项待审核候选** `IM43-R1..R5`（选中调用、实际行为、repair OR disclosure、Testing/Integration 证明归属、仅 material packaging seam 时 clean installed public entrypoint），另单列 **1 项不可计数的解释性范围保护** `IM43-SCOPE`。完整保留 R18 七项及其历史 Git blob 不修改，提供 7→5+scope 的精确映射、每项源行位置、条件及反例。基于候选真实源码、历史台账、两份跨 Owner 标准进行 Web-first 源码审查与结构验证；不新增虚构 Gate、Runner、抽象 SMT 模型或非必要本地任务。

**资格边界：** R19 是同一助手场景下的 source-first 自对抗审查与计数纠偏，并**未**由不同真人/独立身份签署 Review；5 个细分未被升格为正式 ADS 全规范已批准“原子规则”，更没有产生源⇄形式模型语义等价、实测公共调用或真实 CAS 的 PASS。全规范义务分母依然 UNKNOWN。源代码和输入的受审 Scope 限于一个真实新增候选段落；R17 Python 13/13 双环境和原生 32/32 保持原精确 SHA 历史资格，不重跑。


## 34. #1366 R20 — 测试实际执行清单的源代码/日志/收据闭环（2026-11-11）

R19 后评估下一步：R11/R13/R17 Native/Python 都已各自 Exact-SHA 通过；R18/R19 以一个候选段落原子义务审查纠偏收敛。**不重复验证、不再增加同类抽象 SMT 模型**，改为消费真实历史测试执行结果，检验候选 `standards/TESTING_STANDARD.md:64–68` §6.1 的“实际选中/执行的测试方法清单 ≠ 命令名/绿色汇总数量”约束。

本轮直接从 GitHub 读取 R17 的两个实际 `unittest` 源文件、其双环境逐方法日志、机器收据，在固定 Git blob 下核对 **13 个声明方法的全限定 ID 与 Windows/WSL2 各 13 条执行 ID 完全一致**，无漏测、重复、额外 ID；真实执行是**历史 R17**，本轮是 **20/20 源码与证据回读**，不是原生测试重跑。新增 `formal/v4.19/coverage/executed_inventory_audit.py` 提供可复用的固定输入/源码 AST/日志/收据 fail-closed 读取；新增 `formal/tests/test_executed_inventory_audit.py`，在当前离线 Python 3.13.5 隔离仓库形状的合成 fixture 上实际 **9/9 PASS、零跳过**，其中含绿色但漏测、重复 ID、源码篡改、日志/机器收据篡改等反例。其实际原始输入读回与 Python fixture 执行的资格明确分离。

机器文件 `formal/v4.19/r20/R20_RECORDED_TEST_INVENTORY_READBACK.json`、审查 `R20_RECORDED_TEST_INVENTORY_REVIEW.md`。**新脚本在完整 Git exact-checkout 中对真实 R17 四份源文件进行整体 CLI 执行仍 NOT_RUN**，不可把隔离 9/9 称为完整实际工作树已运行；无新 Z3/cvc5/TLC。真实 v4.19 Claim/CAS 和标准⇄SMT 语义等价 NOT_PROVEN，全 ADS 原子规则分母 UNKNOWN。保持已通过 R17 的历史资格，不新建 FIR/Gate/CI，不合并/Freeze/Release。


## 35. #1366 R21 — 主 Issue 当前性修复与有限证明验收矩阵（2026-11-11）

重新读取当前实验 `5b65e0a8a2567e187783448ad7b1c2942c051289`、主 Issue #1366、候选 PR #1365 和 R11/R14/R16/R17/R20 精确 Git blob，发现主 Issue 顶端仍错误标记 R11 固化 HEAD `a501dead...` 为 **latest**，§6-A 仍保留 `[ ]`，但后面的 §10 和本实验 R11 机器回执已明确 `acceptance_stop_condition.met=true`（61/61 Python，35/35 Native，16/16 Z3/cvc5，source/model/tool pre/post PASS）。这是主 Issue 进度消费的当前性缺陷（项目管理/证据索引，**不是 ADS 正式规范缺陷**），应修正主入口而不是重复执行全套。

本轮将 M0–M4、§6 A–D、R20 单独待跑事项、R14 真实发布者资格/Claim/CAS 三个未证明边界固化于 `formal/v4.19/r21/R21_PROOF_QUALIFICATION_MATRIX.json` 和 `R21_CONVERGENCE_DECISION.md`：**A 只对已执行 R11 exact subject 已完成；M2 有界试点已通过；B/C/D 并非自动全部通过**。46 文件/7 变更/25 草案不是完整 ADS 原子义务分母；R20 Python 审计器最新 exact-checkout CLI 仍 `NOT_RUN`；PR #1365 OPEN/未合并、R16 14 refs 中 0 个合法候选 pin；R14-GAP-01/02/03 依赖真实有效 producer、serialized READY/QUEUED/Claim-CAS 与持久读回，不能用抽象 guard 替代。

本轮实际执行的是 **14/14 GitHub 收据/状态一致性读取**、原始状态纠偏；**不**执行全量 Python/Z3/cvc5/TLC 或伪造真实 CAS。R11、R17 的历史 exact-SHA PASS 仅作为已存在证据复用。主 Issue 顶端恢复到该轮最新 Git 提交与正确 §6-A 分类，旧 §7–§10 历史记录照存、不追认或覆盖。**止损规则：**无真实新增失败/代码变动时停止生成细碎同类验证轮次；下一个可执行的新代码门槛仅为 R20 精确工作树针对性执行，真实生产 E2E 门槛只在合法有效版本/producer 可识别后启动。
