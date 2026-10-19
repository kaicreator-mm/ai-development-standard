# Agent Execution Metadata — Collector Adapter & Storage Reference

**Status:** non-normative implementation guidance for a **separate future project**, not a shipped ADS collector. The only owning standard for this concern is [Agent Task Execution Metadata Standard](../standards/AGENT_EXECUTION_METADATA_STANDARD.md). Earlier normative owners of GitHub/CI/Task Learning/Agent Capability remain authoritative. No project name, runtime or provider API availability is assumed.

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
