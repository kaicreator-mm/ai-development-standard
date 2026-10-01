# T-016 Execution Contract

Exact base: `version/v4.8.0@94cad2b0487e8a552c66d6bcd1cba36b7779383d`.
Authority: Frozen Product/L2/DAG R1 > T-016 Task Pack > this contract. Freedom: F1 bounded implementation.

## Source write set
- `schemas/agent-capability-evidence-v1.schema.json`
- `scripts/test_v48_agent_capability_evidence.py`
- `references/AGENT_CAPABILITY_EVIDENCE_REFERENCE.md`

Execution Pack files are read-only to the Builder.

## Contract kernel
Implement only Agent Capability Evidence v1 as historical exact-subject evidence. Positive and negative observations are first-class. Evidence may reference logical Agent and environment/runner identities but must not copy their owner facts. Historical success never becomes current Availability, Validation or Review PASS. Evidence strength is bounded/layered and must not collapse into a universal scalar Agent score. Provider/model identity is provenance only.

Measured time/resource/cost/economic fields must permit NOT_MEASURED/absence. Performance or savings conclusions require an actually comparable measured methodology; #469 bounded successes alone cannot prove a blanket strong-to-low-cost rule.

Do not own current availability, routing authorization, Validation/Review state or economic policy.
