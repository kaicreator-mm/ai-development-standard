<!-- v4.11 Task Pack CANDIDATE ONLY; author=#970@6094572750; product=#943, L2=#954, DAG=#966; not frozen; no Builder/Claim authority -->

## V411-T04 — source-bound immutable-Task-Pack-ready DRAFT (author only)

```ini
PACK_DRAFT=SOURCE_BOUND_READY_FOR_INDEPENDENT_REVIEW
AUTHORSHIP_TASK_ISSUE=#970
INTENDED_FUTURE_PATH=docs/implementation/4.11.0/task-packs/V411-T04_reuse_first_source_license.md
TASK_ID=V411-T04
ONE_CONCERN=REUSE_FIRST_SOURCE_LICENSE
FROZEN_PRODUCT=#943@6084264198
PRODUCT_COMMIT=34df09a2433aec5523ab80c90e885f6d9fc78803
PRODUCT_PRD_BLOB=d30f202e8ea662731ff8a4f2ad1ad88cfc5bb179
FROZEN_L2=#954
L2_COMMIT=f1fc21be366579cbeafa98217b52e106a55b41a5
L2_BLOB=c0fa361474996a0626c63e93574a284ae3eb8d91
FROZEN_DAG=#966
DAG_HEAD=26fc83911185675bdea3c540df6df15c0241402b
DAG_BLOB=9866d35ae1512b156cfdc94cc01aec2fa897f3e6
CURRENT_INSPECTED_QUALIFIED_MAIN=b9461d48d902a2c7c00adff6746afc7a02a0ac3e
PACK_CONTROLLER=#967
SOURCE_PREFLIGHT=#963@6094406584
FROZEN_DAG_PREDECESSORS=NONE
RISK=medium
REVIEW_POLICY=required
L3_REQUIRED=YES
EXECUTION_READY=NO
NATIVE_TASK_ISSUE_AND_DEPENDENCIES=NOT_MATERIALIZED
PACK_FREEZE=NO
BRANCH_SOURCE_PR_MERGE=NONE_BY_AUTHOR
BUILD_HOST_TESTS=NOT_RUN_BY_AUTHOR
RELEASE_HIDDEN_RQ=NOT_RUN
```

### 1. One concern, actual source and acceptance boundary

**Goal.** J12 Reuse-First H1/H2/H3/BUILD_NEW with durable L1→L2→L3 handoff, upstream exact-source/license and NOTICE currentness. Adopt mature outside ideas/code proportionally with an accountable decision and exact provenance. H1/H2/H3/BUILD_NEW have distinct evidence floors; material source/version/license drift changes current reliance, while legitimate BUILD_NEW and genuinely nonmaterial Fast Path remain possible. No blanket vendoring demand or universal open-source legal verdict.

**Already implemented on qualified v4.10 owner source; retain rather than duplicate.** Dependency owner already knows locked dependency identity, material source/registry/provenance changes, license/SBOM project-policy authority, Validation Impact and Fast Path. Architecture owner already requires alternatives/tradeoffs, material contract/ownership, unknown and bounded architecture decisions. L1/L2/L3 prompts separately collect alternative or upstream evidence; focused v4.1/v4.3 tests check parts of this but no complete J12 mode-specific currentness proof. Preserve all, do not add a second research lifecycle.

**Concrete still-missing v4.11 delta.** No explicit H1 pattern harvest, H2 spec/module reconstruction, H3 direct reuse, BUILD_NEW-with-rationale choice and no mode-specific L1 discovery → L2 owned disposition → L3 source/contract/test consumption. Generic license language does not bind specific mode to immutable upstream commit/path/observed license/NOTICE, derivation or re-evaluation on source/license changes. Existing dependency test helper does not receive upstream revision/license/reuse mode.

