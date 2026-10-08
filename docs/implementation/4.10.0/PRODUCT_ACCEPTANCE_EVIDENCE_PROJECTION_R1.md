# v4.10.0 Product Acceptance Evidence Projection R1

Status: **PROJECTION_ONLY=true; authorizes_execution=false; authorizes_release_qualification=false; verdict_authority=LATER_GATES_AND_OWNING_STANDARDS_ONLY**

Authority: Frozen Product #837 (`docs/implementation/4.10.0/PRD.md` v0.4 blob `b0b9906035eee253aad4bff0274d3d4c8f90b9db` — §1.1/§2/§9/§13/§16/§18/§19/§20); Frozen L2 #842 (`L2_FREEZE.md`, review #839); refined DAG Freeze #848 (`REFINED_TASK_DAG_FREEZE_R1.md`, review #847) + `EXECUTION_DAG_MATERIALIZATION_R1.md` (#849); Task Pack R1 §V410-T07A (`TASK_PACKS_R1.md` blob `3300f8494ecb2120d96fff520cd09270b538344b`); integrated predecessor V410-T06B (#861) at the rebind subject below.

Rebind subject (exact candidate identity of this projection): base SHA `0518202c715dcf91784a694bdf4a8eeeaeb16ab6`, tree `75566c464505386fedffde803e05e3e726922434` — the merged #861 integration tip. Every producer blob identity in this record was re-verified at that exact tree (`git rev-parse 0518202c…:<path>`) during the V410-T07A JIT; none was inherited from preview facts.

This artifact is an **acceptance-evidence index/projection**. It maps each active Product requirement's PRD §19 evidence obligation to durable evidence producers with exact-subject/currentness identity and projects the visible release-blocker state. It points to evidence; it never manufactures an acceptance result, never redefines a Product requirement, never issues a Version Closure / Release Qualification / `ADS_CORE_FEATURE_FREEZE_ELIGIBLE` assertion, and never creates a second Release verdict or state machine. Release authority stays with RELEASE_STANDARD; exact-subject evidence meaning (including the only legal NOT_APPLICABLE) stays with VALIDATION_STANDARD; lifecycle/gate routing stays with DEVELOPMENT_WORKFLOW; requirement meaning stays with the Frozen Product.

## Negative rules (binding on this projection)

1. **Exact-subject binding:** every CANDIDATE_BOUND producer names a blob identity; candidate drift or thaw renders the row historical (reachable but non-current) and reopens `UNRESOLVED`. No verdict or evidence ever transfers to a successor exact subject (PRD §16).
2. **Fail-closed routing:** missing or ambiguous owner/evidence yields an explicit `UNRESOLVED` row with `route_to_owner` — never a guess and never a convenience reclassification from cost, docs-only label, file count, speed, or model confidence; UNKNOWN gate applicability routes per RELEASE_STANDARD §11.4 to the stronger legal path or BLOCKED.
3. **No cross-layer manufacture:** CI / Task / PR results, machine-conformance results, scheduler dispatch/admission/claim events, Validation or Review outcomes on other gate families, provider/model votes, and multi-lane duplicate evidence are provenance only; they never upgrade a row beyond `EVIDENCE_CURRENT` and never by themselves clear any §19.3 blocker. A test suite's existence or registration is not an acceptance result; an enforcement claim without a real verifier is a defect, not evidence.
4. **Provenance-only lanes:** dispatch/admission/claim_key/admission_generation/compatibility_group facts are recorded as provenance; the same logical evidence emitted on multiple scheduler/dispatch lanes counts once; compatibility_group evidence binds only its derived claim_key scope. WEB-origin evidence never substitutes for required LOCAL real-host exact-subject validation; scheduler origin never implies Reviewer/Validator independence.
5. **Visibility:** every negative leaves fresh-observer-reconstructible state — the affected row shows `UNRESOLVED` with exact subject, owning standard and missing-evidence description; rejected evidence is preserved with its rejection reason, never silently dropped, never rendered as an acceptance result.
6. **Adoption-path separation:** authority-required evidence is mandatory on both Minimum-ADS and Advanced-ADS paths; Advanced-only orchestration producers never become Minimum-path requirements and Minimum-path blockers stay constructible with zero scheduler/runtime evidence.
7. **Closure separation:** `#900` provenance remediation stays a distinct version-closure blocker input; `#865` V410-V01 is a later closure-input Validation, not a Product acceptance producer; `ADS_CORE_FEATURE_FREEZE_ELIGIBLE` remains an explicit Product-authority decision (§1.1) reachable only through the T07B decision-support path — Version Closure, Controller state, CI success, Reviewer or model votes cannot manufacture it.

