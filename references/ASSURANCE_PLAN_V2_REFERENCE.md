# Assurance Plan v2 Reference

`assurance-plan-v2` is a versioned successor inside the existing `assurance-plan` owner family. It does not create a second assurance owner or lifecycle.

Canonical machine contract: `schemas/assurance-plan-v2.schema.json`.
Historical v1 remains valid under `schemas/assurance-plan-v1.schema.json`.

## 1. Resolution order

The deterministic order is:

```text
1. resolve the concern's current Gate Authority and baseline requirement;
2. ask that owner whether reduction is positively permitted for this exact subject;
3. prove every required reduction predicate from current durable facts / deterministic checks / owner records;
4. resolve the concern to BASELINE | REDUCED | STRONGER | BLOCKED;
5. compose all concern resolutions conjunctively with no cross-owner cancellation;
6. select a path that satisfies the composed floor or is stronger;
7. bind the result to exact currentness inputs.
```

Cross-owner composition never runs first. A permission from owner A cannot cancel owner B's requirement.

## 2. Positive permission and proof

`REDUCED` is legal only when:

```text
owner_permission.decision == ALLOW_REDUCTION
AND predicate_proofs has at least one required proof
AND every required predicate proof has state == TRUE
AND every proof uses basis durable-fact | deterministic-check | owner-record
AND all authority/proof/currentness refs are current
```

`FALSE`, `UNKNOWN`, missing, ambiguous or stale permission/proof is not a reduction proof. Route to the stronger legal path or BLOCKED.

The following signals are never sufficient on their own:

```text
docs-only
risk:low
Fast Path label
recommended + skip
small file count
a strong model/provider
model judgment or confidence
another concern's PASS
```

A model may propose predicates or explain evidence; it is not the sole proof basis for lowering assurance.

## 3. Assurance floor vs selected path

The assurance floor is the composed set of owner-bound requirements after valid concern-local resolutions. It is not a single global numeric score.

`selected_path` is the actual execution/assurance path chosen after that floor exists. It must be `SATISFIES_FLOOR`, `STRONGER_THAN_FLOOR`, or `BLOCKED`.

A selected path cannot rewrite the floor to justify itself.

## 4. Adverse findings

`finding_carry_forward_policy=unresolved-valid-findings-carry-forward` preserves the existing Adversarial Review owner rule.

A fresh PASS does not erase a current unresolved blocker. A finding leaves the current unresolved set only through the owning disposition/successor/currentness rules. v2 does not redefine finding aggregation; `finding-union-blocker-dominance` and `unresolved-valid-blocker-dominates` remain the existing authority.

## 5. Currentness binding

A v2 plan binds currentness across all material inputs:

```text
subject identity
owner authority refs + digest
proof input refs + digest
Task Pack ref + digest
Release decision refs + digest (the digest also binds an empty set)
unresolved finding refs + digest (the digest also binds an empty set)
final binding digest
```

`state=CURRENT` is valid only when every bound component is exact and current under its owner. Any material mismatch makes the prior binding `STALE`; unresolved or unprovable status is `UNKNOWN`. Both fail closed for any assurance reduction.

The machine record stores the binding. Execution-time owners such as Dispatch/Claim/merge consume/recheck it in their own tasks; v2 does not preimplement those transitions.

## 6. Example: legal reduction

```yaml
concern_id: review-policy
owner_ref: standards/REVIEW_POLICY_STANDARD.md@<current>
gate_ref: review-policy
baseline_requirement_ref: review-required
owner_permission:
  decision: ALLOW_REDUCTION
  authority_ref: <owner-positive-rule>
  currentness_ref: <current-owner-proof>
predicate_proofs:
  - predicate_ref: <bounded-low-risk-predicate>
    state: TRUE
    basis: deterministic-check
    evidence_refs: [<durable-evidence>]
    currentness_ref: <current-proof>
resolution: REDUCED
selected_requirement_ref: review-not-required
currentness_ref: <exact-concern-binding>
```

This is legal only if the owning review policy actually grants that reduction. Merely naming the predicate does not grant authority.

## 7. Example: illegal optimistic reduction

```yaml
owner_permission:
  decision: UNKNOWN
predicate_proofs:
  - state: TRUE
    basis: deterministic-check
resolution: REDUCED
```

Invalid: owner permission is not positive. The correct route is baseline/stronger path or BLOCKED.

Likewise, `ALLOW_REDUCTION + predicate state UNKNOWN` is invalid.

## 8. v1/v2 compatibility

v1 and v2 share the same semantic owner and preserve v1 activities/aggregation vocabulary. v2 intentionally uses an explicit protocol version and adds mandatory proof/composition/currentness fields; a v1-only parser is not assumed to accept a v2 instance.

Therefore compatibility is version-aware:

- historical v1 record validity: preserved;
- owner-family semantics and aggregation authority: preserved;
- v2 reader support for explicit v2 records: new capability;
- direct validation of a v2 instance against the v1 schema: not claimed;
- adoption by v1-only consumers: requires explicit version negotiation/update, not silent reinterpretation.

See `references/ASSURANCE_PLAN_V2_COMPATIBILITY.json` for the v4.2 Compatibility Record.

## 9. Ownership boundaries

T-002 does not own:

- authority/applicability registry entries — T-003;
- execution reducer / Dispatch / Claim / merge-time recheck — T-007;
- gate-evidence transfer and successor wiring — T-010;
- Review, Validation or Release verdict meaning;
- manifest/adoption discovery — T-011.

If those surfaces are required to make this contract appear functional, stop and route to the owning Task rather than extending T-002 scope.
