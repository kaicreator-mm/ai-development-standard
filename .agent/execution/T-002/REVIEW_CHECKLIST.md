# T-002 Review Checklist

- Exact base and candidate HEAD unchanged.
- Write set contains only Execution Pack files + `EXECUTION_ARCHITECTURE_STANDARD.md` + focused test.
- READY/Dispatch/Claim remain canonical.
- Logical profile, infrastructure owner facts, derived Availability and Capability Evidence are not conflated.
- Hard filters precede ranking; cost/latency cannot promote INELIGIBLE/UNKNOWN.
- Work claim + all required resources linearize all-or-none.
- Capacity N invariant is explicit and testable.
- Crash ambiguity fails closed and reconciles before replacement.
- Independent per-key CAS is not represented as composite proof.
- No second scheduler, Availability owner or Exchange family.
- Independent Validation PASS and genuinely Fresh Review required before merge.
