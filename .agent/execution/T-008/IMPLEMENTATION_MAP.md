# T-008 Implementation Map

Read first, in order:

1. `docs/implementation/4.8.0/task-packs/T08_scheduling_conformance.md`
2. `docs/implementation/4.8.0/L3_REFERENCE_PACKS.md#t-008--eligibilityresource-conformance`
3. Frozen L2 §§7–9
4. `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §§6, 11, 27
5. existing `scripts/test_v48_execution_architecture.py`

Implement exactly one new focused conformance module: `scripts/test_v48_scheduling_conformance.py`.

Keep the oracle deterministic and self-contained. Represent READY work, candidate logical Agent/profile facts, Availability/currentness, independence constraints, capacity groups, required units and durable accepted binding facts as explicit in-memory test inputs. Exercise selection as two phases: hard-filter derivation first, optional ranking second.

For admission scenarios, model the full protected set `{work claim + every required resource/capacity/compatibility binding}` and expose a single commit boundary. Inject failures immediately before, during/at, and after publication so tests can distinguish rejected/no-state, accepted all-or-none state, and ambiguous state requiring durable reconciliation.

Do not modify `EXECUTION_ARCHITECTURE_STANDARD.md` to make a test pass. A mismatch between the merged owner semantics and the deterministic oracle is a finding against T-002/current architecture and must be escalated rather than repaired inside T-008.

Do not implement a distributed locking protocol. The model may assert that unsupported composite concurrency routes to existing single-writer admission or `BLOCKED/UNAVAILABLE`.
