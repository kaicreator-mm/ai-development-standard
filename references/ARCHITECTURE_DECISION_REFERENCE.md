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

## v4.19 candidate: selected path evidence during structural refactor

**Source:** [DomainHarness #1013](https://github.com/kaicreator-mm/domain-harness/issues/1013), [#1100](https://github.com/kaicreator-mm/domain-harness/issues/1100), [#1264](https://github.com/kaicreator-mm/domain-harness/issues/1264). A new BUILD-selected Kernel Hook exported from a package is not evidence that the selected Primary calls it. A real public entrypoint may also fail to wire trusted Host ports even if isolated K/S/Host PRs all build.

**Golden, when material:** record one traceable public consumer entry → installed/selected contract → Host/Kernel/adapter composition → invoked operation → result/negative; assign a later integration owner when the dependent code is not yet executable. State retained durability/replay/CAS invariants and which real tests will prove them. If the source-only L2 decision cannot prove a physical seam, record `UNKNOWN` rather than fabricated PASS. **Forbidden:** treat imported/initialized code or a checked retained-feature row as execution proof; expand L2 into a compulsory full-platform demo for every leaf.
