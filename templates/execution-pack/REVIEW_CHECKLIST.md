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

l3:
  - L3 requirement satisfied per Task Pack
```

Result vocabulary: `REVIEW_PASS / CHANGES_REQUESTED / VALIDATION_REQUESTED / BLOCKED` with P0–P3 findings. A HEAD change invalidates exact-head review automatically.
