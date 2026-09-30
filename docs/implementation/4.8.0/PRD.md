# ai-development-standard v4.8.0 PRD — Evidence-Driven Agent Orchestration & Standard Evolution

Status: **DRAFT PRODUCT AUTHORITY — NOT FROZEN**

Planning baseline: `main@e75fe834469c5ea9f9a384f7d84e38c3a48afa46`

This Draft PRD is a durable Product hypothesis. It MUST proceed through L1 Product Evidence, explicit Product Freeze, L2 Architecture Evidence/Freeze and only then Task DAG Freeze. It does not authorize implementation, new runtime infrastructure, schema migration, scheduler deployment, or modification of existing v4.1–v4.7 Frozen authority.

## 1. Product intent

v4.8.0 closes the loop between AI-assisted project execution and evolution of the AI Development Standard itself.

The Product goal is:

> A project can assign executable work to appropriate Agents using current capability, authority and resource facts; preserve important implementation learning as exact-subject evidence; coordinate Agents through transport-independent exchanges without weakening durable authority; and turn repeated, validated project friction into explicit ADS evolution candidates rather than ad-hoc standard drift.

v4.8 builds on v4.7 convergence. It does not replace Operation, Work Item, Task Pack, Execution Pack, Dispatch, Review, Validation, Release or canonical GitHub durable facts.

## 2. Product problem

The current ADS defines strong execution, validation, review, handoff and authority semantics, but five gaps remain at the system level.

### 2.1 Implementation knowledge is under-specified after Task completion

A Task can finish with code, tests, Validation and Review evidence while losing important reusable facts such as:

- why a material implementation choice was selected;
- what failure or ambiguity was discovered during implementation;
- what Task Pack/L3 assumption proved incomplete;
- which workaround or technical debt remains;
- which negative oracle caught the defect;
- whether the problem is project-local or evidence of ADS friction.

Issue/PR history may contain fragments, but ADS does not yet define a compact, exact-subject learning artifact or minimum completion-learning contract.

### 2.2 Model/risk policy is not yet a complete capability assignment contract

ADS already states that model strength follows task risk and that bounded lower-cost Agents can execute after Contract/Tests/Reference material exists. However, dispatch still lacks a general machine-readable way to compare Task requirements with an Agent's actual execution capabilities, environments, permissions and proven evidence.

### 2.3 Scheduling is insufficiently resource-aware

Canonical DAG/ready-state/claim semantics determine whether work is executable, but ADS does not yet define how a controller may choose among multiple READY Tasks and multiple eligible Agents according to:

- capability fit;
- environment availability;
- model/agent cost class;
- machine/device constraints;
- project concurrency limits;
- scarce shared resources;
- expected escalation risk;
- independence requirements.

### 2.4 Agent collaboration is GitHub-native but not yet transport-abstracted enough

GitHub is the durable reference implementation and should remain one canonical fact surface, but Agents may increasingly communicate through webhooks, local runtimes, queues, orchestration services or direct protocol adapters.

ADS needs a minimal exchange abstraction that preserves identity, authority, idempotency, provenance and exact-subject binding without making a message bus a new source of Product/Task truth.

### 2.5 Project execution does not yet form a disciplined ADS evolution loop

Projects discover recurring problems in prompts, Task Packs, Execution Packs, validation ownership, review coverage, capability routing and standard usability. Today those observations can become scattered Issues or local workarounds.

ADS needs a falsifiable feedback path that distinguishes:

```text
PROJECT_DEFECT
AGENT_EXECUTION_DEFECT
ENVIRONMENT_OR_TOOL_DEFECT
PROJECT_SPECIFIC_REQUIREMENT
STANDARD_FRICTION_CANDIDATE
ADS_EVOLUTION_CANDIDATE
```

and requires evidence before a local observation becomes a normative standard change.

## 3. Frozen-candidate Product shape

L1 should evaluate five Product concerns.

1. **Task Learning & Implementation Knowledge**
2. **Agent Capability & Assignment**
3. **Resource-Aware Scheduling**
4. **Agent Exchange & Collaboration**
5. **Evidence-Driven ADS Evolution Loop**

Two cross-cutting acceptance mechanisms are also proposed:

6. **Multi-Agent orchestration dogfood**
7. **Cross-project evolution dogfood**, including measured follow-up to `ai-development-standard#469`

