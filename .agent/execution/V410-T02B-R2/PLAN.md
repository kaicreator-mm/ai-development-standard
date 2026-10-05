# V410-T02B R2 Plan

1. Re-read #853, branch HEAD, current integration HEAD and all owner blobs immediately before claim.
2. Publish accepted serialized Builder `DISPATCH_CLAIMED` before any source mutation.
3. Implement the smallest same-family additive projection needed for causal parent linkage and responsibility mode/handoff pairing.
4. Keep fields optional/backward compatible and preserve historical event/dispatch validity.
5. Add focused positive/negative tests from L3 Wave C.
6. Run focused protocol/schema/event-writer/execution regressions.
7. Open exact candidate PR to `version/v4.10.0`; stop for Concern Validation + Fresh Independent Review.

Target drift before claim requires a fresh staleness/currentness decision; do not silently mutate against a stale base.