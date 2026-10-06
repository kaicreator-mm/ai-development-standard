# V410-T06B Backward-Compatibility / Golden / Conformance Fixture Inventory

- Pack: `V410-T06B-LOCAL-BACKCOMPAT-FIXTURE-INVENTORY-R1`
- Task: `V410-T06B` (Central projection and machine conformance wiring) — preparation/inventory unit only.
- Exact base: `30334e8c7b90a327f8597b86c88c785b98df07f7` (= `origin/version/v4.10.0` tip).
- Scope: inventory only. No fixture, source, standard, schema, or template was mutated by this unit.
- Kind legend: `backcompat` = pins historical/legacy behavior that must keep working; `golden` = pins golden template/example/fixture data; `conformance` = machine-conformance projection of an owner standard; `contract` = pins a normative contract surface (authority/ownership/schema).

## A. Regression / backcompat / carryforward / conformance test suites (`scripts/test_*.py`)

All producer commands are relative to the repository root and were confirmed to exist at the base SHA.

| Fixture | Kind | Owning concern | Producer command | Pins-what | Projection-wiring risk note |
|---|---|---|---|---|---|
| scripts/test_v33_semantic_regressions.py | backcompat | V3.3 lifecycle semantics (T-003 lineage) | `python scripts/test_v33_semantic_regressions.py` | Legacy `ai-dev:event:v1` remains read-only historical compatibility evidence; new writers must not emit it | A central event/projection rewrite could break the transmogrify/legacy-reader split; treat as high-risk surface |
| scripts/test_v33_lifecycle_contracts.py | contract | V3.3 lifecycle governance | `python scripts/test_v33_lifecycle_contracts.py` | V3.3 lifecycle contract clauses | Prose→machine projection must not re-derive lifecycle authority |
| scripts/test_v34_lifecycle_contracts.py | contract | V3.4 lifecycle governance | `python scripts/test_v34_lifecycle_contracts.py` | V3.4 lifecycle contract clauses | Same as above for v3.4 lineage |
| scripts/test_v34_review_repairs.py | backcompat | V3.4 review repair fixes | `python scripts/test_v34_review_repairs.py` | Legacy non-dispatch report format remains compatible after review repairs | Projection renaming of report/event kinds could silently break legacy compatibility |
| scripts/test_v40_adoption_migration.py | conformance | V4.0 adoption/migration (A0/A1 levels) | `python scripts/test_v40_adoption_migration.py` | Adoption profiles, `A0_COMPATIBILITY` mode, migration examples in `templates/golden/V4_ADOPTION_MIGRATION_EXAMPLES.json` | Central wiring must not reclassify adoption levels or rewrite golden migration examples |
| scripts/test_v40_dogfood_hardening.py | conformance | V4.0 dogfood hardening | `python scripts/test_v40_dogfood_hardening.py` | Dogfood golden hardening examples (`V4_DOGFOOD_HARDENING_EXAMPLES.json`) | Golden example drift under projection is silent-failure prone |
| scripts/test_v40_final_hardening.py | conformance | V4.0 final hardening | `python scripts/test_v40_final_hardening.py` | Final-hardening golden examples | Same |
| scripts/test_v40_operation_contracts.py | conformance | V4.0 operation contracts | `python scripts/test_v40_operation_contracts.py` | Operation assurance golden examples (`V4_OPERATION_ASSURANCE_EXAMPLES.json`) | Same |
| scripts/test_v40_r2_machine_hardening.py | conformance | V4.0 R2 machine hardening | `python scripts/test_v40_r2_machine_hardening.py` | R2 machine hardening golden examples (`V4_R2_MACHINE_HARDENING_EXAMPLES.json`) | Machine-projection changes directly touch what this pins; high-risk |
| scripts/test_v40_r3_carryforward.py | backcompat (carryforward) | V4.0 R3 fresh-review carryforward | `python scripts/test_v40_r3_carryforward.py` | FIR1 provider-diverse basis enforcement, FIR2 hidden allow-list, FIR3 canonical facade fail-closed errors | Central wiring must not relax these carried-forward invariants; flag explicitly |
| scripts/test_v40_reference_flows.py | conformance | V4.0 reference flows | `python scripts/test_v40_reference_flows.py` | Golden reference flows (`V4_REFERENCE_FLOWS.json`) | Reference-flow golden file is projection input; drift risk |
| scripts/test_v40_t010_canonical_surface.py | contract | T-010 canonical surface | `python scripts/test_v40_t010_canonical_surface.py` | T-010 canonical surface identity | Projection must not create a second canonical surface |
| scripts/test_v40_t010_successor_hardening.py | contract | T-010 successor hardening | `python scripts/test_v40_t010_successor_hardening.py` | Successor/currentness binding for T-010 | Stale-passing-verifier override risk maps here |
| scripts/test_v40_t012_pre_release_hardening.py | contract | T-012 pre-release hardening | `python scripts/test_v40_t012_pre_release_hardening.py` | Pre-release evidence obligations | Release-wiring projection must not weaken these |
| scripts/test_v41_execution_foundation_conformance.py | conformance | V4.1 execution foundation | `python scripts/test_v41_execution_foundation_conformance.py` | Execution foundation conformance, golden examples `V41_EXECUTION_FOUNDATION_EXAMPLES.json` | Direct machine-conformance surface; central projection touches it |
| scripts/test_v41_execution_foundation_contracts.py | contract | V4.1 execution foundation | `python scripts/test_v41_execution_foundation_contracts.py` | Execution foundation contract clauses | — |
| scripts/test_v41_adoption_wiring.py | conformance | V4.1 adoption wiring | `python scripts/test_v41_adoption_wiring.py` | V4.1 adoption wiring conformance | — |
| scripts/test_v41_configuration_secrets.py | contract | V4.1 configuration/secrets | `python scripts/test_v41_configuration_secrets.py` | Configuration/secrets contract | — |
| scripts/test_v41_dependency_toolchain.py | contract | V4.1 dependency/toolchain | `python scripts/test_v41_dependency_toolchain.py` | Dependency/toolchain contract | — |
| scripts/test_v41_external_systems.py | contract | V4.1 external systems | `python scripts/test_v41_external_systems.py` | External-systems contract | — |
| scripts/test_v41_git_execution.py | contract | V4.1 git execution | `python scripts/test_v41_git_execution.py` | Git execution contract | — |
| scripts/test_v41_workspace_artifact.py | contract | V4.1 workspace/artifact | `python scripts/test_v41_workspace_artifact.py` | Workspace/artifact contract | — |
| scripts/test_v42_interface_compatibility.py | contract | Interface Compatibility Governance (canonical owner) | `python scripts/test_v42_interface_compatibility.py` | Canonical contract kind/identity, baseline/candidate identity, change operations; schema `schemas/compatibility-record-v1.schema.json` | THE compatibility authority. Any central wiring must project FROM this, never duplicate it; stale-passing-verifier override maps here |
| scripts/test_v42_api_compatibility_conformance.py | conformance | V4.2 API compatibility | `python scripts/test_v42_api_compatibility_conformance.py` | API-level compatibility conformance | — |
| scripts/test_v42_cross_standard_conformance.py | conformance | V4.2 cross-standard wiring | `python scripts/test_v42_cross_standard_conformance.py` | Cross-standard conformance enumerates `test_v42_interface_compatibility.py` etc. as canonical producers | Central wiring must keep this producer enumeration truthful |
| scripts/test_v42_data_migration.py | conformance | V4.2 data migration | `python scripts/test_v42_data_migration.py` | Data-migration conformance | — |
| scripts/test_v42_migration_conformance.py | conformance | V4.2 migration runtime | `python scripts/test_v42_migration_conformance.py` | SQLite runtime identity bound, transition preserves data, rollback/recovery, fixture subjects not collapsed | Fixture-subject non-collapse is exactly the "do not collapse fixtures" invariant |
| scripts/test_v42_evolution_contracts.py | contract | V4.2 evolution | `python scripts/test_v42_evolution_contracts.py` | Evolution contract clauses | — |
| scripts/test_v42_adoption_wiring.py | conformance | V4.2 adoption wiring | `python scripts/test_v42_adoption_wiring.py` | V4.2 adoption wiring conformance | — |
| scripts/test_v43_task_decomposition.py | contract | Task Decomposition (canonical owner) | `python scripts/test_v43_task_decomposition.py` | Task decomposition governance contract | Canonical owner; projection must not absorb decomposition authority |
| scripts/test_v43_archetype_profiles.py | contract | V4.3 archetype profiles | `python scripts/test_v43_archetype_profiles.py` | Archetype profile contract | — |
| scripts/test_v43_architecture_design.py | contract | V4.3 architecture design | `python scripts/test_v43_architecture_design.py` | Architecture design contract | — |
| scripts/test_v43_conformance_dogfood.py | conformance | V4.3 conformance dogfood | `python scripts/test_v43_conformance_dogfood.py` | Conformance dogfood fixtures (`docs/implementation/4.3.0/dogfood/fixtures/`) | Dogfood fixture paths are pinned; projection moves could orphan them |
| scripts/test_v43_dag_mutation_contract.py | contract | V4.3 DAG mutation | `python scripts/test_v43_dag_mutation_contract.py` | DAG mutation contract | — |
| scripts/test_v43_go_java_rust_profiles.py | contract | V4.3 language profiles | `python scripts/test_v43_go_java_rust_profiles.py` | Go/Java/Rust profile contract | — |
| scripts/test_v43_ts_python_profiles.py | contract | V4.3 language profiles | `python scripts/test_v43_ts_python_profiles.py` | TS/Python profile contract | — |
| scripts/test_v43_profile_framework.py | contract | V4.3 profile framework | `python scripts/test_v43_profile_framework.py` | Profile framework contract | — |
| scripts/test_v43_implementation_quality.py | contract | V4.3 implementation quality | `python scripts/test_v43_implementation_quality.py` | Implementation quality contract (pre-v4.10 owner) | Overlaps T03A v4.10 successor; wiring must not double-own |
| scripts/test_v43_task_dag_governance.py | contract | V4.3 task DAG governance | `python scripts/test_v43_task_dag_governance.py` | Task DAG governance contract | — |
| scripts/test_v47_authority_registry.py | contract | V4.7 authority registry | `python scripts/test_v47_authority_registry.py` | Authority registry content | Central projection reads this; do not duplicate registry |
| scripts/test_v47_compatibility_aliases.py | backcompat | V4.7 compatibility aliases | `python scripts/test_v47_compatibility_aliases.py` | Renamed-but-valid compatibility aliases keep resolving | Projection renames could break alias resolution; flag |
| scripts/test_v47_convergence_metadata_contracts.py | contract | V4.7 convergence metadata | `python scripts/test_v47_convergence_metadata_contracts.py` | Convergence metadata contract | — |
| scripts/test_v47_progressive_disclosure.py | contract | V4.7 progressive disclosure | `python scripts/test_v47_progressive_disclosure.py` | Progressive disclosure contract | — |
| scripts/test_v47_reference_conventions.py | contract | V4.7 reference conventions | `python scripts/test_v47_reference_conventions.py` | Reference conventions contract | — |
| scripts/test_v47_state_dimension_registry.py | contract | V4.7 state dimension registry | `python scripts/test_v47_state_dimension_registry.py` | State dimension registry (schema `state-dimension-registry-v1.schema.json`) | Second-registry prohibition maps here |
| scripts/test_v48_contract_compatibility.py | backcompat | V4.8 contract compatibility | `python scripts/test_v48_contract_compatibility.py` | Three v4.8 contract families, stale-exact-subject records stay historical, historical v4 interchange payload remains valid, frozen v4 migration sentinels; data: `fixtures/v48_contract_compatibility/cases.json` | Highest-density backcompat pins; any schema/central change must re-run this; sentinel breakage is silent otherwise |
| scripts/test_v48_interchange_replay_restart.py | backcompat (golden) | V4.8 interchange replay/restart | `python scripts/test_v48_interchange_replay_restart.py` | Replay/restart semantics pinned by 6 golden scenario fixtures under `fixtures/v48_interchange_replay/` | Golden JSON scenarios are projection input; do not relocate or rewrite |
| scripts/test_v48_interchange_profile.py | contract | V4.8 interchange profile | `python scripts/test_v48_interchange_profile.py` | Interchange profile contract (also reads `fixtures/v48_interchange_replay/`) | — |
| scripts/test_v48_agent_capability_profile.py | contract | V4.8 agent capability profile | `python scripts/test_v48_agent_capability_profile.py` | Capability profile contract | — |
| scripts/test_v48_agent_capability_evidence.py | contract | V4.8 agent capability evidence | `python scripts/test_v48_agent_capability_evidence.py` | Capability-evidence contract (claim != proof) | — |
| scripts/test_v48_execution_architecture.py | contract | V4.8 execution architecture | `python scripts/test_v48_execution_architecture.py` | Execution architecture contract | — |
| scripts/test_v48_execution_ownership.py | contract | V4.8 execution ownership | `python scripts/test_v48_execution_ownership.py` | Execution ownership contract | — |
| scripts/test_v48_governance_conformance.py | conformance | V4.8 governance | `python scripts/test_v48_governance_conformance.py` | Governance conformance | — |
| scripts/test_v48_integration_closure.py | conformance | V4.8 integration closure | `python scripts/test_v48_integration_closure.py` | Integration closure conformance | — |
| scripts/test_v48_orchestration_dogfood.py | conformance | V4.8 orchestration dogfood | `python scripts/test_v48_orchestration_dogfood.py` | Orchestration dogfood fixtures (`docs/implementation/4.8.0/dogfood/orchestration/fixtures/`) | Fixture paths pinned |
| scripts/test_v48_registry_adoption.py | conformance | V4.8 registry adoption | `python scripts/test_v48_registry_adoption.py` | Registry adoption conformance; carryforward of prior-version invariants | Second-registry prohibition maps here |
| scripts/test_v48_scheduling_conformance.py | conformance | V4.8 scheduling | `python scripts/test_v48_scheduling_conformance.py` | Scheduling conformance | — |
| scripts/test_v48_task_learning.py | contract | V4.8 task learning | `python scripts/test_v48_task_learning.py` | Task learning contract (bounded rationale, no private CoT) | — |
| scripts/test_v48_ads_evolution_governance.py | contract | V4.8 ADS evolution governance | `python scripts/test_v48_ads_evolution_governance.py` | ADS evolution governance contract | — |
| scripts/test_protocol_schemas.py | contract | Event/protocol schemas | `python scripts/test_protocol_schemas.py` | Machine-readable event protocol schema surface | Direct projection surface; schema drift breaks protocol compat |
| scripts/test_verify_standard.py | golden | Repository verifier | `python scripts/test_verify_standard.py` | `verify_standard.py` behavior: golden example file existence, interface-compat owner repair routing, `templates/golden/V41_EXECUTION_FOUNDATION_EXAMPLES.json` presence | This suite detects stale-passing-verifier style drift; central wiring must keep it green |
| scripts/test_work_item_contract_and_golden_templates.py | golden | Work item contract + golden templates | `python scripts/test_work_item_contract_and_golden_templates.py` | `templates/GOLDEN_INDEX.md` required surface set, per-row golden linkage, no duplicate surfaces | GOLDEN_INDEX is the golden discovery surface; a second index/registry is forbidden |
| scripts/test_execution_architecture.py | contract | Execution architecture | `python scripts/test_execution_architecture.py` | Execution architecture contract | — |
| scripts/test_pointer_only_trigger_contract.py | contract | Pointer-only trigger | `python scripts/test_pointer_only_trigger_contract.py` | Pointer-only trigger contract | — |
| scripts/test_project_execution_profile.py | contract | Project execution profile | `python scripts/test_project_execution_profile.py` | Project execution profile contract | — |
| scripts/test_task_dag_lane_parallelism.py | contract | Task DAG lanes | `python scripts/test_task_dag_lane_parallelism.py` | Task DAG lane/parallelism contract | — |
| scripts/test_verify_project_standard.py | conformance | Project-standard verification | `python scripts/test_verify_project_standard.py` | Project-standard verification conformance | — |
| scripts/test_v410_stage1_lifecycle_contracts.py | backcompat (carryforward) | V410-T01A Stage-1 lifecycle | `python scripts/test_v410_stage1_lifecycle_contracts.py` | v4.10 Stage-1 lifecycle regression pins (evidence vs authority, no new state machine, fail-closed) | Predecessor pins that T06B projection must not regress |
| scripts/test_v410_t01b_product_projections.py | conformance | V410-T01B product projections | `python scripts/test_v410_t01b_product_projections.py` | Product evidence/research/review projections conformance | Direct predecessor projection surface |
| scripts/test_v410_t02a_collaboration_control.py | conformance | V410-T02A collaboration control | `python scripts/test_v410_t02a_collaboration_control.py` | Human + multi-agent responsibility/control semantics | Direct predecessor projection surface |
| scripts/test_v410_t02b_machine_projection.py | conformance | V410-T02B machine projection | `python scripts/test_v410_t02b_machine_projection.py` | GitHub/event/machine projection for collaboration control | Nearest-neighbor to T06B central wiring; highest overlap risk |
| scripts/test_v410_t03a_implementation_quality.py | conformance | V410-T03A implementation quality | `python scripts/test_v410_t03a_implementation_quality.py` | Automation-first implementation quality conformance | — |
| scripts/test_v410_t04a_gate_repair_routing.py | conformance | V410-T04A gate repair routing | `python scripts/test_v410_t04a_gate_repair_routing.py` | Gate applicability from shared authority chain, no preference/discovery-order adjudication, fail-closed | Gate-wiring projection must not introduce ordering adjudication |
| scripts/test_v410_t05a_shared_code_safety.py | conformance | V410-T05A R3 shared-code safety | `python scripts/test_v410_t05a_shared_code_safety.py` | Shared-code/reuse safety under existing owners | Guards against central wiring becoming a de-facto new owner |

