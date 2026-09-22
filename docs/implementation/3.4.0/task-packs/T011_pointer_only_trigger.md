# T-011 — Pointer-only ChatGPT Web task trigger enforcement

Issue: #64  
Parent version: #47  
Closure: #57  
Integration target: `version/v3.4.0`  
Materialization baseline: `f90669abda9fab35f4759469f1369ac55ba702fe`  
Review Policy: `required`  
Validation scope: `concern`  
Agent freedom: `F1_BOUNDED_IMPLEMENTATION`

## Goal

Eliminate prompt-contract drift by making user-visible ChatGPT Web task triggers pointer-only and requiring all task-specific execution instructions to be durable in GitHub before invocation.

## Dependencies

- T-009 complete.
- This is a post-closure corrective task discovered after the first T-010 closure.
- Reopened T-010 depends on T-011 merge before fresh final closure.

## Allowed changes

- `standards/ISSUE_FIRST_TASK_TRIGGER.md`
- `standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md`
- compatible clarification in existing Web/interaction/execution-pack authority where necessary
- relevant `templates/**` and repository-owned role bootstrap material
- `scripts/**` conformance regression
- `.github/workflows/verify-standard.yml`
- `standard-manifest.json`
- `docs/implementation/3.4.0/**` corrective-task / closure bookkeeping

## Forbidden changes

- introducing a second Prompt lifecycle or prompt authority;
- moving Task/Execution Pack/Dispatch semantics into chat;
- weakening exact-SHA Validation, Review, Release Qualification, or authority ordering;
- unrelated v3.4 behavior changes.

## Required invariants

```text
GitHub Issue + referenced repository authority = complete executable task contract
user-visible ChatGPT Web trigger = pointer only
No durable contract -> no trigger
No Issue update -> no new task-specific instruction in chat
```

Allowed trigger identity is limited to repository, Issue/PR, optional role, and optional dispatch id when needed for disambiguation.

Task-specific SHA/branch/scope/write-set/acceptance/commands/gates/review/failure/closeout/evidence instructions MUST NOT be emitted in the user-visible trigger.

## Required validation

- `python scripts/verify_standard.py`
- `python scripts/test_pointer_only_trigger_contract.py`
- existing v3.3/v3.4 verifier chain through `verify-standard`
- exact-head GitHub Actions `verify-standard`
- required Independent Review on the exact T-011 PR HEAD

## Acceptance

- Issue-first trigger authority uses MUST-level durable-contract and pointer-only semantics.
- Incomplete Issue => update/materialize GitHub first, no expanded chat prompt.
- Changed task requirement => persist first; the copied trigger remains the same short pointer form.
- Local Agent Handoff uses the same invariant.
- Execution Pack `LOCAL_AGENT_PROMPT.md`, if retained, is explicitly durable repository material and not the user-visible trigger.
- Automated regression rejects old permissive wording and representative long task-specific trigger payloads.
- Existing Web/Interaction authority remains GitHub-first and no second lifecycle is introduced.

## Completion

T-011 is complete only after implementation, full required validation, required Independent Review PASS, and merge to `version/v3.4.0`. The resulting version candidate then returns to T-010/#57 for fresh closure.