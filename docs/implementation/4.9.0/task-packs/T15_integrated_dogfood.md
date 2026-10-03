# T-015 Task Pack — Integrated Dogfood / Release Evidence Handoff

Status: **MATERIALIZED TASK PACK — NOT BUILDER READY**

Authority: Frozen Product #709; Frozen L2 #714; Frozen Task DAG v0.2 blob `b9fe0cc7089f64929b4bcf45f7230d950e864db2`; DAG Freeze #719; Issue #734.

```yaml
task_id: T-015
issue: 734
dependencies: [T-011/#730, T-012/#731, T-013/#732, T-014/#733]
lineage_currentness_refs: [LG_SEQ_FULL]
lineage_currentness_posture: UNKNOWN
integration_target: version/v4.9.0-after-planning-integration
review_policy: required
validation_owner: integrated-dogfood-and-closure-handoff
l3_requirement: integration-plan-required
implementation_admission: NO
jit_branch: true
```

Normative concern/allowed write set/forbidden scope/acceptance are immutable DAG v0.1 blob `4f358ba2b32e01ae17ddcdf970151cf28e44bb3f` section `### T-015`, composed with Frozen DAG v0.2 admission rules.

Full sequential predecessor lineage and all native dependencies must be current. This Task produces integration/dogfood/release evidence handoff only; it cannot issue Version Closure or Release Qualification verdict.
