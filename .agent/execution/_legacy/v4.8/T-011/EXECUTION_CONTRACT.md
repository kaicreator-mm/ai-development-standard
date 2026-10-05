# T-011 Execution Contract

## Exact subject

- Base: `94955c6f93fd7316406ea96bce8f7c32a62509ef`
- Base tree: `bb7f25f1e05ff2423fc79029465bcf7be458a82c`
- Target: `version/v4.8.0`
- Task: `T-011` / Issue `#517`
- Task Pack blob: `e1c412c44f67df736d1b1598a590a0eac31a4b22`
- L3 blob: `9d40ed242b146a54b9ccbf39fe0a85fc2efcfac6`

The Builder may implement only the bounded heterogeneous orchestration dogfood described by the Task Pack/L3. This pack does not authorize changes to Product/L2/DAG, normative standards, schemas, upstream completed Task artifacts, CI/workflows, T-014 or Release/Closure authority.

## Builder write set

Exactly:

```text
scripts/test_v48_orchestration_dogfood.py
docs/implementation/4.8.0/dogfood/orchestration/**
```

If another path is required, stop and request an Execution Pack rebind. A normative semantic/public-contract change requires `ARCHITECTURE_AMENDMENT_REQUIRED` or separately authorized repair rather than widening this Task.

## Required semantics

The dogfood must preserve and compose existing authority:

1. hard eligibility before optional ranking;
2. stale/missing material Availability -> `UNKNOWN` and fail closed;
3. reviewer/validator independence as a hard filter;
4. composite all-or-none work + scarce-resource admission; capacity-N never exceeds N; N=1 is exclusive;
5. existing Interchange v1 family and `ai-dev:event:v2` writer/admission semantics; ACK/progress/heartbeat are non-authoritative;
6. accepted Claim is the T-017 durable Start Record; current-state labels/cards are derived visibility, not a lock;
7. crash/restart reconstructs authoritative state from durable facts only;
8. timeout/stale replacement fails closed on ambiguous claim/publication/resource state;
9. bounded executor acts only within exact authority/currentness/write-set/freedom constraints and escalates on semantic ambiguity;
10. provider/model identity is provenance, not correctness/authorization/ranking authority;
11. synthetic evidence is never presented as real host/device/provider/runtime evidence;
12. measured dogfood data is descriptive only; no blanket strong-to-low-cost or savings conclusion.

## Planning/implementation phase separation

This JIT planning phase may create/update only Task Pack, task-scoped L3 and `.agent/execution/T-011/**`. It must not create the focused dogfood script or dogfood result artifacts. Those are Builder work after a separate accepted Builder dispatch/claim.

## Completion evidence

Builder terminal must bind exact candidate SHA/tree, exact base, exact diff, scenario/evidence matrix, command results and evidence classes. Independent Validation is required on the exact candidate, followed by genuinely Fresh Independent Review. External environment claims require environment-specific exact-subject Validation or remain `NOT_RUN/BLOCKED`.
