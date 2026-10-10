<!-- v4.11 Task Pack CANDIDATE ONLY; author=#968@6094571852; product=#943, L2=#954, DAG=#966; not frozen; no Builder/Claim authority -->

## V411-T01 — source-bound immutable-Task-Pack-ready DRAFT (author only)

```ini
PACK_DRAFT=SOURCE_BOUND_READY_FOR_INDEPENDENT_REVIEW
AUTHORSHIP_TASK_ISSUE=#968
INTENDED_FUTURE_PATH=docs/implementation/4.11.0/task-packs/V411-T01_pinned_effective_rules.md
TASK_ID=V411-T01
ONE_CONCERN=PINNED_EFFECTIVE_RULES
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
SOURCE_PREFLIGHT=#961@6094394270
FROZEN_DAG_PREDECESSORS=NONE
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

**Goal.** One pinned ADS effective-rule trace; A0–A4 non-weakening; actual-risk-driven multi-J conjunction. Produce owner-local normative resolution semantics and a focused falsifiable trace test. For the same inspected material facts, A0/manual and A4/automated must demand the same hard predicates. One job label, profile or lower-authority override must never suppress another owner's required gate. Provide a proposed T11 shared verifier/schema integration delta without editing its files.

**Already implemented on qualified v4.10 owner source; retain rather than duplicate.** Immutable 40-hex ADS revision + VERSION resolution, one standard pin, current §4 owner precedence (Frozen PRD/Contract > Frozen L2 > Overrides > Task > defaults), same mandatory validation/review/release floor for A0–A4, fail-closed applicability and proportionate Fast Path already exist. Preserve v4.0 adoption tests, v4.10 gate-routing tests and v4.9 C01 conjunction/currentness models. Existing v4.9 helper composes **given** concerns; it does not discover risks from actual affected-source observations.

**Concrete still-missing v4.11 delta.** Neither owner presently defines a complete auditable R01/R12 effective-rule trace that jointly binds immutable pin, current authority subject, profile/role/archetype, job-label **set**, independently inspected changed-source risk, per-owner precedence, cross-owner AND, evidence freshness and UNKNOWN/CONFLICT. Omitting J07 can wrongly hide actually inspected security materiality if decisions are based solely on declarations. Current generic verifier only tests existence of overrides, not contradictory adoption values; T11 owns shared verifier repair.

**Task deliverable:** minimal owner-local normative clauses plus **one unique** focused test `scripts/test_v411_t01_effective_rules.py`; a source/currentness-bound PR-local test report and exact-HEAD independent Review; an explicit T11 handoff for any required centrally owned projection. These are future Builder deliverables, **not work completed by this author**. The ultimate implementation PR targets the authorized v4.11 version integration branch (expected `version/v4.11.0` **only after** #973's seed readback and controller admission), one concern/one PR; never direct to `main` or old planning ancestry.

**Non-goals:** a second ADS method/authority, new mandatory runtime/server/scheduler/DB, wholesale stage rewriting, universal job combinations or automatic real-host/release PASS, changes owned by any other Task, and promoting fixture simulation to independently executed proof.

### 2. Frozen dependency, sole owner and explicit exclusions

- Frozen logical DAG has **zero executable predecessors** for V411-T01; this describes only topology, **not current Task READY**. All gate/Claim/Issue admission prerequisites still apply. Task author here has no executable Builder identity.
- **Allowed future normative write set** (no other existing source path):
  - `standards/PROJECT_ADOPTION.md` (inspected blob `cb1edecc0423a0c34c0b6457cdde18ab36c18bfb`, only §§2.2, 3.4, 3.7 bounded effective-rule/adoption addition)
  - `standards/DEVELOPMENT_WORKFLOW.md` (inspected blob `a7fef842927e58a93b671fe9869b9395559845ac`, **only** §4 Gate Authority effective-rule/provenance subsection)
  - **NEW unique** `scripts/test_v411_t01_effective_rules.py` only; no reuse of any shared existing test.
- **Read-only / forbidden writes:** all `schemas/**`, `templates/**`, `standard-manifest.json`, shared verifiers (including `scripts/verify_standard.py` and `scripts/verify_project_standard.py`), shared legacy tests, `templates/GOLDEN_INDEX.md`, `checklists/version-closure.md`, `docs/implementation/4.11.0/{PRD.md,PRODUCT_PROOF_MATRIX.md,L2_ARCHITECTURE_EVIDENCE.md,TASK_DAG.md}`, other Tasks' owner clauses, `main`, `version/v4.10.0`, frozen planning branches. Any shared change **proposal** is routed to exclusive T11; no shadow schema or parallel common-file writer.
- **Authority:** Product #943 explicit human-approved Freeze, separately reviewed/frozen L2 #954 and DAG #966. Their exact refs are inputs; preflight #961@6094394270 was read-only advisory and its prior `DAG_FREEZE=NO` status is **historical at preflight time**, superseded as a planning state by independently recorded #966, not retroactively converted into execution evidence. Any mismatch at real dispatch blocks and demands scoped rebind.

### 3. Tests — executable acceptance oracles, not keyword-only checks

For all cases, assert exact fixture subject and relevant source/role/authority identity, **decision**, missing/stale evidence and absence of unauthorized side effects; use deterministic offline fixtures where appropriate. Each positive and negative case must actually execute against the later candidate or explicitly report `NOT_RUN/BLOCKED`.

| Positive | Grounded scenario | Required oracle |
| --- | --- | --- |
| P01 | Exact single standard revision, current owner identities, accepted authority sources | Trace resolves and retains pin/owner/subject/observation/proof refs; no second methodology |
| P02 | Identical SERVICE/BROWNFIELD permission/security/migration/deploy/effect facts under A0 and A4 | Required gates and independent Review/authority floor identical; only evidence collection mechanism varies |
| P03 | J03+J06+J07+J08 with valid current observations and all owner proofs | Conjunction of independently applicable predicates permits bounded admission, not single-label winning |
| P04 | Inspected low-risk CLI/A0 docs-only nonmaterial Fast Path | Only actually applicable tasks/gates required; no blanket costly record forced |

| Adversarial | Input / fault | Required fail-closed oracle |
| --- | --- | --- |
| N01 | Remove J07 label while inspected change still affects security | Security owner gate remains REQUIRED; NOT_APPLICABLE forbidden |
| N02 | Contradict Frozen security review with override review:not-required | CONFLICT and affected gate BLOCKED/NOT_RUN; lower authority never weakens |
| N03 | Missing observation for permission/API/side effect or earlier assessment from stale HEAD | UNKNOWN, not inspected ABSENT; no PASS |
| N04 | Valid local N/A in one owner while another requires migration or security | Other required gate persists; cross-concern AND |
| N05 | Mixed/latest pins, wrong owner blob, missing trace/ref/subject | Reject currentness; no inferred authority |
| N06 | J09+J10+J11+J12 material conjunction without an equivalent covered class | UNVERIFIED/BLOCKED with owner/equivalence or repair path; never blanket PASS |

**Acceptance threshold:** all in-scope focused cases green on the exact implementation PR HEAD; negative scenario cannot mutate a protected gate, authority or source; existing owner/regression tests remain passing or failure is documented/blocking. Run tests against actual owner-facing contracts, not a detached self-certifying model or mere search-for-words script. If common T11 wiring is not yet present, mark that part `DEFERRED_TO_T11` with specific missing field/test and keep whole-program conformance `NOT_RUN`.

### 4. Contract — existing authority with bounded new semantics

Input tuple: resolved immutable ADS revision; Frozen Product/L2/Task/override authority; exact candidate or PR subject; LIBRARY/SERVICE/CLI, NEW/BROWNFIELD, A0–A4, role; declared J set; independently observed source/security/permission/API/migration/deploy/external-effect facts with observation ref/currentness. Output: owner-scoped effective requirement/gate and minimal `EFFECTIVE_RULE_TRACE` projection `{standard_revision, owner_ref/blob, authority_tier/ref, exact_subject, adoption, archetype, actor_role, declared_jobs, observed_fact/ref, applicability_reason, obligation, required_evidence/currentness, resolution, decision_owner/ref}`. Preserve existing gate states; `PRESENT/ABSENT_WITH_INSPECTED_SCOPE/UNKNOWN` are epistemic facts, not new Gate enum. Resolve precedence **within** concern, then AND all applicable owners across concerns. No risk-label-only waiver.

The Task Pack defines WHAT; no exact-base patch, dynamic line-map, version-branch HEAD assumption or hidden chat prompt is an authority here. Material new semantics must preserve compatible historical readers and avoid silently changing preexisting event/Gate/release states.

### 5. Implementation — minimum owner-local delta

Add small non-breaking passages to Project Adoption §§2.2/3.4/3.7 and Workflow §4 effective-rule subsection; preserve anchors/preexisting semantics. Implement fixture-fed owner-contract assertions in unique test (positive and adversarial **decisions**, not prose-only substring asserts); reference existing actual owner logic, do not invent a production global rules engine. T02 exclusively produces affected-source inventory/inspected ABSENT vs UNKNOWN; T11 owns override parsing, any trace schema, manifest, template and shared verifier; T12 proves real integrated X01/S and extra material classes.

**L3 Required handoff, ordered:** Tests above → this Contract → bounded owner-local Implementation → Failure Handling below → exact References here. Builder must record an L3 evidence link, exact PR HEAD/base and source test identity; introduce no extra requirement from a local prompt. Task Claim/dispatch, actual code author, validator and independent reviewer remain distinct truthfully attributed actors.

### 6. Failure handling and UNKNOWN routing

Unresolved pin/role/owner/ref or owner contradiction → BLOCKED/CONFLICT and owning authority route. Uninspected material facts → UNKNOWN/BLOCKED and T02 intake. Old evidence changed by source/profile/contract/security change → affected obligations re-evaluate; preserve old historical facts. Any missing shared projection → `DEFERRED_TO_T11`, not T01 integrated PASS.

For any relevant source, permission, required test/environment, reviewer independence or canonical GitHub identity unverified, report the specific missing proof and `NOT_RUN/BLOCKED`; do not use an optimistic PASS/NOT_APPLICABLE. Failures block only genuine dependents; other disjoint concerns may proceed. Any Frozen Product/L2 incompatibility is escalated to owning authority and affected independent review, not patched by this Builder.

### 7. Validation, Review and merge admission

- **Owner-local verification commands to evaluate and run later, not executed here:** `python -m unittest scripts.test_v411_t01_effective_rules` (or repository-supported direct Python invocation), `python scripts/test_v40_adoption_migration.py`, `python scripts/test_v410_t04a_gate_repair_routing.py`, `python scripts/test_v49_conformance_suite.py`, `python scripts/test_v49_gate_currentness.py`; verify commands against actual environment and report exact command/exit/log.
- **Execution proof:** future real Local Build Host/Validator records tested exact HEAD/tree, OS/toolchain, command, exit code, source/fixture SHA, evidence location, any permitted waiver authority and unrun material cases. Offline and source-only tests are **not** remote/host integration validation. Evidence from earlier v4.10 or preflight is reused for analysis but never relabelled v4.11 PASS.
- **Review:** `risk:high`, `review:required`; require genuinely fresh independent Reviewer other than author and Builder; bind all material findings, currentness, allowed write-set, counterexamples and final verdict to the exact PR HEAD. Review PASS alone is not release permission.
- **Merge gate:** Task Issue must reference independently reviewed/FROZEN repository Pack and a **separately** created canonical native blocked-by graph; current qualified-main Stage3 baseline seed #973 must be verified. Controller/Local materializer creates exact-base JIT Execution Pack and obtains protected accepted Claim. Only after owner-local tests, required Validation and fresh Review, final current-state sweep and truthful merge readiness may a one-concern PR merge to authorized version branch. Recheck exact HEAD/branch currentness just before merge; no automatic Task-draft→Task-issue promotion.
- **Later integration:** T02 source risk/affected inventory; T11 centralized overrides/schema/template/verifier and provenance projection; T12 finite S/X and material uncovered J09+J10+J11+J12 conformance; V01 real-host exact release evidence. Candidate Freeze, Hidden Validation, independent Fresh Closeout, RQ, and guarded main integration are **separate V/R work items**; none is authorized or marked PASS by this Pack author.

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
- Owner preflight (historical advisory only): https://github.com/kaicreator-mm/ai-development-standard/issues/961#issuecomment-6094394270. Actual normative owner blobs were **re-fetched** from exact qualified predecessor `b9461d48d902a2c7c00adff6746afc7a02a0ac3e`; future dispatch rechecks source against current lawful integration HEAD.
- Applicable current standard: `standards/EXECUTION_PACK_STANDARD.md`, `standards/TASK_DECOMPOSITION_STANDARD.md`, `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, `standards/ISSUE_FIRST_TASK_TRIGGER.md` from exact qualified v4.10 predecessor. Future integration may only use each exact separately reviewed owner.

**Next:** an **independent Pack Reviewer**, not this author or future Builder, challenges this draft for scope, executable oracle coverage, actual source-bounded gaps, provenance and DAG non-conflict. #967 integrator then materializes **one immutable repository Pack file** at the intended path and its single index entry on a legally verified stage3 integration branch, conducts authoritative Pack Review/currentness, and only afterward permits separately qualified Local native Task Issue/blocked-by creation. This Issue comment is **NOT a Pack Freeze**, executable Task Issue, Builder Claim, implementation, CI result or Release decision.
