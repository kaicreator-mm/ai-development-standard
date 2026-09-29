# ai-development-standard v4.6.0 PRD — AI-native / Agentic Development Governance

Status: **FROZEN PRODUCT — 2026-09-30; authorized by Fresh Independent owner-currentness Review #280**

## 1. Product intent

v4.6.0 makes AI-native development a first-class **vertical governance layer** without replacing the v4 execution, assurance, handoff or release architecture already in place.

The Product goal is that an unfamiliar capable Agent can participate across Product, Architecture, Planning, Implementation, Review, Validation, Release, Deployment and Operations using durable authority rather than hidden chat/session context.

v4.6 adds only the cross-lifecycle governance that is currently missing. Existing owners remain authoritative wherever they already solve the problem.

## 2. New normative owners

Product Freeze establishes exactly three new owner domains:

1. **Intent & Assumption Governance**
2. **Context Engineering Standard**
3. **Skill / Reusable Agent Procedure Governance**

The following are **extensions/convergence of existing owners, not new parallel standards/state machines**:

- F0–F3 Agent autonomy / escalation;
- risk/model routing;
- Independent Review / assurance / model-diversity coverage;
- AI/Agent provenance;
- Dispatch / Local Agent handoff / context-loss recovery;
- Fast Path.

## 3. Intent & Assumption Governance

Natural-language intent and Agent interpretation MUST remain distinguishable until appropriately promoted into durable authority.

Core distinctions:

```text
USER_INTENT
INTERPRETATION
ASSUMPTION
UNKNOWN
DECISION_REQUIRED
DURABLE_REQUIREMENT
```

Required semantics:

- chat/user intent is not automatically Frozen Product Authority;
- material Agent interpretation MUST NOT be restated as user fact without evidence/authority;
- high-impact `ASSUMPTION` / `UNKNOWN` cannot silently become public contract, data semantic, security rule or architecture decision;
- low-risk details may be completed under granted autonomy;
- `DECISION_REQUIRED` routes to the applicable Product/Architecture/human authority;
- a `DURABLE_REQUIREMENT` exists only after promotion through the existing Product/Architecture/Task authority path;
- contradictions are preserved/routed rather than guessed away.

This standard feeds existing L1/PRD/Architecture/Task processes; it does not replace them.

## 4. Context Engineering Standard

Define effective context authority, currentness, provenance and progressive disclosure across sources such as:

```text
system / organization constraints
pinned ADS revision
repository AGENTS / project overrides
Frozen Product / Architecture
Task DAG / Task Pack
Execution Pack / Dispatch
Issue / PR / structured events
source / tests / evidence
approved external resources / tool results
historical chat / memory
```

Required semantics:

- current higher-authority durable facts override stale/lower-authority historical context;
- historical chat/memory MUST NOT override current Git/GitHub/Frozen authority;
- exact-currentness-sensitive actions re-read live identity before acting;
- required project truth MUST NOT exist only in ephemeral chat/session state;
- context is selected through progressive disclosure/materiality rather than unconditional repository-wide loading;
- external resource/tool output is evidence/data until promoted by the applicable authority;
- context provenance/currentness is recorded when material to a claim;
- insufficient/contradictory required context fails closed to UNKNOWN/BLOCKED/DECISION_REQUIRED rather than guessed truth.

Context Engineering is not another lifecycle state machine or project database.

## 5. Skill / Reusable Agent Procedure Governance

Durable reusable Agent behavior is separated from broad rules, project facts and one-off Task authority:

```text
Stable repository/Agent rules  -> standard / AGENTS / policy
Reusable procedure             -> Skill / reusable Agent procedure
Project/domain durable fact    -> project docs/contracts
Task-specific authority        -> Task Pack / Execution Pack / Issue
Invocation                     -> pointer / Dispatch
Ephemeral discussion           -> chat/session
```

Material reusable Skills/procedures should be able to declare:

```text
identity/version
source / maintenance owner
purpose / scope
trigger / applicability
required inputs / authority refs
allowed tools / side-effect classes
outputs / durable result surface
failure / escalation behavior
validation / evaluation refs
compatibility / deprecation
security / provenance notes
```

Required rules:

