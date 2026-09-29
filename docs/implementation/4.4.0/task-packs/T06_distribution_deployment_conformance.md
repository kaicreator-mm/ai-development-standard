# Task Pack — T06 Distribution / Deployment Conformance & Dogfood

```yaml
task_id: T06
repository: kaicreator-mm/ai-development-standard
version: 4.4.0
integration_target: version/v4.4.0
merge_target: version/v4.4.0
dependencies: [T03, T04]
allowed_write_set:
  - v4.4 distribution/deployment conformance fixtures and evidence
  - scripts/test_v44_distribution_deployment_conformance.py
  - docs/implementation/4.4.0/dogfood/distribution-deployment/**
forbidden_scope:
  - new normative policy
  - production side effects without explicit authority
  - migration/data recovery redefinition
acceptance:
  - container/service or equivalent deployed-service path is exercised when applicable
  - immutable digest/identity is distinct from alias/tag/channel
  - publication success does not imply deployment success
  - Deployment Plan and actual Result are exact-identity bound
  - partial/failure/rollback states are distinguishable
  - staging does not substitute for production
  - credential/tool capability does not imply side-effect authority
  - artifact rollback does not imply data migration rollback
required_gates:
  - focused conformance tests
  - exact-subject Validation for each required real external/environment tuple
  - Fresh Independent Review
validation_owner: T06
review_policy: required
l3_requirement: docs/implementation/4.4.0/L3_REFERENCE_PACKS.md#t06--distribution--deployment-conformance--dogfood
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: missing registry/runtime/target environment/access creates explicit Validation Request or BLOCKED/NOT_RUN evidence. Mock/sandbox evidence must be labeled to the fidelity it proves and cannot be promoted to unexecuted production truth.
