# v4.1 Conformance Status / Version Closure Inputs

Status: **T08 REPAIRED IMPLEMENTATION CANDIDATE — new exact-SHA Validation and Fresh Independent Review REQUIRED**

This file is a durable *input* to Version Closure. It is not a Closure or Release Qualification verdict. Predecessor #363 Validation PASS and #364 Review CHANGES_REQUESTED apply only to predecessor SHA; neither transfers to this successor.

## Actual executable gate and evidence strength

`python scripts/test_v41_execution_foundation_conformance.py` runs seven **real, existing** T01–T07 owner suites using the current checkout's `sys.executable` and absolute script paths, then runs T08's illustrative integrated matrix/direct schema-owner checks. These seven include the contract suite's historical v4 Dispatch/Validation Report/Execution Pack payload fixtures, Dependency/Toolchain's risk-exception checks, Git exact-SHA/local-authority/cleanup checks, Config/Secrets checks, Workspace/Artifact producer/promotion checks, External-System BLOCKED/fidelity/retry checks, and actual adoption wiring. `scripts/test_verify_standard.py`, already invoked by repository `verify-standard` CI, calls this integrated T08 runner and also tests that a material owner-standard mutation in an isolated copied repo makes the integrated gate FAIL. This is not merely a separately green T08 oracle.

| Concern | Executable input | Claim boundary |
|---|---|---|
| historical compatibility | actual T01 owner contract suite: old Dispatch/Validation Report/Execution Pack, with and without optional v4.1 refs | additive; no historical reinterpretation |
| Context/Toolchain/Config | actual T01/T02/T04 suites + direct schema checks and Node/npm/non-Node examples | context is non-authoritative; local tools cannot rewrite repository truth |
| risk exception | actual T02 schema checks + accepted-risk-not-PASS/remediation negatives | disposition cannot grant PASS or prove remediation |
| Git/workspace | actual T03/T05 tests + local/unpushed task-claim, rewritten exact SHA and unknown-ownership cleanup negatives | local branch is not live Issue; no old evidence reuse or destructive unowned cleanup |
| artifacts | actual T05 tests + cache/build-output/promotion matrix requiring source/build refs | producer/build/identity binding is modeled; no real release artifact qualification |
| external | actual T06 tests + unavailable/NOT_RUN, sandbox/write, project-defined fidelity and overall deadline negatives | provider labels extensible; no real production/provider or higher-fidelity PASS |
| adoption and Fast Path | actual T07 suite + non-material Fast Path positive | no optional-contract adoption by symmetry |
| evidence separation | Task/Review -> Release READY negative | T08 cannot issue Release or Closure verdict |

The T08 example evaluator is a **supplementary deterministic conformance model**, not a replacement for the real owner suites, a real external provider, real artifact production or a full project test strategy. The custom fidelity/deadline examples lock the forbidden inferences for their declared toy tuples; actual project-defined equivalence/retry policy still belongs to the project/external owner.

## Required successor gates

1. On current successor exact HEAD, run `python scripts/test_v41_execution_foundation_conformance.py`; confirm all seven owner suites actually executed and the expanded matrix passes.
2. Run `python scripts/test_verify_standard.py` and `python scripts/verify_standard.py`; confirm the isolated copied-repository owner-weakening adversarial regression *fails its mutated child run as designed* while the parent suite passes.
3. Bind tested SHA, live version base, Python/platform, command/exit results and clean worktree to new exact-subject Validation. Missing required environment remains BLOCKED/NOT_RUN, not guessed PASS.
4. Obtain a genuinely NEW Fresh Independent Review for the successor HEAD, including all #364 P1/P2 findings and exact five-file Task Pack write-set.
5. If both gates PASS and currentness is safe, expected-head merge to `version/v4.1.0`; only then hand these bounded inputs to a **separate** Version Closure / Release Qualification authority.

## Non-verdicts

- `RELEASE_READY = NOT_DECIDED_HERE`
- `VERSION_CLOSURE = NOT_EXECUTED_HERE`
- `HIDDEN_VALIDATION = NOT_CLAIMED_BY_T08`
- `REAL_PRODUCTION_EXTERNAL_EXECUTION = NOT_CLAIMED_BY_T08`
- `MULTI_PLATFORM_PACKAGE_INSTALL = NOT_CLAIMED_BY_T08`

No test-only success, CI success or supplementary fixture result can be promoted to higher-fidelity/Release evidence by inference.
