# Task Pack — T04 Reference Convention Standard

```yaml
task_id: T04
repository: kaicreator-mm/ai-development-standard
version: 4.7.0
integration_target: version/v4.7.0
merge_target: version/v4.7.0
dependencies: []
allowed_write_set:
  - standards/REFERENCE_CONVENTION_STANDARD.md
  - references/REFERENCE_CONVENTION_REFERENCE.md
  - scripts/test_v47_reference_conventions.py
forbidden_scope:
  - mandatory universal Subject Identity object
  - mandatory universal Authority object
  - historical schema rename/rewrite
  - exact-SHA/currentness semantic change
acceptance:
  - compatible reference meanings for exact/requested/tested/current SHA and expected base are explicit
  - mutable refs cannot replace exact subject identity when material
  - authority refs point to durable authority rather than capability
  - evidence/provenance refs never transfer PASS across subjects
  - existing owner-specific field names remain valid when semantically unambiguous
adversarial_minimum:
  - branch/tag alias cannot replace exact SHA when exact identity is required
  - credential/tool/provider ref cannot become authority ref
  - evidence ref cannot authorize mutation
  - naming normalization cannot rewrite historical payload meaning
required_gates:
  - focused semantic tests
  - concern Validation
  - Fresh Independent Review
validation_owner: T04
review_policy: required
l3_requirement: docs/implementation/4.7.0/L3_REFERENCE_PACKS.md#t04--reference-convention-standard
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: cosmetic inconsistency alone never authorizes a wire/schema migration. Incompatible normalization is recorded as future-major input.
