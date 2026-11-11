# R34 — Tally Host Writer Admission Interleaving Review

**OUTPUT_LABEL:** `ADS_1366_R34_WRITER_ADMISSION_INTERLEAVING_REVIEW`  
**Subject:** Tally v2 @ `2c6631dbdc3458d4dea43fdc7d78cd292c0aebe9`, consuming the effective ADS v4.18.0 pin.  
**ADS candidate:** PR #1365 @ `dac263fa4c0ab155406d2f2117459b34322cc988` remains OPEN / not frozen.  
**Review type:** exact-source review + bounded Python interleaving model. This is not a deployed runtime race result or an independent second reviewer sign-off.

## 1. R33 is accepted; do not repeat it

R33 at ADS experiment HEAD `2728bfcba4c76412a0aca4b64df5236c8a2fa342` directly read the original Host SQLite registries for historical Tally #166/#169, verified their physical Claim keys, generation, revision=1, `PUBLISHED_VERIFIED`, native comment identities and the Woodpecker #98 API result. **R30 P2-01 is closed for the historical v4.18 subjects.** The transient revision-0 reservation row, tamper-evident custody, cross-process concurrent admission and K journal/successor evidence remain separately qualified. R33 must not be re-run merely to obtain another copy of the same receipt.

## 2. Exact source facts relevant to Writer exclusion

| Source | Exact pin / blob | What it proves — and what it does not |
| --- | --- | --- |
| Tally `single-writer.mjs` | `version/v2@2c6631db...`, blob `7df6426ffd0086b7480cf9258ffe1e71d2d15bb5` | Reads one task key, asks the source for current facts, then uses `mustBeAbsent` on that task-specific key. No shared admission mutex/global CAS key is implemented in this function. |
| Tally `host-admission-source.mjs` | same Tally SHA, blob `0b493e0cd85769ab654538d2edd7b94bd7bef17e` | `registrySnapshot()` reads `list/get` twice and rejects local drift; `activeIncompatibleClaimCount` counts rows with a different protected key. The scan is not atomic with the later reservation; `taskAuthority` does not contain a frozen `exactWriteSet`. |
| Tally `single-writer.test.mjs` | blob `a98b9053e3674e5c3a5946f7f2826e4c33972da6` | `Promise.all` races two controllers on the **same** protected key with real DH SQLite. This correctly proves one per-key winner; it does not exercise different Task keys or overlapping write sets. |
| Tally `host-admission-source.test.mjs` | blob `e40ffb2c44194e76780a048ce38a940ba84b6e82` | Twelve source tests; no multi-Task write-set or barrier-controlled concurrent snapshot test. |
| DomainHarness `sqlite-adapter.ts` | v0.10.2 tag `cee14399d9d0af4e20e34b9111861b16a465b690`, blob `3d5e69a88bafe38dcef73ecd44ea346025d864cf` | `BEGIN IMMEDIATE` takes the SQLite write lock before revision read. This is a physical atomicity guarantee **per key / transaction**, not a cross-key Task write-set lock. |
| DomainHarness `sqlite-cas-multiprocess.test.ts` | same DH tag, blob `00e4167ef9bc7df6db773bb28221e34d0d1d8303` | Uses a real second OS process, but sequentially: parent creates, child duplicate-create conflicts, child exact-revision update succeeds, parent/reopen reads it. It is not a simultaneous two-process race. |
| Tally W-Cx tests | `host-cas.test.mjs` blob `47d61d7f43e4f5b4a651adc8146e4d3bd7738567`; WAL stress blob `f549e9c6559d63a0f7f650efe229ee0ce11b0564` | Same-key race across two connections; optional 4-process WAL initialization writes distinct keys. Neither is a cross-process same-key race nor a multi-Task write-set exclusion test. |

The Host writer configuration field `exclusiveHostControl: true` is checked as a boolean assertion. In the inspected controller/source there is no implementation of a mutex, lease, shared global reservation key or Task Pack overlap check that makes this assertion true under concurrent invocations. An external Host queue/singleton could supply that guarantee, but it has not been read back or tested here.

## 3. Historical Task write-set pair: exact, disjoint, sequential

