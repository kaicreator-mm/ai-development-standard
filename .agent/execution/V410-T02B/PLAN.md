# V410-T02B Plan

1. Re-read #853, current branch HEAD, baseline `67c6828...`, all pinned owner blobs, and confirm no active incompatible claim.
2. Publish accepted Builder claim before any source mutation.
3. Implement smallest reuse-first projection. Prefer optional `parent_dispatch_ref` and `responsibility_mode` on existing dispatch/event-v2 structures only where tests prove reconstruction otherwise impossible.
4. Update protocol/template text only to explain the same-family additive projection; do not create a parallel lifecycle or authority.
5. Add focused positive/negative tests from L3 Wave C.
6. Run focused protocol/schema/event-writer suites plus relevant regression.
7. Produce exact candidate PR to `version/v4.10.0`, then stop for exact-SHA Concern Validation + Fresh Independent Review.

Any baseline drift or material owner mismatch requires JIT rebind before source mutation.