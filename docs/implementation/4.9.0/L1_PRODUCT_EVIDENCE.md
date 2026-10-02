# v4.9.0 L1 Product Evidence — Adaptive Proportional Development Orchestration

Status: **COMPLETE RESEARCH / PRE-FREEZE — ADVERSARIAL PRODUCT REVIEW REQUIRED**

Research date: 2026-10-03

Planning baseline: `main@9383244abb8172b5ae5135cbd559c72837799375`

Planning parent: `#697`

Primary dogfood input: `#680`

This document is Product evidence only. It does not authorize Product Freeze, L2, Task DAG materialization, implementation, scheduler deployment, or weakening of any existing Frozen authority/gate.

## 1. L1 verdict

**PROCEED WITH A UNIFIED v4.9 PRODUCT CANDIDATE.**

The evidence supports treating the current problems as one Product concern rather than a collection of unrelated workflow exceptions:

> ADS needs a standard way to derive the **minimal sufficient execution workflow** from live durable facts and material risk, select an eligible Agent/environment, standardize how each role claims/executes/hands off/terminates work, and learn from repeated execution friction — while deterministic rules preserve non-negotiable authority, exact-subject truth and independence.

Recommended Product shape:

1. **Proportional Assurance Profiles** — materiality/risk/authority impact determines the minimum required assurance shape instead of universal release-grade ceremony.
2. **Adaptive Orchestration under Deterministic Guardrails** — a high-capability control plane may make live scheduling/materiality/recovery choices, but cannot mint PASS or waive Frozen authority.
3. **Agent Operating Model / Role Execution Protocol** — a common execution lifecycle plus role-specific contracts for Builder, Reviewer, Validator, Planner/Architect, Controller/Orchestrator, Release Qualifier, Hidden Validator and specialized roles.
4. **Evidence Reuse / Currentness Equivalence** — exact-subject evidence may remain current across provably irrelevant target movement; material semantic change still invalidates/requires successor evidence.
5. **Execution Learning / Recurring Failure Escalation** — repeated workflow waste or repeated defect families should preferentially improve earlier deterministic prevention/checking rather than add downstream ceremony.

v4.9 SHOULD NOT create a second Dispatch/Claim lifecycle, a second Task state machine, a universal Agent score, an unchecked autonomous scheduler authority, or a standard-specific exception only for `ai-development-standard`.

## 2. Internal evidence — current ADS already contains the substrate

### 2.1 Development Workflow is already proportional in principle

Current `standards/DEVELOPMENT_WORKFLOW.md` already provides:

- Version Branch vs Trunk/Fast Path integration modes;
- risk-based Review Policy (`required | recommended | not-required`);
- on-demand Architecture Research Demo;
- stage checkpoints that do not require one branch/Issue per artifact;
- JIT Task branch/Execution Pack creation after dependencies resolve;
- canonical live Task DAG through GitHub Issue Dependencies;
- mandatory truthfulness for required Validation/Review/Release evidence.

**Finding:** the gap is not absence of proportional concepts. The gap is that the execution model still tends to materialize or re-run more workflow than the live concern actually requires. v4.9 should operationalize proportionality, not merely restate it.

### 2.2 v4.8 already owns capability, eligibility and constraint-first assignment

Frozen v4.8 Product separates:

```text
Capability Claim
Availability / Resource Fact
Capability Evidence
```

and defines a selection pipeline:

```text
READY set
+ Task requirements/risk/freedom/environment/independence
+ capability/availability/evidence
→ hard eligibility filtering
→ feasible choices
→ optional ranking/optimization
→ existing Dispatch reservation / Claim admission
```

It also explicitly states that capability is not authorization and that cost/latency cannot make an ineligible executor eligible.

**Finding:** v4.9 must extend from **eligible assignment** to **adaptive workflow composition and role execution semantics**. It must not replace v4.8 scheduling or capability ownership.

### 2.3 v4.8 T-017/#646 already owns execution-start visibility and Claim admission

#646 standardizes, over the existing Dispatch/Claim lifecycle:

- `NO_CLAIM_NO_EXECUTION`;
- accepted Claim as the durable start fact;
- visible `state:claimed → state:implementing` projection without treating labels/comments as a lock;
- actor/operator/session/exact-subject provenance;
- terminal ownership release;
- idempotent resume and safe timeout/stale reconciliation;
- optional non-authoritative heartbeat/progress.

**Finding:** v4.9 should define what every role MUST verify before Claim, what it may do after accepted Claim, what evidence it must produce, and what authority its terminal has. It should reuse accepted Claim rather than create a new lease/lock system.

## 3. Dogfood evidence — orchestration amplification is real