## B. Golden / fixture data files

| Fixture | Kind | Owning concern | Producer command | Pins-what | Projection-wiring risk note |
|---|---|---|---|---|---|
| fixtures/v48_contract_compatibility/cases.json | golden (backcompat cases) | V4.8 contract compatibility | `python scripts/test_v48_contract_compatibility.py` | Concrete backcompat case records incl. stale-exact-subject negatives | Silent-break risk: suite still passes if file relocated only if path constant updated; never rewrite case semantics |
| fixtures/v48_interchange_replay/ack_progress_non_authority.json | golden | V4.8 interchange replay | `python scripts/test_v48_interchange_replay_restart.py` | Ack-progress non-authority replay scenario | Relocation/relabel breaks replay semantics invisibly |
| fixtures/v48_interchange_replay/conflicting_payload_digest.json | golden | V4.8 interchange replay | `python scripts/test_v48_interchange_replay_restart.py` | Conflicting digest replay scenario | Same |
| fixtures/v48_interchange_replay/lost_replayed_delivery.json | golden | V4.8 interchange replay | `python scripts/test_v48_interchange_replay_restart.py` | Lost replayed delivery scenario | Same |
| fixtures/v48_interchange_replay/restart_durable_reconstruction.json | golden | V4.8 interchange replay | `python scripts/test_v48_interchange_replay_restart.py` | Restart durable reconstruction scenario | Same |
| fixtures/v48_interchange_replay/same_identity_payload.json | golden | V4.8 interchange replay | `python scripts/test_v48_interchange_replay_restart.py` | Same-identity payload scenario | Same |
| fixtures/v48_interchange_replay/stale_subject_request.json | golden | V4.8 interchange replay | `python scripts/test_v48_interchange_replay_restart.py` | Stale subject request scenario | Same |
| docs/implementation/4.3.0/dogfood/fixtures/planner_bounded_executor.json | golden | V4.3 conformance dogfood | `python scripts/test_v43_conformance_dogfood.py` | Planner bounded-executor dogfood scenario | Path pinned by suite; do not move |
| docs/implementation/4.3.0/dogfood/fixtures/shortcut_negative_matrix.json | golden | V4.3 conformance dogfood | `python scripts/test_v43_conformance_dogfood.py` | Shortcut negative matrix scenario | Same |
| docs/implementation/4.8.0/dogfood/orchestration/fixtures/scenario_manifest.json | golden | V4.8 orchestration dogfood | `python scripts/test_v48_orchestration_dogfood.py` | Orchestration scenario manifest | Same |
| docs/implementation/4.8.0/dogfood/orchestration/fixtures/t011_builder_claim_event.json | golden | V4.8 orchestration dogfood | `python scripts/test_v48_orchestration_dogfood.py` | T-011 builder-claim event fixture | Same |
| templates/golden/ANTI_PATTERNS.md | golden | GOLDEN_TEMPLATE_STANDARD | `python scripts/test_work_item_contract_and_golden_templates.py` | Anti-pattern golden guidance | Text drift under projection weakens standard examples |
| templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md | golden | GOLDEN_TEMPLATE_STANDARD | `python scripts/test_work_item_contract_and_golden_templates.py` | Standard conformance examples | Same |
| templates/golden/STANDARD_COVERAGE.json | golden | GOLDEN_TEMPLATE_STANDARD | `python scripts/test_work_item_contract_and_golden_templates.py` | Standard coverage golden data | Same |
| templates/golden/V41_EXECUTION_FOUNDATION_EXAMPLES.json | golden | V4.1 execution foundation | `python scripts/test_verify_standard.py`, `python scripts/test_v41_execution_foundation_conformance.py` | Execution foundation golden examples; existence asserted by verifier regression | Dual-consumer file; deleting/renaming breaks two suites |
| templates/golden/V4_ADOPTION_MIGRATION_EXAMPLES.json | golden | V4.0 adoption migration | `python scripts/test_v40_adoption_migration.py` | Adoption/migration golden examples | — |
| templates/golden/V4_DOGFOOD_HARDENING_EXAMPLES.json | golden | V4.0 dogfood hardening | `python scripts/test_v40_dogfood_hardening.py` | Dogfood hardening golden examples | — |
| templates/golden/V4_OPERATION_ASSURANCE_EXAMPLES.json | golden | V4.0 operation contracts | `python scripts/test_v40_operation_contracts.py` | Operation assurance golden examples | — |
| templates/golden/V4_R2_MACHINE_HARDENING_EXAMPLES.json | golden | V4.0 R2 machine hardening | `python scripts/test_v40_r2_machine_hardening.py` | R2 machine-hardening golden examples | — |
| templates/golden/V4_REFERENCE_FLOWS.json | golden | V4.0 reference flows | `python scripts/test_v40_reference_flows.py` | Reference flows golden data | — |
| templates/GOLDEN_INDEX.md | golden (discovery index) | GOLDEN_TEMPLATE_STANDARD | `python scripts/test_work_item_contract_and_golden_templates.py` | Required surface set + per-surface golden linkage | Sole golden discovery index; a second index/registry is explicitly forbidden for T06B |

