# T-008 Review Checklist

- Exact JIT base is `54a55086a12d406df07eb80706ba14f861101256` / tree `781dec96941ac53ce912e27e6196079c2e895819`; T-002/#510 is merged and is the sole v4.8 semantic owner for execution architecture.
- Candidate implementation diff is exactly `scripts/test_v48_scheduling_conformance.py`; planning pack artifacts are not rewritten by the Builder.
- Multiple READY work items and heterogeneous logical Agent profiles are exercised with explicit deterministic facts.
- Stale/missing material Availability resolves to `UNKNOWN` and fails closed.
- Reviewer/validator independence is a hard predicate, not a ranking hint.
- Hard filtering completes before optional ranking; no optimization promotes `INELIGIBLE` or `UNKNOWN`.
- Capacity-N and exclusive N=1 invariants hold at every accepted canonical transition.
- Work claim plus all required resource/capacity/compatibility bindings accept all-or-none at one logical linearization point.
- Independent per-key CAS/leases or sequential reservations are rejected as composite proof.
- No accepted partial canonical state is observable.
- Crash/publication ambiguity blocks incompatible replacement admission until durable facts are reconciled.
- No alternate scheduler/state database, durable Availability owner, Exchange family, Review/Validation state or Closure/Release authority is introduced.
- No novel distributed multi-key CAS/lease algorithm is smuggled into this conformance Task; such a need routes to a separate Research Demo/Validation.
- `python -B scripts/test_v48_scheduling_conformance.py`, `python -B scripts/test_v48_execution_architecture.py` and `python -B scripts/verify_standard.py` pass on the exact candidate.
- Independent exact-subject concern Validation precedes a genuinely Fresh required Review. Builder, Validator and Reviewer remain distinct.