The exact machine contracts, storage paths, scheduler algorithm and transport adapters belong to L2/implementation, not this Draft PRD.

## 4. Task Learning & Implementation Knowledge

v4.8 should define a compact **Task Learning Record** concept or compatible equivalent.

Its purpose is not to create another design authority or force long retrospective documents. It captures only material reusable learning discovered during execution.

Candidate minimum dimensions:

```text
task / work-item identity
implementation exact subject (commit/tree/PR as applicable)
authority refs (Frozen Product/L2/Task Pack/Execution Pack)
material implementation decisions
encountered failures / surprises
Task Pack/L3 deviations or clarifications
reusable constraints / invariants discovered
technical debt / known limitations
validation/review evidence refs
standard-friction observations
knowledge status / confidence / disposition
```

### Product invariants

- learning records are subordinate to current Product/Architecture/Task authority;
- they do not expose or require private chain-of-thought;
- implementation rationale is recorded as concise engineering justification, not hidden reasoning transcript;
- claims about behavior should point to code/tests/evidence where feasible;
- records bind to exact implementation identity when their truth depends on exact code;
- later code drift must not silently inherit stale implementation claims;
- project-specific experience does not automatically become cross-project standard authority.

### Proportionality

Small/Fast-Path work may record only `NONE_MATERIAL` plus required evidence refs. High-risk or surprising work should record the material learning necessary for future maintenance/refactor and standard feedback.

## 5. Knowledge-to-implementation consistency

v4.8 must distinguish three levels of consistency.

### Identity consistency

The learning record points to the actual implementation subject and current authority identities.

### Behavioral consistency

Material behavioral claims should be backed by executable tests, validation evidence, source references or explicit limitations.

### Independent consistency for high-risk work

When Review is required, the reviewer should detect material mismatch between claimed implementation decisions/constraints and the actual exact subject.

A record saying `fail closed` without a corresponding reachable rejection behavior must not be accepted merely because the prose exists.

Engineering rationale itself is not generally executable proof; v4.8 should verify the claimed constraints and evidence rather than pretend to prove private reasoning.

## 6. Agent Capability Profile

v4.8 should generalize model-selection policy into a provider-neutral capability description.

Candidate capability dimensions include:

```text
reasoning / architecture capability
coding / refactor capability
review capability
validation / real-host capability
available tools / connectors
environments / OS / runtime / device access
repository / external-system access
context-window or context-handling class
cost / latency class
parallel execution capacity
independence eligibility
supported agent_freedom levels
historically proven execution profiles
```

### Product invariants

- declared capability is not proven capability;
- provider/model name is provenance, not sufficient capability proof;
- prior success may influence assignment but never replaces current Task Validation;
- credentials/tool availability do not imply mutation or side-effect authority;
- capability description does not grant Product/Architecture/Task authority;
- dynamic Agent/session identity remains distinct from durable capability class/profile.

## 7. Capability-aware assignment

A controller may derive candidate assignment from:

```text
READY Work Items
+ Task requirements / risk / agent_freedom
+ required environment / tools
+ independence constraints
+ Agent Capability Profiles
+ current resource availability
+ project policy / budget
= derived Assignment Plan
```

The Assignment Plan is a controller decision/derived artifact. Existing Dispatch/Claim semantics remain the execution admission boundary.

### Assignment must fail closed when

- no eligible Agent satisfies required authority/environment/profile;
- capability evidence is stale or materially ambiguous;
- reviewer/validator independence would be violated;
- Task requires stronger semantic authority than the candidate Agent may exercise;
- the required real platform/resource is unavailable;
- scheduling would create an incompatible duplicate active execution.

## 8. Resource-Aware Scheduling

v4.8 should define policy for controllers that schedule READY work without making a centralized scheduler mandatory.

Scheduling may consider:

```text
Task priority / dependency criticality
eligible Agent set
Agent concurrency limits
host CPU/memory/GPU/device capacity
scarce Build Host / platform availability
external API / quota limits
budget / cost class
expected duration or retry history
integration/write-set conflict risk
required reviewer/validator independence
```

### Hard constraints before optimization

Authority, dependency, exact-base, write-set, validation, review and independence constraints are hard gates. Cost/throughput optimization happens only among conforming choices.

### Concurrency rules

v4.8 must compose with the existing duplicate-dispatch / atomic claim / serialization rules. It must not create a new claim authority.

