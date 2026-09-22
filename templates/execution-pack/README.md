# Execution Pack templates

Core artifact fill-in templates for a JIT Execution Pack (`.agent/execution/<task-id>/`).

Files:

- `MANIFEST.yaml` — pack identity, exact base binding, freedom, inventory
- `EXECUTION_CONTRACT.md` — bounded execution contract (subordinate to Task Pack)
- `TEST_MATRIX.yaml` — required checks mapped onto the exact base
- `FAILURE_MATRIX.yaml` — failure handling expectations and negative oracle
- `IMPLEMENTATION_MAP.md` — files/areas to touch on this exact base
- `REVIEW_CHECKLIST.md` — what an independent reviewer verifies

Optional artifacts (`INTERFACE_SEED.*`, `SEMANTIC_KERNEL_SEED.*`, `REFERENCE_PATCH.diff`, `LOCAL_AGENT_PROMPT.md`, reference fixtures) are added per task; empty placeholders MUST NOT be required.

Small tasks MAY compress these into minimal content; trivial Fast Path tasks MAY skip the Execution Pack entirely (`standards/EXECUTION_PACK_STANDARD.md` §11).
