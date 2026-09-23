# v4.0 Operation Assurance Plan

Status: CANDIDATE — T-003 / Issue #75
Version: 4.0.0
Baseline: `version/v4.0.0@638e0bedb3ce8ab50ae045b3f7cb29a3f179e2f8`
Parent authority: `ARCHITECTURE_DECISION.md` + `OPERATION_CONTRACT.md`

## 1. Purpose

Operation Assurance is the mechanism by which a material Operation is challenged and validated before acceptance. It is part of the parent Operation contract, not a second lifecycle, not a second source of workflow state, and not a replacement for `VALIDATION_STANDARD.md` or `GITHUB_AGENT_INTERACTION_PROTOCOL.md`.

Core rule:

```text
Assurance selects and orders required evidence/challenge work.
Owning standards still define what each evidence result means.
```

An Assurance Plan may be trivial, linear, or a DAG/partial order. v4 does not impose a universal `Challenge -> Validate` sequence.

## 2. Five separate assurance dimensions

Every material Assurance Plan resolves these dimensions independently:

```text
Policy        — whether an assurance activity is required/recommended/not-required
Mode          — how the activity is performed
Coverage      — what dimensions/claims are being checked
Independence  — which independence controls are required and satisfied
Aggregation   — how multiple results/findings are combined and conflicts resolved
```

They MUST NOT be collapsed into one field such as `review_level` because doing so hides materially different guarantees.

### 2.1 Policy

Canonical requirement values:

```text
required
recommended
not-required
```

For Review this preserves the v3.4 Review Policy exactly. Other assurance activities MAY define equivalent requirement semantics under their owning authority, but must not invent PASS for work not executed.

### 2.2 Mode

Mode identifies execution form, for example:

```text
single-independent
cross-peer
specialist
model-diverse-adversarial
executable-validation
hidden-validation
coherence-review
human-authority-review
```

Mode is descriptive routing/configuration. It does not by itself prove independence or PASS.

### 2.3 Coverage

Coverage is an explicit set of required review/validation dimensions or claims, for example:

```text
contract
architecture
authority-boundary
implementation
failure-semantics
migration
security
concurrency
recovery
validation-evidence
cross-artifact-coherence
release-evidence
```

A generic `PASS` cannot satisfy an Assurance Plan if required coverage dimensions are missing.

### 2.4 Independence

Independence is modeled by separate axes defined below.

### 2.5 Aggregation

Aggregation combines evidence/findings without majority-vote correctness. T-004 owns the detailed finding/conflict/aggregation protocol. T-003 only fixes the non-negotiable rule that unresolved valid blocking findings cannot be canceled by unrelated PASS results.

## 3. Assurance Plan logical contract

```yaml
assurance_plan:
  assurance_plan_id: <stable id>
  operation_id: <parent operation id>
  subject_ref: <durable subject ref>
  subject_identity: <exact/tuple/candidate/etc when required>

  activities:
    - assurance_id: <stable activity id>
      kind: review | validation | challenge | hidden-validation | coherence | other
      policy: required | recommended | not-required
      mode: <mode>
      coverage: [<dimensions>]
      independence_requirements:
        context: none | required
        model: none | required
        executor: none | required
        evidence: none | required
      depends_on: [<assurance_id>]
      authority_ref: <owning standard/contract>
      acceptance_predicate: <declared predicate>

  aggregation:
    blocking_findings_must_resolve: true
    majority_vote_for_correctness: forbidden
    conflict_route: <T-004 policy ref>

  completion_predicate: <all required assurance predicates satisfied>
```

This is a logical contract. T-009 owns the machine schema.

## 4. Partial-order / DAG semantics

Assurance activities MAY execute in parallel when their predicates are independent.

Valid examples:

```text
Review ───────┐
              ├─> Aggregation / Acceptance
Validation ───┘
```

or:

```text
Candidate Validation
      ↓
Independent Review
      ↓
Targeted re-validation requested by Reviewer
      ↓
Acceptance
```

or:

```text
Blind Reviewer A ──┐
Blind Reviewer B ──┼─> Cross Challenge -> Aggregation
Specialist Review ─┘
```

The plan must represent actual dependencies rather than impose a global sequence.

## 5. Four independence axes

### 5.1 Context independence

The assessor reconstructs required facts from durable authority rather than inheriting the producer's private working context.

For required Independent Review this preserves v3.4 semantics: a fresh session/context may satisfy context independence if it reconstructs from GitHub and pinned authority.

### 5.2 Model independence

The assessor uses a materially different model system/family/provider configuration from another assessor where the Assurance Plan requires model diversity.

Model independence is a risk-control mechanism, not correctness evidence.

The plan MUST record enough identity/provenance to audit the claim without making a vendor-specific model name part of the core protocol. A project/profile MAY pin stronger requirements such as provider diversity.

### 5.3 Executor independence

The executor responsible for producing the assurance result is independent from the executor/role whose work is being assured to the degree required by policy.

Examples:

```text
Builder != required Independent Reviewer context
Validator role does not repair source in the same validation dispatch
Release decision authority is distinct from ordinary CI execution
```

