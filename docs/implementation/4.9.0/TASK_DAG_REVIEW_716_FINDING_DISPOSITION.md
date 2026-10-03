# v4.9.0 Task DAG Review #716 Finding Disposition

Source review: #716 comment `5968275856`  
Reviewed DAG v0.1 blob: `4f358ba2b32e01ae17ddcdf970151cf28e44bb3f`  
Reviewed HEAD/tree: `6e469aed534052906434dc62bc05b4daa2337eb4` / `0be285a5283502eb627ce1ef1a41b5615b7ec2fe`  
Verdict: **FAIL — P0=0 / P1=1 / P2=0 / P3=0**  
Disposition controller: #717

## F1 — P1 INCOMPLETE_PREDECESSOR_LINEAGE_GATING

**Disposition: ACCEPTED / RESOLVED IN DAG v0.2 CANDIDATE.**

Root cause: v0.1 correctly modeled external lineage as a non-Task-edge predicate, but only made v4.8/full-final lineage gates explicit. Tasks that directly consume v4.2 Compatibility, v4.3 DAG Governance or v4.7 registry surfaces could therefore become dependency-ready before those predecessor owners were integrated/current.

Repair:

- introduce named `LG42_COMPAT`, `LG43_DAG`, `LG47_REGISTRY`, `LG48_EXEC`, `LG48_LEARNING`, `LG_SEQ_FULL` predicates;
- bind explicit per-Task lineage currentness refs;
- require materialized Task Packs/Issues to carry reconstructible `LINEAGE_CURRENTNESS_REFS`;
- re-check lineage at JIT/Dispatch admission, independently of upstream Task completion;
- missing/stale/unknown predecessor refs => `WAITING_LINEAGE`, `DISPATCH=NO`, `CLAIM=NO`;
- preserve lineage predicates as external admission facts, never fake native Task dependency edges;
- preserve the no-generic-predecessor-rebind rule.

Counterexample closures include:

```text
T-001 DONE + v4.2 absent -> T-002 WAITING_LINEAGE
T-002 DONE + v4.7 absent -> T-003 WAITING_LINEAGE
T-007 DONE + v4.3 absent -> T-009 WAITING_LINEAGE
upstream DONE + predecessor drift -> T-011/T-012 re-evaluate, no stale READY inheritance
```

## Non-findings preserved

#716 otherwise passed Product/L2 coverage, task coverage, owner lanes, parallelism, machine-family accounting, assurance continuity, Release lane, DAG governance, registry wiring, conformance coverage, dogfood decomposition, proportional Review safety, scope size and implementation-gate separation. DAG v0.2 does not reopen those semantics.

## Gate

```text
F1=RESOLVED_IN_V02_CANDIDATE
P0_OPEN=0
P1_OPEN=0
P2_OPEN=0
P3_OPEN=0
TASK_COUNT=15_UNCHANGED
DEPENDENCY_EDGES=UNCHANGED
FROZEN_PRODUCT=UNCHANGED
FROZEN_L2=UNCHANGED
TASK_DAG_FREEZE=NO
IMPLEMENTATION_AUTHORITY=NO
NEXT=FRESH_COMPLETE_DELTA_TASK_DAG_REVIEW
```
