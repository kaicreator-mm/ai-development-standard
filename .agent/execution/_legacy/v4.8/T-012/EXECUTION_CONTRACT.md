# T-012 Execution Contract

## Exact subject

- Base: `257e95531551960cb163a3e20ab2b3d13f415d3c`
- Base tree: `1171de2c8afb08d6f793a258ffd0b586007e9dbf`
- Target: `version/v4.8.0`
- Branch: `task/v4.8.0-t12-469-dogfood`
- Task: `T-012` / Issue `#518`
- Task Pack blob: `10168f6ea2a1cb3b0ffff9c1a493b0904d82942f`
- L3 blob: `82f0ac808f423d861c030413046c2b2e689bfc1d`
- Source evidence planning anchor: `ai-development-standard#469@5925124956`

The Builder may implement only the bounded #469 evidence synthesis described by the Task Pack/L3. This pack does not authorize Product/L2/DAG, normative standards, schemas, model-routing policy, completed upstream Task artifacts, CI/workflows, T-014, Version Closure or Release authority changes.

## Builder write set

Exactly:

```text
docs/implementation/4.8.0/dogfood/469/**
```

Expected outputs are `EVIDENCE_MATRIX.md`, `EXECUTION_OBSERVATIONS.md` and `RESULT.md`. Another file under the same directory is permitted only when strictly evidence-supporting and subordinate to those outputs.

If a path outside the write set is required, stop. Do not widen the pack. A normative semantic/public-contract change may be recorded only as an evidence disposition routed to ordinary ADS evolution governance.

## Freedom / execution-profile contract

`agent_freedom=F1_BOUNDED_IMPLEMENTATION`.

The Builder may organize tables and wording inside the fixed evidence contract. It may not invent missing measurements, reinterpret Review/Validation authority, change source statuses, redesign routing policy, or infer a savings/universal model rule.

A bounded/lower-cost Builder is admissible only when current capability/profile/evidence and Task constraints make it hard-eligible. Provider/model identity is provenance only. If no bounded Builder is eligible, an eligible stronger Builder may execute the same F1 contract; the freedom ceiling does not widen.

Material ambiguity about source meaning/currentness, comparability, authority, write set or required disposition must stop/escalate rather than be guessed through.

## Dual currentness preflight

Before authoritative Builder work, both currentness dimensions must pass:

1. **Repository currentness** — live `version/v4.8.0` still equals base `257e95531551960cb163a3e20ab2b3d13f415d3c`; Task Pack/L3 blobs and branch match this pack; native #518 blockers remain zero.
2. **Source-evidence currentness** — re-read #469. If a material successor exists after planning anchor comment `5925124956`, stop with `BLOCKED_SOURCE_CURRENTNESS` and request an explicit evidence rebind before writing result artifacts.

Repository base and source-evidence currentness are independent. Passing one does not waive the other.

## Required evidence semantics

The candidate must preserve:

1. #469 is dogfood evidence, not standard authority;
2. exact source refs distinguish historical checkpoint, current consumed anchor and T-012's own observations;
3. source-reported external executions are not presented as T-012 executions;
4. Builder, independent Validator and Fresh Reviewer identities/results remain distinct;
5. `0`, `NONE_REPORTED`, `NOT_REPORTED`, `NOT_MEASURED`, `NOT_APPLICABLE` and `BLOCKED` remain semantically distinct;
6. provider/model identity is provenance only;
7. green Builder/Validation status does not erase later Fresh Review findings;
8. stale pack/L3/base/source evidence cannot silently rebind;
9. clarification/escalation/edit-test-loop/drift/rework fields are recorded only when exact evidence supports them;
10. T-012 records its own Builder execution metrics separately from source-task metrics;
11. economic/cost claims require comparable measured methodology; otherwise `ECONOMIC_SAVINGS=NOT_MEASURED`;
12. bounded successes do not establish a blanket strong→low-cost rule;
13. any `ADS_EVOLUTION_CANDIDATE` is only an input to ordinary ADS governance, never automatic adoption.

## Planning/implementation phase separation

Phase 1 may create/update only the T-012 Task Pack, task-scoped L3 and `.agent/execution/T-012/**`. It must not create or edit `docs/implementation/4.8.0/dogfood/469/**` result artifacts.

The result directory is Phase-2 Builder work after a separate accepted Builder dispatch/claim.

## Completion evidence

Builder terminal must bind:

- exact live base and Pack HEAD/tree;
- exact candidate HEAD/tree;
- exact candidate diff and write-set proof;
- exact #469 source anchor/currentness result consumed;
- BDF-01..BDF-12 evidence-matrix coverage;
- T-012 Builder profile/provenance and actually observed measurements;
- `git diff --check`, exact changed-path listing and `python -B scripts/verify_standard.py` results;
- `ECONOMIC_SAVINGS=NOT_MEASURED` unless the exact evidence includes a genuinely comparable measured methodology;
- Validation and Fresh Review as pending, not self-claimed.

Independent Validation is required on the exact candidate and consumed source evidence, followed by genuinely Fresh Independent Review on the exact validated candidate.
