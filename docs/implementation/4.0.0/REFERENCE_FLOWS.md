# v4.0 Reference Flows

Status: CANDIDATE — T-010 / Issue #82
Version: 4.0.0
JIT baseline: `version/v4.0.0@21301c89dd48542238a06c6264cb715f33f0648d`
Parent authority: `ARCHITECTURE_DECISION.md`, `OPERATION_CONTRACT.md`, `ASSURANCE_PLAN.md`, `ADVERSARIAL_REVIEW.md`, `AGENT_INTERCHANGE.md`, `OPERATION_ROUTING_INTEGRATION.md`, `WORK_ITEM_OPERATION_INTEGRATION.md`, `VALIDATION_RELEASE_INTEGRATION.md`

## 1. Purpose

These flows prove that v4 can express the development lifecycle without creating a second workflow or flattening orthogonal truth dimensions.

Every flow is written as:

```text
authority
-> Operation sequence
-> subject identity
-> Assurance Plan
-> durable evidence
-> failure/recovery route
-> acceptance/controller boundary
```

The examples are normative reference material for v4 semantics. They do not replace the owning standards or make example values authoritative project state.

## 2. Common invariants

All flows preserve:

1. GitHub/repository/evidence durable facts remain Source of Truth in the GitHub profile.
2. Operation routing is a derived projection; Gate, Validation, provider, dispatch, candidate and release truth remain orthogonal.
3. Review and executable Validation are distinct ASSURE activities.
4. Validation PASS requires actual execution under the Validation authority.
5. exact identity is required whenever truth depends on source/artifact/candidate identity.
6. a PRODUCE actor cannot self-assert required independent assurance.
7. majority voting never establishes correctness.
8. unresolved valid P0/P1 findings block aggregate PASS.
9. Fast Path means operation elision, not truth elision.
10. Candidate Freeze, Release Qualification and repository integration are distinct decisions/transitions.

## 3. Flow RF-01 — Major Product / PRD definition

**Authority:** existing product evidence, business authority, version Issue.

```text
product-evidence (RESEARCH, when needed)
  -> product-definition (PRODUCE)
  -> review (ASSURE, risk-selected)
  -> product acceptance/freeze (CONTROL or owning authority decision)
```

Subject identity is the PRD/product-definition candidate ref and immutable candidate revision used by review. Product evidence is an input, not Product authority.

Assurance dimensions:

```text
policy: required for major product boundary freeze
mode: single-independent or model-diverse-adversarial when risk justifies
coverage: scope, exclusions, authority, acceptance, failure semantics
independence: explicit context/model requirements
aggregation: finding-union + blocker-dominance
```

Failure routes:

- missing evidence -> RESEARCH;
- authority contradiction -> owning Product authority;
- valid blocking review finding -> CHANGES_REQUIRED;
- candidate identity drift -> STALE_IDENTITY and re-dispatch.

Acceptance means the Product candidate is accepted/frozen by its owning authority. It does not imply Architecture, implementation or release PASS.

## 4. Flow RF-02 — Major Architecture / L2 freeze

**Authority:** frozen Product/Contract > architecture evidence > architecture candidate.

```text
architecture-research (RESEARCH, when uncertainty exists)
  -> architecture-definition (PRODUCE)
  -> architecture review (ASSURE)
  -> executable research/validation where required (ASSURE)
  -> architecture acceptance/freeze (CONTROL / authority decision)
```

For a major architecture boundary, AR2-style expanded assurance is appropriate when the plan explicitly requires context + model independence. A bare `AR2` label is insufficient.

Review cannot decide an unexecuted runtime/platform fact. A factual conflict about behavior routes to executable Validation. Architecture Freeze may occur only after required assurance predicates are satisfied on the exact architecture candidate identity.

## 5. Flow RF-03 — Ordinary bounded implementation Task

**Authority:** frozen Product/Architecture + Task Issue/Task Pack + JIT Execution Pack.

```text
implementation (PRODUCE)
  -> repository validation (ASSURE)
  -> applicable Review Policy decision
  -> merge/repository integration controller (CONTROL)
```

This is the default cost-controlled path. No ceremony-only Product, Architecture or adversarial-review Operations are materialized when existing authority is sufficient.

Required facts remain separate:

```text
routing projection: candidate-ready / assurance-pending / acceptable
validation result: PASS | FAIL | BLOCKED | NOT_RUN
review policy/result: owning review contract
provider/dispatch: independent dimensions
merge controller: re-reads current predicates before effect
```

Fast changes in HEAD make exact-head Validation/Review historical; they are not migrated to the new HEAD.

## 6. Flow RF-04 — High-risk public contract / security Task

**Authority:** frozen Product + Architecture + public contract/security authority + Task Pack.

```text
implementation (PRODUCE)
  -> executable validation (ASSURE)
  -> model-diverse-adversarial review (ASSURE)
  -> specialist/security review when required (ASSURE)
  -> conflict routing / targeted re-validation (ASSURE)
  -> aggregation
  -> merge controller (CONTROL)
```

The Assurance Plan expands policy/mode/coverage/independence/aggregation explicitly. Model diversity is a risk control, not executable evidence.

Blind-first-pass is required before reviewers see sibling conclusions when independent perspectives are claimed. After first-pass findings are durable, cross-challenge may occur. Reviewer count cannot waive a valid blocker.

