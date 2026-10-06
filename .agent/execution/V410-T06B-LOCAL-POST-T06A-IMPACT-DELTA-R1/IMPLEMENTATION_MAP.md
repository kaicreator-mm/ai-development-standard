# V410-T06B LOCAL-POST-T06A-IMPACT-DELTA-R1 implementation map

Read-only analysis unit. There is no implementation seam: the map below records *what was
inspected*, *what was executed*, and *what is handed to the T06B implementation unit*.

## 1. Surfaces inspected (exact bindings)

| Surface | Binding | Role in this analysis |
|---|---|---|
| PR #925 candidate | head `f294173c970d35cf9f9ce4eb4925339e324a801a`; merge `refs/pull/925/merge` @ `1b68c331`; base `eea3e69be5ac3e9c1a78f19e9bdf243ad9c58601` | Analysis subject (un-merged) |
| `scripts/test_v410_owner_convergence.py` | new in PR #925, 349 lines, 22 tests, `BASE_SHA=eea3e69…` (line 45), `MANIFEST_BLOB=21730a02…` (line 46) | Source of the C1–C6 collision set (§5) |
| `references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md` | new in PR #925, 103 lines, unregistered | Source of routes R2–R4 and contradictions X1–X3 |
| `scripts/test_v48_registry_adoption.py` | blob `55f78fd9b88bb0e4efd97790b9586beb78e06206` | `semantic_registry_problems` (508–532, count guard 530–531); `section_conformance_problems` (439–483, set guard 463–466, additions guard 479–482); `AUTHORIZED_SECTION_ADDITIONS` (101–126) |
| `scripts/verify_standard.py` | 251 lines | Adjudicates the R1-vs-R2 verifier dispute (§3.3) |
| `.agent/execution/V410-T06A-R1/TEST_MATRIX.yaml` | line 35 | The false prose enforcement claim routed to T06B (R4) |
| `.agent/execution/V410-T06A-R2/{MANIFEST,TEST_MATRIX,FAILURE_MATRIX,EXECUTION_CONTRACT}.yaml/.md` | — | Routing record R1, R5; corrected note (TEST_MATRIX:36); failure classes N7/N8 |
| `.agent/execution/V410-T06B-LOCAL-BACKCOMPAT-FIXTURE-INVENTORY-R1/BACKCOMPAT_FIXTURE_INVENTORY.md` | 149 lines, base `30334e8` | Delta target (D2–D4) |
| `scripts/test_v410_t06b_backcompat_fixture_inventory.py` | `BASE_SHA=30334e8…` (line 34), `check_head_binding()` (55–84, allow-list 77–78) | D6 |
| `standard-manifest.json` | blob `21730a0251e35e13591d2c84de1c66d6ab2c2408` at the subject | Growth-probe target; sections inventory (12 sections), `semantic_authorities.entries` = 11 |
| `.github/workflows/verify-standard.yml` | 26 explicit `run: python` steps | D7 |
| `scripts/test_v48_orchestration_dogfood.py` | `candidate_paths_between()` (151–166); ODF-11 method (969–1067), write-set assertion (1019–1054, assert at 1053) | D8 |

## 2. Executed verifications (all read-only or reverted)

| Probe | Location | Net effect |
|---|---|---|
| Baseline: verifier + all 77 suites + focused suite at `f294173` | detached scratch `succ` | none (read-only) |
| Registry-growth probe, routes A–D | scratch copy `scratch` (no VCS) | manifest restored each case; final guard run `OK` |
| Successor-collision probe, cases P1/E/F/G | detached scratch `succ` | `reset` + `checkout` + `clean` per case |
| Guard-evolution probe, cases H/I | detached scratch `succ` | same; final `git status --short` empty |
| Prior-inventory-script probe | `succ` at `f294173` + copied artifacts | artifacts removed; `git status --short` empty |

Cross-checked afterwards: no modification in `v410-t06a-owner-convergence` (owner of PR #925's
branch) or `v410-t06b-local-backcompat-fixture-inventory-r1`. No pre-existing file anywhere was
changed by this unit.

## 3. Handoff to the T06B implementation unit

This map does not prescribe implementation. It records the decision surface T06B owns:

1. **Disposition of C1–C6** (§5). Required, not optional: no T06B configuration keeps
   `scripts/test_v410_owner_convergence.py` green (best case H → 4 failures). C1 fails for every
   successor candidate unconditionally. Cheapest resolution window is *before* PR #925 merges.
2. **Guard evolution** (route R1/R2), guarded by contradictions X1/X2. Constructively proven
   feasible by case H: guard allow-list + manifest changed *together* → guard suite `OK`,
   verifier `PASS`.
3. **Seven GAP-family registrations** (route R3; case I shows the mechanical shape).
4. **False-prose disposition** (route R4 / acceptance a3): the R1 note at
   `V410-T06A-R1/TEST_MATRIX.yaml:35`, plus reference §3's `BLOCKED…` prose once the gap closes (X3).
5. **Rebind of the prior T06B inventory and its script** (D3, D4, D6) — the rebind failure is
   unavoidable, so it must be planned.
6. **Evidence form**: because CI cannot see any of this (D7), enforcement lives in T06B's own
   full-visible-set run + concern Validation + Independent Review. Measure on a **committed**
   tree: an uncommitted path reddens `test_v48_orchestration_dogfood.py` ODF-11 for reasons
   unrelated to the change (D8).

## 4. Explicit non-authority

This pack proposes, names, and evidences. It does **not** implement, repair, rebind, amend,
disposition, or verdict on any surface named above, and its "recommended shape" statements are
not authorizations. See FAILURE_MATRIX S3 (VERDICT_AUTHORITY) and S8
(SUCCESSOR_DEFECT_REPAIRED_IN_PLACE).
