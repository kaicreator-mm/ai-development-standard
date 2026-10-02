# ai-development-standard v4.9.0 PRD — Adaptive Proportional Development Orchestration

Status: **FIRST REVIEW CANDIDATE — NOT FROZEN; ADVERSARIAL PRODUCT REVIEW REQUIRED**

Planning baseline: `main@9383244abb8172b5ae5135cbd559c72837799375`

Planning parent: `#697`

Primary planning/dogfood input: `#680`

L1 evidence: `docs/implementation/4.9.0/L1_PRODUCT_EVIDENCE.md`

This PRD is a Product candidate only. It does not authorize L2, Task DAG materialization, implementation, schema migration, scheduler deployment, or any waiver of existing Frozen Product/L2/Review/Validation/Release authority.

## 1. Product intent

v4.9.0 makes ADS execution proportional, adaptive and role-consistent without weakening fail-closed truth.

The Product goal is:

> Given live durable project facts, ADS can determine the **minimal sufficient legal workflow**, identify the roles actually required, select an eligible Agent/environment for each role, standardize how that role claims/executes/hands off/terminates work, reuse prior evidence only when equivalence is defensible, and convert repeated execution friction into governed improvement candidates — while deterministic authority constraints prevent optimistic downgrade, stale-evidence reuse and independence collapse.

v4.9 builds on existing ADS Product/Architecture/Task/Execution/Dispatch-Claim/Validation/Review/Release semantics. It does not replace them with a new universal Agent runtime.

## 2. Product problems

### 2.1 Assurance depth is not sufficiently proportional to material risk

Real v4.x dogfood has shown small/medium changes expanding into long chains of Builder, Validation, Fresh Review, merge, Stage1, Freeze, Hidden, Closeout, Release Qualification, Repository Integration and successor rebind.

Those gates are valuable when they discover or protect against material risk. They are waste when applied mechanically to concerns whose risk/authority/release significance does not justify the same depth.

ADS needs a standard distinction between:

```text
concern-level assurance
vs
version/release-level assurance
```

and must make gate omission/reuse/not-applicable decisions explicit rather than silent.

### 2.2 Runtime orchestration decisions cannot all be frozen at planning time

Whether work is actually ready, whether target movement is materially relevant, whether evidence is reusable, which Agent/environment is available, whether a repair is bounded, and whether a recurring defect is systemic are live-state decisions.

A fully pre-expanded execution graph creates avoidable Issues, stale work, guaranteed-BLOCKED dispatches and repeated rebind/review cycles.

### 2.3 Agent role behavior is not yet expressed as one standard operating model

ADS already has Builder/Reviewer/Validator/Controller/Release roles and Dispatch/Claim ownership, but their common execution contract is spread across multiple standards.

The system needs one provider-neutral model for:

```text
Role
→ Eligibility
→ Dispatch
→ Claim
→ Start
→ Execution
→ Evidence/Handoff
→ Terminal
→ Ownership Release
```

with role-specific authority deltas.

### 2.4 Independence is too easily conflated with Issue count

Current dogfood demonstrates that distinct independent phases can share one durable Issue while preserving different actor/session claims and terminal verdicts.

ADS needs to define independence as an authority/actor/session property rather than requiring a new GitHub object for every gate.

### 2.5 Exact-subject truth lacks a bounded equivalence/reuse path

A changed candidate or material composition change must invalidate affected evidence. But unrelated branch movement or topology-only target movement may produce no new semantic decision value.

ADS needs an explicit path to prove evidence remains applicable without treating every base movement as either automatically safe or automatically invalidating.

### 2.6 Repeated failures can cause more ceremony instead of earlier prevention

When the same failure family recurs, repeatedly adding repair/Validation/Review cycles treats symptoms instead of improving the earliest reliable detection point.

ADS needs a lightweight recurrence/root-cause escalation loop that can propose checker/template/schema/orchestrator-policy improvements through normal governance.

## 3. Product shape

v4.9 freezes, if Product Review authorizes it, four integrated Product pillars:

