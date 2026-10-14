# V411 N08 — Prospective Product → L2 → T12 → V01 compound-scope amendment packet

> **DRAFT / NOT FROZEN / NOT RELEASE AUTHORITY.** This is a reviewable change-control **proposal** for one bounded Product concern on a dedicated branch, not a substitute for the current Frozen PRD/L2/Task Pack blobs. Do not merge, use for V01 PASS, freeze V02, or change a required gate until the owning Product / L2 / Task Pack / Release roles have explicitly authorized the successor and a genuinely independent review has passed.

```ini
EVENT=V411_N08_PROSPECTIVE_PRODUCT_SCOPE_CHANGE_PACKET
SOURCE_PRODUCT_USER_DIRECTION=#943@6155977141
PRODUCT_FROZEN_AUTHORITY=#943@6084264198
CURRENT_RELEASE_EVIDENCE=#1021@6162591281
SOURCE_CANDIDATE=version/v4.11.0@322e86845f78de8ea8cadb05ec624bfbb3a5de20
SOURCE_TREE=b793e5b1f65fa5309b7cf9dab8cb5d0168d74abd
SOURCE_PRD_BLOB=d30f202e8ea662731ff8a4f2ad1ad88cfc5bb179
SOURCE_PRODUCT_PROOF_MATRIX_BLOB=f59a6daf5430ece66103a830e392a04f71623ff0
SOURCE_L2_BLOB=c0fa361474996a0626c63e93574a284ae3eb8d91
SOURCE_T12_PACK_BLOB=a2af3ef49c852ff36cbb0a4eaac7d13e817b7890
SOURCE_V01_PACK_BLOB=8885201ac2501f3a6e3a3d31123a63c2546986d2
RELEASE_STANDARD_BLOB=c4d72506253ca7f3d95e305dbd84aae0e1fbe2cb
CHANGE_KIND=PRODUCT_ACCEPTANCE_NARROWING_WITH_PROSPECTIVE_REBASELINE
OLD_FROZEN_OBLIGATIONS=UNMODIFIED_AND_STILL_BIND_322e868_CANDIDATE
NEW_CANDIDATE_REQUIRED=YES_IF_THIS_CHANGE_IS_ADOPTED
THIS_PACKET_GATE_VERDICT=NONE
N08_PRESENT=MATERIAL_INTERSECTION_UNKNOWN
S08_REAL_HUMAN_DENY=STILL_REQUIRED
NO_SOURCE_TEST_SCHEMA_NORMATIVE_CHANGE_IN_THIS_PR=YES
```

## 1. Why change, what is deliberately *not* being weakened

Frozen Product PRD §2.2–2.4 requires AND/obligation-union of all **actual** materially applicable jobs, representative X01–X08 positive/negative tests, and explicit handling of unlisted material intersections. Original Product Freeze accepted `J09+J10+J11+J12` as an **in-scope fail-closed L2/Release proof obligation**; that original choice remains authoritative for the original exact in-flight candidate. T12 reports `material_disposition=MATERIAL_INTERSECTION_UNKNOWN` and four negative omission oracles PASS; it has **not** demonstrated a genuine four-job same-work-subject executable positive release pathway.

Subsequent Product Authority #943@6155977141 explicitly approved **equivalent-test reuse and exclusion of very low-ROI / fringe standalone physical campaigns**, not silently changing old frozen gates to N/A or manufacturing 4-way PASS. An independent V01 Validator #1021@6162591281 identified the resulting Product/L2/Pack contradiction as one of the barriers to V01 PASS. Release §11.5 forbids **retroactive** reduction of mandatory gates on an in-flight authority-bound candidate. Therefore this packet is **prospective only**; any accepted change must materialize a new reviewed baseline/new version candidate with gate-by-subject re-evaluation.

## 2. Proposed precise Product acceptance delta (scope decision)

**Accept for a prospective successor (subject to review):**

