# V410-T04B Execution Contract

Exact base: `7a0ee000174512df85bf3d2cd611e8b2cf55c840`.
Task Pack: `docs/implementation/4.10.0/TASK_PACKS_R1.md#V410-T04B`.
L3: `docs/implementation/4.10.0/L3_WAVE_D_R1.md#V410-T04B`.
Execution environment: `LOCAL`.

## Allowed write set

- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`
- existing Review finding/aggregation machine contracts, primarily `schemas/agent-event-v2.schema.json`, only where deterministic finding reconstruction requires additive structure
- directly-owned focused Review-currentness tests/templates only where materially required

## Forbidden scope

- second Review lifecycle/status/event/registry
- Validation or Release ownership
- majority/model-count/provider-brand authority
- transfer of old exact-subject verdicts to successor HEADs
- rewrite/duplication of T04A repair-routing or T02B causality/responsibility semantics
- central manifest/discovery wiring reserved for T06A/T06B

## Admission and completion

No implementation mutation before an accepted serialized Builder claim. Any owner/base/Task-Pack conflict fails closed. Candidate completion requires exact HEAD/tree evidence, bounded write set, focused regression, independent concern Validation and Fresh Independent Review before merge. Task/PR PASS is not Release PASS.