# Task Pack — T03 State-Dimension / Forbidden-Inference Registry

```yaml
task_id: T03
repository: kaicreator-mm/ai-development-standard
version: 4.7.0
integration_target: version/v4.7.0
merge_target: version/v4.7.0
dependencies: [T01]
allowed_write_set:
  - registries/state-dimensions-v1.json
  - references/STATE_DIMENSION_REGISTRY_REFERENCE.md
  - scripts/test_v47_state_dimension_registry.py
forbidden_scope:
  - live workflow/state mutation
  - global master enum
  - owner vocabulary redefinition
  - Validation/Review/Release/Deployment verdict issuance
acceptance:
  - current state dimensions are explicitly qualified by canonical owner
  - closed vs extensible vocabulary posture follows the owning contract
  - required forbidden cross-dimension inferences are machine-readable
  - equal-looking tokens across owners remain semantically separate
adversarial_minimum:
  - Task done cannot imply Validation PASS
  - Review PASS cannot imply Validation PASS
  - Validation PASS cannot imply Release READY
  - Release READY cannot imply Deployment SUCCESS
  - Deployment SUCCESS cannot imply Runtime Healthy
  - provider/tool AVAILABLE cannot imply mutation authority
  - old exact-SHA PASS cannot imply successor PASS
  - mock/sandbox PASS cannot imply real-environment PASS
required_gates:
  - focused semantic tests
  - concern Validation
  - Fresh Independent Review
validation_owner: T03
review_policy: required
l3_requirement: docs/implementation/4.7.0/L3_REFERENCE_PACKS.md#t03--state-dimension--forbidden-inference-registry
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: never invent or close a domain vocabulary merely to make registry data uniform. Unknown owner/vocabulary facts remain explicit and route to the source owner.