1. **Required and unchanged:** all J01–J12 individually; all 18 S+/S−, eight representative X+/X−; all mandatory Product R01–R12; all applicable security/permission/human DENY, idempotent effect/recovery, license and consumer window duties; AND/obligation union and omission fail-closed; exact-subject/local-or-real fidelity truth. All X01–X08 must still be executed at their stated required fidelity. S08 genuine real operator DENY remains an independent real authority requirement.
2. **Conditional, prospective exclusion from only the positive physical 4-way campaign:** a newly constructed **physical, actual-release, same-work-subject** `J09+J10+J11+J12` E3 campaign may be outside the successor ADS standards-repository v4.11 acceptance envelope **ONLY IF BOTH** (a) no actually owned ADS v4.11 release workload exercises that four-job combination **AND** (b) an attributable, exact-subject L2 *and* Release owner materiality/equivalence analysis demonstrates **no novel material safety/permission/authority/currentness/side-effect predicate beyond already executed and owner-accepted current X01–X08/owner proof**. Their independent owner decisions must explicitly accept bounded residual consumer risk, observed downstream effects and any distinct unsupported deployment posture. **Missing, stale, disputed or novel predicate => `MATERIAL_INTERSECTION_UNKNOWN/HOLD`; no scope exclusion, no coverage credit, no narrowed V01 gate.** The **negative union and strict no-promotion** remain mandatory with owner-level fidelity, not metadata-only test success. This is a **possible Product scope exclusion**, not Release-owned `NOT_APPLICABLE` for any real security, Hidden, incident, license or deployment gate.
3. **Honest consumer contract:** the 4-way actual material outcome remains `MATERIAL_INTERSECTION_UNKNOWN` / `UNVERIFIED` and is **not supported as pre-authorized** by v4.11. A consumer performing the *actual* 4-way must present fresh Product/L2 and Release owner decisions, same-work-subject actor/tenant/permission/source/license/deprecation/incident/side-effect proof; otherwise `HOLD/BLOCKED`. **Under-declaration is not an escape:** if a project labels only `J09+J10+J11` but observed source/license drift makes `J12` materially applicable, the effective rule must infer the missing J12 and return 4-way `HOLD` until proof. If truly **only three jobs are applicable**, do not invent J12, but preserve the exact three-job AND and any unproved novel triple as `UNKNOWN/BLOCKED`; do not borrow a proposed 4-way exception or omit actually applicable Hidden/RQ. An Agent must derive applicable jobs from material facts, not only declared labels. The project must not claim ADS v4.11 verified or approved the real four-job positive.
4. **Forbidden economy:** a four-way actual *supported* case may not omit a constituent job gate, defer existing required release gates backwards, treat Hidden/RQ as V01 PASS, reclassify UNKNOWN as N/A, suppress a required current negative, or use one in-process fixture to impersonate a real-human/native GitHub Review/external effect.

**Expected benefit:** avoid high-cost fabricated 4-service/full-release integration merely to verify a scenario not owned by this standard-repository product; preserve tested deterministic prohibition of dangerous authorization-by-aggregation. **Risk/impact:** adopters with truly simultaneous release+incident+retirement+reuse receive only fail-closed handling, **not** a 4-way positive use-case certificate. Future releasability needs explicit named project/owner evidence or a later version-scoped campaign, with trigger: actual consumer/roadmap demand or observation of a new material intersection.

### 2.1 Negative evidence fidelity — independently reviewed minimum (F02)
  
The existing T12 runner at `scripts/test_v411_t12_abc_conformance.py` lines 1237–1285 only computes local `complete(fact_map)` metadata/work-subject checks and truthfully emits `MATERIAL_INTERSECTION_UNKNOWN`. **Those 4 omission-negative fixture passes do not execute the authoritative effective-rule/Release/effect-admission owner boundary and cannot themselves establish owner-enforced deny.** Do not relabel them as a production owner negative or as a real 4-way positive.

