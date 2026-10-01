# ai-development-standard v4.8.0 PRD — Evidence-Driven Agent Orchestration & Standard Evolution

Status: **FROZEN PRODUCT AUTHORITY — 2026-10-01**

Planning baseline: `main@e75fe834469c5ea9f9a384f7d84e38c3a48afa46`

L1 evidence: `docs/implementation/4.8.0/L1_PRODUCT_EVIDENCE.md`

This PRD is Frozen Product Authority after L1 research/currentness repair and Fresh Independent Product Review R3 #490. It does not itself authorize implementation, schema migration, scheduler deployment, new Agent runtime infrastructure, or changes to existing v4.1–v4.7 Frozen semantics.

## 1. Product intent

v4.8.0 closes the feedback and allocation loop around the existing ADS execution model.

The Product goal is:

> A project can preserve material implementation learning as evidence, determine which currently available Agents/resources are eligible for work, select among eligible choices without weakening authority or independence, exchange work across transports while retaining one durable fact chain, and turn repeated validated project friction into explicit ADS evolution candidates that still pass normal ADS governance.

v4.8 builds on v4.7 convergence and preserves existing Product/L1/L2/Task, Task DAG, Task Pack, Execution Pack, Operation, Dispatch/Claim, Review, Validation, Release, Deployment and Runtime authorities.

## 2. Product problems

### 2.1 Material implementation learning can disappear after Task completion

A Task may finish with code/tests/Validation/Review while future maintainers still lack concise durable knowledge about:

- why a material implementation choice was selected;
- what failure/constraint was discovered only during implementation;
- where Task Pack/L3 needed clarification or proved incomplete;
- which reusable invariant or negative oracle mattered;
- what technical debt/limitation remains;
- whether observed friction appears project-local, Agent-local, environment-local or standard-level.

### 2.2 Existing model/risk policy lacks a complete eligibility evidence model

ADS already routes Strong vs bounded/local work by risk, but does not yet define a provider-neutral way to distinguish:

```text
declared capability
current environment/resource availability
observed/proven capability evidence
```

or compare those facts with Task requirements and independence constraints.

### 2.3 Ready-set scheduling lacks standard resource-selection semantics

ADS can compute READY work and serialize dispatch/claim, but it does not yet define a standard separation between:

```text
hard eligibility constraints
vs
optional cost/throughput/priority optimization
```

when multiple Tasks/Agents/hosts/devices are simultaneously available.

### 2.4 Agent communication is durable/GitHub-native but transport binding is not generalized

GitHub remains the reference durable fact system, but future execution may use webhooks, queues, local runtimes, orchestration services or Agent-to-Agent protocols. ADS needs a small transport-neutral binding that preserves identity, provenance, correlation, replay/idempotency and exact-subject semantics without creating another lifecycle.

### 2.5 Project experience is not yet a disciplined ADS evolution input

Projects discover standard friction, but local observations can be confused with Agent defects, environment failures or project-specific requirements. ADS needs a classification/promotion process so project learning can become evidence for standard evolution without automatic standard mutation.

## 3. Product shape

v4.8 freezes these five concerns:

1. **Task Learning Evidence**
2. **Agent Capability Evidence & Eligibility**
3. **Constraint-first Assignment & Resource Scheduling**
4. **Transport-neutral Agent Exchange Binding**
5. **Evidence-driven ADS Evolution Feedback**

Two cross-cutting acceptance mechanisms are required:

6. **Heterogeneous Multi-Agent Orchestration Dogfood**
7. **Cross-project Evolution Dogfood**, including measured follow-up to `ai-development-standard#469`

## 4. Task Learning Evidence

v4.8 requires a proportionate way to preserve material reusable execution learning after Task completion.

The implementation may be a small schema/profile/closeout extension; Product does not require a new standalone authority document.

Minimum semantic dimensions:

```text
work-item/task identity
implementation exact subject where relevant
current authority refs
material decision summary + concise engineering rationale
unexpected failure/constraint discovered
Task Pack/L3 deviation or clarification
reusable invariant / failure family
known limitation / technical debt
source/test/Validation/Review evidence refs
standard-friction classification when applicable
currentness / disposition
```

### 4.1 Hard rules

- Task Learning is evidence/history, not Product/Architecture/Task authority.
- It MUST NOT expose or require private chain-of-thought.
- It MUST NOT duplicate large PR/Validation/Review bodies when references suffice.
- Exact-code behavioral claims bind to the exact subject they describe.
- Later code drift does not silently inherit stale learning claims.
- Material behavioral claims should be supported by source/tests/Validation or explicit limitation.
- Where Review is required, material mismatch between learning claims and actual implementation is reviewable.

