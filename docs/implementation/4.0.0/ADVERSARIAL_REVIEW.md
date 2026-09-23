# v4.0 Adversarial Review, Finding and Aggregation Contract

Status: CANDIDATE — T-004 / Issue #76
Version: 4.0.0
Baseline: `version/v4.0.0@74fa5892481e06f33db186d85e0c6d38a04dc508`
Parent authority: `ARCHITECTURE_DECISION.md` + `OPERATION_CONTRACT.md` + `ASSURANCE_PLAN.md`

## 1. Purpose

This document defines the v4 adversarial-review layer inside an Operation Assurance Plan. It owns model-diverse review modes, blind-first-pass behavior, normalized findings, cross-challenge, conflict handling, aggregation and coherence review.

It does not create a second review lifecycle or replace executable Validation.

Core rule:

```text
Adversarial review tries to falsify acceptance claims.
It does not vote truth into existence and it does not manufacture missing evidence.
```

## 2. Review modes

A Review assurance activity may select one of these modes when justified by risk:

```text
single-independent
cross-peer
specialist
model-diverse-adversarial
coherence-review
human-authority-review
```

`single-independent` preserves the v3.4 fresh-context Independent Review baseline.

`cross-peer` uses multiple independently produced reviews of the same subject.

`specialist` targets one or more dimensions requiring specialized authority or expertise.

`model-diverse-adversarial` requires independent first-pass reasoning from materially different model systems/configurations as declared by the Assurance Plan.

`coherence-review` evaluates composition across otherwise-passing tasks/contracts/repos/authorities. It does not replace Integration Validation.

`human-authority-review` is an authority-bearing human review when project policy explicitly requires human judgment. Human participation does not automatically imply model or evidence independence.

## 3. Blind first pass

For `model-diverse-adversarial` and any other mode that claims independent perspectives, reviewers SHOULD perform a blind first pass before seeing other reviewers' conclusions.

The blind phase receives:

```text
subject identity
frozen authority
required coverage dimensions
relevant evidence refs
review question / falsification goal
```

It SHOULD NOT receive another reviewer's verdict, rationale or proposed fixes before the first-pass finding set is durably produced.

Purpose:

- reduce anchoring and agreement pressure;
- preserve genuinely independent counterexample generation;
- make disagreement observable rather than erased by prompt sharing.

A project MAY skip blind-first-pass only when the selected review mode does not claim independent perspectives or when the Assurance Plan explicitly records why collaborative review is the intended mode.

## 4. Model-diversity semantics

Model independence is satisfied only when the Assurance Plan's declared independence rule is met by materially different model execution systems/configurations.

The core protocol is vendor-neutral. The durable review record MUST state the basis for the independence claim, for example:

```text
provider-diverse
model-family-diverse
architecture/system-diverse
project-approved materially-different configuration
```

The following are not sufficient by themselves:

- multiple prompts to the same continuing context;
- multiple personas in one response;
- the same model/session with different wording;
- multiple reviewers that only repeat the same evidence without independent analysis.

A same-model fresh context may satisfy **context independence** when policy requires that only. It MUST NOT be labeled model-independent merely because the context is fresh.

Model diversity is a risk-control mechanism, not correctness evidence.

## 5. Finding contract

Every material finding SHOULD resolve a logical record with:

```yaml
finding:
  finding_id: <stable id>
  operation_id: <parent operation>
  assurance_id: <review/challenge activity>
  reviewer_ref: <logical reviewer/operator>
  subject_ref: <durable subject>
  subject_identity: <exact identity when required>
  dimension: <coverage dimension>
  severity: P0 | P1 | P2 | P3
  claim: <bounded falsifiable statement>
  evidence_refs: [<durable refs>]
  counterexample_or_failure_mode: <when applicable>
  proposed_disposition: <optional>
  caused_by: <optional finding/challenge ref>
```

Machine representation is deferred to T-009.

Findings are append-oriented. Correction creates a superseding/corrective record; it does not silently erase the original material finding.

## 6. Severity semantics

Canonical review severity remains:

