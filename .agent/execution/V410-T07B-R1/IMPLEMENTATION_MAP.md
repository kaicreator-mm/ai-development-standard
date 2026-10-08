# V410-T07B R1 implementation map — owner mapping, decision-path topology, JIT decisions

## Owner boundary (REUSE_FIRST_OWNER_MAP, #863@6003305569 — rebound, not rediscovered)

- **Frozen Product authority #837** (PRD v0.4 blob `b0b9906035eee253aad4bff0274d3d4c8f90b9db`, §1.1/§19.4) owns the `ADS_CORE_FEATURE_FREEZE_ELIGIBLE` decision itself: the human Product authority owner, or an explicitly delegated actor within §28.3-bounded authority with a durable delegation fact. Delegation chains cannot launder authority.
- **DEVELOPMENT_WORKFLOW** (blob `a7fef842927e58a93b671fe9869b9395559845ac`) owns the Stage-1 recording semantics this task mirrors: a Controller may deterministically RECORD a freeze transition only after the Product authority (or its authorized routing rule) authorizes it — never pre-fill, default, or infer.
- **EXECUTION_ARCHITECTURE_STANDARD** (blob `0bb9e30481c2a37b5596ee940091597552435eed`) owns the Human Decision Queue (§19) and responsibility/attenuation/human-control semantics (§28.2/§28.3/§28.4). The record rides these existing surfaces; no second control workflow is created.
- **T07A acceptance-evidence index** (`docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md`, blob `65baefd3a1d087d3692e6e603dbe098546bc7cb1` at this base) is the pointer-only evidence-input projection: the record references its rows R1/R2/R3/R4/R6/R7/R11/R12 plus the closure blocker inputs; it never embeds them.
- **VALIDATION_STANDARD** owns exact-subject evidence meaning; **RELEASE_STANDARD** owns Candidate/Closure/Release authority and consumes but never owns the Product decision; **T06B machine-conformance surfaces** check record conformance and hold zero decision authority.
- This task (`V410-T07B`) owns ONLY the record plumbing: template, decision-path reference, checklist row, focused conformance suite, pack.

## Deliverable topology

