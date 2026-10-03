# T-003 Task Pack — Authority / State Registry Integration

Status: **MATERIALIZED TASK PACK — NOT BUILDER READY**

Authority: Frozen Product #709; Frozen L2 #714; Frozen Task DAG v0.2 blob `b9fe0cc7089f64929b4bcf45f7230d950e864db2`; DAG Freeze #719; Issue #722.

```yaml
task_id: T-003
issue: 722
dependencies: [T-002/#721]
lineage_currentness_refs: [LG47_REGISTRY]
lineage_currentness_posture: UNKNOWN
integration_target: version/v4.9.0-after-planning-integration
review_policy: required
validation_owner: registry-and-forbidden-inference
l3_requirement: bounded
implementation_admission: NO
jit_branch: true
```

Normative concern/allowed write set/forbidden scope/acceptance are the exact immutable DAG v0.1 blob `4f358ba2b32e01ae17ddcdf970151cf28e44bb3f` section `### T-003`, composed with Frozen DAG v0.2 admission rules.

Before Builder dispatch: native dependency edge hydrated/satisfied; exact v4.7 Authority/Applicability + State registry identities current; Task Pack/L3/Assurance/admission current. Missing/stale lineage => `WAITING_LINEAGE`.
