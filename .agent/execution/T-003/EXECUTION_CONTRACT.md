# T-003 JIT Execution Contract

## Exact authority

- Issue: #722 / T-003 Authority / State Registry Integration.
- Base: `version/v4.9.0@df94641e6082dc7a2988e73eafdffd3bf42668b9`, tree `a8c86675d003d397636304f3441a14385660f9c5` (post lineage-composition PR #792).
- Frozen Product (`a8ec7030...`), Frozen L2 (`bd41ea01...`), Frozen Task DAG v0.2 (`b9fe0cc7...`), current Task Pack (`14c65526...`) and L3 remain authoritative.
- Immutable DAG v0.1 `### T-003` (blob `4f358ba2...`) is the normative concern definition, composed with the Frozen DAG v0.2 admission rules.
- Native blockers zero; lineage LG47_REGISTRY current at base (surfaces verified at admission). Any base/authority drift before Builder mutation requires Controller rebind.

## Required result

Integrate v4.9 semantic concerns with the v4.7-inherited Authority/Applicability + State-Dimension/Forbidden-Inference registries WITHOUT creating a second discovery table:

1. `standard-manifest.json`: add canonical owner/applicability entries for the v4.9 concerns (assurance proof/currentness per T-002's Assurance Plan v2, Role Execution Profile v1 reference, Release applicability reference, and other new v4.9 semantic concerns) — entries reference owners; they never grant semantic/mutation/merge/dispatch/review/validation/release authority; preserve all inherited entries verbatim (union, zero duplicates).
2. `registries/state-dimensions-v1.json`: register proof/currentness and the `WAITING_LINEAGE` derived posture plus the v4.9 forbidden inferences required by Frozen L2; no workflow lifecycle state.
3. The two registry reference documents: document the new entries/dimensions without granting authority.
4. `scripts/test_v49_authority_state_registry.py`: new focused verifier enforcing owner uniqueness, currentness, no second registry/workflow state, and the negative oracles N01–N14 from the #722 preflight (duplicate owner => fail; registry metadata as authority => forbidden; task-DONE => lineage-current forbidden; Role Profile => capability-proven forbidden; capability => role-action/terminal-authority forbidden; concern-level => version-level Release applicability forbidden; proof/currentness => Validation/Review/Release PASS or Task READY forbidden; WAITING_LINEAGE => canonical workflow state forbidden; stale/broken ref => permissive owner forbidden, fail closed; old-SHA PASS => successor PASS forbidden; provider/model/runtime availability => authority forbidden; second discovery table/resolver forbidden; v4.8 registry/adoption metadata as semantic authority forbidden; inherited F01–F10 state-dimension negatives intact and non-weakened).

## Hard boundaries

- Must not change domain-owner semantics or create workflow state; no second discovery table or resolver.
- Read-only schema inputs (both v1 schemas) must not be mutated; if a v1 schema cannot represent a Frozen v4.9 requirement, STOP and route for architecture/rebind (BLOCKED) rather than widening scope.
- No registry metadata may grant authority; `WAITING_LINEAGE` stays a derived, non-dispatch projection.
- No Product/L2/DAG/normative-owner mutation; frozen blobs must resolve unchanged at the candidate.
- Missing/unavailable evidence => `NOT_RUN|BLOCKED`, never synthetic PASS.

## Mutation authority

Only the six Builder paths in MANIFEST `builder_write_set` are writable (pack revision T003-PACK-R2 added `templates/golden/STANDARD_COVERAGE.json` per #722@5985991276: the CI-pinned golden-template coverage ledger is the mechanical twin of a `normative_standards` registration and must travel in the same change), plus the six immutable `.agent/execution/T-003/**` planning files. Everything else read-only. Builder tests are not independent Validation.
