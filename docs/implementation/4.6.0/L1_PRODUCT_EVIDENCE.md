# v4.6.0 L1 Product Evidence — AI-native / Agentic Development Governance

Status: **COMPLETE RESEARCH — supports substantial PRD narrowing; Product Freeze waits for stable v4.1–v4.5 semantic-owner boundaries**

Research date: 2026-09-30

Baseline reviewed:

- `main@e9eb39235e45e9ad90407b803ab1c8679d348dbf`
- Draft `docs/implementation/4.6.0/PRD.md`
- `docs/implementation/4.6.0/AI_NATIVE_AUTHORITY_INVENTORY.md`
- current `AGENTS.md`
- `EXECUTION_PACK_STANDARD.md`
- `MODEL_USAGE_POLICY.md`
- `LOCAL_AGENT_HANDOFF_PROTOCOL.md`
- `EXECUTION_ARCHITECTURE_STANDARD.md`
- `GITHUB_AGENT_INTERACTION_PROTOCOL.md`
- `ISSUE_FIRST_TASK_TRIGGER.md`
- `schemas/assurance-plan-v1.schema.json`
- `schemas/review-aggregation-v1.schema.json`
- v4.1–v4.5 Product/planning boundaries available at research time

This is Product evidence, not Product Freeze.

## 1. Recommendation

**PROCEED WITH MAJOR NARROWING.**

The AI-native Product problem is strongly evidenced, but the Draft PRD currently mixes genuinely missing governance with concerns already owned by v4 standards.

L1 supports three genuinely new cross-lifecycle normative owners:

1. **Intent & Assumption Governance**
2. **Context Engineering Standard**
3. **Skill / Reusable Agent Procedure Governance**

L1 does **not** support creating new competing owners for:

- Agent autonomy levels — F0–F3 are already owned by `EXECUTION_PACK_STANDARD.md` / `MODEL_USAGE_POLICY.md`;
- Dispatch/Handoff lifecycle — already owned by Execution Architecture / GitHub interaction / Local Agent handoff;
- Independent Review / model-diverse assurance — already represented by current Assurance/Review contracts;
- Validation/Release state — existing owners remain authoritative;
- Fast Path as a separate lifecycle — Fast Path remains a risk/materiality policy across existing owners.

v4.6 should therefore be a **vertical governance/convergence release with only three new owner domains and additive extensions/references to existing assurance/provenance/handoff mechanisms**.

## 2. Existing ADS evidence: AI-native execution is already substantial

### 2.1 Durable authority hierarchy already exists

`EXECUTION_PACK_STANDARD.md` already freezes:

```text
Frozen Product Authority
> Frozen Architecture Authority
> Task DAG
> Task Pack
> Execution Contract
> Semantic / Interface Seed
> Agent implementation choice
```

It also separates:

```text
Task Pack      = durable WHAT
Execution Pack = exact-base JIT HOW
Dispatch       = WHO / WHERE / WHICH IDENTITY
```

**Finding:** v4.6 MUST NOT create a parallel “AI context/task authority” hierarchy.

### 2.2 Bounded autonomy already exists

The current machine-readable freedom vocabulary is:

```text
F0_MECHANICAL
F1_BOUNDED_IMPLEMENTATION
F2_ENGINEERING_DISCRETION
F3_ARCHITECTURE_REQUIRED
```

and lower-cost executors cannot self-promote or silently resolve Frozen/Task Pack contradictions.

**Finding:** retain F0–F3. v4.6 may clarify how Product/Architecture/Review/Operations roles escalate, but must not introduce another autonomy scale.

### 2.3 Handoff/context-loss recovery already exists

`LOCAL_AGENT_HANDOFF_PROTOCOL.md` freezes:

```text
GitHub Issue + repository facts + pinned standard = durable contract
chat = invocation transport
No durable contract -> no trigger
replacement worker reconstructs from GitHub facts
crashed worker is never recovered from chat history
```

**Finding:** v4.6 should generalize the lifecycle invariant:

> **No required development truth may exist only in ephemeral Agent/session/chat context.**

It should not replace the current handoff protocol.

## 3. External evidence: Instructions, Skills, Context and Tools are distinct layers

### 3.1 Durable repository instructions

AGENTS.md provides repository/directory-scoped persistent Agent instructions, with more-specific nested instructions taking precedence for their subtree.

Source: https://agents.md/

GitHub Copilot similarly supports repository and path-specific custom instructions.

Source: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions

**Finding:** durable broadly applicable rules belong in repository/project authority, not copied into every task prompt.

### 3.2 Reusable Agent Skills are distinct from broad instructions

