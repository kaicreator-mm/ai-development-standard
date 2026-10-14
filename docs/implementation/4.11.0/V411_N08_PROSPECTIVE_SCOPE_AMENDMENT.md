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
2. **Remove only from v4.11 product *positive executable acceptance envelope*:** a newly constructed **physical, actual-release, same-work-subject 4-way** `J09+J10+J11+J12` campaign *where no v4.11-owned deployment/recovery/retirement/upstream combination is actually executed*. It is not a required separately executed reference journey or an automatic consumer promise for v4.11. The **negative union/oracle and strict no-promotion** rule remain mandatory. This is Product scope exclusion, **not** an applicability `NOT_APPLICABLE` for real Release/Hidden/incident/license gates.
3. **Honest consumer contract:** the 4-way actual material outcome remains `MATERIAL_INTERSECTION_UNKNOWN` / `UNVERIFIED` and is **not supported as pre-authorized** by v4.11. Any downstream project doing that real combination must first provide its own current Product/L2 owners, exact actual actor/tenant/upstream/license/deprecation/incident evidence, admissible real source/negative witnesses and owning Release applicability; otherwise `HOLD/BLOCKED`. The project must not claim ADS v4.11 verified or approved that compound.
4. **Forbidden economy:** a four-way actual *supported* case may not omit a constituent job gate, defer existing required release gates backwards, treat Hidden/RQ as V01 PASS, reclassify UNKNOWN as N/A, suppress a required current negative, or use one in-process fixture to impersonate a real-human/native GitHub Review/external effect.

**Expected benefit:** avoid high-cost fabricated 4-service/full-release integration merely to verify a scenario not owned by this standard-repository product; preserve tested deterministic prohibition of dangerous authorization-by-aggregation. **Risk/impact:** adopters with truly simultaneous release+incident+retirement+reuse receive only fail-closed handling, **not** a 4-way positive use-case certificate. Future releasability needs explicit named project/owner evidence or a later version-scoped campaign, with trigger: actual consumer/roadmap demand or observation of a new material intersection.

## 3. Targeted successor edits required *after owning acceptance*

This document is **not itself** any of those accepted successor files. Do not claim the following until each subject is separately reviewed and frozen, keeping the prior frozen blob IDs in history.

| Owner | Target successor decision | Positive & negative acceptance |
| --- | --- | --- |
| **Product #943** | Reviewed **successor PRD v0.3.x** and proof-matrix scope clause: label 4-way **physical positive trial out-of-envelope, explicitly unsupported**, retain actual-material UNKNOWN and mandatory fail-closed union. Identify affected consumer and next-version revisit trigger; leave X01–X08 and S08 unchanged. | S/X same; 4-way missing J09/J10/J11/J12 cannot authorize anything; Project using full 4-way gets HOLD pending own independent proof |
| **L2 #954** | Exact L2 §10 successor allocation: single existing owner closure resolver with negative four-way union oracle; no 4-way hosted scenario created; no new scheduler/gate. | Preserves existing job-AND, identity/actor/currentness and transport; tested negative for each omission; no source-only PASS |
| **T12 #1020** | Exact registry/Pack successor as needed: do **not** delete 52 positive-negative owner assertion records; preserve `MATERIAL_INTERSECTION_UNKNOWN` and `unverified_count` for the 4-way; clearly distinguish test-only negative contract from excluded standalone real 4-way journey. | Runner's original raw successful exits retained at original SHA; new candidate targeted currentness/impact tests, no fabricated 4-way positive |
| **V01 #1021** | Independently updated current-version Gate×subject evidence/Pack **only on new lawful successor**: four-way physical trial no longer a Product-required separate positive journey, but the negative union check is REQUIRED_NOW; actual later-stage V03 Hidden/R01 RQ NOT_RUN until real execution; exact current proof and human S08 still needed. | Fresh Validator and Fresh Reviewer check delta and prior historical red ledger; V01 PASS only if **all** remaining currently required gates are proven; never retroactively PASS old candidate |
| **Release** | Authorized `RELEASE_STANDARD.md` §11.2 per-gate×new-subject applicability and §11.5 prospective migration; no batch downgrade | Original `322e868...` remains BLOCKED; new candidate's own evidence and owner decision mandatory |

### Proposed wording for each successor owner

> For the v4.11 successor product envelope, the unprecedented real four-job `J09+J10+J11+J12` same-subject **positive physical execution campaign** is not a separately supported or required reference journey. Its source risk remains `MATERIAL_INTERSECTION_UNKNOWN`; the deterministic AND/union **omission negatives and fail-closed HOLD** remain mandatory. Actual consumers using this four-way case must acquire current independent applicability and material proof or remain BLOCKED. No real S/X, human DENY, current security/permission, persisted-effect, Hidden, Fresh Closeout or RQ obligation is removed by this wording.

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
