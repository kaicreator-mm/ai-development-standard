# Review Checklist — T-004 Task Learning Closeout / Template Wiring

Fresh independent Review occurs only after independent concern Validation PASS and is bound to the exact current PR HEAD.

## Exact identity

- [ ] PR targets `version/v4.8.0` and the reviewed HEAD is recorded exactly.
- [ ] Candidate ancestry/currentness is compatible with planning commit produced by Issue #636; no stale JIT pack was silently rebound.
- [ ] Diff is exactly the seven implementation paths in `00bf08ea3ad64f75d77d7cc36655ce7711310086` Task Pack / `MANIFEST.yaml`; no planning-pack file is counted as Builder implementation.

## Scope and ownership

- [ ] T-004 changes adoption/closeout templates/checklists only.
- [ ] `schemas/task-learning-v1.schema.json` and `references/TASK_LEARNING_EVIDENCE_REFERENCE.md` semantics were not changed.
- [ ] `standards/EXECUTION_ARCHITECTURE_STANDARD.md`, scheduler/admission/resource/Availability/Interchange semantics, and tests/runtime implementation were not changed.
- [ ] No Product/Architecture/Task/ADR/Incident/Review/Validation/merge/release authority was transferred to Task Learning.

## Closeout contract

- [ ] Literal `TASK_LEARNING=NONE_MATERIAL` remains an explicit proportional Fast Path.
- [ ] Material learning is expressed via durable refs/digests rather than copied evidence bodies.
- [ ] Stale, ambiguous, or non-current learning cannot be presented as current behavioral proof or silently rebound.
- [ ] The generic templates point to the T-001 evidence contract rather than reimplementing its schema/currentness semantics.
- [ ] Execution Pack template additions are requirement/reference wiring only; T-002 retains Execution Architecture ownership.

## Privacy and evidence

- [ ] No private chain-of-thought, hidden evaluator material, credentials, secrets, or verbose scratch reasoning is required.
- [ ] Builder evidence records exact candidate SHA/tree, exact changed paths, regression results, and its own learning closeout outcome.
- [ ] Independent Validation evidence is actually independent and exact-candidate; Builder evidence was not relabeled as Validation PASS.
- [ ] Review is genuinely fresh and exact-HEAD; any HEAD change invalidates this review result.

## Required regressions

- [ ] `python -B scripts/test_work_item_contract_and_golden_templates.py`
- [ ] `python -B scripts/test_v48_task_learning.py`
- [ ] `python -B scripts/test_pointer_only_trigger_contract.py`
- [ ] `python -B scripts/verify_standard.py`

## Result

Use the repository's current Review protocol. Any P0/P1 scope, ownership, authority, currentness, privacy, or Fast Path violation is blocking. A PASS authorizes only the next controller/merge decision for this task; it is not Version Closure or Release PASS.
