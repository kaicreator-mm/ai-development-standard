# T11 — Cross-standard Conformance & Dogfood / Closure Inputs

Depends on: T10
Frozen Product: `68ce6fd157a0b932651c42f67627e9dc0b8880c3`
Frozen L2: `b90f9b698edcc426051a93569634fcef7a74e644`
Review: required | Validation: integration/closure-input | Freedom: `F1_BOUNDED_IMPLEMENTATION`

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

## Local gate
If chosen dogfood requires unavailable real toolchains/agents, create a dedicated exact-scope Validation handoff. No local environment is assumed by default.

## Reference
`L3_REFERENCE_PACKS.md#t11--conformance--dogfood`.