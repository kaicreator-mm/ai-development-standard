# ADS v4.15.1 — Report Interoperability Bug-Fix Product / Compatibility Decision (R0)

**Status:** DRAFT_NOT_FROZEN / Independent Product & L2 Review NOT_RUN / Source Implementation NOT_AUTHORIZED. **Owner intake:** [#1261](https://github.com/kaicreator-mm/ai-development-standard/issues/1261). Original observed issue [#1258](https://github.com/kaicreator-mm/ai-development-standard/issues/1258); native GitHub simulation [#1257](https://github.com/kaicreator-mm/ai-development-standard/issues/1257#issuecomment-6334134321).

## Immutable baseline and reason for patch

- v4.15 version integration: `89e2b5170734f2a6b85f41d92efe6b1d86634e02`; qualified immutable candidate: `639675e96dd4c2ed123b7684a4c5d25437a13341`; its entire tree remains immutable.
- The original report-only v4 schema blob `88c96dda7f8bcaabe1766a807599ed15bbeae2de` is closed with strict `additionalProperties:false`. Historical v3 Work Item/Intent/Event wire and the original v4 Report remain byte-identical.
- Actual v4 Simulation #1257 published 8 structured comments and demonstrated: two differently scoped `model_input_tokens` values cannot be attributed to provider/route/window by schema; v4 has a single typed `cost` basis; cross-Issue correction passes structural validation but must fail publisher/consumer target-authority semantics. No actual producer/Tally TS/credentials/Host/real E2E were tested. **Do not widen this source validation into runtime PASS.**

## Product decision to review

**Chosen R0 proposal (needs independent review and Product authority Freeze):** one additive *report-only* successor wire `ads/github/v5` under ADS standards **v4.15.1**, without changing any `ads/github/v4` bytes or historical source interpretation. Standards semver and GitHub report wire identity are **not interchangeable**: the v5 wire is explicitly separately negotiated, never silently inferred from `VERSION=4.15.1`, and is not compatible with consumers pinned exclusively to v4.15.0. The alternative (aggregate-only v4) must be rejected or accepted explicitly by Product owner; cannot pretend it solves model-route comparison. This v5 proposal is an **opt-in patch delivery**, not a claim that v5 production adoption has occurred.

### P1. Comparable bounded public metric observation

For each finite bounded public metric:

- Use **typed** `metric_id` from a versioned registry and constrained unit/measurement kind. Minimal names proposed: `model.requests.logical`, `model.requests.physical`, `tool.calls.logical`, `tool.calls.physical`, `tokens.input.total`, `tokens.output.total`, `tokens.input.cache_read`, `tokens.input.cache_write`, `tokens.output.reasoning`, `duration.task.wall_ms`, `duration.model.union_ms`, `duration.tool.union_ms`, `duration.wait.union_ms`. Unregistered aliases (e.g. `input_tokens`) are noncomparable; never quietly map unknown names to a known metric.
- Include `scope` (`PHYSICAL_CALL|LOGICAL_CALL|ATTEMPT|TASK`), `logical_call_ref` and `physical_attempt_ref` when actually supported, `window` (`MEASURED_INTERVAL|OPERATION_REF|UNKNOWN` plus coherent time/clock source or ref), `mapping_revision`, `coverage`, `epistemic`, source refs and currentness. Missing instrumented dimension must be `UNKNOWN`, not fabricated by Task/Issue identity or comment timestamps.
- Optional scoped `model` with independently source-qualified provider, requested, selected and provider-resolved model identifiers, each separately `OBSERVED|SELF_REPORTED|UNKNOWN`; `route_policy_revision` if observed. Requested/selected are not synonyms of resolved. Opaque `source_refs` cannot be parsed as trusted provider/model/route.
- Explicit `aggregation` policy: physical leaves counted once per logical+physical id; `tokens.input.cache_read` is a subset of `tokens.input.total` when inclusion is source-proven and must not be added again; `tokens.output.reasoning` similarly. Parent + child spans, concurrent model/tool intervals and logical retries cannot simply be summed. Keep `denominator` and `excluded/unknown` populations to report completeness; no false exact Task totals from PARTIAL coverage.
- Bounded public GitHub summary only; full Step/Span/private Trace/Manifest remains in task-meta. No new mandatory per-step GitHub writes, universal Agent Hook or Tally access to private task-meta data.

### P2. Distinct evidence-qualified costs

- Add `cost_observations[]` with `basis=BILLED|PROVIDER_REPORTED|ESTIMATED|UNKNOWN`, currency, source refs, currentness, `pricing_revision` and measured period for estimates, and independent optional model/call scope identity. Preserve actual billed invoice separate from estimate and provider-reported number; cross-currency/incompatible rate revisions are *not addable* absent explicit lawful conversion.
- Missing total/denominator/billing = `UNKNOWN`; `0` requires complete genuine zero evidence. No duplicate cost for parent/child logical/physical events. Public report must not include invoices, API tokens, private Trace or secrets.

### P3. Corrective notice acceptance / native authority

- `EXECUTION_CORRECTION` has canonical subject `issue_ref`, `task_ref` and targeted native comment. Within the successor semantics, shape/normalization **must reject** `target.issue_ref` unequal to the subject owning Issue and `target.task_ref` unequal to subject Task (plus malformed target-comment URL prefix).
- Even consistent shape is **not** sufficient for effective REVOKE/REDACT/DISPUTE: Tally-style reader checks real native target comment ID/URL, owner repository/Issue, original report identity/revision/digest/namespace/Attempt, source currentness, actual publisher correction authority and permission/receipt. Unknown authority => `UNVERIFIED`, no change to target. Same GitHub transport login is not proof of same publisher.
- Existing v4 correction parse/reconciliation remains historically immutable, subject to its documented extra consumer checks; do not back-edit old comments or new-test v4 as if it already rejected cross-Issue.

### P4. Pin / compatibility / release boundary

- `ads/github/v3` Work Item/Intent/Event remain current as governed by existing v4.15 source; historical v3 reports read-only. Existing `ads/github/v4` reports remain readable but cannot supply absent v5 dimensions; model-route/cost breakdown becomes `UNKNOWN/NOT_COMPARABLE` without native source evidence.
- The v5 report is only accepted when a project explicitly pins a **qualified immutable ADS v4.15.1 SHA** and declares v5 capability for both writer and reader; no floating `main`, implicit pin upgrade, or v4.15.0 consumer silent acceptance. Additive/new wire fields must never be emitted by an unchanged v4 profile.
- Version branch `version/v4.15.1` derives from `version/v4.15@89e2b517...` because 4.15.0 is not yet merged into main; source PR `#1211` stays Draft and main remains `584512e...`. No version→main release before prerequisite v4.15 authority/sequence and new Release Qualification.

## Executable falsification matrix (all examples use simulated metrics; code language free)

| Case | Input | Expected normative result |
| --- | --- | --- |
| V01 | Model A 80 input/10 output, Model B 40 input/8 output with real call IDs, independent model receipts | 120/18 aggregate only with compatible coverage; A 80/10, B 40/8 independently attributable; no double count |
| V02 | Same numbers but model attribution only in free-text `source_refs` | UNKNOWN model breakdown, no inferred route |
| V03 | logical call 1 / physical retries 2, duplicate webhook delivery | 1 logical, 2 physical; dedupe by physical id; avoid double usage |
| V04 | 100 input tokens includes 25 cache-read, 10 output includes 3 reasoning | input TOTAL=100 not 125; output TOTAL=10 not13 |
| V05 | two overlapping model intervals plus enclosing parent span | interval union from supported coherent clock; no nested sum, otherwise UNKNOWN |
| V06 | BILLED USD 1.25 plus ESTIMATED USD 1.00 or different currencies | keep separate and provenance, never falsely publish BILLED USD 2.25 |
| V07 | missing model/window/cost source, partial population | null/UNKNOWN for unsupported dimension; no guessed denominator |
| V08 | v4 Report v4.15 historical reader | unchanged schema SHA and legacy v4 behavior; v5 dimension is not guessed |
| V09 | v4.15-pinned v4 reader encounters v5 | UNSUPPORTED_SCHEMA, no partial interpretation or accidental v5 write |
| V10 | crossed Issue in correction body / URL | INVALID_SEMANTICS before shape-valid v5 normalization; no target revoke |
| V11 | aligned Correction but target publisher authority or readback absent | UNVERIFIED, no REVOKE even when schema valid |
| V12 | native GitHub edit creates same identity with two digests | CONFLICT and append-only successor ambiguity; no last-wins |
| V13 | unsupported metric alias or mismatched canonical unit | INVALID/NOT_COMPARABLE, not silent conversion |
| V14 | no native Task/Attempt binding; only synthetic published JSON | collector-only/UNKNOWN; never Task, Review, CI or Release PASS |

## Role/write boundaries

- **Product/Architecture Planning**: this draft checkpoint, independent approval of wire strategy/compatibility/authority and scoped Task acceptance. It **does not create** an admitted Builder Claim.
- **Implementation Task(s) after Freeze**: allowed new `schemas/github/v4.15.1/`, strict report-only parser/validator/positive-negative fixture and existing protocol §16 successor amendment, tests and source manifest/workflow as justified; exact base, approved write set and required independent source Review.
- **Forbidden**: mutate v4.15 original `schemas/github/v4.15/report.schema.json`, v3 schema, frozen `docs/implementation/4.15.0`, historical Claim/Issue events, real task-meta/Tally runtime, `main`, or v4.15.1 published/effective adoption before appropriate Release Gate.
- **Closure**: true tests on exact candidate SHA, required independent source Review, compatibility matrix, no regression in v4/v3, qualified Release and future repository integration decision. A documentation-only assertion and a simulated POST alone are insufficient.

**Unresolved until independent Product/L2 review:** Is new v5 wire under standards patch 4.15.1 acceptable as *additive* with explicit negotiation, or should compatibility-owner require a different release/version identity? Is the minimal typed vocabulary sufficient for the original #1258 report comparison goal? Does v5 correction need any permitted cross-namespace delegation path? Findings route to revision of this proposal; never assume source author also supplied independent review.
