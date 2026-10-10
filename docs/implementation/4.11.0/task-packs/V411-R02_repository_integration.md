<!-- v4.11 Task Pack CANDIDATE ONLY; author=LOCAL_BATCH_B_SUBAGENT_#984; product=#943, L2=#954, DAG=#966; not frozen; no Builder/Claim authority -->

## V411-R02 — Guarded Repository Integration DRAFT (author only)

```ini
PACK_DRAFT=LOCAL_DRAFT_READY_FOR_INDEPENDENT_REVIEW
AUTHORSHIP=LOCAL_BATCH_B_SUBAGENT_DRAFT
INTENDED_FUTURE_PATH=docs/implementation/4.11.0/task-packs/V411-R02_repository_integration.md
TASK_ID=V411-R02
ONE_CONCERN=GUARDED_REPOSITORY_INTEGRATION_OF_ONE_QUALIFIED_RELEASE_INTO_MAIN
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
FROZEN_DAG_PREDECESSORS=R01
RISK=critical
REVIEW_POLICY=required
L3_REQUIRED=YES
EXECUTION_READY=NO
NATIVE_TASK_ISSUE_AND_DEPENDENCIES=NOT_MATERIALIZED
PACK_FREEZE=NO
BRANCH_SOURCE_PR_MERGE=NONE_BY_AUTHOR
BUILD_HOST_TESTS=NOT_RUN_BY_AUTHOR
RELEASE_HIDDEN_RQ=NOT_RUN
RQ_VERDICT_INPUT=UNKNOWN_UNTIL_R01
FINAL_BASELINE=UNKNOWN_UNTIL_R02_RUNS
MERGE_TO_MAIN=NOT_AUTHORIZED_BY_THIS_DRAFT
```

### 1. One concern, actual source and acceptance boundary

**Goal.** After a lawful Release Qualification, exactly one guarded Repository Integration of the qualified release into `main`, owned by a distinct repository-integrator actor. The integrator re-reads current `main` and the qualified candidate; verifies expected-head — an exact main drift/currentness recheck immediately before the merge, then an expected-head merge or an owner-admitted qualified equivalence for any delta; performs the legal merge of qualified source only (fast-forward preferred, explicit merge commit otherwise, per `standards/RELEASE_STANDARD.md` §8); validates the final merged `main` exact SHA/tree sanity; and records the immutable final baseline identity, with an optional tag alias that is NEVER a substitute for the Git SHA.

**Lawful input.** The R01 decision record with verdict READY — the currently pinned `standards/RELEASE_STANDARD.md` §8 admits Repository Integration only "After READY", and §6 reserves CONDITIONAL for authority-accepted limitations, not for integration admission. A missing, stale-candidate, BLOCKED, FAIL or CONDITIONAL RQ verdict means no integration-qualified source exists and integration is BLOCKED; R02 creates no admission exception, and any non-READY admission could only come from a pre-existing exact release-owner decision identity under the then-pinned standard, never from a local or integrator self-admission.

**Acceptance boundary.** An integration record binding exact pre-merge `main` head, observed head at the final recheck, merge mode, candidate SHA/tree vs final `main` baseline SHA/tree (distinguished per §8), final-main sanity result, baseline identity, and optional tag alias. No new product content may ride along; no force, no history rewrite; the frozen candidate ref stays immovable.

### 2. Frozen dependency, sole owner and explicit exclusions

- Frozen DAG: `FROZEN_DAG_PREDECESSORS=R01`, the sole true predecessor. R01's verdict identity must be re-read and current at dispatch; frozen-DAG edges are planning topology, not live READY.
- **Sole owner:** one distinct LOCAL repository-integrator actor (operator/session different from the R01 RQ actor and from every Builder/Validator/Closeout actor). An L3 executor must never collapse V02/V03/V04/R01/R02 into one actor or terminal.
- **Allowed write set (the authorized release merge + final baseline/ref/tag identity evidence only):**
  - the single authorized release merge to `main` (one fast-forward, or one explicit merge commit of the qualified source);
  - the immutable final baseline/ref/tag identity record, published as a canonical append-only Issue/event — NEVER a commit to `main` and never a write to the frozen candidate; any optional file mirror of the record lives only on a separate non-main evidence ref that can never become part of the qualified candidate or `main`;
  - optional annotated tag alias on the final baseline (identical to the candidate SHA when the fast-forward path holds) — alias only.
