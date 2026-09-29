# Task Pack — T05 Build / Package Conformance & Dogfood

```yaml
task_id: T05
repository: kaicreator-mm/ai-development-standard
version: 4.4.0
integration_target: version/v4.4.0
merge_target: version/v4.4.0
dependencies: [T02]
allowed_write_set:
  - v4.4 build/package conformance fixtures and evidence
  - scripts/test_v44_build_package_conformance.py
  - docs/implementation/4.4.0/dogfood/build-package/**
forbidden_scope:
  - new normative delivery policy
  - provider-specific global mandates
  - Release/Deployment verdicts
acceptance:
  - at least one non-container package/install path is exercised or truthfully handed off
  - exact source/profile/toolchain/output binding is proven
  - package content-policy positives and leakage negatives are covered
  - promotion binds immutable artifact identity
  - rebuilt bytes cannot inherit old qualification
  - install/upgrade/package validation is executed when material
required_gates:
  - focused conformance tests
  - exact-subject Validation on required real tuple(s)
  - Fresh Independent Review
validation_owner: T05
review_policy: required
l3_requirement: docs/implementation/4.4.0/L3_REFERENCE_PACKS.md#t05--build--package-conformance--dogfood
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: if required platform/package tooling is unavailable, create a dedicated exact-SHA Validation Request with platform/toolchain/profile and cleanup scope. Static/simulated evidence only proves the dimensions it actually executes.