1. **Proportional Assurance**
2. **Adaptive Orchestration**
3. **Agent Operating Model**
4. **Execution Learning & Recurrence Escalation**

Cross-cutting invariants:

5. **Deterministic Guardrails / Fail-Closed Authority**
6. **Evidence Currentness / Equivalence**
7. **Provider- and Transport-Neutral Role Semantics**

## 4. Pillar P1 — Proportional Assurance

### 4.1 Product requirement

ADS MUST derive the minimum required assurance depth from materiality, authority impact, current evidence and release significance rather than defaulting every concern to the maximum workflow.

A Product/L2 implementation may use risk/materiality classes or profiles. Candidate research defaults include:

```text
A — semantic-neutral maintenance
B — bounded normative semantic change
C — machine contract / lifecycle / authority / gate change
D — release-significant compatibility / migration change
```

These labels are not themselves sufficient authority. File count, model name, “docs-only” labeling or self-declared low risk MUST NOT automatically down-classify a material semantic/authority change.

### 4.2 Required assurance outputs

Before authoritative dispatch/merge/release transitions, the system must be able to resolve, as applicable:

```text
materiality / risk basis
required role set
required Validation scope
Review Policy
independence requirements
release-significant applicability
required Closure/Freeze/Hidden/RQ applicability
evidence reuse/currentness disposition
explicit NOT_APPLICABLE / NOT_RUN / BLOCKED states
```

### 4.3 Concern assurance vs release assurance

A normal Task/PR may require focused Validation and/or Review without automatically becoming a version release candidate.

Full Version Closure / Candidate Freeze / Hidden / Fresh Closeout / Release Qualification SHOULD default only when current Product/Release authority makes the change/version release-significant or when newly surfaced risk requires escalation.

### 4.4 Fast Path strengthening

Fast Path must be a real proportional execution profile, not merely a smaller branch structure around the same full set of gates.

It must still preserve:

- current authority discovery;
- required Review Policy resolution;
- required Validation truth;
- accepted Claim/start ownership when authoritative Agent execution occurs;
- exact-subject evidence where applicable;
- explicit escalation when risk grows.

## 5. Pillar P2 — Adaptive Orchestration

### 5.1 Product requirement

ADS SHOULD support a high-capability orchestration control plane that reads live durable facts and selects the next legal work JIT rather than requiring the entire execution script to be materialized in advance.

Candidate responsibility includes:

```text
read live Task DAG / Issues / PRs / refs / Claims / terminals / evidence
compute actually-ready work
classify materiality/risk/authority impact
resolve required assurance/roles
choose eligible Agent/model/environment
control concurrency/JIT admission
avoid duplicate or knowingly blocked dispatch
consume terminals
choose bounded repair vs escalation
resolve evidence reuse vs successor validation/review
record lightweight execution decision/learning evidence
```

### 5.2 Deterministic guardrail principle

The high-capability model is a reasoning/control-plane resource, not a supreme authority.

The architecture MUST preserve a separation equivalent to:

```text
High-capability reasoning
  → ambiguous decomposition/materiality/recovery/trade-offs

Deterministic policy/contract checks
  → mandatory gates, illegal transitions, authority constraints,
    independence constraints, exact-subject/currentness invariants

Durable fact plane
  → GitHub/repository/evidence/current operation facts
```

### 5.3 Orchestrator hard boundaries

The Orchestrator MUST NOT:

- mint a required independent Review/Validation/Hidden/RQ PASS;
- silently waive Frozen Product/L2/Task/Release requirements;
- treat private chat memory as canonical current project state;
- hide uncertainty by inventing completion;
- bypass Dispatch/Claim admission;
- make cost/latency/availability override hard eligibility;
- mutate the standard automatically from local learning.

### 5.4 Task DAG reinterpretation

v4.9 SHOULD research/authorize the Task DAG primarily as:

```text
allowed work
+ dependency constraints
+ ownership boundaries
+ required evidence/assurance constraints
```

rather than a requirement to pre-materialize every Builder/Validator/Reviewer/Controller execution object.

