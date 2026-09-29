# ai-development-standard v4.6.0 PRD — AI-native / Agentic Development Governance

Status: **DRAFT PRODUCT AUTHORITY — requires L1 Product Evidence review and explicit PRD Freeze before implementation**

## 1. Product intent

v4.6.0 makes AI-native development a first-class governance layer across the entire software lifecycle. The goal is not to add model-specific tricks or prompt folklore; it is to standardize durable principles that remain valid as models improve: intent capture, context authority, Agent autonomy, skill/prompt governance, AI-generated change assurance, provenance, handoff/recovery and low-ceremony Fast Path execution.

The version should ensure that an unfamiliar capable Agent can safely participate in Product, Architecture, Planning, Implementation, Review, Validation, Release and Operations without relying on hidden chat history or model-specific assumptions.

## 2. Problem

Traditional software standards assume that a human developer retains context, intent and tacit reasoning. AI-native development breaks that assumption:

- user intent often starts as natural-language chat, screenshots or loosely specified goals;
- context is assembled dynamically from repository files, Issues, standards, memory, tools and current source;
- Agents may infer assumptions that look plausible but are not product facts;
- prompts/skills can behave like executable procedures but are often unmanaged text;
- model/session changes can erase working context;
- AI-generated code may compile while misunderstanding intent, inventing APIs/business rules or weakening tests;
- multiple models/roles require explicit autonomy, independence and handoff rules;
- chat-only success claims are not durable project state.

v4 already contains important pieces such as Task/Execution Packs, agent_freedom, pointer-only triggers, GitHub durable facts, independent review, model routing and Hidden Validation. v4.6 must converge these into one coherent AI-native governance layer without duplicating their existing normative owners.

## 3. Scope

### 3.1 Intent → Spec Governance

Standardize the transition from human natural-language intent to durable product/task authority.

Core distinctions:

```text
USER_INTENT
INTERPRETATION
ASSUMPTION
UNKNOWN
DECISION_REQUIRED
DURABLE_REQUIREMENT
```

Required rules:

- chat intent is not automatically Frozen Product Authority;
- material Agent inference must not silently become product truth;
- unresolved high-impact UNKNOWNs must remain explicit until resolved by the appropriate authority;
- low-risk details may be completed under bounded autonomy when policy allows;
- acceptance criteria and durable authority should capture the result before downstream Agents depend on it.

### 3.2 Context Engineering Standard

Define context authority, precedence, freshness and minimum currentness checks.

Context may include:

```text
system/organization instructions
pinned ADS revision
repository AGENTS / project overrides
Frozen Product / Architecture
Task DAG / Task Pack
Execution Pack / Dispatch
Issue / PR / structured events
source/tests/evidence
historical chat/memory
```

Required principles:

- higher-authority durable facts override lower-authority historical context;
- stale chat/memory MUST NOT override current Git/GitHub facts;
- exact-currentness-sensitive operations must re-read live subject identity before acting;
- required project truth MUST NOT exist only in ephemeral chat context;
- context selection should use progressive disclosure rather than dumping the entire repository into every Agent invocation.

### 3.3 Prompt / Skill Governance

Define durable categories and ownership for reusable Agent behavior.

Proposed separation:

```text
Stable repository/Agent rules  → standard / AGENTS / policy
Reusable procedure             → Skill
Project/domain durable fact    → project docs/contracts
Task-specific authority        → Task/Execution Pack
Invocation                     → short pointer/dispatch
Ephemeral discussion           → chat
```

For material reusable Skills/Agent procedures, support metadata such as:

```text
identity/version
scope
required inputs
allowed tools/side effects
outputs
failure behavior
validation/evaluation
compatibility
source/maintenance owner
```

Skills/prompts must remain subordinate to Product/Architecture/Task/Validation authority.

### 3.4 Agent Autonomy & Escalation

Converge and clarify existing bounded freedom semantics.

Current freedom model is retained as the starting point:

```text
F0_MECHANICAL
F1_BOUNDED_IMPLEMENTATION
F2_ENGINEERING_DISCRETION
F3_ARCHITECTURE_REQUIRED
```

v4.6 should define cross-lifecycle escalation rules, including:

- when an Agent may autonomously repair mechanical/internal issues;
- when a public contract/product behavior/security/data/architecture decision exceeds granted authority;
- prohibition on self-promoting autonomy level;
- explicit BLOCKED/CONTRADICTION/DECISION_REQUIRED paths;
- human authority where destructive/production-sensitive actions require it.

