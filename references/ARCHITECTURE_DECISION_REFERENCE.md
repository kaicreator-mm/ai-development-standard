# Architecture Decision Reference

Non-normative companion to `standards/ARCHITECTURE_DESIGN_STANDARD.md`.

A material decision may use this compact shape:

```text
Decision ID / title:
Status / authority ref:
Product / requirement refs:
Scope / non-goals:
Drivers / constraints:
Invariants:
Ownership / boundaries:
Affected contracts:
Decision:
Alternatives considered:
Rationale:
Trade-offs:
Failure modes:
Security / durability / observability / deployment assumptions:
Compatibility refs:
Migration/recovery refs:
Evidence refs:
Assumptions / UNKNOWNs + dispositions:
Escape hatch / evolution path:
Affected Tasks / implementation refs:
```

Use only material fields; do not create empty boilerplate.

## Example reasoning boundary

If a queue-vs-direct-call decision is material, record the actual driver (durability, latency, failure isolation, ordering, coupling), alternatives, failure semantics and operational cost. “Event-driven is modern” is not evidence.

If the decision changes an external contract, reference v4.2 compatibility evidence. If it changes durable state, reference v4.2 migration/recovery. The architecture document should not manufacture those outcomes.

## UNKNOWN disposition

Useful dispositions include:

- prove before Freeze;
- bounded experiment/research task;
- explicit Product/Architecture decision;
- safely defer to a named implementation Validation task;
- blocked pending external fact.

Never leave a high-impact UNKNOWN as an implicit choice for the implementation Agent.

## Format independence

This reference can be used inside an ADR, design document, Frozen L2 artifact or equivalent. The repository may adopt a stronger project-specific template via PROJECT_OVERRIDES; it need not rename existing design history solely to match this reference.
