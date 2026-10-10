<!-- v4.11 Task Pack CANDIDATE ONLY; author=LOCAL_BATCH_B_SUBAGENT_#984; product=#943, L2=#954, DAG=#966; not frozen; no Builder/Claim authority -->

## V411-T02 — affected-source materiality inventory DRAFT (author only)

```ini
PACK_DRAFT=LOCAL_DRAFT_READY_FOR_INDEPENDENT_REVIEW
AUTHORSHIP=LOCAL_BATCH_B_SUBAGENT_DRAFT
INTENDED_FUTURE_PATH=docs/implementation/4.11.0/task-packs/V411-T02_source_materiality_inventory.md
TASK_ID=V411-T02
ONE_CONCERN=AFFECTED_SOURCE_MATERIALITY_INVENTORY_INSPECTED_ABSENT_VS_UNINSPECTED_UNKNOWN
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
FROZEN_DAG_PREDECESSORS=T01
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

**Goal.** One affected-source materiality inventory per changed subject, produced inside the Workflow risk-intake section. For every actually inspected changed source the owner records an epistemic state — `PRESENT` (material class observed, with inspection ref), `ABSENT_WITH_INSPECTED_SCOPE` (class checked and genuinely absent within the stated inspected scope), or `UNKNOWN` (not actually inspected, uninspectable, or currentness unproven). A missing or optimistic job label is never a safe shortcut: an uninspected material change is `BLOCKED`, never `NOT_APPLICABLE`. The inventory consumes T01's effective-rule floor **read-only** and supplies observed facts to it; it is not a second authority.

**Already implemented on qualified v4.10 owner source; retain rather than duplicate.** `standards/DEVELOPMENT_WORKFLOW.md` §3 "Stage 0 — Intake / Baseline" already records scope/HEAD/acceptance/known blockers; §2 "Intake 时先选择 Integration Mode" owns integration mode; §4 "Gate Authority" (subsections "Gate applicability 与合法来源" and "Applicability UNKNOWN 或矛盾：fail closed") owns gate applicability and fail-closed routing — T01 owns only the effective-rule subsection there; §5 "Blocker Propagation" and §7 "快速路径" own proportionality.

**Concrete still-missing v4.11 delta.** No owner today derives materiality from *actually inspected changed sources* (diff-derived permission/API/deployment/security/external-effect facts) with a per-source epistemic state. An omitted or optimistic `J02_DOCS_LOW_RISK`-style label can hide a real permission/API/deployment delta from applicability closure, and "not inspected" is silently conflated with "checked and absent". T02 supplies exactly this distinction and the actual source/HEAD/currentness observation the DAG row demands.

**Task deliverable (future Builder work, not done by this author):** bounded normative risk-intake clauses + one unique focused test `scripts/test_v411_t02_risk_intake.py`; source/currentness-bound PR-local test report and exact-HEAD independent Review. **Non-goals:** a second applicability authority, gate-enum changes, risk-scoring engines, wholesale intake rewriting, T01 floor edits, T11 shared wiring, release/host PASS.

### 2. Frozen dependency, sole owner and explicit exclusions

- **Frozen DAG predecessors exactly `T01`** (its effective-rule floor and `PRESENT/ABSENT_WITH_INSPECTED_SCOPE/UNKNOWN` semantics, consumed read-only). Frozen DAG §3 also makes `T13` follow `T02`, and `T08` follows `T02`; both are successors this pack must not preempt. Dependency edges are planning facts; no Task READY exists before canonical native materialization.
- **Allowed future normative write set (no other existing source path):**
  - `standards/DEVELOPMENT_WORKFLOW.md` (inspected blob `a7fef842927e58a93b671fe9869b9395559845ac`), **risk-intake section only**.
  - **NEW unique** `scripts/test_v411_t02_risk_intake.py` only; no reuse or edit of any existing shared test.
- **DAG ambiguity resolved here:** the inspected blob contains **no section literally named "risk-intake"**. Resolution: T02 owns one new bounded intake-stage-adjacent section (co-located with §2/Stage 0 intake duties); preexisting §2 and Stage 0 semantics are preserved verbatim; the section is disjoint from T01's §4 effective-rule subsection and from T13's future role-conduct section — three distinct sequential owners of one file, serialized by the frozen DAG.
- **Read-only / forbidden writes:** `standards/DEVELOPMENT_WORKFLOW.md` sections outside the risk-intake section (including all T01-owned clauses); the central Task template (`templates/**`, explicitly read-only per the DAG row); all `schemas/**`, `standard-manifest.json`, shared verifiers (`scripts/verify_standard.py`, `scripts/verify_project_standard.py`), existing shared tests, `templates/GOLDEN_INDEX.md`, `checklists/version-closure.md`, `docs/implementation/4.11.0/{PRD.md,PRODUCT_PROOF_MATRIX.md,L2_ARCHITECTURE_EVIDENCE.md,TASK_DAG.md}`, `docs/implementation/4.11.0/TASK_PACKS.json`, other Tasks' owner clauses (T03–T14 owners), `main`, `version/v4.10.0`, frozen planning branches. Shared projections are **proposals routed to exclusive T11**; no shadow schema/template.

### 3. Tests — executable acceptance oracles, not keyword-only checks

All cases bind exact subject + changed-source set + per-source inspected ref/HEAD; assert decision, epistemic state, required-gate set inherited from the T01 floor, and absence of unauthorized mutation. Deterministic offline Git/diff fixtures are legal; claims beyond fixture scope stay `NOT_RUN/BLOCKED`.

| Positive | Grounded scenario | Required oracle |
| --- | --- | --- |
| P01 | Inspected diff actually touches permission/API/deployment surface, declared `J` set includes it | Inventory records `PRESENT` per class with source path + inspected blob/HEAD ref; T01 floor gate set unchanged and enforced |
| P02 | Full changed-source set inspected; no material class present | Per-class `ABSENT_WITH_INSPECTED_SCOPE` carrying the inspected scope ref; proportionate Fast Path retained, no speculative ceremony |
| P03 | `J02_DOCS_LOW_RISK`-labeled change, inspection confirms docs-only scope | Proportional A0 path stands; inventory still lists per-source states, no blanket full-version record forced |
| P04 | Same subject resolved through T01 effective-rule trace with inventory facts attached | Conjunction of owner predicates identical to T01 floor; inventory adds observations only, no second resolution path |

| Adversarial | Input / fault | Required fail-closed oracle |
| --- | --- | --- |
| N01 | Diff shows permission/API/deployment change while label is `J02`-only or missing | Decision `BLOCKED`; `NOT_APPLICABLE`/`PASS` forbidden; missing label never waives observed materiality |
| N02 | Material-class file in changed set has no real inspection (no observation ref/currentness) | `UNKNOWN`, never `ABSENT_WITH_INSPECTED_SCOPE`; downstream gate stays `NOT_RUN/BLOCKED` |
| N03 | Inspection ref from stale HEAD (older than candidate/tree) | Currentness check fails; state demoted to `UNKNOWN`; stale ABSENT never promoted to current absence |
| N04 | Inventory output used to waive/demote a T01-required gate, or minted as new gate enum/authority | Rejected: epistemic facts only; higher-authority requirement persists unchanged |
| N05 | Materiality data encoded in central Task template/schema/manifest to bypass owner section | Rejected: template/schema/manifest read-only; additive proposal routed to T11 as `DEFERRED_TO_T11`, no shadow file |

**Acceptance threshold:** all in-scope focused cases green on the exact implementation PR HEAD; negative cases cannot mutate any gate, authority or owner section; existing owner/regression tests keep passing or the failure is documented and blocking. If T11 shared wiring is absent, affected projections stay `DEFERRED_TO_T11` and whole-program conformance stays `NOT_RUN`.

### 4. Contract — existing authority with bounded new semantics

Input: exact subject; candidate HEAD/tree; changed-source set with per-source inspection evidence (path, inspected blob/HEAD ref, class observations); declared `J` set; role/archetype context. Output: one `MATERIALITY_INVENTORY` risk trace per subject — `{subject, source_path, inspected_ref, material_class_observed, epistemic_state∈{PRESENT,ABSENT_WITH_INSPECTED_SCOPE,UNKNOWN}, currentness, required_gate_ref, resolution_route}` — produced by and consumed under the risk-intake section. The three states are **epistemic facts about inspection**, not new Validation Gate states; gate applicability stays with §4 authority resolution (T01 floor). An uninspected source is `UNKNOWN` by default; `ABSENT_WITH_INSPECTED_SCOPE` requires affirmative inspection evidence within a stated scope. The pack defines WHAT only: no exact-base patch, line map, transient-HEAD branch command or chat prompt is authority.

### 5. Implementation — minimum owner-local delta

Add one bounded risk-intake section to `standards/DEVELOPMENT_WORKFLOW.md` defining inventory duty, per-source epistemic states, currentness binding and the missing-label-never-a-shortcut rule; preserve all anchors and neighboring sections. Implement `scripts/test_v411_t02_risk_intake.py` as fixture-fed **decision** assertions (positive and adversarial), not prose substring checks; reference real owner logic. T01 floor, §4 gate authority, T13 role conduct and T08 human authority stay untouched. T11 exclusively owns any shared schema/template/manifest/verifier projection of the trace. **L3 order:** Tests → Contract → bounded Implementation → Failure Handling → References; Builder records L3 evidence, exact PR HEAD/base and test identity with truthfully distinct author/builder/validator/reviewer actors.

### 6. Failure handling and UNKNOWN routing

Uninspected material fact → `UNKNOWN`/`BLOCKED` routed per §4 "Applicability UNKNOWN 或矛盾：fail closed" to the owning authority; never silently `N/A`. Conflicting observations or label-vs-inspection contradiction → `CONFLICT` with owning-authority route, preserving historical facts. Stale or missing inspection ref → re-inspection demanded, no inferred currentness. Missing shared projection → `DEFERRED_TO_T11`, not T02 integrated PASS. Frozen Product/L2 incompatibility escalates to owning authority and independent review; this Builder never patches it locally.

### 7. Validation, Review and merge admission

- **Owner-local verification commands to evaluate and run later, NOT executed by this draft author:** `python -m unittest scripts.test_v411_t02_risk_intake` (or repository-supported direct Python invocation), plus regression `python scripts/test_v49_gate_currentness.py`, `python scripts/test_v410_t04a_gate_repair_routing.py`, `python scripts/test_v40_adoption_migration.py`, `python scripts/test_v49_conformance_suite.py`. Future runs must record exact command/exit/log against the real environment.
- **Execution proof:** the future real Build Host/Validator binds tested exact HEAD/tree, OS/toolchain, command, exit code, fixture/source SHA and evidence location; source-only/offline results never become host, Hidden or Release validation.
- **Review:** `risk:high`, `review:required`; a genuinely fresh independent Reviewer distinct from author and Builder binds currentness, write-set conformance, findings and verdict to the exact PR HEAD. Review PASS alone is not release permission.
- **Merge gate:** canonical native blocked-by graph (T01 → T02; T02 → T13, T02 → T08) created and read back, #973 baseline seed verified, JIT Execution Pack + protected accepted Claim, then one-concern PR to the authorized v4.11 integration branch only; exact-HEAD recheck immediately before merge; no automatic draft→issue promotion.
- **Later integration:** T13 consumes T02 inventory states for role-scoped required evidence; T08/T09/T12/V01 consume them downstream; Candidate Freeze, Hidden, Fresh Closeout, RQ and guarded integration remain separate V/R work items, none PASSed by this pack.

### 8. Bounded Agent Freedom & deferred evidence ledger

```ini
F0_MECHANICAL=fixture_wiring_docs_links_imports_and_semantics_preserving_repair_only
F1_BOUNDED_IMPLEMENTATION=YES_EXACT_OWNER_CONTRACT_AND_POSITIVE_NEGATIVE_ORACLES_FIXED
F2_ENGINEERING_DISCRETION=ONLY_PROVEN_NONMATERIAL_INTERNAL_CHOICES_WITHIN_WRITESET
F3_ARCHITECTURE_REQUIRED=ESCALATE_TO_FROZEN_L2_PRODUCT_OR_OWNING_AUTHORITY_NO_SELF_PROMOTION
ACTOR_PRIVILEGE_ESCALATION=FORBIDDEN
PR_TEST_RUN=NOT_RUN
REAL_BUILD_HOST=NOT_RUN
NATIVE_DEPENDENCY_READBACK=NOT_RUN
T01_FLOOR_CONSUMPTION=READ_ONLY_ASSUMED_CURRENT_AT_DISPATCH
T11_CENTRAL_WIRING=DEFERRED_NOT_SATISFIED
T12_A_B_C_CONFORMANCE=NOT_RUN
V01_V02_V03_V04_R01_R02=NOT_RUN
```

Epistemic ledger: current integration HEAD post-#973, native dependency readback, admitted Builder/Reviewer operators, real execution of the focused and regression tests, T11 wiring and integrated conformance are **UNKNOWN/NOT_RUN** until each owning actor supplies evidence. No universal applicability completeness or release qualification is asserted; the unknown-inspection denominator must stay stated, never absorbed into a PASS.

### 9. Durable References and next owner

- Frozen Product: https://github.com/kaicreator-mm/ai-development-standard/issues/943#issuecomment-6084264198 (PRD blob above; `PROPORTIONALITY` and applicability-closure invariants apply).
- Frozen L2: https://github.com/kaicreator-mm/ai-development-standard/issues/954; Frozen DAG: https://github.com/kaicreator-mm/ai-development-standard/issues/966 (T02 row + §3 topology).
- Task Pack Controller: https://github.com/kaicreator-mm/ai-development-standard/issues/967; version seed: https://github.com/kaicreator-mm/ai-development-standard/issues/973.
- Batch A T01 candidate (predecessor, READ ONLY, do not duplicate): PR https://github.com/kaicreator-mm/ai-development-standard/pull/978.
- Applicable current standards: `EXECUTION_PACK_STANDARD.md` §2/§5/§6/§8, `TASK_DECOMPOSITION_STANDARD.md`, `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, `VALIDATION_STANDARD.md` from the exact qualified v4.10 baseline; owner blobs re-inspected at the version seed table above.

**Next:** an **independent Pack Reviewer**, not this author or a future Builder, challenges this draft for scope, oracle coverage, actual source-bounded gaps, provenance and DAG non-conflict against the inspected blob `a7fef842927e58a93b671fe9869b9395559845ac`. #967 then materializes one immutable repository Pack at the intended path with its index entry, conducts authoritative Pack Review/currentness, and only then permits separately qualified native Task Issue/blocked-by creation. This file is **NOT a Pack Freeze**, executable Task Issue, Builder Claim, implementation, CI result or Release decision.
