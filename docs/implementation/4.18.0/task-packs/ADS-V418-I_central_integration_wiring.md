# ADS v4.18.0 — Task Pack I

> **TASK_PACK_STATE:** FROZEN_PLANNING_CONTRACT / NOT_EXECUTION_PACK / NOT_SOURCE_CLAIM
> **Work Item:** [#1326](https://github.com/kaicreator-mm/ai-development-standard/issues/1326)
> **Frozen Product:** PRD blob `98772b4594caa44b2611853ae482132f7aefa36b` / #1320 Product Freeze
> **Frozen L2:** blob `e3b5106c2fdaa8b2a0bbac5adb32b810fcbd51dd` / #1321 L2 Freeze
> **Planning DAG:** `docs/implementation/4.18.0/TASK_DAG.md` snapshot; GitHub native Issue Dependencies own actual execution order

## Task identity, result and boundaries

- **Task ID:** ADS-V418-I
- **Goal:** Once A/B/C merge, create I-owned cross-source test, register both E1 tests in existing manifest and execute them through a new v4.18-specific CI workflow, preserving exact historic verify-standard workflow blob.
- **Integration target:** `version/v4.18`, never `main` before Release Qualification.
- **Risk:** high
- **Review policy:** required; a required independent Review must come from a genuinely distinct operator/context.
- **Agent freedom:** `F1_BOUNDED_IMPLEMENTATION`, fixed here; may be narrowed in an accepted JIT Execution Pack, never widened by executor.
- **L3/reference:** This pack's below bounded Tests/Contract/Implementation/Failure reference forms the minimal L3 for this source-only concern; no additional complex L3 artifact is necessary absent a new architecture UNKNOWN.

## Dependencies (live native Issue facts supersede this explanatory section)

native blocked_by A #1323, B #1324, C #1325; no source writing before all complete

## Allowed write-set

- standard-manifest.json
- .github/workflows/verify-v418-planning.yml NEW (A01-authorized I-owned dedicated E1 workflow; preserve historical verify-standard.yml byte-for-byte)
- tests/test_v418_integrated_planning_conformance.py NEW
- coverage/index ONLY if prior verification requires

## Forbidden scope

- .github/workflows/verify-standard.yml (pinned v4.9 owner must stay untouched)
- A/B/C-owned source except independently approved repair
- old T13/T05A tests, v4.17 Golden, release metadata

## Acceptance (falsifiable)

- [ ] All dependencies accepted and source integrated/current
- [ ] No shared wiring written in A/B/C workfronts
- [ ] Real dedicated v4.18 CI run executes both new tests and mandatory inherited source tests; existing pinned verify-standard job remains green
- [ ] Independent source Review; no fake historic all-PASS

## Explicit Task Pack Revision R2 — A01 frozen-architecture CI route

**Authority:** [#1321 A01 Architecture Amendment](https://github.com/kaicreator-mm/ai-development-standard/issues/1321#issuecomment-6397761622). The initial source-only PR #1331 CI proved that modifying historically pinned `.github/workflows/verify-standard.yml` caused v4.9 `test_v49_conformance_suite.py::C12CoverageManifest.test_c12_test_oracle_lane_discipline` failure (Git blob 9fa6099… expected). I Builder restored original pinned blob at its HEAD 5703bef… before changing this Task Pack. This controlled planning **revision** changes *only the CI file routing* from modifying existing workflow to creating `.github/workflows/verify-v418-planning.yml`; identity, outcomes, dependency graph, role/review policy, E1-only requirements, full historical T13/T05A subtest obligations and Release authority are unchanged.

This revision must be re-bound at source review: current version branch Task Pack blob must equal the revision recorded on Issue #1326; I's existing same-operator `SINGLE_WRITER_ADMISSION` Claim remains singular, not an opportunity for another incompatible claim. Integration base drift is planning-only with no change to A/B/C material writes; any other conflict requires source currentness reconciling. The qualified distinct I reviewer shall independently verify this amendment and actual GitHub CI before I merger.

## Tests → Contract → Implementation → Failure Handling → Reference

### Tests and exact evidence

- Original verify-standard.yml actual run unchanged **and** new verify-v418-planning.yml actual independent GitHub CI run; no owner blob divergence
- G418 unit + integrated suite
- Lane and Golden/wiring suites
- T13/T05A full per-subtest difference check
- v4.17 G01–G14 36 tests

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
