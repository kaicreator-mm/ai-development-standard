# ADS v4.12 — #1123 Task DAG R4 Write-Set Successor Candidate

> **STATE: WRITER-SCOPE AMENDMENT CANDIDATE, NOT FROZEN / NO EXECUTION AUTHORIZATION.** Distinct bounded successor to the actual Frozen R3 Task DAG blob `adc9e522f3b734a59898091945b9c7545530565a`. Do **not** edit the R3 file or assert this R4 source is already a native GitHub Task DAG. It adapts only missing self-declared actor/Owner-credential implementation scope after user-approved #1123 Product intake.

```ini
EVENT=ADS_V412_I1123_DAG_R4_AUTHOR_WRITESET_AMENDMENT
ISSUE=#1123
PREDECESSOR_PRODUCT_R3_BLOB=0bfbf782c8859e79df52c9b57904ad80bcd718e9
PROPOSED_PRODUCT_R4_DELTA_BLOB=e924fa29d8fe3c846eeb7f6ca41131609b19b0ad
PREDECESSOR_L2_R5_BLOB=68608ef6456334d627db1797ba2e023233c84ce7
PROPOSED_L2_R6_DELTA_BLOB=aede88044697ba45f712ecfa49f615ce48e8af58
FROZEN_DAG_R3_BLOB=adc9e522f3b734a59898091945b9c7545530565a
SOURCE_SCOPE_CANDIDATE_BLOB=6d783ecb8b02a61d4e2d60174e1a12832f27b948
VERSION=v4.12.0
IMPLEMENTATION_TASKS=5_UNCHANGED
RELEASE_CHECKPOINT=S06_TYPE_RELEASE_UNCHANGED
NATIVE_TASK_EDGES=4_UNCHANGED
NEW_TASK_ISSUES=0
NEW_REVIEW_OR_RELEASE_GATES=0
NEW_IDENTITY_SERVICE=0
DAG_AMENDMENT_CONTROLLER_ADMISSION=NOT_RECORDED
DAG_R4_FREEZE=NOT_RECORDED
PREDECESSOR_V411_RELEASE=NOT_QUALIFIED
NATIVE_CLAIMS=NONE
```

## 1. Delta-only graph: preserve original scheduling

```text
S01 ─┐
     ├─> S03 ─┐
S02 ─┘        ├─> S05 --[Release admission only]--> S06 type:release
S04 ──────────┘
```

The implementation DAG edges remain exactly **S01→S03, S02→S03, S03→S05, S04→S05**. S01/S02/S04 are source-disjoint initial implementation concerns; S03 follows the accepted S01/S02 contract; S05 integrates only after accepted S03/S04. S05→S06 is the existing **Release qualification prerequisite**, not a fifth native Builder Task dependency. Do not split into extra Actor Owner Issue, identity credential Gate, cross-version release checkpoint or "human signature service."

## 2. Source-write-set successor — permitted only after actual R4 owner admission

The table is a **PROPOSAL**, never actual accepted Task Claim or ALLOWED_CHANGES until Product/L2/DAG successor and Pack currentness are accepted:

