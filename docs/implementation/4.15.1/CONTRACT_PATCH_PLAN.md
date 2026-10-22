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


## R1 — six-issue pre-freeze contract expansion (2026-10-22)

**Status: PRODUCT_SCOPE_CANDIDATE / NOT_FROZEN / NO IMPLEMENTATION CLAIM.** This section extends the R0 narrow report proposal at user direction; no v4.15.0 frozen bytes/main/Task/Gate change is authorized. All changes are prospective, source-bounded standards semantics. Existing Task Learning, GitHub report and ADS Evolution governance must be reused before adding fields.

| Priority | Issue / owner | Minimal v4.15.1 standards acceptance | Out of scope |
| --- | --- | --- | --- |
| P1 | #1258 metrics/route/cost | Typed metric ID and comparable unit/scope/window/provider/requested-selected-resolved model source, logical/physical identity, inclusive cache rules, BILLED-vs-ESTIMATED separate costs; missing basis UNKNOWN | Collector, model router, hidden Trace in GitHub, same-wire v4 mutation |
| P1 | #1259 failed/dirty/precommit Attempt | Truthful source-unpinned public disposition or explicit nonpublication with insufficient evidence; no fabricated HEAD SHA. Known exact subject/no verifier stays NOT_RUN/UNKNOWN | Automatic Task/Gate PASS, new canonical Attempt admission |
| P1 | #1198 experience applicability | Evidence-bound task class/risk/env/profile/prerequisites/exclusions/counterexamples/currentness and feedback distinction PRESENTED/ACCEPTED/APPLIED/INDEPENDENTLY_CHECKED/OBSERVED_EFFECT using existing v4 feedback wherever sufficient | Task Learning v3, forced reuse of irrelevant lessons, automatic policy selection |
| P1 | #1206 optional improvement experiment | Source-bound baseline/variant IDs, comparable cohort, independent semantic verifier, actual total cost including failed probes/rework and unknown observations, trial isolation/authority boundary; no uplift without valid comparator | Harness/optimizer implementation, mandatory A/B trials, numeric score as Release truth |
| P2 | #1260 bounded execution phases | Observed physical operation versus declared Step/Phase, clock-source/interval union/wall and wait scope, retries vs duplicated deliveries, partial/unknown coverage; only bounded public aggregates | Universal Phase Engine, mandatory OTel/Agent SDK, private full Step/Span timeline |
| P2, high product importance | Existing DEVELOPMENT_WORKFLOW section 8 + Task Learning v2: evolution evidence handoff | Traceable Evidence/Task Learning -> Applicability -> optional Experiment/Use Feedback -> ADS Evolution Intake -> Candidate decision with immutable source/version, owner, exclusions/contradictions, publication class, decision and next lawful Task/BUILD ref. Preserve NO_CHANGE/MORE_EVIDENCE/OPEN_ADS_INTAKE and normal Product/L2/Task/Review/Release authority | New Evolution state machine, automatic standard edits, numeric auto-promotion, hidden validation/CI waive, automatic Domain Package activation |

**Specific sixth-item rule:** existing v4.8-era normative DEVELOPMENT_WORKFLOW section 8 already owns classification and promotion. The only potential new contract is a minimal machine-reconstructible source-qualified evidence handoff, NOT a new evolution governance engine. Where current Task Learning v2 and section 8 refs already suffice, a short reference/example and negative fixture are preferred over a new schema.

### Additional falsification oracles N15–N25 (language-independent)

- N15 dirty or precommit Attempt with no immutable source: last HEAD is not its tested source; no fabricated 40-hex SHA or Gate PASS.
- N16 true exact source with zero actual verifier invocation: verifier truth NOT_RUN/UNKNOWN, never a fake checker.
- N17 external verifier accepted ACK but lost terminal response: evidence UNKNOWN, not PASS.
- N18 parent/child model/tool spans overlap or clock basis incompatible: union of well-grounded intervals only, otherwise UNKNOWN.
- N19 old v4 reader sees future report profile: refuse unsupported schema; historical v3 Work Item/Event and v4 report bytes unchanged.
- N20 experience applies by keyword but fails tech/risk/host exclusion: NOT_APPLICABLE/INSUFFICIENT_EVIDENCE, not an auto recommendation.
- N21 procedure merely presented, never applied: no successful reuse or effect claim.
- N22 procedure applied with verifier absent or negative: NOT_PROVEN or negative result, not effective.
- N23 baseline 1 sample vs candidate 1 cheap success plus failed expensive probes: total cost/denominators prevent unjustified ROI.
- N24 phase labeled TEST in Agent prose without actual native tool/Host observation: self-reported, not observed 120s testing.
- N25 numeric score or one successful probe attempts evolution promotion/Package activation: existing Evolution classifier yields NO_CHANGE/MORE_EVIDENCE or explicit OPEN_ADS_INTAKE via normal owner, never self-authorized mutation.

### One executable standards-only vertical slice

Use synthetic task-meta measurements (two models and retries, one dirty failed Attempt), GitHub-style source records, a **GitHub-only** synthetic Tally reducer for experience applicability, feedback, controlled baseline/probe comparisons and evolution-source handoff. Any language suffices. Test public formats and normative reduction; never call toy simulation native task-meta/Tally/runtime PASS. Include realistic misbindings, negative traces, corrections, version/source drift and missing evidence. Real #1210/#1231 remain separate NOT_RUN.