For any **future accepted** successor scope, require a targeted executable owner proof (or a documented, independently accepted *current* exact-subject equivalence showing the same observable admission/refusal behavior) that drives the **existing** applicable effective-rule + Release admission owner, not a duplicate test-local decision engine. Feed a single actual-work-subject set of required J09 release, J10 incident/recovery, J11 consumer/deprecation, J12 current upstream/license facts; independently drop each materially applicable predicate, replace each with stale/wrong-head or wrong-tenant/scope/actor evidence, and inject **under-declared actual J12**. Check each case is `UNKNOWN/HOLD/BLOCKED` at the owner admission boundary and that no unauthorized external effect or Release advancement occurs, with exact tool/version/actor/failure evidence; for truly 3-of-4 applicable facts require only their actual three-job union but still block any novel unproved triple. Test `PROVEN_EQUIVALENT` vs `MISSING/NOT_RUN` distinctly. If no executable owned boundary exists or current proof is not shown, the affected V01 requirement remains **BLOCKED**, even if Product excludes a standalone 4-way E3 positive campaign. **No requirement** to build a fake remote 4-service platform to satisfy this targeted negative.

### 2.2 Explicit partial-job counterexamples (F03)

| Observed facts vs declarations | Required deterministic owner outcome |
| --- | --- |
| Declared `J09+J10+J11`; material upstream revision/license changes during the same work item (thus **observed J12**) | Compute actual **4-way** union; missing current J12 source/license/permission proof or novel predicate ⇒ `MATERIAL_INTERSECTION_UNKNOWN/HOLD`, never release by a 3-way label or proposed physical-exclusion clause |
| Declared `J09+J10+J11`; **no** actual upstream/reuse fact or J12 obligation | Do **not** hallucinate J12; enforce all **three** applicable gates including valid Hidden/RQ at the appropriate release stage; an unproved materially novel 3-way case ⇒ `UNKNOWN/BLOCKED`; 4-way exemption cannot serve as 3-way proof |
| Same 4 actual jobs, only three present or fourth stale, wrong subject/actor/tenant/authority | Existing owner union MUST hold/deny with no release/effect mutation, never infer one missing job from other three PASS events |

## 3. Targeted successor edits required *after owning acceptance*

This document is **not itself** any of those accepted successor files. Do not claim the following until each subject is separately reviewed and frozen, keeping the prior frozen blob IDs in history.

| Owner | Target successor decision | Positive & negative acceptance |
| --- | --- | --- |
| **Product #943** | Reviewed **successor PRD v0.3.x** and proof-matrix scope clause: label 4-way **physical positive trial out-of-envelope, explicitly unsupported**, retain actual-material UNKNOWN and mandatory fail-closed union. Identify affected consumer and next-version revisit trigger; leave X01–X08 and S08 unchanged. | S/X same; 4-way missing J09/J10/J11/J12 cannot authorize anything; Project using full 4-way gets HOLD pending own independent proof |
| **L2 #954** | Exact L2 §10 successor allocation: single existing owner closure resolver with existing-authority **executed** negative four-way admission oracle (each omitted/stale/wrong-subject job) or keep V01 BLOCKED; local T12 `complete(fact_map)` alone is not owner proof; no 4-way hosted scenario or new scheduler/gate. | Preserves existing job-AND, identity/actor/currentness and transport; tested negative for each omission; no source-only PASS |
| **T12 #1020** | Exact registry/Pack successor as needed: do **not** delete 52 positive-negative owner assertion records; preserve `MATERIAL_INTERSECTION_UNKNOWN` and `unverified_count` for the 4-way; clearly distinguish test-only negative contract from excluded standalone real 4-way journey. | Runner's original raw successful exits retained at original SHA; new candidate targeted currentness/impact tests, no fabricated 4-way positive |
| **V01 #1021** | Independently updated current-version Gate×subject evidence/Pack **only on new lawful successor**: four-way physical trial no longer a Product-required separate positive journey, but the **actual owner-boundary** negative union check is REQUIRED_NOW (or stays BLOCKED if unproven); actual later-stage V03 Hidden/R01 RQ NOT_RUN until real execution; exact current proof and human S08 still needed. | Fresh Validator and Fresh Reviewer check delta and prior historical red ledger; V01 PASS only if **all** remaining currently required gates are proven; never retroactively PASS old candidate |
| **Release** | Authorized `RELEASE_STANDARD.md` §11.2 per-gate×new-subject applicability and §11.5 prospective migration; no batch downgrade | Original `322e868...` remains BLOCKED; new candidate's own evidence and owner decision mandatory |

