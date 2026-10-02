# Review Checklist — <task-id>

What an independent reviewer verifies for this task (used by WEB_REVIEWER dispatches).

```yaml
exact_identity:
  - current PR HEAD/base match reviewed dispatch
  - evidence SHAs match claimed results
authority:
  - Task Pack acceptance satisfied
  - write set respected; forbidden scope untouched
  - Execution Pack subordinate; no silent base_sha rewrite

contract_and_failure:
  - public contracts/invariants unchanged or explicitly authorized
  - failure cases fail closed (negative oracle honored)
  - no weakened/deleted tests

task_learning_closeout:
  - exactly one path is declared: TASK_LEARNING=NONE_MATERIAL or durable material-learning evidence ref(s)/digest(s)
  - material learning is reference-first and interpreted under references/TASK_LEARNING_EVIDENCE_REFERENCE.md
  - stale, ambiguous, mutable, malformed or non-current exact-subject evidence remains historical only and is not silently rebound
  - Task Learning does not replace Product/Architecture/Task/ADR/Incident/Review/Validation/merge/release authority
  - no private chain-of-thought, hidden evaluator material, credentials, secrets or verbose scratch reasoning is required
  - NONE_MATERIAL remains proportional and does not require an empty Task Learning object
  - closeout wiring does not redefine JIT admission/currentness/scheduling/resource semantics

l3:
  - L3 requirement satisfied per Task Pack
```

Result vocabulary: `REVIEW_PASS / CHANGES_REQUESTED / VALIDATION_REQUESTED / BLOCKED` with P0–P3 findings. A HEAD change invalidates exact-head review automatically.
