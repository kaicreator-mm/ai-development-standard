# ADS v4.16.0 — T07 integrated source and Release Qualification ledger

**Status:** SOURCE CANDIDATE ONLY / RELEASE QUALIFICATION NOT_RUN  
**Task:** [#1271](https://github.com/kaicreator-mm/ai-development-standard/issues/1271)  
**Frozen Product/L2/DAG:** [#1261](https://github.com/kaicreator-mm/ai-development-standard/issues/1261)  
**Current pre-T07 immutable integration base:** `version/v4.16@595598a2da31178fa4c0db39981796f58cf273c5`  
**Admitted Builder:** [Claim #1271@6359804245](https://github.com/kaicreator-mm/ai-development-standard/issues/1271#issuecomment-6359804245)  
**Prohibited:** main merge, release tag, VERSION or CHANGELOG bump before actual qualified source closure and separate Release authority.

## 1. Qualified inputs and immutable dependency chain

| Task | Existing version source result | T07 reuse |
|---|---|---|
| T01 #1265 | Closed; strict `ads/github/v5:report` Schema published | C01, C06–C10 |
| T02 #1266 | Closed; source-constrained physical metric/cost/clock, 71 fixtures | C02–C05, C12 |
| T03 #1267 | Closed; PR #1291 exact H `ec7e3eabcc1ebe0af6d8b4c76bfb6d0eefaa9b59` → version integration `595598a2da31178fa4c0db39981796f58cf273c5` | C01, C06–C09, v3/v4/v5 mixed reader |
| T04 #1268 | Closed; applicability / comparative economics / Evolution reuse | C11, C13, C14 |
| T05 #1269 | Closed; Web-first and Validator native writeback boundary | C15, C16 |
| T06 #1270 | Closed; existing Agent selection/delegated effect owner crosswalk | A03, G09–G12 |

T03 R1 pin-mismatched Validator Claim and Review BLOCK remain immutable historical. T03 R2 separate correctly pinned Validator [#1267@6359505586](https://github.com/kaicreator-mm/ai-development-standard/issues/1267#issuecomment-6359505586) PASSED (127 tests, Python 3.14.7), independent R2 Reviewer [#1267@6359709623](https://github.com/kaicreator-mm/ai-development-standard/issues/1267#issuecomment-6359709623) PASSED P0/P1/P2=0; no source code fix was required, only the admission path. Do not equate PASS at old R1 Claim with accepted R2 Claim.

## 2. Executable C01–C16 and A03/G09–G12 source closure

The **single machine-checkable** contract is [`tests/fixtures/v416/t07/integration_manifest.json`](../../../tests/fixtures/v416/t07/integration_manifest.json): **21 acceptance groups** mapped to the six real T01–T06 Python test entrypoints, and **five historical regression suites**. `scripts/test_v416_t07_integration.py` checks that mapping, source/fixture existence, original SHA-1 Git blobs of v3/v4/v5 schemas and external gates, then **executes all 11 real suites**. It requires an explicit immutable HEAD, clean checkout and all underlying unittest exit codes/parsed method counts; a skipped, missing or failed suite blocks source conformance. Separate `--run` is deliberately mandatory: manifest-only checking cannot qualify execution.

Commands on clean detached exact PR HEAD, `core.autocrlf=false` (avoid native CRLF corruption):

```sh
python3.14 scripts/test_v416_t07_integration.py --expected-sha <EXACT_T07_PR_HEAD> --run --json-out /tmp/ads-v416-t07-source-receipt.json
```

On Windows, use `py -3.14 scripts/test_v416_t07_integration.py --expected-sha <EXACT_T07_PR_HEAD> --run --json-out C:/Temp/ads-v416-t07-source-receipt.json`. A result of `SOURCE_CONFORMANCE_PASS_ONLY` is limited to exact tested standards-source behavior. The generated file contains exit codes, methods executed, individual bounded log digests, pinned HEAD and remains local; publish actual receipt/exit summary on Issue #1271 after an admitted independent Validator Claim. If no local environment or required dependencies are available, set `NOT_RUN/BLOCK`, never infer from GitHub generic docs CI.

Coverage facts are reproducible but narrower than implementation integration:
- C01/C06–C10: strict v5 report-only schema, source-null Attempt, immutable correction and observational reader; old v3/v4 schema bytes unchanged
- C02–C05/C12: physical retry, billing scope, overlapping costs and uncertain clocks from **supplied deterministic source fixtures**; no authenticated provider invoice or wall-clock witness
- C11/C13/C14: candidate experiment/effectiveness and established Task Learning owner; no new optimizer or normative auto-promotion
- C15/C16: bounded Web/Local handoff and source evidence shape; no GitHub native authenticated permission acceptance merely from fixtures
- A03/G09–G12: delegated Tool/Effect authority intersection and stale/late callback fail-closed examples, **not** an actual Host/Provider invocation


### R2 validation-runner integrity repair (after R1 BLOCK)

The independent exact-H R1 [BLOCK #1271@6360941918](https://github.com/kaicreator-mm/ai-development-standard/issues/1271#issuecomment-6360941918) identified three P1 and one P2 omissions in the first T07 runner. R2 implements, without changing any historical normative Schema:

- A built-in fixed `EXPECTED_SUITES` table binds all 11 canonical **suite IDs to their exact Python entrypoint and owning fixture**, disallowing a test/fixture swap while preserving IDs
- An immutable `EXPECTED_SCHEMA_PINS` three-path map fixes both actual required Schema paths and independently recorded original Git blob hashes, rejecting editable alternative self-selected pins
- `EXPECTED_GROUPS` binds the exact full 21-group C01–C16/A03/G09–G12 ownership relationship, not just a partial subset
- Each subprocess is wrapped with actual `unittest.TextTestRunner.run` observation, providing real `TestResult.testsRun`, skip/error/failure and unexpected-success evidence through an off-repository temporary audit. Text such as `Ran 99 tests in …` is **never** used to count tests. Zero executed methods or **any skipped tests** fail closed
- `--self-test` executes **8 integrity controls**: suite command substitution, fixture substitution, Schema SHA substitution, Schema path substitution, C01 owner substitution, stdout-only fake, 100%-skipped unittest, and a real positive control. This is an actual runtime probe, not a mock of `audited_suite`

**R2 physical source qualification remains NOT_RUN until independently executed** at a fresh exact R2 SHA with `py -3.14 scripts/test_v416_t07_integration.py --self-test` and the full `--run --expected-sha` commands. The old exact-H Python 149/149 real suite result remains truthful historical evidence but **does not transfer** across this repair. Generic CI cannot replace either new R2 test run. A separate exact-H independent Reviewer must verify and dispose P1×3/P2×1 before version merge. No premature VERSION/CHANGELOG, main, tag or Release PASS.


## 3. Release Gate ledger (immutable facts only)

| Gate | Current status | Required actual next evidence |
|---|---|---|
| Integrated full source regression | NOT_RUN | Python 3.14 exact-H receipt for all 11 suites, including 21 acceptance groups, plus independent validation |
| Hidden Validation | NOT_RUN | Locate applicable pack with exact test subject/runner/secret handling; if unavailable report NOT_APPLICABLE/NOT_RUN with reason and approved scope owner, **not fabricated PASS** |
| Critical Journeys | NOT_RUN | Source-only C01–C16/A03/G09–G12 negative/positive integrated qualification; disclose unavailable native E2E separately |
| Packaging/source artifacts | NOT_RUN | Verify exact SHA/tree, schemas, manifest docs links, VERSION/CHANGELOG consistency, no private/source credentials |
| Independent composed-version Review | NOT_RUN | Fresh separate WEB_REVIEWER against exact T07 PR H and any required findings |
| Release Qualification | NOT_RUN | Independent RQ based on current complete gate ledger and explicit applicability/exception decisions |
| `VERSION` and `CHANGELOG.md` | NOT_READY | **Currently VERSION=4.15.0**. Edit only under T07 contract's conditioned qualified version closure, with independent review of the delta |
| Main integration and tag | NOT_RUN | Need separate qualified release authority, exact-main base currentness and explicit permission; version merge alone is insufficient |

**Strict boundary:** `REAL_TASKMETA_GITHUB_TALLY_E2E=NOT_RUN` ([#1210](https://github.com/kaicreator-mm/ai-development-standard/issues/1210)), `REAL_CONTROLLER_HOST_DEMO=NOT_RUN` ([#1231](https://github.com/kaicreator-mm/ai-development-standard/issues/1231)), `GITHUB_NATIVE_PUBLISHER_ACL=NOT_RUN`, `AUTHENTICATED_PROVIDER_CLOCK_AND_BILLING=NOT_RUN`. These are external and deferred, **not source-qualification PASS**, and not new source Release Gate unless qualified Product/L2 explicitly made them source-release blocking. See frozen source-first disposition.

## 4. Predecessor, branch and migration

- The present main branch is the former v4.14 pin. The v4.15 source integration PR [#1211](https://github.com/kaicreator-mm/ai-development-standard/pull/1211) remains **DRAFT**; it may not be treated as Release-qualified or merged implicitly.
- The v4.16 version branch includes the qualified v4.15 source candidates in ancestry. Its own source closure must explicitly distinguish **cumulative version source payload**, historical predecessor delivery, compatibility and Release scope, and not pretend that main is already on v4.15.
- The opt-in v5 reader is **not** the effective writer default or a native GitHub authority grant before an authorized adopted ADS pin; legacy v3/v4 paths remain as historically frozen.
- v4.17 research C08 and R7 proposals are **out of v4.16 scope** and not closure blockers.

## 5. Required next transition

1. Admitted independent local/CI validation runs the **exact T07 PR HEAD** with Python 3.14, supplies genuine raw exits and source receipt.
2. Independent Reviewer inspects candidate delta, source verification and release gate boundaries (P0/P1/P2); repair only new real findings.
3. Only source-verified and review-qualified T07 changes may be merged into `version/v4.16`; the T07 Task is NOT_DONE until release-qualification acceptance is separately recorded per its critical gate contract.
4. Version owner and independent Release authority assess Full Regression, hidden applicability, Critical Journeys, Packaging, effective permission and predecessor; only an actually qualified release may set VERSION/CHANGELOG and decide main/tag. Unverified gate or conflicted authority is BLOCKED/UNKNOWN, not a waiver by default.
