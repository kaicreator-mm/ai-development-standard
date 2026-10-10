<!-- v4.11 Task Pack CANDIDATE ONLY; author=LOCAL_BATCH_B_SUBAGENT_#984; product=#943, L2=#954, DAG=#966; not frozen; no Builder/Claim authority -->

## V411-V01 — TRUE independent real-host visible Validation/Closure of the exact integrated candidate DRAFT (author only)

```ini
PACK_DRAFT=SOURCE_BOUND_READY_FOR_INDEPENDENT_REVIEW
AUTHORSHIP=LOCAL_BATCH_B_SUBAGENT_DRAFT
INTENDED_FUTURE_PATH=docs/implementation/4.11.0/task-packs/V411-V01_independent_validation_closure.md
TASK_ID=V411-V01
ONE_CONCERN=INDEPENDENT_VISIBLE_VALIDATION_CLOSURE_OF_EXACT_CANDIDATE
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
FROZEN_DAG_PREDECESSORS=T12
RISK=critical
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

**Goal.** One concern: a genuinely **independent** Closure-scope Validator — a distinct actor from every Builder, owner-local Validator and Reviewer of T01–T14/T11/T12, and distinct from the V02 Candidate Freeze Controller — validates the exact dependency-complete integrated candidate (exact candidate SHA/tree produced by T12's terminal) on a real host, visibly, under validation scope `closure` (`VALIDATION_STANDARD.md` §4): visible full regression, Critical Journeys, applicable production build/artifact packaging/install, external tenant/effect evidence or positively grounded `NOT_APPLICABLE`, actual CI/profile runs when release-required, architecture/docs reconciliation, and a closure inventory. This is **not Task-PR CI**: Task/PR-local CI or review success never transfers to the candidate. The Validator owns the exact Validation Tuple `<exact tested SHA> × <real platform/environment> × <runtime/toolchain> × <validation profile>` (§3); a tuple proves only itself.

**Acceptance boundary.** Gate×subject resolution per Release authority (`RELEASE_STANDARD.md` §11): each Release-owned gate × exact subject carries an applicability decision `REQUIRED_NOW | DEFERRED_TO_VERSION_CLOSURE | NOT_APPLICABLE | UNKNOWN` plus exactly one Gate state `PASS | FAIL | BLOCKED | NOT_RUN | NOT_APPLICABLE` (§1). Every `REQUIRED_NOW` gate must be `PASS` on the exact candidate tuple or the overall closure verdict is not PASS; `UNKNOWN` applicability or missing evidence stays `NOT_RUN/BLOCKED` and routes to the Release owner — it never becomes `NOT_APPLICABLE` or PASS. An inherited concern-stage `DEFERRED_TO_VERSION_CLOSURE` never satisfies a version gate by inheritance (`CONCERN_DEFERRED != VERSION_GATE_SATISFIED`, RELEASE §11.1/§11.3): every inherited deferral must receive a fresh gate × composed-version-subject applicability re-evaluation, owned by the Release authority and durably bound on the exact version candidate; any inherited deferral still unresolved at the version-candidate boundary keeps its gate `BLOCKED/NOT_RUN` and the closure verdict not-PASS — it can never yield Closure PASS, while an actually `REQUIRED_NOW` gate must still `PASS` and a positively authority-grounded `NOT_APPLICABLE` remains valid. Any permitted CI waiver exists **only by owning policy**, recorded with its authority ref. No Builder self-PASS: the Validator must not repair, weaken, merge, or close anything (§9); a real defect produces `FAIL` and a separate Builder dispatch.

**Non-goals:** no implementation-source delta, no Candidate Freeze/Hidden/Fresh Closeout/RQ/integration authority (V02/V03/V04/R01/R02 remain six distinct actors and terminals per the frozen DAG), no new workflow state machine, no universal-completeness claim over the unknown intersection denominator, and no release PASS manufactured by this Pack draft.

### 2. Frozen dependency, sole owner and explicit exclusions

- **Frozen DAG row:** `FROZEN_DAG_PREDECESSORS=T12` exactly — the sole TRUE dependency; V01 sits at position T11 → T12 → **V01** → V02 → V03 → V04 → R01 → R02 in the frozen topology. No extra dependency is invented. This describes topology only, **not current Task READY**; DAG freeze, native Issue materialization, Pack admission and protected Claim prerequisites still apply.
- **Sole owner:** one dispatch with role `validator`, execution profile `CLOSURE_VALIDATOR`, admitted as a single distinct actor; it owns the exact Validation Tuple and its own terminal. An L3 executor must never collapse V01 into a Builder terminal or into V02–R02.
- **Allowed future write set — own gate evidence artifacts only** (exact evidence output paths, derived from v4.10 precedent naming `docs/implementation/4.10.0/V410_V01_VALIDATION_CONTRACT.md`; all three are NEW paths, absent at version seed tree `1bfac20e90c69bb57db4f293148b7264d292b5be`; uniqueness re-verified at JIT dispatch):
  - `docs/implementation/4.11.0/V411_V01_VALIDATION_CONTRACT.md` — version closure work contract and per gate×subject applicability decision record binding `gate_id, subject_ref, subject_identity, applicability, release_authority_ref, decision_ref, basis_or_proof_refs, candidate_or_currentness_identity, decided_at, actor_or_operator` (RELEASE §11.2), including one fresh re-evaluation record for every inherited concern-stage `DEFERRED_TO_VERSION_CLOSURE`.
  - `docs/implementation/4.11.0/V411_V01_VALIDATION_EVIDENCE.md` — exact-SHA tuple evidence index explicitly binding the triplet `tested_sha` (actual executed commit) × `evidence_only_head` (later evidence-recording commit) × `candidate_sha`/tree plus the final branch/ref identity carrying them, so later evidence-recording commits are never relabelled as the tested SHA; also base/HEAD drift facts, host/platform/runtime/profile, exact commands, exit codes, key logs/refs (VALIDATION §6–§7, §12 minimum).
  - `docs/implementation/4.11.0/V411_V01_CLOSURE_INVENTORY.md` — closure inventory: full gate×subject state table, known limitations/deferred items, architecture/docs reconciliation result. This is V01's own evidence artifact; `checklists/version-closure.md` remains a READ ONLY input, never rewritten here. Machine payloads use read-only `schemas/validation-report.schema.json`; durable evidence recording preferably lives in Issue/events/external evidence storage (VALIDATION §7), and only the three paths above may be written in-repo.
- **Read-only / forbidden writes:** all `schemas/**`, `templates/**`, `standard-manifest.json` (inspected `971ebcb65c19f68e8d634d75d8ea96ee30957edf`), shared verifiers `scripts/verify_standard.py` (`a6233b79f8b60594e79302eee1c0e1bb30d0eab0`), `scripts/verify_project_standard.py`, `templates/GOLDEN_INDEX.md` (`b36d4947cfe7db101e9eb4955ea889b55d988ed1`), `checklists/version-closure.md` (`2483856a53fbc0127378c45915ad2518819de996`), `docs/implementation/4.11.0/{PRD.md,PRODUCT_PROOF_MATRIX.md,L2_ARCHITECTURE_EVIDENCE.md,TASK_DAG.md}`, all T01–T14/T11/T12 implementation source and owner clauses (incl. `scripts/test_v411_merge_admission.py`, `scripts/test_v411_task_learning.py`, T12 golden fixtures), `TASK_PACKS.json`, all other V/R pack files, `main`, frozen planning branches, `version/v4.10.0`. Binding read set (inspected blob guards at the version seed): `standards/VALIDATION_STANDARD.md@1522b85f9e68cc4a1591ea5899b53c224998e5a8`, `standards/RELEASE_STANDARD.md@c4d72506253ca7f3d95e305dbd84aae0e1fbe2cb`, `standards/EXECUTION_ARCHITECTURE_STANDARD.md@5588d2196677b1b4878563de65edf2beaa10178f`; a changed blob at dispatch demands scoped currentness rebind before execution.

### 3. Tests — executable acceptance oracles, not keyword-only checks

Every oracle is executed later by the owning CLOSURE_VALIDATOR on a real host against the exact candidate; the draft author executed **nothing** (`NOT_RUN`).

| Positive | Grounded scenario | Required oracle |
| --- | --- | --- |
| P01 | Clean checkout of exact candidate SHA/tree; `requested_head_sha == current ref HEAD`; working tree clean | Full visible regression executed on the exact tuple; per-gate `PASS/FAIL` with commands+exit codes bound to `tested_sha` |
| P02 | Frozen-scope Critical Journeys on a real host | Each journey outcome recorded with actor/host/runtime identity; no journey inherited from Task PRs |
| P03 | Applicable production build + artifact packaging/install where Release applicability is `REQUIRED_NOW` | Artifact identity, build/package/install commands and results recorded on the same tuple |
| P04 | External tenant/effect gate applicable | Real external evidence captured, or a positively authority-grounded `NOT_APPLICABLE` decision with basis refs |
| P05 | CI/profile runs that owning policy makes release-required | Actual provider runs recorded; any waiver cites the owning policy ref and scope, never cost/effort |
| P06 | Architecture/docs reconciliation inputs current | Reconciliation verdict per owner doc with exact blob identities; mismatches listed as unresolved findings |

| Adversarial | Input / fault | Required fail-closed oracle |
| --- | --- | --- |
| N01 | CI PASS offered as platform/CJ/packaging/external PASS | Gate stays `NOT_RUN`; CI is executor, never Release Authority (VALIDATION §8/§13) |
| N02 | `requested_head_sha != current HEAD` at dispatch | `HEAD_DRIFT`; no execution as PASS evidence; no silent switch to successor SHA |
| N03 | Older-SHA/Task-PR evidence relabelled as candidate closure | Rejected; PASS never rewritten onto another SHA/tree/tuple (VALIDATION §6/§13) |
| N04 | `NOT_APPLICABLE` claimed from cost, change size, docs-only appearance or model confidence | Invalid; applicability `UNKNOWN`, gate `NOT_RUN/BLOCKED`, routed to Release owner |
| N05 | Missing external-effect evidence while gate is applicable | `UNKNOWN/BLOCKED`; no closure PASS; blocker propagates only through real edges (VALIDATION §11) |
| N06 | Validator repairs source or weakens/deletes a test to clear a gate | Discipline `FAIL`; defect routed to separate Builder dispatch; original gate state preserved |
| N07 | Base/merge-result advanced after validation without `VALIDATION_IMPACT_DECISION` | Old evidence not reused as merge-result PASS; affected gates re-established |
| N08 | Concern-stage `DEFERRED_TO_VERSION_CLOSURE` inherited into Version Closure with no fresh version-candidate decision | Every inherited deferral re-evaluated fresh by the Release owner on the exact composed candidate; any unresolved inherited deferral stays `BLOCKED/NOT_RUN` and the closure verdict is not-PASS, never inherited as version-gate-satisfied (RELEASE §11.1/§11.3) |
| N09 | Evidence-only descendant `evidence_only_head` E != tested candidate `tested_sha` C promoted as tested/freezable by ancestry | E does not inherit C's executed tuple; freeze C or record an explicit owner-attributed `VALIDATION_IMPACT_DECISION` with gate-specific revalidation where affected/unknown (VALIDATION §6/§7) |

**Acceptance threshold:** every in-scope gate×subject row carries exactly one applicability value and one Gate state with durable evidence refs; every inherited concern-stage `DEFERRED_TO_VERSION_CLOSURE` carries a fresh version-candidate Release-owned re-evaluation record and any still-unresolved inherited deferral keeps the overall closure verdict not-PASS; any `REQUIRED_NOW` row not `PASS` makes the overall closure verdict not-PASS, recorded truthfully as `FAIL/BLOCKED/NOT_RUN` — never renamed (RELEASE §10).

### 4. Contract — existing authority with bounded new semantics

Existing authority owns all semantics: `VALIDATION_STANDARD.md` §1–§13 (gate states, tuple, closure scope, exact-SHA drift, validator allowed/MUST-NOT set, evidence minimum, prohibited practices), `RELEASE_STANDARD.md` §2/§3/§10/§11 (inputs, prepared vs frozen, closure checklist, gate×subject applicability), `EXECUTION_ARCHITECTURE_STANDARD.md` dispatch lifecycle and validator profiles, `checklists/version-closure.md` as closure input. Bounded new semantics: v4.11 instantiates the closure contract for this version candidate and adds only the three owned evidence artifacts above; no new Gate enum, no new lifecycle state, no second validation authority. `UNKNOWN` is epistemic routing, not a sixth gate state. Contradictions with Frozen Product/L2 route upward as `TASK_PACK_DEFECT/ARCHITECTURE_CONTRADICTION` — never silently resolved by the executor.

### 5. Implementation — minimum owner-local delta

The deliverable is evidence, not source: execute the declared closure profile on the exact candidate and record the three owned artifacts, with machine payloads against read-only `schemas/validation-report.schema.json`. L3 mapping: Tests (§3 oracles) → Contract (§4) → Implementation (validation run + artifacts) → Failure Handling (§6) → References (§9). Builder role is `NOT_APPLICABLE` for this node; any source repair discovered here requires a separate Builder dispatch and re-establishes affected evidence under exact-SHA currentness rules. Validation ownership is `closure` (whole-candidate); concern/integration scopes stay with their owning Tasks and are inputs, never substitutes.

### 6. Failure handling and UNKNOWN routing

Missing/failed prerequisite, unavailable environment/toolchain/provider → `BLOCKED` (infrastructure facts use `CI_INFRA_EXCEPTION`, never product FAIL/PASS). Missing evidence for a plausibly applicable gate → `UNKNOWN` applicability + `NOT_RUN/BLOCKED` state, routed to the Release authority; fail-closed. Executed-but-failed required check → `FAIL` with exact subject and repair routed to a separate Builder dispatch; deterministic FAIL is not erased by opportunistic re-runs. HEAD/BASE/merge-result/CANDIDATE drift handled per VALIDATION §6 (new dispatch identity for new candidate; `VALIDATION_IMPACT_DECISION` discipline for evidence-preserving successors). Waiver requests route to owning policy only. Any Frozen Product/L2 contradiction escalates to owning authority; V01 never patches authority text.

### 7. Validation, Review and merge admission

- **Owner-local verification commands to evaluate and run later by the owning validator, not executed by this author:** the repository's registered regression entrypoints, `python scripts/test_v49_conformance_suite.py`, the T12-registered v4.11 golden fixture/conformance suite, applicable build/package/install toolchain commands, and release-required CI/profile triggers — exact command set bound at JIT dispatch against the then-current candidate; every command reports exit code/log or explicit `NOT_RUN/BLOCKED`.
- **Execution proof:** real host records exact tested HEAD/tree, OS/arch/toolchain, commands, exit codes, evidence locations, waiver authority refs, and unrun material cases; earlier v4.10 or planning-stage evidence is analysis input only, never relabelled v4.11 PASS.
- **Review:** `risk:critical`, `review:required`; a genuinely fresh independent Reviewer, distinct from the Validator and every Builder, binds verdict to the exact evidence artifact SHAs; Review PASS is not release permission.
- **Admission:** V01's terminal is its durable validation evidence, not a merge; committing the three owned artifacts on the authorized v4.11 integration branch occurs only after dependency-complete T12 admission and independent Review. Candidate Freeze (V02), Hidden (V03), Fresh Closeout (V04), RQ (R01) and Repository Integration (R02) are separate actors/terminals — none authorized or marked PASS here.

### 8. Bounded Agent Freedom & deferred evidence ledger

```ini
F0_MECHANICAL=EVIDENCE_ARTIFACT_WIRING_LINKS_ONLY_NO_SOURCE_DELTA
F1_BOUNDED_IMPLEMENTATION=VALIDATION_EXECUTION_PER_FROZEN_GATES_AND_ORACLES_FIXED
F2_ENGINEERING_DISCRETION=NONE_VALIDATOR_MAY_NOT_REDESIGN_WEAKEN_OR_REPAIR
F3_ARCHITECTURE_REQUIRED=ESCALATE_TO_OWNING_RELEASE_PRODUCT_OR_L2_AUTHORITY
ACTOR_PRIVILEGE_ESCALATION=FORBIDDEN
BUILDER_SELF_PASS=FORBIDDEN
VALIDATOR_SOURCE_REPAIR=FORBIDDEN
CANDIDATE_IDENTITY=UNKNOWN_UNTIL_T12_TERMINAL
VISIBLE_FULL_REGRESSION=NOT_RUN
CRITICAL_JOURNEYS=NOT_RUN
PLATFORM_BUILD_PACKAGE_INSTALL=NOT_RUN
EXTERNAL_EFFECT_EVIDENCE=NOT_RUN
CI_PROFILE_RUNS=NOT_RUN
ARCHITECTURE_DOCS_RECONCILIATION=NOT_RUN
CLOSURE_INVENTORY=NOT_PRODUCED
V02_V03_V04_R01_R02=NOT_RUN_BY_THIS_NODE
```

Epistemic ledger: exact candidate identity, host/platform/toolchain coverage, external-boundary access, provider availability, waiver policy currentness and gate×subject truth remain `UNKNOWN/NOT_RUN` until the owning Validator supplies real evidence. No whole-version P1/P2/P3 completeness, closure PASS or release qualification is asserted by this draft.

### 9. Durable References and next owner

- Frozen Product: https://github.com/kaicreator-mm/ai-development-standard/issues/943#issuecomment-6084264198 (PRD/matrix blobs above).
- Frozen L2: https://github.com/kaicreator-mm/ai-development-standard/issues/954; Frozen DAG: https://github.com/kaicreator-mm/ai-development-standard/issues/966 (exact head/blob above; §2 V01 row and §3 topology control).
- Task Pack Controller: https://github.com/kaicreator-mm/ai-development-standard/issues/967; version seed: https://github.com/kaicreator-mm/ai-development-standard/issues/973; Batch A candidates READ ONLY: https://github.com/kaicreator-mm/ai-development-standard/pull/978 (do not duplicate).
- Governing standards (exact qualified v4.10 owner baseline, re-read at dispatch): `standards/VALIDATION_STANDARD.md`, `standards/RELEASE_STANDARD.md`, `standards/EXECUTION_ARCHITECTURE_STANDARD.md`, `checklists/version-closure.md`.

**Next:** an **independent Pack Reviewer**, not this author, challenges this draft for scope, oracle coverage, actor independence and DAG non-conflict; #967 materializes one immutable repository Pack file at the intended path plus its index entry. This Issue/draft comment is **NOT a Pack Freeze, dispatch, validation execution, closure verdict or Release decision**; the CLOSURE_VALIDATOR runs everything later on a real host, and V02 Candidate Freeze belongs to a different actor entirely.
