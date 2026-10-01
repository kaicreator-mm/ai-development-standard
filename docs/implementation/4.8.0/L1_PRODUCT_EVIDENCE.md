# v4.8.0 L1 Product Evidence — Evidence-Driven Agent Orchestration & Standard Evolution

Status: **COMPLETE RESEARCH / PRE-FREEZE — FRESH INDEPENDENT PRODUCT REVIEW REQUIRED**

Research date: 2026-10-01

Baseline reviewed:

- `main@e75fe834469c5ea9f9a384f7d84e38c3a48afa46`;
- Draft `docs/implementation/4.8.0/PRD.md` initial commit `c2f5d2231799fcc41c41869917b18f0f661276ae`;
- `standards/DEVELOPMENT_WORKFLOW.md`;
- `standards/EXECUTION_ARCHITECTURE_STANDARD.md`;
- `standards/MODEL_USAGE_POLICY.md`;
- Frozen v4.7 Product/L2/DAG;
- v4.5 engineering-feedback dogfood/task evidence;
- `ai-development-standard#45`, `#184` and `#469`;
- `#469` checkpoint/currentness through comment `5925124956`: actual bounded low-cost implementation has progressed through independent gates—S00/C01/A01a/C02 are merged after Validation + fresh Review, while A01b has independent real-Chrome Validation PASS with fresh Review still pending. Economic savings remain unmeasured and no blanket low-cost routing rule is supported.

This document is Product evidence only. It does not authorize Product Freeze, schemas, runtime services, scheduler deployment, Agent transport migration or Task DAG execution.

## 1. L1 verdict

**PROCEED WITH NARROWING.**

The five proposed concerns are real, but the Draft PRD should be corrected to avoid introducing five new parallel authorities.

Recommended Product shape:

1. **Task Learning Evidence** — a compact exact-subject evidence record, not a second design authority;
2. **Agent Capability Evidence & Eligibility** — provider-neutral capability claims plus observed/proven evidence, not a global Agent score;
3. **Constraint-first Assignment & Resource Scheduling** — hard eligibility filtering before optional optimization/ranking, reusing existing Dispatch/Claim authority;
4. **Transport-neutral Agent Exchange Binding** — a common envelope/binding over existing ADS operations/results, not a second task/event lifecycle;
5. **Evidence-driven ADS Evolution Feedback** — project observations -> classified friction -> evidence aggregation -> ordinary ADS change governance, never self-amending.

Two acceptance mechanisms remain appropriate:

- heterogeneous multi-Agent scheduling/independence dogfood;
- cross-project ADS evolution dogfood, with `#469` as one measured evidence stream rather than a normative L3 mandate.

## 2. Internal evidence — ADS already has the substrate

### 2.1 Current execution architecture already separates durable facts, derived queues and bounded controllers

`EXECUTION_ARCHITECTURE_STANDARD.md` already defines:

```text
GitHub/repository/evidence = durable facts
Reducer                    = derived current state
Queues                     = derived ready work
Controllers                = bounded transitions
Agents                     = role-scoped workers
```

It already derives Builder/Reviewer/Validator ready sets, permits a scheduler to recompute them, keeps queues non-authoritative and requires existing Dispatch/Claim admission before execution.

**Finding:** v4.8 should extend eligibility/resource-selection semantics, not invent another scheduler lifecycle or live DAG.

### 2.2 Existing claim serialization already protects multi-Agent concurrency

Current architecture requires no more than one incompatible active dispatch per `(work item, role)` unless higher authority explicitly permits parallelism, and defines `SINGLE_WRITER_ADMISSION` / `LINEARIZABLE_CONDITIONAL_WRITE` as acceptable serialization modes.

**Finding:** resource-aware scheduling must compose with this admission boundary. Scheduling choice does not itself authorize execution.

### 2.3 Existing model policy already separates semantic risk from mechanical execution

`MODEL_USAGE_POLICY.md` says model strength follows task risk, not title. Strong models own Product/Architecture/high-risk semantic judgment, while bounded lower-cost/local Agents may own repository integration, adapters, fixtures, compile/type/lint, packaging and real-host work after Contract/Tests/Reference material exists.

**Finding:** the missing Product is not another strong-vs-weak rule; it is a provider-neutral, machine-readable way to represent eligibility evidence and select among available executors.

### 2.4 v4.7 already provides discovery/read-routing convergence

Frozen v4.7 Product/L2 establishes canonical authority/applicability discovery, qualified state dimensions, reference conventions and progressive disclosure without creating a global lifecycle owner.

**Finding:** v4.8 capability/scheduling/exchange metadata must be discoverable through v4.7 mechanisms and must not become a competing context/authority database.

### 2.5 v4.5 already proves the value of durable engineering feedback

