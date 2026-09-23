# T-005 Task Pack — Agent Interchange Correlation Envelope and GitHub Mapping

Issue: #77
Parent version: #72
Baseline: `638e0bedb3ce8ab50ae045b3f7cb29a3f179e2f8`
Review Policy: required
Risk: high
Validation scope: concern
Agent freedom: F1_BOUNDED_IMPLEMENTATION

## Goal

Define the minimal lifecycle-wide exchange/correlation contract for Agent collaboration without introducing a second workflow or prematurely breaking `ai-dev:event:v2`.

## Allowed changes

- `docs/implementation/4.0.0/AGENT_INTERCHANGE.md`
- this Task Pack
- T-005 pointer/metadata in `docs/implementation/4.0.0/TASK_PACKS.json`

## Forbidden changes

- schema/reducer/verifier implementation;
- changing released event-v2 semantics;
- implementing T-004 finding aggregation;
- creating event-v3 without a demonstrated breaking requirement;
- transport software.

## Tests / review oracle

A reviewer must verify:

1. every exchange correlates to an Operation or bounded controller/assurance requirement;
2. `operation_id`, `dispatch_id`, exchange identity and subject identity remain distinct;
3. logical operator attribution preserves v3.4 semantics;
4. stale/duplicate/superseded/conflict handling is append-oriented and fail-closed;
5. ACK/delivery state cannot become workflow/Gate/Release truth;
6. GitHub remains the reference durable profile;
7. pointer-only invocation remains intact;
8. transport-neutrality is limited to the logical envelope, not project authority;
9. event-v2 reuse/additive extension is sufficient for current v4 requirements;
10. no parallel Agent state machine is introduced.

## Failure handling

- if additive event-v2 cannot express a required invariant, record a concrete breaking reason and route to architecture authority before proposing event-v3;
- if event semantics conflict with released owning standards, CHANGES_REQUESTED;
- if runtime behavior cannot be statically established, request validation rather than infer.

## Completion

Repository verifier PASS on final exact HEAD + Fresh Independent Review PASS on same HEAD + focused merge to `version/v4.0.0`.
