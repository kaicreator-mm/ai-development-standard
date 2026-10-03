# T-002 Execution Contract

## Subject
Implement the same-family Assurance Plan v2 proof/composition/currentness contract authorized by Frozen v4.9 Product/L2/DAG, on base `version/v4.9.0@722bb229e9136c21116e1c03a0af65342c187e0a`.

## Allowed semantics
- preserve canonical owner `assurance-plan` and all v1 historical records;
- add versioned v2 machine contract only inside the same family;
- represent concern-local Gate Authority precedence before cross-owner monotonic conjunction;
- require owner-positive permission plus deterministic proof before any reduction;
- distinguish assurance floor from selected execution path;
- bind currentness to subject, owner authority, proof inputs, Task Pack, Release decision refs and unresolved-finding digest;
- carry unresolved adverse findings forward until owner-valid disposition/successor rules say otherwise;
- preserve v4.0 Adversarial Review aggregation ownership;
- produce explicit v4.2 compatibility evidence.

## Hard negatives
`docs-only`, `risk:low`, Fast Path, `recommended+skip`, file count, provider/model strength or model judgment alone MUST NOT prove a reduction. UNKNOWN/ambiguous/missing owner permission or proof MUST NOT lower assurance.

## Source write set
Exactly the five paths in `MANIFEST.yaml`. Immutable `.agent/execution/T-002/**` bookkeeping is outside source semantics.

## Forbidden
No manifest/registry wiring, no T-003 authority registry work, no T-007 execution reducer/Dispatch/Claim integration, no T-010 gate-currentness integration, no Release/Validation/Review PASS semantics, no mutation of v1 or review-aggregation schemas.

Any need to expand these boundaries is `TASK_PACK_DEFECT` or architecture/DAG amendment, not local implementation freedom.
