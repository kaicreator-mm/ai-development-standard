# Task Pack — T07 Adoption & Cross-standard Wiring

```yaml
task_id: T07
repository: kaicreator-mm/ai-development-standard
version: 4.4.0
integration_target: version/v4.4.0
merge_target: version/v4.4.0
dependencies: [T02, T03, T04]
allowed_write_set:
  - standard-manifest.json
  - templates/project/.dev-standard/PROJECT_OVERRIDES.md
  - standards/PROJECT_ADOPTION.md
  - selected Validation/Release/checklist reference-only wiring
  - docs/implementation/4.4.0/MIGRATION_ADOPTION.md
  - templates/golden/STANDARD_COVERAGE.json
  - scripts/test_v44_adoption_wiring.py
forbidden_scope:
  - T01-T06 semantic redesign
  - new workflow/Gate/Release state machine
  - mandatory delivery stages for genuinely non-applicable projects
acceptance:
  - all v4.4 owners/contracts/references are discoverable
  - Golden coverage remains exact for active normative standards
  - project overrides can declare applicable build/package/distribution/deployment stages without weakening truth
  - existing Validation/Release/checklists reference owners rather than duplicate them
  - Fast Path/non-deployed projects are not forced to create fake delivery records
  - historical releases are not retrofitted with missing provenance/deployment truth
required_gates:
  - focused wiring regression
  - integration Validation
  - Fresh Independent Review
validation_owner: T07
review_policy: required
l3_requirement: docs/implementation/4.4.0/L3_REFERENCE_PACKS.md#t07--adoption--cross-standard-wiring
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: manifest/Golden/adoption inconsistency is repaired in T07 rather than waived. Any normative owner conflict routes back to the owning Task/authority; central wiring may not silently resolve it by rewriting semantics.