## Requirement rows (machine record)

```json
{
  "record_schema": "v410-acceptance-projection-v1",
  "rebind_subject": {
    "base_sha": "0518202c715dcf91784a694bdf4a8eeeaeb16ab6",
    "base_tree": "75566c464505386fedffde803e05e3e726922434"
  },
  "candidate_exact_subject": "UNBOUND_UNTIL_T08A_INTEGRATION",
  "rows": [
    {
      "row_id": "V410-ACC-R1",
      "requirement_id": "R1",
      "prd_ref": "docs/implementation/4.10.0/PRD.md blob b0b9906035eee253aad4bff0274d3d4c8f90b9db section 19.1 item 1",
      "canonical_owner": "composition: VALIDATION_STANDARD owns exact-subject evidence meaning; Frozen Product section 4.1 owns the risk/policy selection rule; end-to-end falsification routes to V410-T08A integration with V410-V01 (#865) as later closure-input Validation",
      "evidence_producers": [
        {"producer_kind": "DOC", "durable_ref": "docs/implementation/4.10.0/PRODUCT_FREEZE.md", "exact_subject_binding": "DURABLE_STATIC", "blob_identity": "6b5bbd348a7dc3647e67fddac973edb1779c37c6"},
        {"producer_kind": "DOC", "durable_ref": "docs/implementation/4.10.0/PRODUCT_THAW_R1.md", "exact_subject_binding": "DURABLE_STATIC", "blob_identity": "608aa7c54e12d58fc119caa70f41d1b52015f8be"},
        {"producer_kind": "DOC", "durable_ref": "docs/implementation/4.10.0/TASK_PACKS_R1.md", "exact_subject_binding": "DURABLE_STATIC", "blob_identity": "3300f8494ecb2120d96fff520cd09270b538344b"},
        {"producer_kind": "CONFORMANCE_SUITE", "durable_ref": "scripts/test_v410_t01b_product_projections.py", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "a27e65e5e5ddf182533657e8fdb47d2cc4cc83ad"}
      ],
      "current_exact_subject": "UNBOUND_UNTIL_T08A_INTEGRATION",
      "currentness_rule": "any successor Product freeze/thaw on a new exact subject, or blob drift of any pinned producer, supersedes this row to historical; rebind required, no transfer to a successor (PRD section 16)",
      "blocker_projection": "UNRESOLVED",
      "missing_evidence_description": "no end-to-end discovery/proportionality falsification case exists yet on a visible integrated candidate (one sufficient-evidence/low-risk compact path plus one risk/policy-selected Product Review path)",
      "route_to_owner": "V410-T08A produces the falsification case on the integrated candidate; V410-V01 (#865) provides the later closure-input Validation; RELEASE_STANDARD owns any closure disposition",
      "rejected_provenance": [
        {"ref": "docs/implementation/4.10.0/L1_PRODUCT_EVIDENCE.md", "rejection_reason": "stale_subject"}
      ],
      "adoption_path": "MINIMUM_AND_ADVANCED",
      "authority_note": "pointer-only; requirement meaning stays in Frozen Product section 19.1 item 1"
    },
    {
      "row_id": "V410-ACC-R2",
      "requirement_id": "R2",
      "prd_ref": "docs/implementation/4.10.0/PRD.md blob b0b9906035eee253aad4bff0274d3d4c8f90b9db section 19.1 item 2",
      "canonical_owner": "composition: DEVELOPMENT_WORKFLOW owns lifecycle routing; RELEASE_STANDARD owns closure; references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md (integrated T06A) is the owner-discovery projection",
      "evidence_producers": [
        {"producer_kind": "DOC", "durable_ref": "references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "b5d0b09a4a3cef999745536e587925b871fd73c3"},
        {"producer_kind": "CONFORMANCE_SUITE", "durable_ref": "scripts/test_v410_owner_convergence.py", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "2e8bd6f9f12c5eee10f93684e1992faae181475e"},
        {"producer_kind": "DOC", "durable_ref": "docs/implementation/4.10.0/PRODUCT_FREEZE.md", "exact_subject_binding": "DURABLE_STATIC", "blob_identity": "6b5bbd348a7dc3647e67fddac973edb1779c37c6"}
      ],
      "current_exact_subject": "UNBOUND_UNTIL_T08A_INTEGRATION",
      "currentness_rule": "owner-map drift, any newly reachable duplicate/contradictory authority, or blob drift of any pinned producer supersedes this row to historical; rebind required",
      "blocker_projection": "UNRESOLVED",
      "missing_evidence_description": "closure evidence that no unresolved material duplicate or contradictory authority remains in the current owner/lifecycle graph does not exist yet (section 1.1 precondition 2)",
      "route_to_owner": "V410-T08A integration + RELEASE_STANDARD closure evaluation; unresolved discovery gaps route to the owning standards via references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md",
      "rejected_provenance": [],
      "adoption_path": "MINIMUM_AND_ADVANCED",
      "authority_note": "pointer-only; the owner-convergence reference is a projection, not an authority"
    },
    {
      "row_id": "V410-ACC-R3",
      "requirement_id": "R3",
      "prd_ref": "docs/implementation/4.10.0/PRD.md blob b0b9906035eee253aad4bff0274d3d4c8f90b9db section 19.1 item 3",
      "canonical_owner": "composition: VALIDATION_STANDARD owns exact-subject evidence meaning; GITHUB_AGENT_INTERACTION_PROTOCOL and EXECUTION_ARCHITECTURE_STANDARD own the collaboration/dispatch semantics; no second Task/Dispatch lifecycle",
      "evidence_producers": [
        {"producer_kind": "CONFORMANCE_SUITE", "durable_ref": "scripts/test_v410_t02a_collaboration_control.py", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "850093ca2e4a9763054fc93d0c688fb8098ac0a5"},
        {"producer_kind": "CONFORMANCE_SUITE", "durable_ref": "scripts/test_v410_t02b_machine_projection.py", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "4b7c043d5788bb1fdfb3c7f2194da1e038ad1c96"},
        {"producer_kind": "CONFORMANCE_SUITE", "durable_ref": "scripts/test_v410_t06b_multi_dispatch_conformance.py", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "2b236a5e0d0a13009fc75450a05593f657719e5b"}
      ],
      "current_exact_subject": "UNBOUND_UNTIL_T08A_INTEGRATION",
      "currentness_rule": "schema/protocol/execution-architecture drift on a new exact subject, or blob drift of any pinned producer, supersedes this row to historical; the same suite execution counts once, never as multiple independent falsification cases",
      "blocker_projection": "UNRESOLVED",
      "missing_evidence_description": "no fresh-observer end-to-end reconstruction case (requester/delegator, responsibility owner, executor, subject, evidence, transition cause) exists yet on a visible integrated candidate",
      "route_to_owner": "V410-T08A produces the falsification case; V410-V01 (#865) provides the later closure-input Validation",
      "rejected_provenance": [
        {"ref": "scheduler dispatch/admission/claim events on #862 lanes", "rejection_reason": "scheduler_only"}
      ],
      "adoption_path": "MINIMUM_AND_ADVANCED",
      "authority_note": "pointer-only; T06B conformance wiring is Dispatch-level machinery, never R3 acceptance by itself"
    },
    {
      "row_id": "V410-ACC-R4",
      "requirement_id": "R4",
      "prd_ref": "docs/implementation/4.10.0/PRD.md blob b0b9906035eee253aad4bff0274d3d4c8f90b9db section 19.1 item 4",
      "canonical_owner": "composition: Frozen Product section 7 owns controllability meaning; VALIDATION_STANDARD and the owning Review policy protect quality evidence; EXECUTION_ARCHITECTURE_STANDARD owns Human Decision Queue control points",
      "evidence_producers": [
        {"producer_kind": "DOC", "durable_ref": "docs/implementation/4.10.0/PRODUCT_THAW_R1.md", "exact_subject_binding": "DURABLE_STATIC", "blob_identity": "608aa7c54e12d58fc119caa70f41d1b52015f8be"},
        {"producer_kind": "CONFORMANCE_SUITE", "durable_ref": "scripts/test_v410_stage1_lifecycle_contracts.py", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "dd5b2b56c83d90f16522cea0c29fedea677e78da"},
        {"producer_kind": "CONFORMANCE_SUITE", "durable_ref": "scripts/test_v410_t03a_implementation_quality.py", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "23933868e20fb6e76c41bc16167979a6c4ad0eb1"},
        {"producer_kind": "ISSUE_EVENT", "durable_ref": "#862@6052647951+#862@6052650587+#862@6052653911", "exact_subject_binding": "EVENT_BOUND"}
      ],
      "current_exact_subject": "UNBOUND_UNTIL_T08A_INTEGRATION",
      "currentness_rule": "the EVENT_BOUND dispatch chain is this task's own provenance instance, never self-certifying acceptance; blob drift of any pinned producer or a successor product subject supersedes this row to historical",
      "blocker_projection": "UNRESOLVED",
      "missing_evidence_description": "the authority-sensitive human-control case (authorized human approves/rejects/stop-redirects automation and the resulting causation is recorded) has no end-to-end falsification case yet on a visible integrated candidate",
      "route_to_owner": "V410-T08A produces the routine no-human-line-review case and the authority-sensitive control case on the integrated candidate",
      "rejected_provenance": [],
      "adoption_path": "MINIMUM_AND_ADVANCED",
      "authority_note": "pointer-only; human control points stay required on both adoption paths, mandatory line-by-line human review stays forbidden (PRD section 20)"
    },
    {
      "row_id": "V410-ACC-R6",
      "requirement_id": "R6",
      "prd_ref": "docs/implementation/4.10.0/PRD.md blob b0b9906035eee253aad4bff0274d3d4c8f90b9db section 19.1 item 5",
      "canonical_owner": "composition: VALIDATION_STANDARD owns fail-closed gates and the only legal not-applicable classification; DEVELOPMENT_WORKFLOW owns bounded root-class repair routing",
      "evidence_producers": [
        {"producer_kind": "CONFORMANCE_SUITE", "durable_ref": "scripts/test_v410_t04a_gate_repair_routing.py", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "aa46924d431604e7b7c0f8d865285e7f0160c8ba"},
        {"producer_kind": "CONFORMANCE_SUITE", "durable_ref": "scripts/test_v410_t04b_review_currentness.py", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "d67a2ab9ab04c0c3fa30f14404751d3c6d457c72"},
        {"producer_kind": "CONFORMANCE_SUITE", "durable_ref": "scripts/test_v410_t05a_shared_code_safety.py", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "f24ebce75532607535ee63e169a8d823eb7c6749"}
      ],
      "current_exact_subject": "UNBOUND_UNTIL_T08A_INTEGRATION",
      "currentness_rule": "gate-routing/repair-policy drift on a new exact subject, or blob drift of any pinned producer, supersedes this row to historical",
      "blocker_projection": "UNRESOLVED",
      "missing_evidence_description": "the attempted gate-reduction rejection case (cost/file-count/label/model-confidence/speed justification rejected fail-closed) and the bounded non-converging-repair adjudication case have no end-to-end falsification evidence yet on a visible integrated candidate",
      "route_to_owner": "V410-T08A produces both falsification cases; convenience reclassifications route per VALIDATION_STANDARD and RELEASE_STANDARD section 11.4",
      "rejected_provenance": [
        {"ref": "any cost/docs-only/file-count/speed/model-confidence gate reduction", "rejection_reason": "convenience_na"}
      ],
      "adoption_path": "MINIMUM_AND_ADVANCED",
      "authority_note": "pointer-only; V410-T05B's DONE_NO_CHANGE_REQUIRED disposition stays recorded in its own durable closeout, not restated here as evidence"
    },
    {
      "row_id": "V410-ACC-R7",
      "requirement_id": "R7",
      "prd_ref": "docs/implementation/4.10.0/PRD.md blob b0b9906035eee253aad4bff0274d3d4c8f90b9db section 19.1 item 6",
      "canonical_owner": "composition: EXECUTION_ARCHITECTURE_STANDARD owns dispatch/claim machinery; TASK_DAG_GOVERNANCE owns DAG mutation; REFINED_TASK_DAG_FREEZE_R1 + TASK_PACKS_R1 own granularity authority",
      "evidence_producers": [
        {"producer_kind": "DOC", "durable_ref": "docs/implementation/4.10.0/REFINED_TASK_DAG_FREEZE_R1.md", "exact_subject_binding": "DURABLE_STATIC", "blob_identity": "ba9cc3320c49980b8ce31857428801ccb5a7b39f"},
        {"producer_kind": "DOC", "durable_ref": "docs/implementation/4.10.0/EXECUTION_DAG_MATERIALIZATION_R1.md", "exact_subject_binding": "DURABLE_STATIC", "blob_identity": "e184941d096c27df560965c7a88d7740fef9ea50"},
        {"producer_kind": "DOC", "durable_ref": "docs/implementation/4.10.0/TASK_DAG.md", "exact_subject_binding": "DURABLE_STATIC", "blob_identity": "3b8a0e4fc479b527c54e85783b4514716bec8815"},
        {"producer_kind": "DOC", "durable_ref": "docs/implementation/4.10.0/TASK_PACKS_R1.md", "exact_subject_binding": "DURABLE_STATIC", "blob_identity": "3300f8494ecb2120d96fff520cd09270b538344b"},
        {"producer_kind": "CONFORMANCE_SUITE", "durable_ref": "scripts/test_v410_t06b_multi_dispatch_conformance.py", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "2b236a5e0d0a13009fc75450a05593f657719e5b"}
      ],
      "current_exact_subject": "UNBOUND_UNTIL_T08A_INTEGRATION",
      "currentness_rule": "DAG re-freeze/materialization on a new exact subject, or blob drift of any pinned producer, supersedes this row to historical; dual-scheduler serialization and MULTI_DISPATCH_CONCURRENCY_R1 remain provenance machinery, never R7 acceptance by themselves",
      "blocker_projection": "UNRESOLVED",
      "missing_evidence_description": "the split-or-atomic falsification case (semantically broad work item split across independent evidence seams or explicitly kept atomic, with no hidden DAG mutation / fake parallelism / overlapping shared-authority write set) has no end-to-end evidence yet on a visible integrated candidate",
      "route_to_owner": "V410-T08A produces the falsification case; hidden-DAG negatives stay owned by the T06B conformance surfaces",
      "rejected_provenance": [],
      "adoption_path": "MINIMUM_AND_ADVANCED",
      "authority_note": "pointer-only; no numeric universal limits are created by this row"
    },
    {
      "row_id": "V410-ACC-R11",
      "requirement_id": "R11",
      "prd_ref": "docs/implementation/4.10.0/PRD.md blob b0b9906035eee253aad4bff0274d3d4c8f90b9db section 19.1 item 7",
      "canonical_owner": "composition: V410-T06B (integrated) is the primary machine-conformance owner; EXECUTION_ARCHITECTURE_STANDARD owns the projected semantics; stale-verifier/false-claim detection stays with the conformance surfaces",
      "evidence_producers": [
        {"producer_kind": "CONFORMANCE_SUITE", "durable_ref": "scripts/test_v410_t06b_core_inventory.py", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "bc763552d0a521750eebe4c04dde28d1bda054b9"},
        {"producer_kind": "CONFORMANCE_SUITE", "durable_ref": "scripts/test_v410_t06b_multi_dispatch_conformance.py", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "2b236a5e0d0a13009fc75450a05593f657719e5b"},
        {"producer_kind": "CONFORMANCE_SUITE", "durable_ref": "scripts/test_v410_t02b_machine_projection.py", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "4b7c043d5788bb1fdfb3c7f2194da1e038ad1c96"},
        {"producer_kind": "DOC", "durable_ref": "references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "b5d0b09a4a3cef999745536e587925b871fd73c3"}
      ],
      "current_exact_subject": "UNBOUND_UNTIL_T08A_INTEGRATION",
      "currentness_rule": "schema/verifier/manifest drift on a new exact subject, or blob drift of any pinned producer, supersedes this row to historical; a stale passing verifier can never override current owner authority",
      "blocker_projection": "UNRESOLVED",
      "missing_evidence_description": "the whole-project visible conformance run (stale-verifier-cannot-override and false enforcement-claim detection end to end) has no evidence yet on the visible integrated candidate; prose-machine contradiction discovery beyond integrated suites stays open",
      "route_to_owner": "V410-T08A runs whole-project visible conformance; V410-V01 (#865) provides the independent closure-input Validation",
      "rejected_provenance": [
        {"ref": "scripts/test_v410_t07a_evidence_inventory.py on retained prep branch task/v4.10.0-v410-t07a-local-evidence-inventory-r1@a248c3a", "rejection_reason": "stale_subject"}
      ],
      "adoption_path": "MINIMUM_AND_ADVANCED",
      "authority_note": "pointer-only; conformance results never grant Release/Closure authority"
    },
    {
      "row_id": "V410-ACC-R12",
      "requirement_id": "R12",
      "prd_ref": "docs/implementation/4.10.0/PRD.md blob b0b9906035eee253aad4bff0274d3d4c8f90b9db section 19.1 item 8",
      "canonical_owner": "composition: Frozen Product section 16 owns lineage/compatibility meaning; RELEASE_STANDARD owns release identity; DEVELOPMENT_WORKFLOW owns compatibility owners; V410-T07B owns the freeze-decision decision-record support path",
      "evidence_producers": [
        {"producer_kind": "DOC", "durable_ref": "docs/implementation/4.10.0/PRODUCT_FREEZE.md", "exact_subject_binding": "DURABLE_STATIC", "blob_identity": "6b5bbd348a7dc3647e67fddac973edb1779c37c6"},
        {"producer_kind": "DOC", "durable_ref": "docs/implementation/4.10.0/L2_FREEZE.md", "exact_subject_binding": "DURABLE_STATIC", "blob_identity": "0a3ed1bf06b623e555ae279ee1d427b3f589c5ed"},
        {"producer_kind": "DOC", "durable_ref": "docs/implementation/4.10.0/REFINED_TASK_DAG_FREEZE_R1.md", "exact_subject_binding": "DURABLE_STATIC", "blob_identity": "ba9cc3320c49980b8ce31857428801ccb5a7b39f"},
        {"producer_kind": "DOC", "durable_ref": "references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md", "exact_subject_binding": "CANDIDATE_BOUND", "blob_identity": "b5d0b09a4a3cef999745536e587925b871fd73c3"}
      ],
      "current_exact_subject": "UNBOUND_UNTIL_T08A_INTEGRATION",
      "currentness_rule": "any re-freeze on a new exact subject, compatibility-surface drift, or blob drift of any pinned producer supersedes this row to historical; a reconstructed/recomposed successor never inherits historical qualification automatically (PRD section 16)",
      "blocker_projection": "UNRESOLVED",
      "missing_evidence_description": "the fresh-adopter navigation falsification case (no private chat history), the successor non-inheritance enforcement case, and the durable section 1.1 core-feature-freeze decision-record path have no end-to-end evidence yet",
      "route_to_owner": "V410-T07B builds the freeze-decision decision-record support path; V410-T08A produces the fresh-adopter and successor-non-inheritance falsification cases",
      "rejected_provenance": [
        {"ref": "docs/implementation/4.10.0/L1_PRODUCT_EVIDENCE.md", "rejection_reason": "stale_subject"}
      ],
      "adoption_path": "MINIMUM_AND_ADVANCED",
      "authority_note": "pointer-only; current version identity never moves backward to recover old semantics"
    }
  ],
  "closure_blocker_inputs": [
    {
      "blocker_id": "BLK-900-PROVENANCE-CAMPAIGN",
      "distinct_from_product_rows": true,
      "owning_standard": "provenance remediation campaign #900; Validator/Reviewer campaign verdicts are closure evidence; RELEASE_STANDARD owns closure",
      "durable_ref": "issue #900 (state OPEN, live-verified at the rebind subject)",
      "exact_subject_binding": "EVENT_BOUND",
      "state": "OPEN",
      "note": "per-unit remediation rows and campaign verdicts are version-closure blocker inputs; multi-dispatch conformance results never waive them"
    },
    {
      "blocker_id": "BLK-865-V01-CLOSURE-VALIDATION",
      "distinct_from_product_rows": true,
      "owning_standard": "VALIDATION_STANDARD via the V410-V01 contract",
      "durable_ref": "docs/implementation/4.10.0/V410_V01_VALIDATION_CONTRACT.md blob 8df051f49573ee3784cbc97e0be7a87b8e8f7c90 + issue #865 (state OPEN, live-verified at the rebind subject)",
      "exact_subject_binding": "EVENT_BOUND",
      "state": "OPEN",
      "note": "NOT_YET_DISPATCHABLE until V410-T08A integration; a later closure-input Validation, never a Product acceptance producer"
    },
    {
      "blocker_id": "BLK-19-2-GATE-APPLICABILITY",
      "distinct_from_product_rows": true,
      "owning_standard": "RELEASE_STANDARD section 11 gate-applicability decision records",
      "durable_ref": "standards/RELEASE_STANDARD.md (untouched owner; decisions live in its durable records)",
      "exact_subject_binding": "DURABLE_STATIC",
      "state": "OPEN",
      "note": "a gate marked not-applicable must be legally not-applicable under its owning standard, never omitted by convenience; UNKNOWN applicability routes to the stronger legal path or BLOCKED per RELEASE_STANDARD section 11.4"
    },
    {
      "blocker_id": "BLK-FREEZE-DECISION-SUPPORT",
      "distinct_from_product_rows": true,
      "owning_standard": "explicit Product authority per PRD section 1.1; V410-T07B owns the decision-record support path",
      "durable_ref": "docs/implementation/4.10.0/PRD.md blob b0b9906035eee253aad4bff0274d3d4c8f90b9db section 1.1",
      "exact_subject_binding": "DURABLE_STATIC",
      "state": "OPEN",
      "note": "this index holds zero field path to any ADS_CORE_FEATURE_FREEZE_ELIGIBLE assertion; Version Closure, Controller state, CI success, Reviewer or model votes cannot manufacture the decision; NO is a legitimate evidence-backed outcome"
    }
  ]
}
```

