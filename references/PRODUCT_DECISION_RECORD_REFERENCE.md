# Product Decision Record Reference — core-feature-freeze eligibility decision path

Status: **RECORD_SUPPORT_ONLY=true; decision_authority=PRODUCT_AUTHORITY_ONLY; NO_AUTO_YES=true; PRODUCT_DECISION=NONE; ELIGIBILITY_VERDICT=NONE**

This reference describes the durable decision path for `ADS_CORE_FEATURE_FREEZE_ELIGIBLE` — who decides, what inputs the decision consumes, how the decision is recorded, how supersession works, and which signals can never produce the value. It is support plumbing owned by V410-T07B; it holds no decision authority and never makes or implies the decision. The record surface itself is `templates/product-decision-record.md`.

## 1. Who decides (authority)

- The decision is an explicit **Product-authority** decision under Frozen Product #837 §1.1 (`docs/implementation/4.10.0/PRD.md` v0.4 blob `b0b9906035eee253aad4bff0274d3d4c8f90b9db`): "It may be made by the human Product authority owner or by an explicitly delegated actor within bounded authority, with the decision and evidence durably recorded."
- Delegated authority is bounded by `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §28.3 (`EFFECTIVE_CHILD_AUTHORITY` intersection; capability/credentials/tool/model access never create authority; **delegation chains cannot launder authority**). A delegation fact is valid for the record only if its grantor is the Product authority owner and its bounded scope covers this decision.
- No other actor may be recorded as `actor_authority`: Builder, Validator, Reviewer, Controller and scheduler roles self-authorizing the decision produce an invalid, non-conformant record with no decision effect (§28.3 authority attenuation).

## 2. What the decision consumes (evidence inputs — refs, never copies)

The §1.1 minimum inputs, each bound to its durable producer via the integrated T07A acceptance-evidence index (`docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md`, blob `65baefd3a1d087d3692e6e603dbe098546bc7cb1` at the V410-T07B rebind base `cea2e0ccd045e8fcebaf110273129b198ed259fd`):

| # | §1.1 minimum input | Durable ref (pointer) | Owner of meaning |
| --- | --- | --- | --- |
| 1 | All required §19 acceptance evidence satisfied on the applicable release subject | T07A index rows V410-ACC-R1/R3/R4/R6 (+R7) with currentness | Frozen Product §19 + VALIDATION_STANDARD |
| 2 | R2 owner/lifecycle convergence — no unresolved material duplicate or contradictory authority | T07A index row V410-ACC-R2; `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md` | DEVELOPMENT_WORKFLOW + T06A discovery |
| 3 | R11 — no unresolved material prose↔machine-contract/template/verifier/CI contradiction | T07A index row V410-ACC-R11 | T06B conformance surfaces + Frozen Product §10.3 |
| 4 | Reachable legacy/backlog ambiguity dispositioned under §10.4 | T07A index rows + §19.3 blocker projection | Frozen Product §10.4 + owning standards |
| 5 | R12 exact-subject/currentness/compatibility/lineage truth | T07A index row V410-ACC-R12 | Frozen Product §16 |
| + | §19.2 required-gate satisfaction; §19.3 blocker state (incl. #900 campaign and #865 V410-V01 as closure blocker inputs, distinct from Product requirement rows) | T07A index `closure_blocker_inputs` + RELEASE_STANDARD §11 decision records | RELEASE_STANDARD |

Rules for consuming inputs: every input is read as an exact durable ref **with its currentness at decided_at**; stale evidence stays reachable-but-historical and cannot satisfy a current input row; WEB/scheduler-environment capability evidence never substitutes for required LOCAL real-host exact-subject evidence; the same logical evidence emitted on multiple dispatch lanes counts once; machinery facts (environment, scheduler origin, compatibility_group, admission_generation) are evidence inputs only and can never widen or select Product authority.

## 3. How the decision is recorded (recording rule + surfaces)

- **Recording rule** (mirrors `standards/DEVELOPMENT_WORKFLOW.md` Stage-1 Product-Freeze semantics): a controller/actor may RECORD a decision only after the authorized Product-authority act exists as durable fact — never pre-fill, default, or infer the value. A record missing the `authority_act_ref` is invalid and carries no decision effect.
- The record is made by filling `templates/product-decision-record.md` (all 8 minimum field groups) and publishing it as a **durable GitHub fact** (issue/comment/PR), with the publication ref recorded inside the record. The Human Decision Queue (`standards/EXECUTION_ARCHITECTURE_STANDARD.md` §19) is the routing surface for the authority-sensitive decision; §28.4 keeps human control on those existing surfaces — no new state dimension, event family, lifecycle or release verdict is created.
- The machine layer (validators/suites such as `scripts/test_v410_t07b_decision_record.py`) checks record **conformance only** — required-field presence, exact-subject binding, delegation-authority validity, supersession reference integrity, absence of any auto-population path — and never produces, defaults, or suggests a value.

## 4. Value semantics (both outcomes legal)

- The value vocabulary is exactly the two legal outcomes of PRD §1.1; **both are legal**. The affirmative outcome means future ADS evolution defaults to bounded evidence-driven maintenance; the evidence-backed negative outcome means v4.10 may have been delivered successfully while justified core work remains — it MUST name the blocking evidence refs (`blocking_evidence_refs`) and is **not itself a v4.10 delivery failure** unless it also demonstrates an unmet active Product requirement.
- Fail-closed routing: insufficient, stale, ambiguous or contradictory evidence never defaults to an affirmative outcome; it routes to the evidence-backed negative outcome (with blocking refs) or `BLOCKED_TO_PRODUCT_AUTHORITY`.

## 5. Supersession and currentness

- A decision binds **one exact subject** (repository, version, candidate SHA+tree). A materially changed successor subject requires a successor record that explicitly references and supersedes the prior record; the old decision never auto-transfers and never silently binds the new subject.
- History is **append-only**: prior records remain reachable as historical records and are never rewritten or erased. `decided_at` plus the supersession chain form the lineage a fresh observer reconstructs without private chat history.
- Decision currentness is independent of Release currentness: Release READY on the exact candidate is an input fact, not the decision. After material evidence drift on an unchanged subject, the owning Product authority (never a machine layer) determines whether re-decision is required.

## 6. No-auto-affirmative rules (hard negatives)

Each of the following is an explicit rejection class, implemented as fail-closed validator checks in `scripts/test_v410_t07b_decision_record.py`:

1. Release READY / Version Closure / Candidate Freeze state can never produce an affirmative outcome (PRD §19.4/§20: closure alone never implies it).
2. V01 or any Validation PASS can never produce it (TASK_OR_PR_PASS != RELEASE_PASS; even Release PASS is only an input fact; #865 V410-V01 is closure-input Validation, not the freeze decision).
3. CI PASS, Reviewer PASS, Controller derived state, machine-conformance PASS, or multi-model vote majority can never produce it — authority comes solely from the Product authority owner.
4. Missing, stale or contradictory evidence must not default to an affirmative outcome — fail closed to the negative outcome with blockers or BLOCKED_TO_PRODUCT_AUTHORITY.
5. A stale decision must not bind a materially changed successor candidate/subject — exact-subject binding only; supersession required.
6. A Builder/Validator/Reviewer/Controller (or scheduler) cannot self-authorize or self-record the decision (§28.3); only the human Product authority owner or a validly delegated, §28.3-bounded actor with a durable delegation fact may be recorded.
7. #861 machinery facts (environment/scheduler/compatibility_group/admission) can never widen or select Product authority — evidence inputs only; multi-lane duplicates are never independent evidence.

## 7. Fresh-observer reconstruction

A fresh observer reconstructs the decision state from durable facts alone: run `python scripts/test_v410_t07b_decision_record.py` (template/reference/checklist conformance + validator), read the T07A index blocker projection (`python scripts/test_v410_t07a_acceptance_projection.py`), and read any published record via its `publication_ref`. At the V410-T07B rebind subject no record exists (correct by design — none may be created by any implementation Task), every T07A evidence row projects UNRESOLVED, and the §19.3 blockers are visibly not cleared.
