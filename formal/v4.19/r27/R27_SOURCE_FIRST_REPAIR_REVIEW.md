# ADS #1366 R27 — Native-case identity admission bug, with true negative witness

**Current scope**: formal experiment runner only. Candidate PR #1365 `dac263fa4c0ab155406d2f2117459b34322cc988` is OPEN/unmerged and not legally activated. R25's exact-source/native **35/35** and Python **77/77** remain valid only for its **executed** model HEAD `6edd2bad98b455e1bcdd2895f50830412af25cff`.

## Real proof-qualification defect found in code

The original `formal/suite/differential.py` verifies independent **Z3/cvc5 pairs**, and already rejects **orphan or duplicate native case IDs globally**. That is **not** the missing check.

The original `formal/suite/expanded.py:main_v1` takes the `run_case` result list and determines `good` from positive statuses and solver-pair PASS without comparing the **TLC result's model/property/purpose identity or expected result** against the selected declaration. A synthetic result with a **valid TLC ID** but a **foreign `model_id`** and a correct Z3/cvc5 paired result makes the original differential return PASS and the original aggregate `good=True`. In the independently run Python reproduction using the checked original differential behavior, the new identity auditor rejects precisely this mismatch.

This is a **bounded experiment tool P2 proof-admission gap**, not a claim of an actual forged Claim or a broken ADS normative policy.

## Code fix, not another issue or toy SMT model

- `suite/execution_inventory.py` checks selected/results length and **ordered** identity: `id`, `tool`, `purpose`, `property_id`, `model_id`, and `expected` (plus recognized result statuses). Missing, duplicated, reordered, mutated or malformed results yield `FAIL`.
- `suite/expanded.py` now audits returned native case results **before** invoking solver differential. On mismatch, it emits `EXECUTION_RESULT_IDENTITY_MISMATCH`, blocks any `MODEL_AND_SOURCE_PASS`, preserves true solver FAIL severity, records `execution_inventory_audit` in the receipt, and does not increase `source_bound_verified_obligations`.
- Crucially `suite/execution_inventory.py` is added to `model_inputs` so both before/after Exact-SHA runner identity checks cover **the new guard itself**.
- Test sources: `formal/tests/test_execution_inventory.py` (**14** methods, actually executed in isolated Python 3.13.5: **14/14 PASS**, zero skips) and `formal/tests/test_execution_inventory_admission.py` (**1** native-free full `main_v1` negative suite-entrypoint integration test, authored but **NOT_RUN** without real full Git tree).

### Qualification and exact next step

The Python unit tests were actually executed from locally authored source whose Git blobs exactly match the posted new test/helper blobs. The original bug demonstration used an isolated reconstruction of GitHub's original differential source and predicate, **not** a full exact-Git checkout of the current runner.

After this **actual runner code change**, no claim of full 35/35 strict or full 77/77 Python PASS at the new branch HEAD is authorized until one tight integration repair+validation run on a real exact HEAD checkout. Do **not** repeat R25's evidence-only tests as if they qualified the new helper bytes, and do **not** create a new routine CI/Gate to compensate.

The production effective-v4.19 Task pin, READY/QUEUED publisher, accepted Claim/CAS and durable readback remain independently NOT_PROVEN. Full source/model semantic equivalence and full ADS rule denominator are still UNKNOWN/NOT_PROVEN.
