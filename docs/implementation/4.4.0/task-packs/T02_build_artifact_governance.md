# Task Pack — T02 Build & Artifact Governance

```yaml
task_id: T02
repository: kaicreator-mm/ai-development-standard
version: 4.4.0
integration_target: version/v4.4.0
merge_target: version/v4.4.0
dependencies: [T01]
allowed_write_set:
  - standards/BUILD_ARTIFACT_GOVERNANCE_STANDARD.md
  - references/BUILD_ARTIFACT_REFERENCE.md
  - scripts/test_v44_build_artifact.py
forbidden_scope:
  - v4.1 artifact-class redefinition
  - Release verdict ownership
  - provider-specific OCI/SLSA/package mandate
acceptance:
  - exact source/profile/toolchain/output identity
  - materially different build profiles produce distinct build identities
  - build output cannot self-promote into release/distribution artifact
  - immutable artifact identity is distinct from mutable name/tag/channel
  - rebuilt/new bytes cannot inherit prior artifact qualification
  - package content policy rejects secret/cache/runtime/Agent-only leakage by default
required_gates:
  - focused semantic tests
  - concern Validation
  - Fresh Independent Review
validation_owner: T02
review_policy: required
l3_requirement: docs/implementation/4.4.0/L3_REFERENCE_PACKS.md#t02--build--artifact-governance
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: product/package-specific requirements that cannot be generalized remain project/profile authority; never turn one provider format or reproducibility level into a global requirement without new authority.
