# v4.9.0 Task DAG Revision History

Task DAG snapshots are immutable planning evidence. `TASK_DAG.md` is the current candidate authority only.

| Revision | Status | Review / reason | DAG blob | Identity |
|---|---|---|---|---|
| v0.1 | superseded / rejected for Freeze | #715 first candidate; #716 Fresh Review FAIL `P0=0/P1=1/P2=0/P3=0` due incomplete predecessor-lineage gating | `4f358ba2b32e01ae17ddcdf970151cf28e44bb3f` | reviewed HEAD `6e469aed534052906434dc62bc05b4daa2337eb4`, tree `0be285a5283502eb627ce1ef1a41b5615b7ec2fe` |
| v0.2 | current successor / not frozen | #717 repairs only #716 F1 by making per-Task predecessor currentness explicit and reconstructible | `b9fe0cc7089f64929b4bcf45f7230d950e864db2` | first materialization identity recorded by successor commit; Fresh Review must bind final live HEAD/tree + this blob |

## v0.1

- Task count: 15.
- Owner lanes, Review Policies, validation ownership, L3 posture and implementation scope were accepted by #716 except for F1.
- Defect: only v4.8/full-final lineage gates were explicit; direct consumers of v4.2/v4.3/v4.7 predecessor owners could become dependency-ready prematurely.

## v0.2

- Task count/identities/dependency edges unchanged.
- Adds named lineage currentness predicates and an exact per-Task lineage matrix.
- Adds Task Pack/Issue `LINEAGE_CURRENTNESS_REFS` materialization/admission requirements.
- Upstream completion cannot substitute for the dependent Task's own dispatch-time predecessor currentness.
- `WAITING_LINEAGE` remains derived/non-dispatch and never becomes a fake Task dependency edge or canonical workflow state.

## Invariants

1. Historical DAG snapshots are never rewritten to make old Review evidence current.
2. Review terminals bind exact DAG blob/HEAD/tree.
3. Material successor DAG requires successor Review.
4. Frozen Product/L2 remain unchanged.
5. Implementation remains unauthorized until explicit DAG Freeze + Task Pack/Issue materialization.
