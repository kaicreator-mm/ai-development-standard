# V410 Provenance Remediation — Local Command Inventory (R1)

Preparation unit: `V410-PROVENANCE-LOCAL-COMMAND-INVENTORY-R1`
Parent campaign: Issue #900 (v4.10 provenance remediation campaign)
Audit / adjudication inputs: #898 (`V410_EXECUTION_PACK_PROVENANCE_AUDIT=FINDINGS`), #899 (`V410_PROVENANCE_REMEDIATION_ADJUDICATION=PASS`)
Repository: `kaicreator-mm/ai-development-standard`
Version: `v4.10.0`
Preparation base SHA: `30334e8c7b90a327f8597b86c88c785b98df07f7` (= `origin/version/v4.10.0` tip at preparation time; HEAD verified equal at generation)
Branch: `task/v4.10.0-v410-provenance-local-command-inventory-r1`
Mode: `NO_SOURCE_CHANGE` preparation. Every command listed below is a checked-in deterministic concern-evidence command to be executed by the campaign on the final exact integration subject; nothing in this inventory is executed as campaign evidence by this preparation unit.

## Admission timing statement (per Issue #900)

Preparation MAY proceed now and has proceeded on base `30334e8c7b90a327f8597b86c88c785b98df07f7`. Campaign EXECUTION MUST wait until V410-T08A (Issue #864) is integrated and the implementation DAG is dependency-complete, and MUST then bind to that exact integration SHA/tree. At preparation time #864 is OPEN and NOT integrated; this inventory is therefore current-state input only and every per-leaf command entry must be re-verified for entrypoint existence on the final campaign subject before execution.

## Why these seven leaves are affected (from #898 / #899, preserved verbatim as findings)

Integrated #850/#851/#852/#853/#854/#855/#856 used Execution Packs whose core inventory was `TASK.md/CONTEXT.md/PLAN.md/COMMANDS.md/DOD.md/HANDOFF.md`, while the applicable Execution Pack Standard at claim time already required exactly `MANIFEST.yaml/EXECUTION_CONTRACT.md/TEST_MATRIX.yaml/FAILURE_MATRIX.yaml/IMPLEMENTATION_MAP.md/REVIEW_CHECKLIST.md` and classified incomplete core inventory `PACK_INVALID` / fail-closed. #854 additionally records its Builder claim as posted post-implementation. Historical semantic tests, exact-candidate Validation, Fresh Review and merge records remain historical facts; they do not retroactively repair execution provenance and do not transfer as remediation PASS.

## Campaign-level binding procedure (execute in this order, before any campaign execution)

1. Re-read the live integration SHA of `origin/version/v4.10.0` and confirm Issue #864 (V410-T08A) is integrated; record `EXACT_SUBJECT_SHA` and `EXACT_SUBJECT_TREE` (`git rev-parse HEAD` and `git rev-parse HEAD^{tree}` on the unchanged exact subject).
2. Confirm the implementation DAG (#848 freeze) is dependency-complete on that exact subject; any drift supersedes this inventory's base assumptions.
3. Create ONE canonical JIT Execution Pack for this coherent remediation concern with the current required six-artifact core inventory (`MANIFEST.yaml`, `EXECUTION_CONTRACT.md`, `TEST_MATRIX.yaml`, `FAILURE_MATRIX.yaml`, `IMPLEMENTATION_MAP.md`, `REVIEW_CHECKLIST.md`), exact-base binding to the T08A-integrated SHA and the current pinned `standards/EXECUTION_PACK_STANDARD.md`.
4. Publish/accept a serialized Builder/remediation claim BEFORE any campaign execution (claim-before-execution is mandatory; for #854 this is in addition to, not a repair of, its historical finding).
5. Re-verify every `python scripts/...` entrypoint listed below exists on the exact campaign subject tree; record any missing entrypoint as BLOCKED for that unit, not as permission to substitute.
6. Execute the seven per-leaf units on the exact subject; record per-unit result fields.

## Terminal gate checklist (from Issue #900)

- [ ] All seven units (#850-#856) report `PASS` on one stable exact SHA/tree.
- [ ] LOCAL Validator campaign dispatched on the same exact SHA/tree; it MAY batch commands but MUST return separate per-task concern verdict rows.
- [ ] Genuinely fresh independent WEB Reviewer campaign dispatched on the same exact SHA/tree; it MAY batch reading but MUST return separate per-task review verdict/findings and verify campaign provenance itself.
- [ ] Any subject drift supersedes affected campaign gate evidence (rebind or stop).
- [ ] Historical Validation/Review PASS treated as historical-only; `HISTORICAL_NONCONFORMANCE_PRESERVED=YES`.
- [ ] `SOURCE_MUTATION=NONE`; any material residual gap routed as a bounded repair to its owning concern, not repaired under this campaign.
- [ ] No Candidate Freeze / Release PASS claimed by this campaign; terminal block cleared only per #900 terminal block semantics.

## Per-leaf re-execution units

All commands run from repository root on the exact campaign subject tree. Every listed entrypoint exists and is deterministic at preparation base `30334e8c7b90a327f8597b86c88c785b98df07f7`.

---

### UNIT_850 — V410-T01A Stage-1 canonical lifecycle semantics

- Original task identity: Issue #850, `V410-T01A`, branch `task/v4.10.0-v410-t01a-stage1`, Execution Pack `.agent/execution/V410-T01A/` @ `c46bd637b35d04392d1cf797575bd0c31b38fac8` (legacy six-file inventory; PACK_INVALID per #898).
- Original acceptance summary: Stage-1 canonical lifecycle semantics on owner `standards/DEVELOPMENT_WORKFLOW.md`; keep policy-required-evidence guard explicit; pointer-only trigger contracts; schema conformance; fail closed on lifecycle drift.
- Historical execution provenance: Builder claim on the legacy pack; claim admission predated implementation but the pack itself was PACK_INVALID. Historical semantic result is preserved as fact, not authority.
- Current successor acceptance state: integrated via merge `df1ee51a0d6d1c30092c01102ca320db51091535` (PR #878) into `version/v4.10.0`; owner `standards/DEVELOPMENT_WORKFLOW.md` current at preparation tree. No conformant successor re-execution exists for this leaf; this campaign unit is its first conformant-provenance acceptance pass.
- Commands to re-establish current acceptance (exact lines):
  - `python scripts/test_v410_stage1_lifecycle_contracts.py` — expected: test suite PASS; locks Stage-1 lifecycle contracts and pointer-only trigger semantics against current owners.
  - `python scripts/test_protocol_schemas.py` — expected: schema conformance PASS.
- Result fields (fill at execution): subject_sha= | owner_currentness= | verdict=PASS|FAIL|BLOCKED | evidence_log=
- Notes: current successor acceptance = passing the checked-in T01A-focused suite plus protocol schema conformance on the exact subject. Historical acceptance (PR #878 merge) remains provenance-nonconformant; do not conflate.

### UNIT_851 — V410-T01B Product evidence/research/review planning projections

- Original task identity: Issue #851, `V410-T01B`, branch `task/v4.10.0-v410-t01b-product-projections`, Execution Pack `.agent/execution/V410-T01B/` @ `c6f7c63b62ec588d30d2da5d80097404bd7fe0cd` (legacy inventory; PACK_INVALID).
- Original acceptance summary: project Stage-1 Product evidence/research/review semantics into `prompts/L1_PRODUCT_EVIDENCE.md` and `templates/research-issue.md`; L1 != mandatory Product Research; Product Research proportional; Product-vs-Architecture Research distinct; Product Review risk/policy-selected; Product Review PASS != Product Freeze; no second Research lifecycle.
- Current successor acceptance state: integrated via merge `f1daaffb6ae3469dc0e77e881ed73e17e6586295` (PR #880); successor-focused script `scripts/test_v410_t01b_product_projections.py` checked in. No conformant re-execution exists; campaign unit is first conformant pass.
- Commands to re-establish current acceptance (exact lines):
  - `python scripts/test_v410_t01b_product_projections.py` — expected: PASS; locks the four Product projection invariants against `prompts/L1_PRODUCT_EVIDENCE.md` and `templates/research-issue.md`.
  - `python scripts/test_protocol_schemas.py` — expected: PASS.
- Result fields (fill at execution): subject_sha= | owner_currentness= | verdict=PASS|FAIL|BLOCKED | evidence_log=
- Notes: current successor acceptance is defined by the checked-in T01B projection suite on the exact subject, not by the PR #880 merge record.

### UNIT_852 — V410-T02A Human + Multi-Agent responsibility/control semantics

- Original task identity: Issue #852, `V410-T02A`, branch `task/v4.10.0-v410-t02a-collaboration-control`, Execution Pack `.agent/execution/V410-T02A/` @ `23779876db8e58d242d6399d2de35e7cbe72a221` (legacy inventory; PACK_INVALID).
- Original acceptance summary: Human + Multi-Agent responsibility/control semantics on owner `standards/EXECUTION_ARCHITECTURE_STANDARD.md`; collaboration-control clauses; no new event/state/lifecycle/registry family.
- Current successor acceptance state: integrated via merge `2276afe` (PR #879); successor-focused script `scripts/test_v410_t02a_collaboration_control.py` checked in. No conformant re-execution exists; campaign unit is first conformant pass.
- Commands to re-establish current acceptance (exact lines):
  - `python scripts/test_v410_t02a_collaboration_control.py` — expected: PASS; locks collaboration-control responsibility semantics on the current `EXECUTION_ARCHITECTURE_STANDARD.md`.
  - `python scripts/test_execution_architecture.py` — expected: PASS; existing architecture conformance suite.
  - `python scripts/test_protocol_schemas.py` — expected: PASS.
- Result fields (fill at execution): subject_sha= | owner_currentness= | verdict=PASS|FAIL|BLOCKED | evidence_log=
- Notes: current successor acceptance is the checked-in T02A-focused suite plus existing architecture/schema conformance on the exact subject; the PR #879 merge is historical-only for provenance.

### UNIT_853 — V410-T02B GitHub/event/machine projection for collaboration control (R2)

- Original task identity: Issue #853, `V410-T02B` R2, branch `task/v4.10.0-v410-t02b-machine-projection-r2`, Execution Pack `.agent/execution/V410-T02B-R2/` @ `8b535ae9d39aa5257c580ca06307c7953c7d282d` (legacy inventory even at R2 rebind; PACK_INVALID per #898).
- Original acceptance summary: reuse-first same-family optional machine projection (`parent_dispatch_ref` + `responsibility_mode`) on the existing dispatch/agent-event-v2 family; owners `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `schemas/dispatch.schema.json`, `schemas/agent-event-v2.schema.json`, `templates/agent-event-comment.md`; no new event/state/lifecycle/registry family.
- Current successor acceptance state: integrated via merge `fee097d` (PR #887); successor-focused script `scripts/test_v410_t02b_machine_projection.py` checked in. No conformant re-execution exists; campaign unit is first conformant pass.
- Commands to re-establish current acceptance (exact lines):
  - `python scripts/test_v410_t02b_machine_projection.py` — expected: PASS; positive/negative contract for the dispatch/event projection on current schemas.
  - `python scripts/test_protocol_schemas.py` — expected: PASS.
  - `python scripts/verify_event_writer_surfaces.py` — expected: PASS; event-writer surface verification.
- Result fields (fill at execution): subject_sha= | owner_currentness= | verdict=PASS|FAIL|BLOCKED | evidence_log=
- Notes: current successor acceptance is the checked-in T02B-focused suite on the exact subject; the R2 pack's rebind fixed currentness, not core-inventory conformance.

### UNIT_854 — V410-T03A Automation-first implementation quality

- Original task identity: Issue #854, `V410-T03A`, branch `task/v4.10.0-v410-t03a-implementation-quality`, Execution Pack `.agent/execution/V410-T03A/` @ `744a88bad4ac43d5df0f8c1ea27fc7348e53365b` (legacy inventory; PACK_INVALID).
- Original acceptance summary: automation-first implementation quality on owner `standards/IMPLEMENTATION_QUALITY_STANDARD.md`; quality gates enforced by executable evidence; fail closed on gate ambiguity.
- Current successor acceptance state: integrated via merge `46fe74936cd88184bbd898643851b585d3299291` (PR #876); successor-focused script `scripts/test_v410_t03a_implementation_quality.py` checked in. No conformant re-execution exists; campaign unit is first conformant pass.
- Commands to re-establish current acceptance (exact lines):
  - `python scripts/test_v410_t03a_implementation_quality.py` — expected: PASS; locks automation-first quality clauses on the current owner.
  - `python scripts/test_protocol_schemas.py` — expected: PASS.
- Result fields (fill at execution): subject_sha= | owner_currentness= | verdict=PASS|FAIL|BLOCKED | evidence_log=
- Notes: current successor acceptance is the checked-in T03A-focused suite on the exact subject; PR #876 merge is historical-only for provenance.

#### Historical finding retained for UNIT_854 (mandatory, per #899 / #900)

The historical record retains the independent adjudication finding that the T03A Builder **claim posted post-implementation** (claim-after-implementation defect, recorded in #899). This campaign MUST NOT rewrite, soften, or close that historical finding. The only thing this campaign proves for #854 is that the NEW campaign execution itself is claim-before-execution: the campaign-level serialized Builder/remediation claim must be durably published before the first campaign evidence execution, and UNIT_854's result fields must reference only this new campaign execution, never the historical PR #876 evidence. `HISTORICAL_NONCONFORMANCE_PRESERVED=YES` is required at campaign terminal.

### UNIT_855 — V410-T03B Agent-dispatchable Task decomposition and safe parallelism

- Original task identity: Issue #855, `V410-T03B`, branch `task/v4.10.0-v410-t03b-task-decomposition`, Execution Pack `.agent/execution/V410-T03B/` @ `bbb491ca8f952c159930cfb9bbadf1c2a9aa940b` (legacy inventory; PACK_INVALID).
- Original acceptance summary: agent-dispatchable Task decomposition and safe parallelism on owner `standards/TASK_DECOMPOSITION_STANDARD.md`; decomposition reference and conformance dogfood.
- Current successor acceptance state: integrated via merge `98ccd07ee18f3a8a8f10e91e04295324ebb130d8` (PR #875); successor-focused script `scripts/test_v43_task_decomposition.py` checked in. No conformant re-execution exists; campaign unit is first conformant pass.
- Commands to re-establish current acceptance (exact lines):
  - `python scripts/test_v43_task_decomposition.py` — expected: PASS; locks agent-dispatchable decomposition semantics on the current owner.
  - `python scripts/test_protocol_schemas.py` — expected: PASS.
- Result fields (fill at execution): subject_sha= | owner_currentness= | verdict=PASS|FAIL|BLOCKED | evidence_log=
- Notes: current successor acceptance is the checked-in decomposition suite on the exact subject; PR #875 merge is historical-only for provenance.

### UNIT_856 — V410-T04A Gate applicability and repair-routing convergence

- Original task identity: Issue #856, `V410-T04A`, branch `task/v4.10.0-v410-t04a-gate-repair-routing`, Execution Pack `.agent/execution/V410-T04A/` @ `b3031478a3a703180fec355983b4f6f2a97d862b` (legacy inventory; PACK_INVALID).
- Original acceptance summary: fail closed on ambiguous gate applicability; reject cost/docs-only/model-confidence/speed gate downgrades; route repair to root defect class; escalate non-converging repair without arbitrary universal retry cap; owners `standards/DEVELOPMENT_WORKFLOW.md` and `standards/VALIDATION_STANDARD.md`.
- Current successor acceptance state: integrated via merge `41236cb` (PR #884); successor-focused script `scripts/test_v410_t04a_gate_repair_routing.py` checked in. No conformant re-execution exists; campaign unit is first conformant pass.
- Commands to re-establish current acceptance (exact lines):
  - `python scripts/test_v410_t04a_gate_repair_routing.py` — expected: PASS; locks gate-applicability and repair-routing convergence clauses on current owners.
  - `python scripts/test_v34_review_repairs.py` — expected: PASS; existing review-repair regression suite.
  - `python scripts/test_protocol_schemas.py` — expected: PASS.
- Result fields (fill at execution): subject_sha= | owner_currentness= | verdict=PASS|FAIL|BLOCKED | evidence_log=
- Notes: current successor acceptance is the checked-in T04A-focused suite plus existing review-repair conformance on the exact subject; PR #884 merge is historical-only for provenance.

## Union of campaign execution commands (deterministic, checked-in at preparation base)

```text
python scripts/test_v410_stage1_lifecycle_contracts.py
python scripts/test_v410_t01b_product_projections.py
python scripts/test_v410_t02a_collaboration_control.py
python scripts/test_v410_t02b_machine_projection.py
python scripts/test_v410_t03a_implementation_quality.py
python scripts/test_v43_task_decomposition.py
python scripts/test_v410_t04a_gate_repair_routing.py
python scripts/test_execution_architecture.py
python scripts/test_v34_review_repairs.py
python scripts/verify_event_writer_surfaces.py
python scripts/test_protocol_schemas.py
```

Re-verify all eleven entrypoints on the exact campaign subject before execution. `NO_SOURCE_CHANGE` / `NO_CHANGE_REQUIRED` is legal only when actual current-state execution proves each unit acceptance; it is not a waiver.
