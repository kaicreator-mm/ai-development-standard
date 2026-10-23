# ADS v4.16.0 — T07 integrated source and Release Qualification ledger

> **Currentness boundary (A03, source documentation only).** This is a registered historical T07 implementation/validation design ledger, not the latest GitHub release decision or an adoption pin. Its archived status table and original next steps retain real prior-stage facts; they are not current gate outcomes. For current `VERSION`, exact candidate SHA/tree, original failure/repair lineage, authoritative gate applicability, Freeze and independent RQ, read the ordered native events of [Issue #1271](https://github.com/kaicreator-mm/ai-development-standard/issues/1271). At the prior frozen candidate `2df2825e47a81ca1b1306e8899d55c49a7a8c776`, RQ was **CONDITIONAL**, not READY; later SHA changes invalidate that qualification for successors until independently re-run. External task-meta/Tally #1210 and Controller/Host #1231 remain separately unproven and are never inferred to PASS from source evidence.

**Status:** HISTORICAL T07 source-preparation/R2 evidence ledger — **not the current Release Qualification verdict**  
**Task:** [#1271](https://github.com/kaicreator-mm/ai-development-standard/issues/1271)  
**Frozen Product/L2/DAG:** [#1261](https://github.com/kaicreator-mm/ai-development-standard/issues/1261)  
**Historical pre-T07 immutable integration base (at original authoring):** `version/v4.16@595598a2da31178fa4c0db39981796f58cf273c5`  
**Admitted Builder:** [Claim #1271@6359804245](https://github.com/kaicreator-mm/ai-development-standard/issues/1271#issuecomment-6359804245)  
**Historical guard at original authoring:** main merge, release tag and unreviewed VERSION/CHANGELOG bump were prohibited. Later A02 created a reviewed `4.16.0` *candidate identity*, not an effective release; consult #1271 for all subsequent gate and integration decisions.

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

**Historical R2 pre-execution requirement (subsequently executed under independent admission, not a current NOT_RUN gate):** a fresh exact R2 SHA required `py -3.14 scripts/test_v416_t07_integration.py --self-test` and the full `--run --expected-sha` commands. The previous R1 exact-H Python 149/149 result remains historical and was not transferred across this repair. Actual R2 source validation at its then-current SHA was recorded at [#1271@6361803791](https://github.com/kaicreator-mm/ai-development-standard/issues/1271#issuecomment-6361803791); a later independent final integrated-source run is recorded at [#1271@6364342194](https://github.com/kaicreator-mm/ai-development-standard/issues/1271#issuecomment-6364342194). Generic CI could not replace the R2 test run. The separate R2 Reviewer later disposed P1×3/P2×1 in [#1271@6362426065](https://github.com/kaicreator-mm/ai-development-standard/issues/1271#issuecomment-6362426065). These are historical milestones, not a current main/tag/Release PASS.


## 3. Archived pre-A02 Release Gate snapshot (historical facts only)

**Do not use this table to determine present release eligibility.** Every status below is the state when this source-preparation ledger was first authored, before A02, final integrated validation, composed review, Freeze and independent RQ. The authoritative later immutable records are the ordered GitHub events on [T07 #1271](https://github.com/kaicreator-mm/ai-development-standard/issues/1271), including original frozen candidate [#6364740861](https://github.com/kaicreator-mm/ai-development-standard/issues/1271#issuecomment-6364740861) and independently qualified **CONDITIONAL** RQ [#6365024336](https://github.com/kaicreator-mm/ai-development-standard/issues/1271#issuecomment-6365024336) at exact source `2df2825e47a81ca1b1306e8899d55c49a7a8c776`. An A03 successor does **not** inherit those results and must be requalified by its own exact-SHA GitHub records.

| Gate | Historical status at original authoring (not current) | Original required evidence |
|---|---|---|
| Integrated full source regression | NOT_RUN | Python 3.14 exact-H receipt for all 11 suites, including 21 acceptance groups, plus independent validation |
| Hidden Validation | NOT_RUN | Locate applicable pack with exact test subject/runner/secret handling; if unavailable report NOT_APPLICABLE/NOT_RUN with reason and approved scope owner, **not fabricated PASS** |
| Critical Journeys | NOT_RUN | Source-only C01–C16/A03/G09–G12 negative/positive integrated qualification; disclose unavailable native E2E separately |
| Packaging/source artifacts | NOT_RUN | Verify exact SHA/tree, schemas, manifest docs links, VERSION/CHANGELOG consistency, no private/source credentials |
| Independent composed-version Review | NOT_RUN | Fresh separate WEB_REVIEWER against exact T07 PR H and any required findings |
| Release Qualification | NOT_RUN | Independent RQ based on current complete gate ledger and explicit applicability/exception decisions |
| `VERSION` and `CHANGELOG.md` | NOT_READY | **At this pre-A02 snapshot VERSION was 4.15.0**. A separately admitted and independently reviewed A02 later prepared `VERSION=4.16.0` at frozen predecessor `2df2825e…`; read the active source SHA and later #1271 events for current identity, not this historical row |
| Main integration and tag | NOT_RUN | Need separate qualified release authority, exact-main base currentness and explicit permission; version merge alone is insufficient |

**Strict boundary:** `REAL_TASKMETA_GITHUB_TALLY_E2E=NOT_RUN` ([#1210](https://github.com/kaicreator-mm/ai-development-standard/issues/1210)), `REAL_CONTROLLER_HOST_DEMO=NOT_RUN` ([#1231](https://github.com/kaicreator-mm/ai-development-standard/issues/1231)), `GITHUB_NATIVE_PUBLISHER_ACL=NOT_RUN`, `AUTHENTICATED_PROVIDER_CLOCK_AND_BILLING=NOT_RUN`. These are external and deferred, **not source-qualification PASS**, and not new source Release Gate unless qualified Product/L2 explicitly made them source-release blocking. See frozen source-first disposition.

## 4. Predecessor, branch and migration

- At the time this source-preparation ledger was authored, main was the former v4.14 pin. The v4.15 source integration PR [#1211](https://github.com/kaicreator-mm/ai-development-standard/pull/1211) remains **DRAFT**; it may not be treated as Release-qualified or merged implicitly.
- The v4.16 version branch includes the qualified v4.15 source candidates in ancestry. Its own source closure must explicitly distinguish **cumulative version source payload**, historical predecessor delivery, compatibility and Release scope, and not pretend that main is already on v4.15.
- The opt-in v5 reader is **not** the effective writer default or a native GitHub authority grant before an authorized adopted ADS pin; legacy v3/v4 paths remain as historically frozen.
- v4.17 research C08 and R7 proposals are **out of v4.16 scope** and not closure blockers.

## 5. Historical next-transition plan (subsequently executed/superseded)

This checklist records the original plan at R2 authoring time. It is **not** a live queue. The final source Validator, composed Reviewer, Freeze and independent CONDITIONAL RQ later reported through GitHub #1271. New A03 candidate work is separately governed; do not infer READY, a new Freeze or completed main integration from this historical sequence.

1. Admitted independent local/CI validation runs the **exact T07 PR HEAD** with Python 3.14, supplies genuine raw exits and source receipt.
2. Independent Reviewer inspects candidate delta, source verification and release gate boundaries (P0/P1/P2); repair only new real findings.
3. Only source-verified and review-qualified T07 changes may be merged into `version/v4.16`; the T07 Task is NOT_DONE until release-qualification acceptance is separately recorded per its critical gate contract.
4. Version owner and independent Release authority assess Full Regression, hidden applicability, Critical Journeys, Packaging, effective permission and predecessor. Version identity can be prepared under a separately admitted Task amendment (A02); **a candidate VERSION is not a Release verdict**. Final main/tag integration still follows the separately current Release qualification authority. Unverified gate or conflicted authority is BLOCKED/UNKNOWN, not a waiver by default.
