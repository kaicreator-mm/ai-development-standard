# T-003 Task Pack — Assurance Plan and Independence Axes

Issue: #75
Parent version: #72
Baseline: `638e0bedb3ce8ab50ae045b3f7cb29a3f179e2f8`
Review Policy: required
Risk: high
Validation scope: concern
Agent freedom: F1_BOUNDED_IMPLEMENTATION

## Goal

Define the logical Operation Assurance Plan and machine-oriented independence axes without creating a parallel lifecycle or weakening Validation/Review authority.

## Allowed changes

- `docs/implementation/4.0.0/ASSURANCE_PLAN.md`
- this Task Pack
- T-003 pointer/metadata in `docs/implementation/4.0.0/TASK_PACKS.json`

## Forbidden changes

- schemas or verifier implementation;
- event-v2/event-v3 changes;
- reducer/workflow implementation;
- T-004 finding/conflict algorithm details beyond non-negotiable boundaries;
- released Validation/Release authority changes.

## Tests / review oracle

A reviewer must be able to prove:

1. Policy, Mode, Coverage, Independence and Aggregation are distinct;
2. Assurance is a DAG/partial order rather than a fixed pipeline;
3. context/model/executor/evidence independence are orthogonal;
4. model diversity cannot substitute for executable evidence;
5. actual Validation PASS remains owned by `VALIDATION_STANDARD.md`;
6. ordinary low-risk Tasks can use a minimal plan without ceremonial review;
7. named profiles expand to underlying dimensions and cannot hide them;
8. no parallel Assurance state machine is created;
9. subject identity/staleness remains governed by owning standards;
10. `MODEL_USAGE_POLICY` model-strength routing and model-diversity assurance remain separate authorities.

## Failure handling

- authority ambiguity -> BLOCKED / route to #72 architecture authority;
- conflict with v3.4 Validation/Review semantics -> CHANGES_REQUESTED;
- runtime fact not provable statically -> request appropriate Validation rather than infer PASS.

## Completion

Repository verifier PASS on final exact HEAD + Fresh Independent Review PASS on the same HEAD + focused merge to `version/v4.0.0`.
