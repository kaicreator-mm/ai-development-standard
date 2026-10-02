# ai-development-standard v4.9.0 PRD — Adaptive Proportional Development Orchestration

Status: **AUTHOR PRE-REVIEW REVISED CANDIDATE — NOT FROZEN; INDEPENDENT ADVERSARIAL PRODUCT REVIEW REQUIRED**

Planning baseline: `main@9383244abb8172b5ae5135cbd559c72837799375`

Planning parent: `#697`

Primary planning/dogfood input: `#680`

L1 evidence: `docs/implementation/4.9.0/L1_PRODUCT_EVIDENCE.md`

Author-side adversarial pre-review: PR #698 comment `5961233246` (non-independent; not Product Review authority).

This PRD is a Product candidate only. It does not authorize Product Freeze, L2, Task DAG materialization, implementation, scheduler deployment, schema migration, gate omission, evidence transfer, or any weakening of current/pinned Product, Architecture, Task, Review, Validation, Execution or Release authority.

## 1. Product intent

v4.9.0 makes ADS execution more proportional, adaptive and role-consistent while preserving fail-closed authority.

The Product goal is:

> Given live durable project facts and an already-authorized assurance floor, ADS can select the **minimal sufficient legal workflow above that floor**, identify the roles actually required, select an eligible Agent/environment for each role, standardize how that role claims/executes/hands off/terminates work, reuse prior evidence only when the owning Gate Authority positively permits transfer and every required binding dimension remains equivalent, and turn repeated execution friction into governed improvement candidates.

v4.9 builds on existing ADS Product/Architecture/Task/Execution/Dispatch-Claim/Review/Validation/Release semantics. It does not replace them with a second lifecycle or a universal autonomous Agent runtime.

## 2. Product problem and evidence boundary

### 2.1 Orchestration amplification is real

v4.x dogfood shows that small and medium concerns can expand into long chains of Builder, Validation, Fresh Review, merge, Stage1, Candidate Freeze, Hidden, Closeout, Release Qualification, Repository Integration and successor currentness/rebind work.

Those gates are valuable when they protect a material authority/risk boundary. They are waste when execution objects or repeated gates add no new decision value.

### 2.2 Current proportional mechanisms are not enough operationally

ADS already has Fast Path, risk-based Review Policy, on-demand architecture demos, JIT Task admission and derived READY queues. The remaining problem is not absence of proportional concepts; it is lack of a sufficiently explicit runtime contract for selecting the smallest legal workflow from live facts without allowing optimistic downgrade.

### 2.3 Runtime decisions cannot all be pre-expanded at planning time

Readiness, currentness, evidence transferability, environment availability, bounded repair, sequence waits and recurrence signals are live facts. Pre-materializing every possible Builder/Validator/Reviewer/Controller node creates stale work and guaranteed-BLOCKED dispatches.

### 2.4 Role behavior is distributed across standards

Builder, Reviewer, Validator, Controller, Release Qualifier and other roles exist, but their common operating contract is distributed across workflow/interaction/execution/review/validation/release standards.

### 2.5 Evidence generality is PARTIAL

The strongest direct evidence is ADS self-dogfood in #680. External interoperability/scheduling standards support the architectural shape, but do not by themselves prove ADS gate-reduction correctness for downstream projects.

Therefore:

```text
GENERALITY_EVIDENCE=PARTIAL
STANDARD_SELF_EXCEPTION_ALLOWED=NO
DOWNSTREAM_DOGFOOD_REQUIRED_BEFORE_RELEASE=YES
```

Product Freeze may define the model, but release qualification of v4.9 must include downstream/manual GitHub-native dogfood proving the model can reduce ceremony without weakening required authority.

## 3. Four integrated Product pillars

v4.9 freezes, if independent Product Review authorizes it, four integrated pillars:

1. **P1 — Proportional Assurance**
2. **P2 — Adaptive Orchestration**
3. **P3 — Agent Operating Model**
4. **P4 — Execution Learning & Recurrence Escalation**

They compose as:

```text
current/pinned authority defines assurance floor + selectable policy
        ↓
P1 resolves the minimum legal assurance/role set at or above that floor
        ↓
P2 selects legal JIT work and an eligible executor/environment
        ↓
P3 defines how each role claims, executes, evidences, hands off and terminates
        ↓
P4 records only material learning/recurrence and feeds ordinary ADS governance
```

