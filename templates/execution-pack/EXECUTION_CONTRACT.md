# Execution Contract — <task-id>

> Subordinate to the Task Pack and Frozen Authority. This contract MAY narrow execution freedom; it MUST NOT redefine PRD, Architecture, task scope, public contract, required invariant, validation ownership or review requirement. Contradictions route upward as `TASK_PACK_DEFECT` / `ARCHITECTURE_CONTRADICTION` / `EXECUTION_PACK_INVALID`.

```yaml
task_pack_ref:
base_sha:
branch:
agent_freedom:               # inherited or narrowed from Task Pack; never silently widened
public_contracts_fixed: []   # interfaces/contracts the executor must not change
invariants: []               # required invariants with verification pointers
write_set: []                # narrowed allowed paths on this exact base
forbidden: []                # explicit prohibitions
completion_rule:             # what "done" means for this dispatch
blocker_rule:                # how FAIL/BLOCKED is published and routed
```

Implementation order (default): `Tests → Contract → Core → Failure Handling → L3`.

A defect above the granted freedom level is published, not silently fixed.
