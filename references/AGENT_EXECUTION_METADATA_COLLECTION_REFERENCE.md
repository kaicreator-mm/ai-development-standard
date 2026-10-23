# Agent Execution Metadata — Collector Adapter & Storage Reference

**Status:** non-normative implementation guidance for a **separate future project**, not a shipped ADS collector. The normative owner is [GitHub Agent Interaction Protocol](../standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md), section 10, **Passive Task execution metadata: collection, storage and use**. This reference provides adapter and storage examples under that existing owner, not a new normative/machine family. Earlier normative owners of GitHub/CI/Task Learning/Agent Capability remain authoritative. No project name, runtime or provider API availability is assumed.

## 1. Source-of-truth crosswalk: do not duplicate existing machines

| Consumer question | Source | Output/ref and authority limitation |
| --- | --- | --- |
| Which Task is allowed, dispatched and accepted? | Native GitHub Issue/Dependencies, current Dispatch/Claim and Agent Event v2 | Read-only correlation; never infer accepted Claim from hook logs |
| What source was changed/validated? | Git SHA/tree, PR, source-verified executed checks, CI Evidence manifest | Pin exact source; avoid branch/ref aliases as validation identity |
| Who acted? | self-declared `operator_kind/operator_id/session_ref/role` plus actual accepted context | GitHub actor is transport, not executor identity; model/provider is extra provenance |
| What did the Agent decide? | Level 1 Issue decision comment with `DECISION/EXECUTION/REUSE/LIMITS` | Self-report, unless cited code/tests independently support it |
| How many tools/models/tokens/seconds/currency units? | official hook/SDK/OTel/provider receipts or measured Host/resource feed | Only report what is truly covered, and state source and denominator |
| Was a lesson reusable? | Existing Task Learning v1/v2, tied to immutable source and actual tests | Materials-only; `NONE_MATERIAL` is normal |
| Is an Agent capable on this class? | Agent Capability Profile **claims** + Agent Capability Evidence v1 | Positive/negative/mixed source-bound evidence; not universal score/authorization |
| What improvement should follow? | Skill Procedure owner, ADS Evolution Intake; existing Product/L2/DAG change path | Recommendation only; no auto-promotion from counts |

## 2. Collection coverage matrix — adapters may be partial

| Source/adapter class | Typically observable | Usually **not** established by this source alone |
| --- | --- | --- |
| **GitHub read-only** | Task/PR/merge/Issue note/official reviewer outcome, exact SHA, check links | in-process steps, tool counts, real provider billed tokens, Agent private reasoning |
| **CI/Host** | actual commands/exit/step wall times, resource measurements if instrumented, test scope | model prompts/token usage, independent model quality, production health |
| **Native Agent hook/event** | specific known callback stages, configured tools, session/call IDs, provider-exposed usage | uninstrumented background calls, other transports, all resource or actual billed amounts |
| **SDK/tool/MCP wrapper** | wrapped model/tool call start/end/result status and invocation id | calls that bypass wrapper; full raw prompts/args are neither needed nor default-collected |
| **OTel GenAI** | spans/logs/metrics with trace linkage, model/tool names, declared token fields when exporter emits | canonical ADS Dispatch/Claim, total actual bill, all operations across missing instrumentation |
| **Agent Level 1 report** | rationale/alternatives, reuse explanation, unexpected problems and cited refs | objective duration/tokens/cost/correctness simply from Agent's prose |

A provider's available hook names and payload guarantees are an **adapter implementation/version fact**, not an ADS universal property. For Claude Code, Codex, ZCode and additional agents, require each implementation adapter to document real supported lifecycle callbacks/exports, with test fixtures pinned to the installed version. Do not invent common hooks or declare unsupported stage-level time/cost observable.

### 2.1 OpenTelemetry interoperability guidance

Prefer using OTel traces/metrics/logs as a standard carrier when supported; its **GenAI semantic conventions have versioned/developing fields**, so the adapter must declare the semantic-convention revision and the exact mapping applied. Relevant official sources (as read on 2026-10-19; reverify when implementing):