### Compatibility and staged work

Retain the proposed *separate opt-in successor report wire* from R0 for schema additions, but explicitly seek Product/compatibility review before committing its name or choosing a standards PATCH with a new wire. No same-wire incompatible mutation. Keep one parent version #1261; issue-specific source owners #1258/#1259/#1198/#1206/#1260 stay linked, not cloned into duplicate Issue DAG. Source execution after lawful Review/Freeze may be split by concerns: (A) typed wire+unknown-source+correction, (B) applicability+experiment evidence, (C) timing/evolution handoff+conformance. Review current contract first; if it already covers any subitem, mark ALREADY_COVERED and do not reimplement.

**No Freeze and no v4.15.1 source work authorized by this R1 draft.**


## R2 — #1241 Plan-first / Web-first / Remaining-only Handoff scope (2026-10-22)

**Status: SEVENTH PRODUCT CANDIDATE / NOT_FROZEN / NO NEW GATE / SOURCE NOT_AUTHORIZED.** #1241 was absent from the R1 six-item summary. User explicitly called this out; treat it as a separate **workflow/practice standards** concern for v4.15.1, not part of the v5 Report wire and not contingent on the new task-meta metrics.

**Existing issue/owner:** [#1241](https://github.com/kaicreator-mm/ai-development-standard/issues/1241), which already has project dogfood on Shun Assistant and v4.15 S04/S05/S06. Reuse TASK_DECOMPOSITION, EXECUTION_PACK, EXECUTION_ARCHITECTURE, LOCAL_AGENT_HANDOFF, Issue/Task Pack, existing Claim/Dispatch and Review/Validation owners; [#1173](https://github.com/kaicreator-mm/ai-development-standard/issues/1173) already covers parent-child Task/evidence×environment, and #1235/#1237 source-bound recovery.

### Product behavior to consider for v4.15.1

1. **Plan-first (pre-source, read-only):** a simple 1–N-step table inside the existing Task Pack/Issue, with deliverable, evidence class, currently available WEB / CI / LOCAL capability, exact allowed write set and dependencies, actual currentness/Claim preflight, and disposition for each remainder. A simple Task can be 3 lines; no new file, child Issue, Review, Freeze or formal planning Gate is compulsory.
2. **Web-first (preference, not a permission):** Web handles all *actually supported* read, contract, source, fixture, PR and CI orchestration after applicable legal Builder Claim is accepted. Lack of physical Host/real token/independent reviewer ability is evidence UNKNOWN/NOT_RUN; cannot be recast as Web PASS. When a designated independent reviewer is required, the source Builder cannot impersonate one.
3. **Handoff only the real residual:** materialized GitHub checkpoint includes immutable source/ref, completed bounded validation tuple, scope/write-set forbidden paths, actual Claim terminal/resource/generation disposition and next eligible role, plus only missing steps. A pointer-only Local Agent trigger is generated only for unavoidable environment/credential/physical evidence; CI can be chosen when it truly covers the profile.
4. **No concurrent protected writer:** uncertain old Claim/lease/generation or missing current authority => HOLD, not second Builder in Local or a new unproven generation. Same-key resume/handoff must follow current admission and historical recovery rules.
5. **Quality unchanged:** existing optional/required independent Review and real Host gates remain owned by original authority. Do not infer task success from source compilation, synthetic demo, partial Handoff or step checkbox; one concern one PR still applies.

### Focused norm/dogfood matrix N26–N31

- N26 **WEB_ONLY**: bounded docs/schema case where Web has legal Claim and source/CI tools; no Local dispatch should be emitted.
- N27 **WEB + CI**: Web authors source and CI covers actual targeted check with recorded SHA/job/profile; no second physical Host attempt without applicable gate.
- N28 **WEB + LOCAL physical**: a real Host/credential/OS capability is required after Web finishes safe part; GitHub checkpoint contains completed refs and restricted remaining Local scope; Host evidence NOT_RUN before it actually executes.
- N29 **UNKNOWN Claim**: dispatch message is schema-valid but composite admission/currentness or old key is unproven; first protected source write refused and Local handoff cannot create concurrent Claim.
- N30 **Required independent Review**: Builder supplies exact source/diff/probes but cannot self-PASS; Reviewer receives GitHub pointer and current check evidence, not private original chat.
- N31 **Plan simplicity**: tiny one-step change with no Local requirements does not acquire a new Task DAG, child Issue, formal Plan Freeze, independent review beyond existing Policy or unnecessary CI rerun.

### Ownership, disposition and small-version boundary

- Implement as one **separate bounded documentation / lightweight Task Pack or Execution Pack guidance concern** only if detailed crosswalk of §6/§11/§23/§27/§29 and LOCAL_AGENT_HANDOFF finds a real uncovered executable behavior. If current clauses suffice, prefer one example + three negative probes and record ALREADY_COVERED/EXECUTION_GAP instead of duplicated normative text.
- This work can be planned/reviewed independently of report v5 design and does **not** cause the Report schema to incorporate execution planning or a second event/claim state machine.
- R2 acceptance is a *prospective product scope decision*, not implementation authority or a new v4.15.1 Release Gate. Cross-project time/cost savings remain UNKNOWN until measured by actual task-meta evidence; no invented claimed percentage.
