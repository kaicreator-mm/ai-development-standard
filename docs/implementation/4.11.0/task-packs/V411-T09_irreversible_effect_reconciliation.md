<!-- v4.11 Task Pack CANDIDATE ONLY; author=#976@6094587423; frozen Product=#943 L2=#954 DAG=#966; no Pack Freeze or Builder authority -->

# DRAFT Task Pack — V411-T09 Irreversible pre-effect DENY and lost-ACK reconciliation

```ini
PACK_TASK=V411-T09
SOURCE_ISSUE=#976
PRIMARY_CONCERN=PRE_EFFECT_HUMAN_DENY_GUARD_AND_UNCERTAIN_EXTERNAL_OUTCOME_RECOVERY
TRUE_PREDECESSORS=T08
RISK=CRITICAL
REVIEW=FRESH_INDEPENDENT_REQUIRED
PACK_DRAFT=SOURCE_BOUND_READY_FOR_INDEPENDENT_REVIEW
IMPLEMENTATION_STATUS=BLOCKED_WAITING_DEPENDENCY
REAL_BUILD_HOST_TEST=NOT_RUN
PRE_EFFECT_SINK_COUNTER_PROOF=NOT_RUN
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


## Concrete source findings: existing vs missing

- `standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md@6da46996fe29cb20d9d052eb45f43dbf3c97ae38` §4 binds material tenant/environment, §6/§14 require explicit actual side-effect authority, §10 disallows unsafe non-idempotent write retries, §§13/16 constrain cleanup/evidence fidelity. These are genuine pre-existing *normative* requirements, not already proven end-to-end runtime guards.
- `standards/DATA_MIGRATION_GOVERNANCE_STANDARD.md@df60d132651db697ae6613f3f055410472b3bf76` §§5,8–10 distinguish fresh install / upgrade / recovery, destructive transition recovery and production mutation permission. `EXECUTION_ARCHITECTURE_STANDARD.md@5588d2196677b1b4878563de65edf2beaa10178f` §§11,27–28 owns Claim/resource/currentness/handoff and §28.4 human control; `GITHUB_AGENT_INTERACTION_PROTOCOL.md@ea007939639bbd6b4afbff1d71fdc19eb83d00be` owns accepted event provenance. Both are read-only to T09.
- Existing `scripts/test_v41_external_systems.py@55ed797e5e460ede1a8503599ed649f4fcbf1541` has a deterministic `test_retries_are_bounded_and_write_retries_require_safety` oracle and lower-fidelity/tenant tests, **not** a post-Claim human DENY effect-boundary sink-counter test. `scripts/test_v48_execution_ownership.py@b59daf77076fe0f8788c7a1be543c92412e8facf` models durable Claim/release. [#949@6085049416](https://github.com/kaicreator-mm/ai-development-standard/issues/949#issuecomment-6085049416) reports *local Git* U02 E2; Frozen L2 explicitly records actual authenticated human post-Claim DENY and real GitHub API/multihost E2 **NOT_RUN**. They must not be described as existing PASS.
- Needed v4.11 delta: when A has already lawfully CLAIMED, a subsequently accepted CURRENT HUMAN DENY must be re-resolved at the *actual irreversible external mutation boundary*, even though claim earlier succeeded; when an external mutation might have succeeded but ACK is lost, successor B must not blind retry. Distinguish safe readback/true provider dedup/authorized compensation from guesswork.

## Owner scope, actors and precise allowed mutation

Write only `standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md`, **bounded effect clauses**, `standards/DATA_MIGRATION_GOVERNANCE_STANDARD.md` **effect/recovery clauses only**, and new unique `scripts/test_v411_t09_effect_boundary.py`. T08's human authority owner, T05 Interaction, T06 Claim, T07 Merge, T11 schema/manifest and Release/Validation are read-only; T09 consumes their accepted contracts, not their ownership. Scope includes no production credentials or network side effects.

Builder must run safe observable effect adapter on an admitted real Local Build Host or eligible isolated environment; safe persistent local sink (e.g., sqlite/file with transactionally read-back effect IDs and counters) permitted as E2-like internal test, but cannot claim actual provider/multihost parity. External service/tenant-specific proof is qualified separately by independent Validator/V01 when required. A and B need distinct recorded logical operators/Claim generations for successor traces. T08 human authority evidence must be independently verifiable, not a forged local string.

## L3 — Tests → Contract → Implementation → Failure Handling → References

**Mandatory positive + adversarial cases** (the actual mutated sink count is measured, not a boolean in a synthetic model):

| Oracle | Execution trace | Assertion |
|---|---|---|
| T09-N01 | A gets accepted current Claim, then real authoritative HUMAN **DENY** from T08, then A reaches guarded irreversible write | Refresh canonical decision *after Claim, immediately before effect*; action rejected, persisted unauthorized sink mutation count **0**; A's previous Claim remains historical and does not veto the new DENY |
| T09-N02 | B successor is READY/eligible after A; valid unsuperseded DENY still current | B's effect attempt blocked before sink, actual total unauthorized mutations **0**, no READY/retry override |
| T09-N03 | GitHub quoted approval/LLM/tool text, old/wrong-tenant human approval, stale HEAD or unsafe operation scope | Authentication + source/subject/currentness mismatch fail closed even when token/API credential physically allows write |
| T09-N04 | A authorized write **commits once** in persistent test sink; ACK dropped; B distinct operator wakes | `EFFECT_OUTCOME_UNKNOWN` until reconciled; B issues **no unsafe second mutation**, persistent same-effect count remains **1** |
| T09-N05 | A may not have committed; ACK lost; current readback insufficient | Do not infer failure/success from timeout; HOLD `BLOCKED/NOT_RUN` until permitted reconciliation; no blind retry |
| T09-P06 | Verified provider persistent effect-state readback or proven same-effect-id dedup with strong current source/tenant identity | One legal reconciliation path; idempotent replay, if specifically proven, never increments real sink count twice |
| T09-P07 | Idempotency unavailable but explicitly authorized compensation with current exact subject, target, human/safety permission and documented post-condition | Only the authorized compensating transition allowed; never treat the compensation attempt as proof of original ACK or safe retry |
| T09-N08 | B/C competing successor, rebase, tenant drift, external readback outage, effect-ID collision, wrong credentials or partial recovery publication | Preserve BLOCKED/UNKNOWN, no guessed next effect, distinct actor attempts and target/effect IDs observable |
| T09-P09 | J06 interrupted destructive migration with verified backup/snapshot recovery vs fresh install | Separate executed recovery evidence and exact target/tenant; a successful fresh install or a down-script's existence is not interrupted-recovery PASS |

**Contract:** Each real effect attempt consumes (not creates) verified current Claim/authority lineage, human decision identity/currentness from T08, exact repository+source/head+operation, target/tenant/environment, effect and attempt IDs, applicable side-effect permission, and material migration/recovery safety. Read canonical human DENY as late as permitted before an irreversible action; if inability to close race/read source makes safe enforcement impossible, **block the effect** and route to owner adjudication—do not promise impossible cross-GitHub/external-API global atomicity. `effect-may-have-succeeded + lost ACK` is UNKNOWN until trustworthy observed state, provider dedup or lawfully authorized compensation establishes what action is safe. No blanket exactly-once claim.

**Implementation:** Add owner-local normative decision table/checkpoint for post-Claim pre-effect guard, ACK ambiguity and next-actor reconciliation, preserve existing authority graph. Write unique focused test with real persistent sink counter and crash/ACK injection between commit and acknowledgment; record events with actual source and actor/provenance, assert counts before/after. L2/#949 E2 remains research and is not imported as production implementation. New common field proposal → T11 with clearly labeled pending integration gate.

**Failure:** pre-effect authority stale/inaccessible, DENY present, lost ACK unverifiable, compensation scope unknown, changed tenant/target, effect ID missing, unsafe retry → `BLOCKED` and explicit durable failure observation, with no unauthorized mutation. Cleanup itself requires applicable side-effect authority; no destructive shared test environment.

**References:** Frozen PRD §§2.4/4/5, Frozen L2 §§5.3/6/U02/10, Frozen DAG §2 T09 and §3 T08→T09, the four qualified-main owner paths above, `scripts/test_v41_external_systems.py`, #949 local U02 research, #975 T08 Pack/accepted actual predecessor result (TBD). T09 ≠ T08: human decision *record/provenance* vs physical effect *enforcement*.

## Owner-local acceptance and gate transfer

On actual JIT admitted PR: command+exit, exact tested git SHA/tree, sink fixture location/proof/reset, **pre/post counters**, source readbacks/actor IDs/generation/effect target, real-host classification, both pass/fail logs, current reviewer. If T08 verified human basis or effect seam is unavailable, emit targeted BLOCKED, never a counterfeit E5. T12/V01 later own integrated real-host/conditional external fidelity and cross-job X01/X03/X07; independent review stays required. **Nothing above was executed by this Pack-authoring Issue**.