GitHub Agent Skills package detailed reusable instructions plus optional scripts/resources and load them when relevant; GitHub also warns that third-party skills may contain hidden/malicious instructions or scripts and should be inspected before installation/use.

Source: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills

**Finding:** v4.6 needs a reusable Skill/procedure governance contract with identity, source/provenance, applicability, inputs, tools/side effects, outputs, failure/escalation and evaluation — subordinate to Product/Architecture/Task authority.

### 3.3 MCP separates prompts, resources and tools

MCP's server primitives distinguish:

```text
prompts   -> user-controlled templates
resources -> application-controlled context/data
tools     -> model-controlled callable actions
```

Source: https://modelcontextprotocol.io/specification/draft/server/index

**Finding:** AI-native governance should not collapse instructions, contextual data and action capability into one opaque prompt. Tool availability/capability is not side-effect authority; resource availability is not Product truth.

## 4. New Owner 1 — Intent & Assumption Governance

Natural-language work often begins before durable Product/Task authority exists. The missing governance is not “how to write a prompt”; it is how Agent interpretation is prevented from silently becoming project truth.

Required durable distinctions:

```text
USER_INTENT          what the human/source actually requested
INTERPRETATION       Agent's parsed meaning
ASSUMPTION           unverified completion/inference
UNKNOWN              unresolved material fact
DECISION_REQUIRED    higher authority must decide
DURABLE_REQUIREMENT  promoted into the applicable Product/Task authority
```

Required rules:

- chat/user intent is not automatically Frozen Product Authority;
- interpretation must remain distinguishable from user-stated fact when material;
- high-impact UNKNOWN/ASSUMPTION cannot silently become public contract, security rule, data semantic or architecture decision;
- low-risk details may be completed under granted autonomy;
- promotion into durable requirement occurs through the existing Product/Architecture/Task authority path;
- contradictory intent/evidence routes to decision, not guessed reconciliation.

This owner feeds L1/PRD/Task Pack processes; it does not replace them.

## 5. New Owner 2 — Context Engineering Standard

Current ADS distributes context/currentness rules across AGENTS, GitHub interaction, Execution Pack, handoff and Validation. A fresh Agent still lacks one explicit cross-lifecycle context-selection contract.

Context sources may include:

```text
system / organization constraints
pinned ADS revision
repository AGENTS / project overrides
Frozen Product / Architecture
Task DAG / Task Pack
Execution Pack / Dispatch
Issue / PR live state
source / tests / evidence
approved external resources/tools
historical chat / memory
```

Required invariants:

- higher-authority current durable facts override lower-authority historical context;
- stale chat/memory MUST NOT override current Git/GitHub/frozen authority;
- exact-currentness-sensitive action re-reads live subject identity before acting;
- required truth MUST NOT exist only in chat/history;
- context selection uses progressive disclosure and materiality rather than dumping the entire repository into every invocation;
- external resource/tool output is evidence/data until promoted through the applicable authority path;
- context provenance/freshness is captured when material to a result claim.

This owner describes effective context selection, not another project state model.

## 6. New Owner 3 — Skill / Reusable Agent Procedure Governance

A material reusable Skill/procedure should be durably identifiable and inspectable.

Recommended Product fields:

