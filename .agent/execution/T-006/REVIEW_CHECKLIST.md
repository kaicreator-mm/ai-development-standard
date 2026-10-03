# T-006 Review Checklist

Use this checklist for independent exact-subject Validation/Review of the future T-006 candidate. It does not authorize either gate by itself.

## Identity and currentness

- [ ] Candidate SHA/tree are explicit and match the reviewed subject.
- [ ] Candidate is derived from a current/rebound `version/v4.8.0` base.
- [ ] #512 native dependencies are current and canonical.
- [ ] Task Pack and L3 blobs match the JIT Execution Pack.
- [ ] Diff is exactly the five-path Builder write set.

## Manifest / family invariants

- [ ] `schemas/task-learning-v1.schema.json` is discoverable exactly once.
- [ ] `schemas/agent-capability-profile-v1.schema.json` is discoverable exactly once.
- [ ] `schemas/agent-capability-evidence-v1.schema.json` is discoverable exactly once.
- [ ] No fourth T-006 v4.8 machine family exists.
- [ ] `schemas/interchange-envelope-v1.schema.json` remains exactly one entry.
- [ ] Existing/historical manifest inventory was not removed or semantically repurposed.
- [ ] Required v4.8 owner references and focused verifiers are discoverable.

## Authority boundaries

- [ ] Registry/discovery/adoption is metadata only.
- [ ] T-006 reference explicitly states `authority_effect=NONE`.
- [ ] T-006 reference explicitly states `gate_effect=NONE`.
- [ ] T-006 reference explicitly states `mutation_authorized=false`.
- [ ] No provider/model label is treated as authorization/correctness/eligibility proof.
- [ ] Capability profile/evidence is not promoted into Validation/Review truth.
- [ ] No sibling semantic owner is restated or rewritten.

## Adoption / progressive disclosure

- [ ] Project adoption remains pinned/currentness-aware.
- [ ] Optional/materiality-driven context is not globally mandatory.
- [ ] Fast Path remains lightweight.
- [ ] `TASK_LEARNING=NONE_MATERIAL` remains a valid path when no material learning exists.
- [ ] Historical projects/payloads do not require destructive rewrite.
- [ ] Migration guidance is additive and keeps Interchange v1.

## v4.7 lineage boundary

- [ ] Current v4.8 tree is not falsely claimed to contain the v4.7 registry/progressive-disclosure implementation.
- [ ] v4.7 predecessor references are treated only as lineage/read-only inputs.
- [ ] T-006 does not invent a replacement semantic-authority store/resolver.

## Verification evidence

- [ ] `python -B scripts/test_v48_registry_adoption.py`
- [ ] `python -B scripts/test_v48_task_learning.py`
- [ ] `python -B scripts/test_v48_agent_capability_profile.py`
- [ ] `python -B scripts/test_v48_agent_capability_evidence.py`
- [ ] `python -B scripts/test_v48_interchange_profile.py`
- [ ] `python -B scripts/test_v48_contract_compatibility.py`
- [ ] `python -B scripts/test_work_item_contract_and_golden_templates.py`
- [ ] `python -B scripts/verify_standard.py`
- [ ] Any NOT_RUN/BLOCKED evidence is explicit and is not upgraded to PASS.

## Gate separation

- [ ] Builder did not self-validate independently.
- [ ] Independent Validation is bound to the exact candidate.
- [ ] Fresh Independent Review begins only after qualifying Validation PASS.
- [ ] Review does not merge; expected-head merge remains a later controller action.
- [ ] T-013 and T-014 remain untouched by this task.