Cross-cutting invariants:

- fail-closed authority;
- no self-minted independent PASS;
- typed evidence currentness/transfer rules;
- multi-dimensional independence;
- existing Dispatch/Claim ownership preserved;
- manual/GitHub-native execution remains possible.

## 4. Authority precedence and monotonic assurance floor

### 4.1 Assurance Floor

Before proportional workflow selection, the system MUST resolve an `ASSURANCE_FLOOR` from current/pinned higher authority, including as applicable:

```text
Frozen Product / Scope
Frozen Architecture / Contract
Task / Task Pack / Execution Pack
PROJECT_OVERRIDES that are allowed by higher authority
Review Policy
Validation authority/profile
Release authority/applicability
security / ownership / independence constraints
```

The Orchestrator may always **escalate** above the floor when new risk/evidence requires it.

The Orchestrator MUST NOT reduce below the floor merely because a model judges the work low-risk, documentation-only, cheap, disjoint or easy.

A lower workflow is legal only when the **owning higher authority positively defines selectable proportional profiles/conditions** and the current durable facts prove the required predicates.

```text
NO_POSITIVE_AUTHORITY_FOR_REDUCTION => NO_REDUCTION
UNKNOWN_OR_AMBIGUOUS_CLASSIFICATION => ESCALATE_OR_BLOCK
```

Absence of an explicit prohibition is not permission to omit a gate.

### 4.2 Authority vs orchestration

```text
Authority defines what is required/permitted and who owns the decision.
Orchestration selects the next legal action from current facts inside that authority.
```

A high-capability model can reason about ambiguity; it cannot create new authority by reasoning quality.

## 5. P1 — Proportional Assurance

### 5.1 Product requirement

ADS MUST support proportional assurance profiles or equivalent policy so a concern is not automatically expanded to maximum ceremony when current authority permits a smaller legal path.

Candidate materiality dimensions include:

```text
semantic impact
machine-contract/schema impact
lifecycle/state impact
authority/gate ownership impact
security/data integrity impact
migration/compatibility impact
runtime composition impact
release applicability
current evidence/currentness
```

Class A/B/C/D-like labels may be useful defaults, but no single label, file count, model identity or `docs-only` tag is sufficient authority.

### 5.2 Required resolution

Before authoritative dispatch/merge/release transitions, the system must be able to resolve, as applicable:

```text
ASSURANCE_FLOOR
materiality / risk basis
required role set
required Validation scope
Review Policy
required independence dimensions
release applicability owner + result
Closure/Freeze/Hidden/Closeout/RQ applicability
currentness/evidence disposition
NOT_APPLICABLE / NOT_RUN / BLOCKED truth
```

### 5.3 Concern assurance vs release assurance

A Task/PR may require focused Validation and/or Review without itself becoming a complete version-release workflow.

However, **Release Standard/current pinned release authority remains the owner of release applicability**. v4.9 does not itself grant the Orchestrator authority to classify a version out of currently mandatory release gates.

If current authority requires Version Closure, Candidate Freeze, Hidden, Fresh Closeout or Release Qualification, those gates remain required until an authorized standard/project policy explicitly changes that requirement.

Unknown release applicability MUST fail closed or choose the stronger currently authorized path.

Historical projects pinned to older ADS semantics retain those semantics; v4.9 cannot retroactively shorten their release path.

### 5.4 Fast Path strengthening

Fast Path should become a genuinely smaller workflow only where the assurance floor and current authority permit it. It must still preserve current authority discovery, required Review/Validation truth, Claim/start ownership where applicable, exact-subject evidence and escalation when risk grows.

## 6. P2 — Adaptive Orchestration

### 6.1 Product requirement

ADS SHOULD support a high-capability orchestration control plane that reads live durable facts and selects the next legal work JIT instead of requiring every execution phase to be pre-materialized.

Candidate responsibilities:

```text
read live DAG / Issues / PRs / refs / Claims / terminals / evidence
compute actually-ready work
resolve ASSURANCE_FLOOR and selectable profiles
classify live materiality only inside authorized policy
resolve required roles/gates
choose eligible Agent/model/environment
control JIT admission/concurrency
avoid duplicate or knowingly blocked dispatch
consume terminals
choose authorized bounded repair vs escalation
request evidence-reuse proof where gate authority permits it
record compact execution decision/learning evidence
```

### 6.2 Deterministic guardrails

