# v4.6.0 L3 Reference Packs — AI-native / Agentic Development Governance

Status: **FROZEN IMPLEMENTATION REFERENCE — 2026-09-30**

Inputs:
- Frozen Product `e6aa04981110376e623d19b7dd4d0c6d0e139bdf`
- Frozen L2 `f47ea81e8f8df32ac6c8b7cc922c405a17b704d9`
- Frozen Task DAG `d3607c61f22b2c15fbb07d412c4e222e818b31c9`

L3 is implementation guidance subordinate to Frozen Product/L2/DAG. It does not grant scope beyond each Task Pack.

## T01 — Shared AI-native Machine Contracts

### Tests
- schema subset/meta validation;
- historical Dispatch/Execution Pack payloads remain valid without v4.6 refs;
- Intent record cannot manufacture Frozen Product authority;
- Skill metadata cannot manufacture side-effect authority;
- no Context Snapshot / new Assurance result / lifecycle state.

### Contract
Implement `intent-assumption-record-v1` and `skill-metadata-v1`. Optional named refs in Dispatch/Execution Pack are permitted only as backward-compatible discoverability pointers.

### Failure handling
Unsupported repository schema keywords, authority ambiguity, or any need for a new lifecycle state => stop and escalate to L2 rather than inventing a workaround.

## T02 — Intent & Assumption Governance

### Tests
Reject chat→Frozen Product, interpretation→user fact, assumption/UNKNOWN→durable requirement, self-promotion without authority, and contradiction erasure.

### Contract
Normative owner explains classification, materiality, promotion references and routing while preserving Product/Architecture/Task authority.

### Failure handling
If promotion semantics require changing existing Product authority, block and escalate; do not redefine Product Freeze.

## T03 — Context Engineering

### Tests
Reject stale chat/memory overriding current durable authority, larger-context-is-better inference, ephemeral-only required truth, skipped live currentness reread for exact-sensitive actions, and external tool output→Product truth.

### Contract
Define precedence, currentness, provenance and progressive disclosure using durable references; no full context snapshot/database.

### Failure handling
Same-level contradictions remain explicit conflict/UNKNOWN/DECISION_REQUIRED and route to the owning authority.

## T04 — Skill / Procedure Governance

### Tests
Reject installed→trusted, tool capability→side-effect authority, Skill instruction→Product/Task override, embedded secret/project authority, one-off Task fact→Skill authority, and incompatible Skill version silently accepted.

### Contract
Map reusable procedure identity, applicability, authority inputs, tool/side-effect classes, outputs, failure/escalation, evaluation/compatibility/security refs.

### Failure handling
Untrusted provenance or missing applicable side-effect authority fails closed; no automatic execution.

## T05 — Existing-owner Assurance / Dispatch / Handoff Integration

### Tests
Assert F0–F3 remains single autonomy vocabulary; assurance coverage remains on existing plan; review judgment remains existing aggregation; same transport account != independent logical operator; model metadata != independence by itself; Dispatch remains execution handoff.

### Contract
Non-normative integration reference and conformance test only. No new standard or state family.

### Failure handling
Any discovered missing field that materially requires wire change must be classified additive optional vs future-major before mutation.

## T06 — Session / Operator Handoff Dogfood

### Tests
A fresh logical executor receives only durable pointers/fixture packet and must reconstruct exact subject, frozen/current authority, completed evidence, blockers, next action and forbidden assumptions. Hidden chat transcript is unavailable by construction.

### Contract
Dogfood may use repository fixture facts first. Real multi-Agent/runtime execution is required only for claims that static fixtures cannot prove.

### Failure handling
Unavailable real capability becomes exact-subject Validation Request. Static fixture PASS may not be relabeled as real-runtime PASS.

## T07 — Adoption & Cross-standard Wiring

### Tests
Manifest + Golden coverage exactness; PROJECT_OVERRIDES profile is materiality-driven/non-weakening; new owners referenced not duplicated; Fast Path does not force empty records; no historical retrofit; no v4.7 resolver.

### Contract
Central wiring only. Include `templates/golden/STANDARD_COVERAGE.json` explicitly because expanding normative owners requires Golden coverage alignment.

### Failure handling
If central wiring needs a path outside Task Pack, amend authority before writing it; technical necessity is not write authority.

## T08 — Cross-standard Conformance / Closure Inputs

### Tests
Integrated forbidden inference matrix from Frozen Product §11/L2 §13, historical compatibility, v4.1–v4.5 ownership boundaries, fresh-session dogfood evidence binding and Fast Path proportionality.

### Contract
Produce durable closure inputs, not Closure verdict.

### Failure handling
Subject drift invalidates exact-bound evidence; unresolved P0/P1, missing required runtime dogfood or owner conflict remains BLOCKED for Version Closure.
