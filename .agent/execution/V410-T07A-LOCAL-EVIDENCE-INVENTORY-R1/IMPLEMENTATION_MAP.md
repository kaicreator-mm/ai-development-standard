# V410-T07A-LOCAL-EVIDENCE-INVENTORY-R1 Implementation Map

## What was built

Additions only (no pre-existing file modified):

| File | Role |
|---|---|
| .agent/execution/V410-T07A-LOCAL-EVIDENCE-INVENTORY-R1/EXECUTION_CONTRACT.md | Claim recorded before any mutation; dependency/currentness state; allowed/forbidden scope |
| .agent/execution/V410-T07A-LOCAL-EVIDENCE-INVENTORY-R1/MANIFEST.yaml | Pack manifest with exact base SHA, integrated predecessor SHAs, PENDING-task note |
| .agent/execution/V410-T07A-LOCAL-EVIDENCE-INVENTORY-R1/EVIDENCE_INVENTORY.md | **Primary deliverable** — PRD §19 R1/R2/R3/R4/R6/R7/R11/R12 mapped to durable producers with CURRENT/PENDING currentness, §19.2 gates, §19.3 blockers, §19.4 honest state, Minimum/Advanced ADS paths, exact identity anchors |
| .agent/execution/V410-T07A-LOCAL-EVIDENCE-INVENTORY-R1/TEST_MATRIX.yaml | Suites + negative invariants |
| .agent/execution/V410-T07A-LOCAL-EVIDENCE-INVENTORY-R1/FAILURE_MATRIX.yaml | Failure classes incl. PASS_INFERRED_FROM_PRESENCE and PENDING_WITHOUT_OWNER |
| .agent/execution/V410-T07A-LOCAL-EVIDENCE-INVENTORY-R1/IMPLEMENTATION_MAP.md | This map |
| .agent/execution/V410-T07A-LOCAL-EVIDENCE-INVENTORY-R1/REVIEW_CHECKLIST.md | Fresh-review checklist |
| scripts/test_v410_t07a_evidence_inventory.py | Stdlib verification: HEAD bound to base (exact, or descendant with additive-only drift inside the write set), PRD §19 markers, CURRENT-path existence, PENDING owner concern |

## Design decisions

- **Row-level currentness.** Producers are marked CURRENT (exists at base SHA) or PENDING
  (owned by a not-yet-integrated task). CURRENT never means PASS; the inventory is a
  reconstructibility aid per the T07A pack purpose.
- **Every R-item keeps at least one PENDING producer** so release blockers stay visible:
  R1->T04B; R2->T06A; R3->T06B; R4->T08A/V01; R6->T04B/T05B; R7->T06B; R11->T06B/T08A;
  R12->T06A/T07B/V01.
- **No Release authority redefinition.** §19.3 blockers are rendered as visibility rows; the
  Release/Closure/RQ verdict stays with its existing owners (PENDING under T08A/V01).
- **Provenance first.** EXECUTION_CONTRACT.md (containing the serialized claim) was the first
  file written of this pack, before EVIDENCE_INVENTORY.md and before the script run.

## Verification record (verbatim)

Generation-time run: `python scripts/test_v410_t07a_evidence_inventory.py` (run from
worktree root, BEFORE the pack commit, while HEAD still equalled the pinned base SHA):

```text
CHECK head==base_sha: PASS (30334e8c7b90a327f8597b86c88c785b98df07f7)
CHECK prd_section_19_exists: PASS (5 markers)
CHECK inventory_rows: total=42 current=31 pending=11 paths_checked=30
EVIDENCE_INVENTORY_VERIFIED=PASS
```

### Gate repair (R1, post-generation)

Requiring `HEAD == base_sha` made the gate unrunnable at the pack's own committed
revision: the pack commit necessarily moves HEAD one commit above the pinned base, so a
Fresh Independent Review checking out this branch got FAIL and the PASS existed only via
an out-of-band base checkout. Repaired in place to the binding rule this campaign already
uses: HEAD must equal the pinned base, or descend from it with every changed path inside
this unit's additive write set (pack directory + this script). Because case 1b confines
every difference from base to that write set, every other path is byte-identical to the
base tree, so the CURRENT-path and PENDING-owner checks retain exactly the assurance they
had at base.

Repaired run on this pack branch (verbatim, exit 0):

```text
CHECK head_binding: PASS (descendant fa4c162fe79a2afc62a3a09f7a550201ec2f45fe; additive-only drift inside the allowed write set, 8 paths)
CHECK prd_section_19_exists: PASS (5 markers)
CHECK inventory_rows: total=42 current=31 pending=11 paths_checked=30
EVIDENCE_INVENTORY_VERIFIED=PASS
```

The inventory figures are unchanged from the generation-time run (`total=42 current=31
pending=11 paths_checked=30`), so no inventory claim depended on the check that was
repaired.

Relied-upon existing suites (sanity run at base SHA, all OK):

```text
test_v410_stage1_lifecycle_contracts: OK
test_v410_t01b_product_projections: OK
test_v410_t02a_collaboration_control: OK
test_v410_t02b_machine_projection: OK
test_v410_t03a_implementation_quality: OK
test_v410_t04a_gate_repair_routing: OK
test_v410_t05a_shared_code_safety: OK
```

Note: the base-SHA equality check quoted above is retained here as the historical
generation-time record only. The standing gate is the repaired binding rule described in
"Gate repair (R1, post-generation)", which passes at the pack's own committed revision and
still proves the inventory was derived on the pinned base.

## Known limitations

- No dedicated `test_v410_t03b` script exists at base SHA; R7 relies on the T03B merge
  semantics plus the pre-existing `scripts/test_v43_task_decomposition.py`. Recorded in the
  inventory, not treated as a defect.
- Review records (#833, #839, #847 etc.) are cited from the durable freeze docs; this unit
  did not re-fetch external review threads (no network per HARD RULES).
- End-to-end §19.1.4 (R4) falsification and Release-gate suites are intentionally PENDING
  under T08A/V01 and are not simulated.
