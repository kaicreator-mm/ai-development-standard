# v4.0 Canonical AI Development Operation Contract

Status: CANDIDATE — T-002 / Issue #74
Version: 4.0.0
Baseline: `version/v4.0.0@abefb96ff1603e60add987c4c33983e4fe050211`
Parent authority: `docs/implementation/4.0.0/ARCHITECTURE_DECISION.md`

## 1. Purpose

This document defines the canonical logical contract for an **AI Development Operation** and maps the released v3.4 lifecycle into that contract without changing v3.4 execution, Validation, Review, Candidate, Release, or GitHub authority semantics.

The Operation Contract is a correlation and lifecycle abstraction. It is not a new Source of Truth, not a replacement for Work Items, and not a flat state machine.

Core invariant:

```text
one development lifecycle
+ one canonical Operation Protocol
+ one routing model
+ orthogonal truth dimensions
```

## 2. Operation definition vs Operation instance

v4 distinguishes two concepts.

### 2.1 Operation definition

A reusable semantic definition of a type of development work, for example `architecture-definition`, `implementation`, or `release-qualification`.

It defines:

```text
operation_type
operation_kind
expected authority class
required subject/input shape
allowed actor roles
candidate-output class
acceptance/failure semantics
allowed successor relationships
```

### 2.2 Operation instance

One concrete execution/correlation of an Operation definition for a repository/version/work item/subject.

It binds:

```text
operation_id
work item / version context
authority refs
subject refs + exact identity where required
input refs
actor/dispatch refs
candidate-output refs
assurance plan ref when applicable
current routing projection
result / transition refs
```

A definition is reusable semantics. An instance is durable project-specific work.

## 3. Canonical Operation kinds

Every material Operation resolves exactly one semantic kind:

```text
PRODUCE
RESEARCH
ASSURE
DECIDE
CONTROL
```

### PRODUCE

Creates or changes an authoritative candidate artifact/decision within declared scope.

Examples: Product Definition, Architecture Definition, Task Decomposition, Implementation.

A PRODUCE Operation may create a candidate subject, but it does not self-assert independent assurance or release truth.

### RESEARCH

Produces bounded evidence for an unresolved hypothesis or uncertainty.

Examples: Product Evidence, Architecture Research Demo.

A RESEARCH result proves only the declared hypothesis/evidence boundary. It does not silently become Product/Architecture authority.

### ASSURE

Challenges, reviews, tests, validates, or otherwise produces assurance evidence about a subject without owning the subject's production authority.

Examples: Independent Review, Adversarial Review, Validation, Hidden Validation, Coherence Review.

ASSURE is a semantic umbrella only. Review and executable Validation retain distinct truth rules and owners.

### DECIDE

Aggregates authorized facts/evidence into an authority-bearing decision.

Example: Release Qualification.

A DECIDE Operation cannot manufacture missing evidence; `NOT_RUN/BLOCKED` inputs remain non-PASS.

### CONTROL

Performs a bounded deterministic transition after declared predicates are satisfied.

Examples: Task Materialization, Candidate Freeze, Merge/Repository Integration Controller actions.

A CONTROL Operation does not invent product semantics or downgrade mandatory gates.

## 4. Canonical logical contract

The minimal logical form is:

```yaml
operation:
  protocol_version: ai-dev-operation/v1
  operation_id: <stable instance id>
  operation_type: <canonical or project-defined type>
  operation_kind: PRODUCE | RESEARCH | ASSURE | DECIDE | CONTROL

  context:
    repository: <owner/repo>
    version_or_scope: <ref>
    work_item_ref: <optional durable ref>

  authority:
    refs: [<durable refs>]
    resolution: <normal authority-chain basis>

  subject:
    refs: [<durable refs>]
    identity_binding: <none | exact | tuple | candidate | project-defined>
    identity: <when applicable>

  inputs:
    refs: [<durable refs>]

  actor_contract:
    allowed_roles: [<roles>]
    execution_profile: <optional profile>
    agent_freedom: <optional F0-F3 or successor>

  entry_criteria: [<predicates>]
  candidate_outputs: [<declared output classes/refs>]

  assurance_plan_ref: <optional durable ref>

  acceptance_criteria: [<predicates>]
  failure_routes: [<route definitions>]
  next_operations: [<dependency/successor refs>]
```

