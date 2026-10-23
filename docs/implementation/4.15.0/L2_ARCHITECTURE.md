# ADS v4.15.0 — L2 Architecture (R1 / focused Review repair candidate)

**Status:** `L2_R1_CANDIDATE / FOCUSED_INDEPENDENT_REVIEW_NOT_RUN / NOT_FROZEN`. Original [R0 independent L2 review](https://github.com/kaicreator-mm/ai-development-standard/issues/1213#issuecomment-6284889724): P0=0/P1=4/P2=5; source-author repairs are **not** a Review PASS. No Task DAG or implementation authorization.
**Frozen Product:** [#1207@6284631551](https://github.com/kaicreator-mm/ai-development-standard/issues/1207#issuecomment-6284631551), `PRD.md@fbeacd479f5a9a0d3dc1a3f853abe623cc211031`, `L1_PRODUCT_EVIDENCE.md@34a8833056e8a3e31ba2238777fde21e816ce6ac`.
**Architecture evidence / material UNKNOWNs:** [L2_ARCHITECTURE_EVIDENCE.md](L2_ARCHITECTURE_EVIDENCE.md).
**Source baseline:** v4.14.0 `main@584512e8566408bed479192753c12a036309d277`; version branch `version/v4.15`.
**Architecture scope:** ADS standards/Schema/conformance for **task-meta → GitHub** and **GitHub → Tally + feedback**; actual task-meta and Tally implementations remain in their own repos.

## 1. Context and single factual authority per boundary

```text
 actual Agent / Host / Model / Tool runtime
       │ provider hooks and source receipts (NOT Claim/Gate authority)
       ▼
 task-meta native adapter → normalized Attempt/Step/Tool/Token/Verifier/cost
       │  private store/immutable Manifest (task-meta owned; inaccessible to Tally)
       │  v4 typed/safe Report Publish / actual comment readback
       ▼
             GitHub Issue / PR / CI / Review
  - canonical native Work Item, dependency, Claim/PR/Review/CI facts
  - ADS v4 schema-validated Report comment (observational; not a Gate)
       │ native GitHub API only; version/evidence/source readback
       ▼
 Tally v2 DomainHarness C GitHub Adapter → Engineering B / selected S
       │ derived read model, Agent/Task decisions, verified feedback
       └───── v4 kind:report / EXPERIENCE_USE_FEEDBACK ───→ GitHub
```

DomainHarness's selected one K Primary governs **Domain App** state/admission/journal/external effect; actual CI/Host/GitHub own their terminal external facts. Neither ADS nor a report creates an alternative Task DAG, Agent credential, Gate verdict, business Effect permit or scheduler. A GitHub comment is a *publisher observation* until inspected with its actual owning source.

## 2. Canonical v4 wire and compatibility split (FR02 / #1205)

### 2.1 Per-kind wire compatibility — P1-1 and P2-5 resolution

**Chosen design: v4 is REPORT-ONLY.** The unchanged single first-line `<!-- ads:github -->`, single fenced YAML mapping with exactly `schema`, `kind`, `data` and human Markdown afterwards remain. A v4.15 writer **continues emitting `schema: ads/github/v3` for `work_item`, `intent` and `event`**; these are still **current executable** inputs for a v4.15 reader, subject to their original GitHub authority/Claim semantics. Only new `kind: report` uses `schema: ads/github/v4`. No previously live v3 Task Issue, Intent or Agent Event needs mutation or migration.

New `schemas/github/v4.15/report.schema.json` Draft 2020-12 is a **report-only** strict discriminated schema accepting exactly `schema: ads/github/v4` and `kind: report`. The v4.15 verifier dispatches on **both** schema identity and kind. For all non-report kinds, it uses the **original unchanged v3 root and pinned offline `$ref` registry** (Task Contract / Agent Event v2). There is **no duplicate copy** of ten Work Item profile shapes. The v3 source Schema blob `a8c5d852c239f69850e7d856af75ca8179aff1dd` remains byte-identical.

| GitHub record | v4.14 reader/agent | v4.15 reader/agent | New v4.15 writer |
| --- | --- | --- | --- |
| v3 `work_item` | current executable with native authority checks | **current executable** with same checks | **v3** |
| v3 `intent` | current admissible mutation request | **current admissible** request | **v3** |
| v3 `event` | current Agent Event v2 | **current Agent Event v2** | **v3** |
| v3 `report` | current per v4.14 pin | **historical read-only** via original v3 schema; absent new fields = `UNKNOWN/INSUFFICIENT_EVIDENCE` | no new v3 reports under v4.15 pin |
| v4 `report` | `UNSUPPORTED_SCHEMA` or clean ignore, never partial parsing or PASS | current validated *observational evidence*, not Task PASS | **v4** |
| v4 non-report or unknown pair | reject/ignore | reject `INVALID_SCHEMA/UNSUPPORTED_SCHEMA` | forbidden |

An active v4.14-pinned Agent may continue its own v3 reports without re-binding accepted Claims; mixed-pin readers must not treat unseen v4 reports as proof of success. The `latest-only` clause of Protocol §16.4 must be **prospectively narrowed in v4.15 to current accepted identity per kind and effective source pin**, while v4.14 remains exactly as qualified. This behavior/authority change requires focused compatibility tests. v4.15 historical v3 **report** reading does not enable v3 current report admission.

### 2.2 New v4 reports and complete v3 report-kind migration — P1-2

Exactly three **new v4 `data.report_kind`** profiles under the *same* outer `kind: report`:
- **`EXECUTION_SUMMARY`**: task-meta-owned Task/Attempt execution report with actor/source/coverage/verifier/cost and immutable private `manifest_ref` and SHA-256 digest, required; Tally consumes only GitHub-safe `data`.
- **`EXPERIENCE_USE_FEEDBACK`**: Tally-owned, **manifest-free** report of presented/accepted/applied/skipped/independently_checked/observed_effect with actor/Task/Attempt/procedure/source and limits; never an Agent Event or Task PASS.
- **`EXECUTION_CORRECTION`**: bounded correction/revocation **notice** targeting a prior accepted comment of the same owning Issue/report namespace and original profile/subject; cross-namespace attempted corrections are `DISPUTED/UNVERIFIED`, not automatic invalidation. A correction does **not** carry replacement execution facts; replacement requires a new revision of the source profile.

| Old v3 `report_kind` | New v4 report publication disposition |
| --- | --- |
| `EXECUTION_SUMMARY` | v4 `EXECUTION_SUMMARY` initial immutable revision |
| `EVIDENCE_UPDATE` | **new immutable revision of the same v4 `EXECUTION_SUMMARY` `report_id` and Attempt**, with updated task-meta-owned manifest/ref/digest and source-bound late CI/Host/Review verifier refs. Original revision persists. Tally may also read native late CI/Review directly; it cannot synthesize task-meta coverage. |
| `TASK_LEARNING` | Material knowledge adds a **new immutable revision** of that v4 `EXECUTION_SUMMARY`, with new task-meta manifest/digest and Task Learning v2 source ref; if no accepted summary exists, report `INSUFFICIENT_EVIDENCE` rather than invent a new profile. The separate §10 Level-1 `TASK_LEARNING=NONE_MATERIAL | ref` note is **unchanged**. |
| `EXECUTION_CORRECTION` | v4 `EXECUTION_CORRECTION` safe notice + new target-profile revision for any replacement |
| (no v3 kind) | v4 `EXPERIENCE_USE_FEEDBACK` |

The v4.15-pinned writer does **not** emit v3 report kinds; the v4.14-pinned writer/reader retains its qualified format until lawful version adoption. Ordinary late evidence is a source-bound **new revision**, not automatic `corrects_ref` invalidation; false former evidence uses correction notice and separately accepted replacement revision. Protocol §10 publication text will explicitly document the table during #1205 implementation. The same Issue/report_id/revision dedupe/readback rule applies, with no per-step GitHub spam.

### 2.3 Minimum data semantics and strictness

`report_id`, integer `revision`, `report_kind` and actual stable owner refs are mandatory. Each profile uses `additionalProperties:false`, exact type validation and source-bound field requirements. Machine parsing only reads typed `data`, not Markdown text, examples or quoted records.

**Execution summary minimum semantic groups** (L2 field naming may be refined by implementation **without changing** Product meaning; conformance fixtures freeze exact final keys before publisher adoption):

| Group | Required consumer meaning | Invalid inference |
| --- | --- | --- |
| `subject` | repository, actual GitHub Issue, Task/Run/Attempt, exact `source_sha` and immutable ADS/profile revision, source/currentness | branch `main` proves source SHA |
| `actor` | self-declared logical `operator_kind/operator_id/session_ref/role`, explicit transport actor if separately observed | same GitHub login = same Agent |
| `measurement` | bounded aggregated time/Tool/Model/token/cache/cost observations with numeric unit/currency/pricing/billing basis **per available metric**, epistemic class, missing/coverage marker and no nested double count | absent charge = 0; Agent prose = billed amount |
| `verifier` | actual verified/tested subject, CI/Host/Review refs, required checked/failed/skipped/unchecked semantic scope, strict vs partial/UNKNOWN **as report evidence claim** | valid YAML or 19/20 checks = Task/Gate PASS |
| `experience` | optional safe learning ref, task/risk/technology applicability, exclusions/counterexamples or `NONE_MATERIAL`/UNKNOWN | one historical success = universally reusable procedure |
| `manifest` | immutable stable private object ref and lowercase SHA-256 digest owned by task-meta; access/redaction classification | digest proves source admission or grants Tally private access |

**Feedback minimum:** `task_ref`, `attempt_ref`, actor/session, `experience_ref/procedure_revision`, action/observation phase, **`publisher_source_sha`** (actual Tally build), **`ads_subject_sha`** (tested frozen ADS candidate + schema identity, or exact qualified effective SHA in production), **`limits`**, actual observed-at/GitHub source refs, and independent verifier source **only if checked**. The comment's GitHub-generated ID/URL is a subsequent external receipt, never prefilled in its own body.

`COMPLETE|PARTIAL|UNKNOWN` capture coverage describes the **collector's** observed scope. `OBSERVED|SELF_REPORTED|INFERRED|UNKNOWN` qualifies **each material claim**. Task strict completion is resolved **outside** the report by existing ADS exact Task/CI/Host/Review gate authority. Safe v4 Report projection never requires raw prompts, chain-of-thought, full tool arguments, private credentials or all step spans.

## 3. Writer → GitHub → reader: observable digest, edit and correction integrity (FR03/FR04; P1-4/P2-1)

**Common public conflict comparator:** both task-meta and Tally publisher, and the GitHub-only Tally reader, deterministically compute `data_digest = SHA256(RFC8785_JCS(JSON_normalized_validated_yaml_data))`, i.e. the validated schema-compatible **`data` mapping only** canonicalized as JSON under pinned rules. Non-JSON types, NaN/Infinity, duplicate YAML keys/aliases and unsafe coercion must be rejected before JCS. Store the digest in the **actual GitHub publication/readback receipt or local derived index**, **not inside the comment's `data`** (no impossible self-hash). Identity key: `(canonical owning GitHub Issue, publisher namespace, report_id, revision, report_kind)`; same identity+digest observed twice may be deduplicated, different digest ⇒ `CONFLICT` (never last writer wins). The immutable private `manifest_sha256` of task-meta-owned execution summaries is a **separate** object integrity claim; neither feedback publisher nor GitHub-only reader needs or may retrieve its private contents.

**Publisher:** task-meta stores and reads back its immutable private source/manifest and builds one sanitized schema-valid execution Report; Tally instead publishes one manifest-free schema-valid feedback Report with its actual build/ADS candidate source. Each writer witnesses real GitHub permissions/Issue currentness, creates the comment, and readbacks GitHub ID/body + canonical data digest into its own receipt. After a lost POST ACK, search/paginate the owning Issue; same identity+digest may reuse the real comment URL, conflicting digest ⇒ `CONFLICT`, no blind duplicate. GitHub comment publication **is not atomic exactly-once** across concurrent writers; unresolved race is `UNKNOWN`. Neither a source-only schema check nor a POST 201 grants Task/Gate PASS.

**Reader edits and integrity WITHOUT private receipts:** obtain actual GitHub comment `id, created_at, updated_at` and GraphQL `lastEditedAt/userContentEdits` where available. For a witnessed in-place body edit (`updated_at > created_at` due to edit, or GraphQL edit signal) or a later observed changed `data_digest` on the **same GitHub comment ID**, mark that report `UNVERIFIED/CONFLICT`, even if its new body remains schema-valid. Treat a new accepted source-bound revision/correction as the only requalification path; never take newest timestamp as latest valid evidence. Where the original first-published digest/edits are unavailable, **do not pretend GitHub offers cryptographic immutability**; historical integrity is `UNKNOWN/INSUFFICIENT_EVIDENCE` as applicable. All these inputs are native GitHub or directly computed from its YAML; **no task-meta private receipt access**. GitHub-only reader can verify syntax, observed edits, conflicting revisions and native facts, not every hidden private source claim.

**Correction authority:** an `EXECUTION_CORRECTION` notice is valid for revocation only if its publisher namespace, owning Issue, target original `report_id` / kind / Task subject and actual prior GitHub comment reference are aligned and required admission/currentness are witnessed. Self-declared logical Agent identity alone is **not** ownership proof; same GitHub login transporting multiple logical Agents is no grant to cancel another namespace's report. Cross-namespace attempted correction ⇒ **`DISPUTED/UNVERIFIED`** notice, no automatic cancellation or promoted replacement outcome. A valid notice can invalidate the prior evidence; distinct correct facts must appear in a **new revision of the original summary/feedback profile** (new digest and real GitHub readback), not in the correction notice.

**Reader:** Tally paginates actual GitHub Issue/Dependencies/PR/CI/Review/Claim and v3/v4 Report comments, validates exact pinned per-kind schema, computes public digest, tests native edit/currentness, replay/correction namespace, source/revision and cross-credential coverage. Stale, revoked, duplicate-conflict, edit-unknown or source-unverified records stay `UNKNOWN/INSUFFICIENT_EVIDENCE`. Late real CI/Host/Review evidence can be read directly; unless task-meta actually publishes an updated summary revision, Tally cannot infer private capture was updated. Tool/Host ACK is not terminal result and telemetry is never a Gate authority.

**Sensitive comment removal:** authorized publisher may remove/redact/minimize a leaked GitHub report when GitHub permissions allow. Publish a sanitized correction/revocation tombstone referencing the former known comment identity/digest without leaking contents, respecting source namespace ownership and actual readback; fail-closed consumers invalidate the exposed data. These privacy actions may override append-only presentation, but GitHub copies/caches cannot be promised erased.

## 4. Effective ADS revision vs pre-RQ validation pin (FR06)

| Mode | Permitted source | Authority & limitations |
| --- | --- | --- |
| Effective production adoption | qualified `RELEASE_QUALIFICATION=READY`, actually main-integrated **exact 40-hex SHA**, project-local §6 reviewed/authorized compatible pin; **Tag optional** | frozen running Task/Claim pins not retroactively rebound |
| Legacy v4.12 advisory recommendation | historical selector requires tag+GitHub Release; absent tag yields `NO_SAFE_RECOMMENDATION` | this advisory output is not a veto of distinct manual qualified adoption; no silent selector change |
| Pre-RQ interoperability validation | **exact frozen v4.15 candidate SHA** resolved in isolated smoke adapter/Issue under test-only config | not a production project pin and never used to authorize an existing real Task/Claim/Effect; candidate drift forces affected E2E re-run |
| Rejected | floating `main`, unqualified SHA, semver only, unofficial v3 additional fields, stale or incompatible version | `BLOCKED/UNKNOWN`, never implicit fallback |

Prospective `PROJECT_ADOPTION.md` change scope: clarify **manual qualified main SHA** vs optional publication alias and the unchanged conservative v4.12 read-only selector. Do **not** update the selector to claim a safe recommendation without its original conditions. For J1–J6, the real task-meta writer and Tally reader execute against a bounded frozen v4.15 schema validation test subject on an isolated smoke Issue/branch; effective project pins remain unchanged. After final v4.15 RQ/main, each project may elect local compatible adoption separately. No pre-RQ circular dependency remains.

## 5. GitHub-only Tally reader and feedback writer witness (FR04 / Product P2)

**Same actual build/entrypoint (P2-2):** execute the true Tally TypeScript GitHub C-adapter reader **and the publishing path that emits `EXPERIENCE_USE_FEEDBACK`** from the same pinned source/build; record any test config differences, `publisher_source_sha` and exact frozen `ads_subject_sha` (test subject, not production adoption). No fixture-only alternate mini-reader is sufficient for E3. A feedback record must distinguish inputs derived solely from GitHub from separately source-qualified Host/runx/Kernel adapter observations; such other evidence never creates a hidden task-meta private dependency.

**Actual permissions (P2-3):** record a secret-redacted, independently verifiable *effective* permission/grant inventory for reader and feedback writer: token type, target repositories and applicable native Issue/PR/CI/Checks READ, Issue-comment WRITE when publishing, probes/currentness. Prefer least-privilege GitHub App installation token with observed installation/repository grants; an existing classic PAT may have `X-OAuth-Scopes` observable. **Fine-grained PAT effective permission grants cannot generally be read back via the API**, so mere secret-redacted token configuration is not proof; if actual grants cannot be established, classify scope proof `UNKNOWN` and do not claim a scoped-negative PASS. No broad PAT issuance is required merely to satisfy a test; user-selected authorized access applies. Never log token bytes.

**Private egress denial:** record the same reader process's environment/config allowlist and actual denied/absent task-meta API, database, SDK, object store or private Manifest endpoint/credential. Inject a private Manifest URL and task-meta API address as negative inputs; they must be refused/denied and yield `INSUFFICIENT_EVIDENCE` while GitHub-only reads work. This applies to the GitHub-only **reader/conformance surface**, not Tally's separate lawfully admitted Host/Tool/Kernel interfaces. A network deny log plus actual code-path instrumentation is stronger evidence than a self-description.

## 6. Bounded conformance layers and executable proof owners (FR07)

| Layer | ADS v4.15 conformance obligation | Real implementation / actual witness |
| --- | --- | --- |
| E1 Schema | v4 **report-only** root with typed profiles, strict parsing and JCS data digest; v3 non-report remains **current executable** across pins, v3 reports historical-only for v4, v3-only reader rejects/ignores v4 reports | ADS verifier/source tests; no GitHub mutation or Gate PASS from schema |
| E2 Publication | one real Agent + private task-meta source report → actual GitHub issue comment/receipt, fail on duplicate/stale/conflict | task-meta #3/#5/#12 source and GitHub readback; must be genuine |
| E3 GitHub-only consumer | actual Tally TS C GitHub adapter reads that report and native GitHub refs, resolves all available actor/attempt/verifier/cost or UNKNOWN, no private Manifest | Tally #62/#65 source + independently inspected credential grants/egress witness |
| E4 Reliability negatives | second/retried/corrected Attempt, failed verifier with many green checks, edited/collision/revoked report, 429/network timeout | source-bound actual affected behaviors; deterministic fakes only for unrelated failure inputs |
| E5 Usage feedback | Tally v4 manifest-free feedback → GitHub post/readback and later source-bound actual CI/Host observed-use comparison | Tally v2 actual publisher + ADS readback; no automatic Candidate activation |
| E6 Version qualification | exact frozen integration SHA/schema+external reader/publisher pins; CI and independent Review + closure/RQ | ADS #1210; missing actual external code gives **`BLOCKED/NOT_RUN`**, not scoped waiver |

At least one real Agent/Host/Task sequence is essential. Broad three-provider hook compatibility, large datasets and actual new Domain Package production deployment are explicitly NOT required in v4.15. No per-step GitHub spam or published raw telemetry.

## 7. Planned implementation seams after L2 Freeze (not yet executable DAG)

**Architecture A / #1208:** source §10 owner crosswalk + marginal observation/coverage/metrics publication semantics and fixtures, no new provider hook implementation.

**Architecture B / existing #1205:** report-only `ads/github/v4` schema + safe validator/JCS digest, preserve original v3 schema+current non-report use; v3 `EVIDENCE_UPDATE/TASK_LEARNING` map to new immutable summary revision, v3 historical reports and focused positive/negative conformance.

**Architecture C / #1209:** normative GitHub-only Tally reader/feedback with same-build and verified-grant/egress witness, JCS digest, edit/conflict and namespace-correction oracles, no Tally runtime code in ADS.

**Architecture D / #1210:** real cross-repo test contract using real task-meta and Tally code/GitHub Issue and GitHub-only credentials, release candidate and independent closure; **this cannot be marked PASS before the external slices exist**.

```text
Frozen Product + source L2
          ↓ independent Architecture Review / L2 Freeze (later)
  A reuse/capture owner ─┐
  B v4 schema/validator ├──→ C reader/feedback contract
  D adoption clarification┘         ↓
                        real task-meta+Tally external implementation
                                      ↓
                         real GitHub-only E2E / negative results
                                      ↓
                             Version Closure + Release RQ
                                      ↓
                           single version/v4.15 → main
```

The arrows are **prospective architecture dependency candidates**, not native GitHub Task Dependencies or acceptance of Builder Claims. Materialize a correct Issue Task DAG only after Architecture Freeze.

## 8. L2 independent review questions / selected risks

1. Is the per-kind × reader-pin × writer-pin choice conclusive: v3 non-report Work Item/Intent/Event **current executable** across v4.14/v4.15 pins; v4 only `kind: report`, historical v3 report read-only under v4.15; no open Task rewrite or alternate Task/Event authority?
2. Are `subject/actor/measurements/verifier/manifest/feedback` source-qualified enough for Tally to consume GitHub **without** access to private Manifest, and fail closed on missing quality/actual billing?
3. Are former v3 `EVIDENCE_UPDATE` and `TASK_LEARNING` mapped to immutable summary revisions with distinct late CI/Host provenance and unchanged Level-1 learning notes? Does candidate-as-test subject vs effective RQ-qualified main SHA avoid release loops without tag ceremony?
4. Does the credential-permission inventory require **actual grants**, plus denied private egress, satisfy R1 Product P2 without invented owner identity checks?
5. Does RFC8785 canonical `data` digest plus GitHub-native edit metadata suffice **without private publisher receipts**, and does namespace-restricted correction avoid cross-publisher cancellation under a shared GitHub login? Exercise thought probes: edited/revoked comment, lost ACK, same-ID differing digest, failed verifier, late CI and nested retries.
6. Are U1–U8 source-based architecture dispositions aligned with Stage 2.3: **U3 static-sufficient for witness design, no pre-L2 demo**, U6 BLOCKED **only for real E2/E3/E5/E6 and RQ, not L2 Freeze**, while runtime evidence stays NOT_RUN?
7. Output a source-bound verdict `L2_FREEZE_READY=YES|NO`, P0/P1/P2 and exact changes, with reviewer self-declaration distinct from author; **L2 Review input is not L2 Freeze**.

**Stage-2 R1 limitations:** no actual v4 protocol/schema implementation, no executed v4 fixture, no real external task-meta/Tally E2E, no native Task DAG and no new Product authority decision. Prior R0 independent `L2_FREEZE_READY=NO` remains historical pending independent R1 delta verdict. Source-author text changes do not prove runtime PASS.
