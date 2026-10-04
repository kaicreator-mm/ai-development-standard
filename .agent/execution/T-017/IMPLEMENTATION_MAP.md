# T-017 Implementation Map

Read first, in order:

1. `docs/implementation/4.8.0/task-packs/T17_execution_ownership_visibility.md`
2. `docs/implementation/4.8.0/L3_T17_EXECUTION_OWNERSHIP.md`
3. Frozen DAG R2 T-017 definition and #686 native dependency proof
4. `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` §§5, 8, 12
5. `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §§4–6, 9, 11, 11.1
6. `schemas/agent-event-v2.schema.json` as a read-only compatibility input
7. `scripts/test_v48_execution_architecture.py`
8. `scripts/test_v48_interchange_replay_restart.py`

Implement exactly three paths:

- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md`
- `scripts/test_v48_execution_ownership.py`

## GitHub interaction protocol

Add the smallest writer/start-record clarification around the existing `DISPATCH_CLAIMED` event. The accepted Claim is the durable Start Record. New writers should expose existing operator/session/time/profile/subject/pack identity and optional admission provenance when available. Keep historical event-v2 claims compatible. State explicitly that current workflow labels/state-card metadata are reconstructible visibility projections, never claim locks or execution authority.

## Execution architecture

Add the smallest bounded lifecycle clarification around existing section 11 semantics: active ownership is derived from durable Claim/dispatch facts; accepted start projects through claimed→implementing; terminal/release states remove incompatible active ownership only after durable facts reconcile; same operator/same dispatch resume is idempotent; different-operator replacement after TIMEOUT/STALE remains serialized and fail-closed on ambiguity. Progress/heartbeat is optional and non-authoritative and cannot fabricate Task/Validation failure or implicit release. Preserve Fast Path/manual `SINGLE_WRITER_ADMISSION` proportionality.

Do not create a new state dimension, lifecycle, scheduler, claim authority, event family or runtime database.

## Focused conformance

Create `scripts/test_v48_execution_ownership.py` as a deterministic self-contained oracle over explicit durable facts. Cover the complete TEST_MATRIX and validate both:

- a representative enriched new-writer `DISPATCH_CLAIMED` using existing event-v2 fields/additive provenance;
- a historical valid event-v2 Claim lacking richer optional T-017 provenance.

The test should read current normative text/schema as necessary to prevent documentation/oracle divergence, but it must not repair predecessor semantics or mutate schemas.

If any requirement cannot be expressed inside this exact three-path write set without Product/L2/schema/new-lifecycle expansion, STOP with `ARCHITECTURE_AMENDMENT_REQUIRED` or `CONTROLLER_REBIND_REQUIRED` as applicable.
