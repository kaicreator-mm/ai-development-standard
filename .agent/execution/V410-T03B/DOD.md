# Definition of Done

- decomposition remains qualitative: one coherent concern + maximum safe parallelism.
- shared-write collisions, atomic invariants and central-wiring patterns have clear safe handling.
- dependencies mean actual completed-result/integrated-baseline requirements, not conversation order.
- no numeric universal split thresholds are introduced.
- no fake READY by dependency deletion; no stacked-PR substitution for native DAG.
- DAG mutation authority remains with `TASK_DAG_GOVERNANCE_STANDARD.md`.
- focused positive/negative tests pass on exact candidate.
- concern Validation PASS + required Fresh Independent Review PASS bind unchanged candidate.
- merge target is `version/v4.10.0`; Task/PR PASS is not Release PASS.
- proportional Task Learning closeout is recorded.