### 4.2 Proportionality

Fast-Path/simple work may record:

```text
TASK_LEARNING=NONE_MATERIAL
```

plus ordinary evidence refs. A long retrospective is not mandatory.

## 5. Agent Capability Evidence & Eligibility

v4.8 standardizes a provider-neutral eligibility model, not a universal Agent ranking.

### 5.1 Required conceptual split

```text
Capability Claim
  what an Agent/runtime declares it can perform

Availability / Resource Fact
  what environment/tool/resource is currently reachable

Capability Evidence
  what kinds of execution have actually been observed/validated
```

Candidate dimensions include:

```text
reasoning / architecture
coding / refactor
review eligibility
validation / real-host ability
languages / archetypes
tools / connectors
environments / OS / runtimes / devices
repository / external-system access class
agent_freedom ceiling
cost / latency class
parallel capacity
independence eligibility
observed execution profile refs
```

### 5.2 Hard rules

- declared capability != proven capability;
- capability != authorization;
- tool/credential availability != mutation/side-effect permission;
- provider/model name is provenance, not sufficient eligibility proof;
- historical evidence may inform assignment but never replaces current Validation;
- dynamic operator/session identity remains distinct from reusable capability profile/class;
- no global scalar quality score becomes correctness authority.

## 6. Constraint-first Assignment & Resource Scheduling

v4.8 standardizes scheduling semantics without requiring a centralized scheduler service.

### 6.1 Selection pipeline

```text
canonical READY set
        +
Task requirements / risk / freedom / environment / independence
        +
Capability Claims + current Availability + relevant Capability Evidence
        ↓
hard eligibility filtering
        ↓
feasible Agent/resource choices
        ↓
optional project-defined ranking/optimization
        ↓
existing Dispatch reservation / Claim admission
```

### 6.2 Hard filters

At minimum where applicable:

```text
Task dependency/current workflow state
Task Pack / Execution Pack currentness
authority + agent_freedom
required capability/environment/device
write-set/concurrency compatibility
reviewer/validator independence
exact subject/base/currentness
claim serialization availability
security/side-effect authority
project concurrency/resource limits
```

No cost/latency/priority rule may make an ineligible executor eligible.

### 6.3 Optional optimization

Projects/controllers MAY rank feasible choices by:

```text
priority / critical path
queue age
cost / latency class
resource utilization
host/device scarcity
retry/escalation history
integration drift risk
```

Optimization policy is project-configurable. ADS owns safety/meaning boundaries, not one universal scoring formula.

### 6.4 Concurrency

Existing duplicate-dispatch and atomic claim/serialization semantics remain canonical. v4.8 does not create another claim authority.

## 7. Transport-neutral Agent Exchange Binding

v4.8 defines a minimal exchange binding/envelope for moving existing ADS semantic objects between logical Agents/controllers across transports.

### 7.1 Exchange families

The binding may carry/reference existing semantics such as:

```text
DISPATCH / CLAIM
RESULT
BLOCKER
HANDOFF
REVIEW_REQUEST / REVIEW_RESULT
VALIDATION_REQUEST / VALIDATION_RESULT
DECISION_REQUEST / DECISION_RESULT
PROGRESS / HEARTBEAT when explicitly non-authoritative
```

It does not define replacement Review/Validation/Task states.

### 7.2 Common cross-transport metadata

Candidate minimum:

```text
exchange_id
protocol/binding version
operation / work-item / dispatch refs
sender role/operator/session provenance
intended receiver role/capability target
subject/exact identity when applicable
authority refs
semantic message type
causation/correlation/reply refs
created/currentness/expiry where applicable
idempotency/replay identity
bounded payload or payload/artifact reference
transport provenance
```

### 7.3 Transport rule

Reference/allowed adapters may include:

```text
GitHub Issue/PR/event
webhook
local IPC/runtime
message queue/stream
orchestrator service
A2A-style Agent protocol adapter
```

Transport is never Product/Task/Gate authority by itself.

### 7.4 Durable materialization rule

Any exchange that changes authoritative workflow/gate/side-effect/evidence truth must be materialized through the existing canonical durable owner. Transient messages may carry progress but cannot be the only source required to reconstruct current authority.

Crash/restart must be able to reconstruct authoritative current state without private chat or transient queue history.