- Skill instructions remain subordinate to Frozen Product/Architecture/Task/Validation/Release authority;
- installing/possessing a Skill does not authorize its side effects;
- external/third-party Skills are untrusted executable/procedural content until accepted by project policy;
- secret values/hidden project authority MUST NOT be casually embedded in reusable Skills;
- one-off Task facts belong in Task/Execution authority rather than being promoted into a Skill for convenience;
- invocation remains a pointer/dispatch rather than a duplicate contract.

## 6. Existing autonomy & escalation — preserve F0–F3

The existing freedom vocabulary remains authoritative:

```text
F0_MECHANICAL
F1_BOUNDED_IMPLEMENTATION
F2_ENGINEERING_DISCRETION
F3_ARCHITECTURE_REQUIRED
```

v4.6 may provide cross-lifecycle mapping/clarification, but MUST NOT introduce a second autonomy scale.

Required invariants:

- Agent cannot self-promote freedom level;
- Product/public-contract/security/data/architecture decisions above granted authority route upward;
- destructive/production-sensitive actions still require applicable human/project authority where existing owners require it;
- capability/model strength does not itself grant authority.

## 7. Assurance & AI-generated change — extend current Assurance architecture

v4.6 MUST NOT introduce a second Review/Assurance result state or parallel assurance-plan family.

Current `assurance-plan-v1` / Review / Validation architecture remains authoritative. v4.6 may add AI-native coverage dimensions such as:

```text
intent alignment
unsupported assumptions
invented APIs/contracts/domain rules
architecture alignment
security shortcuts
silent dependency/toolchain invention
silent test weakening
scope/write-set compliance
unnecessary complexity
```

These are review/assurance coverage concerns, not new judgments.

AI-authored changes do not universally require human review. Review/assurance remains risk-based under existing policy.

## 8. Agent / model provenance — proportional extension

Existing event/assurance/review contracts already distinguish role, logical operator/session and transport account, and can carry reviewer model provenance when material.

v4.6 should standardize proportional provenance guidance:

```text
requesting / intent authority
builder / validator / reviewer logical operator
Task / Issue / PR / SHA bindings
model provider/family/configuration only when material to independence/audit/reproducibility
model-diversity evidence when explicitly required
```

Do not require private chain-of-thought, full token history, hidden reasoning or full model parameter logging as project evidence.

Same GitHub/API account does not imply same logical operator/context.

## 9. Handoff & context-loss recovery — generalize existing protocol

Frozen invariant:

> **No required development truth may exist only in a lost Agent/session/chat.**

Existing Dispatch / GitHub interaction / Local Agent Handoff remain owners. v4.6 requires that a successor Agent can reconstruct from durable facts:

```text
what was requested
what is frozen/current
exact subject/source identity
what changed
what passed/failed/blocked
what remains
who/what owns next action
what must not be assumed
```

No complete chat transcript is required as project authority.

## 10. Fast Path refinement

Core principle:

> **Reduce ceremony, not truth.**

Fast Path may omit non-material L1/L2/Task DAG/Execution Pack/Independent Review/Hidden Validation when existing Product/project/risk authority permits, while preserving applicable:

```text
scope / authority
Git/subject identity and safety
focused tests/checks
truthful Validation/evidence
integration result
```

An Agent cannot self-label risky/complex work as “small” to bypass Frozen or required gates.

## 11. Product-level forbidden inferences

v4.6 conformance MUST reject at least:

```text
user chat -> Frozen Product automatically
Agent interpretation -> user-stated fact
ASSUMPTION/UNKNOWN -> durable requirement without authority
historical chat/memory -> override current Git/GitHub/Frozen authority
larger context dump -> higher context quality automatically
external resource/tool output -> Product truth automatically
tool capability -> side-effect authority
Skill installed -> Skill trusted / action authorized
Skill instruction -> override Frozen Product/Architecture/Task
model capability -> F3 authority
same GitHub account -> same logical operator/context
AI-generated code compiles -> intent/domain correctness
AI-authored change -> mandatory human review universally
recorded model/provider -> independence automatically proven
Fast Path label -> required gates waived
```

## 12. Machine-readable expectations

L2 MUST **prefer extension/reuse before new schema creation**.

Evaluate:

