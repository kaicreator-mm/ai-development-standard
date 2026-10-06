# V410-T06B LOCAL R1 Implementation Map

Exact baseline: `30334e8c7b90a327f8597b86c88c785b98df07f7` (= `origin/version/v4.10.0` tip).

Canonical semantic owners read from that exact tree (blob SHAs):
- `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` @ `266aefe32e0990c24fc8c1d6d731c4a3456fc3fc` (canonical compatibility authority)
- `standards/GOLDEN_TEMPLATE_STANDARD.md` @ `d7f73f107c9cbd72a89113419b2c3252670aadda` (golden template authority)
- `standards/EXECUTION_PACK_STANDARD.md` @ `c7bd2e4ffb87a0ac7fabc54fd78c4eb1fae6ef0d` (pack authority)
- `standards/CI_EVIDENCE_STANDARD.md` @ `35f387f257aac5505a1153abf7180dfd83daa556` (CI evidence authority)
- `schemas/execution-pack-manifest.schema.json` @ `ae2ced9c1a6115b9cfd3613a12d0a5889571e448`
- `templates/GOLDEN_INDEX.md` @ `b36d4947cfe7db101e9eb4955ea889b55d988ed1` (sole golden discovery index)
- `docs/implementation/4.10.0/TASK_PACKS_R1.md` @ `3300f8494ecb2120d96fff520cd09270b538344b`
- `scripts/verify_standard.py` @ `565cd024809b852ce155cd71396b0208b7acd0e6` (repository verifier entrypoint)

This unit's additive artifacts only:
- `.agent/execution/V410-T06B-LOCAL-BACKCOMPAT-FIXTURE-INVENTORY-R1/` (six core pack files + `BACKCOMPAT_FIXTURE_INVENTORY.md`)
- `scripts/test_v410_t06b_backcompat_fixture_inventory.py`

Implementation shape: read-only inspection of the exact tree; classify every backcompat/golden/conformance/contract fixture surface into `BACKCOMPAT_FIXTURE_INVENTORY.md` (Tables A/B/C + explicit silent-break flags in Table D); verify with the stdlib-only script (HEAD binding, fixture existence, producer entrypoint existence, kind counts).

## Gate repair (R1, post-generation)

The gate as first committed could not run: `check_head_binding()` referenced an undefined name `HEAD` while building the `git diff` argument, so the script aborted with `NameError` on its first check. The generation-time block below it ("HEAD binding: exact base …") was written before the pack commit, when `git rev-parse HEAD` still returned the pinned base; it cannot hold once this pack's own commit exists. Repaired in place: HEAD must now either equal the pinned base or descend from it with additive-only drift confined to this unit's allowed write set, which is the invariant this pack's `TEST_MATRIX.yaml` already declares (`head_binding_exact_or_additive_only_to_allowed_write_set`). Repository-relative path checks are also anchored to the repository root so the gate is CWD-independent.

Verified result on this pack branch (verbatim, `python scripts/test_v410_t06b_backcompat_fixture_inventory.py`, exit 0):

```text
HEAD binding: additive-only drift from base 30334e8c7b90a327f8597b86c88c785b98df07f7 to e060f11da186f70ee0834f831ca0542a2371e816 (allowed write set only, 8 paths)
fixture paths verified: 114/114
producer entrypoints verified: 76/76
kind_count[backcompat]=8
kind_count[golden]=23
kind_count[conformance]=27
kind_count[contract]=48
kind_count[TOTAL]=106
BACKCOMPAT_FIXTURE_INVENTORY_VERIFIED=PASS
```

Every substantive figure the generation-time block claimed (114/114 fixture paths, 76/76 producer entrypoints, all four kind counts, TOTAL=106) is reproduced by the repaired run; only the binding predicate was defective.

Central projection / machine-conformance wiring remains gated T06B implementation work, admission-gated on T06A. This pack is durable non-authoritative input to that unit.