## 7. Flow RF-05 — Cross-Task / cross-contract coherence review

**Authority:** integrated current candidates/results + owning cross-contract/project authorities.

```text
locally accepted Tasks/contracts
  -> coherence-review (ASSURE)
  -> finding/conflict union
  -> executable Integration Validation when composition behavior is uncertain
  -> disposition / changes / acceptance
```

Coherence Review asks whether separately valid pieces compose semantically. It is not Integration Validation.

Typical coverage:

- cross-task semantics;
- contract compatibility;
- shared authority ownership;
- state-machine assumptions;
- migration/recovery ordering;
- release-evidence coherence.

A coherence finding about runtime composition routes to executable Integration Validation instead of becoming review-derived runtime PASS.

## 8. Flow RF-06 — Version closure and Release Qualification

**Authority:** version Issue + merged integration baseline + closure authority + Release Standard.

```text
closure preparation (PRODUCE/CONTROL composition)
  -> full regression / required integration evidence (ASSURE)
  -> candidate preparation
  -> candidate freeze (CONTROL)
  -> hidden validation / critical journeys as required (ASSURE)
  -> release qualification (DECIDE)
  -> repository integration to main (CONTROL)
  -> immutable released baseline
```

Non-substitution rules:

```text
PR PASS != Release PASS
Candidate PREPARED != FROZEN
Release READY != repository integration completed
Hidden Validation evidence != visible review evidence
```

Release Qualification consumes authorized evidence for one frozen candidate SHA/tree. Missing mandatory evidence remains NOT_RUN/BLOCKED and cannot be manufactured by DECIDE.

## 9. Flow RF-07 — Fast Path

**Authority:** existing frozen authority fully covers scope; no material boundary change.

Minimum materialization:

```text
baseline
  -> implementation (PRODUCE)
  -> required validation (ASSURE)
  -> resolved Review Policy
  -> merge controller (CONTROL)
  -> durable fact chain
```

Fast Path is ineligible when scope contains material public-contract, architecture, security/trust, migration/recovery, concurrency/exactly-once, cross-repository/authority, unknown-validation, unresolved-blocker, model-diverse/coherence, nontrivial Execution Pack or material dependency-graph concerns.

No empty Product/Architecture/Review Operations are created merely for conformance.

## 10. Flow RF-08 — Stale identity / conflict / blocker recovery

**Authority:** current Task/PR/candidate identity + owning Validation/Review/Architecture authority.

Example sequence:

```text
implementation HEAD A
  -> Validation PASS on HEAD A
  -> new commit produces HEAD B
  -> prior PASS becomes historical/stale for HEAD B
  -> Review detects factual conflict
  -> requested route = validation-needed (derived, non-authoritative)
  -> Validation executes on HEAD B
  -> findings are unioned on exact HEAD B
  -> blocker is dispositioned or changes requested
  -> acceptance only after current predicates pass
```

Recovery rules:

- old evidence is not rewritten;
- `requested_route` is a derived request, not workflow authority;
- factual conflicts route to executable evidence;
- authority conflicts route upward to durable authority;
- duplicate/superseded findings preserve source identities and linkage;
- duplicate `finding_id` inputs fail closed;
- unresolved blockers remain blockers regardless of PASS count.

## 11. Operation / Assurance / Exchange projection

A material flow may use an Operation instance across multiple dispatches/exchanges:

```text
operation_id = stable logical work correlation
dispatch_id = one executable handoff
exchange_id = one interchange message/result correlation
assurance_id = one assurance activity
```

These identities are related but not interchangeable. Delivery/ACK/exchange success is never Gate, Review, Validation or Release truth.

## 12. Reference-flow acceptance matrix

| Flow | Operation kinds | Assurance characteristic | Identity boundary | Key non-substitution |
|---|---|---|---|---|
| RF-01 Product | RESEARCH/PRODUCE/ASSURE/CONTROL | product-boundary review | product candidate revision | evidence != Product authority |
| RF-02 Architecture | RESEARCH/PRODUCE/ASSURE/CONTROL | architecture + optional model-diverse | architecture candidate | review != runtime Validation |
| RF-03 Bounded Task | PRODUCE/ASSURE/CONTROL | minimum required | exact PR HEAD | routing != validation truth |
| RF-04 High-risk | PRODUCE/ASSURE/CONTROL | blind model-diverse + specialist as needed | exact contract/code subject | model agreement != evidence |
| RF-05 Coherence | ASSURE (+ Validation when routed) | cross-artifact coherence | integrated subject set | coherence != Integration Validation |
| RF-06 Closure | PRODUCE/ASSURE/CONTROL/DECIDE | closure/hidden/release | frozen candidate SHA/tree | PR PASS != Release PASS |
| RF-07 Fast Path | PRODUCE/ASSURE/CONTROL | reduced operations | exact implementation subject | reduced ceremony != reduced truth |
| RF-08 Recovery | PRODUCE/ASSURE/CONTROL | conflict/evidence routing | current exact identity | stale evidence != current evidence |

## 13. T-010 boundary

T-010 proves architecture usability through reference flows and self-dogfood evidence. It does not define migration/adoption policy (T-011), perform version closure (T-012), or perform Release Qualification/repository integration (T-013).
