# Architecture Research Demo Standard

## 1. Purpose

Architecture Research Demo（也可称 Architecture Spike / Executable Evidence Demo）用于消除一个会影响架构冻结或公共运行语义的 **重要 UNKNOWN**。

它的目标不是实现产品功能，而是用最小可执行系统证明或证伪一个明确假设，并产生可被 L2 Architecture Evidence 引用的 exact-SHA evidence。

核心原则：

```text
Demo resolves an architecture UNKNOWN.
Demo is evidence, not production implementation.
```

Demo 不得成为每个 Task 的固定前置 Gate。

## 2. Lifecycle position

默认位置：

```text
L1 Product Evidence
→ PRD / Scope Freeze
→ L2 Architecture Evidence
   ├── source/design/failure-case research
   └── Architecture Research Demo / Spike（按需）
→ L2 Architecture Freeze
→ Task DAG
→ L3（按需）
→ Production Implementation
```

PRD Freeze 决定“做什么/为什么做”。Research Demo 验证“候选架构假设是否成立”。L2 Freeze 决定“怎么做”。

PRD Freeze 后某个技术方案失败，默认应替换/调整候选架构，而不是自动重新打开 PRD。只有 Demo 证明产品要求本身互相矛盾、不可实现或成本/约束与 Frozen PRD 根本冲突时，才报告 Architecture Contradiction 并请求重新打开产品范围。

L2 Freeze 后的普通 Task 默认直接实现。只有新发现的高影响 Architecture UNKNOWN 才重新创建 Research Demo；不得机械执行 `Demo → Production` 双实现流程。

## 3. When a Demo is required

当以下条件同时成立时 SHOULD/MUST 创建 Demo：

```text
material architecture assumption is UNKNOWN
+ it can change architecture / public contract / durability / failure semantics
+ static/source/design evidence is insufficient
= executable evidence required
```

典型场景：

- 新 runtime/control-flow/persistence/compiler boundary；
- crash/restart/retry/idempotency/exactly-once or at-least-once semantics；
- concurrency/transaction/data-integrity behavior；
- 新平台/SDK 的关键运行限制；
- 两个候选架构方案的差异无法仅靠静态分析判断；
- dynamic workflow / sandbox / distributed coordination / cache identity 等高影响机制；
- 文档声称支持但实际 runtime behavior 仍未验证的关键能力。

通常不需要 Demo：

- 已有 Frozen L2 + proven pattern 下的普通实现；
- CRUD、局部 UI、简单 refactor；
- 只需 unit/contract test 即可确认的 implementation detail；
- 已有等价 exact-SHA executable evidence 且环境/假设未变化；
- 为了“形式完整”而重复已经证明的机制。

## 4. Every Demo starts with a falsifiable hypothesis

Research Issue MUST 写出可证伪 Hypothesis，不能只写“研究 X 是否适合”。

推荐形式：

```text
If <precondition / crash window / input>,
then <observable behavior>,
and <counter/state/effect identity> must equal <expected value>.
```

示例：

```text
If a stale XState snapshot is restored after an AI result has been durably committed,
then the workflow must converge to the expected parent state,
and underlying ModelPort execution count must remain 1.
```

最终状态只能是：

```text
PASS
FAIL
BLOCKED
```

不得用“看起来可行”“整体基本 OK”代替 evidence result。

## 5. Minimal but real

Demo SHOULD 尽可能小，但不得伪造正在验证的边界。

硬规则：

> The component or boundary under test MUST be real; unrelated dependencies MAY be deterministic fakes.

例如验证 SQLite process-crash recovery：

```text
fake domain scenario      = allowed
fake deterministic model = allowed
real SQLite persistence   = required
real separate process     = required
real hard process death   = required
```

验证 semantic identity/cache semantics 时，可以使用 in-memory cache store，只要被验证对象是 canonical identity、hit/miss、schema/guard behavior，而不是 persistence durability。

Agent MUST 明确列出：

- Real Under Test；
- Deterministic Fakes；
- intentionally NOT tested components。

## 6. Determinism by default

Architecture Evidence 默认应可重复执行。

优先使用：

- deterministic FakeModelPort；
- deterministic tools；
- fixed inputs；
- controlled/fixed clock；
- fixed random seed when applicable；
- explicit execution counters；
- stable fixtures and canonical serialization。

只有当研究对象本身是 provider/model/platform behavior 时，才 SHOULD 依赖真实非确定性外部系统，并必须记录其环境和限制。

## 7. Required scenarios

每个 Demo 至少包含：

1. positive / happy path；
2. relevant boundary case；
3. negative or invalid input/capability case；
4. failure path；
5. recovery/retry path when the hypothesis concerns durability/recovery；
6. fail-closed behavior where authority/validation boundaries are involved。

不能只证明“一个正常样例能跑”。

## 8. Observable evidence

Demo Issue MUST 指定可观测量，而不是只比较最终 return value。

常见 observable evidence：

```text
modelCallCount
toolExecutionCount
mutationEffectCount
cacheHit / cacheMiss
restoredParentState
restoredChildState
emittedDomainEvent
journal identity
artifact/content digest
validation rejection reason
process exit / restart identity
```

Assertions 应直接证明 Hypothesis 中的关键不变量。

## 9. Evidence strength

Demo 使用最小充分的 Evidence Strength，不机械要求最高成本环境。