```text
P0 — catastrophic / authority-breaking / release-blocking defect requiring immediate stop
P1 — material correctness, safety, contract or architecture defect that blocks acceptance
P2 — non-blocking but substantive defect/debt/risk requiring explicit disposition
P3 — minor improvement, clarity or maintainability finding requiring disposition when policy asks
```

A project MAY define domain examples but MUST NOT redefine P0/P1 as non-blocking merely to obtain PASS.

## 7. Finding union

When multiple reviews exist, aggregation begins with a **finding union**, not a vote count.

Rules:

1. preserve every independently raised material finding;
2. equivalent findings may be grouped under one root finding only when equivalence is explicit and source reviewers remain linked;
3. a PASS from one reviewer cannot delete another reviewer's valid blocker;
4. absence of a finding from another reviewer is not evidence that the finding is false;
5. duplicate wording may be deduplicated for presentation, never for authority/history.

## 8. Cross-challenge

After blind first passes are durable, reviewers MAY challenge another reviewer's finding or rationale.

A challenge must identify:

```text
challenged finding/result
specific disputed claim
counter-evidence or counterexample
whether the dispute concerns fact, authority interpretation, severity, or applicability
requested resolution route
```

Cross-challenge is not permission for last-writer-wins editing. Both the challenged finding and the challenge remain durable.

## 9. Conflict classes

Useful conflict classes include:

```text
FACT_CONFLICT
AUTHORITY_INTERPRETATION_CONFLICT
APPLICABILITY_CONFLICT
SEVERITY_CONFLICT
EVIDENCE_ADEQUACY_CONFLICT
DUPLICATE_OR_OVERLAP
```

A conflict is only current when the competing claims are both credible under current identity/authority. Stale or invalid evidence is dispositioned first rather than treated as an equal current opinion.

## 10. Conflict resolution routes

Conflicts route according to what could resolve them:

### Factual/runtime uncertainty

Route to required executable Validation or stronger evidence. Review consensus cannot decide an unexecuted runtime fact.

### Authority interpretation conflict

Route to the nearest higher durable authority owner: Frozen Product/Contract, Frozen Architecture, Project Override, Task authority, or explicit amendment process.

### Specialist question

Route to a specialist review activity when the required competence is narrower than the general review.

### Severity disagreement

Resolve the underlying impact/authority facts first. Aggregation MUST use the highest still-valid blocking severity until an authorized disposition demonstrates why reduction is justified.

### Duplicate/overlap

Group for presentation while preserving all source finding identities.

## 11. Aggregation

The aggregation step consumes:

```text
required coverage matrix
review results
finding union
challenge records
validation/evidence requested by conflicts
current subject identity
current authority
```

Allowed top-level review outcomes remain:

```text
PASS
CHANGES_REQUESTED
VALIDATION_REQUESTED
BLOCKED
```

Aggregation invariants:

1. majority vote for correctness is forbidden;
2. any unresolved valid P0/P1 blocks PASS;
3. a higher-authority blocker cannot be waived by reviewer count;
4. P2/P3 require explicit disposition when policy requires complete disposition;
5. missing required coverage cannot be hidden behind generic PASS results;
6. required independence conditions must be satisfied, not merely claimed;
7. `NOT_RUN` validation remains `NOT_RUN`;
8. unresolved credible conflict remains non-PASS until routed/resolved;
9. aggregation is bound to the same subject identity rules as its inputs.

Example:

```text
Reviewer A: PASS
Reviewer B: PASS
Reviewer C: P1 valid blocker
=> aggregate != PASS
```

## 12. Coverage matrix

For high-risk review, the Assurance Plan SHOULD identify required coverage explicitly, for example:

```yaml
coverage:
  contract:
    required: true
    reviewer_ref: R1
  architecture:
    required: true
    reviewer_ref: R2
  failure_semantics:
    required: true
    reviewer_ref: R1
  validation_evidence:
    required: true
    reviewer_ref: R3
```

One reviewer MAY cover multiple dimensions. Multiple reviewers MAY cover the same dimension. Reviewer count is not itself coverage.

## 13. Coherence review

Coherence Review exists for defects that appear only when locally valid changes are composed.

Typical scope:

```text
cross-task semantics
cross-contract compatibility
cross-repository authority boundaries
shared state-machine assumptions
migration ordering
failure/recovery composition
release evidence coherence
```