This is a logical contract. T-009 decides the minimum machine schema representation. GitHub reference implementations SHOULD reuse Issue/Task Pack/Execution Pack/event fields rather than duplicate the whole object in one payload.

## 5. Required invariants

### 5.1 Stable correlation identity

`operation_id` identifies one logical Operation instance across dispatches, reviews, validations, retries and transport events.

A retry/re-dispatch MAY retain the same `operation_id` when it is still the same logical work subject, but each dispatch/exchange keeps its own identity.

A replacement subject that invalidates the prior Operation's accepted candidate MAY require a successor Operation instance or an explicit subject-identity update according to the owning workflow. Historical evidence is never rewritten.

### 5.2 Authority is referenced, not copied into existence

An Operation MUST reference the durable authority that governs it. It MUST NOT create higher authority merely because a field says `authority`.

Normal precedence remains:

```text
Frozen Product / Contract
> Frozen Architecture
> allowed PROJECT_OVERRIDES
> Task DAG / Task Pack
> Operation Contract / Assurance Plan
> Execution Pack / Dispatch / Exchange
> Agent implementation choice
```

Validation and Release authority remain with their owning standards.

### 5.3 Subject identity is explicit where truth depends on identity

Operations involving source/artifact/release truth MUST declare the relevant identity binding.

Examples:

```text
Independent Review     -> exact PR HEAD identity
Validation             -> exact subject × environment/toolchain × profile tuple
Candidate Freeze       -> candidate SHA/tree
Release Qualification  -> frozen candidate identity + authorized evidence set
Repository Integration -> validated candidate + resulting repository baseline
```

No Operation abstraction permits evidence to migrate silently to a different identity.

### 5.4 Inputs and outputs are durable refs

Material inputs/outputs SHOULD be durable repository/GitHub/evidence references. Chat summaries are not authoritative inputs.

An output may be:

```text
candidate artifact
research evidence
a review/validation result
a decision
a controller transition record
```

depending on Operation kind.

### 5.5 Actor role does not equal authority owner

An actor executes an Operation under declared role/profile. The actor does not gain authority beyond the Operation contract.

Examples:

```text
Builder executing IMPLEMENTATION cannot self-assert Independent Review PASS
Validator executing VALIDATION cannot repair source under the same validator dispatch
Reviewer executing REVIEW cannot become Builder in the same review role/session
Controller executing FREEZE cannot waive an unsatisfied mandatory gate
```

### 5.6 Fast Path uses operation elision

Low-risk bounded work MAY omit Product/Architecture/Research/Adversarial Operations when existing authority is sufficient.

Fast Path MUST NOT synthesize empty Operations for conformance.

The minimum remains:

```text
Baseline
-> PRODUCE/Implementation
-> required ASSURE/Validation
-> applicable Review Policy decision
-> CONTROL/Merge when predicates pass
-> durable fact chain
```

Escalation to additional Operations occurs when risk, ambiguity, public contract, architecture, security, data-integrity, or evidence conditions require it.

## 6. Routing model

The abstract Operation routing projection is:

```text
PLANNED
READY
ACTIVE
CANDIDATE_READY
ASSURANCE_PENDING
ACCEPTABLE
COMPLETED
```

with alternate routes:

```text
CHANGES_REQUESTED
BLOCKED
SUPERSEDED
CANCELLED
```

This is a **routing projection**, not universal truth.

It MUST NOT absorb or replace:

```text
Gate state: PASS / FAIL / BLOCKED / NOT_RUN / NOT_APPLICABLE
Validation truth
provider/channel state
dispatch state
candidate state: PREPARED / FROZEN / THAWED / INVALIDATED
release verdict: NOT_READY / READY / CONDITIONAL / BLOCKED / FAIL
```

