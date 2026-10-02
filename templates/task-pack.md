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
task_learning_closeout:        # TASK_LEARNING=NONE_MATERIAL | durable evidence ref(s)/digest(s); semantics/currentness per references/TASK_LEARNING_EVIDENCE_REFERENCE.md
```

## Why

<one paragraph: rationale, risk, planning decision this task encodes>

## Acceptance detail

<expand each acceptance criterion into a verifiable statement>

## Task Learning Closeout

Record exactly one proportional closeout path for the task:

- `TASK_LEARNING=NONE_MATERIAL`; or
- one or more durable Task Learning evidence refs/digests interpreted under `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`.

Prefer references/digests over copied evidence bodies. Missing, ambiguous, mutable or stale exact-subject/currentness evidence remains historical only and must not be silently rebound as current behavioral proof. Task Learning is evidence, not Product/Architecture/Task/ADR/Incident/Review/Validation/merge/release authority, and no private chain-of-thought, hidden evaluator material, credentials, secrets or verbose scratch reasoning is required.

## Out of scope

<explicit non-goals; contradictions discovered at execution time route upward as TASK_PACK_DEFECT / ARCHITECTURE_CONTRADICTION / EXECUTION_PACK_INVALID — never silently resolved>
