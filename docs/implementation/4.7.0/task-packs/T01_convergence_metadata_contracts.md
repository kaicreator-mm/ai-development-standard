# Task Pack — T01 Convergence Metadata Contracts

```yaml
task_id: T01
repository: kaicreator-mm/ai-development-standard
version: 4.7.0
integration_target: version/v4.7.0
merge_target: version/v4.7.0
dependencies: []
allowed_write_set:
  - schemas/authority-applicability-entry-v1.schema.json
  - schemas/state-dimension-registry-v1.schema.json
  - scripts/test_v47_convergence_metadata_contracts.py
forbidden_scope:
  - standard-manifest population
  - live state ownership or transitions
  - universal Subject/Authority/Context Snapshot objects
  - mutation/merge/side-effect/Validation/Release authorization
acceptance:
  - Authority/Applicability Entry requires semantic concern plus canonical owner ref and remains discovery metadata only
  - State-Dimension Registry binds dimension owner/vocabulary posture and forbidden source->target inference metadata
  - both contracts remain additive metadata families rather than lifecycle result objects
  - historical standard-manifest payload remains valid without v4.7 semantic metadata
  - no global PASS/READY/BLOCKED or master lifecycle enum is created
adversarial_minimum:
  - registry entry cannot grant Task Pack write authority
  - state metadata cannot issue live Validation/Review/Release/Deployment state
  - capability/provider availability cannot become authority
  - contract existence cannot force optional capability adoption
required_gates:
  - focused schema/semantic tests
  - concern Validation
  - Fresh Independent Review
validation_owner: T01
review_policy: required
l3_requirement: docs/implementation/4.7.0/L3_REFERENCE_PACKS.md#t01--convergence-metadata-contracts
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: any field that would duplicate owner prose, live state or mutation authority requires L2/planning amendment. Do not broaden T01 to manifest population or routing implementation.
