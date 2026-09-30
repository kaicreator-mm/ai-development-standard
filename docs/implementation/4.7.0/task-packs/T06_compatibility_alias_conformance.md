# Task Pack — T06 Compatibility / Alias Conformance

```yaml
task_id: T06
repository: kaicreator-mm/ai-development-standard
version: 4.7.0
integration_target: version/v4.7.0
merge_target: version/v4.7.0
dependencies: [T02, T04]
allowed_write_set:
  - references/COMPATIBILITY_ALIAS_CONFORMANCE.md
  - scripts/test_v47_compatibility_aliases.py
forbidden_scope:
  - physical standards/reference path moves
  - compatibility entry deletion
  - duplicate normative owner creation
  - historical path meaning reinterpretation
acceptance:
  - every compatibility entry/alias resolves to one canonical target
  - alias cycles and broken targets fail closed
  - old stable paths may remain discoverable without duplicate normative ownership
  - manifest canonical owner metadata and compatibility entries agree
  - path migration remains evidence-driven and separately authorized
adversarial_minimum:
  - alias presence cannot make alias a normative owner
  - canonical registry target cannot silently delete old stable path
  - aesthetic cleanup cannot authorize breaking migration
  - broken alias cannot be ignored because canonical target exists elsewhere
required_gates:
  - focused compatibility tests
  - concern Validation
  - Fresh Independent Review
validation_owner: T06
review_policy: required
l3_requirement: docs/implementation/4.7.0/L3_REFERENCE_PACKS.md#t06--compatibility--alias-conformance
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: a needed physical move or alias retirement requires its own compatibility/migration authority. T06 records/validates routing only.