1. Intent/Assumption disposition record/event only if cross-Agent durable promotion/currentness needs it.
2. Effective Context/Authority references only if deterministic pointers are insufficient; avoid full content snapshots.
3. Skill Metadata as the strongest candidate new machine contract.
4. Assurance/provenance additions as extensions to current Assurance/Review/Event/Dispatch contracts.
5. Handoff/recovery through current Dispatch + Local Agent Handoff unless a concrete missing field is evidenced.

No duplicate Task/Review/Validation/Release state model is allowed.

## 13. Compatibility posture

Target: additive/non-weakening v4 minor release.

Existing Agent/event/dispatch/Review/Validation semantics remain authoritative and are referenced/converged, not replaced.

Any proposal requiring incompatible dispatch/event wire changes, core authority-chain changes, destructive role renames or historical evidence reinterpretation is routed to v4.7/future-major migration planning.

## 14. Non-goals

v4.6 does not:

- prescribe prompt-writing tricks or private chain-of-thought techniques;
- mandate an LLM vendor/model or permanent model ranking;
- create another autonomy scale;
- create a second Review/Assurance/Validation/Release state machine;
- create a second handoff/dispatch lifecycle;
- require multiple Agents or human review for every Task;
- require model/provider telemetry for trivial mechanical work;
- replace domain-specific Harnesses or project Product/Architecture authority;
- implement the v4.7 repository-wide resolver/convergence refactor.

## 15. Product acceptance

v4.6.0 is complete when:

1. Intent/Assumption, Context Engineering and Skill Governance each have clear normative ownership;
2. required truth cannot depend on hidden chat/session context;
3. context authority/currentness/progressive-disclosure rules are deterministic enough for independent Agents;
4. interpretation/assumption/UNKNOWN cannot silently become Frozen Product facts;
5. Skills/procedures have durable authority/security/provenance boundaries;
6. F0–F3 remains the single autonomy vocabulary and cross-lifecycle escalation is coherent;
7. AI change assurance extends existing Assurance/Review rather than creating another result system;
8. Agent/model provenance is proportional and supports required independence claims;
9. fresh Agent recovery works from durable GitHub/repository facts;
10. Fast Path remains low ceremony without allowing gate bypass;
11. at least one dogfood scenario demonstrates session/model/operator handoff without loss of authority truth.

## 16. Product Freeze basis and next gate

Product Freeze is authorized by Fresh Independent owner-overlap/currentness Review **#280**, which verified the current v4.1–v4.5 Product/L2 owner map, canonical v4.3–v4.5 planning merges, non-duplication of assurance/autonomy/handoff/lifecycle states, and eligibility to Freeze without waiting for full upstream implementation completion.

Frozen Product evidence:

- `docs/implementation/4.6.0/AI_NATIVE_AUTHORITY_INVENTORY.md` — historical/non-normative inventory; its earlier fourth candidate is superseded by L1/Product Freeze;
- `docs/implementation/4.6.0/L1_PRODUCT_EVIDENCE.md`;
- `docs/implementation/4.6.0/UPSTREAM_OWNER_CURRENTNESS.md`;
- #280 exact-subject PASS on planning HEAD `9b168097cadeb36784f937f645d087a4e7da5d17` against `main@bc3feeccf130fcfc7b49efaf44983e4dcdac6e5d`.

Frozen decisions:

1. exactly three new normative owner domains are introduced (§2);
2. autonomy/Assurance/Review/Dispatch/Handoff/Validation/Release/Fast Path and v4.1–v4.5 semantic owners remain existing authorities;
3. no required truth may exist only in ephemeral Agent/session/chat context;
4. Skill/procedure authority remains subordinate to Product/Architecture/Task/side-effect authority;
5. no provider/model mandate or private chain-of-thought evidence requirement is introduced;
6. v4.6 remains additive/non-weakening and may not create a parallel lifecycle state machine.

Next gate: **L2 Architecture Evidence**. L2 must select the minimum new machine-contract set and reuse/extension points without reopening these Product decisions.

`LOCAL_ENV=NOT_REQUIRED` for Product Freeze/L2. Session-loss/handoff dogfood or real multi-Agent capability experiments require an explicit exact-scope handoff only at their later executable gate.