Coherence Review consumes already-produced local results and current integrated/frozen authority. It does not retroactively convert local validation into integration validation.

If a coherence finding concerns executable composition, route to Integration Validation rather than infer runtime PASS.

## 14. Recommended risk triggers for model-diverse adversarial review

Model-diverse review SHOULD be considered for:

- major Product/PRD boundary freeze;
- major Architecture Freeze;
- public API/schema/contract breaking change;
- security/permission/trust boundary;
- funds/data-integrity/irreversible operations;
- migration/recovery/exactly-once/concurrency semantics;
- cross-project authority/ownership boundary;
- complex state-machine core semantics;
- release qualification for a major version.

It SHOULD NOT be a universal per-PR requirement.

## 15. Derived AR0–AR3 profiles

v4 retains AR0–AR3 as **normative convenience labels**, never as sufficient machine truth.

```text
AR0 — no adversarial review requirement
AR1 — context-independent review
AR2 — context-independent + model-diverse adversarial review
AR3 — AR2 + independently generated executable/real-world evidence
```

Whenever an AR label is used normatively, the durable Assurance Plan MUST expand it into explicit Policy / Mode / Coverage / Independence / Aggregation requirements. A bare `AR2` field without expansion is insufficient.

Projects may define stricter derived profiles but may not weaken the expanded requirements behind a selected label.

## 16. Event/interchange compatibility

T-004 does not introduce a new `ai-dev:event:v2` event enum value.

Important compatibility rule from #98:

```text
adding an unrestricted payload property may be additive;
adding a value to the released closed `event` enum is a protocol compatibility change.
```

Therefore logical `CHALLENGE` and `FINDING` semantics do not automatically imply dedicated event-v2 enum values.

Until T-009 freezes machine mapping:

- use existing v2 event types only when their existing semantics honestly match the record;
- additional correlation/finding payload fields may be used only where allowed without changing the existing event meaning;
- otherwise record the durable challenge/finding as append-oriented GitHub evidence referenced by the Assurance Plan rather than mislabeling it as an existing event;
- any proposal for a new closed-enum event value must explicitly address validator/version compatibility.

## 17. Human participation

Human review may satisfy context/executor independence when the person is genuinely independent from the producing execution context as required by policy.

Human review does not automatically satisfy:

```text
model independence
evidence independence
executable validation
```

A human authority may resolve an authority interpretation conflict only when the project/standard grants that human role the relevant authority.

## 18. Cost control

Ordinary bounded work may remain AR0/AR1 according to Review Policy and risk.

Escalation to AR2/AR3 must be tied to explicit risk/authority/evidence need. More reviewers or more models are not a substitute for better coverage or evidence.

The standard optimizes for the minimum assurance sufficient to protect the relevant authority boundary.

## 19. Ownership boundaries

- `ASSURANCE_PLAN.md` owns assurance composition and independence axes.
- this document owns adversarial review modes, normalized findings, blind-first-pass, finding union, cross-challenge, conflict resolution, aggregation, coherence review and AR0–AR3 expansion semantics.
- `VALIDATION_STANDARD.md` owns executable Validation truth.
- `AGENT_INTERCHANGE.md` owns correlation/interchange semantics.
- `GITHUB_AGENT_INTERACTION_PROTOCOL.md` owns GitHub writer/role/event interaction.
- T-006 owns reducer/controller integration.
- T-009 owns schemas/verifiers/event-version implementation decisions.

## 20. Anti-patterns

Forbidden:

- majority vote as correctness;
- two reviewers canceling one valid P1 because they voted PASS;
- showing reviewers each other's conclusions before a claimed blind first pass;
- labeling same-model fresh context as model diversity;
- using model agreement as runtime evidence;
- using reviewer count as coverage;
- silently deleting findings during deduplication;
- creating a parallel Review state machine;
- adding a new event-v2 enum value and calling it automatically backward-compatible.

## 21. T-004 completion boundary

T-004 freezes adversarial review/finding/conflict/aggregation/coherence semantics. It does not implement reducer logic, JSON schemas, verifier code, event enum changes, transport software or release qualification.
