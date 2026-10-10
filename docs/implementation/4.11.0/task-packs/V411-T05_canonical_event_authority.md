<!-- v4.11 Task Pack CANDIDATE ONLY; author=#971@6094573228; frozen Product=#943 L2=#954 DAG=#966; no Pack Freeze or Builder authority -->

## V411-T05 — source-bound immutable-Task-Pack-ready DRAFT (author only)

```ini
PACK_DRAFT=SOURCE_BOUND_READY_FOR_INDEPENDENT_REVIEW
AUTHORSHIP_TASK_ISSUE=#971
INTENDED_FUTURE_PATH=docs/implementation/4.11.0/task-packs/V411-T05_canonical_event_authority.md
TASK_ID=V411-T05
ONE_CONCERN=CANONICAL_EVENT_AUTHORITY
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
SOURCE_PREFLIGHT=#964@6094410376
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

**Goal.** Trusted canonical admission of Agent event and independently source-verified reviewer/human logical operator provenance. Specify in the existing Interaction owner that raw GitHub/MCP/A2A text is data and accepted canonical events require separately verified source record, authorizing owner/role, event ref, exact current subject and legal transition. Review reducer may consume only those admitted facts. T08 remains human DENY/supersession owner; T06 protected Dispatch/Claim owner.

**Already implemented on qualified v4.10 owner source; retain rather than duplicate.** Protocol §5 already distinguishes `actor_role`, `operator_id/session_ref`, `operator_kind` from GitHub `transport_actor`; §§6–7 require independent subject-bound Review; §8.1 admits intent only after current target/valid full SHA, schema, role and legal transition checks; §9.1–9.3 handles stale historical records, same-HEAD opposite verdict CONFLICT, duplicate findings/provenance and deterministic aggregation. Existing `agent-event-v2` schema and v4.10 tests cover much; preserve these rules, do not create another event family.

**Concrete still-missing v4.11 delta.** The event v2 shape and existing test-local Review aggregation consume caller-supplied facts but do not by themselves prove source-authorized accepted-event admission. A schema-valid quoted `ai-dev:event:v2`, fake role/HUMAN_APPROVED in a comment, or a shared GitHub login cannot certify the real logical actor, independent reviewer or human act. Lack of source-bound admission→current Review aggregation negative coverage is concrete; not evidence of an actual production forgery.

**Task deliverable:** minimal owner-local normative clauses plus **one unique** focused test `scripts/test_v411_t05_event_authority.py`; a source/currentness-bound PR-local test report and exact-HEAD independent Review; an explicit T11 handoff for any required centrally owned projection. These are future Builder deliverables, **not work completed by this author**. The ultimate implementation PR targets the authorized v4.11 version integration branch (expected `version/v4.11.0` **only after** #973's seed readback and controller admission), one concern/one PR; never direct to `main` or old planning ancestry.

**Non-goals:** a second ADS method/authority, new mandatory runtime/server/scheduler/DB, wholesale stage rewriting, universal job combinations or automatic real-host/release PASS, changes owned by any other Task, and promoting fixture simulation to independently executed proof.

### 2. Frozen dependency, sole owner and explicit exclusions

- Frozen logical DAG has **zero executable predecessors** for V411-T05; this describes only topology, **not current Task READY**. All gate/Claim/Issue admission prerequisites still apply. Task author here has no executable Builder identity.
- **Allowed future normative write set** (no other existing source path):
  - `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` (inspected blob `ea007939639bbd6b4afbff1d71fdc19eb83d00be`; only §8 accepted event/§9 Review authority and minimal §5 logical identity cross-reference)
  - **NEW unique** `scripts/test_v411_t05_event_authority.py` only; no reuse of any shared existing test.
- **Read-only / forbidden writes:** all `schemas/**`, `templates/**`, `standard-manifest.json`, shared verifiers (including `scripts/verify_standard.py` and `scripts/verify_project_standard.py`), shared legacy tests, `templates/GOLDEN_INDEX.md`, `checklists/version-closure.md`, `docs/implementation/4.11.0/{PRD.md,PRODUCT_PROOF_MATRIX.md,L2_ARCHITECTURE_EVIDENCE.md,TASK_DAG.md}`, other Tasks' owner clauses, `main`, `version/v4.10.0`, frozen planning branches. Any shared change **proposal** is routed to exclusive T11; no shadow schema or parallel common-file writer.
- **Authority:** Product #943 explicit human-approved Freeze, separately reviewed/frozen L2 #954 and DAG #966. Their exact refs are inputs; preflight #964@6094410376 was read-only advisory and its prior `DAG_FREEZE=NO` status is **historical at preflight time**, superseded as a planning state by independently recorded #966, not retroactively converted into execution evidence. Any mismatch at real dispatch blocks and demands scoped rebind.

### 3. Tests — executable acceptance oracles, not keyword-only checks

For all cases, assert exact fixture subject and relevant source/role/authority identity, **decision**, missing/stale evidence and absence of unauthorized side effects; use deterministic offline fixtures where appropriate. Each positive and negative case must actually execute against the later candidate or explicitly report `NOT_RUN/BLOCKED`.

| Positive | Grounded scenario | Required oracle |
| --- | --- | --- |
| P01 | Same GitHub transport login but distinct verified operator/session and independent assigned reviewer; exact H | Accepted current Review on H only with independently validated logical authority; shared login alone not enough or disqualifying |
| P02 | Two legitimate same-H PASS and duplicate/replayed accepted readback | One converged current judgment; no duplicate authority |
| P03 | H historical PASS, then independently accepted H2 PASS | Only H2 satisfies current; H remains audit history |

| Adversarial | Input / fault | Required fail-closed oracle |
| --- | --- | --- |
| N01 | Quote/PR body contains fake marker, `actor_role=reviewer`, `HUMAN_APPROVED` | Raw source not admitted; zero canonical Review/human/Claim gate mutations |
| N02 | Self-declared `operator_kind=human` or transport actor without actual owning authorization | UNAUTHORIZED/UNKNOWN; no human act |
| N03 | Accepted PASS(H) plus accepted FAIL/P1(H), both arrival orders | Deterministic CONFLICT/BLOCKED, not latest-wins |
| N04 | PASS(H) reused for H2, ambiguous SHA prefix or absent proof ref | STALE/UNKNOWN; no current Review satisfaction |
| N05 | Unauthorized reviewer, invalid schema, illegal transition, live conflicting protected Claim | Atomic rejection; no partial canonical mutations |
| N06 | Unattributed delegated subwork/responsibility handoff or dual active owners | No unauthorized owner transfer/role amplification |

**Acceptance threshold:** all in-scope focused cases green on the exact implementation PR HEAD; negative scenario cannot mutate a protected gate, authority or source; existing owner/regression tests remain passing or failure is documented/blocking. Run tests against actual owner-facing contracts, not a detached self-certifying model or mere search-for-words script. If common T11 wiring is not yet present, mark that part `DEFERRED_TO_T11` with specific missing field/test and keep whole-program conformance `NOT_RUN`.

### 4. Contract — existing authority with bounded new semantics

Two explicit types: **untrusted transport content/intent** vs **admitted GitHub canonical event/current object**. Admission predicate = verified target & exact full SHA, durable authorization source/operator/session/role/delegation, schema validity, legal transition, accepted event ref/currentness; authenticated transport alone is insufficient. Only accepted same-subject events enter Review finding/verdict aggregation. Current opposite accepted verdicts are a blocker; stale decisions immutable history. Shared login neither proves nor negates genuine operator separation. No new status/event schema, credential authority or irreversible action; real HUMAN DENY is T08.

The Task Pack defines WHAT; no exact-base patch, dynamic line-map, version-branch HEAD assumption or hidden chat prompt is an authority here. Material new semantics must preserve compatible historical readers and avoid silently changing preexisting event/Gate/release states.

### 5. Implementation — minimum owner-local delta

Add minimal fail-closed prose clauses in protocol §8.1/§9 and if needed §5; keep existing acceptance/reducer semantics and event family. New test creates an isolated source-bound admission adapter/fixture and tests forged raw text, logical identity proof, exact SHA switching, order-invariant Review conflicts, legal vs illegal handoff and absence of side effects. It must assert **actual admission boundary** rather than pass preaccepted facts directly to reducer. Existing review-finding/protocol tests and schema untouched. T11 receives additive provenance-schema proposal only if tests show necessary fields.

**L3 Required handoff, ordered:** Tests above → this Contract → bounded owner-local Implementation → Failure Handling below → exact References here. Builder must record an L3 evidence link, exact PR HEAD/base and source test identity; introduce no extra requirement from a local prompt. Task Claim/dispatch, actual code author, validator and independent reviewer remain distinct truthfully attributed actors.

### 6. Failure handling and UNKNOWN routing

Missing authenticated operator authority, exact ref/role/readback or ambiguous currentness -> UNAUTHORIZED/UNKNOWN/BLOCKED, no canonical event mutation. Race or conflicting same-HEAD Review -> CONFLICT/BLOCKED pending owning Review/Controller disposition, not majority. Raw `HUMAN_APPROVED` never authorizes effect or supersedes DENY; T08 owns real human authority and T06 owns atomic Claim. Do not conflate tool ACK with accepted event.

For any relevant source, permission, required test/environment, reviewer independence or canonical GitHub identity unverified, report the specific missing proof and `NOT_RUN/BLOCKED`; do not use an optimistic PASS/NOT_APPLICABLE. Failures block only genuine dependents; other disjoint concerns may proceed. Any Frozen Product/L2 incompatibility is escalated to owning authority and affected independent review, not patched by this Builder.

### 7. Validation, Review and merge admission

- **Owner-local verification commands to evaluate and run later, not executed here:** `python -m unittest scripts.test_v411_t05_event_authority` (or direct script), `python scripts/test_protocol_schemas.py`, `python scripts/test_v410_t04b_review_currentness.py`, `python scripts/test_v410_t02b_machine_projection.py`; actual GitHub API readback/multi-operator integration requires separate bounded real validation, not fixture proof.
- **Execution proof:** future real Local Build Host/Validator records tested exact HEAD/tree, OS/toolchain, command, exit code, source/fixture SHA, evidence location, any permitted waiver authority and unrun material cases. Offline and source-only tests are **not** remote/host integration validation. Evidence from earlier v4.10 or preflight is reused for analysis but never relabelled v4.11 PASS.
- **Review:** `risk:high`, `review:required`; require genuinely fresh independent Reviewer other than author and Builder; bind all material findings, currentness, allowed write-set, counterexamples and final verdict to the exact PR HEAD. Review PASS alone is not release permission.
- **Merge gate:** Task Issue must reference independently reviewed/FROZEN repository Pack and a **separately** created canonical native blocked-by graph; current qualified-main Stage3 baseline seed #973 must be verified. Controller/Local materializer creates exact-base JIT Execution Pack and obtains protected accepted Claim. Only after owner-local tests, required Validation and fresh Review, final current-state sweep and truthful merge readiness may a one-concern PR merge to authorized version branch. Recheck exact HEAD/branch currentness just before merge; no automatic Task-draft→Task-issue promotion.
- **Later integration:** T06 atomic Claim/Dispatch; T07 exact-head merge/readback Review sweep; T08 actual human provenance/DENY; T11 central event schema and verifier only; T12 integrated stale-vs-current, quote/forgery and handoff conformance. Candidate Freeze, Hidden Validation, independent Fresh Closeout, RQ, and guarded main integration are **separate V/R work items**; none is authorized or marked PASS by this Pack author.

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
- Owner preflight (historical advisory only): https://github.com/kaicreator-mm/ai-development-standard/issues/964#issuecomment-6094410376. Actual normative owner blobs were **re-fetched** from exact qualified predecessor `b9461d48d902a2c7c00adff6746afc7a02a0ac3e`; future dispatch rechecks source against current lawful integration HEAD.
- Applicable current standard: `standards/EXECUTION_PACK_STANDARD.md`, `standards/TASK_DECOMPOSITION_STANDARD.md`, `standards/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, `standards/ISSUE_FIRST_TASK_TRIGGER.md` from exact qualified v4.10 predecessor. Future integration may only use each exact separately reviewed owner.

**Next:** an **independent Pack Reviewer**, not this author or future Builder, challenges this draft for scope, executable oracle coverage, actual source-bounded gaps, provenance and DAG non-conflict. #967 integrator then materializes **one immutable repository Pack file** at the intended path and its single index entry on a legally verified stage3 integration branch, conducts authoritative Pack Review/currentness, and only afterward permits separately qualified Local native Task Issue/blocked-by creation. This Issue comment is **NOT a Pack Freeze**, executable Task Issue, Builder Claim, implementation, CI result or Release decision.