- **Read-only / forbidden writes:** implementation source and the frozen candidate ref; V01–V04 and R01 evidence artifacts; all `schemas/**`, `templates/**`, `standard-manifest.json`, shared verifiers (`scripts/verify_standard.py`, `scripts/verify_project_standard.py`), `templates/GOLDEN_INDEX.md`, `checklists/version-closure.md`, `docs/implementation/4.11.0/{PRD.md,PRODUCT_PROOF_MATRIX.md,L2_ARCHITECTURE_EVIDENCE.md,TASK_DAG.md}`, other Tasks' owner clauses, `TASK_PACKS.json`, frozen planning branches. `main` is writable ONLY through this one authorized merge transition; force-push, reset, rebase, history rewrite, GitHub Release creation and any other direct `main` mutation are forbidden.
- Inspected read-set guards at version seed `5f224dd662f12fc57fb1bb270ed30e6eb1d83413` (tree `1bfac20e90c69bb57db4f293148b7264d292b5be`): `standards/RELEASE_STANDARD.md@c4d72506253ca7f3d95e305dbd84aae0e1fbe2cb`, `standards/VALIDATION_STANDARD.md@1522b85f9e68cc4a1591ea5899b53c224998e5a8`, `standards/EXECUTION_ARCHITECTURE_STANDARD.md@5588d2196677b1b4878563de65edf2beaa10178f`; re-read current lawful blobs at dispatch and rebind on drift.

### 3. Tests — executable acceptance oracles, not keyword-only checks

The repository-integrator actor executes these oracles later against real Git/readback evidence; **this draft author ran nothing**. They are integration-acceptance checks on the produced record, not production code; no new shared test file is created.

| Positive | Grounded scenario | Required oracle |
| --- | --- | --- |
| P01 | `main` head equals the expected head read back immediately before merge; candidate SHA/tree equal the freeze record; fast-forward valid | FF merge performed; final `main` == candidate SHA/tree; baseline record cites exact SHA/tree |
| P02 | `main` advanced after RQ, and the owning authority admits a documented qualified equivalence for the delta (validation_impact=none basis per VALIDATION_STANDARD §6 discipline) | Explicit merge commit; both validated candidate SHA/tree and final `main` baseline SHA/tree recorded; final-main sanity verified |
| P03 | Drift detected at the pre-merge recheck | Merge halted; currentness recheck re-run; proceed only on restored expected head or owner-admitted equivalence, else BLOCKED |
| P04 | A merge commit is required | Two-identity record (candidate vs final baseline) plus declared final-main tree sanity executed and PASS |
| P05 | Record published after the merge with no further `main` mutation — FF path: candidate C→`main` C; merge-commit path: both identities recorded | Append-only Issue/event publication; independent post-record re-read of final `main` SHA/tree equals the recorded final baseline (`main=C` on the FF path) ⇒ PASS |

| Adversarial | Input / fault | Required fail-closed oracle |
| --- | --- | --- |
| N01 | Candidate ref SHA/tree no longer matches the V02 freeze record at integration time | BLOCKED; no merge; §4 thaw/invalidation path |
| N02 | No lawful R01 verdict (missing, stale-candidate, BLOCKED, FAIL, CONDITIONAL) | BLOCKED; unqualified source never integrates |
| N03 | Drift "resolved" by force-push, reset or silent rebase of `main` | Forbidden; history immutable; BLOCKED plus owner escalation |
| N04 | Extra product/docs changes ride along in the merge (smuggled scope) | Forbidden; the merge contains qualified source only; violation = BLOCKED plus defect record |
| N05 | Tag recorded as the release identity replacing the Git SHA, or a tag on a wrong/unmerged SHA | Invalid; the immutable Git SHA is canonical identity (§9); tag is alias only |
| N06 | Final-main tree sanity fails, or merge-result delta is unevaluated | BLOCKED; no final baseline declared |
| N07 | After FF candidate C→`main` C, the record is published by a second commit C′ to `main` | Baseline PASS refused because `main=C′` ≠ `record.final_main_sha=C`; no second `main` transition; BLOCKED plus defect record; merge-commit path analogous — any post-merge `main` commit diverges final baseline SHA/tree from the recorded two identities |
| N08 | A locally self-admitted CONDITIONAL (or any ad hoc admission) is offered as the integration input | BLOCKED; pinned §8 admits integration only after READY; R02 defines no admission exception and no self-authorization; escalate to the owning release authority |