v4.5 incident/recovery work requires durable engineering feedback/follow-up and distinguishes recovered/verified/follow-up states. This is narrower than Task implementation learning but demonstrates that operational experience should produce durable follow-up rather than disappear after immediate success.

**Finding:** v4.8 should generalize only the development-learning gap; it should not duplicate incident postmortem ownership.

### 2.6 #469 proves bounded execution feasibility while preserving independent gates

`#469` explicitly tracks whether Git-tracked L3 references plus compact Issue dispatch improve bounded lower-cost execution. Current checkpoint `5925124956` advances the prior historical `5918608303` state: the earlier statement `ACTUAL_LOW_COST_IMPLEMENTATION_OUTCOME=PENDING` is no longer current.

Observed execution/gate state is now:

- S00 PR #230: bounded low-cost Builder completed; independent Build Host Validation PASS and fresh high-capability Review #231 PASS; Controller merged as `47ee4b0548776b54210882b0228439d4e5d74221`.
- C01 PR #232: bounded Builder completed; independent Validation and fresh Review #234 PASS; Controller merged as `cdebcc45c80e64477a32eb4ffb35fda8f6e0e608`.
- A01a PR #235: bounded Builder path completed; independent Build Host Validation and fresh Review #237 PASS; Controller merged as `c2f206f7669cd3d6e575761675e2b90765159a0e`.
- C02 PR #238: bounded low-cost Builder completed; independent Build Host Validation and fresh Review #241 PASS; Controller merged as `c7e546df11a08a3b2a48285d4fda79f768c5c15e`.
- A01b PR #240: bounded low-cost Builder candidate plus independent real Chrome 154 Validation #242 comment `5924983582` PASS; required fresh Review #243 remains pending and the PR remains unmerged, so `A01b=VALIDATED_REVIEW_PENDING`.

Several Builders reported `CLARIFICATIONS=0`, bounded edit/test loops and no drift, which is useful task-class capability evidence. But comparable input-pack/token/cost baselines were not measured. Fresh high-capability Reviews also surfaced nonblocking P2/P3 findings and downstream design obligations after green Builder/Validation work. That supports continued role/risk separation and independent strong review rather than eliminating it.

The evidence boundary is explicit:

`ACTUAL_LOW_COST_IMPLEMENTATION_OUTCOME=PARTIALLY_MEASURED_POSITIVE_EXECUTION`

`ECONOMIC_SAVINGS=NOT_MEASURED`

`BLANKET_STRONG_TO_LOW_COST_RULE=NOT_SUPPORTED`

`STANDARD_CHANGE=NOT_AUTHORIZED`

`PROPOSED_DISPOSITION=MORE_EVIDENCE`

Provider/model identity remains provenance, not normative policy; Product routing should continue to rely on task-class capability evidence, current availability, risk, environment and independence constraints. Success in these bounded UX Harness tasks does not establish universal capability across unrelated tasks/platforms.

**Finding:** v4.8 should standardize the evidence loop around such experiments, including currentness and independent-gate evidence, without predetermining a universal low-cost outcome or claiming unmeasured economic benefit.

## 3. External evidence — learning/provenance should be explicit but bounded

### 3.1 Google SRE postmortem practice

Google SRE describes postmortems as written records of incidents, impact, actions, root causes and follow-up actions, and emphasizes using them to prevent recurrence and improve systems.

Sources:

- https://sre.google/sre-book/postmortem-culture/
- https://sre.google/workbook/postmortem-culture/

**Finding:** durable learning after consequential execution has established operational value. However, a full postmortem is too heavy for every development Task; ADS should use proportional Task Learning Evidence with `NONE_MATERIAL` for simple work.

### 3.2 W3C PROV separates Entity, Activity and Agent provenance

W3C PROV-O models provenance using distinct `Entity`, `Activity` and `Agent` concepts and relations such as generation, usage, derivation, association and delegation.

Source:

- https://www.w3.org/TR/prov-o/

**Finding:** ADS learning/capability/evolution evidence should bind artifacts, execution activity and responsible Agent/operator explicitly instead of storing unqualified prose. ADS does not need RDF/PROV-O as a required wire format; the provenance separation is the useful Product lesson.

## 4. External evidence — Agent capability discovery and communication are becoming protocol concerns

### 4.1 A2A 1.0 provides capability discovery and task/message separation

The Agent2Agent protocol is an open interoperability protocol for independent Agents. Its current specification defines Agent Cards/capabilities, capability validation, task lifecycle, messages, artifacts, streaming and push notification mechanisms. It also explicitly separates Messages from Task output Artifacts and warns that transient Messages are not necessarily reliable storage for critical information.

Sources:

- https://a2a-protocol.org/v1.0.0/
- https://a2a-protocol.org/dev/specification/
- Linux Foundation A2A project announcement: https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents

