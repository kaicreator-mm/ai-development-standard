# Failure Matrix — <task-id> @ <base_sha>

Failure handling expectations and the negative oracle for this task.

```yaml
failure_cases:               # what must fail closed / be rejected
  - case:
    input:
    expected_rejection:      # e.g. HEAD_DRIFT / PACK_STALE_MATERIAL / INVALID_SCHEMA

defect_routing:
  product_defect:            # repair only under Builder dispatch, new SHA, revalidate
  environment_inability:     # BLOCKED, not FAIL, not PASS
  authority_contradiction:   # TASK_PACK_DEFECT / ARCHITECTURE_CONTRADICTION / EXECUTION_PACK_INVALID; stop and route upward

negative_oracle:             # adversarial cases the implementation must reject
  - case:
    why:
```

A Validator discovering a real defect publishes `FAIL` and MUST NOT repair source. Environment inability publishes `BLOCKED`.
