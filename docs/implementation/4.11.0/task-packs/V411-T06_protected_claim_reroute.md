<!-- v4.11 Task Pack CANDIDATE ONLY; author=#974@6094568983; frozen Product=#943 L2=#954 DAG=#966; no Pack Freeze or Builder authority -->

# DRAFT Task Pack — V411-T06 Protected Dispatch/Claim + WEB→LOCAL reroute

```ini
PACK_TASK=V411-T06
SOURCE_ISSUE=#974
PRIMARY_CONCERN=ATOMIC_PROTECTED_CLAIM_AND_LAWFUL_UNCLAIMED_WEB_TO_FRESH_LOCAL_REROUTE
TRUE_PREDECESSORS=T05
RISK=HIGH
REVIEW=FRESH_INDEPENDENT_REQUIRED
PACK_STATUS=SOURCE_BOUND_READY_FOR_INDEPENDENT_REVIEW
IMPLEMENTATION_STATUS=BLOCKED_WAITING_DEPENDENCY
BUILDER_CLAIM=NONE
REAL_BUILD_HOST_TEST=NOT_RUN
```

## Governing authority / immutable identity

- Repository: `kaicreator-mm/ai-development-standard`; version `v4.11.0`; Program [#938](https://github.com/kaicreator-mm/ai-development-standard/issues/938), Task Pack integrator [#967](https://github.com/kaicreator-mm/ai-development-standard/issues/967).
- **Product:** [#943@6084264198](https://github.com/kaicreator-mm/ai-development-standard/issues/943#issuecomment-6084264198), PRD `34df09a2433aec5523ab80c90e885f6d9fc78803:docs/implementation/4.11.0/PRD.md@d30f202e8ea662731ff8a4f2ad1ad88cfc5bb179`, matrix `@f59a6daf5430ece66103a830e392a04f71623ff0`.
- **L2:** [#954](https://github.com/kaicreator-mm/ai-development-standard/issues/954), `f1fc21be366579cbeafa98217b52e106a55b41a5:L2_ARCHITECTURE_EVIDENCE.md@c0fa361474996a0626c63e93574a284ae3eb8d91`, genuinely fresh R3 [#953@6093710027](https://github.com/kaicreator-mm/ai-development-standard/issues/953#issuecomment-6093710027).
- **DAG:** [#966](https://github.com/kaicreator-mm/ai-development-standard/issues/966), `26fc83911185675bdea3c540df6df15c0241402b:TASK_DAG.md@9866d35ae1512b156cfdc94cc01aec2fa897f3e6`. Frozen DAG's literal historical draft header is not an unfreeze; #966 is the exact Freeze record.
- **Qualified source inspected (READ ONLY):** `main@b9461d48d902a2c7c00adff6746afc7a02a0ac3e` (qualified v4.10; main branch readback matched when drafting). [#960@6094457818](https://github.com/kaicreator-mm/ai-development-standard/issues/960#issuecomment-6094457818) documents clean-main rebind. [#973](https://github.com/kaicreator-mm/ai-development-standard/issues/973) is the separate LOCAL baseline seed owner; **the version branch and current integration base were NOT confirmed/assigned for this draft**. Do not merge or cherry-pick the old planning ancestry.
- Draft scope: one Task Pack written as this Issue comment **only**. This is source-bound planned acceptance, not a Builder Claim or executed verification. The canonical repository Task Pack/index may be authored **only** by #967's single authorized integrator after independent Pack Review.

## Common implementation admission and gates

1. `BLOCKED_WAITING_DEPENDENCY` until all named predecessors actually complete with accepted exact-current source/Review/Validation, the canonical 20-issue native GitHub `blocked_by` graph is materially created/read back and exact branch/Pack/role/permissions are admitted. Frozen DAG edges are planning, not live READY. `#967@6094483165` gives the intended 30-edge projection, not a REST success.
2. Before local Builder starts, JIT bind the exact implementation base SHA/tree, adopted ADS immutable pin, owner-file blob, accepted predecessor result and full read/write-set. Require legal Task → Execution Pack → Dispatch → **accepted** protected Claim. No speculative PR/branch, no inherited historical PASS, no self-review.
3. Task-owned author-side tests + applicable real Build Host validation on an exact PR HEAD; independent, genuinely distinct **Fresh Reviewer** required by critical/high risk, current exact HEAD/tree and changed path set. No conflicting accepted same-head Review, unknown authority, stale source or missing proof may merge. A Task PR PASS never implies v4.11 P1/P2/P3, V01 Closure, Candidate Freeze, Hidden, Fresh Closeout or RQ.
4. Shared `schemas/**`, `templates/**`, `standard-manifest.json`, `scripts/verify_standard.py`, existing shared tests, `templates/GOLDEN_INDEX.md` and closure checklist are **T11 exclusive/read-only here**. Formal additive schema/manifest or shared verifier proposals go to T11, with lawful DAG/owner amendment on actual conflict; no schema shadows and no fabricated integrated PASS. T12 may use only its unique scenario/fixture/test files.
5. Failed legal preconditions → explicit `BLOCKED`/missing-proof disposition, accepted-fact readback and owner escalation. Do not silently relabel as N/A, weaken a mandatory Review, treat advisory coordination issues as canonical gate or create runtime/scheduler/DB/new authority.


## Source-based current vs missing

- Existing qualified-main `standards/EXECUTION_ARCHITECTURE_STANDARD.md@5588d2196677b1b4878563de65edf2beaa10178f` §11/§11.1.1 already establishes `SINGLE_WRITER_ADMISSION | LINEARIZABLE_CONDITIONAL_WRITE`, protected `repo#task:role:group`, monotonic generation, exactly one incompatible active Claim, append-only terminals, and fail-closed publication ambiguity; §27 already requires work+all resource reservations at one serialization point. §28 owns responsibility handoff/control; its actual numbering differs from historical pre-integration L2 blob (`0bb9e304`) after v4.10 qualified main integration—re-read live numbered scope at Builder JIT.
- Existing `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md@ea007939639bbd6b4afbff1d71fdc19eb83d00be` §8.4.2/§8.5 separates WEB/LOCAL provenance from claim-key identity and makes `DISPATCH_CLAIMED` the accepted Start Record. `schemas/dispatch.schema.json@90bea62524beb0215d5f40cf0be9986786648fec` is a read-only schema reference.
- `scripts/test_execution_architecture.py@a17ba7290458b4115c985faaf5d65773c0cfd16d` already includes duplicate/race, stale generation, idempotent replay and group-authority negative fixtures; `scripts/test_v48_execution_ownership.py@b59daf77076fe0f8788c7a1be543c92412e8facf` includes takeover/terminal/restart reconstruction. These **do not establish** an actual durable old-WEB-unclaimed → cancelled generation → admitted new LOCAL Reviewer → fresh independent Claim trace, nor arbitrary multiresource failure is atomically handled by live adapters.
- New bounded delta: exact-current source-backed protected reroute admission with explicit durable CANCEL/SUPERSEDE and generation; all-or-none reservation across keys/resources; safe late-claim and stale tenant/HEAD rejection; legal independent reviewer wake/drain. No new scheduling engine or state database.

## Owner and actors

**Write only:** `standards/EXECUTION_ARCHITECTURE_STANDARD.md` **Claim/Dispatch §§27–28** and **new unique** `scripts/test_v411_t06_claim_admission.py`. Section 11 historical clauses, §14 Merge (T07), §29 Task Learning (T14), and Interaction accepted-event owner (T05) are **reference only**, unless a separately authorized owner/DAG amendment changes scope. No editing common tests or schemas.

Builder: separately admitted LOCAL source/contract implementer with claim-admission test capability; Controller/authorized single writer: protected reservation and reroute authority; Fresh independent LOCAL Reviewer: distinct operator/session and applicable real-host capability; Validator: owner-local exact-head tests with a safe durable Git test fixture and/or actor-separated adapter boundary. Test doubles may establish deterministic logic only; remote GitHub multihost/current-source claims need real readback and may be `NOT_RUN`.

## L3 — Tests → Contract → Implementation → Failure Handling → References

**Tests/negative oracle IDs** (positive counterpart for each):
- `T06-N01`: two schedulers race the SAME default protected key, including different WEB/LOCAL origins → exactly ONE accepted dispatch/claim; losing proposal is STALE/REJECTED, no canonical accepted event/partial mutation.
- `T06-N02`: older WEB Reviewer dispatch is already CLAIMED → a controller attempting an unclaimed reroute cannot steal/release it; STOP until owning cancellation/terminal/recovery authority and durable resolution, no second LOCAL Claim.
- `T06-N03`: WEB is provably `DISPATCHED_UNCLAIMED`; Controller source-guard CANCEL/SUPERSEDE(g), publish new role-correct LOCAL proposal/admission(g+1), read back current generation, distinct Fresh LOCAL operator independently claims; late WEB Claim(g) is rejected. Verify prior events remain historical, no duplicate terminal.
- `T06-N04`: composite resource set `{claim_key,R1,R2}` and R2 exhausted/unknown or conditional write fails → **0** accepted claim and **0** owned resource bindings, no per-resource CAS-success chain presented as atomic.
- `T06-N05`: stale base/PR HEAD, tenant/environment or Task Pack identity, compatibility-group grant forged/stale, or late old generation → ineligible/UNKNOWN and no accepted mutation.
- `T06-N06`: old dispatch ACK/publication outcome unknown, no canonical admission ref, or GitHub readback unavailable → block incompatible replacement until durable reconciliation. Advisory OPEN issue/derived queue must not create new blocker for unrelated legal gate.
- `T06-P07`: authorized same-operator same-dispatch resume is idempotent; legal fresh terminal allows wake/reduction of downstream real blocked_by only after accepted current Reviewer/Validator evidence; do not infer Review PASS from mere Claim.

**Contract:** preserve canonical event-v2, `DISPATCH_CLAIMED` Start Record and existing serialization mode; atomic logical decision consumes work + all required resource bindings and expected generation, resource cap, exact base/head, tenant and scope. `execution_environment`, `scheduler_origin`, provider label and cost ranking cannot mint authority. Delegated children inherit attenuated rights, not parallel claim keys by naming trick. Cancellation of unclaimed dispatch advances protected generation only through authorized current single writer and immutable event readback.

**Implementation:** minimal owner-local normative text specifying preconditions, generation sequence, canonical cancellation/currentness, claim atomicity and bounded liveness; unique test uses actual owner contract/schema boundaries where available. If a real adapter cannot demonstrate a single composite serialization point, encode BLOCKED/fallback to designated single writer; do not introduce an optimistic per-key mutex as authority. Route any event/schema field proposal to T11 without editing it.

**Failure/recovery:** mismatched generation, claimed old WEB, unknown authority, partial binding/readback, competing writer → fail closed and record exact protected key, both generations, work/role/actor/HEAD/resource ids, losing attempt and subsequent lawful repair. Cancellation never rewrites prior accepted Claim; no automatic timeout seizure.

**References:** Frozen PRD §§2–5; Frozen L2 §§5.1,5.3,6; Frozen DAG §2 T06 and §3 dependencies; execution §11/§27/§28; interaction §8.4.2–8.5; `scripts/test_execution_architecture.py`, `scripts/test_v48_execution_ownership.py`. Consumed predecessor: T05 current accepted-event/human/Review provenance contract, with exact T05 merged SHA **TBD only after merge**.

## Acceptance and terminal boundary

PASS at owner-local level requires reviewed normative rule + focused positive/negative test outputs, test command/exit status and exact subject; real claims of multihost require admissible actor-separated readback. Integrator T11 consumes any additive schema proposal and T12 later proves S16/S17/S08 and compound cases. This draft has **no execution proof**; `REAL_TESTS=NOT_RUN; CURRENT_INTEGRATION_BASE=NOT_BOUND; TASK_READY=NO; VERSION_PASS=NO`.