R32 already verified Tally #169 → PR #170 (7/7 exact paths). R34 adds the corresponding #166 mapping:

- #166 frozen write set: `host-admission-source.mjs` and `host-admission-source.test.mjs`; merged PR #167 changed exactly those **2/2** paths, zero out-of-scope.
- #169 frozen write set: seven selected-business paths; merged PR #170 changed exactly those **7/7** paths, zero out-of-scope.
- The two write sets have **zero intersecting paths**.
- #166 closed at `2026-10-29T22:49:56Z`; #169 was created at `23:34:19Z` and its Claim was published at `23:35:02Z`, **45m06s after #166 closed**.

This is useful source-bound Task → PR evidence for two historical tasks. It is a **sequential disjoint** example, not a concurrent overlapping Writer witness. It cannot close P2-02.

## 4. Bounded interleaving model

New standalone diagnostic model: `R34_WRITER_ADMISSION_INTERLEAVING.py`. It enumerates all 20 order-preserving interleavings of two requests, each with `snapshot → reserve → publish`.

Actual source-shaped assumptions: both snapshots can finish before either per-key reservation; the task keys differ; each `mustBeAbsent` CAS is scoped to its own key; the Host request carries no Task Pack write set; no external mutex is assumed.

Result from executing the exact model source in an isolated CPython 3.13.5 runtime:

| Scenario | Bounded result |
| --- | ---: |
| Different keys + overlapping/unknown write sets + no global lock | **12/20** schedules accept both |
| Example witness | `AS, BS, AR, AP, BR, BP` |
| Same protected key, per-key CAS only | 0/20 double accepts |
| Mutex covering snapshot through reservation | 0/20 double accepts |
| Atomic known-write-set guard with overlap/unknown | 0/20 double accepts |
| Known disjoint write sets under that guard | 12/20 safe parallel accepts |

Python unit tests: **6/6 PASS**, exit 0. An unrelated spreadsheet-runtime warmup warning appeared on stderr during interpreter startup; it did not change the test result. This is a bounded model execution, not execution from the exact ADS Git checkout, not a Z3/cvc5 run, and not a real Host race.

**Interpretation:** the source shape admits a concrete TOCTOU schedule if two task-specific controller calls overlap. This does not yet prove that the deployed Host invokes them concurrently. The next experiment must test the actual Tally controller/source and public SQLite adapter with a deterministic barrier, and must separately determine whether an external Host queue serializes calls.

## 5. R34 decision and next action

- **R30 P2-01:** CLOSED by R33 for historical v4.18 Claim records.
- **R30 P2-02:** PARTIAL. Historical Task write sets are now bound exactly to their merged PRs (2/2 and 7/7) and are disjoint/sequential; source-derived cross-key race candidate found; actual concurrent Host behavior remains NOT_RUN.
- **R30 P2-03:** PARTIAL. Historical K/Woodpecker evidence exists, but durable K journal readback and successor/Grant/resource reconciliation remain NOT_PROVEN.
- **No Tally/DH implementation defect is declared yet.** No Repair, Tally source edit, DH source edit, real GitHub POST, Task/Claim creation or production registry mutation occurred.
- The R34 Python model is **not yet added to frozen `formal/v4.19/r10/suite.json`**. Keep the existing R29 97/97 + 35/35 exact-subject result unchanged. Promote/integrate this model only after exact Node24 runtime reproduction and independent source review establish the intended source invariant.

Next local probe is recorded in the R34 machine receipt as `ADS_1366_R35_CROSS_KEY_HOST_WRITER_RUNTIME_PROBE`: use exact Tally v2 and DH v0.10.2 source pins, run the existing DH process test, run two real OS processes racing the same physical CAS key, then run two different Tally task-key controllers against one shared real SQLite registry with both source snapshots barrier-released before reservation. Use fake GitHub ports only, no GitHub POST. Preserve exact Node/npm/package hashes, process exits, winner count and final DB readback. If both distinct-key controllers return `RECORDED` for overlapping write-set fixtures, record a concrete consumer counterexample and stop before source repair; if one blocks, identify the external serialization mechanism and prove its authority. No tracked Tally/DH changes are authorized by this R34 probe.
