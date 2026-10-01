# v4.8.0 L3 Implementation Reference Packs

Status: **CANDIDATE L3 REFERENCE — NOT BUILDER READY**

Authority: Frozen Product + Frozen L2 `f88c85454e80101a0fdf56050e21f11a05279841` + Frozen Task DAG R1 `634dd746cd16da970bb01822a1b6c59714c52429` / `72dfeee93c092296004c7083b71fdd877d7f1b34` + per-Task Packs under `task-packs/`.

This file is implementation guidance only. Task Packs own scope/write-set/acceptance; JIT Execution Packs own exact-base execution narrowing. L3 cannot expand Frozen Product/L2/DAG or manufacture Validation/Review truth.

## Shared negative oracles

Reject all of the following across v4.8:

```text
capability claim -> proven capability
Capability Evidence -> current Validation/Review PASS
provider/model label -> authorization or global correctness score
runner/host fact -> Logical Agent Profile owner
stale Availability -> hard eligibility satisfied
ranking/cost/latency -> INELIGIBLE/UNKNOWN becomes ELIGIBLE
independent per-key CAS -> composite work+resource admission proven
transport ACK/progress -> Task/Review/Validation completion
transient queue/chat state -> durable authority
Task Learning rationale -> private chain-of-thought requirement
Task Learning -> Product/Architecture/Task/ADR/Incident authority
STANDARD_FRICTION_CANDIDATE -> automatic standard change
#469 bounded successes -> blanket strong-to-low-cost rule
NOT_MEASURED economics -> savings claim
```

## T-001 — Task Learning Evidence

**Tests:** exact-subject binding; stale successor negative; `NONE_MATERIAL`; secret/CoT rejection; evidence-layer validation.
**Contract:** compact refs/summaries only; historical after drift; no authority substitution.
**Implementation:** JSON Schema + focused fixtures; keep optional fields bounded; prefer refs/digests to copied logs.
**Failure handling:** ambiguous subject/currentness fails closed; do not weaken to repository-name-only identity.
**Reference:** Frozen L2 Task Learning sections; Execution Architecture owner boundary.

## T-015 — Logical Agent Capability Profile

**Tests:** logical claims accepted; OS/toolchain/resource/concurrency ownership-copy rejected; Skill-is-proof rejected; credential-is-authority rejected.
**Contract:** profile is claim metadata for logical executor/model/operator classes, not current availability/trust/proof.
**Implementation:** provider-neutral classes; provenance fields allowed; infrastructure requirements represented by refs/classes, not duplicated inventories.
**Failure handling:** unknown/missing claim remains unknown; never synthesize capability from provider identity.
**Reference:** Frozen L2 + `CI_RUNNER_CAPABILITY_STANDARD.md` + v4.6 Skill governance.

## T-016 — Agent Capability Evidence

**Tests:** positive/negative evidence; stale exact-subject; evidence→current PASS rejection; economic non-inference.
**Contract:** historical evidence about a capability/task class; bounded strength layers, no global scalar score.
**Implementation:** bind actual subject/environment/role/result/review/validation refs; measured fields nullable/NOT_MEASURED.
**Failure handling:** missing comparable baseline forbids savings/performance conclusion.
**Reference:** Frozen L2 + #469 evidence boundary.

## T-002 — Execution Architecture Core

**Tests:** READY/currentness; hard filter ordering; independence conflict; stale Availability; capacity 1/N; multi-resource contention; injected crash between evaluation/publication; replacement admission after reconciliation.
**Contract:** canonical READY/Dispatch/Claim retained. Admission set = work claim + all required resource units, committed at one linearization point.
**Implementation:** prefer existing single-writer admission for first conforming path. If using a composite conditional transaction, it must be genuinely linearizable across the full set. Ranking receives ELIGIBLE choices only.
**Failure handling:** no safe composite primitive => serialize through designated writer or `BLOCKED/UNAVAILABLE`; ambiguous crash state => reconcile durable bindings before new incompatible admission.
**Reference:** `EXECUTION_ARCHITECTURE_STANDARD.md` §11.1 and Frozen L2.

## T-003 — Existing Interchange v1 profile

**Tests:** first demonstrate whether a concrete v4.8 field/ref gap exists; historical envelope fixtures; duplicate/replay/conflict/currentness; GitHub event mapping.
**Contract:** existing Interchange v1 remains generic owner/family; `NO_CHANGE_REQUIRED` is successful if no gap exists.
**Implementation:** prefer adapter/profile documentation over schema mutation; if mutation is needed, keep it additive and backward-compatible. Receiver capability refs bind T-015.
**Failure handling:** conflicting same-id payload fails closed; stale subject rejected; ACK/progress never promotes workflow state.
**Reference:** `docs/implementation/4.0.0/AGENT_INTERCHANGE.md`, `schemas/interchange-envelope-v1.schema.json`, `GITHUB_AGENT_INTERACTION_PROTOCOL.md`.

## T-004 — Task Learning closeout wiring

