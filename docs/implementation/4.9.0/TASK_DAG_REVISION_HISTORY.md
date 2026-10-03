# v4.9.0 Task DAG Revision History

Task DAG snapshots are immutable planning evidence. `TASK_DAG.md` is the current DAG authority.

| Revision | Status | Review / reason | DAG blob | Identity |
|---|---|---|---|---|
| v0.1 | superseded / rejected for Freeze | #715 first candidate; #716 Fresh Review FAIL `P0=0/P1=1/P2=0/P3=0` due incomplete predecessor-lineage gating | `4f358ba2b32e01ae17ddcdf970151cf28e44bb3f` | reviewed HEAD `6e469aed534052906434dc62bc05b4daa2337eb4`, tree `0be285a5283502eb627ce1ef1a41b5615b7ec2fe` |
| v0.2 | **FROZEN** | #717 repaired only #716 F1; #718 complete-delta Fresh Review PASS `P0=0/P1=0/P2=0/P3=0`; Freeze #719 | `b9fe0cc7089f64929b4bcf45f7230d950e864db2` | first materialized HEAD `1aac857f48b6731d219beaadd5c3074288a7fdff`, tree `cc1581add5d6349d415c1785030570411c2e1a90`; reviewed HEAD `3c023b45a8ad7515f40a72858b5333943f68cf79`, tree `c0a6458c9e0e20effd6b5dc1853118cb4a02c2f0` |

## v0.1

- Task count: 15.
- Owner lanes, Review Policies, validation ownership, L3 posture and implementation scope were accepted by #716 except for F1.
- Defect: direct consumers of v4.2/v4.3/v4.7 predecessor owners could become dependency-ready prematurely.

## v0.2

- Task count/identities/dependency edges unchanged.
- Adds named lineage-currentness predicates and exact per-Task lineage matrix.
- Adds Task Pack/Issue `LINEAGE_CURRENTNESS_REFS` materialization/admission requirements.
- Upstream Task completion cannot substitute for a dependent Task's own dispatch-time predecessor currentness.
- `WAITING_LINEAGE` remains derived/non-dispatch and never becomes a fake Task dependency edge or canonical workflow state.
- #718 independently re-tested the complete delta and #716 counterexample, with no findings.
- Frozen by #719 without changing DAG semantics.

## Invariants

1. Historical DAG snapshots are never rewritten to make old Review evidence current.
2. Review terminals bind exact DAG blob/HEAD/tree.
3. Material DAG changes after Freeze require explicit DAG amendment/review authority.
4. Frozen Product/L2 remain unchanged.
5. Task Pack/Issue materialization follows the Frozen DAG; implementation execution remains admission-bound per Task.
