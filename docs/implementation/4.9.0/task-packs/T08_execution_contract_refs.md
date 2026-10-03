# T-008 Task Pack — Work Item / Execution Pack / Dispatch Reference Wiring

Status: **MATERIALIZED TASK PACK — NOT BUILDER READY**

Authority: Frozen Product #709; Frozen L2 #714; Frozen Task DAG v0.2 blob `b9fe0cc7089f64929b4bcf45f7230d950e864db2`; DAG Freeze #719; Issue #727.

```yaml
task_id: T-008
issue: 727
dependencies: [T-007/#726]
lineage_currentness_refs: [LG42_COMPAT, LG48_EXEC]
lineage_currentness_posture: UNKNOWN
integration_target: version/v4.9.0-after-planning-integration
review_policy: required
validation_owner: schema-historical-compatibility-and-claim-binding
l3_requirement: bounded
implementation_admission: NO
jit_branch: true
```

Normative concern/allowed write set/forbidden scope/acceptance are immutable DAG v0.1 blob `4f358ba2b32e01ae17ddcdf970151cf28e44bb3f` section `### T-008`, composed with Frozen DAG v0.2 admission rules.

Only backward-compatible refs may be wired; no duplicate Task scope, Claim authority or gate truth. Dependency and lineage must be current at admission.
