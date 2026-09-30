# Task Pack — T07 Unified Semantic Conformance

```yaml
task_id: T07
repository: kaicreator-mm/ai-development-standard
version: 4.7.0
integration_target: version/v4.7.0
merge_target: version/v4.7.0
dependencies: [T02, T03, T04, T05, T06]
allowed_write_set:
  - references/V47_SEMANTIC_CONFORMANCE_MATRIX.md
  - scripts/test_v47_semantic_conformance.py
  - scripts/v47_conformance.py
forbidden_scope:
  - new CONVERGENCE_PASS or global Gate state
  - owner semantics rewrite
  - Version Closure verdict
  - physical repository refactor
acceptance:
  - owner uniqueness and manifest-to-owner consistency are executable checks
  - Task Pack mutation authority is checked independently of registry/discovery metadata
  - qualified state forbidden-inferences are exercised across v4.1-v4.6
  - exact identity/currentness non-transfer is tested
  - profile/PROJECT_OVERRIDES and compatibility alias semantics are composed
  - historical payload/manifest compatibility remains explicit
adversarial_minimum:
  - CI success cannot substitute for required Validation/Review
  - registry presence cannot authorize mutation
  - same state token across dimensions cannot transfer meaning
  - old SHA evidence cannot transfer to successor
  - mock/static evidence cannot be promoted to higher-fidelity claim
required_gates:
  - integrated semantic tests
  - integration Validation
  - Fresh Independent Review
validation_owner: T07
review_policy: required
l3_requirement: docs/implementation/4.7.0/L3_REFERENCE_PACKS.md#t07--unified-semantic-conformance
agent_freedom: F1_BOUNDED_IMPLEMENTATION
jit_branch: true
risk: high
```

Failure handling: classify failures as owner ambiguity, mutation-authority defect, state/inference defect, compatibility defect or local implementation defect. Product/L2 contradiction routes to Planning Amendment; this task cannot silently redefine authority.
