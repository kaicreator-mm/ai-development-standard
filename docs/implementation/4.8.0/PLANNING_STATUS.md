# v4.8.0 Planning Status

Status: **PRODUCT FROZEN — L2 FROZEN — TASK DAG R1 FROZEN — TASK ISSUES 16/16 MATERIALIZED / NATIVE DAG + TASK PACKS PENDING — IMPLEMENTATION NOT READY**

## Currentness semantics

This file is descriptive planning metadata. It MUST NOT claim an embedded commit SHA/tree is the live current planning subject because editing this file changes that subject. Exact review/freeze/checkpoint subjects are bound through durable GitHub facts plus immutable blob identities.

## Frozen Product / Architecture Authority

```text
PRODUCT_FREEZE_BLOB=8720264f56a23e352b347dd74df966b9416c9129
FROZEN_PRD_BLOB=f26439580e00de6ed8b2e27d732a3095eb566219
PRODUCT_REVIEW=#490@5926142930 PASS
FROZEN_L2_BLOB=f88c85454e80101a0fdf56050e21f11a05279841
L2_FREEZE_BLOB=f495535b6a16c30b3043fbacedb19cc8be01d541
ARCH_REVIEW=#502@5927313354 PASS
DOGFOOD_BASIS=#469@5925124956
```

Exactly three new default machine families remain Frozen: Task Learning Evidence v1, Logical Agent Capability Profile v1, Agent Capability Evidence v1. Existing Interchange and runner/host/resource owners are reused; Availability is derived; hard eligibility precedes ranking; work claim + all required scarce-resource/capacity bindings share one all-or-none composite admission linearization point.

## Frozen Task DAG R1

Historical R0 commit `0a4607e857c3971b9eff6092de46f67ba0a698f5` / blob `16ff752ba9c42ee037bb6939c4beb7d235f87cd6` is superseded for execution planning after #504 audit `5927557494` found T-001 improperly combined three independent machine-contract concerns.

Canonical R1:

```text
TASK_DAG_COMMIT=634dd746cd16da970bb01822a1b6c59714c52429
TASK_DAG_BLOB=72dfeee93c092296004c7083b71fdd877d7f1b34
TASK_DAG_CONTROLLER_TERMINAL=#504@5927716800
TASK_COUNT=16
ROOT_TASKS=T-001,T-015,T-016,T-005
PRE_CLOSURE_JOIN=T-014
EXPECTED_NATIVE_EDGES=38
```

R1 preserves T-002..T-014 stable identities, narrows T-001 to Task Learning Evidence, and adds T-015 Logical Agent Capability Profile + T-016 Agent Capability Evidence as independent contract concerns. This restores one-concern-per-PR and safe capability-based root parallelism while retaining T-002 as the single semantic owner lane for shared `EXECUTION_ARCHITECTURE_STANDARD.md` changes.

## Canonical Task map

```text
T-001 #507   Task Learning Evidence Contract
T-015 #522   Logical Agent Capability Profile Contract
T-016 #524   Agent Capability Evidence Contract
T-003 #508   Existing Interchange v1 Profile / Adapter Mapping
T-005 #509   ADS Evolution Governance / Intake
T-002 #510   Execution Architecture Core
T-004 #511   Task Learning Closeout / Template Wiring
T-006 #512   Registry / Discoverability / Adoption Wiring
T-007 #513   Contract / Historical Compatibility Conformance
T-008 #514   Eligibility / Composite Resource Admission Conformance
T-009 #515   Interchange Replay / Restart Conformance
T-010 #516   Task Learning / Evolution Governance Conformance
T-011 #517   Heterogeneous Multi-Agent / Resource / Transport Dogfood
T-012 #518   #469 Task-Class / Bounded-Agent Dogfood
T-013 #519   Cross-Project ADS Evolution Dogfood
T-014 #520   Integrated Convergence / Version Closure Inputs
```

Duplicate T-015 #523 is closed and has no Task Pack/L3/native dependency/JIT/Builder authority. All canonical Task Issues remain `PLANNED / NOT_BUILDER_READY`. No task branch has been authorized or pre-created.

## Native execution DAG

GitHub Issue Dependencies become the canonical live execution DAG only after materialization/read-back.

Historical R0 writer handoff #521 is closed superseded and MUST NOT be executed. Current R1 writer/read-back handoff is **#525** and MUST prove:

```text
TASK_ISSUES=16/16
EXPECTED_EDGES=38
OBSERVED_EDGES=38
MISSING_EDGES=none
EXTRA_EDGES=none
CYCLE=NO
ROOTS=#507,#522,#524,#509
PRE_CLOSURE_JOIN=#520
DUPLICATE_T015_523=EXCLUDED
TASK_READY_MUTATION=NOT_PERFORMED
```

Until #525 PASS, Issue-body dependency lists are descriptive only and roots are not Builder-ready.

## Task Pack / L3 posture

Task Packs and required L3/reference packs are the next Stage 2 planning checkpoint. They MUST bind R1 blob `72dfeee93c092296004c7083b71fdd877d7f1b34`, never historical R0.

- every canonical Task T-001..T-016 receives a Task Pack appropriate to its concern;
- T-001/T-015/T-016/T-002/T-003/T-005/T-014 require high-capability semantic/reference guidance before bounded Builder dispatch;
- T-012 requires risk-scaled L3 plus a later JIT exact-base Execution Pack before bounded/low-cost Builder execution;
- T-011/T-013 require explicit evidence matrices and real-vs-synthetic boundaries;
- packs/L3 cannot expand Frozen Product/L2/DAG or manufacture Validation/Review/Release truth.

Native dependency materialization and Task Pack authoring may proceed as separate planning actions, but **Builder READY requires both** plus planning integration, current exact version baseline, resource/currentness and role/independence gates.

## Dogfood evidence boundary

```text
ACTUAL_LOW_COST_IMPLEMENTATION_OUTCOME=PARTIALLY_MEASURED_POSITIVE_EXECUTION
ECONOMIC_SAVINGS=NOT_MEASURED
BLANKET_STRONG_TO_LOW_COST_RULE=NOT_SUPPORTED
STANDARD_CHANGE=NOT_AUTHORIZED
PROPOSED_DISPOSITION=MORE_EVIDENCE
```

Provider/model identity remains provenance. No economic/routing conclusion may be promoted without declared comparable evidence and required gates.

## Current gates

- Product: **FROZEN**;
- L2 Architecture: **FROZEN**;
- Task DAG R1: **FROZEN**;
- canonical Task Issues: **MATERIALIZED 16/16 / PLANNED**;
- native Issue Dependency graph: **PENDING #525**;
- Task Packs / required L3: **PENDING**;
- planning integration / `version/v4.8.0`: **NOT YET ESTABLISHED**;
- Builder dispatch / task branches: **NOT AUTHORIZED**;
- implementation: **NOT STARTED**.

## Required sequence

```text
Frozen Product + Frozen L2 + Frozen Task DAG R1
-> #525 native dependency materialization/read-back
+ Task Packs / required L3/reference packs
-> planning checkpoint currentness/review as required
-> canonical planning integration
-> establish version/v4.8.0 exact baseline
-> Controller recomputes READY roots
-> JIT task branch + exact-base Execution Pack
-> Builder -> Validation -> required Fresh Review -> per-concern merge
-> T-014 closure inputs
-> Version Closure / Release Qualification
```

No Task may infer READY from being a DAG root alone.