**Finding:** v4.8 should keep its conceptual exchange model transport/provider neutral and should be able to map to A2A-style capability/task/message transports. ADS must still keep its stronger durable authority/exact-subject semantics; external protocol task state cannot automatically become ADS Validation/Review/Release truth.

### 4.2 Capability declaration alone is not sufficient evidence

A2A requires clients to inspect declared capabilities before attempting optional operations, but a declaration does not prove the quality/correctness of arbitrary engineering execution.

**Finding:** ADS must distinguish `declared capability`, `current availability` and `observed/proven execution evidence`. Historical success may improve assignment confidence but cannot substitute for current Validation.

## 5. External evidence — event exchange benefits from stable identity and deduplication

CloudEvents provides a vendor-neutral event format and requires stable context attributes such as `id`, `source`, `specversion` and `type`; `source + id` is defined so consumers can treat duplicates deterministically.

Source:

- https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md

**Finding:** an ADS Agent Exchange binding should include protocol version, exchange identity, source/operator provenance, semantic type, subject/correlation and replay/idempotency identity. ADS does not need to adopt CloudEvents wholesale; it can reuse the proven envelope principles.

## 6. External evidence — resource scheduling should separate feasibility from optimization

Kubernetes scheduler first filters Nodes that cannot satisfy a Pod's constraints/resources, then scores feasible Nodes and binds one placement. Its documented factors include resource requirements, hardware/software/policy constraints, affinity/anti-affinity, data locality and interference.

Source:

- https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/

**Finding:** ADS should use the same Product-level separation:

```text
hard eligibility / authority / environment / independence filters
        ↓
feasible Agent/resource set
        ↓
optional project-defined ranking/optimization
        ↓
existing Dispatch/Claim admission
```

This avoids cost/throughput scoring weakening correctness gates.

## 7. Product correction 1 — Task Learning Evidence, not universal retrospective authority

The Draft PRD's Task Learning Record is supported with these corrections.

### Required concept

A compact durable record of **material execution learning** may contain:

```text
subject/task refs
material decision summary + engineering rationale
unexpected failure/constraint discovered
Task Pack/L3 deviation or clarification
reusable invariant / failure family
known limitation / technical debt
Validation/Review/source/test refs
standard-friction classification
confidence/disposition/currentness
```

### Not required

- private chain-of-thought;
- narration of every implementation step;
- duplicate copies of PR/Validation/Review evidence;
- a new Product/Architecture authority;
- a full retrospective for ordinary Fast-Path work.

### Consistency levels

1. **identity-bound** — exact subject/current authority refs;
2. **behavior-supported** — executable/source/evidence refs for material behavioral claims;
3. **independently challenged where risk requires** — required Review detects material mismatch.

A rationale can be recorded without claiming it is mathematically proven. Tests prove behavior/invariants, not hidden reasoning.

## 8. Product correction 2 — Capability Claim + Capability Evidence, not one score

L1 supports provider-neutral capability routing, but rejects a universal scalar Agent quality score.

Minimum conceptual split:

```text
Capability Claim
  what this Agent/runtime says it can do

Availability / Resource Fact
  what is currently reachable/available

Capability Evidence
  what exact kinds of work/environments were actually executed and validated
```

Examples of dimensions:

```text
reasoning/architecture
coding/refactor
review eligibility
real-host/platform validation
languages/archetypes
tool/connectors
environments/device
agent_freedom ceiling
cost/latency class
parallel capacity
independence constraints
```

Provider/model identity is provenance, not normative routing policy by itself.

## 9. Product correction 3 — Constraint-first scheduling

L1 supports a standard scheduling semantic, not a mandatory scheduler implementation.

Hard filters include:

```text
Task dependency/ready state
authority + agent_freedom
required capability/environment
write-set/concurrency compatibility
reviewer/validator independence
required exact identity/currentness
claim serialization availability
security/side-effect authorization boundary
```

Only after filtering may a project/controller optimize for:

```text
priority / critical path
cost/latency
queue age
resource utilization
retry/escalation history
host/device scarcity
integration drift risk
```

No optimizer may convert an ineligible Agent into an eligible one.

## 10. Product correction 4 — Exchange Binding, not parallel lifecycle

L1 supports a transport-neutral Agent Exchange **binding/envelope** over existing ADS semantic owners.

The envelope should be able to carry/reference existing semantic objects such as Dispatch, Claim, Result, Blocker, Handoff, Review/Validation request/result and decision request/result.

It should provide only cross-transport concerns such as:

```text
exchange identity + protocol version
sender/operator/session provenance
recipient role/capability target
operation/work-item/dispatch correlation
subject/exact identity where needed
authority refs
causation/reply refs
idempotency/replay/currentness
bounded payload or payload/artifact ref
transport metadata
```

Critical results must be persisted into existing durable ADS/GitHub evidence owners. Transient transport history is never sufficient for current authoritative state.

