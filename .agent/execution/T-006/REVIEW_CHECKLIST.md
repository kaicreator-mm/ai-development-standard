# T-006 Successor Review Checklist

## Exact subject / authority

- [ ] New successor PR, HEAD, TREE and current base are recorded; PR #741 is not reused.
- [ ] Candidate was built from pinned `version/v4.8.0@e433c18bef84fea15abbc8d308fd9c9b4384c520` or a formally rebound successor base.
- [ ] Task Pack blob = `b9e6eb77a3828cfa8dcdc6f6d54e92cbcdb8e308` and L3 blob = `d566d37abe4df6e0f39732da412b0f7cd00724a4`, unless a formally recorded rebind supersedes this pack.
- [ ] v4.7 source = `d8f613127d0167453297a5a5e983de048607aa07` / tree `721dd393b7693d2ce82ebe0533a7fa51726d0a78`.

## Write-set / carry-forward

- [ ] Candidate diff is a subset of the exact 22-path Builder write set.
- [ ] All 16 COPY_EXACT paths match pinned v4.7 bytes/blob identities.
- [ ] `standard-manifest.json`, `standards/PROJECT_ADOPTION.md`, and project override template were composed from current v4.8, not overwritten wholesale by v4.7 versions.
- [ ] Version-specific v4.7 T07/T09/closure/dogfood/release evidence was not rebound or copied as current v4.8 evidence.

## Semantic invariants

- [ ] Exactly three v4.8 machine families are registered once.
- [ ] Interchange v1 is reused exactly once; no v2/second semantic owner.
- [ ] Availability remains derived and is not a fourth durable family.
- [ ] Registry has one canonical owner per semantic concern; same existing owner may serve distinct concerns without creating duplicate authority.
- [ ] Registry/read routing remain `authority_effect=NONE`, `gate_effect=NONE`, `mutation_authorized=false`.
- [ ] State dimensions remain owner-qualified and forbidden cross-dimension inference is preserved.
- [ ] Provider/model provenance or availability never grants correctness, authorization, routing admission, Validation/Review/Release truth.
- [ ] Logical Agent capability profile/evidence does not absorb runner/host resource facts, current Availability, or current Validation/Review truth.
- [ ] Fast Path remains lightweight and `TASK_LEARNING=NONE_MATERIAL` remains valid.
- [ ] Historical exact-SHA evidence cannot transfer to successor exact subject.

## Fresh Review P1/P3

- [ ] P1-01 is actually closed: v4.7 registry/read-routing stack is current discovery machinery, not lineage-only prose.
- [ ] P3-01 is hardened with contradiction-aware mutation probes, not token-presence-only assertions.
- [ ] RA-N03/N04/N05/N09/N13 inject contradictory grants while retaining safe tokens and still fail closed.
- [ ] RA-N01/N02/N06/N07/N08/N10/N11/N12 also fail closed as specified.

## Gates / separation

- [ ] All Task Pack commands pass on exact candidate.
- [ ] Builder evidence is not treated as independent Validation.
- [ ] A genuinely independent exact-subject Validator produces PASS before Fresh Review.
- [ ] A genuinely fresh high-capability Reviewer consumes the exact Validation subject and independently reviews the candidate.
- [ ] No merge occurs from Builder/Validator/Reviewer roles; Controller expected-head integration remains separate.
