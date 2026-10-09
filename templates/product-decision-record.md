# Product Decision Record — ADS_CORE_FEATURE_FREEZE_ELIGIBLE (fill-in template)

Status: **RECORD_SUPPORT_ONLY=true; decision_authority=PRODUCT_AUTHORITY_ONLY; NO_AUTO_YES=true**

This template is the durable record surface for the explicit Product-authority decision `ADS_CORE_FEATURE_FREEZE_ELIGIBLE` (Frozen Product #837, `docs/implementation/4.10.0/PRD.md` v0.4 blob `b0b9906035eee253aad4bff0274d3d4c8f90b9db`, §1.1/§19.4). It SUPPORTS the decision; it never makes it. The template ships EMPTY: every value slot is a to-be-filled-by-authority placeholder, and no filled instance may be produced by any implementation Task, Controller, CI path, verifier or template itself.

## Who may fill this template

- The **human Product authority owner** (Frozen Product #837 §1.1), or
- an **explicitly delegated actor** with a durable delegation fact whose grantor is the Product authority owner and whose scope is inside the §28.3 bounded delegatable authority (`standards/EXECUTION_ARCHITECTURE_STANDARD.md` §28.3). Delegation chains cannot launder authority: no composition of delegations confers authority that no participant holds from its canonical owner.

Nobody else may be recorded as `actor_authority`. Builder, Validator, Reviewer, Controller, scheduler, CI, model votes, Release READY, Version Closure and Validation outcomes are evidence inputs or provenance only — they can never decide, manufacture, default, or auto-populate the value.

## Recording rule (binding, mirrors DEVELOPMENT_WORKFLOW Stage-1 Product-Freeze semantics)

A controller/actor may RECORD a decision only after the authorized Product-authority act exists as durable fact — never pre-fill, default, or infer the value. A record without the durable authority-act ref is invalid and carries no decision effect. Insufficient or contradictory evidence routes to an evidence-backed negative outcome (naming the blocking evidence refs) or to BLOCKED_TO_PRODUCT_AUTHORITY routing — never to an inferred affirmative outcome.

## How to record

1. Fill every slot of the machine-record skeleton below (one record per exact subject).
2. Reference evidence — NEVER copy it. Every evidence input is an exact durable ref plus its currentness at decided_at.
3. Publish the filled record as a durable GitHub fact and record its publication ref in the record itself.
4. A decision on a materially changed successor subject requires a NEW record that explicitly supersedes the prior record; history is append-only — prior records stay reachable as historical records and are never rewritten or erased.

## Machine record (single fenced JSON block — fill ALL slots)

```json
{
  "record_schema": "v410-product-decision-record-v1",
  "decision_identity": {
    "record_id": "<unique record id, e.g. PDR-<version>-<sequence> — TO_BE_FILLED>",
    "decision_key": "ADS_CORE_FEATURE_FREEZE_ELIGIBLE",
    "subject": {
      "repository": "<owner/repository — TO_BE_FILLED>",
      "version": "<semantic version of the release subject — TO_BE_FILLED>",
      "candidate_sha": "<40-hex exact candidate commit SHA the decision binds — TO_BE_FILLED>",
      "candidate_tree": "<40-hex exact candidate tree SHA the decision binds — TO_BE_FILLED>"
    }
  },
  "actor_authority": {
    "actor": "<deciding actor identity — TO_BE_FILLED>",
    "actor_role": "<HUMAN_PRODUCT_AUTHORITY_OWNER | DELEGATED_ACTOR_WITHIN_BOUNDED_AUTHORITY — TO_BE_FILLED>",
    "authority_basis": "<Frozen Product #837 section 1.1 for the owner role; for a delegated actor: the durable delegation fact ref with its bounded scope — TO_BE_FILLED>",
    "delegation_ref": "<durable delegation fact ref; REQUIRED if and only if actor_role is the delegated role; grantor MUST be the Product authority owner — TO_BE_FILLED or OMITTED_FOR_OWNER_ROLE>",
    "authority_act_ref": "<durable GitHub ref of the authorized Product-authority act this record documents; REQUIRED — a record without it is invalid — TO_BE_FILLED>",
    "authority_owner_ref": "docs/implementation/4.10.0/PRODUCT_FREEZE.md (record #837; Fresh re-review #833 PASS) + docs/implementation/4.10.0/PRD.md blob b0b9906035eee253aad4bff0274d3d4c8f90b9db section 1.1"
  },
  "evidence_inputs": [
    {
      "input_id": "<minimum-input id, e.g. ACC-R1..ACC-R12 row subset, GATE-19-2, BLOCKERS-19-3, OWNER-CONVERGENCE, R11-CONTRADICTION, R12-LINEAGE — TO_BE_FILLED>",
      "durable_ref": "<exact durable ref INTO the owning evidence producer (T07A index row / gate decision record / blocker state / convergence reference) — a pointer, NEVER a copy — TO_BE_FILLED>",
      "subject_binding": "<CANDIDATE_BOUND | DURABLE_STATIC | EVENT_BOUND — TO_BE_FILLED>",
      "currentness_at_decided_at": "<CURRENT | HISTORICAL — TO_BE_FILLED>",
      "ref_identity": "<blob identity for static/CANDIDATE_BOUND refs, or event id for EVENT_BOUND refs — TO_BE_FILLED>"
    }
  ],
  "decision_value": "<TO_BE_RECORDED_BY_PRODUCT_AUTHORITY_ONLY: one of the two legal outcome values defined by PRD section 1.1; both are legal; an evidence-backed negative outcome MUST name blocking_evidence_refs and is not itself a delivery failure>",
  "blocking_evidence_refs": [
    "<REQUIRED if the recorded value is the negative outcome: exact durable refs of the blocking evidence / remaining justified core concerns; otherwise omit>"
  ],
  "rationale_and_limitations": "<evidence-based rationale; explicit limitations, bounded-scope notes for delegated authority, and any re-decision policy note — TO_BE_FILLED>",
  "decided_at": "<ISO-8601 timestamp of the authorized Product-authority act — TO_BE_FILLED>",
  "publication_ref": "<durable GitHub publication of THIS filled record (issue/comment/PR ref) — TO_BE_FILLED>",
  "supersession": {
    "supersedes_record_id": "<record id of the prior superseded record, or NONE_FOR_FIRST_RECORD on this subject lineage>",
    "prior_record_ref": "<durable ref to the prior record; REQUIRED unless supersedes_record_id is NONE_FOR_FIRST_RECORD>",
    "supersession_rule": "a materially changed successor subject requires this successor record; history is append-only; prior records remain historical and are never rewritten or erased"
  },
  "recording_rule": "a controller/actor may record this decision only after the authorized Product-authority act exists as durable fact — never pre-fill, default, or infer the value",
  "routing_on_insufficient_evidence": "BLOCKED_TO_PRODUCT_AUTHORITY — insufficient, stale, ambiguous or contradictory evidence is never resolved by an inferred value; it routes back to the Product authority"
}
```

## Negative rules (binding on every filled record)

1. **Product-authority-only:** the value originates solely from the authorized Product-authority act named in `authority_act_ref`; no CI/Review/Validation/Release/Controller/model-vote signal may populate it.
2. **No auto-value:** no default, derived, or inferred value path exists; the machine layer (validators/suites) checks record CONFORMANCE only and never produces a value.
3. **Fail-closed:** missing/stale/contradictory evidence never becomes a satisfied minimum input; it routes to the evidence-backed negative outcome (with blocking refs) or BLOCKED_TO_PRODUCT_AUTHORITY.
4. **Exact-subject binding:** the record binds exactly one subject (version + candidate SHA+tree); it never auto-transfers to a successor subject — only explicit supersession carries a decision forward.
5. **Refs, never copies:** evidence inputs are pointers into the owning producers (the T07A acceptance-evidence index `docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md` rows R1/R2/R3/R4/R6/R7/R11/R12 plus its closure blocker inputs, §19.2 gate decision records, §19.3 blocker state, the owner-convergence reference, the R11 contradiction state, the R12 lineage); embedding evidence bodies makes the record non-conformant.
6. **Append-only lineage:** supersession references and supersedes; it never erases or rewrites a prior record.
7. **Machinery facts are evidence only:** execution environment, scheduler origin, compatibility_group, admission_generation and dispatch-lane facts never widen or select Product authority, and the same logical evidence emitted on multiple lanes counts once.
