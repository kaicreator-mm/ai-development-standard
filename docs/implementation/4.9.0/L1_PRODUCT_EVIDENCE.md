# v4.9.0 L1 Product Evidence — Adaptive Proportional Development Orchestration

Status: **COMPLETE RESEARCH / AUTHOR PRE-REVIEW REVISED / PRE-FREEZE — INDEPENDENT ADVERSARIAL PRODUCT REVIEW REQUIRED**

Research date: 2026-10-03

Planning baseline: `main@9383244abb8172b5ae5135cbd559c72837799375`

Planning parent: `#697`

Primary dogfood input: `#680`

Author-side adversarial pre-review: PR #698 comment `5961233246`.

This document is Product evidence only. It does not authorize Product Freeze, L2, Task DAG materialization, implementation, scheduler deployment, gate omission, evidence transfer, or weakening of existing/pinned authority.

## 1. L1 verdict

**PROCEED WITH A UNIFIED v4.9 PRODUCT CANDIDATE, WITH EXPLICIT SAFETY CORRECTIONS.**

The evidence supports one integrated Product loop:

```text
higher authority / assurance floor
        ↓
proportional legal workflow selection
        ↓
adaptive JIT orchestration
        ↓
standardized role execution
        ↓
material learning / recurrence escalation
```

The initial Draft correctly identified the problem but author-side adversarial review found six Product-level safety gaps that must be corrected before independent review:

1. dynamic reasoning needs a monotonic higher-authority `ASSURANCE_FLOOR`;
2. evidence transfer must be gate-owned and typed, not generic equivalence;
3. independence must remain multi-dimensional, not session-count based;
4. Release applicability must remain owned by current/pinned Release authority;
5. Task DAG reinterpretation must not permit runtime scope/dependency mutation;
6. ADS-self dogfood does not by itself prove downstream generality.

The revised PRD now treats those as Product invariants rather than L2 implementation details.

## 2. Internal substrate already exists

### 2.1 Development Workflow already contains proportional concepts

Current `standards/DEVELOPMENT_WORKFLOW.md` already includes:

- Version Branch vs Trunk/Fast Path;
- risk-based Review Policy;
- on-demand Architecture Research Demo;
- stage checkpoints without one Issue/branch per artifact;
- JIT Task branch / Execution Pack creation;
- GitHub Issue Dependencies as canonical live execution DAG;
- fail-closed required Validation/Review/Release truth.

**Finding:** v4.9 should operationalize proportionality; it should not invent another lifecycle merely to say “Fast Path”.

### 2.2 v4.8 already owns capability, eligibility and constraint-first assignment

Frozen v4.8 Product already separates:

```text
Capability Claim
Availability / Resource Fact
Capability Evidence
```

and uses:

```text
READY set
+ requirements/risk/freedom/environment/independence
+ capability/availability/evidence
→ hard eligibility
→ feasible executors
→ optional optimization
→ existing Dispatch / Claim
```

**Finding:** v4.9 must extend from eligible assignment to legal workflow composition and role operating semantics; v4.8 remains owner of capability/eligibility/resource-selection foundations.

### 2.3 v4.8 T-017/#646 already owns execution-start/Claim semantics

#646 establishes:

- `NO_CLAIM_NO_EXECUTION`;
- accepted Claim as durable start fact;
- operator/session/exact-subject provenance;
- visible running-state projection without using labels as locks;
- terminal ownership release;
- idempotent resume and safe timeout/stale handling;
- non-authoritative progress/heartbeat.

**Finding:** v4.9 should standardize pre-Claim, execution, evidence/handoff and terminal behavior for roles while reusing accepted Claim; it must not create another lease/lock authority.

### 2.4 Existing v4 authority already treats independence as more than session identity

v4 work has explicitly separated independence dimensions such as model/context/executor/evidence independence in high-risk review/dogfood flows. Current practice also distinguishes Builder, Validator, Reviewer, Hidden holder, Release Qualifier and Controller roles.

**Finding:** same-Issue phase coalescing may reduce containers, but a fresh session alone cannot prove every required independence dimension.

## 3. #680 dogfood evidence — orchestration amplification is real

#680 records long chains such as:

```text
Builder
→ exact-subject Validation
→ Fresh Review
→ merge
→ Stage1
→ Candidate Freeze
→ Hidden
→ Closeout
→ Release Qualification
→ Repository Integration
→ successor currentness/rebind
```

Observed costs include Issue/dispatch noise, repeated currentness work, known-sequence BLOCKED dispatches and bookkeeping sessions whose orchestration effort can dominate the actual concern.

The Product hypothesis is **not** “remove gates”. It is:

> preserve the assurance floor and every authority-bearing boundary, while avoiding execution objects/repeated work that add no new decision value.

## 4. PRACTICE-01 observations

### 4.1 Phase-separated durable work items

Fresh Closeout→RQ and Builder→independent Validation were carried as separate phases in one durable Issue while retaining distinct claims/roles/terminals.

