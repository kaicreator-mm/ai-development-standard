# T-008 Task Pack — Eligibility / Composite Resource Admission Conformance

Status: **FINAL TASK PACK — JIT EXECUTION PACK REQUIRED**

Authority: Frozen Product; Frozen L2 blob `f88c85454e80101a0fdf56050e21f11a05279841`; Frozen DAG R1 commit `634dd746cd16da970bb01822a1b6c59714c52429` / blob `72dfeee93c092296004c7083b71fdd877d7f1b34`; Issue #514.

```yaml
task_id: T-008
lane: scheduling-conformance
dependencies: [T-002]
integration_target: version/v4.8.0
review_policy: required
validation_scope: concern
validation_owner: independent-from-builder
l3_requirement: reference
agent_freedom_ceiling: F2_ENGINEERING_DISCRETION
jit_branch: true
execution_pack: JIT
```

## Scope

Own deterministic conformance only for the T-002 execution-architecture semantics already merged into the integration target:

- multiple simultaneously READY Tasks and heterogeneous logical Agent profiles;
- fresh, stale, missing and conflicting Availability/resource facts;
- reviewer/validator independence conflicts;
- hard eligibility filtering before optional ranking;
- capacity-N contention and exclusive `N=1`;
- multi-resource composite admission in which the work claim plus every required scarce-resource/compatibility binding share one all-or-none linearization point;
- injected partial-write, publication-loss and crash ambiguity followed by fail-closed durable reconciliation before any incompatible replacement admission.

This Task exercises the canonical READY/Dispatch/Claim owner. It does not create another scheduler lifecycle, state database, durable Availability family, resource owner, Exchange family, Review/Validation state, Closure authority or Release authority.

## Builder write set

The exact JIT Execution Pack may narrow this Task Pack. The authorized implementation surface for the current concern is deterministic conformance code only. The current JIT pack binds:

- `scripts/test_v48_scheduling_conformance.py`

Golden/reference scenarios SHOULD be represented deterministically inside that focused conformance module. If a separate fixture/reference artifact becomes materially necessary, STOP and request an explicit Execution Pack rebind before creating it.

The Builder MUST NOT modify `standards/EXECUTION_ARCHITECTURE_STANDARD.md`, Product/L2/DAG authority, schemas, runtime owners or existing T-002 implementation/tests as part of T-008.

## Acceptance

1. Hard predicates are evaluated before ranking; `INELIGIBLE`/`UNKNOWN` cannot be promoted by cost, latency, priority, evidence strength or other optimization.
2. Stale/missing material Availability fails closed as `UNKNOWN`.
3. Reviewer/validator independence conflicts are hard-filter failures.
4. Competing READY work and heterogeneous profiles produce deterministic eligible/ineligible/unknown outcomes from the same durable facts.
5. For every capacity group `G`, active accepted units never exceed configured `N`; exclusive resources behave as `N=1`.
6. A claim requiring multiple resources is accepted only when the work claim and all required bindings linearize all-or-none at one admission point.
7. Independent per-key CAS/leases or sequential successful reservations do not count as composite proof.
8. No accepted canonical partial state is observable.
9. Injected crash/publication ambiguity blocks incompatible replacement admission until durable work/Dispatch/resource/generation/release/supersession facts are reconciled.
10. If no conforming composite primitive is available, the oracle requires existing single-writer serialization or `BLOCKED/UNAVAILABLE`; it does not invent a novel distributed algorithm.
11. Historical/Fast Path behavior remains non-weakened and no alternate scheduler/state owner appears.

## Required gates

Builder evidence MUST include the focused deterministic conformance suite, the existing T-002 semantic regression, and the repository verifier on the exact candidate.

Required Validation is independent concern Validation covering race/capacity/composite/crash/failure behavior on the exact Builder candidate. Validation PASS is evidence only for that exact subject.

After qualifying Validation, a genuinely Fresh exact-HEAD Review is required. Builder, Validator and Fresh Reviewer identities remain distinct. PR/Task PASS does not imply Version Closure or Release PASS.