Architecture MUST preserve a separation equivalent to:

```text
High-capability reasoning
  → ambiguity, decomposition, prioritization, recovery trade-offs

Deterministic policy/contract enforcement
  → assurance floor, mandatory gates, illegal transitions,
    independence policy, authority ownership, evidence bindings

Durable fact plane
  → GitHub/repository/evidence/current operation facts
```

### 6.3 Orchestrator hard boundaries

The Orchestrator MUST NOT:

- mint required independent Review/Validation/Hidden/RQ PASS;
- reduce below `ASSURANCE_FLOOR` without positive higher-authority permission;
- silently waive Frozen Product/L2/Task/Release requirements;
- invent a new evidence-transfer rule not owned by the applicable Gate Authority;
- treat private chat memory as canonical current state;
- hide `BLOCKED`, `NOT_RUN`, `NOT_APPLICABLE`, stale or unknown truth;
- bypass existing Dispatch/Claim admission;
- make cost/latency/availability override hard eligibility;
- mutate ADS automatically from project learning.

### 6.4 Task DAG boundary

The Frozen Task DAG/current Task authority remains the semantic work envelope.

Adaptive orchestration MAY JIT materialize authorized execution phases, role handoffs, gates and durable containers **inside** that envelope.

It MUST NOT invent a material new implementation concern, change dependency/ownership semantics, or widen Frozen scope merely because live reasoning considers it useful. Such change requires the existing Task/Architecture/Product amendment path as applicable.

### 6.5 Non-dispatch wait states

When work is deterministically not ready, orchestration SHOULD preserve a durable wait state such as `WAITING_LINEAGE` or equivalent rather than dispatch a task whose only legal result is a known sequence block.

### 6.6 Controller transitions are still authority-bearing

Controller-direct execution can avoid unnecessary Issues, but not every controller action is mere bookkeeping.

Merge, Candidate Freeze, thaw/invalidate, release integration and similar transitions may be deterministic only **after** their owning authority and exact prerequisites are satisfied. Coalescing the container does not remove the authority boundary.

## 7. P3 — Agent Operating Model

### 7.1 Role, not vendor/model, is normative

ADS MUST define a provider-neutral **Agent Execution Base Contract** plus role-specific **Role Profiles**.

ChatGPT, Claude, Codex, local agents and future runtimes are executors of roles; provider/model identity is provenance/capability evidence, not authority by itself.

### 7.2 Base lifecycle

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

Existing v4.8 Dispatch/Claim authority remains canonical. v4.9 MUST NOT create a second lease/lock/task lifecycle.

### 7.3 Common pre-Claim requirements

Before authoritative execution, the applicable contract must establish as needed:

```text
work remains READY/current
dependencies satisfied
role matches dispatch
required capability/tools/environment available
required independence policy satisfied
no incompatible accepted active Claim
current authority refs read
exact subject/base/target resolved
allowed scope/write set resolved
forbidden scope/actions resolved
required evidence + terminal authority resolved
```

No accepted Claim where Claim is required => no authoritative execution.

### 7.4 Common execution requirements

An Agent must remain inside owned authority, re-check live facts on material drift, surface blockers/deviations, preserve exact-subject truth, avoid silently widening scope, and record only material evidence/learning required by policy.

Private chain-of-thought is never required.

### 7.5 Common terminal requirements

A terminal must be durably attributable to at least the applicable:

```text
role
work item / dispatch / claim
operator/principal/session provenance
exact subject/base/target
terminal state/verdict
outputs/artifacts/PR/commit refs
checks/tests/evidence refs
deviations/limitations/remaining risk
handoff/next gate
ownership release
```

Exact schema/event representation is L2.

### 7.6 Role Profile contract

Every standardized authority-bearing role must be expressible with:

```text
Eligibility
Required Inputs
Allowed Actions
Forbidden Actions
Required Evidence
Terminal Authority
Independence Policy
Environment / mutation class
```

Projects/domains may define stricter specialized profiles but cannot weaken higher ADS authority.

## 8. Required role semantics

### 8.1 Builder

Builder owns authorized mutable implementation/work-product production. It cannot start required authoritative mutation before accepted Claim/start and cannot self-approve an independent gate required by current authority.

Builder must consume current authority, stay within the concern/write set, produce required implementation/tests/docs/checks, record material deviations/blockers, stop on insufficient authority and emit an exact output/handoff terminal.

