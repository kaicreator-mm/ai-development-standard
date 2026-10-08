# V410-T07B R1 execution contract — core-feature-freeze Product-decision support (record plumbing)

Exact base: `cea2e0ccd045e8fcebaf110273129b198ed259fd` (tree `cef6ce2e91cc62f4e1afe53b4a048f3fa4812fa2`), the merged #933 integration tip (V410-T07A R1 + authorized R2 carried-guard rebind). Task: #863. Execution environment: LOCAL. Branch: `task/v4.10.0-v410-t07b-core-freeze-decision-support`.
Frozen authorities: Product #837 (PRD v0.4 blob `b0b9906035eee253aad4bff0274d3d4c8f90b9db`), L2 #842, refined DAG #848, Task Pack R1 §V410-T07B (`TASK_PACKS_R1.md` blob `3300f8494ecb2120d96fff520cd09270b538344b`). Direct dependency V410-T07A INTEGRATED at this exact base; its acceptance-evidence index `docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md` (blob `65baefd3a1d087d3692e6e603dbe098546bc7cb1` at this base) is the primary evidence-input anchor of the decision path.

## Authority boundary (binding, restated verbatim-level from the fast-path handoff #863@6046064159 and dryrun #863@6040872034)

This task **supports but never makes the `ADS_CORE_FEATURE_FREEZE_ELIGIBLE` decision**. `PRODUCT_DECISION=NONE`. `ELIGIBILITY_VERDICT=NONE` for this entire chain — planning, pack, template, reference, checklist row, tests and any successor consume these surfaces without ever creating a decision value. The recording rule (mirroring DEVELOPMENT_WORKFLOW Stage-1 Product-Freeze semantics, blob `a7fef842927e58a93b671fe9869b9395559845ac`): **a controller/actor may RECORD a decision only after the authorized Product-authority act exists as durable fact — never pre-fill, default, or infer the value.** No shipped file in this change contains a decided value; the template ships empty with explicit to-be-filled-by-authority slots.

risk=high; agent_freedom=F1_BOUNDED_IMPLEMENTATION; validation_scope=concern.

## Goal (Task Pack §V410-T07B)

Support, but not decide, `ADS_CORE_FEATURE_FREEZE_ELIGIBLE=YES|NO`: an explicit Product-authority decision path exists; required evidence inputs are referenceable and reconstructible; an evidence-backed negative outcome is legal; Closure/Release READY/CI/Controller/Reviewer/model vote cannot manufacture an affirmative outcome.

## L3 seed (from #863@6003305569, bound at this JIT)

This pack embeds the repo L3 convention (`Tests → Contract/Invariant → Implementation seam → Failure Handling → References`), the same convention the integrated V410-T06B-R1 and V410-T07A-R1 packs use.

### Tests

