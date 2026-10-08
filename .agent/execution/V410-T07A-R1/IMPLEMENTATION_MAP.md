# V410-T07A R1 implementation map — owner mapping, projection structure, JIT decisions

## Owner boundary (REUSE_FIRST_OWNER_MAP, #862@6003300393 — rebound, not rediscovered)

- **RELEASE_STANDARD** owns Candidate/Freeze/Hidden/Release Qualification authority and §11 gate applicability. The projection never emits READY|CONDITIONAL|BLOCKED|FAIL-style Release verdicts.
- **VALIDATION_STANDARD** owns exact-subject evidence meaning — including the only legal NOT_APPLICABLE. `concern` Validation is this task's validation scope.
- **DEVELOPMENT_WORKFLOW** owns lifecycle/gate routing (repair routing, currentness rules).
- **Frozen Product #837 PRD §18/§19** owns requirement meaning and acceptance obligations (PRD.md blob `b0b9906035eee253aad4bff0274d3d4c8f90b9db`). The index restates no requirement text as index-owned meaning; rows carry immutable `prd_ref` anchors only.
- **EXECUTION_ARCHITECTURE_STANDARD** owns claim_key/admission_generation/compatibility_group/execution_environment semantics — provenance producer only.
- **T06A/T06B** provided owner discovery + machine/projection surfaces (integrated at this base); they hold no Product acceptance authority either.

## Deliverable topology

