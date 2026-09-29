# Task Pack — T01 Shared Delivery Machine Contracts

```yaml
task_id: T01
repository: kaicreator-mm/ai-development-standard
version: 4.4.0
integration_target: version/v4.4.0
merge_target: version/v4.4.0
dependencies: []
allowed_write_set:
  - schemas/build-manifest-v1.schema.json
  - schemas/artifact-promotion-v1.schema.json
  - schemas/deployment-plan-v1.schema.json
  - schemas/deployment-result-v1.schema.json
  - narrowly justified optional references in existing evidence/release schemas
  - scripts/test_v44_delivery_contracts.py
forbidden_scope:
  - normative delivery policy
  - provider-specific build/distribution/deployment mandates
  - new workflow/Gate/Release state authority
acceptance:
  - repository-supported Draft 2020-12 schemas
  - build output and promoted artifact are distinct records
  - deployment plan and result are distinct records
  - immutable artifact identity is required where promotion claims exist
  - deployment outcomes are namespaced domain facts, not Validation/Release states
  - secret values are not ordinary durable fields
  - historical payloads remain valid when optional refs are absent
required_gates:
  - focused schema/semantic tests
  - concern Validation
  - Fresh Independent Review
validation_owner: T01
review_policy: required
l3_requirement: docs/implementation/4.4.0/L3_REFERENCE_PACKS.md#t01--shared-delivery-machine-contracts
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: unsupported schema keywords, historical compatibility regressions, or pressure to add lifecycle/provider authority fail closed and remain inside T01 repair; never weaken the repository schema verifier.
