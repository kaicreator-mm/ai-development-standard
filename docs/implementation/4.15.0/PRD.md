# ADS v4.15.0 — Product Requirements (R0 / Review Candidate)

**Status:** `PRODUCT_DRAFT / INDEPENDENT_PRODUCT_REVIEW_REQUIRED / NOT_FROZEN`. This text is **not** an implementation authorization.
**Version mode:** `version/v4.15` based on current main `584512e8566408bed479192753c12a036309d277`; **one** eventual final version→main integration only after qualified Release. No direct mid-version `main` PR merges.
**Product owner intake:** [#1207](https://github.com/kaicreator-mm/ai-development-standard/issues/1207). **L1 evidence:** [L1_PRODUCT_EVIDENCE.md](L1_PRODUCT_EVIDENCE.md). Existing bounded work: [#1208](https://github.com/kaicreator-mm/ai-development-standard/issues/1208), **reuse** [#1205](https://github.com/kaicreator-mm/ai-development-standard/issues/1205), [#1209](https://github.com/kaicreator-mm/ai-development-standard/issues/1209), [#1210](https://github.com/kaicreator-mm/ai-development-standard/issues/1210).

## 1. Problem and outcome

ADS v4.14 supplied one declarative `ads/github/v3` Work Item/Intent/Event/Report carrier and shape-only validator with immutable private Task Report manifest pointer; it did **not** implement a real task-meta Report Publisher or Tally GitHub consumer. Existing `report.data` is intentionally narrow and does not by itself give Tally a guaranteed machine-readable Task/Attempt/verifier/metrics/learning summary without opening private task-meta objects.

**Desired v4.15 outcome:** two versioned, stable GitHub interface contracts and one real cross-repository interoperability proof:
```text
Agent/Host execution (actual observations)
    → task-meta capture, correlate, private immutable evidence
    → one bounded, safe ADS GitHub Issue Task Report + actual readback
    → Tally v2 GitHub-only reader (Issue/PR/CI/Review + ADS Report)
    → evidence-derived Task/Attempt/cost/quality/experience assessment
    → Tally source-qualified ADS GitHub use/outcome feedback + readback
```
ADS owns **standard and conformance**, task-meta and Tally own production code in their repositories; GitHub native authorities and DomainHarness K/remote provider effects are not duplicated.

## 2. Explicit Product decisions (proposed for Product Review)

**D01 Scope.** v4.15 is **not** the full #1199 Agent management suite or automatic Domain Package evolution. It covers required task-meta↔GitHub publication and Tally↔GitHub read/feedback. #1200/#1201/#1206 are not globally admitted. Reuse #1198/#1202 only for minimal semantics required by a real Attempt/verifier/use record.

**D02 Carrier.** The v4.14 canonical `<!-- ads:github -->` and `schema: ads/github/v3; kind: report` remain authoritative **unless** the L2 compatibility decision proves a new independently versioned machine profile indispensable. Existing `report.data` is `additionalProperties:false`; no new private fields may be smuggled into v3 YAML. The future Tally reader MUST have a deterministic, validated and privacy-safe **GitHub-visible** projection, not infer typed facts from arbitrary free-text prose. L2 may choose a bounded and demonstrably compatible Markdown profile **or** a separately versioned additive protocol via normal compatibility/Release; do not assume which before source/negative tests.

**D03 No private consumer link.** Tally MUST read **only actual GitHub** (Issue/Dependencies/Claim/PR/CI/Review/ADS comments). It MUST NOT require task-meta API/SDK/DB/raw Trace/private Manifest dereference, even if task-meta stores complete private data. Publisher may keep internal private objects. Missing GitHub-safe detail implies `INSUFFICIENT_EVIDENCE`, never an invisible private bypass.

**D04 Authority.** Telemetry is observational, and ADS schema validation produces only shape validity. GitHub owns Issue/PR/Review/CI actual facts, accepted Claim and permissions. Strict Task/Release PASS requires the existing exact-subject authoritative verifier/Gate; a tool response/ACK, completed Agent Attempt, parsed summary, or partial green checks cannot assert Task PASS. DomainHarness K, applicable C adapter and external Host keep their own actual Effect and remote completion authority.

**D05 Identity/cost.** Report distinguishes Task, Run, Attempt, self-declared logical actor/session/role, exact source/ADS pin, verifier subject/coverage, observed/inferred/self-reported/unknown measurements, duplicate and retry scopes, billed vs estimated cost; missing values remain UNKNOWN, never 0. No GitHub-transport-account operator test. Provider adapters may report a limited capture profile honestly; no universal hooks mandated.

**D06 Writer/reader resilience.** Producer uses stable Issue + report_id + revision and original digest; POST-after-commit lost ACK is reconciled by GitHub readback, not blind duplicate write. Changed payload with same identity is CONFLICT, later accepted correction cites actual `corrects_ref`. Reader handles pagination, 429/backoff, stale source, duplicate/conflicting versions, edited historical bodies and unverifiable refs without false pass or double counting.

**D07 Privacy and scale.** Public GitHub only contains a bounded sanitized per-terminal Attempt Report plus material correction/learning when necessary; no raw prompts/secrets/private chain-of-thought/high-cardinality steps or arbitrary private Manifest contents. GitHub API costs and rate limits must be measured where relevant; no per-step Issue spam.

**D08 Consumer feedback.** Tally publishes source-qualified recommendation `presented / accepted / applied / skipped / independently checked / observed effect` distinctions on a legal ADS GitHub surface referencing task/attempt/procedure/version and true CI/Host evidence. These are *derived usage observations*, not new Task/Release Gate states. `APPLIED` is not quality proof.

**D09 Compatibility & release identity.** ADS effective revision is an **exact immutable 40-character SHA**; consumers must check source/wire/behavior/authority compatibility and local adoption currentness before any effective upgrade. v4.14 has real Release Qualification and main-merge source evidence, but optional Tag/Release absent; `PROJECT_ADOPTION.md` published-stable discovery meaning must be reconciled explicitly. Product Review may approve a narrow **adoption/evidence clarification** without weakening published-stable/currentness floor, but neither a floating main nor a branch draft becomes an adopted standard.

**D10 Real integration requirement.** Source-schema conformance alone cannot close this version's **E2E acceptance**. Require an actually running supported Agent source adapter, actual task-meta Publisher, actual GitHub Issue comment/readback, and an actual Tally GitHub-only reader built/tested in its own repo. A focused minimal reader/vertical slice is enough; full Tally v2 Product delivery, all Agent adapters or Domain Package evolution are not prerequisites. If external implementations remain unavailable, **version E2E and release qualification remain NOT_RUN/BLOCKED**, not source-only PASS by scope relabeling.

## 3. Requirements with acceptance

| ID / priority | Requirement | Acceptance and owner |
| --- | --- | --- |
| FR01 P0 | Reuse ADS passive Task metadata and define normalized capture-quality/causality semantics for source Agent/Host, Task/Run/Attempt/Step/Tool/Model/Verifier, exact currentness, actor/role and retry lineage | ADS #1208 contract/negative examples; task-meta implementation #3/#2/#13; no fake OTel universality, no nested double count |
| FR02 P0 | Deterministic bounded **machine-readable GitHub-visible** Task Report consumer profile | ADS existing #1205, L2 compatibility choice and schema/protocol validation; actor/Attempt/Task/source/verifier/metrics/coverage/experience basics readable without private Manifest; unknowns explicit |
| FR03 P0 | Durable privacy-safe task-meta→GitHub publication and reconciliation contract | ADS §§10/16 reuse, typed receipt/correction/identity negative fixtures; real task-meta #5/#12 writer & GitHub comment URL with SHA currentness |
| FR04 P0 | Tally GitHub-only read, validate, reconcile and safely consume existing native facts plus Report/Task Learning | ADS #1209 normative consumer rules; real TS Tally #65/#62 GitHub Adapter; no direct task-meta link |
| FR05 P0 | Source-bound Tally→GitHub recommendation/use/outcome feedback (no authority mint) | One real feedback publication/readback; `recommended != applied != independently verified`; reuse existing ADS standard owner |
| FR06 P0 | Exact ADS adoption/publication identity and cross-version compatibility decision | Explicit current `PROJECT_ADOPTION.md` proof; tested consumer exact source/shape/semantic incompatibility and no hidden float `main` |
| FR07 P0 | Real two-direction cross-project conformance | ADS #1210 independent exact-source proof; real task-meta and Tally code/ref/test; privacy isolation / no private resolver, retry/correction/strict negative |
| FR08 P1 | Risk-proportionate independent review and version governance | Stage-1 Product Review→explicit Freeze, L2 evidence→Freeze, Task DAG/native dependencies, concern PR→version, exact regression/independent closure/RQ, one main merge |
| FR09 P1 | Bounded performance and compatibility | GitHub comment rate/size/pagination/429 failure modes, no per-tool Issue write; unsupported provider fields reported UNKNOWN |

## 4. Real critical journeys and falsifiable negatives

| Journey | Positive witness | Required negative / no-go |
| --- | --- | --- |
| J1 Agent→task-meta→GitHub | One real supported Agent Attempt with source-qualified partial/complete metric coverage, published safe Report, GitHub comment+digest readback | Provider model/cost absent must be UNKNOWN; never expose raw Trace/private Manifest |
| J2 GitHub→Tally | Reader given **GitHub-only** authorization resolves report revision, actual Task/Attempt/exact code/ADS, strict verifier and known/unknown cost, one lesson or NONE_MATERIAL | No private task-meta URL/token/Manifest read; invalid schema/subject fails closed |
| J3 corrections/retries | Lost POST ACK reconciled, correction cites accepted predecessor; no duplicate metrics when 2 Attempts or parent/child spans | Same report ID/revision with conflicting digest => conflict not last writer wins |
| J4 verifier truth | Real CI/Host/Review predicates checked for bound SHA and exact semantic requirements, Task outcome deduced by lawful owner | 19/20 passing checks or tool ACK ≠ STRICT_TASK_SUCCESS; final verifier failure remains failure |
| J5 usage feedback | Tally publishes GitHub usage evidence (shown vs applied vs checked/outcome) with source refs | Proposals and self-rated progress cannot change GitHub Task or Kernel Effect/Package acceptance |
| J6 compatibility | Both projects pin actual qualified and compatible ADS commit; one valid+one invalid wire sample | Unreleased or incompatible proposed extension never silently accepted |

## 5. Non-goals / implementation separation

- No ADS-native Agent/Host management daemon, task-meta DB/collector, Tally TS app/DomainHarness Engine, universal Agent RPC, cross-project service proxy or model training.
- No private Task Report Manifest resolution by Tally; no new ADS Account/Owner credential Gate, Task/Gate state, Event v3 or separate duplicate Task Learning schema by default.
- No rewriting frozen v4.14 files, retroactive migration of historical GitHub comments, or mandatory new Tag/GitHub Release if exact adopted source qualification can legally be proved.
- No implementation of all Claude Code/Codex/ZCode hooks as the v4.15 acceptance floor: one real supported Agent is sufficient, other adapters remain project-local.
- No automatic Experience→Domain Package BUILD or uncontrolled Harness² probe recursion in this version.

## 6. Release blockers / evidence levels

`REQUIRED_NOW` version criteria once scoped & frozen: canonical accepted PRD/L2/DAG authority, exact v4.15 wire/profile and adoption evidence, positive/negative schema/consumer conformance, **J1–J6 bounded actual producer/GitHub/consumer interoperability**, applicable visible CI, independent Review for normative/wire/authority changes, final candidate freeze, applicable hidden pack disposition, Release Qualification. Github and external consumer acceptance must show *actual* code and GitHub receipts on exact SHA. No PR/CI-only PASS as RQ.

Declared status at draft: `Product Review=NOT_RUN; Product Freeze=NO; L2=NOT_STARTED; Task DAG=NOT_ADMITTED; task-meta/Tally E2E=NOT_RUN; v4.15 Release Qualification=NOT_READY`. Existing v4.14 independent validation is **reused only for unchanged foundation**, not as proof of new functionality.

## 7. Stage 1 independent Product Review checklist / exit

Reviewer should independently read the immutable PRD/L1 blobs and `version/v4.15` HEAD, predecessor v4.14 source/Report schema and #1205/#1208/#1209/#1210, with self-declared **distinct** logical operator/context; assess:
1. Product intended user/outcome, ADS vs task-meta/Tally vs GitHub/DomainHarness owners, no duplicated authority;
2. D02 actual feasible schema/profile choices without undocumented v3 additions; D09 published-stable pin legality and backwards/current consumer impact;
3. D10 real cross-project integration as required scope vs third-party availability; no silent downgrade to fixtures;
4. privacy, retry, correction, strict-semantic verifier, cost UNKNOWN, same Github account/multiple Agents; no fabricated CI/Review/Release;
5. classification `P0/P1/P2`, `PRODUCT_FREEZE_READY=YES|NO`, exact SHA and required repairs.

Only after an independently adequate Product Review may the **declared Product authority** issue an explicit source-bound Product Freeze. **L2/DAG/Builder authorization are later separate decisions.**