```text
skill/procedure identity + version
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

- Skill instructions are subordinate to Product/Architecture/Task/Validation/Release authority;
- installing/possessing a Skill does not authorize its side effects;
- external/third-party Skills are untrusted procedure content until accepted through project policy;
- a Skill may package scripts/resources but secret values and hidden project authority must not be embedded casually;
- task-specific one-off authority belongs in Task/Execution Pack, not promoted into a Skill merely for reuse convenience;
- invocation remains pointer/dispatch-like; it does not duplicate the full Skill/Task contract.

## 7. Assurance & Provenance — extend existing owners, do not duplicate

The Draft PRD proposed an AI-generated Change Assurance owner. Current machine contracts already cover most of this domain.

`assurance-plan-v1.schema.json` already represents:

```text
review
validation
hidden validation
coherence review
authority review
independence requirements
model-diverse-adversarial mode
finding/blocker aggregation policy
exact subject identity binding
```

`review-aggregation-v1.schema.json` already carries reviewer provenance including provider/model family/model/executor/context and blind-first-pass references where applicable.

**L1 correction:** v4.6 should not create a second Assurance state/object family. Instead it should add AI-native review dimensions/guidance and provenance semantics to the existing Assurance/Review architecture where gaps remain.

AI-generated change review dimensions may include, when material:

```text
intent alignment
unsupported assumptions
invented API/domain rules
architecture alignment
silent dependency/toolchain invention
security shortcuts
silent test weakening
scope/write-set compliance
unnecessary complexity
```

These are coverage dimensions, not a new Review result state.

Provenance should remain proportional. Do not require full model parameter/token/chain-of-thought logging for ordinary tasks.

## 8. Handoff / Recovery — generalize, do not replace

Modern Agent SDKs expose explicit handoff identity/context filtering, supporting the architectural distinction between the handoff subject, destination role and selected context.

Reference: https://openai.github.io/openai-agents-python/handoffs/

ADS should keep existing GitHub/Dispatch/Local Agent ownership and ensure a successor Agent can reconstruct:

```text
what was requested
what is frozen/current
exact subject/source identity
what changed
what passed/failed/blocked
what remains
who/what owns next action
which assumptions are forbidden
```

No full chat transcript is required or desirable as project authority.

## 9. Model / operator provenance boundary

Current `MODEL_USAGE_POLICY.md` correctly routes capability by risk rather than task title. v4.6 should preserve provider neutrality and distinguish:

```text
actor role
logical operator/executor/session
transport account
model/provider/family when material to independence/provenance
```

Model/provider identity is required only when it materially supports a claim such as model-diverse independent review or reproducibility/audit. It is not universal project telemetry.

## 10. Fast Path — refine eligibility, never create a second lifecycle

Core rule:

> **Reduce ceremony, not truth.**

Fast Path may omit non-material L1/L2/Task DAG/Execution Pack/Independent Review/Hidden Validation steps under existing risk/authority rules, but retains applicable:

```text
scope/authority
Git identity/safety
focused tests/checks
truthful Validation/evidence
integration result
```

An Agent cannot self-label complex/high-risk work “small” to bypass Frozen or required gates.

## 11. Product-level forbidden inferences

v4.6 conformance should reject at least:

```text
user chat statement -> Frozen Product requirement automatically
Agent interpretation -> user intent fact
ASSUMPTION/UNKNOWN -> durable requirement without authority
historical chat/memory -> override current Git/GitHub authority
large context dump -> higher context quality by definition
resource/tool available -> Product truth / side-effect authority
Skill installed -> Skill trusted / side effects authorized
Skill instruction -> override Frozen Product/Architecture/Task
model capable -> granted F3 authority
same GitHub account -> same logical operator/context
AI-generated code compiled -> intent/domain correctness
AI-authored change -> mandatory human review in all cases
reviewer model/provider recorded -> independence automatically proven
Fast Path label -> required gates waived
```

## 12. Machine-readable expectations

L2 should prefer extending existing objects before adding new schemas.

Candidates:

1. **Intent/Assumption disposition** — may be a lightweight record/event if durable cross-Agent promotion/status needs machine exchange.
2. **Context Manifest / Effective Context References** — only if deterministic authority/currentness cannot be resolved from existing pointers; avoid full content snapshots.
3. **Skill Metadata** — likely useful for reusable procedure identity/version/applicability/tools/evaluation.
4. **Assurance/Provenance extensions** — extend `assurance-plan`, review/event/dispatch records where needed rather than new parallel result objects.
5. **Handoff/recovery** — reuse current Dispatch/Local Agent Handoff schema and GitHub facts unless a missing field is proven.

## 13. Counter-evidence / scope risks

- Modern models improve quickly; model rankings/vendor-specific instructions would age badly.
- Excessive context manifests/Skill metadata can create bureaucracy for trivial work.
- Existing ADS already has a strong Agent execution architecture; broad rewrites would create duplicate authority rather than solve a gap.
- Some repositories do not use reusable Skills at all; Skill governance should be NOT_APPLICABLE when no material reusable procedure exists.
- Model/provider provenance can become privacy/cost-heavy if required indiscriminately.

## 14. L1 verdict

**Evidence supports v4.6 only after major narrowing.**

Recommended Product shape:

```text
NEW OWNERS
- Intent & Assumption Governance
- Context Engineering Standard
- Skill / Reusable Agent Procedure Governance

EXTEND / CONVERGE EXISTING OWNERS
- F0–F3 Autonomy / escalation
- Assurance / Review coverage + provenance
- Dispatch / Handoff / recovery
- Model routing
- Fast Path
```

Product Freeze should wait until v4.1–v4.5 semantic owner boundaries are stable enough to guarantee that the vertical layer references rather than steals their authority. Full implementation completion is not required before Freeze; stable Product/L2 owner boundaries are sufficient.

`LOCAL_ENV=NOT_REQUIRED` at L1. A later session-loss/handoff dogfood may require real independent/local Agent execution and must use an explicit exact-scope handoff Issue.