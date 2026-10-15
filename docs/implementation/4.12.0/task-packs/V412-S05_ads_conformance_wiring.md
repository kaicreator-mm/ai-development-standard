# V412-S05 — Single integration owner for manifest / CI / version conformance

> **CURRENT 2026-10-16 REBIND:** v4.11 standards baseline is now qualified/integrated `main@aac1e1206e4033601616c295e768e51fbc16efb1`; the dedicated `version/v4.12.0` checkpoint is `da5a5bf70a79ec76e0cf9cf7eecc5686dc39e6d5`. User-scoped Product R4 `e924fa29...`, L2 R6 `aede8804...`, Task DAG R4 writer-scope `421378b8...` now have sequential freeze checkpoints (Product `bb3e8baf`, L2 `6f9c13bc`, DAG `0d6c5823`; PR #1130). Earlier statements that the v4.11 predecessor is unqualified, or that R4/R6/DAG-R4 scope is only prospective, describe **earlier authorship history**; they do not govern the current task. This rebind **does not** constitute Pack Freeze, native Issue/Dependency materialization, accepted CAS Claim, implementation execution, or Release PASS. Validate current version HEAD again immediately before any real Task Claim.

> **TASK PACK PLANNING DRAFT (NOT FROZEN / NOT EXECUTABLE).** Read-only author preparation on the v4.12 planning branch. The *Task DAG* itself is exact-owner-frozen, but this Pack is not Task/Claim admission. No baseline release or source writer granted.

```ini
TASK_ID=V412-S05
CANONICAL_TYPE=type:task
ONE_CONCERN=ADS_CONFORMANCE_WIRING
PRODUCT_R3_BLOB=0bfbf782c8859e79df52c9b57904ad80bcd718e9
L2_R5_BLOB=68608ef6456334d627db1797ba2e023233c84ce7
FROZEN_DAG_BLOB=adc9e522f3b734a59898091945b9c7545530565a
PRODUCT_R4_SCOPED_BLOB=e924fa29d8fe3c846eeb7f6ca41131609b19b0ad
L2_R6_SCOPED_BLOB=aede88044697ba45f712ecfa49f615ce48e8af58
DAG_R4_SCOPED_BLOB=421378b8329f51c46697485f57fc9920cfaefed6
PRODUCT_R4_FREEZE_COMMIT=bb3e8bafe459c9fb735b390894a9df24c3d155d0
L2_R6_FREEZE_COMMIT=6f9c13bc607ac098a2a35493cba57dc6e9e1b6b3
DAG_R4_FREEZE_COMMIT=0d6c58230e180cd2fbadbe18d3b12c9d651c0447
V411_QUALIFIED_MAIN_SHA=aac1e1206e4033601616c295e768e51fbc16efb1
V412_INITIAL_SCOPED_INTEGRATION_SHA=da5a5bf70a79ec76e0cf9cf7eecc5686dc39e6d5
DAG_FREEZE_CHECKPOINT=7949caf630edbe83d1dff1ffb7cee8906b77c56f
DAG_FREEZE_RECORD_BLOB=f0a998a73c9319564b239026220ee44934778153
TARGET_VERSION=4.12.0
REAL_V411_RELEASE_PREDECESSOR=QUALIFIED_MAIN_aac1e1206e4033601616c295e768e51fbc16efb1
REAL_V412_IMPL_BASELINE=version/v4.12.0@da5a5bf70a79ec76e0cf9cf7eecc5686dc39e6d5
PACK_STATUS=REBIND_CANDIDATE_REVIEW_PENDING_NOT_FROZEN
NATIVE_TASK_ISSUE=NOT_MATERIALIZED
NATIVE_DEPENDENCIES=NOT_MATERIALIZED
READY=NO
ACCEPTED_CAS_CLAIM=NONE
TASK_PR_SOURCE=NOT_CREATED
TASK_VALIDATION=NOT_RUN
TASK_REVIEW=NOT_RUN
TASK_MERGE=NOT_DONE
FROZEN_DAG_PREDECESSORS=V412-S03;V412-S04
REVIEW_POLICY=required
RISK=high
L3_REQUIRED=YES
ALLOWED_CHANGES=ONLY_EXACT_PATHS_AND_SCOPES_BELOW_ON_LAWFUL_IMPLEMENTATION_BASELINE
FORBIDDEN_CHANGES=ALL_OTHERS_INCLUDING_FROZEN_PRD_L2_DAG_CLAIM_RELEASE
```

## 1. Goal / source evidence reuse

Assemble approved S01–S04 into one ADS standard candidate with two source-pinned checker fixture cases, unaffected existing owner contract/Golden/manifest conformance, one bounded exact-candidate regression and truthful Version Closure input.

**Inspect first, build only missing delta.** Read qualified predecessor *exact* relevant normative owner/git blobs and tests and compare to Frozen R3/L2 before implementation. Reuse source-true contracts; no second claim service, graph scheduler, review/gate controller, app generator, or mandatory redundant verification.

## 2. Allowed and forbidden source changes

- **Allowed after legal admission:** Exclusive `standard-manifest.json`, `scripts/verify_standard.py`, `templates/GOLDEN_INDEX.md` only if new artifacts demand registration
- **Allowed after legal admission:** Existing `.github/workflows/verify-standard.yml` registration and source-history availability, only after eligible v4.11 descendant
- **Allowed after legal admission:** Selected `docs/implementation/4.12.0/` conformance/transition records and version docs, no rewriting S01/S02/S04 substantive owners

**Forbidden by default:** all files not specifically assigned above; frozen Product/L2/DAG and research frozen source; shared canonical metadata/manifest/CI unless specifically owned above; other Task writer paths; release/tag/Claim manipulation; external network/secrets/irreversible side effects without separate current authority. Reconcile exact glob and section write sets against the *qualified* version integration tree before Task READY/Claim.

## 3. Tests → Contract → Implementation → Failure Handling → Reference

**Focused executable or source-verifiable acceptance oracles** (a planned oracle is not an executed PASS):

- P01 manifest lists required new source surfaces (and only actually shipped scripts) with no double owner or path drift
- P02 focused v4.12 checker and existing impacted owner schema/Golden/Task DAG tests pass at exact eligible integrated SHA
- P03 one new and one mature internal consumer snapshot verified by exact source/checker; no generated app Release expectation
- N01 verifier sees missing/corrupted schema/manifest/Git path, noncanonical label/Review Policy or stale binding and fails closed
- N02 inherited historic-main shallow checkout with missing historical refs is resolved by source-equivalent v4.11 #1038/#1040 full-fetch fix through lawful predecessor integration; never label existing old CI FAIL as new v4.12 conformance PASS
- N03 full regression, real Host, Hidden, human DENY or Release-owner proof not actually executed → NOT_RUN/BLOCKED, not auto-PASS from docs
- N04 S01–S04 unrelated small PR patches don't spawn repeated full validation or fresh human rounds absent material change

**Contract.** One downstream source/manifest/CI writer owns shared integration. Test outcome bound to merged source commit/tree, actual exit/skips and applicable Gate authority; multiple assertions can reuse same exact source execution if each is proven by actual log. Version Release remains S06 existing owner, never S05 self-decision.

**Implementation strategy.** After real S01/S02/S03/S04 merged acceptance, register only needed checker/test into existing verify-standard profile. Preserve v4.11 inherited fixes, run focused validations then one candidate regression. Maintain existing legal release evidence/packaging process.

**Failure handling.** Qualified version predecessor unavailable, source drift or required Gate unavailable → hold integration and record source/owner-specific blockers. CI waiver only with legitimate owner disposition, not default automatic PASS.



**References (immutable planning owner input):** frozen Product R3 blob `0bfbf782c8859e79df52c9b57904ad80bcd718e9`; frozen L2 R5 blob `68608ef6456334d627db1797ba2e023233c84ce7`; frozen DAG blob `adc9e522f3b734a59898091945b9c7545530565a`; checkpoint `7949caf630edbe83d1dff1ffb7cee8906b77c56f`; canonical `standards/DEVELOPMENT_WORKFLOW.md` §Stage2.4/2.5/2.6, `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md` §10/§12.1, `GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `TASK_DAG_GOVERNANCE_STANDARD.md`, `VALIDATION_STANDARD.md`, `RELEASE_STANDARD.md`. Those are verified historical version owners, **not** an assertion that the current v4.11 branch released.

## 3A. #1099 Review/Validation/Release convergence — verify once, never invent PASS

S05, the **single shared conformance wiring owner**, implements only a missing projection of #1099 and the already Frozen FR-05/FR-07 onto existing `VALIDATION_STANDARD`, `RELEASE_STANDARD`, current Review/Workflow owners. The norm owner of Gate applicability remains the existing Release owner S06; **S05 may not invent waiver policy or amend frozen gates**.

**Evidence economy / stage-aware verification:**
- **Small mechanical repair:** review its exact diff, write-set, affected invariant and genuinely new negative/root failure classes, reuse unchanged earlier Review subject only where provenance/currentness allow. A prior source-only review **cannot** become an exact new-HEAD machine PASS. Material behavior/security/data/effect change may require focused actual negative execution before merge; subject-specific owner policy decides, not apparent patch size.
- **One version candidate campaign:** run required full dependency-complete regression **once on the current exact candidate** (unless required extra distinct Host/Hidden/RQ/E3 and newly material source invalidation). One real executed log may support multiple evidence rows if their *entire material predicates*, actor/environment/identity/fidelity, negative and exact source subject actually match. Same script-name or old E1 fixture is not equivalent truth.
- **No repetitive rounds:** no R4/R5 full-PR rereview after a 2-line fix unless a new material source/authority/semantic counterexample appears. Reuse `VALIDATION_IMPACT_DECISION` / currentness obligation with `REUSED_EXACT_EVIDENCE | DEFERRED_TO_CANDIDATE | NOT_RUN` as descriptive decisions, **not new Gate states**.
- **Delivery type matters:** ADS is `STANDARDS_SPECIFICATION` with scripts as deterministic reference checks, not inherently a deployed multi-host Claim or Release service. Preserve scope and owner-qualified Release §11.2/11.5; the separate #1116 type-aware design can be source input, not silent replacement of frozen v4.11 mandatory E3/Hidden gates. Genuine later runtime adopters own their real-world Claim/Human/E3 proofs.
- **No fabricated cost claims:** when actual logged CI/Host/review duration or comparable baseline is missing report `UNKNOWN` rather than asserting e.g. “75% saved”. If optional work is legally excluded, record only meaningful consumer impact and decision-owner disposition in existing Task Result metadata, no new tracking DB.

**Required focused negatives (S05 integration test registration, not additional Gate):**
- `ROI-V01`: two separately named validation rows with identical exact candidate+predicate+actor+Host/fidelity reuse one executed proof; changed permission/subject/required independent owner makes reuse fail.
- `ROI-V02`: tiny repaired source diff may obtain legitimate current review, but unexecuted exact-HEAD test remains `NOT_RUN`, never Release PASS.
- `ROI-V03`: new material side effect or security violation defeats Fast Path and triggers applicable focused negative now; no dangerous merge as mere cost savings.
- `ROI-V04`: Frozen `REQUIRED_NOW` from older v4.11 candidate remains mandatory until lawful prospective owner rebaseline; a new v4.12 ROI rubric cannot retroactively waive it.
- `ROI-V05`: repeated independent Review/Host run with no new predicate/impact is not *universally mandatory*; stop if owner policy permits and valid equivalent current evidence exists, else label the unresolved required predicate `BLOCKED/NOT_RUN`.
- `ROI-V06`: version candidate source drift invalidates only affected reusable evidence where owner currentness allows, but full candidate rerun occurs when actually required by release policy; do not blindly treat historical 139 jobs as mandatory for a standards-only target.

**S06 remains the original Release Authority.** An optional scenario legitimately outside a pre-Freeze Product promise differs from a required Release gate that did not run. Any required human/Hidden/real external proof cannot be silently replaced by model critiques, source assertions, or “high ROI”.

## 3B. Self-declared logical reviewers and shared GitHub transport — current v4.11 contract tests

**Reuse current normative predecessor, not frozen-era credential rules:** `GITHUB_AGENT_INTERACTION_PROTOCOL.md` exact v4.11 blob `b3f1191b2ee0c469e9b425d2336d4adbc47d6ede` has already adopted #1122 self-declared operator/context attribution, and `RELEASE_STANDARD.md` §11.7 addresses ADS standards-only release. Existing focused #1122 tests were reviewed/merged; reuse them after verifying source/currentness. S05 must not introduce a second reviewer-account registry, cross-session proof machinery, human-signature credential validator or login-inequality Gate.

**Source-first gap search:** Inspect the then-qualified v4.11 exact predecessor schema, Review/Claim/Assurance/Release tests and verifier. Distinguish actor credential/identity tests (prospectively remove if the exact owner authorizes that delta) from semantic Source Owner/proof applicability, real CAS serialization, exact SHA and runtime/effect safety (retain). Log `ALREADY_SATISFIED` when the actual required behavior is covered; add one focused case only for a demonstrated missing behavior. Do not silently alter `ASSURANCE_PLAN_STANDARD`, `RELEASE_STANDARD` or `EXECUTION_ARCHITECTURE_STANDARD`: those files are outside S05's frozen source-write ownership and would need a lawful DAG/Task Pack amendment.

**Focused conformance, not a new Gate:**
- `ID-V01` accepted same-GitHub transport with distinct **declared** Builder/Reviewer logical operator/session and exact current PR subject ⇒ do not reject for shared login or missing real-Session proof.
- `ID-V02` two different GitHub accounts with the **same declared logical context** ⇒ not independent merely because accounts differ.
- `ID-V03` distinctly declared Reviewer events are accepted for attribution without questioning Session authenticity; **but** a quoted raw event, malformed event, missing accepted canonical admission or stale exact subject cannot mint Review PASS.
- `ID-V04` declared Release/Review actor without actual required validation, correct Claim generation/serialization or source-currentness ⇒ cannot make a technical Gate PASS.
- `ID-V05` optional `transport_actor` value (same/different/absent where contract allows) never changes ADS logical actor qualification; a GitHub-native required approving review is separately subject to real platform rules.
- `ID-V06` preserve actual downstream service/human-effect `NOT_PROVEN` when ADS only validates standards; do not fabricate real runtime authority/consent/Human DENY from declared agent role.
- `ID-V07` `CURRENT_OWNER_AUTHORITY` or `OWNER_PERMISSION` as *semantic rule applicability*, not physical Owner authentication, must remain effective until the lawful owning policy explicitly revises what proof may authorize a reduction; do not accidentally turn missing required evidence into `NOT_APPLICABLE`.

**Record objective subject truth:** `actor_role/operator_kind/operator_id/session_ref` self declaration, optional GitHub transport and accepted canonical event reference, exact Task/PR SHA, real Review/Validation outcome and any external GitHub branch-protection status. Test the correct source/technical predicates, not the claimed real-world identity. No source implementation or test PASS is claimed by this planned Pack.

## 3C. #1123 proposed assurance/release conformance — source-owned S05 delta

**Proposed only, not yet admitted.** Consume Product R4 delta candidate blob `e924fa29d8fe3c846eeb7f6ca41131609b19b0ad`, L2 R6 `aede88044697ba45f712ecfa49f615ce48e8af58`, and DAG R4 proposed scope blob `421378b8329f51c46697485f57fc9920cfaefed6`. Existing Frozen R3 exact files and `PACK_FREEZE=NOT_RECORDED` remain unchanged. No v4.12 normative source write now.

**Proposed extra S05 single-writer source surfaces (only after actual successor Freeze, and only proven clauses):**
- `standards/ASSURANCE_PLAN_STANDARD.md` §§9–10: remove a *physical Owner/credential* check **if present**, never remove or silently bypass semantic rule authority, source-current proof and `REQUIRED_PREDICATE_PROOFS_PRESENT` for real assurance reduction.
- `standards/RELEASE_STANDARD.md` §§11.1–11.7: reuse actual #1122 §11.7 for ADS standard-only self-declared release process, remove leftover identity-specific signer verification only where genuinely present. Keep true Release gate-by-subject, qualifying evidence and `NOT_PROVEN` source vs deployed-runtime limits. S06 still performs existing Release decision.
- If demonstrably necessary after exact source gap review, explicitly add scoped tests to `scripts/test_v411_i1122_self_declared_executor.py`, `scripts/test_v411_t05_event_authority.py` (new v4.12 tests may prefer a uniquely named `scripts/test_v412_actor_trust.py`), and exact affected schema `schemas/agent-event-v2.schema.json`, `schemas/assurance-plan-v2.schema.json`, `schemas/dispatch.schema.json`. These are **candidate eligible exact paths**, not broad `schemas/**` or `scripts/**` carte blanche. Avoid needless schema format churn; version behavior/protocol change may require an explicit semantic compatibility statement without a schema change.
- S05 retains already owned `standard-manifest.json`, `scripts/verify_standard.py`, `templates/GOLDEN_INDEX.md` and relevant CI wiring only when adding actual source requires registration. Does **not** touch `AGENTS.md`, S01 Interaction/Execution Architecture, review prompt, S04 PROJECT_ADOPTION, S02 DAG template or S03 checker.

**Focused real validation when eligible:** recheck merged v4.11 #1122 source/tests by exact SHA, then test same-transport distinct **declared** contexts accepted, two accounts/same logical declaration not independent, no Session reality proof requirement, raw quoted fake event rejected, missing/failed required executable tests cannot PASS, Claim CAS race remains one-winner, semantic `OWNER_PERMISSION` cannot be deleted to make source/proof Gate vanish, Release executor self-declared yet still has actual source-current candidate Gate evidence, GitHub native approving Review still follows external branch ruleset. Only run additional tests when source gap is real. One candidate-scoped Release conformance campaign, no copy of a historical 139-case suite merely for ceremony.

**No identity suspicion or false PASS:** the executor declaration is trusted for *actor attribution*; executable test truth, security/effect authorization, currentness and approval facts are not the same as physical actor identity. This source-task proposal is NOT an Assurance reduction decision, source PR, Reviewer PASS, native Claim, Hidden test or S06 Release PASS.


## 3D. #1119 Option A — read-only qualified latest-compatible ADS deterministic selector

**New prospective source pins:** user-approved feasibility blob `be7f0785083890b42aab5efb17d735df8a69adab`; unfrozen Product R4 `e924fa29d8fe3c846eeb7f6ca41131609b19b0ad`, L2 R6 `aede88044697ba45f712ecfa49f615ce48e8af58`, DAG R4 proposed writer scope `421378b8329f51c46697485f57fc9920cfaefed6`. Original Frozen Product R3/L2 R5/DAG R3 remain the actual historical authority until lawful successors are frozen. This Pack is **not** an execution license or executable checker now.

**S05 exclusive new proposed write paths:** `scripts/v412_ads_compatible_select.py` and `scripts/test_v412_ads_compatible_select.py`. These names are **not** part of Frozen DAG R3 write permissions and require actual DAG R4 successor Freeze + accepted Task Pack/Claim first. They are the smallest bounded genuine implementation of #1119 Option A; do **not** pretend `standards/PROJECT_ADOPTION.md` prose already delivers an operational resolver. S04 only owns adoption policy/examples; `INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` / `schemas/compatibility-record-v1.schema.json` are existing **read-only semantic/schema inputs**, not an automatically granted writer set. Existing S05 manifest, `scripts/verify_standard.py`, Golden index and CI are conditional registration/wiring if the actual tool is shipped.

**Tests → Contract → Implementation → Failure Handling → Reference:**
- **Tests:** two source-pinned consumer snapshots (new/mature, may reuse existing legitimate S03 fixtures only where version/compatibility fields truly match) and bounded cases: `LC01` opt-in + verified qualified stable ADS release + source/authority/schema/behavior compatibility proven ⇒ **read-only exact-SHA recommendation**; `LC02` same semver/distinct SHA ⇒ not identical; `LC03` #1123 agent/Review/Claim/Release semantic change with unchanged schema ⇒ NOT_AUTO/UNKNOWN pending material proof; `LC04` tag/main/latest/unqualified candidate/unsigned self-asserted PASS/release evidence not current ⇒ REJECT; `LC05` active Task or frozen candidate remains on its current pin; `LC06` no opt-in / unsupported consumer windows / missing actual qualifying source ⇒ NO_SAFE_RECOMMENDATION; `LC07` two incomparable stable release lines ⇒ explicit uncertainty not arbitrary latest; `LC08` real CLI/checker invocation creates **no** GitHub PR/consumer file change, leaves exact old pin untouched; `LC09` resulting suggestion has exact old/new source, proof refs and checkpoint-only proposed adoption. Assertion counts must correspond to real executed commands on current SHA.
- **Contract:** one pure read-only selection operation with input pinned consumer `.dev-standard/VERSION`, optional `TRACK_LATEST_COMPATIBLE_STABLE` preference, verified-source snapshots of qualified immutable candidate Release(s), actual `compatibility-record-v1` for all material consumer dimensions, and explicit release-line ordering. Output `READ_ONLY_RECOMMENDATION` with old/new exact SHAs, compatibility/qualification evidence and next-checkpoint instructions, or `NO_SAFE_RECOMMENDATION`/insufficiency. A mere `qualified=true` field, semver, tag name, mutable branch or owner string cannot supply genuine qualification evidence; underlying source currentness must actually be verified or result stays `UNVERIFIED`. No hidden extra protocol-version schema field required.
- **Implementation:** small deterministic script/CLI with no project write API/network update credentials. Prefer reuse of current `standards/PROJECT_ADOPTION.md` immutable pin resolver / `compatibility-record-v1` schema; add only genuinely needed shared verifier/manifest/Golden registration in S05's existing write set. Use comparator only when the relevant release line/order is established and non-ambiguous; deterministic failures and transparent no-recommendation are preferred to an unsafe “latest”.
- **Failure:** release not actually qualified, unsupported/stale SHA/tree, missing manifest/source evidence, material compatibility UNKNOWN, non opted-in project, conflicting current Claim/frozen candidate, consumer window uninspected ⇒ **no upgrade recommendation**, not an upgrade PASS. If an actual GitHub API write, project PR, remote pin alteration or previous Task binding mutation occurs, the #1119 Option A read-only contract is violated; do not promote as successful.
- **Reference:** #1119 approved Option A feasibility `be7f0785083890b42aab5efb17d735df8a69adab`; v4.11 `standards/PROJECT_ADOPTION.md` blob `a8c2d7a01a3610d9444d17df614ec6cacf58b67e`, `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` blob `15e355f6ec86370599f2dda7b61963d93fead66f`, Release source §11 and current `compatibility-record-v1` owner. Retain S06 real Release control. **Cross-project automatic PR updater/activation executor** is **v4.13 Option B**, not this S05 Task.

**Status:** only an author-scoped Pack candidate and proposed source path. No actual resolver, output, tests, project updates, Task Claims, independent Review or release has been performed by writing this section.

## 4. Execution readiness / Review / closure

- Intended concern predecessor(s): V412-S03, V412-S04. Native issue edges require actual API mutation and readback; Markdown is advisory historical.
- Risk: **high**. Stage 2.6 pre-dispatch Review Policy candidate: **required**, subject to stronger authority. A Builder cannot self-prove `review:required`.
- Source implementation base: v4.11 is qualified and version/v4.12.0 exists. **TASK still HOLD** until this Pack's exact source/index is frozen, canonical native Task/dependencies are read back, and a valid current accepted CAS Claim precedes the first normative source write. Do not implement on historic-main planning PR #1101.
- Author/responsible executor shall acquire a current accepted CAS Claim for the *real native Task Issue* before any implementation-source write; a GitHub comment/status alone is insufficient.
- Verification must report exact subject/commit/tree, real command/exit/skip, provenance and strength E1/E2/E3. Only the owning gate/Release actor may promote a result; PR-local PASS ≠ version Release PASS.
- Closeout when authorized source PR is merged on current version integration branch after required Review/validation and canonical readback; otherwise state BLOCKED/NOT_RUN with minimal owning remedy, no duplicate Task Issue/hidden test program.

```ini
TASK_IMPLEMENTATION=NOT_STARTED
TASK_REVIEW=NOT_RUN
TASK_CLAIM=NONE
PACK_FREEZE=NOT_RECORDED
REAL_INTEGRATION_BASE=VERSION_BRANCH_AT_da5a5bf70a79ec76e0cf9cf7eecc5686dc39e6d5
```
