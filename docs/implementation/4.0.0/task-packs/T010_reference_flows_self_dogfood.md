# T-010 Task Pack — Reference Flows and Self-Dogfood Multi-Model Review

Task: T-010 / Issue #82
R3 coordination: #143
Parent version: #72
Dependency: T-009 / #81 plus R2 machine hardening #140 / PR #141 / Review #142
JIT baseline: `version/v4.0.0@7a8c3c3608bc42325a1ac3c15a335747dea25ddb`
Branch: `task/v4.0.0-t010-r3-reference-flows-dogfood`
Review Policy: required
Risk: critical
Validation scope: integration
Agent freedom: F1_BOUNDED_IMPLEMENTATION

## Goal

Prove the v4 architecture with end-to-end reference flows and execute a new durable blind model-diverse self-dogfood review against the exact post-R2-hardening v4 subject.

Prior dogfood #127 and #135 remain historical `CHANGES_REQUESTED` evidence. They are regression inputs, never current PASS evidence.

## Frozen inputs

- #72 / #82 / #143;
- merged T-001..T-009 v4 architecture and machine contracts;
- historical dogfood #127/#135 and their durable blind records;
- R2 hardening completion #140 / PR #141 / Fresh Review #142;
- new integration baseline `7a8c3c3608bc42325a1ac3c15a335747dea25ddb`;
- #142 carry-forward FIR-1/2/3;
- `ADVERSARIAL_REVIEW.md`, `ASSURANCE_PLAN.md`, `OPERATION_CONTRACT.md` and current v4 machine rules/facade.

## Allowed write set

- `docs/implementation/4.0.0/REFERENCE_FLOWS.md`
- `docs/implementation/4.0.0/SELF_DOGFOOD_PROTOCOL.md`
- `docs/implementation/4.0.0/SELF_DOGFOOD_EVIDENCE.md` after durable R3 dogfood execution
- `templates/golden/V4_REFERENCE_FLOWS.json`
- `scripts/test_v40_reference_flows.py`
- `scripts/v40_r3_hardening.py`
- `scripts/test_v40_r3_carryforward.py`
- `scripts/v40_semantics.py`
- `schemas/review-aggregation-v1.schema.json`
- `standard-manifest.json`
- `.github/workflows/verify-standard.yml`
- `docs/implementation/4.0.0/TASK_PACKS.json` (T-010 pointer only)
- this Task Pack.

## Required pre-dogfood hardening

Close #142 carry-forward with machine regression:

1. FIR-1/P2: declared MDA diversity basis is actually enforced; provider-diverse cannot pass same-provider or identical-model reuse hidden behind labels.
2. FIR-2/P3: Hidden shared-metadata allow-list constrains values to public scalar metadata, preventing structured fixture/oracle smuggling.
3. FIR-3/P3: canonical semantic facade handles malformed reachable input with structured fail-closed errors rather than uncaught AttributeError.

## Required reference scenarios

1. major Product/PRD definition;
2. major Architecture/L2 freeze;
3. ordinary bounded implementation Task;
4. high-risk public-contract/security Task;
5. cross-Task/cross-contract coherence review;
6. version closure/release qualification;
7. Fast Path;
8. stale identity/conflict/blocker recovery.

Each scenario exposes authority, Operation sequence/kinds, exact identity boundary, Assurance dimensions, durable evidence, recovery route and a non-substitution invariant.

## Dogfood subject

Dogfood the exact integrated post-R2-hardening architecture/machine-contract subject at:

```text
sha: 7a8c3c3608bc42325a1ac3c15a335747dea25ddb
```

Do not use the moving T-010 R3 PR HEAD as dogfood subject. Recording dogfood evidence must not invalidate the dogfood evidence itself.

## Required dogfood assurance

- two independently durable blind first-pass reviews;
- both materialized as required `model-diverse-adversarial` lanes;
- declared basis: `provider-diverse` unless an explicit pre-dispatch amendment changes it for a valid reason;
- provider/model/executor/context provenance recorded durably;
- fresh contexts reconstructing only from durable authority;
- no sibling or detailed historical conclusions consumed before each blind first pass is published;
- same 14-dimension coverage matrix for both passes;
- finding union, no majority vote;
- P0/P1 blocker class protected from duplicate/superseded weakening;
- required activity coverage and result identity attested at aggregation;
- cross-challenge only after both first-pass records are durable;
- factual/runtime conflicts routed to executable evidence;
- aggregate exact-subject-bound and compatible with current machine semantics.

## Staged completion

### Stage A — harden + author reference/protocol candidate

Close FIR-1/2/3, reconstruct reference flows, R3 dogfood protocol, machine-readable scenarios and focused regressions.

### Stage B — repository-real validation

Run full `verify-standard` on exact T-010 R3 candidate HEAD. Static inspection is not Validation PASS.

### Stage C — local model-diverse dogfood execution

A fresh local coordinator obtains two blind provider-diverse first passes and durable GitHub records. This is an executor/context/model-independence boundary and MUST NOT be simulated by the Builder context.

### Stage D — evidence closure

Add `SELF_DOGFOOD_EVIDENCE.md` containing only durable refs, identity/provenance/coverage/aggregation metadata and dispositions; do not copy private model scratchpad or hidden evaluator payload.

Any Stage D commit invalidates earlier PR-head CI/Review evidence; rerun exact-head repository validation.

### Stage E — Fresh Independent PR Review

Review the final exact T-010 R3 PR HEAD after dogfood evidence is committed. Dogfood evidence does not replace this Review.

## Validation commands

The authoritative CI chain includes the existing verifier suite plus:

```text
python scripts/test_v40_r3_carryforward.py
python scripts/test_v40_reference_flows.py
```

The focused regressions fail if FIR-1/2/3 regress, required scenario coverage is missing, or reference-flow/dogfood declarations violate v4 orthogonality/non-substitution.

## Forbidden scope

- no migration/adoption policy (T-011);
- no T-012 Closure review;
- no T-013 Release Qualification/main integration;
- no event-v3;
- no second lifecycle/reducer/DAG;
- no majority-vote dogfood aggregation;
- no claiming two prompts from one continuing model/session as model diversity;
- no changing diversity basis after seeing results merely to obtain PASS;
- no inventing Validation truth from review consensus;
- no relabeling #127 or #135 from CHANGES_REQUESTED to PASS.

## Completion

FIR-1/2/3 + all eight scenarios + machine regressions PASS → new durable blind provider-diverse R3 dogfood evidence → evidence committed → final exact-head full verifier PASS → required Fresh Independent Review PASS → merge to `version/v4.0.0` → close #82.
