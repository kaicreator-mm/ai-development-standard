# V410-T06B LOCAL R1 Review Checklist

Fresh Independent Review must verify on one unchanged exact candidate:

- [ ] This Execution Pack has the exact canonical six core artifact names (MANIFEST.yaml, EXECUTION_CONTRACT.md, TEST_MATRIX.yaml, FAILURE_MATRIX.yaml, IMPLEMENTATION_MAP.md, REVIEW_CHECKLIST.md) plus the primary deliverable BACKCOMPAT_FIXTURE_INVENTORY.md, with valid exact-base (`30334e8c7b90a327f8597b86c88c785b98df07f7`), task, and branch binding.
- [ ] Builder claim (user dispatch of this LOCAL inventory unit against this exact pack/base) is recorded in EXECUTION_CONTRACT.md; any sequencing caveat is disclosed, not hidden.
- [ ] Allowed write set respected: only the pack directory and `scripts/test_v410_t06b_backcompat_fixture_inventory.py` were added; zero pre-existing files modified.
- [ ] Inventory Tables A/B/C cover: (A) all semantic-regression/backcompat/carryforward/contract/conformance suites, (B) every golden/fixture data file including `fixtures/`, `templates/golden/`, and dogfood fixture dirs, (C) machine/event/projection/schema surfaces including `schemas/`, `templates/execution-pack/`, `.agent/execution/`, and CI wiring.
- [ ] Table D explicitly flags the silent-break surfaces: legacy `ai-dev:event:v1` boundary, R3 carryforward invariants, v4.8 frozen sentinels + `fixtures/v48_contract_compatibility/cases.json`, replay golden scenarios, sole GOLDEN_INDEX, canonical compatibility authority, alias resolution, verifier freshness, T02B overlap, and predecessor-pack currentness.
- [ ] Verification script output is reproduced verbatim and shows PASS binding HEAD to the exact base (`30334e8c…` either exactly, or as its descendant with additive-only drift confined to this unit's allowed write set) with 114/114 fixture paths plus 76/76 producer entrypoints.
- [ ] Negative invariants hold: no fixture mutated by the inventory, no second registry/index created, no blanket migration, stale-passing-verifier class is inventoried as a risk rather than "fixed" here.
- [ ] T06B execution admission remains gated on T06A; this pack does not pre-empt or perform central wiring.
- [ ] Exact HEAD/tree and target currentness are re-read before any successor semantic mutation; predecessor pack evidence is not transferred as current authority.
- [ ] Concern Validation + Fresh Independent Review are both required for any successor candidate; Task/PR PASS is not Release PASS.