Positive (conformance terminal #863@6013682453 P1-P6, rebound):
1. A human Product authority owner can issue an affirmative decision from sufficient current evidence (every §1.1 minimum input present and current at decided_at); the record carries all 8 contract elements.
2. The Product authority can issue an evidence-backed negative outcome with explicit blocking evidence refs; the negative outcome is a legitimate terminal, visibly distinct from a delivery failure.
3. An explicitly delegated actor within §28.3-bounded authority can be recorded as actor_authority only with a durable delegation fact whose grantor is the Product authority owner (chains cannot launder authority); bounded scope is reconstructible.
4. A fresh observer reconstructs decision identity, exact subject, actor + authority basis, evidence refs + currentness, value, rationale/limitations from durable facts alone.
5. A successor decision explicitly supersedes a prior record on a materially changed successor candidate; history is append-only, the prior record stays reachable as historical.
6. Evidence inputs are held as references (ref-shaped), never embedded copies; the record stays valid without embedding evidence bodies.

Negative (AUTHORITY_NEGATIVES 1-7 from #863@6040872034 + N1-N11 from #863@6013682453, bound into TEST_MATRIX.yaml and the focused suite):
1. Release READY / Candidate Freeze state ⇒ affirmative: REJECTED.
2. V01/Validation PASS ⇒ affirmative: REJECTED.
3. CI / Review / machine-conformance / model-majority / scheduler activity ⇒ affirmative: REJECTED.
4. Missing evidence defaulting to an affirmative value: REJECTED — fails closed to the evidence-backed negative outcome or BLOCKED_TO_PRODUCT_AUTHORITY routing, never an inferred affirmative.
5. A stale decision binding a materially changed successor candidate: REJECTED — explicit supersession required.
6. Builder/Validator/Reviewer/Controller self-authorizing the Product decision: REJECTED — only the human Product authority owner or a §28.3-bounded delegated actor with a durable delegation fact may be recorded as actor_authority.
7. #861 machinery facts (environment/scheduler/compatibility_group/admission) widening or selecting Product authority: REJECTED — evidence inputs only, never authority.
Plus recording-rule enforcement: a record missing the durable authority-act ref is invalid — no record may exist without the authorized Product-authority act as durable fact.

### Contract / invariants

- `DECISION_RECORD_SUPPORT_ONLY=true; decision_authority=PRODUCT_AUTHORITY_ONLY; PRODUCT_DECISION=NONE; ELIGIBILITY_VERDICT=NONE; NO_AUTO_YES=true` on every shipped surface.
- The value vocabulary is exactly the two legal outcomes with both legal; the machine layer (validator/tests) checks record CONFORMANCE and never produces, defaults or suggests a value (N11).
- Exact-subject binding: the record binds one exact subject (repository, version, candidate SHA+tree); a materially changed successor subject requires a successor record through explicit supersession; prior records stay historical, append-only, never rewritten (PRD §16).
- Evidence inputs are exact durable refs with currentness-at-decided_at — NEVER copies (T07A index rows R1/R2/R3/R4/R6/R7/R11/R12 subsets, §19.2 gate satisfaction, §19.3 blocker state, T06A owner-convergence, R11 contradiction state, R12 lineage).
- Fail-closed: insufficient or contradictory evidence routes to the evidence-backed negative outcome or BLOCKED_TO_PRODUCT_AUTHORITY — never an inferred affirmative (§1.1).
- No new state dimension, event family, lifecycle, or release verdict is created; the record rides existing Human Decision Queue (EXECUTION_ARCHITECTURE_STANDARD §19) / closeout / reference / template surfaces (§28.4).

### Implementation seam

Allowed write set (verbatim from Task Pack §V410-T07B): existing Product/human-decision + closeout/reference/template surfaces needed for durable evidence-input/decision record path. Concretely:
- NEW `templates/product-decision-record.md` — fill-in record template, 8 minimum fields, single fenced JSON machine-record skeleton with to-be-filled-by-authority slots (no decided value).
- NEW `references/PRODUCT_DECISION_RECORD_REFERENCE.md` — decision-path reference: who decides, what inputs, how recorded, supersession, no-auto-affirmative rules.
- EDIT `checklists/version-closure.md` — one decision-recording row pointing at template + reference.
- NEW `scripts/test_v410_t07b_decision_record.py` — focused deterministic suite (stdlib unittest): the 7 authority negatives as fail-closed validator mutants + positive plumbing cases.
- Six-core pack artifacts (this directory).
- One pre-authorized carried-guard rebind (disclosed): `scripts/test_v410_owner_convergence.py` TASK_CANDIDATES registry — add the V410-T07B candidate entry with T07B's own prefixes and move the active flag, exactly the successor-rebind mechanism the T07A R2 repair designed. Zero removed tests; no other assertion weakened.

Do NOT touch: `schemas/`, `standards/`, `scripts/v34_rules.py`, `scripts/verify_standard.py`, `templates/agent-event-comment.md`, `docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md` or its suite `scripts/test_v410_t07a_acceptance_projection.py`, `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md`, `standard-manifest.json`, `templates/GOLDEN_INDEX.md` (exact-set pinned by the carried golden verifier — registration declined), any other T07A/T06B deliverable content.

### Failure handling

- Missing/ambiguous authority basis, subject or evidence ⇒ the record is invalid; no conformance; carries no decision effect.
- Any template/verifier/CI path that auto-populates or defaults the value ⇒ rejected (the machine layer checks conformance, never produces the decision).
- Insufficient/contradictory evidence ⇒ route to the evidence-backed negative outcome or BLOCKED_TO_PRODUCT_AUTHORITY per the owning Product authority — never an inferred affirmative.
- Carried-suite red on a successor tree that a legal T07B path triggers (positional carried-assertion debt) ⇒ STOP and return to Controller for an authorized bounded rebind (the T07A R2 precedent); never widen scope, never weaken a carried assertion unilaterally.

### References

- Frozen Product #837 / `docs/implementation/4.10.0/PRD.md` (§1.1, §19.2, §19.3, §19.4, §20, §22 item 8; blob `b0b9906035eee253aad4bff0274d3d4c8f90b9db`)
- `docs/implementation/4.10.0/PRODUCT_FREEZE.md` (record #837; Fresh re-review #833 PASS lineage)
- `docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md` (integrated T07A index; blob `65baefd3a1d087d3692e6e603dbe098546bc7cb1` at this base)
- `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md` (integrated T06A; blob `b5d0b09a4a3cef999745536e587925b871fd73c3`)
- `standards/DEVELOPMENT_WORKFLOW.md` Stage-1 Product-Freeze recording semantics; `standards/EXECUTION_ARCHITECTURE_STANDARD.md` §19 Human Decision Queue + §28.2/§28.3/§28.4 responsibility/attenuation/human-control
- `docs/implementation/4.10.0/V410_V01_VALIDATION_CONTRACT.md` (blob `8df051f49573ee3784cbc97e0be7a87b8e8f7c90`; V01 is closure-input Validation, NOT the freeze decision)
- #900 (provenance remediation campaign — closure blocker input, distinct from Product requirement rows), #865 (V410-V01, NOT_YET_DISPATCHABLE until T08A)
- Precompute set: #863@6003305569 / @6013682453 / @6037701246 / @6040872034 / @6046064159

## Forbidden scope (verbatim from Task Pack §V410-T07B)

`new execution/release state dimension; implementation Task making final Product decision; automatic YES from CI/Review/Release`

Additionally forbidden by the fast-path handoff (#863@6046064159): self-minting `ADS_CORE_FEATURE_FREEZE_ELIGIBLE`; laundering Controller/Closure/CI/Review state into Product authority; inheriting predecessor qualification.

## Gate obligations

Focused decision-conformance + authority-negative suite green; all carried producer suites green (see TEST_MATRIX.yaml); `python scripts/verify_standard.py`; `python scripts/verify_event_writer_surfaces.py`; `tools/task-check.sh`; fresh LOCAL Concern Validation; genuinely Fresh Independent Review on one unchanged HEAD/tree. Review PASS is not Release PASS; the Builder does not merge; no merge until Validation + Independent Review PASS.