1. `docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md` — the acceptance-evidence index/projection:
   - authority header (`PROJECTION_ONLY=true; authorizes_execution=false; authorizes_release_qualification=false; verdict_authority=LATER_GATES_AND_OWNING_STANDARDS_ONLY`) + rebind subject identity (base SHA `0518202c…` / tree `75566c46…`);
   - exactly 8 requirement rows R1/R2/R3/R4/R6/R7/R11/R12 in one fenced JSON machine record (ROW_SCHEMA per #862@6013713353: row_id, requirement_id, prd_ref, canonical_owner, evidence_producers[{producer_kind, durable_ref, exact_subject_binding, blob_identity?}], current_exact_subject, currentness_rule, blocker_projection, missing_evidence_description, route_to_owner, rejected_provenance, adoption_path, authority_note);
   - `closure_blocker_inputs` section distinct from requirement rows: BLK-900 (#900 campaign, EVENT_BOUND, OPEN), BLK-865 (#865 V410-V01, closure-input Validation, NOT_YET_DISPATCHABLE until T08A), BLK-GATES (§19.2 gate-family applicability → RELEASE_STANDARD §11 decision records), BLK-FREEZE-DECISION (ADS_CORE_FEATURE_FREEZE_ELIGIBLE → Product authority §1.1 via the T07B decision-support path);
   - negative rules (BLOCKER_RULES 1-7) and a rejected-evidence provenance appendix.
2. `scripts/test_v410_t07a_acceptance_projection.py` — parses the record block fail-closed, asserts P1-P5 completeness on the real document and N-case negatives via row-validator mutants.
3. This six-core pack (`.agent/execution/V410-T07A-R1/`), mirroring the V410-T06B-R1 family convention with the L3 seed embedded in EXECUTION_CONTRACT.md.

## Row-to-producer binding (executed at the rebind subject)

| Row | Current producers (binding / blob at 0518202c) | End-to-end owner still pending |
| --- | --- | --- |
| R1 | PRODUCT_FREEZE.md (DURABLE_STATIC 6b5bbd34), PRODUCT_THAW_R1.md (DURABLE_STATIC 608aa7c5), TASK_PACKS_R1.md (DURABLE_STATIC 3300f849), test_v410_t01b_product_projections.py (CANDIDATE_BOUND a27e65e5) | V410-T08A falsification case + V410-V01 closure Validation |
| R2 | references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md (CANDIDATE_BOUND b5d0b09a), test_v410_owner_convergence.py (CANDIDATE_BOUND d2347fca — rebound by the R2 successor-aware guard repair; was ec895815 at 0518202c), PRODUCT_FREEZE.md (DURABLE_STATIC 6b5bbd34) | closure-time no-contradictory-authority evidence (T08A + RELEASE_STANDARD closure) |
| R3 | test_v410_t02a_collaboration_control.py (CANDIDATE_BOUND 850093ca), test_v410_t02b_machine_projection.py (CANDIDATE_BOUND 4b7c043d), test_v410_t06b_multi_dispatch_conformance.py (CANDIDATE_BOUND 2b236a5e) | V410-T08A fresh-observer reconstruction case |
| R4 | PRODUCT_THAW_R1.md (DURABLE_STATIC 608aa7c5), test_v410_stage1_lifecycle_contracts.py (CANDIDATE_BOUND dd5b2b56), test_v410_t03a_implementation_quality.py (CANDIDATE_BOUND 23933868), dispatch chain #862@6052647951/@6052650587/@6052653911 (EVENT_BOUND, provenance-only instance) | V410-T08A authority-sensitive human-control case |
| R6 | test_v410_t04a_gate_repair_routing.py (CANDIDATE_BOUND aa46924d), test_v410_t04b_review_currentness.py (CANDIDATE_BOUND d67a2ab9), test_v410_t05a_shared_code_safety.py (CANDIDATE_BOUND f24ebce7) | V410-T08A gate-reduction/repair-convergence case |
| R7 | REFINED_TASK_DAG_FREEZE_R1.md (DURABLE_STATIC ba9cc332), EXECUTION_DAG_MATERIALIZATION_R1.md (DURABLE_STATIC e184941d), TASK_DAG.md (DURABLE_STATIC 3b8a0e4f), TASK_PACKS_R1.md (DURABLE_STATIC 3300f849), test_v410_t06b_multi_dispatch_conformance.py (CANDIDATE_BOUND 2b236a5e) | V410-T08A split-or-atomic falsification case |
| R11 | test_v410_t06b_core_inventory.py (CANDIDATE_BOUND bc763552), test_v410_t06b_multi_dispatch_conformance.py (CANDIDATE_BOUND 2b236a5e), test_v410_t02b_machine_projection.py (CANDIDATE_BOUND 4b7c043d), references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md (CANDIDATE_BOUND b5d0b09a) | V410-T08A whole-project visible conformance + V410-V01 |
| R12 | PRODUCT_FREEZE.md (DURABLE_STATIC 6b5bbd34), L2_FREEZE.md (DURABLE_STATIC 0a3ed1bf), REFINED_TASK_DAG_FREEZE_R1.md (DURABLE_STATIC ba9cc332), references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md (CANDIDATE_BOUND b5d0b09a) | T07B freeze-decision record path + T08A fresh-adopter/successor-non-inheritance case |

Every row is `blocker_projection=UNRESOLVED` at this subject with `current_exact_subject=UNBOUND_UNTIL_T08A_INTEGRATION` — honest per PRD §19.3: the end-to-end falsification owners have not yet produced their evidence, so no row may claim current acceptance. Currentness at this subject means "producer exists, byte-identical to the recorded blob identity, and durably reconstructible" — never a PASS.

## JIT decisions

- Checklist mutation: declined (DISP-NO-CHECKLIST-MUTATION in TEST_MATRIX.yaml).
- Manifest registration: declined — `scripts/verify_standard.py` requires none, and the `test_v48_registry_adoption.py` RA exact-set guards forbid unlisted additions (DISP-NO-MANIFEST-MUTATION).
- Retained prep-branch artifact (`task/v4.10.0-v410-t07a-local-evidence-inventory-r1@a248c3a`, `scripts/test_v410_t07a_evidence_inventory.py`): reference-only; this suite is written fresh; the projection records it in rejected provenance and the focused suite asserts its absence from the checkout.
- L1_PRODUCT_EVIDENCE.md (blob `d810af79…`, SUPERSEDED): historical lineage evidence, admitted ONLY in rejected_provenance rows — never a current producer.

## Boundary

No T06B-owned surface edits, no standards edits, no schema/template/verifier changes, no historical event migration, no Release/Validation/Review/Freeze authority. The Builder does not merge.