### 3.5 AI-generated Change Assurance

Define risk-based assurance specifically for AI-generated or Agent-authored changes.

Review dimensions should include, where material:

```text
intent alignment
architecture alignment
unsupported assumptions
invented APIs/contracts/domain rules
security shortcuts
silent dependency/toolchain invention
silent test weakening
unnecessary complexity
scope/write-set compliance
```

The standard MUST NOT require human review for every AI-authored change. Assurance remains risk-based and composes with the existing Review Policy.

### 3.6 AI / Agent Provenance

Define what execution provenance must be retained when it materially affects trust/independence/reproducibility.

Potential facts:

```text
human intent owner / requesting authority
builder operator / dispatch
model capability class or provider/family when material
reviewer/validator identity
independence/model-diversity evidence when required
Task/Issue/PR/SHA bindings
```

Do not force full model parameter logging for trivial mechanical tasks. Provenance must be proportional to the evidence claim.

### 3.7 Agent Handoff & Context-loss Recovery

Formalize the invariant:

> No required development truth may exist only in a lost session/chat.

A successor Agent should be able to reconstruct:

```text
what was requested
what is frozen/current
exact source/task identity
what changed
what passed/failed/blocked
what remains
who/what owns next action
what must not be assumed
```

Prefer extension/convergence of existing handoff standards rather than creating parallel lifecycle models.

### 3.8 AI-native Fast Path Refinement

Preserve the benefit of conversational development for small/low-risk changes.

Core principle:

> Reduce ceremony, not truth.

Fast Path may omit heavy L1/L2/Task DAG/Execution Pack/Independent Review/Hidden Validation when risk and existing authority permit, while retaining required scope, identity, Git safety, focused testing/validation and integration truth.

Fast Path eligibility must be deterministic/risk-bounded enough that Agents cannot simply label difficult work “small” to bypass controls.

## 4. Non-goals

v4.6 does not:

- prescribe prompt-writing tricks or chain-of-thought techniques;
- mandate a specific LLM vendor/model;
- define permanent model rankings;
- require multiple Agents for every Task;
- require human review for all AI-generated code;
- store private chain-of-thought as project evidence;
- create a second Task/Review/Validation/Release state machine;
- replace domain-specific Harnesses or project Product/Architecture authority.

## 5. Cross-lifecycle model

AI-native governance is a vertical layer, not a new sequential stage:

```text
Product → Architecture → Planning → Code → Test → Release → Deploy → Operate
   │           │            │        │       │        │         │
   └───────────┴────────────┴────────┴───────┴────────┴─────────┘
                              │
                    AI-native Governance
          Intent / Context / Skills / Autonomy
          Assurance / Provenance / Handoff / Recovery
```

## 6. Machine-readable expectations

L2 should evaluate whether to extend existing schemas/events for:

- assumption/unknown/decision disposition;
- effective context/authority manifest references;
- Skill metadata;
- autonomy/escalation reason;
- Agent provenance;
- handoff/recovery state.

Prefer extending canonical objects over creating redundant parallel schemas.

## 7. Compatibility posture

Target: additive/non-weakening minor release. Existing v4 Agent/event/dispatch/review semantics remain authoritative and should be converged, not replaced. If a proposed unification requires incompatible wire/lifecycle changes, defer those semantics to a major-version path.

## 8. Product acceptance

v4.6.0 is complete when:

1. AI-native governance is explicit across the lifecycle rather than scattered implicit behavior;
2. chat-only information cannot become required hidden authority;
3. context precedence/currentness rules are deterministic enough for independent Agents;
4. intent assumptions/UNKNOWNs cannot silently become Frozen Product facts;
5. Skills/prompts have clear authority boundaries;
6. Agent autonomy/escalation is consistent with existing Task/Execution Pack freedom;
7. AI-generated change assurance is risk-based and does not eliminate Fast Path automation;
8. a fresh Agent can recover a non-trivial interrupted workflow using only durable GitHub/repository facts;
9. at least one dogfood scenario demonstrates session/model handoff without loss of authority truth.

## 9. Next gate

Before Freeze:

1. run L1 Product Evidence across Agent Skills/spec-driven development/context/handoff/provenance practices;
2. inventory existing v4 AI-native rules to avoid duplicate normative ownership;
3. revise and Freeze this PRD;
4. run L2 Architecture Evidence with explicit convergence plan;
5. generate Task DAG emphasizing extensions/adapters/migrations rather than parallel replacement systems.