### 8.2 Reviewer

Reviewer owns an evaluative verdict against the exact review subject and current authority.

For a required independent Review, the Review phase MUST be read-only with respect to its subject. A repair requires a separately authorized mutable phase/role and then successor Review as current authority requires.

Reviewer must inspect actual subject/evidence, verify scope/currentness/forbidden behavior, emit severity findings and preserve the required independence dimensions.

### 8.3 Validator

Validator owns executed truth for specified tests/build/runtime/host/environment/scenario oracles. It must distinguish executed from inferred/not-run evidence and preserve required exact-subject/environment/profile bindings.

Reviewer and Validator are different semantic roles even when their phases share one durable Issue container.

### 8.4 Controller / Orchestrator

Controller/Orchestrator owns authorized workflow coordination: READY recomputation, JIT dispatch/materialization, eligible executor selection, terminal consumption, authorized deterministic state transitions, wait states and escalation.

It cannot substitute for an independent verdict or invent evidence.

### 8.5 Planner / Product Researcher, Architect / Architecture Researcher, Integration Agent, Hidden Validator, Release Qualifier and specialized roles

v4.9 requires these roles, when standardized/used, to be expressible through the same Base Contract and to declare their terminal authority, mutation/read-only class, required environment and independence policy.

Product does not require identical lifecycle depth for all roles. Detailed role-specific schemas/commands belong to L2/Task implementation.

## 9. Independence semantics

### 9.1 Independence is multi-dimensional

A different Issue or session is not sufficient proof of independence.

The applicable higher authority may require one or more independent dimensions such as:

```text
principal / logical executor independence
session/context independence
model/provider/configuration diversity
Builder-vs-Reviewer author conflict separation
Validator environment/host independence
evidence-source independence
Hidden-holder/private-evaluator separation
Release/Controller role separation
```

v4.9 MUST preserve the existing ADS distinction among independence dimensions rather than collapse them into `session_ref`.

### 9.2 Phase-separated durable work item

One durable work item MAY carry multiple sequential phases only when:

- current authority permits phase coalescing;
- each phase has an unambiguous role/dispatch/claim/current subject;
- **every applicable independence dimension**, not merely session identity, is satisfied;
- previous terminal evidence remains immutable/history-preserving;
- phase transition is explicit;
- a mutable actor cannot self-approve a required independent phase.

A separate Issue may still be required when environment, confidentiality, write isolation or authority requires a distinct durable container.

## 10. Typed evidence currentness and transfer

### 10.1 Evidence is bound to a declared tuple

Different evidence families bind to different dimensions. Examples include:

```text
concern Validation      → subject + validation profile + environment/toolchain + authority refs
integration Validation  → source subject + target/base + merge/composed result + profile/environment
Review                  → review subject/diff + current authority + required independence policy
Hidden                  → exact candidate + private pack/revision + holder/independence policy
Closeout/RQ             → frozen candidate + required predecessor gate bindings + release authority
```

Exact binding sets are owned by the applicable Gate Authority and frozen in L2/implementation.

### 10.2 Positive transfer permission

Prior evidence may be reused as current only if **all** are true:

1. the owning Gate Authority positively declares that evidence family transferable/rebindable under stated predicates;
2. every binding dimension required by that authority is equal or proven equivalent;
3. no explicitly non-transferable dimension changed;
4. no current-target/current-authority rule requires fresh execution;
5. the equivalence proof itself is durable/current.

```text
NO_TRANSFER_RULE => HISTORICAL_ONLY
UNKNOWN_BINDING => HISTORICAL_ONLY_OR_BLOCKED
MATERIAL_BINDING_CHANGE => SUCCESSOR_ASSURANCE_REQUIRED
```

Path disjointness, unchanged source HEAD/tree or ancestor topology MAY be inputs to a gate-specific proof, but are never universal evidence-transfer authority.

### 10.3 Non-transferable evidence

A Gate Authority may declare evidence fresh-only/non-transferable even when some structural identities appear equivalent. v4.9 cannot override that by generic equivalence reasoning.

## 11. Gate/container coalescing

Execution containers and bookkeeping MAY be coalesced where current authority permits it; authority itself cannot be coalesced to reduce count.

A coalesced work item must keep role, principal/session, exact subject, terminal, independence and phase history machine-distinguishable.

## 12. Scheduling / Agent selection

