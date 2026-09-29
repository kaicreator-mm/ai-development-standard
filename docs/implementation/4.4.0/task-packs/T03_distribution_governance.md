# Task Pack — T03 Distribution Governance

```yaml
task_id: T03
repository: kaicreator-mm/ai-development-standard
version: 4.4.0
integration_target: version/v4.4.0
merge_target: version/v4.4.0
dependencies: [T01]
allowed_write_set:
  - standards/DISTRIBUTION_GOVERNANCE_STANDARD.md
  - references/DISTRIBUTION_REFERENCE.md
  - scripts/test_v44_distribution.py
forbidden_scope:
  - mandatory distribution for every product
  - canonical artifact identity ownership
  - Deployment result ownership
  - mandatory standalone distribution schema
acceptance:
  - mutable alias/tag/channel is not canonical immutable bytes identity
  - publication binds immutable artifact identity where supported
  - repointed/replaced alias cannot inherit prior qualification
  - publication success does not imply Deployment success
  - distribution can be truthfully NOT_APPLICABLE
required_gates:
  - focused semantic tests
  - concern Validation
  - Fresh Independent Review
validation_owner: T03
review_policy: required
l3_requirement: docs/implementation/4.4.0/L3_REFERENCE_PACKS.md#t03--distribution-governance
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: medium-high
```

Failure handling: if a publication system lacks immutable binding, record the limitation and required alternative evidence; mutable locator alone can never become proof of artifact bytes.
