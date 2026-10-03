# ai-development-standard v4.9.0 PRD — Adaptive Proportional Development Orchestration

Status: **CLAUDE-FINDINGS REVISED CANDIDATE — NOT FROZEN; FRESH SUCCESSOR PRODUCT REVIEW REQUIRED**

PRD revision: `v0.4`

Planning baseline: `main@9383244abb8172b5ae5135cbd559c72837799375`

Planning parent: `#697`

Primary planning/dogfood input: `#680`

Claude adversarial review: `#702@5966353271` on PRD v0.3 / PR #698 HEAD `0c9b352c106f0068cec2f15baab96b4add724ff4`, tree `f5c20c25422f9f28284e2c59f583b7c98ead3c27`, verdict `FAIL`, findings `P0=0/P1=3/P2=6/P3=3`.

v4.8 predecessor Product authority reused by v4.9:

```text
V48_FROZEN_PRD_BLOB=f26439580e00de6ed8b2e27d732a3095eb566219
V48_FROZEN_L2_BLOB=f88c85454e80101a0fdf56050e21f11a05279841
```

This document supersedes PRD v0.3 as the current Product candidate. It is **not** Frozen Product Authority. It does not authorize L2, Task DAG materialization, implementation, scheduler deployment, schema migration, gate omission, evidence transfer, Product Freeze, merge or Release Qualification.

## 1. Product intent

v4.9.0 makes ADS execution more proportional, adaptive and role-consistent while preserving fail-closed authority.

The Product goal is:

> Given live durable project facts and current/pinned authority, ADS can select the **minimal sufficient legal workflow at or above a monotonic assurance floor**, identify the roles actually required, select an eligible Agent/environment for each role, standardize claim/execution/evidence/handoff/terminal behavior, reuse prior evidence only under gate-owned positive transfer rules, and feed material execution learning into the existing v4.8 learning/evolution path — without allowing model judgment, orchestration convenience, migration or evidence reuse to weaken authority.

v4.9 builds on existing ADS Product/Architecture/Task/Execution/Dispatch-Claim/Review/Validation/Release semantics and on the frozen v4.8 capability/scheduling/learning/evolution substrate. It does not create parallel authority lifecycles.

## 2. Product problem and evidence boundary

### 2.1 Orchestration amplification is real

v4.x dogfood in #680 shows small and medium concerns expanding into chains of Builder, Validation, Fresh Review, merge, Stage1, Candidate Freeze, Hidden, Closeout, Release Qualification, integration and successor currentness/rebind work.

These gates are valuable when they protect a material authority or risk boundary. They are waste when duplicated containers, handoffs or repeated gates add no new decision value.

### 2.2 Existing proportional mechanisms are not operationally complete

ADS already has Fast Path, risk-based Review Policy, on-demand architecture demos, JIT Task admission and derived READY queues. The missing Product contract is how to select the smallest **authorized** workflow from live facts without optimistic downgrade, stale-PASS transfer, independence laundering, adverse-verdict suppression or scope widening.

### 2.3 Runtime decisions cannot all be pre-expanded

Readiness, currentness, evidence transferability, environment availability, bounded repair, sequence waits and recurrence signals depend on live facts. Pre-materializing every possible execution phase creates stale work and guaranteed-BLOCKED dispatches.

### 2.4 Role behavior is distributed across standards

Builder, Reviewer, Validator, Controller, Hidden Validator, Release Qualifier and specialized roles exist, but their common operating contract is distributed across workflow, interaction, execution, review, validation and release standards.

### 2.5 Direct evidence and quantification gap

The strongest direct evidence is ADS self-dogfood in #680. It establishes the existence and shape of orchestration amplification and includes examples where high-assurance gates found real problems, but the current L1 corpus does **not** yet provide a complete quantified baseline separating useful decision-value from ceremony across a representative sample.

Therefore:

```text
ORCHESTRATION_AMPLIFICATION=SUPPORTED_QUALITATIVELY
AMPLIFICATION_QUANTIFICATION=PARTIAL
GENERALITY_EVIDENCE=PARTIAL
STANDARD_SELF_EXCEPTION_ALLOWED=NO
DOWNSTREAM_DOGFOOD_REQUIRED_BEFORE_RELEASE=YES
```

No numeric savings claim is authorized at Product Freeze. The missing baseline measurements must be collected through the downstream dogfood contract in §16 rather than invented retrospectively.

### 2.6 v4.8 predecessor authority and lineage

