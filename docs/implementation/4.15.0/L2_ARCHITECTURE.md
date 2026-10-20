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

**Feedback minimum:** `task_ref`, `attempt_ref`, actor/session, `experience_ref/procedure_revision`, action/observation phase, actual observed-at/source refs, and independent verifier source **only if checked**. A public GitHub comment's generated comment ID/URL is **not** prefilled into its own body; it becomes an external receipt following actual POST and readback.

`COMPLETE|PARTIAL|UNKNOWN` capture coverage describes the **collector's** observed scope. `OBSERVED|SELF_REPORTED|INFERRED|UNKNOWN` qualifies **each material claim**. Task strict completion is resolved **outside** the report by existing ADS exact Task/CI/Host/Review gate authority. Safe v4 Report projection never requires raw prompts, chain-of-thought, full tool arguments, private credentials or all step spans.

## 3. Writer→GitHub→reader: idempotence, corrections and privacy (FR03/FR04)

**Publisher responsibility, task-meta:** validate source/version and redaction, privately store immutable evidence and actually readback its digest, construct v4 Report, safe YAML+full Schema check (`SHAPE_VALID_ONLY`), own Issue currentness/permission check, read prior comments for `(Issue, report_id, revision)`, then POST and re-read actual GitHub URL/body. If a timeout follows a successful POST, search/paginate/readback and **reuse** actual same-id+same-content record; conflicting same-id revision+different content is `CONFLICT`, never last-writer-wins. No exactly-once guarantee across concurrent GitHub writers; expose UNKNOWN when reconciliation unavailable. Detailed adapters/spool/trace retention are implemented **only in task-meta**.

**Tally reader responsibility:** paginated GitHub Issue + comment + PR/CI/Review/Claim/dependency facts, explicit per-project exact version resolver, safe YAML and pinned v3/v4 validators, source/currentness integrity (including eventual GitHub comment edits), deterministic report identity, revision and correction ordering, and bounded token/price/metric aggregation without retry or parent-child double count. A late revision is not current just because its timestamp is newer; accepted source refs and correction predecessor determine current evidence. A stale, missing or privacy-revoked report ⇒ `INSUFFICIENT_EVIDENCE`. Tool/host accepted ACK is not terminal effect; real Host/CI outcome readback is required for any verifier claim.

**Feedback publisher (Tally):** v4 `EXPERIENCE_USE_FEEDBACK` with GitHub-source facts, stable id/revision and subsequent real GitHub receipt; no private manifest, no Tally→task-meta RPC. `APPLIED` alone is not proof of effectiveness or requirement satisfaction.

**Privacy incident:** authorized publisher removes/redacts a mistaken sensitive GitHub comment as permission allows, never recirculates the secret in a correction. Publish a separate safe `EXECUTION_CORRECTION` tombstone naming previous known comment/owner report ref and invalidation only; reader invalidates original report after real readback. Append-oriented principle may yield to privacy/security duties; GitHub forks/caches may persist and cannot be promised removed. Edited reported body/digest or unexpected GitHub edit without matching immutable receipt ⇒ `UNVERIFIED/CONFLICT`.

## 4. Effective ADS revision vs pre-RQ validation pin (FR06)

| Mode | Permitted source | Authority & limitations |
| --- | --- | --- |
| Effective production adoption | qualified `RELEASE_QUALIFICATION=READY`, actually main-integrated **exact 40-hex SHA**, project-local §6 reviewed/authorized compatible pin; **Tag optional** | frozen running Task/Claim pins not retroactively rebound |
| Legacy v4.12 advisory recommendation | historical selector requires tag+GitHub Release; absent tag yields `NO_SAFE_RECOMMENDATION` | this advisory output is not a veto of distinct manual qualified adoption; no silent selector change |
| Pre-RQ interoperability validation | **exact frozen v4.15 candidate SHA** resolved in isolated smoke adapter/Issue under test-only config | not a production project pin and never used to authorize an existing real Task/Claim/Effect; candidate drift forces affected E2E re-run |
| Rejected | floating `main`, unqualified SHA, semver only, unofficial v3 additional fields, stale or incompatible version | `BLOCKED/UNKNOWN`, never implicit fallback |

Prospective `PROJECT_ADOPTION.md` change scope: clarify **manual qualified main SHA** vs optional publication alias and the unchanged conservative v4.12 read-only selector. Do **not** update the selector to claim a safe recommendation without its original conditions. For J1–J6, the real task-meta writer and Tally reader execute against a bounded frozen v4.15 schema validation test subject on an isolated smoke Issue/branch; effective project pins remain unchanged. After final v4.15 RQ/main, each project may elect local compatible adoption separately. No pre-RQ circular dependency remains.

## 5. GitHub-only Tally credentials, permission witness, isolation (FR04 / R1 P2-2)

