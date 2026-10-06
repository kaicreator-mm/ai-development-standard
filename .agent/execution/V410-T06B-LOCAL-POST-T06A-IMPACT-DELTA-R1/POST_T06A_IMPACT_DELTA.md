# V410-T06B — Post-T06A Impact & Conflict Delta (PR #925)

```text
authority_effect=NONE
gate_effect=NONE
mutation_authorized=false
verdict_authority=NONE
analysis_subject=PR #925 @ f294173c970d35cf9f9ce4eb4925339e324a801a (base eea3e69, NOT merged)
verdict=NOT_READY_BY_DESIGN
```

This is **planning/analysis evidence only**. It is not a runtime registry, not a resolver, not a resolver contract, not a precedence layer, not a lifecycle or service. It carries no mutation, merge, side-effect, verdict-transfer, gate-waiver, Product-Freeze or Release-READY authority. It does not implement, repair, rebind, or disposition any surface it names. Every disposition it recommends is **for the T06B implementation unit to decide and evidence**, not for this unit to execute or pre-approve.

---

## 0. Subject binding (exact)

- **Analysis subject:** PR #925, head `f294173c970d35cf9f9ce4eb4925339e324a801a`, `refs/pull/925/merge` @ `1b68c331e2ce921bd85de00311b04ec57c0afa50`. Base `eea3e69be5ac3e9c1a78f19e9bdf243ad9c58601` (tree `09db8216ec49caf84b45f404474cfbf4cb5e6ad2`) = PR #918 / V410-T04B R4 merge = current `version/v4.10.0` tip. **PR #925 is open and un-merged**; its candidate is exactly one merge ahead of the base.
- **T06B task definition:** Task Pack `docs/implementation/4.10.0/TASK_PACKS_R1.md#V410-T06B`. Write set: *"shared schemas/templates/checklists/golden/verifier/CI projection surfaces materially affected by settled upstream owners; v4.10 conformance tests"*. Forbidden: central semantic rewrite; second registry; blanket touch-every-file migration. Dependency: `[V410-T06A]` — **not yet satisfied at the base.**
- **T06B acceptance (verbatim anchors used below):** (a1) shared projections match canonical owners; (a2) stale passing verifier cannot override current authority; (a3) **false prose enforcement claims are detected/dispositioned**; (a4) positive and negative conformance coverage exists for material authority/currentness semantics; (a5) only materially affected shared surfaces are changed.
- **Prior T06B unit:** `V410-T06B-LOCAL-BACKCOMPAT-FIXTURE-INVENTORY-R1`, branch head `16b7daffea8d752a441c39cbabb156b09a7417c1`, pinned base `30334e8c7b90a327f8597b86c88c785b98df07f7` (T05A R3 merge) — **one merge stale** relative to this unit's base. Its deliverable is `.../BACKCOMPAT_FIXTURE_INVENTORY.md` (114 fixture paths, 106 rows, `BACKCOMPAT_FIXTURE_INVENTORY_VERIFIED=PASS` on its own branch).
- **Integration drift between the two bases** (`30334e8` → `eea3e69`, measured): 30 paths.

All line numbers below are at the stated subject; blob ids are git blob ids (40 hex).

---

## 1. What PR #925 adds (complete, measured)

`refs/pull/925/merge` vs base `eea3e69`: **14 files, +1008 insertions, −0 deletions — purely additive.**

| Path | Note |
|---|---|
| `.agent/execution/V410-T06A-R1/{MANIFEST,EXECUTION_CONTRACT,TEST_MATRIX,FAILURE_MATRIX,IMPLEMENTATION_MAP,REVIEW_CHECKLIST}` | Superseded for execution by R2; retained as published history, metadata-corrected in place |
| `.agent/execution/V410-T06A-R2/{same six}` | Authoritative T06A pack |
| `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md` | **New source surface, NOT manifest-registered** (103 lines) |
| `scripts/test_v410_owner_convergence.py` | **New source surface, NOT manifest-registered** (349 lines, 22 tests) |

