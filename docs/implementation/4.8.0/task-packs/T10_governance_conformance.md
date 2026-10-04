# T-010 Task Pack — Task Learning / Evolution Governance Conformance

Status: **FINAL TASK PACK — JIT EXECUTION PACK REQUIRED**

Authority: Frozen Product blob `f26439580e00de6ed8b2e27d732a3095eb566219`; Frozen L2 blob `f88c85454e80101a0fdf56050e21f11a05279841`; Frozen Task DAG R2 commit `d2f18854043c59712c1c9d2518f45843b0ad129c` / blob `21d45c8d1a4ec94621eb8ca6051f21ece8227fdc`; Task Issue #516; native dependencies T-004/#511 + T-005/#509 are DONE and current `blocked_by=0/2`.

```yaml
task_id: T-010
lane: governance-conformance
dependencies: [T-004, T-005]
integration_target: version/v4.8.0
review_policy: required
validation_scope: concern
validation_owner: independent-from-builder
l3_requirement: risk-scaled
agent_freedom_ceiling: F2_ENGINEERING_DISCRETION
jit_branch: true
execution_pack: JIT
```

## Scope

T-010 owns deterministic executable/fixture conformance for the already-merged Task Learning closeout semantics from T-004 and ADS evolution classification/promotion semantics from T-005. It tests the composition of those owners; it does **not** redefine either owner.

Required evidence classes are:

- `NONE_MATERIAL` Fast Path;
- material Task Learning with durable identity/evidence references and bounded confidence layers;
- stale/missing/mutable exact-subject learning retained as historical-only evidence;
- project/Agent/environment/project-specific observations that do not promote to ADS standard change;
- `STANDARD_FRICTION_CANDIDATE` routed only to `NO_CHANGE` or `MORE_EVIDENCE` until an explicit later reclassification;
- `ADS_EVOLUTION_CANDIDATE` routed only to ordinary durable ADS Intake and the normal `Intake -> L1 -> PRD -> L2 -> Task -> Review/Validation` governance chain;
- privacy/publication classification with fail-closed evidence minimization;
- explicit rejection of secrets, credentials, private chain-of-thought and hidden-evaluator/Hidden Validation payload leakage;
- Task Learning evidence, classification, confidence or disposition that never becomes Product/Architecture/Task/ADR/Incident/Review/Validation/merge/release authority.

The Task MUST preserve T-001/T-004 Task Learning ownership, T-005 Development Workflow governance ownership, v4.5 Incident ownership, v4.6 Intent/Skill ownership, and Frozen Product/L2/DAG authority.

## Builder write set

The exact JIT Execution Pack may narrow this Task Pack but MUST NOT broaden it. The authorized implementation surface is one deterministic conformance module:

- `scripts/test_v48_governance_conformance.py`

Scenario fixtures SHOULD be represented deterministically inside that focused module. If implementation proves that a separate fixture/reference artifact is materially necessary, STOP and request an explicit Execution Pack rebind before creating it.

The Builder MUST NOT modify:

- `schemas/task-learning-v1.schema.json`;
- `references/TASK_LEARNING_EVIDENCE_REFERENCE.md`;
- `standards/DEVELOPMENT_WORKFLOW.md`;
- T-004 template/checklist wiring;
- existing T-001/T-004/T-005 tests;
- Product/L2/DAG authority;
- ADR/Incident/Intent/Skill/Review/Validation/Release owners.

Any need to alter owner semantics is `ARCHITECTURE_AMENDMENT_REQUIRED` or an upstream owner repair, not T-010 Builder discretion.

## Acceptance

1. `TASK_LEARNING=NONE_MATERIAL` remains a valid proportional Fast Path and does not require an empty Task Learning object.
2. Material Task Learning is valid only as bounded evidence with durable work/authority/evidence refs; exact-code behavioral claims require canonical immutable exact-subject identity.
3. Missing, mutable, malformed, ambiguous or drifted exact-subject/currentness identity leaves the learning record historical-only and cannot be silently rebound to successor code.
4. `IDENTITY_BOUND`, `BEHAVIOR_SUPPORTED` and `INDEPENDENTLY_CHALLENGED` remain evidence-strength layers only; none creates current Review/Validation PASS or a global scalar score.
5. Task Learning `friction_classification` and `disposition` are routing/evidence metadata only; they cannot self-amend ADS or bypass T-005 governance.
6. `PROJECT_DEFECT`, `AGENT_EXECUTION_DEFECT`, `ENVIRONMENT_OR_TOOL_DEFECT` and `PROJECT_SPECIFIC_REQUIREMENT` route to their existing owners and do not open an ADS standard change.
7. `STANDARD_FRICTION_CANDIDATE` permits `NO_CHANGE` or `MORE_EVIDENCE`; count/score/success-rate/failure-rate/cost/latency/provider/model/heuristic evidence cannot automatically promote it.
8. `ADS_EVOLUTION_CANDIDATE` permits `OPEN_ADS_INTAKE` only as entry to ordinary ADS governance; it is not approval and grants no normative mutation authority.
9. Ambiguous cause/evidence fails toward `MORE_EVIDENCE`, not upward promotion.
10. Publication classification is explicit and separate from evidence strength/promotion status. Missing `PUBLISHABLE` authority fails closed; `PROJECT_PRIVATE`/`RESTRICTED` material is not copied into public standard evidence.
11. Secrets, credentials, private chain-of-thought and hidden-evaluator/Hidden Validation payloads are never publication material, including when an observation is otherwise publishable.
12. Refs/digests and minimized non-sensitive summaries are preferred over copied evidence bodies.
13. Task Learning/governance evidence never substitutes for Frozen Product/L2/DAG, Task, ADR/Incident, Review/Validation, merge or release authority.
14. T-010 adds no new evolution lifecycle/schema, self-amending telemetry loop, promotion threshold, scheduler authority or standard-change authority.
15. Existing T-001/T-004/T-005 focused tests and repository verifier remain green on the exact implementation candidate.

## Required gates

Builder evidence MUST bind exact base, JIT Pack HEAD, candidate HEAD/tree and prove the implementation diff is exactly the one authorized script. Required commands are:

```text
python -B scripts/test_v48_governance_conformance.py
python -B scripts/test_v48_task_learning.py
python -B scripts/test_v48_ads_evolution_governance.py
python -B scripts/test_work_item_contract_and_golden_templates.py
python -B scripts/verify_standard.py
```

Required Validation is independent exact-subject concern Validation over the full learning/classification/privacy negative-oracle matrix. Validation must independently verify that the focused T-010 oracle does not merely restate strings while permitting a contradictory route or authority transition.

Only after qualifying Validation may a genuinely Fresh Independent Review assess the exact current PR HEAD. Builder, Validator and Reviewer identities remain distinct. PR/Task PASS does not imply T-013/T-014 completion, Version Closure or Release Qualification.

## Out of scope / stop conditions

No Task Learning schema/reference semantic change, no Development Workflow owner rewrite, no template/checklist owner repair, no automated evolution lifecycle, no universal numeric promotion rule, no hidden-evaluator exposure, no economic-savings inference and no blanket strong-to-low-cost routing policy.

If current owner artifacts cannot satisfy this Task without semantic mutation, STOP with `ARCHITECTURE_AMENDMENT_REQUIRED` or a clearly identified upstream-owner repair request. Do not weaken a negative oracle to make the conformance suite pass.
