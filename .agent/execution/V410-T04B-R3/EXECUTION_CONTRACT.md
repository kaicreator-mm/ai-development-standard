# V410-T04B R3 Repair Execution Contract

Exact base: `30334e8c7b90a327f8597b86c88c785b98df07f7`.
Task Pack: `docs/implementation/4.10.0/TASK_PACKS_R1.md#V410-T04B`.
L3: `docs/implementation/4.10.0/L3_WAVE_D_R1.md#V410-T04B`.
Execution environment: `LOCAL`.

## Repair authority

This is a bounded successor repair after Fresh Independent Review R1 on historical candidate
`82ac1e909875bea1b4838cf010f768e601802ca8` returned `CHANGES_REQUESTED` with exactly two P1 findings.

P1-1: newly emitted material REVIEW_RESULT findings must be machine-reconstructible; historical bucket-only payloads remain readable, but a current/new material finding without stable identity, severity, root-defect class and evidence/provenance must not satisfy the current aggregate path.

P1-2: different independent finding IDs that represent the same logical defect need a durable deterministic equivalence/disposition path using the existing finding/disposition family (for example DUPLICATE/duplicate_of or an equivalent already-owned relation); ambiguous/conflicting equivalence fails closed.

## Allowed write set

- `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`
- `schemas/agent-event-v2.schema.json`
- `templates/agent-event-comment.md`
- directly-owned `scripts/test_v410_t04b_review_currentness.py`
- existing review finding/aggregation semantics only if a concrete same-family gap requires a minimal change

## Forbidden scope

No second Review lifecycle/event/status/registry. No new finding registry. No majority/model-count/provider authority. No Validation/Release ownership. No rewrite of T04A repair-routing or T02B causality/responsibility. No central manifest/discovery wiring. No authority transfer from PR #901 or its gates.

The R3 executor must reconstruct/port only the semantically required T04B changes onto this current base; legacy `.agent/execution/V410-T04B/{TASK,CONTEXT,PLAN,COMMANDS,DOD,HANDOFF}.md` artifacts from historical PR #901 are not part of R3 and must not be introduced.