Observed:

```text
fewer Issue containers
mandatory gate skipped = 0
independent terminal preserved = yes
exact subject preserved = yes
```

**Finding:** Issue count is not the definition of independence.

### 4.2 Controller-direct transitions

Valid terminals were consumed into expected-head merge, state reconciliation and other controller actions without creating dedicated Issues solely for deterministic coordination.

**Finding:** orchestration objects should exist for new mutable work, independent decision value, environment isolation or a separately attributable terminal—not just because a transition exists.

### 4.3 Known sequence waits

Known lineage blocks were kept as wait states instead of dispatching guaranteed `BLOCKED_SEQUENCE` work.

**Finding:** derived live readiness should control JIT dispatch.

### 4.4 Branch movement/currentness

#680 contains cases where candidate content remained unchanged while only target topology/branch state moved; repeat Review/Validation would have produced no observed new decision value.

**Finding:** a future gate-owned currentness/transfer mechanism is worth researching.

**Safety correction:** this evidence does **not** prove that disjoint paths or unchanged HEAD universally preserve Review/Validation/Hidden/Release evidence. Different evidence kinds bind to different tuples; transfer must be owned by the applicable Gate Authority.

### 4.5 Real Hidden finding still escalated

v4.6 Hidden found a release-significant P1. PRACTICE-01 did not optimize it away: thaw/invalidate, bounded repair and affected successor gates remained required.

**Finding:** adaptive orchestration must deepen assurance when new risk appears.

## 5. Product evidence for the Agent Operating Model

Current ADS already has role-specific behavior, but it is distributed. A common provider-neutral lifecycle is supported:

```text
Role
→ Eligibility
→ Dispatch
→ Claim
→ Start
→ Execution
→ Evidence / Handoff
→ Terminal
→ Ownership Release
```

The role—not ChatGPT/Claude/Codex/vendor name—should be normative.

A common Base Contract should resolve current authority, exact subject, readiness, eligibility, independence policy, Claim/start, allowed/forbidden actions, required evidence, terminal authority and handoff.

Role Profiles should express deltas such as:

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

## 6. Role distinctions supported by current practice

### Builder
Mutable work producer. It may verify its own bounded implementation assumptions but cannot mint an independent gate verdict required by higher authority.

### Reviewer
Evaluative authority against an exact subject/current authority. For required independent Review, the phase should be read-only; repairs require a separately authorized mutable phase followed by successor review as applicable.

### Validator
Executes specified test/build/runtime/environment oracles and reports executed truth; it is not the same semantic role as Reviewer.

### Controller / Orchestrator
Coordinates legal next work and authorized deterministic transitions; it does not inherit independent Review/Validation/Release authority.

### Other authority-bearing roles
Planner/Product Researcher, Architect/Architecture Researcher, Integration Agent, Hidden Validator, Release Qualifier and project/domain roles should use the same Base Contract/Profile pattern while declaring their own terminal authority/environment/independence rules.

## 7. Safety correction — monotonic assurance floor

The strongest author-side pre-review finding is that “minimal sufficient workflow” is unsafe unless bounded by positive higher authority.

Recommended Product rule:

```text
current/pinned authority
→ resolve ASSURANCE_FLOOR
→ dynamic reasoning may escalate
→ reduction allowed only through a positively authorized proportional profile
→ unknown/ambiguous predicates => stronger path or BLOCKED
```

This prevents an LLM from turning its own risk judgment into omission authority.

## 8. Safety correction — typed evidence bindings and positive transfer permission

Different evidence families can bind to different dimensions:

```text
concern Validation
integration/merge-result Validation
Review
Hidden
Closeout
Release Qualification
```

Potential binding dimensions include subject SHA/tree, base/target/merge-result identity, authority revisions, environment/toolchain/profile, independence policy, private pack revision and predecessor-gate lineage.

Recommended Product rule:

```text
Gate Authority owns binding set + transfer policy.
No positive transfer rule => historical-only.
Any unknown/changed required binding => historical-only/BLOCKED/successor assurance.
```

Path disjointness or unchanged source may be proof inputs but cannot be universal authority.

## 9. Safety correction — multi-dimensional independence

A distinct `session_ref` can prove session separation but not necessarily principal/executor, model, author/reviewer, host/environment, evidence-source or Hidden-holder independence.

Recommended Product rule: same-Issue phase coalescing is valid only when **all independence dimensions required by the owning authority** remain satisfied and attributable.

## 10. Safety correction — Release applicability ownership

The initial wording risked implying that the Orchestrator could decide that work is “not release-significant” and skip the current Release Standard.

Recommended Product rule: current/pinned Release authority owns release applicability. The Orchestrator may evaluate predicates defined by that authority, but cannot invent a lower release path. Unknown applicability is stronger-path/BLOCKED, and older pinned projects keep their older release requirements.