JIT execution objects/phases may be materialized when live facts prove they are required.

### 5.5 Wait states

When work is deterministically not ready, orchestration SHOULD preserve a durable non-dispatch wait state such as `WAITING_LINEAGE`/equivalent rather than create a guaranteed-BLOCKED Agent task solely for bookkeeping.

## 6. Pillar P3 — Agent Operating Model

### 6.1 Product requirement

ADS MUST define one common provider-neutral **Agent Execution Base Contract** and role-specific **Role Profiles**.

The normative abstraction is the role, not the model/vendor/application.

A concrete ChatGPT/Claude/Codex/local/runtime Agent is an executor of a role subject to eligibility, capability, environment and independence rules.

### 6.2 Base lifecycle

Authoritative Agent work must be representable as:

```text
ELIGIBILITY
→ DISPATCH
→ CLAIM
→ START
→ EXECUTION
→ EVIDENCE / HANDOFF
→ TERMINAL
→ OWNERSHIP RELEASE
```

Existing Dispatch/Claim authority remains canonical. v4.9 MUST NOT create a second task lock/lease authority.

### 6.3 Common pre-Claim requirements

Before an Agent begins authoritative execution, the execution contract must be able to establish, as applicable:

```text
work item/operation remains READY/current
dependencies satisfied
role matches dispatch
required capability/environment available
independence constraints satisfied
no incompatible accepted active Claim
current Product/L2/Task/Execution authority refs read
exact subject/base/target resolved
allowed scope/write set resolved
forbidden scope/actions resolved
required evidence/terminal authority resolved
```

Only accepted Claim/start facts authorize authoritative execution where Claim is required by existing ADS semantics.

### 6.4 Common execution requirements

During execution, an Agent must:

- remain within owned concern and allowed authority;
- re-check live facts when a material assumption may have changed;
- not silently widen Frozen Product/L2/Task scope;
- surface material deviation/blocker/authority insufficiency;
- preserve exact-subject/currentness semantics;
- avoid exposing private chain-of-thought;
- record only material structured learning required by current policy.

### 6.5 Common terminal requirements

A terminal result must be durably attributable to the role/work/dispatch/claim/exact subject and expose enough structured evidence for the next controller/role to act without guessing.

Candidate semantic dimensions:

```text
role
work item / dispatch / claim
operator/session provenance
exact subject/base/target where applicable
terminal state / verdict
outputs/artifacts/PR/commit refs
checks/tests/evidence refs
deviations/limitations/remaining risk
handoff/next required role or gate
ownership release
```

Exact event/schema shape is L2.

### 6.6 Role Profile model

Each standardized role profile SHOULD define only:

```text
Eligibility
Required Inputs
Allowed Actions
Forbidden Actions
Required Evidence
Terminal Authority
```

Projects/domains may add stricter specialized roles/profiles without weakening higher ADS authority.

## 7. Standard Role Profile — Builder

### 7.1 Responsibility

Produce the authorized mutable implementation/work product for the owned concern.

### 7.2 Required Product behavior

Builder MUST NOT begin authoritative mutation before required accepted Claim/start.

Builder MUST:

- consume Frozen/current authority and exact execution subject;
- respect owned concern/write set and sibling boundaries;
- implement required source/tests/fixtures/docs/checks within scope;
- validate its own bounded implementation assumptions where possible;
- record material deviations, blockers and newly discovered authority gaps;
- stop/escalate when Product/L2/Task authority is insufficient;
- produce a structured implementation terminal with exact output identity and downstream gate requirements.

Builder MUST NOT self-approve a Review/Validation/Release verdict that current authority requires to be independent.

## 8. Standard Role Profile — Reviewer

### 8.1 Responsibility

Produce an independent evaluative verdict on the exact review subject against current authority and evidence requirements.

### 8.2 Required Product behavior

Reviewer SHOULD be read-only by default.

Where Review is required, Reviewer MUST:

