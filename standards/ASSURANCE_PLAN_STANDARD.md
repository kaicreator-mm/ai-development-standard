# Assurance Plan Standard

## 1. Purpose and owner continuity

This standard is the stable normative owner surface for the existing ADS Assurance Plan family. It **canonicalizes** the v4.0 owner; it does not create a new assurance lifecycle, aggregation authority, workflow state, or gate-result authority.

```text
CANONICAL_OWNER_ID=assurance-plan
LEGACY_AUTHORITY=docs/implementation/4.0.0/ASSURANCE_PLAN.md
V1_SCHEMA=schemas/assurance-plan-v1.schema.json
AGGREGATION_AUTHORITY=docs/implementation/4.0.0/ADVERSARIAL_REVIEW.md
AGGREGATION_SCHEMA=schemas/review-aggregation-v1.schema.json
OWNER_CONTINUITY=SAME_FAMILY
```

The v4.0 Assurance Plan semantics and `assurance-plan-v1` records remain valid history and compatible inputs. Consumers SHOULD resolve the legacy implementation document and the canonical standard above to the same semantic owner identity.

## 2. Authority boundary

The Assurance Plan selects and orders required assurance work. Each owning standard still defines what its result means.

In particular:

- `VALIDATION_STANDARD.md` owns executable Validation truth;
- Review policy and review-result semantics remain owned by their applicable review authority;
- `RELEASE_STANDARD.md` owns candidate/release authority;
- Product, Architecture and Task authority are not granted by an Assurance Plan;
- model/provider identity, confidence, routing preference, file count, labels, or prose do not independently create assurance authority.

Canonicalization MUST NOT be interpreted as permission to translate one evidence family into another or to treat missing/`NOT_RUN` work as PASS.

## 3. Existing aggregation authority is preserved

Finding aggregation remains the v4.0 Adversarial Review concern. The canonical Assurance Plan owner consumes that authority; it does not redefine it.

The existing machine contract remains:

```text
aggregation.policy=finding-union-blocker-dominance
aggregation.blocker_resolution=unresolved-valid-blocker-dominates
aggregation.majority_vote_for_correctness=false
```

Therefore:

1. every current valid material finding remains in the finding union until validly dispositioned;
2. a PASS from another reviewer cannot cancel an unresolved valid blocker;
3. majority vote cannot create correctness;
4. correction/disposition is append-oriented and must remain attributable;
5. stale evidence is handled by the owning currentness rules, not silently promoted or deleted.

## 4. Family and versioning rule

`schemas/assurance-plan-v1.schema.json` remains the v1 machine family contract. A later successor such as v2 is a **same-family versioned successor**, not a second proportional-assurance owner.

A successor MAY add fields or semantics only under its Frozen Product/Architecture/Task authority and applicable compatibility governance. The successor MUST preserve explicit continuity to `CANONICAL_OWNER_ID=assurance-plan` and MUST NOT silently change the meaning of historical v1 records.

v4.9 T-002 owns any authorized v2 proof/composition/currentness contract. This T-001 canonicalization does not pre-authorize those semantics.

## 5. Canonical resolution and aliases

New ADS work SHOULD reference this standard as the stable owner surface. Historical references to:

```text
docs/implementation/4.0.0/ASSURANCE_PLAN.md
schemas/assurance-plan-v1.schema.json
```

remain valid and resolve to the same owner family. Alias/reference wiring may improve discoverability but MUST NOT grant semantic authority or create a parallel owner.

If owner resolution is ambiguous or two surfaces claim conflicting assurance semantics, the consumer MUST fail closed and route to the authority/architecture governance path rather than use last-writer-wins.

## 6. Forbidden interpretations

The following are non-conformant:

- creating a second `proportional-assurance` owner beside the Assurance Plan family;
- treating the canonical document as a replacement for Validation, Review, Release, Product, Architecture, or Task authority;
- changing `finding-union-blocker-dominance` or blocker dominance as part of canonicalization;
- making majority vote an acceptance predicate;
- invalidating historical v1 records because this stable owner surface now exists;
- claiming v4.9 T-002 successor semantics before the successor is independently implemented and admitted.

## 7. Compatibility rule

Projects pinned to an older applicable ADS revision remain governed by that pinned authority. Adoption of this canonical owner surface is additive/prospective unless an owning migration authority explicitly says otherwise.

If canonicalization would require reinterpretation of historical Assurance Plan or Adversarial Review records, stop with an authority/architecture contradiction; do not repair it locally in an implementation Task.
