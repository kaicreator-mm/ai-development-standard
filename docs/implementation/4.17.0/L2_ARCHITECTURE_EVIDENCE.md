# ADS v4.17.0 — L2 Architecture Evidence R1 (protocol-first, independently reviewable)

**State:** `L2_R1_SOURCE_CANDIDATE / R0_INDEPENDENT_REVIEW_BLOCK_P1_1_P2_1 / R1_INDEPENDENT_REVIEW_NOT_RUN / L2_FREEZE_NO / TASK_DAG_NOT_ADMITTED`. R0 independent review: [#1303@6367660683](https://github.com/kaicreator-mm/ai-development-standard/issues/1303#issuecomment-6367660683). This R1 is a focused **author-side** repair, not an accepted architecture.
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

**Independent opportunity denominators (R0 review P2-01 fixed):** `D_obs_pivot` includes a source-qualified unique causal strategy-selection transition with **both** previous/current governed strategy identities (and material-difference comparison) observable under the same eligible governed scope. `N_obs_pivot` counts those opportunities with independently qualified material strategy change. By contrast, `D_obs_revisit` includes **only** a source-qualified unique *new selection opportunity* for which **a distinct earlier source-qualified visited strategy, a subsequent witnessed departure from it, and a causally known history up to this new selection** all exist, and current-vs-earlier strategy equivalence (including a nonmatch) is owner-decidable. `N_obs_revisit` counts only those `D_obs_revisit` opportunities where the selected strategy genuinely matches a prior visited/departed strategy. An initial transition A→B with no earlier departure **is not a negative in D_obs_revisit**. With fully witnessed A→B→A′, D_obs_pivot=2/N_obs_pivot=2; D_obs_revisit=1/N_obs_revisit=1 (second return opportunity only). A later fully qualified new selection that *doesn't* return to any prior departed strategy is a legitimate Revisit true negative (0/1 on its own eligible basis).

**INFERRED denominators follow the same structural distinction, without elevating hypothesis to fact:** `D_inf_pivot` requires one unique fully feature-covered causal labeler comparison with known version/revision/cohort; `D_inf_revisit` **additionally requires** an observed version/source lineage supporting the labeler's *hypothesized prior visit then departure*, full eligible selection opportunity, and revision-bounded similarity/nonmatch criteria. Their numerators count **classifier labels**, never owner-observed Pivot/Revisit. A missing earlier state/departure, unreliable causal ordering, insufficient classifier features, permission gaps, unresolved equivalence, unknown identity or contradictory source leaves the affected lane's *opportunity* **UNKNOWN and excluded from both its N and D** with excluded/eligible coverage disclosed. `D=0` on either eligible lane => `NOT_COMPARABLE`, never rate 0. All observed/inferred denominators are **separate**; neither the fact a GitHub object exists nor a labeler's confidence creates owner-qualified strategy authority.

**Identity and equivalence:** stable accepted strategy reference/revision + scope/owner; an A′ may use a different code SHA if its strategy/goal *equivalence is independently owner-qualified*. INFERRED equivalence is a classifier hypothesis bound to its revision, and is NOT owner approval. Exact canonical GitHub native source refs must be resolved before public summary; otherwise analysis remains private/UNKNOWN. `OBSERVED` vs `INFERRED` comparisons use **separate** N/D opportunity bases. No universal Pivot percentage.

Minimum conformance pairs for future shared Golden (not executed at L2):
- A(owner-X)→B(owner-Y)→A′(owner-equivalent X) with witnessed causal lineage: 2/2 Pivot and 1/1 Revisit in the *OBSERVED* eligible opportunity basis; negative: attempted code rollback without owner decision/causal source cannot prove observed Revisit.
- Actual GitHub PR/source evidence with fixed private labeler can produce a **labeled inferred** candidate, never OBSERVED; negative: revision missing, same command replay or parallel incomparable branch causes INSUFFICIENT_EVIDENCE.
- Confirmed unchanged owner-goal across version update gives fully observed Pivot **0/1**, not UNKNOWN; unobserved goal is UNKNOWN (0/0 not a zero rate).
- Actor self-report contradicts approved Product goal, or an ungraded/hidden/missing verifier outcome: do not promote; denied publication or a v4-only reader seeing a v5 observation remains RESTRICTED/UNSUPPORTED rather than public proof.

## 4. C10 correction-to-dependent-input/currentness (L2-D03)

**Source-kind-discriminated material-dependency identity (R0 review P1-01 fixed):** A derived claim/Experience suggestion/consumer context may depend only on public source premises that were **actually consumed as material inputs by the selecting consumer**. Two independent facts must be distinguished: (a) the existing GitHub/native record and source-owner truth and (b) a **witnessed Tally-local/consumer-local material-consumption edge** identifying which qualified premises influenced that particular new context/selection/promotion. The existence of a GitHub comment, matching timestamp, hyperlink or similar text does **not** witness material use. Missing/unverifiable consumer material-use attribution for a claimed material edge => `UNKNOWN/INSUFFICIENT_EVIDENCE` for a **new decision relying on that edge**, not automatic invalidation of all unrelated context.

**Identity by source kind, with only actually applicable fields:**

| Input kind | Minimum qualified identity and readback | Conditionally applicable additional identity | Forbidden requirement |
| --- | --- | --- | --- |
| Native GitHub Task/Issue/amendment/dependency/PR/Review/CI/accepted Claim/Dispatch or referenced owned Product source | Canonical repository + native object kind + actual native object ID/URI, exact applicable immutable subject/ref/commit or witnessed object-body revision/snapshot, owning authority/scope/currentness and observed lineage; native digest **only when actually available and independently witnessed**; record readback/pagination completeness for the relevant native collection | Task/Attempt/exact source SHA, parent/cause, actor/owner, comment body digest, CI run ref, approval revision **only where that native object really carries them** | Fabricating `report_id`, `publisher_namespace`, Report data-only digest or missing `Attempt` for a native PR/Review/CI/Issue; assuming mutable native text has immutable content without a witnessed snapshot |
| ADS `ads/github/v4` or `ads/github/v5` structured public Report | Canonical repository/owning Issue/native comment ref/ID plus native body or source-witnessed public data digest, **actual applicable report profile**, publisher/namespace, report kind and ID/revision, original Task/Attempt binding where that report schema actually requires it, publisher/source pin, qualified owner/currentness, full report-correction/lineage verification | Exact v5 target tuple (namespace/report identity/revision/Attempt/Task/ADS profile/native comment and data digest) **when applying a v5 correction notice**, or v4 owner-supported correction lineage | Treating a schema-valid Report alone as actual native authority, applying a foreign DISPUTE as REVOKE, or imposing v5 correction target keys on native records/historical v3/v4 records |

**Gate/read qualification:** Resolve the effective ADS/native profile *per source kind*, verify actual native ownership, object/snapshot integrity and relevant completeness before promoting a material input. If a source lacks the identity, authority, consumer-use witness or complete collection needed **for its own kind**, mark its *dependent new promotion* `UNKNOWN/INSUFFICIENT_EVIDENCE`; do not forge other-kind fields and do not block independently qualified unrelated sources. This is a reconstructible read-only assessment combining existing GitHub truth and an **application-local** material-use reference, **not** a new ADS Candidate/Claim/Report state machine, publisher API or Tally-to-task-meta private transport. A nonmaterial correction does not cascade to unrelated claims.

| Re-read of a material *consumed* premise at a **new** selection/promotion/admission checkpoint | Derived public-input qualification | What MUST NOT happen |
| --- | --- | --- |
| `VERIFIED_CURRENT`: identity/digest/source/owner complete, correction lineage checked through terminal pagination | May remain eligible for normal owning candidate assessment. Qualification ≠ Task/Review PASS or legal Tool authority. | Inferring action/effect or ignoring stronger current owner denial. |
| `VERIFIED_REVOKED_OR_STALE`: verified same-owner/source-aligned REVOKE/REDACT or superseded material source premise | Block *new* dependent adoption until reevaluated against new independent valid source. Keep old report and actual effect lineage intact. | Retroactive history rewrite, live hot-swap/rollback of running BUILD, invalidation of independent unaffected premise. |
| `UNVERIFIABLE_OR_PARTIAL`: 429/403, incomplete pagination, unavailable owner or native target, conflicting digest, incompatible ADS profile | `UNKNOWN/INSUFFICIENT_EVIDENCE` for *new* materially reliant promotion; bounded retry and owner resolution. | Turning missing history or permission denial into empty-success/currentness. |
| `FOREIGN_DISPUTED`: foreign publisher/namespace or otherwise non-authoritative DISPUTE notice | Notice **alone** never revokes verified target; record notice and check any actual material native/source conflict. | Auto-cancel cross-owner source, reconstruct historical BUILD outcome from a foreign statement. |

**Timings and source-kind negative cases:** Native PR/Review/Issue without any `report_id` remains valid input if its own native authority, snapshot and actual material-use edge are qualified. A v5 `EXECUTION_CORRECTION` target *does* require the exact target report's profile-appropriate publisher/namespace/ID/revision, Task/Attempt/native comment/source data digest. Missing material-use attribution, denied native collection or incomplete pagination => UNKNOWN, never a fabricated Report identity; a verified unrelated native premise remains unaffected. Bounded reevaluation at new material context assembly, new candidate selection/ranking/promotion and *before* later new native execution admission; no constant polling SLA implied. A previously authorized BUILD remains pinned to its own exact occurrence and actual historical effect receipts. Any new compensation/rollback requires separate existing K/Host/Task authority; no direct ADS consumer RPC. If there is a verified replacement, independently validate new source/report revision; there is no implicit cure by arrival time.

Source-only conformance pairs later: native Issue/PR/Review with no Report ID but witnessed material-use edge ACT vs same missing edge UNKNOWN; v5 correction target tuple qualified vs wrong publisher/report digest refused; sole material report revoked vs unrelated report unaffected; missing final GitHub page vs complete clean-read; true same namespace REVOCATION vs foreign DISPUTE; same already-running BUILD pin vs new admission after correction; replacement with independent verification vs self-declared correction text.

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
| `P02` C10 protocol clarification | Same GAIP file, **§16.6–16.7** only; avoid replacing P01 bytes | P01 accepted into `version/v4.17` (shared-file serialized currentness) | Source-kind-specific native vs Report identity; witnessed material-use edge; partial collection, owner correction and unaffected premise negatives / independent scoped Review | **SECOND**, normative |
| `P03` bounded Golden/reader/source conformance | Existing registered Golden/ref/test owners + scoped new assets only if evidence demands | P01/P02 source accepted | Up to 14 *planned* paired cases, reuse existing; actual tests and needed manifest coverage | **DEFER to post-protocol** |
| `P04` Integrated standards-source Release Qualification | Version/manifest/Release artifacts per version owner | P01/P02/P03 + all applicable evidence | Actual Full Regression, source CJ, Packaging, positive Hidden applicability, independent composed Review/RQ | **LATER; cannot claim Release PASS now** |

**Dependency note:** P01 and P02 touch one physical GAIP path, so even though clause ownership is disjoint they will be serialized as one concern per PR to `version/v4.17`; never parallel whole-file writes from stale base. Distinct source Review separate from Builder and from release authority. If a task is too large, split its implementation/tests, but DO NOT create duplicate public Schema families. Native Issues/Claim/Task DAG only after L2 Freeze and legality check.

## 7. Proposed Architecture Freeze acceptance (not met yet)

- Independent Architecture Reviewer must check this exact source SHA/blob vs accepted Product Freeze, cited current GAIP/v5 blobs, C08 qualifying *source* witness vs inference and actual unsupported channels, C10 source-kind-specific native-vs-Report identity, *witnessed consumer material-use edge*, corrected premise boundary and actual non-Gate nature.
- Reviewer should report P0/P1/P2 and `L2_FREEZE_READY`, including whether any material UNKNOWN requires `EXECUTABLE_DEMO_REQUIRED`.
- Product/Architecture authority must explicitly post `L2_FREEZE` on exact L2 blob/commit after an actual independent PASS; no self-review, no automatic source authority from this authored document.
- Then issue a minimal native Task DAG and separate Task/Claim admissions; do not edit GAIP normative source under this unfrozen L2.

**Current:** `PRODUCT_FREEZE=YES / L2_REVIEW=NOT_RUN / L2_FREEZE=NO / TASK_DAG=NOT_ADMITTED / PROTOCOL_IMPLEMENTATION=NOT_RUN / REAL_E2E=NOT_RUN`.

**R1 repair provenance:** focused correction of [#1303 independent R0 review #6367660683](https://github.com/kaicreator-mm/ai-development-standard/issues/1303#issuecomment-6367660683) P1-01 (kind-specific C10 identity and consumer-use edge) and P2-01 (separate observed/inferred Pivot vs Revisit opportunity denominator). No original Product, old GAIP normative bytes or schema modified by this L2 source update; an independent fresh R1 L2 delta review is required.
