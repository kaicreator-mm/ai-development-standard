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

## 8. Assurance Plan v2 — same-family successor

`schemas/assurance-plan-v2.schema.json` is the v4.9 same-family successor machine contract.

```text
V2_SCHEMA=schemas/assurance-plan-v2.schema.json
V2_PROTOCOL=ai-dev-assurance/v2
V2_OWNER_FAMILY=assurance-plan
V2_PREDECESSOR_PROTOCOL=ai-dev-assurance/v1
```

v2 adds explicit proof, owner-scoped composition and currentness binding. It does **not** change the meaning of v1 records, create a second owner, or grant Review/Validation/Release/Execution authority.

A v1-only parser is not assumed to accept a v2 instance. Version-aware consumers MUST negotiate/select the schema version explicitly. Historical v1 records remain valid under v1.

## 9. Gate Authority precedence before reduction or composition

A concern MUST resolve its own current Gate Authority and baseline requirement before any cross-owner composition occurs.

For an assurance reduction to be legal on an exact subject, all of the following are required:

```text
CURRENT_OWNER_AUTHORITY
AND OWNER_PERMISSION=ALLOW_REDUCTION
AND REQUIRED_PREDICATE_PROOFS_PRESENT
AND EVERY_REQUIRED_PREDICATE_STATE=TRUE
AND EVERY_PROOF_BASIS in {durable-fact, deterministic-check, owner-record}
AND PROOF_AND_PERMISSION_CURRENT
```

If owner permission is `DENY_REDUCTION`, `UNKNOWN`, missing, ambiguous or stale, reduction is forbidden. If any required predicate is `FALSE`, `UNKNOWN`, missing, ambiguous or stale, reduction is forbidden. The route is the stronger legal path or BLOCKED according to the owning workflow.

A model may propose a predicate or summarize evidence, but model judgment/provider strength/confidence MUST NOT be the sole proof basis for lowering assurance.

The following facts do not independently prove reduction eligibility:

```text
docs-only
risk:low
Fast Path
recommended + skip
small file count
model/provider strength
model confidence or prose judgment
an unrelated gate PASS
```

## 10. Owner-scoped assurance floor and cross-owner composition

The v2 assurance floor is an explicit set of owner-bound requirements, not one global risk/review score.

Within each concern, valid owner permission and proof may resolve the concern to:

```text
BASELINE
REDUCED
STRONGER
BLOCKED
```

Only after concern-local resolution are the results composed across owners.

Cross-owner composition is:

```text
policy=conjunctive-no-cancellation
cancellation_allowed=false
```

One owner's permission or local PASS MUST NOT cancel another owner's current requirement. Unknown/conflicting owner authority fails closed rather than using last-writer-wins.

## 11. Assurance floor versus selected path

The assurance floor records the minimum current owner-bound obligations after legal concern-local resolutions. The selected path records what will actually be executed.

These are distinct machine facts. The selected path MUST be classified as exactly one of:

```text
SATISFIES_FLOOR
STRONGER_THAN_FLOOR
BLOCKED
```

A chosen execution path cannot retroactively redefine the floor in order to justify itself. Optional ranking/optimization happens only after hard owner/floor predicates are satisfied by their owning orchestration semantics.

## 12. Currentness binding

A v2 Assurance Plan currentness record MUST bind the exact material inputs used to resolve the plan:

```text
subject identity
owner authority refs + digest
proof input refs + digest
Task Pack ref + digest
Release decision refs + digest
unresolved finding refs + digest
final binding digest
```

An empty Release-decision or unresolved-finding set is still bound by its digest; omission is not equivalent to an empty set.

The binding state is:

```text
CURRENT
STALE
UNKNOWN
```

`CURRENT` means every bound component is exact and current under its owner-defined currentness rule. Any material identity/digest drift makes the prior binding `STALE`. Missing, ambiguous or unprovable currentness is `UNKNOWN`.

`STALE` and `UNKNOWN` MUST NOT authorize a lower assurance path. They route to recomputation/rebinding, stronger legal assurance, or BLOCKED under the owning transition. T-007/T-010 own runtime/gate wiring that consumes this contract; this section does not preimplement those transitions.

## 13. Adverse-finding carry-forward

v2 fixes the plan-side rule:

```text
finding_carry_forward_policy=unresolved-valid-findings-carry-forward
```

The current unresolved-finding set and digest are part of currentness. A new reviewer, new model, new route, or unrelated PASS cannot make a current adverse finding disappear.

A finding leaves the current unresolved set only through the applicable owner-defined disposition, successor-subject rule, or currentness rule. Existing Adversarial Review aggregation remains authoritative; v2 does not redefine finding equivalence, severity, challenge, or aggregation.

## 14. v4.2 compatibility evidence

Assurance Plan v2 adoption is governed by `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md`.

The compatibility record MUST bind explicit v1 baseline and v2 candidate identities, change operations and dimension-specific outcomes. No schema/checker outcome may manufacture behavioral/consumer compatibility.

For this successor:

- owner-family semantics: compatible;
- historical v1 record validity: compatible;
- existing aggregation authority: compatible;
- direct v1-schema validation of a v2 instance: not claimed and recorded as incompatible;
- version-aware adoption: conditional on explicit version negotiation/update.

This is not a defect in v1 history and MUST NOT be rewritten as universal compatibility. See `references/ASSURANCE_PLAN_V2_COMPATIBILITY.json`.

## 15. Task ownership boundary

T-002 owns only this same-family v2 contract, proof/composition/currentness representation, v4.2 compatibility evidence and focused deterministic conformance.

It does not own:

- Authority/Applicability or State registry integration (T-003);
- execution reducer, JIT, Dispatch/Claim/merge-time recheck (T-007);
- gate-owned evidence transfer/currentness integration (T-010);
- Release applicability semantics;
- Review or Validation result meaning;
- central manifest/adoption wiring (T-011).

If using v2 requires one of those surfaces to change, the affected work remains pending for its owning Task; T-002 MUST NOT preimplement it.