## 11. Safety correction — Task DAG scope boundary

JIT execution phases are supported, but Frozen Task DAG/current Task authority remains the semantic work envelope.

The Orchestrator may materialize authorized role phases/gates/containers JIT. Material new concerns, dependency changes, ownership changes or scope expansion require normal amendment/governance.

## 12. External evidence — interoperability and scheduling shape

### 12.1 A2A v1.0

A2A v1.0 defines Agent Cards with capabilities/skills/interfaces/security requirements plus stateful Tasks, Messages and Artifacts for collaboration across independent Agent systems.

Sources:

- https://a2a-protocol.org/v1.0.0/
- https://a2a-protocol.org/latest/topics/key-concepts/
- https://a2a-protocol.org/dev/specification/

**Finding:** provider-neutral capability/task interchange is a real interoperability concern. A2A Task completion must not automatically become ADS Review/Validation/Release truth.

### 12.2 Kubernetes scheduler framework

Kubernetes separates infeasible-node filtering, scoring feasible nodes, reservation/permit/pre-bind/bind stages.

Sources:

- https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/
- https://kubernetes.io/docs/reference/scheduling/config/

**Finding:** this supports v4.8/v4.9 separation of legality/eligibility, optional optimization and binding. It does not prove ADS assurance reduction.

## 13. Generality evidence boundary

Direct proportional-assurance evidence is currently strongest in `ai-development-standard` self-dogfood.

Therefore L1 records:

```text
PRODUCT_PROBLEM=SUPPORTED_IN_ADS_DOGFOOD
DOWNSTREAM_GENERALITY=PARTIAL
EXTERNAL_ARCHITECTURAL_ANALOGY=SUPPORTED
CROSS_PROJECT_GATE_REDUCTION_PROOF=NOT_YET_PROVEN
```

The correct Product response is not to block all research, nor to claim universal proof. It is to require downstream/manual GitHub-native dogfood as a v4.9 release acceptance scenario.

## 14. Bounded Execution Learning / Recurrence evidence

Repeated defect/workflow patterns can indicate a missing earlier checker/template/contract/policy rather than a need for another human gate.

v4.9 should standardize only lightweight material learning + recurrence escalation hooks:

```text
observation
→ possible recurrence
→ same / related / unknown / different root-cause relation
→ earliest prevention/detection candidate
→ ADS improvement candidate
→ normal governance
```

A universal history-mining service, autonomous root-cause engine or learning database is not justified by current evidence and should remain non-goal/future work.

## 15. Product risks still requiring independent adversarial review

Independent Review must still try to falsify at least:

1. whether `ASSURANCE_FLOOR` is sufficiently non-weakening;
2. whether positive gate-owned evidence transfer is implementable without stale-PASS laundering;
3. whether multi-dimensional independence remains machine-checkable under phase coalescing;
4. whether Release applicability remains unambiguously outside Orchestrator authority;
5. whether Task DAG scope protection is sufficient;
6. whether the four pillars are too large for one minor version;
7. whether Agent Operating Model duplicates v4.8 ownership;
8. whether P4 can remain lightweight;
9. whether downstream dogfood requirement is enough to avoid an ADS-self-only design;
10. whether backward compatibility with v4.x durable facts is credible.

## 16. L2 questions intentionally deferred

Architecture, not Product, should decide:

- exact schema/event shape for execution decisions;
- representation/storage of role profiles;
- policy engine technology;
- exact materiality/profile predicates;
- exact gate binding-set/transfer algorithms;
- scheduler/service topology;
- GitHub/A2A/queue/local transport mappings;
- recurrence fingerprint implementation;
- telemetry aggregation.

L2 may not weaken the Product invariants above.

## 17. L1 disposition

```text
L1_STATUS=COMPLETE_RESEARCH_AUTHOR_PRE_REVIEW_REVISED
PRODUCT_DIRECTION=PROCEED
PRODUCT_PROBLEM=SUPPORTED
DOWNSTREAM_GENERALITY=PARTIAL
ASSURANCE_FLOOR_REQUIRED=YES
EVIDENCE_TRANSFER=GATE_OWNED_POSITIVE_PERMISSION_ONLY
INDEPENDENCE=MULTI_DIMENSIONAL
RELEASE_APPLICABILITY_OWNER=CURRENT_PINNED_RELEASE_AUTHORITY
TASK_DAG_RUNTIME_SCOPE_WIDENING=FORBIDDEN
P4_SCOPE=LIGHTWEIGHT_LEARNING_AND_ESCALATION
PRODUCT_FREEZE=NO
INDEPENDENT_ADVERSARIAL_PRODUCT_REVIEW=REQUIRED
L2_AUTHORITY=NO
TASK_DAG_AUTHORITY=NO
IMPLEMENTATION_AUTHORITY=NO
```

The next authoritative step is a genuinely independent adversarial Product Review on the successor exact PR candidate. Author-side pre-review is not independent Product Review evidence.
