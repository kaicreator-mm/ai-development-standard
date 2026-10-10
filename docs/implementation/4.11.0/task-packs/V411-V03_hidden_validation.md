<!-- v4.11 Task Pack CANDIDATE ONLY; author=LOCAL_BATCH_B_SUBAGENT_#984; product=#943, L2=#954, DAG=#966; not frozen; no Builder/Claim authority -->

## V411-V03 — formal Hidden-Validation-only stage gate DRAFT (candidate only)

```ini
PACK_DRAFT=SOURCE_BOUND_READY_FOR_INDEPENDENT_REVIEW
AUTHORSHIP=LOCAL_BATCH_B_SUBAGENT_DRAFT
INTENDED_FUTURE_PATH=docs/implementation/4.11.0/task-packs/V411-V03_hidden_validation.md
TASK_ID=V411-V03
ONE_CONCERN=FORMAL_HIDDEN_VALIDATION_ONLY_ON_FROZEN_CANDIDATE
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
FROZEN_DAG_PREDECESSORS=V02
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

**Goal.** Exactly the frozen DAG row: formal **Hidden Validation only** on the exact candidate frozen by V411-V02. One independent **Hidden Validator** — an actor distinct from every Builder, from the V01 visible Validator, from the V02 Candidate Freeze controller, and from the V04 Fresh Closeout Reviewer — prepares a **private immutable validation pack** (new pack identity, revision, checksum), executes it in an **isolated run** against the exact frozen SHA/ref/tree, and publishes a **public-safe terminal verdict only**: blind-spot/pack-defect classification and `PASS|FAIL|BLOCKED|NOT_RUN` disposition. Private vectors and pack bytes are never published to GitHub; only their identity/checksum and the public-safe outcome are.

**Already-owned authority; retain rather than duplicate.** `standards/VALIDATION_STANDARD.md` §1 owns the five gate states and forbids executor-convenience `NOT_APPLICABLE`; §3 owns the validation tuple; §5 defines the Hidden profile as independent scenarios unavailable to implementation context and makes CI an executor, not authority; §6 owns exact-SHA/drift discipline; §9 bounds a Validator (no source repair, no merge, no PASS without execution). `standards/RELEASE_STANDARD.md` §4 owns operational immutability of the frozen candidate; §5 owns Hidden independence, the escaped-defect classification vocabulary (`OUT_OF_SCOPE / VISIBLE_TEST_GAP / HIDDEN_PACK_BLIND_SPOT / BOTH_VISIBLE_AND_HIDDEN_GAP / PACK_DEFECT / PRODUCT_DEFECT_NOT_SUITABLE_FOR_HIDDEN`) and the rule to expose only public-safe disposition, never private fixture payloads; `standards/TEST_DATA_AND_SCENARIO_STANDARD.md` owns scenario/oracle quality. No new validation authority, gate enum or workflow state machine is created here.

**Concrete still-missing v4.11 delta.** No owner yet binds for v4.11: (a) the exact split between the private run record and the public-safe terminal; (b) publication of pack identity/revision/checksum with zero payload leak and its negative evidence; (c) refusal-on-drift against the V02 freeze record; (d) the single distinct Hidden-Validator actor admission with fail-closed `NOT_RUN/BLOCKED` for unavailable or insufficient environment; (e) the exact public evidence artifact path.

**Deliverable (future owning actor, NOT this author):** the public-safe terminal verdict at exactly `docs/implementation/4.11.0/V411_V03_HIDDEN_VALIDATION_VERDICT.md` (NEW file, single public write) plus the private-side record held in independent non-public immutable evidence storage. **Non-goals:** release verdict (R01), Final Closeout (V04), Candidate Freeze (V02), any implementation-source change, Hidden-vector authoring inside this Pack, simulated/emulated stand-in results for unavailable environments, and inherited v4.10 Hidden evidence.

### 2. Frozen dependency, sole owner and explicit exclusions

- True predecessor is exactly **V02 (V411-V02 Candidate Freeze)** per frozen DAG §2; topology `V01 → V02 → V03 → V04 → R01 → R02`. V02 is **NOT_MATERIALIZED**; its freeze identity is `UNKNOWN` here. Execution before an admitted V02 freeze is a contract violation, not an acceleration. Authority inputs at dispatch: the V02 freeze record (candidate SHA/tree/ref, pinned standard revision, visibility tuple) as read-only input alongside Frozen Product/L2/DAG exact refs; any mismatch blocks with a scoped rebind demand.
- **Sole owner:** the independently admitted Hidden Validator (role `validator`, Hidden profile per `VALIDATION_STANDARD.md` §5/§9), a distinct operator/session/host from Builder(s), V01 Validator, V02 freeze controller, V04 Fresh Closeout Reviewer, R01 RQ actor and R02 integrator. An L3 executor must never collapse V02/V03/V04/R01/R02 into one actor or one terminal.
- **Allowed writes (only):**
  - `docs/implementation/4.11.0/V411_V03_HIDDEN_VALIDATION_VERDICT.md` — NEW public-safe terminal (no prior blob; exact path is a write guard).
  - Private side, **non-public only**: private pack bytes, private run record (commands, exit codes, logs, host identity, timestamps) in independent Hidden evidence storage. No repository path is granted or may be invented; pack bytes in any GitHub surface are a defect.
- **Read-only / forbidden writes** (seed-inspected guards): `standards/VALIDATION_STANDARD.md@1522b85f9e68cc4a1591ea5899b53c224998e5a8`, `standards/RELEASE_STANDARD.md@c4d72506253ca7f3d95e305dbd84aae0e1fbe2cb`, `standards/DEVELOPMENT_WORKFLOW.md@a7fef842927e58a93b671fe9869b9395559845ac`, `standards/EXECUTION_ARCHITECTURE_STANDARD.md@5588d2196677b1b4878563de65edf2beaa10178f`, `standards/TEST_DATA_AND_SCENARIO_STANDARD.md@5e234f9ab806565a5e728660a3e30dd17fad22d7`, all `schemas/**` (incl. `schemas/validation-report.schema.json@0d0eed72105e5a303a13e67a3166696e926e29c3`), `templates/**`, `standard-manifest.json@971ebcb65c19f68e8d634d75d8ea96ee30957edf`, shared verifiers `scripts/verify_standard.py@a6233b79f8b60594e79302eee1c0e1bb30d0eab0` and `scripts/verify_project_standard.py`, `templates/GOLDEN_INDEX.md@b36d4947cfe7db101e9eb4955ea889b55d988ed1`, `checklists/version-closure.md@2483856a53fbc0127378c45915ad2518819de996`, `docs/implementation/4.11.0/{PRD.md,PRODUCT_PROOF_MATRIX.md,L2_ARCHITECTURE_EVIDENCE.md,TASK_DAG.md}`, all implementation source, V01/V02/V04/R01/R02 owned artifacts, `TASK_PACKS.json`, other nodes' owner clauses, `main`, frozen planning branches, and the frozen candidate ref itself (V03 holds **no** authorized ref transition; drift is reported, never repaired or re-frozen).
### 3. Tests — executable acceptance oracles, not keyword-only checks

Every case is future work of the owning Hidden Validator on a real isolated host against the admitted V02-frozen candidate; **none is executed by this draft author** (`NOT_RUN`). Each case binds exact frozen candidate SHA/ref/tree and pack identity/checksum; per-case evidence lives in the private record, only public-safe aggregates in the terminal.

| Positive | Grounded scenario | Required oracle |
| --- | --- | --- |
| P01 | Declared candidate ref/SHA/tree re-read and matched against V02 freeze record before execution on isolated host | Terminal records exact frozen identity equality; run proceeds only on match |
| P02 | Private pack prepared with NEW identity/revision/checksum; scenarios target failure families unavailable to implementation context | Private record binds pack checksum to run; terminal publishes identity/checksum only |
| P03 | All private cases execute clean with captured commands/exit codes | Public-safe terminal `DISPOSITION=PASS`, per-family outcome counts, zero vector payloads |
| P04 | A scenario exposes a candidate defect or a pack/scenario defect | Exactly one RELEASE §5 classification recorded; truthful `FAIL` or defect disposition; leak-free publication |
| P05 | Some required environment/toolchain dimension unavailable or insufficiently isolated | Terminal declares `NOT_RUN`/`BLOCKED` per affected family with reason; never simulated results |

| Adversarial | Input / fault | Required fail-closed oracle |
| --- | --- | --- |
| N01 | Candidate ref/SHA/tree drifts after freeze (CANDIDATE drift) | Execution refused; terminal `NOT_RUN/BLOCKED`; no PASS on drifted tree; invalidation routed to V02/release authority per RELEASE §4 thaw path |
| N02 | Hidden Validation attempted before admitted V02 freeze, or against a non-frozen ref | No execution; `BLOCKED` with missing-prerequisite proof; no early verdict |
| N03 | Pack checksum mismatch or non-immutable pack identity at run time | Run aborted `BLOCKED`; unverified bytes never execute; new pack identity required |
| N04 | Any Hidden vector or pack bytes discovered on a public GitHub surface | Leak ⇒ recorded defect (`PACK_DEFECT` class), affected evidence invalidated, verdict corrected, re-issuance under new private identity; zero-leak assertion becomes `LEAK_DETECTED` |
| N05 | Pressure to convert `NOT_RUN/BLOCKED` into PASS, or to reuse v4.10 Hidden evidence | Forbidden; old Hidden evidence stays historical for its old candidate/pack identity only |
| N06 | Builder/V01/V02/V04/R01 actor authors, edits or influences the private pack or verdict | Actor-separation violation ⇒ `BLOCKED` + escalation; verdict authored by any other actor is void |

**Acceptance threshold:** the public terminal is complete and self-sufficient for V04/R01 consumption without revealing any vector; all executed families have private command/exit/log evidence; every unexecuted or blocked family is explicitly `NOT_RUN/BLOCKED`; the zero-leak assertion is positive (scan performed) and its negative evidence (leak ⇒ defect) is stated.

### 4. Contract — existing authority with bounded new semantics

Private record (non-public): pack bytes + identity/revision/checksum, per-case scenario family, exact commands, exit codes, key logs, host class, environment/toolchain identity, run start/end, operator identity. Public-safe terminal (exact fields, no payloads):

```text
VALIDATION_ID=V411-V03
CANDIDATE_SHA / CANDIDATE_TREE / CANDIDATE_REF   (must equal V02 freeze record)
FREEZE_RECORD_REF
HIDDEN_PACK_ID / HIDDEN_PACK_REVISION / HIDDEN_PACK_CHECKSUM
ISOLATED_RUN_HOST_CLASS (no private host secrets)
PER_FAMILY_OUTCOME_COUNTS (public-safe aggregates only)
BLIND_SPOT_OR_PACK_DEFECT_CLASSIFICATION (RELEASE §5 vocabulary or NONE)
DISPOSITION=PASS|FAIL|BLOCKED|NOT_RUN
NOT_RUN_OR_BLOCKED_DECLARATIONS (per unavailable family, with reason)
ZERO_LEAK_ASSERTION=ASSERTED|LEAK_DETECTED(+defect ref)
PRIVATE_RECORD_REF (identity/reference of private record only)
EVIDENCE_REFS
```

States use `VALIDATION_STANDARD.md` §1 exactly; `NOT_RUN/BLOCKED` are never converted. Classification uses RELEASE §5 vocabulary only; no new enum, no second validation authority, no silent change to preexisting gate/release states; the Pack defines WHAT and never specifies vectors.

### 5. Implementation — minimum owner-local delta

Owning-actor procedure only: re-verify freeze identity → JIT-prepare private pack (new identity/revision/checksum per RELEASE §5 strengthening rules; scenario quality per `TEST_DATA_AND_SCENARIO_STANDARD.md`) → isolated clean run on exact frozen SHA/tree → private record capture → public-safe verdict authored from the fixed §4 field list → positive zero-leak scan of the public tree → publish the one artifact. No exact-base patches, no line maps, no transient-HEAD commands; the terminal targets the authorized v4.11 version integration branch, one concern/one PR, never `main`.

**L3 Required handoff, ordered:** §3 oracles → §4 contract → this procedure → §6 failure routing → §9 references. Builder/validator/reviewer remain distinct attributed actors; the draft author ran nothing.

### 6. Failure handling and UNKNOWN routing

Drift/ref/pre-freeze/checksum faults → `BLOCKED`/`NOT_RUN` with the exact missing proof; never an optimistic PASS or executor-convenience `NOT_APPLICABLE` (`VALIDATION_STANDARD.md` §1). Environment/toolchain/isolation insufficiency → declared per family, not simulated. Confirmed candidate defect → truthful `FAIL` + classification; repair is a separate Builder dispatch and re-freeze, never in-run repair. Discovered leak → N04 defect path; prior verdict superseded, never silently rewritten. Frozen Product/L2 contradictions route to the owning authority; anything needing later consumption is labelled for V04/R01 with owner and gate, never promoted to version PASS here.

### 7. Validation, Review and merge admission

- **Commands evaluated and run later by the owning actor on real hosts, NOT_RUN by this author:** freeze readback (`git rev-parse`/`git cat-file` against the V02 freeze record), checksum verification of private pack bytes, isolated-run execution per private TEST_MATRIX, public-tree leak scan for pack bytes/vectors before publication. Execution proof records real host role, OS/toolchain identity, exact frozen SHA/tree, per-family outcome/state and any `NOT_RUN/BLOCKED` declaration per `VALIDATION_STANDARD.md` §12 (§7 tested-SHA vs evidence-only-head respected); private detail stays private, only public-safe aggregates publish.
- **Review:** `risk:critical`, `review:required`; a genuinely fresh independent Reviewer, distinct from the Hidden Validator, every Builder, and the V02 actor, binds findings and verdict to the exact terminal blob and frozen candidate identity. Review PASS is not release permission and never substitutes for the executed private run.
- **Merge gate:** the terminal merges only to the authorized v4.11 version integration branch after admitted V02, this reviewed Pack, canonical native blocked-by edges and a protected accepted Claim; no direct `main` write; no self-freeze. **Later consumption:** V04 re-derives version gate truth from this terminal as input (not inherited truth); R01 owns the release verdict; R02 owns integration — none authorized or marked PASS by this Pack.

### 8. Bounded Agent Freedom & deferred evidence ledger

```ini
F0_MECHANICAL=PRIVATE_PACK_EXECUTION_AND_PUBLIC_VERDICT_TRANSCRIPTION_ONLY
F1_BOUNDED_IMPLEMENTATION=NONE_NO_IMPLEMENTATION_AUTHORITY_IMPLEMENTATION_SOURCE_READ_ONLY
F2_ENGINEERING_DISCRETION=NONE_CLASSIFICATION_AND_DISPOSITION_ARE_ORACLE_FIXED
F3_ARCHITECTURE_REQUIRED=ESCALATE_TO_FROZEN_L2_PRODUCT_OR_OWNING_RELEASE_AUTHORITY_NO_SELF_PROMOTION
ACTOR_PRIVILEGE_ESCALATION=FORBIDDEN
HIDDEN_PACK_BYTES_OR_VECTORS_IN_PUBLIC_GITHUB=FORBIDDEN_LEAK_IS_DEFECT
PRIVATE_RUN_EXECUTED=NOT_RUN
PUBLIC_VERDICT_PUBLISHED=NOT_PUBLISHED
ZERO_LEAK_ASSERTION=NOT_ASSERTED
CANDIDATE_FREEZE_IDENTITY=UNKNOWN_UNTIL_V02
V04_V01_R01_R02=NOT_RUN
```

Epistemic ledger: V02 freeze record, private pack identity/checksum, isolated-host admission and coverage, per-family outcomes, leak-scan result, and the terminal blob itself remain `UNKNOWN/NOT_RUN` until the owning Hidden Validator supplies real evidence. This draft asserts no Hidden PASS, no pack completeness, and no release qualification.

### 9. Durable References and next owner

- Frozen Product: https://github.com/kaicreator-mm/ai-development-standard/issues/943#issuecomment-6084264198 (PRD blob above); Frozen L2: https://github.com/kaicreator-mm/ai-development-standard/issues/954; Frozen DAG: https://github.com/kaicreator-mm/ai-development-standard/issues/966 (exact head/blob above).
- Task Pack Controller: https://github.com/kaicreator-mm/ai-development-standard/issues/967; version seed: https://github.com/kaicreator-mm/ai-development-standard/issues/973; Batch A candidates READ ONLY: https://github.com/kaicreator-mm/ai-development-standard/pull/978.
- Governing owners from the qualified v4.10 baseline: `standards/VALIDATION_STANDARD.md` (§1, §3, §5, §6, §7, §9, §12, §13), `standards/RELEASE_STANDARD.md` (§3–§7, §11.6), `standards/TEST_DATA_AND_SCENARIO_STANDARD.md`, `standards/EXECUTION_ARCHITECTURE_STANDARD.md` (dispatch/CLOSURE_VALIDATOR profile), `schemas/validation-report.schema.json` when a machine payload is produced.

**Next:** an **independent Pack Reviewer**, not this author or any future stage actor, challenges this draft for scope, oracle coverage, leak-boundary soundness, provenance and DAG non-conflict. #967 then materializes the immutable repository Pack and index entry after authoritative review; separate admission creates the V411-V03 native Issue and blocked-by edge. This file is **NOT a Pack Freeze, Task Issue, Claim, executed validation, verdict or Release decision**; all gate states remain `NOT_RUN`.
