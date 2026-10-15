# V412-S05 — Single integration owner for manifest / CI / version conformance

> **TASK PACK PLANNING DRAFT (NOT FROZEN / NOT EXECUTABLE).** Read-only author preparation on the v4.12 planning branch. The *Task DAG* itself is exact-owner-frozen, but this Pack is not Task/Claim admission. No baseline release or source writer granted.

```ini
TASK_ID=V412-S05
CANONICAL_TYPE=type:task
ONE_CONCERN=ADS_CONFORMANCE_WIRING
PRODUCT_R3_BLOB=0bfbf782c8859e79df52c9b57904ad80bcd718e9
L2_R5_BLOB=68608ef6456334d627db1797ba2e023233c84ce7
FROZEN_DAG_BLOB=adc9e522f3b734a59898091945b9c7545530565a
DAG_FREEZE_CHECKPOINT=7949caf630edbe83d1dff1ffb7cee8906b77c56f
DAG_FREEZE_RECORD_BLOB=f0a998a73c9319564b239026220ee44934778153
TARGET_VERSION=4.12.0
REAL_V411_RELEASE_PREDECESSOR=NOT_YET_QUALIFIED
REAL_V412_IMPL_BASELINE=NOT_YET_PINNED
PACK_STATUS=AUTHOR_PREPARED_NOT_REVIEWED_OR_FROZEN
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

## 3B. Same GitHub login, independent operators — existing-protocol conformance cases

**Source owner reuse:** `GITHUB_AGENT_INTERACTION_PROTOCOL.md` §5/§7/§8.1.1 and the existing `schemas/agent-event-v2.schema.json` operator fields already distinguish logical execution from GitHub `transport_actor`. S05 **must not** introduce a new Agent Account registry, login inequality Gate, mandatory multi-provider round or second Review engine. S01 owns normative stage/admission wording; S05 owns *only genuinely missing* current-schema/template/shared-verifier tests/wiring.

**Before making any new validator**, inspect whether the existing agent-event / Review / Issue/PR admission path currently uses GitHub `user.login` as the **independence predicate**. Record `ALREADY_SATISFIED` for proven correct checks; otherwise add the smallest focused negative assertions below to an existing genuinely executed test suite on the eligible exact integration SHA:

- `ID-V01`: two truly independently dispatched contexts with distinct accepted `operator_id/session_ref`, same authenticated GitHub `transport_actor` and current exact-HEAD ⇒ logical Review not auto-rejected by shared login.
- `ID-V02`: different GitHub accounts but the same independently established logical operator/implementation context ⇒ Reviewer independence DENY.
- `ID-V03`: a single Builder creates a fictional fresh `session_ref` and forges `operator_id`, or pastes valid-looking `ai-dev:event-v2` comment ⇒ `UNAUTHORIZED/UNKNOWN`; no self-certified Review PASS.
- `ID-V04`: distinct genuine Review operator but stale subject SHA / conflicting accepted Review / missing admission ref ⇒ fails current exact-subject requirement.
- `ID-V05`: real GitHub branch protection requiring a native eligible PR approval is **not** satisfied by two logical Agents with one GitHub account posting comments. Keep external platform requirement BLOCKED until lawfully satisfied; don't call an ADS structured comment a native GitHub `APPROVED`.
- `ID-V06`: if a Product/security/regulated owner explicitly demands different **humans**, model/session separation cannot replace actual human-person independence or human approval.

**Record provenance not passwords:** `actor_role/operator_kind/operator_id/session_ref/transport_actor` + exact Task/PR SHA, verified admission/event ID and, if relevant, GitHub branch-protection result. Test both the same-transport good case and the different-transport bad case. An event JSON schema parse alone proves only shape, not the asserted real origin. No fake host/session identity or fabricated test PASS. These are scoped Task Pack oracles; actual normative/runtime changes await lawful source Claim and qualified v4.11 predecessor.

## 4. Execution readiness / Review / closure

- Intended concern predecessor(s): V412-S03, V412-S04. Native issue edges require actual API mutation and readback; Markdown is advisory historical.
- Risk: **high**. Stage 2.6 pre-dispatch Review Policy candidate: **required**, subject to stronger authority. A Builder cannot self-prove `review:required`.
- Source implementation base: **HOLD** until actual v4.11 Release-qualified predecessor integrated or legally adopted into a v4.12 version branch. Never write normative source under the historic-main planning PR.
- Author/responsible executor shall acquire a current accepted CAS Claim for the *real native Task Issue* before any implementation-source write; a GitHub comment/status alone is insufficient.
- Verification must report exact subject/commit/tree, real command/exit/skip, provenance and strength E1/E2/E3. Only the owning gate/Release actor may promote a result; PR-local PASS ≠ version Release PASS.
- Closeout when authorized source PR is merged on current version integration branch after required Review/validation and canonical readback; otherwise state BLOCKED/NOT_RUN with minimal owning remedy, no duplicate Task Issue/hidden test program.

```ini
TASK_IMPLEMENTATION=NOT_STARTED
TASK_REVIEW=NOT_RUN
TASK_CLAIM=NONE
PACK_FREEZE=NOT_RECORDED
REAL_INTEGRATION_BASE=NOT_VERIFIED
```