**Acceptance threshold:** the integration record binds exact 40-hex SHAs, tree hashes, timestamps, merge mode, actor identity and evidence refs; identity claims by ref name or tag alone are invalid; no completeness or release-quality assertion beyond what R01's verdict and the executed merge prove.

### 4. Contract — existing authority with bounded new semantics

`standards/RELEASE_STANDARD.md` §7 places Repository Integration after the verdict and before optional tag/GitHub Release; §8 — the currently pinned integration authority — admits it only "After READY" and requires re-reading live candidate/`main` refs, confirming the frozen candidate still matches its SHA/tree, confirming the target branch has not diverged in a way that changes approved content, preferring fast-forward, distinguishing validated candidate SHA/tree from final `main` baseline SHA/tree, verifying required tree/content equivalence or project-declared final-main sanity, and forbidding smuggled product changes; §9 makes the immutable Git commit SHA (and tree) the canonical release identity, tags/GitHub Releases optional aliases, and fixes the minimum recorded identity fields. `standards/VALIDATION_STANDARD.md` §6 owns exact-SHA evidence and the HEAD/BASE/MERGE-RESULT/CANDIDATE drift classes: the expected-head recheck mirrors the exact-SHA dispatch rule, and owner-admitted equivalence follows the VALIDATION_IMPACT_DECISION discipline (positive impact=none basis), never silent reuse. `standards/EXECUTION_ARCHITECTURE_STANDARD.md` owns the bounded repository/release controllers (read-only reference).

Bounded R02-owned output semantics (additive only): `INTEGRATION_RECORD` = {rq_verdict_ref, candidate_sha, candidate_tree, expected_main_head, observed_main_head_at_recheck, merge_mode, final_main_sha, final_main_tree, tree_sanity_result, post_record_main_sha, post_record_main_tree, baseline_identity_record_ref, tag_alias_optional, integrated_at, integrator_actor, review_ref}. `baseline_identity_record_ref` binds the canonical append-only Issue/event publication — never a `main` commit; `post_record_main_sha/tree` are the independent post-publication re-read of `main` and MUST equal `final_main_sha/tree`, else BLOCKED. No new merge states and no second integration lifecycle are created; the Task Pack defines WHAT, never a base-dependent patch or branch-HEAD assumption.

### 5. Implementation — minimum owner-local delta

Zero mutation of the candidate; the only Git mutation authorized is the single `main` transition. Ordered WHAT-steps: (1) re-read the R01 decision record and confirm a lawful verdict identity; (2) re-read the candidate ref and verify SHA/tree still equal the freeze record — mismatch stops as BLOCKED; (3) read the current `main` head and compare with the expected head recorded at RQ time; (4) run the immediate pre-merge currentness recheck; (5) merge qualified source only — `--ff-only` when valid, otherwise one explicit merge commit carrying no additional scope; (6) read back final `main` exact SHA/tree and execute the declared final-main sanity check; (7) publish the immutable record as a canonical append-only Issue/event — never as a `main` commit and never on the frozen candidate; (8) independently re-read final `main` exact SHA/tree and require `post_record_main_sha/tree` = `final_main_sha/tree`, else BLOCKED; (9) optionally create the annotated tag alias and/or mirror the record to a separate non-main evidence ref that can never become part of the qualified candidate or `main`. **L3 Required handoff, ordered:** oracles (§3) → contract (§4) → this procedure → failure handling (§6) → references (§9). The integrator records the L3 evidence link, exact before/after identities and operator identity; no extra requirement comes from any local prompt.

### 6. Failure handling and UNKNOWN routing

`main` drift after readback ⇒ re-run the currentness recheck; proceed only when the head equals the expected head or the owning authority has admitted qualified equivalence; otherwise BLOCKED. No force push, no reset, no silent rebase, no history rewrite of `main` at any time. Candidate identity drift versus the freeze record ⇒ BLOCKED; RELEASE_STANDARD §4 thaw/invalidation and re-qualification are required; the old RQ verdict remains historical only. Unqualified source (missing/stale/unlawful RQ) ⇒ BLOCKED. Final-main tree sanity failure or an unevaluated material merge-result delta ⇒ BLOCKED plus owning-authority escalation; no final baseline is declared. Post-record re-read of `main` differing from the published record — including any record commit to `main` — ⇒ BLOCKED plus defect record; the second `main` transition is forbidden and history stays immutable. Tag/identity ambiguity ⇒ the Git SHA always wins; BLOCKED until corrected. Any attempted action beyond the authorized write set ⇒ stop, record, escalate; no self-authorization and no improvisation.