v4.9 reuses frozen v4.8 Product/L2 authority for capability evidence, Agent eligibility/resource selection, Dispatch/Claim execution ownership, Task Learning Evidence and ADS Evolution Intake.

The reused predecessor is bound to:

```text
V48_FROZEN_PRD_BLOB=f26439580e00de6ed8b2e27d732a3095eb566219
V48_FROZEN_L2_BLOB=f88c85454e80101a0fdf56050e21f11a05279841
```

If either owning v4.8 authority is thawed, amended or superseded before v4.9 L2/Release, v4.9 MUST perform a currentness re-evaluation before relying on it.

v4.9 Release Qualification MUST NOT complete before the required v4.8 predecessor is integrated into the release lineage applicable to v4.9.

## 3. Product shape and ownership

v4.9 defines four integrated pillars:

1. **P1 — Proportional Assurance**
2. **P2 — Adaptive Orchestration**
3. **P3 — Agent Operating Model**
4. **P4 — Execution Learning & Recurrence Escalation**

They compose as:

```text
current/pinned owners + durable facts
        ↓
P1 resolves a monotonic assurance floor and legal proportional profile
        ↓
P2 selects legal JIT work and an eligible executor/environment
        ↓
P3 governs claim, execution, evidence, handoff and terminal behavior
        ↓
P4 extends v4.8 Task Learning / ADS Evolution with bounded execution-friction evidence
```

Cross-cutting invariants:

- fail-closed authority;
- no self-minted independent PASS;
- no model-only proof for a reduction predicate;
- typed gate-owned evidence currentness/transfer;
- multi-dimensional independence;
- adverse findings cannot be shopped around or silently superseded;
- v4.8 Dispatch/Claim and Task Learning/Evolution ownership preserved;
- manual/GitHub-native execution remains possible.

## 4. Authority precedence and monotonic assurance floor

### 4.1 Applicable authority owners

Before proportional workflow selection, the system MUST resolve all applicable current/pinned authority owners, including as relevant:

```text
Frozen Product / Scope
Frozen Architecture / Contract
Task / Task Pack / Execution Pack
PROJECT_OVERRIDES allowed by higher authority
Review Policy / Review authority
Validation authority/profile
Release authority/applicability
security / ownership / independence constraints
```

### 4.2 Per-owner reduction permission

A requirement may be reduced only when the authority that **owns that requirement** positively defines the selectable lower profile/condition.

For each owner-scoped reduction:

1. every predicate required by that owner's permission MUST be established by current durable facts or a deterministic check accepted by that owner;
2. model reasoning MAY propose or interpret a candidate classification, but model judgment alone MUST NOT be the proof that authorizes reduction;
3. an unproven, stale, contradictory or ambiguous predicate/classification MUST choose the stronger currently legal path or return `BLOCKED`;
4. absence of prohibition is not positive permission.

```text
NO_POSITIVE_OWNER_PERMISSION => NO_REDUCTION_FOR_THAT_OWNER
UNPROVEN_OR_AMBIGUOUS_PREDICATE => STRONGER_PATH_OR_BLOCKED
MODEL_JUDGMENT_ONLY => NOT_SUFFICIENT_FOR_REDUCTION
```

### 4.3 Multi-owner composition

The resolved `ASSURANCE_FLOOR` MUST be the **monotonic conjunction / least-permissive composition of all concurrently applicable owner requirements**.

- an authority may relax only requirements it owns;
- one owner's permission MUST NOT cancel another owner's concurrently applicable requirement;
- when applicable owners impose different minimum requirements, the stronger compatible requirement wins;
- when owner applicability, ownership or cross-owner compatibility is unknown, the system MUST choose the stronger currently legal path or return `BLOCKED`.

```text
ASSURANCE_FLOOR = CONJUNCTION(APPLICABLE_OWNER_REQUIREMENTS)
CROSS_OWNER_CONFLICT_OR_UNKNOWN => STRONGER_PATH_OR_BLOCKED
```

The Orchestrator may escalate above the floor when new risk/evidence requires it. It MUST NOT reduce below the floor for cost, speed, file count, provider/model confidence, `docs-only` labeling or convenience.

### 4.4 Authority vs orchestration

```text
Authority defines what is required/permitted and who owns the decision.
Orchestration selects the next legal action from current facts inside that authority.
```

Reasoning quality does not create authority.

## 5. P1 — Proportional Assurance

### 5.1 Product requirement

