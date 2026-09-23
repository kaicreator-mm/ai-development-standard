# T-009 Task Pack — Schemas, Golden/Forbidden Examples and Verifier Regressions

Task: T-009 / Issue #81
Parent version: #72
Dependencies: T-007 / #79 + T-008 / #80
JIT baseline: `version/v4.0.0@13ff64905c2828cc1bd3c340cc30a1fd12e798f5`
Branch: `task/v4.0.0-t009-machine-contracts`
Review Policy: required
Risk: high
Validation scope: concern
Agent freedom: F1_BOUNDED_IMPLEMENTATION

## Goal

Implement the minimum machine-readable v4 Operation/Assurance/interchange contracts and executable semantic regressions required to make the frozen T-001..T-008 architecture fail closed without creating a second workflow/event protocol.

## Frozen inputs

- #72 / #81;
- merged T-001..T-008 v4 artifacts;
- `schemas/agent-event-v2.schema.json` and current v3.4 machine contracts;
- `scripts/test_protocol_schemas.py` dependency-free JSON-Schema subset;
- downstream obligations recorded on #81 from #92, #110, #113, #115 and #117.

## Allowed write set

- `schemas/operation-v1.schema.json`
- `schemas/operation-binding-v1.schema.json`
- `schemas/assurance-plan-v1.schema.json`
- `schemas/review-finding-v1.schema.json`
- `schemas/review-aggregation-v1.schema.json`
- `schemas/interchange-envelope-v1.schema.json`
- `scripts/v40_rules.py`
- `scripts/test_v40_operation_contracts.py`
- `templates/golden/V4_OPERATION_ASSURANCE_EXAMPLES.json`
- `standard-manifest.json`
- `.github/workflows/verify-standard.yml`
- `docs/implementation/4.0.0/TASK_PACKS.json` (T-009 pointer only)
- this Task Pack.

## Required machine invariants

1. `project-defined` subject identity may extend but never weaken owning exact-SHA / Validation Tuple / candidate binding.
2. Operation Binding is explicitly correlation-only/non-authoritative relative to workflow/Gate/dispatch/candidate/release truth.
3. event-v2 remains the existing event protocol; logical interchange families do not become new event-v2 enum values and no event-v3 is introduced without a concrete break.
4. Assurance keeps policy/mode/coverage/independence/aggregation distinct; majority voting for correctness is forbidden.
5. model-diverse-adversarial assurance requires durable blind first-pass evidence; collaboration cannot retain an independence claim.
6. Review findings remain durable: aggregation is finding-union + blocker-dominance, cannot silently drop findings, and unresolved valid blockers cannot be voted away.
7. Review aggregate judgment and requested workflow route are separate machine fields.
8. P2 requires durable explicit disposition; P3 requires explicit disposition when the selected policy requires it.
9. Semantic controller-effect idempotency uses deterministic normalized JSON over controller kind + owning authority + subject identity + expected precondition + intended effect target; transport/exchange identity is excluded from the semantic key.
10. Fast Path is machine-bounded and escalates for public contract, architecture, security/trust, migration/recovery, concurrency/exactly-once, cross-repo/authority, unknown validation, unresolved blocker, model-diverse/coherence, nontrivial Execution Pack, or material dependency-graph conditions.
11. Validation PASS semantic guard requires successful actual command evidence and cannot survive HEAD/BASE/MERGE-RESULT/CANDIDATE drift by assertion.
12. Candidate Freeze and Release Qualification remain distinct and release READY stays bound to the frozen candidate SHA/tree.
13. Hidden shared metadata uses canonical `pack_identity / pack_revision / pack_checksum / candidate_sha` vocabulary and rejects private fixture/scenario/oracle payload leakage.
14. `WORK_ITEM_OPERATION_INTEGRATION.md` Fast Path semantics are included in the machine/golden design.

## Golden / Forbidden coverage

Positive and adversarial examples MUST cover at least:

- non-weakening project-defined identity;
- correlation-only operation binding;
- additive event-v2 correlation without enum repurposing;
- valid model-diverse blind review;
- majority-vote rejection;
- missing blind-pass rejection;
- P2/P3 finding disposition and silent-drop rejection;
- unresolved blocker preventing PASS;
- judgment/route orthogonality;
- stable semantic-action key across transport retries;
- Fast Path escalation;
- Validation PASS execution/drift guard;
- candidate/release identity binding;
- Hidden canonical metadata and leak rejection.

## Validation

Required authoritative concern validation:

```text
python scripts/verify_standard.py
python scripts/test_verify_standard.py
python scripts/test_verify_project_standard.py
python scripts/test_project_execution_profile.py
python scripts/test_protocol_schemas.py
python scripts/test_v33_lifecycle_contracts.py
python scripts/test_v33_semantic_regressions.py
python scripts/test_v34_lifecycle_contracts.py
python scripts/test_v34_review_repairs.py
python scripts/test_v40_operation_contracts.py
python scripts/test_pointer_only_trigger_contract.py
python scripts/test_work_item_contract_and_golden_templates.py
python scripts/verify_event_writer_surfaces.py
python scripts/test_execution_architecture.py
python scripts/verify_runner_capability_reference.py
```

GitHub Actions `verify-standard` is an accepted repository-real clean executor for this concern when it runs on the exact PR HEAD. Static inspection alone is not PASS.

## Forbidden scope

- no event-v3;
- no new third-party dependency;
- no second reducer/workflow/DAG;
- no rewrite of existing v3.4 event semantics merely to carry v4 correlation;
- no T-010 reference-flow/self-dogfood implementation;
- no T-011 migration guidance;
- no actual Candidate Freeze, Hidden execution, Release Qualification or repository integration;
- no weakening of T-001..T-008 frozen invariants.

## Completion

Implementation on exact branch HEAD → repository-real full verifier + focused v4 regression PASS → required Fresh Independent Review PASS → merge to `version/v4.0.0`.
