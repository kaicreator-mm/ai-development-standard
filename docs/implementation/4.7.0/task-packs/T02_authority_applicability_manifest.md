# Task Pack — T02 Authority / Applicability Manifest Registry

```yaml
task_id: T02
repository: kaicreator-mm/ai-development-standard
version: 4.7.0
integration_target: version/v4.7.0
merge_target: version/v4.7.0
dependencies: [T01]
allowed_write_set:
  - standard-manifest.json
  - references/AUTHORITY_APPLICABILITY_REGISTRY_REFERENCE.md
  - scripts/test_v47_authority_registry.py
forbidden_scope:
  - duplicate canonical registry file
  - normative owner prose duplication
  - Task Pack/mutation authority grant
  - physical path migration
acceptance:
  - existing manifest sections remain backward-compatible
  - semantic entries resolve one canonical owner and applicable metadata
  - duplicate competing owners fail closed
  - optional/non-applicable tags do not create mandatory adoption
  - compatibility aliases route to owners without becoming owners
adversarial_minimum:
  - manifest entry cannot authorize file write/merge/side effect
  - registry presence cannot substitute for Frozen Product/L2/Task authority
  - broken/cyclic owner or alias target fails
  - file/discovery order cannot resolve material owner conflict
required_gates:
  - focused manifest/semantic tests
  - concern Validation
  - Fresh Independent Review
validation_owner: T02
review_policy: required
l3_requirement: docs/implementation/4.7.0/L3_REFERENCE_PACKS.md#t02--authority--applicability-manifest-registry
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: duplicate owner, broken target or materially ambiguous applicability is BLOCKED and routes to the owning planning authority; never silently choose by ordering.
