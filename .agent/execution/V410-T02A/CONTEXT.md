# Context

Currentness binding:
- integration baseline `c1a40700336309e2dbb4771fcd893a257d260aa8`;
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md` blob `765fc07c4a6ab9fb47a4d81c8adaaae505dc69f4`;
- native DAG #866 PASS/read-back 17/17;
- task has no predecessors.

Required semantics:
- `DELEGATED_SUBWORK`: delegator retains responsibility.
- `RESPONSIBILITY_HANDOFF`: active responsibility transfers explicitly within legally delegatable authority.
- child authority is bounded by delegatable ∩ Task/Work ∩ role ∩ external/project authorization.
- responsibility/causation is reconstructible.
- Human controllability supports inspect/pause/cancel/redirect/authority decisions without making humans routine relays.

Currentness drift or requirement for an incompatible new execution-state family fails closed.