## Rejected-evidence provenance appendix

Preserved with reasons; never silently dropped, never rendered as an acceptance result:

| Ref | Reason | Disposition |
| --- | --- | --- |
| `docs/implementation/4.10.0/L1_PRODUCT_EVIDENCE.md` (blob `d810af790d158710be05761a3057f81ce6853294`, marked SUPERSEDED) | `stale_subject` | historical L1 lineage evidence only; admissible for lineage questions, never a current producer |
| PR #927 preview heads `a7dc1273cfdfc694888367a70d807d1c76e63eaf` / `41df8e5ab2cb01208c1db375cd44c0177a814558` and all preview-exact facts | `stale_subject` | NON_INTEGRATED preview; every preview fact was rebound at `0518202c…` or dropped |
| retained prep branch `task/v4.10.0-v410-t07a-local-evidence-inventory-r1` (`fa4c162` + `a248c3a`, carries `scripts/test_v410_t07a_evidence_inventory.py`) | `stale_subject` + `wrong_layer` | reference-only, never a candidate; this task's suite was written fresh; the retained artifact stays absent from the checkout |
| WEB-origin precompute terminals (#862@6003300393/@6011927853/@6012768804/@6013713353/@6034650781/@6040863477/@6043147928/@6043147928/@6046061801) | `wrong_layer` | planning provenance; never a substitute for LOCAL real-host exact-subject evidence |
| CI / Task / PR results; Validation / Review outcomes on other gate families; machine-conformance results | `wrong_layer` | provenance only; never Product acceptance or blocker clearance by themselves (§19.2 gates stay owned by their own standards) |
| scheduler dispatch/admission/claim events; `compatibility_group` facts; multi-lane duplicate emissions | `scheduler_only` / `double_count` | provenance lanes; counted once, scope-pinned to the derived claim_key |
| provider/model diversity or vote counts | `vote_without_policy` | no authority without the owning Review/Validation policy (§3/§20) |
| Advanced-only orchestration evidence promoted onto the Minimum path | `scope_leak` | forbidden; authority-required evidence only on Minimum-ADS |
| legacy pack inventories (`TASK/PLAN/CONTEXT/COMMANDS/DOD/HANDOFF` under `.agent/execution/V410-T01A|V410-T01B|V410-T02A|V410-T02B-R2/`) | `wrong_layer` | PACK_INVALID provenance facts recorded by audit #898, preserved as-is; presence is a currentness observation, never a conformance verdict |
| any assertion of this index being an acceptance/Release/freeze verdict | `index_overreach` | structurally impossible here; the record block carries no verdict vocabulary and no release-state machine |

## Fresh-observer reconstruction

A fresh observer reconstructs the §19.3 blocker state at any checkout by running `python scripts/test_v410_t07a_acceptance_projection.py`: it re-parses this record block, re-verifies every pinned producer blob against the checkout, and fails closed on any drift, gap, or vocabulary violation. At the rebind subject every requirement row and every closure blocker input projects `UNRESOLVED`/`OPEN` — the PRD §19.3 blocker "any active requirement lacks passing falsification evidence" is visibly not cleared, and no verdict authority was consumed or created to say so.