`1b68c331` (merge ref) is a merge of `f294173` into `eea3e69`. No pre-existing file is modified, and in particular **`standard-manifest.json` carries a zero delta** — the pack's adopted `OPTION_A_ZERO_MANIFEST_DELTA`.

### 1.1 Baseline health at the subject (measured, not assumed)

Run on a clean detached checkout at `f294173`:

| Command | Result |
|---|---|
| `python scripts/verify_standard.py` | `standard verification: PASS`; `manifest files: 220`; `bootstrap-required files: 41` |
| all 77 `scripts/test_*.py` | **PASS=77 FAIL=0** |
| `python scripts/test_v410_owner_convergence.py` | `Ran 22 tests … OK` |

**PR #925 does not leave the tree red.** T06B therefore inherits a green baseline, and the D5/D6 redness reported below is caused by T06B's own chartered work rather than by PR #925. The one exception is **D8**, which is a pre-existing property of the base and unrelated to PR #925.

---

## 2. What PR #925 routes to T06B (delta D1 — the charter change)

This is the largest single impact: PR #925 **creates T06B obligations that the existing T06B LOCAL inventory could not know about.**

| Route | Source (exact) | Routed content |
|---|---|---|
| **R1** | `MANIFEST.yaml:53` `routed_gap: REGISTRY_GROWTH_AND_FROZEN_INVENTORY_GUARD_EVOLUTION -> #861` | Evolution of the v4.8 frozen-inventory guard is assigned to T06B/#861 |
| **R2** | reference §3: `DISCOVERY_REGISTRATION=BLOCKED_BY_V48_FROZEN_INVENTORY_GUARD`; *"the missing piece is the mechanical mechanism (evolving the frozen-inventory guard), which is conformance-wiring territory owned by T06B (#861)"* | Names T06B as the owner of the missing mechanism |
| **R3** | reference §1.2, seven rows, each `STATUS=GAP`, `ACTION=STOP_FOR_DISPOSITION (ROUTED_TO=T06B(#861))` | Seven material v4.10 owner families with no current discovery row route to T06B |
| **R4** | reference §5(b): the R1 `TEST_MATRIX.yaml` note is *"factually wrong"* and *"recorded as a projection/instruction defect for the conformance-wiring owner"* | An in-tree false prose enforcement claim routes to T06B |
| **R5** | `EXECUTION_CONTRACT.md:41`, `FAILURE_MATRIX.yaml` N8 | Stale-projection defects recorded with `ACTION=REWIRE_PROJECTION`, routed to #861, *"never silently repaired inside T06A"* |

**Alignment check against T06B's Task Pack:** R1/R2 land on the write-set clause *"…verifier/CI projection surfaces materially affected by settled upstream owners"*. R4 lands squarely on acceptance **(a3)** *"false prose enforcement claims are detected/dispositioned"*. R2's "evolving the frozen-inventory guard" also touches **(a2)** *"stale passing verifier cannot override current authority"*. **The routing is within T06B's charter — it is not a scope violation.**

### 2.1 The seven routed GAP families (reference §1.2)

Each row cites an exact owner blob and a registry check showing no entry:

| CONCERN | CANONICAL_OWNER (blob) |
|---|---|
| task decomposition / Agent-dispatchable granularity | `standards/TASK_DECOMPOSITION_STANDARD.md` @ `f355c020f07828a62ad617ffa80cb40b708ab4d4` |
| live DAG mutation / currentness | `standards/TASK_DAG_GOVERNANCE_STANDARD.md` @ `e2ecfdbf0cd79f750aff40276e46a59159465f78` |
| Task / Execution Pack | `standards/EXECUTION_PACK_STANDARD.md` @ `c7bd2e4ffb87a0ac7fabc54fd78c4eb1fae6ef0d` |
| implementation quality / maintainability | `standards/IMPLEMENTATION_QUALITY_STANDARD.md` @ `3beba2d0324d95674b7bad2ef621e2aa81c66563` |
| public / cross-module compatibility | `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` @ `266aefe32e0990c24fc8c1d6d731c4a3456fc3fc` |
| project adoption (Minimum/Advanced routing) | `standards/PROJECT_ADOPTION.md` @ `aac0d4bff0ed67e6e23d89903e58732524cab024` |
| reference conventions / discoverability | `standards/REFERENCE_CONVENTION_STANDARD.md` @ `ba6a95b124c1804ea4e13c5c6d058e9ade2cc905` |

