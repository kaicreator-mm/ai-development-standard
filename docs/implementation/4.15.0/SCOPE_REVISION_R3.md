# ADS v4.15 scope revision R3 — ADS contracts before external implementation

**SOURCE_DRAFT / INDEPENDENT_DELTA_REVIEW_NOT_RUN / NOT_REFROZEN**.
This supersedes the **unaccepted R2 proposal only**, not the historical accepted freezes. R2's [independent review](https://github.com/kaicreator-mm/ai-development-standard/pull/1226#issuecomment-6293787398) found P0=0/P1=4/P2=3. This text is an author repair, not Review PASS.

Human direction [recorded at #1207@6293679128](https://github.com/kaicreator-mm/ai-development-standard/issues/1207#issuecomment-6293679128):

> task-meta 发布器和 Tally TS 消费链尚未实现，真实 E2E 无法通过。这个先不做，完成 v4.15 后 task-meta 和 tally 才能按规范完成

## 1. Exact subject and precedence

Predecessor version SHA: `a1c2ddd8c7f48374a3425b2e98c5b9dee798534a`; governing ADS main: `584512e8566408bed479192753c12a036309d277`.

The proposed **new Product/L2/DAG freeze subject** is this overlay's exact final Git blob, DEFERRED_E2E_ORACLE.md, SCOPE_DAG_MUTATION_PROPOSAL.json, and the following eight predecessor blobs. The separate freeze records must name the actual reviewed commit and final blobs; source files do not self-hash. The R2 proposal is excluded from new freeze authority.

| Predecessor under docs/implementation/4.15.0/ | Exact blob |
| --- | --- |
| PRD.md | `fbeacd479f5a9a0d3dc1a3f853abe623cc211031` |
| L1_PRODUCT_EVIDENCE.md | `34a8833056e8a3e31ba2238777fde21e816ce6ac` |
| L2_ARCHITECTURE.md | `cf4721a90122a9c9bad486209d478f2adf81e0dc` |
| L2_ARCHITECTURE_EVIDENCE.md | `4c280d690f087efe39a0d3d6b07860d4806b18b4` |
| TASK_DAG.md | `2de26c1f82d29ad0317b219058fe6b3a34147398` |
| PRODUCT_FREEZE.md | `82a060ce8bbe74fbf1dbb4901b8dc0cf8f56dc92` |
| L2_FREEZE.md | `928428d7fc074f17f33bb557b7a3fbaa285cfa4a` |
| TASK_DAG_FREEZE.md | `90e4bbe7154bc4228cc0d81954aba658309cfcd6` |

**Activation:** independent focused review must resolve valid blockers. A declared Product authority distinct from this author and reviewer must issue the new exact-source Product Freeze; separate declared L2 and DAG decisions must bind the same reviewed subject and appropriate upstream decisions. RELEASE_STANDARD §11.7 accepts self-declared executor attribution; this adds no account/credential or second-signature gate. Neither the human direction alone, this proposal nor a reviewer recommendation supplies those Freeze transitions.

**Precedence after activation:** only the clauses enumerated below are superseded, exclusively in their release sequencing/evidence meaning and with the stated replacements. All other clauses remain unchanged. All original normative runtime behaviors remain binding on future implementations. Historical status, review and freeze statements still describe their exact old subjects, never R3's current acceptance. Unlisted material contradictions block activation until explicitly repaired. No original frozen blob is edited.

## 2. Clause-level supersession inventory (P1-1)

Filenames resolve solely to §1 blobs. Replacement **C**: this ADS release must deliver all ADS-owned contract/conformance obligations in §3; real runtime execution is deferred to #1210, NOT_RUN, neither waived nor evidence for this ADS RQ. Replacement **P**: later integration binds qualified immutable ADS SHA as isolated test subject or lawful project-local effective adoption; pre-RQ external candidate testing is no longer required for this release. Existing pins/active Claims are unaffected.

| ID | File / precise anchor | Replacement |
| --- | --- | --- |
| P01 | PRD §1 desired outcome and flow: “one real cross-repository interoperability proof”; D01 required publication/read-feedback | ADS delivers two stable contracts plus §3 conformance and handoff. Flow is future integration design; actual execution C. |
| P02 | PRD D03 final GitHub-only credentials/egress witness sentences; D06/D07 publication/retry/edit/privacy behavior | Runtime obligations retained for #1210, execution C. Deterministic recorded-input conformance remains mandatory, not optional. |
| P03 | PRD D09 paragraph **“No circular E2E acceptance”** | P replaces pre-RQ external sequencing only; manual qualified-SHA adoption rules and compatibility proof unchanged. |
| P04 | PRD D10 entire paragraph, including “no unilateral scope shrink” | Explicit human-directed revision through §1 replaces the old external-runtime release prerequisite with C. Never label future runtime PASS. |
| P05 | PRD §3 FR01/FR03/FR04/FR05 acceptance columns (external implementation refs, “real task-meta”, “real TS Tally”, “One real feedback publication/readback”) | ADS contract/schema/fixture acceptance §3 is mandatory now; actual external code and feedback publication C. Owner refs retained in §4. |
| P06 | PRD FR06 candidate-as-test-subject requirement; FR07 real cross-project conformance | FR06 P, retaining manual adoption negatives; FR07 becomes §3 ADS conformance now with unchanged future actual oracle §4. |
| P07 | PRD §4 J1–J6 table, all positive runtime witness cells and runtime negatives | C/P; original complete table preserved verbatim in deferred oracle. Deterministic negatives remain mandatory under §3. |
| P08 | PRD §5 “one real supported Agent is sufficient” | Applies to #1210; no real external adapter prerequisite for ADS RQ. |
| P09 | PRD §6 REQUIRED_NOW paragraph, including actual J1–J6 and pre-RQ candidate E2E; following R1 status paragraph | Runtime portion C/P; all other ADS gates remain. R1 status stays historical, not new R3 status. |
| P10 | PRD §7 review items 2/3/5 and final Freeze paragraph | R3 review evaluates exact scoped delta, P and §1 activation; wire/privacy/authority floors retained. |
| L01 | L1 L1-1 “end-to-end evidence must involve actual implementations”; L1-3 J1–J3; L1-5 Q6; L1-6 bounded real smoke | C. Q6 resolved by explicit human direction plus new source-bound decisions; real journey truth unchanged. |
| A01 | L2 §4 pre-RQ interoperability table row and final candidate/adoption paragraph | P, preserving test-subject vs effective adoption isolation. |
| A02 | L2 §5 entire same-build/grant/egress witness requirement | Normative future oracle unchanged and preserved verbatim; actual execution C. |
| A03 | L2 §6 E2/E3/E5 rows, runtime part of E4, E6 including “not scoped waiver”; following “At least one real Agent/Host/Task sequence is essential” paragraph | Runtime execution C; E6 scoped ADS RQ requires §3 and all applicable ADS release gates. Essential real sequence applies to #1210; E1 and deterministic E4 must PASS. |
| A04 | L2 §7 Architecture D and external-implementation→E2E→RQ diagram | ADS contract/conformance→ADS RQ precedes separately admitted external implementation→#1210; actual runtime never PASS before code exists. |
| A05 | L2 §8 questions 3/4/6 and R1 limitations paragraph | P/C for timing only; R1 facts remain historical, no independent R3 verdict inferred. |
| E01 | L2 Evidence §A PROJECT_ADOPTION/RELEASE_STANDARD/task-meta/Tally rows' pre-RQ/runtime release effects | P/C; §11.7 is standards-contract precedent, not proof that external code executed. |
| E02 | L2 Evidence B.5 live witness, B.7 actual E2E release prerequisite, B.8 candidate pin | B.5 future behavior retained, execution C; B.7 replaced with §3 scope plus #1210 NOT_RUN; B.8 P. |
| E03 | L2 Evidence §C U3 RELEASE_BLOCKING_E2E_OBLIGATION, U5, U6 and U8 runtime dispositions/release effects | U3/U6/U8 actual runtime blocks #1210, not scoped ADS RQ; U5 P. No runtime PASS from static design. |
| E04 | L2 Evidence §C “L2 Freeze eligibility” paragraph; §D #1209/#1210 bullets | C/P timing and §1 activation; actual build/grant/egress oracle retained in #1210. |
| D01 | TASK_DAG first diagram (external prerequisite node and S05/S06); following external-prerequisite paragraph | Proposed §5 topology; external prerequisites belong to #1210 outside release path. |
| D02 | TASK_DAG S05/S06 table rows; native edge block; following dispatch-order paragraph | §5 new Task identities and explicit old→new mapping; no in-place repurposing or automatic native mutation. |
| D03 | TASK_DAG safeguard bullet 3 real smoke, bullet 5 source-only cannot substitute/unresolved S05, bullet 6 pre-RQ pin | C/P; new ADS conformance is a scoped deliverable, never a substitute PASS for actual runtime. |
| D04 | TASK_DAG final “Current state” paragraph | Old R0 status stays historical. R3 current status §1 remains unactivated until real decisions. |
| F01 | PRODUCT_FREEZE frozen decision summary runtime-E2E sentence and “L2 mandatory carry-forward” RQ sentence | Historical freeze preserved; new exact Product decision must activate C and §6 disclosure. |
| F02 | L2_FREEZE “Required later proofs” paragraph's runtime/RQ effect | Future oracle unchanged; new exact L2 decision activates C/P timing. |
| F03 | TASK_DAG_FREEZE canonical S05/S06 nodes, mandatory S05 P2-2 bullet, branch-control “E2E/RQ remains BLOCKED/NOT_RUN” | §5 new DAG decision/native transition. P2-2 actual runtime oracle retained in #1210, NOT_RUN, no longer alone blocks scoped ADS RQ. Other branch/admission controls unchanged. |

## 3. Mandatory ADS executable acceptance (P1-4)

Every ADS-owned executable check from L2 §2–§3, E1, deterministic E4 and TASK_DAG_FREEZE S02 P2-1 **must execute and PASS** against the integrated exact candidate before S05′ acceptance. Missing implementation, unsupported executable check, failure or absent evidence blocks acceptance. There is no “to the extent implemented” escape clause.

- Strict Draft2020-12 v4 report-only dispatch and all three profiles; duplicate YAML keys/aliases, unsafe tags/coercion, non-JSON and non-finite values rejected; RFC8785 JCS independently grounded vectors and data-only SHA256 digest, no self-hash.
- Summary required immutable manifest vs manifest-free feedback; typed actor/subject/coverage/measurement/verifier/experience and UNKNOWN; correction notice distinct from replacement revision.
- Original v3 schema bytes and offline refs preserved; current executable v3 Work Item/Intent/Event across pins; v3 reports historical under v4.15; v3-only refusal/ignore of v4; invalid kind/schema pairs and mixed/effective source pin negatives.
- Late v3 EVIDENCE_UPDATE/TASK_LEARNING→new immutable v4 EXECUTION_SUMMARY revision; distinct EXECUTION_CORRECTION; unchanged §10 Level-1 learning note. No inferred private capture update or invented profile.
- Recorded GitHub-shaped input decisions: Issue/publisher/report/revision/kind identity, same-digest dedupe, different-digest conflict, edit/revocation/unknown-integrity handling, cross-namespace/Issue/Task correction refusal, stale source, missing cost/verifier and strict-vs-partial semantics. Green partial checks/tool ACK never create Task PASS.
- Complete ADS-owned handoff contracts and deterministic recorded-input oracles for pagination, 429, retry/lost ACK, privacy redaction/tombstone, same-build feedback/reader and no private resolver. Fixtures never prove real HTTP/credential/external behavior.

Checks may be implemented in S02/S03/S05′ but must all be passing at S05′. Evidence names commands, true exits, source/tree and coverage. SHAPE_VALID_ONLY alone is not semantic conformance, Claim admission, Task PASS or RQ.

## 4. Named deferred real integration and retained oracle (P1-3)

**[ADS #1210](https://github.com/kaicreator-mm/ai-development-standard/issues/1210)** is the durable future real-integration owner: **NOT_RUN / not waived / not v4.15 scoped RQ evidence**. #1219 remains the old real-E2E Task identity/history; it is explicitly superseded for the version path, never rewritten into a fixture Task.

External owners: [task-meta #3](https://github.com/kaicreator-mm/task-meta/issues/3), [#5](https://github.com/kaicreator-mm/task-meta/issues/5), [#12](https://github.com/kaicreator-mm/task-meta/issues/12), [#13](https://github.com/kaicreator-mm/task-meta/issues/13), [#14](https://github.com/kaicreator-mm/task-meta/issues/14); [Tally #62](https://github.com/kaicreator-mm/tally/issues/62), [#63](https://github.com/kaicreator-mm/tally/issues/63), [#65](https://github.com/kaicreator-mm/tally/issues/65). Their Product/L2/DAG/Task authority stays local to each project.

[DEFERRED_E2E_ORACLE.md](DEFERRED_E2E_ORACLE.md) preserves original PRD J1–J6, L2 §5/E2–E6 and DAG P2-2 **verbatim** from the pinned blobs. Only old release timing is superseded by §2, never actual runtime behavior.

Exactly these external execution classes may remain NOT_RUN for scoped ADS RQ: (1) actual Agent capture/private immutable source and sanitized task-meta publication/readback; (2) same-build real TS reader+feedback writer, effective grant witness and denied/absent private egress; (3) actual POST/lost-ACK/retry/pagination/429/permission-denial; (4) remote edit/correction/privacy removal/tombstone/readback; (5) actual CI/Host/Review verifier and observed-use/effect comparison; (6) cross-project exact-build integration and optional effective adoption. ADS deterministic checks in §3 cannot be transferred into these categories to skip them.

## 5. Explicit DAG mutation proposal, not in-place Task edits (P1-2)

Propose **SUPERSEDE #1219 WITH new S05′** and **SUPERSEDE #1220 WITH new S06′**. New Issue IDs are not yet allocated. [SCOPE_DAG_MUTATION_PROPOSAL.json](SCOPE_DAG_MUTATION_PROPOSAL.json) uses dag-mutation-record-v1 as a draft with pending approval; it does not authorize or perform any mutation.

S05′: new ADS conformance/handoff Task, dependencies #1217 and #1218, required independent review/high risk, all §3 checks PASS and named #1210 handoff. Its exact Task Pack must bound source edits to justified ADS schema/script/test/protocol/reference work and v4.15 evidence, exclude external production implementations and false runtime claims.

S06′: new ADS scoped closure/RQ Task, dependency accepted S05′ (transitively S01–S04), required independent review/critical risk, all applicable ADS regression/hidden disposition/findings/currentness and exact-candidate scoped RQ. It must cite #1210 and §6 mandatory labels. Concern merges target version/v4.15; the user prohibition on main merge remains.

| Old predecessor→successor | Proposed active version edge |
| --- | --- |
| #1215→#1216 | unchanged |
| #1216→#1217 | unchanged |
| #1217→#1219 | #1217→new S05′ |
| #1218→#1219 | #1218→new S05′ |
| #1219→#1220 | new S05′→new S06′ |

After Product/L2/DAG activation, allocate new exact Task Packs/IDs and record explicit supersession lineage; rebind affected DF/MI mapping as applicable under TASK_DAG_GOVERNANCE §10A. Re-evaluate Task Pack/claim/finding currentness, preserve old claims/history, do not assume closure or reuse admission. Authorized native executor then performs the approved old→new edge transition, retaining old topology evidence; read all affected old/new blocked_by lists completely back, verify exact five-edge active graph and absence of cycles before dispatch. Missing approval/IDs/native capability/readback/mapping proof means HOLD/NATIVE_DAG_NOT_PROVEN. No native mutation has occurred in this proposal.

## 6. Mandatory disclosure, pins and later compatibility defects (P2-1/P2-2)

Following RELEASE_STANDARD §11.7's standards-contract precedent, **RQ and release notes must carry** `REAL_TASKMETA_GITHUB_PUBLICATION_NOT_PROVEN` and `REAL_TALLY_GITHUB_ONLY_READER_FEEDBACK_NOT_PROVEN`, plus other applicable existing limitations. These are truthful epistemic labels, never PASS-convertible claims or new Gate states.

After scoped ADS qualification, integration tests the qualified exact SHA as an isolated test subject or lawfully adopted project-local pin under PROJECT_ADOPTION §6/S04. Old pre-RQ external candidate testing is not required for this release. Effective pins/active Claims do not change incidentally.

Defects found during later adoption/integration route through existing INTERFACE_COMPATIBILITY_GOVERNANCE source/wire/behavior/authority procedures, a separately reviewed revision or new schema identity as required. Never mutate released v4.15 schema bytes, historical RQ or prior comments to claim retroactive compatibility. #1225 currentness/admission findings remain separately open. Product/L2/DAG authority routing is §1 (P2-3), not inferred from this author or reviewer.
