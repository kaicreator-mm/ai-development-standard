# T-006 Task Pack — Operation Routing, Reducer and Orthogonal State Integration

Issue: #78
Parent version: #72
Baseline: `2457eaafc00be7ddae4ccee3c2fbe0deb7fe8e3a`
Review Policy: required
Risk: high
Validation scope: concern
Agent freedom: F1_BOUNDED_IMPLEMENTATION

## Goal

Integrate v4 Operation/correlation semantics into the existing reducer/execution architecture without creating a second state machine, third execution DAG, or mixed truth/routing status.

## Inputs

- merged T-001..T-005 v4 authority/artifacts;
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md`;
- #99 controller-effect idempotency obligation;
- #101 Operation graph / canonical DAG obligation;
- #110 P2-1 Review judgment vs route separation.

## Allowed changes

- `docs/implementation/4.0.0/OPERATION_ROUTING_INTEGRATION.md`;
- this Task Pack;
- T-006 pointer in `docs/implementation/4.0.0/TASK_PACKS.json`.

## Forbidden changes

- JSON/event/dispatch schema implementation;
- verifier/reducer executable code;
- T-007 Work Item / Execution Pack contract changes;
- T-008 release/validation authority changes;
- new runtime DB/queue authority;
- new event-v2 enum values.

## Tests / review oracle

A reviewer must verify at least:

1. v3.4 workflow/Gate/provider/dispatch/candidate/release dimensions remain orthogonal;
2. `operation_id` is correlation, not a replacement workflow state;
3. GitHub Task Issues + Issue Dependencies remain the canonical live execution DAG;
4. Operation edges cannot independently mark Tasks READY/BLOCKED;
5. Review judgment and requested workflow route are separate dimensions;
6. `VALIDATION_REQUESTED` cannot manufacture Validation PASS;
7. stale Operation/exchange evidence is historical and not rebound;
8. semantic controller-effect idempotency is stable across fresh `exchange_id` retries;
9. merge/freeze/repository-integration preflight re-reads exact current identity;
10. Builder/Reviewer/Validator ready sets remain projections of one architecture;
11. reducer/recovery can be reconstructed from durable facts after cache loss;
12. Fast Path does not acquire ceremonial Operation requirements;
13. no T-007/T-008/T-009 implementation scope is entered.

## Failure handling

- conflicting authoritative facts fail closed and route to owning authority;
- runtime/factual uncertainty routes to Validation/evidence rather than reducer inference;
- unresolvable subject identity makes the Operation/exchange stale/invalid for current effects;
- if machine enforcement is required, route it to T-009 rather than implementing it here.

## Completion

Repository verifier PASS on final exact HEAD + Fresh Independent Review PASS on same HEAD + focused merge to `version/v4.0.0`.