### Proposed wording for each successor owner

> Only if the exact-subject L2 and Release owners confirm BOTH no actual ADS-owned four-job workload AND no novel material safety predicate beyond actually proven owner/X controls, and independently accept bounded residual consumer risk, for the v4.11 successor product envelope, the unprecedented real four-job `J09+J10+J11+J12` same-subject **positive physical execution campaign** is not a separately supported or required reference journey. Its source risk remains `MATERIAL_INTERSECTION_UNKNOWN`; the executed **owner-boundary** AND/union **omission/stale/wrong-subject negatives and fail-closed HOLD** remain mandatory (T12 local metadata tests alone are insufficient); partial three-of-four declared sets must be resolved from **observed actual job facts**. Actual consumers using this four-way case must acquire current independent applicability and material proof or remain BLOCKED. No real S/X, human DENY, current security/permission, persisted-effect, Hidden, Fresh Closeout or RQ obligation is removed by this wording.

## 4. Strict approval and restart protocol — no retroactive V01 shortcut

1. Product Owner explicitly approves **this exact narrow scope** and consumer limitation; an independent Product adversarial Reviewer checks the actual scope reduction, its negative oracle and no loophole for real deployed four-way.
2. L2 owner performs exact-current successor/independent review; T12/V01 Pack owners accept/review the changed proof boundary. Where the original frozen pack requires a stronger real witness, the old gate stays BLOCKED until that successor is legally frozen.
3. Materialize a **new exact candidate SHA/tree** (never edit original `322e868` evidence as though new). Run one `VALIDATION_IMPACT_DECISION`: carry over only unaffected executed facts with full source/toolchain fidelity, rerun affected T12/V01 oracle + currentness and the official S08 genuine-human witness. Preserve original Windows 139 script census `125 × exit0 / 14 × exit1` as historical and never relabel; owner-classified replacement test semantics require distinct Validator confirmation.
4. After distinct V01 evidence + Fresh Review, and **only if** V01 PASS on new candidate, V02 Controller freezes **that** SHA/tree; then real V03 Hidden, V04 Fresh Closeout, R01 RQ, R02 guarded main integration sequentially. Old candidate's blocked closure cannot transfer merely by ancestry.
5. If any owner rejects this change or a genuine high-impact 4-way consumer turns out to be in-scope, abandon the narrowing, keep full original obligation BLOCKED, and build one actual material same-subject witness, not 28 redundant tasks.

## 5. Review checklist (anti-overengineering)

- [ ] Product Owner approval binds this exact proposed wording and consumer impact, not just an informal “low ROI” label.
- [ ] Independent model-diverse critical challenge + deterministic source checks; human intervenes only at a real Product authority decision.
- [ ] No misleading “new Product Freeze”/V01 PASS in this proposal PR.
- [ ] Existing 52 fixture assertions and all X hard negatives preserved.
- [ ] Unknown real four-way stays UNKNOWN; any real user case gets HOLD/BLOCKED until own proof.
- [ ] Human S08 remains required and genuinely attributable; a generated `human:` string is insufficient.
- [ ] New Release subject and per-gate currentness migration respects §11.5; Hidden/RQ never inferred.
- [ ] No ancillary schema, CI, Task DAG or automation introduced merely to enable this change.

**Decision sought:** `APPROVE_NARROW_PROSPECTIVE_SUCCESSOR | REJECT_AND_REQUIRE_REAL_FOURWAY_PROOF | REQUEST_BOUNDING_REVISIONS`. An approved answer authorizes the applicable owner-specific successor review/implementation; it does not yet close V01.