#680 records that routine and medium ADS changes have repeatedly expanded into chains similar to:

```text
Builder
→ exact-subject Validation
→ Fresh Independent Review
→ merge
→ Version Closure Stage1
→ Candidate Freeze
→ Hidden Validation
→ Fresh Closeout
→ Release Qualification
→ Repository Integration
→ post-integration/currentness rebind
```

The issue identifies the resulting costs: Issue noise, repeated current-target invalidation, controller complexity, unnecessary independent sessions, and orchestration work dominating implementation work.

The hypothesis is therefore not “remove gates.” It is:

> determine which gates and independent actors materially contribute new assurance for this concern, while making omission/reuse/coalescing explicit and auditable.

## 4. PRACTICE-01 evidence — object count can drop without assurance loss

The bounded #680 shadow practice produced multiple live examples under existing Frozen authority.

### 4.1 Phase-separated durable work items

Fresh Closeout and Release Qualification phases were carried in the same durable Issue while still requiring distinct actor/session claims and distinct terminal verdicts.

Likewise, v4.2 #689 reused one durable work item for Builder then independent LOCAL Validation.

Observed value:

- fewer Issue containers and dispatch bookkeeping steps;
- no mandatory gate skipped;
- independent actor requirement preserved;
- exact candidate binding preserved.

**Finding:** independence is primarily an actor/session/authority property, not an Issue-count property.

### 4.2 Controller-direct deterministic transitions

Controller consumed valid PASS terminals, performed expected-head merges, Candidate Freeze/state reconciliation and native DAG rereads without creating dedicated execution Issues solely for deterministic bookkeeping.

**Finding:** a durable work item should exist when new independent decision value, mutable work, a distinct environment, or a separately terminal verdict is required — not merely because a state transition exists.

### 4.3 WAITING_LINEAGE instead of guaranteed BLOCKED dispatch

When integration could not legally start before predecessor lineage reached main, PRACTICE-01 retained a controller wait state rather than dispatching an Issue whose only possible result was `BLOCKED_SEQUENCE`.

**Finding:** readiness must be derived from live durable facts; pre-materializing impossible work adds no assurance.

### 4.4 Branch movement/currentness proof

v4.8 T004 PR #651 and DAG R2 PR #684 provided a concrete case where target movement did not change the reviewed concern: changed paths were disjoint, candidate source/head did not change, Product/L2 did not change, and repeat review would have produced no new decision value.

v4.2 also produced a case where historical branch topology caused merge conflicts while the candidate itself remained semantically validated; retargeting to an exact ancestor made the PR mergeable without changing the candidate tree.

**Finding:** v4.9 should research an explicit **evidence-equivalence/currentness proof**, not a blanket rule that every target movement invalidates every exact-subject result.

### 4.5 Real high-risk findings still require full escalation

v4.6 private Hidden validation found a real release-significant P1 identity defect. PRACTICE-01 did not optimize it away: the candidate was thawed/invalidated, repaired, and remained subject to successor Fresh Review/Stage1/Freeze/Hidden obligations.

**Finding:** proportional orchestration must reduce ceremony only where decision value/risk permits it. New material risk must deepen or restore assurance.

## 5. New Product gap — Agent Operating Model is not yet unified

Current ADS has role concepts and many role-specific constraints, but the common operating contract is distributed across workflow, interaction, execution, validation, review and release rules.

The missing product is a provider-neutral model:

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

### 5.1 Why Role, not vendor/model, should be normative

ADS must standardize `Builder`, `Reviewer`, `Validator`, `Planner/Architect`, `Controller/Orchestrator`, `Release Qualifier`, `Hidden Validator`, etc., not ChatGPT/Claude/Codex-specific procedures.

A concrete Agent/model/runtime is an executor of a role. Provider/model identity remains provenance/capability evidence, not the definition of authority.

### 5.2 Common Base Contract candidate

Every authoritative Agent execution should resolve at least:

```text
role
work item / operation / dispatch
current readiness
current authority refs
exact subject/base/target when applicable
capability/environment requirements
independence constraints
accepted Claim/start fact
allowed actions/write set
forbidden actions
required evidence
terminal authority
handoff / successor semantics
ownership release
```

The exact schema belongs to L2; Product needs the semantic requirement.

### 5.3 Role Profile candidate

Each standardized role should define only the delta from the common Base Contract:

```text
Eligibility
Required Inputs
Allowed Actions
Forbidden Actions
Required Evidence
Terminal Authority
```

This avoids duplicating a complete lifecycle per role.

## 6. Builder evidence and Product requirements