### 7. Validation, Review and merge admission

- **Owner verification commands to evaluate and run later by the repository-integrator actor, NOT_RUN by this draft author:** read-only identity checks (`git rev-parse`, `git cat-file -e`, drift inspection such as `git diff --stat <expected>..<observed>`), the single authorized merge (`git merge --ff-only` when valid, else one lawful explicit merge), post-merge readback/sanity, optional `git tag -a`; record exact command/exit/log/evidence location. Any `main` publication uses the repository's lawful push channel; force flags are forbidden.
- **Review:** `risk:critical`, `review:required`; a genuinely fresh independent Reviewer, distinct from the integrator and the RQ actor, binds the integration record to the exact before/after SHAs; a same-actor or stale-identity review is invalid.
- **Merge admission:** this node IS the single authorized release merge to `main`; it authorizes no other merge, no other writer and no second `main` transition — post-merge record publication creates no `main` commit. The admission input is the R01 READY verdict identity under the currently pinned §8. Dispatch requires current canonical native Task Issue + blocked-by dependencies; no automatic promotion from this draft.
- **Distinct-actor rule:** RQ actor (R01) and repository integrator (R02) must be different operators/sessions; V01→V02→V03→V04→R01→R02 are never collapsed into one actor, issue or terminal.

### 8. Bounded Agent Freedom & deferred evidence ledger

```ini
F0_MECHANICAL=identity_readback_single_authorized_merge_execution_and_record_wiring_only
F1_BOUNDED_IMPLEMENTATION=NO_SOURCE_IMPLEMENTATION_INTEGRATION_CONTRACT_AND_ORACLES_FIXED
F2_ENGINEERING_DISCRETION=ONLY_PROVEN_NONMATERIAL_RECORD_WIRING_CHOICES_INSIDE_WRITESET
F3_ARCHITECTURE_REQUIRED=ESCALATE_TO_OWNING_RELEASE_AUTHORITY_NO_SELF_AUTHORIZED_INTEGRATION
ACTOR_PRIVILEGE_ESCALATION=FORBIDDEN
FORCE_PUSH_OR_HISTORY_REWRITE=FORBIDDEN
CANDIDATE_IDENTITY=UNKNOWN_UNTIL_V02_FREEZE
RQ_VERDICT_INPUT=UNKNOWN_UNTIL_R01
FINAL_BASELINE=UNKNOWN_UNTIL_R02_RUNS
R02_MERGE=NOT_RUN
R02_REVIEW=NOT_RUN
TAG_ALIAS=OPTIONAL_NEVER_IDENTITY_SUBSTITUTE
```

Epistemic ledger: the qualified candidate identity, the lawful RQ verdict reference, the expected and observed `main` heads, merge mode, final baseline SHA/tree, sanity result and any tag alias remain UNKNOWN/NOT_RUN until the owning integrator actor supplies real readback evidence. This draft performs no merge, creates no ref or tag, and asserts no release.

### 9. Durable References and next owner

- Frozen Product: https://github.com/kaicreator-mm/ai-development-standard/issues/943#issuecomment-6084264198 (PRD/matrix blobs in the INI block).
- Frozen L2: https://github.com/kaicreator-mm/ai-development-standard/issues/954; Frozen DAG: https://github.com/kaicreator-mm/ai-development-standard/issues/966 (exact head/blob above).
- Task Pack Controller: https://github.com/kaicreator-mm/ai-development-standard/issues/967; version seed: https://github.com/kaicreator-mm/ai-development-standard/issues/973.
- Batch A candidate packs (READ ONLY, do not duplicate): https://github.com/kaicreator-mm/ai-development-standard/pull/978.
- Owning standards at the qualified v4.10 predecessor baseline: `standards/RELEASE_STANDARD.md` (§§4, 7–9), `standards/VALIDATION_STANDARD.md` (§§1, 6, 12), `standards/EXECUTION_PACK_STANDARD.md` §2; future dispatch re-reads each exact separately reviewed owner at the then-current lawful integration HEAD.

**Next:** an **independent Pack Reviewer**, not this author or any future integrator, challenges this draft for scope, oracle coverage, actor-distinctness, merge-guard sufficiency and DAG non-conflict. #967 then materializes one immutable repository Pack file at the intended path plus its single index entry, conducts authoritative Pack Review/currentness, and only afterward permits separately qualified native Task Issue/blocked-by creation. This draft is NOT a Pack Freeze, executable Task Issue, dispatch, merge authorization, or release decision.
