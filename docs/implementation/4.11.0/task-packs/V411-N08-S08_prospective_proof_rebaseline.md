# V411-PROOF-REBASELINE — prospective N08/S08 L3 Task Pack delta (DRAFT, no executable admission)

> Product [#943@6167214986] authorizes **prospective** proof-scope change only. This is one **cross-owner coordination Pack** to make the impact, owner write sets and handoffs executable; it does not erase/change existing Frozen T08/T09/T12/V01 Pack blobs, alter native DAG, or count a completed Issue. The predecessor exact frozen subject `322e86845f78de8ea8cadb05ec624bfbb3a5de20` remains `V01=BLOCKED`. This Pack is **not an authorized dispatch** without Product successor exact Freeze, independently reviewed/owner-frozen L2 **design** (which may select conservative N08 UNKNOWN→HOLD), and independent Pack review/owner admission. The future Release §11.2/§11.5 **gate×new-candidate** decision and owner negative execution are required *before V01 PASS and protected Release actions*, not before authorizing implementation of the bounded adapter needed to produce their evidence. An unimplemented owner seam cannot bootstrap itself into a required pre-Builder positive Release signature.

```ini
TASK_PACK_STATE=DRAFT_UNADMITTED
SUBJECT=V411_PROSPECTIVE_N08_S08_PROOF_REBASELINE
PRODUCT_ACT=#943@6167214986
PRODUCT_PR=#1105@7c4f78b7c6eb9e3f9f5c88961316e1c3267de16f
PRODUCT_PRD_BLOB=edc9ef4d44edec035bac282dcc69467adf338729
PRODUCT_MATRIX_BLOB=2c9320321a70cc2fb51979e88b55af044ebacfde
L2_PR=#1106@c94a4fbf3383f07368ce6e9123d99c134f2ffdee
L2_BLOB=6c5d446b4155a326545682387b64ad39e80a04c6
ORIGINAL_T08_PACK=7999e5b294a56d051218832705b5e9279b4be3ee
ORIGINAL_T09_PACK=3b338da726db0ab053609d6b6c557d9670d13951
ORIGINAL_T12_PACK=a2af3ef49c852ff36cbb0a4eaac7d13e817b7890
ORIGINAL_V01_PACK=8885201ac2501f3a6e3a3d31123a63c2546986d2
ORIGINAL_CANDIDATE=322e86845f78de8ea8cadb05ec624bfbb3a5de20
PRODUCT_FREEZE_SUCCESSOR=#943@6170435421_EXACT_HEAD_1105
ARCHITECTURE_FREEZE_SUCCESSOR=PENDING_NEW_L2_R2_REVIEW
RELEASE_OWNER_NEW_CANDIDATE_DECISION=NOT_ISSUED_REQUIRED_BEFORE_V01_PASS
N08_REAL_OWNER_NEGATIVE=NOT_PROVEN
S08_SYNTHETIC_SQLITE_A_B=LOCAL_NON_GATE_EXIT0_#1108@6173669394_NOT_FORMAL
REAL_HUMAN_DENY_E2E=NOT_PROVEN
V01=BLOCKED
```

## 1. Dependencies and authority

**Admission DAG for work within the existing v4.11 Release/Review flow** (NOT six new native version-release tasks):

```text
P0 Product exact-reviewed/frozen successor (#1105/#943@6170435421)
   → P1 L2 source-reviewed + Architecture-owner **design** Freeze, conservative UNKNOWN→HOLD (#1106)
   → P2 this bounded implementation Task Pack independent review/freeze
   → P3 T08 source provenance/test-only boundary contracts  ┐
   → P4 T09 same-file-backed SQLite A→B synthetic veto tests ├─→ P6 T12 bounded material conformance
   → P5 N08 actual owner union admission negative             ┘
   → P6A new exact candidate + Release owner §11.2/§11.5 decision on observed owner proofs
   → P7 V01 fresh exact-new-candidate Validation/Review (Issue #1021)
   → V02 #1022 → V03 #1023 → V04 #1024 → R01 #1025 → R02 #1026
```

P3/P4/P5 can be prepared separately as **one concern / one PR** with non-overlapping writes; integration must be based on a source-supported owner. P6 cannot treat prior T12 52 assertions as new tested material proofs or bypass Owner acceptance. P7 does not start until P6 + Release gate×exact-subject facts are complete. A current draft may be reviewed read-only before its predecessors close but **cannot be executed as a Frozen Gate claim**.

## 2. Invariants and owned write sets

| Lane | Existing owner | Intended future write set (requires exact L3/Claim admission) | Read-only / avoid |
| --- | --- | --- | --- |
| P3 T08 | Interaction human authority contract | Owner-local T08 test/contract amendments and bounded source provenance contract, only if needed after inspection | No writing historical human record, no new source credential, no change to Release Standard/PRD |
| P4 T09 | External Effect/Migration reconciliation owner | `scripts/test_v411_t09_effect_boundary.py` and **one** new bounded companion runner only if isolated DB verification cannot live in owner-local test; no protected actual service mutation | No fake operator-supplied `HUMAN_AUTHORITY_FILE`, no cross-tenant effect, no rewrites to current historical V01 evidence |
| P5 N08 | Project Adoption/Workflow/Release owner *existing* admission | Existing owner admission/wiring contract and scoped negative integration tests only after source-owner selection; otherwise record missing interface as BLOCKED, no second policy engine | `test_v411_t12_abc_conformance.py` metadata `complete(facts)` alone is insufficient; no release PR/merge effect |
| P6 T12 | Existing T12 conformance assembly | Registry/runner targeted successor evidence/fixtures, preserving original 52 historical raw results and all S/X requirements | No authority promotion or changing prior `MATERIAL_INTERSECTION_UNKNOWN` to PASS by editing fixture text |
| P7 V01 | Independent Closure Validator | Existing exact three V01 evidence file paths on lawful successor only, with release-owner gate×subject identity; archive current #1103 historical BLOCKED packet rather than relabel tested SHA | Cannot change Builder/owner test code or V02/Hidden/RQ; source fixes go back to owner |

No single PR may simultaneously make owner implementation and independently approve its own Validation/Review. The Product/L2/Task Pack successor append-only source is a prospective alternative; canonical historical Frozen blobs stay immutable by exact SHA.

## 3. Tests — falsifiable positive and negative oracles

### 3.1 P3 historical human provenance and no authority escalation

- P3-P01: read immutable #1021@6163883456 and independently checked receipt digest #1021@6163960062; classify as **genuine historic human APPROVE on old exact candidate**, not DENY. In new candidate records use `HUMAN_PROVENANCE_HISTORICAL_APPROVE`, include **historical exact subject** and independent source verification ref.
- P3-N01: old human APPROVE with rewritten new `subject_head`, `decision=DENY` coercion, spoofed `human:`, `source_class` text, JSON SHA alone, `accepted` string and transport laundering **must not** yield current genuine human authority.
- P3-N02: `UNIT_LEVEL_AUTHORITY_FIXTURE_ONLY` or `SYNTHETIC_TEST_ONLY_DENY` supplied to a real authority-consuming boundary MUST fail closed, even if fixture has plausible fields. Test and real authority namespace/sink/consumer are separately bound. A test-only fixture must never supersede genuine APPROVE or any genuine DENY.
- P3 evidence strength: old human receipt = **historical real source**, P3-N01/N02 = deterministic guard proof only. No updated human signature/record and no human E2E veto PASS.

### 3.2 P4 actual SQLite effect mechanism

- P4-P01: in a clean, isolated real local Build Host process use one **real file-backed SQLite** DB and one same protected effect identity (candidate/job/tenant/scope/operation/effect_id). Actor A has a **test-helper modeled** accepted Claim (actual native protected Claim admission = NOT_PROVEN) and receives an explicitly **synthetic test-only DENY** before protected effect; execute the existing T09 owning sink and observe a refused A attempt with no protected effect. A genuine native CLAIMED/READY transition is not inferred or waived for a consumer requiring that proof.
- P4-P02: actor B, distinct **test-helper** operator/generation/attempt ID, modeled otherwise READY (not an authoritative native READY successor), attempts **same exact effect**, with synthetic denial fixture re-read if supported; B is refused. Close and independently reopen DB, read `attempts` with two blocked entries and `effects` (or actual protected effects table) with count=0; preserve auditable non-effect writes separately.
- P4-N01: wrong tenant/scope/effect/head/actor, stale decision, unauthorized supersession, untrusted transport wrapper, missing authority, read-error, replay and B/C competition must not produce a protected effect or PASS. A local fake flag-only result is not enough. Report real exit codes, schema/owner source blob, environment and exact SHA.
- P4-N02: historical human APPROVE **must not** be provided as the synthetic DENY nor edited. Synthetic DENY test must not claim actual human refused an operation. Real external provider and multi-host linearization are **NOT_RUN** unless separately actually executed.
- P4 gate is `BLOCKED` until actual execution and independent negative review; user has **not** authorized an Agent to mint any human DENY.

### 3.3 P5 N08 exact actual-applicability / owner admission negatives

- P5-P01: The implementation must not *assume* either optional Product eligibility condition. L2/Release owners may separately establish both — no ADS-owned actual four-job workload and no novel material predicate — with current exact-subject proof and accepted residual risk, allowing the physical-positive exclusion only then. While either remains UNKNOWN/novel, the stronger four-way N08 negative owner-admission obligation stays REQUIRED/BLOCKED; this is an **implementation task to satisfy**, not a reason to prohibit admission of its own Task Pack. The actual Release owner must decide gate applicability on the later real candidate before V01 PASS.
- P5-N01: actual declared four-job set missing each of J09/J10/J11/J12, wrong-work-subject/currentness, wrong actor/tenant/scope, stale license or unreconciled incident, or source proof omitted -> existing **owner-level** admission returns `HOLD/BLOCKED`, no unauthorized release advancement or side-effect. Must invoke real owning admission or independently accepted exact semantic equivalent — **not** only T12 `complete(fact_map)`.
- P5-N02: declared `J09+J10+J11` with **observed actual** upstream source/license change implies J12 and real 4-way unknown/HOLD; truly only three facts with J12 inspected absent uses their three-job AND, no invented J12, no free exemption for an unknown novel triple. Hidden/RQ applicability does not vanish.
- P5-N03: an Agent labels a 4-way unproved composite as PASS, NOT_APPLICABLE or “waived due to cost”, even when 4 metadata omissions pass → reject; no owner decision => Release/V01 remains BLOCKED.
- P5 if no existing executable owner seam is accessible, provide a bounded **owner integration gap** plus exact needed interface; do not manufacture a production-capable four-job API solely to turn gate green.

### 3.4 P6/P7 conformance and closure

- P6 retains all original required S01–S18 and X01–X08 ± denominator, original 52 T12 assertion rows as *historical* output. Add explicit **new** records for `HUMAN_HISTORICAL_APPROVE`, `SQLITE_SYNTHETIC_DENY_MECHANISM`, `REAL_HUMAN_DENY_E2E_NOT_PROVEN`, `N08_OWNER_ADMISSION_ACTUAL_NEGATIVES`, `FOURWAY_MATERIAL_INTERSECTION_UNKNOWN`; names are epistemic/proof labels, NOT new Validation Gate states.
- P6 must report mixed fidelity separately, with actual per-command exit/attempt/effect readbacks, source identity/tenant/actor/role/permission and failed-negative model; cannot count synthetic P2 as real human veto E3 or old P1 as new candidate currentness.
- P7 closure must attach exact `tested_sha × evidence-only-head × candidate_sha/tree`, real Host OS/toolchain/profile, gate-by-subject Release applicability and evidence identity for every inherited deferred gate, raw 139 history 125 exit0/14 exit1, delta-impact reruns and distinct Fresh Reviewer.
- P7 REQUIRED_NOW gate still not PASS → V01 remains BLOCKED; no V02 before actually accepted V01. Hidden/RQ are later real gates and never transferred from Task PR CI or self-review.

## 4. Contract — no new authority plane

Product scope §10 / proof matrix §5 [PR #1105], L2 existing-owner §14 [PR #1106], `PROJECT_ADOPTION`, `DEVELOPMENT_WORKFLOW`, `RELEASE_STANDARD` §11 and `EXTERNAL_SYSTEM_EXECUTION` / Interaction human-control owners remain normative. This L3 Pack is a reviewed dispatch **proposal** and must not add an alternate rules service, mandatory agent daemon, new Gate enum, global database, real-human credential generator, or independent-review bypass. Source-limited internal simulations are allowed only as explicitly test-only conformance, never as a live authority source.

## 5. Implementation and smallest lawful path

1. **WEB**: consume the already exact-frozen Product #943@6170435421 and get independent delta review + accountable *design-only* L2 Freeze for #1106's conservative existing-owner placement; do not require implementation-dependent real Release proof to freeze the design, and do not claim the optional C1/C2 exclusion.
2. **WEB**: independent Pack Reviewer checks this successor against accepted Product/L2 design, original Frozen T08/T09/T12/V01 blobs and §11.5. The Pack owner may freeze a **bounded implementation Pack** with N08 actual owner seam and negative test still specified as mandatory *deliverables*, not accepted gate results. Review alone is not Freeze.
3. **Builder + focused local Validator**: after Pack admission, implement one-concern owner-local T08/T09/T12 deltas as needed and a minimal Project Adoption/Workflow/Release owner-admission bridge that consumes real current owner decisions (not a second policy engine); reuse #1108's already observed local 6/6 technical-only SQLite receipts without treating them as authenticated Claim/Human or formal candidate-proof PASS. Execute actual owner N08 omissions/undeclared J12/stale+revoke denials and isolated SQLite proof with proper exact-source readbacks.
4. **Release owner / independent Validator**: pin the **new actual candidate**. Decide Release §11.2/§11.5 applicability at that exact subject using observed evidence and accountable owning decisions (no synthetic human signature); run focused impacted actual Host/critical-journey tests and explicit `VALIDATION_IMPACT_DECISION`. Preserve original 139 history (125 exit0/14 exit1) as immutable raw FAIL; new successor executions have their own exit values.
5. **V01 independent Closure Validator**: with Pack/owner proofs and candidate-bound Release decisions actually current, issue V01 PASS or truthful BLOCKED, then admit V02→R02 strictly by original native DAG.

## 6. Failure handling, limitations and stopping rules

- **No owner actual four-way workload / no novel predicate not actually proven** → N08 positive exclusion not effective; `MATERIAL_INTERSECTION_UNKNOWN/HOLD`, gate BLOCKED.
- **Synthetic DENY falsely presented as genuine human act** → critical FAIL, no promotion; fully isolate test data and refuse unsafe effect.
- **Human historical APPROVE with wrong exact SHA** → historical evidence only; no new candidate currentness.
- **SQLite test returns PASS but no observed sink/DB readback** → fidelity insufficient, BLOCKED, do not infer actual A/B behavior.
- **Missing genuine human veto end-to-end** → `REAL_HUMAN_DENY_E2E_NOT_PROVEN` remains; standards-only successor may report narrower proof only if authorized, high-risk real consumer stays blocked until own proof.
- **Missing independent role, Product/L2/Pack owner, Release applicability or Validation evidence** → BLOCKED and precisely name owner; do not issue round after round of duplicate LLM Review absent a new material counterexample.
- **Stage order:** Product exact Freeze → L2 *design-only* Freeze (UNKNOWN→HOLD allowed) → Pack freeze to authorize implementing missing proof → independent Builder/Host owner negatives → new exact candidate + actual owning Release §11.2/§11.5 decision → V01. Design/Pack admission may not silently flip ANY unresolved N08/S08 Release gate. No extra release gate or premature version tag.

## 7. References / evidence preflight

- Human Product Authority: #943@6167214986; original Product Freeze #943@6084264198; N08 reviewed predecision PR #1102@4fd81ed; S08 security challenger #943@6165647665.
- Product PR #1105 exact source `7c4f78b7c6eb9e3f9f5c88961316e1c3267de16f`, Product exact Freeze #943@6170435421; L2 source amended #1106@`c94a4fbf3383f07368ce6e9123d99c134f2ffdee` (new delta review/Architecture freeze pending).
- Original T08 Pack `7999e5b2...`; T09 Pack `3b338da7...`; T12 Pack `a2af3ef4...`; V01 Pack `8885201a...`; original version candidate `322e868...`; Test runner T09 `scripts/test_v411_t09_effect_boundary.py@3e1d6a2d...`, T12 `scripts/test_v411_t12_abc_conformance.py@e66eaee2...`.
- Honest Host status: V01 #1021@6156596087 (139 scripts 125 exit0/14 exit1; T12 52 assertions but material 28 BLOCKED/4 later NOT_RUN), independent V01 #1021@6162591281 = BLOCKED; historical human APPROVE #1021@6163883456 reviewed #1021@6163960062. No real human DENY proof. Current Draft #1103 evidence-only reviews PASS integrity **with** V01 BLOCKED.