ADS MUST support proportional assurance profiles or equivalent policy so a concern is not automatically expanded to maximum ceremony when **all applicable owners and proven predicates** permit a smaller path.

Candidate materiality dimensions include:

```text
semantic impact
machine-contract/schema impact
lifecycle/state impact
authority/gate ownership impact
security/data-integrity impact
migration/compatibility impact
runtime composition impact
release applicability
current evidence/currentness
```

No single label, file count, model identity or `docs-only` tag is sufficient authority.

### 5.2 Required resolution

Before authoritative dispatch/merge/release transitions, the system must resolve as applicable:

```text
applicable authority owners
owner-scoped reduction predicates + proof refs
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

Current/pinned Release authority remains the owner of release applicability. The Orchestrator cannot independently classify a candidate out of mandatory release gates.

v4.9 Product scope **does include** defining prospective proportional release-applicability predicates owned by `RELEASE_STANDARD.md`, so that concern-level changes can avoid unrelated release ceremony where Release authority positively permits it. L2/implementation may encode those predicates only inside these Product constraints:

- positive Release-authority permission is required;
- predicates require durable/deterministic proof under §4.2;
- unknown/ambiguous release predicates fail closed;
- migration/proportional policy is prospective only under §17;
- no already-required gate for an in-flight Frozen/qualified candidate may be removed retroactively.

Until such Release-owned predicates are Frozen and applicable, existing mandatory Version Closure, Candidate Freeze, Hidden, Fresh Closeout and Release Qualification requirements remain unchanged.

### 5.4 Fast Path

Fast Path may be genuinely smaller only where the composed floor and proven owner predicates permit it. It preserves current authority discovery, required Review/Validation truth, Claim/start ownership, exact-subject evidence and escalation when risk grows.

## 6. P2 — Adaptive Orchestration

### 6.1 Product requirement

ADS SHOULD support a high-capability orchestration control plane that reads live durable facts and selects the next legal work JIT instead of requiring every possible phase to be pre-materialized.

Candidate responsibilities:

```text
read live DAG / Issues / PRs / refs / Claims / terminals / evidence
compute actually-ready work
resolve owners + proven predicates + ASSURANCE_FLOOR
propose materiality classifications inside authorized policy
resolve required roles/gates
choose eligible Agent/model/environment
control JIT admission/concurrency
avoid duplicate or knowingly blocked dispatch
consume all authoritative terminals/findings
choose authorized bounded repair vs escalation
request gate-owned evidence-transfer proof
record compact decision/learning evidence
```

### 6.2 Deterministic guardrails

Architecture MUST preserve separation equivalent to:

```text
High-capability reasoning
  → ambiguity, decomposition, prioritization, recovery trade-offs

Deterministic policy/contract enforcement
  → owner composition, predicate proof, assurance floor, mandatory gates,
    illegal transitions, finding dominance, independence, evidence bindings

Durable fact plane
  → GitHub/repository/evidence/current operation facts
