# T-002 Execution Contract

Exact base: `version/v4.8.0@22e8e1701661689fb39a5c363eed424cf827c403`.

Implement only Frozen T-002 Execution Architecture semantics. Preserve canonical READY/Dispatch/Claim. Derive `ELIGIBLE|INELIGIBLE|UNKNOWN`; apply authority/currentness/independence/security/resource hard filters before optional ranking. Composite admission MUST linearize the work claim plus every required scarce/capacity binding all-or-none. Capacity N may never over-allocate. Crash/publication ambiguity fails closed and must reconcile durable bindings before replacement admission.

Allowed implementation paths are only `standards/EXECUTION_ARCHITECTURE_STANDARD.md` and `scripts/test_v48_execution_architecture.py`. Any need for another path is a material scope expansion and requires Controller rebind before edit.

Do not create a second scheduler/state database, a durable Availability owner, a new Exchange family, or claim independent per-key CAS/leases prove composite atomicity. Builder may not self-certify Validation or Fresh Review.
