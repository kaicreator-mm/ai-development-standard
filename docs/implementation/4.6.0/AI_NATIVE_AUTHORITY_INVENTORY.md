# v4.6 Existing AI-native Authority Inventory

Status: **RESEARCH INVENTORY — non-normative input to v4.6 L1**

Inventory baseline: `main@e9eb39235e45e9ad90407b803ab1c8679d348dbf`

Purpose: determine what v4.6 genuinely needs to own versus what already has a normative owner. The inventory intentionally avoids creating new authority.

## 1. Existing durable owners

| Concern | Existing owner(s) | Existing semantics to preserve | v4.6 posture |
|---|---|---|---|
| Product/Architecture authority precedence | `DEVELOPMENT_WORKFLOW.md`, `EXECUTION_PACK_STANDARD.md` | Frozen Product > Frozen Architecture > Task DAG > Task Pack > Execution Contract > implementation choice | reference/converge; do not replace |
| Task Pack / Execution Pack / exact-base execution authority | `EXECUTION_PACK_STANDARD.md` | Task Pack = WHAT; Execution Pack = JIT HOW on exact base; Dispatch = WHO/WHERE/identity | reuse |
| bounded Agent autonomy | `EXECUTION_PACK_STANDARD.md`, `MODEL_USAGE_POLICY.md` | F0_MECHANICAL / F1_BOUNDED_IMPLEMENTATION / F2_ENGINEERING_DISCRETION / F3_ARCHITECTURE_REQUIRED; executor cannot self-promote | cross-lifecycle clarification only |
| model strength routing | `MODEL_USAGE_POLICY.md` | task risk/evidence drives strong vs lower-cost routing; strong model for product/architecture/high-risk judgment | reuse; provider-neutralize terminology where needed |
| local/real-host handoff | `LOCAL_AGENT_HANDOFF_PROTOCOL.md` | Issue/repository facts are durable contract; chat is pointer-only transport; exact identity/currentness; Builder/Validator role separation | reuse; generalize recovery invariant |
| pointer-only task trigger | `ISSUE_FIRST_TASK_TRIGGER.md`, `LOCAL_AGENT_HANDOFF_PROTOCOL.md` | no durable contract -> no trigger; user-visible trigger does not duplicate contract | reuse |
| dispatch lifecycle / durable Agent events | `EXECUTION_ARCHITECTURE_STANDARD.md`, `GITHUB_AGENT_INTERACTION_PROTOCOL.md` | canonical dispatch/event/reducer architecture and operator attribution | reuse; no parallel agent state machine |
| Web/Local roles | `CHATGPT_WEB_ROLE.md`, `CODEX_ROLE.md`, `LOCAL_AGENT_HANDOFF_PROTOCOL.md` | role-specific authority/capability boundaries | preserve; avoid vendor permanence |
| handoff/context-loss recovery | `LOCAL_AGENT_HANDOFF_PROTOCOL.md` §12 | replacement worker reconstructs from GitHub facts; crashed worker never recovered from chat history | elevate to general AI-native invariant |
| exact-SHA Review/Validation independence | Review/Validation standards + web-review bootstrap | role separation, immutable subject, no self-repair under Validator/Reviewer | reuse and connect to AI provenance |
| CI/runner capability/fallback | CI standards + GitHub capability fallback | unavailable capability -> alternate executor/BLOCKED, never fake PASS | reuse |
| Hidden Validation / scenario evidence | Test Data / Validation / release architecture | hidden fixture separation, scenario truth, escaped-defect feedback | reuse |
| GitHub durable work-item truth | `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, interaction protocol | Issue/PR structured facts over chat summaries | reuse |
| project adoption/bootstrap | `PROJECT_ADOPTION.md`, `AGENTS.md` conventions, repository bootstrap | pinned standard/project overrides/bootstrap provide project-specific authority | converge context precedence, not replace |

## 2. Existing autonomy contract is already strong

`EXECUTION_PACK_STANDARD.md` freezes machine-readable freedom:

```text
F0_MECHANICAL
F1_BOUNDED_IMPLEMENTATION
F2_ENGINEERING_DISCRETION
F3_ARCHITECTURE_REQUIRED
```

and states the lower-cost executor cannot silently resolve Task Pack/Architecture contradictions.

**Inventory conclusion:** v4.6 does not need a new autonomy-level model. It should make applicability/escalation consistent across Product/Architecture/Planning/Implementation/Review/Validation/Release/Operations while preserving F0–F3 as the execution freedom vocabulary.

## 3. Existing handoff/recovery contract is already strong

`LOCAL_AGENT_HANDOFF_PROTOCOL.md` already freezes:

```text
GitHub Issue + repository facts + pinned standard = durable contract
chat = invocation transport
No durable contract -> no trigger
replacement worker reconstructs from GitHub facts alone
crashed worker is never recovered from chat history
```

**Inventory conclusion:** v4.6 should generalize this into a lifecycle-wide invariant:

> No required development truth may exist only in an ephemeral agent/session context.

It should not create a second handoff protocol.

## 4. Existing model policy is risk-based but role/provider language can be converged

`MODEL_USAGE_POLICY.md` routes Strong models to Product/Architecture/high-risk judgment and lower-cost/local executors to bounded work with Tests/Contract/Reference Packs. This is already aligned with AI-native multi-agent execution.

Gaps:

- vocabulary is partly tied to current role/product names (`ChatGPT Web`, `Codex`);
- provenance/independence/model-diversity facts are not centrally described across lifecycle claims;
- there is no general context-authority/currentness standard outside execution-specific documents.

v4.6 should converge semantics without invalidating existing role files.

## 5. Durable instructions / skills / invocation separation — external practice

Current external Agent ecosystems reinforce a useful separation:

- repository/custom instructions for broadly applicable rules;
- Agent Skills for detailed reusable task-specific procedures loaded when relevant;
- user invocation for selecting/triggering a task;
- tools/resources for actions/context rather than embedding everything into prompts.

Sources:

- GitHub Agent Skills: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- AGENTS.md: https://agents.md/
- MCP server primitives: https://modelcontextprotocol.io/specification/draft/server/index

This maps naturally onto existing ADS:

```text
Stable rule/authority       -> standard / AGENTS / project authority
Reusable procedure          -> Skill
Project/domain fact         -> project docs/contracts
Task authority              -> Task Pack / Execution Pack / Issue
Invocation                  -> pointer-only trigger / Dispatch
Ephemeral discussion        -> chat/session
```

## 6. Context authority gap

Existing standards establish pieces of precedence/currentness, but there is no single AI-native normative owner that tells an unfamiliar Agent how to select/reconstruct effective context across:

```text
system/org constraints
pinned ADS revision
repository AGENTS / project overrides
Frozen Product / Architecture
Task DAG / Task Pack
Execution Pack / Dispatch
Issue / PR live facts
source / tests / evidence
external tool/resource data
historical chat / memory
```

Proposed gap owner: **Context Engineering Standard**.

Key invariant:

```text
current higher-authority durable facts > stale lower-authority/history
```

Historical chat/memory may assist discovery but cannot override current Git/GitHub/frozen authority.

## 7. Intent → Spec gap

Product workflow already freezes PRD through evidence, but natural-language Agent inference is not centrally classified before it becomes durable authority.

Proposed v4.6 gap owner: **Intent & Assumption Governance** with durable distinctions:

```text
USER_INTENT
INTERPRETATION
ASSUMPTION
UNKNOWN
DECISION_REQUIRED
DURABLE_REQUIREMENT
```

This owner must compose with existing Product/L1/PRD Freeze rather than replace them.

## 8. Skill / reusable procedure governance gap

Existing ADS has prompts/bootstrap/templates but no general normative contract for reusable Agent Skills/procedures.

A reusable material Skill should be able to state:

```text
identity/version
purpose/scope
trigger/applicability
required inputs
allowed tools/side effects
outputs
failure/escalation behavior
validation/evaluation refs
compatibility/maintenance owner
```

Skill instructions remain subordinate to Product/Architecture/Task/Validation authority.

Important external security evidence: GitHub warns that third-party skills may contain hidden/malicious instructions or scripts and recommends preview/inspection before installation.

**Finding:** v4.6 should treat imported Skills as executable/untrusted procedure content subject to source/provenance/review policy, not trusted merely because installed.

## 9. Handoff semantics — external practice

Modern Agent SDKs expose explicit handoff objects, optional structured handoff metadata and context/history filtering. This shows handoff identity/context selection are distinct architectural concerns.

Source: https://openai.github.io/openai-agents-python/handoffs/

ADS should remain framework-neutral but can standardize durable facts needed to recover/delegate safely:

```text
source role/operator
destination role/capability
reason/scope
subject identity
current authority refs
completed evidence
remaining work
allowed side effects
next action / blocker
```

Existing GitHub Issue/Dispatch objects should carry/reference these facts; do not create a chat transcript as the handoff object.

## 10. MCP primitive separation — external practice

MCP distinguishes:

```text
prompts   -> user-controlled reusable interaction templates
resources -> application-controlled context/data
tools     -> model-controlled callable actions
```

This reinforces a v4.6 Product rule: instructions/context/actions must not be collapsed into one opaque prompt blob. Tool capability does not equal side-effect authority; resource availability does not make it Product truth; a prompt does not override project authority.

## 11. Candidate v4.6 owners after inventory

The inventory supports a narrowed v4.6 Product shape:

### New/explicit cross-lifecycle owners
1. **Intent & Assumption Governance**
2. **Context Engineering Standard**
3. **Skill / Reusable Agent Procedure Governance**
4. **AI Change Assurance & Provenance Standard** (may be one owner or split in L2 if evidence shows distinct lifecycle authority)

### Convergence/clarification, not new owners
- F0–F3 autonomy/escalation: keep Execution Pack/Model Usage ownership, add cross-lifecycle mapping/reference.
- Handoff/recovery: keep existing Local Agent/GitHub/Dispatch ownership, generalize no-chat-only truth and cross-role recovery semantics.
- Fast Path: refine eligibility/reference existing lifecycle owners; do not create a separate lightweight lifecycle.
- Review/Validation/Release state: preserve existing owners.

## 12. Future-major / v4.7 candidates discovered

Do not solve these in v4.6 by incompatible rewrite:

- replacing current dispatch/event wire protocol;
- renaming/removing current execution profiles in a breaking way;
- collapsing all Agent roles into one universal runtime object;
- moving every prompt/template/role file into a new incompatible hierarchy;
- changing the core authority chain.

These are convergence/migration inputs for v4.7 or future v5 if compatibility cannot be preserved.