## C. Machine / event / projection / schema surfaces

| Fixture | Kind | Owning concern | Producer command | Pins-what | Projection-wiring risk note |
|---|---|---|---|---|---|
| schemas/compatibility-record-v1.schema.json | contract | Interface Compatibility Governance | `python scripts/test_v42_interface_compatibility.py` | Compatibility record schema (required fields) | Canonical compatibility schema; T06B must project from it, never fork it |
| schemas/agent-event-v2.schema.json | contract | Event protocol | `python scripts/test_protocol_schemas.py` | Current event envelope schema (v2) | Legacy v1 transmogrify boundary depends on this staying v2 |
| schemas/state-dimension-registry-v1.schema.json | contract | V4.7 state dimension registry | `python scripts/test_v47_state_dimension_registry.py` | State dimension registry schema | Second-registry prohibition anchor |
| schemas/execution-pack-manifest.schema.json | contract | EXECUTION_PACK_STANDARD | `python scripts/test_v48_registry_adoption.py` (among v34/v41/v48 suite references); `python scripts/verify_standard.py` | Execution-pack manifest schema | T06B/T06A pack projection consumes it; schema edits ripple to all packs |
| templates/execution-pack/ (MANIFEST.yaml.md, EXECUTION_CONTRACT.md, TEST_MATRIX.yaml.md, FAILURE_MATRIX.yaml.md, IMPLEMENTATION_MAP.md, REVIEW_CHECKLIST.md, README.md) | contract (templates) | EXECUTION_PACK_STANDARD | concern Validation | Canonical execution-pack file templates | T06B projection/template wiring must render exactly these six names |
| templates/agent-event-comment.md | contract (template) | GITHUB_AGENT_INTERACTION_PROTOCOL | `python scripts/test_v410_t02b_machine_projection.py` | Agent event comment template (pinned via `TEMPLATE` constant) | Event projection renames could desync template from schema |
| .agent/execution/V410-T01A .. V410-T05A-R3 (predecessor packs) | conformance (durable evidence) | v4.10 predecessor tasks | pack Validation | Durable execution evidence of settled owners | Historical evidence; must not be silently re-bound as current authority (currentness invariant) |
| .agent/execution/_legacy | backcompat | legacy task packs | none (historical) | Legacy pack lineage | Read-only history; do not migrate wholesale (no blanket touch-every-file migration) |
| scripts/verify_standard.py | contract (verifier) | Repository verifier | `python scripts/verify_standard.py` | Standard verification entrypoint used by CI (`.github/workflows/verify-standard.yml`) | Stale-passing-verifier cannot override current authority: this is the verifier whose freshness T06B must preserve |
| scripts/resolve_standard_read_set.py | contract | Standard read-set resolution | `python scripts/resolve_standard_read_set.py` | Read-set resolution used by verification | Projection wiring feeding wrong read-sets breaks verifier freshness |
| .github/workflows/verify-standard.yml | contract (CI wiring) | CI evidence | CI run | Invokes `verify_standard.py`, `test_verify_standard.py`, `test_v33_*` | Central conformance wiring lands here; keep producer list truthful |

