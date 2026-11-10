# ADS #1366 — R24: repair vacuous source PASS at both Python entrypoints

## Execution-first finding

An earlier exact-Git source-readback of `formal/suite/run.py` (blob `7af42fb6a36ab0d22ad0fb18f7936814d45d9a2e`) and `formal/suite/expanded.py` (blob `3a7bbbedb9420b62e5722d8c817f61983dd6d77b`) exposes the same source-qualification error:

`source_check` / `source_alignment` verify the checked out candidate HEAD, then build an empty `checks=[]` when `source_map.sources=[]`; both return `PASS` because `all([])` is True. For a standalone/simpler runner path without mandatory traceability this creates a plausible **false source-bound PASS** despite having checked zero normative source objects. An individual `anchors=[]` similarly passes the presence check vacuously.

**Do not confuse** this experiment runner's proof-admission bug with an observed production ADS controller defect.

## Repairs committed in original experiment branch

1. `formal/suite/run.py`: after existing candidate HEAD preflight, insist that `sources` be a nonempty list; each entry must contain nonempty string anchors. Missing/empty/malformed source rows produce `FAIL`, not `PASS`. Preserve positive real source rows, previously known `NOT_RUN` when checkout missing, and wrong-head `BLOCKED`.
2. `formal/suite/expanded.py`: identical fail-closed policy; no new intermediate logic layer or product Gate.
3. `formal/tests/test_source_binding_nonvacuity.py`: 7 executable unittest cases covering both entrypoints, positive source Git blob bytes, the uncovered empty inventory, invalid source rows/anchors, actual source drift and no-checkout behavior.
4. Historic 4 source maps read directly from GitHub contain **6,6,7,7** nonempty entries with valid anchors and pinned source blob formats. Existing input shape should remain compatible; true exact-checkout imported test run is still pending.

## Evidence qualification

**Actually executed in this Web environment:** CPython 3.13.5 red→green reproduction of the **isolated exact helper behavior seam**, using an isolated synthetic repo-shaped filesystem and mocked candidate HEAD. Before repair: **7 tests, expected RED, 4 failures + 5 subcase errors**; after repair: **7/7 PASS, 0 skips**. The isolated modules are *copies of the two helper bodies with minimal imports*, **not imported modules from a full Git checkout**, so this does **not** qualify as post-change exact-Git source-runner tests or strict native solver verification.

**Historical results remain:** R11 strict 61/61 Python and 35/35 native and R17/R20 evidence retain only their original subject hashes. Since these two Python runner files are source-model input dependencies, their modified blobs must not inherit full strict results at this new code commit. Follow-up actual exact-checkout regression and affected strict suite should be done as one Delivery-First repair+validation handoff only if Web environment cannot provide needed pinned native tools.

**Severity:** experimental P1 (empty source proof admission) and experimental P2 (empty anchor proof admission), both **code-repaired in this single write set**, exact-worktree run **NOT_RUN**. Formal ADS normative P0/P1/P2 not newly confirmed. No new normative schema, Claim, CI Action, Freeze, Merge or Release.
