# V410-T06A R3 execution contract — durable-form repair + scope correction on the unmerged candidate

Integration base: `eea3e69be5ac3e9c1a78f19e9bdf243ad9c58601` (tree `09db8216ec49caf84b45f404474cfbf4cb5e6ad2`) = current `version/v4.10.0` tip (re-read at this rebind: unchanged). Task: #860. Execution environment: LOCAL. Dispatch: `V410-T06A-BUILDER-R3` on branch `task/v4.10.0-v410-t06a-owner-convergence` (PR #925, open, unmerged; head at rebind `f294173c970d35cf9f9ce4eb4925339e324a801a`).

Frozen authorities: Product #837, L2 #842 §§3/5 (blob `b03f12700153e128f4a4c02b7e8d7adf960fd7d3`), refined DAG #848, Task Pack R1 §V410-T06A. Predecessors #851/#857/#858/#859 durable DONE.

This pack supersedes `V410-T06A-R2` **for execution only**; R2 stays byte-identical as the executed authority of the f294173 candidate. The R2 resolution is retained: Option A, zero `standard-manifest.json` delta, carried guards unmodified, the seven discovery-gap families recorded and routed to T06B (#861).

## 1. Why this generation exists (measured at the rebind)

```text
baseline @ f294173 (clean detached worktree):  77/77 scripts/test_*.py PASS
                                                verify_standard.py PASS (manifest files: 220)
                                                focused suite: Ran 22 tests ... OK
```

Four findings from the rebind, all pack-level, none requiring source mutation by the controller:

1. **R1 machine-conformance defect (corrected in place by this round).** `V410-T06A-R1/TEST_MATRIX.yaml` and `V410-T06A-R1/IMPLEMENTATION_MAP.md` shipped the claim that the new surfaces must be registered in `standard-manifest.json` sections for `verify_standard` to pass, and instructed it. Read `scripts/verify_standard.py` at the base: it verifies that manifest-declared paths exist and that bootstrap-required assets are declared; it performs **no undeclared-file scan**. The candidate measures PASS with both surfaces unregistered. Worse, the instruction is machine-incompatible: any such registration fails the carried RA-05 exact-set guard. Corrected in place with provenance in the R1 pack (`MANIFEST.yaml` `conformance_corrections`, `TEST_MATRIX.yaml` `corrections`, `IMPLEMENTATION_MAP.md` corrections section).
2. **Frozen-v4.8 inventory contradiction — dispositioned.** See §2.
3. **Candidate-scope assertions live in the focused suite.** The R2 suite asserts the candidate shape against the frozen base (`git diff --name-only eea3e69` set equality, manifest blob identity, entry-id set, non-registration, guard source freeze). Any successor candidate that tracks any file fails the first of these; the authorized T06B evolution (guard + manifest together) fails four. This is the `SNAPSHOT_ASSERTION_SELF_INVALIDATION` class. The repair is bounded in §3.
4. **Rebind-tip expectation, declared.** At this rebind commit the branch tip additionally carries the six `.agent/execution/V410-T06A-R3/*` paths, so `test_candidate_diff_shape_is_exact` is expected to FAIL until the Builder's repair lands. This is measured and recorded in `TEST_MATRIX.yaml` (`rebind_tip_expectation`) — it is not the candidate under validation. CI does not run any `scripts/test_v410_*` suite, so this does not surface as a CI signal (verified: no `test_v410` step in `.github/workflows/verify-standard.yml`).

## 2. Disposition — frozen v4.8 inventory vs v4.10 registry growth (authority-consistent)

Subject: `scripts/test_v48_registry_adoption.py@55f78fd9b88bb0e4efd97790b9586beb78e06206`, `semantic_registry_problems` (exact count: carried + exactly three v4.8 entries) and `section_conformance_problems` (exact section sets over frozen baseline ∪ authorized additions), carried into v4.10 by the v4.8/v4.9 composition — versus Frozen L2 #842 §3: *"v4.10 extends that registry only when a material current owner is missing; it does not create a competing registry."*

Authority chain (highest first): Frozen Product #837 **>** Frozen Architecture L2 #842 **>** refined Task DAG #848 **>** Task Pack R1 §V410-T06A/§V410-T06B **>** Execution Pack (R1/R2/R3) **>** agent choice.

**Finding.** The guard is a carried conformance projection of the v4.8 inventory — a lower-authority artifact than the Frozen Architecture. Its **invariant** (unique-owner resolution; no unauthorized additions; count pinned to carried + authorized new) remains authoritative as a rejection of unauthorized mutation. Its **pinned inventory** (11 semantic rows; exact section sets as of v4.8) is stale with respect to the L2-authorized v4.10 growth.

**Disposition (binding).**

1. Registry growth remains authorized by Frozen L2 §3 and is owned by **V410-T06B (#861)**, whose charter is conformance wiring and whose acceptance criteria (a2) *"stale passing verifier cannot override current authority"* and (a3) *"false prose enforcement claims are detected/dispositioned"* name exactly this case.
2. Guard evolution is therefore (a) required for T06B completion, (b) **forbidden to T06A** (T06A's write set excludes verifier/CI wiring; NO_GREEN_BY_DELETION forbids T06A green-by-weakening), and (c) **not a silent repair**: the guard and the manifest delta MUST move together so the invariant keeps holding. Constructive proof already measured: with guard allow-list and manifest changed together, the guard suite returns to OK and `verify_standard` stays PASS.
3. **T06A-scope readings** (binding for this task only; R2 wording is retained byte-identical as the executed authority and is read through this disposition):
   - reference §2 *"must remain unmodified"* = **not amended by T06A** — not a global immutability claim;
   - `PASS_UNMODIFIED` in the T06A matrices = the T06A candidate's negative proof that no unauthorized manifest mutation occurred;
   - N7's *"or amending a carried conformance guard ⇒ FAIL"* = scoped to **T06A's candidate** (no green by deleting or weakening a carried guard). It does not constrain T06B's authorized evolution.
4. The discovery gap stays **OPEN** in T06A (`STATUS=GAP`, `ACTION=STOP_FOR_DISPOSITION`, `ROUTED_TO=T06B(#861)`); *"MUST NOT be claimed as closed"* binds claims made **without** the disposition. T06B closes it only through its own authorized, evidenced work.

No source, guard, manifest or write-set mutation is made by this disposition. `authority_effect=NONE`, `gate_effect=NONE`.

## 3. Successor write set (exactly two surfaces)

### Surface A — `scripts/test_v410_owner_convergence.py` (durable-form repair)

Required properties (the implementation is the Builder's; the properties are fixed):

```text
P1 successor-safe   the suite PASSES on any successor tip whose change set is authorized by that
                    successor's own pack; no assertion may depend on the branch tip being exactly
                    this candidate
P2 recorded         T06A's R2 candidate resolution stays machine-recorded in-tree as dated evidence
                    with its recorded identities: frozen-base diff shape = the 14 declared paths,
                    manifest blob 21730a0251e35e13591d2c84de1c66d6ab2c2408, guard non-amendment,
                    non-registration, zero manifest delta — as a record, not a live tip assertion
P3 durable twins    guard behavior is tested by function (a mutated in-memory manifest must still be
                    rejected), not by freezing the guard's source text or its additions constant
P4 fail-closed      every N1-N7 mutant is still rejected; no negative case weakened
P5 no green by      no semantic assertion is removed to satisfy P1; the P2 record is not obtained by
   deletion         deleting the negative cases
```

The concrete failing shape to avoid is recorded (the rebind-tip measurement and the case-H/case-I reproduction: 4 and 6 failures respectively); the Builder MUST reproduce the successor-collision and the authorized-evolution simulation as evidence for P1, and MUST record the committed-tree full-suite result (commit before measuring — an uncommitted working tree reddens `test_v48_orchestration_dogfood.py` ODF-11 independently of this task).

### Surface B — `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md` (scope correction)

```text
Q1  guard family: "not amended by T06A" + evolution ownership recorded as T06B (#861) under the
    Frozen L2 §3 authorization — replacing a bare "must remain unmodified" reading
Q2  the gap remains STATUS=GAP / ACTION=STOP_FOR_DISPOSITION / ROUTED_TO=T06B(#861); no closure claim
Q3  §5(b)'s defect record updated to the corrected state (R1 pack correction landed; residual
    conformance-wiring ownership with T06B)
Q4  non-authority declarations, exact-SHA evidence refs and §4 reconstructibility preserved; no
    resolver/runtime contract/precedence layer/lifecycle/service introduced
Q5  the gap-discipline tokens asserted by the focused suite either remain present, or are consciously
    updated in the same commit as their assertions
```

## 4. Forbidden

- Any `standard-manifest.json` delta (Option A retained); any amendment of a carried conformance guard; any schema/template/prompt/checklist/golden/verifier/CI change; any upstream semantic-owner rewrite; a second owner registry; a new event family/state dimension/lifecycle.
- Weakening or deleting a fail-closed case to obtain green; removing a declared gap row; claiming the gap closed.
- Rewriting recorded historical blobs, the `V410-T06A-R2` pack artifacts, or `base_sha`; any silent rebinding.
- Verdict/gate/mutation semantics anywhere in the diff; merge by the Builder; self-approval.

## 5. Gate obligations

On the exact committed candidate: LOCAL Concern Validation PASS, then WEB Fresh Independent Review PASS (independence by context separation), both bound to one unchanged HEAD/tree. `tools/task-check.sh` PASS at closeout. Review PASS is not Release PASS. T06B boundary: registry growth, guard evolution and any residual stale projection stay recorded/routed to #861, never repaired inside T06A.

## 6. Successor dispatch decision (controller-owned, recorded here)

```text
DISPATCH_ID       = V410-T06A-BUILDER-R3
ROLE              = builder
EXECUTION_PROFILE = LOCAL_BUILDER
TASK              = V410-T06A (#860); PR #925
BRANCH            = task/v4.10.0-v410-t06a-owner-convergence
EXPECTED_BASE_SHA = eea3e69be5ac3e9c1a78f19e9bdf243ad9c58601
START_POINT       = the branch head produced by V410-T06A-PACK-REBIND-R2 (this commit)
EXECUTION_PACK    = .agent/execution/V410-T06A-R3/ (classify_pack_staleness == PACK_CURRENT)
AGENT_FREEDOM     = F1_BOUNDED_IMPLEMENTATION
DECISION          = DISPATCH (bounded repair round)
```

**Why a successor Builder, and not an alternative:**

| Alternative | Verdict |
|---|---|
| merge PR #925 unchanged | rejected — the candidate ships a live assertion (`test_candidate_diff_shape_is_exact`) that fails for **every** successor candidate, including the next authorized task, and four more that the authorized T06B evolution falsifies. Merging would put a known self-invalidating regression into the integration base, and the correction would then become a cross-task amendment. |
| route the whole suite disposition to T06B (#861) as the only handling | rejected — T06B is chartered for shared projections, registry growth and guard evolution; this suite is T06A's own unmerged artifact and the repair is inside T06A's declared write set. The cheapest authorized moment is now, before merge. T06B's own obligations are untouched by this repair. |
| close T06A with the gap recorded and the suite as-is | rejected — the gap routing is already recorded and is not what blocks this task; the self-invalidating assertion class is. |

**Bounded scope:** §3 surfaces A and B only. No manifest delta, no guard change, no upstream owner change. The Builder does **not** edit pack material: `V410-T06A-R3/*` and the corrected `V410-T06A-R1/*` are controller-owned; if the Builder believes the pack is wrong, it emits `STOP_FOR_DISPOSITION` instead of editing it.

**Independence:** the Builder's claim precedes its source writes; validation and review come from separate contexts on one unchanged HEAD/tree. The rebind tip is not the candidate: `test_candidate_diff_shape_is_exact` failing there is the declared, measured by-design state.