A Builder should not begin authoritative mutable work before accepted Claim. Before Claim/start it should prove that the work remains READY/current, its dependencies are satisfied, its execution profile/environment is eligible, and no independence/ownership conflict exists.

During execution it should remain inside the owned concern/write set, verify material assumptions against durable facts, record material deviations/findings, and stop/escalate rather than silently widen Frozen Product/L2 authority.

Builder completion should expose enough structured evidence for downstream automation to consume without parsing an essay, including exact result identity, actual write set, checks/tests, PR/commit/artifact refs, deviations, remaining risks and required handoff.

**Product boundary:** v4.9 does not require narration/private chain-of-thought or a full retrospective for every Task.

## 7. Reviewer evidence and Product requirements

Independent Review is not “a second Builder.” Product semantics should make the distinction explicit.

Default Review behavior where Review is required:

- bind to the exact review subject/current authority;
- remain read-only unless a separately authorized repair role is created;
- independently inspect actual change/evidence, not merely trust Builder summary;
- verify scope/currentness/authority/negative cases and claimed evidence;
- produce durable severity findings and a terminal verdict;
- never silently fix the subject and then review its own mutation.

**Finding:** Reviewer independence must be machine-checkable using role/operator/session/dispatch facts where the authority requires independent review.

## 8. Validator evidence and Product requirements

Validator answers a different question from Reviewer: whether the exact subject actually satisfies specified executable/environmental oracles.

Product semantics should distinguish:

```text
Reviewer: conforms to authority/design/scope/evidence requirements?
Validator: actually runs/behaves as required in the specified environment/scenarios?
```

The two roles may share a durable Issue container under proportional execution, but where independence is required their actor/session/terminal authority remains distinct.

## 9. Controller / Orchestrator evidence and Product requirements

#680 planning evidence supports a high-capability orchestration control plane because many runtime decisions depend on live facts that cannot be fully frozen at Task-DAG planning time:

- whether target drift is materially relevant;
- whether evidence remains current/reusable;
- which Agent/environment is presently available;
- whether a task is actually READY;
- whether a known blocker warrants waiting vs dispatch;
- whether a repeated finding indicates a systemic standard gap;
- whether a bounded repair is sufficient or release requalification is required.

However, the orchestrator must not become a supreme authority.

Candidate hard Product invariants:

1. GitHub/repository/evidence remain the durable fact plane.
2. The orchestrator cannot self-mint required independent PASS.
3. Frozen Product/L2/gate authority cannot be silently waived.
4. Dynamic reductions/reuse/coalescing must have durable explainable basis.
5. Deterministic rules should reject illegal transitions and unsafe downgrades.
6. Uncertainty stays explicit as `BLOCKED`, `NOT_RUN`, `NOT_APPLICABLE`, stale/unknown, etc.
7. Materiality/risk uncertainty should fail closed or escalate, not optimistically down-classify.

## 10. Product correction — static classes alone are insufficient

#680 proposes Class A/B/C/D-like risk/materiality categories as research inputs:

- semantic-neutral maintenance;
- bounded normative semantic change;
- machine-contract/lifecycle/authority change;
- release-significant compatibility/migration change.

L1 supports these as deterministic defaults/guardrails, but not as the whole scheduler.

Real execution shows that workflow depth also depends on live facts such as currentness, overlap, environment, existing evidence and newly surfaced defects.

Recommended direction:

> **Adaptive orchestration with static deterministic profiles/guardrails**, not purely static profiles and not unconstrained LLM judgment.

## 11. External evidence — A2A supports role/capability/task interoperability, but not ADS authority

A2A Protocol v1.0 defines discoverable Agent Cards including identity, capabilities, skills, supported interfaces and security requirements; it also defines stateful Tasks, Messages and Artifacts for long-running collaboration across independent Agent systems.

Sources:

- https://a2a-protocol.org/latest/topics/key-concepts/
- https://a2a-protocol.org/dev/specification/
- https://a2a-protocol.org/dev/topics/life-of-a-task/

**Finding:** provider-neutral capability/role/task interchange is an industry-level interoperability concern. ADS should remain mappable to such transports, but A2A Task completion must not automatically become ADS Validation/Review/Release truth. ADS retains its exact-subject and authority semantics.

## 12. External evidence — scheduling should separate feasibility, choice and binding

Kubernetes Scheduling Framework separates filtering infeasible nodes, scoring feasible nodes, reservation/permit and binding. It also provides explicit extension points rather than making every policy part of one scoring function.

Sources:

- https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/
- https://kubernetes.io/docs/concepts/scheduling-eviction/scheduling-framework/

**Finding:** v4.8's hard-eligibility-before-optimization rule is externally consistent. v4.9 should preserve a similar separation:

