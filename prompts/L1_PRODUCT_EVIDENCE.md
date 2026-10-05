# L1 Product Evidence Prompt

你正在执行 Stage-1 的 L1 产品证据步骤。目标不是整理竞品列表，而是在进入 PRD/架构前验证“真实问题是否存在、产品形态是否成立、用户实际怎样完成任务、当前替代方案是什么、什么证据可能推翻我们的假设”。

## 生命周期位置与投影边界

本 prompt 是 `standards/DEVELOPMENT_WORKFLOW.md` Stage 1 与 Frozen Product / L2 4.1–4.3 的执行面投影，不是语义 owner，不新增生命周期、状态或权威。规范序列：

```text
Idea/Intent
→ Intake/Baseline
→ semantic L1 Product Evidence
→ Product Research（as needed）
→ Draft PRD / Scope
→ selected Product Review
→ Product Freeze
```

- **L1 是语义框架/证据步骤**：回答“解决什么问题、为谁解决、成功标准是什么”。L1 不要求独立成文件，**不得被坍缩为强制外部研究**。
- 本 prompt 只生产 evidence / decision input：**不持有 Product authority**、**不产生 Product Freeze**，也**不构成第二产品权威**。研究结论（含 PASS）都只是 evidence/judgment，由 Product authority 采纳或拒绝。
- **selected Product Review** 是对 Draft PRD / Scope 这一确切 Product subject 的独立 evidence/judgment，按 applicable policy 与风险选择；它同样不产生冻结效力：**Product Review PASS 不能替代或自动产生 Product Freeze**。
- **Product Freeze** 是 Product authority 的显式冻结行为，与既有 “PRD / Scope Freeze” 是同一事件，不是本 prompt 或 Research 可以触发的新 gate。

## 选择与比例（as needed）

- **仅当现有/静态证据不足以做出当前 PRD 决策时**才选择 Product Research；范围与所需决策成比例，并 MUST 记录**有界 purpose** 与它支撑的 **decision relevance**（这条证据用来决定什么）。
- 低风险/证据充分且没有更高权威 owner 要求时，**不得被强制加入独立 Product Research 或独立 Product Review**，可以保持 compact/inline，并如实记录 `NO_RESEARCH_REQUIRED`。
- `NO_RESEARCH_REQUIRED` 与 inline 都必须是**如实**结论，不是 waiver：**applicable policy 要求的证据不得因 compact/inline 而被跳过**；已存在等价证据时 MUST 引用其 durable 身份（exact ref/sha），而不是凭印象声称“已足够”。
- **不得为了形式制造 research ceremony**（空 Research Issue、空 research 分支、为“看起来完整”而补齐的清单）。选择适用性 UNKNOWN 或相互矛盾时 **fail closed**，交给 authority/risk disposition，**不得静默降级**。

## Product Research 与 Architecture Research 的边界

- **Product Research** 属于 **Stage 1**，发生在 Product Freeze **之前**，回答产品范围/acceptance 层面的 UNKNOWN。
- **Architecture Research / Research Demo** 属于 **Stage 2**，发生在 Product Freeze **之后**，回答可证伪的架构假设，owner 是 `standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md`。
- **不得把 Architecture Research / Demo 前移到 Product Freeze 之前**充当 product discovery 的替代品。Freeze 后若 Architecture Research 发现产品范围不可行/矛盾，走既有 Product thaw/contradiction 路径，不得静默弱化 Frozen 产品范围。
- 两者保持 purpose / terminology / routing 一致（R10 由既有 owner 收敛实现），但**不合并为第二个 Research authority**，也不引入通用 Research pipeline。

## standards / protocol / governance 产品的附加考虑

当“产品”本身就是标准/协议/治理规范时，L1 在 material 情况下 SHOULD 额外消费既有 owner 证据：

- 现有 normative owner 的重叠/冲突，以及是否引入 duplicate authority；
- 内部 dogfood 与既有 incident/review 证据；
- compatibility / SemVer 影响（消费者群体与契约面）；
- authority weakening 风险与已知反模式。

这些是对既有 owner 的消费，**不引入新的研究家族**，也不扩大产品范围。

## 输入

- Product idea / target users / geography / constraints
- Existing code/docs if any
- Known assumptions

## 研究要求

当确实选择了 Product Research 时按以下要求执行；未选择时按上一节如实记录 disposition，不执行本节清单。

1. 找真实产品、真实用户 workflow、行业替代方案和失败案例。
2. 区分事实、用户证据、厂商主张、推断和假设。
3. 重点搜索反证：为什么用户可能不需要它、为什么已有方案已经足够、为什么形态可能不成立。
4. 归纳用户 Job / Trigger / Workflow / Pain / Existing workaround，而不是仅按功能表比较。
5. 分析竞争产品如何演化，哪些能力是核心，哪些是历史包袱。
6. 输出产品边界：应该做什么、不应该做什么、哪些假设必须在 PRD 中设置 Gate。

## 输出

- Problem Evidence
- User Workflow Evidence
- Alternatives / Competitors
- Counter-evidence
- Product Shape Findings
- Key Assumptions and Validation Plan
- Recommendation: Proceed / Narrow / Reframe / Stop
- Research selection disposition（`selected` / `inline` / `NO_RESEARCH_REQUIRED`，含所依据的既有证据身份）
- Decision relevance（这条证据支撑哪个确切 PRD 决策）

所有时间敏感事实应有可验证来源。不要为了支持既定 idea 过滤反证。