## 8. Evidence-driven ADS Evolution Feedback

v4.8 makes project execution a first-class evidence input to ADS evolution while preserving normal change governance.

### 8.1 Classification

At minimum distinguish:

```text
PROJECT_DEFECT
AGENT_EXECUTION_DEFECT
ENVIRONMENT_OR_TOOL_DEFECT
PROJECT_SPECIFIC_REQUIREMENT
STANDARD_FRICTION_CANDIDATE
ADS_EVOLUTION_CANDIDATE
```

### 8.2 Promotion path

```text
Task Learning / execution observation
  ↓
classification
  ↓
STANDARD_FRICTION_CANDIDATE when material/repeatable
  ↓
evidence aggregation / reproduction where feasible
  ↓
ADS_EVOLUTION_CANDIDATE
  ↓
ordinary ADS Intake -> L1 -> PRD -> L2 -> Task -> Review/Validation
  ↓
STANDARD_CHANGE | NO_CHANGE | MORE_EVIDENCE
```

### 8.3 Promotion evidence

Promotion should consider:

- materiality/risk;
- recurrence or a strong falsifying counterexample;
- independent reproduction where feasible;
- affected ADS owner/version;
- project diversity/comparability;
- measured failure/rework/friction;
- whether root cause is truly standard-level rather than project/Agent/environment-specific.

No universal numeric threshold is required at Product level.

### 8.4 No self-amending standard

No project telemetry, heuristic threshold, scheduler or Agent automatically mutates Frozen ADS authority. Evolution candidates re-enter the standard's normal governance.

## 9. Relationship to #469

`ai-development-standard#469` remains dogfood evidence collection.

v4.8 consumes measured results only after actual low-cost/local execution and relevant validation/review exist, including:

```text
clarification / escalation count
contract/write-set drift caught
negative-oracle effectiveness
stale L3/base rebinds
local edit-build-test loops
strong-model vs bounded-agent observed effort/cost
review findings and rework
```

v4.8 MUST NOT freeze a blanket multi-file L3 requirement or claim economic improvement from planning-only evidence.

## 10. Knowledge consistency model

A learning/feedback claim can have three distinct confidence layers:

```text
IDENTITY_BOUND
BEHAVIOR_SUPPORTED
INDEPENDENTLY_CHALLENGED
```

The layers do not collapse:

- correct SHA binding does not prove behavior;
- a passing test does not prove every stated rationale;
- reviewer agreement does not replace real execution evidence;
- historical capability success does not prove current Task PASS.

## 11. Security, privacy and trust

v4.8 requires:

- no secrets/credentials/private chain-of-thought in learning/capability/exchange records;
- references/digests rather than copied sensitive bodies where possible;
- explicit project-private vs publishable cross-project evidence handling;
- no hidden validation/evaluator leakage;
- authenticated transport identity distinguished from logical operator/session identity;
- capability/availability never interpreted as authority;
- minimum necessary performance/telemetry retention;
- external side effects continue to require existing explicit authority.

## 12. Evidence-friendly metrics

Observed metrics MAY include:

```text
clarifications / escalations
attempt / repair loops
validation/review failures
contract/write-set drift findings
stale/rebind events
elapsed time when actually measured
strong-model vs bounded-agent usage where observable
resource utilization class
queue/wait time
final outcome / rework
```

Metrics are descriptive evidence. They MUST NOT be converted into unsupported causal claims or universal Agent rankings without comparable populations and sufficient methodology.

## 13. Interaction with existing ADS owners

v4.8 preserves:

```text
Product / L1 / L2 / Task authority
Task DAG / native Issue Dependencies
Task Pack / Execution Pack
Operation / Work Item
Dispatch / Claim / serialization
Review / Assurance
Validation / exact-subject evidence
Release / Deployment / Runtime / Incident / Maintenance
v4.6 Intent / Context / Skill / Autonomy owners
v4.7 authority registry / read routing / conformance
```

v4.8 may extend existing owner standards or add small machine metadata families only when L2 shows a genuine semantic gap.

## 14. Multi-Agent orchestration dogfood

A conforming dogfood must attempt to falsify the design with at least:

- heterogeneous Agent capability profiles;
- multiple simultaneously READY Tasks;
- scarce shared host/device/resource;
- incompatible duplicate assignment race;
- reviewer/validator independence conflict;
- stale capability/availability data;
- Task/base/currentness drift;
- transport duplicate/replay/loss/recovery;
- Agent unable to satisfy declared capability;
- higher-cost Agent unnecessary for a bounded task;
- lower-cost Agent escalation on semantic ambiguity;
- restart reconstruction from durable facts only.