The registry check basis is `standard-manifest.json` @ blob `21730a0251e35e13591d2c84de1c66d6ab2c2408`.

---

## 3. Adjudication of PR #925's contested claims (measured)

T06B should **not** re-derive these. Both sides of the T06A R1-vs-R2 contradiction were tested directly.

### 3.1 "Registry growth is machine-blocked" — **VERIFIED TRUE**

`scripts/test_v48_registry_adoption.py` (blob `55f78fd9b88bb0e4efd97790b9586beb78e06206`) contains two exact guards:

- `semantic_registry_problems()` at lines **508–532**, with the count guard at **530–531**:
  `if len(entries) != len(V47_SEMANTIC_AUTHORITY_ENTRIES) + len(V48_NEW_AUTHORITY_ENTRIES)` → `"semantic registry entry count deviates from carried + exactly three new"`. `V47_SEMANTIC_AUTHORITY_ENTRIES` (lines 84–93) is 8 hard-coded entries; `V48_NEW_AUTHORITY_ENTRIES` (95–99) is exactly 3.
- `section_conformance_problems()` at lines **439–483**, with the exact-set guard at **463–466** (`manifest section set changed: only … are allowed`) and the additions guard at **479–482** (`unauthorized additions to <section>: […]`). `AUTHORIZED_SECTION_ADDITIONS` (101–126) hard-codes `references` → 6 paths and `verification` → 8 paths.

Four independent growth routes were probed (details in §6.1). **All four are blocked**; the verifier passes in every case. With a schema-valid, uniquely-resolving 12th semantic row, the *only* resulting failure is precisely:

```text
FAIL: test_ra05_registry_resolves_one_owner_per_concern_without_authority
AssertionError: Lists differ: ['semantic registry entry count deviates from carried + exactly three new'] != []
```

**Consequence for T06B:** the blocker is real and mechanical, and it is now T06B's to resolve. T06A's diagnosis is correct.

### 3.2 "T06B may not amend the guard" — **FALSE as a machine constraint**

`55f78fd9…` is **not self-pinned**: `grep` for the blob across the tree finds it only in `V410-T06A-R1/MANIFEST.yaml:54`, `V410-T06A-R2/MANIFEST.yaml:79`, and the reference §2 table. No script, schema, manifest, or CI workflow asserts the guard's blob or forbids its amendment.