The **real reader-test process** must run with only GitHub API credentials and a redacted source-bound *actual effective permission inventory*: PAT classic/fine-grained granted scopes or GitHub App repo permissions as applicable, target repos and Issue/PR/CI/checks read privileges actually exercised; feedback tests separately require Issue comment write authorization. Record how scopes/grants were verified and currentness; if provider cannot expose a concrete grant, mark `UNKNOWN` and refrain from claiming the permission-scoped negative passed. Never print raw tokens.

Provide separate capture of environment/config allowlist and **actual network egress isolation or denied/absent task-meta/private object endpoints**, not a plain assertion. Inject a negative private-Manifest URL and task-meta API address; the reader must refuse/receive denied access and return `INSUFFICIENT_EVIDENCE`, while GitHub reads succeed. These controls apply to the **GitHub-only conformance reader**; Tally's other independent Host/runx adapters are not globally forbidden from their legitimate Tool/Effect paths, which remain K-admitted and source governed.

## 6. Bounded conformance layers and executable proof owners (FR07)

| Layer | ADS v4.15 conformance obligation | Real implementation / actual witness |
| --- | --- | --- |
| E1 Schema | v4 root and typed discriminated reports; strict positive/negative, unsafe YAML rejection, v3 reader incompatibility and v4 historical read-only | ADS verifier and source tests; no GitHub mutation or Gate PASS from schema |
| E2 Publication | one real Agent + private task-meta source report → actual GitHub issue comment/receipt, fail on duplicate/stale/conflict | task-meta #3/#5/#12 source and GitHub readback; must be genuine |
| E3 GitHub-only consumer | actual Tally TS C GitHub adapter reads that report and native GitHub refs, resolves all available actor/attempt/verifier/cost or UNKNOWN, no private Manifest | Tally #62/#65 source + independently inspected credential grants/egress witness |
| E4 Reliability negatives | second/retried/corrected Attempt, failed verifier with many green checks, edited/collision/revoked report, 429/network timeout | source-bound actual affected behaviors; deterministic fakes only for unrelated failure inputs |
| E5 Usage feedback | Tally v4 manifest-free feedback → GitHub post/readback and later source-bound actual CI/Host observed-use comparison | Tally v2 actual publisher + ADS readback; no automatic Candidate activation |
| E6 Version qualification | exact frozen integration SHA/schema+external reader/publisher pins; CI and independent Review + closure/RQ | ADS #1210; missing actual external code gives **`BLOCKED/NOT_RUN`**, not scoped waiver |

At least one real Agent/Host/Task sequence is essential. Broad three-provider hook compatibility, large datasets and actual new Domain Package production deployment are explicitly NOT required in v4.15. No per-step GitHub spam or published raw telemetry.

## 7. Planned implementation seams after L2 Freeze (not yet executable DAG)

**Architecture A / #1208:** source §10 owner crosswalk + marginal observation/coverage/metrics publication semantics and fixtures, no new provider hook implementation.

**Architecture B / existing #1205:** new `ads/github/v4` canonical root/typed report Schema and safe validator, old v3 frozen, runtime-independent positive/negative fixtures, v3/v4 compatibility and adoption guidance.

**Architecture C / #1209:** normative Tally reader and feedback profile, actual GitHub permission/egress witness contract, correction/replay/version/currentness oracles, no Tally runtime code in ADS.

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

1. Does the single v4 report kind-family provide **both** typed execution summary and manifest-free feedback while preserving v3 unchanged and existing Agent Event v2/Task authority? Are explicit report `report_kind` profiles and correction minimal rather than duplicating Task Learning, Event or stored Task State?
2. Are `subject/actor/measurements/verifier/manifest/feedback` source-qualified enough for Tally to consume GitHub **without** access to private Manifest, and fail closed on missing quality/actual billing?
3. Do v4 reader historical v3 semantics and candidate-as-test subject vs qualified effective main SHA avoid compatibility/regression and RQ acceptance loops? No tag ceremony or silent relaxation of old selector.
4. Does the credential-permission inventory require **actual grants**, plus denied private egress, satisfy R1 Product P2 without invented owner identity checks?
5. Do edited/revoked comments, lost ACK, conflicts, missing verifier, late delivery, nested retry metrics and same GitHub login multiple sessions avoid false PASS or duplicate effects?
6. Are U1–U8 evidence strengths, required demo ownership and genuine external implementation blockers honestly dispositioned? Does the architecture demand a new pre-L2 spike or can real E2E remain a later required Product acceptance? Missing source/schema/real credentials cannot be represented as PASS.
7. Output a source-bound verdict `L2_FREEZE_READY=YES|NO`, P0/P1/P2 and exact changes, with reviewer self-declaration distinct from author; **L2 Review input is not L2 Freeze**.

**Stage-2 R0 limitations:** no actual v4 protocol/schema implementation, no executed v4 fixture, no real external task-meta/Tally E2E, no native Task DAG and no new Product authority decision. L2 review must not make any of those claims.
