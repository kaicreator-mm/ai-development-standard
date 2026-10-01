# Execution Contract — <task-id>

> Subordinate to the Task Pack and Frozen Authority. This contract MAY narrow execution freedom; it MUST NOT redefine PRD, Architecture, task scope, public contract, required invariant, validation ownership or review requirement. Contradictions route upward as `TASK_PACK_DEFECT` / `ARCHITECTURE_CONTRADICTION` / `EXECUTION_PACK_INVALID`.

```yaml
task_pack_ref:
authority_refs: []             # inherited applicable Frozen/Core owner pointers; never a local replacement authority
implementation_profile_refs: [] # inherited/resolved pinned profile paths; do not rediscover by file order or local tools
project_overrides_ref:         # project selection/specialization source when applicable
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

## v4.3 authority / profile consumption

The Execution Pack consumes the Task Pack's durable authority/profile pointers; it MUST NOT create a duplicate Task object/schema or independently recalculate higher authority.

- `authority_refs` and `implementation_profile_refs` may be copied from or narrowed consistently with the Task Pack for this exact execution subject; they MUST NOT be used to widen task scope or weaken Frozen/Core requirements.
- `project_overrides_ref` points to the project-owned selection/specialization/strengthening facts. PROJECT_OVERRIDES may strengthen applicable defaults but MUST NOT weaken Frozen/Core or Task authority.
- Profile applicability is based on durable project facts and pinned references, never Agent-local compiler/runtime availability, IDE discovery, glob order or file order.
- A material unresolved profile conflict or missing required authority pointer is `BLOCKED` and routes upward; the executor does not choose a winner by preference.
- Historical/legacy Tasks and Fast Path work do not gain retroactive profile ceremony. When no implementation-profile decision is material, truthful non-applicability is sufficient.

Implementation order (default): `Tests → Contract → Core → Failure Handling → L3`.

A defect above the granted freedom level is published, not silently fixed.
