# T-010 Task Pack — Reference Flows and Self-Dogfood Multi-Model Review

Task: T-010 / Issue #82
Parent version: #72
Dependency: T-009 / #81 including hardening #120/#123
JIT baseline: `version/v4.0.0@21301c89dd48542238a06c6264cb715f33f0648d`
Branch: `task/v4.0.0-t010-reference-flows-dogfood`
Review Policy: required
Risk: high
Validation scope: integration
Agent freedom: F1_BOUNDED_IMPLEMENTATION

## Goal

Prove the v4 architecture with end-to-end reference flows and execute one durable blind model-diverse self-dogfood review against the exact post-T-009 v4 subject.

## Frozen inputs

- #72 / #82;
- merged T-001..T-009 v4 architecture and machine contracts;
- #110 carry-forward on blind independent vs collaborative review;
- T-009 final hardening merge baseline `21301c89dd48542238a06c6264cb715f33f0648d`;
- `ADVERSARIAL_REVIEW.md`, `ASSURANCE_PLAN.md`, `OPERATION_CONTRACT.md` and current v4 machine rules.

## Allowed write set

- `docs/implementation/4.0.0/REFERENCE_FLOWS.md`
- `docs/implementation/4.0.0/SELF_DOGFOOD_PROTOCOL.md`
- `docs/implementation/4.0.0/SELF_DOGFOOD_EVIDENCE.md` after durable dogfood execution
- `templates/golden/V4_REFERENCE_FLOWS.json`
- `scripts/test_v40_reference_flows.py`
- `standard-manifest.json`
- `.github/workflows/verify-standard.yml`
- `docs/implementation/4.0.0/TASK_PACKS.json` (T-010 pointer only)
- this Task Pack.

## Required reference scenarios

1. major Product/PRD definition;
2. major Architecture/L2 freeze;
3. ordinary bounded implementation Task;
4. high-risk public-contract/security Task;
5. cross-Task/cross-contract coherence review;
6. version closure/release qualification;
7. Fast Path;
8. stale identity/conflict/blocker recovery.

Each scenario must expose authority, Operation sequence/kinds, exact identity boundary, Assurance dimensions, durable evidence, recovery route and a non-substitution invariant.

## Dogfood subject

Dogfood the exact integrated v4 architecture/machine-contract subject at:

```text
sha: 21301c89dd48542238a06c6264cb715f33f0648d
```

Do not use the moving T-010 PR HEAD as dogfood subject. Recording dogfood evidence must not invalidate the evidence itself.

## Required dogfood assurance

- two independently durable blind first-pass reviews;
- materially different model systems/families/configurations sufficient for a declared model-diversity basis;
- fresh contexts reconstructing only from durable authority;
- no sibling conclusions consumed before each blind first pass is published;
- same coverage matrix for both passes;
- finding union, no majority vote;
- cross-challenge only after first-pass publication;
- factual/runtime conflicts routed to executable evidence;
- aggregate exact-subject-bound and compatible with T-009 machine semantics.

## Staged completion

### Stage A — author reference/protocol candidate

Create reference flows, dogfood protocol, machine-readable scenarios and focused regression.

### Stage B — repository-real validation

Run full `verify-standard` on exact T-010 candidate HEAD. Static inspection is not Validation PASS.

### Stage C — local model-diverse dogfood execution

A fresh local coordinator must obtain two blind model-diverse first passes and durable GitHub records. This is an executor/independence boundary and MUST NOT be simulated by the Builder context.

### Stage D — evidence closure

Add `SELF_DOGFOOD_EVIDENCE.md` containing only durable refs, identity/provenance/coverage/aggregation metadata and dispositions; do not copy hidden/private model scratchpad.

Any Stage D commit invalidates earlier PR-head CI/Review evidence; rerun exact-head repository validation.

### Stage E — Fresh Independent PR Review

Review the final exact T-010 PR HEAD after dogfood evidence is committed. Dogfood evidence does not replace this Review.

## Validation commands

The authoritative CI chain includes the existing verifier suite plus:

```text
python scripts/test_v40_reference_flows.py
```

The focused regression must fail if required scenario coverage is missing or if a reference flow violates v4 orthogonality/non-substitution declarations.

## Forbidden scope

- no migration/adoption policy (T-011);
- no T-012 Closure review;
- no T-013 Release Qualification/main integration;
- no event-v3;
- no second lifecycle/reducer/DAG;
- no majority-vote dogfood aggregation;
- no claiming two prompts from one continuing model/session as model diversity;
- no inventing Validation truth from review consensus.

## Completion

All eight scenarios + machine regression PASS → durable blind model-diverse dogfood evidence → evidence committed → final exact-head full verifier PASS → required Fresh Independent Review PASS → merge to `version/v4.0.0`.