v4.9 reuses v4.8 capability, availability, eligibility, resource-selection and Dispatch/Claim ownership.

Conceptually:

```text
legal workflow at/above ASSURANCE_FLOOR
→ required role
→ hard executor eligibility
   capability + tools/environment + authority/freedom
   + independence + security/access + current availability/resource
→ feasible executor set
→ optional project optimization
→ Dispatch
→ existing Claim admission
```

Provider/model name alone does not grant eligibility or authority. If no eligible executor exists, the work is BLOCKED/waits/escalates; the scheduler cannot fall back to an ineligible executor.

## 13. P4 — Execution Learning & Recurrence Escalation

### 13.1 Bounded Product requirement

v4.9 requires lightweight material learning/recurrence evidence and escalation hooks, **not** a universal autonomous analytics/root-cause platform.

Candidate categories:

```text
standard_gap
workflow_waste
missing_contract
useful_pattern
bad_pattern
repeated_failure_mode
proposed_ads_improvement
```

Simple/Fast-Path work may record `NONE_MATERIAL` or equivalent.

### 13.2 Recurrence signal

When evidence suggests the same or related failure family recurs, the Controller/Orchestrator may request a bounded recurrence audit distinguishing:

```text
same root cause
related root cause
unknown relation
different/superficially-similar cause
```

The audit should seek the earliest reliable prevention/detection point: Task Pack/L3/template, schema/contract, checker, policy rule, orchestration rule, or Product/Architecture gap.

### 13.3 Governance boundary

Learning is evidence, not authority mutation:

```text
execution observations
→ bounded recurrence/learning evidence
→ ADS improvement candidate
→ normal L1/Product/Architecture governance
→ future standard change
```

Automated cross-project mining, universal fingerprinting and a dedicated learning database are non-goals for v4.9 unless separately authorized later.

## 14. Durable execution decision

v4.9 requires enough auditability to explain workflow/Agent/gate choices without storing chain-of-thought.

A compact record should be able to reference as applicable:

```text
subject/current durable state
ASSURANCE_FLOOR + owning authority
selected authorized profile/roles
materiality/risk predicates
selected Agent/environment + eligibility evidence
gates required/coalesced/reused/not-applicable
transfer/currentness proof refs
wait/dependency/concurrency decision
unexpected blocker/escalation
outcome
```

The exact schema/storage is L2.

## 15. Required Product acceptance scenarios

Implementation/release evidence must eventually prove at least:

### A. Low-risk semantic-neutral maintenance
An authorized low-assurance profile completes with bounded gates and does not silently bypass a higher assurance floor.

### B. Bounded normative semantic change
Focused Review/Validation is selected according to current authority without unrelated release ceremony.

### C. Machine-contract/high-risk change
Schema/lifecycle/authority changes cannot be down-classified by file count, labels or model judgment.

### D. Release-significant/currently release-governed change
The full required Closure/Freeze/Hidden/Closeout/RQ path remains required when current Release authority says so.

### E. Same durable container, multiple independent phases
Distinct phases share one Issue only while all applicable independence dimensions and terminals remain distinguishable.

### F. Duplicate Claim race
Only the accepted Claim starts authoritative incompatible work.

### G. Wrong-role / independence rejection
An otherwise capable Agent is ineligible when required independence policy conflicts.

### H. Gate-specific evidence transfer
Unrelated target movement reuses evidence only under a positive gate-owned transfer rule and complete binding equivalence.

### I. Material/unknown binding drift
Changed or unknown contract/authority/composition/environment binding makes affected evidence historical-only or blocks until successor assurance.

### J. Hidden/release high-risk finding
A real release finding triggers required thaw/repair/requalification rather than proportional optimization.

### K. Known sequence block
Work stays in a non-dispatch wait state instead of creating a guaranteed-BLOCKED task.

### L. Task-DAG scope protection
Adaptive orchestration cannot invent new semantic implementation work/dependencies outside frozen Task authority.

### M. Downstream manual/GitHub-native dogfood
At least one downstream project applies the proportional profile + Role Operating Model without a mandatory scheduler daemon and demonstrates reduced orchestration objects/steps while preserving all required authority/gates.

### N. Recurring failure
A repeated materially-related defect can produce a bounded prevention/escalation candidate without automatically adding a new human gate or mutating ADS.

## 16. Metrics / telemetry

v4.9 SHOULD support descriptive measurement of:

```text
execution work items/issues created
controller-direct transitions
independent sessions/gates
known-blocked dispatches avoided
revalidation/rebind events and causes
evidence transfer/coalescing decisions
implementation work vs orchestration steps
recurrence signals and prevention actions
```

No universal savings claim, Agent quality score or economic conclusion is authorized without measured evidence.

## 17. Compatibility and migration

- Existing v4.x durable records remain historical truth.
- Existing Dispatch/Claim semantics remain the execution admission foundation.
- v4.9 does not retroactively invalidate full-chain execution because a future proportional path would be shorter.
- Existing/pinned release policies remain binding until explicitly migrated.
- New metadata should prefer backward-compatible writer/profile extensions.
- Manual GitHub-native execution remains supported; no scheduler daemon is mandatory.
- A2A/queues/local transports may map to ADS semantics but external Task completion never automatically becomes ADS Review/Validation/Release truth.

## 18. Security and privacy

v4.9 MUST NOT require secrets, credentials, private chain-of-thought, private Hidden fixture/oracle contents, or unnecessary personal identity.

Only authorized operator/principal/session provenance needed for accountability/independence should be retained.

Tool/transport availability does not grant mutation authority. Capability does not grant Review/Validation/Release authority.

## 19. Non-goals

v4.9 does not require:

- a universal scheduler daemon;
- replacement of GitHub as the reference durable fact plane;
- a second Dispatch/Claim/task lifecycle;
- autonomous risk downgrade below higher authority;
- generic evidence reuse from path disjointness or unchanged HEAD alone;
- one-session-equals-independent semantics;
- automatic ADS mutation from project learning;
- an autonomous cross-project root-cause analytics platform;
- a universal Agent quality score;
- provider/model-specific normative procedures;
- blanket low-cost routing;
- blanket removal of independent Review/Validation;
- full release ceremony for concerns to which current Release authority does not apply;
- disclosure of private chain-of-thought;
- a special easier rule only for `ai-development-standard`.

## 20. Product Freeze blockers

The PRD MUST NOT freeze until an independent adversarial Product Review has verified/dispositioned at least:

1. monotonic `ASSURANCE_FLOOR` and optimistic downgrade prevention;
2. Release authority ownership and historical-pinned compatibility;
3. gate-specific positive evidence-transfer authority and binding completeness;
4. multi-dimensional independence under same-Issue phase coalescing;
5. Task-DAG semantic scope protection;
6. v4.8 capability/scheduling/Dispatch/Claim ownership preservation;
7. Role Profile machine-checkability without vendor hard-coding;
8. bounded P4 learning/recurrence scope;
9. downstream-generalization acceptance requirement;
10. full Hidden/Closeout/RQ preservation where current authority requires it;
11. compatibility with historical durable facts;
12. whether the four-pillar scope remains coherent for one minor version.

## 21. Product acceptance criteria for Freeze

Product Freeze requires a current independent review showing the candidate establishes, without architecture overreach:

```text
ASSURANCE_FLOOR is non-weakening and monotonic
adaptive reasoning cannot mint reduction authority
release applicability remains owned by current/pinned Release authority
P1/P2/P3/P4 remain one coherent execution loop
v4.8 capability/Dispatch/Claim ownership is preserved
Task DAG semantic scope cannot be widened by runtime orchestration
independence is multi-dimensional, not Issue/session count
Evidence transfer is gate-owned, typed and fail-closed
Reviewer/Validator/Builder/Controller authority separation is explicit
other authority-bearing roles fit one Base Contract/Profile model
manual/GitHub-native execution remains possible
downstream dogfood is required before v4.9 release
P4 remains lightweight evidence/escalation, not a new analytics platform
L2 implementation choices remain open where appropriate
```

## 22. Current gate

```text
VERSION=v4.9.0
PRD_STATUS=AUTHOR_PRE_REVIEW_REVISED_CANDIDATE
PRODUCT_FREEZE=NO
INDEPENDENT_ADVERSARIAL_PRODUCT_REVIEW=REQUIRED
L2_AUTHORITY=NO
TASK_DAG_AUTHORITY=NO
IMPLEMENTATION_AUTHORITY=NO
```

The next authoritative step is a genuinely independent adversarial Product Review bound to the successor exact PR HEAD/tree. This author-side pre-review is quality evidence only and must not satisfy the independent gate.