| Task | Unchanged R3 owner | **New exact proposed file ownership (scope limited)** | Negative / integration boundary |
|---|---|---|---|
| **S01** | `standards/DEVELOPMENT_WORKFLOW.md`, `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` | `standards/EXECUTION_ARCHITECTURE_STANDARD.md`; `AGENTS.md`; `prompts/independent-review-bootstrap.md` (only real #1123 actor-credential/normal-process role/Claim contradictions, source-first comparison to v4.11 #1122) | No CAS weakening, removal of canonical admitted event vs raw quoted text check, old version migration rewrite, other prompt family, semantic Release/Assurance source |
| **S02** | `standards/TASK_DAG_GOVERNANCE_STANDARD.md`; `templates/task-dag.md` | **None** | No additional Reviewer/identity graph, no change to binding algorithm just for declarations |
| **S03** | `scripts/v412_scaffold_dag_check.py`, focused tests and uniquely named source-pinned fixture files only | **None** | Never re-use fake GitHub actor presence as proof of real tests or Claim |
| **S04** | `standards/PROJECT_ADOPTION.md`, uniquely owned examples only | **No additional standard file required**; add bounded prospective protocol compatibility/pinned consumer examples *within the existing owner path* | `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` remains outside write set; #1119 rolling compatible adoption stays future |
| **S05** | `standard-manifest.json`, `scripts/verify_standard.py`, `templates/GOLDEN_INDEX.md`, owned CI integration | `standards/ASSURANCE_PLAN_STANDARD.md`; `standards/RELEASE_STANDARD.md` **only exact actor-credential vs semantic Gate/Release applicability clauses**; selected existing `schemas/**` and `scripts/test_*` source-conformance assertions as explicitly enumerated in S05 current Task Pack after audit | Identity gate removal does not automatically remove source-true `CURRENT_OWNER_AUTHORITY` as *policy*; stronger Gate evidence and real Release §11.7 preserved; no wide schema migrations or duplicate metadata owner |

Other original R3 allowed paths, risk classification, Task concern descriptions, tests and failure handling remain in force. Any exact path not covered by R3 or this admitted R4 delta remains forbidden. S05 is not permitted to modify `standards/EXECUTION_ARCHITECTURE_STANDARD.md`; S01 is not permitted to modify `standards/ASSURANCE_PLAN_STANDARD.md` or `standards/RELEASE_STANDARD.md`. Both changes must come only after a lawful actual Task Pack Freeze/admission with these exact inputs.

**S06** remains `type:release` and owns only the release decision/qualification, not writing normative S05 implementation source. Existing v4.11 §11.7 accepts self-declared Release executors for the standards-only artifact; a Reviewer/test/CI/Release PASS still requires its factual predicate and exact subject. Avoid an unnecessary new Owner sign-off.

## 3. Review, atomic Claim and test impact

| Task | Existing Review Policy | #1123-targeted test oracles | Required validation |
|---|---|---|---|
| **S01** | `required` | A1123-01/02/04/05, L2-ID01–05; actor declaration recognized on same GitHub account, distinct GitHub account same declared actor not falsely independent, unadmitted quote rejected, CAS race still holds | Source exact normative clause impact + focused current Workflow/Interaction/Execution tests |
| **S02** | `required` | No new actor-auth tests; original paired anchor/DAG negative fixtures unchanged | Original narrow source review only |
| **S03** | `required` | Proven Git object identity vs fictitious agent proof remains separate | Actual checker test on its later lawful exact HEAD |
| **S04** | `recommended` | A1123-07, L2-ID09; older pin/protocol migration, same transport/declared distinct examples | Focused documentation/adoption conformance |
| **S05** | `required` | A1123-03/04/06/08/09, L2-ID05–10; remove actor-credential Owner check only where source proves it; retain objective assurance floor and external GitHub rule; no pretend Release PASS | Existing v4.11 #1122 checks as source baseline + new focused actual exact-HEAD tests where missing, one version-candidate integration regression when eligible |

**Actor provenance** under current merged v4.11 #1122 uses **self-declared logical** `actor_role/operator_kind/operator_id/session_ref`. No independent cross-session identity challenge or special GitHub Owner credentials. Existing `required` Review remains a substantive exact-head review of source, distinct **declared context**, findings and relevant tests. The original Reviewer need not open new credential-verification Session for a documentation-only Task.

**Technical truth continues unchanged**: native Task dependency edges must exist/read back before source Claim; Task allowed changes and current baseline correct; one serialized Claim writer/generation or real linearizable CAS; no duplicate source writers; protected GitHub branch checks actually enforced; real CI/host test exit and failures preserved; no stale SHA; any actual necessary protected-effect authority/consent cannot be inferred from declared agent identity.

## 4. Material DAG mutation and immutable records

- R3 DAG Git blob is unchanged and remains the historical Controller-frozen owner decision.
- R4 is a **successor source-write-set** change, not a live Issue graph rewrite. Its **five nodes and four native edges** are identical to R3. This can be admitted by existing Task DAG Controller as a bounded write-set amendment, **only after actual Product/L2 successor scopes are frozen**.
- Upon genuine R4 admission the successor/binding checkpoint should record `dag-mutation-record-v1` or existing appropriate owner-tracked amendment/lineage evidence as required by Task DAG Governance; only when an actual native Task graph exists does the Controller mutate/read back native Issue Dependencies. No fabricated past native issue.
- Before any implementation, the Task Pack index and each affected Pack must be **re-pinned to this actual frozen successor identity**. The current Pack candidates may describe proposed clauses but do not confer new writer privileges.
- v4.11 version `candidate/v4.11.0-aac1e120` is **Candidate Frozen only**, not v4.11 Release-qualified main. Existing #1023 V03/#1024 V04/#1025 R01/#1026 R02 must truthfully close or yield legitimate applicable successor qualifications first. No ancient-main Draft PR #1101/#1124 merge as a back door.

## 5. State

```ini
R3_DAG_FROZEN=UNCHANGED
R4_DAG_SOURCE_CANDIDATE=AUTHOR_PREPARED
R4_PRODUCT_DELTA_FREEZE=NOT_RECORDED
R6_L2_DELTA_FREEZE=NOT_RECORDED
R4_DAG_AMENDMENT_FREEZE=NOT_RECORDED
S01_S05_EXPANDED_WRITE_AUTHORIZATION=NONE_UNTIL_APPROVED
S04_PROTOCOL_ADOPTION_GUIDE=PROPOSED
V412_TASK_PACK_FREEZE=NOT_RECORDED
V412_SOURCE_IMPLEMENTATION=NOT_STARTED
V412_RELEASE=NOT_QUALIFIED
```

## 6. User-approved #1119 Option A — no new Task or edge, S04/S05 source scope only

**Product/L2 source bindings updated before this DAG delta:** Product R4 current candidate blob `e924fa29d8fe3c846eeb7f6ca41131609b19b0ad`; L2 R6 current candidate blob `aede88044697ba45f712ecfa49f615ce48e8af58`; #1119 approved Option A feasibility source blob `be7f0785083890b42aab5efb17d735df8a69adab`. User has **not** approved moving Class B automated cross-repository updater into v4.12. The preexisting Frozen Product R3/L2 R5/DAG R3 exact identities stay unchanged.

**Write-set extension to be admitted ONLY after Product/L2/DAG successor Freezes:**
- **S04** remains the sole `standards/PROJECT_ADOPTION.md`/uniquely owned adoption example writer. It adds the prospective opt-in `TRACK_LATEST_COMPATIBLE_STABLE` **selection preference** and immutable effective execution pin semantics, plus compatibility/consumer currentness examples. No additional paths, GitHub updater, other repository PRs or automatic pin mutation. `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` is **READ ONLY source owner**; its existing compatibility-record-v1 predicates are reused.
- **S05** gains exactly the **new unique files** `scripts/v412_ads_compatible_select.py` and `scripts/test_v412_ads_compatible_select.py` for bounded deterministic read-only qualified-release and material compatibility selection. It may register this script/test in its **already owned** manifest, verifier, Golden index and CI *if actual integration requires*. A source-pinned `compatibility-record-v1` currentness assertion may be exercised via the new dedicated test without changing existing schema. S05 remains the central conformance writer for previously proposed #1123 Assurance/Release deltas, but does not modify S04 adoption or S01 Interaction.
- **S01/S02/S03/S06 unchanged** by #1119; S03's paired Scaffold/DAG checker is not conflated with the qualified-release compatibility selector. The existing **four native Task edges** remain `S01→S03`, `S02→S03`, `S03→S05`, `S04→S05`. **Exactly five implementation Tasks**, plus one existing `type:release` S06 checkpoint; zero extra subtask/identity/Release Gates.
- No scheduler service, cross-repo catalog daemon, authorization credential checker or GitHub PR emitter is in the v4.12 write set. The real opt-in project updater / PR creator, activation and rollback execution remains **v4.13 Class B**. The v4.12 tool may output a proposed old/new pin and activation/rollback instructions; **output does not equal project mutation**.

### S04/S05 focused acceptance additions

| Check | Assigned Task | Expected real evidence |
|---|---|---|
| #1119 opt-in vs PINNED/manual default | S04 contract, S05 tests | without opt-in no upgrade proposal; always immutable execution SHA |
| qualified candidate commit and canonical manifest/version and actual Release Qualification | S05 | a self-asserted boolean/tag or mutable `main/latest` is rejected without source-verified release refs |
| material `compatibility-record-v1` consumer / authority / protocol behavior window | S04 source semantics + S05 test | #1123 actor/Review/Claim/Release semantic difference blocks auto-eligibility despite unchanged schema |
| exact old/new subject binding and stable release ordering | S05 | same semver/different SHA not collapsed, incomparable line or missing immutable object remains UNKNOWN |
| active Task/Claim or Frozen candidate | S04+S05 | latest suggestion never changes live effective `.dev-standard/VERSION` or old proof |
| selector physically read-only | S05 | exact executable test proves no project files/other repos modified, no external GitHub PR, real command+exit status |
| v4.12 Release gate | S06 | no fabricated mandatory adopter upgrade, no automatic v4.12 Release PASS |

**Source-writing preconditions remain unchanged:** Actual v4.11 predecessor Release qualified, Product R4/L2 R6/DAG R4 successor Freeze, corresponding current Task Pack with enumerated S05 unique files, native Task/Dependencies and accepted canonical Claim; qualified integration PR/CI/Review/Version Release predicates are still real. Author drafting the resolver contract gives no permission to implement it in the old-main planning branch.

```ini
I1119_OPTION_A_IN_R4_DAG_CANDIDATE=YES
I1119_OPTION_B_PROJECT_UPDATER_IN_V412=NO
REUSED_CORE_TASKS=5
TASK_DEPENDENCY_EDGES=4
S05_NEW_SCRIPT=scripts/v412_ads_compatible_select.py
S05_NEW_TEST=scripts/test_v412_ads_compatible_select.py
R4_DAG_FREEZE=NOT_RECORDED
REAL_PROJECT_UPDATES=0
```