```

### 6.3 Orchestrator hard boundaries

The Orchestrator MUST NOT:

- mint required independent Review/Validation/Hidden/RQ PASS;
- use model reasoning as sole proof for a reduction predicate;
- reduce below the composed `ASSURANCE_FLOOR`;
- let one owner's permission cancel another owner's requirement;
- silently waive Frozen Product/L2/Task/Release requirements;
- invent evidence-transfer authority;
- treat private chat memory as canonical state;
- hide `FAIL`, findings, `BLOCKED`, `NOT_RUN`, `NOT_APPLICABLE`, stale or unknown truth;
- supersede, ignore or re-dispatch around an adverse independent terminal merely to obtain a PASS;
- shop among reviewers/validators after an adverse terminal without an owning-authority disposition or a successor subject;
- bypass existing Dispatch/Claim admission;
- make cost/latency/availability override hard eligibility;
- mutate ADS automatically from project learning.

Existing finding-union, blocker-dominance and unresolved-finding semantics remain binding. A re-review after FAIL requires either:

```text
successor subject after authorized repair
OR
owning-authority finding disposition that explicitly authorizes re-review
```

### 6.4 Task DAG boundary

The Frozen Task DAG/current Task authority remains the semantic work envelope.

Adaptive orchestration MAY JIT materialize authorized execution phases, role handoffs, gates and durable containers inside that envelope.

It MUST NOT invent a material new implementation concern, change dependency/ownership semantics or widen Frozen scope. Whether a proposed addition is within the envelope is itself an authority-sensitive classification and is subject to §4.2 proof/fail-closed rules.

### 6.5 Non-dispatch wait states

When work is deterministically not ready, orchestration SHOULD preserve a durable wait state such as `WAITING_LINEAGE` or equivalent rather than dispatch work whose only legal result is a known sequence block.

### 6.6 Controller transitions remain authority-bearing

Controller-direct execution can avoid unnecessary Issues, but merge, Candidate Freeze, thaw/invalidate, release integration and similar transitions remain authority-bearing and may occur only after their owning authority and exact prerequisites are satisfied.

## 7. P3 — Agent Operating Model

### 7.1 Role, not vendor/model, is normative

ADS MUST define a provider-neutral **Agent Execution Base Contract** plus role-specific **Role Profiles**.

Provider/model identity is provenance/capability evidence, not authority by itself.

### 7.2 Base lifecycle and v4.8 ownership

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

v4.9 reuses the v4.8 capability/eligibility/resource-selection and Dispatch/Claim execution-ownership model bound in §2.6. v4.9 MUST NOT create a second task, lease, lock, scheduler-ownership or claim lifecycle.

### 7.3 Common pre-Claim requirements

Before authoritative execution, the applicable contract establishes as needed:

```text
work remains READY/current
dependencies satisfied
role matches dispatch
required capability/tools/environment available
required independence policy satisfied
selector/executor conflict policy satisfied
no incompatible accepted active Claim
current authority refs read
exact subject/base/target resolved
allowed scope/write set resolved
forbidden scope/actions resolved
required evidence + terminal authority resolved
```

No accepted Claim where Claim is required means no authoritative execution.

### 7.4 Common execution requirements

An Agent must remain inside owned authority, re-check live facts on material drift, surface blockers/deviations, preserve exact-subject truth, avoid silently widening scope, and record only material evidence/learning required by policy.

Private chain-of-thought is never required.

### 7.5 Common terminal requirements

A terminal is durably attributable to the applicable:

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

Builder owns authorized mutable implementation/work-product production. It cannot begin required authoritative mutation before accepted Claim/start and cannot self-approve an independent gate.

Builder MUST:

- consume Frozen/current authority and exact execution subject;
- stay inside the owned concern/write set and sibling boundaries;
- implement required source/tests/fixtures/docs/checks within scope;
- record material deviations/blockers/new authority gaps;
- stop when Product/L2/Task authority is insufficient;
- emit an exact output/handoff terminal.

### 8.2 Reviewer

Reviewer owns an evaluative verdict against the exact review subject and current authority. Required independent Review is read-only with respect to its subject. Repair requires a separately authorized mutable phase/role followed by successor Review when required.

Reviewer MUST inspect the actual subject and evidence, verify scope/currentness/authority/forbidden behavior as applicable, emit severity findings and preserve required independence dimensions.

### 8.3 Validator

Validator owns executed truth for specified tests/build/runtime/host/environment/scenario oracles. It distinguishes executed from inferred/not-run evidence and preserves exact-subject/environment/profile bindings.

Reviewer and Validator remain different semantic roles even when phases share one durable Issue.

### 8.4 Controller / Orchestrator

Controller/Orchestrator owns authorized workflow coordination: READY recomputation, JIT dispatch/materialization, eligible executor selection, terminal consumption, authorized deterministic transitions, waits and escalation. It cannot substitute for an independent verdict, ignore an adverse terminal or invent evidence.

### 8.5 Other authority-bearing roles

Planner/Product Researcher, Architect/Architecture Researcher, Integration Agent, Hidden Validator, Release Qualifier and specialized roles, **when standardized or used by the applicable project**, MUST be expressible through the same Base Contract and declare terminal authority, mutation/read-only class, required environment and independence policy.

Product does not require identical lifecycle depth for all roles. Detailed role-specific schemas/commands belong to L2/Task implementation where the role is in scope.

## 9. Independence semantics

### 9.1 Independence is multi-dimensional

A different Issue or session is not sufficient proof of independence. v4.9 MUST preserve the existing ADS distinction among independence dimensions rather than collapse them into `session_ref` or container count.

Applicable authority may require one or more dimensions:

```text
principal / logical executor independence
session/context independence
model/provider/configuration diversity
Builder-vs-Reviewer author conflict separation
Validator environment/host independence
evidence-source independence
Hidden-holder/private-evaluator separation
Release/Controller role separation
executor-selector conflict separation when selector authored/materially controlled the subject
```

### 9.2 Phase-separated durable work item

One durable work item MAY carry multiple sequential phases only when:

- current authority permits phase coalescing;
- each phase has an unambiguous role/dispatch/claim/current subject;
- every applicable independence dimension is satisfied;
- previous terminal evidence remains immutable/history-preserving;
- the phase transition is explicit;
- a mutable actor cannot self-approve a required independent phase.

A separate Issue remains required when environment, confidentiality, write isolation or authority requires a distinct durable container.

## 10. Typed evidence currentness and transfer

### 10.1 Evidence binds to a declared tuple

Different evidence families bind to different dimensions. Examples:

```text
concern Validation      → subject + profile + environment/toolchain + authority refs
integration Validation  → source + target/base + composed result + profile/environment
Review                  → subject/diff + current authority + independence policy
Hidden                  → exact candidate + private pack/revision + holder policy
Closeout/RQ             → frozen candidate + predecessor gate bindings + release authority
```

Exact binding sets are owned by the applicable Gate Authority and MUST be frozen in L2/implementation before generic orchestration can evaluate transfer for that family.

### 10.2 Positive transfer permission

Prior evidence is current only if all are true:

1. the owning Gate Authority positively declares the evidence family transferable under stated predicates;
2. every required binding dimension is equal or proven equivalent;
3. no explicitly non-transferable dimension changed;
4. no current-target/current-authority rule requires fresh execution;
5. the equivalence proof itself is durable/current.

```text
NO_TRANSFER_RULE => HISTORICAL_ONLY
UNKNOWN_BINDING => HISTORICAL_ONLY_OR_BLOCKED
MATERIAL_BINDING_CHANGE => SUCCESSOR_ASSURANCE_REQUIRED
```

Path disjointness, unchanged HEAD/tree or ancestor topology may be proof inputs but are never universal transfer authority.

### 10.3 Fresh-only / non-transferable evidence

A Gate Authority may declare evidence fresh-only or non-transferable even when structural identity appears equivalent. v4.9 cannot override that declaration through generic equivalence reasoning.

## 11. Gate/container coalescing

Execution containers and bookkeeping MAY be coalesced where current authority permits; authority itself cannot be coalesced merely to reduce count.

A coalesced work item keeps role, principal/session, exact subject, terminal, independence and phase history machine-distinguishable.

## 12. Scheduling / Agent selection

v4.9 reuses the v4.8 capability, availability, eligibility, resource-selection and Dispatch/Claim substrate bound in §2.6.

Conceptually:

```text
legal workflow at/above ASSURANCE_FLOOR
→ required role
→ hard executor eligibility
   capability + tools/environment + authority/freedom
   + independence + selector-conflict + security/access
   + current availability/resource
