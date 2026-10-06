# V410 Provenance Remediation — Local Command Inventory R1 Implementation Map

Exact baseline: `30334e8c7b90a327f8597b86c88c785b98df07f7` (HEAD verified at generation).

## Affected leaves and current integrated successors (read from the exact tree)

- #850 V410-T01A — integrated `df1ee51a0d6d1c30092c01102ca320db51091535` (PR #878); owner `standards/DEVELOPMENT_WORKFLOW.md`; focused evidence `scripts/test_v410_stage1_lifecycle_contracts.py`.
- #851 V410-T01B — integrated `f1daaffb6ae3469dc0e77e881ed73e17e6586295` (PR #880); owners `prompts/L1_PRODUCT_EVIDENCE.md`, `templates/research-issue.md`; focused evidence `scripts/test_v410_t01b_product_projections.py`.
- #852 V410-T02A — integrated `2276afe` (PR #879); owner `standards/EXECUTION_ARCHITECTURE_STANDARD.md`; focused evidence `scripts/test_v410_t02a_collaboration_control.py`.
- #853 V410-T02B R2 — integrated `fee097d` (PR #887); owners `standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`, `schemas/dispatch.schema.json`, `schemas/agent-event-v2.schema.json`, `templates/agent-event-comment.md`; focused evidence `scripts/test_v410_t02b_machine_projection.py`.
- #854 V410-T03A — integrated `46fe74936cd88184bbd898643851b585d3299291` (PR #876); owner `standards/IMPLEMENTATION_QUALITY_STANDARD.md`; focused evidence `scripts/test_v410_t03a_implementation_quality.py`; retains historical claim-posted-post-implementation finding.
- #855 V410-T03B — integrated `98ccd07ee18f3a8a8f10e91e04295324ebb130d8` (PR #875); owner `standards/TASK_DECOMPOSITION_STANDARD.md`; focused evidence `scripts/test_v43_task_decomposition.py`.
- #856 V410-T04A — integrated `41236cb` (PR #884); owners `standards/DEVELOPMENT_WORKFLOW.md`, `standards/VALIDATION_STANDARD.md`; focused evidence `scripts/test_v410_t04a_gate_repair_routing.py`.

Shared supporting evidence at baseline: `scripts/test_protocol_schemas.py`, `scripts/test_execution_architecture.py`, `scripts/test_v34_review_repairs.py`, `scripts/verify_event_writer_surfaces.py`.

## Execution Pack authority

- `standards/EXECUTION_PACK_STANDARD.md` @ `c7bd2e4ffb87a0ac7fabc54fd78c4eb1fae6ef0d`
- `schemas/execution-pack-manifest.schema.json` @ `ae2ced9c1a6115b9cfd3613a12d0a5889571e448`

## Preparation-unit artifacts

- `.agent/execution/V410-PROVENANCE-LOCAL-COMMAND-INVENTORY-R1/` (this pack; six core artifacts + `COMMAND_INVENTORY.md` primary deliverable)
- `scripts/test_v410_provenance_command_inventory.py` (preparation gate; PASS recorded at baseline)

## Gate repair (R1, post-generation)

The gate as first committed required `HEAD == preparation base`, which can only hold
before this pack's own commit lands; a reviewer checking out this branch got FAIL and the
recorded PASS existed only via an out-of-band base checkout. HEAD must now equal the
preparation base or descend from it with additive-only drift confined to this unit's
allowed write set (pack directory + this script). That case confines every difference from
base to the write set, so every command entrypoint checked by the gate is byte-identical to
the base tree and the check keeps its original assurance.

Repaired run on this pack branch (verbatim, exit 0), which also exercises the inventory
parser that the base-equality check had been masking:

```text
HEAD_SHA=30334e8c7b90a327f8597b86c88c785b98df07f7
HEAD_BINDING=descendant_additive_only
PARSED_COMMANDS=17
UNIT_SECTIONS=7
LEAVES_COVERED=850,851,852,853,854,855,856
COMMAND_INVENTORY_VERIFIED=PASS
```

All seven affected leaves are covered exactly once, all 17 inventoried command entrypoints
exist on this branch, and the #854 historical-finding retention checks pass.

## Conformance model

`.agent/execution/V410-T05A-R3/` (PR #902) is the conformant re-execution model mimicked by this pack's structure. Unlike T05A-R3, none of the seven affected leaves has a conformant successor; this campaign is each leaf's first conformant-provenance acceptance pass on the current integrated state.

## Campaign binding

Execution binds to the exact T08A-integrated SHA/tree after #864 integration; this baseline inventory is current-state preparation input only.
