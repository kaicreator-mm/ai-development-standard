# T-001 Task Pack — Authority, Vocabulary and Compatibility Freeze

Task: T-001
Issue: #73
Parent version: #72
Integration target: `version/v4.0.0`
Released baseline: `7ebaf66cba8fdc3a672e9b1d7fe9bd9e730a3805`
Review Policy: required
Risk: critical
Validation scope: concern
Agent freedom: F3_ARCHITECTURE_REQUIRED
Execution Pack: not required — planning/architecture standards task

## Goal

Freeze the v4 terminology, authority boundaries and v3.4 compatibility contract so all downstream Tasks share one durable architecture authority.

## Inputs

- #71 `V4_DRAFT_ARCHITECTURE_V0`;
- #72 v4 version contract;
- released v3.4 standard at the exact baseline above;
- current normative lifecycle/execution/work-item/interaction/validation/release/model-usage authorities.

## Required outputs

1. `docs/implementation/4.0.0/ARCHITECTURE_DECISION.md`;
2. `docs/implementation/4.0.0/TASK_DAG.md`;
3. `docs/implementation/4.0.0/TASK_PACKS.json`;
4. this Task Pack;
5. exact-head validation evidence and required Independent Review result in GitHub.

## Tests / checks

- architecture decision contains one lifecycle + one canonical Operation Protocol + one routing model + orthogonal truth dimensions;
- no flat-state regression;
- Assurance Plan is a partial-order/DAG, not a universal fixed pipeline;
- Review Policy/Mode/Coverage/Independence/Aggregation are separated;
- context/model/executor/evidence independence are separated;
- majority-vote correctness is prohibited;
- multi-model agreement is not Validation evidence;
- v3.4→v4 compatibility table names all hard invariants retained or generalized;
- Fast Path remains reduced-operation rather than reduced-truth;
- Task DAG and Issue mapping are recoverable from durable facts;
- capability fallback for missing native Issue Dependency mutation is explicit.

## Allowed changes

```text
docs/implementation/4.0.0/**
```

## Forbidden changes

```text
standards/**
schemas/**
templates/**
scripts/**
VERSION
```

Those belong to downstream Tasks.

## Failure handling

If a contradiction with released v3.4 authority is discovered, record it explicitly and keep T-001 non-PASS until resolved. Do not silently reinterpret v3.4.

If repository-real `verify-standard` cannot be executed from the Web environment, publish an exact-HEAD Validation handoff and do not claim PASS.

Builder context MUST NOT self-assert required Independent Review PASS.

## Completion

T-001 completes only after the candidate files satisfy required exact-head validation, a fresh independent reviewer returns PASS for the same exact HEAD, and the Task PR merges to `version/v4.0.0`. At that point `ARCHITECTURE_DECISION.md` becomes the frozen v4 planning authority for T-002..T-013.
