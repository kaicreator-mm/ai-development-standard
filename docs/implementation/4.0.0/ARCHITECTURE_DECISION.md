# v4.0 Architecture Decision — Unified Operation Protocol and Compatibility Authority

Status: CANDIDATE — becomes FROZEN only when T-001/#73 satisfies required validation + Independent Review and merges to `version/v4.0.0`
Version: 4.0.0
Released baseline: `main@7ebaf66cba8fdc3a672e9b1d7fe9bd9e730a3805` (`VERSION=3.4.0`)
Version Issue: #72
Task: T-001 / #73
Architecture input: #71 `V4_DRAFT_ARCHITECTURE_V0`

This document is the v4 planning authority checkpoint. It generalizes the v3.4 GitHub-native execution architecture without replacing its exact-identity, Validation, Candidate Freeze, Hidden Validation, or Release Authority semantics.

## 1. Core formulation

v4 adopts:

> **One AI development lifecycle, one canonical Operation Protocol, one routing model, and multiple explicitly orthogonal truth dimensions. Agent collaboration, challenge, review, validation and evidence are integrated facets of lifecycle operations, not competing top-level workflows.**

v4 explicitly rejects a single flat state model. The following remain separate truth dimensions:

```text
operation/workflow routing state
Gate state
Validation truth
execution-channel/provider state
dispatch state
candidate state
release verdict
```

No v4 schema, reducer or convenience status may collapse those dimensions into one overloaded `status`.

## 2. Canonical Operation taxonomy

All material lifecycle work uses one Operation Protocol with an explicit `operation_kind`:

```text
PRODUCE  — creates or changes an authoritative candidate artifact/decision
RESEARCH — creates bounded evidence for an unresolved hypothesis
ASSURE   — challenges/reviews/validates a subject without owning that subject
DECIDE   — aggregates authorized facts into an authority-bearing decision
CONTROL  — performs a bounded deterministic transition after predicates are satisfied
```

Representative mapping:

```text
Product Definition             PRODUCE
Product / Architecture Evidence RESEARCH
Architecture Definition        PRODUCE
Task Decomposition             PRODUCE
Task Materialization           CONTROL
Implementation                 PRODUCE
Independent/Adversarial Review ASSURE
Validation / Hidden Validation ASSURE
Candidate Freeze               CONTROL
Release Qualification          DECIDE
Repository Integration         CONTROL
```

The taxonomy is semantic, not a requirement to create one Issue, branch, document or state transition for every listed concept.

## 3. Lifecycle and Operation composition

The canonical lifecycle remains one authority/dependency graph:

```text
Intake / Baseline
→ Product Definition / Acceptance
→ Architecture Definition / Acceptance
→ Task Decomposition + Materialization
→ Implementation Concerns
→ Integration
→ Version Closure / Candidate Preparation
→ Candidate Freeze
→ Hidden / Release Assurance
→ Release Qualification
→ Repository Integration
→ Immutable Baseline
```

An Operation may depend on or spawn bounded child Operations. A child Operation cannot silently redefine parent Product/Architecture/Task authority. Contradictions route upward through explicit amendment or decision paths.

Fast Path is a **reduced-Operation path, not reduced truth**. Low-risk bounded work may omit Product/Architecture/Adversarial Operations when existing frozen authority is sufficient, but cannot omit required Validation, exact identity, GitHub fact-chain or applicable Review Policy decisions.

## 4. Assurance Plan, not fixed assurance sequence

v4 rejects a universal normative sequence such as:

```text
Prepare → Execute → Challenge → Validate → Accept
```

because exact-SHA cost ordering, reviewer-requested Validation, Architecture Research Demo and Hidden Validation create valid alternative orderings.

Instead each subject may carry an **Assurance Plan** represented as a DAG/partial order of requirements, for example:

```text
REVIEW
ADVERSARIAL_CHALLENGE
VALIDATION
COHERENCE_REVIEW
HIDDEN_VALIDATION
```

The plan defines ordering constraints and completion predicates without merging their authority semantics.

## 5. Review architecture dimensions

v4 separates five dimensions that MUST NOT be conflated:

```text
Review Policy       — required | recommended | not-required
Review Mode         — single-independent | specialist | cross-peer | multi-perspective | project-defined
Coverage            — required review dimensions
Independence        — context/model/executor/evidence constraints
Aggregation Policy  — finding union, conflict/disposition and aggregate gate semantics
```

Candidate review dimensions include:

```text
product
architecture
authority-boundary
contract
implementation
security/trust
failure-semantics
data-integrity/migration
concurrency/recovery
validation-evidence
cross-task-coherence
release
```

A generic `REVIEW_RESULT: PASS` cannot satisfy a required dimension that was not covered.

## 6. Independence axes

v4 models independence as separate controls:

```text
context independence
model independence
executor independence
evidence independence
```

Named assurance levels/profiles MAY bundle these axes for convenience but MUST NOT hide which controls were actually satisfied.

Model diversity is selected when common-mode reasoning failure has material propagation/blast radius; it is not universal. Typical escalation candidates include major Product/Architecture freeze, public contract/schema changes, cross-project authority boundaries, core runtime/state-machine semantics, security/trust boundaries, high-impact migration/data integrity/concurrency/recovery, major coherence checkpoints and selected release qualification.

Critical invariant:

```text
multi-model agreement != executable/runtime/real-world Validation evidence
```

## 7. Adversarial review and aggregation

When an Assurance Plan requires model-diverse adversarial review, the default shape is:

