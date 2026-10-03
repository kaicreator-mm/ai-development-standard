# Assurance Plan Owner Continuity Reference

This reference explains how existing Assurance Plan artifacts resolve after v4.9 T-001 canonicalization. It is explanatory evidence; `standards/ASSURANCE_PLAN_STANDARD.md` is the stable normative owner surface.

## Canonical mapping

| Surface | Role | Owner-family result |
|---|---|---|
| `standards/ASSURANCE_PLAN_STANDARD.md` | stable normative owner surface | `assurance-plan` |
| `docs/implementation/4.0.0/ASSURANCE_PLAN.md` | historical v4.0 authority definition | same `assurance-plan` family |
| `schemas/assurance-plan-v1.schema.json` | v1 machine contract | same `assurance-plan` family |
| `docs/implementation/4.0.0/ADVERSARIAL_REVIEW.md` | finding/conflict/aggregation authority | delegated aggregation concern; not a second Assurance Plan owner |
| `schemas/review-aggregation-v1.schema.json` | aggregation machine contract | preserves finding union/blocker dominance |

## Positive resolution examples

### Historical v1 record

A project pinned to an ADS revision using `assurance-plan-v1` may continue to read and interpret that record under its pinned authority. Canonicalization does not invalidate or reinterpret it.

### New owner reference

New work may point to `standards/ASSURANCE_PLAN_STANDARD.md` for owner identity while continuing to use the applicable versioned Assurance Plan schema. A future v2 remains a versioned successor in the same family.

### Aggregation

When multiple review results exist, Assurance Plan aggregation delegates to the existing Adversarial Review semantics. A valid unresolved blocker survives unrelated PASS results; majority voting does not establish correctness.

## Negative examples

The following must be rejected or routed upward:

- declaring both `assurance-plan` and `proportional-assurance` as competing owners for the same semantic concern;
- treating a canonical owner reference as permission to convert Review PASS into Validation PASS;
- using three PASS results to outvote one current valid blocking finding;
- marking a historical v1 record invalid only because the canonical owner document moved to `standards/`;
- using a registry/manifest alias as semantic authority;
- assuming future Assurance Plan v2 proof/currentness semantics before T-002 authority is implemented.

## Failure posture

```text
ambiguous owner resolution
or conflicting owner semantics
or required historical reinterpretation
=> FAIL_CLOSED / AUTHORITY_OR_ARCHITECTURE_ROUTING
```

T-001 only canonicalizes owner continuity. It does not repair sibling standards or expand the Assurance Plan family contract.