The GitHub profile may continue to expose the more detailed v3.4 `state:*` vocabulary. T-006 owns reducer mapping.

## 7. Entry, candidate, assurance and acceptance

An Operation instance is executable only when its `entry_criteria` are satisfied by durable/derived authorized facts.

For PRODUCE Operations:

```text
entry satisfied
-> work execution
-> candidate output exists
-> required assurance predicates evaluated
-> acceptance criteria satisfied
-> completed / successor unlocked
```

This is not a fixed assurance ordering. Review, Validation, research, or other assurance dependencies may form a DAG/partial order.

`candidate_outputs` are not accepted outputs until the required acceptance predicates are satisfied.

## 8. Failure and recovery routes

The common failure-route vocabulary is conceptual, not a new Gate state:

### CHANGES_REQUIRED

The candidate exists but must be changed before acceptance. Routes to a producing Operation/Builder path.

### VALIDATION_NEEDED

A required runtime/platform/executable fact is missing. Routes to an ASSURE/Validation Operation.

### AUTHORITY_CONTRADICTION

Lower-level execution cannot satisfy or reconcile higher authority. Routes upward to Product/Architecture/Task authority rather than silent redesign.

### BLOCKED

Execution/assurance cannot proceed because of a real prerequisite/environment/access/dependency blocker. The associated Gate/provider/dispatch dimensions retain their own exact states.

### STALE_IDENTITY

The subject/base/candidate identity no longer matches the dispatched/reviewed/validated identity. Historical results remain historical; affected work is superseded/re-dispatched.

### SUPERSEDED

A newer authorized Operation/candidate replaces this routing instance. Does not rewrite old evidence.

## 9. Operation composition and DAG semantics

Operations form one lifecycle dependency graph.

Relationships MAY include:

```text
requires
produces-input-for
assures
blocks
supersedes
controls-transition-for
```

A child/sub-operation is not a second lifecycle authority.

Example:

```text
ARCHITECTURE_DEFINITION (PRODUCE)
  requires PRODUCT_ACCEPTED
  may require ARCHITECTURE_RESEARCH (RESEARCH)
  produces architecture candidate
  may require ARCHITECTURE_REVIEW (ASSURE)
  -> ARCHITECTURE_ACCEPTANCE / FREEZE (CONTROL or authority-specific acceptance)
```

The planning DAG and live GitHub Issue Dependency DAG remain distinct exactly as in v3.4.

## 10. v3.4 lifecycle mapping

| v3.4 lifecycle concept | v4 Operation interpretation | Kind | Notes |
|---|---|---|---|
| Intake / Baseline | context establishment | not necessarily materialized | may be implicit for Fast Path |
| L1 Product Evidence | Product Evidence | RESEARCH | only when needed |
| PRD / Scope Definition | Product Definition | PRODUCE | candidate until accepted/frozen |
| Product/Scope Freeze | Product Acceptance/Freeze | CONTROL / authority acceptance | must not manufacture missing evidence |
| L2 Architecture Evidence | Architecture Research/Evidence | RESEARCH | includes bounded demos where required |
| L2 Architecture Definition | Architecture Definition | PRODUCE | produces architecture candidate |
| Architecture Freeze | Architecture Acceptance/Freeze | CONTROL / authority acceptance | explicit amendment required after freeze |
| Task DAG definition | Task Decomposition | PRODUCE | planning/history authority |
| Task Issue materialization | Task Materialization | CONTROL | live DAG remains GitHub Issue Dependencies |
| L3 / Semantic Kernel preparation | bounded planning/execution input | PRODUCE or sub-artifact | only when risk/policy requires |
| Task implementation | Implementation | PRODUCE | one concern/PR default preserved |
| Minimal CI / tests | Validation evidence | ASSURE/executor-specific | CI remains executor, not Release Authority |
| Independent Review | Review | ASSURE | risk-based, exact-head when executed |
| real-host/platform Validation | Validation | ASSURE | actual execution required for PASS |
| merge controller | Integration transition | CONTROL | predicates re-read before merge |
| integration owner work | Integration | PRODUCE + ASSURE as applicable | cross-component behavior |
| Candidate Preparation | closure preparation | PRODUCE/CONTROL sub-operations | not Candidate Freeze |
| Candidate Freeze | Candidate Freeze | CONTROL | exact candidate visible gates required |
| Hidden Validation | Hidden Validation | ASSURE | independent evidence |
| Version Closure | Closure aggregation/work | PRODUCE/ASSURE/CONTROL composition | not one overloaded status |
| Release Qualification | Release Qualification | DECIDE | READY/CONDITIONAL/BLOCKED/FAIL authority preserved |
| version -> main | Repository Integration | CONTROL | separate from Release Qualification |
| immutable main baseline | accepted output / durable fact | output, not necessarily an Operation | canonical release identity |