**Tests:** material vs NONE_MATERIAL; exact ref preservation; stale-source closeout; no copied hidden evidence.
**Contract:** templates expose refs/checks only; semantic meaning remains T-001/T-002 owned.
**Implementation:** minimal optional fields/checklist steps; preserve Fast Path.
**Failure handling:** missing required currentness/evidence ref => closeout cannot claim supported behavioral learning.

## T-005 — ADS Evolution Governance

**Tests:** each classification; project-specific false-positive; environment/Agent defect false-positive; `MORE_EVIDENCE`; `NO_CHANGE`; privacy restriction.
**Contract:** observations classify and route; only ordinary ADS governance changes the standard.
**Implementation:** additive workflow/template/checklist language; no global numeric threshold.
**Failure handling:** insufficient cross-project evidence => MORE_EVIDENCE, not automatic promotion.

## T-006 — Registry / adoption wiring

**Tests:** manifest completeness; exactly three new schema families; existing Interchange listed once; project adoption discovery; historical verification.
**Contract:** registry/discovery is metadata only.
**Implementation:** central shared-file changes happen here after semantic owners merge.
**Failure handling:** duplicate owner/family entry is a blocking conformance failure.

## T-007 — Contract compatibility

**Tests:** integrated three-family fixtures plus all shared negative oracles; old v4 payloads remain valid.
**Contract:** test-only concern; must not repair sibling semantics inside this Task.
**Implementation:** use stable fixtures/golden examples and deterministic schema validation.
**Failure handling:** a semantic defect becomes a finding against owning Task, not an ad-hoc test workaround.

## T-008 — Eligibility/resource conformance

**Tests:** competing READY tasks; heterogeneous profiles; stale Availability; independence conflict; rank ordering; capacity N; multi-resource all-or-none; crash ambiguity/recovery.
**Contract:** executable oracle for T-002, no new scheduler semantics.
**Implementation:** deterministic model/reference reducer; inject failures around the single linearization point.
**Failure handling:** any accepted partial state or over-allocation is P1/P0-level blocking evidence.

## T-009 — Interchange replay/restart conformance

**Tests:** duplicate same payload; conflicting payload; stale request; lost/replayed delivery; ACK non-authority; restart reconstruction.
**Contract:** test existing Interchange + existing semantic owners.
**Implementation:** deterministic replay log fixtures; reconstruct from durable facts only.
**Failure handling:** last-writer-wins conflict or dependence on transient queue history is blocking.

## T-010 — Learning/evolution governance conformance

**Tests:** NONE_MATERIAL/material; stale learning; every defect class; NO_CHANGE/MORE_EVIDENCE; publication/privacy; hidden evaluator leakage negative.
**Contract:** test-only concern.
**Failure handling:** classification that directly mutates normative authority is blocking.

## T-011 — Heterogeneous orchestration dogfood

**Tests/scenarios:** multiple READY items; at least two materially different logical Agent profiles; fresh/stale environment facts; scarce resource race; reviewer/validator independence; transport duplicate/loss; crash/restart; bounded executor escalation.
**Contract:** evidence producer only; no silent semantic repair.
**Implementation:** maintain an evidence matrix with `SYNTHETIC|REAL`, subject identity, environment, executor, expected oracle and actual result.
**Failure handling:** any unavailable real environment produces exact-subject Validation handoff/NOT_RUN, never synthetic PASS.

## T-012 — #469 bounded-agent dogfood

**Tests/evidence:** exact Task-class pack identity; clarification/escalation; edit/test loops; negative oracles; write-set drift; stale base/rebind; independent Validation/Review; measured resource/time/cost when comparable.
**Contract:** `ECONOMIC_SAVINGS=NOT_MEASURED` until comparable evidence exists; no blanket routing rule.
**Implementation:** before bounded/low-cost execution, create JIT exact-base Execution Pack with allowed write set, semantic kernel, positive/negative tests, failure matrix and escalation triggers.
**Failure handling:** ambiguity, contract expansion, stale refs or unavailable required environment => stop/escalate; never self-certify.

## T-013 — Cross-project evolution dogfood

**Tests/evidence:** at least two materially distinct streams when available; classification agreement/challenge; false-positive rejection; repeated friction; privacy/publication; NO_CHANGE/MORE_EVIDENCE/evolution-candidate routes.
**Contract:** evidence producer only; standard change still follows ordinary ADS governance.
**Failure handling:** single-project/provider anecdote cannot justify universal policy.

## T-014 — Integrated convergence / closure inputs

**Tests:** full repository verifier/regression plus integrated v4.8 oracles; owner uniqueness; three-family count; Interchange reuse; scheduling/resource invariants; Fast Path/backward compatibility; dogfood evidence-strength audit.
**Contract:** produces durable Version Closure inputs only, not Release Qualification.
**Implementation:** run after all blockers merge on exact integration baseline; bind all evidence to that baseline.
**Failure handling:** any mandatory NOT_RUN/BLOCKED, stale evidence, owner duplication, overclaim or regression blocks closure-input PASS and routes to owning Task/repair.

## JIT rule

No branch or Execution Pack is frozen here. After canonical planning integration establishes exact `version/v4.8.0`, the Controller must recompute native blockers/currentness/resources and create each Task branch + Execution Pack JIT. A Pack/L3 root is not sufficient for READY.