Projects should be able to declare bounded parallelism at project, capability/resource and work-item classes. The standard should define semantics, not mandate one scheduler implementation.

## 9. Agent Exchange & Collaboration

v4.8 should define a minimal **Agent Exchange Envelope** or compatible abstraction for messages exchanged between logical Agents/controllers.

Candidate exchange families reuse existing semantics rather than inventing new lifecycle truth:

```text
DISPATCH / CLAIM
RESULT
BLOCKER
HANDOFF
REVIEW_REQUEST / REVIEW_RESULT
VALIDATION_REQUEST / VALIDATION_RESULT
DECISION_REQUEST / DECISION_RESULT
PROGRESS / HEARTBEAT where non-authoritative
```

Candidate common envelope fields:

```text
exchange_id
operation/work-item/dispatch refs
sender role/operator/session
intended receiver role/capability
subject / exact identity when applicable
authority refs
message type + protocol version
causation / correlation refs
created_at / expiry where relevant
idempotency / replay identity
payload ref or bounded payload
provenance / transport metadata
```

### Transport rule

Transport is replaceable:

```text
GitHub Issue/PR/event
webhook
local runtime IPC
message queue / stream
orchestrator service
future Agent-to-Agent protocol adapter
```

But transport is **not authority**. Material state/gate/side-effect results must become canonical durable facts under the existing owner contracts.

### Recovery rule

A fresh controller must be able to reconstruct authoritative current state without relying on transient queue contents or chat history.

## 10. Evidence-Driven ADS Evolution Loop

v4.8 should make project feedback a first-class but non-normative evidence source.

Candidate lifecycle:

```text
Task execution
  -> Task Learning Record
  -> project-local classification
  -> repeated / material Standard Friction Candidate
  -> cross-project or repeated evidence aggregation
  -> ADS Evolution Candidate
  -> normal ADS Product/L1/L2/Task/Review/Validation process
  -> standard change or NO_CHANGE/MORE_EVIDENCE
```

### Required classification discipline

An observed problem must be classified before it can propose standard mutation. At minimum distinguish:

```text
PROJECT_DEFECT
AGENT_EXECUTION_DEFECT
ENVIRONMENT_OR_TOOL_DEFECT
PROJECT_SPECIFIC_REQUIREMENT
STANDARD_FRICTION_CANDIDATE
ADS_EVOLUTION_CANDIDATE
```

The same symptom repeated across independent projects/tasks materially strengthens standard-level evidence, but repetition alone is not causal proof.

### No self-amending standard

Projects and Agents may create evidence and candidate Issues. They may not automatically edit Frozen ADS authority because a heuristic threshold fired. Normative ADS changes still follow ordinary Product/L1/L2/Task/Review/Validation/Release governance.

## 11. Relationship to `#469` L3 hybrid dogfood

`ai-development-standard#469` remains evidence collection, not normative adoption.

v4.8 should consume its measured findings after real low-cost local execution exists, especially:

- strong-model preparation vs low-cost executor division;
- contract/write-set drift caught;
- negative-oracle effectiveness;
- clarification/escalation count;
- stale L3/base rebinding;
- local edit/build/test loops;
- strong-model vs local-model effort/cost;
- independent Review findings and rework.

The Product must not mandate a blanket multi-file L3 pack or claim cost savings until evidence supports the claim.

## 12. Interaction with existing ADS owners

v4.8 must preserve and compose with existing authority.

```text
Product / L1 / L2 / Task authority        retained
Task DAG / Issue Dependencies             retained
Task Pack / Execution Pack                retained
Operation / Dispatch / claim              retained
Review / Assurance                         retained
Validation / exact-subject evidence       retained
Release / Deployment / Runtime owners     retained
v4.6 Context / Skill / Autonomy owners    retained
v4.7 registry / read-routing convergence  retained
```

v4.8 may add metadata or derived policies only where a new semantic owner is genuinely required.

It must not create competing workflow-state, gate-state or lifecycle authorities.

## 13. Security / privacy / trust posture

- learning records must not capture secrets, credentials, private chain-of-thought or hidden evaluator material;
- capability records must not expose secret values merely to prove tool access;
- transport/envelope provenance must distinguish claimed identity from authenticated transport identity;
- scheduling cannot infer authorization from tool, credential or network availability;
- external side effects remain governed by existing explicit authority contracts;
- performance/history data should be minimized to what is necessary for assignment/evolution evidence.

