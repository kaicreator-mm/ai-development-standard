# Task Pack — T08 Adoption & Cross-standard Wiring

```yaml
task_id: T08
repository: kaicreator-mm/ai-development-standard
version: 4.5.0
integration_target: version/v4.5.0
merge_target: version/v4.5.0
dependencies: [T02, T03, T04]
allowed_write_set:
  - standard-manifest.json
  - templates/project/.dev-standard/PROJECT_OVERRIDES.md
  - standards/PROJECT_ADOPTION.md
  - selected Testing/Test Data/Validation/Release/checklist reference-only wiring
  - docs/implementation/4.5.0/MIGRATION_ADOPTION.md
  - templates/golden/STANDARD_COVERAGE.json
  - scripts/test_v45_adoption_wiring.py
forbidden_scope:
  - T01-T07 semantic redesign
  - new global operations/lifecycle state machine
  - mandatory production observability/incident machinery for non-runtime projects
acceptance:
  - all v4.5 owners/contracts/references are discoverable
  - Golden coverage remains exact for active normative standards
  - project overrides can declare runtime/incident/maintenance applicability without weakening truth
  - existing Testing/Validation/Release owners are referenced rather than duplicated
  - libraries/non-runtime projects can truthfully mark runtime/incident capabilities NOT_APPLICABLE while retaining maintenance semantics if relevant
  - historical releases/incidents/support facts are not retrofitted
required_gates: [focused wiring regression, integration Validation, Fresh Independent Review]
validation_owner: T08
review_policy: required
l3_requirement: docs/implementation/4.5.0/L3_REFERENCE_PACKS.md#t08--adoption--cross-standard-wiring
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: manifest/Golden/adoption inconsistencies are repaired in T08, not waived. Normative owner conflicts route back to their owner; central wiring cannot settle them by duplicating or weakening semantics.