```text
workflow/gate legality
→ role requirement
→ executor eligibility
→ optional ranking/resource policy
→ Dispatch/Claim binding
```

No optimization score may bypass authority/independence/currentness constraints.

## 13. Recurring failure evidence — fix prevention before adding more gates

#680 records an additional failure mode: materially similar defects and orchestration failures can recur across versions. Treating every recurrence as isolated tends to create repeated Builder/Validation/Review/Hidden cycles.

Recommended Product principle:

```text
repeated/materially-related failure
→ recurrence detection
→ root-cause relationship analysis
→ earliest reliable detection/prevention point
→ checker/template/schema/orchestrator-policy improvement candidate
→ ordinary ADS Product/Architecture governance
```

This must not auto-mutate the standard, and superficial textual similarity is not enough to prove common root cause.

## 14. Required Product distinctions for the Draft PRD

The PRD should make these distinctions explicit:

### 14.1 Authority vs orchestration

```text
Authority says what is required/permitted.
Orchestration selects the next legal work from live facts.
```

### 14.2 Role vs Agent

```text
Role defines responsibility/authority contract.
Agent/runtime/model is an eligible executor of that role.
```

### 14.3 Independence vs Issue count

```text
Independence is actor/session/authority separation.
A separate GitHub Issue is only one possible durable container.
```

### 14.4 Exact subject vs target movement

```text
Candidate identity change/material composition change may invalidate evidence.
Unrelated branch movement should be eligible for explicit equivalence proof rather than automatic rerun.
```

### 14.5 Concern assurance vs version release assurance

A concern needing focused Validation/Review is not automatically a reason to run full Candidate Freeze/Hidden/RQ/Version Closure. Release-significant scope remains eligible/required for the full path.

### 14.6 Learning vs authority mutation

Execution observations can create ADS improvement candidates; they do not become new Product/L2 authority by themselves.

## 15. Product risks requiring adversarial review

The Draft PRD must be attacked for at least these risks:

1. **Optimistic downgrade:** adaptive materiality classification silently reduces required assurance.
2. **Authority collapse:** Orchestrator becomes de facto Product/Review/Validation authority.
3. **Evidence laundering:** stale evidence is reused after a materially changed subject.
4. **Independence laundering:** same actor/session performs roles that higher authority requires to be independent.
5. **Container confusion:** phase coalescing in one Issue makes role terminals ambiguous.
6. **Over-standardization:** Role Profiles become rigid scripts that prevent project/domain specialization.
7. **Under-specification:** natural-language role guidance remains too vague for machine checking.
8. **Telemetry explosion:** execution learning recreates task-gate explosion as logging ceremony.
9. **Scheduler duplication:** v4.9 accidentally creates a second lifecycle beside v4.8 Dispatch/Claim.
10. **Static-profile gaming:** low-risk labels/file counts are used to down-classify semantic/high-authority changes.
11. **Strong-model single point of correctness:** all orchestration correctness depends on one LLM judgment.
12. **Hidden/release erosion:** proportional execution is misread as permission to skip release-significant gates.

## 16. Product questions intentionally deferred to L2

The following are Architecture decisions, not Product decisions:

- exact schema/event shape for an execution decision;
- whether role profiles are documents, schemas, registries or code-generated views;
- exact materiality classifier implementation;
- deterministic policy engine technology;
- exact evidence-equivalence algorithm;
- scheduler runtime/service topology;
- transport mapping to GitHub/A2A/queues/local agents;
- lease/timeout storage details beyond reuse of existing Claim semantics;
- exact recurrence fingerprint algorithm;
- exact telemetry aggregation mechanism.

## 17. L1 Product recommendation

Proceed to an adversarially reviewed Draft PRD with four integrated pillars:

```text
P1 Proportional Assurance
P2 Adaptive Orchestration
P3 Agent Operating Model
P4 Execution Learning
```

The pillars compose as:

```text
P1 determines the minimum required assurance/roles
        ↓
P2 chooses legal JIT work and eligible executor/environment
        ↓
P3 defines how the chosen role claims, executes, evidences and terminates
        ↓
P4 captures only material learning/recurrence and feeds ordinary ADS evolution
```

### Pre-Freeze disposition

```text
L1_STATUS=COMPLETE_RESEARCH
PRODUCT_DIRECTION=PROCEED
PRODUCT_FREEZE=NO
ADVERSARIAL_PRODUCT_REVIEW=REQUIRED
L2_AUTHORITY=NO
TASK_DAG_AUTHORITY=NO
IMPLEMENTATION_AUTHORITY=NO
```

The next authoritative step is Draft PRD adversarial Product Review. Findings must be durably dispositioned before Product Freeze.