Synthetic/reference-model proof must remain labeled synthetic. Claims about real external runtimes/hosts require real Validation.

## 15. Cross-project evolution dogfood

At least one dogfood path should gather friction evidence from more than one Task/project when available and test:

```text
observation classification
false-positive prevention
privacy/minimization
repeated friction aggregation
promotion to ADS Evolution Candidate
NO_CHANGE / MORE_EVIDENCE route
```

`#469` is one seed evidence stream but cannot be the only basis for a broad economic/performance claim.

## 16. Fast Path

A low-risk simple single-Agent task may remain:

```text
one directly eligible executor
ordinary Dispatch/Claim or current Fast-Path equivalent
no scheduler runtime
TASK_LEARNING=NONE_MATERIAL when true
no evolution candidate
```

v4.8 is not successful if it makes trivial maintenance materially harder.

## 17. Product acceptance

v4.8 Product is complete when:

1. material Task execution learning can be preserved compactly and tied to exact subject/evidence;
2. simple work can explicitly record no material learning;
3. Task Learning remains evidence/history rather than mutation authority;
4. capability claim, current availability and proven capability evidence are distinct;
5. provider/model identity is not itself an eligibility/correctness verdict;
6. hard eligibility filters run before optimization/ranking;
7. Task requirements can be matched to Agent/environment/independence/resource constraints;
8. existing Dispatch/Claim/serialization remains execution admission authority;
9. no centralized scheduler implementation is mandatory;
10. transport-neutral exchange can map to GitHub and non-GitHub channels without a second lifecycle;
11. critical exchange results become durable authoritative facts;
12. restart/recovery does not depend on transient transport or chat;
13. project observations are classified before standard-friction promotion;
14. ADS evolution candidates require evidence and still enter normal ADS governance;
15. cross-project feedback minimizes private/sensitive data;
16. #469 remains dogfood until real evidence supports a normative L3 change;
17. multi-Agent dogfood proves/falsifies eligibility, resource contention, concurrency and independence behavior;
18. Fast Path remains proportional.

## 18. Non-goals

v4.8 does not:

- build a mandatory centralized scheduler/orchestrator service;
- replace GitHub as the current reference durable project fact surface;
- mandate a vendor/model/provider;
- infer authority from capability/tool/credential availability;
- create a global Agent score or leaderboard as correctness authority;
- require every Task to produce a long retrospective or large L3 pack;
- expose private chain-of-thought;
- make historical performance substitute for current Validation/Review;
- automatically modify ADS from telemetry;
- create another Task DAG, Operation lifecycle, Dispatch state machine, Review state or Validation state;
- adopt A2A, CloudEvents, PROV or Kubernetes as normative wire/runtime dependencies;
- guarantee economic/performance improvement before measured dogfood evidence.

## 19. Product Freeze record

Product Freeze is explicitly authorized and recorded after Fresh Independent Product Review R3 #490:

```text
review_subject_head = b8c3879a65c9159759457744c2a24e7e5777c8c1
review_subject_tree = 14c1bf8dd4e684b90c633ca50ff1762471f21f1c
review_main = e75fe834469c5ea9f9a384f7d84e38c3a48afa46
dogfood_input = #469@5925124956
review_verdict = PASS
product_freeze_authorization = YES
P0 = 0
P1 = 0
P2 = 0
P3 = 0
```

The Freeze basis includes the bounded currentness repair #489 and treats #488 as historical stale-input review evidence only. Immediately before this Freeze record, Controller re-read #469 and found no materially newer checkpoint than `5925124956`; therefore the #490 before/after currentness result remains valid.

This Product Freeze does not authorize implementation, schema migration, scheduler deployment, new Agent runtime infrastructure, L2 conclusions, Task DAG execution, or changes to existing v4.1–v4.7 Frozen semantics. Proceed next to L2 Architecture Evidence and Architecture UNKNOWN disposition. Only after L2 Freeze may Task DAG become Frozen/executable planning authority.

If later evidence demonstrates a material contradiction in this Frozen Product authority, the contradiction must be recorded explicitly and the Product scope reopened through normal ADS governance; implementation findings do not silently rewrite Frozen Product semantics.

`LOCAL_ENV=NOT_REQUIRED` for Product Freeze. Real Agent/resource/transport claims remain later dogfood/Validation concerns.