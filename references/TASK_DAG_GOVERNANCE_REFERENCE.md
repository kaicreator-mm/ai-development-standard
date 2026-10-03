# Task DAG Governance Reference

Non-normative guidance for `TASK_DAG_GOVERNANCE_STANDARD.md`.

## Mutation worksheet

```text
mutation_class:
requested_by:
approved_by:
reason:
affected_task_refs:
old_topology_ref:
new_topology_ref:
old_edges:
new_edges:
scope_impact:
release_impact:
task_pack_impact_refs:
review_impact:
validation_impact_ref:
```

This maps directly to `dag-mutation-record-v1`. The record is evidence; an authorized controller still performs native Issue Dependency mutation and reads the result back.

## Example — dependency removal

Before removing `T02 -> T05`, ask whether the edge encoded a still-material contract or evidence dependency. If yes, removing the edge to make T05 READY is invalid. If the dependency is truly obsolete, record why, update affected Task Pack/Review/Validation posture as required, then mutate and re-read native topology.

## Example — scope growth

If a Task starts owning a new normative concern or different integration owner, do not silently append files to its write-set. Consider SPLIT/ADD/SUPERSEDE or a planning amendment.

## Example — unavailable connector capability

If the current tool can read blocked-by edges but cannot write them, create a controller/local handoff containing exact intended edges and a read-back equality check. Do not treat body text as live topology.

## Review prompts

1. Is this really a material topology/identity change?
2. Who authorized it?
3. Can old and new edges be reconstructed?
4. Which Task Packs and Review/Validation evidence become stale?
5. Would dependency removal manufacture readiness?
6. Is native graph mutation actually performed and read back?
7. Is code/PR ancestry being confused with Task dependency authority?