- bind to exact subject/current authority;
- independently inspect actual diff/artifacts/evidence;
- verify scope/currentness/authority/negative or forbidden behavior as applicable;
- produce severity findings and terminal verdict;
- preserve required actor/session independence.

Reviewer MUST NOT silently repair the candidate and then approve its own mutation. Repair requires a separately authorized mutable role/phase followed by successor review as applicable.

## 9. Standard Role Profile — Validator

### 9.1 Responsibility

Execute required tests/build/runtime/host/environment/scenario oracles against the exact validation subject and report observed truth.

### 9.2 Required Product behavior

Validator MUST distinguish executed evidence from inferred/not-run evidence and report `PASS | FAIL | BLOCKED | NOT_RUN | NOT_APPLICABLE` or the current authoritative equivalent without fabrication.

Where independent Validation is required, its actor/session must satisfy the declared independence requirement.

Validator and Reviewer are semantically different roles even when one durable Issue container carries both phases.

## 10. Standard Role Profile — Controller / Orchestrator

### 10.1 Responsibility

Observe durable state, determine legal next work, perform deterministic controller transitions, dispatch required roles, consume terminals and maintain workflow currentness.

### 10.2 Allowed Product behavior

The Controller/Orchestrator may, under authority:

- recompute READY sets;
- make JIT dispatch/materialization decisions;
- select among eligible Agent/environment choices;
- perform deterministic merge/freeze/state bookkeeping transitions owned by Controller authority;
- coalesce compatible durable work phases without collapsing role independence;
- keep deterministically blocked work in wait states;
- request bounded repair/escalation from new evidence;
- emit execution-decision/learning records.

### 10.3 Forbidden Product behavior

The Controller/Orchestrator cannot substitute its own judgment for a required independent terminal or invent evidence on behalf of an Agent/environment.

## 11. Other standardized roles

v4.9 MUST support the same Base Contract/Profile model for at least the following where applicable:

- Planner / Product Researcher;
- Architect / Architecture Researcher;
- Integration Agent;
- Hidden Validator;
- Release Qualifier;
- domain/project specialized execution roles.

The Product does not require every role to have identical lifecycle depth. A role profile may be read-only, evidence-only, mutable, environment-bound, or independent-gate authority.

## 12. Independence semantics

### 12.1 Independence is not container count

Where authority requires independence, it MUST be attributable through role/operator/session/dispatch/execution facts.

A separate Issue MAY be used when useful, but a new Issue object is not by itself proof of independence and is not always required.

### 12.2 Phase-separated durable work item

One durable work item MAY carry multiple sequential phases if:

- the authority permits it;
- each phase has an unambiguous role/dispatch/claim/current subject;
- required independent actors/sessions remain distinct;
- previous terminal evidence remains immutable/history-preserving;
- phase transition is explicit;
- no mutable role is allowed to self-approve a required independent phase.

## 13. Evidence currentness / equivalence

### 13.1 Hard rule

A materially changed candidate/contract/authority/runtime composition cannot inherit stale PASS by convenience.

### 13.2 Explicit equivalence path

v4.9 SHOULD support a bounded durable proof that prior exact-subject evidence remains applicable across target/base movement when all required equivalence predicates are established.

Candidate factors for L2 research:

```text
candidate source/head/tree unchanged
changed paths disjoint or semantically irrelevant
owned contract/schema/authority unchanged
runtime composition impact absent or proven bounded
required current-target rule does not explicitly forbid reuse
merge/rebase transformation does not alter validated subject
```

If equivalence cannot be proved, affected evidence becomes historical-only and successor Validation/Review is required according to current authority.

## 14. Gate coalescing and evidence reuse

Compatible bookkeeping/execution containers MAY be coalesced; authority MUST NOT be coalesced merely to reduce count.

Every coalesced/reused/not-applicable decision must be explainable from durable facts such as:

- role/session independence;
- exact-subject identity/equivalence;
- disjointness;
- current authority;
- explicit materiality/release applicability.

## 15. Pillar P4 — Execution Learning & Recurrence Escalation

### 15.1 Product requirement

