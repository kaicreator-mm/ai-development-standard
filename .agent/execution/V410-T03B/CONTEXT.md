# Context

Currentness binding:
- integration baseline `c1a40700336309e2dbb4771fcd893a257d260aa8`;
- `standards/TASK_DECOMPOSITION_STANDARD.md` blob `df13bcfc29d9a5caddf997918047298157a67504`;
- native DAG #866 PASS/read-back 17/17;
- task has no predecessors.

Core invariant: minimum coherent concern + maximum safe parallelism.

Required cases include coherent multi-file concern, sequential ownership of one file, true independent lanes, central wiring isolation and large atomic invariants that must not be faked into parallel Tasks.

Reject LOC/file/token/time thresholds, fake parallelism, conceptual-order dependencies, readiness fabrication and stacked PR as live-DAG substitute.