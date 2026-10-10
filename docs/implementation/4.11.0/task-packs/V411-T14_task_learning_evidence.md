<!-- v4.11 Task Pack CANDIDATE ONLY; author=LOCAL_BATCH_B_SUBAGENT_#984; product=#943, L2=#954, DAG=#966; not frozen; no Builder/Claim authority -->

## V411-T14 — R11 bounded factual Task Learning evidence DRAFT (author only)

```ini
AUTHORSHIP=LOCAL_BATCH_B_SUBAGENT_DRAFT
INTENDED_FUTURE_PATH=docs/implementation/4.11.0/task-packs/V411-T14_task_learning_evidence.md
TASK_ID=V411-T14
ONE_CONCERN=R11_BOUNDED_FACTUAL_TASK_LEARNING_SOURCE_CURRENCY_EPISTEMIC_STRENGTH_AND_SUBORDINATE_CONSUMPTION
FROZEN_PRODUCT=#943@6084264198
PRODUCT_COMMIT=34df09a2433aec5523ab80c90e885f6d9fc78803
PRODUCT_PRD_BLOB=d30f202e8ea662731ff8a4f2ad1ad88cfc5bb179
PRODUCT_MATRIX_BLOB=f59a6daf5430ece66103a830e392a04f71623ff0
FROZEN_L2=#954
L2_COMMIT=f1fc21be366579cbeafa98217b52e106a55b41a5
L2_BLOB=c0fa361474996a0626c63e93574a284ae3eb8d91
FROZEN_DAG=#966
DAG_HEAD=26fc83911185675bdea3c540df6df15c0241402b
DAG_BLOB=9866d35ae1512b156cfdc94cc01aec2fa897f3e6
QUALIFIED_PREDECESSOR_MAIN=b9461d48d902a2c7c00adff6746afc7a02a0ac3e
VERSION_SEED_HEAD=5f224dd662f12fc57fb1bb270ed30e6eb1d83413
VERSION_SEED_TREE=1bfac20e90c69bb57db4f293148b7264d292b5be
PACK_CONTROLLER=#967
PACK_BATCH_B_AUTHORING=#984
FROZEN_DAG_PREDECESSORS=T07
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

**Goal.** Frozen Product requirement R11: Task Learning delivered as bounded factual evidence with real cited source and current subject, explicit epistemic strength (factual confidence vs unsupported inferred lesson), rejection of stale or forged private deliberation, and later-work consumption strictly as subordinate evidence — never Product/L2/Task mutation authority. Positive AND negative learning records are in scope; `ALREADY_SATISFIED` may be claimed only if the exact production source plus current executable tests prove full R11 equivalence, otherwise the missing owner-local semantics are implemented.

**Already implemented on qualified owner sources; retain rather than duplicate.** `references/TASK_LEARNING_V2_REFERENCE.md@529f2e52fa6ca9e2a41fe154f91c039f33d5eb5f` preserves the v4.8 owner family: v1 core fields (`learning_id`, `repository_ref`, `work_item_ref`, `implementation_subject_ref`, `confidence_layers`, `currentness_ref`, `disposition`, source/test/validation/review refs) unchanged; v2 adds only friction/recurrence reference fields, all resolve-or-fail-closed; "Authority and routing boundaries" makes v1/v2 records evidence refs only, never Gate PASS, with no numeric promotion threshold; non-goals forbid private chain-of-thought capture and any learning database/lifecycle. `standards/DEVELOPMENT_WORKFLOW.md` §8 (READ ONLY to this Task) already classifies Task Learning observations as evidence producers routed through existing owners. `standards/EXECUTION_ARCHITECTURE_STANDARD.md@5588d2196677b1b4878563de65edf2beaa10178f` supplies §12 exact-subject/drift discipline and §29.1-style currentness consumption patterns this Task reuses without redefining.

**Concrete still-missing v4.11 delta.** The frozen DAG names the **Task Learning evidence owner section** of `EXECUTION_ARCHITECTURE_STANDARD.md` as this Task's canonical owner surface; the inspected blob contains **no such section** (the file ends at §29.7). Resolution carried by this pack: T14 additively establishes that owner section in the canonical file (exact section number/anchor assigned at implementation, after §29; no renumbering of §1–§29), encoding what the reference doc asserts but no execution owner yet enforces: (a) cited source must resolve against the real production source and remain current-subject-bound at consumption time; (b) confidence must separate source-bound factual content from unsupported inference, and an unsupported inferred lesson never enters a record as fact; (c) private deliberation asserted without durable boundary-external evidence — or cited from a stale/defunct subject — is rejected as forged/stale, never evidence by accumulation; (d) later work consumes records only as subordinate evidence feeding existing owners (Review, Validation, v4.8 Evolution Intake), never as authority to mutate Product, L2, Task scope or bypass stages.

**Task deliverable:** the additive owner section plus bounded clarifying edits to `references/TASK_LEARNING_V2_REFERENCE.md`, and **one unique** focused test `scripts/test_v411_task_learning.py`; PR-local test report and exact-HEAD independent Review; explicit T11 handoff for any schema/manifest projection. These are future Builder deliverables, **not work completed by this author**. The implementation PR targets the authorized v4.11 version integration branch after #973 seed readback and controller admission; one concern/one PR; never direct to `main`.

**Non-goals:** a second learning family or intake lifecycle, a learning database, private chain-of-thought capture, workflow state, automatic ADS mutation, numeric promotion thresholds, changes to v1/v2 schemas or the shared suite, and any version PASS claim.

### 2. Frozen dependency, sole owner and explicit exclusions

- Exact frozen predecessor is **T07** (DAG §3: `T05 → T06 → T07 → T14`; T06/T07/T14 touch different sections of the same owner file and require ordered baselines — T14 builds on the T07-integrated file state). Predecessor completion is a planning fact; native dependencies are NOT_MATERIALIZED and Task READY stays BLOCKED until controller admission.
- **Allowed future normative write set** (no other existing source path):
  - `standards/EXECUTION_ARCHITECTURE_STANDARD.md` — the **Task Learning evidence owner section** (inspected owner blob `5588d2196677b1b4878563de65edf2beaa10178f`; additive new section only; all existing sections read-only).
  - `references/TASK_LEARNING_V2_REFERENCE.md` (inspected blob `529f2e52fa6ca9e2a41fe154f91c039f33d5eb5f`; bounded, family-preserving clarifications only).
  - **NEW unique** `scripts/test_v411_task_learning.py` only.
- **Read-only / forbidden writes:** `schemas/task-learning-v1.schema.json`, `schemas/task-learning-v2.schema.json` and all `schemas/**` (shared schemas are read-only before T11), `scripts/test_v49_task_learning_v2.py` (inspected blob `2cb452ea90838b0660271152637b735048dcc39c`) and `scripts/test_v48_task_learning.py` (observation/regression reference only), `standard-manifest.json`, shared verifiers (`scripts/verify_standard.py`, `scripts/verify_project_standard.py`), `templates/**` including `templates/GOLDEN_INDEX.md`, `checklists/version-closure.md`, `standards/DEVELOPMENT_WORKFLOW.md` (T01/T02/T13 owner sections), `docs/implementation/4.11.0/{PRD.md,PRODUCT_PROOF_MATRIX.md,L2_ARCHITECTURE_EVIDENCE.md,TASK_DAG.md}`, other Tasks' owner clauses (T07's §14, T06's §§27–28 included), `TASK_PACKS.json`, `main`, frozen planning branches. Any additive schema/manifest need is a recorded T11 handoff; no schema shadow file.

### 3. Tests — executable acceptance oracles, not keyword-only checks

Fixtures are deterministic and offline: recorded instances against the read-only v1/v2 schema contracts, resolvable/stale/unresolvable ref sets, and a simulated later-work consumer asserting subordinate-evidence-only outcomes. Each case asserts decision, source/subject resolution state, epistemic classification and absence of authority side effects.

| Positive | Grounded scenario | Required oracle |
| --- | --- | --- |
| P01 | Factual record: resolvable repository/work-item/subject refs, source test/validation/review evidence, current at citation and consumption | Accepted as bounded evidence; confidence layers classify factual content; zero authority side effects; disposition recorded |
| P02 | Simple work item with no reusable material learning | `TASK_LEARNING=NONE_MATERIAL` fast path; no empty ceremony record instantiated |
| P03 | Later work consumes a current record as input to an existing route (Review context or v4.8 Evolution Intake via `friction_classification`/`ads_evolution_candidate_ref`) | Consumption is subordinate-evidence-only; intake entry is pointed at, not created/approved; Product/L2/Task untouched |
| P04 | Negative record: factual failure/constraint learned, with evidence refs | Same-family acceptance as positive; negative lesson bound to the same source/currentness discipline |
| P05 | v1 record consumed by v2-aware reader; v2 instance against v1 parser expectations | Version-aware behavior preserved read-only: v1 validity intact, no silent reinterpretation in either direction, v2 fails closed on v1 |

| Adversarial | Input / fault | Required fail-closed oracle |
| --- | --- | --- |
| N01 | `implementation_subject_ref`/`currentness_ref` stale at consumption time | Record demoted to immutable historical evidence; cannot satisfy any current R11 claim; no rebinding |
| N02 | "Lesson" sourced only from claimed private model deliberation with no durable boundary-external evidence | Rejected as forged/unverifiable provenance; no record created; private deliberation is never evidence by itself |
| N03 | Confidence asserted beyond source refs, or any ref field unresolvable | Unsupported inference marked non-factual; claim fails closed; never stored/presented as fact |
| N04 | Record (or accumulation of records) used to edit Product/L2/Task content or mark an evolution candidate approved | Mutation blocked; accumulation grants no authority; route stays the existing owners' ordinary governance |
| N05 | Numeric score/count proposed as automatic promotion threshold | Rejected; no count/score converts evidence into authority; owner/currentness/counterevidence review still required |
| N06 | `ALREADY_SATISFIED` claimed without exact production source plus current executable tests proving full R11 equivalence | Claim rejected; missing owner-local semantics must be implemented instead; equivalence proof is never asserted from schema existence alone |

**Acceptance threshold:** all in-scope focused cases green on the exact implementation PR HEAD; no negative case mutates a protected authority, schema or normative file; existing `scripts/test_v48_task_learning.py` / `scripts/test_v49_task_learning_v2.py` remain passing read-only. Assertions exercise real owner contracts and decisions, not substring search. T11-dependent central projection is `DEFERRED_TO_T11`; integrated compound conformance is `DEFERRED_TO_T12`.

### 4. Contract — existing authority with bounded new semantics

Input tuple: candidate learning observation; its durable evidence refs (repository/work item/subject; test, validation, review refs); citation-time and consumption-time currentness reads; producer identity. Output: an admissible bounded record reusing the v1/v2 vocabulary unchanged, with owner-local admissibility semantics defined in the new owner section: `source_binding` (refs must resolve to real production source at citation AND at each consumption), `epistemic_layers` distinguishing `FACTUAL_SOURCE_BOUND` from `UNSUPPORTED_INFERRED` content, `provenance_authenticity` (durable boundary-external evidence required; private deliberation alone never qualifies), and `consumption_mode=SUBORDINATE_EVIDENCE_ONLY`. `UNKNOWN` resolution state is a fact, never a default. No new schema fields are introduced by this Task; if manifest/schema registration of the projection is needed, an additive proposal is handed to exclusive T11 and the owner-local contract still stands on existing refs.

The Task Pack defines WHAT; no exact-base patch, line map or HEAD-locked command is authority. The owner section must preserve the reference doc's family identity, fast path, compatibility and boundaries byte-compatibly and create no second authority path.

### 5. Implementation — minimum owner-local delta

Add the Task Learning evidence owner section to `standards/EXECUTION_ARCHITECTURE_STANDARD.md` additively after §29 (exact number/anchor at implementation), citing rather than copying `references/TASK_LEARNING_V2_REFERENCE.md` and the read-only schemas; apply bounded clarifying edits to the reference doc only where R11 semantics need an explicit statement (source/currency at consumption, epistemic strength, provenance authenticity, subordinate consumption, ALREADY_SATISFIED equivalence bar). Implement the unique test as fixture-fed owner-contract assertions (positive and adversarial **decisions**, not prose-only substring asserts). T11 exclusively owns schema/manifest/verifier wiring; T12 later proves integrated R11/R02 compound cases; V01 provides real-host closure. No runtime store, scheduler or lifecycle is introduced.

**L3 required handoff, ordered:** Tests above → this Contract → bounded owner-local Implementation → Failure Handling below → exact References here. Builder records an L3 evidence link, exact PR HEAD/base and source test identity; Task Claim/dispatch, code author, validator and independent reviewer remain distinct truthfully attributed actors.

### 6. Failure handling and UNKNOWN routing

Unresolvable or stale ref, ambiguous subject, unverifiable provenance, authority-boundary violation, or an `ALREADY_SATISFIED` equivalence claim lacking exact-source/current-test proof → `BLOCKED`/`REJECTED` with the exact record id, refs and missing proof recorded, routed to the owning authority (record producer repair, existing Evolution Intake, or T11 for central wiring). Currentness drift after acceptance demotes the record to historical only; it is never retroactively ratified. Never relabel a rejection as `NONE_MATERIAL` ceremony to close a Task; never promote an inferred lesson into factual confidence. Failures block only genuine dependents; disjoint concerns proceed. Any Frozen Product/L2 incompatibility escalates to owning authority and independent review, not patched by this Builder.

### 7. Validation, Review and merge admission

- **Owner-local verification commands to evaluate and run later, not executed by this author:** `python -m unittest scripts.test_v411_task_learning` (or repository-supported direct Python invocation); read-only regression references `python scripts/test_v48_task_learning.py` and `python scripts/test_v49_task_learning_v2.py`; verify commands against the actual environment and report exact command/exit/log.
- **Execution proof:** a real Local Build Host/Validator later records tested exact HEAD/tree, OS/toolchain, command, exit code, fixture/source SHA and evidence location. Offline owner-local results are not integrated validation. Shared-schema integrated verification is `DEFERRED_TO_T11`; whole-version A/B/C conformance is `DEFERRED_TO_T12`.
- **Review:** `RISK=medium`, `REVIEW_POLICY=required`; a genuinely fresh independent Reviewer other than author and Builder binds findings, currentness, write-set conformance and verdict to the exact PR HEAD. Review PASS is not release permission.
- **Merge gate:** canonical native Task Issue + blocked-by graph materialized and read back; reviewed/frozen repository Pack; #973 stage3 baseline verified; protected accepted Claim; then a final current-state sweep and exact-head recheck immediately before the one-concern PR merges to the authorized version branch. No self-declared merge-ready; no Task-draft→Task-issue auto-promotion.
- **Later integration:** T11 owns any central projection; T12 proves R11/R02 integrated conformance; V01/V02/V03/V04/R01/R02 remain separate work items, none authorized or marked PASS here.

### 8. Bounded Agent Freedom & deferred evidence ledger

```ini
F0_MECHANICAL=fixture_wiring_docs_links_imports_and_semantics_preserving_repair_only
F1_BOUNDED_IMPLEMENTATION=YES_EXACT_OWNER_CONTRACT_AND_POSITIVE_NEGATIVE_ORACLES_FIXED
F2_ENGINEERING_DISCRETION=ONLY_PROVEN_NONMATERIAL_INTERNAL_CHOICES_WITHIN_WRITESET
F3_ARCHITECTURE_REQUIRED=ESCALATE_TO_FROZEN_L2_PRODUCT_OR_OWNING_AUTHORITY_NO_SELF_PROMOTION
ACTOR_PRIVILEGE_ESCALATION=FORBIDDEN
SHARED_SCHEMA_SUITE_MANIFEST_EDITS=FORBIDDEN_HANDOFF_TO_T11
PR_TEST_RUN=NOT_RUN
REAL_BUILD_HOST=NOT_RUN
NATIVE_DEPENDENCY_READBACK=NOT_RUN
T11_CENTRAL_WIRING=DEFERRED_NOT_SATISFIED
T12_A_B_C_CONFORMANCE=DEFERRED_NOT_RUN
V01_V02_V03_V04_R01_R02=NOT_RUN
```

Epistemic ledger: current post-#973 integration HEAD, predecessor T07 merged exact SHA and the resulting owner-file section state, native blocked-by readback, current Builder/Reviewer admission, the new focused test, any schema/manifest projection, and real later-work consumption traces remain UNKNOWN/NOT_RUN until each owning actor supplies real evidence. No universal R11 completeness or release qualification is asserted.

### 9. Durable References and next owner

- Frozen Product: https://github.com/kaicreator-mm/ai-development-standard/issues/943#issuecomment-6084264198 (R11 Task Learning; PRD §13 friction/recurrence origin; PRD/matrix blobs above).
- Frozen L2: https://github.com/kaicreator-mm/ai-development-standard/issues/954 (L2 §7.3 friction fields); Frozen DAG: https://github.com/kaicreator-mm/ai-development-standard/issues/966 (T14 row, §2/§3 ordered baseline).
- Task Pack Controller: https://github.com/kaicreator-mm/ai-development-standard/issues/967; version seed: https://github.com/kaicreator-mm/ai-development-standard/issues/973. Batch A candidates are READ ONLY context: https://github.com/kaicreator-mm/ai-development-standard/pull/978.
- Owner sources cited by inspected blob: `standards/EXECUTION_ARCHITECTURE_STANDARD.md@5588d2196677b1b4878563de65edf2beaa10178f` (§12, §29; no existing Task Learning section — T14 establishes it), `references/TASK_LEARNING_V2_REFERENCE.md@529f2e52fa6ca9e2a41fe154f91c039f33d5eb5f`, `scripts/test_v49_task_learning_v2.py@2cb452ea90838b0660271152637b735048dcc39c` (READ ONLY), `schemas/task-learning-v1.schema.json` / `schemas/task-learning-v2.schema.json` (READ ONLY). Future dispatch rechecks every ref against the then-current lawful integration HEAD.

**Next:** an **independent Pack Reviewer**, not this author or any future Builder, challenges this draft for scope, executable oracle coverage, actual source-bounded gaps, provenance and DAG non-conflict. #967 then materializes one immutable repository Pack file at the intended path with its single index entry, conducts authoritative Pack Review/currentness, and only afterward permits separately qualified native Task Issue/blocked-by creation. This file is **NOT a Pack Freeze**, executable Task Issue, Builder Claim, implementation, CI result or Release decision.
