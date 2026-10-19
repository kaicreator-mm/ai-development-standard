# Agent Task Execution Metadata — Collection, Storage & Use Standard

Status: **Normative — prospective source-only ADS extension**. This document is a standard for *future* consumers; it does not assert that any provider hook, collector, plugin, monitoring platform, hosted trace backend, historical-version adoption, or live evaluation exists.

## 1. Purpose and authority

This standard defines a **passive, provider-neutral engineering evidence plane** for one Agent's or multiple Agents' work on a Task. It defines **WHAT** information is worth recording, **HOW** observations are admitted/correlated, **HOW** collected data are logically stored and retained, and **HOW** the resulting information may be used for engineering learning and bounded Agent effectiveness analysis.

The ADS repository defines only contract semantics. A separate implementation project may implement connectors, hooks, CLI/IDE plugins, buffering, OTel ingestion, SQLite/Postgres indexes, storage, aggregation, UI and scheduled analysis. None of those implementations are present or authorized by this standard. This is **not** a new workflow or independent state/evidence/permission authority.

Existing canonical owners are preserved:

| Subject | Existing authority that MUST prevail |
| --- | --- |
| Work Item, Task DAG and Claim/Dispatch | `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, `TASK_DAG_GOVERNANCE_STANDARD.md`, `EXECUTION_ARCHITECTURE_STANDARD.md` |
| Logical operator, Issue note, canonical agent event | `GITHUB_AGENT_INTERACTION_PROTOCOL.md` and `schemas/agent-event-v2.schema.json` |
| Agent-to-agent correlation/transport | `schemas/interchange-envelope-v1.schema.json` (correlation only) |
| Validation/CI/Review/Release truth | `VALIDATION_STANDARD.md`, `CI_EVIDENCE_STANDARD.md`, Review and Release owners |
| Runtime after deployment, Incident and Skill | `OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD.md`, `INCIDENT_RECOVERY_FEEDBACK_STANDARD.md`, `SKILL_PROCEDURE_GOVERNANCE_STANDARD.md` |
| Task Learning / Agent capability | `schemas/task-learning-v1.schema.json`, `schemas/task-learning-v2.schema.json`, `schemas/agent-capability-profile-v1.schema.json`, `schemas/agent-capability-evidence-v1.schema.json`; `EXECUTION_ARCHITECTURE_STANDARD.md` §30 |
| Standards evolution | `DEVELOPMENT_WORKFLOW.md` §8; observations cannot approve or mutate standards |

An observation may **link to** these owners; it MUST NOT reissue their canonical events, rename their Gate states, redefine Agent identity or assert source/validation/review/release truth from an Agent's narration. Introducing a future mandatory machine wire schema or registering a new machine family requires separate scoped Product/compatibility/manifest approval; the field tables here define the **semantic minimum for adapters and consumers**, not a new event-v3 or mandatory JSON format.

## 2. Collection profile and measurement truth

A collector declares its own versioned **capture profile**: identity/source discovery coverage, supported event classes and fields, source API/hook/SDK/OTel capabilities, permissions/privacy scope, sampling/drops, whether each measurement is provider-billed, provider-reported, OS-measured, adapter-derived or self-reported. `SUPPORTED` means the instrumentation can emit the field, **not** that each event was actually observed.

The default is **low-cost metadata-only**: collect existing durable Task/PR/CI refs, minimal activity transitions and non-sensitive measurement summaries. No project must capture prompts, tool arguments/results, full transcripts, proprietary model reasoning, private chain-of-thought, hidden evaluation cases, proprietary contents or secrets. These are **not** part of the ordinary collection contract. A source lacking hooks may still provide bounded GitHub/CI/Issue/CLI evidence; its per-step, model-call and token fields remain `UNKNOWN` rather than guessed.

### 2.1 Three logically separate evidence layers

| Layer | Subject | Source-of-truth posture |
| --- | --- | --- |
| **Canonical engineering facts** | GitHub Issue/PR/Claim, exact Git source, CI/Validation/Review/Release results | Read through their original authority, never replaced by a collector |
| **Execution observations** | Agent sessions/attempts/steps, model/tool calls, retries, timings, measured usage, source errors | Passive measurements with exact originating source/capability/coverage |
| **Derived analysis** | task lessons, cause clusters, comparative metrics, cost/quality patterns, prevention proposals | Recomputable projections with cited evidence, no automatic normative effect |

Absence of an observation means **not observed**, never that an operation did not occur; a missing observer cannot declare `NOT_APPLICABLE` for another authority's required validation.

## 3. WHAT to collect: minimum correlation and optional signal catalog

### 3.1 Common logical observation envelope

Every normalized **material observation** accepted for future aggregation MUST preserve, or explicitly mark unresolved, these concepts (field names are **logical**, not mandatory new schema keys):

| Concept | Definition / absence |
| --- | --- |
| `observation_id` | Stable idempotency key, namespaced by capture source + source run/event identity; do not deduplicate merely by timestamp or content |
| `source` | collector/adapter id and revision, upstream kind (native hook/SDK/OTel/CLI/GitHub/CI/Issue/manual), upstream event/ref + stable scope, mapping semantic-convention revision |
| `time` | source event timestamp and ingestion timestamp with timezone/precision, plus source duration/monotonic clock provenance where available |
| `work_context` | repository/work-item ref, current task/PR exact source, effective immutable ADS pin **when known and source-verified** |
| `attempt_context` | accepted `dispatch_id` + accepted Claim/Attempt ref when actually resolved; Agent session and parent/child execution relationship |
| `actor_context` | **self-declared** `operator_kind/operator_id/session_ref/role`; GitHub transport actor is separate; model/provider/profile and environment are extra provenance only |
| `operation` | operation class and source/native event name; optional trace/span/parent span ids, step/call id, correlation and causation refs |
| `outcome` | observed completion/error/cancel/timeout/blocked/unknown at this operation's scope; never canonical Gate PASS from tool success |
| `evidence_class` | `OBSERVED | SELF_REPORTED | INFERRED | UNKNOWN` **per claim** and source/ref/capture method; one record may contain mixed classes |
| `integrity_and_coverage` | payload digest/ref where applicable; source completeness, known sampling/drops, unavailable fields, stale/unresolvable references |
| `privacy_class` | `PROJECT_PRIVATE | RESTRICTED | PUBLISHABLE` as established by the source owner; missing public clearance does not imply publishable |

Never invent a missing `dispatch_id`, `operator_id`, Task link, current SHA, model, elapsed time, cost or source-run identity. An unbound hook event MAY be retained as a **private uncorrelated observation** for later reconciliation, but MUST NOT be attributed to a Task/Agent by a speculative nearest timestamp or GitHub login. If corrected later, preserve the original observation and add a source-linked binding/correction rather than rewriting history.

### 3.2 Capture classes and materiality

| Class | Collect when actually available | Not implied |
| --- | --- | --- |
| **Identity and workflow links** | project/Task/Issue, accepted Claim/Dispatch, attempted role/session, PR/HEAD, version pin, parent/child/attempt/retry/supersession links | local READY/Claim authority |
| **Execution steps** | attempted/finished phase, operation type, start/end/duration, status, tool/Skill name & version, retry and error class, external action boundaries | that every reasoning step or tool is visible |
| **Model routing and usage** | provider + actual model/revision when exposed; inference request id, route/escalation/fallback, observed input/output/cache tokens and provider billing identifier | full token coverage, guaranteed billing equality or model quality |
| **Tool and environment** | source-qualified tool calls, success/failure, latency, command/exit *metadata* (not secret command content), runner/environment/host class, actual measured CPU/memory/network when exposed | successful Task, healthy production or permitted side effect |
| **Engineering artifacts and outcomes** | exact commit/PR, code/test/Review/CI/Host refs, actual skipped tests/gates, reopened/follow-up issues, defects and external blockers | passing full regression/Hidden/Release |
| **Human-readable decisions** | Issue Level 1 `DECISION/EXECUTION/REUSE/EVIDENCE/LIMITS/TASK_LEARNING`; meaningful alternatives, troubleshooting outcome and limitations | private chain-of-thought or independently proven claims |

Agent roles can report materially different evidence: Builder reuse/implementation choices; Reviewer challenge, finding and blind spot; Validator performed/skipped checks and environmental scope; Planner/Architect constraints and selected alternatives. Use *existing* corresponding canonical objects for formal Review/Validation/Task result.

### 3.3 Measurement definitions and cost truth

- **Time:** keep observed elapsed wall duration of each operation, its start/end or equivalent native timing origin, unit, and clock source. Sum **only disjoint intervals**. Parent/child spans, concurrently running workers, retries and multi-step idle/wait time MUST NOT be double-counted as wall time or agent active time. Distinguish Task wall time, Agent active time, model latency, tool latency, CI queue/execute time, and Host time; missing clocks/late delivery make the relevant value `UNKNOWN`.
- **Model tokens:** record source terminology/definition plus normalized input/output and cache-hit/cache-creation counts **only when supported**; cached/reasoning subdivisions may already be included in provider input/output totals. Never add nested subcounts to inclusive totals. Streaming chunks and retried requests are not independent successful completions by default; bind provider request/attempt identity. Estimated tokenizer counts are labelled `INFERRED`, never provider-billed.
- **Money:** record actual billed amount/currency/billing period and source, **or** derived estimate with effective pricing revision, unit basis, date and model/route. Do not present estimates as billed spend; store both when available without summing them. Provider request-level pricing, local hardware/energy, API and CI/Host cost are distinct categories. Conversion/rate and policy must be explicit for cross-currency or cross-provider comparisons.
- **Tools/retries:** count physical attempts separately from unique logical calls; classify success, failure, timeout, cancellation, retry and fallback. A missing hook event never establishes zero calls. Duplicate delivery is not an extra tool call.
- **Resources:** units, observation interval, source host/runner identity and shared-utilization basis must be supplied before allocating shared resources to one Agent. Counts/costs can be **`NOT_MEASURED`** or non-comparable under the existing Agent Capability Evidence schema.
- **Correctness:** a Task marked closed, a model self-rating, or a tool success cannot be used as independent code correctness. Quality is evidenced by applicable exact-source tests, independent review where required and later regressions within declared observation windows.

### 3.4 Evidence-class semantics

- `OBSERVED`: an actually emitted provider/host/CI/GitHub event with a resolvable source. It proves **the event or measurement observed**, not every assertion inside its content.
- `SELF_REPORTED`: the Agent's own description, decision or claimed result. The existence of the Issue comment is observed; its claim remains self-reported until verified.
- `INFERRED`: a reproducible consumer interpretation/calculation grounded in cited inputs and declared method/uncertainty.
- `UNKNOWN`: source missing, coverage incomplete, identity conflicted, stale or measurement unavailable. Use an explicit reason where material; never coerce `UNKNOWN` to zero, false or NOT_APPLICABLE.

Evidence-class, completeness, source-currentness and privacy classification are **orthogonal**. A true observation from a stale subject is still historical evidence, never silently current proof.

## 4. HOW to collect: transport-neutral adapter contract

A collector may receive source records from **(1)** provider-native events/hooks/official logs, **(2)** instrumented Agent/SDK/tool or MCP wrappers, **(3)** OpenTelemetry spans/logs/metrics, **(4)** process and Host resource measurements, **(5)** GitHub/API/CI evidence readback, **(6)** Agent Issue completion comments. These are alternatives/composable sources, **not** a claim that every IDE, Codex, Claude Code, ZCode or provider exposes a common hook API.

Each connector SHOULD publish a capability/coverage declaration containing: supported source-version, actual available operations/fields, opt-in capture classes, permissions, failure modes, expected duplication/replay, privacy restrictions and tested mappings. Missing provider API data stays unknown, never inferred from prompts or reconstructed model internals.

**Prefer OpenTelemetry as the interoperable *tracing carrier*, not as ADS Task authority.** For real model calls, map compatible OTel GenAI operation names, provider/model, input/output usage, tool spans and trace/span parent-child IDs. OTel GenAI semantic conventions have evolving stability/versioned vocabulary: pin the adapter's upstream convention revision and **version its mapping**, preserve native source identity, and do not require all providers to expose token/cost/hook events. OTel `trace_id` does not replace ADS `dispatch_id` or accepted GitHub Claim; tracing can begin before a Task is known. No raw GenAI input/output/tool-call arguments are collected by default.

### 4.1 Ingestion order / identity rules

1. **Observe and redact at source** under the source's authorized project/privacy policy; emit only safe metadata/refs by default. Fail closed on sensitive-content policy uncertainty, but do not break real Task execution merely because optional instrumentation is unavailable.
2. **Persist a durable source receipt**, stable event ID/source scope, adapter+mapping revision, observed/ingested time and integrity/coverage marker. A transient stream event without replay guarantee is `PARTIAL/UNKNOWN` until recovered.
3. **Normalize non-authoritatively**; correlate exact accepted Issue/Claim/Dispatch/Attempt and logical operator contexts when deterministically resolvable. Trace IDs link instrumented steps, not Work Item permission; ambiguous multi-writer attribution is `UNRESOLVED`.
4. **Deduplicate** deliveries with the stable upstream identity and provider attempt/generation; preserve multiple genuine retries/attempts as distinct. Duplicate webhook delivery must be idempotent; same ID with conflicting payload is a conflict requiring evidence-based reconciliation, never last-writer-wins.
5. **Handle late/reordered/corrected data** by append-only correction/linkage and recomputable projections. Retain original observed and ingestion times (including timezones/precision); do not sort by arrival order to infer causality or duration when clocks are not comparable.
6. **Re-read authoritative sources before judgment**: an Issue comment, trace, API timeout or local projection never proves a passed Validation/Review/merge, actual current branch or Release. Distinguish OBSERVED external facts, report-only claims and not-yet-read surfaces.

Instrument a few important operation boundaries before expanding expensive step-level capture. Where collection overhead, dropped batches, API limits, privacy omissions or sampling interfere, record **coverage and degradation**. Dropped data must not be interpreted as an Agent/tool failure or as zero work.

## 5. HOW to store: logical storage contract (vendor-neutral)

A conformant implementation SHOULD separate four logical layers. These are **logical responsibilities**, not a mandate to provision four physical databases:

| Layer | Retained data | Required properties |
| --- | --- | --- |
| **Origin/evidence references** | GitHub/CI/Review source identities and provider event refs, resolver metadata | Immutable source identity where applicable, currentness and access limits; external authority stays external |
| **Append-only observation journal** | minimal native-safe event receipt, normalized payload/digest, producer/adapter revision, capture gaps and corrections | Stable ID, idempotent/replay-safe, original/ingestion times, immutable history, integrity checks |
| **Queryable index/projection** | Task/Attempt/session/trace/step link graph, class/status, token/time/cost totals with comparable basis, coverage | Rebuildable from journal + authoritative readback; derived truth/provenance and correction generation, not new canonical Issue/Gate state |
| **Learning/analysis outputs** | linked Task Learning v1/v2, Agent Capability Evidence v1, cohort report and improvement proposals | Same-family schemas and exact evidence refs; versioned/dated query method, uncertainty and subordinate consumption |

**Logical join keys:** source namespace + event/attempt revision; repository + Work Item; accepted dispatch/Claim when present; logical `operator_id + session_ref + role`; immutable Git subject; source trace/span/parent; cited evidence/learning/capability IDs. Each join states `BOUND | PARTIAL | UNRESOLVED | CONFLICT` or equivalent: consumers may not equate a time-nearby model call, shared provider key or GitHub username with a uniquely proven Agent attempt.

**Physical implementation choices are consumer-owned**: e.g. SQLite for a small local index with append-only newline JSON and content-addressed blobs, optional Postgres for multi-writer shared indexing, object storage for compressed approved artifacts and OTel exporter/collector for traces. These are examples, **not** hard ADS dependencies. Partitions SHOULD prevent cross-project/tenant disclosure and large binary/raw diagnostic data from contaminating hot query or GitHub Issue surfaces.

- **Immutability/consistency:** never modify already accepted source receipts in place; record correction, supersession, redaction/tombstone or derived-revision provenance. Publication of an index pointer must not expose incomplete data as `COMPLETE`; support crash-safe replay, retry and actual missing-page detection. Integrity hashes are useful but do not prove who produced an untrusted event.
- **Access and privacy:** project/source authority defines `PROJECT_PRIVATE | RESTRICTED | PUBLISHABLE`; no implicit promotion to public from a GitHub artifact or an aggregate. Minimize personal data, secrets, tokens, paths, user prompts, model outputs and Hidden Validation cases. Encrypt and protect data appropriately to sensitivity; enforce explicit access rights, redaction before export, bounded query/aggregation access and deletion/retention policies.
- **Retention:** project/organization Product policy selects raw/summary/derived retention and allowable aggregation scope, including data-subject deletion requirements. Do not invent a universal TTL or store indefinite private payloads because they might help future model evaluation. After authorized deletion, keep only permissible audit metadata/tombstones; dependent analyses become `STALE/UNAVAILABLE` rather than pretending their source remains inspectable.
- **Currentness:** preserve historical record tied to immutable old SHA, but do not bind it to new code without new evidence; provider/API/schema/price-table version drift invalidates affected current comparison, not the historical event.

## 6. HOW to use: subordinate learning and evaluation contract

### 6.1 Engineering lessons and prevention

Level 1 Issue closeout is the **human-readable summary**. Material Level 2 learning uses **existing Task Learning v1/v2**, especially v2 `execution_friction_class`, `recurrence_refs`, `root_cause_relation`, `recurrence_audit_ref`, `prevention_point_refs` and `ads_evolution_candidate_ref`. Use `TASK_LEARNING=NONE_MATERIAL` for routine tasks; do not mint an empty object or a parallel `agent-learning` family.

A learning synthesizer may propose: same/related/distinct/unknown root cause; reuse of existing code/Skill/tool; earlier L1/L2/L3/Task Pack prevention point; escaped test/Review blind spot; safe workflow improvement. Every material conclusion includes its exact evidence set, counterevidence and known applicability. Wording similarity, repetition count or model consensus alone proves no common root cause. A later consumer can attach **applied / independently verified effective / ineffective / not applicable / unknown** as *derived, source-cited consumption observations*; these are **not** new Task Learning v2 schema fields, normative success scores or automatic standard promotions.

If the lesson suggests publishing/changing a Skill, reuse `SKILL_PROCEDURE_GOVERNANCE_STANDARD.md`. If it suggests changing ADS, follow `DEVELOPMENT_WORKFLOW.md` §8 classification and ordinary Intake→L1→PRD→L2→Task governance; a chart or threshold does not authorize edits.

### 6.2 Agent capability evidence and fair comparisons

Use **existing Agent Capability Profile v1** for declarations and **Agent Capability Evidence v1** for independently source-bound positive/negative/mixed outcomes; preserve `logical_operator_or_executor_ref`, role/task class/exact subject/environment refs, evidence strength and `economic_measurement_status`. Do not introduce a competing quality-score family, change identity to GitHub account, or treat a model/provider label as a verified executor's skill.

A comparative report **MUST** declare: task cohort/acceptance scope and risk, executing role and independence policy, observed attempted vs completed denominator (include blocked/failed/superseded where relevant), source/evidence availability, outcome horizon for regressions, external tool/Host/CI condition, missing/fallback model attribution and actual compatible usage/cost method. Incomparable cohorts are `INSUFFICIENT_COMPARABLE_EVIDENCE` rather than a numeric winner. Separate Reviewer-detected defects from Builder-introduced defects, tool/environment failures from implementation mistakes, and self-declared difficulty from independently bounded Task facts.

Derived suggestions may inform risk-bounded Agent routing or Skill choice at the consuming product's discretion but never override existing hard eligibility, write ownership, required Review independence, Gate result or human-protected decisions.

### 6.3 Evaluation/reprocessing safety

Every derived report SHOULD state input watermark/time window, immutable evidence refs, mapping and query/calculation revision, coverage, sampling, denominator, exclusions, uncertainty and later correction/recompute provenance. A result can be **historically correct but currently inapplicable** after source/Task scope changes. Contradictory measurements (e.g. billed vs estimated tokens, changed provider IDs, a denied merge, stale Review) require reconciliation or an explicit `CONFLICT` / `UNKNOWN`; choosing the most favorable value is forbidden.

## 7. Adoption profiles and conformance / negative tests

A consumer MAY adopt incrementally without blocking Task/PR/CI:

- **A: durable-only** — native GitHub/CI/Issue, Level 1 notes; no model/tool step claims or measured token/cost.
- **B: bounded instrumentation** — selected native hooks or SDK/CLI tool wrappers with source-stable IDs, partial coverage and trace linkage.
- **C: evidence-qualified analysis** — additive OTel/Host measurements plus read-only Learning/Agent Capability Evidence synthesis, with cohort and privacy checks.

Profiles are illustrative **capture maturity**, NOT `.dev-standard/VERSION` adoption `A0–A4` and not a workflow/release Gate. Missing optional capture is `UNKNOWN`, not a new BLOCKED Task. The owning Issue/CI/Release rules always apply independently.

A conforming ADS interpretation MUST reject at least these false conclusions:

1. **No native hooks** + GitHub Issue closed -> inferred zero tool calls/tokens/cost or inferred success of an unexecuted Host gate.
2. **One shared GitHub actor** for two self-declared logical operators -> identities merged, or identity judged from transport login.
3. **Duplicate provider event/webhook** + real retry + nested parent spans -> inflated call/token totals and double-counted wall time.
4. **Missing/stale SHA**, conflicting dispatch, incomplete pagination or guessed temporal join -> current Task/Claim/Review proof.
5. **Estimated cost** lacking pricing version or incompatible currency/billing basis -> actual bill, comparable saving or numerical Agent ranking.
6. **Sensitive content in native tool/prompt logs** -> copied wholesale to GitHub Issue/public ADS learning.
7. **High-score repeated Task Learning** -> automatic ADS standard mutation, bypassed Review or narrowed hard Agent eligibility.
8. **Lost raw observation/corrected late data** -> silent rewritten event, fully complete data claim or deleted failure attempt.

See `references/AGENT_EXECUTION_METADATA_COLLECTION_REFERENCE.md` for adoption decision map, OTel crosswalk, storage example and implementation-project handoff checklist.

## 8. Compatibility and ownership

This additive standard applies **prospectively only when a project adopts an appropriate exact compatible ADS revision**. Existing released tags, v4.0 `agent-event-v2`, v4.8 capability families, v4.9 Task Learning v2, v4.13 Issue closeout and CI/Review/Release contracts are unchanged; a new standard document is not a guarantee that legacy agents and tools implement it. Any later mandatory normalized wire schema must be separately justified, compatibility-reviewed, and source/test/manifest-registered; **do not silently rewrite prior schema contracts**.

ADS owns **data meaning, evidence/source boundaries and consumption rules**. Independent implementation projects own adapter-specific source capability probes, instrumentation, storage, access control and user-facing analytics. If a provider changes hook semantics, that adapter's mapping/version changes while ADS Task/Review/Release authority stays unchanged.