**Task deliverable:** minimal owner-local normative clauses plus **one unique** focused test `scripts/test_v411_t04_reuse_first.py`; a source/currentness-bound PR-local test report and exact-HEAD independent Review; an explicit T11 handoff for any required centrally owned projection. These are future Builder deliverables, **not work completed by this author**. The ultimate implementation PR targets the authorized v4.11 version integration branch (expected `version/v4.11.0` **only after** #973's seed readback and controller admission), one concern/one PR; never direct to `main` or old planning ancestry.

**Non-goals:** a second ADS method/authority, new mandatory runtime/server/scheduler/DB, wholesale stage rewriting, universal job combinations or automatic real-host/release PASS, changes owned by any other Task, and promoting fixture simulation to independently executed proof.

### 2. Frozen dependency, sole owner and explicit exclusions

- Frozen logical DAG has **zero executable predecessors** for V411-T04; this describes only topology, **not current Task READY**. All gate/Claim/Issue admission prerequisites still apply. Task author here has no executable Builder identity.
- **Allowed future normative write set** (no other existing source path):
  - `standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md` (inspected blob `5501ee46708c612071647be85bf7a368c6473cbe`; source/license/validation-impact and currentness §§6/9/13 only)
  - `standards/ARCHITECTURE_DESIGN_STANDARD.md` (inspected blob `66218c8a2779a9f84c67433426b9c5512f9f831a`; bounded reuse choice/alternatives/contracts/escape under existing design decision and Fast Path)
  - **NEW unique** `scripts/test_v411_t04_reuse_first.py` only; no reuse of any shared existing test.
- **Read-only / forbidden writes:** all `schemas/**`, `templates/**`, `standard-manifest.json`, shared verifiers (including `scripts/verify_standard.py` and `scripts/verify_project_standard.py`), shared legacy tests, `templates/GOLDEN_INDEX.md`, `checklists/version-closure.md`, `docs/implementation/4.11.0/{PRD.md,PRODUCT_PROOF_MATRIX.md,L2_ARCHITECTURE_EVIDENCE.md,TASK_DAG.md}`, other Tasks' owner clauses, `main`, `version/v4.10.0`, frozen planning branches. Any shared change **proposal** is routed to exclusive T11; no shadow schema or parallel common-file writer.
- **Authority:** Product #943 explicit human-approved Freeze, separately reviewed/frozen L2 #954 and DAG #966. Their exact refs are inputs; preflight #963@6094406584 was read-only advisory and its prior `DAG_FREEZE=NO` status is **historical at preflight time**, superseded as a planning state by independently recorded #966, not retroactively converted into execution evidence. Any mismatch at real dispatch blocks and demands scoped rebind.

### 3. Tests — executable acceptance oracles, not keyword-only checks

For all cases, assert exact fixture subject and relevant source/role/authority identity, **decision**, missing/stale evidence and absence of unauthorized side effects; use deterministic offline fixtures where appropriate. Each positive and negative case must actually execute against the later candidate or explicitly report `NOT_RUN/BLOCKED`.

| Positive | Grounded scenario | Required oracle |
| --- | --- | --- |
| P01 | H1 cited upstream pattern and local constrained design | PATTERN_HARVEST allowed; no direct-copy or behavior-equivalence inferred |
| P02 | H2 source-inspired locally specified module with exact source/derivation context, contract and differential/behavior/failure tests | Bounded SPEC_MODULE_RECONSTRUCTION admissible with disclosed divergence/risks |
| P03 | H3 exact immutable upstream SHA/paths + inspected policy-authorized license/NOTICE obligations, attribution and local behavior tests | Bounded DIRECT_CODE_REUSE admissible, not Release PASS |
| P04 | BUILD_NEW after plausible mature comparators and concrete incompatible license/coupling/security/maintenance rationale | Accountable NEW BUILD admissible; not a silent default |
| P05 | Inspected low-risk immmaterial change with no material upstream dependency or higher gate | Proportional Fast Path, no mandatory external research/catalog |

| Adversarial | Input / fault | Required fail-closed oracle |
| --- | --- | --- |
| N01 | Historic H3 permission relied on revision A/license; new reliance at B has materially changed license/NOTICE | Historical A preserved, B cannot inherit permission; policy authority disposition and Validation Impact |
| N02 | L2 cites A but L3 uses B or upstream behavior/source path materially drifts | STALE/UNKNOWN; fresh equivalence/source check before reuse |
| N03 | Known mature material comparator ignored; BUILD_NEW has no rationale/decision owner | BLOCKED/UNKNOWN, no default greenlight |
| N04 | H2 presented as 'LLM rewritten' without origin/derivation disclosure or behavior tests | No provenance laundering; blocked material reconstruction assertion |
| N05 | Unknown repository rights, conflicting license or missing NOTICE | No lawful H3 assumption merely because repository is public |
| N06 | Omitted J12/docs-only/A0 but actual vendored source/license change; J05+J12 intersection | Apply material obligations despite labels and Fast Path |
| N07 | README, unpinned latest or arbitrary checker claims reuse/equivalence/release PASS | Evidence not owner decision/real current validation |

**Acceptance threshold:** all in-scope focused cases green on the exact implementation PR HEAD; negative scenario cannot mutate a protected gate, authority or source; existing owner/regression tests remain passing or failure is documented/blocking. Run tests against actual owner-facing contracts, not a detached self-certifying model or mere search-for-words script. If common T11 wiring is not yet present, mark that part `DEFERRED_TO_T11` with specific missing field/test and keep whole-program conformance `NOT_RUN`.

### 4. Contract — existing authority with bounded new semantics

Input: inspected actual material capability, L1 comparator/prior art ref, L2 design decision authority + alternatives, selected mode H1/H2/H3/BUILD_NEW, immutable upstream repo/full SHA and material paths, license file/NOTICE/revision observations, project license-policy owner, local contract/test/exception/failure evidence and L3 consumption. Output: durable mode/disposition with provenance, scope, code/derivation boundary, applicable obligations, re-evaluation triggers and allowed/not-allowed action. Architecture owns choice/local contracts; Dependency owns upstream identity/license/currentness; Validation alone owns executed proof; no auto-promotion across L1→L2→L3.

The Task Pack defines WHAT; no exact-base patch, dynamic line-map, version-branch HEAD assumption or hidden chat prompt is an authority here. Material new semantics must preserve compatible historical readers and avoid silently changing preexisting event/Gate/release states.

### 5. Implementation — minimum owner-local delta

Small Architecture subsection for selection, alternatives, BUILD_NEW and proportional Fast Path; small Dependency cross-reference for exact source/license/NOTICE, project-policy and invalidation. Unique deterministic offline fixture suite with material source/license/pin/decision-owner switches and asserted verdict changes; source-identity/behavior counterexamples, not static string-only proof. Read existing L1/L2/L3 prompts and #929/#930/#931 as reference, but do not edit them; any shared template/schema fields go as a bounded proposal to T11.

**L3 Required handoff, ordered:** Tests above → this Contract → bounded owner-local Implementation → Failure Handling below → exact References here. Builder must record an L3 evidence link, exact PR HEAD/base and source test identity; introduce no extra requirement from a local prompt. Task Claim/dispatch, actual code author, validator and independent reviewer remain distinct truthfully attributed actors.

### 6. Failure handling and UNKNOWN routing

Missing full upstream identity/license/NOTICE or derivation materiality => UNKNOWN/BLOCKED and project license/security authority; changed implementation source/behavior => required fresh tests/Validation Impact; novel material architecture contradiction => owning L2 authority and affected fresh Review; preserve valid historic upstream fact, no unsafe copied code.

For any relevant source, permission, required test/environment, reviewer independence or canonical GitHub identity unverified, report the specific missing proof and `NOT_RUN/BLOCKED`; do not use an optimistic PASS/NOT_APPLICABLE. Failures block only genuine dependents; other disjoint concerns may proceed. Any Frozen Product/L2 incompatibility is escalated to owning authority and affected independent review, not patched by this Builder.

### 7. Validation, Review and merge admission

- **Owner-local verification commands to evaluate and run later, not executed here:** `python -m unittest scripts.test_v411_t04_reuse_first` (or direct script), `python scripts/test_v41_dependency_toolchain.py`, `python scripts/test_v43_architecture_design.py`; actual clean-host read-only upstream check where applicable, with recorded exact source/license and no arbitrary network mutation.
- **Execution proof:** future real Local Build Host/Validator records tested exact HEAD/tree, OS/toolchain, command, exit code, source/fixture SHA, evidence location, any permitted waiver authority and unrun material cases. Offline and source-only tests are **not** remote/host integration validation. Evidence from earlier v4.10 or preflight is reused for analysis but never relabelled v4.11 PASS.
- **Review:** `risk:medium`, `review:required`; require genuinely fresh independent Reviewer other than author and Builder; bind all material findings, currentness, allowed write-set, counterexamples and final verdict to the exact PR HEAD. Review PASS alone is not release permission.
- **Merge gate:** Task Issue must reference independently reviewed/FROZEN repository Pack and a **separately** created canonical native blocked-by graph; current qualified-main Stage3 baseline seed #973 must be verified. Controller/Local materializer creates exact-base JIT Execution Pack and obtains protected accepted Claim. Only after owner-local tests, required Validation and fresh Review, final current-state sweep and truthful merge readiness may a one-concern PR merge to authorized version branch. Recheck exact HEAD/branch currentness just before merge; no automatic Task-draft→Task-issue promotion.
- **Later integration:** T11 owns L1/L2/L3 shared prompt/template/schema/manifest projections if justified; T12 J12 plus X02 J05+J12 and J09+J10+J11+J12 unverified case; V01 actual current dependency/license/test and release proof. Candidate Freeze, Hidden Validation, independent Fresh Closeout, RQ, and guarded main integration are **separate V/R work items**; none is authorized or marked PASS by this Pack author.

### 8. Bounded Agent Freedom & deferred evidence ledger

```ini
F0_MECHANICAL=fixture_wiring_docs_links_imports_and_semantics_preserving_repair_only
F1_BOUNDED_IMPLEMENTATION=YES_EXACT_OWNER_CONTRACT_AND_POSITIVE_NEGATIVE_ORACLES_FIXED
F2_ENGINEERING_DISCRETION=ONLY_PROVEN_NONMATERIAL_INTERNAL_CHOICES_WITHIN_WRITESET
F3_ARCHITECTURE_REQUIRED=ESCALATE_TO_FROZEN_L2_PRODUCT_OR_OWNING_AUTHORITY_NO_SELF_PROMOTION
ACTOR_PRIVILEGE_ESCALATION=FORBIDDEN
PREFLIGHT_SOURCE_ONLY=TRUE
PR_TEST_RUN=NOT_RUN
REAL_BUILD_HOST=NOT_RUN
NATIVE_DEPENDENCY_READBACK=NOT_RUN
T11_CENTRAL_WIRING=DEFERRED_NOT_SATISFIED
T12_A_B_C_CONFORMANCE=NOT_RUN
V01_V02_V03_V04_R01_R02=NOT_RUN
```

Epistemic ledger: unverified current post-#973 integration HEAD, native Task issues/blocked-by actual REST+GraphQL readback, current Builder/Reviewer operator admission, new focused tests, shared wiring, real environment coverage, and uncovered materially distinct supported job combinations remain **UNKNOWN/NOT_RUN** until each owning actor supplies real evidence. No universal P1/P2/P3 completeness or release qualification is asserted.

### 9. Durable References and next owner

- Frozen Product: https://github.com/kaicreator-mm/ai-development-standard/issues/943#issuecomment-6084264198 (PRD blob above).
- Frozen L2: https://github.com/kaicreator-mm/ai-development-standard/issues/954; architecture blob above.
- Frozen DAG: https://github.com/kaicreator-mm/ai-development-standard/issues/966; DAG exact head/blob above. DAG author reviewed by https://github.com/kaicreator-mm/ai-development-standard/issues/959#issuecomment-6094398472.
- Task Pack Controller: https://github.com/kaicreator-mm/ai-development-standard/issues/967; independent version seed: https://github.com/kaicreator-mm/ai-development-standard/issues/973.
- Owner preflight (historical advisory only): https://github.com/kaicreator-mm/ai-development-standard/issues/963#issuecomment-6094406584. Actual normative owner blobs were **re-fetched** from exact qualified predecessor `b9461d48d902a2c7c00adff6746afc7a02a0ac3e`; future dispatch rechecks source against current lawful integration HEAD.
- Applicable current standard: `standards/EXECUTION_PACK_STANDARD.md`, `standards/TASK_DECOMPOSITION_STANDARD.md`, `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, `standards/ISSUE_FIRST_TASK_TRIGGER.md` from exact qualified v4.10 predecessor. Future integration may only use each exact separately reviewed owner.

**Next:** an **independent Pack Reviewer**, not this author or future Builder, challenges this draft for scope, executable oracle coverage, actual source-bounded gaps, provenance and DAG non-conflict. #967 integrator then materializes **one immutable repository Pack file** at the intended path and its single index entry on a legally verified stage3 integration branch, conducts authoritative Pack Review/currentness, and only afterward permits separately qualified Local native Task Issue/blocked-by creation. This Issue comment is **NOT a Pack Freeze**, executable Task Issue, Builder Claim, implementation, CI result or Release decision.
