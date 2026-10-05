# V410-T04B Plan

1. Re-read #857, native blockers, current integration HEAD, this branch/pack identity and exact owner blobs immediately before claim.
2. Publish accepted serialized Builder `DISPATCH_CLAIMED` before any source mutation.
3. Consume integrated T04A/T02B semantics; do not redefine them.
4. Implement the smallest same-family finding/currentness projection needed for deterministic reconstruction and aggregation.
5. Preserve exact-subject Review semantics: stale results historical-only; conflicts/ambiguity fail closed; no reviewer/model-count authority.
6. Bind root-defect classification to integrated T04A vocabulary; route repair/escalation back to T04A owner semantics.
7. Add focused positive/negative tests and run directly relevant protocol/schema/currentness regressions.
8. Open exact candidate PR to `version/v4.10.0`; stop for independent concern Validation + Fresh Independent Review.

Any target/owner drift before claim or material conflict with integrated T02B requires Controller rebind; do not silently widen scope.