ADS should preserve only material execution learning needed to improve future execution/standard quality without creating a mandatory retrospective for every Task.

Candidate lightweight categories:

```text
standard_gap
workflow_waste
missing_contract
useful_pattern
bad_pattern
repeated_failure_mode
proposed_ads_improvement
```

### 15.2 Recurring Failure Audit

When evidence suggests materially the same or related failure pattern is recurring, the Orchestrator/Controller SHOULD be able to request a recurrence audit that distinguishes:

```text
same root cause
related root cause
unknown relation
different cause / superficial similarity
```

The goal is to identify the earliest reliable prevention/detection point, such as:

```text
Task Pack/L3/template
schema/contract
pre-merge checker
release-identity checker
policy rule
orchestration rule
Product/Architecture gap
```

### 15.3 Governance boundary

Execution learning is evidence, not self-amending authority.

The flow is:

```text
project execution observations
→ evidence aggregation / recurrence signal
→ ADS improvement candidate
→ normal L1/Product/Architecture governance
→ future standard version
```

## 16. Scheduling / Agent selection product semantics

v4.9 reuses v4.8 eligibility semantics and extends them with role/workflow requirements.

Selection should conceptually resolve:

```text
legal/required workflow
→ required role
→ hard executor eligibility
   - capability
   - tools/environment
   - authority/freedom
   - independence
   - security/access
   - availability/resource
→ feasible executor set
→ optional project-defined optimization
   - priority/critical path
   - queue age
   - cost/latency class
   - scarce environment/device
   - parallel capacity
   - retry history
→ Dispatch
→ existing Claim admission
```

Provider/model name alone MUST NOT grant authority or eligibility.

## 17. Required durable execution decision

v4.9 requires sufficient auditability to explain why a workflow/Agent/gate choice was made, but it does not require verbose reasoning logs or chain-of-thought.

A compact decision record should be able to reference, as applicable:

```text
subject/current durable state
selected assurance profile/required roles
materiality/risk/authority basis
selected Agent/environment and eligibility refs
gates required/coalesced/reused/not applicable
evidence reused/currentness basis
concurrency/dependency/wait decision
unexpected blocker/rework/escalation
outcome
```

The exact storage/schema is L2.

## 18. Required product acceptance scenarios

v4.9 implementation must eventually prove, at Product level, at least these scenario families.

### A. Semantic-neutral bounded maintenance

A low-risk non-semantic change can complete with bounded checks/review policy without automatically entering full release ceremony, while current authority remains explicit.

### B. Bounded normative change

A semantic rule change selects focused independent Review/Validation as required by risk without automatically creating unrelated release gates.

### C. Machine-contract/high-risk change

Schema/lifecycle/authority changes receive stronger exact-subject Validation + independent Review and cannot be down-classified by a low file count or “docs” label.

### D. Release-significant change

Compatibility/migration/release-significant work still enters the full required Closure/Freeze/Hidden/RQ path.

### E. One durable Issue, multiple independent phases

Builder/Validator/Reviewer or Closeout/RQ phases may share a durable work item while independent actor/session terminals remain machine-distinguishable.

### F. Duplicate claim race

Two eligible Agents race the same incompatible role/work item; only accepted Claim may start authoritative execution.

### G. Wrong-role / independence rejection

An otherwise capable Agent cannot claim a required independent role when it conflicts with current independence policy.

### H. Branch movement only

A reviewed/validated unchanged concern survives unrelated target movement only after explicit equivalence/currentness proof; unsafe ambiguity fails closed.

### I. Material drift

A changed contract/schema/runtime composition invalidates affected old evidence and requires successor assurance.

### J. Hidden high-risk finding

A real Hidden/release P1 cannot be optimized away; thaw/repair/requalification is triggered according to current authority.

### K. Known sequence block

Work that cannot legally start remains a wait-state and does not generate pointless Agent execution.

### L. Recurring failure

Repeated materially-related defects can trigger systemic root-cause/prevention analysis without automatically adding another human gate.

## 19. Product metrics / telemetry