## D. Surfaces a central wiring change could silently break (explicit flags)

1. `scripts/test_v33_semantic_regressions.py` — legacy `ai-dev:event:v1` read-only evidence boundary: an event projection rewrite could make legacy history unreadable without failing loudly.
2. `scripts/test_v40_r3_carryforward.py` — carried-forward FIR1/FIR2/FIR3 invariants: a central wiring pass could relax them while other suites still pass.
3. `scripts/test_v48_contract_compatibility.py` + `fixtures/v48_contract_compatibility/cases.json` — frozen v4 migration sentinels and historical-payload validity: highest silent-break density.
4. `fixtures/v48_interchange_replay/*.json` — golden replay scenarios consumed by path constants in two suites; relocation silently orphans them only if suites are updated in step (which would mask the break).
5. `templates/GOLDEN_INDEX.md` + `scripts/test_work_item_contract_and_golden_templates.py` — sole golden discovery index; T06B must not create a parallel index.
6. `scripts/test_v42_interface_compatibility.py` + `schemas/compatibility-record-v1.schema.json` — canonical compatibility authority; duplication here equals the forbidden "second registry".
7. `scripts/test_v47_compatibility_aliases.py` — alias resolution: renaming during projection breaks old aliases quietly.
8. `scripts/test_verify_standard.py` + `scripts/verify_standard.py` — verifier freshness: a stale verifier passing against projected surfaces is the exact failure class named in TASK_PACKS §V410-T06B acceptance.
9. `scripts/test_v410_t02b_machine_projection.py` — nearest-neighbor projection suite; T06B wiring overlapping T02B-owned surfaces risks double ownership.
10. `.agent/execution/` predecessor packs — currentness invariant: historical qualification must not silently bind to the T06B successor.

## E. Notes

- Suites under `scripts/test_v41_*` / `test_v43_*` / `test_v48_*` not individually listed as backcompat are contract/conformance fixtures of their version owners; they are listed in Table A for completeness because central conformance wiring runs them as gate inputs.
- No `backcompat`-named files exist in the tree; backcompat coverage lives inside the semantic-regression, carryforward, and compatibility suites inventoried above.
- All paths and producer entrypoints were verified to exist at base `30334e8c7b90a327f8597b86c88c785b98df07f7` by `scripts/test_v410_t06b_backcompat_fixture_inventory.py`.
