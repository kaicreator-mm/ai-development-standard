<!-- v4.11 Task Pack CANDIDATE ONLY; author=LOCAL_BATCH_B_SUBAGENT_#984; product=#943, L2=#954, DAG=#966; not frozen; no Builder/Claim authority -->

## V411-T07 — Merge Controller last-admission exact-state sweep and guarded merge readiness DRAFT (author only)

```ini
AUTHORSHIP=LOCAL_BATCH_B_SUBAGENT_DRAFT
INTENDED_FUTURE_PATH=docs/implementation/4.11.0/task-packs/V411-T07_merge_controller_admission.md
TASK_ID=V411-T07
ONE_CONCERN=MERGE_CONTROLLER_LAST_ADMISSION_EXACT_STATE_SWEEP_AND_GUARDED_MERGE_READINESS
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
FROZEN_DAG_PREDECESSORS=T05,T06
RISK=high
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

**Goal.** One exact-state last-admission sweep feeding guarded merge readiness: immediately before merge the Merge Controller re-reads every admission surface (PR/native Reviews, linked Task/Review/Validation refs, required CI/profile conditions, native Issue Dependencies, unresolved release-significant findings), binds each read to the exact source-head/target identity, records a sweep-completeness watermark, rechecks exact head currency at the merge step itself, and fails closed on any stale-head, same-head conflict, post-sweep late blocker, or incomplete/paginated readback. No fictitious atomic GitHub snapshot is ever claimed: a sweep is a bounded, identity-recorded sequence of reads, not a snapshot.

**Already implemented on qualified v4.10 owner source; retain rather than duplicate.** `standards/EXECUTION_ARCHITECTURE_STANDARD.md@5588d2196677b1b4878563de65edf2beaa10178f` §14 already scopes the Merge Controller to deterministic merges whose prerequisites are satisfied, requires re-reading current head/target and stale evidence/base drift before merge, mandates post-merge records (source head, base/target before, integration SHA, tree/method) and downstream ready-set recomputation, and states merge control is not Release Qualification. §12 defines HEAD/BASE/MERGE-RESULT/CANDIDATE drift with fail-closed revalidation on unknown impact. §29.1 makes merge/merge-ready an authority-bearing transition that must consume Assurance Plan `currentness_binding` (CURRENT/STALE/UNKNOWN) immediately before acting. `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md@ea007939639bbd6b4afbff1d71fdc19eb83d00be` §11 lists merge-ready prerequisites and §9.1 exact-subject Review currentness (a previous subject's PASS never satisfies a successor subject).

**Concrete still-missing v4.11 delta.** No owner defines the sweep itself as a falsifiable procedure: which surfaces are read, in what identity-bound order, what recorded fact proves a surface read was complete (listing watermark/pagination completeness), how a late blocker arriving between surface reads invalidates the sweep, how two opposite accepted Reviews at the same exact subject fail closed instead of last-writer-wins, and the exact-head recheck that guards the merge step. The Frozen Product #3 negative location names same-HEAD opposite accepted Reviews, late blocker/watermark update and incomplete GitHub readback; none has an owner-local oracle today.

**Task deliverable:** minimal additive normative clauses under §14 and its subordinate merge-admission procedures plus **one unique** focused test `scripts/test_v411_merge_admission.py`; a source/currentness-bound PR-local test report and exact-HEAD independent Review; an explicit T11 handoff for any shared-suite edit. These are future Builder deliverables, **not work completed by this author**. The implementation PR targets the authorized v4.11 version integration branch only after #973 seed readback and controller admission; one concern/one PR; never direct to `main`.

**Non-goals:** new merge authority, Release Qualification or release verdicts, a second review policy or Review owner, changes to T05's accepted-event/Review authority sections or native schemas, a GitHub snapshot/cache authority, and any automatic version PASS.

### 2. Frozen dependency, sole owner and explicit exclusions

- Exact frozen predecessors are **T05, T06** (DAG §2 row; §3 topology `T05 → T06 → T07` and `T05 + T06 → T07` agree set-wise). §3 additionally orders T07's §14 edit after T06's Execution §27–28 edit — an ordered same-file baseline constraint, not an extra dependency. Predecessor completion is a planning fact only; native Issue Dependencies are NOT_MATERIALIZED and Task READY stays BLOCKED until controller admission.
- **Allowed future normative write set** (no other existing source path):
  - `standards/EXECUTION_ARCHITECTURE_STANDARD.md` **§14 Merge Controller and subordinate merge-admission procedures only** (inspected blob `5588d2196677b1b4878563de65edf2beaa10178f`; §§11, 15, 17, 18, 27–29 and T14's future Task Learning section are other owners' scope).
  - **NEW unique** `scripts/test_v411_merge_admission.py` only.
- **R2-F07 shared test guard:** existing shared `scripts/test_execution_architecture.py` (inspected blob `a17ba7290458b4115c985faaf5d65773c0cfd16d`) is a manifest-registered shared suite usable by T07 **READ ONLY** as observation/reference. Any proposed common-suite edit is an explicit handoff proposal recorded in this pack for exclusive T11; T07 never edits it. A pending T11 common-suite edit is **not** evidence that T07 passed integrated verification: that gate is labelled `DEFERRED_TO_T11` (and T12 for integrated conformance), never promoted to PASS.
- **Read-only / forbidden writes:** `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` (T05 owns its accepted-event/Review authority sections; blob `ea007939639bbd6b4afbff1d71fdc19eb83d00be`), native review/event schemas (`schemas/agent-event-v2.schema.json`, `schemas/dispatch.schema.json`, all `schemas/**`), `templates/**`, `standard-manifest.json`, shared verifiers (`scripts/verify_standard.py`, `scripts/verify_project_standard.py`), `templates/GOLDEN_INDEX.md`, `checklists/version-closure.md`, `docs/implementation/4.11.0/{PRD.md,PRODUCT_PROOF_MATRIX.md,L2_ARCHITECTURE_EVIDENCE.md,TASK_DAG.md}`, other Tasks' owner clauses, `TASK_PACKS.json`, `main`, frozen planning branches — except where this DAG row grants ownership; the shared set is exclusively writable by T11.

### 3. Tests — executable acceptance oracles, not keyword-only checks

Fixtures use a deterministic injected read-boundary adapter that models sequential surface reads with explicit completeness/watermark facts; no live GitHub call is required for owner-local proof, and live multihost readback stays `NOT_RUN` until an admissible integrated environment exists. Each case asserts decision, sweep identity/completeness facts, exact subject bindings and absence of unauthorized mutation.

| Positive | Grounded scenario | Required oracle |
| --- | --- | --- |
| P01 | All §11/§14 prerequisites current: required Review PASS at exact subject, required Validation/Task links resolve, no unresolved release-significant finding, plan CURRENT | Complete sweep recorded with sweep identity, per-surface read refs and completeness facts; merge-ready admits; post-merge record carries source head, base before, integration SHA |
| P02 | Stale-subject PASS on an older HEAD coexists with current required PASS at live subject | Stale fact remains historical, is not counted; readiness computed from current facts only |
| P03 | Exact-head recheck at merge step finds head unchanged since sweep | Merge proceeds on the recorded sweep; no re-review demanded |
| P04 | Downstream dependent work exists after merge | Ready sets recomputed from MERGE_RESULT; downstream not prematurely READY before it |

| Adversarial | Input / fault | Required fail-closed oracle |
| --- | --- | --- |
| N01 | Blocker/dependency created after sweep completion, before merge | Recorded sweep invalidated; merge BLOCKED with zero partial mutation; re-sweep required |
| N02 | Reviews/checks listing truncated by pagination or watermark gap | Sweep marked INCOMPLETE; absence of blockers never inferred from an unread remainder; fail closed |
| N03 | Two opposite accepted REVIEW_DECISION events at the same exact subject | CONFLICT, not last-writer-wins; merge-ready denied; routes to Review-conflict handling under T05's read-only contract |
| N04 | HEAD/base drift after evidence (§12) | Stale evidence/base drift rejected; old evidence stays historical; no merge |
| N05 | Required Validation/Task/Review link missing, ambiguous, or bound to a different subject | Currentness fails closed; condition unsatisfied, never guessed |
| N06 | Implementation presents one cached combined read as GitHub-atomic truth | Oracle rejects any snapshot claim; sweep identity + exact-head recheck discipline enforced |
| N07 | Plan currentness STALE/UNKNOWN at the merge transition (§29.1) | Merge/merge-ready blocked; no lower-assurance path; recompute/rebind or stronger legal path only |

**Acceptance threshold:** all in-scope focused cases green on the exact implementation PR HEAD; no negative case mutates a protected merge record, gate or source; existing owner/regression tests remain passing or the failure is documented and blocking. Assertions exercise real owner contracts and decisions, not substring search. If T11 wiring (schema/manifest projection of sweep facts) is absent, that part is `DEFERRED_TO_T11` and whole-program conformance stays `NOT_RUN`/`DEFERRED_TO_T12`.

### 4. Contract — existing authority with bounded new semantics

Input tuple: exact source head, base/target SHA at sweep time, declared merge-ready prerequisites, per-surface read results with completeness/watermark facts, unresolved-finding aggregate, Assurance Plan currentness binding. Output: a bounded `LAST_ADMISSION_SWEEP` projection `{sweep_id, exact_source_head, exact_base_target, surfaces[{surface, read_ref, completeness, identity}], blockers, unresolved_findings, plan_currentness, verdict}` consumed by the guarded merge step: merge executes only when every surface is COMPLETE and current at the exact subject, no blocker exists, plan is CURRENT, and an exact-head recheck at the merge step itself still matches `exact_source_head`; any mismatch re-sweeps. Completeness is a recorded fact claim that must be readback-supported, never defaulted to complete. No new Gate enum value; current/stale fact rules of Interaction §9.1 are consumed read-only; §14's existing pre/post-merge duties and §29.1 consumption are preserved byte-compatible.

The Task Pack defines WHAT; no exact-base patch, line map, HEAD-locked branch command or hidden prompt is authority. Material new semantics must keep historical readers compatible and never silently reinterpret prior MERGE_RESULT or Review facts.

### 5. Implementation — minimum owner-local delta

Add small additive passages under §14 (and subordinate merge-admission procedure bullets) specifying: surface inventory, identity-bound read order, sweep-completeness watermark, late-blocker invalidation, same-head conflict fail-closed, exact-head merge recheck, and the no-atomic-snapshot rule; preserve all existing anchors and semantics. Implement the unique test as fixture-fed owner-contract assertions over the injected read-boundary adapter (positive and adversarial **decisions**, not prose-only substring asserts). Record any proposed addition to the shared `scripts/test_execution_architecture.py` as a T11 handoff item in the PR description without editing that file. T11 exclusively owns any central schema/manifest/verifier projection of sweep facts; T12 later proves integrated compound cases (Product #3 negatives) at conformance scale.

**L3 required handoff, ordered:** Tests above → this Contract → bounded owner-local Implementation → Failure Handling below → exact References here. Builder records an L3 evidence link, exact PR HEAD/base and source test identity; Task Claim/dispatch, code author, validator and independent reviewer remain distinct truthfully attributed actors.

### 6. Failure handling and UNKNOWN routing

Incomplete or failed surface read, watermark gap, late blocker, HEAD/base drift, same-head Review conflict, unresolvable link or STALE/UNKNOWN plan binding → `BLOCKED` (or `CONFLICT` where distinct) with the exact sweep id, subject identities and missing surface recorded, and the lawful route (re-sweep, rebind, review-conflict owner, T11 projection, owning authority). Never emit an optimistic merge-ready, never treat an unread remainder as empty, never ratify a merge that proceeded on an invalidated sweep. Failures block only genuine dependents; disjoint concerns proceed. Any Frozen Product/L2 incompatibility escalates to owning authority and independent review, not patched by this Builder.

### 7. Validation, Review and merge admission

- **Owner-local verification commands to evaluate and run later, not executed by this author:** `python -m unittest scripts.test_v411_merge_admission` (or repository-supported direct Python invocation); read-only regression references `python scripts/test_execution_architecture.py`, `python scripts/test_v48_execution_ownership.py`, `python scripts/test_v410_t06b_multi_dispatch_conformance.py`; verify commands against the actual environment and report exact command/exit/log.
- **Execution proof:** a real Local Build Host/Validator later records tested exact HEAD/tree, OS/toolchain, command, exit code, fixture/source SHA and evidence location. Offline owner-local results are not remote/integrated validation. Shared-suite integrated verification is `DEFERRED_TO_T11`; integrated A/B/C conformance is `DEFERRED_TO_T12`.
- **Review:** `RISK=high`, `REVIEW_POLICY=required`; a genuinely fresh independent Reviewer other than author and Builder binds findings, currentness, write-set conformance and verdict to the exact PR HEAD. Review PASS is not release permission.
- **Merge gate:** canonical native Task Issue + blocked-by graph materialized and read back; reviewed/frozen repository Pack; #973 stage3 baseline verified; protected accepted Claim per §11/§27–28; then a final current-state sweep and exact-head recheck immediately before the one-concern PR merges to the authorized version branch. No self-declared merge-ready; no Task-draft→Task-issue auto-promotion.
- **Later integration:** T14 consumes the T07-integrated baseline of the same owner file; T11 owns shared projections; T12 proves Product #3 conformance; V01/V02/V03/V04/R01/R02 remain separate work items, none authorized or marked PASS here.

### 8. Bounded Agent Freedom & deferred evidence ledger

```ini
F0_MECHANICAL=fixture_wiring_docs_links_imports_and_semantics_preserving_repair_only
F1_BOUNDED_IMPLEMENTATION=YES_EXACT_OWNER_CONTRACT_AND_POSITIVE_NEGATIVE_ORACLES_FIXED
F2_ENGINEERING_DISCRETION=ONLY_PROVEN_NONMATERIAL_INTERNAL_CHOICES_WITHIN_WRITESET
F3_ARCHITECTURE_REQUIRED=ESCALATE_TO_FROZEN_L2_PRODUCT_OR_OWNING_AUTHORITY_NO_SELF_PROMOTION
ACTOR_PRIVILEGE_ESCALATION=FORBIDDEN
SHARED_SUITE_EDITS=FORBIDDEN_HANDOFF_TO_T11
PR_TEST_RUN=NOT_RUN
REAL_BUILD_HOST=NOT_RUN
LIVE_GITHUB_READBACK=NOT_RUN
NATIVE_DEPENDENCY_READBACK=NOT_RUN
T11_CENTRAL_WIRING=DEFERRED_NOT_SATISFIED
T12_A_B_C_CONFORMANCE=DEFERRED_NOT_RUN
V01_V02_V03_V04_R01_R02=NOT_RUN
```

Epistemic ledger: current post-#973 integration HEAD, predecessor T05/T06 merged exact SHAs, native blocked-by readback, current Builder/Reviewer admission, the new focused test, shared wiring, live multihost sweep behavior and pagination-failure classes remain UNKNOWN/NOT_RUN until each owning actor supplies real evidence. No universal Product #3 completeness or release qualification is asserted.

### 9. Durable References and next owner

- Frozen Product: https://github.com/kaicreator-mm/ai-development-standard/issues/943#issuecomment-6084264198 (Product #3 dispatch/review/merge admission safety; PRD/matrix blobs above).
- Frozen L2: https://github.com/kaicreator-mm/ai-development-standard/issues/954; Frozen DAG: https://github.com/kaicreator-mm/ai-development-standard/issues/966 (T07 row, §2/§3, R2-F07 guard).
- Task Pack Controller: https://github.com/kaicreator-mm/ai-development-standard/issues/967; version seed: https://github.com/kaicreator-mm/ai-development-standard/issues/973. Batch A candidates are READ ONLY context: https://github.com/kaicreator-mm/ai-development-standard/pull/978.
- Owner sources cited by inspected blob: `standards/EXECUTION_ARCHITECTURE_STANDARD.md@5588d2196677b1b4878563de65edf2beaa10178f` (§12, §14, §29.1), `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md@ea007939639bbd6b4afbff1d71fdc19eb83d00be` (§9, §11), `scripts/test_execution_architecture.py@a17ba7290458b4115c985faaf5d65773c0cfd16d` (READ ONLY). Future dispatch rechecks every ref against the then-current lawful integration HEAD.

**Next:** an **independent Pack Reviewer**, not this author or any future Builder, challenges this draft for scope, executable oracle coverage, actual source-bounded gaps, provenance and DAG non-conflict. #967 then materializes one immutable repository Pack file at the intended path with its single index entry, conducts authoritative Pack Review/currentness, and only afterward permits separately qualified native Task Issue/blocked-by creation. This file is **NOT a Pack Freeze**, executable Task Issue, Builder Claim, implementation, CI result or Release decision.