The *"must remain unmodified"* wording is therefore a **T06A-task-local constraint** (T06A's own TEST_MATRIX requires `PASS_UNMODIFIED`), expressed in T06A-owned prose — **not** a global machine invariant. T06B is mechanically free to evolve the guard; the constraint on doing so is one of ownership and governance, not of machinery. §8 records the governance contradiction that T06B must still resolve.

### 3.3 "The R1 TEST_MATRIX note is factually wrong" — **VERIFIED TRUE**

`V410-T06A-R1/TEST_MATRIX.yaml:35` ships the claim:

> `notes: 220 manifest files + token assertions; new reference/test must be registered (manifest sections + verification) before this passes`

Read `scripts/verify_standard.py` (251 lines): it checks (i) bootstrap-required assets exist and are declared, (ii) every **declared** manifest path exists (lines 104–105), (iii) no duplicate declarations, (iv) token/enum assertions on named standards and schemas. It contains no `register`/`undeclared` logic and **never** scans for undeclared files.

Measured at `f294173`: `verify_standard` → `PASS`, `manifest files: 220`, with **both** new files unregistered. The numeric claim "220" is correct; the causal claim is **false**. R2's corrected note (`V410-T06A-R2/TEST_MATRIX.yaml:36`) is the accurate statement.

**Consequence for T06B (this is a3's first work item):** the false note remains **shipped inside PR #925** in the R1 pack, which is retained as published history. T06B must either disposition it (e.g. supersede the R1 note with an explicit correction reference) or record why leaving it is acceptable. Note the coupling in §5 C6: the R2 pack's own test asserts the R1 pack's presence.

---

## 4. Delta against the T06B LOCAL fixture inventory (D2, D3, D4)

### D2 — Two new surfaces enter T06B's inventory scope

The inventory at base `30334e8` has **no row** for either new PR #925 surface. Both are material to acceptance **(a5)** ("only materially affected shared surfaces are changed") and to the inventory's own section D ("surfaces a central wiring change could silently break"):

| New surface | Why it is materially in T06B scope |
|---|---|
| `scripts/test_v410_owner_convergence.py` (22 tests) | A conformance regression suite that T06B's own work provably reddens (§5) and that T06B must disposition |
| `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md` | An unregistered reference/discovery surface; its §2/§3 prose asserts constraints T06B's work falsifies (§8) |

### D3 — The blocker is materially under-described in the inventory

The inventory's treatment of the guard suite is:

- Table A (line 70): *"Registry adoption conformance; carryforward of prior-version invariants. Second-registry prohibition maps here."*
- Table C (line 123): listed only as a **producer** for `schemas/execution-pack-manifest.schema.json` — *"among v34/v41/v48 suite references"*.

Neither row mentions the exact-count or exact-set registry-growth guards, and section D (the explicit silent-break flag list, items 1–10) does **not** include it. Yet PR #925 now names this suite as the single mechanical obstacle to registry growth and assigns its evolution to T06B. **The inventory's risk model omits T06B's primary obligation.** This is the most important inventory gap to close.

### D4 — Four inventoried surfaces drifted under T04B (PR #918) before PR #925

Between the inventory base `30334e8` and this unit's base `eea3e69`, PR #918 modified surfaces the inventory records as pinned:

| Drifted path | Inventory row | Concrete effect |
|---|---|---|
| `schemas/agent-event-v2.schema.json` (**M**) | Table C line 121 — *"Legacy v1 transmogrify boundary depends on this staying v2"* | The schema content changed; the inventory's "pins-what" prose must be re-verified at the new base |
| `templates/agent-event-comment.md` (**M**) | Table C line 125 — *"pinned via `TEMPLATE` constant"* | Template changed under a pinned consumer |
| `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md` (**M**) | Table C concern owner | Owner standard moved |
| `scripts/test_v410_t04b_review_currentness.py` (**A**) | **absent from the inventory** | A new conformance suite the inventory does not carry |

The inventory's own §E claim — *"All paths and producer entrypoints were verified to exist at base `30334e8…`"* — remains *literally* true, but its pins-what descriptions are **one merge stale**. T06B must re-verify rather than carry them.

---

## 5. Conflict surface: PR #925 assertions T06B provably collides with (D5)

**This is the central finding.** `scripts/test_v410_owner_convergence.py` ships six assertions that encode *T06A's* zero-delta resolution as invariants. T06B's chartered work necessarily falsifies them.

| # | Test (line) | Assertion | T06B action that breaks it |
|---|---|---|---|
| C1 | `test_candidate_diff_shape_is_exact` (**320–330**) | `git diff --name-only eea3e69` == exactly the 14 T06A paths (`BASE_SHA` at line 45) | **Any** successor candidate that tracks **any** file |
| C2 | `test_manifest_blob_identity_proves_zero_delta` (**170–178**) | `git hash-object standard-manifest.json` == `21730a02…` (line 46) | Any manifest delta |
| C3 | `test_no_manifest_rows_added_for_gap_families` (**164–168**) | entry-id set == the 11 current ids; no GAP-family owner ref | Adding the seven §1.2 rows |
| C4 | `test_reference_and_test_are_not_manifest_registered` (**194–198**) | Neither new file appears in **any** manifest section | Registering them |
| C5 | `test_carried_guards_are_not_amended_by_this_task` (**185–192**) | The two new paths are absent from `t48.AUTHORIZED_SECTION_ADDITIONS` | Evolving the guard's allow-list |
| C6 | `test_gap_is_recorded_and_never_claimed_closed` (**282**) + token asserts at **149–150** (`ROUTED_TO=T06B(#861)`, `DISCOVERY_REGISTRATION=BLOCKED_BY_V48_FROZEN_INVENTORY_GUARD`) | The gap stays open and the token stays present | Closing the gap / editing that prose |

### 5.1 Measured collision matrix

Each case was applied to a detached scratch checkout at `f294173`, the suites executed, then the tree restored (verified `git status --short` empty). `guard` = `test_v48_registry_adoption.py`, `verify` = `verify_standard.py`, `focused` = `test_v410_owner_convergence.py` (22 tests).

| Case | guard | verify | focused failures |
|---|---|---|---|
| clean `f294173` | OK | PASS (220) | none — 22 OK |
| **P1** +1 tracked successor file (staged) | OK | PASS | **1** → C1 |
| **E** register T06A ref+test in manifest (no guard change) | FAIL (1) | PASS (221) | **4** → C1, C2, C4, +`test_carried_frozen_inventory_guards_pass_on_the_real_manifest` (**180–183**) |
| **F** evolve guard allow-list only (no manifest change) | FAIL (1) | PASS | **3** → C1, C5, +same guards test |
| **G** guard + manifest, partially (references only) | FAIL (1) | PASS | **5** → C1, C2, C4, C5, +same guards test |
| **H** guard + manifest **together**, completely | **OK** | PASS | **4** → C1, C2, C4, C5 |
| **I** H + seven GAP rows | **OK** | PASS | **6** → C1, C2, C3, C4, C5, C6 |

Readings:

1. **Case H is the constructive proof that T06A's diagnosis is right and the fix is mechanical.** With guard allow-list and manifest changed *together*, the guard suite returns to `OK` and the verifier stays green. Nothing about T06B's obligation is impossible.
2. **No T06B configuration can keep the focused suite green.** Even the best case (H) leaves 4 failures; the full target shape (I) leaves 6. The suite is not a durable regression; it is a snapshot of T06A's candidate.
3. **C1 fails unconditionally.** Proven in case P1: staging a single new path makes `test_candidate_diff_shape_is_exact` fail with
   `AssertionError: Items in the first set but not the second: '.agent/execution/V410-T06B-SUCCESSOR-PROBE/MANIFEST.yaml'`.
   Because it asserts *set equality* against a **frozen base SHA**, it breaks for T06B, T07A, T07B, T08A, V01 — every successor. (Note the assertion covers **tracked** changes only: untracked files are invisible to `git diff`, so the breakage appears at the first `git add`/commit, not at first write.)

**Consequence:** T06B cannot satisfy acceptance (a1)–(a5) while leaving `scripts/test_v410_owner_convergence.py` untouched. An explicit, evidenced disposition of that suite is a **required deliverable** of the T06B implementation unit, not an optional cleanup.

---

## 6. Self-invalidating base pinning — and T06B's own artifact has it too (D6)

Both the T06A suite and the *prior T06B unit's own* verification script bind to a frozen base SHA. This is a **systemic** conflict, not a T06A-specific defect.

### 6.1 `scripts/test_v410_owner_convergence.py`
`BASE_SHA = "eea3e69…"` (line 45); `test_candidate_diff_shape_is_exact` diffs the worktree against it. Breakage shown in §5.1/P1.

### 6.2 `scripts/test_v410_t06b_backcompat_fixture_inventory.py` (the prior T06B unit's artifact)
`BASE_SHA = "30334e8c…"` (line 34); `check_head_binding()` (lines 55–84) accepts only (i) `HEAD == 30334e8…`, or (ii) HEAD descending from it with `git diff --name-only 30334e8…HEAD` limited to `PACK_DIR/*` + `SELF` (lines 77–78). Measured:

| Location | Result |
|---|---|
| its own branch `16b7daff` (base + pack) | `BACKCOMPAT_FIXTURE_INVENTORY_VERIFIED=PASS` — 114/114 paths, 76/76 entrypoints |
| detached scratch at `f294173` (post-T06A tip) | **`exit=1`**, `FAIL: HEAD f294173… is not bound to base 30334e8… and drift is outside the allowed write set` (30 drifted paths) |

**The moment T06B's branch is rebound onto the post-T06A tip, its own inventory verification goes red — independently of anything T06B does.** The rebind is required (T06B depends on T06A), so this failure is *unavoidable* and must be planned for, not discovered.

> Method note: the guard script printed its failure verdict while the pipeline's exit code reflected `tail`; the true exit code was re-measured separately as `1`.

---

## 7. Verification visibility: CI blindness and the dirty-tree hazard (D7, D8)

### D7 — CI cannot see the successor breakage

`.github/workflows/verify-standard.yml` runs a **fixed 26-step list** of explicit `run: python …` commands. `grep` for `test_v410` in that workflow returns **nothing**:

- `scripts/test_v410_owner_convergence.py` — **not in CI**
- all other `scripts/test_v410_*.py` — **not in CI**

Consequences for T06B:

1. The red suite in §5 will **not** fail the authoritative Linux gate on a `main` push. It will silently remain red.
2. T06B therefore **cannot rely on CI** to detect or enforce the disposition. The disposition must be carried in T06B's own evidence (LOCAL full-visible-set run + concern Validation + Independent Review).
3. Conversely, adding the successor-affected suite to CI without first fixing C1 would convert a silent local red into a permanent CI red — an ordering constraint worth recording.

### D8 — A dirty working tree reddens a carried suite (measurement hazard, **not** caused by PR #925)

Discovered while measuring this unit's own pack. `scripts/test_v48_orchestration_dogfood.py` tests `ODF-11` (`test_odf11_bounded_executor_eligible_success`, method lines 969–1067; write-set verification block 1019–1054) builds its candidate path set from

```python
candidate_paths_between(pack_head, lane_head)      # lines 151-166
  = git diff --name-only <pack_head>..<lane_head>  # durable T-011 lane diff
  + git status --porcelain --untracked-files=all   # ALL uncommitted working-tree paths
```

and then asserts every path is either exactly `scripts/test_v48_orchestration_dogfood.py` or under `docs/implementation/4.8.0/dogfood/orchestration/` (lines 1034–1053).

**Measured** in a clean detached checkout at `f294173`:

| Tree state | exit | Evidence |
|---|---|---|
| clean | **0** | passes |
| + one untracked `.agent/execution/PROBE-PACK/MANIFEST.yaml` | **1** | `AssertionError: False is not true : path outside Builder write set: .agent/execution/PROBE-PACK/MANIFEST.yaml` |
| same path staged | **1** | same |
| path removed | **0** | passes; `git status --short` empty |

Consequences for T06B's evidence runs:

1. **Any LOCAL builder with uncommitted work has a red `test_v48_orchestration_dogfood.py`** — including a builder whose new files are entirely legitimate. This is a property of the base, present before PR #925 and unaffected by it.
2. A "full visible set" measurement is therefore only meaningful on a **committed** tree. This unit's own pack reproduced it exactly: `PASS=75 FAIL=1` on its uncommitted tree versus `PASS=76 FAIL=0` on the same tree after commit — differing *only* by this effect, with ODF-11 the single failure.
3. T06B should commit before measuring, or it will record a false red and risk misattributing it to its own change (or to PR #925).

---

## 8. Open contradictions requiring T06B disposition (recorded, not decided here)

These are **governance** conflicts that no amount of measurement resolves. This unit records them; T06B must disposition each explicitly. No recommendation here is an authorization.

| # | Contradiction | Sides |
|---|---|---|
| X1 | **`NO_GREEN_BY_DELETION` vs the routing.** T06A `FAILURE_MATRIX.yaml` N7: trigger *"…or amending a carried conformance guard"*, expected `FAIL`. Yet T06A routes guard evolution to T06B. | Read literally, N7 forbids exactly what R1/R2 assign to T06B. N7 is T06A-scoped in intent (*"never silently repaired inside T06A"*, N8), but its wording is unconditional. |
| X2 | **"must remain unmodified" vs the routed evolution.** Reference §2 marks `test_v48_registry_adoption.py` *"**must remain unmodified**"*; §3 and `MANIFEST.yaml` route its evolution to T06B. | Same tension, in prose. |
| X3 | **Gap-open prose vs gap closure.** Reference §3 asserts `DISCOVERY_REGISTRATION=BLOCKED_BY_V48_FROZEN_INVENTORY_GUARD` and *"MUST NOT be claimed as closed"*; C6 asserts that token's presence. A T06B that closes the gap falsifies both. | Leaving the prose creates an in-tree false statement — itself an (a3) violation. |
| X4 | **"stale passing verifier" framing.** Acceptance (a2) requires that a stale passing verifier cannot override current authority; T06A's C1/C2/C4/C5 instead make a *correct*, authorized evolution look like a failure. | Distinguishing "a stale verifier caught a real regression" from "a snapshot test forbids an authorized change" is exactly T06B's (a2)/(a3) judgement call. |

**Recommended shape (analysis only):** treat the §5 collision as a single, bounded `ACTION=REWIRE_PROJECTION` disposition owned by T06B, carrying (i) the case-H/I reproduction, (ii) an explicit statement that C1–C6 encoded T06A's *candidate-local* zero-delta resolution rather than durable semantics, and (iii) the replacement regression form. The cheapest moment to fix C1 is **before PR #925 merges** — still T06A's own candidate, where the correction costs one file; after the merge it becomes a cross-task amendment.

---

## 9. Reproduction record (commands and observed output)

All commands run from a repository root. Scratch copies live under `_tmp/v410-t06b-post-t06a-impact-delta-r1/` and were removed from consideration after use; every mutation was reverted and verified.

```text
# subject extraction (no network: mirror carries the PR ref)
git -C _mirror/ai-development-standard.git for-each-ref refs/pull/925
  -> refs/pull/925/merge 1b68c331e2ce921bd85de00311b04ec57c0afa50
git -C _mirror/ai-development-standard.git diff --name-status eea3e69..f294173
  -> 14 x A (additive only)

# baseline health at f294173 (clean detached checkout)
python scripts/verify_standard.py                        -> PASS; manifest files: 220
for f in scripts/test_*.py; do python "$f"; done         -> PASS=77 FAIL=0
python scripts/test_v410_owner_convergence.py            -> Ran 22 tests ... OK

# guard-claim adjudication (scratch, manifest restored each time)
A append schema-valid 12th semantic_authorities row
  -> guard exit=1: "semantic registry entry count deviates from carried + exactly three new"
  -> verify_standard exit=0 PASS (manifest files: 220)
B sections.references += V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md
  -> guard exit=1: "unauthorized additions to references: ['references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md']"
  -> verify_standard exit=0 PASS (221)
C sections.verification += scripts/test_v410_owner_convergence.py
  -> guard exit=1: "unauthorized additions to verification: ['scripts/test_v410_owner_convergence.py']"
  -> verify_standard exit=0 PASS (221)
D new dedicated section for both files
  -> guard exit=1: FAILED (failures=1)   -> verify_standard exit=0 PASS (222)
   (guard RA-06 also reports "'BLOCKED' != 'RESOLVED'": the read router fails closed)

# successor-collision probe (detached scratch at f294173)
P1 stage 1 new path  -> focused FAILED (failures=1): test_candidate_diff_shape_is_exact
H  guard+manifest together, complete -> guard OK; verify PASS; focused FAILED (failures=4)
I  H + seven GAP rows                -> guard OK; verify PASS; focused FAILED (failures=6)

# prior T06B artifact, same design flaw
python scripts/test_v410_t06b_backcompat_fixture_inventory.py   # own branch 16b7daff -> PASS
python scripts/test_v410_t06b_backcompat_fixture_inventory.py   # at f294173       -> exit=1
  FAIL: HEAD f294173… is not bound to base 30334e8… and drift is outside the allowed write set

# dirty-tree hazard (D8), clean detached checkout at f294173
python scripts/test_v48_orchestration_dogfood.py                       -> exit=0  (clean)
touch .agent/execution/PROBE-PACK/MANIFEST.yaml                        -> exit=1
  AssertionError: False is not true : path outside Builder write set:
  .agent/execution/PROBE-PACK/MANIFEST.yaml
git add -A; python scripts/test_v48_orchestration_dogfood.py           -> exit=1  (staged)
rm -rf .agent/execution/PROBE-PACK; python … -> exit=0  (restored)
```

**Repo hygiene:** after all probes, `git status --short` was empty in the scratch worktree and in both pre-existing worktrees (`v410-t06a-owner-convergence`, `v410-t06b-local-backcompat-fixture-inventory-r1`). No pre-existing file anywhere was modified by this unit.

---

## 10. Summary — the delta T06B must absorb

| ID | Delta | Severity |
|---|---|---|
| **D1** | T06B acquires the frozen-inventory-guard evolution obligation + seven GAP-family registration rows + an in-tree false-prose disposition (routes R1–R5). Within T06B's write set and matching (a2)/(a3). | High — charter-level |
| **D2** | Two new unregistered PR #925 surfaces enter T06B's inventory scope; neither appears in the prior inventory. | Medium |
| **D3** | The prior inventory materially under-describes `scripts/test_v48_registry_adoption.py` — it omits the exact-count/exact-set guards that are now T06B's primary obligation — and section D does not flag it as a silent-break surface. | High — inventory completeness |
| **D4** | Four inventoried surfaces drifted under PR #918 before PR #925; re-verify pins-what prose rather than carrying it. | Medium |
| **D5** | Six committed assertions (C1–C6) in `scripts/test_v410_owner_convergence.py` are falsified by T06B's chartered work; **C1 fails for every successor candidate regardless of T06B's choices**; no configuration keeps the suite green (best case H → 4 failures). An evidenced disposition of this suite is a required T06B deliverable. | **Blocking — highest** |
| **D6** | T06B's own prior inventory script is base-pinned the same way and **will** fail at the post-T06A rebind, independent of T06B's choices. Plan the rebind. | High — unavoidable |
| **D7** | CI runs a fixed 26-step list excluding all `test_v410_*` suites, so none of D5/D6 will surface in CI; enforcement must come from T06B's own evidence. | Medium — visibility |
| **D8** | `test_v48_orchestration_dogfood.py` ODF-11 fails on **any** uncommitted working-tree path, so LOCAL full-set measurements are only valid on a committed tree. Pre-existing at the base, not caused by PR #925 — but it will produce a false red in T06B's evidence runs if not anticipated. | Medium — measurement hazard |

**Verified-correct claims T06B need not re-litigate:** PR #925 leaves 77/77 suites + verifier green; registry growth is genuinely machine-blocked on all four routes; the "must remain unmodified" guard constraint is task-local prose, not a machine invariant; the R1 `verify_standard` note is genuinely false and R2's correction is genuinely accurate.
