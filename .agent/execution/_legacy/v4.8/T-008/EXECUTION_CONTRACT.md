# T-008 Execution Contract

Exact base: `version/v4.8.0@54a55086a12d406df07eb80706ba14f861101256` / tree `781dec96941ac53ce912e27e6196079c2e895819`.

Authority: Frozen Product/L2/DAG R1 > finalized T-008 Task Pack > v4.8 L3 T-008 reference > this exact-base contract. T-002/#510 is the merged semantic owner. Task Pack freedom ceiling is F2; this Execution Pack narrows Builder freedom to `F1_BOUNDED_IMPLEMENTATION`.

## Builder write set

The exact implementation write set is:

- `scripts/test_v48_scheduling_conformance.py`

The six `.agent/execution/T-008/**` artifacts, Task Pack and L3 materialization are planning authority produced by #637 and are read-only to the implementation Builder. No other source, standard, schema, fixture, reference or workflow file may be modified without an explicit Controller rebind.

## Contract kernel

T-008 is deterministic conformance over T-002 semantics, not a semantic-owner lane. The Builder must model explicit durable facts and prove:

1. current claimability/currentness, logical capability, current Availability/resource facts, security/authority, reviewer/validator independence, write-set compatibility and required evidence policy are hard predicates;
2. every hard predicate is resolved before optional ranking and `INELIGIBLE`/`UNKNOWN` never enters ranking;
3. stale/missing material Availability resolves to `UNKNOWN` and fails closed;
4. the protected admission set contains the work claim plus every required scarce-resource/capacity/compatibility binding;
5. capacity-N accepted active units never exceed N and N=1 is exclusive;
6. multi-resource admission accepts all members of the protected set or none at one logical linearization point;
7. independent per-key CAS/leases/sequential reservations are insufficient proof;
8. crash/publication ambiguity blocks incompatible replacement until durable claim/Dispatch/resource/generation/release/supersession facts are reconciled.

The reference oracle may simulate the two already-authorized modes — `SINGLE_WRITER_ADMISSION` and `LINEARIZABLE_CONDITIONAL_WRITE` — but must not design a new distributed multi-key CAS/lease algorithm.

If the focused conformance cannot be expressed without modifying T-002 semantic owners or creating a separate fixture/reference artifact, STOP and request `CONTROLLER_REBIND_REQUIRED`; do not broaden the write set.