1. `templates/product-decision-record.md` — the fill-in decision-record template:
   - authority header (`RECORD_SUPPORT_ONLY=true; decision_authority=PRODUCT_AUTHORITY_ONLY; NO_AUTO_YES=true; PRODUCT_DECISION=NONE; ELIGIBILITY_VERDICT=NONE` on this task's chain) + usage rule (who may fill, when a record may exist);
   - one fenced JSON machine-record skeleton, `record_schema=v410-product-decision-record-v1`, with the 8 minimum fields as to-be-filled-by-authority slots (no decided value):
     (1) `decision_identity` — unique record_id + `decision_key=ADS_CORE_FEATURE_FREEZE_ELIGIBLE` + exact subject (repository, version, candidate SHA+tree);
     (2) `actor_authority` — actor + authority basis (human Product authority owner, or delegated actor with durable §28.3-bounded delegation fact; grantor must be the Product authority owner) + durable authority-act ref;
     (3) `evidence_inputs` — exact durable refs with currentness-at-decided_at, NEVER copies (T07A index rows R1/R2/R3/R4/R6/R7/R11/R12 subsets, §19.2 gate satisfaction, §19.3 blocker state, T06A owner-convergence, R11 contradiction state, R12 lineage);
     (4) `decision_value` — fill-in slot enumerating the two legal outcomes (both legal; a negative outcome names blocking evidence refs and is not a delivery failure);
     (5) `rationale_and_limitations`;
     (6) `decided_at` + durable GitHub publication ref;
     (7) `supersession` — successor references and supersedes prior record; append-only history;
     (8) `recording_rule` — verbatim;
   - negative rules (the no-auto-affirmative set) and fail-closed routing stated on the template prose.
2. `references/PRODUCT_DECISION_RECORD_REFERENCE.md` — the decision-path reference: who decides, what inputs (the §1.1 minimum inputs mapped to their producers), how recorded (recording rule + Human Decision Queue §19 + durable GitHub fact), supersession/currentness, the 7 no-auto-affirmative authority negatives, fail-closed routing.
3. `checklists/version-closure.md` — one decision-recording row in the Freeze Integrity section pointing at template + reference with the no-auto-affirmative rule.
4. `scripts/test_v410_t07b_decision_record.py` — focused stdlib suite: record-model validator (in-file, T07A pattern: markdown doc + single fenced JSON machine record; validator functions inside the test file) + P1-P6 positives + AN1-AN7 authority negatives + recording-rule enforcement + surface/pack/write-set guards.
5. This six-core pack (`.agent/execution/V410-T07B-R1/`), mirroring the V410-T07A-R1 family convention (which mirrors V410-T06B-R1).

## §1.1 minimum-input to producer binding (rebound at cea2e0cc)

| §1.1 minimum input | Durable evidence-input ref (pointers, never copies) | Producer owner |
| --- | --- | --- |
| 1. §19 acceptance evidence on the applicable release subject | T07A index rows V410-ACC-R1/R3/R4/R6 (blob `65baefd3…` at this base) | T07A projection + end-to-end falsification owners (T08A/V01) |
| 2. R2 owner/lifecycle convergence, no unresolved duplicate/contradictory authority | T07A index row V410-ACC-R2; `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md` (blob `b5d0b09a…`) | T06A discovery + T07A projection |
| 3. R11 no unresolved material prose↔machine contradiction | T07A index row V410-ACC-R11 | T06B conformance surfaces + T07A projection |
| 4. §10.4 legacy/backlog disposition | T07A index rows V410-ACC-R11/R12 + §19.3 blocker projection | owning standards via the projection |
| 5. R12 exact-subject/currentness/compatibility truth | T07A index row V410-ACC-R12 | Frozen Product §16 + T07A projection |
| gate + blocker state | §19.2 gate satisfaction; §19.3 blocker state incl. BLK-900/BLK-865 rows of the T07A index | RELEASE_STANDARD §11 + campaign #900 / #865 |
| lineage truth | R12 lineage rows (PRODUCT_FREEZE.md `6b5bbd34…`, L2_FREEZE.md `0a3ed1bf…`, REFINED_TASK_DAG_FREEZE_R1.md `ba9cc332…`) | Frozen authorities |

At this subject every one of these inputs projects `UNRESOLVED`/`OPEN` per the T07A index — so the honest current state is: **no conformant record could be completed yet, and none exists** (correct by design; only the Product authority may ever produce one).

## JIT decisions

- Checklist row: TAKEN (one row in checklists/version-closure.md Freeze Integrity section; the T07A JIT had explicitly left an optional checklist mutation declined for T07A — the decision-recording row is T07B's own deliverable).
- GOLDEN_INDEX registration: DECLINED — the surface set is exact-pinned by the carried golden verifier (`GOLDEN_INDEX_REQUIRED_SURFACES`); a row would fail `scripts/test_work_item_contract_and_golden_templates.py` and require a W13-class authorized co-evolution (DISP-NO-GOLDEN-INDEX-REGISTRATION).
- Manifest registration: DECLINED — `verify_standard.py` requires none; RA exact-set guards forbid unlisted additions (DISP-NO-MANIFEST-MUTATION).
- docs/implementation/4.10.0 index row: INAPPLICABLE — PLANNING_STATUS.md is the frozen-planning durable-state record, not an implementation-doc index; no such index exists (DISP-NO-PLANNING-STATUS-MUTATION).
- Pre-authorized carried-guard rebind: TAKEN (disclosed) — `scripts/test_v410_owner_convergence.py` TASK_CANDIDATES gains the V410-T07B entry (own prefixes, active flag moved per the registry's own successor-rebind rule); zero removed tests. Blob-pin cascade on the T07A projection row R2 pin (`d2347fca…`) is NOT executed here (T07A deliverables are not touched by this task) and is recorded as the known second-order seam in TEST_MATRIX.yaml.
- No decision instance: the template ships empty; zero decided values in any shipped file (grep receipt in the builder terminal).

## Boundary

No standards edits, no schema/template-family changes beyond the new record template, no verifier changes, no new state dimension/event family/lifecycle/release verdict, no Release/Validation/Review authority, and NEVER the Product decision itself. The Builder does not merge.
