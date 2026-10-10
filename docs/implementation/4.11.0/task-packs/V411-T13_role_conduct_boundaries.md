<!-- v4.11 Task Pack CANDIDATE ONLY; author=LOCAL_BATCH_B_SUBAGENT_#984; product=#943, L2=#954, DAG=#966; not frozen; no Builder/Claim authority -->

## V411-T13 — R02 role-scoped individual engineering conduct DRAFT (author only)

```ini
PACK_DRAFT=LOCAL_DRAFT_READY_FOR_INDEPENDENT_REVIEW
AUTHORSHIP=LOCAL_BATCH_B_SUBAGENT_DRAFT
INTENDED_FUTURE_PATH=docs/implementation/4.11.0/task-packs/V411-T13_role_conduct_boundaries.md
TASK_ID=V411-T13
ONE_CONCERN=R02_ROLE_SCOPED_INDIVIDUAL_ENGINEERING_CONDUCT_CHAIN
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
FROZEN_DAG_PREDECESSORS=T02
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

**Goal.** Frozen Product requirement **R02 INDIVIDUAL_AGENT_ENGINEERING_CONDUCT**: an Agent acting in any declared supported role/job/profile/archetype resolves one complete conduct chain `Input → Allowed acts → Required evidence → Handoff/Exit` for the WEB and LOCAL transports and the Builder/Reviewer/Validator engineering roles (plus Product/Architect/Planner/Controller actors already described in the Frozen PRD actor model). Role legality, allowed mutation, required evidence and exit/handoff come from durable authority; unsupported role/class fails closed; material omissions become `GAP/UNVERIFIED`, never PASS. No invented powers: a WEB actor cannot assert real-host facts it cannot observe, and a Builder cannot self-award Fresh independent Review. Low-risk A0 conduct stays proportional to the Frozen PRD `PROPORTIONALITY` invariant.

**Already implemented on qualified v4.10 owner source; retain rather than duplicate.** `standards/DEVELOPMENT_WORKFLOW.md` (inspected blob `a7fef842927e58a93b671fe9869b9395559845ac`) already owns §3 "Stage 2.6 — Review Policy Selection", §3 Stage 4 "4.4 Independent Review（按需）" (reviewer re-reads pinned standard/Task Issue/deps/diff, reviewer-route distinction), Stage 4 "4.6 Local Agent Handoff（按需）", §4 "Gate Authority" fail-closed applicability, §5 "Blocker Propagation". `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` §8.4.2/§8.5 separates WEB/LOCAL provenance (T05 owner, read-only here). `standards/TASK_DECOMPOSITION_STANDARD.md` §2 "Required durable Task facts" already demands agent-dispatchable durable facts; §11 "Validation / Review decomposition" owns exact-subject evidence.

**Concrete still-missing v4.11 delta.** No single Workflow owner section binds each role/transport/archetype to its full conduct chain with source-bound positive and negative evidence; TASK_DECOMPOSITION_STANDARD has no role/Task entry requirements stating which conduct facts a Task must resolve before dispatch; "unsupported role/archetype" has no explicit fail-closed disposition; and the no-invented-powers rules (WEB≠real host, Builder≠self-Fresh-review) live only in other owners' protocol text rather than as enforceable individual conduct law. T13 owns exactly these gaps; it does not rewrite dispatch/claim, merge, human-authority or Task Learning owners.

**Task deliverable (future Builder work, not done by this author):** bounded role-conduct section + Task-standard role/Task entry requirements + one unique focused test `scripts/test_v411_t13_role_conduct.py`; exact-HEAD independent Review. **Non-goals:** second interaction/execution authority, scheduler/DB, gate-enum changes, T01/T02/T05–T10/T14 owner rewrites, real-host/release PASS by conduct text.

### 2. Frozen dependency, sole owner and explicit exclusions

- **Frozen DAG predecessors exactly `T02`** (its `MATERIALITY_INVENTORY` epistemic states feed role-required evidence; T01's effective-rule floor arrives transitively and stays **read-only**: both T01 and T02 owner sections are frozen to T13). Frozen DAG §3: `T13` follows `T02` because the two own distinct sequential sections of `DEVELOPMENT_WORKFLOW.md`; `T08` follows `T13` for legal scope/human delegation cross-section, so T13 must leave human-authority semantics to T08 untouched.
- **Allowed future normative write set (no other existing source path):**
  - `standards/DEVELOPMENT_WORKFLOW.md` (inspected blob `a7fef842927e58a93b671fe9869b9395559845ac`), **role-conduct section only**.
  - `standards/TASK_DECOMPOSITION_STANDARD.md` (inspected blob `f355c020f07828a62ad617ffa80cb40b708ab4d4`), **role/Task entry requirements only**.
  - **NEW unique** `scripts/test_v411_t13_role_conduct.py` only; no edit/reuse of existing shared tests.
- **DAG ambiguity resolved here:** neither the "role-conduct section" nor the TDS "role/Task entry requirements" exists verbatim in the inspected blobs. Resolution: both are NEW bounded sections added by T13 — the Workflow section sequential to (not overlapping) T02's risk-intake section and T01's §4 effective-rule subsection; the TDS addition adjacent to §2 without renumbering or rewriting existing §§1–14 semantics.
- **Read-only / forbidden writes:** T01 effective-rule clauses and T02 risk-intake section (owner-frozen); `GITHUB_AGENT_INTERACTION_PROTOCOL.md` accepted-event/Review authority (T05); `EXECUTION_ARCHITECTURE_STANDARD.md` Claim/Dispatch §§27–28 (T06) and §14 Merge Controller (T07); Workflow human-authority section (T08); `schemas/**`, `templates/**` (incl. central Task template), `standard-manifest.json`, shared verifiers (`scripts/verify_standard.py`, `scripts/verify_project_standard.py`), existing shared tests, `templates/GOLDEN_INDEX.md`, `checklists/version-closure.md`, `docs/implementation/4.11.0/{PRD.md,PRODUCT_PROOF_MATRIX.md,L2_ARCHITECTURE_EVIDENCE.md,TASK_DAG.md,TASK_PACKS.json}`, other Tasks' owner clauses, `main`, `version/v4.10.0`, frozen planning branches. Shared projections are proposals to exclusive T11.

### 3. Tests — executable acceptance oracles, not keyword-only checks

All cases bind exact actor identity/transport + role/job/profile/archetype + subject; assert the resolved chain (input, allowed acts, required evidence, exit), decision, and absence of unauthorized mutation or claimed evidence. Deterministic offline fixtures legal; anything beyond fixture scope stays `NOT_RUN/BLOCKED`.

| Positive | Grounded scenario | Required oracle |
| --- | --- | --- |
| P01 | Each declared role/transport/archetype resolves a full conduct chain from durable facts alone (no chat context) | Trace records input refs, allowed-mutation scope, per-material-class required evidence (consumes T02 inventory states), exit/handoff condition |
| P02 | WEB actor completes its allowed acts and hands off for real-host evidence | WEB chain ends in handoff requiring LOCAL/host owner; no asserted host/build result; provenance recorded |
| P03 | Builder finishes implementation; Reviewer/Validator are distinct actors | Builder exit requires independent Fresh Review admission it did not produce; Reviewer/Validator chains bind source-bound evidence to exact subject/HEAD |
| P04 | Low-risk CLI/A0 docs-only change | Role duties proportional: no speculative research ceremony, no blanket gates; applicable duties from T01 floor + T02 inventory still enforced |

| Adversarial | Input / fault | Required fail-closed oracle |
| --- | --- | --- |
| N01 | WEB session asserts real host/build/main state as evidence | Rejected: transport cannot mint LOCAL/host facts; `GAP/UNVERIFIED`, chain cannot exit via that claim |
| N02 | Builder self-awards Fresh independent review or marks own PR review PASS | Rejected: self-review never satisfies required Review; admission stays BLOCKED until genuinely independent reviewer |
| N03 | Undeclared/unsupported role, archetype or actor class requests conduct powers | Fail closed: no default powers; disposition `GAP/UNVERIFIED`/`BLOCKED` routed to owning authority |
| N04 | Role chain omits required evidence where T02 inventory shows `PRESENT` material class | Material omission → `GAP/UNVERIFIED`; exit/handoff denied; `NOT_APPLICABLE` forbidden |
| N05 | Profile/override tries to weaken Frozen review/evidence floor for one role | Non-weakening per T01 floor; lower authority fails; higher requirement persists |

**Acceptance threshold:** all in-scope focused cases green on the exact implementation PR HEAD; adversarial cases cannot mint authority, evidence or exit; existing owner/regression tests keep passing or the failure is documented and blocking. Missing T11 wiring → affected projections `DEFERRED_TO_T11`; integrated conformance stays `NOT_RUN` until T12.

### 4. Contract — existing authority with bounded new semantics

Input: actor identity/transport; declared role/job/profile/archetype; exact subject; T01 effective-rule floor; T02 materiality inventory states. Output: one `ROLE_CONDUCT_TRACE` per actor-subject — `{actor, transport, role/job/profile/archetype, legality_ref, input_refs, allowed_acts_scope (write set), required_evidence[] (per material class, with currentness), refusal_grounds, exit_or_handoff_condition, resolution_route}` — owned by the role-conduct section, with TDS role/Task entry requirements stating which conduct facts a Task must resolve to be agent-dispatchable. Conduct resolution is per-actor; it never creates a second gate authority, new Validation Gate state or scheduler; Dispatch/Claim, merge admission, human authority and Task Learning remain with their existing owners. The pack defines WHAT only; no exact-base patch, line map or transient-HEAD assumption is authority.

### 5. Implementation — minimum owner-local delta

Add one bounded role-conduct section to `standards/DEVELOPMENT_WORKFLOW.md` (chain definition, role/transport legality, no-invented-powers rules, unsupported-role fail-closed disposition, A0 proportionality) and one bounded role/Task entry requirements section to `standards/TASK_DECOMPOSITION_STANDARD.md`; preserve all anchors and preexisting semantics. Implement `scripts/test_v411_t13_role_conduct.py` as fixture-fed **decision** assertions (positive and adversarial), not substring checks. T01/T02 owner sections untouched; T05–T08/T14 owners read-only. T11 exclusively owns any shared schema/template/manifest/verifier projection. **L3 order:** Tests → Contract → bounded Implementation → Failure Handling → References; Builder records L3 evidence, exact PR HEAD/base and test identity with truthfully distinct author/builder/validator/reviewer actors.

### 6. Failure handling and UNKNOWN routing

Unsupported role/class or missing legality ref → fail closed (`GAP/UNVERIFIED`/`BLOCKED`), routed to the owning authority per §4 "Applicability UNKNOWN 或矛盾：fail closed"; never granted default powers. Required evidence missing/stale (T02 `UNKNOWN`, stale HEAD) → exit denied until real evidence or owning-authority disposition; never `N/A` because costly. WEB/LOCAL provenance conflict or self-review attempt → `CONFLICT`/rejection with owning-authority route, historical facts preserved. Missing shared projection → `DEFERRED_TO_T11`, not T13 integrated PASS. Frozen Product/L2 incompatibility escalates; this Builder never patches it.

### 7. Validation, Review and merge admission

- **Owner-local verification commands to evaluate and run later, NOT executed by this draft author:** `python -m unittest scripts.test_v411_t13_role_conduct` (or repository-supported direct Python invocation), plus regression `python scripts/test_v49_gate_currentness.py`, `python scripts/test_v410_t04a_gate_repair_routing.py`, `python scripts/test_v49_conformance_suite.py`. Future runs record exact command/exit/log against the real environment.
- **Execution proof:** the future real Build Host/Validator binds tested exact HEAD/tree, OS/toolchain, command, exit code, fixture/source SHA and evidence location; conduct-text or offline results never become host, Hidden or Release validation.
- **Review:** `risk:high`, `review:required`; genuinely fresh independent Reviewer distinct from author and Builder binds currentness, write-set conformance, findings and verdict to the exact PR HEAD. Review PASS alone is not release permission.
- **Merge gate:** canonical native blocked-by graph (T02 → T13; T13 → T08; T13 → T11) created and read back, #973 baseline seed verified, JIT Execution Pack + protected accepted Claim, then one-concern PR to the authorized v4.11 integration branch only; exact-HEAD recheck immediately before merge; no automatic draft→issue promotion.
- **Later integration:** T08 consumes T13's legal scope/handoff boundaries for human delegation; T11 wires any shared projection; T12 proves S08–S12/S15–S18 role-scoped conformance; Candidate Freeze, Hidden, Fresh Closeout, RQ and guarded integration remain separate V/R work items, none PASSed by this pack.

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
T01_T02_OWNER_SECTIONS=READ_ONLY_FROZEN_TO_T13
T11_CENTRAL_WIRING=DEFERRED_NOT_SATISFIED
T12_A_B_C_CONFORMANCE=NOT_RUN
T08_HUMAN_AUTHORITY=PREDECESSOR_CONSUMER_NOT_OWNED_HERE
V01_V02_V03_V04_R01_R02=NOT_RUN
```

Epistemic ledger: current integration HEAD post-#973, native dependency readback, admitted distinct Builder/Reviewer/Validator operators, real execution of focused and regression tests, T11 wiring, T12 integrated role conformance and all V/R stages remain **UNKNOWN/NOT_RUN** until each owning actor supplies real evidence. No claim that role-conduct text alone satisfies R02: owner-local positive/negative proof plus independent Review is the Task-level boundary, never whole-version PASS.

### 9. Durable References and next owner

- Frozen Product: https://github.com/kaicreator-mm/ai-development-standard/issues/943#issuecomment-6084264198 — R02 (conduct chain), R07 (WEB cannot fabricate LOCAL evidence), `TRANSPORT_EQUIVALENCE`, `PROPORTIONALITY` invariants (PRD blob above).
- Frozen L2: https://github.com/kaicreator-mm/ai-development-standard/issues/954; Frozen DAG: https://github.com/kaicreator-mm/ai-development-standard/issues/966 (T13 row + §3 `T01 → T02 → T13` topology).
- Task Pack Controller: https://github.com/kaicreator-mm/ai-development-standard/issues/967; version seed: https://github.com/kaicreator-mm/ai-development-standard/issues/973.
- Batch A/B candidates (READ ONLY, do not duplicate): PR https://github.com/kaicreator-mm/ai-development-standard/pull/978.
- Applicable current standards: `EXECUTION_PACK_STANDARD.md` §2/§5/§6/§8, `GITHUB_WORK_ITEM_CONTRACT_STANDARD.md`, `VALIDATION_STANDARD.md` from the exact qualified v4.10 baseline; owner blobs re-inspected at the version seed table above.

**Next:** an **independent Pack Reviewer**, not this author or a future Builder, challenges this draft for scope, oracle coverage, actual source-bounded gaps, provenance and DAG non-conflict against inspected blobs `a7fef842927e58a93b671fe9869b9395559845ac` and `f355c020f07828a62ad617ffa80cb40b708ab4d4`. #967 then materializes one immutable repository Pack at the intended path with its index entry, conducts authoritative Pack Review/currentness, and only then permits separately qualified native Task Issue/blocked-by creation. This file is **NOT a Pack Freeze**, executable Task Issue, Builder Claim, implementation, CI result or Release decision.