v4.9 SHOULD make it possible to describe, without inventing unsupported economic claims:

```text
execution work items/issues created
controller-direct transitions
independent sessions/gates
known-blocked dispatches avoided
revalidation/rebind events
branch-movement-only vs material revalidation causes
evidence reuse/coalescing decisions
implementation work vs orchestration steps
recurring-failure detections/systemic prevention actions
```

Metrics are descriptive evidence. No universal cost-savings claim or Agent ranking is authorized without measured evidence.

## 20. Compatibility and migration

v4.9 must be additive over existing durable v4.x history where possible.

- Existing Task/Review/Validation/Release records remain historical truth.
- Existing Dispatch/Claim semantics remain the execution admission foundation.
- v4.9 must not retroactively declare previously legal full-chain execution invalid simply because a future proportional path would be shorter.
- New role/profile/decision metadata should prefer backward-compatible writer/profile extensions over invalidating historical events.
- Downstream projects may adopt proportional/adaptive behavior incrementally; absence of an optional optimizer/runtime service must not make manual GitHub-native execution impossible.

## 21. Security, privacy and authority constraints

v4.9 MUST NOT require storing:

- secrets/credentials;
- private chain-of-thought;
- hidden evaluator/private Hidden dataset contents;
- unnecessary personal identity beyond authorized operator/session provenance.

Transport/tool availability does not grant mutation authority. Agent capability does not grant Review/Validation/Release authority.

## 22. Non-goals

v4.9 does not require:

- a universal autonomous scheduler daemon;
- replacement of GitHub as the current ADS reference durable fact plane;
- a second Dispatch/Claim/task lifecycle;
- always-on high-frequency heartbeat;
- a universal scalar Agent quality score;
- provider/model-specific normative procedures;
- blanket low-cost Agent routing;
- blanket removal of independent Review/Validation;
- automatic evidence reuse after any base movement;
- automatic ADS mutation from project learning;
- special treatment that only makes `ai-development-standard` easier;
- disclosure of private chain-of-thought;
- full release ceremony for every non-release-significant concern.

## 23. Product Freeze blockers

The PRD MUST NOT freeze until adversarial Product review has dispositioned at least:

1. whether adaptive materiality can be gamed/down-classified;
2. whether the Orchestrator gains implicit authority beyond scheduling;
3. whether evidence-equivalence rules can launder stale PASS;
4. whether phase coalescing can hide independence failure;
5. whether Role Profiles are sufficiently machine-checkable without becoming rigid vendor scripts;
6. whether the proposal duplicates v4.8 scheduler/Dispatch/Claim ownership;
7. whether telemetry/learning reintroduces process explosion;
8. whether full release/Hidden paths remain unambiguously required when release-significant;
9. whether the Product scope is too large for one minor version and, if so, what coherent narrowing preserves the core loop;
10. whether backward compatibility with current v4.x durable facts is credible.

## 24. Product acceptance criteria

Product Freeze requires evidence that the reviewed PRD establishes all of the following without architecture overreach:

```text
P1 proportional assurance semantics are clear
P2 adaptive orchestration authority boundaries are clear
P3 Agent Operating Model role/base-contract semantics are clear
P4 execution learning/recurrence governance is clear
v4.8 capability/Dispatch/Claim ownership is preserved
independence != Issue count is explicit
evidence reuse is fail-closed and equivalence-based
concern assurance != release assurance is explicit
release-significant full path is preserved
provider/model identity does not become authority
manual/GitHub-native execution remains possible
L2 implementation choices remain open where appropriate
```

## 25. Current gate

```text
VERSION=v4.9.0
PRD_STATUS=FIRST_REVIEW_CANDIDATE
PRODUCT_FREEZE=NO
ADVERSARIAL_PRODUCT_REVIEW=REQUIRED
L2_AUTHORITY=NO
TASK_DAG_AUTHORITY=NO
IMPLEMENTATION_AUTHORITY=NO
```

The next step is adversarial Product review. Review findings must be durably recorded and resolved before any explicit Product Freeze.