→ feasible executor set
→ optional project optimization
→ Dispatch
→ existing Claim admission
```

Provider/model name alone does not grant eligibility or authority. If no eligible executor exists, work waits/BLOCKED/escalates; the scheduler cannot use an ineligible fallback.

## 13. P4 — Execution Learning & Recurrence Escalation

### 13.1 Ownership: extend v4.8, do not duplicate it

P4 reuses and extends the frozen v4.8 ownership families:

```text
Task Learning Evidence v1
TASK_LEARNING=NONE_MATERIAL
ADS_EVOLUTION_CANDIDATE
existing ADS Evolution Intake / ordinary L1→PRD→L2→Task governance
```

v4.9 MUST NOT create a parallel learning record family, parallel evolution-intake lifecycle or second authority path.

### 13.2 v4.9 Product delta

The v4.9 delta is limited to:

- execution-friction categories that may be represented as backward-compatible extensions/mappings of v4.8 Task Learning Evidence;
- a bounded recurrence-audit escalation hook that helps distinguish `same root cause | related root cause | unknown relation | different/superficial similarity`;
- explicit linkage from recurring execution friction to the existing `ADS_EVOLUTION_CANDIDATE` path.

Candidate friction categories include:

```text
workflow_waste
missing_contract
execution_ambiguity
repeated_failure_mode
useful_pattern
bad_pattern
```

Simple work may continue to record `NONE_MATERIAL` under the v4.8 owner.

### 13.3 Bounded recurrence audit

The Controller/Orchestrator or owning workflow authority may request a recurrence audit when durable evidence indicates materially related recurrence.

The audit seeks the earliest reliable prevention/detection point, such as Task Pack/L3/template, schema/contract, deterministic checker, policy rule, orchestration rule or Product/Architecture gap.

Its output is evidence for existing Evolution Intake, not automatic authority mutation.

### 13.4 P4 non-goals

v4.9 does not authorize:

- automated cross-project mining;
- universal recurrence fingerprinting;
- a dedicated learning database;
- an autonomous cross-project root-cause analytics platform;
- a parallel Task Learning/Evolution record family or intake path.

Any such expansion requires separate Product authority.

## 14. Durable execution decision

v4.9 requires enough auditability to explain workflow/Agent/gate choices without storing chain-of-thought.

A compact record should reference as applicable:

```text
subject/current durable state
applicable owners + ASSURANCE_FLOOR
reduction predicates + durable/deterministic proof refs
selected authorized profile/roles
selected Agent/environment + eligibility evidence
gates required/coalesced/reused/not-applicable
transfer/currentness proof refs
wait/dependency/concurrency decision
adverse terminal/finding disposition refs
unexpected blocker/escalation
outcome
```

Exact schema/storage is L2.

## 15. Required Product acceptance scenarios

Implementation/release evidence must eventually prove at least:

### A. Low-risk semantic-neutral maintenance
An authorized lower profile completes with bounded gates only after its owner predicates are proven by durable/deterministic evidence.

### B. Bounded normative semantic change
Focused Review/Validation is selected according to current authority without unrelated release ceremony only where prospective Release-owned applicability predicates positively permit that path.

### C. Machine-contract/high-risk change
Schema/lifecycle/authority changes cannot be down-classified by file count, labels or model judgment.

### D. Release-significant/currently release-governed change
The full required Closure/Freeze/Hidden/Closeout/RQ path remains required when current Release authority says so.

### E. Same durable container, multiple independent phases
Distinct phases share one Issue only while all applicable independence dimensions and terminals remain distinguishable.

### F. Duplicate Claim race
Only the accepted Claim starts authoritative incompatible work.

### G. Wrong-role / independence rejection
An otherwise capable Agent is ineligible when required independence or selector-conflict policy conflicts.

### H. Gate-specific evidence transfer
Target movement reuses evidence only under a positive gate-owned transfer rule and complete binding equivalence.

### I. Material/unknown binding drift
Changed or unknown contract/authority/composition/environment binding makes affected evidence historical-only or blocks until successor assurance.

### J. Hidden/release high-risk finding
A real release finding triggers required thaw/repair/requalification rather than proportional optimization.

### K. Known sequence block
Work stays in a non-dispatch wait state instead of creating a guaranteed-BLOCKED task.

### L. Task-DAG scope protection
Adaptive orchestration cannot invent new semantic implementation work/dependencies outside Frozen Task authority.

### M. Single-owner ambiguous reduction predicate
One known owner positively permits reduction only when predicate `P` holds; when `P` is ambiguous/unproven, model reasoning cannot authorize reduction and the result is stronger path or `BLOCKED`.

### N. Adverse Review cannot be shopped around
Reviewer R1 returns a blocking finding; orchestration cannot discard it and seek R2 PASS. Re-review occurs only after successor subject or owning-authority disposition.

### O. Prospective migration
A project may migrate authority prospectively through owning governance, but an in-flight Frozen/qualified candidate retains gates already required under its bound authority.

### P. Downstream manual/GitHub-native dogfood
A qualifying downstream project meets the non-vacuous auditable contract in §16 and proves at least one authorized proportional delta without unauthorized gate omission, stale-PASS transfer or independence loss.

### Q. Recurring failure
A materially related recurrence produces a bounded v4.8-compatible Task Learning / `ADS_EVOLUTION_CANDIDATE` output without creating a parallel learning lifecycle.

## 16. Downstream dogfood and measurement contract

### 16.1 Purpose

Downstream dogfood is required before v4.9 Release Qualification can claim downstream generality. It is not required to establish Product problem existence, and it does not require a universal numeric ROI threshold.

### 16.2 Qualifying downstream project

A qualifying downstream project MUST be a distinct product/repository with its own pinned Product/Architecture/Task/Review/Validation/Release authority artifacts. It MUST NOT be:

- the `ai-development-standard` repository itself;
- a mirror or synthetic copy of ADS governance whose only purpose is to satisfy the test;
- a run whose authority baseline is not durably inspectable.

### 16.3 Exact-candidate binding

Dogfood evidence MUST bind to the exact v4.9 candidate/revision or released ADS version whose semantics it exercises. Candidate drift is handled by the applicable evidence-currentness rules in §10.

### 16.4 Baseline and selected execution

The evidence must record, before interpreting success:

```text
project + pinned authority refs
baseline legal workflow/gate contract
selected proportional workflow
mechanisms exercised
execution containers/issues
role dispatches/claims
independent gates/sessions
rebind/revalidation events
decision-value account for omitted/coalesced/reused steps
```

The baseline is the legal workflow under the project's bound authority without the tested v4.9 proportional decision, not an invented maximum ceremony strawman.

### 16.5 Mechanism exercise matrix

For every mechanism for which Release claims downstream generality, evidence records `EXERCISED | NOT_EXERCISED` and a proof reference:

```text
owner-permitted reduction
cross-owner floor composition
same-container phase coalescing
gate-owned evidence transfer
fail-closed unknown/ambiguous predicate
non-dispatch wait
prospective release-applicability selection, if claimed
```

`NOT_EXERCISED` is truthful evidence but cannot support a generality claim for that mechanism.

At least one observed or deliberately induced unknown/ambiguous reduction-predicate case MUST be exercised and shown to take stronger path or `BLOCKED`.

### 16.6 Non-vacuity / positive proportional outcome

To satisfy downstream generality, at least one authorized reduction, coalescing, reuse or avoided known-blocked dispatch MUST produce a **nonzero baseline-vs-selected delta** while all required authority remains preserved.

If baseline and selected workflows are identical and no proportional mechanism materially changes execution, the run is useful compatibility evidence but:

```text
DOWNSTREAM_GENERALITY=NOT_SATISFIED
```

No minimum percentage or economic threshold is Frozen at Product level.

### 16.7 Independent safety audit

The safety-negative account MUST be checked by an executor satisfying the applicable independent evidence-source policy and not acting as the orchestrating or Builder principal for the tested decisions.

The audit must establish from durable baseline/terminal evidence:

```text
UNAUTHORIZED_GATE_OMISSION=0
STALE_PASS_TRANSFER=0
INDEPENDENCE_LOSS=0
CROSS_OWNER_REQUIREMENT_CANCELLATION=0
ADVERSE_TERMINAL_SUPPRESSION=0
```

Self-attestation by the orchestrator/Builder is insufficient for Release generality evidence.

### 16.8 Manual/GitHub-native viability

At least one qualifying run MUST remain executable through manual/GitHub-native interaction without requiring a scheduler daemon or proprietary transport.

### 16.9 Claim boundary

Release claims of downstream generality MUST enumerate exactly which mechanisms were exercised and supported. A run exercising only one mechanism cannot imply generality for unexercised mechanisms.

### 16.10 Quantification use

The §16 baseline also supplies the currently missing #680 quantification evidence: execution objects, dispatches, gates, rebinds/revalidations and decision-value accounting. These measurements may support later descriptive claims but do not retroactively alter Product authority.

## 17. Compatibility and migration

- Existing v4.x durable records remain historical truth.
- Existing v4.8 Dispatch/Claim and Task Learning/Evolution semantics remain the ownership foundation until explicitly superseded by higher authority.
- v4.9 does not retroactively invalidate full-chain execution because a future proportional path would be shorter.
- Projects pinned to older ADS authority retain that authority unless the project's owning authority explicitly migrates through normal governance.
- Migration is **prospective only**.
- Migration MUST NOT remove or shorten gates already required for an in-flight Frozen, qualified or otherwise authority-bound candidate.
- New metadata should prefer backward-compatible writer/profile extensions.
- Manual GitHub-native execution remains supported; no scheduler daemon is mandatory.
- External A2A/queue/local transport completion never automatically becomes ADS Review/Validation/Release truth.

## 18. Security and privacy

v4.9 MUST NOT require secrets, credentials, private chain-of-thought, private Hidden fixture/oracle contents or unnecessary personal identity.

Only provenance needed for accountability/independence should be retained. Tool availability does not grant mutation authority. Capability does not grant Review/Validation/Release authority.

## 19. Non-goals

v4.9 does not require or authorize:

- a universal scheduler daemon;
- replacement of GitHub as reference durable fact plane;
- a second Dispatch/Claim/task lifecycle;
- autonomous risk downgrade below higher authority;
- model-only proof of reduction predicates;
- generic evidence reuse from path disjointness or unchanged HEAD alone;
- one-session-equals-independent semantics;
- automatic ADS mutation from project learning;
- automated cross-project learning mining;
- universal recurrence fingerprinting;
- a dedicated learning database;
- an autonomous cross-project root-cause analytics platform;
- a parallel Task Learning/Evolution family or intake path;
- a universal Agent quality score;
- provider/model-specific normative procedures;
- blanket low-cost routing;
- blanket removal of independent Review/Validation;
- full release ceremony for concerns to which current Release authority positively declares non-applicability;
- retrospective shortening of gates for in-flight Frozen/qualified candidates;
- disclosure of private chain-of-thought;
- a special easier rule only for `ai-development-standard`.

## 20. Product Freeze preconditions

PRD v0.4 MUST NOT freeze until a **fresh independent Product Review bound to the exact v0.4 candidate** verifies/dispositions at least:

1. F1 per-owner predicate proof and fail-closed ambiguity;
2. F2 non-vacuous auditable downstream dogfood;
3. F3 v4.8 Task Learning/Evolution ownership preservation;
4. multi-owner assurance-floor monotonicity;
5. prospective Release-applicability ownership and migration protection;
6. adverse-terminal/finding dominance and anti-review-shopping behavior;
7. Task-DAG semantic scope protection;
8. v4.8 capability/resource/Dispatch/Claim predecessor ownership and exact authority bindings;
9. Role Profile scope and multi-dimensional independence;
10. gate-owned typed evidence transfer/currentness;
11. full Hidden/Closeout/RQ preservation where current authority requires it;
12. historical PRD revision immutability;
13. four-pillar coherence and version size;
14. complete v0.3→v0.4 diff accounting for no semantic regression or unreviewed Product scope expansion.

### 20.1 Successor-review discipline

Any material post-review Product revision invalidates the prior exact-candidate Freeze recommendation for the successor content.

The successor must receive either:

- a full independent Product Review; or
- a bounded independent review whose declared scope covers the **complete predecessor→successor diff**, not only named findings, with diff-level evidence supporting `NO_PRODUCT_REGRESSION` and `NO_UNREVIEWED_SCOPE_EXPANSION`.

Controller disposition alone cannot satisfy this Freeze precondition.

#701 remains historical evidence for its exact v0.3 bounded review but is not sufficient evidence that v0.3 had no regression after #702 falsified that conclusion.

## 21. Product acceptance criteria for Freeze

Product Freeze requires a current exact-candidate independent review showing:

```text
ASSURANCE_FLOOR is monotonic across all applicable owners
owner reduction predicates require durable/deterministic proof
unknown/ambiguous predicates choose stronger path or BLOCKED
adaptive reasoning cannot mint reduction authority
release applicability remains Release-authority owned and prospective
migration cannot shorten in-flight bound candidate gates
adverse findings cannot be suppressed or reviewer-shopped
P1/P2/P3/P4 remain one coherent execution loop
v4.8 capability/Dispatch/Claim ownership is preserved by exact predecessor refs
v4.8 Task Learning/Evolution ownership is reused rather than duplicated
Task DAG scope cannot be widened by runtime orchestration
independence is multi-dimensional and selector conflicts are representable
Evidence transfer is gate-owned, typed and fail-closed
manual/GitHub-native execution remains possible
downstream dogfood is non-vacuous, auditable and candidate-bound before Release
L2 choices remain open where Product has not fixed them
```

## 22. Revision and review discipline

- `PRD.md` is the current Product candidate only.
- Every material Product revision is preserved byte-for-byte under `prd-history/`.
- Review terminals remain bound to the exact PRD revision/blob/HEAD/tree they reviewed.
- Findings are dispositioned in successor artifacts; historical review evidence is never rewritten to appear current.
- A PASS on predecessor content does not transfer automatically to successor content.

## 23. Current gate

```text
VERSION=v4.9.0
PRD_REVISION=v0.4
PRD_STATUS=CLAUDE_FINDINGS_REVISED_CANDIDATE
PRODUCT_AUTHORITY=DRAFT_ONLY
PRODUCT_FREEZE=NO
CLAUDE_REVIEW=#702@5966353271 FAIL_ON_V03
CLAUDE_FINDING_DISPOSITION=#706
FRESH_V04_PRODUCT_REVIEW=REQUIRED
L2_AUTHORITY=NO
TASK_DAG_AUTHORITY=NO
IMPLEMENTATION_AUTHORITY=NO
```

The next authoritative step is a fresh independent Product Review bound to the exact v0.4 candidate and covering the complete v0.3→v0.4 diff.