```text
Authoritative subject + frozen facts
  ├─ Reviewer A isolated first pass
  └─ Reviewer B isolated first pass
        ↓
Finding union
        ↓
Cross challenge when required
        ↓
Conflict classification
        ↓
Disposition / specialist or authority escalation
        ↓
Aggregation
```

First-pass reviewers SHOULD NOT see peer conclusions before their own durable first-pass result when isolated review is required.

Aggregation is finding-based, not vote-based:

```text
PASS + PASS + unresolved valid blocking finding != PASS
```

A credible unresolved conflict remains non-PASS until disposition. Reviewer count cannot waive a higher-authority blocker.

## 8. Cross-artifact coherence assurance

v4 adds explicit coherence assurance because:

```text
all leaf Tasks individually correct
!=
dependency-complete system semantically coherent
```

Coherence review examines authority ownership, contracts, state-transition assumptions, failure semantics, duplicated/contradictory responsibility and cross-repository boundaries. It does not replace Integration Validation.

## 9. Agent Interchange boundary

Agent interchange is a transport/correlation facet of Operations, not a second workflow.

A conceptual exchange envelope may identify:

```text
exchange identity/type
operation/work-item correlation
subject immutable identity when required
actor role + logical operator identity
payload/evidence references
predecessor/causal identity when relevant
```

GitHub remains the first normative durable reference profile. Transport-neutral conceptual correlation MUST NOT weaken the GitHub profile's Issue authority, event admission, exact identity, pointer-only invocation or reconstructability from durable facts.

T-005 decides whether extending `ai-dev:event:v2` is sufficient. v4 does not assume `event-v3` merely because the major version changed.

## 10. Authority hierarchy

v4 preserves the existing authority chain and adds Operation/Assurance contracts below frozen planning authority:

```text
Frozen Product / Contract
> Frozen Architecture
> Project Overrides within allowed authority
> Task DAG / Task Pack
> Operation Contract / Assurance Plan
> Execution Pack / Dispatch / Exchange
> Agent implementation choice
```

Validation truth and Release Qualification keep their owning standards and are not downgraded to generic Operation metadata.

## 11. v3.4 → v4 compatibility contract

| v3.4 concept | v4 disposition |
|---|---|
| GitHub/repository/evidence durable facts | PRESERVE |
| Chat is workspace/transport, not project state | PRESERVE |
| Issue-first + pointer-only task invocation | PRESERVE |
| Frozen planning DAG vs live Issue Dependency DAG | PRESERVE |
| Task Pack vs JIT exact-base Execution Pack | PRESERVE |
| Builder / Reviewer / Validator authority separation | PRESERVE |
| risk-based Review Policy | PRESERVE and generalize with Mode/Coverage/Independence/Aggregation |
| exact-SHA Review evidence | PRESERVE |
| Validation Tuple / actual execution for PASS | PRESERVE |
| concern / integration / closure validation ownership | PRESERVE |
| orthogonal workflow/Gate/provider/dispatch/candidate/release state | PRESERVE |
| reducer / ready-set / bounded controllers | PRESERVE and correlate to Operations |
| Candidate Freeze / thaw / successor semantics | PRESERVE |
| Hidden Validation + escaped-defect feedback | PRESERVE |
| Release Qualification separate from repository integration | PRESERVE |
| `PR PASS != Release PASS` | PRESERVE |
| one concern, one PR default | PRESERVE |
| Trunk/Fast Path | PRESERVE; formalize as reduced-operation path |
| same-model fresh-context Independent Review | PRESERVE for ordinary AR1-style assurance when policy allows |
| single generic Review PASS for all concerns | GENERALIZE — required coverage becomes explicit |
| single-reviewer-only mental model | GENERALIZE — multi-review/adversarial modes added where risk selects them |
| GitHub-native event protocol | PRESERVE as reference profile; add lifecycle-wide correlation only as needed |

## 12. Normative ownership plan

v4 SHOULD minimize new authorities.

Expected ownership:

```text
DEVELOPMENT_WORKFLOW / successor core lifecycle authority
  owns lifecycle + Operation semantics at human-readable level

EXECUTION_ARCHITECTURE_STANDARD
  owns durable facts / reducer / routing / controllers and orthogonal state dimensions

GITHUB_WORK_ITEM_CONTRACT_STANDARD
  owns GitHub Work Item materialization/profile

GITHUB_AGENT_INTERACTION_PROTOCOL
  owns GitHub exchange/event admission/writer semantics

VALIDATION_STANDARD
  continues to own executable Validation truth

RELEASE_STANDARD
  continues to own candidate/release truth

MODEL_USAGE_POLICY
  owns model-strength routing; v4 Assurance rules own model-diversity/independence requirements
```

A dedicated thin Operation/Assurance standard is allowed only if it reduces duplication rather than creating another parallel lifecycle.

## 13. Explicit non-goals

v4 MUST NOT:

- require multiple models for every PR;
- use majority vote as correctness evidence;
- treat model agreement as Validation PASS;
- require one orchestrator service;
- turn every stage into an Issue/branch/schema;
- expose private chain-of-thought;
- make provider/model brand names normative;
- weaken exact identity, platform/toolchain truth, Candidate Freeze, Hidden Validation or Release Qualification;
- create parallel lifecycle/state authorities for Review, Validation or Agent Interchange.

## 14. Freeze effect

When T-001/#73 is independently reviewed, validated and merged, this document becomes the frozen planning authority for T-002..T-013. Later Tasks may refine machine representation and mappings but MUST route any contradiction with Sections 1–13 through an explicit Architecture Amendment rather than silently redefining v4 semantics.