## 11. Product correction 5 — Evidence-driven evolution, not auto-standard mutation

L1 supports the Draft classification direction, narrowed into an explicit escalation ladder:

```text
OBSERVATION
  -> classify project/agent/environment/spec/standard-friction
  -> STANDARD_FRICTION_CANDIDATE when material/repeatable
  -> evidence aggregation across tasks/projects where available
  -> ADS_EVOLUTION_CANDIDATE
  -> normal ADS Intake / L1 / PRD / L2 / Task / Review / Validation
  -> STANDARD_CHANGE | NO_CHANGE | MORE_EVIDENCE
```

### Promotion must consider

- materiality/risk;
- recurrence or strong single counterexample;
- independent reproduction where feasible;
- affected ADS authority and version;
- project diversity/comparability;
- whether the root cause is actually standard, Agent execution, environment or project-specific policy;
- measurable costs/failures rather than unsupported preference.

No numeric universal threshold is frozen at Product level; L2 may define a deterministic candidate policy with project override boundaries.

## 12. Privacy / security correction

Cross-project learning/metrics can leak code, customer data, prompts, hidden evaluation material, credentials or internal performance data.

v4.8 Product therefore requires:

- minimum necessary evidence;
- references/digests instead of copied sensitive bodies where possible;
- no secrets/credentials/private chain-of-thought;
- explicit project-private vs publishable evidence classification;
- aggregate statistics only when the source population/meaning remains truthful;
- no use of capability/telemetry to infer mutation authority.

## 13. Fast Path correction

v4.8 must remain optional/proportional for trivial work.

A low-risk single-Agent task may satisfy v4.8 with:

```text
no scheduler runtime
one eligible executor chosen directly
ordinary Dispatch/Claim semantics
Task Learning = NONE_MATERIAL when true
no cross-project evolution candidate
```

The version is successful only if it improves complex multi-Agent work without turning all maintenance into orchestration bureaucracy.

## 14. Product acceptance after L1

Recommended Product Freeze criteria:

1. Task completion has a proportionate way to preserve material reusable learning bound to evidence/currentness;
2. Task Learning never becomes a competing implementation/Product authority;
3. capability declaration, current availability and proven capability evidence are distinct;
4. Task requirements can be matched to provider-neutral Agent capability/environment/independence constraints;
5. scheduling filters hard constraints before optional optimization;
6. scheduling reuses current Dispatch/Claim/serialization authority;
7. no centralized scheduler service is mandatory;
8. Agent Exchange is a transport binding over existing ADS semantics, not a parallel lifecycle;
9. critical exchange results become durable authoritative facts and crash/restart does not depend on transient messages;
10. project feedback is classified before being promoted to Standard Friction;
11. ADS Evolution Candidates enter normal standard governance and cannot self-amend Frozen authority;
12. cross-project evidence has privacy/minimization rules;
13. `#469` remains measured dogfood until real evidence supports any L3 default;
14. Fast Path remains materially lighter than full orchestration;
15. dogfood must test heterogeneous Agent eligibility, resource contention, duplicate-dispatch exclusion, reviewer/validator independence, transport loss/replay, stale capability/currentness and false standard-friction promotion.

## 15. L1 architecture implications / questions for L2

If Product Freeze is authorized, L2 should decide:

1. whether Task Learning is a new small schema, an extension of completion/closeout evidence, or a profile over existing evidence contracts;
2. whether capability metadata extends existing execution/runner/skill profile contracts or gets one small dedicated evidence family;
3. exact relationship among capability claim, availability and capability evidence;
4. which Task requirements are machine-matchable and where human/strong-model judgment remains necessary;
5. whether scheduling policy belongs in `EXECUTION_ARCHITECTURE_STANDARD.md` as Filter/Score semantics plus project override hooks;
6. whether Agent Exchange is a new envelope schema, an extension to `ai-dev:event`/Dispatch binding, or adapters around existing objects;
7. minimum durable-materialization rules for transient exchanges;
8. replay/idempotency/correlation/security model across GitHub/webhook/queue/A2A adapters;
9. Standard Friction / Evolution Candidate artifact shape and promotion/currentness semantics;
10. dogfood design capable of falsifying benefits and exposing scheduler/exchange/knowledge overhead.

## 16. L1 disposition

**PROCEED_TO_PRODUCT_REVIEW = YES**

**PRODUCT_FREEZE = NOT_YET_AUTHORIZED**

A genuinely fresh high-capability Product reviewer should challenge this exact planning candidate after the Draft PRD is revised to the narrowed L1 shape. P0/P1 Product findings must be resolved before explicit Product Freeze.

`LOCAL_ENV=NOT_REQUIRED` for this L1 stage. Real heterogeneous-Agent/resource/transport claims belong to later executable dogfood/Validation and must not be inferred from this research.