Transport identity may be shared; logical operator/session attribution must make independence auditable.

### 5.4 Evidence independence

The evidence source is independently generated rather than merely another interpretation of the same producer output.

Examples include real Build Host execution, platform integration, simulator/property evidence, hidden validation, or an external authoritative system.

Evidence independence is the strongest answer to questions that cannot be established by text/model review alone.

## 6. Non-substitution invariants

The following are MUST-level:

1. model diversity does not substitute for executable Validation;
2. reviewer agreement does not manufacture runtime truth;
3. a Validation PASS requires actual execution under the owning Validation contract;
4. a hidden-validation requirement cannot be satisfied by visible review;
5. context independence does not imply model independence;
6. model independence does not imply executor independence;
7. executor independence does not imply evidence independence;
8. the same evidence item may be interpreted by multiple reviewers, but this does not create multiple independent evidence sources;
9. `NOT_RUN` remains `NOT_RUN` regardless of reviewer confidence;
10. all assurance results remain subject-identity bound and become stale according to owning identity rules.

## 7. Derived convenience profiles

Projects MAY define named profiles, but each profile MUST expand to the underlying dimensions. Profiles are convenience aliases, not new authority.

Illustrative profiles:

```text
AR0 = no adversarial review requirement
AR1 = context-independent review
AR2 = context-independent + model-diverse adversarial review
AR3 = AR2 + independent executable/real-world evidence
```

These names MAY be used in guidance, but machine truth is the expanded Assurance Plan. T-004 decides whether AR0-AR3 become normative shorthand.

## 8. Review vs Validation boundary

Review/challenge evaluates semantics, consistency, omissions, counterexamples and evidence adequacy.

Validation establishes claims through the execution/evidence method owned by `VALIDATION_STANDARD.md`.

A Reviewer may request Validation, challenge Validation evidence, or identify stale/insufficient evidence. A Reviewer must not convert unexecuted validation into PASS.

A Validator may publish exact evidence and classify environment/toolchain facts. A Validator does not gain product/architecture/review authority merely by executing tests.

## 9. Ordinary-task cost control

Assurance must be risk-proportional.

For a bounded low-risk Task, a valid plan may be only:

```yaml
activities:
  - kind: validation
    policy: required
    mode: executable-validation
  - kind: review
    policy: not-required
```

No empty challenge/reviewer Operations are required.

Escalate assurance when risk/authority requires it, including public contracts, architecture/authority boundaries, security, data integrity, concurrency/recovery, migrations, irreversible operations, cross-project ownership, complex state-machine semantics, or release qualification.

## 10. Assurance placement in the lifecycle

Assurance activities are attached to the Operation whose candidate/result they assess, or to a higher-level coherence/release Operation when the concern is composite.

They MUST NOT create a parallel Review lifecycle. Their routing/evidence facts are consumed by the parent Operation's acceptance predicates and by the existing execution architecture.

When isolation requires a separate Issue/dispatch/role, that Work Item is an executable realization of an assurance activity; it does not become a second parent authority.

## 11. Subject identity and staleness

Every assurance activity whose truth depends on identity MUST bind to the subject identity required by its owning standard.

Examples:

```text
PR Review              exact current PR HEAD
repository validation  exact SHA + environment/toolchain/profile tuple
candidate validation   candidate SHA/tree
release assurance      frozen candidate + evidence-set identity
```

Changing the identity makes prior results historical/stale according to the owning standard. An Assurance Plan cannot override those rules.

## 12. Ownership boundaries

- `OPERATION_CONTRACT.md` owns parent Operation semantics.
- this document owns Assurance Plan composition and independence-axis semantics.
- `GITHUB_AGENT_INTERACTION_PROTOCOL.md` owns GitHub Review interaction/event rules.
- `VALIDATION_STANDARD.md` owns Validation truth/evidence/tuple semantics.
- `MODEL_USAGE_POLICY.md` owns task-risk model-strength routing.
- T-004 owns adversarial review modes, finding union, conflict resolution, aggregation and model-diverse review details.
- T-006 owns reducer/routing integration.
- T-009 owns machine schemas/verifiers.

Model-strength routing and model-diversity assurance are deliberately different:

```text
MODEL_USAGE_POLICY: which model strength should execute the task?
Assurance Plan: does trustworthy acceptance require an independent/model-diverse assessor?
```

## 13. Anti-patterns

Forbidden:

- one `assurance_level` field that hides policy/coverage/independence;
- universal two-reviewer requirement;
- majority vote as correctness;
- treating same-model fresh context as model diversity;
- treating multiple prompts to one model/session as multiple independent reviewers;
- treating green CI as Release Qualification;
- treating review PASS as Validation PASS;
- requiring ceremony-only Operations on Fast Path;
- creating a separate assurance state machine that can disagree with canonical workflow/routing facts.

## 14. T-003 completion boundary

T-003 freezes the logical Assurance Plan and independence axes only. It does not yet define:

- detailed multi-model adversarial protocol / conflict aggregation (T-004);
- interchange envelope/event changes (T-005);
- reducer behavior (T-006);
- schema/verifier implementation (T-009).