- [OpenTelemetry GenAI span conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md)
- [OpenTelemetry GenAI agent span conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md)
- [OpenTelemetry GenAI attributes](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/) — registry attributes may be deprecated/moved, use the pinned upstream revision.
- [OpenTelemetry generic events](https://opentelemetry.io/docs/specs/semconv/general/events/)

| ADS logical concept | Example compatible OTel input (when actually emitted) | Guard |
| --- | --- | --- |
| Model/agent/tool step | `gen_ai.operation.name`: `invoke_agent`, `execute_tool`, inference operation | If a source emits only external SDK calls, internal steps remain unknown |
| Provider and model provenance | `gen_ai.provider.name`, request/response model if available | Multiple models/routers may exist in one Task; do not equate advertised with observed |
| Trace correlation | trace/span/parent span context | Join accepted ADS Dispatch/Task only via real extra correlation bridge, not same timestamp |
| Tool identity | `gen_ai.tool.name`, tool-call IDs where emitted | No automatic input argument/result capture |
| Usage | `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, cache/reasoning subfields if supported | Record inclusive definitions; do not add nested cache/reasoning counts twice |
| Errors and time | span timestamps/status, `error.type`, source clock metadata | One parent span + child spans do not imply additive Task elapsed duration |

**Data privacy**: OTel conventions may describe system instructions, input/output messages and tool arguments. These are sensitive payloads, **not** required ordinary ADS capture; opt-in must be separately authorized at the source and redacted, never promoted to public evidence automatically. No prompt/hidden reasoning is needed to validate cost and callback timing.

## 3. Illustrative collector-side records (NOT a new ADS machine schema)

These examples show one possible **private implementation-owned JSONL index**. They are **not** `ai-dev:event-v2`, cannot be posted as canonical GitHub events, and deliberately contain no prompts, secrets or real customer content. All identities below are fictional placeholders.

### 3.1 Native instrumented model call

```json
{
  "capture_schema": "example-consumer/observation-1",
  "observation_id": "sdkA:run88:call03:completed",
  "observed_at": "2026-10-19T03:01:00Z",
  "ingested_at": "2026-10-19T03:01:01Z",
  "source": {
    "kind": "instrumented-sdk",
    "adapter_revision": "sdkA:1.0",
    "source_event_id": "run88:call03",
    "capture_coverage": "PARTIAL",
    "privacy_class": "PROJECT_PRIVATE"
  },
  "correlation": {
    "work_item_ref": "github:example-org/example-repo#42",
    "dispatch_id": "dispatch:42:builder:r1",
    "operator_id": "self-declared:builder-01",
    "session_ref": "s-01",
    "role": "builder",
    "attempt_id": "attempt-01",
    "binding": "BOUND"
  },
  "operation": {
    "kind": "MODEL_CALL",
    "logical_call_id": "gen-call-03",
    "physical_request_id": "upstream-88",
    "provider": "example",
    "model": "example-model-r1"
  },
  "observations": [
    {"name": "input_tokens", "value": 2000, "unit": "token", "class": "OBSERVED", "basis": "provider-reported", "source_ref": "private:usage/upstream-88"},
    {"name": "output_tokens", "value": 300, "unit": "token", "class": "OBSERVED", "basis": "provider-reported", "source_ref": "private:usage/upstream-88"},
    {"name": "cost", "value": 0.004, "unit": "USD", "class": "INFERRED", "basis": "price-table/example-model-r1@2026-10-19", "source_ref": "private:pricing/rev2"}
  ],
  "outcome": "SUCCEEDED"
}
```

The cost is **inferred**, not billed; the provider-reported token totals are **observed only for that physical request**. Neither says the Task passed validation. The example's guessed provider and prices are illustrative, not real current price claims.

### 3.2 Ambiguous CLI-only event

```json
{
  "capture_schema": "example-consumer/observation-1",
  "observation_id": "cliB:proc9:stderr-12",
  "source": {"kind": "process-log", "privacy_class": "RESTRICTED", "capture_coverage": "PARTIAL"},
  "correlation": {"binding": "UNRESOLVED"},
  "operation": {"kind": "PROCESS_DIAGNOSTIC", "error_type": "child-exited-nonzero"},
  "observations": [{"name": "tool_calls", "value": null, "class": "UNKNOWN", "reason": "source has no tool hooks"}],
  "outcome": "UNKNOWN"
}
```

Its `UNKNOWN` value cannot become **0 tool calls** or be attributed to whichever Task happened near the process timestamp.

## 4. Recommended implementation-owned storage design (not mandated)

```text
project-policy + adapter capability manifest
              |
      protected source ingest/redaction
              |
     durable receipt/journal  [immutable keyed events, native refs, corrections]
              |                         |
              |                    private approved raw artifacts  [content hashes, access, retention]
              v                         |
     normalized query projection        |
     work_item / attempt / step / model / tool / evidence / usage
              |
       reconciliation against canonical GitHub/CI exact source
              |
     derived Task Learning + Agent Capability Evidence + reports
```

A small implementation can use SQLite WAL for query/index state and append-only JSONL chunks for journal, with external artifacts under a private content-addressed directory. A multi-host implementation might use transactional shared DB + object storage and OTel collector/exporter; database brand, ingestion throughput and retention days remain implementation/product choices. **Do not** make GitHub Issues a dump of full private execution traces; publish a compact decision note + safe immutable refs and exact result there.

Minimum logical index relationships:

```text
source_event(source_namespace, source_event_id, source_attempt, payload_digest)
normalized_observation(observation_id, source_event_ref, observed_at, ingested_at, mapping_rev)
correlation_link(observation_id, work_item_ref?, dispatch_id?, attempt_id?, operator_id?, session_ref?, role?, exact_sha?, binding_state)
operation_link(observation_id, trace_id?, span_id?, parent_span_id?, call_id?, retry_of?)
measurement(observation_id, metric_name, value?, unit?, source_basis, epistemic_class, source_ref?, completeness)
evidence_ref(observation_id, canonical_source_ref, verified_at?, source_currentness)
derived_report(report_id, input_watermark, input_refs, query_revision, cohort, coverage, caveats)
```

`?` means optional/unknown, not universally `NULL == NOT_APPLICABLE`. The journal may include duplicate delivery receipts but the projection must be idempotent. Changing an inferred classification or report must create a new derived revision or correction lineage, not overwrite source events. Index and raw payload lifecycles are independent; deletion must invalidate dependent derived analyses when source no longer verifies.

## 5. Consumer can implement conformance with small fixtures

| Case | Source conditions | Correct interpretation |
| --- | --- | --- |
| C01: minimal-only | GitHub Issue closed and source-bound L1 decision note, zero native hooks | Decision note present, model/tool/token/time **UNKNOWN**, not zero; no Host PASS |
| C02: retry and replay | one parent Agent span, two nested tool spans; one delivery repeated twice; one real provider retry | Two real tool operations if two distinct IDs, one duplicate receipt excluded, retry distinct; parent/child time not double summed |
| C03: multi-actor | same GitHub transport user, two different declared operators/sessions | Distinct logical Agents, independent source evidence; no login-based merge |
| C04: stale subject | Task Learning references an old SHA; new PR HEAD exists | Historical learning retained; current applicability unproven |
| C05: mixed fidelity | one Agent report says PASS, current CI is FAILED | Report is SELF_REPORTED and conflicts with real CI; no PASS inferred |
| C06: mixed sources | real invoice USD + locally estimated cost using old prices | Keep billed and estimate separate; incompatible bases not added |
| C07: privacy fail | native log contains auth token and tool response contents | Reject/redact before durable capture or outward publication; no GitHub dump |
| C08: clock disagreement | host UTC timestamp and skewed client clock, no common monotonic | Preserve both, declare incomparable wall duration, no negative duration |
| C09: missing pagination | GitHub issue comment fetch is truncated/unresolved | Incomplete observation/readback; no zero missing/closed claims |
| C10: learning re-use | Task A discovered pattern; Task B applied it and cited same code/test evidence | Maintain historical Task Learning v2 links; effectiveness is separately evidenced, no automatic schema mutation or promotion |
| C11: mixed tasks | one docs-only Task, one E3 multi-process integration | Distinct cohorts; insufficient basis for raw speed/cost/quality ranking |
| C12: collector disconnected | instrumentation stops for 20 min, Task continues normally | Collector health unknown/failed, Task state unchanged; missed events are UNKNOWN, not Agent failure |

## 6. Handoff contract for a separate collector project

A future independent implementation project SHOULD produce, under its own Product/L2/Task DAG:

1. **Adapter capability/source matrix** for installed versions of ZCode/Claude Code/Codex/any SDK, including tested event names, availability, coverage, source privacy and definitive *unavailable* fields.
2. **Privacy and publication plan**, metadata-only by default, explicit project/tenant opt-in for sensitive content, reliable redaction and deletion.
3. **Bounded event/metric normalization design** mapping both OTel revision and native events to Section 3 semantics; per-observation source/binding/epistemic class; unknown-rate tests.
4. **Durable journal + query/index design** with replay, dedupe, late correction, conflicting source identities, identity/version migration and privacy-class partitioning; publish safe Issue references, not raw traces.
5. **Consumer reports** for L1 completeness, Task Learning v2 material cases, Agent Capability Evidence v1 comparable samples, actual usage/cost windows, test/review regression and correction lineage.
6. **One small real end-to-end trial** per supported adapter, reporting *actually observed* source coverage, task correlation failures, missing data, overhead and privacy checks; mock fixtures prove contract shape only.
7. **No cross-system authorization**: report source truth/currentness; do not write canonical GitHub Task/Claim/Review/Validation/Release from telemetry observation.

ADS can define/revise standards using normal versioning; **this reference does not create an implementation Task or launch an independent project**.


## 7. Task Report Publication Contract v1 — document + Issue locator

**Normative owner:** `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` §10, `Task Report Publication Contract v1`. This section is an illustrative interoperability example for an implementation project. It is not an active collector, a new ADS machine schema family or a GitHub Event v3.

### 7.1 Manifest example — one final Attempt revision

This is a **fictional valid-shape example** with deliberately dummy 64-hex digests; do not present these bytes as verified evidence. All file locators represent immutable object IDs resolved with project authorization, **not publicly fetchable credentials**.

```json
{
  "schema_version": "ads/task-report-manifest/v1",
  "report_id": "task-report:example-repo:120:attempt-001:execution-summary",
  "report_kind": "EXECUTION_SUMMARY",
  "revision": 1,
  "work_item_ref": "github:example-org/example-repo#120",
  "attempt_ref": "collector:example-repo:attempt-001",
  "attempt_binding": "COLLECTOR_ONLY",
  "actor": {
    "role": "builder",
    "operator_kind": "codex",
    "operator_id": "agent:builder-01",
    "session_ref": "example-session-01"
  },
  "subject_ref": "git:example-org/example-repo@0123456789abcdef0123456789abcdef01234567",
  "generated_at": "2026-10-19T06:10:00Z",
  "privacy_class": "PROJECT_PRIVATE",
  "coverage": "PARTIAL",
  "source_refs": [
    "github:example-org/example-repo#120",
    "github:example-org/example-repo/pull/125"
  ],
  "documents": [
    {
      "kind": "EXECUTION_SUMMARY",
      "storage_ref": "object:private-reports/example-repo/tasks/120/attempt-001/r1/summary.md",
      "media_type": "text/markdown",
      "size_bytes": 2048,
      "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    },
    {
      "kind": "METRICS",
      "storage_ref": "object:private-reports/example-repo/tasks/120/attempt-001/r1/metrics.json",
      "media_type": "application/json",
      "size_bytes": 1024,
      "sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    },
    {
      "kind": "TRACE",
      "storage_ref": "object:private-reports/example-repo/tasks/120/attempt-001/r1/events.jsonl.gz",
      "media_type": "application/gzip",
      "size_bytes": 4096,
      "sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
    }
  ],
  "supersedes": null
}
```

Notes: `COLLECTOR_ONLY` is not proof of a canonical accepted Dispatch; it means this example's Attempt was **not** bound to one. `coverage=PARTIAL` expressly avoids asserting all model, tool or billing events were captured. `subject_ref` is the exact subject claimed by the producer; a consumer re-resolves it against authoritative source. A real publisher computes the **manifest SHA-256 over its actual UTF-8 JSON bytes**, stores the manifest at an immutable revision identity such as `object:private-reports/example-repo/tasks/120/attempt-001/r1/manifest.json`, and publishes that digest with the link; a manifest cannot embed its own final digest without circularity.

A second revision uses the *same* `report_id`, `revision: 2`, a new distinct `r2/` document and manifest path, and `supersedes: {"storage_ref": "object:.../r1/manifest.json", "sha256": "<actual r1 manifest SHA-256>", "revision": 1}`. The `<...>` span here is descriptive only, not valid JSON. Retain the immutable r1 bytes for provenance for as long as allowed by project retention rules.

### 7.2 Latest-only v3 Issue comment example (object Manifest remains v1)

The GitHub **comment** now uses the common `<!-- ads:github -->` marker and `kind: report`; its `data` is validated by `schemas/github/v4.14/structured-interaction.schema.json`. The durable OSS/S3 object **Manifest** in §7.1 still uses the established `ads/task-report-manifest/v1` JSON dialect. The fictional digest below is illustrative; a real publisher computes/checks actual stored bytes.

~~~~markdown
<!-- ads:github -->
```yaml
schema: ads/github/v3
kind: report
data:
  report_id: task-report:example-repo:120:attempt-001:execution-summary
  report_kind: EXECUTION_SUMMARY
  revision: 1
  attempt_ref: collector:example-repo:attempt-001
  manifest_ref: object:private-reports/example-repo/tasks/120/attempt-001/r1/manifest.json
  manifest_sha256: dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
  coverage: PARTIAL
```

## Decision and evidence

TASK_DECISION_SUMMARY=REPORTED
ACTOR=builder, agent:builder-01, session_ref=example-session-01
SUBJECT=Issue #120, PR #125, git:example-org/example-repo@0123456789abcdef0123456789abcdef01234567
DECISION=Reuse existing helper rather than duplicate parser; cite actual source PR.
EVIDENCE=CI NOT_RUN unless independently linked
LIMITS=PARTIAL collector coverage; billing UNKNOWN
TASK_LEARNING=NONE_MATERIAL
~~~~

No explicit `derived publication identity` or second `ISSUE_COMMENT_REPORT` intent is emitted. The GitHub publisher derives dedupe identity from **actual owning Issue + report_id + revision**, reads back the real comment and reconciles provider retries. GitHub Labels may mark the whole Issue, never an individual comment.

### 7.3 Suggested storage convention (not a forced vendor layout)

```text
<private-immutable-object-root>/
  example-repo/
    tasks/
      120/
        attempts/
          attempt-001/
            r1/
              summary.md
              metrics.json
              events.jsonl.gz
              manifest.json    <-- publish after confirming included files
            r2/
              summary.md
              manifest.json    <-- new immutable correction/revision
```

Use OSS/S3/MinIO stable immutable object IDs, or a cloud drive's **stable file ID plus verified checksum** and source-specific access/retention controls; neither a mutable shared-name file nor a temporary signed download URL is a valid durable publication locator. For private storage, the GitHub comment can contain an **opaque resolver URI** and a source-bound digest; the private resolver returns an authorized temporary URL on demand. The comment itself must be safe at the Issue's actual public/private visibility level.

Publication order: (1) reserve a source-stable `report_id`/Attempt key; (2) write scrubbed files under immutable object IDs and verify actual bytes/digests; (3) write immutable manifest and verify its own digest; (4) read all accessible existing Issue comments/pagination for `derived publication identity`; (5) publish one concise comment and read back its real ID/URL; (6) if delivery outcome ambiguous, re-read/reconcile before retrying. Never treat a successful object upload as proof that a GitHub comment was written.

### 7.4 Idempotency/correction cases

| Case | Producer action | Consumer outcome |
| --- | --- | --- |
| Same report ID/revision/key and same manifest digest delivered twice | Re-read first actual comment, do not create second where controllable | One primary publication; repeated transport receipt not new usage |
| Same key and different manifest SHA-256 | Raise `CONFLICT`, examine source and use new revision or correction | Both source facts preserved; no silent last-writer-wins |
| First POST timed out after GitHub may have accepted it | Full Issue comments readback before retry | Actual URL if found; else queued bounded retry, no fabricated comment URI |
| Two publishers race without a shared lease | One publisher queue is preferable; if duplicates arise mark duplicates in derived view with links | No claimed exactly-once guarantee from GitHub comment POST |
| `EXECUTION_CORRECTION` after stale source or redaction | New report references superseded publication; retain permitted historical receipts | Subsequent readers follow authoritative corrections without deleting history |
| Object exists but manifest unavailable/checksum wrong | Hold comment publication; retry source or record local publication failure | `NOT_PUBLISHED`/unavailable, never an Issue-linked PASS |
| Manifest storage uses expiring presigned HTTPS link | Publish stable opaque resolver locator instead | Temporary signed URL never becomes durable Issue URL |
| Issue Label `task-report:available` applied | Search hint only | Doesn't prove the individual report/manifest is valid |
| Failed/blocked Attempt with material evidence | Emit terminal summary when applicable; truthfully name failure and incomplete coverage | Not a successful Task completion or automatic Review/Validation FAIL |
| API limit 429/403 with `Retry-After` or other primary/secondary notice | Queue/coalesce; obey official headers and exponential backoff with jitter | Task work continues; report remains pending until real readback |

### 7.5 GitHub write budget and data-free implementation

**MVP recommendation:** one terminal summary comment per actual Attempt, then only *material* Learning/Evidence/Correction comments. Normal high-frequency tool/step telemetry stays in immutable objects. Project-selected queueing may coalesce pending updates. Use Webhooks and conditional GET where supported instead of aggressive polling. Serialized mutating requests (at least ~1 second spacing is GitHub's official best-practice advice as of writing) and server-provided backoff/rate-limit headers are preferable to fixed hourly budget claims. GitHub secondary limits are variable and not a guaranteed numeric service quota.

With no DB, the independent collector can reconstruct an index from **Issue comment publication markers + stable object manifests**. It still needs a durable, idempotent **publisher queue/journal** (which can be files/object-based) for network partitions, retry safety and multi-writer conflict handling. GitHub does **not** provide an atomic transaction spanning OSS object writes and Issue comment POST; records must be recoverable at every intermediate stage.

### 7.6 Producer and consumer acceptance matrix

1. A single valid manifest and real source-bound checksum link on a completed Attempt can serve the existing Level 1 note and the document index.
2. Wrong `schema_version`, `report_kind`, negative revision/size, missing sha256, mutable document ref or ambiguous Attempt link is rejected or held as UNKNOWN; do not silently accept.
3. `supersedes` is null for r1 and points to exactly r(n-1) bytes for successor; a correction's declared target is explicit.
4. A public Issue containing a restricted raw URL/secret is a publication failure even when document checksum matches.
5. Duplicate/collision, missing paginated comments, ambiguous POST, provider rate limits, private drive permissions and disappearance of source objects all fail honestly, with Task authority unchanged.
6. A Level 1 Issue note published independently before any collector exists remains valid; the collector may link it as an exact existing comment rather than duplicate it.

## 8. v4.15 projection-only source/coverage crosswalk (illustrative, not a publishable v4 Schema)

This section illustrates the **existing §10 observation semantics** as GitHub-safe projection choices; S02/#1205 will define/validate the exact current `ads/github/v4` YAML fields. Do **not** post the examples below as a GitHub machine record, and do **not** treat this reference as an adapter, second Task Contract or provider-independent billing API. The actual Tally consumer reads only source-qualified GitHub comments/native PR/CI/Review facts and has no access to the private manifest.

| Observed source fact | Bounded GitHub-safe public meaning | Intentionally not inferred |
| --- | --- | --- |
| Native Host records a completed child tool invocation with provider call ID `call-7`, parent root `span-1`, and a second delivery of the **same** event | One counted physical tool call when the event ID, Attempt and binding are verified; `source=HOST`, coverage `PARTIAL` if sibling tools are not instrumented | Root `span-1` + child + duplicate are **not** three calls, and an unobserved tool is not `0` |
| Provider usage receipt for `call-7`: 120 input and 20 output tokens, pricing table revision known, invoice absent | `OBSERVED/provider-reported` tokens in the call window; spend may be `INFERRED/pricing-revision` only if computed with source-bound rates; **billed** cost `UNKNOWN` | Provider usage != total Task tokens; estimated price != settled invoice or verified charge |
| A CLI process exits 0 while the required Host semantic regression is missing | `SELF_REPORTED` Attempt result/exit and `UNKNOWN` independent semantic completion, linked to exact CI/Host facts that are actually available | Exit 0, valid YAML and a green optional check do not establish strict Task/Gate PASS |
| Initial summary exists; an independent required CI verdict arrives only later | task-meta may create a **new immutable** EXECUTION_SUMMARY revision with updated own private manifest/digest and public verifier source; Tally separately reads actual native CI | Old GitHub body isn't edited; late CI source without new task-meta publication does not prove the collector captured it |
| Two logical Agents share one GitHub transport login | Distinct declared operator IDs/sessions and source-bound Task/Attempt links, with actual adapter coverage | Transport login cannot merge the Agents into one role/session or authorize cross-namespace correction |
| Private manifest is unavailable to a Tally GitHub-only reader | `manifest_ref/digest` is a source locator/integrity claim only; public fields remain readable if independently supported | Private URI inaccessible is **not** permission to query task-meta, infer missing measurement, or declare corrupt source bytes |
| Collector misses the sole token hook but observes a Host wall timer | Host duration may be `OBSERVED` if scope/unit/clock basis are known; tokens, cache and billed cost remain `UNKNOWN` | Missing token/bill fields are not zero, and `capture_coverage=COMPLETE` is unsupported |

### 8.1 Bounded publishable summary decision example

Suppose the owning GitHub Issue is `#42`, one Agent Attempt `attempt-2`, and task-meta observes just one instrumented provider request and an exact Host check. A safe GitHub-visible **projection decision** (not syntax for any ADS Schema) is:

- **IDENTITY:** exact owning Issue `#42`; accepted Attempt `attempt-2`; fully resolved source SHA; self-declared logical operator+session; source adapter revision.
- **OBSERVED:** one distinct physical request, 120 input/20 output tokens in a *single covered request*; cite adapter receipt identity or safe digest (never the private receipt contents).
- **PARTIAL:** only instrumented request(s) represented, with coverage limits explicitly stated; do not report entire Task total unless observed call set is complete.
- **UNKNOWN:** actual billed cost, uninstrumented tool calls, cache tokens and remote output outside the observed scope.
- **VERIFIER:** independently read Host check on exact tested SHA if available; unrelated CI, a partial green result, or the self-reported Attempt is not an accepted Task PASS.
- **PRIVACY:** omit prompts/args/private Trace/credentials and any private URI whose contents are not authorized for the GitHub Issue audience.
- **LEARNING:** `NONE_MATERIAL` absent source-backed applicable improvements; do not manufacture Task Learning evidence.

S02 converts this semantic projection into a strict **single** `ads/github/v4` `kind: report` YAML `data` schema with valid/invalid machine fixtures, immutability and digest checks; S03 defines the GitHub-only reader/feedback; S05 performs the **actual** producer→GitHub→reader/feedback E2E. The existence of this reference does not satisfy those executable acceptances.
