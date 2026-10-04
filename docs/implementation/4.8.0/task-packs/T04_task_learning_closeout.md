# T-004 Task Pack — Task Learning Closeout / Template Wiring

Status: **JIT-PLANNED — Builder admission is owned by Issue #636 terminal currentness**

Authority: Frozen Product blob `f26439580e00de6ed8b2e27d732a3095eb566219` + Frozen L2 blob `f88c85454e80101a0fdf56050e21f11a05279841` + Frozen DAG R1 blob `72dfeee93c092296004c7083b71fdd877d7f1b34`; Task Issue #511. T-001 owns Task Learning evidence semantics; T-002 owns Execution Architecture semantics.

```yaml
task_id: T-004
repository: kaicreator-mm/ai-development-standard
version: 4.8.0
integration_target: version/v4.8.0
merge_target: version/v4.8.0
task_pack_ref: docs/implementation/4.8.0/task-packs/T04_task_learning_closeout.md
dependencies: [T-001, T-002]
allowed_write_set:
  - templates/task-pack.md
  - templates/task-issue.md
  - templates/implementation-pr.md
  - templates/final-closeout.md
  - checklists/pr-review.md
  - templates/execution-pack/EXECUTION_CONTRACT.md
  - templates/execution-pack/REVIEW_CHECKLIST.md
forbidden_scope:
  - schemas/task-learning-v1.schema.json
  - references/TASK_LEARNING_EVIDENCE_REFERENCE.md semantic redefinition
  - standards/EXECUTION_ARCHITECTURE_STANDARD.md
  - scripts/tests/schema/runtime implementation changes
  - ADR/Incident/Product/Architecture/Review/Validation authority redefinition
  - scheduler/admission/resource/availability/interchange semantics
acceptance:
  - applicable task/PR/closeout templates expose an explicit Task Learning closeout result that can be either TASK_LEARNING=NONE_MATERIAL or durable material-learning reference(s)
  - material-learning wiring prefers durable evidence refs/digests over copied evidence bodies and delegates semantic validation to the T-001 Task Learning contract
  - stale or non-current learning remains historical evidence and is never silently rebound or presented as current behavioral proof
  - Task Learning never substitutes for Product/Architecture/Task/ADR/Incident/Review/Validation/merge/release authority
  - no template or checklist requires private chain-of-thought, hidden evaluator material, secrets, or verbose scratch reasoning
  - the NONE_MATERIAL Fast Path remains proportional and does not require an empty task-learning object
  - Execution Pack and review wiring carry only closeout requirements/references; they do not acquire T-002 Execution Architecture semantic ownership
required_gates:
  - independent concern Validation on the exact implementation candidate
  - fresh independent Review on the exact current PR HEAD after Validation PASS
validation_scope: concern
validation_owner: independent-from-builder
review_policy: required
l3_requirement: docs/implementation/4.8.0/L3_REFERENCE_PACKS.md#t-004--task-learning-closeout-wiring
agent_freedom: F2_ENGINEERING_DISCRETION
jit_branch: true
execution_pack: JIT
```

## Why

T-001 already defines the evidence object and `TASK_LEARNING=NONE_MATERIAL` Fast Path, while T-002 owns the execution/currentness architecture. T-004 closes the adoption gap only: ordinary ADS work-item, PR, review, final-closeout and Execution Pack surfaces must make the learning outcome visible and reviewable without copying semantic ownership into templates.

## Acceptance detail

1. **Two explicit closeout paths.** A completed task can record either literal `TASK_LEARNING=NONE_MATERIAL` or one-or-more durable Task Learning evidence references. Templates must not force ceremony when no reusable learning exists.
2. **Reference-first material path.** Material learning uses references/digests and points consumers to `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`; it does not duplicate schema semantics or evidence bodies.
3. **Fail-closed currentness.** If a referenced learning record cannot establish the exact subject/currentness required by T-001, templates/checklists treat it as historical evidence only. No branch/tag/repository-name shortcut becomes current proof.
4. **Authority separation.** Learning can preserve implementation rationale and reusable constraints but cannot replace Frozen Product/L2/DAG, Task acceptance, ADR/Incident authority, independent Review/Validation, merge decision, or Release Qualification.
5. **Privacy and proportionality.** No private chain-of-thought, hidden evaluator content, credentials, secrets, or unnecessary copied logs are requested. `NONE_MATERIAL` stays a one-line Fast Path.
6. **Execution Pack boundary.** `templates/execution-pack/EXECUTION_CONTRACT.md` and `templates/execution-pack/REVIEW_CHECKLIST.md` may require/report the closeout outcome, but must not redefine JIT admission, scheduling, resource ownership, or currentness semantics owned by T-002.
7. **Bounded implementation.** The implementation PR changes exactly the seven declared template/checklist paths; any need for schema/reference/standard/test/runtime changes is a planning defect or upstream repair request, not Builder discretion.

## Required Validation

Independent Validation must bind to the exact implementation candidate SHA and verify:

```text
python -B scripts/test_work_item_contract_and_golden_templates.py
python -B scripts/test_v48_task_learning.py
python -B scripts/test_pointer_only_trigger_contract.py
python -B scripts/verify_standard.py
```

In addition, Validation must inspect the seven-file diff for both closeout paths, reference-first evidence, stale/currentness fail-closed behavior, authority separation, no-private-CoT/privacy language, and absence of T-002 semantic changes. A fresh independent exact-HEAD Review is required after Validation PASS.

## Out of scope

No Task Learning schema/reference semantic change, no Execution Architecture change, no new scheduler/admission/resource/Availability/Interchange behavior, no change to ADR/Incident/Product/Architecture authority, no implementation of T-005 evolution governance, and no Version Closure or Release Qualification. Contradictions route upward as `TASK_PACK_DEFECT`, `ARCHITECTURE_CONTRADICTION`, or `EXECUTION_PACK_INVALID`; they are never silently resolved.
