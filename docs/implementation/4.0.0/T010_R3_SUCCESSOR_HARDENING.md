# T-010 R3 Successor Hardening

Status: CANDIDATE — Issue #150 / PR #151
Parent Task: T-010 / #82
Source dogfood: #145, blind lanes #148/#149
Historical candidate: PR #144 @ `3839621dfd8d61e6d6d239d4abeff1b7ce0ed8b3`
Integration base: `version/v4.0.0@7a8c3c3608bc42325a1ac3c15a335747dea25ddb`

## 1. Purpose

This successor closes machine-contract defects exposed by the provider-diverse R3 dogfood. It inherits the reference flows and FIR-1/2/3 hardening from historical PR #144 but does not rewrite #127, #135, or #145 from `CHANGES_REQUESTED` to PASS.

The successor remains inside T-010. It does not execute T-011/T-012/T-013 and does not create event-v3, a second lifecycle, a second reducer, a third live execution DAG, or majority-vote correctness.

## 2. P1 blocker closure map

| Dogfood group | Source IDs | Machine closure |
|---|---|---|
| MD-1 | R3A-001, R3B-005 | `v40_r3_hardening.validate_model_diversity_basis` + `v40_t010_successor_hardening.validate_mda_cardinality`; a single composite MDA activity must carry at least two durable provenances, provider-diverse requires distinct providers and model IDs |
| FD-1 | R3A-003, R3B-006 | `validate_blocker_resolution_contract` + `review-finding-v1.schema.json`; P0/P1 resolution requires bounded `resolution_code`, evidence and severity-preserving linkage; free-text waiver is not resolution truth |
| VA-1 | R3B-004 | `validate_validation_activity_execution` + `review-aggregation-v1.schema.json`; required Validation result PASS binds to a structured execution tuple and exact subject identity |
| VA-2 | R3B-009, R3B-012 | requested-SHA guards in canonical semantics + PASS wire requirements; requested/tested/checked-out identity must remain exact |
| MC-1 | R3B-010 | `validation-report.schema.json` and `agent-event-v2.schema.json` PASS conditionals are strengthened so schema-only consumers cannot accept under-bound PASS records that the canonical facade rejects |
| CR-1 | R3B-011 | `validate_release_freeze_evidence_binding`; verdictive Release Qualification requires durable Candidate Freeze evidence ref, exact candidate SHA/tree evidence identity, and visible closure evidence ref |

## 3. Same-stream P2/P3 dispositions

### R3A-002 — anonymous finding erasure

Closed. `validate_blocker_resolution_contract` rejects a finding without a non-empty `finding_id` before aggregation can treat it as absent.

### R3A-004 — legacy Fast Path primitive

Disposition: **explicit compatibility debt, non-canonical / non-acceptance surface**.

The canonical v4 facade exports `fast_path_eligible` from `v40_r2_hardening`, which is closed-world: every required/disqualifier predicate must be declared and typed. `v40_rules.fast_path_eligible` remains an internal historical primitive for released regression compatibility and MUST NOT be used as a sufficient v4 acceptance surface. Successor regression verifies the canonical exported symbol remains the closed-world implementation. Removing the internal historical primitive is cleanup, not an acceptance blocker, because no current v4 canonical path delegates Fast Path truth to it.

### R3A-005 + R3B-001 — arbitrary authority refs

Closed. `operation-v1.schema.json` plus canonical semantics require durable authority-ref grammar for the Operation and actor contract. Self-authority rejection remains in force.

### R3A-006 — Operation type extensibility

Decision closed: machine v1 accepts the frozen canonical core vocabulary plus a project-namespaced form `namespace:type`. Unnamespaced synonyms are rejected. Project-defined types must still declare one explicit canonical Operation kind; they do not redefine core types.

### R3B-002 — unconstrained next_operations / third-DAG risk

Closed to the machine boundary available here without inventing GitHub dependency authority. Each `next_operations` entry must bind Operation correlation to an owning Work Item as `op:<id>|work-item:#N`. The edge remains non-authoritative correlation. Task readiness continues to come only from GitHub Task Issues + native Issue Dependencies. This schema does **not** claim that the connector can prove a native dependency edge exists; that remains the owning GitHub execution-DAG authority and must fail closed at materialization/controller time when required.

### R3B-007 — PASS with unresolved blocker refs

Closed in `review-aggregation-v1.schema.json`: `judgment=PASS` requires `unresolved_blocker_refs=[]`, in addition to semantic blocker-dominance checks.

### R3B-008 — opaque DECISION envelope

Closed. DECISION interchange is limited to `release-controller` + `release-decision` or `human-authority` + `authority-decision`. The envelope remains `CORRELATION_ONLY_NON_AUTHORITATIVE`; payload classification does not create authority.

### R3A-007 — malformed Candidate Freeze identity

Closed. canonical Candidate Freeze validation requires 40-hex candidate SHA and tree SHA in addition to exact evidence identity binding.

### R3A-008 — coverage vocabulary

Disposition: project-extensible by design. Coverage is explicit and required, but the core protocol does not pretend one universal closed dimension vocabulary fits every project/domain. Projects may use namespaced coverage dimensions; required coverage still has to be attested exactly by the owning Assurance Plan.

## 4. Validation and compatibility

Every closure must retain released v3.3/v3.4 regressions and the v4 T-009/R2/R3 suites. Tightening a false-PASS input class is intentional non-weakening, not a rewrite of historical evidence.

`agent-event-v2` stays event-v2; no logical interchange family is added to its event enum.

## 5. Acceptance boundary

This document is not PASS evidence. PR #151 requires exact-head repository-real full verifier PASS and Fresh Independent Review PASS. If merged, the next T-010 dogfood round must use the new integration baseline as a newly frozen subject and new provider-diverse blind contexts; historical dogfood records remain historical.
