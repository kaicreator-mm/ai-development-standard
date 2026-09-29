# T11 — Cross-standard Conformance & Dogfood / Closure Inputs

```yaml
task_id: T11
dependencies: [T10]
integration_target: version/v4.3.0
merge_target: version/v4.3.0
allowed_write_set:
  - v4.3 conformance/integration suites
  - dogfood fixtures/evidence under docs/implementation/4.3.0/
  - narrowly required test wiring owned by T11
forbidden_scope:
  - Version Closure or Release Qualification verdict
  - Product/Architecture redesign
  - silent profile/DAG authority mutation
acceptance:
  - required planning/profile shortcut negative families are executable
  - profile-resolution and DAG-mutation regressions are integrated
  - high-capability planning dogfood produces bounded Tasks usable by lower-cost executors without redesign
  - exact subject/test/CI/Review/Validation identities and P0-P3 dispositions are durable
required_gates:
  - integration conformance tests
  - integration Validation
  - Fresh Independent Review
validation_owner: T11
review_policy: required
l3_requirement: docs/implementation/4.3.0/L3_REFERENCE_PACKS.md#t11--conformance--dogfood
agent_freedom: F1_BOUNDED_IMPLEMENTATION
risk: high
executor_suitability: Strong planner plus independent validator/reviewer; lower-cost executor used only as bounded dogfood subject
failure_handling:
  - unavailable real toolchain/agent needed by selected dogfood => exact-scope Validation handoff
  - dogfood needing Product/Architecture redesign => fail/route upward rather than adapt oracle
  - any P0/P1 remains blocking for closure handoff
```

Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`

## Goal
Prove v4.3 integrated semantics reject planning/profile shortcuts and demonstrate a high-capability planner producing bounded Tasks consumable by lower-cost executors without redesign.

## Allowed write-set
- v4.3 conformance/integration suites
- dogfood fixtures/evidence under `docs/implementation/4.3.0/`
- narrowly required test wiring owned by this Task

## Required negative families
- popularity -> justified architecture decision;
- unresolved high-impact UNKNOWN -> implementation freedom;
- file count -> coherent Task boundary;
- atomic shared invariant -> safe parallelism;
- dependency removal -> READY;
- PR stack/cherry-pick -> canonical live DAG;
- DAG mutation without durable reason/authority/impact -> valid mutation;
- Agent-local tool version -> repository profile authority;
- profile mapping -> universal tool/style mandate;
- PROJECT_OVERRIDES -> weakening Frozen/Core authority.

## Positive dogfood
Use v4.3 itself or another non-trivial ADS planning subject. Produce Product/Architecture-bound Task DAG + Task Packs; dispatch at least one bounded lower-cost execution interpretation/evaluation and verify it can act from durable facts without redesigning Product/Architecture. Dogfood may be simulation/evaluation at this Task unless real code execution is required by the selected subject.

## Closure inputs
Record exact subject identities, test/CI/Review/Validation results and all P0/P1/P2/P3 dispositions. No Version Closure or Release Qualification verdict is issued by this Task.

## Failure handling
Unavailable required execution becomes an explicit exact-scope Validation handoff. Dogfood that exposes a Product/Architecture contradiction routes upward; tests/oracles are not weakened to force green. Any unresolved P0/P1 blocks closure handoff.

## Local gate
If chosen dogfood requires unavailable real toolchains/agents, create a dedicated exact-scope Validation handoff. No local environment is assumed by default.

## Reference
`L3_REFERENCE_PACKS.md#t11--conformance--dogfood`.
