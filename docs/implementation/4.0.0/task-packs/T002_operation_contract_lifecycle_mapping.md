# T-002 Task Pack — Canonical Operation Contract + Lifecycle Mapping

Issue: #74
Parent version: #72
Depends on: T-001 / #73 DONE
Baseline: `version/v4.0.0@abefb96ff1603e60add987c4c33983e4fe050211`
Integration target: `version/v4.0.0`
Review Policy: required
Risk: high
Validation scope: concern
Agent freedom: F1_BOUNDED_IMPLEMENTATION

## Goal

Define one reusable logical Operation contract and map the released v3.4 lifecycle into it without changing v3.4 execution semantics or prematurely implementing downstream Assurance/Exchange/Reducer schemas.

## Frozen inputs

- `docs/implementation/4.0.0/ARCHITECTURE_DECISION.md`
- `docs/implementation/4.0.0/TASK_DAG.md`
- v3.4 `DEVELOPMENT_WORKFLOW.md`
- v3.4 `EXECUTION_ARCHITECTURE_STANDARD.md`
- v3.4 `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`
- v3.4 `VALIDATION_STANDARD.md`
- v3.4 `RELEASE_STANDARD.md`

## Allowed changes

- `docs/implementation/4.0.0/OPERATION_CONTRACT.md`
- this Task Pack
- T-002 pointer in `docs/implementation/4.0.0/TASK_PACKS.json`

## Forbidden scope

- no v4 schema implementation;
- no event-v3;
- no Assurance finding/aggregation contract;
- no reducer/controller code or normative mapping changes;
- no weakening exact identity/Validation/Release semantics;
- no empty Operation materialization requirement for Fast Path.

## Acceptance

1. operation definition and operation instance are distinguished;
2. each Operation resolves one kind: PRODUCE/RESEARCH/ASSURE/DECIDE/CONTROL unless amended;
3. logical contract covers identity, context, authority, subject, inputs, actor contract, entry, outputs, assurance ref, acceptance, failure and successor relationships;
4. exact subject identity is required where truth depends on identity;
5. one routing projection is defined without flattening orthogonal truth dimensions;
6. common failure/recovery routes are explicit but do not become a replacement Gate state;
7. v3.4 lifecycle is fully mapped, including Product, Architecture, Task, Implementation, Integration, Candidate Freeze, Hidden Validation, Release Qualification and Repository Integration;
8. non-material execution steps are explicitly excluded from automatic Operation materialization;
9. GitHub reference materialization reuses existing durable objects instead of requiring duplicated giant payloads;
10. Fast Path uses operation elision, not reduced truth;
11. downstream T-003..T-009 ownership is explicit.

## Validation

Run the released repository verifier chain on the final exact PR HEAD. Static Web review is useful but is not executable Validation PASS.

## Review

Required Independent Review on final exact HEAD. Reviewer must specifically challenge over-generalization, hidden second state machines, authority duplication, lifecycle mapping gaps and Fast Path ceremony.

## Completion

Focused PR merged to `version/v4.0.0` after exact-head Validation PASS and required Independent Review PASS.
