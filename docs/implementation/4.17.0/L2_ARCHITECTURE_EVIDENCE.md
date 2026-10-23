# ADS v4.17.0 — L2 Architecture Evidence R0 (protocol-first, independently reviewable)

**State:** `L2_R0_SOURCE_CANDIDATE / INDEPENDENT_ARCH_REVIEW_NOT_RUN / L2_FREEZE_NO / TASK_DAG_NOT_ADMITTED`.
**Frozen Product authority:** [#1279 Product Freeze #6367139000](https://github.com/kaicreator-mm/ai-development-standard/issues/1279#issuecomment-6367139000), binding `version/v4.17@767b4762fd580362336fadc351eb274e864d24c9` with Product L1 blob `2604de7d080939839a8fc5fc382c13c09b65a823` / PRD blob `ac49dcf73821bdb80d5fcb4236e487689eea247f`; independent Product R2 Reviewer [#1300@6365932903](https://github.com/kaicreator-mm/ai-development-standard/issues/1300#issuecomment-6365932903) P0/P1/P2=0.
**Qualified predecessor:** `main@718fb02e33b31f568736447b2b905883cc6fcc3a`, `VERSION=4.16.0`, release-qualified candidate tree `719860da1dbd4950acb807b9194ae5fdf892bb04`; [#1271 final closure](https://github.com/kaicreator-mm/ai-development-standard/issues/1271#issuecomment-6366991440).
**Normative source owner:** `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`, inherited blob `dac829232919d495faf8af2d416f4eaaf48f66bf` (§10 Level 3 and passive metadata, §16.6–16.7). Existing strict public v5 `schemas/github/v4.16/report.schema.json` blob `7478313cc006162432649d734e59c5cd77db5106` MUST remain byte-identical; v3/v4 historical wire unchanged.

## 1. Decision scope — standards protocol before fixtures or runtimes

**Decision L2-D01:** v4.17 modifies **only interpretation semantics in the existing GitHub Agent Interaction owner**, not transport or state-machine shape. Deliver two separable narrow normative amendments:
- **C08 / #1287 / GAIP §10**: optional read-only, source-qualified trajectory-analysis convention; distinguish OBSERVED strategy-owner decisions vs INFERRED classifier diagnostics, causal Transition, Pivot/Revisit and comparable numerator/denominator/capture coverage; current authority/Gate unaffected.
- **C10 / #1296 / GAIP §16.6–16.7**: bounded public-input identity and *material prospective dependency* currentness/requalification when accepted owner notice/source correction changes a consumed premise. Tally derived Candidate decisions remain Tally-owned; actual BUILD, K/Host effects and native Claim remain under current execution owners.

These two normative text deltas are version value. **C01/C02/C05** are CLOSE_WITH_REFERENCE without source rewrite. **C03/C04/C06/C07/C09/C11/C12** use existing owners and bounded Golden/test examples *after protocol text*. At most 14 paired positive/negative scenarios is a planning cap, NOT a universal Gate, Task test-count mandate or permission to skip an existing mandatory Release Gate.

## 2. Existing owner and dataflow boundaries (no new wire)

```text
GitHub native Task / accepted Product / PRD or Task amendment / PR / CI / Review
      + actual source and verifier/Build/Host receipts where observable
      | exact immutable scope, source, native ID, owner, integrity, lineage
      v
Existing GAIP §10 Level 3 source-qualified read-only join/analysis
   ├─ OBSERVED: verified owning strategy/goal selection with causal version chain
   ├─ SELF_REPORTED: actor assertion, never upgraded by a native comment alone
   ├─ INFERRED: source-referenced classifier label (revision, cohort, coverage)
   └─ UNKNOWN: missing/unverifiable order/source/currentness/permissions
      |
      v
Optional evidence-qualified diagnostic or existing public ADS report/feedback
ONLY if its effective pinned v3/v4/v5 profile and clearance actually permit it
      |
      v
Tally C GitHub-only reader => local B/S advisory candidate/context requalification
      |
      v
Separate Task/Claim/Dispatch/K/Host authorities => optional actual effect
      |
      v
Existing Experience Use Feedback and native GitHub readback/independent verifier
```

Hard boundaries:
1. An existing **native GitHub Issue/Task amendment**, authoritative Product/PRD, approved Skill/Procedure revision or equivalent accepted owner decision can carry an *observed owner-goal selection* via **existing prose/source-qualified references**; the mere presence of a comment or a diff does not establish its authority. `StrategyCandidateRef` is a **logical Level 3 pointer**, not a normative publication field. No required hook or per-task telemetry.
2. Actual public source refs/feedback are native GitHub only for Tally, with §16.6 complete bounded pagination, native ID/body/digest and owner verification. Tally must not fetch task-meta raw private Trace/manifest/DB/API.
3. No `ads/github/v6`, new `report_kind`, new correction `enum`, implicit opt-in v5 migration or public raw classifier metadata fields. C08 analytical labels may remain in private/offline assessment; publication uses only *existing* cleared compatible profiles, otherwise `UNSUPPORTED/UNKNOWN/NOT_PUBLISHED`. The 4 C10 source statuses below are **analysis labels**, not additions to wire.
4. Positive lawful ACT through existing authorized Claim/Tool remains possible. Review/Validation/Release PASS or K admission cannot be granted by Level 3 inference, Tally selection or a Shape-valid report.
5. Existing source owner and §16.7 currentness/privacy constraints control original and corrected report identity. Historical refs/BUILD/effect receipts never change retroactively.

## 3. C08 source-qualified counting contract (L2-D02)

Define a **qualified VersionState** as one immutable observed version/source identity plus governed goal/strategy scope *where available*, and separately a classifier feature snapshot when only inference is permitted. Causal `Transition` requires unique operation identity and witnessed antecedent/dependent edge. Dedupe repeated delivery by native owner+operation/source occurrence; do not impose an order on truly concurrent incomparable branches.

| Lane | Positive admission | Comparable denominator (scoped and separately tracked) | Forbidden escalation |
| --- | --- | --- | --- |
| `OBSERVED` | Accepted owner-governed **before/after strategy/goal identity** and strategy equivalence (for revisit), same governed scope, actual causal source chain, source integrity/currentness | Unique fully qualified transition opportunities with both strategy identity/equivalence basis observable. Pivot numerator = witnessed material strategy change; Revisit numerator = genuine owner-qualified return after witnessed departure. | Source code diff, model speculation, self-report, ungraded rollback or parallel timestamps cannot masquerade as owner-approved Pivot/Revisit. |
| `INFERRED` | Actual native GitHub refs, lawful source/causal lineage, fixed classifier/labeler revision, comparison cohort/window, capture profile, counterevidence and uncertainty, privacy clearance where public | Unique feature-covered classifier-eligible causal opportunities within **one** declared cohort/labeler version; numerator = source-cited positive **labeler diagnosis** (not actual observed strategy). | Mixing with observed counts; labeling missing events as negatives; comparing incompatible labeler revisions; unqualified efficacy/ranking/Task PASS. |
| `SELF_REPORTED` | Faithful actor attribution as an assertion | **Never included as independent OBSERVED counts**; any optional separate self-report analysis must disclose claim basis | Self-description can't override observed owner intent. |
| `UNKNOWN` | Missing source/lineage, wrong pin, unobserved intermediate, conflicting evidence, denied privacy or absent necessary classifier features | **Excluded from both numerator and denominator**, with unknown/opportunity coverage reported; denominator=0 → `NOT_COMPARABLE` | Treating absent data as 0% or using an aggregate without denominator/currentness. |

**Identity and equivalence:** stable accepted strategy reference/revision + scope/owner; an A′ may use a different code SHA if its strategy/goal *equivalence is independently owner-qualified*. INFERRED equivalence is a classifier hypothesis bound to its revision, and is NOT owner approval. Exact canonical GitHub native source refs must be resolved before public summary; otherwise analysis remains private/UNKNOWN. `OBSERVED` vs `INFERRED` comparisons use **separate** N/D opportunity bases. No universal Pivot percentage.

Minimum conformance pairs for future shared Golden (not executed at L2):
- A(owner-X)→B(owner-Y)→A′(owner-equivalent X) with witnessed causal lineage: 2/2 Pivot and 1/1 Revisit in the *OBSERVED* eligible opportunity basis; negative: attempted code rollback without owner decision/causal source cannot prove observed Revisit.
- Actual GitHub PR/source evidence with fixed private labeler can produce a **labeled inferred** candidate, never OBSERVED; negative: revision missing, same command replay or parallel incomparable branch causes INSUFFICIENT_EVIDENCE.
- Confirmed unchanged owner-goal across version update gives fully observed Pivot **0/1**, not UNKNOWN; unobserved goal is UNKNOWN (0/0 not a zero rate).
- Actor self-report contradicts approved Product goal, or an ungraded/hidden/missing verifier outcome: do not promote; denied publication or a v4-only reader seeing a v5 observation remains RESTRICTED/UNSUPPORTED rather than public proof.

## 4. C10 correction-to-dependent-input/currentness (L2-D03)

**Dependency graph:** a derived claim/Experience suggestion/consumer context may depend only on the actually **consumed material source claims**, each named by repository + canonical Issue/native comment ID+URL/data-only digest + originating publisher/report ID/revision/namespace + Task/Attempt + ADS effective pin/profile + source authority/currentness and relevant verified predecessor lineage. This is a reconstructible reader assessment of the existing GitHub truth, **not a new ADS Candidate/Claim state machine**. A nonmaterial correction does not cascade to unrelated claims.

| Re-read of a material *consumed* premise at a **new** selection/promotion/admission checkpoint | Derived public-input qualification | What MUST NOT happen |
| --- | --- | --- |
| `VERIFIED_CURRENT`: identity/digest/source/owner complete, correction lineage checked through terminal pagination | May remain eligible for normal owning candidate assessment. Qualification ≠ Task/Review PASS or legal Tool authority. | Inferring action/effect or ignoring stronger current owner denial. |
| `VERIFIED_REVOKED_OR_STALE`: verified same-owner/source-aligned REVOKE/REDACT or superseded material source premise | Block *new* dependent adoption until reevaluated against new independent valid source. Keep old report and actual effect lineage intact. | Retroactive history rewrite, live hot-swap/rollback of running BUILD, invalidation of independent unaffected premise. |
| `UNVERIFIABLE_OR_PARTIAL`: 429/403, incomplete pagination, unavailable owner or native target, conflicting digest, incompatible ADS profile | `UNKNOWN/INSUFFICIENT_EVIDENCE` for *new* materially reliant promotion; bounded retry and owner resolution. | Turning missing history or permission denial into empty-success/currentness. |
| `FOREIGN_DISPUTED`: foreign publisher/namespace or otherwise non-authoritative DISPUTE notice | Notice **alone** never revokes verified target; record notice and check any actual material native/source conflict. | Auto-cancel cross-owner source, reconstruct historical BUILD outcome from a foreign statement. |

**Timings:** bounded reevaluation at new material context assembly, new candidate selection/ranking/promotion and *before* later new native execution admission; no constant polling SLA implied. A previously authorized BUILD remains pinned to its own exact occurrence and actual historical effect receipts. Any new compensation/rollback requires separate existing K/Host/Task authority; no direct ADS consumer RPC. If there is a verified replacement, independently validate new source/report revision; there is no implicit cure by arrival time.

Source-only conformance pairs later: sole material report revoked vs unrelated report unaffected; missing final GitHub page vs complete clean-read; true same namespace REVOCATION vs foreign DISPUTE; same already-running BUILD pin vs new admission after correction; replacement with independent verification vs self-declared correction text.

## 5. Architecture UNKNOWN matrix and decision

| High-impact question | Disposition | Current source/negative evidence | Consequence for Stage 2 |
| --- | --- | --- | --- |
| Can an observed strategy carrier exist without a new v5 field? | `STATIC_EVIDENCE_SUFFICIENT` for optional normative **interpretation only** | Already lawful native Task/Product/PRD/owner-approved strategy/procedure source facts, and GAIP §10 Level 3 per-claim OBSERVED; accepted decision+native lineage required. **Actual Task availability remains UNKNOWN** and no real positive Pivot sample claimed. | No mandatory wire migration; Golden must test supplied *qualified* source carrier and denial for a bare comment. |
| Can a source diff be used as real Pivot proof? | `STATIC_EVIDENCE_SUFFICIENT`: NO | Existing per-claim epistemic classification prohibits inferring owner decision from comment/diff. Optional labeled INFERRED diagnostics must stay distinct. | Do not implement a scorer or false OBSERVED default. |
| Must Tally add a public Candidate state or private task-meta connector for correction propagation? | `STATIC_EVIDENCE_SUFFICIENT`: NO | §16.6 consumer readback/correction/feedback already, Tally #71 future local derived invalidation; native effects in EXECUTION_ARCHITECTURE | Amend source-qualification semantics only. |
| Would a new strict Report wire or controlled behavior migration be necessary? | `STATIC_EVIDENCE_SUFFICIENT`: NO for agreed text-only scope | Current v3/v4/v5 Schema validates existing projections, new labels are Level3 analytical concepts and NOT published fields. | Byte-pin schemas; older v4 reader MUST treat v5 unsupported rather than empty. |
| Do live producers/consumers support enough observability and secure actual GitHub E2E? | **`STATIC_EVIDENCE_SUFFICIENT` for this normative source-only architecture; external runtime feasibility/coverage remains `UNKNOWN` and explicitly OUT_OF_SCOPE** | Actual task-meta/Tally #1210, Host #1231 and controlled publishing permission not proven by L1/L2; no broad runtime positive witness here. | Do not assert runtime implementation PASS or a live C08 metric; downstream Test/Release qualification is a separate owner. |

No `EXECUTABLE_DEMO_REQUIRED` is established for the **source-only language-neutral semantic clarification**: existing normative owner and schema facts plus bounded positive/forbidden cases suffice to choose an architecture; if independent Architecture Review identifies an unresolved *material* source feasibility hypothesis, change its disposition and create a scoped Architecture Research Demo before L2 Freeze. Do not call a source-only fixture a live external service test.

## 6. Source write-set and sequential concern DAG proposal (**NOT YET ADMITTED**)

| Planned work item | Allowed file/semantic slice | Depends on | Test/Review intention | Priority this version |
| --- | --- | --- | --- | --- |
| `P01` C08 protocol clarification | `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` §10 only | Frozen Product + approved L2/DAG | Relevant source-positive/forbidden local assertion + independent scoped source Review on exact PR H | **FIRST**, normative |
| `P02` C10 protocol clarification | Same GAIP file, **§16.6–16.7** only; avoid replacing P01 bytes | P01 accepted into `version/v4.17` (shared-file serialized currentness) | Correction identity, partial read, owner invalidation negative / independent scoped Review | **SECOND**, normative |
| `P03` bounded Golden/reader/source conformance | Existing registered Golden/ref/test owners + scoped new assets only if evidence demands | P01/P02 source accepted | Up to 14 *planned* paired cases, reuse existing; actual tests and needed manifest coverage | **DEFER to post-protocol** |
| `P04` Integrated standards-source Release Qualification | Version/manifest/Release artifacts per version owner | P01/P02/P03 + all applicable evidence | Actual Full Regression, source CJ, Packaging, positive Hidden applicability, independent composed Review/RQ | **LATER; cannot claim Release PASS now** |

**Dependency note:** P01 and P02 touch one physical GAIP path, so even though clause ownership is disjoint they will be serialized as one concern per PR to `version/v4.17`; never parallel whole-file writes from stale base. Distinct source Review separate from Builder and from release authority. If a task is too large, split its implementation/tests, but DO NOT create duplicate public Schema families. Native Issues/Claim/Task DAG only after L2 Freeze and legality check.

## 7. Proposed Architecture Freeze acceptance (not met yet)

- Independent Architecture Reviewer must check this exact source SHA/blob vs accepted Product Freeze, cited current GAIP/v5 blobs, C08 qualifying *source* witness vs inference and actual unsupported channels, C10 consumer/native authority/corrected premise boundary and actual non-Gate nature.
- Reviewer should report P0/P1/P2 and `L2_FREEZE_READY`, including whether any material UNKNOWN requires `EXECUTABLE_DEMO_REQUIRED`.
- Product/Architecture authority must explicitly post `L2_FREEZE` on exact L2 blob/commit after an actual independent PASS; no self-review, no automatic source authority from this authored document.
- Then issue a minimal native Task DAG and separate Task/Claim admissions; do not edit GAIP normative source under this unfrozen L2.

**Current:** `PRODUCT_FREEZE=YES / L2_REVIEW=NOT_RUN / L2_FREEZE=NO / TASK_DAG=NOT_ADMITTED / PROTOCOL_IMPLEMENTATION=NOT_RUN / REAL_E2E=NOT_RUN`.
