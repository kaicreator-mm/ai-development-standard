# Task Pack — <task-id> <name>

> Durable planning authority. Exact-base execution detail belongs to the JIT Execution Pack (`.agent/execution/<task-id>/`), not here.

```yaml
task_id:
repository:
version:
integration_target:            # e.g. version/vX.Y.Z
merge_target:
task_pack_ref:                 # stable identity of this pack
dependencies: []               # task ids; live execution DAG = Issue Dependencies
allowed_write_set: []          # path prefixes the executor may touch
forbidden_scope: []            # explicit prohibitions
acceptance: []                 # verifiable criteria
required_gates: []
validation_scope:              # concern | integration | closure
validation_owner:
review_policy:                 # required | recommended | not-required
l3_requirement:                # L3 Reference Pack pointer or not-required — <reason>
agent_freedom:                 # F0_MECHANICAL | F1_BOUNDED_IMPLEMENTATION | F2_ENGINEERING_DISCRETION | F3_ARCHITECTURE_REQUIRED
jit_branch: true               # task branch created only after dependencies merge
execution_pack:                # "JIT" | "not-required — <reason>"
```

## Why

<one paragraph: rationale, risk, planning decision this task encodes>

## Acceptance detail

<expand each acceptance criterion into a verifiable statement>

## Out of scope

<explicit non-goals; contradictions discovered at execution time route upward as TASK_PACK_DEFECT / ARCHITECTURE_CONTRADICTION / EXECUTION_PACK_INVALID — never silently resolved>
