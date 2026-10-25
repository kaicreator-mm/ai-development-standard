# ADS v4.18.0 — Task Pack C

> **TASK_PACK_STATE:** FROZEN_PLANNING_CONTRACT / NOT_EXECUTION_PACK / NOT_SOURCE_CLAIM
> **Work Item:** [#1325](https://github.com/kaicreator-mm/ai-development-standard/issues/1325)
> **Frozen Product:** PRD blob `98772b4594caa44b2611853ae482132f7aefa36b` / #1320 Product Freeze
> **Frozen L2:** blob `e3b5106c2fdaa8b2a0bbac5adb32b810fcbd51dd` / #1321 L2 Freeze
> **Planning DAG:** `docs/implementation/4.18.0/TASK_DAG.md` snapshot; GitHub native Issue Dependencies own actual execution order

## Task identity, result and boundaries

- **Task ID:** ADS-V418-C
- **Goal:** Add optional G418 planning patterns and positive/negative E1 examples to canonical TDS reference, plus self-contained source-only test independent of unmerged A/B code.
- **Integration target:** `version/v4.18`, never `main` before Release Qualification.
- **Risk:** medium
- **Review policy:** recommended; a required independent Review must come from a genuinely distinct operator/context.
- **Agent freedom:** `F1_BOUNDED_IMPLEMENTATION`, fixed here; may be narrowed in an accepted JIT Execution Pack, never widened by executor.
- **L3/reference:** This pack's below bounded Tests/Contract/Implementation/Failure reference forms the minimal L3 for this source-only concern; no additional complex L3 artifact is necessary absent a new architecture UNKNOWN.

## Dependencies (live native Issue facts supersede this explanatory section)

none; only frozen L2 contract, no native A/B prerequisites

## Allowed write-set

- references/TASK_DECOMPOSITION_REFERENCE.md additive section
- tests/test_v418_planning_conformance.py NEW standalone

## Forbidden scope

- existing Golden corpus, G01–G14, historic tests
- normative standards, task-dag template, CI workflows, manifest
- I-owned cross-source test

## Acceptance (falsifiable)

- [ ] E1 cases cover G418-01..07 scenarios with concrete positive/forbidden pairs
- [ ] No real Host/Agent/Human approval or numeric savings fabricated
- [ ] Canonical registered TDS Reference remains Golden home; no duplicate registry owner
- [ ] No A/B unmerged source semantics assumed; standalone test runnable

## Tests → Contract → Implementation → Failure Handling → Reference

### Tests and exact evidence

- tests/test_v418_planning_conformance.py independent E1
- scripts/test_v43_task_decomposition.py
- scripts/test_v42_adoption_wiring.py
- tests/test_v417_golden_consistency.py
- full T05A anti-DRY/mandate corpus oracle

Use actual command/exit/HEAD, source impact and accepted CI results; if runtime is unavailable mark NOT_RUN and do not mint PASS. Historic T13/T05A run can EXIT 1 for exactly three earlier owner-identity subtests; compare complete *subtest identities* at integrated HEAD, not method-pass arithmetic. New failures, errors, unexpected skips or reduced discovery BLOCK. No fake full v4.10 integration success.

### Contract / behavior

Only the frozen L2 architecture and the above bounded outcome/allowed writes are authoritative. Product Option A: advisory dependency classification never grants Builder READY or changes actual native `blocked_by`, Claim, JIT, MI or effective writer.

### Implementation bounds

Issue/Task Pack are **WHAT**, not exact-base HOW. After admitted ready/current Task, controller selects one task branch JIT from current exact integration HEAD, constructs required Execution Pack or a qualifying documented fast path, emits one serialized accepted `DISPATCH_CLAIMED` and records valid work item state before any source modification. No implementation starts from this planning file alone.

### Failure/Blocker Handling

Missing native dependency/current Task, incorrect Claim or active conflicting Writer, material Product/L2 change, test regression, fake Host truth or non-current expected base => HOLD/BLOCK; write exact defect/currentness to owning Issue. Do not make a shadow Issue status source, change other Task's write-set, or edit main.

### Reference

- `standards/TASK_DECOMPOSITION_STANDARD.md`, `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, `standards/EXECUTION_PACK_STANDARD.md`, `standards/EXECUTION_ARCHITECTURE_STANDARD.md`, `standards/TASK_DAG_GOVERNANCE_STANDARD.md` (conditional SF authority), `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `standards/RELEASE_STANDARD.md`.
- Existing owner/source blobs shall be re-read at actual JIT integration HEAD. No historical SHA serves as a future write grant.

## Closeout

Report actual independently accepted scoped Review and Validation, source PR target version branch, merge SHA, Task Learning facts or NONE_MATERIAL. PR success is not version Release PASS.
