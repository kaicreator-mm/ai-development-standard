# ADS v4.18.0 — R Source Candidate / Release Qualification Evidence R0

**Current state:** `SOURCE_CANDIDATE_ONLY / EXACT_FINAL_VERSION_SHA=NOT_YET_FROZEN / RELEASE_RQ=NOT_RUN / MAIN_NOT_MERGED`. This is a planning and Release-input evidence ledger, **not** independent RQ, product scope expansion, human authorization, or release record.

## 1. Sources, scope and exact predecessor

| Subject | Current grounding |
| --- | --- |
| Version umbrella and native DAG | [#1322](https://github.com/kaicreator-mm/ai-development-standard/issues/1322): 5 Task Issues, native four-edge A∥B∥C→I→R |
| Product source | [#1320 Freeze](https://github.com/kaicreator-mm/ai-development-standard/issues/1320#issuecomment-6388802387), PRD blob `98772b4594caa44b2611853ae482132f7aefa36b` |
| L2 source | [#1321 Freeze](https://github.com/kaicreator-mm/ai-development-standard/issues/1321#issuecomment-6395575157), L2 blob `e3b5106c2fdaa8b2a0bbac5adb32b810fcbd51dd` |
| L2 Amendment | [A01](https://github.com/kaicreator-mm/ai-development-standard/issues/1321#issuecomment-6397761622): I creates new isolated v4.18 CI; historical verify-standard workflow blob stays unchanged |
| Source predecessor `main` | `a45644d734fdf94da3e6f9c3f90ffe4ce3c25fda` prior v4.17 source baseline; not an assertion that old v4.17 RQ transfers |
| Integrated pre-R exact version branch | `version/v4.18@2c627606b40f7c82120ae1a0d6736148fe0943e6`, after A/B/C/I fully integrated |
| R Task | [#1327](https://github.com/kaicreator-mm/ai-development-standard/issues/1327), native #1326 blocked_by CLOSED; JIT `task/v4.18-R-version-qualification`; R source metadata only |
| Final R/version candidate identity | `NOT_YET_FROZEN`; bind exact PR HEAD/tree after metadata and evidence are committed, source Review, then actual version-branch merge/currentness |
| Main / Tag / Public Release | `NOT_RUN`; no authorization from these source-only records |

The v4.18 standard change is restricted to safe planning guidance: Task Decomposition §13 one bounded SHOULD, existing Task DAG template, registered TDS Golden Reference G418-01..07, tests/manifest/new bounded CI, and version source identity. **No** new scheduler, executable `blocked_by` semantics, Report/schema family, automated Agent runtime, real permission authorization, required human approval step or measured performance gain.

## 2. Previously completed concerns and test provenance

| Concern | GitHub source and accepted evidence | Result scope |
| --- | --- | --- |
| A | PR [#1328](https://github.com/kaicreator-mm/ai-development-standard/pull/1328); independent Review PASS; two scoped CI SUCCESS | TDS §13; no new T13/T05A qualification |
| B | PR [#1329](https://github.com/kaicreator-mm/ai-development-standard/pull/1329); two CI SUCCESS; **independent R1 Review PASS** [#1329@6397234222](https://github.com/kaicreator-mm/ai-development-standard/pull/1329#issuecomment-6397234222), P0/P1/P2=0, P3=1, `review:recommended`; source concern had been integrated before optional Review was posted | Optional template planning only; independent Reviewer PASS is factual, not Release PASS |
| C | PR [#1330](https://github.com/kaicreator-mm/ai-development-standard/pull/1330); independent Review PASS; C standalone Python E1 7/7 true PASS, two prior CI SUCCESS | Seven source-only Pattern pairs; no physical multi-Agent proof |
| I | PR [#1331](https://github.com/kaicreator-mm/ai-development-standard/pull/1331) HEAD `20872bf31285dc050e42ccfa9d29100e3d274ed4`; independent R1 PASS and focused R2 PASS, P0/P1/P2=0; GitHub squash into version SHA `2c627606b40f7c82120ae1a0d6736148fe0943e6` | CI/manifest/integrated E1 owner; not R Release qualification |

I exact-HEAD CI: `verify-standard #40196419600` SUCCESS, `verify-github-structured-interaction #40196419601` SUCCESS, `verify-v418-planning #40196419506` SUCCESS on Linux **and Windows**. The latter ran v4.3 TDS 16/16, v4.2 wiring 8/8, v4.17 Golden 36/36, C v4.18 E1 7/7 and I combined v4.18 E1 5/5. The existing `.github/workflows/verify-standard.yml` blob `9fa6099f867b4ce68c0963fbd012f8970753c4d6` was retained; I source CI used a new dedicated workflow for v4.18. These are **exact I-subject source CI receipts**, not final R-candidate/whole-version qualification or real Host-runtime demonstrations. Exact-current source Review/CI must be re-evaluated after R metadata and final merge per release authority.

## 3. Historical regression — exhaustive 20-suite red inventory at R1 candidate

**No historical FAIL is declared PASS, waived, or automatically NOT_APPLICABLE.** Distinct independent R R1 [PR #1332@6398558462](https://github.com/kaicreator-mm/ai-development-standard/pull/1332#issuecomment-6398558462) executed a **repo-wide** comparison across all **161** \`scripts/test_*.py\` and \`tests/test_*.py\` suites against the source base \`2c627606b40f7c82120ae1a0d6736148fe0943e6\` and reviewed R1 HEAD \`a3fe8a7e929914169c798bc1f9da3bc1ccd7da35\` (Python 3.14.7; clean worktrees): **161/161 identical exit codes, discovery counts and FAIL/ERROR identity sets**. It also ran all **20** R1-head-red suites against qualified predecessor source \`main@a45644d734fdf94da3e6f9c3f90ffe4ce3c25fda\`: **20/20 have the same failure-ID set** there. This proves the failing identities predate v4.18, **not** that v4.18 may silently ignore them. Some assertion-detail text changes inside the same already-failing IDs due to candidate path/version differences; such changes remain visible to the actual Release applicability owner.

**Inventory completeness rule:** There are exactly **20 red suites = T13 + T05A (2 suites, three exact historic failing subtests) + 18 other already-red suites**. The earlier I R1 source-differential [#1331@6398033901](https://github.com/kaicreator-mm/ai-development-standard/pull/1331#issuecomment-6398033901) reported only 10 red within its deliberately **scoped 41-suite comparison**; it was never an exhaustive repo-wide inventory. The 161-suite evidence supersedes that *count* for R's historical applicability ledger, not the immutable I source test results.

### 3.1 Three exact historical pin subtests, within two complete test processes

| Source suite + exact failing subtest identity | Actually observed state on I and R candidates | Release-owner decision required |
| --- | --- | --- |
| \`scripts/test_v411_t13_role_conduct.py::RoleConductSectionPlacementTests.test_complete_owner_standards_match_reviewed_qualified_source\` (\`owner_path='standards/TASK_DECOMPOSITION_STANDARD.md'\`) | Full old suite \`EXIT=1\`, \`Ran 62\`; one original failing subtest | **UNKNOWN** until subtest-bound positive \`APPLICABLE|NOT_APPLICABLE\` decision under RELEASE_STANDARD §11 |
| Same T13 method (\`owner_path='standards/DEVELOPMENT_WORKFLOW.md'\`) | Second original failed \`owner_path\` subtest; 61 other T13 methods completely PASS | **UNKNOWN**, independently from first subtest |
| \`scripts/test_v410_t05a_shared_code_safety.py::ExactSubjectBindingTests.test_owner_blob_identities_are_pinned\` (\`owner='TASK_DECOMPOSITION_STANDARD.md'\`) | Full old suite \`EXIT=1\`, \`Ran 39\`; single original failing subtest; 38 other methods plus passing IQS/ICGS subtests remain applicable | **UNKNOWN**, independently from T13 |

The dedicated v4.18 Linux and Windows I integration test actually runs both unmodified complete old suites as subprocesses and observes **only** these three FAIL subtest identities, original raw \`EXIT=1\`, required \`Ran 62\`/\`Ran 39\`, no new FAIL/ERROR/SKIP/discovery loss. **Its own 5/5 PASS means "no NEW failures" only**; neither whole old suite is PASS. The frozen L2-D02a proposal allows consideration of only these three precise immutable-owner assertion applicability cases—not method-level, whole-suite or blanket Release waivers.

### 3.2 Eighteen other historically failing suites — all UNKNOWN pending Release owner

| Verified exact script path (18/18) | Observed failure identity / reviewer evidence at R1 HEAD | v4.18 Release applicability |
| --- | --- | --- |
| \`scripts/test_v410_owner_convergence.py\` | **6 FAIL** in independent 161-suite reviewer log; complete per-test names require log publication/positive owner inspection | **UNKNOWN** |
| \`scripts/test_v410_t07a_acceptance_projection.py\` | **2 FAIL** in reviewer log; exact per-test name detail not yet committed to ledger | **UNKNOWN** |
| \`scripts/test_v410_t07b_decision_record.py\` | **1 FAIL** in reviewer log; exact per-test name detail not yet committed to ledger | **UNKNOWN** |
| \`scripts/test_v411_central_wiring.py\` | **27 FAIL** in reviewer log, including existing \`composed_union\` subtests over VERSION/README/CHANGELOG/manifest; full IDs pending retained raw output | **UNKNOWN** |
| \`scripts/test_v411_merge_admission.py\` | **9 FAIL** in reviewer log; exact per-test names pending retained raw output | **UNKNOWN** |
| \`scripts/test_v48_integration_closure.py\` | FAIL \`test_c01_exactly_three_new_v48_machine_families\` | **UNKNOWN** |
| \`scripts/test_v48_registry_adoption.py\` | FAIL \`test_ra02_base_inventory_preserved_additively\` (predecessor v4.17 RA02 disposition is historical-only) | **UNKNOWN** |
| \`scripts/test_v49_integrated_dogfood.py\` | **17 FAIL** in reviewer log; full per-test identities pending retained raw output | **UNKNOWN** |
| \`scripts/test_v410_t08a_integration_runner.py\` | FAIL \`test_this_candidate_diff_stays_inside_the_registered_t08a_prefixes\` (\`Ran 61\`) | **UNKNOWN** |
| \`scripts/test_v411_i1122_self_declared_executor.py\` | ERROR \`test_section_8_1_1_keeps_the_two_input_classes_and_self_declares_attribution\` (\`Ran 20\`) | **UNKNOWN** |
| \`scripts/test_v411_t12_abc_conformance.py\` | Non-unittest verdict \`REGISTRY_OR_WRITESET_FAIL\`; **224 problems at v4.17 main → 237 at v4.18 R1 HEAD**, +13 candidate-path/identity entries, **same FAILED verdict**. This problem-count drift is a material adverse detail despite same identity; do not call identical output. | **UNKNOWN** |
| \`scripts/test_v410_t02b_machine_projection.py\` | FAIL \`test_no_new_state_dimension_or_registry\` (\`Ran 25\`) | **UNKNOWN** |
| \`scripts/test_v411_t05_event_authority.py\` | **5 ERROR IDs** (\`Ran 55\`): \`test_existing_owner_semantics_are_preserved\`, \`test_new_clauses_use_only_canonical_tokens\`, \`test_section_8_1_1_denies_rights_from_forged_markers\`, \`test_section_8_1_1_requires_the_durably_verified_authorization_source\`, \`test_section_8_1_1_separates_the_two_input_classes\` | **UNKNOWN** |
| \`scripts/test_v411_t08_human_denial_authority.py\` | **2 FAIL IDs** (\`Ran 22\`): \`test_owner_write_set_is_exactly_workflow_and_unique_test\`, \`test_t08_is_one_appended_section_and_prior_workflow_is_byte_identical\` | **UNKNOWN** |
| \`scripts/test_v411_t09_effect_boundary.py\` | FAIL \`test_exact_three_path_write_set_and_clean_tree\` (\`Ran 20\`) | **UNKNOWN** |
| \`scripts/test_v411_task_learning.py\` | **2 FAIL IDs** (\`Ran 17\`): \`test_exact_three_path_owner_write_set_and_clean_tree\`, \`test_preexisting_execution_architecture_is_byte_identical\` | **UNKNOWN** |
| \`scripts/test_v49_dogfood_audit_contract.py\` | **6 FAIL subtests** (\`Ran 12\`) of \`test_d08_frozen_authority_and_release_surfaces_unmutated\`, parameters \`read_only=scripts/test_v49_release_applicability.py\`, \`read_only_rebound=\` EXEC_ARCH/WORKFLOW/RELEASE_STANDARD/\`test_v49_gate_currentness.py\`/\`test_v49_execution_core.py\` | **UNKNOWN** |
| \`scripts/test_v49_manual_reference_flow.py\` | FAIL \`test_m01_every_doc_reference_resolves_at_candidate (ref='BOUNDED_SOURCE_REPAIR_CASES.json')\` (\`Ran 20\`) | **UNKNOWN** |

**Evidence-provenance and gap:** Per [R R1](https://github.com/kaicreator-mm/ai-development-standard/pull/1332#issuecomment-6398558462), all 20 scripts were actually red on v4.17 main and the R1 reviewed HEAD, and the reviewer identified all 20 suite paths plus the above failure families. The first eight legacy suites' *full method-level fail-header lists* were **not quoted** in the R1 comment; their numbers and partial class/subject summaries are faithfully disclosed as partial evidence, **not invented exact identities**. Before final Release RQ, obtain/publish their exact raw output/FAIL IDs; perform per-gate × subject positive \`APPLICABLE|NOT_APPLICABLE\` decisions on all 20 suite failure families, **not just T13/T05A**. The fact a suite is old or that no NEW red identity was introduced is not enough for \`NOT_APPLICABLE\`. Unknown relevance of any mandatory gate ⇒ RQ BLOCKED. No R Task scope authorization exists to mutate historical tests or broaden the original 3-subtest exception.

### 3.3 Reproducible entire-repository differential command and evidence requirements

At **each exact** predecessor/current candidate HEAD (including final post-R merge), enumerate independently all files matching \`scripts/test_*.py\` and \`tests/test_*.py\` (the R1 reviewer observed **161**), execute each file with its actual Python interpreter as a **separate** process using \`PYTHONDONTWRITEBYTECODE=1\`, retain complete raw stdout/stderr, exit code, \`Ran N\` method count where present, every \`FAIL:\`/\`ERROR:\` header and every JSON/non-unittest verdict. Compare 161/161 exact suite paths and discovery identities, not only an aggregate red count. Use \`git rev-parse HEAD\` before and after and require clean working tree. The command below is the **prescribed reproducible procedure**; the reviewer used read-only worktrees/Python 3.14.7 for the R1 comparison, but this snippet is **not** itself an assertion that the command was already executed:

\`\`\`python
from pathlib import Path
import json, os, subprocess, sys
files = sorted([*Path("scripts").glob("test_*.py"), *Path("tests").glob("test_*.py")])
assert len(files) == 161, f"Discovery changed: {len(files)}"
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
rows = []
for path in files:
    p = subprocess.run([sys.executable, str(path)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env, timeout=300)
    rows.append({"path":str(path), "exit":p.returncode,
                 "stdout":p.stdout or "", "stderr":p.stderr or ""})
Path("v418_regression_161_raw.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
print("TOTAL", len(rows), "RED", sum(r["exit"] != 0 for r in rows))
\`\`\`

This local output is an **unpublished file** until intentionally attached/reported with current SHA/test IDs in GitHub; do not claim that writing it locally itself creates durable ADS evidence. Prefer an out-of-tree evidence location or clean after capture, keep any secrets out of reports. Reproduce separately at v4.17 main and v4.18 version exact subject, then classify the 20 red test suites individually. The R1 review's broad differential is valid factual input but **not** the Release owner decision or the final candidate qualification.

## 4. Release gates, subject boundaries and owners

| Gate | Applicable v4.18 source subject / required evidence | Current truth |
| --- | --- | --- |
| Product and L2 source Freeze | Already issued, precise PRD/L2 blobs; A01 bounded CI-route amendment | PASS / FROZEN, subject to currentness |
| Native DAG / Task completion | Four GitHub dependency edges, A/B/C/I closed, R claim and final source closeout required | A/B/C/I DONE; R IN_PROGRESS |
| Current standard source and machine contracts | VERSION/README/CHANGELOG identity; TDS/template/G418 Golden registered and manifest; no public schema deltas | CANDIDATE in R Task, current exact R-source CI **NOT_RUN until run** |
| Required source Review | R's own source/whole-candidate independent Review distinct from Builder, exact HEAD/merged tree | **NOT_RUN** |
| Full regression and integrity | Existing canonical CI, new v4.18/Linux-Windows source suite, available historical negative gates | Previous I PASS; current R candidate **NOT_YET_RUN**, 20 inherited historically red suites disclosed |
| Historical pin applicability | Three precise subtests within T13/T05A plus 18 other historical red suites (20 total), with positive Release-owner gate × subject classification required | **UNRESOLVED / RQ BLOCKED pending owner** |
| Source Critical Journeys | Task source→Issue→Claim→native blocked_by→CI→Review→version branch source identity and amendment negative paths | Actual GitHub source evidence available; whole-version final readback `NOT_RUN` |
| Private Hidden Validation | Independently decide `APPLICABLE|NOT_APPLICABLE|UNKNOWN` from actual Product source-only change and Release authority; no fake runtime/secret probe | **NOT_DECIDED** |
| Packaging / artifact | Exact standard-manifest references, VERSION, documented source delivery; no deployed binary/runtime package in Product | Source artifact integrity candidate; exact final packaged/material verification `NOT_RUN` |
| Independent Release Qualification | Separate `READY|CONDITIONAL|BLOCKED|FAIL` bound to exact qualified SHA/tree and unresolved findings | **NOT_RUN** |
| main integration/Tag | No main merge until full-version RQ explicitly authorizes; Tag/public release separate | **NOT_AUTHORIZED** |

No changes to v3 Work Item/Intent/Event, v4/v5 Report Schema, protected authority, Agent runtime or mandatory automated scheduler. `REAL_NATIVE_CLAIM_AND_RELEASE_RUNTIME_NOT_PROVEN`, `REAL_HUMAN_DENY_E2E_NOT_PROVEN`, `REAL_TASKMETA_GITHUB_PUBLICATION_NOT_PROVEN`, `REAL_TALLY_GITHUB_ONLY_READER_FEEDBACK_NOT_PROVEN`. Source-only v4.18 product delivery does not automatically make externally implemented runtimes/version adoption qualified.

## 5. Required release handoff after R source branch merges

1. Independently review the **exact R PR HEAD** and all R-owned changed files; preserve adverse historic test findings and no protected Review/RQ substitution.
2. Confirm actual R version-branch squash/merge SHA and current tree; commit or track the exact source-version Candidate Freeze **only after** complete source branch is present. Metadata identity alone is not Freeze.
3. Complete the source entire-version validation, historical applicability matrix (positive/negative for all affected subjects), relevant Hidden/Critical Journeys/Packaging and Final Closeout. Bind actual command, executor capability, EXIT, source SHA and independently accepted evidence for every required gate.
4. Distinct Release owner executes `READY|CONDITIONAL|BLOCKED|FAIL` judgment. `UNKNOWN` on a required Gate ⇒ `BLOCKED`; no assumed PASS via PR or Green CI.
5. Only if qualified and current may integrate `version/v4.18` into `main` using exact source/currentness guard and confirm resulting Git SHA/tree. Tag/public Release require separate qualification.

**Current claim:** candidate documentation and finite source-level tests only. **Never:** entire Release PASS, three old full-suite PASS, 18 other historic-suite implicit waivers, real physical/Host PASS, accelerated elapsed-time measurement, downstream effective adoption or main merge.
