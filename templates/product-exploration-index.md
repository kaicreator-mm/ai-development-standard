# Product Exploration Evidence Index（可选示例，不是 ADS 新 Schema）

> 用于**多个**相关、尚未解决的 Product Research 问题；优先把本模板内容放入**已有 Product Issue**。简单研究直接内联，`NO_RESEARCH_REQUIRED` 时不创建。此 Index 不是 Product authority 或 Stage 2 Research Demo Issue 的替代品。
>
> Source owner: [ADS Development Workflow Stage 1](../standards/DEVELOPMENT_WORKFLOW.md); optional pattern: [Product Exploration Reference](../references/PRODUCT_EXPLORATION_EVIDENCE_REFERENCE.md).

## Exploration intent / 决策目标
- Product/Scope Issue:
- Problem / target users / why now:
- Decision to support:
- Bounded assumptions that could be falsified:
- Stop condition / time-or-budget bound:

## Evidence index（每次修订追加 exact ref，不重复复制证据全文）

| Question / decision relevance | Study / revision | Original input exact SHA/blob | Actual execution / report ref | Observed result | What is NOT proven | Next |
| --- | --- | --- | --- | --- | --- | --- |
| Q1 | path/to/study-r0 @ commit | SHA | receipt | PASS/FAIL/PARTIAL/BLOCKED/NOT_RUN | ... | ... |

## Current judgment
- Claims proven only at the actually tested scope:
- Significant counterevidence / P0/P1:
- Unresolved UNKNOWN / limitations:
- Next smallest evidence that could change the Product decision:
- Reuse existing exact evidence instead of rerunning unchanged checks:

## Owner disposition（仅记录现有 Product authority 的真实决定）
- Recommendation only: ADOPT / REVISE / CONTINUE / REJECT
- Actual owner decision ref and subject exact SHA:
- Impact on Draft PRD / Product Review / Freeze:
- Stage 2 handoff: If architecture research requires its own Issue, use the existing `ARCHITECTURE_RESEARCH_DEMO_STANDARD.md`; do not silently substitute this Index.

## Practice learning / 下轮修订输入
- Actual Issue/branch/PR count (observed):
- Time, tool/model/human/CI cost (measured or NOT_MEASURED):
- Reused valid evidence:
- Unnecessary handoffs or wasted work:
- Lessons with source-backed counterexample:
- Candidate ADS improvement / related issue:

**Explicitly not:** new mandatory workflow stage, new lifecycle/gate state, new product version per study, auto Product Freeze, or independent qualification based only on a successful demo.