### E1 — Executable Logic Evidence

适合：

- semantic identity；
- schema/guard semantics；
- compiler/validator rules；
- state-machine routing；
- deterministic transform/contract behavior。

最低证据：focused executable tests + exact SHA + repository CI/clean validation where applicable。

### E2 — Integration Evidence

适合：

- XState + RuntimeStore；
- compiler + runtime；
- parent/child actor integration；
- cache + guard/transition integration；
- multiple real internal components working together。

必须使用真实被集成组件，不得把关键 integration seam 全部 fake 掉。

### E3 — Real Environment / Failure Evidence

适合：

- process kill / restart；
- SQLite reopen；
- real mobile force-stop/relaunch；
- filesystem/network/platform behavior；
-真实 SDK/toolchain/platform limitation。

必须使用匹配假设的 Build Host / real process / real persistence / real platform evidence。纯 memory actor recreation 不能证明 OS process death。

Issue MUST 声明 required evidence strength：`E1 | E2 | E3`。

## 10. Research Issue contract

Research Demo Issue SHOULD 使用 `templates/research-demo-issue.md`，至少包含：

- Purpose / Architecture UNKNOWN；
- falsifiable Hypothesis；
- Why executable evidence is needed；
- Frozen PRD/L2 candidate references；
- fixed baseline SHA；
- research branch；
- dependency/consumed exact SHAs；
- Real Under Test / Deterministic Fakes；
- In Scope / Out of Scope；
- executable scenarios；
- negative/failure scenarios；
- observable measurements；
- expected result；
- required environment / Evidence Strength；
- allowed/forbidden changes；
- closeout/evidence requirements。

Research branch SHOULD be isolated, normally named `research_*` or project equivalent.

## 11. Scope control

Research Demo 是 architecture evidence，不是 production feature branch。

优先 write set：

```text
tests/architecture-*/
docs/experiments/*
research fixtures
examples/reference/*
```

Demo 不应静默修改：

- production runtime semantics；
- frozen public contracts；
- release artifacts；
- unrelated production features。

如果 Demo 无法继续，除非增加 production seam：

```text
record precise missing seam
→ create follow-up Issue
→ keep research scope minimal
```

不得“顺手”把 research task 扩成 production rewrite。

## 12. Exact identity

每个 Demo result MUST 记录：

- source baseline exact SHA；
- consumed dependency/research SHAs；
- final research branch exact HEAD；
- relevant runtime/toolchain/platform versions for E2/E3；
- exact commands/profile where meaningful。

Architecture/L2 只能引用实际被验证的 identity；旧 SHA PASS 不自动迁移到新 HEAD。

## 13. Validation and closeout

Demo closeout SHOULD 使用 `templates/research-demo-report.md` 和 `checklists/research-demo-validation.md`。

最终报告至少包含：

```text
Hypothesis
Result: PASS | FAIL | BLOCKED
Expected vs Actual
Observed Evidence
What was proven
What was NOT proven
Failure / negative evidence
KEEP / ADAPT / DROP
Architecture implications
Production seams required
Reusable reference artifacts
Exact identities
```

`What was NOT proven` 是 mandatory。禁止把一个窄 Demo 的 PASS 外推为未验证的 distributed scale、multi-platform、performance、security 或 production readiness。

## 14. Demo completion rule

Demo 的完成标准是 **Evidence complete**，不是 Feature complete。

当 Hypothesis 所需 positive/negative/failure evidence 已完整形成并绑定 exact identity，即可关闭 Demo，即使 production API、migration、monitoring、packaging 尚未设计。

研究任务不得因为“还可以顺便实现更多功能”而无限扩大。

## 15. Promotion rule

Research branch 本身不是 production implementation。

允许进入 L2/production development 的是：

- validated invariant；
- validated contract/schema；
- reference fixture；
- reference scenario/test；
- failure/recovery semantics；
- measured limitations。

Production implementation SHOULD consume these validated facts and reimplement according to Frozen L2 / Task contracts。

不得默认直接 merge 整个 research branch。若确实要复用 research code，必须把它当成普通 production change 重新进行 scope、contract、validation 和 Review Policy 判断。

## 16. Architecture decision boundary

Demo 自己不冻结架构。

```text
Architecture UNKNOWN
→ Research Question
→ Demo Issue
→ Research Branch
→ Executable Evidence
→ PASS / FAIL / BLOCKED
→ Architecture Decision / L2 update
→ L2 Freeze
```

Evidence 与 Architecture Decision 是两个不同对象。

- PASS：支持某个明确 Hypothesis，不代表所有相关设计自动成立；
- FAIL：否定当前 Hypothesis/方案，优先调整候选架构；
- BLOCKED：证据不足，不能猜测 PASS；
- 只有当证据揭示 Frozen PRD 自身 contradiction 时，才升级为产品层 reopening request。

## 17. Core rules for LLM / Agent

1. Demo exists to resolve an important UNKNOWN.
2. Every Demo starts from a falsifiable hypothesis.
3. Test the real boundary; fake only unrelated dependencies.
4. Prove success and failure behavior with observable evidence.
5. Bind conclusions to exact code/environment identity and state what was NOT proven.
6. Promote validated invariants/contracts/fixtures, not the whole research implementation.
7. Do not create a Demo when Frozen Architecture already provides sufficient proven evidence.
