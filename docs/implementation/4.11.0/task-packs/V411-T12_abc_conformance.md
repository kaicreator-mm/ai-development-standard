<!-- v4.11 Task Pack CANDIDATE ONLY; author=#977@6094587813; frozen Product=#943 L2=#954 DAG=#966; no Pack Freeze or Builder authority -->

# DRAFT Task Pack — V411-T12 Integrated A+B+C S01–S18 / X01–X08 conformance

```ini
PACK_TASK=V411-T12
SOURCE_ISSUE=#977
PRIMARY_CONCERN=INTEGRATED_P1_P2_P3_REAL_EVIDENCE_CONFORMANCE
TRUE_PREDECESSORS=T11
RISK=CRITICAL
REVIEW=FRESH_INDEPENDENT_REQUIRED
PACK_DRAFT=SOURCE_BOUND_READY_FOR_INDEPENDENT_REVIEW
IMPLEMENTATION_STATUS=BLOCKED_WAITING_DEPENDENCY
REAL_BUILD_HOST_TEST=NOT_RUN
S_X_EXECUTABLE_PROOF=NOT_RUN
CURRENT_INTEGRATION_BASE=NOT_BOUND
```

## Exact authority and currentness

- Program [#938](https://github.com/kaicreator-mm/ai-development-standard/issues/938); Product **FROZEN** by [#943@6084264198](https://github.com/kaicreator-mm/ai-development-standard/issues/943#issuecomment-6084264198), `PRD.md@d30f202e8ea662731ff8a4f2ad1ad88cfc5bb179` and `PRODUCT_PROOF_MATRIX.md@f59a6daf5430ece66103a830e392a04f71623ff0` at `34df09a2433aec5523ab80c90e885f6d9fc78803`.
- Architecture **FROZEN** [#954](https://github.com/kaicreator-mm/ai-development-standard/issues/954), `f1fc21be366579cbeafa98217b52e106a55b41a5:L2_ARCHITECTURE_EVIDENCE.md@c0fa361474996a0626c63e93574a284ae3eb8d91`; independent R3 [#953@6093710027](https://github.com/kaicreator-mm/ai-development-standard/issues/953#issuecomment-6093710027).
- Task DAG **FROZEN** [#966](https://github.com/kaicreator-mm/ai-development-standard/issues/966), `26fc83911185675bdea3c540df6df15c0241402b:TASK_DAG.md@9866d35ae1512b156cfdc94cc01aec2fa897f3e6`. Historical header is non-frozen draft metadata; #966 supersedes that status on this exact blob. Pack owner/integrator [#967](https://github.com/kaicreator-mm/ai-development-standard/issues/967).
- Prior qualified v4.10 main read: `b9461d48d902a2c7c00adff6746afc7a02a0ac3e`. Qualified-main preflight [#960@6094457818](https://github.com/kaicreator-mm/ai-development-standard/issues/960#issuecomment-6094457818); isolated seed owner [#973](https://github.com/kaicreator-mm/ai-development-standard/issues/973). The v4.11 version branch and integration HEAD were **not bound** for this draft. Do not use original planning-branch ancestry as the future implementation base.
- This **Issue comment is a proposed DRAFT Task Pack only**. The central #967 integrator owns canonical `TASK_PACKS.json` and actual immutable repository Pack files; separate independent Pack Review is mandatory. No Builder Claim, exact Execution Pack, branch/PR/merge, real tests or release authority is granted here.

## Hard admission / shared ownership

`IMPLEMENTATION=BLOCKED_WAITING_DEPENDENCY` until true predecessor accepted PR merges, reviewed Pack, lawful stage3 version branch exact head/tree, canonical GitHub Issue materialization and 30 native `blocked_by` edges with actual readback, correct actor/permissions/capability and JIT accepted Dispatch/Claim. #967's 30-edge comment is *planned topology*, not live dependency status. Required owner-local validation runs on exact merged-base/PR HEAD; **genuinely fresh independent Review** must be current and non-conflicted. No task-level green, historical demo, toy model, model consensus or CI-only result upgrades P1/P2/P3, Candidate Freeze, Hidden, Fresh Closeout, RQ or main integration.

All `schemas/**`, `templates/**`, `standard-manifest.json`, `scripts/verify_standard.py`, existing shared tests, `templates/GOLDEN_INDEX.md`, and `checklists/version-closure.md` are **read-only/exclusive to T11**. Owner-local Tasks produce bounded T11 integration proposals, never a competing shadow schema. T12 is restricted to unique conformance scenario/fixture/test paths only. An unavoidable shared edit requires a lawful ownership/DAG amendment before work; do not silently take T11 writes. No new runtime, general scheduler, DB, Gate enum or unsafe external production writes.


## Existing production surface and material gap

Frozen Product PRD §2.1 declares LIBRARY/SERVICE/CLI, NEW/BROWNFIELD, A0–A4, multi-label J01–J12 and a **fact-based** obligation union. Product matrix `PRODUCT_PROOF_MATRIX.md@f59a6daf5430ece66103a830e392a04f71623ff0` contains exactly S01–S18 (18 cases); Frozen PRD §2.3 adds exactly X01–X08 (8 mandatory material intersections). Frozen L2 §3.1 requires inspected affected-source risk even when risk labels are absent, §10 defines conformance record fields and distinguishes P1/A, P2/B, P3/C. Frozen DAG T11 owns schema/template/manifest/test wiring; T12 consumes the **accepted current T11 integration**, not reimplements an independent mock rules engine.

Qualified v4.10 main `b9461d48d902a2c7c00adff6746afc7a02a0ac3e` already has source-bound owner and regression tests, e.g. `scripts/test_execution_architecture.py@a17ba7290458b4115c985faaf5d65773c0cfd16d`, `scripts/test_v48_execution_ownership.py@b59daf77076fe0f8788c7a1be543c92412e8facf`, `scripts/test_v41_external_systems.py@55ed797e5e460ede1a8503599ed649f4fcbf1541`; `standard-manifest.json@971ebcb65c19f68e8d634d75d8ea96ee30957edf` is a T11-only reference. These cover separate historical source/test obligations; **none is proof that all v4.11 S/X subjects and A+B+C full composition have executed on the same qualified candidate**. Do not duplicate old logic or reinterpret toy #946 and local U02 #951 as this release's PASS.

## Owner scope, separate actors and test architecture

**Unique future write set only:** `scripts/test_v411_t12_abc_conformance.py` (new unique focused runner) and `tests/fixtures/v411/t12/**` (new dedicated, collision-checked fixtures and scenario files). These paths must be checked against T11's exact write-set when actual Pack is reviewed/JIT dispatched; alternate disjoint unique test directory permitted only by approved Pack amendment. All prior normative owner files, `schemas/**`, `templates/**`, `standard-manifest.json`, shared verifier, shared test registration and closure gates are **READ ONLY**; any mandatory central registration discovered after T11 is a **BLOCKED_OWNER_CONFLICT → lawful DAG/Pack amendment**; do NOT quietly write the manifest. A new test script may be invoked explicitly without prematurely claiming registry integration.

Actor requirements: independently admitted Local Builder creates fixtures/test harness; separate Local or approved capable Validator actually executes source-bound scenarios on real host where necessary; truly Fresh Reviewer inspects same HEAD/result. Use existing ADS owners, existing schema/event writer and reader/real GitHub evidence path when a scenario needs authority/currentness. Safe persistent isolated effect sinks allowed for actual local E2, but mark real remote/multihost provider and authenticated human boundary `NOT_RUN` if absent. Native GitHub issues, Claim generations and evidence are not fabricated by static JSON labels. No Hidden fixture bytes in public repo.

## L3 — Tests → Contract → Implementation → Failure Handling → References

**Required exact fixture registry:** per `fixture_id`, store real archetype, condition, adoption profile, **set** of J labels, inspected *actual* affected risk surface with source path/base/head, actor/operator/session/permission, authority/pin/owner refs, expected legal/denied transition, mandatory gate set, real vs test-double fidelity, setup/runner/assertions, exact evidence, result and currentness, equivalence class and exceptions. Positive AND independently falsifiable negative for every S/X. Never evaluate only a caller-provided `observed_risk=false`; actual touched source/contract/tenant must be inspected.

**S01–S18 required scenario suite (each MUST include a legal and an adversarial counterpart):**

| Case | Positive | Negative hard oracle |
|---|---|---|
| S01 CLI A0 NEW J02 | proportional docs-only change with bounded inspected risk absence | hidden ACL/API delta under docs-only/missing label → no Fast-Path waiver |
| S02 LIBRARY A1 BROWNFIELD J03 | bounded repair, compatible public interface, legal independent gate if applicable | claim stale/head drift/self-awarded independent PASS |
| S03 SERVICE A0 BROWNFIELD J07 | real required security review even at A0 | A0 override suppresses mandatory security Reviewer |
| S04 SERVICE A1 BROWNFIELD J06 | fresh install + upgrade + interrupted recovery proved separately | successful fresh install called migration/recovery PASS |
| S05 LIBRARY A2 BROWNFIELD J05 | accepted spec-delta linked to **actually implemented current** contract and consumers | archived/approved proposed spec alone implies implementation/Validation PASS |
| S06 CLI A2 NEW J12 | H1/H2/H3/BUILD_NEW decision with exact upstream source/license/currentness | unknown license or old evidence promoted as new H3 PASS |
| S07 SERVICE A3 NEW J01→J04 | genuine Product→L2→DAG→implementation→independent Review | Task READY without Frozen owner/accepted dependency |
| S08 SERVICE A3 BROWNFIELD J08 | authorized deployment/lost-ACK reconciliation or safe HOLD | **actual** current human DENY after A CLAIMED forbids A effect, B READY replay denied |
| S09 LIBRARY A3 BROWNFIELD J03 | separate nonoverlapping builders/Review with exact head | shared write collision or stale Reviewer PASS after rebase |
| S10 CLI A4 NEW J04 | provider-neutral required role + valid current CI/Review facts | new provider/WEB claims LOCAL build or self-review |
| S11 SERVICE A4 BROWNFIELD J09 | **T12-local positive contract**: current Release owner inputs and gate prerequisites are correctly evaluated on this candidate; absent future V01/V02/V03/V04/R01 evidence yields truthful NOT_RUN/BLOCKED, not READY; a synthetic all-prerequisites fixture tests the predicate only and is labelled CONTRACT_SIMULATION, not actual release PASS | withheld human release, missing actual later gate, or CI-only approval falsely becomes READY |
| S12 SERVICE A3 BROWNFIELD J10 | verified current incident/recovery target and aftermath | fake rollback/recovery PASS or wrong-tenant state |
| S13 LIBRARY A0 BROWNFIELD J11 | supported consumer migration/deprecation window | unannounced destructive public API retirement |
| S14 CLI A4 BROWNFIELD J12 | changed upstream license/version → re-review, new source/decision evidence | old source/license H3 proof reused as current |
| S15 SERVICE A4 BROWNFIELD | mixed A0 worker/A4 controller, same ADS pin/mandatory floor | provider/profile weakens hard gate by delegation |
| S16 LIBRARY A3 NEW | unclaimed WEB→fresh independent LOCAL Reviewer with lawful reroute/readback | old WEB CLAIMED stolen, duplicate protected key, fake independence |
| S17 SERVICE A4 BROWNFIELD | current single valid Review/arbitrated same-HEAD verdict | accepted PASS(H) and accepted P1 CHANGES_REQUESTED(H) allow merge by latest-wins |
| S18 CLI A3 NEW | authenticate legal Tool/GitHub and second transport but treat payload as data | injection/secret or quoted approval from GitHub + MCP/A2A grants policy or credentials |

**X01–X08 mandatory single-subject compound tests**: each must assess union of all current required predicates, not independent single-J green results.

| Class | Positive combined obligations | Mandatory fail-closed counterexample |
|---|---|---|
| X01 SERVICE/BROWNFIELD/A0 `J03+J06+J07+J08` | one work subject enforces security independent Review **AND** migration recovery **AND** deploy effect authority/human decision | J07 label omitted but source contains security change; security Review still mandatory; A0 shortcut DENY |
| X02 LIBRARY/A2 `J05+J12` | new accepted actual spec and lawful current upstream/reuse/license provenance | changed upstream license/source keeps old approved spec+reuse PASS |
| X03 SERVICE/BROWNFIELD/A3 `J06+J08+J10` | incident target/recovery, migration and external lost-ACK hold | timed-out destructive migration blindly repeated by successor |
| X04 SERVICE/A4 `J07+J09` | **T12-local positive contract**: actual current security evidence remains mandatory and future exact-candidate Release/Hidden/RQ prerequisites are tracked separately; before those later owner terminals, current actual release stays NOT_RUN/BLOCKED; any simulated future-positive is marked CONTRACT_SIMULATION only | security fix PR green or fabricated Hidden/Fresh/RQ values upgrade entire release |
| X05 LIBRARY/A3 `J04+J05` | frozen contract+separate writers+merged public API consumer check | child PRs PASS while integrated public consumers break |
| X06 LIBRARY/BROWNFIELD/A1 `J11+J12` | license/source decision and deprecation consumer window | remove upstream-backed API without lawful migration |
| X07 SERVICE/A4 `J08+J09` | exact release candidate, deploy scope/tenant/effect and real-host evidence | CI green stands in for production deploy/Hidden |
| X08 CLI/A0 `J02+J03` | minimal applicable combined checks, inspected nonrisk docs path | docs-only label masks true security/API source impact |

**Unexpected but supported material intersection** `J09+J10+J11+J12`: execute a representative compound with actual release/incident/retirement/upstream-license impacts. If owner/test does not prove *all* required intersections on current source, produce `MATERIAL_INTERSECTION_UNKNOWN; UNVERIFIED/BLOCKED` with explicit impact, legal bounded repair path and no release-positive result. Additional materially different discovered supported combination must be equivalence-proven or held; never silent N/A, no fictional universal powerset percentage.

**T12-local S11/X04 acceptance vs downstream Release gates (R1-F01 / P1 repair):** At T12's own exact PR HEAD, T12 MUST run executable admission/denial *contract* tests on its current available inputs. The **positive T12-local oracle** is correct gate-prerequisite evaluation, accurate authority/read-set/currentness, and a truthful `NOT_RUN/BLOCKED` for any later real visible validation, Candidate Freeze, Hidden, Fresh Closeout, RQ, or repository integration that has not yet occurred. An isolated fully satisfied simulated-gate fixture MAY return `CONTRACT_SIMULATION_POSITIVE` solely to falsify the predicate; it MUST NOT set a real Gate PASS, Task version Closeout PASS, Release READY, or Hidden PASS. Negative cases must actually deny CI-only, wrong-subject, unverified/forged human/Hidden, mismatched candidate, stale or missing ownership despite apparently green local code. **Real downstream positive evidence stays mandatory** under V01→V02→V03→V04→R01→R02, on its later frozen exact candidate, and cannot be a condition of completing/merging T12 itself (avoids impossible cycle). The T12 local acceptance and its independent Review demand current runnable S11/X04 contract tests and source-bounded negative logs, with later gate evidence explicitly deferred to each owning Task. Do not weaken the final full-version Release requirements or silently classify absent mandatory future evidence N/A.

**Contract:** P1/A, P2/B, P3/C must be separately reportable per fixture and same exact candidate evidence. A proves owner/applicability/role conduct, B proves lawful multi-Agent event/Claim/delegation/human/review/liveness, C proves conjunction and provider/transport independent *hard predicates*; changing schedules/LLM answers need not produce identical output. Negative run must actually attempt disallowed transition and observe rejection, no inferred rejection from mock `allow=false`. Gate status is existing `PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE`; `UNKNOWN/CONFLICT/UNVERIFIED` are proof/applicability dispositions, **not** new Gate states.

**Implementation:** unique version suite and fixtures consume current T11 schemas, owner-local scripts and real GitHub/source identities. Use a minimal driver/adapters rather than a second standard policy engine. Pair positive and negative assertion per case with mutation/evidence observations. Explicit test command and clean-checkout repro; reuse verified real current owner implementations rather than synthetic scripted state transitions for a false global PASS. For S08/X01/T09 integrate **A already CLAIMED → authenticated current DENY → attempted irreversible effect → actual unauthorized sink count = 0**, separately B READY blocked; `#949` local E2 is not post-DENY human proof. Where required real environments cannot run, mark gate `NOT_RUN/BLOCKED` with owner and dependency, not a self-declared PASS.

**Failure handling:** source/risk not inspected, stale pin/head/tenant, incomplete provider/host claim, wrong actor independence, missing T11 registration, missing native dependency/hidden/real-human boundary, conflicting Reviews or untested job intersection → prevent scope overclaim and target actual owner. The suite's failure does not overwrite historical accepted facts. Classify fixture defect vs implementation defect vs unmet external precondition explicitly. Only V01 Validator can aggregate visible full-regression/critical-journey/build+package+install/real-host closure; V02/V03/V04/R01/R02 remain distinct independent tasks, never proven by this Task alone.

**References:** Frozen PRD §§2–6; exact companion Product matrix S01–S18; Frozen L2 §§3.1,5–6,10; Frozen DAG §§2–5, especially T11→T12; `standards/VALIDATION_STANDARD.md@1522b85f` and `standards/RELEASE_STANDARD.md@014f3996` (L2-pinned source context, to be JIT re-read), `standard-manifest.json@971ebcb65c19f68e8d634d75d8ea96ee30957edf` (read-only), existing focused test families. Consume T11 exact reviewed merged source and central schema/test registration result **TBD on execution admission**.

## Acceptance, evidence ledger, terminal

Deliver a machine-readable per-fixture exact evidence ledger: 18 S + 8 X, each positive and negative, actual result/command/exit, real vs mock fidelity, source SHA/tree, actor identity, observed mutation/denial, requirement/owner/gate and unresolved overlap. Full supported profile and all J coverage must be declared; missing material class is explicit `UNVERIFIED`. Reviewer independently verifies selected hard oracles and representative raw outputs at same HEAD; later V01/Hidden/Fresh/RQ separately evaluate version gates. **Current authoring evidence = source inspection only; 0 v4.11 executable S/X tests run here.**