## 11. What is not a standalone Operation by default

To avoid ceremony, the following are not automatically materialized as Operations:

```text
simple baseline reads
formatting-only intermediate steps
one test command
one event/comment
one queue projection
one reducer recomputation
one state-card refresh
one prompt transmission
```

They may be execution steps or evidence inside another Operation.

Materialize a separate Operation when independent authority, subject identity, actor boundary, assurance requirement, replay/recovery need, or dependency routing justifies it.

## 12. GitHub reference materialization

In the GitHub profile, an Operation MAY be represented by composition of existing durable objects:

```text
Issue body / Task Pack      -> stable operation assignment/authority
Issue metadata              -> routing/classification projection
Execution Pack              -> JIT exact-base execution constraints
Dispatch                    -> one executable handoff
PR/commit/artifact           -> candidate subject identity
Review/Validation evidence  -> assurance results
structured event            -> append-oriented exchange/history
controller result            -> deterministic transition fact
```

There is no requirement for a duplicated `operation.yaml` when these refs already carry complete authority. T-009 may define a compact schema for interchange/conformance where useful.

## 13. Operation type vocabulary policy

v4 SHOULD keep the protocol extensible without allowing arbitrary synonyms.

Core lifecycle types SHOULD include stable canonical concepts such as:

```text
product-evidence
product-definition
architecture-research
architecture-definition
task-decomposition
task-materialization
implementation
integration
review
validation
coherence-review
candidate-freeze
hidden-validation
release-qualification
repository-integration
```

Projects MAY add domain-specific types under a project namespace when the type has genuinely different semantics. They MUST NOT rename core types merely for style.

T-009 decides machine enum/extensibility mechanics.

## 14. Compatibility constraints

T-002 MUST NOT change these T-001/v3.4 invariants:

- GitHub/repository/evidence durable facts remain truth in the GitHub profile;
- Issue-first and pointer-only invocation remain valid;
- Task Pack vs Execution Pack remain distinct;
- Review and Validation remain separately authoritative;
- actual execution is required for Validation PASS;
- exact identity/drift rules remain unchanged;
- workflow/Gate/provider/dispatch/candidate/release dimensions remain orthogonal;
- Candidate Freeze/Hidden Validation/Release Qualification semantics remain unchanged;
- `PR PASS != Release PASS`;
- Fast Path remains lightweight.

## 15. Downstream ownership

T-002 freezes only the logical Operation contract and lifecycle mapping.

Downstream ownership:

```text
T-003 -> Assurance Plan + independence axes
T-004 -> multi-model review/findings/conflict/aggregation
T-005 -> exchange envelope/correlation + event-v2 mapping
T-006 -> reducer/routing concrete integration
T-007 -> Work Item/Task Pack/Execution Pack/Fast Path integration
T-008 -> Validation/Freeze/Hidden/Release integration
T-009 -> schemas + golden/forbidden examples + verifier regressions
```

If a downstream Task finds this contract internally contradictory, it must raise an explicit Architecture/Planning Amendment rather than silently redefine Operation semantics.
