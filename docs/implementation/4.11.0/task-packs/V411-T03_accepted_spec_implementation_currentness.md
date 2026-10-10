<!-- v4.11 Task Pack CANDIDATE ONLY; author=#969@6094572317; product=#943, L2=#954, DAG=#966; not frozen; no Builder/Claim authority -->

## V411-T03 — source-bound immutable-Task-Pack-ready DRAFT (author only)

```ini
PACK_DRAFT=SOURCE_BOUND_READY_FOR_INDEPENDENT_REVIEW
AUTHORSHIP_TASK_ISSUE=#969
INTENDED_FUTURE_PATH=docs/implementation/4.11.0/task-packs/V411-T03_accepted_spec_implementation_currentness.md
TASK_ID=V411-T03
ONE_CONCERN=ACCEPTED_SPEC_IMPLEMENTATION_CURRENTNESS
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
SOURCE_PREFLIGHT=#962@6094388971
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

**Goal.** J05 accepted ADDED/MODIFIED/REMOVED specification versus actually implemented producer and supported consumer currentness. Make acceptance of spec changes provably distinct from implementation and compatible deployment. For material J05 (and J04/J03 intersections) require bounded source-attributed accepted spec revision, current exact producer implementation, supported affected consumer/window/dimension evidence and revalidation on drift. Do not require an OpenSpec runtime.

**Already implemented on qualified v4.10 owner source; retain rather than duplicate.** The owner already requires exact contract baseline/candidate, change-operation distinct from compatibility outcome, wire/source/behavior dimensions, supported old/new producer-consumer windows, unknown-fail-closed, deprecation/removal and no compatibility→release inference. v1 `schemas/compatibility-record-v1.schema.json@1e68ad8c103b4c151c21a955866cf295168c482d` and existing v4.2 tests/dogfood prove part of those older obligations. Preserve existing v1 readers/history.

**Concrete still-missing v4.11 delta.** The accepted/archived spec-delta's **authority/current identity** is not yet reconciled with exact actually shipped producer subject and current affected consumers. v1 has no accepted-spec currentness/revalidation fields and rejects unrecognized fields (`additionalProperties=false`). Existing evaluator tests supplied baseline/consumer equality, not accepted-spec provenance, ADDED/MODIFIED/REMOVED shipping or changing consumer-window revalidation. T11, not T03, owns any additive schema.

**Task deliverable:** minimal owner-local normative clauses plus **one unique** focused test `scripts/test_v411_t03_spec_implementation_currentness.py`; a source/currentness-bound PR-local test report and exact-HEAD independent Review; an explicit T11 handoff for any required centrally owned projection. These are future Builder deliverables, **not work completed by this author**. The ultimate implementation PR targets the authorized v4.11 version integration branch (expected `version/v4.11.0` **only after** #973's seed readback and controller admission), one concern/one PR; never direct to `main` or old planning ancestry.

**Non-goals:** a second ADS method/authority, new mandatory runtime/server/scheduler/DB, wholesale stage rewriting, universal job combinations or automatic real-host/release PASS, changes owned by any other Task, and promoting fixture simulation to independently executed proof.

### 2. Frozen dependency, sole owner and explicit exclusions

- Frozen logical DAG has **zero executable predecessors** for V411-T03; this describes only topology, **not current Task READY**. All gate/Claim/Issue admission prerequisites still apply. Task author here has no executable Builder identity.
- **Allowed future normative write set** (no other existing source path):
  - `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` (inspected blob `266aefe32e0990c24fc8c1d6d731c4a3456fc3fc`; add only bounded accepted-spec→implementation reconciliation to existing §§3–9/11–12 semantics)
  - **NEW unique** `scripts/test_v411_t03_spec_implementation_currentness.py` only; no reuse of any shared existing test.
- **Read-only / forbidden writes:** all `schemas/**`, `templates/**`, `standard-manifest.json`, shared verifiers (including `scripts/verify_standard.py` and `scripts/verify_project_standard.py`), shared legacy tests, `templates/GOLDEN_INDEX.md`, `checklists/version-closure.md`, `docs/implementation/4.11.0/{PRD.md,PRODUCT_PROOF_MATRIX.md,L2_ARCHITECTURE_EVIDENCE.md,TASK_DAG.md}`, other Tasks' owner clauses, `main`, `version/v4.10.0`, frozen planning branches. Any shared change **proposal** is routed to exclusive T11; no shadow schema or parallel common-file writer.
- **Authority:** Product #943 explicit human-approved Freeze, separately reviewed/frozen L2 #954 and DAG #966. Their exact refs are inputs; preflight #962@6094388971 was read-only advisory and its prior `DAG_FREEZE=NO` status is **historical at preflight time**, superseded as a planning state by independently recorded #966, not retroactively converted into execution evidence. Any mismatch at real dispatch blocks and demands scoped rebind.

### 3. Tests — executable acceptance oracles, not keyword-only checks

For all cases, assert exact fixture subject and relevant source/role/authority identity, **decision**, missing/stale evidence and absence of unauthorized side effects; use deterministic offline fixtures where appropriate. Each positive and negative case must actually execute against the later candidate or explicitly report `NOT_RUN/BLOCKED`.

| Positive | Grounded scenario | Required oracle |
| --- | --- | --- |
| P01 | Authorized ADDED spec S1, H1 producer actually implements, supported C0 and C1 tested for required dimensions | `RECONCILED` for named contract/window only; no Validation/Release PASS |
| P02 | Accepted S1 initially unshipped on H0; then fresh H1 and supported consumer evidence | Fresh H1 reconciliation allowed; H0 historical BLOCKED remains |
| P03 | Inspected nonmaterial diff with no affected producer/consumer | Explicit proportionate nonmaterial disposition; no empty heavyweight record |

| Adversarial | Input / fault | Required fail-closed oracle |
| --- | --- | --- |
| N01 | S1 ADDED accepted/archived while producer stays H0 | NOT_RUN/UNKNOWN/BLOCKED, never implemented |
| N02 | MODIFIED S1 accepted but tests still exercise old H0 | Reject current implementation assertion |
| N03 | REMOVED in H1, old supported C0 still calls removed operation | Current window INCOMPATIBLE/BLOCKED despite C1 PASS |
| N04 | Only H1+C1 tested, still-supported C0 untested | UNKNOWN/BLOCKED old-consumer window |
| N05 | Archive/spec merge/codegen/checker-only GREEN without actual current behavior | No implementation, behavior, Validation or Release promotion |
| N06 | Producer H2 or accepted S2 or supported consumer C2 changes after prior proof | Prior H1/S1/C0 evidence STALE for changed material scope; require revalidation |
| N07 | Missing immutable baseline/delta/approval/current producer/dimension | UNKNOWN/BLOCKED rather than inference |
| N08 | Unmodified historical valid compatibility-record-v1 input | Old v1 reader still accepts it; no new mandatory fields retroactively |

**Acceptance threshold:** all in-scope focused cases green on the exact implementation PR HEAD; negative scenario cannot mutate a protected gate, authority or source; existing owner/regression tests remain passing or failure is documented/blocking. Run tests against actual owner-facing contracts, not a detached self-certifying model or mere search-for-words script. If common T11 wiring is not yet present, mark that part `DEFERRED_TO_T11` with specific missing field/test and keep whole-program conformance `NOT_RUN`.

### 4. Contract — existing authority with bounded new semantics

Owner accepts an evidence projection `{spec_baseline_ref, proposed_delta_ref, acceptance_authority_ref, accepted_spec_current_ref, implementation_subject_ref, affected_producer_consumer_windows, revalidation_refs}` **as proposed logical fields only**, bound to existing contract/baseline/candidate/change_operations/dimensions. Test source exact spec identity/authority and actual code/build/ref + supported consumer versions/windows + required wire/source/behavior observations. An accepted spec is not code, an archive is not successful Validation, and compatibility is not Release authority. Drift invalidates only affected current assertions; preserve source history and valid v1 reader semantics.

The Task Pack defines WHAT; no exact-base patch, dynamic line-map, version-branch HEAD assumption or hidden chat prompt is an authority here. Material new semantics must preserve compatible historical readers and avoid silently changing preexisting event/Gate/release states.

### 5. Implementation — minimum owner-local delta

Bounded text amendment in the one Compatibility Standard, with source-authoritative ownership and currentness conditions. Unique offline fixture tests must vary accepted spec, real producer identity, old/new consumers and required dimensions and verify verdict + missing/stale evidence, not just text presence. Shared schema additive/readback contract handed as proposal to T11; do not inject seven fields into v1 record from T03. T12/V01 separately execute integrated and real consumer/build compatibility.

**L3 Required handoff, ordered:** Tests above → this Contract → bounded owner-local Implementation → Failure Handling below → exact References here. Builder must record an L3 evidence link, exact PR HEAD/base and source test identity; introduce no extra requirement from a local prompt. Task Claim/dispatch, actual code author, validator and independent reviewer remain distinct truthfully attributed actors.

### 6. Failure handling and UNKNOWN routing

Absent actual producer or supported consumer evidence, unaccepted/missing authority, incomplete current window or stale SHA/spec => NOT_RUN/UNKNOWN/BLOCKED; genuine incompatible supported consumer => FAIL/BLOCKED according to owner without relabeling as success. Material untestable external consumers remain explicitly NOT_RUN and routed to Validation owner. Distinguish current assertion from historical report.

For any relevant source, permission, required test/environment, reviewer independence or canonical GitHub identity unverified, report the specific missing proof and `NOT_RUN/BLOCKED`; do not use an optimistic PASS/NOT_APPLICABLE. Failures block only genuine dependents; other disjoint concerns may proceed. Any Frozen Product/L2 incompatibility is escalated to owning authority and affected independent review, not patched by this Builder.

### 7. Validation, Review and merge admission

- **Owner-local verification commands to evaluate and run later, not executed here:** `python -m unittest scripts.test_v411_t03_spec_implementation_currentness` (or direct script), `python scripts/test_v42_interface_compatibility.py`, `python scripts/test_v42_api_compatibility_conformance.py`, `python scripts/test_v42_cross_standard_conformance.py`; independently run v1 reader/schema regression on actual implementation HEAD.
- **Execution proof:** future real Local Build Host/Validator records tested exact HEAD/tree, OS/toolchain, command, exit code, source/fixture SHA, evidence location, any permitted waiver authority and unrun material cases. Offline and source-only tests are **not** remote/host integration validation. Evidence from earlier v4.10 or preflight is reused for analysis but never relabelled v4.11 PASS.
- **Review:** `risk:medium`, `review:required`; require genuinely fresh independent Reviewer other than author and Builder; bind all material findings, currentness, allowed write-set, counterexamples and final verdict to the exact PR HEAD. Review PASS alone is not release permission.
- **Merge gate:** Task Issue must reference independently reviewed/FROZEN repository Pack and a **separately** created canonical native blocked-by graph; current qualified-main Stage3 baseline seed #973 must be verified. Controller/Local materializer creates exact-base JIT Execution Pack and obtains protected accepted Claim. Only after owner-local tests, required Validation and fresh Review, final current-state sweep and truthful merge readiness may a one-concern PR merge to authorized version branch. Recheck exact HEAD/branch currentness just before merge; no automatic Task-draft→Task-issue promotion.
- **Later integration:** T11 exclusively reconciles seven logical refs with old v1 schema (additive backward readability), templates/manifest/verifier; T12 X02 J05+J12 and X05 J04+J05; V01 exact real host and actual supported consumer/API checks. Candidate Freeze, Hidden Validation, independent Fresh Closeout, RQ, and guarded main integration are **separate V/R work items**; none is authorized or marked PASS by this Pack author.

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
- Owner preflight (historical advisory only): https://github.com/kaicreator-mm/ai-development-standard/issues/962#issuecomment-6094388971. Actual normative owner blobs were **re-fetched** from exact qualified predecessor `b9461d48d902a2c7c00adff6746afc7a02a0ac3e`; future dispatch rechecks source against current lawful integration HEAD.
- Applicable current standard: `standards/EXECUTION_PACK_STANDARD.md`, `standards/TASK_DECOMPOSITION_STANDARD.md`, `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, `standards/ISSUE_FIRST_TASK_TRIGGER.md` from exact qualified v4.10 predecessor. Future integration may only use each exact separately reviewed owner.

**Next:** an **independent Pack Reviewer**, not this author or future Builder, challenges this draft for scope, executable oracle coverage, actual source-bounded gaps, provenance and DAG non-conflict. #967 integrator then materializes **one immutable repository Pack file** at the intended path and its single index entry on a legally verified stage3 integration branch, conducts authoritative Pack Review/currentness, and only afterward permits separately qualified Local native Task Issue/blocked-by creation. This Issue comment is **NOT a Pack Freeze**, executable Task Issue, Builder Claim, implementation, CI result or Release decision.