## 14. Observability and metrics

v4.8 may define evidence-friendly execution metrics, but must avoid false precision.

Useful observed metrics include:

```text
clarifications / escalations
attempt / repair loops
validation/review failures
contract/write-set drift findings
stale/rebind events
elapsed execution time where measured
strong-model vs bounded-agent usage where observable
resource utilization class
queue/wait time
final outcome / rework
```

Metrics describe observed execution and may support comparisons. They must not become unsupported causal claims such as `Agent X is 30% better` without comparable populations and controlled evidence.

## 15. Product acceptance

v4.8 Product is complete when the standard can support all of the following without adding competing authority:

1. a completed Task can preserve material reusable implementation learning tied to exact subject/evidence;
2. small tasks can explicitly record no material learning without mandatory retrospective bloat;
3. Task requirements can be compared with provider-neutral Agent capability facts;
4. capability claims are distinguished from observed/proven execution evidence;
5. a controller can derive an eligible Agent assignment without bypassing Dispatch/Claim authority;
6. projects can bound parallelism and scarce-resource use while preserving dependency/independence gates;
7. Agent exchanges can use GitHub or another transport while retaining one durable authoritative fact chain;
8. crash/restart can recover current authoritative state without transient transport history;
9. project execution can emit classified Standard Friction evidence;
10. repeated/material friction can become an ADS Evolution Candidate through an explicit evidence threshold/process;
11. evolution candidates still enter ordinary ADS Product/L1/L2/implementation governance rather than self-amending the standard;
12. `#469` or successor dogfood produces measured evidence before any strong->low-cost L3 default is standardized;
13. integrated dogfood demonstrates multiple heterogeneous Agent profiles executing/validating/reviewing independent work without duplicate execution or independence leakage;
14. Fast Path remains proportionate and does not require full scheduling/learning machinery when one simple local execution is sufficient.

## 16. Non-goals

v4.8 does not:

- build a mandatory centralized scheduler service;
- replace GitHub as the current reference durable project fact system;
- mandate a specific Agent vendor/model/provider;
- infer authorization from capability;
- maintain a global score/ranking that automatically decides correctness;
- require every Task to have a long retrospective or L3 pack;
- expose private chain-of-thought;
- make historical performance substitute for current Validation/Review;
- automatically mutate ADS from project telemetry;
- create a second Task DAG, Operation lifecycle, Dispatch state machine, Review state or Validation state;
- guarantee cost/performance improvement before dogfood evidence exists.

## 17. L1 questions that must be answered before Product Freeze

L1 must explicitly test at least:

1. Is a Task Learning Record a genuinely missing durable artifact, or can existing PR/Issue/Execution Pack structures satisfy the need with a smaller extension?
2. Which learning fields are valuable enough to standardize without turning every Task into retrospective bureaucracy?
3. What evidence is sufficient to say a learning claim matches implementation?
4. Should capability be a new machine contract, a profile extension, or a derived view over existing Dispatch/Skill/Runner data?
5. Which scheduling constraints belong in ADS semantics versus project-specific scheduler policy?
6. Can transport-independent Agent Exchange reuse existing event/Dispatch/Operation contracts without a parallel protocol family?
7. Which exchange facts must be durably materialized and which may remain transient?
8. What minimum idempotency/replay/currentness semantics are necessary for multi-Agent exchange?
9. What evidence threshold should promote `STANDARD_FRICTION_CANDIDATE` to an ADS Evolution Candidate?
10. How should cross-project evidence avoid leaking project-private data?
11. Does #469 produce enough real evidence to standardize any strong-model L3 preparation defaults, or should v4.8 retain only a dogfood obligation?
12. What is the minimum Fast-Path posture that preserves proportionality?

## 18. Product Freeze rule

This Draft PRD is **not Frozen**.

Required next sequence:

```text
Draft PRD
-> L1 Product Evidence
-> revise Product scope
-> Fresh Independent Product Review when required by risk
-> explicit Product Freeze
-> L2 Architecture Evidence
-> Architecture UNKNOWN disposition / demos when required
-> L2 Freeze
-> Task DAG
-> Task Packs / L3 / Issue materialization
-> implementation
```

No Task DAG created before Product/L2 authority may be treated as executable or Frozen.
