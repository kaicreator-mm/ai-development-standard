# T-001 Execution Contract

Exact base: `version/v4.8.0@94cad2b0487e8a552c66d6bcd1cba36b7779383d`.
Authority: Frozen Product/L2/DAG R1 > T-001 Task Pack > this contract. Freedom: F1 bounded implementation.

## Source write set
- `schemas/task-learning-v1.schema.json`
- `scripts/test_v48_task_learning.py`
- `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`

The `.agent/execution/T-001/**` pack is execution authority and must not be rewritten by the Builder.

## Contract kernel
Implement only Task Learning Evidence v1. Exact work/subject/evidence/currentness identity must be explicit. `TASK_LEARNING=NONE_MATERIAL` remains a valid lightweight outcome. Any rationale is a compact externally useful engineering summary; private chain-of-thought is neither required nor accepted. Stale learning is historical-only. Task Learning can never issue or replace Product, Architecture, Task, ADR, Incident, Review or Validation authority.

Do not implement Logical Agent Capability Profile, Agent Capability Evidence, Execution Architecture wiring, scheduler semantics or sibling scope.

If the frozen contract appears insufficient or contradictory, stop with `TASK_PACK_DEFECT` or `ARCHITECTURE_CONTRADICTION`; do not redesign locally.
